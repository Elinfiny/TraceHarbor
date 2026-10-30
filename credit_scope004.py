"""Private candidate only. Import performs no I/O; no default authority exists.
The old allocation and all old receipts are read-only, except the explicitly
admitted slot002/terminal002 append under the original allocation lock.
"""
import datetime,decimal,hashlib,hmac,json,math,os,re,shutil,threading
from pathlib import Path
from quota_ledger import read,exclusive,private_dir,Ledger
from release_policy import Refusal,digest,canonical
import worker_scope004 as w
ID='TRACEHARBOR-RECOVERY004'
ROOT=Path('/var/data/traceharbor-recovery004')
ORIGINAL=Path('/var/data/traceharbor-release68')
PRIOR=Path('/var/data/traceharbor-recovery86')
COOKIE='__Host-traceharbor-recovery004'
DEADLINE=1793379600

def contract():
 from render_recorded_release70 import credit_admission004
 return credit_admission004()

def assert_parent(m):
 import source_extension004 as guard
 if m.root!=ROOT or m.original!=ORIGINAL or m.p['root']!=str(ROOT) or m.config!=m.p['release_config']:raise Refusal('EXACT004_ROOT_CONFIG')
 guard.check_critical(m.p['critical_preimages'])


def authority(m):
 from recovery_auth004 import authority as actual
 return actual(m)



TECHNICAL83_SCOPE='ONLY_TECHNICAL83_NO_GRANT_SESSION_TARGET_SELECTOR_MEDIA_AI'
OWNER83_SHA256='2d21697db1afa56a7611bd40d367223cda367290f546f8a37775f7dad1e7dd04'
OWNER83_PARENT_TREE='33476f59ae86cc6a9dc4cc8ef3ef80af15b9ea67'
OWNER83_PARENT_CONTRACT='16fbb84516bd009ce5a909af076c9395b8f595bfdacaeaa7f7c49c0110ae02b0'
TECHNICAL84_REVIEW='ACCEPT_EXACT_TECHNICAL84_CANDIDATE_FOR_OWNER83_ONLY'
def technical_authority(m):return authority(m)



def ledger(m,*,unspent=False):
 authority(m);v=Ledger(ORIGINAL/'allocation',m.config);s=v.snapshot()
 if s['reserved_calls']not in((3,)if unspent else(3,4)):raise Refusal('EXACT_SHARED_ALLOCATION004_STATE')
 if s['reserved_calls']==4:
  q=read(v.path/'slot-004.json')
  if q['request_sha256']!=m.p['request_sha256']or not(m.root/'e2e-reserved.json').exists():raise Refusal('FOREIGN_SLOT004')
 return v


def idle(m):
 ledger(m,unspent=True)
 if any((m.root/n).exists()for n in ('select/started.json','select/failure.json','native/reserved.json','full/reserved.json','e2e-reserved.json','demo-execution-reserved.json','av/render-reserved.json')):raise Refusal('NEW_SCOPE_ALREADY_CONSUMED')

def credit(m,max_age=600):
 authority(m);files=list((m.root/'credit-observations').glob('*.json'))
 if len(files)!=1:raise Refusal('EXACT_ONE_NEW_OBSERVATION004')
 import standard_billing004
 return standard_billing004.validate_observation(m,read(files[0],65536),max_age)


def _validate_credit_value(m,v,max_age):
 import standard_billing004
 return standard_billing004.validate_observation(m,v,max_age)


def observe_credit(m,v):
 import recovery_auth004
 return recovery_auth004.append_observation(m,v)


def validate_observation(m,v):
 return _validate_credit_value(m,v,120)

def initialize(m):
 technical_authority(m)
 manifest={'scope':ID,'contract_sha256':digest(m.p),'config_sha256':digest(m.config),'retry':False}
 if(m.root/'setup-complete.json').exists():
  if read(m.root/'manifest.json')!=manifest:raise Refusal('NEW_SCOPE_SETUP_DRIFT')
  return
 if(m.root/'setup-reserved.json').exists():raise Refusal('PARTIAL_SETUP_NO_RETRY')
 if shutil.disk_usage(m.root.parent).free<m.p['reserve_free_bytes']:raise Refusal('DISK_RESERVE')
 exclusive(m.root/'setup-reserved.json',{'scope':ID,'state':'UNKNOWN_NO_RETRY'})
 for n in ('select','native','full','exports','av','worker113','credit-observations'):(m.root/n).mkdir(mode=0o700)
 exclusive(m.root/'manifest.json',manifest);exclusive(m.root/'setup-complete.json',{'manifest_sha256':digest(manifest)})

def codec(m):
 authority(m);w.assert_startup();q=read(PRIOR/'native/qualified.json',65536)
 if q.get('state')!='PASS'or q.get('sha256')!=m.p['prior_native_sha256']or q.get('probe',{}).get('worker',{}).get('identity',{}).get('source_commit')!='b536fec226be6eb6584584b3039e8f157a2239e9':raise Refusal('PRIOR_NATIVE146_LINEAGE')
 if w.binary_fingerprints()!=m.p['binary_fingerprints']:raise Refusal('BINARY_LINEAGE_DRIFT')
 return 'vp8'

def grant(m):
 raise Refusal('CONSUMED_OPERATOR67_GRANT_CLOSED')

def arm(m,client_id):
 with m.lock:
  idle(m);codec(m);credit(m,300)
  if not isinstance(client_id,str)or not re.fullmatch('[a-f0-9]{32}',client_id):raise Refusal('TARGET_ID')
  exclusive(m.root/'target.json',{'scope':ID,'client_id':client_id,'request_sha256':m.p['request_sha256'],'at':m.clock()});return {'armed':True}

