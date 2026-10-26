"""PRIVATE294 SOURCE_ONLY. Current activation absent. No IO on import.
Native backend is callable only with cryptographically verified admission.
"""
import os,sys,re,json,hashlib,hmac,time,stat,resource,subprocess,selectors,signal,argparse
LIVE_ADOPTION=None
_ISSUER=object()
def canonical(obj):return json.dumps(obj,sort_keys=True,separators=(',',':')).encode()
def strict_json(raw):
 def pairs(xs):
  d={}
  for k,v in xs:
   if k in d:raise Refusal('JSON_DUPLICATE')
   d[k]=v
  return d
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in ()).throw(Refusal('JSON_NUMBER')))

class VerifiedAdmission:
 def __init__(self,body,proof,issuer):
  if issuer is not _ISSUER:raise Refusal('UNAUTHENTICATED_ADMISSION')
  self._body=canonical(body);self._proof=canonical(proof)
 @property
 def body(self):return strict_json(self._body)
 @property
 def proof(self):return strict_json(self._proof)


class SafeDirectory:
 def __init__(self,directory,uid=None,mode=0o700,gid=None,io=os):
  self.io=io;self.path=path(directory);self.uid=os.geteuid() if uid is None else uid;self.mode=mode;self.gid=gid
  fd=io.open('/',os.O_RDONLY|os.O_DIRECTORY)
  try:
   for part in directory[1:].split('/'):
    nxt=io.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);io.close(fd);fd=nxt
   st=io.fstat(fd);need(stat.S_ISDIR(st.st_mode) and st.st_uid==self.uid and stat.S_IMODE(st.st_mode)==mode and (gid is None or st.st_gid==gid),'PRIVATE_DIRECTORY_IDENTITY')
   self.fd=fd;self.identity=(st.st_dev,st.st_ino);fd=None
  finally:
   if fd is not None:io.close(fd)
 def check(self):
  st=self.io.fstat(self.fd);need((st.st_dev,st.st_ino)==self.identity and st.st_uid==self.uid and stat.S_IMODE(st.st_mode)==self.mode,'DIRECTORY_FD_DRIFT')
 def close(self):self.io.close(self.fd)

