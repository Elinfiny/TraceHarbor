"""NEW qualification of existing immutable media. No synthetic media or replay.
No process/file effect on import. Only Native Owner tooling invokes qualification.
"""
import hashlib,os,datetime,decimal,math
from pathlib import Path
import worker_scope113 as w
CLIP_SHA256='7a906668f0672a5506061fc7ac6687f7ebc3fb6bd92027028c9155ce7bb9e9f4'
CLIP_BYTES=43637
AUTHORITY='TRACEHARBOR-CAPTURE146-DISTINCT-AFTER-CLOSED143'
EPOCH='capture146'
PRIOR113_SHA256='4a7e7e62198c295b3b966f2371af8f46e58e383e2261033b6016393ba1e48517'
PROJECT_SHA256='5188e366a37791c300886650b34c4bd236c6246595821aefb851d06aed926a1c'
ORIGINAL_ALLOCATION='c35a1da9af93bef941fd69a43a83859d'
SCOPE57='TRACEHARBOR-CAPTURE146-DISTINCT-AFTER-CLOSED143'
PROTECTION_IDS=['1a0ed4578628d579','1a12f574972969c4','1a149ba922414010']
ACCOUNT_SHA256='c243e6ed766c1a6fd2f5c2b70851cc23cbf7c97b0b0681f1d705e501465f7697'

def parent(m):
 import recovery86 as r
 m.assert_original();d=m.root/'codec106/vp8';p=d/'media.webm';r.regular(p)
 q=r.read(d/'qualified.json');terminal=r.read(d/'terminal.json');reserved=r.read(d/'reserved.json')
 if p.stat().st_size!=CLIP_BYTES or w.sha(p)!=CLIP_SHA256 or q.get('state')!='FAIL_NO_RETRY'or q.get('probe',{}).get('error')!='PROBE_UNKNOWN'or q.get('sha256')!=CLIP_SHA256 or q.get('bytes')!=CLIP_BYTES or terminal.get('state')!='ENCODED_NOT_QUALIFIED'or terminal.get('bytes')!=CLIP_BYTES or reserved.get('id')!='RECOVERY106-CODEC-VP8-ONCE':raise r.Refusal('EXACT_RETAINED_PARENT_REQUIRED')
 return {'clip_sha256':CLIP_SHA256,'clip_bytes':CLIP_BYTES,'old_qualification_sha256':r.digest(q),'old_terminal_sha256':r.digest(terminal),'old_reservation_sha256':r.digest(reserved),'original84_sha256':m.p['original_capture_sha256']}

def unstarted(m):
 import capture_recovery146 as c
 return c.idle(m)

def prior_qualification(m):
 import recovery86 as r
 q=r.read(m.root/'retained113/qualified.json')
 if r.digest(q)!=PRIOR113_SHA256 or q.get('state')!='PASS_RETAINED_CLIP113'or q.get('identity',{}).get('source_commit')!='8dee06bf428c6d412607ee7b1e8da807521ea3ac'or q.get('worker_profile_sha256')!=w.PROFILE_SHA256:raise r.Refusal('EXACT_PRIOR113_CERTIFICATE_REQUIRED')
 return r.digest(q)

def prepare(m):
 import recovery86 as r
 binding=parent(m);prior=prior_qualification(m);import capture_recovery146 as c;c.require_authority(m);closed=c.old143(m);epoch=m.root/EPOCH;manifest={'schema':'traceharbor.capture146.scope.v1','id':AUTHORITY,'parent':binding,'worker_profile_sha256':w.PROFILE_SHA256,'prior113_qualification_sha256':prior,'scope57':SCOPE57,'closed143':closed,'new_qualification_cap':1,'new_session_cap':1,'new_synthetic_recorders':0,'new_AI_quota':0,'retry':False}
 if epoch.exists():
  r.private_dir(epoch)
  if not(epoch/'setup-complete.json').exists()or r.read(epoch/'manifest.json')!=manifest:raise r.Refusal('RETAINED113_PARTIAL_OR_DRIFT')
 else:
  unstarted(m);epoch.mkdir(mode=0o700);r.exclusive(epoch/'setup-reserved.json',{'id':AUTHORITY,'state':'UNKNOWN_NO_RETRY'});r.exclusive(epoch/'manifest.json',manifest);r.exclusive(epoch/'setup-complete.json',{'manifest_sha256':r.digest(manifest)})
 for name in('operator146','worker113'):(m.root/name).mkdir(mode=0o700,exist_ok=True);r.private_dir(m.root/name)
 (m.root/EPOCH/'select').mkdir(mode=0o700,exist_ok=True);r.private_dir(m.root/EPOCH/'select')

