"""Private candidate only. Import performs no I/O; no default authority exists.
The old allocation and all old receipts are read-only, except the explicitly
admitted slot002/terminal002 append under the original allocation lock.
"""
import datetime,decimal,hashlib,hmac,json,math,os,re,shutil,threading
from pathlib import Path
from quota_ledger import read,exclusive,private_dir,Ledger
from release_policy import Refusal,digest,canonical
import worker_scope67 as w
ID='TRACEHARBOR-RECOVERY96'
ROOT=Path('/var/data/traceharbor-recovery96')
ORIGINAL=Path('/var/data/traceharbor-release68')
PRIOR=Path('/var/data/traceharbor-recovery86')
COOKIE='__Host-traceharbor-recovery96'
DEADLINE=1793379600

def contract():
 from render_recorded_release70 import credit_admission67
 return credit_admission67()

def assert_parent(m):
 import recovery86 as old
 if m.original!=ORIGINAL or m.root!=ROOT:raise Refusal('EXACT_SCOPE_ROOT')
 if old.witness(m.original)!=m.p['original_capture_sha256']:raise Refusal('ORIGINAL84_DRIFT')
 for rel,pin in m.p['parent_pins'].items():
  root=ORIGINAL if rel.startswith('original/')else PRIOR
  name=rel.split('/',1)[1];p=root/name;old.regular(p);b=p.read_bytes()
  if len(b)!=pin['bytes']or hashlib.sha256(b).hexdigest()!=pin['sha256']:raise Refusal('PARENT143_146_DRIFT')

def authority(m):
 import recovery_auth93
 return recovery_auth93.authority(m)

def legacy_authority67_closed(m):
 if (m.root/'standard-authority89.json').exists():
  import standard_billing89
  return standard_billing89.authority(m)
 assert_parent(m);a=read(m.root/'authority.json',65536)
 expected={'schema':'traceharbor.credit67.authority.v1','scope':ID,'accepted':True,'deploy_slot':3,'max_total_deploys':3,'new_AI_max':1,'reallocated_from_HELD':1,'allocation_id':m.config['allocation_id'],'total_call_limit':256,'session_max':1,'selector_max':1,'recording_sessions_max':1,'paid_continuation_disabled':True,'new_cash_USD':'0','credit_call_gross_cap_USD':'0.002','total_cash_cap_USD':'20','new_permissions_terms':False,'request_sha256':m.p['request_sha256']}
 for k,v in expected.items():
  if type(a.get(k))is not type(v)or a[k]!=v:raise Refusal('EXACT_NEW_OWNER_AUTHORITY_REQUIRED')
 if a.get('source_commit')!=w.identity()['source_commit']or not re.fullmatch('[a-f0-9]{40}',a.get('candidate_tree','')):raise Refusal('SOURCE_AUTHORITY_BINDING')
 for k in ('owner_receipt_sha256','independent_review_sha256','contract_sha256'):
  if not re.fullmatch('[a-f0-9]{64}',a.get(k,'')):raise Refusal('ACTUAL_RECEIPT_BINDING')
 if a['contract_sha256']!=digest(m.p):raise Refusal('CONTRACT_AUTHORITY_BINDING')
 if type(a.get('expires'))not in(int,float)or not math.isfinite(a['expires'])or not m.clock()<a['expires']<=DEADLINE:raise Refusal('AUTHORITY_EXPIRED')
 return a

TECHNICAL83_SCOPE='ONLY_TECHNICAL83_NO_GRANT_SESSION_TARGET_SELECTOR_MEDIA_AI'
OWNER83_SHA256='2d21697db1afa56a7611bd40d367223cda367290f546f8a37775f7dad1e7dd04'
OWNER83_PARENT_TREE='33476f59ae86cc6a9dc4cc8ef3ef80af15b9ea67'
OWNER83_PARENT_CONTRACT='16fbb84516bd009ce5a909af076c9395b8f595bfdacaeaa7f7c49c0110ae02b0'
TECHNICAL84_REVIEW='ACCEPT_EXACT_TECHNICAL84_CANDIDATE_FOR_OWNER83_ONLY'
def technical_authority(m):
 return authority(m)

