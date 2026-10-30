"""New scope, one proposed distinct slot003 from the existing allocation. No import I/O.
The old runtime, admission, ledger configuration and HTTP endpoints stay closed.
"""
import hashlib,json,os,subprocess,sys,threading,time,re
from pathlib import Path
import release_integration68 as legacy
from release_integration68 import ReleaseHandler,ipaddress,HOST
import runtime_service,release_policy,provider_receipt004,credit_scope004 as scope
from quota_ledger import Ledger,read,exclusive,ReservationUnknown
from release_policy import Refusal,digest,canonical,deadline,input_admission
from live_service import build_record,verified_analysis
NEW_REQUEST=None # Filled from the source-pinned private contract at Native install.

class Slot004(Ledger):
 def reserve(self,request_sha,cost,now=None):
  deadline(self.config,now)
  if request_sha!=scope.contract()['request_sha256']or self.config!=scope.contract()['release_config']or type(cost)is not int or cost!=456420 or request_sha in self.config['blocked_request_sha256']:raise Refusal('RESERVATION_SHAPE')
  with self.locked():
   count,total,seen=self.scan()
   import source_extension004
   source_extension004.check_history(scope.contract()['history'])
   if count!=3 or request_sha in seen or total+cost>self.config['budget_nanodollars']:raise Refusal('EXACT_SLOT004_ONLY_NO_RETRY')
   value={'slot':4,'request_sha256':request_sha,'reserve_nanodollars':cost,'config_sha256':digest(self.config),'state':'RESERVED_UNKNOWN_NO_RETRY'}
   try:exclusive(self.path/'slot-004.json',value)
   except FileExistsError:raise Refusal('SLOT004_ALREADY_CONSUMED')from None
   except OSError:raise ReservationUnknown('SLOT004_UNKNOWN_NO_RETRY')from None
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
  # No socket, DNS, HTTP or ledger write: validate and construct locally FIRST.
  allocation=Slot004(scope.ORIGINAL/'allocation',self.config)
  boundary,connection=transport_preflight96(self.factory)
  reservation=None;attempted=False;result=None;stage='RESERVATION';error=None
  try:
   attempted=True;reservation=allocation.reserve(digest(payload),cost)
   exclusive(m.root/'ai-dispatch96.json',{'state':'UNKNOWN_CONSUMED_NO_RETRY','stage':'RESERVED_BEFORE_EXCHANGE','request_attempted':'UNKNOWN','request_sha256':digest(payload),'retry':False})
   stage='POST_RESERVATION_GUARDS';scope.credit(m,600);deadline(self.config)
   stage='EXCHANGE';body=boundary.exchange(encoded,key,runtime_service.nebius.EXPECTED_PROJECT_ID)
   stage='COMPLETION_METADATA';provider_receipt004.retain_completion343(body,m.root,self.config['model'])
   if key.encode()in body:raise Refusal('SECRET_REFUSED')
   stage='VALIDATION';analysis,metadata=runtime_service.nebius.decode_response(body,self.config['model'])
   if key in canonical(analysis).decode()or key in canonical(metadata).decode():raise Refusal('SECRET_REFUSED')
   if metadata['usage']['prompt_tokens']!=cert['count']:
    exclusive(m.root/'counter-drift.json',{'state':'CLOSED_NO_RESET','expected':cert['count']});raise Refusal('COUNTER_USAGE_DRIFT')
   metadata['request_sha256']=digest(payload);verified_analysis(analysis,evidence)
   result={'schema':runtime_service.SCHEMA,'mode':'SERVER_RUNTIME_RECORD_ORIGIN_UNATTESTED','record':build_record(raw,analysis,metadata),'attempt':{'request_attempted':True,'retry':False,'origin':'NOT_INDEPENDENTLY_ATTESTED','deadline_seconds':runtime_service.DEADLINE_SECONDS},'limits':runtime_service.LIMITS}
   result['dossier_sha256']=digest(result);runtime_service.verify_runtime_result(result)
  except BaseException as exc:
   result=None;error=safe_exception96(exc,stage,boundary)
  finally:
   # Hard kill cannot run finally: persistent reservation + parent workerreceipt
   # remain UNKNOWN. Never invent a completed terminal or release the slot.
   try:connection.close()
   except BaseException as cleanup_error:
    result=None
    if error is None:error=safe_exception96(cleanup_error,'CLEANUP',boundary)
   if attempted:
    if error is None:error={'stage':'VALIDATION_COMPLETE','exception_type':None,'original_exception_bytes':0,'original_exception_sha256':hashlib.sha256(b'').hexdigest(),'request_attempted':boundary.request_attempted,'retry':False}
    try:exclusive(m.root/'ai-diagnostic96.json',error)
    except Exception:result=None
    try:provider_receipt004.retain(boundary,m.root,key)
    except Exception:result=None
    try:
     if reservation is not None:allocation.terminal(reservation,result is not None)
    except Exception:result=None
  if result is None:raise runtime_service.RuntimeRefusal('NEW_SLOT004_OUTCOME_UNKNOWN_NO_RETRY',consumed=attempted)
  return result

