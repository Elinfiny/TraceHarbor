"""Append-only session continuity on the existing004f root.
Import has no I/O. No grant renewal, timer reset, model call or media changes.
"""
import contextlib,fcntl,hashlib,hmac,json,math,os,re,shutil,stat,tempfile,time,zipfile
from pathlib import Path
import source_extension115 as old
J=old.J;H=old.H;need=old.need;Closed=old.Closed
ROOT=old.ROOT;STAGE=old.STAGE;DIR=ROOT/'session119';EPOCH='TRACEHARBOR-AUTH004F'
BASE_COMMIT='7fadba1e44ed73f25d4298da4c35d302734ef978';BASE_TREE='4459ac97c9fa11b6faad1b872109eeb15376f709'
OLD_SPEC_SHA256='fa21790463cdbaf9aaeb1d57f7b986b3c70e7f1a39ab00b19a8ce54f95038905'
OLD_COMPLETE_SHA256='4af8044e2d7a9dfe46fc370960e546212d949c4d293276705a307e11a162b64f'
OLD_STARTUP_SHA256='eff646c7e841310d831387515fc324c6bdd18195f8992afcf9189c8a411c24e8'
BASE_ARCHIVE_SHA256='1cd294d9624100c2e3696dc04a9b94768d85aaca7d9b57c905c61c20620991b7'
BASE_ARCHIVE_BYTES=102287618
BASE_MANIFEST_SHA256='043dc0f801a41f02fd90e6130f7c4ea0c8ac7f4d0ea0e077f3334a21a88e0db7'
REVIEW119_SHA256='eef69cdea0b1fdbc8c9b466a2f4ea136e87bf0323d3f13fdea1296da1ea8fa21'
BASE_SOURCE_MANIFEST='c34aee71ef8315a9ea9f20c7801fda0cef6d4d53f93791cda0a10e0ce5cb4187'
UNCHANGED_POLICY_SHA256='ba998a54e9ba7061d56fea0124f8346b24157393a670bb41834ecd45815ab1e1'
CHANGED_OLD_FILES=('recovery004f.py','recovery_auth004f.py','render_recorded_release70.py')
PIN_KEYS=('candidate_tree','decision_sha256','contract_sha256','policy_sha256','initial_sha256','install_program_sha256','source_manifest_sha256','handoff_driver_sha256','credential_binder_sha256','preimage_basis_sha256')

def effects():
 return {'same_service':old.SERVICE,'same_root':str(ROOT),'deploy_ordinal':12,'max_new_publications':1,'max_new_deploys':1,'same_plan':True,'session_seconds_max':1800,'max_sessions_total':1,'max_supplementary_grants_if_needed':1,'max_supplementary_credentials_if_needed':1,'preserve_original_grant_bytes_and_expiry':True,'no_rolling_expiry':True,'metadata_global':7,'metadata_local':1,'metadata_min_remaining':1500,'prepare_min_remaining':1320,'unchanged_other_remaining_guards':True,'same_unspent_AI004':old.REQUEST,'max_AI004':1,'additional_AI_budget':False,'finance205_sha256':old.FINANCE,'new_money_plan_terms_permissions':False,'same_allocation':True,'prior_slots':3,'next_slot':4,'HELD_before':253,'HELD_after':252,'native_seconds':2,'full_seconds':224,'AV_seconds':176,'same_Devpost':'1264455','native_Share_and_finallegal_distinct':True,'old_consumed_UNKNOWN_immutable':True,'new_access_preflight_before_secret_or_clock':True,'focus_revalidated_before_arm_and_READY_immediate_click':True,'backup_delta_max_bytes':16777216,'backup_file_max_bytes':16777216,'min_free_bytes':268435456,'append_only_logical_abort_before_session':True}

