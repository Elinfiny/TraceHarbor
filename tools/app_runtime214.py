"""PROPOSED ordinary app runtime; never native custody/attestation or admission.

Activation requires independent acceptance, exact guarded publication and one
provider-native create-only branch. This file does not modify nebius.py's loader.
"""
import sys
sys.dont_write_bytecode = True
import hashlib
import http.client
import importlib.util
import json
import os
from pathlib import Path
import re
import time
from decimal import Decimal

PROFILE = 'APP_RUNTIME_DIAGNOSTIC214'
MODEL = 'nvidia/Nemotron-3_5-Lightning'
REQUEST_SHA = 'e4b08fa3937e4c8348383a5abf934ffbf3832183fadc2907018adbc4a04a71b2'
REQUEST_BYTES = 4935
BRANCH = 'traceharbor/diag214/v1/e4b08fa3937e4c83-15d69a8e12854ff0'
BASE = '1f84a28a26669d1660e0782513e0078050345b84'
RESERVE_USD = Decimal('0.25')
OWNER_FREE_CREDIT_CAP_USD = Decimal('1')
INPUT_UPPER_BOUND = 2000000
OUTPUT_CAP = 1500
MAX_RESPONSE = 262144


class Refusal(ValueError):
    pass


def request_guard(raw):
    if type(raw) is not bytes or len(raw) != REQUEST_BYTES or hashlib.sha256(raw).hexdigest() != REQUEST_SHA:
        raise Refusal('EXACT_REQUEST_REQUIRED')
    req = json.loads(raw)
    if (req['model'] != MODEL or req['max_completion_tokens'] != OUTPUT_CAP or req['n'] != 1
            or req['stream'] is not False or req['store'] is not False
            or req['response_format'] != {'type': 'json_object'}):
        raise Refusal('REQUEST_PROFILE_MISMATCH')
    return req


def caller_guard(ctx, event):
    # These are trusted-runner routing constraints, NOT native emitter authentication.
    expected = {'GITHUB_REPOSITORY': 'Elinfiny/TraceHarbor', 'GITHUB_REPOSITORY_ID': '1391430317',
                'GITHUB_ACTOR_ID': '273768139', 'GITHUB_EVENT_NAME': 'create',
                'GITHUB_REF': 'refs/heads/' + BRANCH, 'GITHUB_RUN_ATTEMPT': '1',
                'TRACE214_APP_PROFILE': PROFILE}
    if any(ctx.get(k) != v for k, v in expected.items()):
        raise Refusal('CALLER_PROFILE_NOT_ADMITTED')
    if event.get('ref') != BRANCH or event.get('ref_type') != 'branch':
        raise Refusal('CREATE_EVENT_MISMATCH')
    if (not re.fullmatch('[0-9a-f]{40}', ctx.get('GITHUB_SHA', ''))
            or not re.fullmatch('[1-9][0-9]*', ctx.get('GITHUB_RUN_ID', ''))):
        raise Refusal('RUN_SOURCE_ID_INVALID')
    return {k: ctx[k] for k in (*expected, 'GITHUB_SHA', 'GITHUB_RUN_ID')}



RAW_INPUT_SHA = 'f57813253ce6f59318354e62d4bee7c6dd133ed33cfc245438d1d5a604cf43a1'
RAW_INPUT_BYTES = 598


def input_for_request(raw):
    from core import canonical, digest
    req = request_guard(raw)
    view = json.loads(req['messages'][1]['content'])
    sources = []
    for source in view['sources']:
        original = {k: source[k] for k in ('id', 'kind', 'title')}
        original['events'] = []
        for event in source['events']:
            if (event['timestamp_state'] != 'known'
                    or event['timestamp_candidates'] != [event['timestamp']]
                    or type(event['timestamp']) is not str):
                raise Refusal('INPUT_RECONSTRUCTION_UNSUPPORTED')
            original['events'].append({k: event[k] for k in ('id', 'text', 'timestamp')})
        if digest(original) != source['sha256']:
            raise Refusal('INPUT_SOURCE_HASH_MISMATCH')
        sources.append(original)
    package = canonical({'schema': 'traceharbor.input.v1', 'synthetic': True,
                         'case_id': view['case_id'], 'title': view['title'], 'sources': sources})
    if len(package) != RAW_INPUT_BYTES or hashlib.sha256(package).hexdigest() != RAW_INPUT_SHA:
        raise Refusal('INPUT_RECONSTRUCTION_MISMATCH')
    bind_input(raw, package)
    return package


