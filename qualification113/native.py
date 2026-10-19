"""PREPARED native NEW three-case group. Execute only in independently admitted exact container."""
import pathlib,sys,os,json,time,resource,hashlib,importlib.util
s=importlib.util.spec_from_file_location('worker','/driver/worker.py')
w=importlib.util.module_from_spec(s);s.loader.exec_module(w)
ROOT=pathlib.Path('/output')
BINDING={k:os.environ['TRACE113_'+k.upper()] for k in ('source_sha','manifest_sha256','once_receipt_sha256','run_id','request_sha256')}
def run_case_command(name,code,stem='install',seconds=12):
 d=ROOT/name;d.mkdir();w.R=d
 try:return w.run([sys.executable,'-I','-c',code],stem,time.monotonic()+seconds)
 except w.StageFailure as e:return e.outcome
def main():
 assert sys.version_info[:2]==(3,12) and os.getuid()==65532
 # Same accepted worker seccomp and parent rlimits, before any child.
 w.restrict()
 assert resource.getrlimit(resource.RLIMIT_FSIZE)==(8388608,67108864)
 assert resource.getrlimit(resource.RLIMIT_AS)==(1073741824,1073741824)
 assert (pathlib.Path('/sys/fs/cgroup/memory.max').read_text().strip())=='1073741824'
 assert pathlib.Path('/sys/fs/cgroup/pids.max').read_text().strip()=='64'
 cpu=pathlib.Path('/sys/fs/cgroup/cpu.max').read_text().split();assert int(cpu[0])==int(cpu[1])
 v=os.statvfs('/cache');assert v.f_frsize*v.f_blocks==536870912
 v=os.statvfs('/output');assert v.f_frsize*v.f_blocks==8388608
 results=[]
 code1="""import os,resource,json,hashlib
p='/cache/native112-9MiB.public'
with open(p,'xb') as f:
 for _ in range(9):f.write(b'x'*1048576)
h=hashlib.sha256()
with open(p,'rb') as f:
 for b in iter(lambda:f.read(65536),b''):h.update(b)
print(json.dumps({'bytes':os.stat(p).st_size,'sha256':h.hexdigest(),'file_limit':resource.getrlimit(resource.RLIMIT_FSIZE),'memory_limit':resource.getrlimit(resource.RLIMIT_AS)}))
"""
 a=run_case_command('case1',code1)
 passed=a['primary'] is None and a['terminal_observed'] and a['original_returncode']==0
 if passed:
  value=json.loads((ROOT/'case1/install.stdout').read_bytes())
  passed=value['bytes']==9437184 and value['file_limit']==[67108864,67108864] and value['memory_limit']==[1073741824,1073741824]
  h=hashlib.sha256()
  for _ in range(9):h.update(b'x'*1048576)
  passed &= value['sha256']==h.hexdigest()
 results.append({'case':1,'kind':'NATIVE','pass':bool(passed),'outcome':a,'cache_write':value if passed else None})
 if passed:
  (ROOT/'native112-sentinel.public').write_bytes(b'PUBLIC112')
  code2="""import os,json,errno
denied={}
for name,action in [('open_write',lambda:os.open('/output/native112-sentinel.public',os.O_WRONLY)),('truncate',lambda:os.truncate('/output/native112-sentinel.public',0)),('rename',lambda:os.rename('/cache/native112-9MiB.public','/output/native112-renamed.public'))]:
 try:action();denied[name]=False
 except OSError as e:denied[name]=e.errno in (errno.EACCES,errno.EPERM,errno.EXDEV,errno.EROFS)
output_fd=False
for name in os.listdir('/proc/self/fd'):
 try:output_fd |= os.readlink('/proc/self/fd/'+name).startswith('/output/')
 except FileNotFoundError:pass
print(json.dumps({'denied':denied,'output_fd_present':output_fd}),flush=True)
assert all(denied.values()) and not output_fd
os.write(1,b'X'*70000)
"""
  b=run_case_command('case2',code2)
  prefix=json.loads((ROOT/'case2/install.stdout').read_bytes().split(b'\n',1)[0])
  ok=b['primary'] is not None and b['primary']['code']=='CAPTURE_FAILURE' and b['original_returncode']==0 and b['streams']['stdout']['truncated'] is True and all(prefix['denied'].values()) and not prefix['output_fd_present'] and (ROOT/'native112-sentinel.public').read_bytes()==b'PUBLIC112'
  results.append({'case':2,'kind':'NATIVE','pass':ok,'denial':prefix,'outcome':b})
  late=run_case_command('case3-late',"import os,time;os.close(1);os.close(2);time.sleep(1)",stem='venv',seconds=5)
  timeout=run_case_command('case3-timeout',"import time;time.sleep(30)",stem='venv',seconds=3)
  ok=late['primary'] is None and late['original_returncode']==0 and timeout['primary']['code']=='DEADLINE' and timeout['terminal_observed'] and timeout['original_returncode']==-9 and timeout['kill_attempts']==1
  results.append({'case':3,'kind':'NATIVE_PROCESS_WITH_SYNTHETIC_FAULT_RECEIPT_REFERENCES','pass':ok,'late':late,'timeout':timeout,'fault_injection':'Use retained case112-originals.json/case3; do not rerun consumed source-stub group'})
 else:
  for i in [2,3]:results.append({'case':i,'kind':'NATIVE','pass':False,'status':'NOT_RUN_DEPENDENCY_CASE1'})
 proof={'binding':dict(BINDING,image='docker.io/library/python@sha256:2ed6491b93cd49272ee6de2b5a38440c3448360322c089fc23e370722d74179d'),'schema':'NEW112_NATIVE_GROUP_V1','cases':results,'all_pass':all(r['pass'] for r in results),'counter':0,'model':0,'install':0,'downloaded_import':0}
 print(json.dumps(proof,sort_keys=True,allow_nan=False),flush=True)
 return 0 if proof['all_pass'] else 1
if __name__=='__main__':
 try:rc=main()
 except BaseException as e:
  print(json.dumps({'schema':'NEW112_NATIVE_GROUP_V1','all_pass':False,'exception_class':type(e).__name__,'native_gate':'UNKNOWN_OR_FAIL_NO_RETRY','cases_may_be_partial':True}),flush=True);rc=1
 sys.exit(rc)

