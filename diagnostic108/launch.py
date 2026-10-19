"""Trusted host candidate108. No private ingress and no downloaded imports."""
import argparse, base64, errno, hashlib, json, os, pathlib, re, selectors, stat, subprocess, sys, time, uuid, importlib.util
_QUAL113 = None
_HOST113 = None
_COUNTER115_RESULT = None
_COUNTER115_RELEASED = False
_COUNTER115_NAMES = frozenset(('counter.stdout','counter.stderr','counter.terminal.json','counter115.intent.json','counter115.ready','counter115.verified.json','beforecounter115.json','aftercounter115.json','counter116.inputs.json','counter116.read-custody.json'))

MODE = 'PUBLIC_INPUTS_ONLY_PRECOUNTER_DIAGNOSTIC'
CAP = 65536
TOTAL = 8388608
STREAMS = tuple(s+'.'+c for s in ('venv','install') for c in ('stdout','stderr'))
ALLOWED = frozenset(('permitted.synthetic','qualification.json','qualification.ready','intent.json','beforevenv.json','beforeinstall.json','afterinstall.json','complete.json','worker-primary.json','worker-terminal.json') + STREAMS + ('venv.terminal.json','install.terminal.json'))
ALLOWED = ALLOWED | _COUNTER115_NAMES
DESTINATIONS = frozenset(('/driver/worker.py','/inputs/request.json','/inputs/requirements.lock','/inputs/manifest.json','/wheels','/control','/output'))
STAGES = frozenset(('INITIALIZATION','ENVIRONMENT','QUALIFICATION','BEFORE_VENV','BEFORE_INSTALL','AFTER_INSTALL','BEFORE_COUNTER','AFTER_COUNTER','TERMINAL','CLEANUP','EXPORT'))
CODES = frozenset(('TERMINAL_MISSING','OOM','WORKER_NONZERO','QUALIFICATION_NOT_APPROVED','DEADLINE','INTENT','OUTPUT_SCHEMA','INITIALIZATION','CLEANUP','EXPORT'))
EXCEPTIONS = frozenset(('AssertionError','ValueError','TypeError','KeyError','FileNotFoundError','PermissionError','OSError','TimeoutError','TimeoutExpired','CalledProcessError','RuntimeError','KeyboardInterrupt','SystemExit','GateFailure','StageFailure','SignalFailure','FileExistsError'))
_HOST_KEY = object()

def prequalification_deadline120(overall,producer=None):
    if producer is None:return overall
    clock=producer.clock;clock.require(520)
    return min(overall,clock.phase(200,320))

def sha(data):
    return hashlib.sha256(data).hexdigest()

def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def strict(raw):
    def pairs(items):
        value = {}
        for k,v in items:
            if k in value:
                raise ValueError('Duplicate JSON')
            value[k] = v
        return value
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in ()).throw(ValueError('Nonfinite JSON')))

def record(root, name, value):
    fd = os.open(root/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'wb') as f:
        f.write(encoded(value))
        f.flush()
        os.fsync(f.fileno())

def safe_class(exc):
    name = type(exc).__name__
    return name if name in EXCEPTIONS else 'OTHER'

def host_capture(errors, operation, exc, channel=None):
    if len(errors) < 24:
        errors.append({'operation':operation,'channel':channel,'exception_class':safe_class(exc)})

def publish_signal(control, name, value, _observer=None):
    """Linux link(2), via os.link: atomic same-directory NO-REPLACE publish.
    Final name is absent until a complete closed fsynced0444 inode is linked.
    An existing final is never adopted, overwritten or removed.
    """
    if name not in ('GO.json','INSTALL_GO.json','COUNTER_GO116.json'):
        raise ValueError('Fixed control name')
    raw = encoded(value)
    if len(raw)>8192:
        raise ValueError('Control cap')
    control = directory(control)
    result = {'name':name,'bytes':len(raw),'sha256':sha(raw),'published':False,'readback_verified':False,'primary':None,'capture_failures':[]}
    rootfd = fd = None
    temporary = '.signal-'+uuid.uuid4().hex
    temp_created = False
    phase = 'PREPARE'
    try:
        rootfd = os.open(control,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
        rootstat = os.fstat(rootfd)
        if rootstat.st_uid!=os.getuid() or rootstat.st_mode & 0o022:
            raise ValueError('Control ownership')
        fd = os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_CLOEXEC,0o600,dir_fd=rootfd)
        temp_created = True
        inode = os.fstat(fd)
        if not stat.S_ISREG(inode.st_mode) or inode.st_nlink!=1 or inode.st_dev!=rootstat.st_dev:
            raise ValueError('Control inode')
        offset = 0
        while offset<len(raw):
            n = os.write(fd,raw[offset:])
            if n<=0:
                raise OSError('Control write')
            offset += n
        os.fchmod(fd,0o444)
        os.fsync(fd)
        closing = fd
        fd = None
        os.close(closing)  # Exactly one close attempt; failure prevents publication.
        if _observer is not None:
            _observer(control,name,raw)
        phase = 'COMMIT'
        os.link(temporary,name,src_dir_fd=rootfd,dst_dir_fd=rootfd,follow_symlinks=False)
        result['published'] = True
        phase = 'READBACK'
        os.fsync(rootfd)
        finalfd = os.open(name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK|os.O_CLOEXEC,dir_fd=rootfd)
        try:
            before = os.fstat(finalfd)
            if not stat.S_ISREG(before.st_mode) or (before.st_dev,before.st_ino)!=(inode.st_dev,inode.st_ino) or stat.S_IMODE(before.st_mode)!=0o444 or before.st_size!=len(raw) or before.st_nlink!=2:
                raise ValueError('Published inode')
            data = bytearray()
            while len(data)<=8192:
                part = os.read(finalfd,min(8193-len(data),8192))
                if not part:
                    break
                data.extend(part)
            after = os.fstat(finalfd)
            if bytes(data)!=raw or any(getattr(before,k)!=getattr(after,k) for k in ('st_dev','st_ino','st_size','st_mtime_ns','st_ctime_ns','st_nlink')):
                raise ValueError('Published readback')
            result['readback_verified'] = True
        finally:
            try:
                os.close(finalfd)
            except BaseException as exc:
                host_capture(result['capture_failures'],'SIGNAL_READBACK_CLOSE',exc)
    except BaseException as exc:
        result['primary'] = {'phase':phase,'exception_class':safe_class(exc),'unknown':True,'retry':False}
    finally:
        if fd is not None:
            try:
                os.close(fd)
            except BaseException as exc:
                host_capture(result['capture_failures'],'SIGNAL_TEMP_CLOSE',exc)
        if temp_created and rootfd is not None:
            try:
                os.unlink(temporary,dir_fd=rootfd)
            except BaseException as exc:
                host_capture(result['capture_failures'],'SIGNAL_TEMP_UNLINK',exc)
        if rootfd is not None:
            try:
                os.fsync(rootfd)
            except BaseException as exc:
                host_capture(result['capture_failures'],'SIGNAL_DIRECTORY_FSYNC',exc)
            try:
                os.close(rootfd)
            except BaseException as exc:
                host_capture(result['capture_failures'],'SIGNAL_DIRECTORY_CLOSE',exc)
    return result

