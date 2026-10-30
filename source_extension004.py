"""Recovery004 immutable-source binding and append-only bootstrap.
Import performs no I/O. Old scopes never receive writes or rollback.
"""
import datetime,fcntl,hashlib,io,json,math,os,re,shutil,socket,stat,tempfile,time,zipfile,sys
from pathlib import Path
ROOT=Path('/var/data/traceharbor-recovery004');STAGE=Path('/var/data/traceharbor-staging')
ROOTS=tuple(Path('/var/data/'+n)for n in('traceharbor-release68','traceharbor-recovery86','traceharbor-recovery67','traceharbor-recovery96'))
BASE_COMMIT='8e8bcf9fcc280151f17025cbf36648e2e8c97972';BASE_TREE='3000b40c18d82fd4679b702ebc779f7002be71a4'
SERVICE='srv-dbh6hgh42hec73c3g9m0';HOST='traceharbor.onrender.com';DEADLINE=1793379600
REQUEST='f80d6d38d3b87b0c93362fb435dd0c4eb7769f64972ddefe35a2fbab9abf9c1b'
FINANCE='63c252ae7a7c0e532e84bab09b244d3ea32ca60ede5ca096fbadbb0d43b4a394'
HOST_RUNTIME_PROFILE={'tree_sha256': 'ecf648782ae45b0c13f8e407125410f7798e60c3dcc407c3a0fefc4b192c3860', 'members': 512, 'files': 449, 'bytes': 5801292, 'python_version': '3.12.14', 'relative_root': '.venv', 'pyvenv_cfg_sha256': '05b96b2c4710a2287e8d35fbddb4bac26494592c81758b2c40351ac9b260f033'}
SOURCE_AMENDMENT={'parent_spec_sha256': 'a1b13ab6f110bc7f2c53c86845b68952461963036eb88237174286569f733f71', 'owner110_sha256': '35ba306dd1743f0589564da0f76c4928f737b25af530966ea9ac472c0f2841bf', 'review109_sha256': '2327f18f8711d1849072e6f7d82089fb009e2fce8dc9ad4be010fa664ba56283', 'predecessor356_sha256': '7a5c13635881f002d2e4a4d1e2cacc63f088b60e390f936b6a1b083b5f9d441b', 'runtime_profile': {'tree_sha256': 'ecf648782ae45b0c13f8e407125410f7798e60c3dcc407c3a0fefc4b192c3860', 'members': 512, 'files': 449, 'bytes': 5801292, 'python_version': '3.12.14', 'relative_root': '.venv', 'pyvenv_cfg_sha256': '05b96b2c4710a2287e8d35fbddb4bac26494592c81758b2c40351ac9b260f033'}, 'old_source_pins_sha256': '50fe05e5fc31f95bd55ca3890c54bf1dfea3f1e43f76915e65b6fea9f12be267', 'history_sha256': '5a96ec5e8abcaa9f81a1256ec964448cb658b9a40cc68a9293876ebaab18d70b', 'policy_sha256': 'd6f7d66428aa9cdfc1cc509d32ea907ad5a001d1bce96325d8e6c1063d4c1575', 'decision_sha256': 'dca8867edea7b45da15307d6bd6419b198614c76bd5b45348ed39d5b6cf0a4e2', 'kind': 'SOURCE_RUNTIME_BOUNDARY_ONLY', 'max_replacement_pre_effect_dispatches': 1, 'old_dispatch_count_retained': 1, 'same_owner110_effects': True, 'no_financial205_reapproval': True}
J=lambda v:json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
H=lambda b:hashlib.sha256(b).hexdigest()
class Closed(ValueError):pass
def need(v,code):
 if not v:raise Closed(code)
def private(p):
 p=Path(p);s=p.lstat();need(stat.S_ISDIR(s.st_mode)and s.st_uid==os.getuid()and not s.st_mode&0o077 and not any(x.is_symlink()for x in(p,*p.parents)),'PRIVATE_DIRECTORY');return p