def safe_exception96(exc,stage,boundary):
 # Hash actual caught exception strings and retained original transport
 # exceptions in memory only. No raw traceback, key, body or exception text.
 names={'ValueError','TypeError','RuntimeError','ProviderError','RuntimeRefusal','Refusal','TimeoutError','OSError','KeyboardInterrupt','SystemExit'}
 def metadata(e):
  try:raw=str(e).encode('utf8','replace');n=len(raw);h=hashlib.sha256(raw).hexdigest();available=True
  except BaseException:n=None;h=None;available=False
  return {'exception_type':type(e).__name__ if type(e).__name__ in names else 'OtherException','original_exception_bytes':n,'original_exception_sha256':h,'exception_string_available':available,'hash_scope':'ACTUAL_EXCEPTION_STRING_NOT_TRACEBACK'}
 value=dict(metadata(exc),stage=stage,request_attempted=bool(boundary.request_attempted),state='UNKNOWN_CONSUMED_NO_RETRY',retry=False)
 value['transport_original_exceptions']=[dict(metadata(e),stage=where if re.fullmatch('[A-Z_]{1,64}',where or'')else 'OTHER_STAGE')for where,kind,e in boundary.vault.originals if kind in('EXCEPTION','CAPTURE_EXCEPTION')][:16]
 return value

def transport_preflight96(factory):
 if factory is None:raise runtime_service.nebius.ProviderError('NATIVE_CAPTURE_OR_TRANSPORT_UNBOUND')
 connection=None
 try:
  # HTTPSConnection construction is local. Explicit factory is bound only by
  # Native worker; tests replace that standard dependency with a denying fake.
  connection=factory('api.tokenfactory.nebius.com',timeout=30)
  if connection.host!='api.tokenfactory.nebius.com' or connection.port!=443 or getattr(connection,'sock',None)is not None or not all(callable(getattr(connection,n,None))for n in ('request','getresponse','close')):raise Refusal('LOCAL_TRANSPORT_PREFLIGHT_REFUSED')
  claimed=False
  def take(host,*,timeout):
   nonlocal claimed
   if claimed or host!='api.tokenfactory.nebius.com':raise Refusal('EXACT_TRANSPORT_ONCE')
   claimed=True;connection.timeout=timeout;return connection
  boundary=runtime_service.nebius.HTTPBoundary(time.monotonic()+runtime_service.DEADLINE_SECONDS,runtime_service._MemoryCapture(),factory=take)
  return boundary,connection
 except BaseException:
  if connection is not None:
   try:connection.close()
   except Exception:pass
  raise

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
   import http.client
   _,prepared=transport_preflight96(http.client.HTTPSConnection)
   prepared.close() # Local-only parent check BEFORE even the E2E reservation.
   exclusive(self.directory/'e2e-reserved.json',{'state':'UNKNOWN_CONSUMED_NO_RETRY','request_sha256':NEW_REQUEST,'recorded_bytes_before_dispatch':self.sink.bytes,'recorded_chunks_before_dispatch':self.sink.next,'retry':False})
   return self.worker(raw,self.config,self.directory)

