"""New dynamic-request release path; cap0/pinNone are still the shipped defaults.
Only trusted server construction can supply reviewed config/counter/state. No
HTTP request, environment value or client flag can enable a release.
"""
import os,time,http.client
import runtime_service as old
import release_policy as policy
from release_policy import Refusal,validate_config,digest,input_admission,deadline
from quota_ledger import Ledger,ReservationUnknown
from core import canonical
from live_service import build_record,verified_analysis

class ReviewedSession:
    def __init__(self,config,ledger,counter,*,_factory=None,_environment=None,_clock=None):
        self.config=dict(validate_config(config));self.ledger=ledger;self.counter=counter
        if ledger.config!=self.config:raise Refusal('LEDGER_CONFIG_PIN')
        self.factory=http.client.HTTPSConnection if _factory is None else _factory
        self.environment=os.environ if _environment is None else _environment;self.clock=_clock
    def _gate(self):
        if type(old.GLOBAL_NEW_CALL_CAP)is not int or old.GLOBAL_NEW_CALL_CAP!=256 or policy.REVIEWED_RELEASE_SHA256 is None or policy.REVIEWED_RELEASE_SHA256!=digest(self.config):raise Refusal('NEW_CALL_CAP_ZERO_OR_RELEASE_PIN')
        deadline(self.config,self.clock() if self.clock else None)
        if self.counter is None:raise Refusal('EXACT_COUNTER_REQUIRED')
    def status(self):
        try:self._gate();enabled=True
        except Exception:enabled=False
        return {'schema':'traceharbor.runtime-status.v1','enabled':enabled,'new_call_cap':256 if enabled else 0,'state':'SERVER_PREFLIGHT_REQUIRED' if enabled else 'NOT_ADMITTED','reason':'PERSISTENT_RELEASE46' if enabled else 'NEW_CALL_CAP_ZERO','mode':'SYNTHETIC_AND_HISTORICAL_REMAIN_SEPARATE','retry':False}
    def dispatch(self,raw):
        try:
            self._gate();evidence,payload,encoded=old.prepare(raw)
            cert=self.counter.count(payload);cost=input_admission(payload,cert,self.config)
            key=old._credential(self.environment)
            reservation=self.ledger.reserve(digest(payload),cost,self.clock() if self.clock else None)
        except ReservationUnknown:
            raise old.RuntimeRefusal('RESERVATION_UNKNOWN',consumed=True) from None
        except Exception:
            raise old.RuntimeRefusal('RELEASE_PREFLIGHT_REFUSED') from None
        boundary=old.nebius.HTTPBoundary(time.monotonic()+old.DEADLINE_SECONDS,old._MemoryCapture(),factory=self.factory)
        result=None
        try:
            deadline(self.config,self.clock() if self.clock else None)
            body=boundary.exchange(encoded,key,old.nebius.EXPECTED_PROJECT_ID)
            if key.encode() in body:raise Refusal('SECRET_REFUSED')
            analysis,metadata=old.nebius.decode_response(body,old.MODEL)
            if key in canonical(analysis).decode() or key in canonical(metadata).decode():raise Refusal('SECRET_REFUSED')
            if metadata['usage']['prompt_tokens']!=cert['count']:
                self.ledger.halt('COUNTER_USAGE_DRIFT');raise Refusal('COUNTER_USAGE_DRIFT')
            metadata['request_sha256']=digest(payload);verified_analysis(analysis,evidence)
            result={'schema':old.SCHEMA,'mode':'SERVER_RUNTIME_RECORD_ORIGIN_UNATTESTED','record':build_record(raw,analysis,metadata),'attempt':{'request_attempted':True,'retry':False,'origin':'NOT_INDEPENDENTLY_ATTESTED','deadline_seconds':old.DEADLINE_SECONDS},'limits':old.LIMITS}
            result['dossier_sha256']=digest(result);old.verify_runtime_result(result)
        except Exception:result=None
        try:self.ledger.terminal(reservation,result is not None)
        except Exception:result=None
        if result is None:raise old.RuntimeRefusal('CALL_OUTCOME_UNKNOWN',consumed=True) from None
        return result