def validate_spec(s):
 need(s.get('schema')=='traceharbor.session119.spec.v1'and s.get('base_commit')==BASE_COMMIT and s.get('base_tree')==BASE_TREE,'119_BASE')
 need(s.get('effects')==effects()and s.get('old_spec_sha256')==OLD_SPEC_SHA256 and s.get('review119_sha256')==REVIEW119_SHA256,'119_EXACT_EFFECTS_LINEAGE')
 need(s.get('finance205_sha256')==old.FINANCE and s.get('request_sha256')==old.REQUEST and s.get('old_complete_sha256')==OLD_COMPLETE_SHA256,'119_SAME_FINANCE_REQUEST')
 need(len(s.get('old_source_pins',{}))==113 and len(s.get('source_pins',{}))==114 and H(J(s['source_pins']))==s.get('source_manifest_sha256'),'119_EXACT_SOURCE_CLOSURE')
 need(H(J(s['old_source_pins']))==BASE_SOURCE_MANIFEST and s.get('policy_sha256')==UNCHANGED_POLICY_SHA256,'119_BASE113_AND_MEDIA_MODEL_POLICY_IMMUTABLE')
 delta={n for n,p in s['source_pins'].items()if s['old_source_pins'].get(n)!=p};need(delta==set(CHANGED_OLD_FILES)|{'session_continuity119.py'},'119_ONLY_FOUR_SOURCE_DELTA')
 need(re.fullmatch('[a-f0-9]{40}',s.get('candidate_tree','')),'119_TREE')
 for key in PIN_KEYS:
  if key!='candidate_tree':need(re.fullmatch('[a-f0-9]{64}',s.get(key,'')),'119_PIN')
 return s

def validate_bindings(s,b,now):
 validate_spec(s);need(b.get('state')=='BOUND_FROM_ACTUAL_SESSION119_RECEIPTS','UNBOUND119_NO_EFFECT')
 f=b.get('finance205',{});need(H(J(f))==old.FINANCE and f.get('accepted')is True and f.get('proposed')is False,'119_FINANCE205_UNCHANGED')
 need(H(J(b.get('review119',{})))==REVIEW119_SHA256,'119_ACTUAL_PREPARATION_LINEAGE')
 o=b.get('technical_owner',{});r=b.get('independent_review',{})
 need(o.get('state')=='ACTUAL_OWNER_SESSION119'and o.get('accepted')is True and o.get('proposed')is False,'119_ACTUAL_TECHNICAL_OWNER')
 need(r.get('state')=='ACTUAL_INDEPENDENT_SESSION119_ACCEPTANCE'and r.get('accepted')is True and r.get('independent')is True and r.get('proposed')is False and r.get('verdict')=='ACCEPT_MINIMAL_SESSION119_INSTALLABLE','119_NEW_WHOLE_REVIEW_REQUIRED')
 for v in(o,r):
  need(v.get('spec_sha256')==H(J(s))and v.get('effects')==effects()and v.get('finance205_sha256')==old.FINANCE and bool(v.get('canonical_source')),'119_WHOLE_RECEIPT')
  for k in PIN_KEYS:need(v.get(k)==s[k],'119_EXACT_RECEIPT_PIN')
 need(type(o.get('expires'))in(int,float)and math.isfinite(o['expires'])and now<o['expires']<=old.DEADLINE,'119_AUTHORITY_EXPIRED')
 need(re.fullmatch('[a-f0-9]{40}',b.get('published_commit',''))and b['published_commit']!=BASE_COMMIT and b.get('published_tree')==s['candidate_tree'],'119_ACTUAL_PUBLICATION')
 z=b.get('reservation',{});need(z.get('effect_id')=='SESSION119-APPEND-DEPLOY12-ONCE'and z.get('state')=='RESERVED_NOT_DISPATCHED'and z.get('dispatch_count')==0 and z.get('max_dispatches')==1 and z.get('spec_sha256')==H(J(s))and z.get('owner_sha256')==H(J(o))and z.get('review_sha256')==H(J(r))and bool(z.get('canonical_source')),'119_EXACT_RESERVATION');return o

