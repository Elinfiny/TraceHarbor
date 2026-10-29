"""Append-only source amendment. No import I/O, new epoch, budget or authority.
The original96 authority, Owner99 and finance205 remain byte-for-byte immutable.
The same file is the inert Native append producer; UNBOUND creates nothing.
"""
import datetime,fcntl,hashlib,io,json,math,os,re,shutil,socket,stat,sys,time,zipfile
from pathlib import Path
J=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
H=lambda b:hashlib.sha256(b).hexdigest()
ROOT=Path('/var/data/traceharbor-recovery96');STAGE=Path('/var/data/traceharbor-staging')
EXT=ROOT/'source100/extension.json';COMPLETE=ROOT/'source100/complete.json';BACKUP=ROOT/'source100/preimages100.zip'
INITIAL=STAGE/'actual-initial100.json';CONTRACT=STAGE/'actual-recovery100.json'
OLD_COMMIT='0d60d8d654c725642746bcd5741692dd12e7cf1b';LIVE_COMMIT='d498fd29e66c88d80f6a4fa28276b00170ccc23c'
OLD_TREE='89fc3c7e434a1fe519699f553a4dff6fae104a31';OLD_CONTRACT='ab9e610fcaf7e78f39aa24619775289dff9917710d8642f238191032e82ded3c'
OLD_A='a2378e24a79c4bda98a8c2cf1a3d91fefd54bd890bbc818e930b365caf99ce68'
OWNER99='dc2fb47ce9b8281ee14219f934895e37f1dac7e06b9c712fe818ffef9bf494f3';REVIEW98='61a0d3486b4a6d5ffdf15e7d65222a28b710cddb3c9da7949f6f1fd419a61017'
FINANCE205='63c252ae7a7c0e532e84bab09b244d3ea32ca60ede5ca096fbadbb0d43b4a394';POLICY='7ad319be56ec43cfdda1c17813fc87d4ff6b407e195e1ba9152b18039335855a'
OLD_INITIAL='2a0d712f9f670667a93a42192fef5a37220d4a239c88a2e3cafe44cfd7647766';DEADLINE=1793379600
REVIEW='ACCEPT_EXACT_STARTUP100_SOURCE_EXTENSION_AND_BOOTSTRAP'
EFFECT='TRACEHARBOR-STARTUP100-APPEND5-DEPLOY7-PRESERVE-OWNER99'
SCOPE='ONLY_SOURCE_STARTUP_DEPLOY7_PRESERVE_UNUSED_OWNER99'
OLD_SEVEN={str(ROOT/'auth96/bootstrap-complete.json'):'11e052f58aca1d4135b092f0ef9560e4696bed68d95298f7b704829a9398aeff',str(ROOT/'auth96/migration.json'):'df0177d02adb608a02a83a79ca0273bf26b19be756a72b77128cfb15e228bcec',str(ROOT/'auth96/preimages96.zip'):'855f7f5668bf8744be2cd44ae32cd68247cb08b27c9a06a59c52d5eea2882cd8',str(ROOT/'recovery-authority96.json'):OLD_A,str(ROOT/'standard-authority89.json'):'117bd1de33746b181ccfff215cf5e09d44ba9634308522d1ac9a99e0bf290f09',str(STAGE/'actual-recovery96.json'):OLD_CONTRACT,str(STAGE/'recovery96-tools/native96.py'):'d14f3ce3e086f4dd65aac0b9b43ca9d56c6d5ba79adb25759b3123a84756aad7'}
def need(ok,code):
 if not ok:raise ValueError(code)
def private(p):
 p=Path(p);s=p.lstat();need(not any(x.is_symlink()for x in(p,*p.parents))and stat.S_ISDIR(s.st_mode)and s.st_uid==os.getuid()and not s.st_mode&0o077,'PRIVATE_DIRECTORY');return p
def raw(p,maximum=33554432,private_file=True):
 p=Path(p);s=p.lstat();need(not any(x.is_symlink()for x in(p,*p.parents))and stat.S_ISREG(s.st_mode)and s.st_uid==os.getuid()and s.st_nlink==1 and s.st_size<=maximum and(not private_file or not s.st_mode&0o077),'PRIVATE_REGULAR_CUSTODY')
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb')as f:
  t=os.fstat(f.fileno());need((s.st_ino,s.st_size,s.st_mtime_ns)==(t.st_ino,t.st_size,t.st_mtime_ns),'READ_DRIFT');return f.read(maximum+1)
