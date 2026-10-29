"""Standard billing guard. No import I/O, inference, billing toggle or reset.
Hashes bind receipts; they do not authenticate Owner or independent reviewer.
Sole Master must read their actual canonical sources before binding receipts.
The project cap is NOT an account-wide provider spending cap.
"""
import datetime, decimal, math, re
from quota_ledger import read
from release_policy import Refusal, digest
import worker_scope67 as w
DEADLINE=1793379600
MODE='STANDARD_PAID89'
REVIEW='ACCEPT_EXACT_STANDARD89_CODE_AND_BOOTSTRAP'

def require(ok, reason):
 if not ok:raise Refusal(reason)

def expected(m):
 return {'schema':'traceharbor.standard89.authority.v1','scope':MODE,'accepted':True,'billing_mode':MODE,'same_service':'srv-dbh6hgh42hec73c3g9m0','deploy_slot':4,'max_total_deploys':4,'new_AI_max':1,'reallocated_from_HELD':1,'allocation_id':m.config['allocation_id'],'total_call_limit':256,'session_max':1,'selector_max':1,'recording_sessions_max':1,'paid_usage_authorized':True,'paid_continuation_disabled':False,'provider_global_hardcap':False,'uncapped_provider_liability_acknowledged':True,'project_credential_binding_not_provider_attested_acknowledged':True,'new_topup_authorized':False,'new_terms_permissions_authorized':False,'call_gross_cap_USD':'0.002','planned_total_USD':'20','request_sha256':m.p['request_sha256'],'policy_sha256':digest(m.p)}

def authority(m):
 import recovery_auth93
 return recovery_auth93.authority(m)

def legacy_standard89_authority_closed(m):
 import credit_scope67 as scope
 from render_recorded_release70 import CREDIT67_SHA256
 scope.assert_parent(m)
 a=read(m.root/'standard-authority89.json',65536)
 for k,v in expected(m).items():require(type(a.get(k))is type(v)and a[k]==v,'ACTUAL_INFORMED_STANDARD89_AUTHORITY_REQUIRED')
 require(a.get('source_commit')==w.identity()['source_commit']and re.fullmatch('[a-f0-9]{40}',a.get('candidate_tree','')),'STANDARD89_SOURCE_BINDING')
 require(a.get('source_contract_sha256')==CREDIT67_SHA256,'STANDARD89_SOURCE_CONTRACT_BINDING')
 owner=a.get('owner_receipt');review=a.get('independent_review')
 require(isinstance(owner,dict)and isinstance(review,dict),'ACTUAL_STANDARD89_RECEIPTS_REQUIRED')
 require(digest(owner)==a.get('owner_receipt_sha256')and digest(review)==a.get('independent_review_sha256'),'STANDARD89_RECEIPT_DIGEST')
 require(owner.get('state')=='ACTUAL_INFORMED_STANDARD89_OWNER_RECEIVED'and owner.get('accepted')is True and owner.get('proposed')is False,'PROPOSALS_AND_OWNER83_ARE_NOT_STANDARD_CONSENT')
 require(re.fullmatch('[a-f0-9]{64}',owner.get('actual_message_utf8_sha256',''))and re.fullmatch('[a-f0-9]{64}',owner.get('decision_text_sha256',''))and bool(owner.get('canonical_source')),'ACTUAL_OWNER_MESSAGE_BINDING')
 for k,v in expected(m).items():require(type(owner.get(k))is type(v)and owner[k]==v,'OWNER_SCOPE_OR_RISK_MISMATCH')
 require(review.get('state')=='ACTUAL_INDEPENDENT_STANDARD89_ACCEPTANCE'and review.get('independent')is True and review.get('proposed')is False and review.get('verdict')==REVIEW,'NEW_INDEPENDENT_STANDARD89_REVIEW_REQUIRED')
 for k in('candidate_tree','source_contract_sha256','policy_sha256'):
  require(review.get(k)==a.get(k),'STANDARD89_REVIEW_BINDING')
 require(review.get('owner_receipt_sha256')==a['owner_receipt_sha256']and bool(review.get('canonical_source')),'REVIEW_OWNER_BINDING')
 require(type(a.get('expires'))in(int,float)and math.isfinite(a['expires'])and m.clock()<a['expires']<=DEADLINE and owner.get('expires')==a['expires'],'STANDARD89_AUTHORITY_EXPIRED')
 return a