def original_grant(s):
 p=ROOT/'auth004/grant.json';pin=old.file_pin(p);need(pin==s['original_grant_pin'],'119_ORIGINAL_GRANT_DRIFT');v=old.read(p)
 need(v.get('scope')==EPOCH and v.get('spec_sha256')==OLD_SPEC_SHA256,'119_ORIGINAL_GRANT_SCOPE');return v

def old_lineage():
 v=old.read(ROOT/'source004/extension004.json');s,b=v['spec'],v['bindings'];need(H(J(s))==OLD_SPEC_SHA256,'119_ORIGINAL_SPEC_DRIFT');old.validate_bindings(s,b,time.time())
 complete=old.bootstrap_readback(s);need(H(J(complete))==OLD_COMPLETE_SHA256,'119_BASE_BOOTSTRAP_DRIFT');check_prior_history(s['history'])
 q=old.read(ROOT/'worker113/preflight'/BASE_COMMIT/'qualified.json');need(H(J(q))==OLD_STARTUP_SHA256 and q['state']=='PASS_NO_MEDIA_NOT_ENCODER_QUALIFICATION','119_OLD_STARTUP_PRESERVED')
 return v

def check_prior_history(history):
 # Same six immutable roots and exact prior admission/tool pins. Only the two
 # specifically pinned119 admissions may be appended; the old guard is unchanged.
 need(set(history['root_preimages'])==set(map(str,old.ROOTS)),'119_SIX_PRIOR_ROOTS')
 for root in old.ROOTS:
  v=old.snapshot(root,allow004=True);p=history['root_preimages'][str(root)];need(H(J(v))==p['tree_sha256']and len(v)==p['members']and sum(x.get('bytes',0)for x in v.values())==p['bytes'],'119_PRIOR_ROOT_DRIFT')
 expected={Path(n).name for n in history['stage_preimages']};need({p.name for p in STAGE.glob('actual-*.json')}<=expected|{'actual-initial115.json','actual-recovery115.json','actual-initial119.json','actual-recovery119.json'},'119_UNEXPECTED_ADMISSION')
 for n,p in history['stage_preimages'].items():need(old.file_pin(n,131072)==p,'119_PRIOR_ADMISSION_DRIFT')
 for n,p in history['stage_extra_preimages'].items():
  if p.get('directory'):old.private(n);need(stat.S_IMODE(Path(n).lstat().st_mode)==p['mode'],'119_PRIOR_TOOL_MODE')
  else:need(old.file_pin(n,1048576)==p,'119_PRIOR_TOOL_DRIFT')
 return True

def authority(m=None):
 import render_recorded_release70 as launch,worker_scope004f as w
 v=old.read(DIR/'extension119.json');s,b=v['spec'],v['bindings'];now=m.clock()if m else time.time();validate_bindings(s,b,now);old_lineage();original_grant(s)
 if m:
  import credit_scope004f as c
  c.assert_parent(m);need(m.root==ROOT and m.config==m.p['release_config']and H(J(m.p))==s['policy_sha256'],'119_EXACT_EXISTING_MODEL_CAPTURE_POLICY')
 ident=w.identity();need(ident['source_commit']==b['published_commit']and launch.ADMISSION_SHA256==s['initial_sha256']and launch.CREDIT004F_SHA256==s['contract_sha256'],'119_CURRENT_SOURCE_AUTHORITY')
 old.source_check(Path(__file__).parent,s['source_pins'],runtime_required=True);bootstrap_readback(s)
 expected={'schema':'traceharbor.session119.authority.v1','spec_sha256':H(J(s)),'effects':effects(),'source_commit':b['published_commit'],'source_tree':b['published_tree'],'expires':b['technical_owner']['expires'],'original_grant_pin':s['original_grant_pin']}
 a=old.read(DIR/'authority119.json');need(a==expected,'119_APPEND_ONLY_AUTHORITY');return a

@contextlib.contextmanager
def allocation_lock():
 fd=os.open(old.ROOTS[0]/'allocation/lock',os.O_RDONLY|os.O_NOFOLLOW)
 try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB);yield
 finally:os.close(fd)

