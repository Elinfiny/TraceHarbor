"""Distinct append-only RECOVERY126. Import has no filesystem or network effect."""
import contextlib,fcntl,hashlib,hmac,json,math,os,re,shutil,stat,tempfile,time,zipfile
from pathlib import Path
import source_extension115 as g
import session_continuity119 as prior
J=g.J;H=g.H;need=g.need;Closed=g.Closed
ROOT=g.ROOT;STAGE=g.STAGE;DIR=ROOT/'session126';AUTH=ROOT/'auth126';OBS=ROOT/'credit-observations126'
BASE_COMMIT='7f3fa34d3120d321634d9c88893cdb5e0d663ae8';BASE_TREE='9db3b4c7790178999227e5505dba395cfc7b823a'
OLD119_COMPLETE='2be9356a6f9db93b8e9cdd173e001abbca8d89a4664a3b56747b448b93b245cd'
OLD114_MANIFEST='593bae679950dfa3a33b5248a51a006d167e855b8f61e520a0d95d2c40957ba9'
POLICY_SHA256='ba998a54e9ba7061d56fea0124f8346b24157393a670bb41834ecd45815ab1e1'
REVIEW126_SHA256='22e1f62d035f286a1553849b1ce1f58d4cbcbb4e717728ecd740f09be13b559e'
EPOCH='TRACEHARBOR-AUTH126'
CHANGED=('credit_scope004f.py','operator004f.js','recovery004f.py','recovery004f_client.js','recovery_auth004f.py','render_recorded_release70.py','standard_billing004f.py')
PIN_KEYS=('candidate_tree','decision_sha256','contract_sha256','policy_sha256','initial_sha256','install_program_sha256','source_manifest_sha256','handoff_driver_sha256','credential_binder_sha256','preimage_basis_sha256')
_CACHE=None

def effects():
 return {'same_service':g.SERVICE,'same_root':str(ROOT),'deploy_ordinal':13,'max_new_publications':1,'max_new_deploys':1,'same_plan':True,'new_auth_epoch':EPOCH,'max_new_credentials':1,'max_new_grants':1,'max_new_sessions':1,'session_seconds_max':1800,'no_rolling_expiry':True,'metadata_global':8,'metadata_local':1,'max_new_observations':1,'metadata_min_remaining':1500,'prepare_min_remaining':1320,'metadata_fresh_seconds':120,'arm_fresh_seconds':300,'preserve119_and_metadata7':True,'same_unspent_AI004':g.REQUEST,'max_AI004':1,'additional_AI_budget':False,'finance205_sha256':g.FINANCE,'new_money_plan_terms_permissions':False,'same_allocation':True,'prior_slots':3,'next_slot':4,'HELD_before':253,'HELD_after':252,'native_seconds':2,'full_seconds':224,'AV_seconds':176,'same_Devpost':'1264455','native_Share_and_finallegal_distinct':True,'old_consumed_UNKNOWN_immutable':True,'backup_delta_max_bytes':16777216,'backup_file_max_bytes':16777216,'min_free_bytes':268435456,'max_delta_nodes':512,'access_before_clocks':True,'actual_foreground_READY_immediate_picker':True,'immutable_verification_cache':'HASH_ON_COLD_ENTRY_EVERY_STAT_AND_FILESET_GUARDED_NO_REFRESH_ON_DRIFT'}

def validate_spec(s):
 need(s.get('schema')=='traceharbor.recovery126.spec.v1'and s.get('base_commit')==BASE_COMMIT and s.get('base_tree')==BASE_TREE,'126_BASE')
 need(s.get('effects')==effects()and s.get('finance205_sha256')==g.FINANCE and s.get('request_sha256')==g.REQUEST,'126_EXACT_EFFECTS_FINANCE_REQUEST')
 need(s.get('review126_sha256')==REVIEW126_SHA256 and s.get('policy_sha256')==POLICY_SHA256 and s.get('old119_complete_sha256')==OLD119_COMPLETE,'126_ACTUAL_LINEAGE')
 a,b=s.get('old_source_pins',{}),s.get('source_pins',{})
 need(len(a)==114 and H(J(a))==OLD114_MANIFEST and len(b)==115 and H(J(b))==s.get('source_manifest_sha256'),'126_EXACT_SOURCE_CLOSURE')
 need({n for n,p in b.items()if a.get(n)!=p}==set(CHANGED)|{'recovery126.py'},'126_ONLY_EIGHT_SOURCE_DELTA')
 need(type(s.get('old_root_preimages'))is dict and 1<=len(s['old_root_preimages'])<=512 and H(J(s['old_root_preimages']))==s.get('old_root_sha256'),'126_ACTUAL_COMPLETE_OLD_ROOT')
 for k in PIN_KEYS:need(re.fullmatch('[a-f0-9]{40}'if k=='candidate_tree'else'[a-f0-9]{64}',s.get(k,'')),'126_PIN')
 return s