def raw(p,maximum=33554432,*,private_file=True):
 p=Path(p);s=p.lstat();need(stat.S_ISREG(s.st_mode)and s.st_uid==os.getuid()and s.st_nlink==1 and s.st_size<=maximum and(not private_file or not s.st_mode&0o077)and not any(x.is_symlink()for x in(p,*p.parents)),'PRIVATE_FILE_CUSTODY')
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb')as f:
  t=os.fstat(f.fileno());need((s.st_ino,s.st_size,s.st_mtime_ns)==(t.st_ino,t.st_size,t.st_mtime_ns),'FILE_CHANGED_DURING_READ');b=f.read(maximum+1)
 need(len(b)==s.st_size,'SHORT_FILE');return b

def read(p,maximum=262144):return json.loads(raw(p,maximum))
def exclusive(p,b):
 p=Path(p);private(p.parent);b=b if type(b)is bytes else J(b);fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'wb')as f:f.write(b);f.flush();os.fsync(f.fileno())
 need(raw(p,max(len(b),1))==b,'WRITE_READBACK_UNKNOWN');fd=os.open(p.parent,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)

def snapshot(root,*,allow004=False):
 root=Path(root);private(root);v={};total=0
 excluded={str(ROOTS[0]/'allocation'/n)for n in('slot-004.json','terminal-004.json')}if allow004 and root==ROOTS[0]else set()
 for p in [root,*sorted(root.rglob('*'))]:
  if str(p)in excluded:continue
  s=p.lstat();need(not p.is_symlink()and s.st_uid==os.getuid(),'HISTORY_CUSTODY');need(len(v)<4096,'HISTORY_MEMBER_BOUND')
  if stat.S_ISDIR(s.st_mode):v[str(p)]={'directory':True,'mode':stat.S_IMODE(s.st_mode)}
  else:
   b=raw(p);total+=len(b);need(total<=67108864,'HISTORY_BYTES_BOUND');v[str(p)]={'bytes':len(b),'sha256':H(b),'mode':stat.S_IMODE(s.st_mode)}
 return v

def check_critical(pins):
 need(type(pins)is dict and len(pins)<=128,'CRITICAL_PIN_SHAPE')
 for name,pin in pins.items():
  p=Path(name);need(any(r in p.parents for r in ROOTS),'CRITICAL_PATH')
  if pin.get('exists')is False:need(not p.exists(),'PRESERVED_ABSENCE_CHANGED');continue
  b=raw(p);need(len(b)==pin['bytes']and H(b)==pin['sha256'],'CONSUMED_PREIMAGE_DRIFT')

def check_history(history):
 need(set(history['root_preimages'])==set(map(str,ROOTS)),'WHOLE_FOUR_ROOTS_REQUIRED');maps={}
 for root in ROOTS:
  v=snapshot(root,allow004=True);pin=history['root_preimages'][str(root)];need(H(J(v))==pin['tree_sha256']and len(v)==pin['members']and sum(x.get('bytes',0)for x in v.values())==pin['bytes'],'WHOLE_CONSUMED_ROOT_DRIFT');maps.update(v)
 stages=history['stage_preimages'];expected={Path(n).name for n in stages}
 need(all(Path(n).parent==STAGE and Path(n).name.startswith('actual-')and Path(n).suffix=='.json'for n in stages),'STAGE_PREIMAGE_PATH')
 need({p.name for p in STAGE.glob('actual-*.json')}<=expected|{'actual-initial004.json','actual-recovery004.json'},'UNEXPECTED_STAGING_ADMISSION')
 for n,pin in stages.items():
  b=raw(n,131072);s=Path(n).lstat();actual={'bytes':len(b),'sha256':H(b),'mode':stat.S_IMODE(s.st_mode)};need(actual==pin,'OLD_STAGING_DRIFT');maps[n]=actual
 return maps