def unstarted(*,allow_branch=False):
 a=old.ROOTS[0]/'allocation';need({p.name for p in a.glob('slot-*.json')}=={'slot-001.json','slot-002.json','slot-003.json'}and not(a/'terminal-004.json').exists(),'119_SHARED_SLOT004_ALREADY_CONSUMED')
 for n in('session119/abort119.json','auth004/session.json','auth004/grant-consumed.json','auth004/grant119-consumed.json','metadata004-reserved.json','metadata004-complete.json','target.json','select/reserved.json','select/started.json','select/failure.json','native/reserved.json','full/reserved.json','e2e-reserved.json','av/render-reserved.json'):
  need(not(ROOT/n).exists(),'119_PREEXISTING_EFFECT_RECONCILE_NO_RETRY')
 need(allow_branch or not(DIR/'branch119.json').exists(),'119_BRANCH_ALREADY_RESERVED')

def prepared(m,presence,focus,access):
 a=authority(m);unstarted();import worker_scope004f as w;w.assert_startup();now=m.clock()
 # A bounded wait is strictly before any secret/grant/session effect and never
 # changes either timestamp. The same strict original focus check then applies.
 until=time.monotonic()+15
 while now<focus.get('at',0)and time.monotonic()<until:time.sleep(0.05);now=m.clock()
 old.validate_focus(focus,now)
 need(presence.get('state')=='ACTUAL_OWNER_PRESENT_FOR_RECOVERY004F'and bool(presence.get('canonical_source'))and type(presence.get('at'))in(int,float)and 0<=now-presence['at']<=120,'119_ACTUAL_OWNER_PRESENCE')
 need(access.get('state')=='ACTUAL_UNTIMED_ACCESS119_VERIFIED'and all(access.get(k)is True for k in('native_input','official_form','provider_UI','capture_unstarted'))and access.get('source_commit')==w.identity()['source_commit']and access.get('instance')==w.identity()['instance']and bool(access.get('canonical_source'))and type(access.get('at'))in(int,float)and 0<=now-access['at']<=300,'119_ACCESS_PROOF_REQUIRED_BEFORE_CLOCKS')
 need(a['expires']-now>=1800 and old.DEADLINE-now>=3600,'119_COMPLETE_DELIVERY_WINDOW');return a,now

def reservation(z,spec_sha256,kind):
 need(z.get('state')=='RESERVED_NOT_DISPATCHED'and z.get('max_dispatches')==1 and z.get('dispatch_count')==0 and z.get('spec_sha256')==spec_sha256 and z.get('effect')==kind and bool(z.get('canonical_source')),'119_DISTINCT_EFFECT_RESERVATION')

def admit_existing(m,presence,focus,access,z,private_nonce_proof):
 a,now=prepared(m,presence,focus,access);reservation(z,a['spec_sha256'],'SESSION119_EXISTING_GRANT_BRANCH');s=old.read(DIR/'extension119.json')['spec'];g=original_grant(s)
 need(private_nonce_proof.get('available')is True and private_nonce_proof.get('sha256')==g['sha256']and bool(private_nonce_proof.get('canonical_source')),'119_EXISTING_NONCE_PRIVATE_CUSTODY')
 need(g['expires']-now>=120,'119_OLD_GRANT_NOT_ENOUGH_ENTRY_MARGIN_WAIT_UNTIMED_NO_EFFECT')
 with allocation_lock():
  unstarted();need(not(DIR/'custody-reserved119.json').exists()and not(ROOT/'auth004/grant119.json').exists(),'119_SUPPLEMENT_BRANCH_ALREADY_USED')
  old.exclusive(DIR/'branch119.json',{'state':'ONE_SESSION_BRANCH_RESERVED_NO_RETRY','mode':'EXISTING','credential_sha256':g['sha256'],'credential_file':'grant.json','grant_expires':g['expires'],'spec_sha256':a['spec_sha256'],'original_grant_pin':s['original_grant_pin'],'at':now,'retry':False})
 return {'state':'EXISTING_GRANT_BRANCH_ADMITTED_ONCE_NO_SESSION','retry':False}

