"""PRIVATE42 Master predicate. No POST, dispatch, live token or new actor.
External admission gate remains deliberately unbound; JSON/hash/PID is not a grant.
"""
import native27_validator42 as v

EXTERNAL_ADMISSION_GATE=None

def conditional_second(log,receipt,run,writer_job,validator_job,observed,now,
                       second_run_id,remaining=1,state=None,grant=None,synthetic_cap=None):
    state=state or v.Sticky();state.retain((log[:v.LOG_MAX+1],receipt,run,writer_job,validator_job,observed))
    try:
        v.need(state.first_unknown is None,'FIRST_UNKNOWN')
        fresh=v.validate(log,run,writer_job,observed,now,remaining,state)
        v.need(v.canonical(receipt)==v.canonical(fresh),'RECEIPT_NOT_EXACT_RECOMPUTATION')
        b=fresh['bindings'];v.context(b,run,writer_job,observed,now,remaining,controller=True)
        v.need(v.integer(validator_job.get('id'),1) and validator_job['id']!=writer_job['id'] and
               type(validator_job.get('run_id')) is int and validator_job.get('run_id')==b['first_run_id'] and type(validator_job.get('attempt')) is int and validator_job.get('attempt')==1 and
               validator_job.get('head_sha')==b['source'] and validator_job.get('status')=='completed' and
               validator_job.get('conclusion')=='success','VALIDATOR_NOT_TERMINAL_SUCCESS')
        v.need(v.integer(second_run_id,1) and second_run_id!=b['first_run_id'],'TWO_RUNS_REQUIRED')
        v.need(observed.get('nonce_state')=='FIRST_APPLIED_VERIFIED' and observed.get('second_attempt_consumed') is False and
               observed.get('unknown_effect') is False,'CONSUMED_OR_UNKNOWN')
        # Only SYNTHETIC descriptors are constructible in this candidate. No live
        # grant verifier exists yet. Future host must bind its EXISTING exact gate.
        v.need(synthetic_cap is v.SYNTHETIC_CAP and type(grant) is dict and
               set(grant)=={'classification','bindings','receipt_sha256','second_run_id'} and
               grant['classification']=='EXPLICIT_SYNTHETIC_ONLY' and grant['bindings']==b and
               grant['receipt_sha256']==v.digest(v.canonical(receipt)) and grant['second_run_id']==second_run_id,
               'AUTHENTIC_EXTERNAL_GRANT_UNBOUND')
        return {'kind':'CONDITIONAL_SECOND_DESCRIPTOR_ONLY','synthetic':True,'live_authority':False,
                'phase':'second','first_run_id':b['first_run_id'],'first_commit':b['commit'],
                'second_run_id':second_run_id,'source':b['source'],'workflow_id':b['workflow_id'],
                'workflow_sha256':b['workflow_sha256'],'driver_sha256':b['driver_sha256'],
                'validator_sha256':b['validator_sha256'],'nonce':b['nonce'],'ref':b['ref'],
                'receipt_sha256':v.digest(v.canonical(receipt)),'expires_at':fresh['expires_at'],
                'dispatch_performed':False,'existing_admission_hook':'EXTERNAL_ADMISSION_GATE=None'}
    except v.Refuse as ex:state.fail(str(ex))

def existing_gate_hook(context):
    """Explicit integration seam; no fallback/minted grant from context values."""
    if EXTERNAL_ADMISSION_GATE is None:return None
    return EXTERNAL_ADMISSION_GATE.verify_exact_distinct_second_admission(context)

if __name__=='__main__':raise SystemExit('INACTIVE42_NO_DISPATCH')
