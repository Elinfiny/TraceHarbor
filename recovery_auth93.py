"""Forward-only authentication epoch. Import has no I/O or effects.
Owner205 finances remain immutable; technical93 is a separate actual receipt.
No old grant/session, observation budget, media phase or ledger is reset.
"""
import hashlib,math,os,re
from pathlib import Path
from quota_ledger import read,exclusive
from release_policy import Refusal,digest
import worker_scope67 as w

EPOCH='TRACEHARBOR-AUTH93'
FINANCE205='63c252ae7a7c0e532e84bab09b244d3ea32ca60ede5ca096fbadbb0d43b4a394'
BASE_COMMIT='ab1bbf06ea37b28b67d17147840e3295c6d92766'
BASE_AUTHORITY='117bd1de33746b181ccfff215cf5e09d44ba9634308522d1ac9a99e0bf290f09'
OLD_AUTH_PINS={'operator67/grant.json':'ea4d1c316a7905abd2a070514ba0e44388dd6b9689d73e5718e0dd63d166da18',
 'operator67/grant-consumed.json':'b10dc306033d82c3db396712d03cb89a5fe1c699ca678d28114cf2b370659305',
 'operator67/session.json':'6162f62c208c403e1ba0899516902faa41080dc5d337838033635b19eb13f561'}
REVIEW='ACCEPT_EXACT_RECOVERY93_INSTALLABLE_RELEASE_AND_BOOTSTRAP'
AUTHORITY='recovery-authority93.json'
HELPER=Path('/var/data/traceharbor-staging/recovery93-tools/native93.py')

def need(ok,why):
 if not ok:raise Refusal(why)

def constants(m):
 return {'schema':'traceharbor.recovery93.authority.v1','scope':EPOCH,'accepted':True,
 'same_service':'srv-dbh6hgh42hec73c3g9m0','deploy_slot':5,'max_total_deploys':5,
 'new_grant_max':1,'new_session_max':1,'new_auth_epoch':EPOCH,'session_seconds_max':1800,
 'prior_grant_session_consumed_preserved':True,'reset_authorized':False,
 'selector_max':1,'recording_sessions_max':1,'new_AI_max':1,'reallocated_from_HELD':1,
 'total_call_limit':256,'allocation_id':m.config['allocation_id'],
 'request_sha256':m.p['request_sha256'],'policy_sha256':digest(m.p),
 'observation_total_max':3,'prior_observations':1,'finance205_sha256':FINANCE205,
 'call_gross_cap_USD':'0.002','planned_total_USD':'20','provider_global_hardcap':False,
 'new_topup_authorized':False,'new_terms_permissions_authorized':False,
 'prior_source_commit':BASE_COMMIT,'prior_standard_authority_sha256':BASE_AUTHORITY}

def operator_path(m):
 return m.root/'auth93'

def preserved(m,a):
 import recovery86
 need(a.get('prior_auth_pins')==OLD_AUTH_PINS,'EXACT_CONSUMED67_PROVENANCE_REQUIRED')
 for rel,h in OLD_AUTH_PINS.items():
  p=m.root/rel;recovery86.regular(p)
  need(hashlib.sha256(p.read_bytes()).hexdigest()==h,'CONSUMED67_RECEIPT_DRIFT')
 p=m.root/'standard-authority89.json';recovery86.regular(p)
 need(hashlib.sha256(p.read_bytes()).hexdigest()==BASE_AUTHORITY,'ORIGINAL205_AUTHORITY_DRIFT')
 # Only the fixed pre-existing files are pinned. Future effects may APPEND files.
 baseline=a.get('preserved_root_files');need(isinstance(baseline,dict)and len(baseline)==31,'EXACT_PREEXISTING_ROOT_PROOF')
 for rel,pin in baseline.items():
  need(isinstance(rel,str)and not Path(rel).is_absolute()and '..'not in Path(rel).parts,'SAFE_RELATIVE_PIN')
  p=m.root/rel;recovery86.regular(p);raw=p.read_bytes()
  need(len(raw)==pin['bytes']and hashlib.sha256(raw).hexdigest()==pin['sha256'],'PREEXISTING_DATA_DRIFT')