def bind_input(raw, package):
    from core import import_package, canonical
    req = request_guard(raw)
    if (type(package) is not bytes or len(package) != RAW_INPUT_BYTES
            or hashlib.sha256(package).hexdigest() != RAW_INPUT_SHA):
        raise Refusal('INPUT_BINDING_MISMATCH')
    evidence = import_package(package)
    view = {k: evidence[k] for k in ('case_id', 'title', 'synthetic')}
    view['sources'] = [{k: s[k] for k in ('id', 'kind', 'title', 'sha256', 'events')}
                       for s in evidence['sources']]
    if canonical(view).decode() != req['messages'][1]['content']:
        raise Refusal('INPUT_BINDING_MISMATCH')
    return evidence


SAFE_PROVIDER_CODES = frozenset({
    'PROVIDER_CHOICE_COUNT', 'PROVIDER_EMPTY_CONTENT', 'PROVIDER_INCOMPLETE_OR_TRUNCATED',
    'PROVIDER_INVALID_JSON_OR_STRUCTURE', 'PROVIDER_MODEL_MISMATCH',
    'PROVIDER_REFUSAL_OR_TOOL_CALL', 'PROVIDER_TOKEN_BOUND_EXCEEDED', 'PROVIDER_USAGE_INVALID',
    'CALL_OUTCOME_UNKNOWN', 'HANDLER_OUTCOME_UNKNOWN', 'CLEANUP_UNKNOWN', 'CLOCK_UNKNOWN',
    'ABSOLUTE_DEADLINE_UNKNOWN', 'PROVIDER_STATUS_INVALID', 'PROVIDER_BODY_INVALID',
    'PROVIDER_RESPONSE_TOO_LARGE', 'PROVIDER_CONTENT_TYPE', 'TRANSPORT_INPUT_REFUSED',
    'ALREADY_ATTEMPTED_NO_RETRY', 'PROJECT_NOT_CONFIGURED'
}) | frozenset('PROVIDER_HTTP_' + str(n) for n in range(100, 600))
SAFE_REFUSAL_CODES = frozenset({'ACTUAL_USAGE_EXCEEDS_ADMITTED_BOUND',
                              'ACTUAL_METER_ESTIMATE_EXCEEDS_RESERVED_CREDIT',
                              'APPLICATION_CAPTURE_COUNT', 'APPLICATION_CAPTURE_BYTES'})



PRODUCT_REASON_MESSAGES214 = {'Object fields do not match the documented schema.': 'SCHEMA_FIELDS', 'Unknown analysis status.': 'SCHEMA_STATUS', 'Text is missing or exceeds its bound.': 'SCHEMA_TEXT_BOUND', 'Invalid Unicode text.': 'SCHEMA_UNICODE', 'Possible secret: synthetic data only; import refused.': 'SCHEMA_SECRET_REFUSED', 'Invalid identifier.': 'SCHEMA_IDENTIFIER', 'Analysis list out of bounds.': 'SCHEMA_LIST_BOUND', 'Source hash mismatch.': 'SOURCE_HASH_MISMATCH', 'Duplicate hypothesis id.': 'SCHEMA_DUPLICATE_HYPOTHESIS', 'Invalid assessment.': 'SCHEMA_ASSESSMENT', 'Citation list out of bounds.': 'CITATION_LIST_BOUND', 'Citation identifier, source hash or exact full-event quote mismatch.': 'CITATION_MISMATCH', 'Missing remediation conditions.': 'REMEDIATION_CONDITIONS', 'Unknown cases must abstain.': 'ABSTENTION_UNKNOWN', 'Unrecognized case did not abstain.': 'ABSTENTION_UNRECOGNIZED', 'Reference conclusion or uncertainty mismatch.': 'REFERENCE_UNCERTAINTY', 'Reference evidence polarity mismatch.': 'REFERENCE_POLARITY', 'Required missing evidence was not requested.': 'UNCERTAINTY_MISSING_REQUIRED', 'Unexpected reference missing-evidence result.': 'REFERENCE_MISSING_UNEXPECTED', 'A provider hypothesis cannot claim reference validation.': 'CLAIM_REFERENCE', 'Uncertainty must identify evidence still needed.': 'UNCERTAINTY_MISSING'}
PRODUCT_REASON_CODES214 = frozenset(PRODUCT_REASON_MESSAGES214.values()) | {'GENERIC_UNCLASSIFIED'}


