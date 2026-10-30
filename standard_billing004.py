"""Standard billing guard. No import I/O, inference, billing toggle or reset.
Hashes bind receipts; they do not authenticate Owner or independent reviewer.
Sole Master must read their actual canonical sources before binding receipts.
The project cap is NOT an account-wide provider spending cap.
"""
import datetime, decimal, math, re
from quota_ledger import read
from release_policy import Refusal, digest
import worker_scope004 as w
DEADLINE=1793379600
MODE='STANDARD_PAID89'
REVIEW='ACCEPT_EXACT_STANDARD89_CODE_AND_BOOTSTRAP'

def require(ok, reason):
 if not ok:raise Refusal(reason)


def authority(m):
 import recovery_auth004
 return recovery_auth004.authority(m)


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
 import credit_scope004 as scope
 try:v=scope.credit(m,300);admitted=True;label=v['billing_status']
 except Exception:admitted=False;label='UNKNOWN'
 ready=m.ready()and admitted
 return {'schema':'traceharbor.runtime-status.v1','enabled':ready,'new_call_cap':1 if ready else 0,'reason':'ONE_FROM253HELD_OTHER252HELD','phases':{n:m.state(n)for n in('select','native','full')},'armed':(m.root/'target.json').exists(),'armed_id':read(m.root/'target.json')['client_id']if(m.root/'target.json').exists()else None,'target_epoch':'004','full_elapsed':m.clock()-m.sinks['full'].started if'full'in m.sinks else None,'session_remaining':int(m.operator.remaining()),'e2e_reserved':(m.root/'e2e-reserved.json').exists(),'e2e_result':(m.root/'e2e-result.json').exists(),'retained_clip_qualification':{'state':'PASS_PRIOR_NATIVE146_LINEAGE','clip_bytes':71412,'new_native_sample_still_required':True},'provider_readiness':{'state':'STANDARD_PAID_ATTEMPT_ADMITTED'if admitted else'NOT_ADMITTED','admitted_attempt':admitted,'billing_mode':MODE,'billing_status':label,'paid_usage_enabled':True if admitted else None,'paid_continuation_disabled':False if admitted else None,'provider_global_hardcap':False,'credential_binding':'CONFIGURED_PROJECT_NOT_PROVIDER_ATTESTED','inference_success_proven':False},'retry':False}
