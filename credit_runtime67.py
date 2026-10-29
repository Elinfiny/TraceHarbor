"""New scope, one conditional slot002 from the existing allocation. No import I/O.
The old runtime, admission, ledger configuration and HTTP endpoints stay closed.
"""
import hashlib,json,os,subprocess,sys,threading,time,re
from pathlib import Path
import release_integration68 as legacy
from release_integration68 import ReleaseHandler,ipaddress,HOST
import runtime_service,release_policy,provider_receipt67,credit_scope67 as scope
from quota_ledger import Ledger,read,exclusive,ReservationUnknown
from release_policy import Refusal,digest,canonical,deadline,input_admission
from live_service import build_record,verified_analysis
NEW_REQUEST=None # Filled from the source-pinned private contract at Native install.

class Slot002(Ledger):
 def reserve(self,request_sha,cost,now=None):
  deadline(self.config,now)
  if not isinstance(request_sha,str)or not re.fullmatch('[a-f0-9]{64}',request_sha)or type(cost)is not int or not 360060<=cost<=851520 or request_sha in self.config['blocked_request_sha256']:raise Refusal('RESERVATION_SHAPE')
  with self.locked():
   count,total,seen=self.scan()
   if count!=1 or request_sha in seen or total+cost>self.config['budget_nanodollars']:raise Refusal('EXACT_SLOT002_ONLY_NO_RETRY')
   value={'slot':2,'request_sha256':request_sha,'reserve_nanodollars':cost,'config_sha256':digest(self.config),'state':'RESERVED_UNKNOWN_NO_RETRY'}
   try:exclusive(self.path/'slot-002.json',value)
   except FileExistsError:raise Refusal('SLOT002_ALREADY_CONSUMED')from None
   except OSError:raise ReservationUnknown('SLOT002_UNKNOWN_NO_RETRY')from None
   return value

class Certificate:
 def __init__(self,certificate):self.certificate=dict(certificate)
 def count(self,payload):
  if self.certificate['request_sha256']!=digest(payload):raise Refusal('EXACT_NEW_COUNTER_CERTIFICATE_REQUIRED')
  return dict(self.certificate)

def full_ack(directory):
 directory=Path(directory)
 for n in ('full/failure.json','full/terminal.json','mark-flow-failed.json','mark-runtime-failed.json'):
  if(directory/n).exists():raise Refusal('FULL_ALREADY_CLOSED')
 q=read(directory/'native/qualified.json',65536)
 if q.get('state')!='PASS'or read(directory/'preview-ready.json')['native_sha256']!=q['sha256']:raise Refusal('NATIVE_PREVIEW_REQUIRED')
 first=read(directory/'full/chunk-00000.json');part=directory/'full/chunk-00000.webm'
 import recovery86
 recovery86.regular(part)
 if not 0<part.stat().st_size<=1048576:raise Refusal('FULL_FIRST_ACK_REQUIRED')
 data=part.read_bytes()
 if first['sequence']!=0 or not 0<len(data)<=1048576 or first['bytes']!=len(data)or first['sha256']!=hashlib.sha256(data).hexdigest():raise Refusal('FULL_FIRST_ACK_REQUIRED')
 if not(directory/'full/reserved.json').exists()or not(directory/'demo-execution-reserved.json').exists():raise Refusal('RECORDED_WORKFLOW_NOT_STARTED')
 return first

class Session:
 def __init__(self,m,*,factory=None,environment=None):
  self.m=m;self.config=m.config;self.factory=factory;self.environment=os.environ if environment is None else environment
 def dispatch(self,raw):
  m=self.m;scope.authority(m);scope.credit(m,600);scope.ledger(m,unspent=True);full_ack(m.root)
  evidence,payload,encoded=runtime_service.prepare(raw)
  if digest(payload)!=m.p['request_sha256']:raise Refusal('EXACT_DISTINCT_NEW_REQUEST_ONLY')
  cert=Certificate(m.p['certificate']).count(payload);cost=input_admission(payload,cert,self.config)
  key=runtime_service._credential(self.environment)
  allocation=Slot002(scope.ORIGINAL/'allocation',self.config);reservation=allocation.reserve(digest(payload),cost)
  boundary=runtime_service.nebius.HTTPBoundary(time.monotonic()+runtime_service.DEADLINE_SECONDS,runtime_service._MemoryCapture(),**({'factory':self.factory}if self.factory is not None else{}))
  result=None
  try:
   # Revalidate once after reservation; failure consumes the reservation, never a retry.
   scope.credit(m,600);deadline(self.config)
   body=boundary.exchange(encoded,key,runtime_service.nebius.EXPECTED_PROJECT_ID)
   if key.encode()in body:raise Refusal('SECRET_REFUSED')
   analysis,metadata=runtime_service.nebius.decode_response(body,self.config['model'])
   if key in canonical(analysis).decode()or key in canonical(metadata).decode():raise Refusal('SECRET_REFUSED')
   if metadata['usage']['prompt_tokens']!=cert['count']:
    exclusive(m.root/'counter-drift.json',{'state':'CLOSED_NO_RESET','expected':cert['count']});raise Refusal('COUNTER_USAGE_DRIFT')
   metadata['request_sha256']=digest(payload);verified_analysis(analysis,evidence)
   result={'schema':runtime_service.SCHEMA,'mode':'SERVER_RUNTIME_RECORD_ORIGIN_UNATTESTED','record':build_record(raw,analysis,metadata),'attempt':{'request_attempted':True,'retry':False,'origin':'NOT_INDEPENDENTLY_ATTESTED','deadline_seconds':runtime_service.DEADLINE_SECONDS},'limits':runtime_service.LIMITS}
   result['dossier_sha256']=digest(result);runtime_service.verify_runtime_result(result)
  except Exception:result=None
  try:provider_receipt67.retain(boundary,m.root,key)
  except Exception:result=None
  try:allocation.terminal(reservation,result is not None)
  except Exception:result=None
  if result is None:raise runtime_service.RuntimeRefusal('NEW_SLOT002_OUTCOME_UNKNOWN_NO_RETRY',consumed=True)
  return result