def run_worker(raw,config,directory):
 if Path(directory)!=scope.ROOT:raise Refusal('EXACT_NEW_WORKER_ROOT')
 command=[sys.executable,str(Path(__file__).parent/'render_recorded_release70.py'),'--credit-worker004',str(scope.ROOT)]
 environment={k:v for k,v in os.environ.items()if k in {'PATH','LANG','LC_ALL','NEBIUS_API_KEY','RENDER','RENDER_EXTERNAL_HOSTNAME','RENDER_GIT_COMMIT'}};environment['PYTHONDONTWRITEBYTECODE']='1'
 def limits():
  import resource
  resource.setrlimit(resource.RLIMIT_CPU,(10,10));resource.setrlimit(resource.RLIMIT_FSIZE,(1048576,1048576));resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
 proc=None
 try:
  import worker_scope004 as w
  w.assert_startup();initial=w.aggregate()
  if initial['current_bytes']>=w.PROFILE['aggregate_abort_bytes']:raise Refusal('NO_AI_AGGREGATE_HEADROOM')
  with w.serialized(scope.ROOT/'worker113'):
   exclusive(Path(directory)/'ai-worker-launch96.json',{'state':'UNKNOWN_CONSUMED_NO_RETRY','stage':'BEFORE_NATIVE_CHILD_START','request_attempted':'UNKNOWN','retry':False})
   proc=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=environment,preexec_fn=limits,start_new_session=True)
   proc.stdin.write(raw);proc.stdin.close()
   measured,out=w.collect(proc,{'wall':40})
   after=w.aggregate();measured.update(oom_kill_delta=after['oom_kill']-initial['oom_kill'],identity=w.identity(),retry=False)
   exclusive(Path(directory)/'ai-worker-receipt.json',measured)
  if measured['returncode']!=0 or measured['guard']or measured['oom_kill_delta']!=0 or len(out)>runtime_service.MAX_RESULT:raise Refusal('NEW_WORKER_OUTCOME_UNKNOWN')
  value=runtime_service.verify_runtime_result(json.loads(out));exclusive(Path(directory)/'e2e-result.json',value);return value
 except Exception:
  # Parent captures a safe terminal even when worker timed out or was killed.
  # No terminal is manufactured for a reservation that never existed.
  try:
   exclusive(Path(directory)/'ai-parent-diagnostic96.json',{'stage':'NATIVE_WORKER_FAILED','state':'UNKNOWN_CONSUMED_NO_RETRY','request_attempted':'UNKNOWN','retry':False})
   ledger=Slot004(scope.ORIGINAL/'allocation',config);q=read(ledger.path/'slot-004.json')
   if q['request_sha256']==NEW_REQUEST and not(ledger.path/'terminal-004.json').exists():ledger.terminal(q,False)
  except Exception:pass
  raise runtime_service.RuntimeRefusal('NEW_E2E_OUTCOME_UNKNOWN_NO_RETRY',consumed=True)from None
 finally:
  if proc is not None:
   try:
    if proc.poll()is None:w.stop(proc)
   except Exception:pass # Outer reservation remains UNKNOWN, never re-dispatched.
   for pipe in(proc.stdin,proc.stdout,proc.stderr):
    try:pipe.close()
    except Exception:pass

def worker(config,p):
 import recovery004
 m=recovery004.Recovery(scope.ROOT,scope.ORIGINAL,config,p)
 if not(m.root/'e2e-reserved.json').exists():raise Refusal('NATIVE_PARENT_RESERVATION_REQUIRED')
 raw=sys.stdin.buffer.read(runtime_service.MAX_REQUEST+1)
 if len(raw)>runtime_service.MAX_REQUEST:raise Refusal('REQUEST_BOUND')
 import http.client
 result=Session(m,factory=http.client.HTTPSConnection).dispatch(raw);sys.stdout.buffer.write(canonical(result));sys.stdout.buffer.flush()
