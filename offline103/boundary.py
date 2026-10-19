"""Trusted host boundary104; never resolves worker-controlled paths."""
import hashlib,json,os,stat,time,subprocess,selectors
ALLOWED={'permitted.synthetic','qualification.json','intent.json','count.json','verified.json','qualification.ready'}|{s+e for s in ('venv','install','counter') for e in ('.stdout','.stderr','.terminal.json')}
def sha(b):return hashlib.sha256(b).hexdigest()
def strict(raw):
    def pairs(items):
        d={}
        for k,v in items:
            if k in d:raise ValueError('Duplicate JSON member')
            d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in ()).throw(ValueError('Nonfinite JSON')))
class Output:
    def __init__(self,path):
        self.fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
        self.dev=os.fstat(self.fd).st_dev
    def close(self):os.close(self.fd)
    def opened(self,name):
        if name not in ALLOWED:raise ValueError('Unsafe output name')
        fd=os.open(name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK|os.O_CLOEXEC,dir_fd=self.fd)
        s=os.fstat(fd)
        if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1 or s.st_dev!=self.dev or s.st_size>8388608:
            os.close(fd);raise ValueError('Unsafe output object')
        return fd,s
    def read(self,name,cap=65536,optional=False):
        try:fd,before=self.opened(name)
        except FileNotFoundError:
            if optional:return None
            raise
        try:
            if before.st_size>cap:raise ValueError('Output cap exceeded')
            b=bytearray()
            while len(b)<=cap:
                part=os.read(fd,min(65536,cap+1-len(b)))
                if not part:break
                b.extend(part)
            after=os.fstat(fd)
            if len(b)>cap or len(b)!=after.st_size or (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns,before.st_nlink)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns,after.st_nlink):raise ValueError('Output changed during read')
            return bytes(b)
        finally:os.close(fd)
    def census(self):
        count=total=0
        with os.scandir(self.fd) as entries:
            for e in entries:
                count+=1
                if count>len(ALLOWED):raise ValueError('Too many output objects')
                fd,s=self.opened(e.name)
                try:total+=s.st_size
                finally:os.close(fd)
                if total>8388608:raise ValueError('Output total cap exceeded')
        return count,total
def validate_result(out,m,source,once,intent_raw,absolute):
    d=strict(out.read('verified.json',8192));intent=strict(intent_raw)
    fixed={'request_sha256':m['request_sha256'],'lock_sha256':m['lock_sha256'],'runtime':m['runtime']['immutable_image'],'source_sha':source,'external_once_receipt_sha256':once,'intent_sha256':sha(intent_raw),'native_or_model_authority':False}
    if set(d)!=set(fixed)|{'count','strict_under3000','result_sha256'}:raise ValueError('Result schema mismatch')
    if any(type(d[k]) is not type(v) or d[k]!=v for k,v in fixed.items()):raise ValueError('Result pins mismatch')
    if type(d['count']) is not int or not 0<=d['count']<=16384 or type(d['strict_under3000']) is not bool or d['strict_under3000']!=(d['count']<3000):raise ValueError('Result numeric mismatch')
    raw=out.read('count.json',8388608)
    if d['result_sha256']!=sha(raw):raise ValueError('Result bytes mismatch')
    full=strict(raw)
    if type(full) is not dict or set(full)!={'projection','provenance','result'}:raise ValueError('Counter document schema mismatch')
    projection,provenance,result=full['projection'],full['provenance'],full['result']
    if not all(type(v) is dict for v in (projection,provenance,result)):raise ValueError('Counter component type mismatch')
    if projection.get('full_request_canonical_sha256')!=m['request_sha256']:raise ValueError('Counter request mismatch')
    tokens=result.get('tokens');count=result.get('count');under=result.get('under_3000_input_tokens')
    if type(tokens) is not list or type(count) is not int or not 0<=count<=16384 or count!=len(tokens) or any(type(t) is not int or t<0 for t in tokens):raise ValueError('Counter token/count mismatch')
    if type(under) is not bool or under!=(count<3000) or count!=d['count'] or under is not d['strict_under3000']:raise ValueError('Counter summary mismatch')
    expected={'served_template_sha256':m['served_template_sha256'],'counter_version':'0.2.1','model':'nvidia/Nemotron-3_5-Lightning','public_artifact_revision':'a9904d24bcc1d289a1950fa9d2b978c47cf903b9','local_files_only':True,'trust_remote_code':False,'add_generation_prompt':True,'add_special_tokens':False}
    if any(type(provenance.get(k)) is not type(v) or provenance[k]!=v for k,v in expected.items()):raise ValueError('Counter provenance mismatch')
    if provenance.get('verified_model_file_sha256')!={v['name']:v['sha256'] for v in m['public_tokenizer']}:raise ValueError('Counter tokenizer mismatch')
    versions=provenance.get('runtime_versions')
    if type(versions) is not dict or any(versions.get(k)!=v for k,v in m['root_versions'].items()) or not str(versions.get('python','')).startswith('3.12.'):raise ValueError('Counter runtime mismatch')
    if intent['absolute_deadline_utc']!=absolute or time.time()>absolute:raise ValueError('Result expired')
    return {'count':count,'strict_under3000':under,'request_sha256':d['request_sha256'],'result_sha256':d['result_sha256'],'native_or_model_authority':False}