def runtime_profile(directory):
 root=Path(directory)/'.venv';need(root.is_dir()and not root.is_symlink(),'EXACT_RENDER_RUNTIME_DIRECTORY');items={};total=0
 for p in [root,*sorted(root.rglob('*'))]:
  if '__pycache__'in p.parts:continue
  s=p.lstat();need(s.st_uid==os.getuid()and len(items)<1024,'RUNTIME_CUSTODY_OR_BOUND');name=str(p.relative_to(root))
  if stat.S_ISLNK(s.st_mode):items[name]={'symlink':os.readlink(p),'mode':stat.S_IMODE(s.st_mode)}
  elif stat.S_ISDIR(s.st_mode):items[name]={'directory':True,'mode':stat.S_IMODE(s.st_mode)}
  elif stat.S_ISREG(s.st_mode):
   b=raw(p,33554432,private_file=False);total+=len(b);need(total<=8388608,'RUNTIME_TOTAL_BYTES');items[name]={'bytes':len(b),'sha256':H(b),'mode':stat.S_IMODE(s.st_mode)}
  else:raise Closed('RUNTIME_SPECIAL_NODE')
 return {'tree_sha256':H(J(items)),'members':len(items),'files':sum('sha256'in x for x in items.values()),'bytes':total,'python_version':'3.12.14','relative_root':'.venv','pyvenv_cfg_sha256':H(raw(root/'pyvenv.cfg',4096,private_file=False))}

def source_check(directory,pins,*,runtime_required=False):
 directory=Path(directory);need(type(pins)is dict and 77<=len(pins)<=128,'SOURCE_CLOSURE_BOUND')
 runtime=directory/'.venv'
 if runtime.exists()or runtime.is_symlink():need(runtime_profile(directory)==HOST_RUNTIME_PROFILE,'PINNED_RENDER_RUNTIME_DRIFT')
 else:need(not runtime_required,'RENDER_RUNTIME_REQUIRED')
 if runtime_required:need(sys.version.split()[0]=='3.12.14'and Path(sys.prefix)==runtime,'EXACT_RENDER_INTERPRETER')
 # Only a successfully hash-verified whole runtime subtree is classified outside
 # Git product source. No unverified prefix, broad ignore or tracked file skip.
 actual={str(p.relative_to(directory))for p in directory.rglob('*')if p.is_file()and '__pycache__'not in p.parts and '.git'not in p.parts and '.venv'not in p.relative_to(directory).parts[:1]}
 need(actual==set(pins),'EXACT_SOURCE_FILESET')
 for name,pin in pins.items():
  rel=Path(name);need(not rel.is_absolute()and '..'not in rel.parts and rel.parts[0]!='.venv','SOURCE_PATH')
  b=raw(directory/rel,1048576,private_file=False);need(len(b)==pin['bytes']and H(b)==pin['sha256'],'SOURCE_CLOSURE_DRIFT')


def effects():
 return {'same_service':SERVICE,'deploy_ordinal':9,'max_additional_deploys':1,'new_root':str(ROOT),'new_auth_epoch':'TRACEHARBOR-AUTH004','new_grants':1,'new_sessions':1,'session_seconds_max':1800,'new_targets':1,'new_selections':1,'new_native_samples':1,'new_full_recordings':1,'new_AI_max':1,'new_allocation_slot':4,'required_prior_slots':3,'HELD_before':253,'HELD_after':252,'total_call_limit':256,'new_observations':1,'global_observation':5,'local_observation':1,'bootstrap_files':8,'bootstrap_directories':4,'new_allocation':False,'reset':False,'retry':False,'financial205_reapproval':False,'planned_total_USD':'20','call_gross_cap_USD':'0.002','tax_multiplier':'2','provider_global_hardcap':False,'new_money_terms_permissions':False,'AI_after_initial_FULLACK':True,'full_seconds':224,'AV_seconds':176,'new_AV_renders':1,'same_Devpost_entry':'1264455','final_legal_distinct':True,'native_Share_distinct':True}