def prepare_selection(m,codec_name):
 with m.lock:
  idle(m);codec(m);v=credit(m,120)
  if codec_name!='vp8'or m.operator.remaining()<1320 or not(m.root/'target.json').exists():raise Refusal('NOT_READY')
  t=datetime.datetime.fromisoformat(v['observed_at_utc'].replace('Z','+00:00')).timestamp();ms=int(min(300-(m.clock()-t),m.operator.remaining()-1320)*1000)
  if ms<=0:raise Refusal('READINESS_EXPIRED')
  key=os.urandom(32).hex();value={'scope':ID,'state':'PREPARED_OWNER_GESTURE_ONLY','key_sha256':hashlib.sha256(key.encode()).hexdigest(),'expires':m.clock()+ms/1000,'identity':w.identity(),'target_sha256':digest(read(m.root/'target.json')),'retry':False};exclusive(m.root/'select/reserved.json',value)
  return {'state':value['state'],'key':key,'lease_ms':ms,'codec':'vp8','picker_seconds':120,'identity':w.identity(),'retry':False}

def start_selection(m,key):
 with m.lock:
  idle(m);credit(m,300);v=read(m.root/'select/reserved.json')
  if not isinstance(key,str)or len(key)!=64 or not hmac.compare_digest(hashlib.sha256(key.encode()).hexdigest(),v['key_sha256'])or m.clock()>=v['expires']or v['identity']!=w.identity()or v['target_sha256']!=digest(read(m.root/'target.json'))or m.operator.remaining()<1320:raise Refusal('CAPABILITY_EXPIRED_OR_DRIFT')
  exclusive(m.root/'select/started.json',{'state':'NATIVE_PERMISSION_PENDING','at':m.clock(),'identity':w.identity(),'retry':False})
  timer=m.selection_timer_factory146(120,lambda:fail_selection(m,'TimeoutError','TIMEOUT'));m.selection_timer146=timer;timer.daemon=True;timer.start();return {'state':'NATIVE_PERMISSION_PENDING','seconds':120,'retry':False}

def fail_selection(m,name,where):
 import recovery86 as old
 with m.lock:
  p=m.root/'select';authority(m)
  if not(p/'reserved.json').exists():raise Refusal('UNRESERVED_FAILURE')
  for n in ('failure.json','terminal.json'):
   if(p/n).exists():return read(p/n)
  v={'state':'FAILED_NO_RETRY','phase':'select','error_name':name if name in old.NAMES else'UnclassifiedError','where':where if where in {'SELECT','TIMEOUT','FLOW','TRACK_ENDED'}else'FLOW','retry':False};exclusive(p/'failure.json',v);exclusive(p/'terminal.json',v)
  if m.selection_timer146:m.selection_timer146.cancel()
  return v

def media_gate(m):
 authority(m);d=m.root/'select';v=read(d/'started.json')
 if(d/'failure.json').exists()or v['identity']!=w.identity()or not 0<=m.clock()-v['at']<=120:raise Refusal('SELECTION_EXPIRED_OR_FAILED')

def reserve(m,phase,codec_name):
 import recovery86 as old,credit_runtime004 as runtime
 with m.lock:
  authority(m);ledger(m,unspent=True);codec(m);credit(m,600 if phase=='native'else 480);media_gate(m)
  if phase not in ('native','full')or codec_name!='vp8':raise Refusal('NO_SYNTHETIC_OR_DIRECT_SELECTION')
  if phase=='full'and(m.state('native').get('state')!='PASS'or not(m.root/'preview-ready.json').exists()or m.operator.remaining()<1150):raise Refusal('NATIVE_PREVIEW_OR_SESSION_GATE')
  seconds=2 if phase=='native'else 224;limit=m.p['diagnostic_bytes']if phase=='native'else m.p['full_bytes']
  exclusive(m.root/phase/'reserved.json',{'scope':ID,'phase':phase,'codec':codec_name,'seconds':seconds,'at':m.clock(),'state':'RESERVED_UNKNOWN_NO_RETRY','retry':False});m.sinks[phase]=__import__('recovery004').Sink(m.root/phase,phase,limit,m.clock)
  if phase=='native':
   if m.selection_timer146:m.selection_timer146.cancel()
   exclusive(m.root/'select/terminal.json',{'state':'STREAM_ACCEPTED_NATIVE_NOT_QUALIFIED','phase':'select','at':m.clock(),'retry':False})
  else:m.call=runtime.CapturedOnceSession(m.config,m.root,m.sinks['full'],gate=lambda:credit(m,600))
  return {'reserved':True,'phase':phase,'seconds':seconds,'byte_limit':limit,'retry':False}

def selection_status(m):
 for n in ('failure.json','terminal.json','started.json'):
  if(m.root/'select'/n).exists():return read(m.root/'select'/n)
 return {'state':'PREPARED_OWNER_GESTURE_ONLY'if(m.root/'select/reserved.json').exists()else'NOT_STARTED','retry':False}

def begin(m,client_id):
 if not m.ready()or read(m.root/'target.json')['client_id']!=client_id:raise Refusal('FULL_ACK_TARGET_REQUIRED')
 credit(m,600);exclusive(m.root/'demo-execution-reserved.json',{'at':m.clock(),'client_id':client_id,'state':'UNKNOWN_NO_RETRY'});return {'begun':True}

def status(m):
 import standard_billing004
 return standard_billing004.status(m)

