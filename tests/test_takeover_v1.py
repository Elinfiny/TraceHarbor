"""Fresh V1 candidate validation. All provider responses are explicitly synthetic.

No historical suite invocation, real credential, network, or live admission.
"""
import copy
import json
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

import live_probe
from core import canonical, digest, import_package, parse_json
from live_service import verify_import
from nebius import ProviderError
from service import analyze

ROOT = Path(__file__).resolve().parents[1]
MODEL = 'nvidia/SYNTHETIC_TEST_ONLY'


def synthetic_response(case='complete', prompt_tokens=100):
    result = copy.deepcopy(analyze((ROOT/'fixtures'/f'{case}.json').read_bytes())['analysis'])
    if result['status'] == 'supported_reference':
        result['status'] = 'uncertain'
        result['missing_evidence'] = ['Synthetic response; real model semantics unverified.']
    for hypothesis in result['hypotheses']:
        if hypothesis['assessment'] == 'supported_reference':
            hypothesis['assessment'] = 'uncertain'
    return canonical({'model': MODEL, 'choices': [{'finish_reason': 'stop',
        'message': {'content': canonical(result).decode()}}],
        'usage': {'prompt_tokens': prompt_tokens, 'completion_tokens': 100,
                  'total_tokens': prompt_tokens+100}})


class FailStopCandidate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='traceharbor-v1-synthetic-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.permit = self.root/'SYNTHETIC_NOT_A_LIVE_GRANT.json'
        _, requests = live_probe.planned_requests(MODEL)
        self.permit.write_bytes(canonical({
            'schema': 'traceharbor.live-admission.v1',
            'operation_id': 'TRACEHARBOR_THREE_SYNTHETIC_REQUESTS_V1',
            'expires_utc': '2099-01-01T00:00:00Z', 'model': MODEL,
            'request_sha256': [digest(request) for request in requests],
            'input_token_upper_bounds': [3000]*3,
            'input_usd_per_million': '1', 'output_usd_per_million': '1',
            'max_cost_usd': '1',
            **{key: 'SYNTHETIC_TEST_ONLY_NOT_PROVIDER_EVIDENCE' for key in (
                'verified_access_evidence', 'verified_credit_and_cap_evidence',
                'verified_model_license_evidence', 'verified_token_bounds_evidence')}
        }))
        self.env = patch.dict('os.environ', {'NEBIUS_MODEL': MODEL,
            'NEBIUS_API_KEY': 'SYNTHETIC_PLACEHOLDER_NOT_A_CREDENTIAL'})
        self.env.start(); self.addCleanup(self.env.stop)
        self.network = patch.object(socket.socket, 'connect',
            side_effect=AssertionError('REAL NETWORK FORBIDDEN IN V1 TEST'))
        self.network.start(); self.addCleanup(self.network.stop)

    def assert_stop(self, effect, expected_error=None, expected_status='REJECTED_OR_UNKNOWN_NO_RETRY'):
        out = self.root/'output'
        with patch.object(live_probe, 'https_once', side_effect=effect) as transport:
            self.assertEqual(live_probe.execute(self.permit, out), 2)
        self.assertEqual(transport.call_count, 1)
        self.assertTrue(Path(str(self.permit)+'.spent').exists())
        terminal = parse_json((out/'1-terminal.json').read_bytes())
        self.assertEqual(terminal['status'], expected_status)
        if expected_error: self.assertEqual(terminal['error'], expected_error)
        self.assertFalse((out/'2-attempt.json').exists())
        self.assertFalse((out/'3-attempt.json').exists())
        self.assertFalse(parse_json((out/'result.json').read_bytes())['completed_three'])

    def test_unknown_transport_stops_before_second_request(self):
        self.assert_stop(ProviderError('TRANSPORT_OUTCOME_UNKNOWN_NO_RETRY'),
                         'TRANSPORT_OUTCOME_UNKNOWN_NO_RETRY')

    def test_provider_refusal_stops_before_second_request(self):
        response = json.loads(synthetic_response())
        response['choices'][0]['message']['refusal'] = 'Synthetic refusal'
        self.assert_stop([canonical(response)], 'PROVIDER_REFUSAL_OR_TOOL_CALL')

    def test_valid_json_bad_citation_stops_before_second_request(self):
        response = json.loads(synthetic_response())
        analysis = json.loads(response['choices'][0]['message']['content'])
        analysis['hypotheses'][0]['supports'][0]['quote'] += ' altered'
        response['choices'][0]['message']['content'] = canonical(analysis).decode()
        self.assert_stop([canonical(response)], 'VerificationError')

    def test_input_usage_over_bound_stops(self):
        self.assert_stop([synthetic_response(prompt_tokens=3001)],
                         expected_status='TOKEN_BOUND_VIOLATION_STOP')

    def test_three_successful_simulated_responses_are_distinct_and_reimportable(self):
        out = self.root/'output'
        with patch.object(live_probe, 'https_once', side_effect=[
                synthetic_response(case) for case in live_probe.CASES]) as transport:
            self.assertEqual(live_probe.execute(self.permit, out), 0)
        self.assertEqual(transport.call_count, 3)
        hashes = []
        for index, case in enumerate(live_probe.CASES, 1):
            attempt = parse_json((out/f'{index}-attempt.json').read_bytes())
            hashes.append(attempt['request_sha256'])
            record = parse_json((out/f'{case}-dossier.json').read_bytes())
            self.assertEqual(verify_import(record), record)
            self.assertEqual(record['live_api'], 'RECORDED_NOT_INDEPENDENTLY_ATTESTED')
        self.assertEqual(len(set(hashes)), 3)
        self.assertTrue(parse_json((out/'result.json').read_bytes())['completed_three'])

    def test_existing_spent_marker_blocks_all_transport(self):
        marker = Path(str(self.permit)+'.spent')
        marker.write_bytes(b'SYNTHETIC EXISTING RESERVATION')
        with patch.object(live_probe, 'https_once') as transport:
            with self.assertRaises(FileExistsError):
                live_probe.execute(self.permit, self.root/'output')
        transport.assert_not_called()
        self.assertEqual(marker.read_bytes(), b'SYNTHETIC EXISTING RESERVATION')

    def test_terminal_write_failure_preserves_attempt_and_never_advances(self):
        original = live_probe.write_new
        def fail_terminal(path, data):
            if path.name == '1-terminal.json': raise OSError('SYNTHETIC_STORAGE_FAILURE')
            return original(path, data)
        out = self.root/'output'
        with patch.object(live_probe, 'https_once', side_effect=ProviderError('PROVIDER_HTTP_429')) as transport:
            with patch.object(live_probe, 'write_new', side_effect=fail_terminal):
                with self.assertRaises(OSError): live_probe.execute(self.permit, out)
        self.assertEqual(transport.call_count, 1)
        self.assertTrue((out/'1-attempt.json').exists())
        self.assertFalse((out/'1-terminal.json').exists())
        self.assertFalse((out/'2-attempt.json').exists())


