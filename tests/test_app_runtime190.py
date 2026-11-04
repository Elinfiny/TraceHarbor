"""Only the new app-wrapper boundary; synthetic transport, no network/credentials."""
import sys
sys.dont_write_bytecode = True
import importlib.util
from importlib.machinery import SourceFileLoader
import json
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get('TRACE190_TEST_SOURCE_ROOT', str(ROOT))).resolve()
PROVIDER = Path(os.environ.get('TRACE190_TEST_PROVIDER_FILE', str(SOURCE/'nebius.py'))).resolve()
REQUEST = Path(os.environ.get('TRACE190_TEST_REQUEST_FILE', str(SOURCE/'offline103/request.json'))).resolve()
sys.path.insert(0, str(SOURCE))

def load(name, p):
    spec = importlib.util.spec_from_loader(name, SourceFileLoader(name, str(p)))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

subject = load('subject190', ROOT/'tools/app_runtime190.py')
provider = load('provider190', PROVIDER)
import service
from live_service import build_record, verify_record


class Response:
    def __init__(self, raw, status):
        self.raw, self.status = raw, status

    def getheader(self, name):
        return 'application/json' if name == 'Content-Type' else str(len(self.raw))

    def read(self, maximum):
        return self.raw[:maximum]


class Connection:
    def __init__(self, response, timeout_post=False):
        self.response, self.timeout_post = response, timeout_post
        self.timeout = 0
        self.sock = None
        self.posts = []
        self.closes = 0

    def request(self, method, path, raw, headers):
        self.posts.append((method, path, raw))  # Never retain dummy Authorization in test report.
        if self.timeout_post:
            raise TimeoutError()

    def getresponse(self):
        return self.response

    def close(self):
        self.closes += 1


class AppRuntime190(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = REQUEST.read_bytes()
        cls.fixture = (SOURCE/'fixtures/complete.json').read_bytes()
        obj = json.loads(cls.fixture)
        obj['sources'][0]['events'][0]['text'] = 'A new synthetic observation outside the known reference.'
        cls.analysis = service.analyze(json.dumps(obj).encode())['analysis']

    def result(self, *, status=200, model=None, prompt=123, completion=11, timeout_post=False, key='fixture-only-key'):
        envelope = {'model': model or subject.MODEL, 'choices': [{'finish_reason': 'stop',
                    'message': {'content': json.dumps(self.analysis)}}],
                    'usage': {'prompt_tokens': prompt, 'completion_tokens': completion,
                              'total_tokens': prompt+completion}}
        connection = Connection(Response(json.dumps(envelope).encode(), status), timeout_post)
        calls = []
        def factory(host, timeout):
            calls.append((host, timeout))
            return connection
        out = subject.execute(self.raw, self.fixture, provider, build_record, key,
                              {'test': 'SYNTHETIC_NOT_NATIVE'}, factory=factory)
        return out, connection, calls

    def test_valid_app_record_reuses_real_transport_decode_and_product_verifier(self):
        out, conn, calls = self.result()
        self.assertEqual(out['outcome'], 'KNOWN_TERMINAL_PRODUCT_RECORD_VERIFIED')
        self.assertFalse(out['native_attestation'])
        self.assertFalse(out['native_custody'])
        self.assertEqual(out['profile'], subject.PROFILE)
        self.assertEqual(out['usage'], {'prompt_tokens':123,'completion_tokens':11,'total_tokens':134})
        self.assertEqual(out['metered_cost_estimate_USD'], '0.00001002')
        self.assertTrue(verify_record(out['provider_record']))
        self.assertEqual(conn.posts[0][2], self.raw)
        self.assertEqual(len(conn.posts), 1)
        self.assertEqual(conn.closes, 1)
        self.assertEqual(calls[0][0], 'api.tokenfactory.nebius.com')

    def test_changed_request_rejected_before_factory(self):
        with self.assertRaisesRegex(subject.Refusal, '^EXACT_REQUEST_REQUIRED$'):
            subject.request_guard(self.raw+b' ')

    def test_request_still_exact_json_object_lightning1500(self):
        req = subject.request_guard(self.raw)
        self.assertEqual(req['model'], subject.MODEL)
        self.assertEqual(req['max_completion_tokens'],1500)
        self.assertFalse(req['stream'])

    def test_absent_secret_refused_before_factory(self):
        with self.assertRaisesRegex(subject.Refusal, '^CREDENTIAL_REFERENCE_UNAVAILABLE$'):
            self.result(key='')

    def test_actual_usage_bound_violation_consumes_known_response(self):
        out, conn, _ = self.result(prompt=2000001)
        self.assertEqual(out['failure_code'],'ACTUAL_USAGE_EXCEEDS_ADMITTED_BOUND')
        self.assertEqual(out['outcome'],'KNOWN_TERMINAL_REFUSAL_OR_INVALID_PRODUCT_RESPONSE')
        self.assertEqual(len(conn.posts),1)
        self.assertNotIn('provider_record',out)

    def test_wrong_model_is_not_integration_success(self):
        out, conn, _ = self.result(model='nvidia/different')
        self.assertEqual(out['failure_code'],'PROVIDER_MODEL_MISMATCH')
        self.assertEqual(len(conn.posts),1)
        self.assertNotIn('provider_record',out)

    def test_output_over1500_refused_and_no_second_post(self):
        out, conn, _ = self.result(completion=1501)
        self.assertEqual(out['failure_code'],'PROVIDER_TOKEN_BOUND_EXCEEDED')
        self.assertEqual(len(conn.posts),1)
        self.assertEqual(conn.closes,1)

    def test_timeout_unknown_consumed_no_retry(self):
        out, conn, _ = self.result(timeout_post=True)
        self.assertEqual(out['outcome'],'UNKNOWN_CONSUMED_NO_RETRY')
        self.assertTrue(out['request_attempted'])
        self.assertEqual(len(conn.posts),1)
        self.assertEqual(conn.closes,1)

    def test_known_provider_refusal_no_retry(self):
        out, conn, _ = self.result(status=403)
        self.assertEqual(out['HTTP_status'],403)
        self.assertEqual(out['failure_code'],'PROVIDER_HTTP_403')
        self.assertEqual(len(conn.posts),1)
        self.assertEqual(conn.closes,1)

    def test_exact_caller_context_and_wrong_attempt(self):
        c={'GITHUB_REPOSITORY':'Elinfiny/TraceHarbor','GITHUB_REPOSITORY_ID':'1391430317',
           'GITHUB_ACTOR_ID':'273768139','GITHUB_EVENT_NAME':'create',
           'GITHUB_REF':'refs/heads/'+subject.BRANCH,'GITHUB_RUN_ATTEMPT':'1',
           'TRACE190_APP_PROFILE':subject.PROFILE,'GITHUB_SHA':'a'*40,'GITHUB_RUN_ID':'123'}
        e={'ref':subject.BRANCH,'ref_type':'branch'}
        self.assertEqual(subject.caller_guard(c,e)['GITHUB_RUN_ID'],'123')
        c['GITHUB_RUN_ATTEMPT']='2'
        with self.assertRaisesRegex(subject.Refusal,'^CALLER_PROFILE_NOT_ADMITTED$'):
            subject.caller_guard(c,e)


if __name__ == '__main__':
    unittest.main()