def qualify_once(m):
 import recovery86 as r
 prepare(m);unstarted(m);w.assert_startup();before=parent(m);epoch=m.root/EPOCH
 r.exclusive(epoch/'qualification-reserved.json',{'id':AUTHORITY+'-CLIP-QUALIFY-ONCE','state':'UNKNOWN_NO_RETRY','parent':before,'identity':w.identity(),'retry':False})
 probe=m.probe(m.root/'codec106/vp8/media.webm','vp8',m.p,receipt=epoch/'worker-probe')
 after=parent(m);ok=before==after and probe.get('pass')is True
 result={'schema':'traceharbor.capture146.qualification.v1','id':AUTHORITY+'-CLIP-QUALIFY-ONCE','state':'PASS_RETAINED_CLIP146'if ok else'FAIL_RETAINED146_NO_RETRY','parent':before,'identity':w.identity(),'worker_profile_sha256':w.PROFILE_SHA256,'probe':probe,'old_FAIL_preserved':True,'new_recorders':0,'retry':False}
 r.exclusive(epoch/'qualified.json',result);return result

def codec(m):
 import recovery86 as r
 __import__('capture_recovery146').require_authority(m);p=m.root/EPOCH/'qualified.json';q=r.read(p);worker=r.read(m.root/EPOCH/'worker-probe/result.json');w.assert_startup()
 if q.get('schema')!='traceharbor.capture146.qualification.v1'or q.get('id')!=AUTHORITY+'-CLIP-QUALIFY-ONCE'or q.get('state')!='PASS_RETAINED_CLIP146'or q.get('parent')!=parent(m)or q.get('identity')!=w.identity()or q.get('worker_profile_sha256')!=w.PROFILE_SHA256 or q.get('probe',{}).get('pass')is not True or worker.get('pass')is not True or worker.get('identity')!=w.identity()or worker.get('guard')is not None:raise r.Refusal('NEW_RETAINED_CERTIFICATE_REQUIRED')
 return 'vp8'

def summary(m):
 import recovery86 as r
 d=m.root/EPOCH;p=d/'qualified.json'
 if not p.exists():return {'state':'UNKNOWN_CONSUMED_NO_RETRY'if(d/'qualification-reserved.json').exists()else'NOT_STARTED','clip_bytes':CLIP_BYTES,'old_qualification':'FAIL_NO_RETRY','new_recorders':0,'retry':False}
 q=r.read(p)
 try:codec(m);state='PASS_RETAINED_CLIP146'
 except Exception:state=q['state']if q.get('state')=='FAIL_RETAINED146_NO_RETRY'else'INELIGIBLE_CERTIFICATE_OR_PROFILE_DRIFT'
 return {'state':state,'codec':'vp8','clip_bytes':CLIP_BYTES,'clip_sha256':CLIP_SHA256,'old_qualification':'FAIL_NO_RETRY','worker_profile_sha256':w.PROFILE_SHA256,'new_recorders':0,'retry':False}

def grant_once(m):
 import recovery86 as r
 prepare(m);unstarted(m);codec(m);provider_active(m,max_age=120)
 old=m.root/'operator113/session.json'
 if old.exists()and r.read(old)['expires']>m.clock():raise r.Refusal('OLD113_SESSION_NOT_EXPIRED')
 for name,key in [('voice.wav','voice_sha256'),('edl.json','edl_member_sha256'),('captions.srt','captions_member_sha256')]:
  asset=m.root/'assets'/name;r.regular(asset)
  if w.sha(asset)!=m.p[key]:raise r.Refusal('ORIGINAL_ASSET_PIN')
 raw=os.urandom(32).hex();r.exclusive(m.root/'operator146/grant.json',{'sha256':hashlib.sha256(raw.encode()).hexdigest(),'scope':'RECOVERY86_ONLY','authority_id':AUTHORITY,'worker_profile_sha256':w.PROFILE_SHA256,'source_commit':w.identity()['source_commit'],'expires':min(m.clock()+m.p['session_seconds'],__import__('capture_recovery146').require_authority(m)['expires'])});return raw

def original_authority(m):
 import recovery86 as r,capture_recovery146 as c
 c.require_authority(m)
 r.r.release_policy.validate_config(m.config)
 r.r.release_policy.deadline(m.config,datetime.datetime.fromtimestamp(m.clock(),datetime.timezone.utc))
 if m.config['allocation_id']!=ORIGINAL_ALLOCATION or m.p.get('AI_calls')!=1 or m.p.get('other_255_held')is not True:raise r.Refusal('ORIGINAL_ONE_ATTEMPT_AUTHORITY_REQUIRED')
 m.assert_original();ledger=r.Ledger(m.original/'allocation',m.config).snapshot()
 if ledger.get('reserved_calls')!=0 or ledger.get('remaining_calls')!=256 or (m.original/'e2e-reserved.json').exists():raise r.Refusal('ORIGINAL_ONE_ATTEMPT_NOT_UNCONSUMED')
 return ledger

