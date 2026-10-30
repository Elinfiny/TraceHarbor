"""Source-only candidate. Import starts no process and performs no I/O.
One worker at a time, exact shared bootstrap/limits for readiness and real work.
RLIMIT_AS bounds virtual addresses; the existing cgroup bounds aggregate RAM.
"""
import contextlib,fcntl,hashlib,json,os,re,selectors,signal,socket,stat,subprocess,sys,time
from pathlib import Path

ROOT=Path('/var/data/traceharbor-recovery004f')
HOST='traceharbor.onrender.com'
PROFILE={'id':'TRACEHARBOR-WORKER113','virtual_AS_bytes':1073741824,
 'aggregate_hard_bytes':536870912,'aggregate_abort_bytes':469762048,
 'memory_poll_seconds':0.05,'CPU_quota':50000,'CPU_period':100000,
 'workers':1,'retry':False,'output_stdout_bytes':65536,'output_stderr_bytes':131072,
 'modes':{'probe':{'cpu':3,'wall':6,'file_bytes':131072},
          'encode':{'cpu':180,'wall':600,'file_bytes':33554432},
          'decode':{'cpu':60,'wall':300,'file_bytes':33554432},
          'final-probe':{'cpu':3,'wall':6,'file_bytes':33554432}}}
ENV={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','PYTHONDONTWRITEBYTECODE':'1',
     'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1'}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
PROFILE_SHA256=digest(PROFILE);ENV_SHA256=digest(ENV)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
class WorkerRefusal(RuntimeError):pass

def private(path):
 s=Path(path).lstat()
 if not stat.S_ISDIR(s.st_mode)or s.st_uid!=os.getuid()or s.st_mode&0o077:raise WorkerRefusal('PRIVATE_DIRECTORY')
def read(path):
 p=Path(path);s=p.lstat()
 if not stat.S_ISREG(s.st_mode)or s.st_uid!=os.getuid()or s.st_mode&0o077 or s.st_size>65536:raise WorkerRefusal('PRIVATE_RECORD')
 return json.loads(p.read_bytes())
def exclusive(path,value):
 p=Path(path);private(p.parent);raw=json.dumps(value,sort_keys=True,separators=(',',':')).encode()
 fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'wb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 fd=os.open(p.parent,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
def directory(path):
 p=Path(path);p.mkdir(mode=0o700,parents=False,exist_ok=True);private(p);return p
def wrapper_environment():
 # Only validated nonsecret host metadata crosses the Python wrapper boundary.
 metadata={k:os.environ.get(k,'')for k in('RENDER','RENDER_EXTERNAL_HOSTNAME','RENDER_GIT_COMMIT')}
 if metadata['RENDER']!='true'or metadata['RENDER_EXTERNAL_HOSTNAME']!=HOST or not re.fullmatch('[a-f0-9]{40}',metadata['RENDER_GIT_COMMIT']):raise WorkerRefusal('EXACT_RENDER_IDENTITY')
 return dict(ENV,**metadata)
def identity():
 wrapper=wrapper_environment()
 return {'source_commit':wrapper['RENDER_GIT_COMMIT'],'instance':socket.gethostname(),'profile_sha256':PROFILE_SHA256,'environment_sha256':ENV_SHA256,'environment_sha256_scope':'MEDIA_BINARY_EXECVE_ONLY','wrapper_environment_sha256':digest(wrapper)}
def aggregate():
 p=Path('/sys/fs/cgroup')
 if Path('/proc/self/cgroup').read_text().strip()!='0::/':raise WorkerRefusal('CGROUP_LAYOUT_NOT_QUALIFIED')
 maximum=(p/'memory.max').read_text().strip();cpu=(p/'cpu.max').read_text().split()
 if maximum!=str(PROFILE['aggregate_hard_bytes'])or cpu!=['50000','100000']:raise WorkerRefusal('EXISTING_AGGREGATE_ENVELOPE_CHANGED')
 current=int((p/'memory.current').read_text());events=dict(x.split()for x in(p/'memory.events').read_text().splitlines())
 return {'hard_bytes':int(maximum),'current_bytes':current,'oom_kill':int(events.get('oom_kill',0))}
def binary_fingerprints():return {name:sha('/usr/bin/'+name)for name in('ffprobe','ffmpeg')}

