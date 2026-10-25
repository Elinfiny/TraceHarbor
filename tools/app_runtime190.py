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

PROFILE = 'APP_RUNTIME_NO_NATIVE_ATTESTATION'
MODEL = 'nvidia/Nemotron-3_5-Lightning'
REQUEST_SHA = 'e4b08fa3937e4c8348383a5abf934ffbf3832183fadc2907018adbc4a04a71b2'
REQUEST_BYTES = 4935
BRANCH = 'traceharbor/app190/v1/e4b08fa3937e4c83'
BASE = 'dadb8ddf69c7884489ca438c28253cdd915f94e3'
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
                'TRACE190_APP_PROFILE': PROFILE}
    if any(ctx.get(k) != v for k, v in expected.items()):
        raise Refusal('CALLER_PROFILE_NOT_ADMITTED')
    if event.get('ref') != BRANCH or event.get('ref_type') != 'branch':
        raise Refusal('CREATE_EVENT_MISMATCH')
    if (not re.fullmatch('[0-9a-f]{40}', ctx.get('GITHUB_SHA', ''))
            or not re.fullmatch('[1-9][0-9]*', ctx.get('GITHUB_RUN_ID', ''))):
        raise Refusal('RUN_SOURCE_ID_INVALID')
    return {k: ctx[k] for k in (*expected, 'GITHUB_SHA', 'GITHUB_RUN_ID')}


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
              'outcome': 'NOT_STARTED', 'retry': False}
    try:
        body = boundary.exchange(raw, key, provider.EXPECTED_PROJECT_ID)
        analysis, metadata = provider.decode_response(body, MODEL)
        metadata['request_sha256'] = REQUEST_SHA
        used = metadata['usage']
        if used['prompt_tokens'] > INPUT_UPPER_BOUND:
            raise Refusal('ACTUAL_USAGE_EXCEEDS_ADMITTED_BOUND')
        cost = (Decimal(used['prompt_tokens']) * Decimal('0.06')
                + Decimal(used['completion_tokens']) * Decimal('0.24')) / Decimal(1000000)
        if cost > RESERVE_USD:
            raise Refusal('ACTUAL_METER_ESTIMATE_EXCEEDS_RESERVED_CREDIT')
        dossier = build_record(fixture, analysis, metadata)
        result.update(outcome='KNOWN_TERMINAL_PRODUCT_RECORD_VERIFIED',
                      model_reported=metadata['model'], usage=used,
                      metered_cost_estimate_USD=str(cost), billed_cost_USD='UNKNOWN_UNLESS_PROVIDER_REPORTS',
                      response_sha256=hashlib.sha256(body).hexdigest(),
                      provider_record=dossier)
    except Exception as exc:
        # Never serialize credentials, request headers, arbitrary exception text or tracebacks.
        safe = str(exc) if isinstance(exc, (provider.ProviderError, Refusal)) else ''
        safe = safe if re.fullmatch('[A-Z0-9_]{1,96}', safe) else type(exc).__name__
        result['failure_code'] = safe
        result['outcome'] = ('KNOWN_TERMINAL_REFUSAL_OR_INVALID_PRODUCT_RESPONSE'
                             if type(capture.status()) is int and type(capture.original_body()) is bytes
                             and len(capture.original_body()) <= MAX_RESPONSE
                             and not safe.endswith('UNKNOWN') else 'UNKNOWN_CONSUMED_NO_RETRY')
    finally:
        result['request_attempted'] = boundary.request_attempted
        result['HTTP_status'] = capture.status()
        result['primary_transport_code'] = boundary.first_primary
        result['original_response_bytes'] = (len(capture.original_body())
                                             if capture.original_body() is not None else None)
        result['application_capture_entries'] = len(capture.originals)
        result['once_scope'] = 'External create-only Git branch + sole reserved caller; no filesystem marker/global exactly-once claim'
    return result


def main():
    root = Path(__file__).resolve().parents[1]
    # No import-time network/credential access. No local standalone live mode.
    ctx = {k: os.environ.get(k) for k in (
        'GITHUB_REPOSITORY', 'GITHUB_REPOSITORY_ID', 'GITHUB_ACTOR_ID', 'GITHUB_EVENT_NAME',
        'GITHUB_REF', 'GITHUB_RUN_ATTEMPT', 'TRACE190_APP_PROFILE', 'GITHUB_SHA', 'GITHUB_RUN_ID')}
    raw = (root/'offline103/request.json').read_bytes()
    request_guard(raw)
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_bytes())
    caller = caller_guard(ctx, event)
    sys.path.insert(0, str(root))
    import nebius
    from live_service import build_record
    key = os.environ.get('NEBIUS_API_KEY')  # Existing Actions secret reference; never printed.
    result = execute(raw, (root/'fixtures/complete.json').read_bytes(), nebius,
                     build_record, key, caller)
    print('TRACE190_APP_RESULT=' + json.dumps(result, ensure_ascii=False, separators=(',', ':')))
    return 0 if result['outcome'] == 'KNOWN_TERMINAL_PRODUCT_RECORD_VERIFIED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
