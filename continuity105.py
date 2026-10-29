"""Prospective bounded credential replacement. Inert until exact private release.
Old AUTH96 files/history never overwritten; same logical scope, same effect budget.
A replacement credential is explicitly a NEW protected effect, not unused grant99.
"""
import hashlib,json,math,os,re,stat,time
from pathlib import Path
from quota_ledger import read,exclusive,private_dir
from release_policy import digest,Refusal
ROOT=Path('/var/data/traceharbor-recovery96');BASE=ROOT/'continuity105';OP=BASE/'operator'
OLD_SESSION_SHA='c857e95bf16dd0da1c38beaa5b677bdfd1056dbcaba7a85f66c7d25f2f35034a'
OLD_EXT_SHA='bc41ce42f45890a7cbaca5cf75535649159faf52b3e0f72ec6c9cb81c5d8a0d0'
DEADLINE=1793379600

def need(v,c):
 if not v:raise Refusal(c)
def scope():return {'new_deploys':1,'deploy_ordinal':8,'replacement_grants':1,'replacement_sessions':1,'new_auth_epochs':0,'global_observation':4,'local_observation':2,'extra_metadata_appends':1,'new_AI_budget':0,'finance205_reapproval':False,'reset':False,'old_auth_files_immutable':True}
def validate(s,b,now):
 need(b.get('state')=='BOUND_FROM_ACTUAL_CONTINUITY105_RECEIPTS','UNBOUND_CONTINUITY105');o=b.get('owner',{});r=b.get('review',{})
 need(o.get('state')=='ACTUAL_OWNER_CONTINUITY105_COMBINED'and o.get('accepted')is True and o.get('proposed')is False and bool(o.get('canonical_source'))and re.fullmatch('[a-f0-9]{64}',o.get('actual_message_utf8_sha256','')),'ACTUAL_NEW_OWNER_REQUIRED')
 for k,v in scope().items():need(type(o.get(k))is type(v)and o[k]==v,'EXACT_COMBINED_SCOPE')
 need(o.get('spec_sha256')==digest(s)and o.get('decision_sha256')==s['decision_sha256'],'OWNER_SPEC_DECISION')
 need(r.get('state')=='ACTUAL_INDEPENDENT_CONTINUITY105_ACCEPTANCE'and r.get('independent')is True and r.get('proposed')is False and r.get('verdict')=='ACCEPT_COMPLETE_CONTINUITY105_AND_METADATA'and bool(r.get('canonical_source'))and r.get('spec_sha256')==digest(s),'ACTUAL_WHOLE_REVIEW')
 need(type(o.get('expires'))in(int,float)and math.isfinite(o['expires'])and now<o['expires']<=DEADLINE,'CONTINUITY105_EXPIRED')
 need(re.fullmatch('[a-f0-9]{40}',b.get('published_commit',''))and b['published_commit']!='de70d4cdcef2f33cc387eba14f3eed4a1975c8ba','NEW_EXACT_COMMIT')
 z=b.get('reservation',{});need(z.get('effect_id')=='CONTINUITY105-APPEND-DEPLOY8-ONCE'and z.get('state')=='RESERVED_NOT_DISPATCHED'and z.get('max_dispatches')==1 and z.get('dispatch_count')==0 and z.get('spec_sha256')==digest(s)and z.get('owner_sha256')==digest(o)and z.get('review_sha256')==digest(r)and bool(z.get('canonical_source')),'ORIGINAL_RESERVATION')
 return o

def release(m):
 import worker_scope67 as w,release_integration68 as integration,render_recorded_release70 as launch,source_extension100 as old
 v=read(BASE/'release.json',131072);s=v['spec'];b=v['bindings'];validate(s,b,m.clock())
 need(w.identity()['source_commit']==b['published_commit'],'ACTUAL_RELEASE_IDENTITY')
 need(hashlib.sha256((ROOT/'auth96/session.json').read_bytes()).hexdigest()==OLD_SESSION_SHA,'ORIGINAL_SESSION_PREIMAGE_DRIFT')
 need(digest(read(old.EXT,131072))==OLD_EXT_SHA,'ORIGINAL_EXTENSION_DRIFT')
 for n,h in s['preimages'].items():
  p=Path(n);st=p.lstat();need(stat.S_ISREG(st.st_mode)and st.st_uid==os.getuid()and st.st_nlink==1 and not st.st_mode&0o077 and not any(q.is_symlink()for q in(p,*p.parents))and hashlib.sha256(p.read_bytes()).hexdigest()==h,'ORIGINAL_PREIMAGE_CUSTODY_DRIFT')
 old.preserved();integration.checked_manifest(Path(__file__).parent,s['source_pins'])
 need(launch.CREDIT67_SHA256==s['contract_sha256']and digest(m.p)==s['policy_sha256'],'NEW_CONTRACT_OLD_POLICY')
 c=read(BASE/'release-complete.json');need(c.get('state')=='CONTINUITY105_RELEASE_COMPLETE'and c.get('release_sha256')==digest(v)and c.get('spec_sha256')==digest(s)and c.get('backup_sha256')==hashlib.sha256((BASE/'before.zip').read_bytes()).hexdigest(),'PARTIAL_RELEASE_CLOSED')
 return v

def authorize_current(m,a,old_extension):
 need(digest(old_extension)==OLD_EXT_SHA,'OLD_EXTENSION_EXACT');release(m);return a

def operator_path(m):release(m);private_dir(OP);return OP

def issue_once(m,presence,reservation,credential_sha256):
 import credit_scope67 as c,worker_scope67 as w
 v=release(m);c.authority(m);c.idle(m);c.ledger(m,unspent=True);c.codec(m);w.assert_startup()
 now=m.clock();need(v['bindings']['owner']['expires']-now>=1800,'INSUFFICIENT_TIME_BEFORE_ISSUE');need(presence.get('state')=='ACTUAL_OWNER_PRESENT_FOR_CONTINUITY105'and bool(presence.get('canonical_source'))and type(presence.get('at'))in(int,float)and 0<=now-presence['at']<=120,'OWNER_PRESENT_NOW')
 need(reservation.get('state')=='RESERVED_NOT_DISPATCHED'and reservation.get('dispatch_count')==0 and reservation.get('max_dispatches')==1 and reservation.get('release_sha256')==digest(v)and bool(reservation.get('canonical_source')),'CREDENTIAL_RESERVATION')
 need(isinstance(credential_sha256,str)and re.fullmatch('[a-f0-9]{64}',credential_sha256)and reservation.get('credential_sha256')==credential_sha256,'HASH_ONLY_CREDENTIAL_BINDING')
 need(m.operator.path==OP and not any((OP/n).exists()for n in('grant.json','grant-consumed.json','session.json')),'REPLACEMENT_ALREADY_ATTEMPTED')
 # Timer starts ONLY HERE, after deployment/review/Owner/preflight. No provider
 # freshness observation is consumed until authenticated browser is prepared.
 exclusive(OP/'grant.json',{'scope':'TRACEHARBOR-AUTH96','sha256':credential_sha256,'expires':min(now+1800,v['bindings']['owner']['expires']),'continuity_release_sha256':digest(v),'original_session_sha256':OLD_SESSION_SHA})
 return {'state':'REPLACEMENT_GRANT_ISSUED_ONCE_HASH_ONLY','expires':min(now+1800,v['bindings']['owner']['expires']),'credential_sha256':credential_sha256}
