import os,sys
def _vm284(pid='self'):
 with open('/proc/'+str(pid)+'/status')as f:
  for line in f:
   if line.startswith('VmSize:'):return int(line.split()[1])*1024
 raise RuntimeError('VmSize not exposed')
_entry_vm284=_vm284()
if _entry_vm284>56*1048576:raise RuntimeError('STARTUP_VMSIZE_HEADROOM_FAILED')
import resource
_before_as284=resource.getrlimit(resource.RLIMIT_AS)
if _before_as284[1]!=resource.RLIM_INFINITY and _before_as284[1]<96*1048576:raise RuntimeError('INHERITED_AS_HARD_LIMIT_TOO_SMALL')
resource.setrlimit(resource.RLIMIT_AS,(64*1048576,96*1048576))
resource.setrlimit(resource.RLIMIT_CPU,(60,60))
resource.setrlimit(resource.RLIMIT_FSIZE,(16*1048576,16*1048576))
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
import json,hashlib,pathlib,subprocess,selectors,time,signal,re,pwd,shutil
_postimports_vm284=_vm284()
if _postimports_vm284>56*1048576:raise RuntimeError('POSTIMPORT_VMSIZE_HEADROOM_FAILED')
_parent_pid284=os.getpid()
_records284=[]
_memory284={'entry_VmSize':_entry_vm284,'postimports_VmSize':_postimports_vm284,'headroom_required':8388608,'parent_AS':list(resource.getrlimit(resource.RLIMIT_AS)),'child_AS':[100663296,100663296],'aggregate_private_AS_contract':167772160,'aggregate_sample_is_not_kernel_cap':True}
def _child_limits284():
 if os.getpid()==_parent_pid284:raise RuntimeError('NEVER_RAISE_AS_IN_PARENT')
 resource.setrlimit(resource.RLIMIT_AS,(96*1048576,96*1048576))
 resource.setrlimit(resource.RLIMIT_CPU,(5,5));resource.setrlimit(resource.RLIMIT_FSIZE,(16*1048576,16*1048576));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
def _group284(pgid):
 rows=[]
 for name in os.listdir('/proc'):
  if not name.isdigit():continue
  try:
   with open('/proc/'+name+'/stat')as f:tail=f.read().rpartition(') ')[2].split()
   if int(tail[2])==pgid and int(tail[3])==pgid:rows.append((int(name),_vm284(name)))
  except (OSError,ValueError,IndexError,RuntimeError):continue
 return rows
def _signal_own284(pgid,sig):
 rows=_group284(pgid)
 if rows:
  try:os.killpg(pgid,sig)
  except ProcessLookupError:pass
 return [pid for pid,vm in rows]