def reserve_custody(m,presence,focus,access,z,private_nonce_proof):
 a,now=prepared(m,presence,focus,access);reservation(z,a['spec_sha256'],'SESSION119_SUPPLEMENT_CUSTODY');s=old.read(DIR/'extension119.json')['spec'];g=original_grant(s)
 unavailable=private_nonce_proof.get('available')is False and bool(private_nonce_proof.get('canonical_source'))
 need(now>=g['expires']or unavailable,'119_SUPPLEMENT_ONLY_EXPIRED_OR_PROVEN_NONCE_UNAVAILABLE')
 with allocation_lock():
  unstarted();need(not(ROOT/'auth004/grant119.json').exists(),'119_SUPPLEMENT_ALREADY_CREATED')
  old.exclusive(DIR/'custody-reserved119.json',{'state':'UNKNOWN_CONSUMED_NO_RETRY','spec_sha256':a['spec_sha256'],'old_grant_pin':s['original_grant_pin'],'reason':'EXPIRED'if now>=g['expires']else'PRIVATE_NONCE_UNAVAILABLE','at':now,'retry':False})
 return {'state':'ONE_SUPPLEMENT_CUSTODY_RESERVED_NO_RETRY','retry':False}

def record_custody_digest(m,sha256):
 a=authority(m);need(re.fullmatch('[a-f0-9]{64}',sha256 or''),'119_HASH_ONLY');q=old.read(DIR/'custody-reserved119.json');need(q['spec_sha256']==a['spec_sha256'],'119_CUSTODY_SCOPE')
 old.exclusive(DIR/'custody-produced119.json',{'credential_sha256':sha256,'spec_sha256':a['spec_sha256'],'retry':False})

def abort_once(z,reason):
 a=authority();reservation(z,a['spec_sha256'],'SESSION119_ABORT');need(reason in('CONTROLLED_STOP','GUARD_REFUSED','UNKNOWN_RECONCILE'),'119_ABORT_REASON')
 with allocation_lock():unstarted(allow_branch=True);old.exclusive(DIR/'abort119.json',{'state':'ABORTED_APPEND_ONLY_NO_OLD_REPLAY','spec_sha256':a['spec_sha256'],'reason':reason,'retry':False})
 return {'state':'ABORTED_NO_RESET_NO_REDEPLOY','retry':False}

def admit_supplement(m,presence,focus,access,z,sha256):
 a,now=prepared(m,presence,focus,access);reservation(z,a['spec_sha256'],'SESSION119_SUPPLEMENT_GRANT');s=old.read(DIR/'extension119.json')['spec'];g=original_grant(s)
 q=old.read(DIR/'custody-reserved119.json');produced=old.read(DIR/'custody-produced119.json');need(q['spec_sha256']==a['spec_sha256']and produced=={'credential_sha256':sha256,'spec_sha256':a['spec_sha256'],'retry':False},'119_ACTUAL_SINGLE_PRIVATE_CUSTODY')
 need(now>=g['expires']or q['reason']=='PRIVATE_NONCE_UNAVAILABLE','119_SUPPLEMENT_BRANCH_CONDITION')
 with allocation_lock():
  unstarted();expiry=min(now+1800,a['expires']);record={'scope':EPOCH,'sha256':sha256,'expires':expiry,'spec_sha256':a['spec_sha256'],'original_grant_pin':s['original_grant_pin'],'retry':False};old.exclusive(ROOT/'auth004/grant119.json',record)
  old.exclusive(DIR/'branch119.json',{'state':'ONE_SESSION_BRANCH_RESERVED_NO_RETRY','mode':'SUPPLEMENT','credential_sha256':sha256,'credential_file':'grant119.json','grant_expires':expiry,'spec_sha256':a['spec_sha256'],'original_grant_pin':s['original_grant_pin'],'at':now,'retry':False})
 return {'state':'ONE_DISTINCT_SUPPLEMENT_GRANT_ADMITTED_NO_SESSION','expires':expiry,'retry':False}

