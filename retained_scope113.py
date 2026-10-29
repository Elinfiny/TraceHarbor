"""NEW qualification of existing immutable media. No synthetic media or replay.
No process/file effect on import. Only Native Owner tooling invokes qualification.
"""
import hashlib,os,datetime,decimal,math
from pathlib import Path
import worker_scope113 as w
CLIP_SHA256='7a906668f0672a5506061fc7ac6687f7ebc3fb6bd92027028c9155ce7bb9e9f4'
CLIP_BYTES=43637
AUTHORITY='TRACEHARBOR-RETAINED113'
ACCOUNT_SHA256='c243e6ed766c1a6fd2f5c2b70851cc23cbf7c97b0b0681f1d705e501465f7697'

def parent(m):
 import recovery86 as r
 m.assert_original();d=m.root/'codec106/vp8';p=d/'media.webm';r.regular(p)
 q=r.read(d/'qualified.json');terminal=r.read(d/'terminal.json');reserved=r.read(d/'reserved.json')
 if p.stat().st_size!=CLIP_BYTES or w.sha(p)!=CLIP_SHA256 or q.get('state')!='FAIL_NO_RETRY'or q.get('probe',{}).get('error')!='PROBE_UNKNOWN'or q.get('sha256')!=CLIP_SHA256 or q.get('bytes')!=CLIP_BYTES or terminal.get('state')!='ENCODED_NOT_QUALIFIED'or terminal.get('bytes')!=CLIP_BYTES or reserved.get('id')!='RECOVERY106-CODEC-VP8-ONCE':raise r.Refusal('EXACT_RETAINED_PARENT_REQUIRED')
 return {'clip_sha256':CLIP_SHA256,'clip_bytes':CLIP_BYTES,'old_qualification_sha256':r.digest(q),'old_terminal_sha256':r.digest(terminal),'old_reservation_sha256':r.digest(reserved),'original84_sha256':m.p['original_capture_sha256']}

def unstarted(m):
 import recovery86 as r
 if any((m.root/n/'reserved.json').exists()for n in('select','native','full'))or(m.original/'e2e-reserved.json').exists()or r.Ledger(m.original/'allocation',m.config).snapshot()['reserved_calls']!=0:raise r.Refusal('ORIGINAL_REMAINING_EFFECT_NOT_UNSTARTED')

def prepare(m):
 import recovery86 as r
 binding=parent(m);epoch=m.root/'retained113';manifest={'schema':'traceharbor.retained113.scope.v1','id':AUTHORITY,'parent':binding,'worker_profile_sha256':w.PROFILE_SHA256,'new_qualification_cap':1,'new_session_cap':1,'new_synthetic_recorders':0,'new_AI_quota':0,'retry':False}
 if epoch.exists():
  r.private_dir(epoch)
  if not(epoch/'setup-complete.json').exists()or r.read(epoch/'manifest.json')!=manifest:raise r.Refusal('RETAINED113_PARTIAL_OR_DRIFT')
 else:
  unstarted(m);epoch.mkdir(mode=0o700);r.exclusive(epoch/'setup-reserved.json',{'id':AUTHORITY,'state':'UNKNOWN_NO_RETRY'});r.exclusive(epoch/'manifest.json',manifest);r.exclusive(epoch/'setup-complete.json',{'manifest_sha256':r.digest(manifest)})
 for name in('operator113','worker113'):(m.root/name).mkdir(mode=0o700,exist_ok=True);r.private_dir(m.root/name)

def qualify_once(m):
 import recovery86 as r
 prepare(m);unstarted(m);w.assert_startup();before=parent(m);epoch=m.root/'retained113'
 r.exclusive(epoch/'qualification-reserved.json',{'id':AUTHORITY+'-CLIP-QUALIFY-ONCE','state':'UNKNOWN_NO_RETRY','parent':before,'identity':w.identity(),'retry':False})
 probe=m.probe(m.root/'codec106/vp8/media.webm','vp8',m.p,receipt=epoch/'worker-probe')
 after=parent(m);ok=before==after and probe.get('pass')is True
 result={'schema':'traceharbor.retained113.qualification.v1','id':AUTHORITY+'-CLIP-QUALIFY-ONCE','state':'PASS_RETAINED_CLIP113'if ok else'FAIL_RETAINED113_NO_RETRY','parent':before,'identity':w.identity(),'worker_profile_sha256':w.PROFILE_SHA256,'probe':probe,'old_FAIL_preserved':True,'new_recorders':0,'retry':False}
 r.exclusive(epoch/'qualified.json',result);return result

def codec(m):
 import recovery86 as r
 p=m.root/'retained113/qualified.json';q=r.read(p);worker=r.read(m.root/'retained113/worker-probe/result.json');w.assert_startup()
 if q.get('schema')!='traceharbor.retained113.qualification.v1'or q.get('id')!=AUTHORITY+'-CLIP-QUALIFY-ONCE'or q.get('state')!='PASS_RETAINED_CLIP113'or q.get('parent')!=parent(m)or q.get('identity')!=w.identity()or q.get('worker_profile_sha256')!=w.PROFILE_SHA256 or q.get('probe',{}).get('pass')is not True or worker.get('pass')is not True or worker.get('identity')!=w.identity()or worker.get('guard')is not None:raise r.Refusal('NEW_RETAINED_CERTIFICATE_REQUIRED')
 return 'vp8'