def bounded(argv,timeout=5,limit=2048,cwd=None,env=None):
 # One direct child at a time; inherited descendant AS caps plus owned-group
 # aggregate sampling. This is not a fabricated kernel memory.max lease.
 if timeout>5:timeout=5
 if not isinstance(argv,list)or not argv or not os.path.isabs(argv[0]):raise RuntimeError('ABSOLUTE_EXECUTABLE_REQUIRED')
 rec={'argv':argv,'parent_pid':_parent_pid284,'AS_parent_before':list(resource.getrlimit(resource.RLIMIT_AS)),'AS_child':[100663296,100663296],'timeout_s':timeout,'stdout':'','stderr':'','exit':'NOT_EXPOSED','failure':None,'own_cleanup':[],'peak_observed_group_VmSize':0}
 out={'stdout':bytearray(),'stderr':bytearray()};s=selectors.DefaultSelector();p=None;start=time.monotonic()
 try:
  p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=cwd,env=env or {'PATH':'/usr/bin:/bin','LANG':'C.UTF-8'},start_new_session=True,preexec_fn=_child_limits284)
  rec['pid']=p.pid;s.register(p.stdout,selectors.EVENT_READ,'stdout');s.register(p.stderr,selectors.EVENT_READ,'stderr')
  while s.get_map():
   if time.monotonic()-start>timeout:raise TimeoutError('CHILD_5S_BOUND')
   vm=sum(v for pid,v in _group284(p.pid));rec['peak_observed_group_VmSize']=max(vm,rec['peak_observed_group_VmSize'])
   if _vm284()+vm>167772160:raise MemoryError('OWNED_GROUP_OBSERVED_AS160_EXCEEDED')
   for k,_ in s.select(.01):
    b=os.read(k.fileobj.fileno(),8192)
    if not b:s.unregister(k.fileobj);continue
    total=sum(map(len,out.values()));take=max(0,limit-total);out[k.data].extend(b[:take])
    if len(b)>take:raise RuntimeError('CHILD_OUTPUT_BOUND')
  p.wait(timeout=max(.01,timeout-(time.monotonic()-start)))
  if _group284(p.pid):raise RuntimeError('OWNED_DESCENDANT_REMAINS_AFTER_LEADER')
 except BaseException as e:
  rec['failure']='BOUNDED_PROBE_FAILED/'+type(e).__name__+':'+str(e)
  if p is not None:
   rec['own_cleanup'].append({'TERM':_signal_own284(p.pid,signal.SIGTERM)})
   try:p.wait(timeout=.2)
   except subprocess.TimeoutExpired:
    rec['own_cleanup'].append({'KILL':_signal_own284(p.pid,signal.SIGKILL)});p.wait(timeout=1)
   if _group284(p.pid):
    rec['own_cleanup'].append({'KILL_REMAINING_SAME_OWNED_SESSION':_signal_own284(p.pid,signal.SIGKILL)})
   rec['remaining_owned_members_at_return']=[pid for pid,vm in _group284(p.pid)]
 finally:
  if p is not None:
   rec['exit']=p.returncode
   for f in [p.stdout,p.stderr]:
    if f:f.close()
  s.close()
  for k,b in out.items():rec[k]=b.decode(errors='replace')
  rec['elapsed_s']=round(time.monotonic()-start,6);rec['AS_parent_after']=list(resource.getrlimit(resource.RLIMIT_AS));_records284.append(rec)
 if rec['AS_parent_after']!=[67108864,100663296]:raise RuntimeError('PARENT_AS_CHANGED')
 return rec

LIMIT=335544320
SYSTEMCTL=None
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb')as f:
  while b:=f.read(8192):h.update(b)
 return h.hexdigest()
def command(source,out,event,uid,gid,run,commit,executables=None):
 need(isinstance(executables,dict),'qualified executable map required')
 for k in ['node','python3','systemd-run','systemctl']:
  x=executables.get(k,{});need(x.get('state')=='QUALIFIED'and re.fullmatch(r'/[A-Za-z0-9_./+-]+',x.get('path',''))and re.fullmatch(r'[0-9a-f]{64}',x.get('sha256','')),'unqualified executable '+k)
 need(type(uid)is int and uid>0 and type(gid)is int and gid>0,'nonroot runner required')
 need(re.fullmatch(r'[0-9]{1,20}',run)and re.fullmatch(r'[0-9a-f]{40}',commit),'bad event identity')
 unit='traceharbor-ui280-a2-'+run+'.service'
 props=['Type=exec','User='+str(uid),'Group='+str(gid),'RemainAfterExit=yes','MemoryAccounting=yes','MemoryMax='+str(LIMIT),'MemorySwapMax=0','TasksMax=96','RuntimeMaxSec=180','TimeoutStopSec=5','KillMode=control-group','SendSIGKILL=yes','PrivateNetwork=yes','PrivateTmp=yes','PrivateIPC=yes','NoNewPrivileges=yes','CapabilityBoundingSet=','AmbientCapabilities=','ProtectSystem=strict','ProtectHome=yes','ProtectControlGroups=yes','ProtectKernelTunables=yes','ProtectKernelModules=yes','ProtectKernelLogs=yes','RestrictSUIDSGID=yes','RestrictRealtime=yes','WorkingDirectory=/run/trace280-source','BindReadOnlyPaths='+source+':/run/trace280-source '+event+':/run/trace280-event.json','BindPaths='+out+':/run/trace280-out','ReadWritePaths=/run/trace280-out']
 env={'PATH':'/usr/bin:/bin:/usr/local/bin','HOME':'/run/trace280-out/home','LANG':'C.UTF-8','GITHUB_ACTIONS':'true','RUNNER_ENVIRONMENT':'github-hosted','GITHUB_EVENT_NAME':'create','GITHUB_RUN_ATTEMPT':'1','GITHUB_RUN_ID':run,'GITHUB_SHA':commit,'GITHUB_REPOSITORY':'Elinfiny/TraceHarbor','GITHUB_ACTOR_ID':'273768139','GITHUB_EVENT_PATH':'/run/trace280-event.json','TRACE267_WORKFLOW_SHA':commit,'TRACE280_UNIT':unit,'TRACE280_PARENT_NETNS':str(os.stat('/proc/self/ns/net').st_ino),'PYTHONDONTWRITEBYTECODE':'1'}
 argv=[executables['systemd-run']['path'],'--system','--unit='+unit,'--description=TraceHarbor corrected attempt2 '+run+' '+commit,'--wait','--pipe','--expand-environment=no']
 argv+=['--property='+x for x in props]+['--setenv='+k+'='+v for k,v in sorted(env.items())]+[executables['node']['path'],'--max-old-space-size=32','/run/trace280-source/tools/ui267/qualify.mjs','--source','/run/trace280-source','--out','/run/trace280-out/result']
 return unit,argv