def consume_operator(operator,raw):
 need(isinstance(raw,bytes)and re.fullmatch(rb'[a-f0-9]{64}',raw),'119_GRANT_SHAPE');need(operator.path==ROOT/'auth004'and operator.scope_id==EPOCH and operator.ttl<=1800,'119_EXACT_OPERATOR')
 a=authority();s=old.read(DIR/'extension119.json')['spec'];original_grant(s)
 with operator.lock,allocation_lock():
  unstarted(allow_branch=True);branch=old.read(DIR/'branch119.json');need(branch['spec_sha256']==a['spec_sha256']and branch['mode']in('EXISTING','SUPPLEMENT'),'119_BRANCH_SCOPE')
  need(branch['credential_file']==('grant.json'if branch['mode']=='EXISTING'else'grant119.json'),'119_BRANCH_CREDENTIAL_PATH');g=old.read(operator.path/branch['credential_file']);now=operator.clock()
  need(g['scope']==EPOCH and now<g['expires']and g['expires']==branch['grant_expires']and hmac.compare_digest(H(raw),branch['credential_sha256'])and hmac.compare_digest(H(raw),g['sha256']),'119_GRANT_REFUSED')
  need(now<a['expires']and a['expires']-now>=1500,'119_AUTHORITY_REMAINING_BEFORE_SESSION')
  marker='grant-consumed.json'if branch['mode']=='EXISTING'else'grant119-consumed.json';branch_sha=H(J(branch));expires=min(now+operator.ttl,now+1800,a['expires'])
  old.exclusive(operator.path/marker,{'scope':EPOCH,'branch_sha256':branch_sha,'spec_sha256':a['spec_sha256'],'consumed_at':now,'retry':False})
  token=os.urandom(32).hex();old.exclusive(operator.path/'session.json',{'sha256':H(token.encode()),'scope':EPOCH,'expires':expires,'consumed_at':now,'branch_sha256':branch_sha,'admission_sha256':a['spec_sha256'],'retry':False});return token

def has_consumed_session(m,a=None):
 a=authority(m)if a is None else a;branch=old.read(DIR/'branch119.json');q=old.read(ROOT/'auth004/session.json');marker='grant-consumed.json'if branch['mode']=='EXISTING'else'grant119-consumed.json';other='grant119-consumed.json'if branch['mode']=='EXISTING'else'grant-consumed.json';c=old.read(ROOT/'auth004'/marker)
 need(not(ROOT/'auth004'/other).exists()and q['scope']==EPOCH and q['admission_sha256']==a['spec_sha256']and q['branch_sha256']==H(J(branch))and c['branch_sha256']==q['branch_sha256']and c['consumed_at']==q['consumed_at']and q['expires']<=min(q['consumed_at']+1800,a['expires']),'119_ONE_SESSION_ENVELOPE_PROOF');return True

def pin(p,*,source=False):
 p=Path(p);s=p.lstat();need(stat.S_ISREG(s.st_mode)and s.st_uid==os.getuid()and s.st_nlink==1 and not any(x.is_symlink()for x in(p,*p.parents))and s.st_size<=16777216 and(source or not s.st_mode&0o077),'119_DELTA_CUSTODY')
 h=hashlib.sha256();n=0
 with p.open('rb')as f:
  while block:=f.read(1048576):h.update(block);n+=len(block)
 need(n==s.st_size,'119_DELTA_SHORT');return {'bytes':n,'sha256':h.hexdigest(),'mode':stat.S_IMODE(s.st_mode)}

