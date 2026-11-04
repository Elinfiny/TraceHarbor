"""Only new adapter tests: actual WSGI calls in memory, no HTTP server or network."""
import sys
sys.dont_write_bytecode = True
import argparse
import hashlib
import io
import json
from pathlib import Path
import os
import unittest
from unittest.mock import patch
from wsgiref.validate import validator

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--source-root', type=Path)
parser.add_argument('--case', action='append', default=[])
args, remaining = parser.parse_known_args()
if remaining:
    parser.error('Unexpected test arguments.')
ROOT = Path(__file__).resolve().parents[1]
SOURCE = (args.source_root or ROOT).resolve()
sys.path.insert(0, str(SOURCE))
sys.path.insert(0, str(ROOT))
ACTIVE = [True]
AUDIT_VIOLATIONS = []


def audit(event, values):
    if not ACTIVE[0]:
        return
    forbidden = event in ('socket.__new__', 'socket.connect', 'socket.bind', 'subprocess.Popen',
                           'os.system', 'os.mkdir', 'os.remove', 'os.rename', 'os.rmdir',
                           'os.chmod', 'os.chown', 'os.symlink', 'os.link', 'os.truncate')
    if event == 'open':
        name, mode, flags = values
        forbidden = forbidden or bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        if isinstance(name, (str, bytes)):
            text = os.fsdecode(name)
            forbidden = forbidden or any(x in text for x in ('/.aws/', '/.ssh/'))
            forbidden = forbidden or Path(text).name in ('credentials', 'credentials.json', '.netrc', 'nebius.py', 'live_probe.py')
    if forbidden:
        AUDIT_VIOLATIONS.append(event)
        raise AssertionError('Forbidden adapter side effect: ' + event)


sys.addaudithook(audit)
import app
import core
import service
import live_service
import wsgi177 as subject
ACTIVE[0] = False
OBSERVATIONS = []
ORIGIN = 'https://traceharbor.invalid'


class CounterInput(io.BytesIO):
    def __init__(self, value=b'', forbidden=False):
        super().__init__(value)
        self.calls = []
        self.forbidden = forbidden

    def read(self, size=-1):
        self.calls.append(size)
        if self.forbidden:
            raise AssertionError('Body read before required guard.')
        return super().read(size)


def environment(path='/', method='GET', data=b''):
    value = {'REQUEST_METHOD': method, 'SCRIPT_NAME': '', 'PATH_INFO': path,
             'QUERY_STRING': '', 'SERVER_NAME': 'traceharbor.invalid', 'SERVER_PORT': '443',
             'SERVER_PROTOCOL': 'HTTP/1.1', 'HTTP_HOST': 'traceharbor.invalid',
             'RAW_URI': path, 'wsgi.url_scheme': 'https', 'wsgi.version': (1, 0),
             'wsgi.input': CounterInput(data), 'wsgi.errors': io.StringIO(),
             'wsgi.multithread': False, 'wsgi.multiprocess': False, 'wsgi.run_once': False}
    if method == 'POST':
        value.update(CONTENT_TYPE='application/json', CONTENT_LENGTH=str(len(data)), HTTP_ORIGIN=ORIGIN)
    return value