def read(p):return json.loads(raw(p,131072))
def stamp(v):
 t=datetime.datetime.fromisoformat(v.replace('Z','+00:00'));need(t.tzinfo is not None,'TIMEZONE_REQUIRED');return t.timestamp()
def owner_scope():
 return {'schema':'traceharbor.startup100.owner.v1','scope':SCOPE,'same_service':'srv-dbh6hgh42hec73c3g9m0','deploy_slot':7,'max_total_deploys':7,'additional_deploys':1,'new_files':5,'new_directories':1,'preserved_owner99_sha256':OWNER99,'preserved_review98_sha256':REVIEW98,'finance205_sha256':FINANCE205,'policy_sha256':POLICY,'new_grants':0,'new_sessions':0,'new_AI_budget':0,'new_observations':0,'new_captures':0,'new_auth_epoch':False,'new_slot004':False,'reset':False,'new_money_terms_permissions':False,'request_sha256':'4ce3b9c3ad74ff1e982e816f677b480064f0f5af9b7a9bc20695f9d8d3d00cf1','same_AUTH96_and_slot003_unstarted_preserved':True}
def verified_extension(e,now):
 need(e.get('schema')=='traceharbor.source-extension100.v1'and e.get('state')=='ACTUAL_APPEND_ONLY_SOURCE_EXTENSION100','ACTUAL_EXTENSION100_REQUIRED')
 s=e.get('spec');o=e.get('technical_owner');r=e.get('independent_review')
 need(all(isinstance(v,dict)for v in(s,o,r))and H(J(s))==e.get('spec_sha256'),'EXACT_EXTENSION_SPEC')
 need(s.get('effect_id')==EFFECT and s.get('Git_base_commit')==OLD_COMMIT and s.get('Git_base_tree')==OLD_TREE and s.get('Native_base_commit')==LIVE_COMMIT and s.get('policy_sha256')==POLICY,'DISTINCT_BASELINES_AND_SAME_POLICY')
 need(s.get('old_seven_sha256')==OLD_SEVEN and s.get('owner99_sha256')==OWNER99 and s.get('review98_sha256')==REVIEW98 and s.get('finance205_sha256')==FINANCE205,'EXACT_PRESERVED99_PROVENANCE')
 need(s.get('new_paths')==[str(INITIAL),str(CONTRACT),str(ROOT/'source100')],'ONLY_FIVE_APPEND_FILES_ONE_DIRECTORY')
 need(o.get('state')=='ACTUAL_OWNER_STARTUP100_DEPLOY7_RECEIVED'and o.get('accepted')is True and o.get('proposed')is False,'NEW_DEPLOY7_OWNER_REQUIRED')
 for k,v in owner_scope().items():need(type(o.get(k))is type(v)and o[k]==v,'DEPLOY7_ONLY_NO_NEW_EFFECT_BUDGET')
 need(bool(o.get('canonical_source'))and re.fullmatch('[a-f0-9]{64}',o.get('actual_message_utf8_sha256',''))and o.get('decision_text_sha256')==s.get('decision_text_sha256'),'ACTUAL_DEPLOY7_MESSAGE_BINDING')
 need(r.get('state')=='ACTUAL_INDEPENDENT_STARTUP100_RELEASE_ACCEPTANCE'and r.get('independent')is True and r.get('proposed')is False and r.get('verdict')==REVIEW and bool(r.get('canonical_source')),'WHOLE_STARTUP100_REVIEW_REQUIRED')
 for k in('candidate_tree','source_contract_sha256','initial_sha256','policy_sha256','decision_text_sha256','bootstrap_program_sha256','baseline_sha256','owner99_sha256','review98_sha256','finance205_sha256'):
  need(r.get(k)==s.get(k),'EXACT_NEW_WHOLE_REVIEW_SOURCE_BINDING')
 need(r.get('spec_sha256')==e['spec_sha256']and H(J(r))==e.get('independent_review_sha256')and H(J(o))==e.get('technical_owner_sha256'),'NEW_EXTENSION_RECEIPT_HASHES')
 need(type(e.get('source_commit'))is str and re.fullmatch('[a-f0-9]{40}',e['source_commit'])and e['source_commit']not in(OLD_COMMIT,LIVE_COMMIT),'DISTINCT_NEW_SOURCE_COMMIT')
 need(type(e.get('expires'))in(int,float)and math.isfinite(e['expires'])and now<e['expires']<=DEADLINE and e['expires']==o.get('expires'),'SOURCE_EXTENSION_EXPIRED')
 z=e.get('append_reservation');need(isinstance(z,dict)and H(J(z))==e.get('append_reservation_sha256')and z.get('state')=='RESERVED_NOT_DISPATCHED'and z.get('effect_id')==EFFECT and z.get('max_dispatches')==1 and z.get('dispatch_count')==0 and z.get('spec_sha256')==e['spec_sha256']and z.get('technical_owner_sha256')==e['technical_owner_sha256']and z.get('review_sha256')==e['independent_review_sha256']and bool(z.get('canonical_source'))and type(e.get('bound_at'))in(int,float)and 0<=e['bound_at']-stamp(z['reserved_at_utc'])<=300 and e['bound_at']<=now,'EXACT_ORIGINAL_APPEND_RESERVATION_BINDING')
 return s