def send_signal(control,name,value,private):
    receipt = publish_signal(control,name,value)
    capture = None
    try:
        record(private,name+'.publication.json',receipt)
    except BaseException as exc:
        capture = safe_class(exc)
    if receipt['primary'] is not None or receipt['capture_failures'] or capture is not None or not receipt['published'] or not receipt['readback_verified']:
        exc = GateFailure('INTENT')
        exc.signal_receipt = receipt
        exc.signal_capture_failure = capture
        raise exc

class Output:
    """Anchored directory; census checks ALL entries before any content read."""
    def __init__(self, path):
        self.fd = os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
        self.dev = os.fstat(self.fd).st_dev
    def close(self):
        os.close(self.fd)
    def opened(self, name):
        if name not in ALLOWED:
            raise ValueError('Output name')
        fd = os.open(name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK|os.O_CLOEXEC,dir_fd=self.fd)
        s = os.fstat(fd)
        if name in _COUNTER115_NAMES and s.st_uid!=65532:
            os.close(fd);raise ValueError('Fixed counter receipt owner')
        if not stat.S_ISREG(s.st_mode) or s.st_nlink != 1 or s.st_dev != self.dev or s.st_size > TOTAL:
            os.close(fd)
            raise ValueError('Output object')
        return fd,s
    def census(self):
        count = total = 0
        with os.scandir(self.fd) as entries:
            for entry in entries:
                count += 1
                if count > len(ALLOWED):
                    raise ValueError('Output count')
                fd,s = self.opened(entry.name)
                os.close(fd)
                total += s.st_size
                if total > TOTAL:
                    raise ValueError('Output total')
        return count,total
    def read(self, name, cap=8192, optional=False):
        try:
            fd,before = self.opened(name)
        except FileNotFoundError:
            if optional:
                return None
            raise
        try:
            if before.st_size > cap:
                raise ValueError('Output cap')
            data = bytearray()
            while len(data) <= cap:
                piece = os.read(fd,min(65536,cap+1-len(data)))
                if not piece:
                    break
                data.extend(piece)
            after = os.fstat(fd)
            fields = ('st_dev','st_ino','st_size','st_mtime_ns','st_ctime_ns','st_nlink')
            if len(data)>cap or len(data)!=after.st_size or any(getattr(before,k)!=getattr(after,k) for k in fields):
                raise ValueError('Output changed')
            return bytes(data)
        finally:
            os.close(fd)

def regular(path, cap):
    """Reject symlinks in every component, then O_NOFOLLOW the final regular file."""
    path = pathlib.Path(path).absolute()
    for parent in (path.parent,*path.parent.parents):
        if parent.is_symlink():
            raise ValueError('Input parent')
    fd = os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK|os.O_CLOEXEC)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink!=1 or before.st_size>cap:
            raise ValueError('Input object')
        with os.fdopen(os.dup(fd),'rb') as f:
            raw = f.read(cap+1)
        after = os.fstat(fd)
        if len(raw)!=after.st_size or len(raw)>cap or any(getattr(before,k)!=getattr(after,k) for k in ('st_dev','st_ino','st_size','st_mtime_ns','st_ctime_ns')):
            raise ValueError('Input changed')
        return raw
    finally:
        os.close(fd)

def directory(path):
    path = pathlib.Path(path).absolute()
    for part in (path,*path.parents):
        if part.is_symlink():
            raise ValueError('Directory link')
    fd = os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
    os.close(fd)
    return path

class HostEvidence:
    __slots__ = ('key','source','mounts')
    def __init__(self, key, source, mounts):
        if key is not _HOST_KEY:
            raise TypeError('Host provenance only')
        self.key,self.source,self.mounts = key,source,mounts

def prove_mounts(bindings, expected, source, extra=None):
    """Called only with trusted-host fixed bindings and externally pinned inputs."""
    destinations=DESTINATIONS|frozenset(extra or ())
    if set(bindings)!=destinations or set(expected)!=destinations-{'/control','/output','/wheels'}:
        raise ValueError('Mount set')
    checked = {}
    for dest in sorted(destinations):
        path,readonly = bindings[dest]
        if readonly is not (dest != '/output'):
            raise ValueError('Mount mode')
        if dest in expected:
            raw = regular(path,max(262144,expected[dest][0]))
            if (len(raw),sha(raw)) != tuple(expected[dest]):
                raise ValueError('Mount hash')
        else:
            directory(path)
        checked[dest] = {'path':str(pathlib.Path(path).absolute()),'readonly':readonly}
    return HostEvidence(_HOST_KEY,source,checked)

class GateFailure(RuntimeError):
    def __init__(self, code):
        if code not in CODES:
            raise ValueError('Failure code')
        self.code = code
        super().__init__(code)

def primary(stage, code, exc):
    return {'stage':stage if stage in STAGES else 'INITIALIZATION','code':code if code in CODES else 'INITIALIZATION','exception_class':type(exc).__name__ if type(exc).__name__ in EXCEPTIONS else 'OTHER','unknown':True,'retry':False}

def terminal_projection(state):
    if type(state) is not dict:
        return {'observed':False,'exit_code':None,'oom':None,'running':None}
    return {'observed':True,'exit_code':state.get('ExitCode') if type(state.get('ExitCode')) is int else None,'oom':state.get('OOMKilled') if type(state.get('OOMKilled')) is bool else None,'running':state.get('Running') if type(state.get('Running')) is bool else None}