def validate_bindings(s,b,now):
 validate_spec(s);need(b.get('state')=='BOUND_FROM_ACTUAL_RECOVERY126_RECEIPTS','UNBOUND126_NO_EFFECT')
 need(H(J(b.get('finance205',{})))==g.FINANCE and b['finance205'].get('accepted')is True and b['finance205'].get('proposed')is False,'126_FINANCE205_UNCHANGED')
 need(H(J(b.get('preparation_review126',{})))==REVIEW126_SHA256,'126_PREPARATION_REVIEW_EXACT')
 o,r=b.get('technical_owner',{}),b.get('independent_review',{})
 need(o.get('state')=='ACTUAL_OWNER_RECOVERY126'and o.get('accepted')is True and o.get('proposed')is False,'126_ACTUAL_NEW_TECHNICAL_OWNER')
 need(r.get('state')=='ACTUAL_INDEPENDENT_RECOVERY126_ACCEPTANCE'and r.get('accepted')is True and r.get('independent')is True and r.get('proposed')is False and r.get('verdict')=='ACCEPT_COMPLETE_RECOVERY126_INSTALLABLE','126_COMPLETE_NEW_REVIEW')
 for v in(o,r):
  need(v.get('spec_sha256')==H(J(s))and v.get('effects')==effects()and v.get('finance205_sha256')==g.FINANCE and bool(v.get('canonical_source')),'126_WHOLE_RECEIPT')
  for k in PIN_KEYS:need(v.get(k)==s[k],'126_EXACT_RECEIPT_PIN')
 need(type(o.get('expires'))in(int,float)and math.isfinite(o['expires'])and now<o['expires']<=g.DEADLINE,'126_AUTHORITY_EXPIRED')
 need(re.fullmatch('[a-f0-9]{40}',b.get('published_commit',''))and b['published_commit']!=BASE_COMMIT and b.get('published_tree')==s['candidate_tree'],'126_ACTUAL_PUBLICATION')
 z=b.get('reservation',{});need(z.get('effect_id')=='RECOVERY126-APPEND-DEPLOY13-ONCE'and z.get('state')=='RESERVED_NOT_DISPATCHED'and z.get('max_dispatches')==1 and z.get('dispatch_count')==0 and z.get('spec_sha256')==H(J(s))and z.get('owner_sha256')==H(J(o))and z.get('review_sha256')==H(J(r))and bool(z.get('canonical_source')),'126_EXACT_RESERVATION')
 return o

def original_root_snapshot():
 maps={};base=ROOT/'source004/preimages004.zip'
 for p in [ROOT,*sorted(ROOT.rglob('*'))]:
  if p==base:continue
  t=p.lstat();need(not p.is_symlink()and t.st_uid==os.getuid()and len(maps)<512,'126_OLD_ROOT_CUSTODY')
  maps[str(p)]={'directory':True,'mode':stat.S_IMODE(t.st_mode)}if p.is_dir()else prior.pin(p)
 need(sum(x.get('bytes',0)for x in maps.values())<=16777216,'126_OLD_ROOT16M');return maps