def collect_delta(source_root):
 archive=ROOT/'source004/preimages004.zip';maps={}
 for p in[ROOT,*sorted(ROOT.rglob('*'))]:
  if p==archive:continue
  need(DIR not in(p,*p.parents),'119_ALREADY_INSTALLED_NO_RETRY');s=p.lstat();need(s.st_uid==os.getuid()and not p.is_symlink()and len(maps)<512,'119_DELTA_NODES')
  maps[str(p)]={'directory':True,'mode':stat.S_IMODE(s.st_mode)}if p.is_dir()else pin(p)
 for p in[STAGE/'actual-initial115.json',STAGE/'actual-recovery115.json',STAGE/'recovery115-tools/install115.py',*(Path(source_root)/n for n in CHANGED_OLD_FILES)]:maps[str(p)]=pin(p,source=Path(source_root)in p.parents)
 need(sum(x.get('bytes',0)for x in maps.values())<=16777216,'119_DELTA_BYTES16M');return maps

def archive_delta(maps,path):
 with zipfile.ZipFile(path,'x',zipfile.ZIP_STORED)as z:
  Path(path).chmod(0o600)
  for n,p in maps.items():
   if p.get('directory'):continue
   with Path(n).open('rb')as src,z.open(n.lstrip('/'),'w')as dst:shutil.copyfileobj(src,dst,1048576)
 need(Path(path).stat().st_size<=16777216,'119_DELTA_ARCHIVE16M')

def restore_delta(path,maps):
 with zipfile.ZipFile(path)as z,tempfile.TemporaryDirectory(prefix='session119-restore-',dir=ROOT.parent)as td:
  files={n:p for n,p in maps.items()if not p.get('directory')};need(z.testzip()is None and set(z.namelist())=={n.lstrip('/')for n in files}and len(z.namelist())==len(files),'119_CRC_MEMBERS')
  for n,p in maps.items():
   rel=Path(n.lstrip('/'));need('..'not in rel.parts,'119_RESTORE_PATH');out=Path(td)/rel
   if p.get('directory'):out.mkdir(parents=True,exist_ok=True);out.chmod(p['mode'])
   else:
    out.parent.mkdir(parents=True,exist_ok=True)
    with z.open(str(rel))as src,out.open('xb')as dst:shutil.copyfileobj(src,dst,1048576);dst.flush();os.fsync(dst.fileno())
    out.chmod(p['mode']);need(pin(out,source=True)==p,'119_ISOLATED_DELTA_READBACK')
 return {'state':'ISOLATED_DELTA_RESTORE_PASS','files':len(files),'nodes':len(maps),'bytes':sum(v['bytes']for v in files.values()),'manifest_sha256':H(J(maps))}