class OfflineJourney(unittest.TestCase):
    def test_full_missing_conflicting_quotes_timeline_roundtrip(self):
        expected = {'complete': 'supported_reference', 'missing': 'uncertain',
                    'contradictory': 'conflicted'}
        for case, status in expected.items():
            with self.subTest(case=case):
                record = analyze((ROOT/'fixtures'/f'{case}.json').read_bytes())
                self.assertEqual(record['analysis']['status'], status)
                self.assertEqual(verify_import(parse_json(canonical(record))), record)
                evidence = record['evidence']
                lookup = {(s['id'], e['id']): (s['sha256'], e['text'])
                          for s in evidence['sources'] for e in s['events']}
                for hypothesis in record['analysis']['hypotheses']:
                    for citation in hypothesis['supports']+hypothesis['contradicts']:
                        self.assertEqual((citation['source_sha256'], citation['quote']),
                            lookup[citation['source_id'], citation['event_id']])
                occurrences = {(o['source_id'], o['event_id'])
                    for e in evidence['timeline'] for o in e['occurrences']}
                self.assertEqual(occurrences, set(lookup))

    def test_rehashed_tamper_is_refused_by_reconstruction(self):
        record = analyze((ROOT/'fixtures'/'complete.json').read_bytes())
        record['evidence']['timeline'][0]['text'] += ' tampered'
        record['dossier_sha256'] = digest({k:v for k,v in record.items() if k != 'dossier_sha256'})
        with self.assertRaisesRegex(ValueError, 'Evidence reconstruction mismatch'):
            verify_import(record)

    def test_unknown_input_abstains_and_invalid_input_is_rejected(self):
        fixture = parse_json((ROOT/'fixtures'/'complete.json').read_bytes())
        fixture['sources'][0]['events'][0]['text'] += ' unseen change'
        record = analyze(canonical(fixture))
        self.assertEqual(record['analysis']['status'], 'unknown')
        self.assertEqual(record['analysis']['hypotheses'], [])
        self.assertEqual(record['analysis']['remediation'], [])
        verify_import(record)
        for raw in [b'{"schema":1,"schema":2}', b'\xff', b'x'*262145]:
            with self.assertRaises(ValueError): import_package(raw)


if __name__ == '__main__': unittest.main(verbosity=2)