def capture_unstarted(*,allow_session=False):
 a=g.ROOTS[0]/'allocation';need({p.name for p in a.glob('slot-*.json')}=={'slot-001.json','slot-002.json','slot-003.json'}and not(a/'terminal-004.json').exists(),'126_SLOT004_ALREADY_CONSUMED')
 names=['target.json','select/reserved.json','select/started.json','select/failure.json','native/reserved.json','full/reserved.json','e2e-reserved.json','demo-execution-reserved.json','av/render-reserved.json','session126/abort126.json','metadata126-reserved.json','metadata126-complete.json']
 if not allow_session:names+=['auth126/grant-consumed.json','auth126/session.json']
 for n in names:need(not(ROOT/n).exists(),'126_NEW_EFFECT_ALREADY_APPLIED_OR_UNKNOWN_'+n)

def legacy_validation():
 v=g.read(ROOT/'session119/extension119.json');s,b=v['spec'],v['bindings'];prior.validate_bindings(s,b,time.time());prior.original_grant(s)
 need(H(J(prior.bootstrap_readback(s)))==OLD119_COMPLETE,'126_OLD119_BOOTSTRAP_DRIFT')
 v115=g.read(ROOT/'source004/extension004.json');s115,b115=v115['spec'],v115['bindings'];g.validate_bindings(s115,b115,time.time());need(H(J(g.bootstrap_readback(s115)))==prior.OLD_COMPLETE_SHA256,'126_OLD115_BOOTSTRAP_DRIFT')
 maps={}
 for root in g.ROOTS:
  snap=g.snapshot(root,allow004=True);pin=s115['history']['root_preimages'][str(root)]
  need(H(J(snap))==pin['tree_sha256']and len(snap)==pin['members']and sum(x.get('bytes',0)for x in snap.values())==pin['bytes'],'126_PRIOR_ROOT_DRIFT');maps.update(snap)
 history=s115['history'];expected={Path(n).name for n in history['stage_preimages']}
 need({p.name for p in STAGE.glob('actual-*.json')}<=expected|{'actual-initial115.json','actual-recovery115.json','actual-initial119.json','actual-recovery119.json','actual-initial126.json','actual-recovery126.json'},'126_UNEXPECTED_ADMISSION')
 for name,pin in history['stage_preimages'].items():need(g.file_pin(name,131072)==pin,'126_PRIOR_ADMISSION_DRIFT');maps[name]=pin
 for name,pin in history['stage_extra_preimages'].items():
  if pin.get('directory'):g.private(name);need(stat.S_IMODE(Path(name).lstat().st_mode)==pin['mode'],'126_PRIOR_TOOL_MODE')
  else:need(g.file_pin(name,1048576)==pin,'126_PRIOR_TOOL_DRIFT')
  maps[name]=pin
 return maps

def signature(path):
 p=Path(path);t=p.lstat();runtime=Path(__file__).parent/'.venv';need(t.st_uid==os.getuid()and(not p.is_symlink()or runtime in p.parents),'126_IMMUTABLE_CUSTODY')
 if stat.S_ISDIR(t.st_mode):return(t.st_dev,t.st_ino,t.st_mode,t.st_uid)
 return (t.st_dev,t.st_ino,t.st_mode,t.st_uid,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns,os.readlink(p)if p.is_symlink()else None)

def immutable_paths(source,s):
 paths={Path(n)for n,p in s['old_root_preimages'].items()}|{source/n for n in s['source_pins']}|{source}
 for root in g.ROOTS:
  paths|={root,*[p for p in root.rglob('*')if not(root==g.ROOTS[0]and str(p)in {str(root/'allocation/slot-004.json'),str(root/'allocation/terminal-004.json')})]}
 stage_files=set(STAGE.glob('actual-*.json'))|set(STAGE.glob('recovery*-tools/install*.py'));paths|=stage_files|{p.parent for p in stage_files}|{DIR,AUTH,OBS,STAGE/'recovery126-tools'}
 for name in('source004/bootstrap-complete.json','session119/complete119.json','session126/complete126.json'):
  c=g.read(ROOT/name);paths.add(ROOT/name);paths|={Path(n)for n in c['file_pins']}
 runtime=source/'.venv'
 if runtime.exists():paths|={runtime,*[p for p in runtime.rglob('*')if '__pycache__'not in p.parts]}
 return paths

