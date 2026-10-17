"""Inactive ONE-request consumer. No native loader/issuer/ledger is installed.

The explicit synthetic route qualifies algorithms only. Python callbacks,
dataclasses, booleans, JSON, UID/PID and private names are never native authority.
Trusted source is the boundary, not a Python sandbox. No real claim is made.
"""
from dataclasses import dataclass
from decimal import Decimal
import math
import hashlib
import json
from nebius import (HTTPBoundary, PrivateOriginals, ProviderError,
                    decode_response, EXPECTED_PROJECT_ID)
from live_service import verified_analysis, build_record, verify_record
from core import import_package, canonical, digest, parse_json

MODEL = 'nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B'
SOURCE = 'e723e4b415b465caeee72a951225d5761928b029'
PAYLOAD_SHA256 = 'a6c905b718e0770f87efc1058f1961beaee6de172c7ab31c74fdbf82774a9b95'
PAYLOAD_BYTES = 4836
INPUT_SHA256 = 'f57813253ce6f59318354e62d4bee7c6dd133ed33cfc245438d1d5a604cf43a1'
EVIDENCE_SHA256 = '1e24c7eb6e3afadfbd767730c39390a9b43a97ba87ef6237407f0982056cecc4'


def native_binding():
    """Future reviewed loader: authentic issuer/runtime/financial/once context.

    Must bind source, actual grant, issuer/project custody, scoped durable
    producer, invocation, nonce, absolute window and protected backend CAS.
    No env/JSON switch or caller-provided callback can implement this loader.
    """
    return None

class OneRequest:
    def __init__(self):
        # Default constructor/CLI fail before credential/backend/network lookup.
        if native_binding() is None:
            raise ProviderError('NO_NATIVE_ADMISSION')
        # Even a changed loader is insufficient without separately reviewed
        # producer implementation; no witness-shaped object is accepted here.
        raise ProviderError('NATIVE_PRODUCER_NOT_IMPLEMENTED')

@dataclass(frozen=True)
class SyntheticPlan:
    """Inert specification, NOT a native admission or a financial grant."""
    nonce: str
    invocation: str
    deadline: float
    source: str = SOURCE
    project: str = EXPECTED_PROJECT_ID
    model: str = MODEL
    synthetic_bound_usd: object = Decimal('0.001')
    mode: str = 'SYNTHETIC_ONLY'

def frozen_request(raw, plan):
    if (type(plan) is not SyntheticPlan or plan.mode != 'SYNTHETIC_ONLY'
            or plan.source != SOURCE or plan.project != EXPECTED_PROJECT_ID
            or plan.model != MODEL or not plan.nonce.startswith('SYNTHETIC89-')
            or not plan.invocation.startswith('SYNTHETIC89-')):
        raise ProviderError('SOURCE_MODEL_PROJECT_OR_SYNTHETIC_SCOPE_REFUSED')
    if (type(plan.synthetic_bound_usd) is not Decimal
            or not plan.synthetic_bound_usd.is_finite()
            or plan.synthetic_bound_usd <= 0):
        raise ProviderError('SYNTHETIC_BOUND_REFUSED')
    if type(plan.deadline) not in (int, float) or not math.isfinite(plan.deadline):
        raise ProviderError('ABSOLUTE_DEADLINE_INVALID')
    if (type(raw) is not bytes or len(raw) != PAYLOAD_BYTES
            or hashlib.sha256(raw).hexdigest() != PAYLOAD_SHA256):
        raise ProviderError('FROZEN_REQUEST_REFUSED')
    value = json.loads(raw)
    if (value['model'] != MODEL or value['n'] != 1
            or value['max_completion_tokens'] != 1500
            or value['stream'] is not False or value['store'] is not False
            or value['response_format'] != {'type': 'json_object'}):
        raise ProviderError('REQUEST_CONTROLS_REFUSED')
    return value

def bound_evidence(input_raw, request_value):
    """Full source package is distinct from its immutable minimized API view."""
    if (type(input_raw) is not bytes or len(input_raw) != 598
            or hashlib.sha256(input_raw).hexdigest() != INPUT_SHA256):
        raise ProviderError('FULL_SOURCE_INPUT_BINDING_REFUSED')
    evidence = import_package(input_raw)  # Unchanged full schema/time/raw checks.
    if (evidence['input_sha256'] != INPUT_SHA256
            or digest(evidence) != EVIDENCE_SHA256):
        raise ProviderError('FULL_NORMALIZED_EVIDENCE_BINDING_REFUSED')
    for source in evidence['sources']:
        if digest(source['raw']) != source['sha256']:
            raise ProviderError('RAW_SOURCE_HASH_REFUSED')
    projection = {'case_id': evidence['case_id'], 'title': evidence['title'],
                  'synthetic': True,
                  'sources': [{k: source[k] for k in
                      ('id', 'kind', 'title', 'sha256', 'events')}
                      for source in evidence['sources']]}
    # Compare the exact public-fields projection; do not rebuild HTTP bytes.
    if canonical(projection) != request_value['messages'][1]['content'].encode():
        raise ProviderError('SOURCE_TO_FROZEN_MESSAGE_REFUSED')
    return evidence

