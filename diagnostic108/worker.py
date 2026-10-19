"""Private candidate108. Standard-library driver; stops after offline installation."""
import ctypes, errno, hashlib, json, os, pathlib, resource, socket, subprocess, sys, time, selectors
R = pathlib.Path('/output')
C = pathlib.Path('/control')
I = pathlib.Path('/inputs')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def emit(name, data):
    with (R / name).open('xb') as f:
        f.write(json.dumps(data, sort_keys=True, allow_nan=False).encode())
        f.flush()
        os.fsync(f.fileno())

def wait(name, deadline):
    while time.monotonic() < deadline:
        try:
            with (C / name).open('rb') as f:
                raw = f.read(8193)
            if len(raw) > 8192:
                raise ValueError('Control cap')
            return json.loads(raw)
        except FileNotFoundError:
            time.sleep(.05)
    raise TimeoutError('Control deadline')

def restrict():
    assert sys.platform == 'linux' and os.uname().machine == 'x86_64'
    os.closerange(3, 1048576)
    allowed = {'PATH':'/usr/local/bin:/usr/bin:/bin','HOME':'/cache','TMPDIR':'/cache/tmp','LANG':'C.UTF-8','PYTHONNOUSERSITE':'1','PYTHONDONTWRITEBYTECODE':'1','HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','HF_HUB_DISABLE_TELEMETRY':'1','HF_HOME':'/cache/hf','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','USE_TORCH':'0','USE_TF':'0'}
    os.environ.clear()
    os.environ.update(allowed)
    pathlib.Path('/cache/tmp').mkdir()
    for key, cap in [(resource.RLIMIT_CPU,120),(resource.RLIMIT_AS,1073741824),(resource.RLIMIT_FSIZE,8388608),(resource.RLIMIT_CORE,0)]:
        resource.setrlimit(key, (cap, 67108864 if key == resource.RLIMIT_FSIZE else cap))
    class F(ctypes.Structure):
        _fields_ = [('code',ctypes.c_ushort),('jt',ctypes.c_ubyte),('jf',ctypes.c_ubyte),('k',ctypes.c_uint)]
    class P(ctypes.Structure):
        _fields_ = [('len',ctypes.c_ushort),('filter',ctypes.POINTER(F))]
    deny = [41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,288,299,307,425,426,427,438,101,310,311,321,303,304,298,323]
    code = [F(0x20,0,0,4),F(0x15,1,0,0xc000003e),F(0x06,0,0,0x80000000),F(0x20,0,0,0),F(0x45,0,1,0x40000000),F(0x06,0,0,0x80000000)]
    for n in deny:
        code.extend([F(0x15,0,1,n),F(0x06,0,0,0x00050000|errno.EPERM)])
    code.append(F(0x06,0,0,0x7fff0000))
    arr = (F * len(code))(*code)
    prog = P(len(code), arr)
    lib = ctypes.CDLL(None, use_errno=True)
    assert lib.prctl(38,1,0,0,0) == 0 and lib.prctl(22,2,ctypes.byref(prog),0,0) == 0

KNOWN_EXCEPTIONS = frozenset(('AssertionError','ValueError','TypeError','KeyError','FileNotFoundError','FileExistsError','PermissionError','OSError','TimeoutError','TimeoutExpired','CalledProcessError','RuntimeError','KeyboardInterrupt','SystemExit'))
def exception_class(exc):
    name = type(exc).__name__
    return name if name in KNOWN_EXCEPTIONS else 'OTHER'

def capture_error(errors, operation, channel, exc):
    if len(errors) < 24:
        errors.append({'operation':operation,'channel':channel,'exception_class':exception_class(exc)})

def worker_primary(stage, code, exc_class, returncode=None, timed_out=False):
    return {'stage':stage,'code':code,'exception_class':exc_class,'returncode':returncode,'timed_out':timed_out,'unknown':True,'retry':False}

class StageFailure(RuntimeError):
    def __init__(self, outcome):
        self.outcome = outcome
        super().__init__('STOP_UNKNOWN_NO_RETRY')