def validate_observation(m,v,max_age):
 authority(m)
 values={'schema':'traceharbor.standard89.billing-observation.v1','scope':MODE,'tenant':'aitenant-e00rrxfyw57s74dbqq','project':'aiproject-e00d73xwjm884tnvcs','billing_mode':MODE,'billing_status':'Active','paid_usage_enabled':True,'paid_continuation_disabled':False,'provider_global_hardcap':False,'provider_confirmed_credit_only':False,'credential_binding':'CONFIGURED_PROJECT_NOT_PROVIDER_ATTESTED','pricing_confirmed':True,'input_nanodollars_per_token':60,'output_nanodollars_per_token':240,'no_inference':True,'identity':w.identity(),'source_kind':'ACTUAL_NEBIUS_UI_READBACK'}
 for k,z in values.items():require(type(v.get(k))is type(z)and v[k]==z,'ACTUAL_STANDARD89_BILLING_METADATA_REQUIRED')
 require(re.fullmatch('[a-f0-9]{64}',v.get('activation_ui_readback_sha256',''))and re.fullmatch('[a-f0-9]{64}',v.get('rates_ui_readback_sha256','')),'STANDARD89_ACTUAL_UI_BINDING')
 try:
  require(type(v['balance_USD'])is str and type(v['tax_multiplier'])is str,'DECIMAL_STRINGS')
  t=datetime.datetime.fromisoformat(v['observed_at_utc'].replace('Z','+00:00'))
  require(t.tzinfo is not None and 0<=m.clock()-t.timestamp()<=max_age,'FRESH_STANDARD89_METADATA')
  balance=decimal.Decimal(v['balance_USD']);tax=decimal.Decimal(v['tax_multiplier']);bound=decimal.Decimal('0.002')
  basis=v.get('tax_basis')
  require((basis=='CONSERVATIVE_UPPER_BOUND_2_NOT_ACTUAL_INVOICE'and tax==2)or(basis=='ACTUAL_ACCOUNT_TAX_EVIDENCE'and re.fullmatch('[a-f0-9]{64}',v.get('tax_evidence_sha256',''))),'HONEST_STANDARD89_TAX_BASIS')
  cost=decimal.Decimal(m.p['certificate']['count']*60+1500*240)/1000000000*tax
  require(balance.is_finite()and tax.is_finite()and 1<=tax<=2 and cost<=bound<=balance,'STANDARD89_PRICE_TAX_BALANCE_BOUND')
 except (KeyError,ValueError,TypeError,decimal.InvalidOperation):raise Refusal('STANDARD89_PRICE_TAX_BALANCE_BOUND')from None
 return v

def status(m):
 import credit_scope67 as scope
 try:v=scope.credit(m,300);admitted=True;label=v['billing_status']
 except Exception:admitted=False;label='UNKNOWN'
 ready=m.ready()and admitted
 return {'schema':'traceharbor.runtime-status.v1','enabled':ready,'new_call_cap':1 if ready else 0,'reason':'ONE_FROM254HELD_OTHER253HELD','phases':{n:m.state(n)for n in('select','native','full')},'armed':(m.root/'target.json').exists(),'armed_id':read(m.root/'target.json')['client_id']if(m.root/'target.json').exists()else None,'target_epoch':'67','full_elapsed':m.clock()-m.sinks['full'].started if'full'in m.sinks else None,'session_remaining':int(m.operator.remaining()),'e2e_reserved':(m.root/'e2e-reserved.json').exists(),'e2e_result':(m.root/'e2e-result.json').exists(),'retained_clip_qualification':{'state':'PASS_PRIOR_NATIVE146_LINEAGE','clip_bytes':71412,'new_native_sample_still_required':True},'provider_readiness':{'state':'STANDARD_PAID_ATTEMPT_ADMITTED'if admitted else'NOT_ADMITTED','admitted_attempt':admitted,'billing_mode':MODE,'billing_status':label,'paid_usage_enabled':True if admitted else None,'paid_continuation_disabled':False if admitted else None,'provider_global_hardcap':False,'credential_binding':'CONFIGURED_PROJECT_NOT_PROVIDER_ATTESTED','inference_success_proven':False},'retry':False}