def protected_sets(source):
 # Mutable media/slot004 locations are deliberately outside these exact old sets.
 roots=list(g.ROOTS)+[ROOT/n for n in('auth004','session119','source004','credit-observations')]
 out={}
 for root in roots:
  out[str(root)]={str(p)for p in root.rglob('*')if not(root==g.ROOTS[0]and str(p)in {str(root/'allocation/slot-004.json'),str(root/'allocation/terminal-004.json')})}
 out['SOURCE']={str(p.relative_to(source))for p in source.rglob('*')if p.is_file()and not any(n in('.git','.venv','__pycache__')for n in p.relative_to(source).parts)}
 out['RUNTIME']={str(p.relative_to(source/'.venv'))for p in(source/'.venv').rglob('*')if '__pycache__'not in p.parts}
 return out

def bootstrap_readback(s):
 c=g.read(DIR/'complete126.json');need(c.get('state')=='RECOVERY126_APPEND_COMPLETE'and c.get('spec_sha256')==H(J(s))and len(c.get('file_pins',{}))==7,'126_COMPLETE_REQUIRED')
 expected={DIR/n for n in('preimages126.zip','preimages126-manifest.json','extension126.json','authority126.json')}|{STAGE/'actual-initial126.json',STAGE/'actual-recovery126.json',STAGE/'recovery126-tools/install126.py'}
 need({Path(n)for n in c['file_pins']}==expected,'126_EXACT_POSTIMAGES')
 for name,pin in c['file_pins'].items():
  actual=prior.pin(name);need(all(actual[k]==pin[k]for k in('bytes','sha256')),'126_POSTIMAGE_DRIFT')
 need(c['restore']['state']=='ISOLATED_DELTA_RESTORE_PASS'and c['base_segment']['sha256']==prior.BASE_ARCHIVE_SHA256,'126_BACKUP_RESTORE_CHAIN');return c

def authority(m=None):
 global _CACHE
 import render_recorded_release70 as launch,worker_scope004f as w
 v=g.read(DIR/'extension126.json');s,b=v['spec'],v['bindings'];now=m.clock()if m else time.time();owner=validate_bindings(s,b,now)
 ident=w.identity();need(ident['source_commit']==b['published_commit']and launch.ADMISSION_SHA256==s['initial_sha256']and launch.CREDIT004F_SHA256==s['contract_sha256'],'126_SOURCE_AUTHORITY')
 for folder in(DIR,AUTH,OBS,STAGE/'recovery126-tools'):g.private(folder)
 if m:need(m.root==ROOT and m.config==m.p['release_config']and H(J(m.p))==POLICY_SHA256,'126_SAME_CAPTURE_MODEL_POLICY')
 source=Path(__file__).parent;key=(H(J(s)),b['published_commit'],ident['instance'])
 if _CACHE is None:
  before=protected_sets(source);paths=immutable_paths(source,s);sig_before={str(p):signature(p)for p in paths};legacy_validation();g.source_check(source,s['source_pins'],runtime_required=True);bootstrap_readback(s)
  for name,pin in s['old_root_preimages'].items():
   if pin.get('directory'):g.private(name);need(stat.S_IMODE(Path(name).lstat().st_mode)==pin['mode'],'126_OLD_DIRECTORY_MODE')
   else:need(prior.pin(name)==pin,'126_OLD_ROOT_FILE_DRIFT')
  sig_after={str(p):signature(p)for p in paths};need(protected_sets(source)==before and immutable_paths(source,s)==paths and sig_before==sig_after,'126_COLD_ENTRY_FILESET_OR_STAT_RACE')
  _CACHE={'key':key,'sets':before,'pins':sig_after}
 else:
  need(_CACHE['key']==key,'126_CACHE_IDENTITY_DRIFT');need(protected_sets(source)==_CACHE['sets'],'126_IMMUTABLE_FILESET_DRIFT')
  for name,pin in _CACHE['pins'].items():need(signature(name)==pin,'126_IMMUTABLE_STAT_DRIFT')
 expected={'schema':'traceharbor.recovery126.authority.v1','spec_sha256':H(J(s)),'effects':effects(),'source_commit':b['published_commit'],'source_tree':b['published_tree'],'expires':owner['expires']}
 a=g.read(DIR/'authority126.json');need(a==expected,'126_APPEND_ONLY_AUTHORITY');return a