def command(mode,operand):
 if mode not in PROFILE['modes']:raise WorkerRefusal('MODE')
 if operand=='preflight':
  return ['/usr/bin/ffmpeg','-hide_banner','-encoders']if mode=='encode'else['/usr/bin/ffmpeg','-version']if mode=='decode'else['/usr/bin/ffprobe','-version']
 if mode=='probe':
  p=Path(operand)
  if p not in {ROOT/'codec106/vp8/media.webm',ROOT/'native/media.webm'}:raise WorkerRefusal('FIXED_MEDIA_PATH')
  s=p.lstat()
  if not stat.S_ISREG(s.st_mode)or s.st_uid!=os.getuid()or s.st_mode&0o077 or not 0<s.st_size<=1048576:raise WorkerRefusal('PRIVATE_MEDIA_BOUND')
  return ['/usr/bin/ffprobe','-v','error','-threads','1','-protocol_whitelist','file,pipe','-count_frames','-show_packets','-show_entries','stream=codec_type,codec_name,width,height,nb_read_frames:format=duration:packet=codec_type,pts_time,duration_time','-of','json',str(p)]
 if operand!='run':raise WorkerRefusal('FIXED_AV_OPERAND')
 import recovery_av004f as av
 return av.commands(ROOT)[mode]

def redact_stderr(raw):
 text=raw[:131072].decode('utf8','replace');classes=[];library=None
 for needle,label in [('failed to map segment','LIBRARY_MAP_FAILED'),('cannot allocate memory','ALLOCATION_FAILED'),('no such file','FILE_OR_LIBRARY_UNAVAILABLE'),('invalid data','INVALID_DATA'),('unknown encoder','ENCODER_UNAVAILABLE'),('error while loading shared libraries','LOADER_FAILURE')]:
  if needle in text.lower():classes.append(label)
 m=re.search(r'error while loading shared libraries: ([A-Za-z0-9_.+-]{1,100}):',text)
 if m:library=m.group(1)
 return {'captured_bytes':len(raw),'captured_sha256':hashlib.sha256(raw).hexdigest(),'classes':classes,'library_basename':library,'other_text':'REDACTED'if raw else None}

def stop(proc):
 if proc.poll()is None:
  try:os.killpg(proc.pid,signal.SIGKILL)
  except ProcessLookupError:pass
 proc.wait(timeout=2)

def collect(proc,limit,clock=time.monotonic,memory=aggregate):
 """Drain both pipes with bounded buffers; never use unbounded communicate()."""
 started=clock();streams={'out':bytearray(),'err':bytearray()};sizes={'out':0,'err':0};peak=0;reason=None
 with selectors.DefaultSelector()as sel:
  for key,f in [('out',proc.stdout),('err',proc.stderr)]:os.set_blocking(f.fileno(),False);sel.register(f,selectors.EVENT_READ,key)
  while sel.get_map()or proc.poll()is None:
   try:current=memory()['current_bytes'];peak=max(peak,current)
   except Exception:reason='MEMORY_OBSERVATION_LOST';break
   if current>=PROFILE['aggregate_abort_bytes']:reason='AGGREGATE_MARGIN_EXHAUSTED';break
   if clock()-started>=limit['wall']:reason='WALL_EXHAUSTED';break
   for k,_ in sel.select(PROFILE['memory_poll_seconds']):
    raw=os.read(k.fileobj.fileno(),8192)
    if not raw:sel.unregister(k.fileobj);continue
    name=k.data;sizes[name]+=len(raw);bound=PROFILE['output_stdout_bytes']if name=='out'else PROFILE['output_stderr_bytes']
    room=max(0,bound-len(streams[name]));streams[name].extend(raw[:room])
    if sizes[name]>bound:reason='OUTPUT_EXHAUSTED';break
   if reason:break
  if reason:stop(proc)
  else:proc.wait(timeout=2)
 for f in(proc.stdout,proc.stderr):f.close()
 rc=proc.returncode
 stderr=redact_stderr(bytes(streams['err']));stderr.update(observed_bytes=sizes['err'],truncated=sizes['err']>len(streams['err']))
 return {'returncode':rc,'signal':-rc if rc is not None and rc<0 else None,'guard':reason,'elapsed_wall':clock()-started,'aggregate_peak_observed':peak,'stdout_bytes':sizes['out'],'stderr':stderr},bytes(streams['out'])