def claim_bytes(plan):
    """Once16's full frozen invocation binding, scoped to ONE new request.

    A future native backend must authenticate its producer and enforce an
    atomic create-if-ABSENT -> ATTEMPTING_CONSUMED plus immutable full readback.
    Existing state, collision, ambiguity or changed invocation means no POST.
    There is no second local ledger, O_EXCL substitute or native implementation.
    """
    return json.dumps({
        'schema': 'TRACEHARBOR_ONE_CONSUMED89_SYNTHETIC_ONLY',
        'state': 'ATTEMPTING_CONSUMED_NO_REFUND_NO_RETRY',
        'source': plan.source, 'request_sha256': PAYLOAD_SHA256,
        'project': plan.project, 'model': plan.model, 'requests': 1,
        'nonce': plan.nonce, 'invocation': plan.invocation,
        'deadline': plan.deadline, 'mode': 'SYNTHETIC_ONLY',
        'native_grant': None, 'synthetic_bound_usd': str(plan.synthetic_bound_usd),
        'input_sha256': INPUT_SHA256, 'evidence_sha256': EVIDENCE_SHA256
    }, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()

class SyntheticRunner:
    """Explicit fake-only algorithm seam; never dispatch this as native work."""
    def __init__(self, plan, backend, boundary, credential):
        self.plan, self.backend, self.boundary, self.credential = plan, backend, boundary, credential
        self.attempted = False

    def execute(self, raw, input_raw=None):
        self.boundary.check('PRE_INPUT_VALIDATION')
        value = self.boundary.invoke('FROZEN_INPUT', lambda: frozen_request(raw, self.plan))
        evidence = self.boundary.invoke('FULL_EVIDENCE', lambda: bound_evidence(input_raw, value))
        if self.attempted:
            raise ProviderError('ALREADY_CONSUMED_NO_RETRY')
        if self.boundary.deadline != self.plan.deadline:
            raise ProviderError('DEADLINE_BINDING_REFUSED')
        self.boundary.check('PRE_REQUEST_CONSUME')
        self.attempted = True
        expected = claim_bytes(self.plan)
        # Fake receipt alone is not native authority: this route is always inert.
        receipt = self.boundary.invoke('CONSUME', lambda:
            self.backend.conditional_absent_to_consumed(self.plan.nonce, expected), 'CLAIM_RECEIPT')
        if receipt != expected:
            self.boundary.fail('CLAIM_AMBIGUOUS_UNKNOWN')
            raise ProviderError(self.boundary.first_primary)
        readback = self.boundary.invoke('FULL_READBACK', lambda:
            self.backend.readback(self.plan.nonce), 'CLAIM_BYTES')
        if readback != expected:
            self.boundary.fail('CLAIM_READBACK_OR_INVOCATION_MISMATCH')
            raise ProviderError(self.boundary.first_primary)
        self.boundary.check('PRE_INVOKE_CREDENTIAL')
        try:
            key = self.credential()  # Private local only, never serialized.
        except Exception as error:
            self.boundary.capture('CREDENTIAL', 'EXCEPTION', error, 'CREDENTIAL_UNKNOWN')
            self.boundary.fail('CREDENTIAL_UNKNOWN')
            raise ProviderError(self.boundary.first_primary) from None
        self.boundary.capture('CREDENTIAL', 'PRESENCE_ONLY', key is not None)
        self.boundary.check('POST_RETURN_CREDENTIAL')
        answer = self.boundary.exchange(raw, key, self.plan.project)
        parsed = self.boundary.invoke('DECODE', lambda: decode_response(answer, MODEL))
        analysis, metadata = parsed
        verified = self.boundary.invoke('VERIFY', lambda: verified_analysis(analysis, evidence))
        metadata['request_sha256'] = PAYLOAD_SHA256
        dossier = self.boundary.invoke('BUILD_RECORD', lambda: build_record(input_raw, analysis, metadata))
        self.boundary.invoke('VERIFY_RECORD', lambda: verify_record(dossier))
        self.boundary.check('POST_FINAL_VERIFICATION')
        return {'mode': 'SYNTHETIC_ONLY', 'native_authority': False,
                'request_sha256': PAYLOAD_SHA256, 'analysis': analysis,
                'usage': metadata['usage'], 'verification': verified, 'dossier': dossier}

def main():
    try:
        OneRequest()
    except ProviderError:
        print('TRACEHARBOR_ONE_REQUEST_INACTIVE')
        return 2
    return 2

if __name__ == '__main__':
    raise SystemExit(main())
