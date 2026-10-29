"""Prepared distinct recovery after the known143 selector failure. No import effects.

Native boot/CLI remains separately admitted. No old files are reset or renamed.
One prepared browser capability is issued before the Owner's direct click. The
120s timer begins only at that click's start request, never while packaging.
"""
import hashlib,hmac,json,math,os,threading
from pathlib import Path

EPOCH='capture146'
AUTHORITY='TRACEHARBOR-CAPTURE146-DISTINCT-AFTER-CLOSED143'
AUTHORITY_PATH=Path('/var/data/traceharbor-staging/capture146-authority.json')
DEADLINE146=1793379600 # 30 Oct 2026,17:00 UTC /19:00 Romania.
PINS={'credit132/qualified.json': {'bytes': 2019, 'sha256': '778ed210defc6aa2592349b30f75e081991fc2bb353f443daeeb41fd4921b57e'}, 'demo-armed.json': {'bytes': 191, 'sha256': '159c4adf2bfa16957728bba4b248fa324df7731727b0db7f2092d6073a204385'}, 'demo-armed113.json': {'bytes': 340, 'sha256': '4f33502b3cc4039bb553e675226c83c547b8201017056364e781fda620e0bf5e'}, 'operator113/grant-consumed.json': {'bytes': 41, 'sha256': 'b0b28d1d8461b18f8502d60b8157cd6e3fa1f02ff84edf024660369441f652f4'}, 'operator113/grant.json': {'bytes': 320, 'sha256': 'a59d1d6cfb195a2caafb164257d8cf73510370f3a002a766301e89e105b190b0'}, 'operator113/session.json': {'bytes': 131, 'sha256': 'bb30406a4fbec46be15bcb71c74e330d414efec965cc7d004f3f8604c6b00153'}, 'retained113/qualified.json': {'bytes': 2023, 'sha256': '4a7e7e62198c295b3b966f2371af8f46e58e383e2261033b6016393ba1e48517'}, 'select/failure.json': {'bytes': 106, 'sha256': 'a38128349b6c7d69b6dea00d6a633ba17eb41d2e0052e1c90ef94941064b48b6'}, 'select/reserved.json': {'bytes': 178, 'sha256': '783b5bcc5107919f79160a09f600e34a94a932b92b4a0c57703a0537dc102091'}}

def require_authority(m):
 import recovery86 as r,worker_scope113 as w
 p=AUTHORITY_PATH
 r.regular(p);a=r.read(p,4096)
 if a.get('schema')!='traceharbor.capture146.authority.v1'or a.get('authority')!=AUTHORITY or a.get('accepted')is not True or a.get('source_commit')!=w.identity()['source_commit']or a.get('deploy_slot')!=2 or a.get('max_total_deploys')!=2 or a.get('max_sessions')!=1 or a.get('max_selectors')!=1 or a.get('additional_AI_calls')!=0 or a.get('paid_continuation_disabled')is not True or a.get('new_cost_permissions_terms')is not False:raise r.Refusal('DISTINCT_OWNER_AND_AUDITOR_AUTHORITY_REQUIRED')
 for key in ('owner_scope_sha256','independent_review_sha256'):
  if not isinstance(a.get(key),str)or not __import__('re').fullmatch('[a-f0-9]{64}',a[key]):raise r.Refusal('DISTINCT_AUTHORITY_RECEIPT_BINDING')
 if type(a.get('expires'))not in(int,float)or not math.isfinite(a['expires'])or not m.clock()<a['expires']<=DEADLINE146:raise r.Refusal('DISTINCT_AUTHORITY_EXPIRED')
 return a

def old143(m):
 import recovery86 as r
 m.assert_original()
 for name,pin in PINS.items():
  p=m.root/name;r.regular(p)
  if p.stat().st_size!=pin['bytes']or hashlib.sha256(p.read_bytes()).hexdigest()!=pin['sha256']:raise r.Refusal('ORIGINAL143_PIN_DRIFT')
 f=r.read(m.root/'select/failure.json')
 if f!={'error_name':'UnclassifiedError','phase':'select','retry':False,'state':'FAILED_NO_RETRY','where':'FLOW'}:raise r.Refusal('KNOWN_CLOSED143_REQUIRED')
 q=r.read(m.root/'credit132/qualified.json')
 if q.get('state')!='PASS_RETAINED_CLIP132'or q.get('identity',{}).get('source_commit')!='fb12392d71be6d2acdcd53e7932983db20c22dec':raise r.Refusal('EXACT_PRIOR132_CERTIFICATE_REQUIRED')
 # No old server stream can survive this failure. The cancelled browser page
 # and original failure are separate evidence; no fabricated terminal is made.
 if (m.root/'select/terminal.json').exists():raise r.Refusal('ORIGINAL143_TERMINAL_DRIFT')
 if r.read(m.root/'operator113/session.json')['expires']>m.clock():raise r.Refusal('OLD113_SESSION_MUST_BE_EXPIRED')
 return {'pins':PINS,'old_state':'FAILED_NO_RETRY','old_terminal_file':False}

def unconsumed_media(m):
 import recovery86 as r
 if any((m.root/n/'reserved.json').exists()for n in('native','full'))or(m.root/'demo-execution-reserved.json').exists()or any((m.original/n).exists()for n in('e2e-reserved.json','e2e-result.json','provider-response132.json'))or(m.root/'av/render-reserved.json').exists():raise r.Refusal('ORIGINAL_MEDIA_OR_E2E_CONSUMED')
 if any(any((m.root/n).iterdir())for n in('native','full')):raise r.Refusal('UNRESERVED_OR_PARTIAL_MEDIA_PRESENT')
 ledger=r.Ledger(m.original/'allocation',m.config).snapshot()
 if ledger.get('reserved_calls')!=0 or ledger.get('remaining_calls')!=256:raise r.Refusal('ORIGINAL_AI_ALLOCATION_CONSUMED')
 return ledger