def legacy_technical83_closed(m):
 if (m.root/'standard-authority89.json').exists():
  import standard_billing89
  return standard_billing89.authority(m)
 # This separate path never creates/promotes the full effect authority.json.
 assert_parent(m);path=m.root/'technical-authority83.json'
 if not path.exists():return authority(m) # Preserve separately approved full path.
 a=read(path,65536)
 expected={'schema':'traceharbor.technical84.authority.v1','scope':TECHNICAL83_SCOPE,'accepted':True,'deploy_slot':3,'max_total_deploys':3,'same_service':'srv-dbh6hgh42hec73c3g9m0','new_AI_max':0,'reallocated_from_HELD':0,'session_max':0,'grant_max':0,'target_max':0,'selector_max':0,'recording_sessions_max':0,'slot002_authorized':False,'paid_continuation_disabled':True,'new_cash_USD':'0','total_cash_cap_USD':'20','new_permissions_terms':False,'owner_receipt_sha256':OWNER83_SHA256,'approved_parent_tree':OWNER83_PARENT_TREE,'approved_parent_contract_sha256':OWNER83_PARENT_CONTRACT}
 for k,v in expected.items():
  if type(a.get(k))is not type(v)or a[k]!=v:raise Refusal('EXACT_NARROW_TECHNICAL83_AUTHORITY_REQUIRED')
 owner=a.get('owner_receipt')
 if not isinstance(owner,dict)or digest(owner)!=OWNER83_SHA256:raise Refusal('ACTUAL_OWNER83_RECEIPT_REQUIRED')
 review=a.get('independent_review84');ident=w.identity()
 if not isinstance(review,dict)or review.get('independent')is not True or review.get('verdict')!=TECHNICAL84_REVIEW or digest(review)!=a.get('independent_review84_sha256'):raise Refusal('ACTUAL_EXACT_TECHNICAL84_CODE_REVIEW_REQUIRED')
 from render_recorded_release70 import CREDIT67_SHA256
 for k in('candidate_tree','postimages_sha256','delta_sha256'):
  if review.get(k)!=a.get(k)or not re.fullmatch('[a-f0-9]{40}'if k=='candidate_tree'else'[a-f0-9]{64}',a.get(k,'')):raise Refusal('TECHNICAL84_REVIEW_BINDING')
 if review.get('contract_sha256')!=CREDIT67_SHA256 or a.get('source_contract_sha256')!=CREDIT67_SHA256 or a.get('contract_sha256')!=digest(m.p)or a.get('source_commit')!=ident['source_commit']:raise Refusal('TECHNICAL84_SOURCE_CONTRACT_BINDING')
 if type(a.get('expires'))not in(int,float)or not math.isfinite(a['expires'])or not m.clock()<a['expires']<=DEADLINE:raise Refusal('TECHNICAL83_AUTHORITY_EXPIRED')
 return a

def ledger(m,*,unspent=False):
 authority(m);v=Ledger(ORIGINAL/'allocation',m.config);s=v.snapshot()
 if s['reserved_calls']not in((2,)if unspent else(2,3)):raise Refusal('EXACT_SHARED_ALLOCATION96_STATE')
 if s['reserved_calls']==3:
  q=read(v.path/'slot-003.json')
  if q['request_sha256']!=m.p['request_sha256']or not(m.root/'e2e-reserved.json').exists():raise Refusal('FOREIGN_SLOT003')
 return v

def idle(m):
 ledger(m,unspent=True)
 if any((m.root/n).exists()for n in ('select/started.json','select/failure.json','native/reserved.json','full/reserved.json','e2e-reserved.json','demo-execution-reserved.json','av/render-reserved.json')):raise Refusal('NEW_SCOPE_ALREADY_CONSUMED')