def owned(props,unit,invocation,uid):
 return bool(isinstance(invocation,str)and re.fullmatch('[0-9a-f]{32}',invocation)and props.get('Id')==unit and props.get('InvocationID')==invocation and props.get('User')==str(uid)and props.get('ControlGroup','').endswith('/'+unit))
def properties(unit):
 r=bounded([SYSTEMCTL,'show',unit,'--no-pager','--property=Id,InvocationID,User,ControlGroup,ActiveState,SubState,Result'],5)
 need(r['exit']==0,'unit readback unavailable')
 return dict(l.split('=',1)for l in r['stdout'].splitlines()if'='in l)
def main():
 source=str(pathlib.Path(sys.argv[1]).resolve(strict=True));out=str(pathlib.Path(sys.argv[2]).resolve(strict=True))
 need(source!=out and all(re.fullmatch(r'/[A-Za-z0-9_./-]+',v)and '..'not in pathlib.Path(v).parts for v in [source,out]),'bounded paths')
 contract=json.load(open(source+'/contracts/ui280_admission.json'))
 # Caller must independently verify current native owned admission/CAS and source.
 # This JSON is execution configuration, never a fabricated lease or authority.
 need(contract.get('schema')=='TRACE_UI282_CONFIGURATION_V1'and contract['status']=='ADOPTED_SEPARATE_NATIVE_ADMISSION_REQUIRED','SOURCE_ONLY_UNADMITTED')
 need(os.geteuid()==0 and int(os.environ.get('SUDO_UID','0'))>0,'existing ephemeral manager privilege required')
 uid=int(os.environ['SUDO_UID']);gid=pwd.getpwuid(uid).pw_gid
 need(pathlib.Path('/proc/1/comm').read_text().strip()=='systemd','no supported existing manager')
 validate_config282(contract)
 for k,x in contract['required_executables'].items():
  need(x['state']=='QUALIFIED' and sha(x['path'])==x['sha256'],'unqualified executable '+k)
 global SYSTEMCTL
 SYSTEMCTL=contract['required_executables']['systemctl']['path']
 version=bounded([contract['required_executables']['systemd-run']['path'],'--version'])
 need(version['exit']==0 and re.match(r'systemd 255\b',version['stdout'])is not None,'manager version behavior drift')
 for path,pin in contract['runtime_sha256'].items():need(sha(source+'/'+path)==pin,'source drift')
 event=os.environ['GITHUB_EVENT_PATH'];ev=json.load(open(event));run=os.environ['GITHUB_RUN_ID'];commit=os.environ['GITHUB_SHA']
 need(os.environ.get('GITHUB_EVENT_NAME')=='create'and os.environ.get('GITHUB_RUN_ATTEMPT')=='1','only separately admitted corrected attempt2 originalevent')
 need(ev['ref_type']=='branch'and ev['ref']=='traceharbor-ui280-attempt2'and ev['repository']['id']==1391430317 and not ev['repository']['private']and ev['sender']['id']==273768139,'wrong exact event')
 unit,argv=command(source,out,event,uid,gid,run,commit,contract['required_executables'])
 # systemd v255 run.c blob88eca0... uses StartTransientUnit(...,"fail").
 # Actual installed behavior/pins require independent qualification; no replace.
 before=bounded([SYSTEMCTL,'show',unit,'--property=LoadState','--value'])
 need(before['exit']==0 and before['stdout'].strip()=='not-found','unit exists/unqualified absence')
 pathlib.Path(out+'/home').mkdir(mode=0o700);os.chown(out+'/home',uid,gid)
 intent={'unit':unit,'argv':argv,'effect':'FUTURE_CORRECTED_UI_ATTEMPT2','source_commit':commit,'creation_mode':'StartTransientUnit fail, documented upstreamv255; never replace/retry','native_provider_setup_identity':'MUST_BE_INDEPENDENTLY_READ_BEFORE_ACCEPTANCE'}
 with open(out+'/UNIT_ATTEMPT.json','x')as f:json.dump(intent,f);f.flush();os.fsync(f.fileno())
 invocation=None;ack=False
 # manager stderr/stdout bounded by bounded(); RuntimeMaxSec enforces descendant end.
 # Capture journal without forwarding credentials or persistent service setup.
 r=bounded(argv,200)
 with open(out+'/MANAGER_RETURN.json','x')as f:json.dump(r,f)
 # No --collect; RemainAfterExit retains the exact invocation for a postread.
 # Missing/foreign identity remains UNKNOWN, never success or permission to kill.
 try:
  props=properties(unit);invocation=props.get('InvocationID');ack=owned(props,unit,invocation,uid)
 except BaseException:props={'state':'POSTOWNERSHIP_NOT_EXPOSED'}
 if r['exit']!=0:
  # Never kill a collision/foreign/unknown unit. Only exact invocation owner.
  if ack and props.get('ActiveState')in['active','activating']:
   check=properties(unit)
   if owned(check,unit,invocation,uid):bounded([SYSTEMCTL,'kill','--kill-who=all','--signal=TERM',unit],5)
  raise RuntimeError('Corrected run failed/unknown; preserve journal; no retry')
 need(r['exit']==0 and ack,'manager result or exact postownership unavailable; UNKNOWN/no retry')
 # Future cleanup is scoped to the same native invocation twice, never foreign.
 check=properties(unit);need(owned(check,unit,invocation,uid),'postownership changed')
 cleanup=bounded([SYSTEMCTL,'stop',unit],10)
 with open(out+'/OWNED_CLEANUP_RETURN.json','x')as f:json.dump(cleanup,f)
 need(cleanup['exit']==0,'owned cleanup unverified; no retry')
 print(json.dumps({'status':'FUNCTIONAL_RESULT_PENDING_INDEPENDENT_NATIVE_SETUP_IDENTITY','unit':unit,'ownership_postread':props,'source_commit':commit,'no_backend_effect_or_cgroup_availability_claim':True}))