def classify_terminal(state, approved):
    t = terminal_projection(state)
    if not t['observed'] or t['running'] is not False or t['exit_code'] is None or t['oom'] is None:
        return 'TERMINAL_MISSING'
    if t['oom']:
        return 'OOM'
    if t['exit_code'] != 0:
        return 'WORKER_NONZERO'
    if not approved:
        return 'QUALIFICATION_NOT_APPROVED'
    return None

def fixed_stage(output):
    stage = 'ENVIRONMENT'
    if output is None:
        return stage
    output.census()
    for name,value in [('beforevenv.json','BEFORE_VENV'),('beforeinstall.json','BEFORE_INSTALL'),('afterinstall.json','AFTER_INSTALL'),('beforecounter115.json','BEFORE_COUNTER'),('aftercounter115.json','AFTER_COUNTER')]:
        raw = output.read(name,optional=True)
        if raw is not None:
            if strict(raw) != {'stage':value,'closed':True}:
                raise GateFailure('OUTPUT_SCHEMA')
            stage = value
    return stage

WORKER_CODES = frozenset(('WORKER_NONZERO','DEADLINE','SPAWN_FAILURE','CAPTURE_FAILURE','WORKER_FAILURE','ISOLATION_FAILURE','TERMINAL_UNKNOWN'))
def project_primary(value):
    if value is None:
        return None
    if type(value) is not dict or value.get('stage') not in STAGES or value.get('exception_class') not in EXCEPTIONS|{'OTHER'} or value.get('code') not in WORKER_CODES or value.get('unknown') is not True or value.get('retry') is not False or type(value.get('timed_out')) is not bool or value.get('returncode') is not None and type(value.get('returncode')) is not int:
        raise ValueError('Worker primary schema')
    return {k:value[k] for k in ('stage','code','exception_class','returncode','timed_out','unknown','retry')}

def project_process(value):
    """Fixed public process custody only; worker declarations are never authority."""
    if type(value) is not dict:
        raise ValueError('Process receipt')
    out = {}
    for k in ('returncode','original_returncode'):
        v = value.get(k)
        if v is not None and (type(v) is not int or abs(v)>2147483647):
            raise ValueError('Process return')
        out[k] = v
    for k in ('terminal_observed','timed_out'):
        if type(value.get(k)) is not bool:
            raise ValueError('Process flag')
        out[k] = value[k]
    for k in ('kill_attempts','wait_attempts'):
        if type(value.get(k)) is not int or not 0<=value[k]<=2:
            raise ValueError('Process attempts')
        out[k] = value[k]
    out['primary'] = project_primary(value.get('primary'))
    operations = frozenset(('OUTPUT_FD_CLOSE','LIBC_LOAD','LANDLOCK_ABI_QUERY',
        'LANDLOCK_ABI_BELOW_3','LANDLOCK_CREATE','CACHE_OPEN','CACHE_OWNER',
        'LANDLOCK_ADD_RULE','NO_NEW_PRIVS','LANDLOCK_RESTRICT','CACHE_LIMIT_RAISE',
        'LANDLOCK_FD_CLOSE','PREEXEC','FD_CLOSE','CUSTODY_READ_AFTER_SPAWN',
        'POLL','KILL','WAIT_REAP','SELECTOR_CLOSE','PIPE_CLOSE','CHANNEL_SAVE',
        'FLUSH','FSYNC','CLOSE','READBACK','TERMINAL_SAVE'))
    def fault(v):
        if type(v) is not dict or v.get('operation') not in operations or v.get('exception_class') not in EXCEPTIONS|{'OTHER'}:
            raise ValueError('Process fault')
        n = v.get('errno')
        if n is not None and (type(n) is not int or not 0<=n<=4095):
            raise ValueError('Process errno')
        return {'operation':v['operation'],'exception_class':v['exception_class'],'errno':n}
    cleanup = value.get('cleanup')
    if type(cleanup) is not list or len(cleanup)>24:
        raise ValueError('Process cleanup cap')
    out['cleanup'] = [fault(x) for x in cleanup]
    labels = value.get('close_attempts')
    allowed = frozenset(('custody_write_parent','custody_read_parent','pipe_stdout','pipe_stderr','capture_stdout','capture_stderr'))
    if type(labels) is not list or len(labels)>6 or len(set(labels))!=len(labels) or any(x not in allowed for x in labels):
        raise ValueError('Process close custody')
    out['close_attempts'] = labels
    c = value.get('isolation')
    if c is None:
        out['isolation'] = None
    else:
        if type(c) is not dict or c.get('schema')!='CACHE_ONLY_CHILD_V112':
            raise ValueError('Isolation receipt')
        abi = c.get('abi')
        if abi is not None and (type(abi) is not int or not 0<=abi<=65535):
            raise ValueError('Public ABI')
        for k in ('restricted','cache_soft_limit_raised'):
            if type(c.get(k)) is not bool:
                raise ValueError('Isolation flag')
        for k in ('close_attempts','output_fds_closed'):
            if type(c.get(k)) is not list or len(c[k])>4 or any(type(x) is not int or not 3<=x<1048576 for x in c[k]) or (k=='output_fds_closed' and len(set(c[k]))!=len(c[k])):
                raise ValueError('Isolation FD custody')
        if type(c.get('cleanup')) is not list or len(c['cleanup'])>4:
            raise ValueError('Isolation cleanup')
        out['isolation'] = {'abi':abi,'restricted':c['restricted'],
            'cache_soft_limit_raised':c['cache_soft_limit_raised'],
            'primary':None if c.get('primary') is None else fault(c['primary']),
            'cleanup':[fault(x) for x in c['cleanup']],
            'close_attempt_count':len(c['close_attempts']),
            'output_fds_closed_count':len(c['output_fds_closed'])}
    return out