def validate_spec(s):
 need(s.get('schema')=='traceharbor.recovery004.spec.v1'and s.get('base_commit')==BASE_COMMIT and s.get('base_tree')==BASE_TREE,'SOURCE004_BASE')
 need(type(s.get('effects'))is dict and all(type(s['effects'].get(k))is type(v)for k,v in effects().items())and s.get('effects')==effects()and s.get('request_sha256')==REQUEST and s.get('request_bytes')==5633,'EXACT004_EFFECT_CAPS')
 need(s.get('counter')=={'count':1607,'request_sha256':REQUEST,'template_sha256':'17dc9cd8a6b70ec56bc2b758f9539a113ba789b5b025105234ae3aed78a5f49d','tokenizer_revision':'a9904d24bcc1d289a1950fa9d2b978c47cf903b9'},'ACCEPTED343_COUNTER')
 need(s.get('finance205_sha256')==FINANCE and re.fullmatch('[a-f0-9]{40}',s.get('candidate_tree','')),'SPEC_FINANCE_TREE')
 for k in('decision_sha256','contract_sha256','policy_sha256','initial_sha256','install_program_sha256','source_manifest_sha256','history_sha256'):
  need(re.fullmatch('[a-f0-9]{64}',s.get(k,'')),'SPEC_PIN')
 need(s.get('source_amendment')==SOURCE_AMENDMENT and H(J(s['old_source_pins']))==SOURCE_AMENDMENT['old_source_pins_sha256']and all(s[k]==SOURCE_AMENDMENT[k]for k in('history_sha256','policy_sha256','decision_sha256')),'EXACT_SOURCE_ONLY_AMENDMENT')
 need(H(J(s['source_pins']))==s['source_manifest_sha256']and H(J(s['history']))==s['history_sha256'],'SPEC_MANIFEST_HISTORY_PIN')
 return s

def validate_bindings(s,b,now):
 validate_spec(s);need(b.get('state')=='BOUND_FROM_ACTUAL_RECOVERY004_RECEIPTS','UNBOUND004_NO_EFFECT')
 o=b.get('technical_owner',{});r=b.get('independent_review',{});f=b.get('finance205',{});a=b.get('source_amendment_review',{})
 need(H(J(o))==SOURCE_AMENDMENT['owner110_sha256']and o.get('state')=='ACTUAL_OWNER_RECOVERY004_COMBINED'and o.get('accepted')is True and o.get('proposed')is False,'IMMUTABLE_ACTUAL_OWNER110_REQUIRED')
 need(H(J(r))==SOURCE_AMENDMENT['review109_sha256']and r.get('state')=='ACTUAL_INDEPENDENT_COMPLETE_RECOVERY004_ACCEPTANCE'and r.get('independent')is True and r.get('proposed')is False,'IMMUTABLE_INDEPENDENT109_REQUIRED')
 need(o.get('spec_sha256')==r.get('spec_sha256')==SOURCE_AMENDMENT['parent_spec_sha256'],'ORIGINAL109_110_SPEC_PRESERVED')
 need(H(J(f))==FINANCE and f.get('state')=='ACTUAL_INFORMED_STANDARD89_OWNER_RECEIVED'and f.get('accepted')is True and f.get('proposed')is False,'FINANCE205_PRESERVED')
 need(a.get('state')=='ACTUAL_INDEPENDENT_RECOVERY004_SOURCE_AMENDMENT_ACCEPTANCE'and a.get('accepted')is True and a.get('independent')is True and a.get('proposed')is False and a.get('verdict')=='ACCEPT_SOURCE_RUNTIME004_WITH_ONE_PRE_EFFECT_REPLACEMENT','ACTUAL_SOURCE_AMENDMENT_REVIEW_REQUIRED')
 need(bool(a.get('canonical_source'))and a.get('spec_sha256')==H(J(s)),'ACTUAL_AMENDMENT_CANONICAL_SPEC')
 for k in('candidate_tree','decision_sha256','contract_sha256','policy_sha256','initial_sha256','install_program_sha256','source_manifest_sha256','history_sha256'):
  need(a.get(k)==s[k],'WHOLE_AMENDED004_RECEIPT_PIN')
 need(a.get('source_amendment')==SOURCE_AMENDMENT and a.get('effects')==o.get('effects')==effects()and a.get('owner110_sha256')==H(J(o))and a.get('review109_sha256')==H(J(r))and a.get('finance205_sha256')==FINANCE,'UNCHANGED_OWNER110_EFFECT_SCOPE')
 need(H(J(b.get('predecessor_bootstrap',{})))==SOURCE_AMENDMENT['predecessor356_sha256'],'ORIGINAL_FAILED_DISPATCH_PRESERVED')
 need(type(o.get('expires'))in(int,float)and math.isfinite(o['expires'])and now<o['expires']<=DEADLINE,'004_AUTHORITY_EXPIRED')
 need(re.fullmatch('[a-f0-9]{40}',b.get('published_commit',''))and b['published_commit']!=BASE_COMMIT and b.get('published_tree')==s['candidate_tree'],'ACTUAL_NEW_SOURCE004_PUBLICATION')
 z=b.get('reservation',{});need(z.get('effect_id')=='RECOVERY004-SOURCEFIX356-APPEND8-DEPLOY9-ONCE'and z.get('state')=='RESERVED_NOT_DISPATCHED'and z.get('max_dispatches')==1 and z.get('dispatch_count')==0 and z.get('spec_sha256')==H(J(s))and z.get('owner_sha256')==H(J(o))and z.get('review_sha256')==H(J(a))and z.get('predecessor356_sha256')==SOURCE_AMENDMENT['predecessor356_sha256']and bool(z.get('canonical_source')),'EXACT_SOURCEFIX004_DISTINCT_RESERVATION')
 need(type(z.get('at'))in(int,float)and 0<=now-z['at']and z['at']<=o['expires'],'004_RESERVATION_TIME')
 return o