def credit(m,max_age=600):
 authority(m);p=m.root/'credit-observations';files=list(p.glob('*.json'))if p.exists()else[]
 if not 1<=len(files)<=3:raise Refusal('CONFIRMED_CREDIT_ONLY_EVIDENCE_REQUIRED')
 values=[read(f,65536)for f in files]
 try:v=max(values,key=lambda x:x['observed_at_utc'])
 except Exception:raise Refusal('CREDIT_SHAPE')
 if any(x['observed_at_utc']==v['observed_at_utc']and x!=v for x in values):raise Refusal('CONFLICTING_CREDIT_EVIDENCE')
 return _validate_credit_value(m,v,max_age)

def _validate_credit_value(m,v,max_age):
 if (m.root/'standard-authority89.json').exists():
  import standard_billing89
  return standard_billing89.validate_observation(m,v,max_age)
 authority(m)
 expected={'schema':'traceharbor.confirmed-credit67.v1','scope':ID,'tenant':'aitenant-e00rrxfyw57s74dbqq','project':'aiproject-e00d73xwjm884tnvcs','provider_confirmed_credit_only':True,'credential_project_binding_confirmed':True,'paid_continuation_disabled':True,'new_money_card_terms_permissions':False,'pricing_confirmed':True,'input_nanodollars_per_token':60,'output_nanodollars_per_token':240,'no_inference':True,'identity':w.identity()}
 for k,z in expected.items():
  if type(v.get(k))is not type(z)or v[k]!=z:raise Refusal('CONFIRMED_CREDIT_ONLY_EVIDENCE_REQUIRED')
 if v.get('billing_status')not in('Active','Suspended'):raise Refusal('REAL_BILLING_LABEL')
 for k in ('provider_confirmation_message_id','protection_message_id'):
  if not re.fullmatch('[a-f0-9]{16}',v.get(k,'')):raise Refusal('REAL_PROVIDER_CONFIRMATION_REQUIRED')
 if v['provider_confirmation_message_id']=='1a1848995f22f435':raise Refusal('OLD_PAID_USAGE_ADVICE_NOT_CREDIT_CONFIRMATION')
 if not re.fullmatch('[a-f0-9]{64}',v.get('provider_confirmation_body_sha256','')):raise Refusal('REAL_PROVIDER_BODY_BINDING')
 try:
  if type(v['balance_USD'])is not str or type(v['tax_multiplier'])is not str:raise ValueError()
  t=datetime.datetime.fromisoformat(v['observed_at_utc'].replace('Z','+00:00'))
  if t.tzinfo is None or not 0<=m.clock()-t.timestamp()<=max_age:raise ValueError()
  balance=decimal.Decimal(v['balance_USD']);tax=decimal.Decimal(v['tax_multiplier']);bound=decimal.Decimal('0.002')
  cost=m.p['certificate']['count']*60+1500*240
  gross=decimal.Decimal(cost)/1000000000*tax
  if not balance.is_finite()or not tax.is_finite()or not 1<=tax<=2 or not gross<=bound<=balance:raise ValueError()
 except Exception:raise Refusal('FRESH_PRICE_TAX_CREDIT_BOUND')
 return v