def project_worker(output, safe):
    result = {}
    for name in ('worker-primary.json','worker-terminal.json','venv.terminal.json','install.terminal.json'):
        entry = {'available':False,'value':None,'refusal':{'reason':'UNAVAILABLE_OR_UNPROVEN'},'declared_evidence_only':True,'authority':False}
        if safe:
            try:
                raw = output.read(name,8192,optional=True)
                if raw is not None:
                    value = strict(raw)
                    if name in ('venv.terminal.json','install.terminal.json'):
                        entry.update(available=True,value=project_process(value),refusal=None)
                        result[name] = entry
                        continue
                    if type(value) is not dict or 'primary' not in value or type(value.get('capture_failure')) is not bool:
                        raise ValueError('Worker terminal schema')
                    projection = {'primary':project_primary(value.get('primary')),'capture_failure':value['capture_failure']}
                    if name == 'worker-terminal.json':
                        if value.get('completion') not in ('DIAGNOSTIC_ONLY_NO_COUNTER','COUNTER115_PENDING_HOST_REVIEW','STOP_UNKNOWN_NO_RETRY') or type(value.get('exit_code')) is not int or value['exit_code'] not in (0,1):
                            raise ValueError('Worker completion schema')
                        projection.update(completion=value['completion'],exit_code=value['exit_code'])
                    entry.update(available=True,value=projection,refusal=None)
                else:
                    entry['refusal'] = {'reason':'MISSING'}
            except BaseException as exc:
                entry['refusal'] = primary('EXPORT','OUTPUT_SCHEMA',exc)
        result[name] = entry
    return result

def export_proof(proof, output, evidence, binding, first, terminal, approved, cleanup, stopped):
    """The only public exporter. Never consumes paths/provenance from worker JSON."""
    # _COUNTER115_RESULT can be set only after fixed host custody validation.
    trusted = isinstance(evidence,HostEvidence) and evidence.key is _HOST_KEY and evidence.source==binding['source_sha']
    safe = trusted and stopped is True and output is not None
    refusal = None
    if safe:
        try:
            output.census()
        except BaseException as exc:
            safe = False
            refusal = primary('EXPORT','OUTPUT_SCHEMA',exc)
    channels = {}
    for name in STREAMS:
        r = {'source':'fixed-worker-output','channel':name,'available':False,'bytes':None,'sha256':None,'truncated':None,'incomplete':None,'data_base64':None}
        if safe:
            try:
                raw = output.read(name,CAP,optional=True)
                if raw is not None:
                    # Only a closed matching producer terminal permits raw publication.
                    stem,channel = name.split('.')
                    traw = output.read(stem+'.terminal.json',8192,optional=True)
                    if traw is not None:
                        t = strict(traw)
                        c = t['streams'][channel]
                        if c['available'] is True and c['bytes']==len(raw) and c['sha256']==sha(raw) and c['truncated'] is False:
                            r.update(available=True,bytes=len(raw),sha256=sha(raw),truncated=False,incomplete=bool(t.get('timed_out') or t.get('exception_class')),data_base64=base64.b64encode(raw).decode())
            except BaseException as exc:
                r['refusal'] = primary('EXPORT','OUTPUT_SCHEMA',exc)
        channels[name] = r
    result = {'schema':'TRACEHARBOR_DIAGNOSTIC108_SAFE_V1','mode':MODE,'binding':binding,'primary':first,'terminal':terminal_projection(terminal),'qualification_approved':approved is True,'cleanup':cleanup,'mount_provenance_observed':trusted,'container_stopped_observed':stopped is True,'raw_exposure_permitted':safe,'census_refusal':refusal,'channels':channels,'counter107':'UNKNOWN','counter108_invoked':False,'completion_authority':'DIAGNOSTIC_ONLY_NO_COUNTER'}
    result['worker_evidence'] = project_worker(output,safe)
    result['counter115_attempted'] = _COUNTER115_RELEASED
    result['counter115'] = _COUNTER115_RESULT if safe and first is None and not cleanup and _COUNTER115_RESULT is not None and _COUNTER115_RESULT.get('source_sha')==binding['source_sha'] else None
    if _COUNTER115_RELEASED:
        result['mode']='PROTECTED_OFFLINE_COUNTER115'
        result['completion_authority']='HOST_CHECKED_CANDIDATE_ONLY_T_NULL_NO_FINANCIAL_AUTHORITY'
    # No raw counter stdout, stderr, tokens, rendering input or worker paths.
    projection_failed = False
    try:
        result['qualification113'] = _HOST113.project_state(sys.modules[__name__],_QUAL113,binding) if _HOST113 is not None else {'schema':'TRACE113_PREQUALIFICATION_V1','binding':binding,'native':'NOT_RUN','inventory':'NOT_RUN','diagnostic_admitted':False}
    except BaseException as exc:
        projection_failed = True
        result['qualification113'] = {'schema':'TRACE113_PREQUALIFICATION_V1','binding':binding,'native':'UNKNOWN','inventory':'UNKNOWN','diagnostic_admitted':False,'projection_failure':safe_class(exc)}
        if result['primary'] is None:
            result['primary'] = primary('EXPORT','OUTPUT_SCHEMA',exc)
    raw = encoded(result)
    if len(raw)>1048576:
        raise ValueError('Proof total cap')
    proof.mkdir(mode=0o700)
    record(proof,'proof.json',result)
    if projection_failed:
        raise GateFailure('OUTPUT_SCHEMA')
    return result

def finish(private, proof, output, evidence, binding, first, terminal, approved, cleanup_fn):
    """Freeze first primary BEFORE cleanup; exporter failure cannot erase it."""
    captures = []
    try:
        record(private,'primary.json',first)
        record(private,'original-terminal.json',terminal)
    except BaseException as exc:
        captures.append(primary('TERMINAL','OUTPUT_SCHEMA',exc))
    cleanup = []
    stopped = terminal_projection(terminal)['running'] is False
    try:
        cleanup,clean_stopped = cleanup_fn()
        stopped = stopped or clean_stopped is True
    except BaseException as exc:
        cleanup.append(primary('CLEANUP','CLEANUP',exc))
    cleanup += captures
    exported = None
    try:
        exported = export_proof(proof,output,evidence,binding,first,terminal,approved,cleanup,stopped)
    except BaseException as exc:
        captures.append(primary('EXPORT','EXPORT',exc))
    result = {'primary':first,'terminal':terminal_projection(terminal),'cleanup':cleanup,'capture_failures':captures,'proof_saved':exported is not None,'exit_code':1 if first is not None or cleanup or captures or exported is None else 0}
    try:
        record(private,'host-terminal.json',result)
    except BaseException:
        result['exit_code'] = 1
    return result