class CapturedOnceSession:
 def __init__(self,config,directory,sink,*,gate,worker=None):
  self.config=config;self.directory=Path(directory);self.sink=sink;self.gate=gate;self.worker=run_worker if worker is None else worker;self.lock=threading.Lock()
 def status(self):
  return {'enabled':bool(self.sink and self.sink.bytes>0 and not self.sink.terminal and not(self.directory/'e2e-reserved.json').exists()),'retry':False}
 def dispatch(self,raw):
  _,payload,_=runtime_service.prepare(raw)
  if digest(payload)!=NEW_REQUEST:raise runtime_service.RuntimeRefusal('EXACT_NEW_REQUEST_ONLY')
  with self.lock:
   if not self.status()['enabled']:raise runtime_service.RuntimeRefusal('ONCE_FULL_ACK_GATE')
   self.gate();full_ack(self.directory)
   exclusive(self.directory/'e2e-reserved.json',{'state':'UNKNOWN_CONSUMED_NO_RETRY','request_sha256':NEW_REQUEST,'recorded_bytes_before_dispatch':self.sink.bytes,'recorded_chunks_before_dispatch':self.sink.next,'retry':False})
   return self.worker(raw,self.config,self.directory)

def run_worker(raw,config,directory):
 if Path(directory)!=scope.ROOT:raise Refusal('EXACT_NEW_WORKER_ROOT')
 command=[sys.executable,str(Path(__file__).parent/'render_recorded_release70.py'),'--credit-worker67',str(scope.ROOT)]
 environment={k:v for k,v in os.environ.items()if k in {'PATH','LANG','LC_ALL','NEBIUS_API_KEY','RENDER','RENDER_EXTERNAL_HOSTNAME','RENDER_GIT_COMMIT'}};environment['PYTHONDONTWRITEBYTECODE']='1'
 def limits():
  import resource
  resource.setrlimit(resource.RLIMIT_CPU,(10,10));resource.setrlimit(resource.RLIMIT_FSIZE,(1048576,1048576));resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
 proc=None
 try:
  import worker_scope67 as w
  w.assert_startup();initial=w.aggregate()
  if initial['current_bytes']>=w.PROFILE['aggregate_abort_bytes']:raise Refusal('NO_AI_AGGREGATE_HEADROOM')
  with w.serialized(scope.ROOT/'worker113'):
   proc=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=environment,preexec_fn=limits,start_new_session=True)
   proc.stdin.write(raw);proc.stdin.close()
   measured,out=w.collect(proc,{'wall':40})
   after=w.aggregate();measured.update(oom_kill_delta=after['oom_kill']-initial['oom_kill'],identity=w.identity(),retry=False)
   exclusive(Path(directory)/'ai-worker-receipt.json',measured)
  if measured['returncode']!=0 or measured['guard']or measured['oom_kill_delta']!=0 or len(out)>runtime_service.MAX_RESULT:raise Refusal('NEW_WORKER_OUTCOME_UNKNOWN')
  value=runtime_service.verify_runtime_result(json.loads(out));exclusive(Path(directory)/'e2e-result.json',value);return value
 except Exception:raise runtime_service.RuntimeRefusal('NEW_E2E_OUTCOME_UNKNOWN_NO_RETRY',consumed=True)from None
 finally:
  if proc is not None:
   try:
    if proc.poll()is None:w.stop(proc)
   except Exception:pass # Outer reservation remains UNKNOWN, never re-dispatched.
   for pipe in(proc.stdin,proc.stdout,proc.stderr):
    try:pipe.close()
    except Exception:pass

def worker(config,p):
 import recovery67
 m=recovery67.Recovery(scope.ROOT,scope.ORIGINAL,config,p)
 if not(m.root/'e2e-reserved.json').exists():raise Refusal('NATIVE_PARENT_RESERVATION_REQUIRED')
 raw=sys.stdin.buffer.read(runtime_service.MAX_REQUEST+1)
 if len(raw)>runtime_service.MAX_REQUEST:raise Refusal('REQUEST_BOUND')
 result=Session(m).dispatch(raw);sys.stdout.buffer.write(canonical(result));sys.stdout.buffer.flush()
