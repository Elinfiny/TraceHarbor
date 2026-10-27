"""New214 diagnostic cases only. No old13 suite, credentials or HTTP."""
import copy
import hashlib
import http.client
import importlib.util
import json
import os
from pathlib import Path
import socket
import sys
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import core
import nebius
from live_service import build_record
from verifier import VerificationError
spec = importlib.util.spec_from_file_location('app214', ROOT/'tools/app_runtime214.py')
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)
RAW = (ROOT/'offline103/request.json').read_bytes()
PACKAGE = app.input_for_request(RAW)
EVIDENCE = core.import_package(PACKAGE)
SENTINEL = 'PRIVATE_DYNAMIC_MODEL_TEXT_DO_NOT_EMIT_214'
OBS = {'boundary_replays': 0, 'network_or_HTTP': 0, 'secret_reads': 0}


def forbidden(*args, **kwargs):
    raise AssertionError('HTTP_OR_SECRET_LOOKUP_FORBIDDEN214')


def valid_analysis():
    source = EVIDENCE['sources'][0]
    event = source['events'][0]
    return {'status': 'uncertain', 'summary': 'Synthetic evidence needs independent timing.',
            'hypotheses': [{'id': 'timing-observation', 'label': 'Unresolved timing',
                            'assessment': 'uncertain',
                            'supports': [core.citation(EVIDENCE, source['id'], event['id'])],
                            'contradicts': []}],
            'missing_evidence': ['Independent scheduler timing.'], 'remediation': []}


def offline_execute(analysis, builder=build_record):
    body = core.canonical({'model': app.MODEL,
                           'usage': {'prompt_tokens': 1335, 'completion_tokens': 1228,
                                     'total_tokens': 2563},
                           'choices': [{'finish_reason': 'stop',
                                        'message': {'content': json.dumps(analysis)}}]})

    class ReplayBoundary:
        # Local bytes, not an HTTPBoundary, request, factory or native receipt.
        def __init__(self, deadline, capture, **kwargs):
            self.capture = capture
            self.request_attempted = False
            self.first_primary = None
        def exchange(self, raw, credential, project):
            if raw != RAW or credential != 'SYNTHETIC_NONCREDENTIAL214':
                raise AssertionError('REPLAY_INPUT')
            self.capture.retain('OFFLINE_REPLAY', 'HTTP_STATUS', 200)
            self.capture.retain('OFFLINE_REPLAY', 'BYTES', body)
            OBS['boundary_replays'] += 1
            return body

    provider = types.SimpleNamespace(HTTPBoundary=ReplayBoundary,
                                     ProviderError=nebius.ProviderError,
                                     EXPECTED_PROJECT_ID=nebius.EXPECTED_PROJECT_ID,
                                     decode_response=nebius.decode_response)
    with patch.object(http.client, 'HTTPSConnection', side_effect=forbidden), \
            patch.object(socket, 'socket', side_effect=forbidden), \
            patch.object(os, 'getenv', side_effect=forbidden):
        result = app.execute(RAW, PACKAGE, provider, builder, 'SYNTHETIC_NONCREDENTIAL214',
                             {'scope': 'SYNTHETIC214_NO_RUNNER_OR_NATIVE_AUTHORITY'},
                             factory=forbidden)
    return result, body