def provider_value(m,v,max_age,require_active=True):
 """require_active retains the old call signature only; means credit admission.
 Billing label is evidence, never rewritten to Active or used as a veto.
 """
 import recovery86 as r
 keys={'schema','billing_status','balance_USD','credit_floor_USD','observed_at_utc','account_sha256','project_sha256','paid_continuation_disabled','protection_message_ids','authority_id','no_inference'}
 if set(v)!=keys or v['schema']!='traceharbor.native-credit-only146.v1'or v['billing_status']not in('Active','Suspended')or v['account_sha256']!=ACCOUNT_SHA256 or v['project_sha256']!=PROJECT_SHA256 or v['no_inference']is not True or type(v['balance_USD'])is not str or type(v['credit_floor_USD'])is not str:raise r.Refusal('EXACT_CREDIT_ONLY_OBSERVATION_REQUIRED')
 if type(v['paid_continuation_disabled'])is not bool or type(v['protection_message_ids'])is not list or type(v['authority_id'])is not str:raise r.Refusal('CREDIT_PROTECTION_EVIDENCE_SHAPE')
 if require_active and (v['paid_continuation_disabled']is not True or v['protection_message_ids']!=PROTECTION_IDS or v['authority_id']!=SCOPE57):raise r.Refusal('NO_PAID_CONTINUATION_PROTECTION_AND_AUTHORITY_REQUIRED')
 observed=datetime.datetime.fromisoformat(v['observed_at_utc'].replace('Z','+00:00'))
 if observed.tzinfo is None or not 0<=m.clock()-observed.timestamp()<=max_age:raise r.Refusal('CREDIT_OBSERVATION_NOT_FRESH')
 try:balance=decimal.Decimal(v['balance_USD']);credit=decimal.Decimal(v['credit_floor_USD'])
 except decimal.InvalidOperation:raise r.Refusal('CREDIT_BALANCE_INVALID')
 if not balance.is_finite()or not credit.is_finite():raise r.Refusal('CREDIT_BALANCE_INVALID')
 if require_active:
  if credit<decimal.Decimal('1.00')or balance<credit:raise r.Refusal('CREDIT_INSUFFICIENT_OR_NOT_VERIFIED')
  original_authority(m)
 return v

def record_provider_observation(m,v):
 """Native Owner only: actual credit+identity observation and read protection.
 No paid-setting write, inference probe, provider entitlement assertion or polling.
 """
 import recovery86 as r
 prepare(m);unstarted(m);provider_value(m,v,120,require_active=False);base=m.root/EPOCH/'provider-observations';base.mkdir(mode=0o700,exist_ok=True);r.private_dir(base)
 if len(list(base.glob('*.json')))>=3:raise r.Refusal('PROVIDER_OBSERVATION_BUDGET')
 value={'observation':v,'identity':w.identity()};r.exclusive(base/(r.digest(value)+'.json'),value);return {'state':'CREDIT_ONLY_OBSERVATION_RECORDED_NOT_INFERENCE_PROOF','sha256':r.digest(value),'billing_status':v['billing_status']}

def provider_active(m,max_age=600):
 """Compatibility name: admit only the ORIGINAL credit-backed attempt."""
 import recovery86 as r
 base=m.root/EPOCH/'provider-observations';files=list(base.glob('*.json'))if base.exists()else[]
 if not 1<=len(files)<=3:raise r.Refusal('NATIVE_CREDIT_OBSERVATION_REQUIRED')
 values=[]
 for p in files:
  value=r.read(p)
  if value.get('identity')!=w.identity():raise r.Refusal('CREDIT_OBSERVATION_IDENTITY_DRIFT')
  values.append(value['observation'])
 # Latest observation governs; an invalid/negative newer receipt cannot fall back.
 try:latest=max(values,key=lambda v:datetime.datetime.fromisoformat(v['observed_at_utc'].replace('Z','+00:00')).timestamp())
 except Exception:raise r.Refusal('CREDIT_OBSERVATION_TIMESTAMP')
 # A same-time conflicting receipt fails closed, independent of directory order.
 if any(v['observed_at_utc']==latest['observed_at_utc']and v!=latest for v in values):raise r.Refusal('CONFLICTING_CREDIT_OBSERVATIONS')
 return provider_value(m,latest,max_age)

def provider_summary(m):
 try:
  v=provider_active(m,max_age=300)
  return {'state':'CREDIT_ONLY_ATTEMPT_ADMITTED','admitted_attempt':True,'billing_status':v['billing_status'],'paid_continuation_disabled':True,'purpose':'ORIGINAL_RECORDED_ATTEMPT_ONLY','proof':'FRESH_CREDIT_IDENTITY_PROTECTION_AND_ORIGINAL_QUOTA; NOT_INFERENCE_SUCCESS'}
 except Exception:return {'state':'NOT_ADMITTED','admitted_attempt':False,'purpose':'ORIGINAL_RECORDED_ATTEMPT_ONLY','proof':'CREDIT_OR_PROTECTION_IDENTITY_AUTHORITY_QUOTA_FRESHNESS_GATE'}