def invoke(argv, root, stem, deadline):
    """First CLI result survives kill/close/channel-save/terminal-save failures."""
    data = {'stdout':bytearray(),'stderr':bytearray()}
    truncated = {'stdout':False,'stderr':False}
    proc = None
    sel = selectors.DefaultSelector()
    terminal = {'returncode':None,'exception_class':None,'timed_out':False,'primary':None,'capture_failures':[],'streams':{},'terminal_saved':False}
    try:
        proc = subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
        for channel in data:
            pipe = getattr(proc,channel)
            os.set_blocking(pipe.fileno(),False)
            sel.register(pipe,selectors.EVENT_READ,channel)
        while sel.get_map() and time.monotonic()<deadline:
            for key,_ in sel.select(min(.05,max(0,deadline-time.monotonic()))):
                piece = os.read(key.fileobj.fileno(),65536)
                if not piece:
                    sel.unregister(key.fileobj)
                    continue
                remaining = max(0,CAP-len(data[key.data]))
                data[key.data].extend(piece[:remaining])
                truncated[key.data] |= len(piece)>remaining
        if sel.get_map() or time.monotonic()>=deadline:
            terminal['timed_out'] = True
            terminal['primary'] = {'code':'DEADLINE','exception_class':'TimeoutExpired','returncode':None}
        else:
            terminal['returncode'] = proc.wait(timeout=max(.001,min(.2,deadline-time.monotonic())))
            if terminal['returncode']!=0:
                terminal['primary'] = {'code':'WORKER_NONZERO','exception_class':'CalledProcessError','returncode':terminal['returncode']}
    except BaseException as exc:
        terminal['exception_class'] = safe_class(exc)
        terminal['timed_out'] |= isinstance(exc,subprocess.TimeoutExpired)
        if terminal['primary'] is None:
            terminal['primary'] = {'code':'DEADLINE' if terminal['timed_out'] else 'INITIALIZATION','exception_class':safe_class(exc),'returncode':terminal['returncode']}
    incomplete = bool(sel.get_map())
    if proc is not None:
        try:
            if proc.poll() is None:
                proc.kill()
        except BaseException as exc:
            host_capture(terminal['capture_failures'],'KILL',exc)
    try:
        sel.close()
    except BaseException as exc:
        host_capture(terminal['capture_failures'],'SELECTOR_CLOSE',exc)
    if proc is not None:
        for channel in data:
            try:
                getattr(proc,channel).close()
            except BaseException as exc:
                host_capture(terminal['capture_failures'],'PIPE_CLOSE',exc,channel)
    for channel in data:
        terminal['streams'][channel] = {'bytes':len(data[channel]) if proc is not None else None,'sha256':sha(data[channel]) if proc is not None else None,'truncated':truncated[channel] if proc is not None else None,'incomplete':incomplete if proc is not None else None,'available':proc is not None,'saved':False}
        handle = None
        if proc is not None:
            try:
                handle = (root/(stem+'.'+channel)).open('xb',buffering=0)
                view = memoryview(data[channel])
                while view:
                    n = handle.write(view)
                    if not n:
                        raise OSError('Channel write')
                    view = view[n:]
                terminal['streams'][channel]['saved'] = True
            except BaseException as exc:
                host_capture(terminal['capture_failures'],'CHANNEL_SAVE',exc,channel)
            if handle is not None:
                try:
                    handle.flush()
                except BaseException as exc:
                    host_capture(terminal['capture_failures'],'CHANNEL_FLUSH',exc,channel)
                try:
                    os.fsync(handle.fileno())
                except BaseException as exc:
                    host_capture(terminal['capture_failures'],'CHANNEL_FSYNC',exc,channel)
                try:
                    handle.close()
                except BaseException as exc:
                    host_capture(terminal['capture_failures'],'CHANNEL_CLOSE',exc,channel)
    if terminal['primary'] is None and (terminal['capture_failures'] or any(s['truncated'] or s['incomplete'] for s in terminal['streams'].values())):
        terminal['primary'] = {'code':'OUTPUT_SCHEMA','exception_class':'RuntimeError','returncode':terminal['returncode']}
    terminal['terminal_saved'] = True
    try:
        record(root,stem+'.terminal.json',terminal)
    except BaseException as exc:
        terminal['terminal_saved'] = False
        host_capture(terminal['capture_failures'],'TERMINAL_SAVE',exc)
        if terminal['primary'] is None:
            terminal['primary'] = {'code':'OUTPUT_SCHEMA','exception_class':safe_class(exc),'returncode':terminal['returncode']}
    return terminal,{k:bytes(v) for k,v in data.items()}

def checked(argv, root, stem, deadline):
    t,data = invoke(argv,root,stem,deadline)
    if t['primary'] is not None or t['capture_failures'] or t['returncode']!=0:
        exc = GateFailure(t['primary']['code'] if t['primary'] is not None else 'OUTPUT_SCHEMA')
        exc.invoke_original = t
        raise exc
    return data['stdout']

def cleanup_once(private, name, terminal, deadline):
    failures = []
    stopped = terminal_projection(terminal)['running'] is False
    commands = ([] if stopped else [('kill',['docker','kill',name])]) + [('inspect',['docker','inspect','-f','{{json .State}}',name]),('logs',['docker','logs',name]),('remove',['docker','rm','-f',name])]
    for stem,argv in commands:
        try:
            t,data = invoke(argv,private,'cleanup-'+stem,min(deadline,time.monotonic()+2))
            if t['returncode']!=0 or t['exception_class'] or t['timed_out'] or t['primary'] is not None or t['capture_failures']:
                failures.append(primary('CLEANUP','CLEANUP',RuntimeError()))
            elif stem=='inspect':
                stopped |= terminal_projection(strict(data['stdout']))['running'] is False
            elif stem=='remove':
                stopped = True
        except BaseException as exc:
            failures.append(primary('CLEANUP','CLEANUP',exc))
    return failures,stopped