@contextlib.contextmanager
def serialized(root):
 directory(root);p=Path(root)/'worker.lock';fd=os.open(p,os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
 try:
  s=os.fstat(fd)
  if not stat.S_ISREG(s.st_mode)or s.st_uid!=os.getuid()or s.st_mode&0o077:raise WorkerRefusal('LOCK_CUSTODY')
  try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:raise WorkerRefusal('WORKER_BUSY_NO_DISPATCH')
  yield
 finally:os.close(fd)

def run(mode,operand,receipt,*,require_startup=True):
 wrapper=wrapper_environment();ident=identity();limit=PROFILE['modes'].get(mode)
 if not limit:raise WorkerRefusal('MODE')
 receipt=Path(receipt)
 if ROOT not in receipt.parents:raise WorkerRefusal('FIXED_RECEIPT_ROOT')
 initial=aggregate()
 if initial['current_bytes']>=PROFILE['aggregate_abort_bytes']:raise WorkerRefusal('NO_AGGREGATE_HEADROOM')
 if require_startup:assert_startup(ident)
 cmd=[sys.executable,str(Path(__file__).resolve()),'--child',mode,operand]
 with serialized(ROOT/'worker113'):
  receipt.mkdir(mode=0o700,exist_ok=False);private(receipt)
  exclusive(receipt/'reserved.json',{'state':'RESERVED_UNKNOWN_NO_RETRY','mode':mode,'operand':'NO_MEDIA'if operand=='preflight'else'FIXED_MEDIA_OR_AV','identity':ident,'limits':limit,'virtual_AS_bytes':PROFILE['virtual_AS_bytes'],'environment_sha256':ENV_SHA256,'environment_sha256_scope':'MEDIA_BINARY_EXECVE_ONLY','wrapper_environment_sha256':digest(wrapper),'argv_sha256':digest(cmd),'retry':False})
  try:
   proc=subprocess.Popen(cmd,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=wrapper,start_new_session=True)
   result,stdout=collect(proc,limit)
  except Exception as e:
   result={'returncode':None,'signal':None,'guard':'SPAWN_OR_MONITOR_ERROR','exception':type(e).__name__,'stderr':{'other_text':'REDACTED'}};stdout=b''
   if 'proc'in locals():stop(proc)
  finally:
   if 'proc'in locals():
    for stream in(proc.stdout,proc.stderr):
     if stream is not None:stream.close()
  try:after=aggregate();oom_delta=after['oom_kill']-initial['oom_kill']
  except Exception:after=initial;oom_delta=None;result['guard']=result.get('guard')or'MEMORY_OBSERVATION_LOST'
  result.update(identity=ident,limits=limit,virtual_AS_bytes=PROFILE['virtual_AS_bytes'],aggregate_hard_bytes=after['hard_bytes'],oom_kill_delta=oom_delta,retry=False)
  result['pass']=result['returncode']==0 and not result.get('guard')and result['oom_kill_delta']==0
  exclusive(receipt/'result.json',result)
  return result,stdout

def assert_startup(ident=None):
 ident=ident or identity();p=ROOT/'worker113/preflight'/ident['source_commit']/'qualified.json';v=read(p)
 if v.get('state')!='PASS_NO_MEDIA_NOT_ENCODER_QUALIFICATION'or v.get('identity')!=ident or v.get('binaries')!=binary_fingerprints()or set(v.get('modes',{}))!=set(PROFILE['modes'])or not all(v['modes'][m].get('pass')is True for m in PROFILE['modes']):raise WorkerRefusal('EXACT_STARTUP_PROFILE_REQUIRED')
 return v

def startup_once():
 ident=identity();private(ROOT);directory(ROOT/'worker113');base=directory(ROOT/'worker113/preflight');base=directory(base/ident['source_commit']);exclusive(base/'bundle-reserved.json',{'identity':ident,'mode_count':4,'media':False,'retry':False})
 before=binary_fingerprints();results={}
 for mode in PROFILE['modes']:
  result,stdout=run(mode,'preflight',base/mode,require_startup=False)
  result=dict(result);result['binary_metadata_present']=bool(re.search(rb'^\s*V\S*\s+libx264\b',stdout,re.M)and re.search(rb'^\s*A\S*\s+aac\b',stdout,re.M))if mode=='encode'else stdout.startswith(b'ffprobe version')or stdout.startswith(b'ffmpeg version')
  result['pass']=result['pass']and result['binary_metadata_present'];results[mode]=result
  if not result['pass']:break
 ok=set(results)==set(PROFILE['modes'])and all(x['pass']for x in results.values())and binary_fingerprints()==before
 value={'state':'PASS_NO_MEDIA_NOT_ENCODER_QUALIFICATION'if ok else'FAIL_CLOSED_NO_RETRY','identity':ident,'binaries':before,'modes':results,'media_read':False,'recorders':0,'AI':0,'retry':False};exclusive(base/'qualified.json',value);return value

def child(mode,operand):
 import resource
 import recovery004f as r
 if Path(r.policy()['root'])!=ROOT:raise WorkerRefusal('ROOT_POLICY_BINDING')
 if mode!='probe':
  import recovery_av004f
 limit=PROFILE['modes'].get(mode)
 if not limit:raise WorkerRefusal('MODE')
 cmd=command(mode,operand)
 resource.setrlimit(resource.RLIMIT_CPU,(limit['cpu'],)*2);resource.setrlimit(resource.RLIMIT_AS,(PROFILE['virtual_AS_bytes'],)*2);resource.setrlimit(resource.RLIMIT_FSIZE,(limit['file_bytes'],)*2);resource.setrlimit(resource.RLIMIT_CORE,(0,0))
 os.execve(cmd[0],cmd,ENV)
if __name__=='__main__':
 if len(sys.argv)==4 and sys.argv[1]=='--child':child(sys.argv[2],sys.argv[3])
 else:raise SystemExit('NO_DIRECT_STARTUP_OR_MEDIA_COMMAND')