class WSGI177Tests(unittest.TestCase):
    def setUp(self):
        ACTIVE[0] = True
        self.target = subject.create_application(allowed_origin=ORIGIN)

    def tearDown(self):
        ACTIVE[0] = False
        self.assertEqual(AUDIT_VIOLATIONS, [])

    def request(self, env, target=None, checked=False):
        capture = []
        def start(status, headers, exc_info=None):
            capture.append((status, dict(headers)))
        target = target or self.target
        input_reader = env.get('wsgi.input')
        body = (validator(target) if checked else target)(env, start)
        try:
            chunks = list(body)
            self.assertTrue(all(type(chunk) is bytes for chunk in chunks))
            data = b''.join(chunks)
        finally:
            body.close()
        self.assertEqual(len(capture), 1)
        status, headers = capture[0]
        self.assertEqual(headers['Content-Length'], str(len(data)))
        self.assertEqual(headers['Cache-Control'], 'no-store')
        self.assertEqual(headers['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(headers['Content-Security-Policy'], subject.CSP)
        self.assertNotIn('Access-Control-Allow-Origin', headers)
        OBSERVATIONS.append({'method': env.get('REQUEST_METHOD'), 'path': env.get('PATH_INFO'),
                             'status': int(status[:3]), 'bytes': len(data),
                             'body_read_sizes': getattr(input_reader, 'calls', [])})
        return int(status[:3]), headers, data

    def refuse_before_read(self, changes, code, *, remove=()):
        env = environment('/analyze', 'POST', b'{}')
        env['wsgi.input'] = CounterInput(b'{}', forbidden=True)
        env.update(changes)
        for key in remove:
            env.pop(key, None)
        status, _, data = self.request(env)
        self.assertEqual(status, code)
        self.assertEqual(env['wsgi.input'].calls, [])
        self.assertIn('error', json.loads(data))

    def test_import_has_no_network_keys_or_file_writes(self):
        self.assertTrue(sys.dont_write_bytecode)
        self.assertNotIn('nebius', sys.modules)
        self.assertNotIn('live_probe', sys.modules)
        self.assertEqual(AUDIT_VIOLATIONS, [])
        self.assertEqual(app.STATIC, subject._STATIC_CONTRACT)
        self.assertEqual(frozenset(app.CASES), subject._CASES_CONTRACT)

    def test_default_unconfigured_refuses_before_read(self):
        env = environment('/analyze', 'POST', b'{}')
        env['wsgi.input'] = CounterInput(b'{}', forbidden=True)
        self.assertEqual(self.request(env, target=subject.application)[0], 503)
        self.assertEqual(env['wsgi.input'].calls, [])

    def test_invalid_origin_configuration(self):
        for origin in ('*', 'https://*.invalid', 'ftp://traceharbor.invalid', 'https://traceharbor.invalid/',
                       'https://u:p@traceharbor.invalid', 'https://traceharbor.invalid?x',
                       'https://TRACEHARBOR.invalid', 'https://traceharbor.invalid:0443',
                       'https://traceharbor.invalid:0', True):
            with self.subTest(origin=origin), self.assertRaises(ValueError):
                subject.create_application(allowed_origin=origin)

    def test_six_get_assets_and_fixtures_exact_bytes(self):
        pairs = {'/': 'web/index.html', '/app.js': 'web/app.js', '/style.css': 'web/style.css'}
        pairs.update({'/fixtures/' + n + '.json': 'fixtures/' + n + '.json' for n in app.CASES})
        for path, source in sorted(pairs.items()):
            with self.subTest(path=path):
                code, headers, data = self.request(environment(path), checked=True)
                self.assertEqual(code, 200)
                self.assertEqual(data, (SOURCE/source).read_bytes())
                self.assertEqual(hashlib.sha256(data).hexdigest(), subject.RESOURCE_PINS[source]['sha256'])

    def test_three_analyze_outputs_exact_native_service(self):
        statuses = {'complete': 'supported_reference', 'missing': 'uncertain', 'contradictory': 'conflicted'}
        for case, expected_status in statuses.items():
            raw = (SOURCE/'fixtures'/(case+'.json')).read_bytes()
            native = service.analyze(raw)
            with self.subTest(case=case), patch.object(subject, 'analyze', wraps=subject.analyze) as real:
                code, _, data = self.request(environment('/analyze', 'POST', raw), checked=True)
                self.assertEqual(code, 200)
                self.assertEqual(json.loads(data), native)
                self.assertEqual(native['analysis']['status'], expected_status)
                self.assertEqual(native['mode'], 'DEMO_NO_AI')
                real.assert_called_once_with(raw)

    def test_export_reimport_uses_actual_parse_and_verifier(self):
        raw = (SOURCE/'fixtures/complete.json').read_bytes()
        result = self.request(environment('/analyze', 'POST', raw))[2]
        with patch.object(subject, 'parse_json', wraps=core.parse_json) as parse, patch.object(subject, 'verify_import', wraps=live_service.verify_import) as verify:
            code, _, accepted = self.request(environment('/verify', 'POST', result), checked=True)
            self.assertEqual(code, 200)
            self.assertEqual(json.loads(accepted), json.loads(result))
            parse.assert_called_once_with(result)
            verify.assert_called_once()

    def test_unknown_input_keeps_native_unknown_and_no_diagnosis(self):
        value = json.loads((SOURCE/'fixtures/complete.json').read_bytes())
        value['sources'][0]['events'][0]['text'] = 'A new synthetic observation outside the known reference.'
        raw = json.dumps(value).encode()
        code, _, data = self.request(environment('/analyze', 'POST', raw), checked=True)
        self.assertEqual(code, 200)
        result = json.loads(data)
        self.assertEqual(result, service.analyze(raw))
        self.assertEqual(result['analysis']['status'], 'unknown')
        self.assertEqual(result['analysis']['hypotheses'], [])

    def test_dossier_and_citation_tamper_refused(self):
        dossier = service.analyze((SOURCE/'fixtures/complete.json').read_bytes())
        for field in ('summary', 'citation'):
            value = json.loads(json.dumps(dossier))
            if field == 'summary': value['analysis']['summary'] += ' changed'
            else: value['analysis']['hypotheses'][0]['supports'][0]['quote'] = 'tampered quote'
            with self.subTest(field=field):
                code, _, data = self.request(environment('/verify', 'POST', json.dumps(value).encode()))
                self.assertEqual(code, 400)
                self.assertNotIn(b'tampered quote', data)

    def test_host_origin_scheme_before_body(self):
        for key, value in [('HTTP_HOST', 'other.invalid'), ('HTTP_HOST', 'traceharbor.invalid:443'),
                           ('HTTP_ORIGIN', 'https://other.invalid'), ('HTTP_ORIGIN', 'null'),
                           ('wsgi.url_scheme', 'http'), ('wsgi.url_scheme', 'ftp')]:
            with self.subTest(key=key, value=value): self.refuse_before_read({key: value}, 403)
        self.refuse_before_read({}, 403, remove=('HTTP_HOST',))

    def test_forwarded_headers_never_supply_trust(self):
        for key in ('HTTP_FORWARDED', 'HTTP_X_FORWARDED_HOST', 'HTTP_X_FORWARDED_PROTO', 'HTTP_X_FORWARDED_PORT'):
            with self.subTest(key=key): self.refuse_before_read({key: 'forged'}, 403)

    def test_original_target_required_and_no_encoded_alias(self):
        self.refuse_before_read({}, 400, remove=('RAW_URI',))
        for changes in ({'RAW_URI': '/%61nalyze'}, {'RAW_URI': '/analyze%2f'},
                        {'REQUEST_URI': '/other'}, {'RAW_URI': 'https://traceharbor.invalid/analyze'}):
            with self.subTest(changes=changes): self.refuse_before_read(changes, 400)

    def test_traversal_query_backslash_and_unknown_routes(self):
        for path in ('/../app.py', '/fixtures/../core.py', '/fixtures%2fcomplete.json', '/web\\app.js',
                     '/?x=1', '/admin', '/run-model', '/debug', '/upload', '/fixtures/unknown.json', '/output.schema.json'):
            with self.subTest(path=path):
                env = environment(path)
                self.assertIn(self.request(env)[0], (400, 404))
        self.refuse_before_read({'QUERY_STRING': 'x=1'}, 404)
        self.refuse_before_read({'SCRIPT_NAME': '/alias'}, 404)

    def test_unsupported_method_and_wrong_route_method(self):
        env = environment('/analyze', 'PUT')
        code, headers, _ = self.request(env)
        self.assertEqual(code, 405)
        self.assertEqual(headers['Allow'], 'GET, POST')
        self.assertEqual(self.request(environment('/analyze'))[0], 404)
        self.refuse_before_read({'PATH_INFO': '/', 'RAW_URI': '/'}, 404)

    def test_invalid_media_before_body(self):
        for media in ('text/plain', '', 'application/json; charset=latin-1', 'application/json; x=y', True):
            with self.subTest(media=media): self.refuse_before_read({'CONTENT_TYPE': media}, 415)
        self.refuse_before_read({}, 415, remove=('CONTENT_TYPE',))

    def test_length_and_chunking_guards_before_body(self):
        for length in (True, False, 2, '-1', '+2', 'True', '1.0', ' 2', '02', '１２'):
            with self.subTest(length=length): self.refuse_before_read({'CONTENT_LENGTH': length}, 400)
        self.refuse_before_read({}, 400, remove=('CONTENT_LENGTH',))
        for length in ('0', '262145', '99999999999999999999'):
            with self.subTest(length=length): self.refuse_before_read({'CONTENT_LENGTH': length}, 413)
        for key in ('HTTP_TRANSFER_ENCODING', 'HTTP_CONTENT_LENGTH', 'HTTP_CONTENT_TYPE', 'wsgi.input_terminated'):
            with self.subTest(key=key): self.refuse_before_read({key: 'chunked'}, 400)

    def test_valid_utf8_media_and_absent_origin(self):
        raw = (SOURCE/'fixtures/missing.json').read_bytes()
        env = environment('/analyze', 'POST', raw)
        env['CONTENT_TYPE'] = 'Application/JSON; charset="UTF-8"'
        env.pop('HTTP_ORIGIN')
        self.assertEqual(self.request(env)[0], 200)
        self.assertEqual(env['wsgi.input'].calls, [len(raw)])

    def test_truncated_and_invalid_stream_bytes(self):
        env = environment('/analyze', 'POST', b'{}')
        env['CONTENT_LENGTH'] = '3'
        self.assertEqual(self.request(env)[0], 400)
        self.assertEqual(env['wsgi.input'].calls, [3])
        class BadReader:
            def read(self, size): return 'text'
        env = environment('/analyze', 'POST', b'{}'); env['wsgi.input'] = BadReader()
        self.assertEqual(self.request(env)[0], 400)

    def test_invalid_utf8_json_schema_and_duplicates(self):
        for raw in (b'\xff', b'{', b'{}', b'{"x":1,"x":2}', b'NaN', b'null'):
            with self.subTest(raw=repr(raw)):
                code, _, data = self.request(environment('/analyze', 'POST', raw))
                self.assertEqual(code, 400)
                self.assertEqual(json.loads(data), {'error': 'Invalid synthetic JSON or dossier.'})

    def test_missing_input_and_timeout(self):
        env = environment('/analyze', 'POST', b'{}'); env.pop('wsgi.input')
        self.assertEqual(self.request(env)[0], 400)
        class SlowReader:
            def read(self, size): raise TimeoutError()
        env = environment('/analyze', 'POST', b'{}'); env['wsgi.input'] = SlowReader()
        self.assertEqual(self.request(env)[0], 408)

    def test_exact_body_cap_and_overreturn_are_bounded(self):
        original = (SOURCE/'fixtures/complete.json').read_bytes()
        raw = original + b' ' * (core.MAX_BYTES - len(original))
        env = environment('/analyze', 'POST', raw)
        original_reader = env['wsgi.input']
        code, _, data = self.request(env, checked=True)
        self.assertEqual(code, 200)
        self.assertEqual(json.loads(data), service.analyze(raw))
        self.assertEqual(original_reader.calls, [core.MAX_BYTES])
        class OverReader:
            def read(self, size): return b'{}x'
        env = environment('/analyze', 'POST', b'{}'); env['wsgi.input'] = OverReader()
        self.assertEqual(self.request(env)[0], 400)

    def test_resource_errors_are_generic_and_close(self):
        with patch.object(subject, '_read_resource', side_effect=subject._ResourceError()):
            code, _, data = self.request(environment('/'))
        self.assertEqual(code, 500)
        self.assertEqual(json.loads(data), {'error': 'Pinned resource unavailable.'})
        self.assertNotIn(str(SOURCE).encode(), data)

    def test_iterable_bytes_cleanup_on_exhaustion_and_early_close(self):
        response = subject.BytesResponse(b'abc')
        self.assertEqual(list(response), [b'abc'])
        self.assertTrue(response.closed)
        self.assertEqual(response.data, b'')
        response.close(); response.close()
        response = subject.BytesResponse(b'abc'); response.close()
        self.assertEqual(list(response), [])
        with self.assertRaises(TypeError): subject.BytesResponse('text')

    def test_start_response_failure_closes_without_second_response(self):
        made = []
        original = subject.BytesResponse
        def make(data):
            value = original(data); made.append(value); return value
        calls = []
        def broken(*args):
            calls.append(args); raise RuntimeError('Synthetic disconnected gateway')
        with patch.object(subject, 'BytesResponse', side_effect=make), self.assertRaises(RuntimeError):
            self.target(environment('/'), broken)
        self.assertEqual(len(calls), 1)
        self.assertTrue(made[0].closed)
        self.assertEqual(made[0].data, b'')


if __name__ == '__main__':
    if args.case:
        for name in args.case:
            if not name.startswith('test_') or not callable(getattr(WSGI177Tests, name, None)):
                parser.error('Unknown test case.')
        suite = unittest.TestSuite(WSGI177Tests(name) for name in args.case)
    else:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(WSGI177Tests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    ACTIVE[0] = False
    print(json.dumps({'schema': 'TRACE177_MEMORY_TEST_RESULTS_V1', 'tests_run': result.testsRun,
                      'failures': len(result.failures), 'errors': len(result.errors),
                      'request_observations': OBSERVATIONS, 'request_count': len(OBSERVATIONS),
                      'audit_violations': AUDIT_VIOLATIONS, 'import_socket_or_file_write_attempts': len(AUDIT_VIOLATIONS),
                      'HTTP_servers_started': 0, 'model_calls': 0}, sort_keys=True))
    raise SystemExit(0 if result.wasSuccessful() else 1)