def observe_credit(m,v):
 idle(m);base=m.root/'credit-observations';private_dir(base)
 if len(list(base.glob('*.json')))>=1:raise Refusal('OBSERVATION_BUDGET')
 # Validate in memory before O_EXCL publication, using the same validator.
 validate_observation(m,v)
 exclusive(base/(digest(v)+'.json'),v);return {'state':'STANDARD_PAID_OBSERVATION_RETAINED_NOT_INFERENCE_PROOF'if(m.root/'standard-authority89.json').exists()else'CONFIRMED_CREDIT_OBSERVATION_RETAINED_NOT_INFERENCE_PROOF','sha256':digest(v)}

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
 for n in ('operator67','select','native','full','exports','av','worker113','credit-observations'):(m.root/n).mkdir(mode=0o700)
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
  if codec_name!='vp8'or m.operator.remaining()<400 or not(m.root/'target.json').exists():raise Refusal('NOT_READY')
  t=datetime.datetime.fromisoformat(v['observed_at_utc'].replace('Z','+00:00')).timestamp();ms=int(min(300-(m.clock()-t),m.operator.remaining()-400)*1000)
  if ms<=0:raise Refusal('READINESS_EXPIRED')
  key=os.urandom(32).hex();value={'scope':ID,'state':'PREPARED_OWNER_GESTURE_ONLY','key_sha256':hashlib.sha256(key.encode()).hexdigest(),'expires':m.clock()+ms/1000,'identity':w.identity(),'target_sha256':digest(read(m.root/'target.json')),'retry':False};exclusive(m.root/'select/reserved.json',value)
  return {'state':value['state'],'key':key,'lease_ms':ms,'codec':'vp8','picker_seconds':120,'identity':w.identity(),'retry':False}

def start_selection(m,key):
 with m.lock:
  idle(m);credit(m,300);v=read(m.root/'select/reserved.json')
  if not isinstance(key,str)or len(key)!=64 or not hmac.compare_digest(hashlib.sha256(key.encode()).hexdigest(),v['key_sha256'])or m.clock()>=v['expires']or v['identity']!=w.identity()or v['target_sha256']!=digest(read(m.root/'target.json'))or m.operator.remaining()<400:raise Refusal('CAPABILITY_EXPIRED_OR_DRIFT')
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
 import recovery86 as old,credit_runtime67 as runtime
 with m.lock:
  authority(m);ledger(m,unspent=True);codec(m);credit(m,600 if phase=='native'else 480);media_gate(m)
  if phase not in ('native','full')or codec_name!='vp8':raise Refusal('NO_SYNTHETIC_OR_DIRECT_SELECTION')
  if phase=='full'and(m.state('native').get('state')!='PASS'or not(m.root/'preview-ready.json').exists()or m.operator.remaining()<250):raise Refusal('NATIVE_PREVIEW_OR_SESSION_GATE')
  seconds=2 if phase=='native'else 224;limit=m.p['diagnostic_bytes']if phase=='native'else m.p['full_bytes']
  exclusive(m.root/phase/'reserved.json',{'scope':ID,'phase':phase,'codec':codec_name,'seconds':seconds,'at':m.clock(),'state':'RESERVED_UNKNOWN_NO_RETRY','retry':False});m.sinks[phase]=old.Sink(m.root/phase,phase,limit,m.clock)
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
 if (m.root/'standard-authority89.json').exists():
  import standard_billing89
  return standard_billing89.status(m)
 try:v=credit(m,300);admitted=True;label=v['billing_status']
 except Exception:admitted=False;label='UNKNOWN'
 return {'schema':'traceharbor.runtime-status.v1','enabled':m.ready(),'new_call_cap':1 if m.ready()else 0,'reason':'ONE_FROM254HELD_OTHER253HELD','phases':{n:m.state(n)for n in('select','native','full')},'armed':(m.root/'target.json').exists(),'armed_id':read(m.root/'target.json')['client_id']if(m.root/'target.json').exists()else None,'target_epoch':'67','full_elapsed':m.clock()-m.sinks['full'].started if'full'in m.sinks else None,'session_remaining':int(m.operator.remaining()),'e2e_reserved':(m.root/'e2e-reserved.json').exists(),'e2e_result':(m.root/'e2e-result.json').exists(),'retained_clip_qualification':{'state':'PASS_PRIOR_NATIVE146_LINEAGE','clip_bytes':71412,'new_native_sample_still_required':True},'provider_readiness':{'state':'CREDIT_ONLY_ATTEMPT_ADMITTED'if admitted else'NOT_ADMITTED','admitted_attempt':admitted,'billing_status':label,'paid_continuation_disabled':True},'retry':False}