def parse_git_commit289(original,expected_sha):
 def check(ok,msg):
  if not ok:raise RuntimeError(msg)
 check(isinstance(original,dict),'GIT_COMMIT_RETURN289')
 check(type(original.get('exit'))is int and original['exit']==0 and original.get('failure')is None,'GIT_COMMIT_READ_FAILED289')
 check(original.get('argv',[])[-3:]==['cat-file','-p',expected_sha],'GIT_COMMIT_COMMAND289')
 text=original.get('stdout');check(isinstance(text,str)and original.get('stderr')=='','GIT_COMMIT_CHANNEL289')
 raw=text.encode('utf-8');check(0<len(raw)<=2048,'GIT_COMMIT_BOUND289')
 check(bool(re.fullmatch('[0-9a-f]{40}',expected_sha)),'GIT_COMMIT_EXPECTED_SHA289')
 actual=hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
 check(actual==expected_sha,'GIT_COMMIT_RAW_ID289')
 check(b'\n\n'in raw and b'\r'not in raw,'GIT_COMMIT_HEADER289')
 header,message=raw.split(b'\n\n',1);fields={};last=None
 for line in header.split(b'\n'):
  if line.startswith(b' '):
   check(last==b'gpgsig','GIT_COMMIT_CONTINUATION289');continue
  check(b' 'in line,'GIT_COMMIT_FIELD289');key,value=line.split(b' ',1)
  check(key in [b'tree',b'parent',b'author',b'committer',b'encoding',b'gpgsig']and bool(value),'GIT_COMMIT_FIELD289')
  fields.setdefault(key,[]).append(value);last=key
 check(len(fields.get(b'tree',[]))==1 and bool(re.fullmatch(b'[0-9a-f]{40}',fields[b'tree'][0])),'GIT_COMMIT_TREE289')
 check(len(fields.get(b'parent',[]))==1 and fields[b'parent'][0].decode('ascii',errors='replace')==CAP_BASE288,'GIT_COMMIT_SOLE_PARENT289')
 check(len(fields.get(b'author',[]))==1 and len(fields.get(b'committer',[]))==1,'GIT_COMMIT_AUTHOR_HEADER289')
 return {'schema':'TRACE289_NATIVE_GIT_COMMIT_PROOF_V1','source_type':'NATIVE_GIT_CAT_FILE_COMMIT_BYTES','sha':expected_sha,'tree':{'sha':fields[b'tree'][0].decode('ascii')},'parents':[{'sha':CAP_BASE288}],'raw_byte_count':len(raw),'raw_sha256':hashlib.sha256(raw).hexdigest(),'original_return':original}