def authority(m):
 import credit_scope67 as scope
 from render_recorded_release70 import CREDIT67_SHA256
 scope.assert_parent(m)
 a=read(m.root/AUTHORITY,65536)
 for k,v in constants(m).items():need(type(a.get(k))is type(v)and a[k]==v,'ACTUAL_TECHNICAL93_SCOPE_REQUIRED')
 need(a.get('source_commit')==w.identity()['source_commit']and re.fullmatch('[a-f0-9]{40}',a.get('candidate_tree','')),'NEW_SOURCE_BINDING')
 need(a.get('source_contract_sha256')==CREDIT67_SHA256,'NEW_CONTRACT_BINDING')
 o=a.get('technical_owner');r=a.get('independent_review');f=a.get('finance205')
 need(isinstance(o,dict)and isinstance(r,dict)and isinstance(f,dict),'ACTUAL_RECEIPTS_REQUIRED')
 need(digest(f)==FINANCE205 and f.get('state')=='ACTUAL_INFORMED_STANDARD89_OWNER_RECEIVED'and f.get('accepted')is True and f.get('proposed')is False,'PRESERVE_ACTUAL_FINANCE205')
 need(o.get('state')=='ACTUAL_TECHNICAL_RECOVERY93_OWNER_RECEIVED'and o.get('accepted')is True and o.get('proposed')is False and bool(o.get('canonical_source')),'NEW_TECHNICAL_OWNER_REQUIRED')
 for k,v in constants(m).items():need(type(o.get(k))is type(v)and o[k]==v,'EXACT_TECHNICAL_OWNER_SCOPE')
 for k in('actual_message_utf8_sha256','decision_text_sha256'):need(re.fullmatch('[a-f0-9]{64}',o.get(k,'')),'ACTUAL_TECHNICAL_MESSAGE_REQUIRED')
 need(digest(o)==a.get('technical_owner_sha256')and digest(r)==a.get('independent_review_sha256'),'ACTUAL_RECEIPT_DIGESTS')
 need(r.get('state')=='ACTUAL_INDEPENDENT_RECOVERY93_RELEASE_ACCEPTANCE'and r.get('independent')is True and r.get('proposed')is False and r.get('verdict')==REVIEW and bool(r.get('canonical_source')),'WHOLE_RECOVERY93_REVIEW_REQUIRED')
 for k in('candidate_tree','source_contract_sha256','policy_sha256','decision_text_sha256','bootstrap_program_sha256','helper_sha256'):
  need(r.get(k)==a.get(k),'WHOLE_REVIEW_BINDING')
 need(r.get('finance205_sha256')==FINANCE205 and o['decision_text_sha256']==a.get('decision_text_sha256'),'DECISION_FINANCE_BINDING')
 need(type(a.get('expires'))in(int,float)and math.isfinite(a['expires'])and m.clock()<a['expires']<=1793379600 and o.get('expires')==a['expires'],'RECOVERY93_AUTHORITY_EXPIRED')
 preserved(m,a)
 migration=read(operator_path(m)/'migration.json',65536)
 need(digest(migration)==a.get('migration_sha256')and migration.get('prior_auth_pins')==OLD_AUTH_PINS and migration.get('epoch')==EPOCH and migration.get('source_commit')==a['source_commit'],'APPEND_MIGRATION_PROOF_REQUIRED')
 complete=read(operator_path(m)/'bootstrap-complete.json',65536)
 need(complete.get('state')=='RECOVERY93_APPEND_COMPLETE'and complete.get('authority_sha256')==digest(a)and complete.get('contract_sha256')==CREDIT67_SHA256 and complete.get('migration_sha256')==digest(migration),'PARTIAL_BOOTSTRAP_NO_EFFECTS')
 need(hashlib.sha256(HELPER.read_bytes()).hexdigest()==a['helper_sha256']==complete.get('helper_sha256'),'PRIVATE93_HELPER_PIN')
 backup=operator_path(m)/'preimages93.zip';recovery86=__import__('recovery86');recovery86.regular(backup)
 need(backup.stat().st_size<=8388608 and hashlib.sha256(backup.read_bytes()).hexdigest()==complete.get('backup_sha256'),'PRIVATE_PREIMAGE_BACKUP_REQUIRED')
 return a

def grant(m):
 import credit_scope67 as scope
 a=authority(m);scope.idle(m);scope.codec(m);scope.credit(m,120)
 raw=os.urandom(32).hex()
 exclusive(operator_path(m)/'grant.json',{'scope':EPOCH,'sha256':hashlib.sha256(raw.encode()).hexdigest(),
  'expires':min(m.clock()+1800,a['expires']),'migration_sha256':a['migration_sha256']})
 return raw