def validate(x, repo, counter=False):
    if not re.fullmatch('[0-9a-f]{40}',x.source_sha) or not re.fullmatch('[0-9a-f]{64}',x.manifest_sha) or not re.fullmatch('[0-9a-f]{64}',x.once_receipt_sha):
        raise GateFailure('INTENT')
    expected_env = {'GITHUB_REPOSITORY':'Elinfiny/TraceHarbor','GITHUB_REPOSITORY_ID':'1391430317','GITHUB_ACTOR_ID':'273768139','GITHUB_EVENT_NAME':'workflow_dispatch','GITHUB_RUN_ATTEMPT':'1','GITHUB_SHA':x.source_sha,'GITHUB_WORKFLOW_SHA':x.source_sha}
    if any(os.environ.get(k)!=v for k,v in expected_env.items()) or not re.fullmatch('[0-9]+',os.environ.get('GITHUB_RUN_ID','')):
        raise GateFailure('INTENT')
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True,timeout=2).strip()!=x.source_sha:
        raise GateFailure('INTENT')
    mf = repo/'diagnostic108/manifest.json'
    raw = regular(mf,262144)
    if sha(raw)!=x.manifest_sha:
        raise GateFailure('INTENT')
    m = strict(raw)
    if m['mode']!=MODE or any(m[k] is not False for k in ('counter_allowed','private_vendor_allowed','model_allowed')) or counter and (m['counter116']['mode']!='PROTECTED_OFFLINE_COUNTER115' or m['counter116']['activation']!='TYPED_CURRENT_NATIVE_PRODUCER_ONLY'):
        raise GateFailure('INTENT')
    for name,pin in m['source_files'].items():
        if name.startswith('/') or '..' in pathlib.PurePosixPath(name).parts:
            raise GateFailure('INTENT')
        value = regular(repo/name,262144)
        if len(value)!=pin['bytes'] or sha(value)!=pin['sha256']:
            raise GateFailure('INTENT')
    if len(regular(repo/'offline103/request.json',4935))!=4935 or len(m['wheels'])!=29:
        raise GateFailure('INTENT')
    return m,mf