def idle(m):
 import recovery86 as r
 require_authority(m);old143(m);unconsumed_media(m)
 if (m.root/EPOCH/'select/started.json').exists()or(m.root/EPOCH/'select/failure.json').exists():raise r.Refusal('DISTINCT_SELECTION_ALREADY_ATTEMPTED')

def directory(m):return m.root/EPOCH/'select'

def fail_selection(m,name,where):
 import recovery86 as r
 d=directory(m)
 with m.lock:
  if not(d/'reserved.json').exists():raise r.Refusal('UNRESERVED_DISTINCT_FAILURE')
  if (d/'failure.json').exists():return r.read(d/'failure.json')
  terminal=d/'terminal.json'
  if terminal.exists():return r.read(terminal) # Stream accepted: native phase owns failure.
  value={'state':'FAILED_NO_RETRY','phase':'select','error_name':name if name in r.NAMES else'UnclassifiedError','where':where if where in {'SELECT','TIMEOUT','FLOW','TRACK_ENDED'}else'FLOW','authority':AUTHORITY,'at':m.clock(),'retry':False}
  r.exclusive(d/'failure.json',value);r.exclusive(terminal,value)
  timer=getattr(m,'selection_timer146',None)
  if timer is not None:timer.cancel()
  return value

def prepare_selection(m,codec):
 import recovery86 as r,retained_scope113 as s,worker_scope113 as w
 with m.lock:
  idle(m);s.codec(m);s.provider_active(m,max_age=120)
  if codec!='vp8'or m.operator.remaining()<400 or not(m.root/EPOCH/'target.json').exists():raise r.Refusal('DISTINCT_SELECTION_NOT_READY')
  observed=s.provider_active(m,max_age=120)
  stamp=__import__('datetime').datetime.fromisoformat(observed['observed_at_utc'].replace('Z','+00:00')).timestamp()
  # Enough lease to use the existing browser tab, without claiming it is fresh
  # forever. Expiry is explicit and never triggers another picker or grant.
  lease_ms=int(min(300-(m.clock()-stamp),m.operator.remaining()-400)*1000)
  if lease_ms<=0:raise r.Refusal('DISTINCT_READINESS_EXPIRED')
  key=os.urandom(32).hex();value={'schema':'traceharbor.capture146.selection.v1','id':AUTHORITY+'-SELECT-ONCE','state':'PREPARED_OWNER_GESTURE_ONLY','key_sha256':hashlib.sha256(key.encode()).hexdigest(),'prepared_at':m.clock(),'expires':m.clock()+lease_ms/1000,'identity':w.identity(),'target_sha256':r.digest(r.read(m.root/EPOCH/'target.json')),'codec':codec,'retry':False}
  r.exclusive(directory(m)/'reserved.json',value)
  return {'state':'PREPARED_OWNER_GESTURE_ONLY','key':key,'lease_ms':lease_ms,'codec':codec,'picker_seconds':120,'identity':w.identity(),'retry':False}

def start_selection(m,key):
 import recovery86 as r,retained_scope113 as s,worker_scope113 as w
 with m.lock:
  idle(m);s.provider_active(m,max_age=300);v=r.read(directory(m)/'reserved.json')
  if not isinstance(key,str)or len(key)!=64 or not hmac.compare_digest(hashlib.sha256(key.encode()).hexdigest(),v['key_sha256']):raise r.Refusal('DISTINCT_SELECTION_CAPABILITY')
  if m.clock()>=v['expires']or v['identity']!=w.identity()or v['target_sha256']!=r.digest(r.read(m.root/EPOCH/'target.json'))or m.operator.remaining()<400:raise r.Refusal('DISTINCT_READINESS_EXPIRED_OR_DRIFT')
  r.exclusive(directory(m)/'started.json',{'state':'NATIVE_PERMISSION_PENDING','at':m.clock(),'key_sha256':v['key_sha256'],'identity':w.identity(),'retry':False})
  # One finite application timer, not a scheduler/agent. It records a timeout
  # independently of an expired cookie or a still-pending browser promise.
  timer=m.selection_timer_factory146(120,lambda:fail_selection(m,'TimeoutError','TIMEOUT'))
  m.selection_timer146=timer;timer.daemon=True;timer.start()
  return {'state':'NATIVE_PERMISSION_PENDING','seconds':120,'retry':False}

def media_gate(m):
 import recovery86 as r,worker_scope113 as w
 require_authority(m)
 d=directory(m);v=r.read(d/'started.json')
 if (d/'failure.json').exists()or v['identity']!=w.identity()or not 0<=m.clock()-v['at']<=120:raise r.Refusal('DISTINCT_SELECTION_EXPIRED_OR_FAILED')
 return v

def accept_stream(m):
 import recovery86 as r
 media_gate(m)
 # Called only once the original native reservation has actually been made.
 timer=getattr(m,'selection_timer146',None)
 if timer is not None:timer.cancel()
 r.exclusive(directory(m)/'terminal.json',{'state':'STREAM_ACCEPTED_NATIVE_NOT_QUALIFIED','phase':'select','at':m.clock(),'retry':False})

def snapshot(m):
 import recovery86 as r
 d=directory(m)
 for name in('failure.json','terminal.json','started.json'):
  if(d/name).exists():return r.read(d/name)
 if(d/'reserved.json').exists():return {'state':'PREPARED_OWNER_GESTURE_ONLY','retry':False}
 return {'state':'NOT_STARTED','retry':False}