def bound_extension(s,b,now):
 need(b.get('state')=='BOUND_FROM_ACTUAL_STARTUP100_RECEIPTS','UNBOUND_NO_EXECUTION')
 e={'schema':'traceharbor.source-extension100.v1','state':'ACTUAL_APPEND_ONLY_SOURCE_EXTENSION100','spec':s,'spec_sha256':H(J(s)),'source_commit':b.get('published_source_commit'),'technical_owner':b.get('technical_owner'),'technical_owner_sha256':H(J(b.get('technical_owner'))),'independent_review':b.get('review'),'independent_review_sha256':H(J(b.get('review'))),'expires':(b.get('technical_owner')or{}).get('expires')}
 z=b.get('reservation');need(isinstance(z,dict)and z.get('state')=='RESERVED_NOT_DISPATCHED'and z.get('effect_id')==EFFECT and z.get('max_dispatches')==1 and z.get('dispatch_count')==0 and z.get('spec_sha256')==e['spec_sha256']and z.get('technical_owner_sha256')==e['technical_owner_sha256']and z.get('review_sha256')==e['independent_review_sha256']and bool(z.get('canonical_source'))and type(b.get('bound_at'))in(int,float)and 0<=b['bound_at']-stamp(z['reserved_at_utc'])<=300 and b['bound_at']<=now,'EXACT_ONE_APPEND_RESERVATION')
 e['append_reservation']=z;e['append_reservation_sha256']=H(J(z));e['bound_at']=b.get('bound_at');verified_extension(e,now);need(len(J(e))<=131072,'EXTENSION_BOUND');return e

def preserved():
 import recovery_forward96
 recovery_forward96.preserved()
 for n,h in OLD_SEVEN.items():need(H(raw(n))==h,'APPLIED96_POSTIMAGE_DRIFT')
 need(H(J(read(STAGE/'actual-admission146.json')))==OLD_INITIAL,'ORIGINAL146_MUST_REMAIN_IMMUTABLE')