def product_reason214(exc):
    """Return only a reviewed code; never stringify or retain exception data."""
    from verifier import VerificationError
    if type(exc) is not VerificationError:
        return 'GENERIC_UNCLASSIFIED'
    args = exc.args
    if type(args) is tuple and len(args) == 1 and type(args[0]) is str:
        return PRODUCT_REASON_MESSAGES214.get(args[0], 'GENERIC_UNCLASSIFIED')
    return 'GENERIC_UNCLASSIFIED'


def failure_code(exc, provider):
    from verifier import VerificationError
    if isinstance(exc, VerificationError):
        return 'PRODUCT_VERIFICATION_REJECTED'
    if isinstance(exc, provider.ProviderError):
        return str(exc) if str(exc) in SAFE_PROVIDER_CODES else 'PROVIDER_FAILURE'
    if isinstance(exc, Refusal):
        return str(exc) if str(exc) in SAFE_REFUSAL_CODES else 'APPLICATION_REFUSAL'
    return 'APPLICATION_FAILURE'


class ApplicationCapture:
    """In-process application originals only; no native custody or escrow claim."""
    scope = 'SYNTHETIC_ONLY'

    def __init__(self):
        self.originals = []
        self.bytes_seen = 0

    def retain(self, stage, kind, value):
        self.originals.append((stage, kind, value))
        if len(self.originals) > 96:
            raise Refusal('APPLICATION_CAPTURE_COUNT')
        if isinstance(value, bytes):
            self.bytes_seen += len(value)
            if len(value) > MAX_RESPONSE + 1 or self.bytes_seen > MAX_RESPONSE * 2 + 2:
                raise Refusal('APPLICATION_CAPTURE_BYTES')

    def status(self):
        return next((v for _, k, v in self.originals if k == 'HTTP_STATUS'), None)

    def original_body(self):
        return next((v for _, k, v in self.originals if k == 'BYTES'), None)