CAP_BASE288='cf8c389bb24fe3eb2f9f2f62d55ced5108205951'
CAP_BRANCH288='review/traceharbor-v1-browser-qa-base180-162-20261023'
def validate_push288(env,ev,proof=None):
 def check(ok,msg):
  if not ok:raise RuntimeError(msg)
 check(env.get('GITHUB_ACTIONS')=='true'and env.get('RUNNER_ENVIRONMENT')=='github-hosted','HOSTED_ONLY288')
 check(env.get('GITHUB_EVENT_NAME')=='push'and env.get('GITHUB_RUN_ATTEMPT')=='1','PUSH_ATTEMPT1_ONLY288')
 check(env.get('GITHUB_REPOSITORY')=='Elinfiny/TraceHarbor'and env.get('GITHUB_ACTOR_ID')=='273768139','REPO_ACTOR288')
 check(env.get('GITHUB_REF')=='refs/heads/'+CAP_BRANCH288 and ev.get('ref')==env.get('GITHUB_REF'),'FULLREF288')
 repo=ev.get('repository',{});owner=repo.get('owner',{});sender=ev.get('sender',{})
 check(type(repo.get('id'))is int and repo['id']==1391430317 and type(owner.get('id'))is int and owner['id']==273768139 and type(sender.get('id'))is int and sender['id']==273768139 and repo.get('full_name')=='Elinfiny/TraceHarbor'and repo.get('private')is False,'NATIVE_IDENTITY288')
 check(all(ev.get(k)is False for k in ['created','deleted','forced']),'EXISTING_NONFORCED_PUSH288')
 after=env.get('GITHUB_SHA','');check(bool(re.fullmatch('[0-9a-f]{40}',after))and after!=CAP_BASE288,'AFTER288')
 check(ev.get('before')==CAP_BASE288,'BEFORE288')
 check(ev.get('after')==after and ev.get('head_commit',{}).get('id')==after and env.get('TRACE282_WORKFLOW_SHA')==after,'HEAD_WORKFLOW288')
 if proof is not None:
  check(isinstance(proof,dict)and proof.get('sha')==after,'COMMIT_PROOF_SHA288')
  parents=proof.get('parents');check(isinstance(parents,list)and len(parents)==1 and isinstance(parents[0],dict)and parents[0].get('sha')==CAP_BASE288,'SOLE_PARENT288')
  check(bool(re.fullmatch('[0-9a-f]{40}',proof.get('tree',{}).get('sha',''))),'COMMIT_TREE288')
 return after