def execute(x, private, binding, counter_requested=False):
    global _HOST113, _COUNTER115_RESULT, _COUNTER115_RELEASED
    _COUNTER115_RESULT = None
    _COUNTER115_RELEASED = False
    overall = time.monotonic()+(720 if counter_requested else 540)
    repo = directory(pathlib.Path(__file__).absolute().parent.parent)
    output = evidence = terminal = None
    approved = False
    first = None
    attempted = False
    stage = 'INITIALIZATION'
    name = None
    sentinel = None
    count = 0
    end = time.monotonic()+180
    counter_plan = bridge = None
    try:
        m,mf = validate(x,repo,counter=counter_requested)
        counter_plan = bridge = None
        if counter_requested:
            spec115=importlib.util.spec_from_file_location('private_counter115',repo/'diagnostic108/counter115.py')
            bridge=importlib.util.module_from_spec(spec115);spec115.loader.exec_module(bridge)
            counter_plan=bridge.prepare_host(sys.modules[__name__],x,repo,m,private)
        temp = directory(os.environ['RUNNER_TEMP'])
        # External once receipt must be reserved against this exact source/hash in
        # the solewriter's admission BEFORE dispatch; local create-only is no substitute.
        once = temp/('traceharbor-diagnostic108-once-'+x.once_receipt_sha)
        with once.open('xb') as f:
            f.write(encoded(binding));f.flush();os.fsync(f.fileno())
        # Whole113 prequalification/inventory gates; no downloaded module imported.
        stage = 'QUALIFICATION'
        spec = importlib.util.spec_from_file_location('trace113_host',repo/'qualification113/host.py')
        host_module = importlib.util.module_from_spec(spec);spec.loader.exec_module(host_module)
        _HOST113 = host_module
        if counter_plan is not None:
            pclock=counter_plan['producer'].clock
            overall=min(overall,counter_plan['producer'].main_end,pclock.end_mono)
        prequal_end=overall-(95 if counter_plan is not None else 0)
        prequal_end=prequalification_deadline120(prequal_end,counter_plan['producer'] if counter_plan is not None else None)
        _HOST113.prequalify(sys.modules[__name__],x,repo,m,private,binding,prequal_end)
        if _QUAL113 is None or _QUAL113['diagnostic_admitted'] is not True or overall-time.monotonic()<(320 if counter_plan is not None else 225):
            raise GateFailure('QUALIFICATION_NOT_APPROVED')
        if counter_plan is not None:
            bridge.complete_intake(sys.modules[__name__],counter_plan,binding,repo,m)
        public = directory(temp/'traceharbor-offline103')
        public_receipt = strict(regular(public/'control/PUBLIC_DATA_ONLY.json',8192))
        if public_receipt.get('worker_ready') is not False:
            raise GateFailure('INTENT')
        wheels = directory(public/'wheels')
        expected_names = {w['filename'] for w in m['wheels']}
        if {p.name for p in wheels.iterdir()}!=expected_names:
            raise GateFailure('INTENT')
        for w in m['wheels']:
            p = wheels/w['filename']
            raw = regular(p,w['bytes'])
            if len(raw)!=w['bytes'] or sha(raw)!=w['sha256']:
                raise GateFailure('INTENT')
            os.chmod(p,0o444)
        os.chmod(wheels,0o555)
        root = temp/'traceharbor-diagnostic108'
        root.mkdir(mode=0o755)
        control = root/'control';control.mkdir(mode=0o755)
        out = root/'output';out.mkdir(mode=0o777);os.chmod(out,0o777)
        output = Output(out)
        if output.census()!=(0,0):
            raise GateFailure('OUTPUT_SCHEMA')
        bindings = {'/driver/worker.py':(repo/'diagnostic108/worker.py',True),'/inputs/request.json':(repo/'offline103/request.json',True),'/inputs/requirements.lock':(repo/'offline103/requirements.lock',True),'/inputs/manifest.json':(mf,True),'/wheels':(wheels,True),'/control':(control,True),'/output':(out,False)}
        expected = {dest:(m['source_files'][str(path.relative_to(repo))]['bytes'],m['source_files'][str(path.relative_to(repo))]['sha256']) for dest,(path,_) in bindings.items() if dest in ('/driver/worker.py','/inputs/request.json','/inputs/requirements.lock')}
        expected['/inputs/manifest.json'] = (len(regular(mf,262144)),x.manifest_sha)
        if counter_plan is not None:
            bindings.update(counter_plan['mounts']);expected.update(counter_plan['expected'])
        evidence = prove_mounts(bindings,expected,x.source_sha,extra=None if counter_plan is None else counter_plan['mounts'])
        if counter_plan is not None:
            bridge.bind_current_mounts(sys.modules[__name__],counter_plan,evidence,bindings,_QUAL113)
        sentinel = temp/('outside-synthetic108-'+x.once_receipt_sha)
        with sentinel.open('xb') as f:
            f.write(b'SYNTHETIC_NOT_SECRET')
        stage = 'ENVIRONMENT'
        if counter_plan is not None:counter_plan['producer'].clock.require(195)
        start = time.monotonic();deadline = start+170;end=start+180;absolute=time.time()+170
        if counter_plan is not None:
            absolute=min(absolute,counter_plan['producer'].clock.end_utc-25)
            deadline=min(deadline,counter_plan['producer'].clock.end_mono-25);end=deadline+10
        name = 'traceharbor-diagnostic108-'+os.environ['GITHUB_RUN_ID']+'-'+x.once_receipt_sha[:12]
        image = m['runtime']['immutable_image']
        # Immutable image already verified/pulled at most once by prequalification.
        args = ['docker','create','--name',name,'--label=trace113.source='+x.source_sha,'--label=trace113.once='+x.once_receipt_sha,'--platform=linux/amd64','--network=none','--read-only','--user=65532:65532','--cap-drop=ALL','--security-opt=no-new-privileges:true','--pids-limit=64','--memory=1g','--memory-swap=1g','--cpus=1','--ulimit=cpu=120:120','--ulimit=nofile=1024:1024','--ulimit=fsize=8388608:67108864','--ipc=private','--workdir=/cache','--tmpfs=/cache:rw,exec,nosuid,nodev,size=512m,uid=65532,gid=65532,mode=700']
        for dest,(path,readonly) in bindings.items():
            args += ['--mount','type=bind,src='+str(path.absolute())+',dst='+dest+(',readonly' if readonly else '')]
        args += [image,'python','-I','/driver/worker.py']
        attempted = True
        checked(args,private,'container-create',deadline)
        checked(['docker','start',name],private,'container-start',deadline)
        pid = int(checked(['docker','inspect','-f','{{.State.Pid}}',name],private,'container-pid',deadline))
        with (pathlib.Path('/proc')/str(pid)/'cgroup').open() as f:
            cgroup_raw = f.read(8193)
        if len(cgroup_raw)>8192:
            raise GateFailure('INTENT')
        cg = [line.split(':',2)[2] for line in cgroup_raw.splitlines() if line.startswith('0::')]
        if len(cg)!=1 or '..' in pathlib.PurePosixPath(cg[0]).parts:
            raise GateFailure('INTENT')
        cpu = pathlib.Path('/sys/fs/cgroup')/cg[0].lstrip('/')/'cpu.stat'
        def usage():
            # Kernel pseudo-file size is zero; read separately from ordinary inputs.
            with cpu.open() as f:
                return int(dict(line.split() for line in f.read(8192).splitlines())['usage_usec'])
        if usage()>120000000:
            raise GateFailure('DEADLINE')
        go = {'absolute_deadline_utc':absolute,'host_sentinel':str(sentinel),'once_receipt_sha256':x.once_receipt_sha,'source_sha':x.source_sha,'manifest_sha256':x.manifest_sha,'output_absent':True}
        if counter_plan is not None:
            go['counter115']=bridge.make_worker_binding(sys.modules[__name__],counter_plan,binding,m,absolute)
        send_signal(control,'GO.json',go,private)
        stage = 'QUALIFICATION'
        while time.monotonic()<deadline:
            count += 1
            state = strict(checked(['docker','inspect','-f','{{json .State}}',name],private,'state-'+str(count),min(deadline,time.monotonic()+2)))
            if state.get('Running') is False:
                terminal = state
                break
            if usage()>120000000:
                raise GateFailure('DEADLINE')
            output.census()
            ready = output.read('qualification.ready',0,optional=True) if not approved else None
            if ready is not None and not approved:
                q = strict(output.read('qualification.json'))
                if set(q)!={'case1_permitted_read_write','case2_denial','credential_env_present'} or q['case1_permitted_read_write'] is not True or q['credential_env_present'] is not False or set(q['case2_denial'])!={'host_file','root_write','socket'} or q['case2_denial']['socket']!=errno.EPERM or q['case2_denial']['host_file'] not in (errno.ENOENT,errno.EACCES,errno.EPERM) or q['case2_denial']['root_write'] not in (errno.EROFS,errno.EACCES,errno.EPERM):
                    raise GateFailure('QUALIFICATION_NOT_APPROVED')
                intent_raw = output.read('intent.json')
                intent = strict(intent_raw)
                wanted = {'source_sha':x.source_sha,'manifest_sha256':x.manifest_sha,'once_receipt_sha256':x.once_receipt_sha,'runtime':image,'request_sha256':m['request_sha256'],'lock_sha256':m['lock_sha256'],'absolute_deadline_utc':absolute,'output_absent':True,'mode':m['mode']}
                if intent!=wanted or type(intent['output_absent']) is not bool:
                    raise GateFailure('INTENT')
                with (control/'FROZEN_INTENT.json').open('xb') as f:
                    f.write(intent_raw);f.flush();os.fsync(f.fileno())
                send_signal(control,'INSTALL_GO.json',{'intent_sha256':sha(intent_raw)},private)
                approved = True
            if approved and counter_plan is not None:
                bridge.release_if_ready(sys.modules[__name__],counter_plan,output,control,private,evidence,state)
            time.sleep(.2)
        stage = fixed_stage(output)
        failure_code = classify_terminal(terminal,approved)
        if failure_code:
            raise GateFailure(failure_code)
        if time.monotonic()>deadline or time.time()>absolute:
            raise GateFailure('DEADLINE')
        output.census()
        complete = strict(output.read('complete.json'))
        expected_type='COUNTER115_PENDING_HOST_REVIEW' if counter_plan is not None else 'DIAGNOSTIC_ONLY_NO_COUNTER'
        expected_stage='AFTER_COUNTER' if counter_plan is not None else 'AFTER_INSTALL'
        if complete!={'type':expected_type,'intent_sha256':sha(intent_raw)} or stage!=expected_stage:
            raise GateFailure('OUTPUT_SCHEMA')
        for stem in ('venv','install'):
            t = strict(output.read(stem+'.terminal.json'))
            if t['returncode']!=0 or t['exception_class'] is not None or t['timed_out'] is not False or t['capture_failures'] or t['primary'] is not None:
                raise GateFailure('OUTPUT_SCHEMA')
        wt = strict(output.read('worker-terminal.json'))
        if wt!={'primary':None,'capture_failure':False,'completion':expected_type,'exit_code':0}:
            raise GateFailure('OUTPUT_SCHEMA')
        if counter_plan is not None:
            _COUNTER115_RESULT=bridge.verify_host_completion(sys.modules[__name__],counter_plan,output,terminal,approved)
    except BaseException as exc:
        try:
            if output is not None:
                observed_stage = fixed_stage(output)
                if observed_stage != 'ENVIRONMENT':
                    stage = observed_stage
        except BaseException:
            pass
        first = primary(stage,exc.code if isinstance(exc,GateFailure) else ('OUTPUT_SCHEMA' if stage not in ('INITIALIZATION','ENVIRONMENT') else 'INITIALIZATION'),exc)
        if hasattr(exc,'intake_cleanup'):
            try:record(private,'intake117-error-cleanup.json',exc.intake_cleanup)
            except BaseException:pass
        if hasattr(exc,'invoke_original'):
            t = exc.invoke_original
            first['host_subprocess_original'] = {'returncode':t['returncode'],'exception_class':t['exception_class'],'timed_out':t['timed_out'],'primary':t['primary'],'capture_failure':bool(t['capture_failures']),'terminal_saved':t['terminal_saved']}
        if hasattr(exc,'signal_receipt'):
            first['signal_original'] = {'published':exc.signal_receipt['published'],'readback_verified':exc.signal_receipt['readback_verified'],'primary':exc.signal_receipt['primary'],'capture_failure':bool(exc.signal_receipt['capture_failures']) or exc.signal_capture_failure is not None}

    def cleanup():
        failures,stopped = _HOST113.cleanup(sys.modules[__name__],private,name,binding,end,_QUAL113) if attempted else ([],False)
        if sentinel is not None:
            try:
                sentinel.unlink(missing_ok=True)
            except BaseException as exc:
                failures.append(primary('CLEANUP','CLEANUP',exc))
        if counter_plan is not None:
            receipt=counter_plan['producer'].cleanup('terminal',None)
            record(private,'intake117-cleanup.json',receipt)
            if receipt['unknown']:failures.append(primary('CLEANUP','CLEANUP',RuntimeError()))
        return failures,stopped
    result = finish(private,pathlib.Path(os.environ['RUNNER_TEMP'])/'traceharbor-diagnostic108-proof',output,evidence,binding,first,terminal,approved,cleanup)
    if counter_requested:
        result['counter115_private_projection']=_COUNTER115_RESULT
        result['counter115_public_export']='NOT_ADMITTED; no raw counter channels or worker paths exported'
    if output is not None:
        try:
            output.close()
        except BaseException:
            result['exit_code'] = 1
    if time.monotonic()>end and attempted:
        result['exit_code'] = 1
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-sha',required=True)
    parser.add_argument('--manifest-sha',required=True)
    parser.add_argument('--once-receipt-sha',required=True)
    parser.add_argument('--counter116',action='store_true')
    parser.add_argument('--counter116-init',action='store_true')
    parser.add_argument('--counter117-cleanup',action='store_true')
    parser.add_argument('--once-expires-utc',type=int)
    parser.add_argument('--coordinator-cutoff-utc',type=int)
    x = parser.parse_args()
    temp = directory(os.environ['RUNNER_TEMP'])
    private = temp/'traceharbor-diagnostic108-private'
    if not x.counter116_init and not x.counter117_cleanup:private.mkdir(mode=0o700)
    binding = {'source_sha':x.source_sha if re.fullmatch('[0-9a-f]{40}',x.source_sha) else None,'manifest_sha256':x.manifest_sha if re.fullmatch('[0-9a-f]{64}',x.manifest_sha) else None,'once_receipt_sha256':x.once_receipt_sha if re.fullmatch('[0-9a-f]{64}',x.once_receipt_sha) else None,'run_id':os.environ.get('GITHUB_RUN_ID') if re.fullmatch('[0-9]+',os.environ.get('GITHUB_RUN_ID','')) else None,'request_sha256':'e4b08fa3937e4c8348383a5abf934ffbf3832183fadc2907018adbc4a04a71b2'}
    if x.counter117_cleanup:
        # Always fallback: source validation + exact known run/nonce/root anchor.
        repo=directory(pathlib.Path(__file__).absolute().parent.parent)
        m,mf=validate(x,repo,counter=True)
        sp=importlib.util.spec_from_file_location('same_cleanup_bridge117',repo/'diagnostic108/counter115.py')
        cb=importlib.util.module_from_spec(sp);sp.loader.exec_module(cb)
        p=cb.producer_module(repo);root=temp/('traceharbor-counter117-intake-'+x.once_receipt_sha)
        try:
            owner=p.OwnedIntake(root,binding,cb.input_pins(),create=False)
            r=owner.cleanup('workflow_always')
            scalar={'schema':'TRACE117_CLEANUP_SAFE','status':r['status'],'paths_observed':len(r['paths']),'unknown':r['unknown'],'retry':False,'secure_erase':False}
        except BaseException as exc:
            scalar={'schema':'TRACE117_CLEANUP_SAFE','status':'UNKNOWN','paths_observed':None,'unknown':True,'retry':False,'secure_erase':False}
        print(encoded(scalar).decode());return 1 if scalar['unknown'] else 0
    if x.counter116_init:
        # Actual future native init step precedes the existing recipient artifact
        # upload. Main later recaptures its caller and exact fresh context.
        repo=directory(pathlib.Path(__file__).absolute().parent.parent)
        m,mf=validate(x,repo,counter=True)
        sp=importlib.util.spec_from_file_location('same_counter_bridge116',repo/'diagnostic108/counter115.py')
        bridge=importlib.util.module_from_spec(sp);sp.loader.exec_module(bridge)
        path=bridge.prepare_host(sys.modules[__name__],x,repo,m,private,initializing=True)
        print(encoded({'recipient_public_path':str(path),'source_sha':x.source_sha,'once_receipt_sha256':x.once_receipt_sha}).decode())
        return 0
    result = execute(x,private,binding,counter_requested=x.counter116)
    print(encoded({'exit_code':result['exit_code'],'primary':result['primary'],'proof_saved':result['proof_saved']}).decode())
    return result['exit_code']

if __name__=='__main__':
    sys.exit(main())
