"""New recovery334 tests only: in-memory HTTPS fakes, no socket/provider/old runner."""
import copy
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import core
import runtime_service as rt
import app

FAKE_KEY = 'mock-private-credential-334-not-a-real-key'
INPUT = core.canonical({'schema': 'traceharbor.input.v1', 'synthetic': True,
    'case_id': 'recovery334', 'title': 'New bounded runtime bridge fixture',
    'sources': [{'id': 'audit334', 'kind': 'audit', 'title': 'Synthetic observation',
        'events': [{'id': 'event334', 'text': 'Synthetic queue became amber; no cause is supplied.',
                    'timestamp': '2031-04-01T12:00:00Z'}]}]})


def analysis():
    return {'status': 'unknown', 'summary': 'Insufficient evidence for a causal hypothesis.',
            'hypotheses': [], 'missing_evidence': ['Independent causal configuration.'], 'remediation': []}


def response(result=None, **updates):
    body = {'model': rt.MODEL, 'choices': [{'finish_reason': 'stop',
            'message': {'content': json.dumps(analysis() if result is None else result)}}],
            'usage': {'prompt_tokens': 100, 'completion_tokens': 50, 'total_tokens': 150}}
    body.update(updates)
    return core.canonical(body)


class FakeResponse:
    def __init__(self, body, status=200): self.body, self.status = body, status
    def getheader(self, name):
        return 'application/json' if name == 'Content-Type' else str(len(self.body))
    def read(self, size): return self.body[:size]


class FakeFactory:
    def __init__(self, body=None, fault=None, status=200):
        self.body = response() if body is None else body
        self.fault, self.status = fault, status
        self.constructs = self.posts = self.closes = 0
        self.paths = []; self.timeouts = []
    def __call__(self, host, timeout):
        assert host == 'api.tokenfactory.nebius.com'
        self.constructs += 1; self.timeouts.append(timeout)
        owner = self
        class Connection:
            sock = None
            def request(self, method, path, payload, headers):
                owner.posts += 1; owner.paths.append(path)
                assert method == 'POST'
                assert headers['Authorization'] == 'Bearer ' + FAKE_KEY
                assert json.loads(payload)['model'] == rt.MODEL
                if owner.fault: raise owner.fault
            def getresponse(self): return FakeResponse(owner.body, owner.status)
            def close(self): owner.closes += 1
        return Connection()


class Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='trace334-new-fixture-')
        self.directory = Path(self.temp.name); os.chmod(self.directory, 0o700)
        self.pin = core.digest(rt.prepare(INPUT)[1])
    def tearDown(self): self.temp.cleanup()
    def admitted_mock(self, factory=None, environment=None):
        factory = FakeFactory() if factory is None else factory
        session = rt.RuntimeSession(_factory=factory,
            _environment={'NEBIUS_API_KEY': FAKE_KEY} if environment is None else environment,
            _state_directory=self.directory)
        # Test-process-only simulation. Real sockets are denied by the outer audit guard.
        return session, factory
    def dispatch_mock(self, session, raw=INPUT):
        with patch.object(rt, 'GLOBAL_NEW_CALL_CAP', 1), patch.object(rt, 'REVIEWED_REQUEST_SHA256', self.pin):
            return session.dispatch(raw)
    def test_01_cap_zero_before_secret_reservation_and_transport(self):
        class DenyEnv:
            def get(self, *_): raise AssertionError('Credential lookup forbidden at cap0')
        session, factory = self.admitted_mock(environment=DenyEnv())
        with self.assertRaisesRegex(rt.RuntimeRefusal, 'NEW_CALL_CAP_ZERO'): session.dispatch(INPUT)
        self.assertEqual(factory.constructs, 0); self.assertEqual(list(self.directory.iterdir()), [])
    def test_02_env_and_request_cannot_enable_cap_zero(self):
        session, factory = self.admitted_mock(environment={'NEBIUS_API_KEY': FAKE_KEY, 'GLOBAL_NEW_CALL_CAP': '1'})
        with self.assertRaises(rt.RuntimeRefusal): session.dispatch(INPUT)
        self.assertEqual(factory.posts, 0)
    def test_03_missing_key_no_dispatch_or_reservation(self):
        session, factory = self.admitted_mock(environment={})
        with self.assertRaisesRegex(rt.RuntimeRefusal, 'CREDENTIAL_NOT_CONFIGURED'): self.dispatch_mock(session)
        self.assertEqual(factory.constructs, 0); self.assertEqual(list(self.directory.iterdir()), [])
    def test_04_request_pin_required(self):
        session, factory = self.admitted_mock()
        with patch.object(rt, 'GLOBAL_NEW_CALL_CAP', 1):
            with self.assertRaisesRegex(rt.RuntimeRefusal, 'EXACT_REQUEST_NOT_ADMITTED'): session.dispatch(INPUT)
        self.assertEqual(factory.posts, 0)
    def test_05_complete_mock_pipeline_and_separate_wrapper(self):
        session, factory = self.admitted_mock(); result = self.dispatch_mock(session)
        self.assertEqual(result['schema'], rt.SCHEMA)
        self.assertEqual(result['record']['analysis']['status'], 'unknown')
        self.assertEqual(result['record']['verification']['semantic_reference'], 'NOT_VERIFIED')
        self.assertEqual(result['record']['live_api'], 'RECORDED_NOT_INDEPENDENTLY_ATTESTED')
        self.assertEqual(rt.verify_runtime_result(result), result)
        self.assertEqual(factory.posts, 1); self.assertEqual(factory.closes, 1)
        self.assertEqual(factory.paths, ['/v1/chat/completions?ai_project_id=' + rt.nebius.EXPECTED_PROJECT_ID])
        self.assertTrue(all(0 < t <= 30 for t in factory.timeouts))
    def test_06_invalid_citation_rejected_no_retry(self):
        ev = rt.prepare(INPUT)[0]; citation = core.citation(ev, 'audit334', 'event334')
        citation['quote'] = 'Not the actual quote'
        a = analysis(); a.update(status='uncertain', hypotheses=[{'id': 'hyp334', 'label': 'Unresolved cause',
            'assessment': 'uncertain', 'supports': [citation], 'contradicts': []}])
        session, factory = self.admitted_mock(FakeFactory(response(a)))
        with self.assertRaises(rt.RuntimeRefusal): self.dispatch_mock(session)
        with self.assertRaises(rt.RuntimeRefusal): self.dispatch_mock(session)
        self.assertEqual(factory.posts, 1)
    def test_07_timeout_unknown_no_retry_or_secret_leak(self):
        session, factory = self.admitted_mock(FakeFactory(fault=TimeoutError(FAKE_KEY)))
        with self.assertRaises(rt.RuntimeRefusal) as failure: self.dispatch_mock(session)
        self.assertTrue(failure.exception.consumed)
        self.assertEqual(failure.exception.public()['effect'], 'UNKNOWN_CONSUMED_NO_RETRY')
        self.assertNotIn(FAKE_KEY, json.dumps(failure.exception.public()))
        with self.assertRaises(rt.RuntimeRefusal): self.dispatch_mock(session)
        self.assertEqual(factory.posts, 1); self.assertEqual(factory.closes, 1)
        for p in self.directory.iterdir(): self.assertNotIn(FAKE_KEY, p.read_text())
    def test_08_restart_existing_marker_blocks_second_factory(self):
        session, factory = self.admitted_mock(); self.dispatch_mock(session)
        other, factory2 = self.admitted_mock()
        with self.assertRaisesRegex(rt.RuntimeRefusal, 'ALREADY_RESERVED_NO_RETRY'): self.dispatch_mock(other)
        self.assertEqual(factory2.constructs, 0)
    def test_09_truncation_and_model_mismatch_reject(self):
        for body in [response(model='nvidia/wrong'), response(choices=[{'finish_reason': 'length', 'message': {'content': '{}'}}])]:
            directory = self.directory / str(len(list(self.directory.iterdir()))); directory.mkdir(mode=0o700)
            session, factory = self.admitted_mock(FakeFactory(body)); session._directory = directory
            with self.assertRaises(rt.RuntimeRefusal): self.dispatch_mock(session)
            self.assertEqual(factory.posts, 1)
    def test_10_provider_secret_echo_never_returned_or_persisted(self):
        a = analysis(); a['summary'] = FAKE_KEY
        session, factory = self.admitted_mock(FakeFactory(response(a)))
        with self.assertRaises(rt.RuntimeRefusal) as failure: self.dispatch_mock(session)
        self.assertNotIn(FAKE_KEY, str(failure.exception))
        for p in self.directory.iterdir(): self.assertNotIn(FAKE_KEY, p.read_text())
    def test_11_response_and_request_bounds(self):
        session, factory = self.admitted_mock(FakeFactory(b'x' * (rt.MAX_RESULT + 1)))
        with self.assertRaises(rt.RuntimeRefusal): self.dispatch_mock(session)
        huge = json.loads(INPUT); huge['sources'][0]['events'] *= 201
        with self.assertRaises(ValueError): rt.prepare(core.canonical(huge))
    def test_12_import_hash_and_mode_tampering_rejected(self):
        session, _ = self.admitted_mock(); result = self.dispatch_mock(session)
        for key, value in [('mode', 'LIVE_ORIGIN_ATTESTED'), ('dossier_sha256', '0' * 64)]:
            changed = copy.deepcopy(result); changed[key] = value
            with self.assertRaises(ValueError): rt.verify_runtime_result(changed)
    def test_13_http_route_integration_cap_zero(self):
        from email.message import Message
        from types import SimpleNamespace
        class Handler(app.Handler):
            def __init__(self):
                self.path = '/runtime/analyze'; self.headers = Message()
                self.headers['Host'] = '127.0.0.1:8787'
                self.headers['Content-Type'] = 'application/json'
                self.headers['Content-Length'] = str(len(INPUT))
                self.server = SimpleNamespace(server_port=8787)
                self.connection = SimpleNamespace(settimeout=lambda _: None)
                self.rfile = io.BytesIO(INPUT); self.answer = None
            def respond(self, code, body, content_type=None): self.answer = code, json.loads(body)
        h = Handler(); h.do_POST()
        self.assertEqual(h.answer[0], 403); self.assertEqual(h.answer[1]['error'], 'NEW_CALL_CAP_ZERO')
        self.assertEqual(h.answer[1]['effect'], 'KNOWN_NO_DISPATCH')
    def test_14_status_is_data_only_no_credentials(self):
        self.assertFalse(rt.status()['enabled']); self.assertEqual(rt.status()['new_call_cap'], 0)
        self.assertNotIn('key', json.dumps(rt.status()).lower())
    def test_15_private_state_refuses_public_or_symlink(self):
        os.chmod(self.directory, 0o755)
        session, factory = self.admitted_mock()
        with self.assertRaisesRegex(rt.RuntimeRefusal, 'PRIVATE_STATE_NOT_QUALIFIED'): self.dispatch_mock(session)
        self.assertEqual(factory.constructs, 0); os.chmod(self.directory, 0o700)
        link = self.directory / 'link'; link.symlink_to(self.directory, target_is_directory=True)
        with self.assertRaises(rt.RuntimeRefusal): rt._private_directory(link)
    def test_16_input_cannot_override_endpoint_or_model(self):
        modified = json.loads(INPUT); modified['endpoint'] = 'https://example.invalid/'
        with self.assertRaises(ValueError): rt.prepare(core.canonical(modified))
        payload = rt.prepare(INPUT)[1]
        self.assertEqual(payload['model'], rt.MODEL); self.assertEqual(payload['max_completion_tokens'], 1500)
    def test_17_unknown_must_abstain(self):
        a = analysis(); a['hypotheses'] = [{'id': 'bad', 'label': 'Invented', 'assessment': 'uncertain', 'supports': [], 'contradicts': []}]
        session, factory = self.admitted_mock(FakeFactory(response(a)))
        with self.assertRaises(rt.RuntimeRefusal): self.dispatch_mock(session)
        self.assertEqual(factory.posts, 1)
    def test_18_ambiguous_reservation_stays_consumed_without_file(self):
        session, factory = self.admitted_mock()
        with patch.object(rt, '_write_exclusive', side_effect=OSError('Synthetic reservation fault')):
            with self.assertRaisesRegex(rt.RuntimeRefusal, 'RESERVATION_UNKNOWN'): self.dispatch_mock(session)
        self.assertEqual(list(self.directory.iterdir()), [])
        with self.assertRaisesRegex(rt.RuntimeRefusal, 'ALREADY_RESERVED_NO_RETRY'): self.dispatch_mock(session)
        self.assertEqual(factory.constructs, 0)
    def test_19_explicit_code_pin_status_keeps_default_zero(self):
        self.assertFalse(rt.status()['enabled'])
        with patch.object(rt, 'GLOBAL_NEW_CALL_CAP', 1), patch.object(rt, 'REVIEWED_REQUEST_SHA256', self.pin):
            self.assertTrue(rt.status()['enabled'])
        self.assertEqual(rt.GLOBAL_NEW_CALL_CAP, 0); self.assertIsNone(rt.REVIEWED_REQUEST_SHA256)

    def test_20_escaped_secret_echo_rejected_after_decode(self):
        a = analysis(); a['summary'] = FAKE_KEY
        raw = response(a).replace(FAKE_KEY.encode(), ('\\u006d' + FAKE_KEY[1:]).encode())
        self.assertNotIn(FAKE_KEY.encode(), raw)
        session, factory = self.admitted_mock(FakeFactory(raw))
        with self.assertRaises(rt.RuntimeRefusal) as failure: self.dispatch_mock(session)
        self.assertNotIn(FAKE_KEY, str(failure.exception))
        for p in self.directory.iterdir(): self.assertNotIn(FAKE_KEY, p.read_text())

if __name__ == '__main__': unittest.main(verbosity=2)