def install(s,b,initial,contract,program,*,source_root=None,now=None):
 now=time.time()if now is None else now;validate_bindings(s,b,now);need(0<=now-b['reservation']['at']<=300,'119_FRESH_PREWRITE_RESERVATION');need(os.environ.get('RENDER')=='true'and os.environ.get('RENDER_GIT_COMMIT')==BASE_COMMIT and os.environ.get('RENDER_EXTERNAL_HOSTNAME')==old.HOST,'119_OLD_INSTANCE')
 source_root=Path.cwd()if source_root is None else Path(source_root);old.source_check(source_root,s['old_source_pins'],runtime_required=source_root==Path.cwd());old_lineage();original_grant(s)
 if source_root==Path.cwd():
  import worker_scope004f as worker
  aggregate=worker.aggregate();need(aggregate['hard_bytes']==536870912 and aggregate['current_bytes']<469762048,'119_ACTUAL_512M_AGGREGATE_MARGIN')
 need(H(program)==s['install_program_sha256']and H(J(initial))==s['initial_sha256']and H(J(contract))==s['contract_sha256']and H(J(contract['policy']))==s['policy_sha256'],'119_INSTALL_PINS')
 need(not DIR.exists()and not(STAGE/'actual-initial119.json').exists()and not(STAGE/'actual-recovery119.json').exists()and not(STAGE/'recovery119-tools').exists(),'119_PARTIAL_OR_APPLIED_NO_RETRY');need(shutil.disk_usage(ROOT.parent).free>=268435456,'119_DELTA_AND_AV_MARGIN256M')
 with allocation_lock():
  unstarted();archive=ROOT/'source004/preimages004.zip';need(old.file_pin(archive)['sha256']==BASE_ARCHIVE_SHA256 and archive.stat().st_size==BASE_ARCHIVE_BYTES,'119_BASE_ARCHIVE_BYTES')
  base_manifest=old.read(ROOT/'source004/preimages004-manifest.json',262144);need(H(J(base_manifest))==BASE_MANIFEST_SHA256,'119_BASE_MANIFEST')
  with zipfile.ZipFile(archive)as z:need(z.testzip()is None and set(z.namelist())=={n.lstrip('/')for n,p in base_manifest.items()if not p.get('directory')},'119_BASE_SEGMENT_CRC_MANIFEST')
  maps=collect_delta(source_root)
  with tempfile.TemporaryDirectory(prefix='.session119-backup-',dir=ROOT.parent)as td:
   backup=Path(td)/'delta119.zip';archive_delta(maps,backup);proof=restore_delta(backup,maps);need(collect_delta(source_root)==maps,'119_PREAPPEND_DRIFT');backup_pin=pin(backup)
   DIR.mkdir(mode=0o700);(STAGE/'recovery119-tools').mkdir(mode=0o700)
   auth={'schema':'traceharbor.session119.authority.v1','spec_sha256':H(J(s)),'effects':effects(),'source_commit':b['published_commit'],'source_tree':b['published_tree'],'expires':b['technical_owner']['expires'],'original_grant_pin':s['original_grant_pin']}
   old.exclusive_copy(DIR/'preimages119.zip',backup);writes={DIR/'preimages119-manifest.json':J(maps),DIR/'extension119.json':J({'spec':s,'bindings':b}),DIR/'authority119.json':J(auth),STAGE/'actual-initial119.json':J(initial),STAGE/'actual-recovery119.json':J(contract),STAGE/'recovery119-tools/install119.py':program}
   for p,data in writes.items():old.exclusive(p,data)
   pins={str(p):{'bytes':len(v),'sha256':H(v)}for p,v in writes.items()};pins[str(DIR/'preimages119.zip')]={k:backup_pin[k]for k in('bytes','sha256')}
   complete={'state':'SESSION119_APPEND_COMPLETE','spec_sha256':H(J(s)),'file_pins':pins,'delta_restore':proof,'base_segment':{'path':str(archive),'bytes':BASE_ARCHIVE_BYTES,'sha256':BASE_ARCHIVE_SHA256,'manifest_sha256':BASE_MANIFEST_SHA256,'accepted_full_restore':OLD_COMPLETE_SHA256,'files':522},'retry':False};old.exclusive(DIR/'complete119.json',complete);original_grant(s);unstarted();need(H(J(bootstrap_readback(s)))==H(J(complete)),'119_COMPLETE_READBACK')
   return {'state':'SESSION119_APPEND8_FILES2_DIRS_VERIFIED_NO_TIMERS','spec_sha256':H(J(s)),'complete_sha256':H(J(complete)),'delta_backup':backup_pin,'restore':proof,'base_segment':complete['base_segment'],'retry':False}

def bootstrap_readback(s):
 v=old.read(DIR/'complete119.json');need(v['state']=='SESSION119_APPEND_COMPLETE'and v['spec_sha256']==H(J(s))and len(v['file_pins'])==7,'119_COMPLETE_REQUIRED')
 expected={DIR/n for n in('preimages119.zip','preimages119-manifest.json','extension119.json','authority119.json')}|{STAGE/'actual-initial119.json',STAGE/'actual-recovery119.json',STAGE/'recovery119-tools/install119.py'};need({Path(n)for n in v['file_pins']}==expected,'119_EXACT_POSTIMAGES')
 for n,p in v['file_pins'].items():
  actual=pin(n);need(all(actual[k]==p[k]for k in('bytes','sha256')),'119_POSTIMAGE_DRIFT')
 need(v['delta_restore']['state']=='ISOLATED_DELTA_RESTORE_PASS'and v['base_segment']['sha256']==BASE_ARCHIVE_SHA256 and v['base_segment']['accepted_full_restore']==OLD_COMPLETE_SHA256,'119_CHAIN_PROOF');return v