@contextlib.contextmanager
def allocation_lock():
 fd=os.open(g.ROOTS[0]/'allocation/lock',os.O_RDONLY|os.O_NOFOLLOW)
 try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB);yield
 finally:os.close(fd)

def reservation(z,spec,kind):
 need(z.get('state')=='RESERVED_NOT_DISPATCHED'and z.get('max_dispatches')==1 and z.get('dispatch_count')==0 and z.get('spec_sha256')==spec and z.get('effect')==kind and bool(z.get('canonical_source')),'126_DISTINCT_RESERVATION')

def prepared(m,presence,focus,access):
 a=authority(m);now=m.clock();capture_unstarted()
 need(presence.get('state')=='ACTUAL_OWNER_PRESENT_FOR_RECOVERY004F'and bool(presence.get('canonical_source'))and type(presence.get('at'))in(int,float)and 0<=now-presence['at']<=120,'126_ACTUAL_OWNER_PRESENT')
 # A small measured host/browser clock lead may be waited out before effects.
 delta=focus.get('at',0)-now
 if 0<delta<=15:time.sleep(delta);now=m.clock()
 g.validate_focus(focus,now)
 import worker_scope004f as w
 need(access.get('state')=='ACTUAL_UNTIMED_ACCESS126_VERIFIED'and all(access.get(k)is True for k in('native_input','official_form','provider_UI','capture_unstarted'))and access.get('source_commit')==w.identity()['source_commit']and access.get('instance')==w.identity()['instance']and bool(access.get('canonical_source'))and type(access.get('at'))in(int,float)and 0<=now-access['at']<=300,'126_REAL_ACCESS_BEFORE_CLOCKS')
 need(a['expires']-now>=3600 and g.DEADLINE-now>=3600,'126_COMPLETE_DELIVERY_WINDOW');return a,now

def reserve_custody(m,presence,focus,access,z):
 a,now=prepared(m,presence,focus,access);reservation(z,a['spec_sha256'],'RECOVERY126_CUSTODY')
 with allocation_lock():capture_unstarted();g.exclusive(DIR/'custody-reserved126.json',{'state':'UNKNOWN_CONSUMED_NO_RETRY','spec_sha256':a['spec_sha256'],'at':now,'retry':False})
 return {'state':'ONE126_PRIVATE_CUSTODY_RESERVED','retry':False}

def record_custody_digest(m,sha):
 a=authority(m);need(re.fullmatch('[a-f0-9]{64}',sha or''),'126_HASH_ONLY');q=g.read(DIR/'custody-reserved126.json');need(q['spec_sha256']==a['spec_sha256'],'126_CUSTODY_SCOPE');g.exclusive(DIR/'custody-produced126.json',{'credential_sha256':sha,'spec_sha256':a['spec_sha256'],'retry':False})

def issue(m,presence,focus,access,z,sha):
 a,now=prepared(m,presence,focus,access);reservation(z,a['spec_sha256'],'RECOVERY126_GRANT');q=g.read(DIR/'custody-produced126.json');need(q=={'credential_sha256':sha,'spec_sha256':a['spec_sha256'],'retry':False},'126_ACTUAL_CUSTODY')
 with allocation_lock():capture_unstarted();expiry=min(now+1800,a['expires']);g.exclusive(AUTH/'grant.json',{'scope':EPOCH,'sha256':sha,'expires':expiry,'spec_sha256':a['spec_sha256'],'retry':False})
 return {'state':'ONE126_GRANT_APPLIED_NO_SESSION','expires':expiry,'retry':False}