def backup(maps):
 out=io.BytesIO()
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)as z:
  for n,pin in maps.items():
   if pin.get('directory'):continue
   b=raw(n);need(H(b)==pin['sha256'],'BACKUP_PREIMAGE_DRIFT');z.writestr(n.lstrip('/'),b)
 b=out.getvalue();need(len(b)<=67108864,'BACKUP_SIZE');return b

def restore_proof(blob,maps):
 z=zipfile.ZipFile(io.BytesIO(blob));need(z.testzip()is None,'BACKUP_CRC')
 files={n:p for n,p in maps.items()if not p.get('directory')};need(set(z.namelist())=={n.lstrip('/')for n in files},'BACKUP_COMPLETE_MANIFEST')
 with tempfile.TemporaryDirectory(prefix='traceharbor004-restore-')as td:
  base=Path(td)
  for n,pin in maps.items():
   rel=Path(n.lstrip('/'));need('..'not in rel.parts and not rel.is_absolute(),'BACKUP_PATH');p=base/rel
   if pin.get('directory'):p.mkdir(parents=True,exist_ok=True);p.chmod(pin['mode'])
   else:
    p.parent.mkdir(parents=True,exist_ok=True);b=z.read(str(rel));need(len(b)==pin['bytes']and H(b)==pin['sha256'],'BACKUP_HASH');fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,pin['mode'])
    with os.fdopen(fd,'wb')as f:f.write(b)
    need(H(p.read_bytes())==pin['sha256']and stat.S_IMODE(p.stat().st_mode)==pin['mode'],'ISOLATED_RESTORE_READBACK')
 return {'state':'ISOLATED_RESTORE_PASS_NO_LIVE_RESTORE','members':len(files),'tree_sha256':H(J(maps))}