def authorize(m,a):
 import render_recorded_release70 as launch,release_integration68 as integration,worker_scope67 as worker
 need(H(J(a))==OLD_A and a['source_commit']==OLD_COMMIT and a['candidate_tree']==OLD_TREE and a['source_contract_sha256']==OLD_CONTRACT and a['technical_owner_sha256']==OWNER99 and a['independent_review_sha256']==REVIEW98,'ORIGINAL96_AUTHORITY_IMMUTABLE')
 e=read(EXT);s=verified_extension(e,m.clock());preserved()
 need(worker.identity()['source_commit']==e['source_commit'],'ACTUAL_NEW_SOURCE_IDENTITY_REQUIRED')
 need(H(J(m.p))==POLICY and launch.ADMISSION_PATH==INITIAL and launch.CREDIT67_PATH==CONTRACT and launch.ADMISSION_SHA256==s['initial_sha256']and launch.CREDIT67_SHA256==s['source_contract_sha256'],'NEW_INITIAL_AND_CONTRACT_BINDING')
 need(H(raw(INITIAL))==s['initial_sha256']and H(raw(CONTRACT))==s['source_contract_sha256'],'NEW_PRIVATE_APPEND_PINS')
 integration.checked_manifest(Path(__file__).parent,s['candidate_source_pins'])
 need(H(raw(Path(__file__),private_file=False))==s['bootstrap_program_sha256'],'EXACT_SOURCE_EXTENSION_PROGRAM')
 complete=read(COMPLETE);need(complete=={'state':'STARTUP100_APPEND_COMPLETE','extension_sha256':H(J(e)),'spec_sha256':H(J(s)),'initial_sha256':s['initial_sha256'],'contract_sha256':s['source_contract_sha256'],'backup_sha256':complete.get('backup_sha256'),'program_sha256':s['bootstrap_program_sha256']},'PARTIAL_EXTENSION100_CLOSED')
 need(H(raw(BACKUP))==complete['backup_sha256'],'PRIVATE_SOURCE100_BACKUP_REQUIRED')
 return a

def snapshot(root):
 out={};root=Path(root)
 for p in sorted(root.rglob('*')):
  q=p.lstat();need(not p.is_symlink()and q.st_uid==os.getuid(),'PRIVATE_SNAPSHOT_CUSTODY')
  out[str(p.relative_to(root))]={'directory':True,'mode':stat.S_IMODE(q.st_mode)}if p.is_dir()else{'bytes':q.st_size,'sha256':H(raw(p)),'mode':stat.S_IMODE(q.st_mode)}
 return out

def verify_preimages(s):
 # Standalone on the actual old LIVE source; never equate it with Git HEAD.
 for n,h in s['old_seven_sha256'].items():need(H(raw(n))==h,'APPLIED96_POSTIMAGE_DRIFT')
 need(H(J(snapshot(s['old95_root'])) )==s['old95_tree_sha256'],'WHOLE95_DRIFT')
 need(H(J(snapshot(s['allocation'])) )==s['allocation_tree_sha256'],'CONSUMED001002_DRIFT')
 need(H(J(read(STAGE/'actual-admission146.json')))==OLD_INITIAL,'ORIGINAL146_DRIFT')
 need(snapshot(ROOT)==s['root96_snapshot'],'UNUSED_OWNER99_STATE_DRIFT')
 for n,h in s['private_pins'].items():need(H(raw(n))==h,'PRIVATE_PREIMAGE_DRIFT')
 for rel,pin in s['parent_pins'].items():
  root=Path('/var/data/traceharbor-release68')if rel.startswith('original/')else Path('/var/data/traceharbor-recovery86');b=raw(root/rel.split('/',1)[1]);need(len(b)==pin['bytes']and H(b)==pin['sha256'],'PARENT27_DRIFT')
 for rel,h in s['asset_pins'].items():need(H(raw(Path(s['assets_root'])/rel))==h,'ASSET3_DRIFT')

def preflight(s):
 need(os.environ.get('RENDER')=='true'and os.environ.get('RENDER_EXTERNAL_HOSTNAME')=='traceharbor.onrender.com'and os.environ.get('RENDER_GIT_COMMIT')==s['Native_base_commit']and socket.gethostname()==s['Native_base_instance'],'ACTUAL_LIVE_BASELINE_REQUIRED_NOT_GIT_HEAD')
 need(Path('/sys/fs/cgroup/cpu.max').read_text().split()==['50000','100000']and Path('/sys/fs/cgroup/memory.max').read_text().strip()=='536870912','SAME_RESOURCE_PLAN_REQUIRED')
 private(ROOT);private(STAGE);need(stat.S_IMODE(ROOT.stat().st_mode)==s['root96_mode'],'ROOT96_MODE_DRIFT');verify_preimages(s)
 for n,pin in s['live_source_pins'].items():
  b=raw(Path.cwd()/n,private_file=False);need(len(b)==pin['bytes']and H(b)==pin['sha256'],'LIVE_D498_SOURCE_DRIFT')
 need(all(not Path(p).exists()for p in s['new_paths']),'SOURCE100_APPEND_ALREADY_ATTEMPTED_NO_RETRY')
 need(shutil.disk_usage(ROOT).free>=167772160+33554432,'BACKUP_CAPTURE_DISK_MARGIN')