def consume_operator(operator,raw):
 need(isinstance(raw,bytes)and re.fullmatch(rb'[a-f0-9]{64}',raw),'126_GRANT_SHAPE');need(operator.path==AUTH and operator.scope_id==EPOCH and operator.ttl<=1800,'126_EXACT_OPERATOR');a=authority()
 with operator.lock,allocation_lock():
  capture_unstarted();q=g.read(AUTH/'grant.json');now=operator.clock();need(q['scope']==EPOCH and q['spec_sha256']==a['spec_sha256']and now<q['expires']and hmac.compare_digest(H(raw),q['sha256']),'126_GRANT_REFUSED');need(a['expires']-now>=1500,'126_AUTHORITY_REMAINING')
  g.exclusive(AUTH/'grant-consumed.json',{'scope':EPOCH,'consumed_at':now,'spec_sha256':a['spec_sha256'],'retry':False});token=os.urandom(32).hex();g.exclusive(AUTH/'session.json',{'scope':EPOCH,'sha256':H(token.encode()),'consumed_at':now,'expires':min(now+operator.ttl,now+1800,a['expires']),'spec_sha256':a['spec_sha256'],'retry':False});return token

def has_consumed_session(m,a=None):
 a=authority(m)if a is None else a;q=g.read(AUTH/'session.json');c=g.read(AUTH/'grant-consumed.json');need(q['scope']==EPOCH and q['spec_sha256']==c['spec_sha256']==a['spec_sha256']and q['consumed_at']==c['consumed_at']and q['expires']<=min(q['consumed_at']+1800,a['expires']),'126_ONE_SESSION_ENVELOPE');return True

def admin_preflight(m):
 a=authority(m);capture_unstarted(allow_session=True)
 import worker_scope004f as w
 w.assert_startup();return {'state':'ACTUAL_PRECLOCK126_SERVER_READY','identity':w.identity(),'at':m.clock(),'session_exists':(AUTH/'session.json').exists(),'session_remaining':m.operator.remaining(),'unstarted':True,'startup_qualified':True,'no_media_AI':True}

def abort_once(z,reason):
 a=authority();reservation(z,a['spec_sha256'],'RECOVERY126_ABORT');need(reason in('CONTROLLED_STOP','GUARD_REFUSED','UNKNOWN_RECONCILE'),'126_ABORT_REASON')
 with allocation_lock():capture_unstarted();g.exclusive(DIR/'abort126.json',{'state':'ABORTED_APPEND_ONLY_NO_RESET','reason':reason,'spec_sha256':a['spec_sha256'],'retry':False})
 return {'state':'ABORTED_NO_REPLAY','retry':False}

def collect_delta(source_root):
 maps=original_root_snapshot()
 for p in [STAGE/'actual-initial119.json',STAGE/'actual-recovery119.json',STAGE/'recovery119-tools/install119.py',*(Path(source_root)/n for n in CHANGED)]:maps[str(p)]=prior.pin(p,source=Path(source_root)in p.parents)
 need(len(maps)<=512 and sum(x.get('bytes',0)for x in maps.values())<=16777216,'126_DELTA_BOUND');return maps

