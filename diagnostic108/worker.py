"""Private candidate108. Standard-library driver; stops after offline installation."""
import ctypes, errno, hashlib, json, os, pathlib, resource, socket, subprocess, sys, time
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
        resource.setrlimit(key, (cap, cap))
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

def run(argv, stem, deadline):
    """Latch child result before every capture/cleanup action; no retry."""
    if stem not in ('venv','install'):
        raise ValueError('Fixed subprocess only')
    stage = 'BEFORE_VENV' if stem == 'venv' else 'BEFORE_INSTALL'
    t = {'returncode':None,'exception_class':None,'timed_out':False,'primary':None,'capture_failures':[],'streams':{}}
    handles = {}
    started = False
    try:
        for channel in ('stdout','stderr'):
            handles[channel] = open_capture(R/(stem+'.'+channel))
        result = subprocess.run(argv,env=dict(os.environ),stdin=subprocess.DEVNULL,stdout=handles['stdout'],stderr=handles['stderr'],timeout=max(.001,deadline-time.monotonic()),close_fds=True)
        started = True
        t['returncode'] = result.returncode
        if result.returncode != 0:
            t['primary'] = worker_primary(stage,'WORKER_NONZERO','CalledProcessError',result.returncode)
    except BaseException as exc:
        started = isinstance(exc,subprocess.TimeoutExpired)
        t['exception_class'] = exception_class(exc)
        t['timed_out'] = isinstance(exc,subprocess.TimeoutExpired)
        t['primary'] = worker_primary(stage,'DEADLINE' if t['timed_out'] else 'SPAWN_FAILURE',t['exception_class'],None,t['timed_out'])
    # Each operation, especially close, receives one attempt independently.
    for channel,handle in handles.items():
        closed = False
        try:
            handle.flush()
        except BaseException as exc:
            capture_error(t['capture_failures'],'FLUSH',channel,exc)
        try:
            os.fsync(handle.fileno())
        except BaseException as exc:
            capture_error(t['capture_failures'],'FSYNC',channel,exc)
        try:
            handle.close()
            closed = True
        except BaseException as exc:
            capture_error(t['capture_failures'],'CLOSE',channel,exc)
        if closed and started:
            try:
                raw = (R/(stem+'.'+channel)).read_bytes()
                t['streams'][channel] = {'available':True,'bytes':len(raw),'sha256':sha(raw),'truncated':False}
            except BaseException as exc:
                capture_error(t['capture_failures'],'READBACK',channel,exc)
    for channel in ('stdout','stderr'):
        t['streams'].setdefault(channel,{'available':False,'bytes':None,'sha256':None,'truncated':None})
    if t['primary'] is None and t['capture_failures']:
        t['primary'] = worker_primary(stage,'CAPTURE_FAILURE',t['capture_failures'][0]['exception_class'],t['returncode'])
    try:
        emit(stem+'.terminal.json',t)
    except BaseException as exc:
        capture_error(t['capture_failures'],'TERMINAL_SAVE','terminal',exc)
        if t['primary'] is None:
            t['primary'] = worker_primary(stage,'CAPTURE_FAILURE',exception_class(exc),t['returncode'])
    if t['primary'] is not None:
        raise StageFailure(t)
    return t

def finish_worker(primary, captures, stage):
    """Return the first result even when no durable capture remains possible."""
    if primary is None and captures:
        primary = worker_primary(stage,'CAPTURE_FAILURE',captures[0]['exception_class'])
    if primary is not None:
        try:
            emit('worker-primary.json',{'primary':primary,'capture_failure':bool(captures)})
        except BaseException as exc:
            capture_error(captures,'PRIMARY_SAVE','terminal',exc)
    completion = 'DIAGNOSTIC_ONLY_NO_COUNTER' if primary is None and not captures else 'STOP_UNKNOWN_NO_RETRY'
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
    try:
        restrict()
        go = wait('GO.json', min(deadline, start + 30))
        assert sys.version_info[:2] == (3,12) and time.time() < go['absolute_deadline_utc']
        raw = (I / 'manifest.json').read_bytes()
        assert sha(raw) == go['manifest_sha256']
        m = json.loads(raw)
        assert m['mode'] == 'PUBLIC_INPUTS_ONLY_PRECOUNTER_DIAGNOSTIC'
        assert all(m[k] is False for k in ('counter_allowed','model_allowed','private_vendor_allowed'))
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
        emit('complete.json', {'type':'DIAGNOSTIC_ONLY_NO_COUNTER','intent_sha256':approval['intent_sha256']})
    except StageFailure as exc:
        primary = exc.outcome['primary']
        cleanup.extend(exc.outcome['capture_failures'])
    except BaseException as exc:
        primary = worker_primary(stage,'WORKER_FAILURE',exception_class(exc))
    return finish_worker(primary,cleanup,stage)

if __name__ == '__main__':
    outcome = main()
    try:
        print(json.dumps(outcome,sort_keys=True,allow_nan=False))
    except BaseException:
        outcome['exit_code'] = 1
    sys.exit(outcome['exit_code'])