def install(s,b,initial,contract,program,*,source_root=None,now=None):
 now=time.time()if now is None else now;validate_bindings(s,b,now)
 need(0<=now-b['reservation']['at']<=300,'FRESH004_PREWRITE_RESERVATION')
 need(os.environ.get('RENDER')=='true'and os.environ.get('RENDER_EXTERNAL_HOSTNAME')==HOST and os.environ.get('RENDER_GIT_COMMIT')==BASE_COMMIT,'EXACT_OLD_NATIVE_SOURCE004')
 source_check(source_root or Path.cwd(),s['old_source_pins'],runtime_required=source_root is None)
 need(H(program)==s['install_program_sha256']and H(J(initial))==s['initial_sha256']and H(J(contract))==s['contract_sha256']and H(J(contract['policy']))==s['policy_sha256'],'BOOTSTRAP004_PAYLOAD_PINS')
 need(not ROOT.exists()and not(STAGE/'actual-initial004.json').exists()and not(STAGE/'actual-recovery004.json').exists()and not(STAGE/'recovery004-tools').exists(),'004_PARTIAL_OR_USED_NO_RETRY')
 need(shutil.disk_usage(ROOT.parent).free>=268435456,'004_BACKUP_AND_AV_DISK_MARGIN')
 lock=os.open(ROOTS[0]/'allocation/lock',os.O_RDONLY|os.O_NOFOLLOW)
 try:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  allocation=ROOTS[0]/'allocation'
  need({p.name for p in allocation.glob('slot-*.json')}=={'slot-001.json','slot-002.json','slot-003.json'}and not(allocation/'terminal-004.json').exists(),'EXPECTED3_NO_SLOT004_BEFORE_BOOTSTRAP')
  maps=check_history(s['history']);blob=backup(maps);proof=restore_proof(blob,maps)
  need(check_history(s['history'])==maps,'004_PREAPPEND_DRIFT');ROOT.mkdir(mode=0o700);(ROOT/'source004').mkdir(mode=0o700);(ROOT/'auth004').mkdir(mode=0o700);(STAGE/'recovery004-tools').mkdir(mode=0o700)
  extension={'spec':s,'bindings':b};authority={'schema':'traceharbor.authority004.v1','scope':'TRACEHARBOR-AUTH004','effects':effects(),'spec_sha256':H(J(s)),'source_commit':b['published_commit'],'source_tree':b['published_tree'],'policy_sha256':s['policy_sha256'],'finance205_sha256':FINANCE,'expires':b['technical_owner']['expires']}
  writes={ROOT/'source004/preimages004.zip':blob,ROOT/'source004/preimages004-manifest.json':J(maps),ROOT/'source004/extension004.json':J(extension),ROOT/'recovery-authority004.json':J(authority),STAGE/'actual-initial004.json':J(initial),STAGE/'actual-recovery004.json':J(contract),STAGE/'recovery004-tools/install004.py':program}
  for p,data in writes.items():exclusive(p,data)
  complete={'state':'RECOVERY004_APPEND8_COMPLETE','spec_sha256':H(J(s)),'file_pins':{str(p):{'bytes':len(v),'sha256':H(v)}for p,v in writes.items()},'restore_proof':proof,'old_history_sha256':s['history_sha256'],'retry':False}
  exclusive(ROOT/'source004/bootstrap-complete.json',complete);need(check_history(s['history'])==maps,'OLD_HISTORY_POSTAPPEND_DRIFT')
  return {'state':'APPENDED8FILES4DIRS_VERIFIED_NO_DEPLOY_OR_TIMERS','spec_sha256':H(J(s)),'backup_sha256':H(blob),'restore_proof':proof}
 finally:os.close(lock)

def bootstrap_readback(s):
 complete=read(ROOT/'source004/bootstrap-complete.json');need(complete.get('state')=='RECOVERY004_APPEND8_COMPLETE'and complete.get('spec_sha256')==H(J(s))and complete.get('old_history_sha256')==s['history_sha256'],'004_PARTIAL_BOOTSTRAP')
 need(len(complete.get('file_pins',{}))==7,'004_SEVEN_POSTIMAGES_REQUIRED')
 for name,pin in complete['file_pins'].items():
  need(Path(name)in{ROOT/'source004'/n for n in('preimages004.zip','preimages004-manifest.json','extension004.json')}|{ROOT/'recovery-authority004.json',STAGE/'actual-initial004.json',STAGE/'actual-recovery004.json',STAGE/'recovery004-tools/install004.py'},'004_POSTIMAGE_PATH')
  data=raw(name,67108864);need(len(data)==pin['bytes']and H(data)==pin['sha256'],'004_BOOTSTRAP_POSTIMAGE_DRIFT')
 need(complete['restore_proof']['state']=='ISOLATED_RESTORE_PASS_NO_LIVE_RESTORE','004_RESTORE_PROOF_REQUIRED');return complete