def install(s,b,initial,contract,program,*,source_root=None,now=None):
 now=time.time()if now is None else now;validate_bindings(s,b,now);need(0<=now-b['reservation']['at']<=300,'126_FRESH_PREWRITE_RESERVATION');need(os.environ.get('RENDER')=='true'and os.environ.get('RENDER_GIT_COMMIT')==BASE_COMMIT and os.environ.get('RENDER_EXTERNAL_HOSTNAME')==g.HOST,'126_OLD_INSTANCE')
 source_root=Path.cwd()if source_root is None else Path(source_root);g.source_check(source_root,s['old_source_pins'],runtime_required=source_root==Path.cwd());legacy_validation();need(original_root_snapshot()==s['old_root_preimages'],'126_CURRENT_PREIMAGES_DRIFT')
 if source_root==Path.cwd():
  import worker_scope004f as w
  x=w.aggregate();need(x['hard_bytes']==536870912 and x['current_bytes']<469762048,'126_ACTUAL512_MARGIN')
 need(H(program)==s['install_program_sha256']and H(J(initial))==s['initial_sha256']and H(J(contract))==s['contract_sha256']and H(J(contract['policy']))==POLICY_SHA256,'126_INSTALL_PINS')
 need(not any(p.exists()for p in(DIR,AUTH,OBS,STAGE/'actual-initial126.json',STAGE/'actual-recovery126.json',STAGE/'recovery126-tools')),'126_PARTIAL_OR_APPLIED_NO_RETRY');need(shutil.disk_usage(ROOT.parent).free>=268435456,'126_FREE256M')
 with allocation_lock():
  capture_unstarted();base=ROOT/'source004/preimages004.zip';need(g.file_pin(base)['sha256']==prior.BASE_ARCHIVE_SHA256 and base.stat().st_size==prior.BASE_ARCHIVE_BYTES,'126_BASE_ARCHIVE_BYTES');bm=g.read(ROOT/'source004/preimages004-manifest.json',262144);need(H(J(bm))==prior.BASE_MANIFEST_SHA256,'126_BASE_MANIFEST')
  with zipfile.ZipFile(base)as z:need(z.testzip()is None and set(z.namelist())=={n.lstrip('/')for n,p in bm.items()if not p.get('directory')},'126_BASE_CRC_MEMBERS')
  maps=collect_delta(source_root)
  with tempfile.TemporaryDirectory(prefix='.recovery126-backup-',dir=ROOT.parent)as td:
   backup=Path(td)/'delta126.zip';prior.archive_delta(maps,backup);proof=prior.restore_delta(backup,maps);need(collect_delta(source_root)==maps,'126_PREAPPEND_DRIFT');bp=prior.pin(backup)
   for p in(DIR,AUTH,OBS,STAGE/'recovery126-tools'):p.mkdir(mode=0o700)
   a={'schema':'traceharbor.recovery126.authority.v1','spec_sha256':H(J(s)),'effects':effects(),'source_commit':b['published_commit'],'source_tree':b['published_tree'],'expires':b['technical_owner']['expires']}
   g.exclusive_copy(DIR/'preimages126.zip',backup);writes={DIR/'preimages126-manifest.json':J(maps),DIR/'extension126.json':J({'spec':s,'bindings':b}),DIR/'authority126.json':J(a),STAGE/'actual-initial126.json':J(initial),STAGE/'actual-recovery126.json':J(contract),STAGE/'recovery126-tools/install126.py':program}
   for p,data in writes.items():g.exclusive(p,data)
   pins={str(p):{'bytes':len(data),'sha256':H(data)}for p,data in writes.items()};pins[str(DIR/'preimages126.zip')]={k:bp[k]for k in('bytes','sha256')}
   c={'state':'RECOVERY126_APPEND_COMPLETE','spec_sha256':H(J(s)),'file_pins':pins,'restore':proof,'base_segment':{'path':str(base),'bytes':prior.BASE_ARCHIVE_BYTES,'sha256':prior.BASE_ARCHIVE_SHA256,'manifest_sha256':prior.BASE_MANIFEST_SHA256,'accepted_full_restore':prior.OLD_COMPLETE_SHA256,'files':522},'retry':False};g.exclusive(DIR/'complete126.json',c);need(H(J(bootstrap_readback(s)))==H(J(c)),'126_COMPLETE_READBACK');capture_unstarted()
   return {'state':'RECOVERY126_APPEND8_FILES4_DIRS_VERIFIED_NO_TIMERS','complete_sha256':H(J(c)),'delta_backup':bp,'restore':proof,'base_segment':c['base_segment'],'retry':False}

ACCESS_SCRIPT126=b'''(()=>{const o=document.getElementById('access126');if(!o)return;const a=new AbortController(),t=setTimeout(()=>a.abort(),8000);fetch('/recovery004f/preflight126',{credentials:'same-origin',cache:'no-store',redirect:'error',signal:a.signal}).then(async r=>{if(!r.ok)throw Error('AUTH_REQUIRED');const v=await r.json();if(v.state!=='ACTUAL_PRECLOCK126_SERVER_READY'||v.unstarted!==true||v.startup_qualified!==true||v.session_exists!==true||v.session_remaining<1500)throw Error('NOT_READY');Object.assign(o.dataset,{ready:'true',source:v.identity.source_commit,instance:v.identity.instance,sampledAt:String(Date.now()),sessionRemaining:String(v.session_remaining)});o.textContent='Acces privat126 verificat. Sesiunea este valabila; captura nu este pornita.';}).catch(()=>{o.dataset.ready='false';o.textContent='Accesul privat126 nu este inca verificat. Nu porni metadate sau captura.';}).finally(()=>clearTimeout(t));})();'''