def open_capture(path):
    return path.open('xb',buffering=0)

class ChildIsolationFailure(RuntimeError):
    def __init__(self, receipt):
        self.receipt = receipt
        super().__init__('CHILD_ISOLATION_STOP')

def safe_fault(operation, exc, fd=None):
    v = {'operation':operation,'exception_class':exception_class(exc),
         'errno':exc.errno if isinstance(exc,OSError) and isinstance(exc.errno,int) else None}
    if fd is not None:
        v['fd'] = fd
    return v

def cache_only_child(stem, output_fds=()):
    """Trusted pre-exec only. Exact syscall failures and close faults stay separate."""
    if stem not in ('venv','install','counter'):
        raise ValueError('Fixed child scope')
    receipt = {'schema':'CACHE_ONLY_CHILD_V112','abi':None,'restricted':False,
               'cache_soft_limit_raised':False,'primary':None,'cleanup':[],
               'close_attempts':[],'output_fds_closed':[]}
    fds = []
    operation = 'OUTPUT_FD_CLOSE'
    def first(exc, op):
        if receipt['primary'] is None:
            receipt['primary'] = safe_fault(op,exc)
    try:
        for fd in output_fds:
            receipt['close_attempts'].append(fd)
            try:
                os.close(fd)
                receipt['output_fds_closed'].append(fd)
            except OSError as exc:
                # A descriptor already closed by Popen is equally unavailable.
                if exc.errno == errno.EBADF:
                    receipt['output_fds_closed'].append(fd)
                else:
                    raise
        operation = 'LIBC_LOAD'
        lib = ctypes.CDLL(None,use_errno=True)
        operation = 'LANDLOCK_ABI_QUERY'
        abi = lib.syscall(444,0,0,1)
        if abi < 0:
            raise OSError(ctypes.get_errno(),'Landlock query')
        receipt['abi'] = abi
        if abi < 3:
            operation = 'LANDLOCK_ABI_BELOW_3'
            raise OSError(errno.ENOTSUP,'Landlock ABI3 required')
        writes = (1<<1) | sum(1<<n for n in range(4,15))
        class Ruleset(ctypes.Structure):
            _fields_ = [('handled_access_fs',ctypes.c_uint64)]
        class Beneath(ctypes.Structure):
            _pack_ = 1
            _fields_ = [('allowed_access',ctypes.c_uint64),('parent_fd',ctypes.c_int32)]
        ruleset = Ruleset(writes)
        operation = 'LANDLOCK_CREATE'
        rulefd = lib.syscall(444,ctypes.byref(ruleset),ctypes.sizeof(ruleset),0)
        if rulefd < 0:
            raise OSError(ctypes.get_errno(),'Landlock create')
        fds.append(rulefd)
        operation = 'CACHE_OPEN'
        cachefd = os.open('/cache',os.O_PATH|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
        fds.append(cachefd)
        operation = 'CACHE_OWNER'
        if os.fstat(cachefd).st_uid != os.getuid():
            raise ValueError('Cache owner')
        rule = Beneath(writes,cachefd)
        operation = 'LANDLOCK_ADD_RULE'
        if lib.syscall(445,rulefd,1,ctypes.byref(rule),0) != 0:
            raise OSError(ctypes.get_errno(),'Landlock rule')
        operation = 'NO_NEW_PRIVS'
        if lib.prctl(38,1,0,0,0) != 0:
            raise OSError(ctypes.get_errno(),'No new privileges')
        operation = 'LANDLOCK_RESTRICT'
        if lib.syscall(446,rulefd,0) != 0:
            raise OSError(ctypes.get_errno(),'Landlock restrict')
        receipt['restricted'] = True
        if stem == 'install':
            operation = 'CACHE_LIMIT_RAISE'
            resource.setrlimit(resource.RLIMIT_FSIZE,(67108864,67108864))
            receipt['cache_soft_limit_raised'] = True
    except BaseException as exc:
        first(exc,operation)
    finally:
        while fds:
            fd = fds.pop()
            receipt['close_attempts'].append(fd)
            try:
                os.close(fd)
            except BaseException as exc:
                receipt['cleanup'].append(safe_fault('LANDLOCK_FD_CLOSE',exc,fd))
                first(exc,'LANDLOCK_FD_CLOSE')
    if receipt['primary'] is not None:
        raise ChildIsolationFailure(receipt)
    return receipt

def child_preexec(stem, report_fd, output_fds):
    """Only a bounded public receipt pipe survives until exec; never output FDs."""
    try:
        os.set_inheritable(report_fd,False)  # kernel closes at exec; not inherited.
        try:
            receipt = cache_only_child(stem,output_fds)
        except ChildIsolationFailure as exc:
            receipt = exc.receipt
        except BaseException as exc:
            receipt = {'schema':'CACHE_ONLY_CHILD_V112','abi':None,'restricted':False,
                       'cache_soft_limit_raised':False,'primary':safe_fault('PREEXEC',exc),
                       'cleanup':[],'close_attempts':[],'output_fds_closed':[]}
        raw = json.dumps(receipt,sort_keys=True,allow_nan=False).encode()+b'\n'
        if len(raw)>4096 or os.write(report_fd,raw)!=len(raw):
            os._exit(125)
        if receipt['primary'] is not None:
            os._exit(126)
    except BaseException:
        os._exit(125)
    # No explicit close: CLOEXEC owns the child receipt FD from this point.
    # On failure _exit closes it. Parent has its own once-only close custody.


def run(argv, stem, deadline):
    """Fixed work/cleanup deadlines, observed return retained, once-only closes."""
    if stem not in ('venv','install','counter'):
        raise ValueError('Fixed subprocess only')
    stage = {'venv':'BEFORE_VENV','install':'BEFORE_INSTALL','counter':'BEFORE_COUNTER'}[stem]
    work_deadline = deadline-2.0
    t = {'returncode':None,'original_returncode':None,'terminal_observed':False,
         'exception_class':None,'timed_out':False,'primary':None,'capture_failures':[],
         'cleanup':[],'streams':{},'isolation':None,'kill_attempts':0,'wait_attempts':0,
         'close_attempts':[]}
    handles, data = {}, {'stdout':bytearray(),'stderr':bytearray()}
    seen = {'stdout':0,'stderr':0}
    proc = None
    sel = None
    custody_r = custody_w = None
    started = False
    initialized = set()
    def failure(code, exc, timed=False):
        if t['primary'] is None:
            t['exception_class'] = exception_class(exc)
            t['timed_out'] = timed
            t['primary'] = worker_primary(stage,code,t['exception_class'],t['returncode'],timed)
    def observed(rc):
        if rc is not None and not t['terminal_observed']:
            t['returncode'] = t['original_returncode'] = rc
            t['terminal_observed'] = True
            if rc != 0 and t['primary'] is None:
                t['primary'] = worker_primary(stage,'WORKER_NONZERO','CalledProcessError',rc)
    def cleanup_fault(op,channel,exc):
        if len(t['cleanup'])<24:
            t['cleanup'].append(dict(safe_fault(op,exc),channel=channel))
        capture_error(t['capture_failures'],op,channel,exc)
        failure('CAPTURE_FAILURE',exc)
    def close_fd(fd,label):
        if fd is not None:
            t['close_attempts'].append(label)
            try:
                os.close(fd)
            except BaseException as exc:
                cleanup_fault('FD_CLOSE',label,exc)
    try:
        if time.monotonic()>=work_deadline:
            raise subprocess.TimeoutExpired(argv,0)
        sel = selectors.DefaultSelector()
        for channel in data:
            handles[channel] = open_capture(R/(stem+'.'+channel))
        custody_r,custody_w = os.pipe()
        output_fds = tuple(h.fileno() for h in handles.values())
        try:
            proc = subprocess.Popen(argv,env=dict(os.environ),stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True,
                pass_fds=(custody_w,),preexec_fn=lambda:child_preexec(stem,custody_w,output_fds))
            started = True
        finally:
            close_fd(custody_w,'custody_write_parent')
            custody_w = None
        os.set_blocking(custody_r,False)
        raw = os.read(custody_r,4097)
        if len(raw)>4096 or not raw.endswith(b'\n'):
            raise ValueError('Missing bounded child receipt')
        custody = json.loads(raw)
        t['isolation'] = custody
        if custody.get('schema')!='CACHE_ONLY_CHILD_V112':
            raise ValueError('Child receipt schema')
        if custody.get('primary') is not None:
            p = custody['primary']
            t['primary'] = worker_primary(stage,'ISOLATION_FAILURE',p['exception_class'])
        elif (custody.get('restricted') is not True or custody.get('abi',0)<3
              or custody.get('cache_soft_limit_raised') != (stem=='install')
              or custody.get('output_fds_closed')!=list(output_fds)):
            raise ValueError('Incomplete child restriction')
        for channel in data:
            pipe = getattr(proc,channel)
            os.set_blocking(pipe.fileno(),False)
            sel.register(pipe,selectors.EVENT_READ,channel)
            initialized.add(channel)
        while sel.get_map() and t['primary'] is None and time.monotonic()<work_deadline:
            for key,_ in sel.select(min(.05,max(0,work_deadline-time.monotonic()))):
                piece = os.read(key.fileobj.fileno(),65536)
                if not piece:
                    sel.unregister(key.fileobj)
                    continue
                channel = key.data
                seen[channel] += len(piece)
                data[channel].extend(piece[:max(0,65536-len(data[channel]))])
        if t['primary'] is None:
            if sel.get_map() or time.monotonic()>=work_deadline:
                raise subprocess.TimeoutExpired(argv,0)
            # EOF does not imply child termination. Use the actual work deadline.
            t['wait_attempts'] += 1
            observed(proc.wait(timeout=max(0,work_deadline-time.monotonic())))
    except BaseException as exc:
        timed = isinstance(exc,subprocess.TimeoutExpired)
        failure('DEADLINE' if timed else ('CAPTURE_FAILURE' if started else 'SPAWN_FAILURE'),exc,timed)
        capture_error(t['capture_failures'],'RUN_OR_SPAWN','terminal',exc)
        # Popen can fail before returning a process object. Preserve any child
        # custody which made it out, without classifying generic error as ABI absence.
        if not started and custody_r is not None:
            try:
                os.set_blocking(custody_r,False)
                raw = os.read(custody_r,4097)
                if raw.endswith(b'\n') and len(raw)<=4096:
                    t['isolation'] = json.loads(raw)
            except BaseException as ce:
                cleanup_fault('CUSTODY_READ_AFTER_SPAWN','terminal',ce)
    finally:
        close_fd(custody_w,'custody_write_parent')
        close_fd(custody_r,'custody_read_parent')
    if proc is not None and not t['terminal_observed']:
        alive = False
        try:
            rc = proc.poll()
            observed(rc)
            alive = rc is None
        except BaseException as exc:
            cleanup_fault('POLL','terminal',exc)
        if alive:
            try:
                t['kill_attempts'] += 1
                proc.kill()
            except BaseException as exc:
                cleanup_fault('KILL','terminal',exc)
            try:
                t['wait_attempts'] += 1
                observed(proc.wait(timeout=max(0,deadline-time.monotonic())))
            except BaseException as exc:
                cleanup_fault('WAIT_REAP','terminal',exc)
        if not t['terminal_observed']:
            failure('TERMINAL_UNKNOWN',RuntimeError('Terminal not observed'))
    if sel is not None:
        try:
            sel.close()
        except BaseException as exc:
            cleanup_fault('SELECTOR_CLOSE','terminal',exc)
    if proc is not None:
        for channel in data:
            pipe = getattr(proc,channel,None)
            if pipe is not None:
                t['close_attempts'].append('pipe_'+channel)
                try:
                    pipe.close()
                except BaseException as exc:
                    cleanup_fault('PIPE_CLOSE',channel,exc)
    for channel,handle in handles.items():
        closed = False
        saved = False
        if started:
            try:
                view = memoryview(data[channel])
                while view:
                    n = handle.write(view)
                    if not n:
                        raise OSError('Bounded stream write')
                    view = view[n:]
                saved = True
            except BaseException as exc:
                cleanup_fault('CHANNEL_SAVE',channel,exc)
        for op,action in [('FLUSH',handle.flush),('FSYNC',lambda:os.fsync(handle.fileno()))]:
            try:
                action()
            except BaseException as exc:
                cleanup_fault(op,channel,exc)
        t['close_attempts'].append('capture_'+channel)
        try:
            handle.close()
            closed = True
        except BaseException as exc:
            cleanup_fault('CLOSE',channel,exc)
        if closed and started and saved and channel in initialized:
            try:
                raw = (R/(stem+'.'+channel)).read_bytes()
                t['streams'][channel] = {'available':True,'bytes':len(raw),'sha256':sha(raw),
                    'truncated':seen[channel]>len(data[channel])}
            except BaseException as exc:
                cleanup_fault('READBACK',channel,exc)
    for channel in data:
        t['streams'].setdefault(channel,{'available':False,'bytes':None,'sha256':None,'truncated':None})
    if t['primary'] is None and any(v['truncated'] for v in t['streams'].values()):
        failure('CAPTURE_FAILURE',RuntimeError('Truncated channel'))
    try:
        emit(stem+'.terminal.json',t)
    except BaseException as exc:
        cleanup_fault('TERMINAL_SAVE','terminal',exc)
    if t['primary'] is not None:
        raise StageFailure(t)
    return t


def finish_worker(primary, captures, stage, counter_complete=False):
    """Return the first result even when no durable capture remains possible."""
    if primary is None and captures:
        primary = worker_primary(stage,'CAPTURE_FAILURE',captures[0]['exception_class'])
    if primary is not None:
        try:
            emit('worker-primary.json',{'primary':primary,'capture_failure':bool(captures)})
        except BaseException as exc:
            capture_error(captures,'PRIMARY_SAVE','terminal',exc)
    completion = ('COUNTER115_PENDING_HOST_REVIEW' if counter_complete else 'DIAGNOSTIC_ONLY_NO_COUNTER') if primary is None and not captures else 'STOP_UNKNOWN_NO_RETRY'
    terminal = {'primary':primary,'capture_failure':bool(captures),'completion':completion,'exit_code':0 if primary is None and not captures else 1}
    try:
        emit('worker-terminal.json',terminal)
    except BaseException as exc:
        capture_error(captures,'WORKER_TERMINAL_SAVE','terminal',exc)
        if primary is None:
            primary = worker_primary(stage,'CAPTURE_FAILURE',exception_class(exc))
    return {'primary':primary,'capture_failure':bool(captures),'capture_failures':captures,'exit_code':0 if primary is None and not captures else 1,'durability_unknown':bool(captures),'retry':False}

def main():
    start = time.monotonic()
    deadline = start + 170
    primary = None
    cleanup = []
    stage = 'ENVIRONMENT'
    counter_complete = False
    try:
        restrict()
        go = wait('GO.json', min(deadline, start + 30))
        assert sys.version_info[:2] == (3,12) and time.time() < go['absolute_deadline_utc']
        raw = (I / 'manifest.json').read_bytes()
        assert sha(raw) == go['manifest_sha256']
        m = json.loads(raw)
        counter_mode = go.get('counter115') is not None
        assert m['mode'] == 'PUBLIC_INPUTS_ONLY_PRECOUNTER_DIAGNOSTIC'
        assert all(m[k] is False for k in ('counter_allowed','private_vendor_allowed','model_allowed'))
        if counter_mode:assert m['counter116']['activation']=='TYPED_CURRENT_NATIVE_PRODUCER_ONLY'
        req = (I / 'request.json').read_bytes()
        assert len(req) == 4935 and sha(req) == m['request_sha256']
        assert sha((I / 'requirements.lock').read_bytes()) == m['lock_sha256']
        stage = 'QUALIFICATION'
        with (R / 'permitted.synthetic').open('xb') as f:
            f.write(b'synthetic')
        assert (R / 'permitted.synthetic').read_bytes() == b'synthetic'
        denied = {}
        for name, action in [('host_file',lambda:pathlib.Path(go['host_sentinel']).read_bytes()),('root_write',lambda:pathlib.Path('/etc/traceharbor-denied').write_text('synthetic')),('socket',lambda:socket.socket(socket.AF_INET,socket.SOCK_STREAM))]:
            try:
                action()
                raise AssertionError('Containment qualification failed')
            except OSError as exc:
                denied[name] = exc.errno
        assert denied['host_file'] in (errno.ENOENT, errno.EACCES, errno.EPERM)
        assert denied['socket'] == errno.EPERM and denied['root_write'] in (errno.EROFS,errno.EACCES,errno.EPERM)
        emit('qualification.json', {'case1_permitted_read_write':True,'case2_denial':denied,'credential_env_present':False})
        intent = {'source_sha':go['source_sha'],'manifest_sha256':go['manifest_sha256'],'once_receipt_sha256':go['once_receipt_sha256'],'runtime':m['runtime']['immutable_image'],'request_sha256':m['request_sha256'],'lock_sha256':m['lock_sha256'],'absolute_deadline_utc':go['absolute_deadline_utc'],'output_absent':go['output_absent'],'mode':m['mode']}
        emit('intent.json', intent)
        with (R / 'qualification.ready').open('xb'):
            pass
        approval = wait('INSTALL_GO.json', deadline)
        assert approval == {'intent_sha256':sha((R / 'intent.json').read_bytes())}
        assert time.time() < go['absolute_deadline_utc']
        stage = 'BEFORE_VENV'
        emit('beforevenv.json', {'stage':stage,'closed':True})
        run([sys.executable,'-m','venv','/cache/env'], 'venv', deadline)
        stage = 'BEFORE_INSTALL'
        emit('beforeinstall.json', {'stage':stage,'closed':True})
        run(['/cache/env/bin/python','-m','pip','install','--no-index','--no-deps','--require-hashes','--find-links=/wheels','-r','/inputs/requirements.lock'], 'install', deadline)
        stage = 'AFTER_INSTALL'
        emit('afterinstall.json', {'stage':stage,'closed':True})
        assert time.monotonic() <= deadline and time.time() <= go['absolute_deadline_utc']
        if counter_mode:
            import importlib.util
            spec=importlib.util.spec_from_file_location('private_counter115','/driver/counter115.py')
            bridge=importlib.util.module_from_spec(spec);spec.loader.exec_module(bridge)
            stage='BEFORE_COUNTER'
            bridge.worker_ready_and_count(sys.modules[__name__],go,m,deadline)
            counter_complete=True;stage='AFTER_COUNTER'
        emit('complete.json', {'type':'COUNTER115_PENDING_HOST_REVIEW' if counter_complete else 'DIAGNOSTIC_ONLY_NO_COUNTER','intent_sha256':approval['intent_sha256']})
    except StageFailure as exc:
        primary = exc.outcome['primary']
        cleanup.extend(exc.outcome['capture_failures'])
    except BaseException as exc:
        if hasattr(exc,'read_custody'):
            # Original read/pin primary and uncertain close survive separately.
            try:emit('counter116.read-custody.json',exc.read_custody)
            except BaseException as ce:capture_error(cleanup,'READ_CUSTODY_SAVE','terminal',ce)
            p=exc.read_custody['primary']
            primary=worker_primary(stage,'WORKER_FAILURE',p['exception_class'] if p is not None else 'OSError')
            for c in exc.read_custody['cleanup']:capture_error(cleanup,'CLOSE','terminal',OSError(c.get('errno') or 5,'Counter read close'))
        else:
            primary = worker_primary(stage,'WORKER_FAILURE',exception_class(exc))
    return finish_worker(primary,cleanup,stage,counter_complete)

if __name__ == '__main__':
    outcome = main()
    try:
        print(json.dumps(outcome,sort_keys=True,allow_nan=False))
    except BaseException:
        outcome['exit_code'] = 1
    sys.exit(outcome['exit_code'])
