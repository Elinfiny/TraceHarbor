"""SOURCE_ONLY future read-only capability collector. Not executed in310.
Versions are probes, never UI/service/sandbox qualification. No install or provider I/O.
"""
import base64,os,sys,json,hashlib,pathlib,subprocess,time,signal,resource,selectors,stat
MAX_OUTPUT=65536
def need(v,m):
 if not v:raise RuntimeError(m)
def read(path,cap=65536):
 with open(path,'rb') as f:b=f.read(cap+1)
 need(len(b)<=cap,'READ_BOUND:'+str(path));return b
def hashed(path):
 p=pathlib.Path(path);rp=p.resolve(strict=True);st=rp.stat();need(stat.S_ISREG(st.st_mode),'REGULAR_FILE')
 h=hashlib.sha256();n=0
 with rp.open('rb')as f:
  first=f.read(4);h.update(first);n+=len(first)
  while True:
   b=f.read(65536)
   if not b:break
   h.update(b);n+=len(b)
 end=rp.stat();need((st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns)==(end.st_dev,end.st_ino,end.st_size,end.st_mtime_ns)and n==st.st_size,'FILE_DRIFT')
 return {'requested':str(p),'realpath':str(rp),'bytes':n,'sha256':h.hexdigest(),'elf':first==b'\x7fELF','mode':oct(st.st_mode&0o7777)}
def probe(argv):
 need(type(argv)is list and len(argv)==2 and argv[1]=='--version','VERSION_ONLY')
 def limits():resource.setrlimit(resource.RLIMIT_AS,(100663296,100663296));os.umask(0o077)
 p=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True,env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','HOME':'/nonexistent'},preexec_fn=limits)
 sel=selectors.DefaultSelector();parts={'stdout':bytearray(),'stderr':bytearray()};started=time.monotonic();error=None
 for name,f in [('stdout',p.stdout),('stderr',p.stderr)]:os.set_blocking(f.fileno(),False);sel.register(f,selectors.EVENT_READ,name)
 try:
  while sel.get_map():
   if time.monotonic()-started>5:raise RuntimeError('TIMEOUT')
   for k,_ in sel.select(0.1):
    b=os.read(k.fileobj.fileno(),4096)
    if not b:sel.unregister(k.fileobj);continue
    room=4096-sum(len(v)for v in parts.values());parts[k.data].extend(b[:room]);need(len(b)<=room,'COMBINED_OUTPUT_BOUND_PREFIX_ONLY')
  rc=p.wait(timeout=max(.01,5-(time.monotonic()-started)))
 except BaseException as e:
  error=type(e).__name__+':'+str(e)
  try:os.killpg(p.pid,signal.SIGKILL)
  except ProcessLookupError:pass
  rc=p.wait(timeout=2)
 finally:sel.close();p.stdout.close();p.stderr.close()
 return {'argv':argv,'exit':rc,'error':error,'elapsed_s':round(time.monotonic()-started,6),'raw_streams':{name:{'encoding':'base64','data':base64.b64encode(bytes(buf)).decode(),'sha256':hashlib.sha256(bytes(buf)).hexdigest(),'bytes':len(buf),'completeness':'COMPLETE' if error is None else 'RETAINED_PREFIX_ONLY'} for name,buf in parts.items()},'child_AS':100663296,'launch_scope':'VERSION_PROBE_ONLY_NOT_SERVICE_OR_UI','raw_complete':error is None}
DEFERRED_VERSION_SLOTS=frozenset({'node','chrome_ELF','chromedriver'})
def collect_binary(name,path):
 f=hashed(path)
 if name=='chrome_wrapper':f['version_probe']={'state':'NOT_RUN_WRAPPER_IS_NOT_ELF','calls':0}
 else:
  need(f['elf'],'EXPECTED_ELF_NOT_WRAPPER')
  if name in DEFERRED_VERSION_SLOTS:f['version_probe']={'state':'DEFERRED_NOT_QUALIFIED','calls':0,'reason':'Known96MiBASprofile failure class; future independent kernel worker320MiB/swap0 plus separateAS8GiB admission required. Passive hash/path is not a version.'}
  else:f['version_probe']=probe([f['realpath'],'--version'])
 return f