class Diagnostic214(unittest.TestCase):
    def test_01_static_whitelist_maps_distinct_safe_codes(self):
        self.assertGreaterEqual(len(app.PRODUCT_REASON_MESSAGES214), 20)
        self.assertEqual(len(set(app.PRODUCT_REASON_MESSAGES214.values())),
                         len(app.PRODUCT_REASON_MESSAGES214))
        for message, code in app.PRODUCT_REASON_MESSAGES214.items():
            with self.subTest(code=code):
                self.assertEqual(app.product_reason214(VerificationError(message)), code)
                self.assertRegex(code, r'^[A-Z][A-Z0-9_]{2,63}$')
                self.assertIn(code, app.PRODUCT_REASON_CODES214)

    def test_02_dynamic_sensitive_nonstring_or_subclass_falls_back_without_stringifying(self):
        class Hostile(VerificationError):
            def __str__(self):
                raise AssertionError('MUST_NOT_STRINGIFY')
        values = [VerificationError(SENTINEL),
                  VerificationError('Object fields do not match the documented schema. '+SENTINEL),
                  VerificationError('Duplicate JSON key: '+SENTINEL),
                  VerificationError(), VerificationError({'sensitive': SENTINEL}),
                  VerificationError('two', SENTINEL), Hostile(SENTINEL),
                  ValueError(SENTINEL)]
        for exc in values:
            with self.subTest(exception_type=type(exc).__name__):
                code = app.product_reason214(exc)
                self.assertEqual(code, 'GENERIC_UNCLASSIFIED')
                self.assertNotIn(SENTINEL, code)

    def test_03_real_product_refusals_are_unchanged_and_granular_with_metadata(self):
        cases = []
        a = valid_analysis(); a.pop('summary')
        cases.append(('schema', a, 'SCHEMA_FIELDS'))
        a = valid_analysis(); a['hypotheses'][0]['supports'][0]['quote'] += ' altered'
        cases.append(('citation', a, 'CITATION_MISMATCH'))
        a = valid_analysis(); a['missing_evidence'] = []
        cases.append(('uncertainty', a, 'UNCERTAINTY_MISSING'))
        a = valid_analysis(); a['hypotheses'][0]['assessment'] = 'supported_reference'
        cases.append(('reference_claim', a, 'CLAIM_REFERENCE'))
        a = valid_analysis(); a['status'] = 'unknown'
        cases.append(('abstention', a, 'ABSTENTION_UNKNOWN'))
        a = valid_analysis()
        a['remediation'] = [{'id': 'observe-only', 'proposal': 'Observe timing.',
                             'preconditions': [], 'risk': 'No action executes.',
                             'rollback': 'Discard proposal.', 'verification': ['Check evidence.']}]
        cases.append(('remediation', a, 'REMEDIATION_CONDITIONS'))
        for name, analysis, expected in cases:
            with self.subTest(reason=name):
                with self.assertRaises(VerificationError):
                    build_record(PACKAGE, analysis, {
                        'endpoint': nebius.ENDPOINT, 'model': app.MODEL,
                        'usage': {'prompt_tokens':1335,'completion_tokens':1228,'total_tokens':2563},
                        'response_sha256':'0'*64, 'request_sha256':app.REQUEST_SHA,
                        'finish_reason':'stop'})
                result, body = offline_execute(analysis)
                self.assertEqual(result['failure_code'], 'PRODUCT_VERIFICATION_REJECTED')
                self.assertEqual(result['verification_reason_code'], expected)
                self.assertEqual(result['verification_stage'], 'PRODUCT_RECORD')
                self.assertEqual(result['model_reported'], app.MODEL)
                self.assertEqual(result['usage'], {'prompt_tokens':1335,'completion_tokens':1228,
                                                   'total_tokens':2563})
                self.assertEqual(result['raw_response_sha256'], hashlib.sha256(body).hexdigest())
                self.assertEqual(result['original_response_bytes'], len(body))
                self.assertEqual(result['captured_body_scope'], 'BOUNDED_CAPTURE')
                self.assertEqual(result['metered_cost_estimate_USD'], '0.00037482')
                self.assertEqual(result['billed_cost_USD'], 'UNKNOWN_NOT_PROVIDER_RECONCILED')
                self.assertFalse(result['request_attempted'])
                self.assertFalse(result['retry'])
                self.assertNotIn('provider_record', result)
                self.assertNotIn('altered', json.dumps(result))
                self.assertFalse(any(k in result for k in ('raw_body','headers','reasoning')))

    def test_04_valid_product_still_creates_a_verified_record(self):
        result, body = offline_execute(valid_analysis())
        self.assertEqual(result['outcome'], 'KNOWN_TERMINAL_PRODUCT_RECORD_VERIFIED')
        self.assertEqual(result['provider_record']['schema'], 'traceharbor.provider-record.v1')
        self.assertEqual(result['provider_record']['evidence']['input_sha256'], app.RAW_INPUT_SHA)
        self.assertEqual(result['response_sha256'], hashlib.sha256(body).hexdigest())
        self.assertNotIn('failure_code', result)
        self.assertNotIn('verification_reason_code', result)
        self.assertFalse(result['request_attempted'])

    def test_05_runtime_dynamic_reason_falls_back_without_leaking(self):
        def reject(*args):
            raise VerificationError(SENTINEL)
        result, body = offline_execute(valid_analysis(), reject)
        self.assertEqual(result['verification_reason_code'], 'GENERIC_UNCLASSIFIED')
        self.assertEqual(result['failure_code'], 'PRODUCT_VERIFICATION_REJECTED')
        self.assertNotIn(SENTINEL, json.dumps(result))
        self.assertEqual(result['raw_response_sha256'], hashlib.sha256(body).hexdigest())
        self.assertEqual(result['usage']['total_tokens'], 2563)

    def test_06_nonproduct_exception_is_not_misclassified_or_logged(self):
        def reject(*args):
            raise RuntimeError(SENTINEL)
        result, _ = offline_execute(valid_analysis(), reject)
        self.assertEqual(result['failure_code'], 'APPLICATION_FAILURE')
        self.assertNotIn('verification_reason_code', result)
        self.assertNotIn(SENTINEL, json.dumps(result))
        self.assertEqual(result['model_reported'], app.MODEL)

    def test_07_exact_input_identity_and_limits_retained(self):
        self.assertEqual(len(PACKAGE), 598)
        self.assertEqual(hashlib.sha256(PACKAGE).hexdigest(), app.RAW_INPUT_SHA)
        self.assertEqual(hashlib.sha256(RAW).hexdigest(), app.REQUEST_SHA)
        self.assertEqual((app.REQUEST_BYTES,app.INPUT_UPPER_BOUND,app.OUTPUT_CAP,
                          app.MAX_RESPONSE,str(app.RESERVE_USD)),(4935,2000000,1500,262144,'0.25'))
        self.assertEqual(app.PROFILE, 'APP_RUNTIME_DIAGNOSTIC214')
        self.assertTrue(app.BRANCH.startswith('traceharbor/diag214/v1/e4b08fa3937e4c83-'))

if __name__ == '__main__':
    unittest.main()