def private_record(root,name,value):
    fd=os.open(root/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'wb') as f:f.write(json.dumps(value,sort_keys=True,allow_nan=False).encode());f.flush();os.fsync(f.fileno())
def cleanup_once(root,cid,terminal):
    failures=[]
    commands=([('kill',['docker','kill',cid])] if terminal is None else [])+[('original-state',['docker','inspect','-f','{{json .State}}',cid]),('docker',['docker','logs',cid]),('remove',['docker','rm','-f',cid])]
    for stem,argv in commands:
        receipt={'step':stem,'utc':time.time(),'returncode':None,'streams':{}}
        proc=None;sel=selectors.DefaultSelector();fds={};start=time.monotonic()
        try:
            # Each stream is independently opened before spawn; absent capture is
            # reported, never replaced with a fabricated empty file.
            for channel in ('stdout','stderr'):
                try:fds[channel]=os.open(root/(stem+'.'+channel),os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
                except BaseException as exc:failures.append({'step':stem,'capture':channel,'type':type(exc).__name__})
            proc=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
            for channel in ('stdout','stderr'):
                pipe=getattr(proc,channel);os.set_blocking(pipe.fileno(),False);sel.register(pipe,selectors.EVENT_READ,channel);receipt['streams'][channel]={'captured_bytes':0,'truncated':False}
            while sel.get_map() and time.monotonic()-start<2:
                for key,_ in sel.select(.05):
                    data=os.read(key.fileobj.fileno(),65536);channel=key.data
                    if not data:sel.unregister(key.fileobj);continue
                    r=receipt['streams'][channel];available=max(0,65536-r['captured_bytes']);piece=data[:available]
                    if channel in fds:
                        try:os.write(fds[channel],piece)
                        except BaseException as exc:failures.append({'step':stem,'capture':channel,'type':type(exc).__name__});os.close(fds.pop(channel))
                    r['captured_bytes']+=len(piece);r['truncated']|=len(piece)!=len(data)
            if proc.poll() is None:proc.kill();receipt['timed_out']=True
            try:receipt['returncode']=proc.wait(timeout=.2)
            except subprocess.TimeoutExpired:receipt['terminal']='UNKNOWN'
            for key in list(sel.get_map().values()):receipt['streams'][key.data]['incomplete']=True
        except BaseException as exc:failures.append({'step':stem,'type':type(exc).__name__})
        finally:
            if proc is not None and proc.poll() is None:
                try:proc.kill()
                except BaseException as exc:failures.append({'step':stem,'kill_capture_process':type(exc).__name__})
            sel.close()
            for fd in fds.values():
                try:os.close(fd)
                except OSError:pass
            try:private_record(root,stem+'.terminal.json',receipt)
            except BaseException as exc:failures.append({'step':stem,'terminal_capture':type(exc).__name__})
    try:private_record(root,'cleanup.json',failures)
    except BaseException:pass
    return failures