def execute(raw, fixture, provider, build_record, key, caller, *, factory=http.client.HTTPSConnection):
    req = request_guard(raw)
    bind_input(raw, fixture)
    if not key or '\n' in key or '\r' in key:
        raise Refusal('CREDENTIAL_REFERENCE_UNAVAILABLE')
    capture = ApplicationCapture()
    boundary = provider.HTTPBoundary(time.monotonic() + 45.0, capture, factory=factory)
    result = {'profile': PROFILE, 'native_attestation': False, 'native_custody': False,
              'request_sha256': REQUEST_SHA, 'request_bytes': REQUEST_BYTES,
              'source_and_run_declared_by_runner': caller, 'model_requested': MODEL,
              'project': provider.EXPECTED_PROJECT_ID, 'platform': 'Nebius Token Factory',
              'credit_reservation_USD': str(RESERVE_USD), 'new_cash_authorized_USD': '0',
              'paid_continuation_authorized': False, 'input_bound_proposed': INPUT_UPPER_BOUND,
              'output_parameter': OUTPUT_CAP, 'request_attempted': False,
              'outcome': 'NOT_STARTED', 'retry': False,
              'verification_stage': 'PRE_HTTP', 'billed_cost_USD': 'UNKNOWN_NOT_PROVIDER_RECONCILED'}
    try:
        result['verification_stage'] = 'TRANSPORT'
        body = boundary.exchange(raw, key, provider.EXPECTED_PROJECT_ID)
        result['verification_stage'] = 'DECODE_MODEL_USAGE'
        analysis, metadata = provider.decode_response(body, MODEL)
        metadata['request_sha256'] = REQUEST_SHA
        used = metadata['usage']
        if used['prompt_tokens'] > INPUT_UPPER_BOUND:
            raise Refusal('ACTUAL_USAGE_EXCEEDS_ADMITTED_BOUND')
        cost = (Decimal(used['prompt_tokens']) * Decimal('0.06')
                + Decimal(used['completion_tokens']) * Decimal('0.24')) / Decimal(1000000)
        if cost > RESERVE_USD:
            raise Refusal('ACTUAL_METER_ESTIMATE_EXCEEDS_RESERVED_CREDIT')
        result.update(model_reported=metadata['model'], usage=used,
                      model_usage_scope='VALIDATED_BOUNDED_METADATA_NOT_PRODUCT_ACCEPTANCE',
                      metered_cost_estimate_USD=str(cost))
        result['verification_stage'] = 'PRODUCT_RECORD'
        dossier = build_record(fixture, analysis, metadata)
        result.update(outcome='KNOWN_TERMINAL_PRODUCT_RECORD_VERIFIED',
                      model_reported=metadata['model'], usage=used,
                      metered_cost_estimate_USD=str(cost), billed_cost_USD='UNKNOWN_UNLESS_PROVIDER_REPORTS',
                      response_sha256=hashlib.sha256(body).hexdigest(),
                      provider_record=dossier)
    except Exception as exc:
        safe = failure_code(exc, provider)
        result['failure_code'] = safe
        if safe == 'PRODUCT_VERIFICATION_REJECTED':
            result['verification_reason_code'] = product_reason214(exc)
        result['outcome'] = ('KNOWN_TERMINAL_REFUSAL_OR_INVALID_PRODUCT_RESPONSE'
                             if type(capture.status()) is int and type(capture.original_body()) is bytes
                             and len(capture.original_body()) <= MAX_RESPONSE
                             and not safe.endswith('UNKNOWN')
                             and not (boundary.first_primary or '').endswith('UNKNOWN')
                             else 'UNKNOWN_CONSUMED_NO_RETRY')
    finally:
        result['request_attempted'] = boundary.request_attempted
        result['HTTP_status'] = capture.status()
        result['primary_transport_code'] = (boundary.first_primary if boundary.first_primary in SAFE_PROVIDER_CODES
                                            else 'TRANSPORT_UNKNOWN' if boundary.first_primary else None)
        result['original_response_bytes'] = (len(capture.original_body())
                                             if capture.original_body() is not None else None)
        result['application_capture_entries'] = len(capture.originals)
        original = capture.original_body()
        if type(original) is bytes:
            result['captured_response_bytes'] = len(original)
            result['captured_body_scope'] = ('BOUNDED_CAPTURE' if len(original) <= MAX_RESPONSE
                                              else 'BOUNDED_PREFIX_NOT_COMPLETE_RESPONSE')
            digest = hashlib.sha256(original).hexdigest()
            result['raw_response_sha256' if len(original) <= MAX_RESPONSE
                   else 'bounded_prefix_sha256'] = digest
        result['once_scope'] = 'External create-only Git branch + sole reserved caller; no filesystem marker/global exactly-once claim'
    return result


def main():
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))
    import nebius
    from live_service import build_record
    # All data binding and caller checks precede access to the secret reference.
    try:
        raw = (root/'offline103/request.json').read_bytes()
        package = input_for_request(raw)
        bind_input(raw, package)
        ctx = {k: os.environ.get(k) for k in (
            'GITHUB_REPOSITORY', 'GITHUB_REPOSITORY_ID', 'GITHUB_ACTOR_ID', 'GITHUB_EVENT_NAME',
            'GITHUB_REF', 'GITHUB_RUN_ATTEMPT', 'TRACE214_APP_PROFILE', 'GITHUB_SHA', 'GITHUB_RUN_ID')}
        event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_bytes())
        caller = caller_guard(ctx, event)
    except (ValueError, KeyError, OSError):
        print('TRACE214_APP_RESULT=' + json.dumps(
            {'profile': PROFILE, 'verification_stage': 'PRE_SECRET',
             'failure_code': 'PREFLIGHT_REJECTED', 'request_attempted': False, 'retry': False}))
        return 1
    key = os.environ.get('NEBIUS_API_KEY')
    try:
        result = execute(raw, package, nebius, build_record, key, caller)
    except Refusal:
        result = {'profile': PROFILE, 'verification_stage': 'PRE_HTTP',
                  'failure_code': 'PRE_HTTP_REFUSED', 'request_attempted': False, 'retry': False}
    print('TRACE214_APP_RESULT=' + json.dumps(result, ensure_ascii=False, separators=(',', ':')))
    return 0 if result.get('outcome') == 'KNOWN_TERMINAL_PRODUCT_RECORD_VERIFIED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