def backup_bytes(s):
 items={}
 for n in s['live_source_pins']:items[str(Path.cwd()/n).lstrip('/')]=raw(Path.cwd()/n,private_file=False)
 for n in [*OLD_SEVEN,str(STAGE/'actual-admission146.json')]:items[n.lstrip('/')]=raw(n)
 out=io.BytesIO()
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=1)as z:
  for n,b in sorted(items.items()):
   i=zipfile.ZipInfo(n,(2026,10,29,0,0,0));i.external_attr=(stat.S_IFREG|0o600)<<16;i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,b)
 b=out.getvalue();need(len(b)<=33554432,'PRIVATE_BACKUP32MiB_BOUND');return b

def add(p,b):
 p=Path(p);private(p.parent);fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'wb')as f:f.write(b);f.flush();os.fsync(f.fileno())
 fd=os.open(p.parent,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
 need(raw(p)==b,'APPEND_READBACK_UNKNOWN_NO_RETRY')

def bootstrap(envelope,mode='append'):
 s=envelope['spec'];need(H(J(s))==PINNED_SPEC_SHA256,'PINNED_SPEC_REQUIRED')
 e=bound_extension(s,envelope['bindings'],time.time());initial=J(envelope['initial']);contract=J(envelope['contract'])
 need(H(initial)==s['initial_sha256']and H(contract)==s['source_contract_sha256'],'EXACT_NEW_APPEND_POSTIMAGES')
 values=[(INITIAL,initial),(CONTRACT,contract),(EXT,J(e))]
 if mode=='readback':
  c=read(COMPLETE);need(c.get('state')=='STARTUP100_APPEND_COMPLETE'and c.get('extension_sha256')==H(J(e))and c.get('spec_sha256')==H(J(s))and c.get('initial_sha256')==H(initial)and c.get('contract_sha256')==H(contract)and c.get('program_sha256')==s['bootstrap_program_sha256']and H(raw(BACKUP))==c.get('backup_sha256'),'SOURCE100_COMPLETE_READBACK')
  for p,b in values:need(raw(p)==b,'SOURCE100_POSTIMAGE_READBACK')
  # Check only old fixed preimages after append, not the old empty root listing.
  for n,h in OLD_SEVEN.items():need(H(raw(n))==h,'APPLIED96_POSTIMAGE_DRIFT')
  print(json.dumps({'state':'STARTUP100_FIVE_APPEND_READBACK_PASS','backup_sha256':c['backup_sha256'],'extension_sha256':H(J(e)),'retry':False},sort_keys=True));return
 need(mode=='append','EXACT_APPEND_MODE');need(0<=time.time()-e['bound_at']<=300,'FRESH_ONE_APPEND_RESERVATION');fd=os.open(s['allocation']+'/lock',os.O_RDONLY|os.O_NOFOLLOW)
 try:
  fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB);preflight(s);backup=backup_bytes(s);verify_preimages(s);need(time.time()<e['expires'],'OWNER_EXTENSION_EXPIRED')
  (ROOT/'source100').mkdir(mode=0o700);add(BACKUP,backup)
  for p,b in values:add(p,b)
  c={'state':'STARTUP100_APPEND_COMPLETE','extension_sha256':H(J(e)),'spec_sha256':H(J(s)),'initial_sha256':H(initial),'contract_sha256':H(contract),'backup_sha256':H(backup),'program_sha256':s['bootstrap_program_sha256']};add(COMPLETE,J(c))
  for n,h in OLD_SEVEN.items():need(H(raw(n))==h,'APPLIED96_POSTIMAGE_DRIFT')
  print(json.dumps({'state':'STARTUP100_APPEND_COMPLETE_NO_DEPLOY_OR_EFFECTS','backup_sha256':H(backup),'extension_sha256':H(J(e)),'retry':False},sort_keys=True))
 finally:os.close(fd)
def main(mode='append'):
 rawdata=sys.stdin.buffer.read(524289);need(0<len(rawdata)<=524288,'ENVELOPE_BOUND');bootstrap(json.loads(rawdata),mode)
