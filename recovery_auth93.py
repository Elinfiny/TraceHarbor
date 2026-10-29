"""Forward-only AUTH96 implementation under compatible private module name.
No import effects, authority defaults, old scope revival, or client activation.
"""
import hashlib,math,os,re
from pathlib import Path
from quota_ledger import read,exclusive
from release_policy import Refusal,digest
import worker_scope67 as w
import recovery_forward96 as f
EPOCH='TRACEHARBOR-AUTH96'
FINANCE205='63c252ae7a7c0e532e84bab09b244d3ea32ca60ede5ca096fbadbb0d43b4a394'
BASE_COMMIT='d498fd29e66c88d80f6a4fa28276b00170ccc23c'
BASE_AUTHORITY='117bd1de33746b181ccfff215cf5e09d44ba9634308522d1ac9a99e0bf290f09'
REVIEW='ACCEPT_EXACT_RECOVERY96_INSTALLABLE_RELEASE_AND_BOOTSTRAP'
AUTHORITY='recovery-authority96.json'
HELPER=Path('/var/data/traceharbor-staging/recovery96-tools/native96.py')
def need(ok,why):
 if not ok:raise Refusal(why)
def operator_path(m):return m.root/'auth96'
def constants(m):
 return {'schema':'traceharbor.recovery96.authority.v1','scope':EPOCH,'accepted':True,'same_service':'srv-dbh6hgh42hec73c3g9m0','deploy_slot':6,'max_total_deploys':6,'new_grant_max':1,'new_session_max':1,'new_auth_epoch':EPOCH,'session_seconds_max':1800,'prior_grant_session_consumed_preserved':True,'reset_authorized':False,'target_max':1,'selector_max':1,'stream_max':1,'native_sample_max':1,'recording_sessions_max':1,'new_AI_max':1,'new_allocation_slot':3,'reallocated_from_HELD':1,'remaining_HELD':253,'total_call_limit':256,'allocation_id':m.config['allocation_id'],'request_sha256':m.p['request_sha256'],'policy_sha256':digest(m.p),'observation_total_max':3,'prior_observations':2,'new_observation_max':1,'finance205_sha256':FINANCE205,'call_gross_cap_USD':'0.002','planned_total_USD':'20','provider_global_hardcap':False,'new_topup_authorized':False,'new_terms_permissions_authorized':False,'prior_source_commit':BASE_COMMIT,'preserved_root95_tree_sha256':f.ROOT95_SHA,'preserved_allocation95_tree_sha256':f.ALLOCATION95_SHA}
def authority(m):
 import credit_scope67 as scope
 from render_recorded_release70 import CREDIT67_SHA256
 import source_extension100 as ext
 scope.assert_parent(m);f.preserved();a=read(m.root/AUTHORITY,65536)
 for k,v in constants(m).items():need(type(a.get(k))is type(v)and a[k]==v,'ACTUAL_TECHNICAL96_SCOPE_REQUIRED')
 need(a.get('source_commit')==ext.OLD_COMMIT and re.fullmatch('[a-f0-9]{40}',a.get('candidate_tree','')),'NEW96_SOURCE_BINDING')
 need(a.get('source_contract_sha256')==ext.OLD_CONTRACT,'NEW96_CONTRACT_BINDING')
 o=a.get('technical_owner');r=a.get('independent_review');z=a.get('finance205')
 need(all(isinstance(v,dict)for v in(o,r,z)),'ACTUAL96_RECEIPTS_REQUIRED')
 need(digest(z)==FINANCE205 and z.get('state')=='ACTUAL_INFORMED_STANDARD89_OWNER_RECEIVED'and z.get('accepted')is True and z.get('proposed')is False,'PRESERVE_ACTUAL_FINANCE205')
 need(o.get('state')=='ACTUAL_TECHNICAL_RECOVERY96_OWNER_RECEIVED'and o.get('accepted')is True and o.get('proposed')is False and bool(o.get('canonical_source')),'NEW_TECHNICAL96_OWNER_REQUIRED')
 for k,v in constants(m).items():need(type(o.get(k))is type(v)and o[k]==v,'EXACT_TECHNICAL96_OWNER_SCOPE')
 for k in('actual_message_utf8_sha256','decision_text_sha256'):need(re.fullmatch('[a-f0-9]{64}',o.get(k,'')),'ACTUAL_TECHNICAL96_MESSAGE_REQUIRED')
 need(digest(o)==a.get('technical_owner_sha256')and digest(r)==a.get('independent_review_sha256'),'ACTUAL96_RECEIPT_DIGESTS')
 need(r.get('state')=='ACTUAL_INDEPENDENT_RECOVERY96_RELEASE_ACCEPTANCE'and r.get('independent')is True and r.get('proposed')is False and r.get('verdict')==REVIEW and bool(r.get('canonical_source')),'WHOLE_RECOVERY96_REVIEW_REQUIRED')
 for k in('candidate_tree','source_contract_sha256','policy_sha256','decision_text_sha256','bootstrap_program_sha256','helper_sha256','baseline_sha256'):
  need(r.get(k)==a.get(k),'WHOLE96_REVIEW_BINDING')
 need(r.get('finance205_sha256')==FINANCE205 and o['decision_text_sha256']==a['decision_text_sha256'],'DECISION96_FINANCE_BINDING')
 need(type(a.get('expires'))in(int,float)and math.isfinite(a['expires'])and m.clock()<a['expires']<=1793379600 and o.get('expires')==a['expires'],'RECOVERY96_AUTHORITY_EXPIRED')
 migration=read(operator_path(m)/'migration.json',65536);complete=read(operator_path(m)/'bootstrap-complete.json',65536)
 need(digest(migration)==a.get('migration_sha256')and migration.get('epoch')==EPOCH and migration.get('source_commit')==a['source_commit'],'APPEND96_MIGRATION_REQUIRED')
 need(complete.get('state')=='RECOVERY96_APPEND_COMPLETE'and complete.get('authority_sha256')==digest(a)and complete.get('contract_sha256')==ext.OLD_CONTRACT and complete.get('migration_sha256')==digest(migration),'PARTIAL96_BOOTSTRAP_CLOSED')
 need(hashlib.sha256(HELPER.read_bytes()).hexdigest()==a['helper_sha256']==complete.get('helper_sha256'),'PRIVATE96_HELPER_PIN')
 backup=operator_path(m)/'preimages96.zip'
 import recovery86
 recovery86.regular(backup);need(backup.stat().st_size<=33554432 and hashlib.sha256(backup.read_bytes()).hexdigest()==complete.get('backup_sha256'),'PRIVATE96_PREIMAGE_BACKUP_REQUIRED')
 need(hashlib.sha256((m.root/'standard-authority89.json').read_bytes()).hexdigest()==BASE_AUTHORITY,'COPIED_FINANCE205_LINEAGE_ONLY')
 return ext.authorize(m,a)

def grant(m):
 import credit_scope67 as scope
 a=authority(m);scope.idle(m);scope.codec(m);scope.credit(m,120)
 raw=os.urandom(32).hex();exclusive(operator_path(m)/'grant.json',{'scope':EPOCH,'sha256':hashlib.sha256(raw.encode()).hexdigest(),'expires':min(m.clock()+1800,a['expires']),'migration_sha256':a['migration_sha256']});return raw