def main():
 need(os.getuid()==1001 and os.getgid()==1001,'NONROOT_NATIVE_UID_GID')
 resource.setrlimit(resource.RLIMIT_AS,(67108864,100663296));os.umask(0o077)
 # Only an explicitly reviewed future ticket may allow this new capability lane.
 a=json.loads(read(sys.argv[1],16384));need(a.get('schema')=='TRACE310_READONLY_CAPABILITY_ADMISSION_V1'and a.get('state')=='ADMITTED_ONCE','FUTURE_ADMISSION_REQUIRED')
 need(a.get('parent')=='68b2f8476b2f0fddf1d9fd9bfdaa6d1a338146c7'and a.get('attempt')==1 and a.get('max_jobs')==1 and a.get('app')is False,'BOUND_SCOPE')
 need(a.get('source_sha256')==hashlib.sha256(read(__file__,32768)).hexdigest(),'FROZEN_COLLECTOR_SHA')
 need(a.get('whole_bytes')==536870912 and a.get('parent_AS_soft')==67108864 and a.get('parent_AS_hard')==100663296 and a.get('child_AS')==100663296,'FINITE_BUDGET')
 out={'schema':'TRACE310_READONLY_CAPABILITIES_V1','effect_id':a['effect_id'],'run_id':os.environ.get('GITHUB_RUN_ID'),'commit':os.environ.get('GITHUB_SHA'),'ImageVersion':os.environ.get('ImageVersion'),'ImageOS':os.environ.get('ImageOS'),'uid':os.getuid(),'gid':os.getgid(),'facts':{},'not_proved':['browser/UI launch','driver service','sandbox effectiveness','permission to create units','dedicated kernel worker320MiB','whole512MiB kernel domain'],'native_git_proof':a.get('native_git_commit_proof'),'effects':{'app':0,'driver_service':0,'browser_UI':0,'model':0,'network_requests':0,'system_configuration':0}}
 out['facts']['os_release']={'raw':read('/etc/os-release',8192).decode(),'sha256':hashlib.sha256(read('/etc/os-release',8192)).hexdigest()}
 slots={'node':'/usr/local/bin/node','python3':'/usr/bin/python3','systemctl':'/usr/bin/systemctl','systemd-run':'/usr/bin/systemd-run','chrome_wrapper':'/usr/bin/google-chrome','chrome_ELF':'/opt/google/chrome/chrome','chromedriver':'/usr/bin/chromedriver'}
 for name,path in slots.items():
  try:out['facts'][name]=collect_binary(name,path)
  except BaseException as e:out['facts'][name]={'state':'NOT_QUALIFIED','error':type(e).__name__+':'+str(e)}
 for name,path,cap in [('self_status','/proc/self/status',16384),('self_cgroup','/proc/self/cgroup',4096),('pid1_status','/proc/1/status',16384),('self_mountinfo','/proc/self/mountinfo',65536)]:
  try:
   raw=read(path,cap);out['facts'][name]={'sha256':hashlib.sha256(raw).hexdigest(),'raw':raw.decode()if name!='self_mountinfo'else None,'bytes':len(raw)}
  except BaseException as e:out['facts'][name]={'state':'NOT_AVAILABLE','error':str(e)}
 for pid in ['self','1']:
  out['facts']['namespaces_'+pid]={}
  for n in ['net','mnt','user','pid']:
   try:out['facts']['namespaces_'+pid][n]=os.readlink('/proc/'+pid+'/ns/'+n)
   except OSError as e:out['facts']['namespaces_'+pid][n]={'unavailable':str(e)}
 try:
  group=read('/proc/self/cgroup',4096).decode();line=next(x for x in group.splitlines()if x.startswith('0::'));relative=line[3:].lstrip('/');need('..'not in pathlib.PurePosixPath(relative).parts,'CGROUP_PATH');cg=pathlib.Path('/sys/fs/cgroup')/relative;out['facts']['current_cgroup']={'path':str(cg),'values':{}}
  for name in ['memory.max','memory.swap.max','memory.current','memory.events','cgroup.controllers','cgroup.events']:
   try:out['facts']['current_cgroup']['values'][name]=read(cg/name,4096).decode()
   except OSError as e:out['facts']['current_cgroup']['values'][name]={'unavailable':str(e)}
 except BaseException as e:out['facts']['current_cgroup']={'state':'NOT_AVAILABLE','error':str(e)}
 out['status']='READONLY_FACTS_NOT_UI_QUALIFICATION'
 out['memory']={'parent_AS':list(resource.getrlimit(resource.RLIMIT_AS)),'maxrss_self_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'maxrss_children_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'RSS_not_VmSize':True,'dedicated_worker_kernel_cap':'NOT_TESTED_NO_SERVICE_CREATED'}
 b=json.dumps(out,ensure_ascii=False,separators=(',',':')).encode();need(len(b)<=MAX_OUTPUT,'FINAL_OUTPUT_BOUND');sys.stdout.buffer.write(b+b'\n')
if __name__=='__main__':
 try:main()
 except BaseException as e:print(json.dumps({'stage':'CAPABILITY310','state':'REFUSED','error':type(e).__name__+':'+str(e)},separators=(',',':')));raise