class AtomicFiles:
 NAMES={'ack294.json','release294.json','plan294.json','event294.json','anchor295.json','runtime295.json','derived298.json','native-context298.json'}
 def __init__(self,directory,file_mode=0o600,logger=None):self.d=directory;self.mode=file_mode;self.events=[];self.logger=logger
 def log(self,event):
  self.events.append(event)
  if self.logger:self.logger(event)
 def bound(self,name):
  base=name[1:-8] if name.startswith('.')and name.endswith('.pending') else name
  need(base in self.NAMES,'LATCH_NAME');return 32768 if base in {'derived298.json','native-context298.json'} else 16384
 def read_bytes(self,name):
  limit=self.bound(name)
  need(name in self.NAMES or name in {'.'+n+'.pending' for n in self.NAMES},'LATCH_NAME');self.d.check();io=self.d.io
  try:fd=io.open(name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=self.d.fd)
  except FileNotFoundError:return None
  try:
   st=io.fstat(fd);need(stat.S_ISREG(st.st_mode) and st.st_uid==self.d.uid and (self.d.gid is None or st.st_gid==self.d.gid) and stat.S_IMODE(st.st_mode)==self.mode and st.st_size<=limit,'LATCH_FILE_IDENTITY')
   b=io.read(fd,limit+1);after=io.fstat(fd)
   need(len(b)==st.st_size and (st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns),'LATCH_PARTIAL_OR_DRIFT')
   return b
  finally:io.close(fd)
 def read(self,name):
  b=self.read_bytes(name);return None if b is None else strict_json(b)
 def write_once(self,name,value):
  need(name in self.NAMES,'LATCH_NAME');self.d.check();io=self.d.io;raw=canonical(value);need(len(raw)<=self.bound(name),'LATCH_BOUND');stage='.'+name+'.pending';fd=None;visible=False
  self.log({'event':'ATOMIC_INTENT','name':name,'stage':stage,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
  try:
   fd=io.open(stage,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,self.mode,dir_fd=self.d.fd)
   if os.geteuid()!=self.d.uid or (self.d.gid is not None and io.fstat(fd).st_gid!=self.d.gid):
    need(os.geteuid()==0,'LATCH_WRITER_OWNER');io.fchown(fd,self.d.uid,self.d.gid if self.d.gid is not None else -1)
   io.fchmod(fd,self.mode);view=memoryview(raw);calls=0
   while view:
    n=io.write(fd,view);calls+=1;self.log({'event':'WRITE_ORIGINAL','count':n});need(0<n<=len(view) and calls<=128,'PARTIAL_WRITE_BOUND');view=view[n:]
   io.fsync(fd);self.log({'event':'FILE_FSYNC','success':True});io.close(fd);fd=None
   # Same-filesystem hardlink gives atomic no-replace publication; staging
   # inode remains evidence. Never overwrite/unlink an unknown final or stage.
   io.link(stage,name,src_dir_fd=self.d.fd,dst_dir_fd=self.d.fd,follow_symlinks=False);visible=True;self.log({'event':'FINAL_VISIBLE','name':name})
   io.fsync(self.d.fd);self.log({'event':'DIRECTORY_FSYNC','success':True})
   return {'state':'COMMITTED_VISIBLE_DURABLE','created':True,'permit_sha256':digest(value)}
  except Exception as e:
   self.log({'event':'ATOMIC_EXCEPTION_ORIGINAL','class':type(e).__name__,'message':str(e),'visible_observed':visible})
   return {'state':'UNKNOWN','created':'NOT_PROVED','visible_observed':visible,'error':type(e).__name__+':'+str(e)}
  finally:
   if fd is not None:io.close(fd)
 def reconcile(self,name,expected):
  # Readonly after crash; visibility is not evidence of past directory fsync.
  raw=canonical(expected);final=self.read_bytes(name);stage=self.read_bytes('.'+name+'.pending')
  if final is not None:return {'state':'VISIBLE_DURABILITY_UNKNOWN' if final==raw else 'CONFLICT_UNKNOWN','sha256':hashlib.sha256(final).hexdigest()}
  return {'state':'STAGED_NOT_VISIBLE_UNKNOWN' if stage==raw else 'PARTIAL_OR_ABSENT_UNKNOWN','stage_sha256':None if stage is None else hashlib.sha256(stage).hexdigest()}

class Journal:
 def __init__(self,directory,binding,name='supervisor294.jsonl',max_bytes=262144,max_events=512,logger=None):
  need(name in ['supervisor294.jsonl','worker294.jsonl'],'JOURNAL_NAME');integer(max_bytes,256,262144);integer(max_events,1,512)
  self.d=directory;self.binding=binding;self.name=name;self.max_bytes=max_bytes;self.max_events=max_events;self.events=[];self.total=0;self.previous='0'*64;self.blocked=False;self.readonly=False;self.io_originals=[];self.logger=logger
  directory.check();self.fd=directory.io.open(name,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,0o600,dir_fd=directory.fd)
  if os.geteuid()!=directory.uid:directory.io.fchown(self.fd,directory.uid,directory.gid if directory.gid is not None else -1)
  directory.io.fchmod(self.fd,0o600);directory.io.fsync(directory.fd)
 def logio(self,row):
  self.io_originals.append(row)
  if self.logger:self.logger(row)
 def append(self,event):
  need(not self.blocked and not self.readonly,'JOURNAL_BLOCKED_OR_READONLY');need(event.get('binding')==self.binding,'JOURNAL_BINDING')
  row={'seq':len(self.events)+1,'previous':self.previous,'binding':self.binding,'event':event};raw=canonical(row)+b'\n'
  if not (len(raw)<=65536 and self.total+len(raw)<=self.max_bytes and len(self.events)<self.max_events):
   self.blocked=True;self.logio({'event':'JOURNAL_TOTAL_OR_EVENT_BOUND','original_status':'NOT_APPENDED','bytes':len(raw),'total':self.total});raise Refusal('JOURNAL_TOTAL_OR_EVENT_BOUND')
  try:
   view=memoryview(raw);calls=0
   while view:
    n=self.d.io.write(self.fd,view);calls+=1;self.logio({'event':'JOURNAL_WRITE_ORIGINAL','count':n,'sequence':row['seq']});need(0<n<=len(view) and calls<=128,'JOURNAL_PARTIAL_WRITE');view=view[n:]
   self.d.io.fsync(self.fd);self.logio({'event':'JOURNAL_FSYNC','seq':row['seq'],'success':True})
  except Exception as e:
   self.blocked=True;self.logio({'event':'JOURNAL_PERSISTENCE_UNKNOWN','class':type(e).__name__,'message':str(e),'original_status':'IN_MEMORY_NOT_DURABLY_PROVED'});raise
  self.events.append(strict_json(canonical(event)));self.total+=len(raw);self.previous=hashlib.sha256(raw[:-1]).hexdigest()
 def close(self):self.d.io.close(self.fd)
 @classmethod
 def recover(cls,directory,binding,name='supervisor294.jsonl',max_bytes=262144,max_events=512):
  need(name in ['supervisor294.jsonl','worker294.jsonl'],'JOURNAL_NAME');integer(max_bytes,256,262144);integer(max_events,1,512);directory.check();io=directory.io
  fd=io.open(name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=directory.fd)
  try:
   st=io.fstat(fd);need(stat.S_ISREG(st.st_mode) and st.st_uid==directory.uid and stat.S_IMODE(st.st_mode)==0o600 and st.st_size<=max_bytes,'RECOVERY_FILE_IDENTITY_BOUND')
   chunks=[];total=0
   while True:
    b=io.read(fd,min(8192,max_bytes+1-total))
    if not b:break
    chunks.append(b);total+=len(b);need(total<=max_bytes,'RECOVERY_TOTAL_BOUND')
   after=io.fstat(fd);need((st.st_ino,st.st_size,st.st_mtime_ns)==(after.st_ino,after.st_size,after.st_mtime_ns),'RECOVERY_DRIFT');raw=b''.join(chunks)
  finally:io.close(fd)
  rows=raw.splitlines(keepends=True);events=[];previous='0'*64;tail=b''
  for index,line in enumerate(rows):
   if not line.endswith(b'\n'):tail=line;break
   need(len(events)<max_events and len(line)<=65536,'RECOVERY_EVENT_BOUND');row=strict_json(line)
   need(set(row)=={'seq','previous','binding','event'} and row['binding']==binding and type(row['seq'])is int and row['seq']==len(events)+1 and row['previous']==previous and row['event'].get('binding')==binding,'RECOVERY_BINDING_ORDER_CHAIN')
   need(canonical(row)+b'\n'==line,'RECOVERY_CANONICAL');events.append(row['event']);previous=hashlib.sha256(line[:-1]).hexdigest()
  obj=object.__new__(cls);obj.d=directory;obj.binding=binding;obj.events=events;obj.readonly=True;obj.blocked=True;obj.fd=None;obj.total=len(raw);obj.previous=previous;obj.io_originals=[];obj.logger=None
  obj.recovery={'state':'READ_ONLY_CONSUMED_OR_UNKNOWN','partial_tail_bytes':len(tail),'partial_tail_sha256':hashlib.sha256(tail).hexdigest(),'raw_sha256':hashlib.sha256(raw).hexdigest(),'event_count':len(events)}
  return obj
class Refusal(RuntimeError):pass

def need(ok,reason):
 if not ok:raise Refusal(reason)

def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def path(value):
 need(isinstance(value,str) and re.fullmatch(r'/[A-Za-z0-9_./-]+',value) and all(p not in ['.','..',''] for p in value[1:].split('/')),'PATH')
 return value

def integer(value,low,high):
 need(type(value)is int and low<=value<=high,'SAFE_INTEGER');return value

def prepare(verified):
 # verify_native is supplied by a caller retaining authenticated provider
 # originals/CAS/provenance. A JSON true flag is never a native verifier.
 need(isinstance(verified,VerifiedAdmission),'NATIVE_ADMISSION_NOT_VERIFIED');admission=verified.body
 a=json.loads(json.dumps(admission));need(a.get('schema')=='TRACE295_NATIVE_ADMISSION_V1','SCHEMA')
 need(a.get('repository')=='Elinfiny/TraceHarbor','REPOSITORY')
 need(re.fullmatch(r'[0-9a-f]{40}',a.get('source_commit','')) is not None,'SOURCE_COMMIT')
 need(re.fullmatch(r'[A-Z0-9_-]{8,96}',a.get('effect_id','')) is not None,'EFFECT_ID')
 need(re.fullmatch(r'[0-9]{1,20}',a.get('run_id','')) is not None,'RUN_ID')
 integer(a.get('uid'),1,2147483647);integer(a.get('gid'),1,2147483647)
 need(a.get('manager_authority')=='EXISTING_INDEPENDENTLY_ADMITTED_NO_PRIVILEGE_ESCALATION','MANAGER_AUTHORITY')
 need(a.get('memory_max')==335544320 and a.get('swap_max')==0,'PHYSICAL_ADMISSION')
 integer(a.get('virtual_as'),100663297,9007199254740991)
 need(a.get('whole_cap')==536870912 and a.get('budget_reconciled') is True,'WHOLE_POOL_ADMISSION')
 need(a.get('sandbox_required') is True and a.get('source_accepted') is True,'SOURCE_SANDBOX_ADMISSION')
 parent=path(a.get('cgroup_parent'));need(re.fullmatch(r'/trace294\.slice',parent) is not None,'SHARED_OR_AMBIGUOUS_CGROUP_FORBIDDEN')
 for key in ['source','out','home','gate_path','control','controller']:path(a.get(key))
 need(a['home']==a['out']+'/home' and a['gate_path']==a['control']+'/release294.json','OWNED_STAGE_BINDING')
 need(len({a['source'],a['out'],a['control'],a['controller']})==4 and all(not x.startswith(y+'/') for x in [a['source'],a['out'],a['control'],a['controller']] for y in [a['source'],a['out'],a['control'],a['controller']] if x!=y),'OWNED_PATH_SEPARATION')
 ev=a.get('runtime_event',{});need(ev.get('ref')=='refs/heads/review/traceharbor-v1-browser-qa-base180-162-20261023' and ev.get('before')=='7fc30e33c753b5335b1492a74eb09889d83b479d' and ev.get('after')==a['source_commit'] and all(ev.get(k)is False for k in ['created','deleted','forced']) and ev.get('repository',{}).get('id')==1391430317 and ev.get('repository',{}).get('private')is False and ev.get('sender',{}).get('id')==273768139 and a.get('native_hosted_context')is True,'QUALIFIER_NATIVE_EVENT_INTERFACE')
 need(re.fullmatch(r'net:\[[0-9]+\]',a.get('parent_netns','')),'PARENT_NETNS_NATIVE_FACT')
 need(set(a.get('binaries',{}))=={'systemd-run','systemctl','python3','node','chrome','chromedriver'},'BINARY_SLOTS')
 for x in a['binaries'].values():
  path(x.get('path'));need(re.fullmatch('[0-9a-f]{64}',x.get('sha256','')) is not None,'BINARY_PIN')
 need(set(a.get('source_pins',{}))=={'tools/ui280/owned_supervisor295.py','tools/ui280/bootstrap295.py','tools/ui267/qualify.mjs','contracts/ui280_admission.json','.github/workflows/traceharbor-ui280.yml','tools/ui280/native298.py','contracts/host298.json','tools/ui280/caller298.js'},'SOURCE_PIN_SET')
 for pin in a['source_pins'].values():need(re.fullmatch('[0-9a-f]{64}',pin) is not None,'SOURCE_PIN')
 need(a.get('release_token') and re.fullmatch('[0-9a-f]{64}',a['release_token']),'RELEASE_BINDING')
 # Unit identity is deterministic for one admitted effect/run/source; no retry nonce.
 unit='traceharbor-ui280-a2-'+a['run_id']+'.service'
 return {'admission':a,'binding':digest(a),'unit':unit,'cgroup':parent+'/'+unit,'phase':'PREPARED'}

def launch_argv(plan):
 a=plan['admission'];unit=plan['unit']
 props=['Type=exec','User='+str(a['uid']),'Group='+str(a['gid']),'Slice='+a['cgroup_parent'].split('/')[-1],
  'Description=Trace294 '+plan['binding'],'RemainAfterExit=yes','MemoryAccounting=yes','MemoryMax=335544320','MemorySwapMax=0',
  'LimitAS='+str(a['virtual_as']),'TasksMax=96','RuntimeMaxSec=180','TimeoutStopSec=5','KillMode=control-group','SendSIGKILL=yes',
  'PrivateNetwork=yes','PrivateTmp=yes','PrivateIPC=yes','NoNewPrivileges=yes','CapabilityBoundingSet=','AmbientCapabilities=',
  'ProtectSystem=strict','ProtectHome=yes','ProtectControlGroups=yes','ProtectKernelTunables=yes','ProtectKernelModules=yes',
  'RestrictSUIDSGID=yes','RestrictRealtime=yes','WorkingDirectory='+a['source'],
  'BindReadOnlyPaths='+a['source']+' '+a['control'],'BindPaths='+a['out'],'ReadWritePaths='+a['out']]
 return [a['binaries']['systemd-run']['path'],'--system','--no-ask-password','--no-block','--unit='+unit,'--expand-environment=no']+['--property='+p for p in props]+[
  '--setenv=PATH=/usr/bin:/bin','--setenv=HOME='+a['home'],'--setenv=LANG=C.UTF-8',
  a['binaries']['python3']['path'],'-I','-S','-B',a['source']+'/tools/ui280/bootstrap295.py','--gated-worker','--anchor',a['control']+'/anchor295.json','--anchor-sha',a['native_anchor_sha256'],'--derived',a['control']+'/derived298.json','--plan',a['control']+'/plan294.json','--binding',plan['binding']]

class Supervisor:
 def __init__(self,plan,transport,journal,gate,clock,kernel,hash_reader,observer=None,resident=None):
  self.observer=observer or native_unit_observation;self.resident=resident or resident_job_bound
  self.plan=strict_json(canonical(plan));self.transport=transport;self.journal=journal;self.gate=gate;self.clock=clock;self.kernel=kernel;self.hash=hash_reader
  self.deadline=clock()+180;self.phase='PREPARED';self.observation='PREPARED';self.invocation=None;self.attempted=False;self.released=False;self.stop_attempted=False;self.uncertain=False;self.process_result=None;self.cleanup_result=None;self.output_bytes=0;self.recovery_observations=[]
  self.replay_locked=bool(getattr(journal,'readonly',False))
  for e in journal.events:
   need(e.get('binding')==plan['binding'],'JOURNAL_BINDING_DRIFT')
   if e.get('event')=='LAUNCH_ATTEMPTING':self.attempted=True
   if e.get('event')=='GATE_ATTEMPTING':self.released=True
   if e.get('event')=='STOP_ATTEMPTING':self.stop_attempted=True
   if e.get('event')=='OWNERSHIP_VERIFIED':self.invocation=e['data']['InvocationID']
  if self.replay_locked or self.attempted or self.released:self.phase='UNKNOWN';self.uncertain=True
  else:self.record('PREPARED',{'phase':self.phase})
 def record(self,event,data):
  row={'binding':self.plan['binding'],'unit':self.plan['unit'],'event':event,'at':self.clock(),'data':data}
  if self.replay_locked:
   need(len(self.recovery_observations)<128 and len(canonical(self.recovery_observations))+len(canonical(row))<=65536,'RECOVERY_OBSERVATION_BOUND');self.recovery_observations.append(row)
  else:self.journal.append(row)
 def state(self,phase,observation=None):
  self.phase=phase;self.observation=observation or phase
  if phase=='UNKNOWN':self.uncertain=True
  self.record('PHASE',{'phase':phase,'observation':self.observation})
 def pins(self):
  a=self.plan['admission']
  for p,pin in [(x['path'],x['sha256'])for x in a['binaries'].values()]+[(a['source']+'/'+p,pin)for p,pin in a['source_pins'].items()]:
   actual=self.hash(p);self.record('PIN_ORIGINAL',{'path':p,'sha256':actual});need(actual==pin,'EXECUTABLE_OR_SOURCE_DRIFT')
 def call(self,argv,label,cleanup=False):
  remaining=self.deadline-self.clock();need(cleanup or remaining>0,'OVERALL180_DEADLINE');bound=5 if cleanup else min(5,remaining)
  self.record('CALL_INTENT',{'argv':argv,'label':label,'timeout':bound,'limit':32768})
  try:r=self.transport(argv,timeout=bound,limit=32768,env={'PATH':'/usr/bin:/bin','HOME':self.plan['admission']['home'],'LANG':'C.UTF-8'})
  except Exception as e:
   self.record('TRANSPORT_EXCEPTION_ORIGINAL',{'class':type(e).__name__,'message':str(e)});self.state('UNKNOWN');raise
  self.record('CALL_RETURN_ORIGINAL',{'label':label,'return':r})
  need(isinstance(r,dict),'MANAGER_RETURN');size=len(r.get('stdout','').encode())+len(r.get('stderr','').encode());self.output_bytes+=size
  need(size<=32768 and self.output_bytes<=65536,'MANAGER_OUTPUT_BOUND');need(type(r.get('elapsed_s'))in [int,float] and 0<=r['elapsed_s']<=bound,'MANAGER_CALL5_TIMEOUT')
  need(r.get('failure') is None and r.get('truncated') is False,'MANAGER_PARTIAL_OR_FAILED');return r
 def read(self,cleanup=False):
  a=self.plan['admission'];return parse_props(self.call([a['binaries']['systemctl']['path'],'show',self.plan['unit'],'--no-pager','--no-ask-password','--property=MainPID,LoadState,Id,Description,InvocationID,User,ControlGroup,ActiveState,SubState,Result,ExecMainCode,ExecMainStatus,LimitAS,MemoryMax,MemorySwapMax'],'READ_SAME_UNIT',cleanup))
 def owned(self,p):
  return bool(p.get('Id')==self.plan['unit'] and p.get('Description')=='Trace294 '+self.plan['binding'] and p.get('User')==str(self.plan['admission']['uid']) and p.get('ControlGroup')==self.plan['cgroup'] and re.fullmatch('[0-9a-f]{32}',p.get('InvocationID','')) and (self.invocation is None or self.invocation==p['InvocationID']))
 def ownership(self,p):
  need(self.owned(p),'FOREIGN_OR_UNKNOWN_OWNER');self.invocation=p['InvocationID'];self.record('OWNERSHIP_VERIFIED',p)
 def capacity(self,p,empty=False):
  need(self.owned(p),'CAPACITY_OWNER');raw=self.kernel(self.plan['cgroup']);self.record('KERNEL_ORIGINAL',raw);a=self.plan['admission']
  need(raw.get('path')==self.plan['cgroup'] and raw.get('truncated') is False and raw.get('memory.max')=='335544320' and raw.get('memory.swap.max')=='0','DEDICATED_KERNEL_CAP')
  need(p.get('LimitAS')==str(a['virtual_as']) and p.get('MemoryMax')=='335544320' and p.get('MemorySwapMax')=='0','VIRTUAL_PHYSICAL_READBACK')
  if empty:need(raw.get('populated') is False,'OWNED_EMPTY_NOT_PROVED')
  else:
   observed=self.observer(self.plan,p);self.record('PRE_APP_ACTUAL_ISOLATION_ORIGINAL',observed);require_pre_app(self.plan,observed);self.record('WHOLE_RESIDENT_ORIGINAL',self.resident())
  return raw
 def unknown(self,stage,e):self.record('ABORT_ORIGINAL',{'stage':stage,'class':type(e).__name__,'message':str(e)});self.state('UNKNOWN');return 'UNKNOWN'
 def start(self):
  need(not self.replay_locked and not self.attempted and self.phase=='PREPARED','LAUNCH_CONSUMED_NO_REPLAY')
  try:
   self.pins();p=self.read();need(p.get('Id')==self.plan['unit'] and p.get('LoadState')=='not-found','UNIT_COLLISION_OR_ABSENCE_UNPROVED')
   self.attempted=True;self.record('LAUNCH_ATTEMPTING',{'argv':launch_argv(self.plan)});self.state('ATTEMPTING')
   r=self.call(launch_argv(self.plan),'LAUNCH_ONCE');need(r.get('exit')==0,'LAUNCH_ACK_UNKNOWN');self.state('ACKNOWLEDGED','PENDING_START');return self.poll_start()
  except Exception as e:return self.unknown('START',e)
 def poll_start(self):
  need(self.attempted,'START_NOT_ATTEMPTED')
  try:
   need(self.clock()<self.deadline,'STARTUP180_DEADLINE');p=self.read()
   # --no-block only enqueues. Empty startup identity is pending; a nonempty
   # conflicting identity is never excused as an ordinary queue condition.
   expected={'Id':self.plan['unit'],'Description':'Trace294 '+self.plan['binding'],'User':str(self.plan['admission']['uid']),'ControlGroup':self.plan['cgroup']}
   for k,v in expected.items():need(p.get(k,'') in ['',v],'FOREIGN_STARTUP_'+k)
   inv=p.get('InvocationID','');need(not inv or (re.fullmatch('[0-9a-f]{32}',inv) and (self.invocation is None or inv==self.invocation)),'STARTUP_INVOCATION_DRIFT')
   if p.get('LoadState')=='not-found' or p.get('ActiveState')=='activating' or not self.owned(p):
    need(p.get('ActiveState') in ['inactive','activating','active'],'INVALID_STARTUP_STATE');self.state('ACKNOWLEDGED','PENDING_START');return 'PENDING_START'
   self.ownership(p)
   if p.get('ActiveState')=='active' and p.get('SubState')=='running':
    self.capacity(p);ack=self.gate.worker_ack();self.record('ACK_ORIGINAL',ack)
    if ack is None:self.state('ACKNOWLEDGED','PENDING_START');return 'PENDING_START'
    need(ack=={'binding':self.plan['binding'],'unit':self.plan['unit'],'invocation':self.invocation,'cgroup':self.plan['cgroup'],'phase':'BLOCKED_BEFORE_BROWSER'},'ACK_BINDING')
    self.state('GATED');return 'GATED'
   return self.capture_completion(p)
  except Exception as e:return self.unknown('POLL_START',e)
 def release(self):
  need(not self.replay_locked and self.phase=='GATED' and not self.released,'RELEASE_CONSUMED_OR_INELIGIBLE')
  try:
   need(self.clock()<self.deadline,'RELEASE180_DEADLINE');self.pins();p=self.read();self.ownership(p);self.capacity(p);need(p.get('ActiveState')=='active' and p.get('SubState')=='running','WORKER_NOT_BLOCKED_RUNNING')
   value={'binding':self.plan['binding'],'unit':self.plan['unit'],'invocation':self.invocation,'cgroup':self.plan['cgroup'],'token':self.plan['admission']['release_token']}
   self.released=True;self.record('GATE_ATTEMPTING',value);r=self.gate.release_once(value);self.record('GATE_RETURN_ORIGINAL',r)
   need(r.get('state')=='COMMITTED_VISIBLE_DURABLE' and r.get('permit_sha256')==digest(value),'RELEASE_VISIBLE_DURABILITY_UNKNOWN');self.state('RELEASED');return 'RELEASED'
  except Exception as e:return self.unknown('RELEASE',e)
 def capture_completion(self,p):
  self.ownership(p);need((p.get('ActiveState'),p.get('SubState')) in [('active','exited'),('inactive','dead'),('failed','failed')],'PROCESS_NOT_COMPLETED')
  need(p.get('ExecMainCode')in ['1','2','3'] and re.fullmatch('[0-9]{1,10}',p.get('ExecMainStatus','')),'EXIT_STATUS_NOT_EXPOSED')
  functional='PASS' if p.get('Result')=='success' and p['ExecMainCode']=='1' and p['ExecMainStatus']=='0' else 'FAIL'
  self.process_result={'functional_exit':functional,'native_result':p.get('Result'),'code':p['ExecMainCode'],'status':p['ExecMainStatus'],'oom':p.get('Result')=='oom-kill','original':p}
  self.record('NATIVE_PROCESS_COMPLETION_BEFORE_STOP',self.process_result);self.state('PROCESS_COMPLETED');return 'PROCESS_COMPLETED'
 def poll_completion(self):
  try:
   need(self.clock()<self.deadline,'RUNTIME180_DEADLINE');p=self.read();self.ownership(p)
   if p.get('ActiveState')=='active' and p.get('SubState')=='running':
    self.capacity(p);self.observation='PENDING_RUNNING';self.record('OBSERVATION',{'state':'PENDING_RUNNING'});return 'PENDING_RUNNING'
   return self.capture_completion(p)
  except Exception as e:return self.unknown('POLL_COMPLETION',e)
 def cleanup(self):
  need(not self.stop_attempted,'STOP_CONSUMED_NO_REPLAY')
  try:
   one=self.read(True);two=self.read(True);need(self.invocation is not None and self.owned(one) and self.owned(two) and one['InvocationID']==two['InvocationID'],'CLEANUP_DOUBLE_OWNER')
   self.stop_attempted=True;self.record('STOP_ATTEMPTING',{'unit':self.plan['unit'],'invocation':self.invocation})
   a=self.plan['admission'];r=self.call([a['binaries']['systemctl']['path'],'stop',self.plan['unit'],'--no-ask-password'],'OWNED_STOP',True)
   if r.get('exit')!=0:
    one=self.read(True);two=self.read(True);need(self.owned(one) and self.owned(two) and one['InvocationID']==two['InvocationID'],'KILL_DOUBLE_OWNER')
    self.record('OWNED_KILL_ATTEMPTING',one);self.call([a['binaries']['systemctl']['path'],'kill','--kill-who=all','--signal=KILL',self.plan['unit'],'--no-ask-password'],'OWNED_KILL',True)
   p=self.read(True);need(self.owned(p) and p.get('ActiveState')in ['inactive','failed'] and p.get('SubState')in ['dead','failed'],'POSTSTOP_IDENTITY_OR_INACTIVE_UNPROVED');self.capacity(p,True)
   self.cleanup_result={'owned_inactive_empty':True,'original':p};self.record('CLEANUP_TERMINAL',self.cleanup_result)
   # A known sameunit process result+owned empty stop may reconcile a prior
   # UNKNOWN; it never resets the launch/release/stop replay guards.
   self.state('TERMINAL' if self.process_result is not None or not self.uncertain else 'UNKNOWN');return self.phase
  except Exception as e:return self.unknown('CLEANUP',e)
 def run(self,sleep):
  result=self.start()
  for _ in range(180):
   if result in ['UNKNOWN','PROCESS_COMPLETED']:break
   if result=='GATED':result=self.release()
   elif result=='RELEASED' or result=='PENDING_RUNNING':result=self.poll_completion()
   elif result=='PENDING_START':result=self.poll_start()
   else:break
   if self.clock()>=self.deadline:result=self.unknown('OVERALL',Refusal('OVERALL180_DEADLINE'));break
   if result.startswith('PENDING'):sleep(min(1,max(0,self.deadline-self.clock())))
  if self.invocation is not None and not self.stop_attempted:self.cleanup()
  return {'phase':self.phase,'process':self.process_result,'cleanup':self.cleanup_result,'launch_consumed':self.attempted,'release_consumed':self.released,'uncertainty_history':self.uncertain}

def parse_props(original):
 need(original.get('exit')==0 and original.get('failure') is None and original.get('truncated') is False,'MANAGER_READBACK_INCOMPLETE')
 result={}
 for line in original['stdout'].splitlines():
  need('=' in line,'MANAGER_PARTIAL_PROPERTY');k,v=line.split('=',1);need(k not in result,'MANAGER_DUPLICATE_PROPERTY');result[k]=v
 return result

def open_nofollow(filename):
 path(filename);parts=filename[1:].split('/');fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
 try:
  for part in parts[:-1]:
   nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
  leaf=os.open(parts[-1],os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
  need(stat.S_ISREG(os.fstat(leaf).st_mode),'REGULAR_FILE_REQUIRED');return leaf
 finally:os.close(fd)
def bounded_bytes(filename,limit):
 fd=open_nofollow(filename)
 try:
  b=os.read(fd,limit+1);need(len(b)<=limit,'READ_TRUNCATED');return b
 finally:os.close(fd)
def incremental_hash(filename,clock=time.monotonic,max_bytes=268435456):
 fd=open_nofollow(filename);h=hashlib.sha256();total=0;end=clock()+5
 try:
  before=os.fstat(fd)
  while True:
   need(clock()<end,'HASH5_DEADLINE');b=os.read(fd,8192)
   if not b:break
   total+=len(b);need(total<=max_bytes,'HASH_FILE_BOUND');h.update(b)
  after=os.fstat(fd);need((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns),'HASH_FILE_DRIFT');return h.hexdigest()
 finally:os.close(fd)

def native_kernel(group):
 path(group);need(group.startswith('/trace294.slice/traceharbor-ui280-a2-') and group.endswith('.service'),'NONDEDICATED_CGROUP')
 base='/sys/fs/cgroup'+group;raw={'path':group,'truncated':False,'originals':{}}
 try:
  for name,limit in [('memory.max',128),('memory.swap.max',128),('memory.current',128),('memory.events',1024),('cgroup.events',1024)]:
   b=bounded_bytes(base+'/'+name,limit);raw['originals'][name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'text':b.decode('ascii')}
  raw['memory.max']=raw['originals']['memory.max']['text'].strip();raw['memory.swap.max']=raw['originals']['memory.swap.max']['text'].strip()
  events={}
  for line in raw['originals']['cgroup.events']['text'].splitlines():
   k,v=line.split();need(k not in events,'CGROUP_DUPLICATE');events[k]=v
  need(events.get('populated')in ['0','1'],'CGROUP_POPULATION_MISSING');raw['populated']=events['populated']=='1'
 except Exception as e:raw['error']=type(e).__name__+':'+str(e)
 return raw

def require_pre_app(plan,obs):
 a=plan['admission'];need(obs.get('uid')==a['uid']and obs.get('gid')==a['gid']and obs.get('cgroup')==plan['cgroup']and re.fullmatch('[0-9a-f]{32}',obs.get('invocation','')),'ACTUAL_UNIT_IDENTITY')
 need(obs.get('memory.max')=='335544320'and obs.get('memory.swap.max')=='0'and obs.get('virtual_as')==a['virtual_as']and obs.get('virtual_as_hard')==a['virtual_as'],'ACTUAL_KERNEL_LIMITS')
 need(obs.get('sandbox')is True and obs.get('private_network')is True and obs.get('mounts_protected')is True,'ACTUAL_PREAPP_ISOLATION')
def observe_pid(plan,pid,invocation):
 a=plan['admission'];base='/proc/'+str(integer(pid,1,2147483647));status=bounded_bytes(base+'/status',8192).decode();fields={x.split(':',1)[0]:x.split(':',1)[1].strip()for x in status.splitlines()if ':'in x};membership=bounded_bytes(base+'/cgroup',2048).decode().splitlines();need(len(membership)==1 and membership[0].startswith('0::'),'SELF_CGROUP_DOMAIN');group=membership[0][3:];raw=native_kernel(group)
 ns={n:os.readlink(base+'/ns/'+n)for n in ['net','mnt','user','cgroup']};limits=bounded_bytes(base+'/limits',8192).decode();m=re.search(r'Max address space\s+(\d+)\s+(\d+)',limits);need(m,'AS_NATIVE_EXPOSED');mounts=bounded_bytes(base+'/mountinfo',65536).decode().splitlines();table={x.split()[4]:set(x.split()[5].split(','))for x in mounts};protected=all('ro'in table.get(a[k],set())for k in ['source','control'])and'rw'in table.get(a['out'],set())
 return {'uid':int(fields['Uid'].split()[1]),'gid':int(fields['Gid'].split()[1]),'cgroup':group,'invocation':invocation,'memory.max':raw.get('memory.max'),'memory.swap.max':raw.get('memory.swap.max'),'virtual_as':int(m[1]),'virtual_as_hard':int(m[2]),'sandbox':fields.get('NoNewPrivs')=='1'and int(fields.get('CapEff','1'),16)==0,'private_network':ns['net']!=a['parent_netns'],'mounts_protected':protected and ns['mnt']!=a['parent_mntns'],'status_original':fields,'namespace_original':ns,'kernel_original':raw,'mountinfo_sha256':hashlib.sha256(('\n'.join(mounts)).encode()).hexdigest()}
def native_self(plan):return observe_pid(plan,os.getpid(),os.environ.get('INVOCATION_ID',''))
def native_unit_observation(plan,props):return observe_pid(plan,int(props.get('MainPID','0')),props.get('InvocationID',''))
def resident_job_bound():
 text=bounded_bytes('/proc/1/status',8192).decode();m=re.search(r'^VmRSS:\s+(\d+) kB',text,re.M);need(m,'MANAGER_RSS_UNEXPOSED');manager=int(m[1])*1024;reserved=335544320+67108864+100663296+manager;need(reserved<=536870912,'WHOLE_RESIDENT512_BEFORE_APP');return {'scope':'ADMITTED_JOB_CONTROLLER64_WORKER320_ONE_CONTROL_CHILD96_AND_FULL_PID1_RSS','manager_rss':manager,'reserved_resident_upperbound':reserved,'cap':536870912,'not_artifact_forecast':True}

def group_members(pgid):
 result=[]
 for n in os.listdir('/proc'):
  if not n.isdigit():continue
  try:
   parts=bounded_bytes('/proc/'+n+'/stat',4096).decode().rpartition(') ')[2].split()
   if int(parts[2])==pgid and int(parts[3])==pgid:result.append(int(n))
  except (OSError,ValueError,IndexError,Refusal):continue
 return result
def child96():
 resource.setrlimit(resource.RLIMIT_AS,(100663296,100663296));resource.setrlimit(resource.RLIMIT_CPU,(5,5));resource.setrlimit(resource.RLIMIT_FSIZE,(16777216,16777216));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
WORKER_ENV_NAMES={'PATH','HOME','LANG','GITHUB_ACTIONS','RUNNER_ENVIRONMENT','GITHUB_EVENT_NAME','GITHUB_RUN_ATTEMPT','GITHUB_RUN_ID','GITHUB_SHA','GITHUB_REPOSITORY','GITHUB_ACTOR_ID','GITHUB_EVENT_PATH','TRACE267_WORKFLOW_SHA','TRACE280_UNIT','TRACE280_PARENT_NETNS','INVOCATION_ID','GITHUB_REF','TRACE295_RUNTIME_CONFIG','TRACE295_RUNTIME_SHA'}
def native_process(argv,timeout,limit,env,stdout_path=None,child_limit=child96):
 need(0<timeout<=180 and 1<=limit<=65536,'PROCESS_BOUND');need(set(env)==({'PATH','HOME','LANG'} if child_limit is not None else WORKER_ENV_NAMES),'PROCESS_ENV')
 start=time.monotonic();p=None;sel=selectors.DefaultSelector();out={'stdout':bytearray(),'stderr':bytearray()};r={'argv':argv,'exit':'NOT_EXPOSED','stdout':'','stderr':'','failure':None,'truncated':False,'own_cleanup':[]};capture=None
 try:
  if stdout_path is not None:capture=os.open(stdout_path,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,0o600)
  p=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,start_new_session=True,preexec_fn=child_limit,close_fds=True)
  for name in ['stdout','stderr']:sel.register(getattr(p,name),selectors.EVENT_READ,name)
  while sel.get_map():
   need(time.monotonic()-start<timeout,'PROCESS_DEADLINE')
   if child_limit is not None:
    def vm(pid):
     text=bounded_bytes('/proc/'+str(pid)+'/status',8192).decode()
     return next(int(line.split()[1])*1024 for line in text.splitlines() if line.startswith('VmSize:'))
    need(vm(os.getpid())+sum(vm(pid)for pid in group_members(p.pid))<=167772160,'MANAGER_GROUP_VIRTUAL160_BOUND')
   for key,_ in sel.select(min(.05,max(0,timeout-(time.monotonic()-start)))):
    b=os.read(key.fileobj.fileno(),8192)
    if not b:sel.unregister(key.fileobj);continue
    if capture is not None:
     view=memoryview(b)
     while view:
      n=os.write(capture,view);need(n>0,'OUTPUT_WRITE');view=view[n:]
    room=limit-sum(map(len,out.values()));out[key.data].extend(b[:max(0,room)])
    if len(b)>room:r['truncated']=True;raise Refusal('PROCESS_OUTPUT_BOUND')
  p.wait(timeout=max(.001,timeout-(time.monotonic()-start)));need(not group_members(p.pid),'OWNED_DESCENDANTS_REMAIN')
 except Exception as e:
  r['failure']=type(e).__name__+':'+str(e)
  if p is not None:
   for sig,wait in [(signal.SIGTERM,.2),(signal.SIGKILL,1)]:
    members=group_members(p.pid)
    if members:
     try:os.killpg(p.pid,sig);r['own_cleanup'].append({'signal':sig,'owned_members':members})
     except ProcessLookupError:pass
    try:
     p.wait(timeout=wait)
     if not group_members(p.pid):break
    except subprocess.TimeoutExpired:pass
   r['remaining_owned_members']=group_members(p.pid)
 finally:
  if p is not None:
   r['exit']=p.returncode
   for f in [p.stdout,p.stderr]:f.close()
  sel.close()
  if capture is not None:os.fsync(capture);os.close(capture)
  r.update({k:v.decode(errors='replace')for k,v in out.items()});r['elapsed_s']=time.monotonic()-start
 return r

class ManagerTransport:
 def __init__(self,verified,plan,runner=native_process,hash_reader=incremental_hash):
  need(isinstance(verified,VerifiedAdmission) and digest(verified.body)==plan['binding'],'MANAGER_NATIVE_AUTHORITY');self.a=verified.body;self.plan=plan;self.runner=runner;self.hash=hash_reader;self.total=0
 def __call__(self,argv,timeout,limit,env):
  need(0<timeout<=5 and limit==32768 and env=={'PATH':'/usr/bin:/bin','HOME':self.a['home'],'LANG':'C.UTF-8'},'MANAGER_BOUNDS_ENV')
  launch=launch_argv(self.plan);ctl=self.a['binaries']['systemctl'];run=self.a['binaries']['systemd-run']
  if argv==launch:binary=run
  else:
   need(argv[0]==ctl['path'] and self.plan['unit'] in argv and argv[1]in ['show','stop','kill'] and not any(x in argv for x in ['--force','--all','--replace']),'MANAGER_COMMAND_SCOPE');binary=ctl
   if argv[1]=='show':need(argv[2]==self.plan['unit'] and len(argv)==6 and argv[3]=='--no-pager' and argv[4]=='--no-ask-password' and argv[5].startswith('--property='),'MANAGER_READ_SCOPE')
   if argv[1]=='stop':need(argv==[ctl['path'],'stop',self.plan['unit'],'--no-ask-password'],'MANAGER_STOP_SCOPE')
   if argv[1]=='kill':need(argv==[ctl['path'],'kill','--kill-who=all','--signal=KILL',self.plan['unit'],'--no-ask-password'],'MANAGER_KILL_SCOPE')
  need(self.hash(binary['path'])==binary['sha256'],'MANAGER_BINARY_PIN');r=self.runner(argv,timeout=timeout,limit=limit,env=env);self.total+=len(r.get('stdout','').encode())+len(r.get('stderr','').encode())
  # The supervisor persists the exact original before judging total/truncation.
  r['transport_cumulative_bytes']=self.total;return r

class GatePair:
 def __init__(self,ack,control):self.ack=ack;self.control=control
 def worker_ack(self):return self.ack.read('ack294.json')
 def release_once(self,value):return self.control.write_once('release294.json',value)

class Worker:
 def __init__(self,plan,gate,ack,journal,clock,observe=native_self,hash_reader=incremental_hash):
  self.plan=plan;self.gate=gate;self.ack=ack;self.journal=journal;self.clock=clock;self.observe=observe;self.hash=hash_reader;self.executed=any(e.get('event')=='WORKER_EXEC_ATTEMPTING'for e in journal.events)
 def record(self,event,data):self.journal.append({'binding':self.plan['binding'],'event':event,'data':data,'at':self.clock()})
 def run(self,execute,sleep):
  need(not self.executed and not getattr(self.journal,'readonly',False),'WORKER_EXEC_CONSUMED');p=self.plan;a=p['admission'];deadline=self.clock()+180
  initial=self.observe(p);self.record('WORKER_INITIAL_ORIGINAL',initial);require_pre_app(p,initial);need(initial.get('uid')==a['uid'] and initial.get('cgroup')==p['cgroup'] and re.fullmatch('[0-9a-f]{32}',initial.get('invocation','')),'WORKER_INITIAL_OWNER')
  ack={'binding':p['binding'],'unit':p['unit'],'invocation':initial['invocation'],'cgroup':p['cgroup'],'phase':'BLOCKED_BEFORE_BROWSER'};result=self.ack.write_once('ack294.json',ack);self.record('ACK_PUBLICATION_ORIGINAL',result);need(result.get('state')=='COMMITTED_VISIBLE_DURABLE','ACK_PERSISTENCE_UNKNOWN')
  for _ in range(180):
   need(self.clock()<deadline,'WORKER180_DEADLINE');permit=self.gate.read('release294.json');self.record('PERMIT_ORIGINAL',permit)
   if permit is None:sleep(min(1,max(0,deadline-self.clock())));continue
   own=self.observe(p);self.record('WORKER_SELF_ORIGINAL',own);require_pre_app(p,own)
   need(permit=={'binding':p['binding'],'unit':p['unit'],'invocation':initial['invocation'],'cgroup':p['cgroup'],'token':a['release_token']},'WORKER_PERMIT_BINDING')
   need(own.get('uid')==a['uid'] and own.get('invocation')==initial['invocation'] and own.get('cgroup')==p['cgroup'] and own.get('memory.max')=='335544320' and own.get('memory.swap.max')=='0' and own.get('virtual_as')==a['virtual_as'] and own.get('virtual_as_hard')==a['virtual_as'] and own.get('sandbox')is True and own.get('private_network')is True,'WORKER_KERNEL_VIRTUAL_SANDBOX')
   for name,x in a['binaries'].items():need(self.hash(x['path'])==x['sha256'],'WORKER_BINARY_PIN')
   for name,pin in a['source_pins'].items():need(self.hash(a['source']+'/'+name)==pin,'WORKER_SOURCE_PIN')
   eff=a['approved_runtime_config']['effective_chrome'];need(self.hash(eff['realpath'])==eff['sha256'],'CHROME_EFFECTIVE_DRIFT')
   self.executed=True;argv=[a['binaries']['node']['path'],'--max-old-space-size=32',a['source']+'/tools/ui267/qualify.mjs','--source',a['source'],'--out',a['out']+'/result']
   self.record('WORKER_EXEC_ATTEMPTING',{'argv':argv,'virtual_as':a['virtual_as'],'kernel_max':335544320})
   env={'PATH':'/usr/bin:/bin','HOME':a['home'],'LANG':'C.UTF-8','GITHUB_ACTIONS':'true','RUNNER_ENVIRONMENT':'github-hosted','GITHUB_EVENT_NAME':'push','GITHUB_RUN_ATTEMPT':'1','GITHUB_RUN_ID':a['run_id'],'GITHUB_SHA':a['source_commit'],'GITHUB_REPOSITORY':a['repository'],'GITHUB_ACTOR_ID':'273768139','GITHUB_EVENT_PATH':a['control']+'/event294.json','TRACE267_WORKFLOW_SHA':a['source_commit'],'TRACE280_UNIT':p['unit'],'TRACE280_PARENT_NETNS':a['parent_netns'][5:-1],'INVOCATION_ID':initial['invocation'],'GITHUB_REF':'refs/heads/review/traceharbor-v1-browser-qa-base180-162-20261023','TRACE295_RUNTIME_CONFIG':a['control']+'/runtime295.json','TRACE295_RUNTIME_SHA':hashlib.sha256(canonical(a['approved_runtime_config'])).hexdigest()}
   r=execute(argv,timeout=min(180,deadline-self.clock()),limit=32768,env=env,stdout_path=a['out']+'/worker294.log',child_limit=None)
   self.record('WORKER_EXEC_RETURN_ORIGINAL',r);need(len(r.get('stdout','').encode())+len(r.get('stderr','').encode())<=32768 and r.get('truncated')is False,'WORKER_OUTPUT_BOUND')
   return r
  raise Refusal('WORKER_GATE_FINITE_BOUND')

class NativeStorage:
 def __init__(self,plan):
  a=plan['admission'];self.controller_dir=SafeDirectory(a['controller'],uid=0,mode=0o700);self.control_dir=SafeDirectory(a['control'],uid=0,mode=0o750,gid=a['gid']);self.ack_dir=SafeDirectory(a['out'],uid=a['uid'],mode=0o700)
  self.control=AtomicFiles(self.control_dir,0o440);self.ack=AtomicFiles(self.ack_dir);self.pair=GatePair(self.ack,self.control)
 def journal(self,binding):return Journal(self.controller_dir,binding)
 def worker_journal(self,binding):return Journal(self.ack_dir,binding,'worker294.jsonl')
 def context(self,plan,name):
  raw=self.control.read_bytes(name);need(raw is not None,'CONTEXT_MISSING');return verify_context_transport(plan,raw)
 def publish_plan(self,plan):
  self.context(plan,'native-context298.json');return self.control.write_once('plan294.json',plan)
 def publish_event(self,plan):return self.control.write_once('event294.json',plan['admission']['runtime_event'])
 def publish_anchor(self,plan):
  context=self.context(plan,'native-context298.json');result=self.control.write_once('anchor295.json',plan['admission']['native_anchor_payload']);need(self.control.write_once('derived298.json',context).get('state')=='COMMITTED_VISIBLE_DURABLE','DERIVED_CONTEXT_PUBLICATION');self.context(plan,'derived298.json');return result
 def publish_runtime(self,plan):return self.control.write_once('runtime295.json',plan['admission']['approved_runtime_config'])

def verify_context_transport(plan,raw):
 import importlib.util
 a=plan['admission'];p=a['source']+'/tools/ui280/native298.py';need(os.path.realpath(p)==p,'CONTEXT_VERIFIER_PATH')
 need(incremental_hash(p)==a['source_pins']['tools/ui280/native298.py'],'CONTEXT_VERIFIER_PIN')
 spec=importlib.util.spec_from_file_location('native298_transport',p);n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
 c=strict_json(raw);n.verify_transport(c,raw,a);return c

def read_worker_plan(filename,binding):
 # Immutable root-owned read-only control directory is mounted read-only to
 # worker. Nonroot worker cannot forge a release; opaque token alone is no auth.
 directory=os.path.dirname(filename);d=SafeDirectory(directory,uid=0,mode=0o750);files=AtomicFiles(d,0o440)
 try:
  need(os.path.basename(filename)=='plan294.json','WORKER_PLAN_FILENAME');plan=files.read('plan294.json')
  need(plan is not None,'WORKER_PLAN_MISSING');raw=files.read_bytes('derived298.json');need(raw is not None,'CONTEXT_MISSING');verify_context_transport(plan,raw)
 finally:d.close()
 need(plan and plan.get('binding')==binding and digest(plan.get('admission'))==binding,'WORKER_PLAN_BINDING')
 need(prepare_shape(plan),'WORKER_PLAN_SHAPE');return plan
def prepare_shape(plan):
 a=plan['admission'];need(plan['unit']=='traceharbor-ui280-a2-'+a['run_id']+'.service' and plan['cgroup']==a['cgroup_parent']+'/'+plan['unit'],'WORKER_UNIT_BINDING');return True

def dormant_pipeline(verified,runner=native_process,kernel=native_kernel,hash_reader=incremental_hash,storage_factory=NativeStorage,clock=time.monotonic,sleep=time.sleep):
 need(isinstance(verified,VerifiedAdmission),'NATIVE_ADMISSION_REQUIRED');need(resource.getrlimit(resource.RLIMIT_AS)==(67108864,100663296),'CONTROLLER64_96_REQUIRED');plan=prepare(verified);storage=storage_factory(plan)
 published=storage.publish_plan(plan);need(published.get('state')=='COMMITTED_VISIBLE_DURABLE','PLAN_PUBLICATION_UNKNOWN')
 published_event=storage.publish_event(plan);need(published_event.get('state')=='COMMITTED_VISIBLE_DURABLE','EVENT_PUBLICATION_UNKNOWN')
 need(storage.publish_anchor(plan).get('state')=='COMMITTED_VISIBLE_DURABLE','ANCHOR_PUBLICATION_UNKNOWN');need(storage.publish_runtime(plan).get('state')=='COMMITTED_VISIBLE_DURABLE','RUNTIME_PUBLICATION_UNKNOWN')
 journal=storage.journal(plan['binding']);transport=ManagerTransport(verified,plan,runner,hash_reader);supervisor=Supervisor(plan,transport,journal,storage.pair,clock,kernel,hash_reader)
 return supervisor.run(sleep)

def worker_entry(filename,binding,plan_reader=read_worker_plan,storage_factory=None,observe=native_self,runner=native_process,hash_reader=incremental_hash,clock=time.monotonic,sleep=time.sleep):
 plan=plan_reader(filename,binding);a=plan['admission']
 if storage_factory is None:
  control=AtomicFiles(SafeDirectory(a['control'],uid=0,mode=0o750,gid=a['gid']),0o440)
  ack=AtomicFiles(SafeDirectory(a['out'],uid=a['uid'],mode=0o700));journal=Journal(ack.d,binding,'worker294.jsonl')
 else:control,ack,journal=storage_factory(plan)
 worker=Worker(plan,control,ack,journal,clock,observe,hash_reader)
 r=worker.run(runner,sleep);return 0 if r.get('exit')==0 and r.get('failure')is None else 1

if __name__=='__main__':raise SystemExit('REVIEWED_BOOTSTRAP295_REQUIRED')