CAP_BRANCH=CAP_BRANCH288
def validate_config282(c):
 need(c.get('schema')=='TRACE_UI282_CONFIGURATION_V1'and c.get('canonical_base')==CAP_BASE288,'config schema/base')
 need(c.get('status')in ['SOURCE_ONLY_NOT_ADOPTED','ADOPTED_SEPARATE_NATIVE_ADMISSION_REQUIRED'],'unknown config status')
 need(c.get('capability_branch')==CAP_BRANCH and c.get('future_ui_branch')=='traceharbor-ui280-attempt2','channel binding')
 need(c.get('ui_workflow_enabled')is False and c.get('external_native_admission_required')is True,'UI must remain inert')
 need(set(c.get('required_executables',{}))=={'node','python3','systemd-run','systemctl','chrome','chromedriver'},'executable slots')
 for x in c['required_executables'].values():
  need(x.get('state')in ['NOT_QUALIFIED','QUALIFIED'],'executable state')
  if x['state']=='NOT_QUALIFIED':need(x.get('path')is None and x.get('sha256')is None,'fabricated unqualified pin')
  else:need(bool(re.fullmatch('/[A-Za-z0-9_./+-]+',x.get('path','')))and bool(re.fullmatch('[0-9a-f]{64}',x.get('sha256',''))),'qualified path/pin')
 for path,pin in c.get('runtime_sha256',{}).items():need(path in ['tools/ui267/qualify.mjs','tools/ui280/run_owned_scope.py','.github/workflows/traceharbor-ui280.yml']and bool(re.fullmatch('[0-9a-f]{64}',pin)),'runtime source pin')
 need(len(c.get('runtime_sha256',{}))==3,'all noncircular runtime pins required')
 return True

def select_mode282(argv,env,ev,c,proof):
 validate_config282(c)
 if argv!=['--capability-readonly']:raise RuntimeError('UI282_DISABLED_SOURCE_ONLY')
 need(isinstance(proof,dict)and proof.get('schema')=='TRACE289_NATIVE_GIT_COMMIT_PROOF_V1'and proof.get('source_type')=='NATIVE_GIT_CAT_FILE_COMMIT_BYTES','NATIVE_GIT_COMMIT_PROOF_REQUIRED289')
 need(parse_git_commit289(proof.get('original_return'),env.get('GITHUB_SHA',''))==proof,'NATIVE_GIT_COMMIT_PROOF_BINDING289')
 validate_push288(env,ev,proof)
 need(c.get('capability_event')=={'name':'push','before':CAP_BASE288,'full_ref':'refs/heads/'+CAP_BRANCH288,'created':False,'deleted':False,'forced':False,'sole_parent':CAP_BASE288,'effect':'TRACE180_READONLY_HOST_CAPABILITY282'},'EVENT_CONFIG288')
 return 'READ_ONLY_CAPABILITY'