def summary(m):
 import recovery86 as r
 d=m.root/'retained113';p=d/'qualified.json'
 if not p.exists():return {'state':'UNKNOWN_CONSUMED_NO_RETRY'if(d/'qualification-reserved.json').exists()else'NOT_STARTED','clip_bytes':CLIP_BYTES,'old_qualification':'FAIL_NO_RETRY','new_recorders':0,'retry':False}
 q=r.read(p)
 try:codec(m);state='PASS_RETAINED_CLIP113'
 except Exception:state=q['state']if q.get('state')=='FAIL_RETAINED113_NO_RETRY'else'INELIGIBLE_CERTIFICATE_OR_PROFILE_DRIFT'
 return {'state':state,'codec':'vp8','clip_bytes':CLIP_BYTES,'clip_sha256':CLIP_SHA256,'old_qualification':'FAIL_NO_RETRY','worker_profile_sha256':w.PROFILE_SHA256,'new_recorders':0,'retry':False}

def grant_once(m):
 import recovery86 as r
 prepare(m);unstarted(m);codec(m);provider_active(m,max_age=120)
 old=m.root/'operator106/session.json'
 if old.exists()and r.read(old)['expires']>m.clock():raise r.Refusal('OLD106_SESSION_NOT_EXPIRED')
 for name,key in [('voice.wav','voice_sha256'),('edl.json','edl_member_sha256'),('captions.srt','captions_member_sha256')]:
  asset=m.root/'assets'/name;r.regular(asset)
  if w.sha(asset)!=m.p[key]:raise r.Refusal('ORIGINAL_ASSET_PIN')
 raw=os.urandom(32).hex();r.exclusive(m.root/'operator113/grant.json',{'sha256':hashlib.sha256(raw.encode()).hexdigest(),'scope':'RECOVERY86_ONLY','authority_id':AUTHORITY,'worker_profile_sha256':w.PROFILE_SHA256,'source_commit':w.identity()['source_commit'],'expires':m.clock()+m.p['session_seconds']});return raw

def provider_value(m,v,max_age,require_active=True):
 import recovery86 as r
 keys={'schema','billing_status','balance_USD','observed_at_utc','account_sha256','no_inference'}
 if set(v)!=keys or v['schema']!='traceharbor.native-provider-ready113.v1'or v['billing_status']not in('Active','Suspended')or v['account_sha256']!=ACCOUNT_SHA256 or v['no_inference']is not True or type(v['balance_USD'])is not str:raise r.Refusal('NATIVE_PROVIDER_ACTIVE_OBSERVATION_REQUIRED')
 if require_active and v['billing_status']!='Active':raise r.Refusal('PROVIDER_NOT_ACTIVE')
 observed=datetime.datetime.fromisoformat(v['observed_at_utc'].replace('Z','+00:00'))
 if observed.tzinfo is None or not 0<=m.clock()-observed.timestamp()<=max_age:raise r.Refusal('PROVIDER_OBSERVATION_NOT_FRESH')
 balance=decimal.Decimal(v['balance_USD'])
 if not balance.is_finite()or balance<(1 if require_active else 0):raise r.Refusal('PROVIDER_BALANCE_INSUFFICIENT')
 return v

def record_provider_observation(m,v):
 """Native Owner CLI only after observing same existing account ACTIVE.
 No inference probe. Each observation is immutable; no polling/background loop.
 """
 import recovery86 as r
 prepare(m);unstarted(m);provider_value(m,v,120,require_active=False);base=m.root/'retained113/provider-observations';base.mkdir(mode=0o700,exist_ok=True);r.private_dir(base)
 if len(list(base.glob('*.json')))>=3:raise r.Refusal('PROVIDER_OBSERVATION_BUDGET')
 value={'observation':v,'identity':w.identity()};r.exclusive(base/(r.digest(value)+'.json'),value);return {'state':'NATIVE_ACTIVE_OBSERVATION_RECORDED','sha256':r.digest(value)}

def provider_active(m,max_age=600):
 import recovery86 as r
 base=m.root/'retained113/provider-observations';files=list(base.glob('*.json'))if base.exists()else[]
 if not 1<=len(files)<=3:raise r.Refusal('NATIVE_PROVIDER_ACTIVE_OBSERVATION_REQUIRED')
 valid=[]
 for p in files:
  try:
   value=r.read(p)
   if value['identity']!=w.identity():continue
   v=provider_value(m,value['observation'],max_age,require_active=False);valid.append(v)
  except Exception:continue
 if valid:
  latest=max(valid,key=lambda v:(datetime.datetime.fromisoformat(v['observed_at_utc'].replace('Z','+00:00')).timestamp(),v['billing_status']!='Active'))
  return provider_value(m,latest,max_age)
 raise r.Refusal('NATIVE_PROVIDER_ACTIVE_OBSERVATION_REQUIRED')

def provider_summary(m):
 try:provider_active(m,max_age=300);return {'state':'Active','purpose':'NEW_CAPTURE_START','proof':'FRESH_NATIVE_UI_OBSERVATION_NO_INFERENCE'}
 except Exception:return {'state':'NOT_READY','purpose':'NEW_CAPTURE_START','proof':'NO_CURRENT_ACTIVE_OBSERVATION'}