def collect_readonly282():
 import shutil
 source=pathlib.Path(__file__).resolve().parents[2]
 c=json.loads((source/'contracts/ui280_admission.json').read_text())
 event=pathlib.Path(os.environ['GITHUB_EVENT_PATH']);need(event.stat().st_size<=262144,'event bound')
 ev=json.loads(event.read_text());receipt=json.loads(pathlib.Path(os.environ['TRACE284_BOOTSTRAP_RECEIPT']).read_text());select_mode282(sys.argv[1:],os.environ,ev,c,receipt.get('native_git_commit_proof'))
 # Only immutable source reads, executable --version, and systemctl show.
 pins={p:sha(source/p)for p in c['runtime_sha256']};need(pins==c['runtime_sha256'],'source bytes drift')
 observed={};versions={}
 names={'node':['node'],'python3':['python3'],'systemd-run':['systemd-run'],'systemctl':['systemctl'],'chrome':['google-chrome','google-chrome-stable','chromium'],'chromedriver':['chromedriver']}
 for key,candidates in names.items():
  original=next((shutil.which(n)for n in candidates if shutil.which(n)),None)
  if original is None:observed[key]={'state':'NOT_INSTALLED'};continue
  resolved=str(pathlib.Path(original).resolve(strict=True));observed[key]={'path':original,'realpath':resolved,'sha256':sha(resolved),'state':'OBSERVED_NOT_ADOPTED'}
  try:
   versions[key]=bounded([original,'--version'],5,2048)
   if versions[key].get('failure') or versions[key]['exit']!=0:observed[key]['state']='BOUNDED_PROBE_FAILED_NOT_QUALIFIED'
  except BaseException as e:versions[key]={'error':type(e).__name__+':'+str(e),'exit':'NOT_EXPOSED'}
 def read(path,limit=4096):
  try:
   with open(path,'rb')as f:b=f.read(limit+1)
   return {'text':b[:limit].decode(errors='replace'),'truncated':len(b)>limit}
  except OSError as e:return {'error':type(e).__name__,'errno':e.errno}
 manager={'pid1_comm':read('/proc/1/comm',128)}
 if 'path'in observed.get('systemctl',{}):
  try:manager['show']=bounded([observed['systemctl']['path'],'show','--no-pager','--property=Version,Features,ControlGroup,SystemState'],5,2048)
  except BaseException as e:manager['show']={'error':type(e).__name__+':'+str(e),'exit':'NOT_EXPOSED'}
 proc=read('/proc/self/status',8192).get('text','')
 status={line.split(':',1)[0]:line.split(':',1)[1].strip()for line in proc.splitlines()if line.split(':',1)[0]in ['VmSize','VmRSS','VmPeak','VmHWM','CapEff','NoNewPrivs','Uid','Gid']}
 cg=read('/proc/self/cgroup',2048);mounts=read('/proc/self/mountinfo',16384)
 mountrows=[s for s in mounts.get('text','').splitlines()if ' - cgroup2 'in s]
 kernel={n:read('/sys/fs/cgroup/'+n,1024)for n in ['cgroup.controllers','memory.max','memory.current','memory.peak','memory.swap.max','memory.events']}
 ns={}
 for n in ['net','mnt','user','cgroup']:
  try:ns[n]=os.readlink('/proc/self/ns/'+n)
  except OSError as e:ns[n]={'errno':e.errno}
 result={'schema':'TRACE_HOST_CAPABILITY282_ACTUAL_READONLY_V1','effect':'TRACE180_READONLY_HOST_CAPABILITY282','source_commit':os.environ['GITHUB_SHA'],'workflow_sha':os.environ['TRACE282_WORKFLOW_SHA'],'run_id':os.environ.get('GITHUB_RUN_ID'),'attempt':1,'branch':CAP_BRANCH,'source_pins':pins,'config_sha256':sha(source/'contracts/ui280_admission.json'),'os_release':read('/etc/os-release',4096),'executables':observed,'version_returns_original':versions,'manager':manager,'self_process_status':status,'cgroup_membership':cg,'cgroup2_mounts':mountrows,'root_cgroup_observations_not_owned_UI_capacity':kernel,'namespaces':ns,'unprivileged_userns_clone':read('/proc/sys/kernel/unprivileged_userns_clone',128),'max_user_namespaces':read('/proc/sys/user/max_user_namespaces',128),'memory284':_memory284,'bootstrap284':json.loads(pathlib.Path(os.environ['TRACE284_BOOTSTRAP_RECEIPT']).read_text()),'child_original_records284':_records284,'UI_audio_unit_cgroupwrites_installs':0,'native_job_setup_identity':'External native setup log required separately; environment ImageVersion is not authoritative','availability_not_UI_capacity_or_permission':True}
 data=json.dumps(result,sort_keys=True,separators=(',',':'));need(len(data.encode())<=32768,'stdout bound')
 print(data)

if __name__=='__main__':
 if sys.argv[1:]==['--capability-readonly']:collect_readonly282()
 else:raise SystemExit('UI282_DISABLED_SOURCE_ONLY; separate future native admission required')

