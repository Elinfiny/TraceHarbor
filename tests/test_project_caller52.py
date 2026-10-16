"""SYNTHETIC caller52 only. Four methods/six cases, actual execute/admit/reservation."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import sys
import tempfile
import types
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

PROJECT = 'aiproject-e00d73xwjm884tnvcs'
MODEL = 'nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B'
BASE = Path(__file__).resolve().parents[1]

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()

def digest(value): return hashlib.sha256(canonical(value)).hexdigest()

class SyntheticSchemaPath:
    def __init__(self, unused): pass
    @property
    def parent(self): return self
    def __truediv__(self, name):
        if name != 'output.schema.json': raise AssertionError('Unexpected schema read')
        return self
    def read_text(self):
        return json.dumps({'properties': {'analysis': {'type': 'object', 'properties': {'synthetic': {'type': 'boolean'}}}}})

class ProjectCaller52(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='SYNTHETIC52-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'fixtures').mkdir()
        for name in ('complete', 'missing', 'contradictory'):
            evidence = {'case_id': 'SYNTHETIC_CALLER52_' + name, 'title': 'Fresh synthetic caller52',
                        'sources': [{'id': 'NEW52_' + name, 'kind': 'synthetic', 'title': 'Synthetic52',
                                     'sha256': hashlib.sha256(('NEW52_' + name).encode()).hexdigest(),
                                     'events': ['SYNTHETIC_CALLER52_EVENT_' + name]}]}
            (self.root / 'fixtures' / (name + '.json')).write_bytes(canonical(evidence))
        self.effects = []
        self.requests = []
        self.outcome = 'success'
        core = types.ModuleType('core')
        core.canonical, core.digest, core.parse_json = canonical, digest, json.loads
        core.import_package = json.loads
        service = types.ModuleType('live_service')
        service.build_record = lambda raw, analysis, metadata: {
            'synthetic_only': True, 'dossier_sha256': digest([json.loads(raw), analysis, metadata])}
        ns = importlib.util.spec_from_file_location('nebius', BASE / 'nebius.py')
        self.nebius = importlib.util.module_from_spec(ns)
        cs = importlib.util.spec_from_file_location('caller52', BASE / 'live_probe.py')
        self.m = importlib.util.module_from_spec(cs)
        with patch.dict(sys.modules, {'core': core, 'live_service': service, 'nebius': self.nebius}):
            ns.loader.exec_module(self.nebius)
            cs.loader.exec_module(self.m)
        self.nebius.Path = SyntheticSchemaPath
        self.m.ROOT = self.root
        def synthetic_get(name):
            self.effects.append(('synthetic_env', name))
            return {'NEBIUS_MODEL': MODEL, 'NEBIUS_API_KEY': 'SYNTHETIC_NOT_A_CREDENTIAL'}.get(name)
        def scoped_open(path, flags, mode=0o777):
            resolved = Path(path).resolve()
            if not resolved.is_relative_to(self.root): raise AssertionError('FS outside fresh synthetic root')
            self.effects.append(('synthetic_fs_open', str(resolved)))
            return os.open(path, flags, mode)
        self.m.os = types.SimpleNamespace(environ=types.SimpleNamespace(get=synthetic_get), open=scoped_open,
            fdopen=os.fdopen, fsync=os.fsync, close=os.close, O_WRONLY=os.O_WRONLY,
            O_CREAT=os.O_CREAT, O_EXCL=os.O_EXCL, O_RDONLY=os.O_RDONLY)
        def synthetic_transport(payload, *, project_id=None):
            self.requests.append((json.loads(canonical(payload)), project_id))
            if project_id != PROJECT: raise AssertionError('Caller did not forward exact explicit project')
            if self.outcome == 'refusal': raise self.m.ProviderError('SYNTHETIC_PROVIDER_REFUSAL52')
            if self.outcome == 'unknown': raise self.m.ProviderError('TRANSPORT_OUTCOME_UNKNOWN_NO_RETRY')
            return canonical({'model': MODEL, 'choices': [{'finish_reason': 'stop',
                'message': {'content': '{"synthetic":true}'}}],
                'usage': {'prompt_tokens': 1, 'completion_tokens': 2, 'total_tokens': 3}})
        self.m.https_once = synthetic_transport

    def fresh_permit(self):
        # Actual planned_requests, request_for and admit are exercised; no imported admission.
        _, requests = self.m.planned_requests(MODEL)
        permit = {'schema': 'traceharbor.live-admission.v1',
            'operation_id': 'TRACEHARBOR_THREE_SYNTHETIC_REQUESTS_V1', 'model': MODEL,
            'expires_utc': (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
            'request_sha256': [digest(p) for p in requests], 'input_token_upper_bounds': [10, 10, 10],
            'input_usd_per_million': '0', 'output_usd_per_million': '0', 'max_cost_usd': '0.000001'}
        for name in ('verified_access_evidence', 'verified_credit_and_cap_evidence',
                     'verified_model_license_evidence', 'verified_token_bounds_evidence'):
            permit[name] = 'SYNTHETIC_CALLER52_NOT_PROVIDER_PROOF'
        path = self.root / 'fresh-synthetic-permit52.json'
        path.write_bytes(canonical(permit))
        return path, self.root / 'fresh-output52', permit

    def assert_reservation_intact(self, permit_path, output, permit):
        marker = Path(str(permit_path) + '.spent')
        self.assertTrue(marker.is_file())
        reserved = json.loads(marker.read_bytes())
        self.assertEqual(reserved['state'], 'RESERVED_DO_NOT_REPLAY')
        self.assertEqual(reserved['reserved_requests'], 3)
        self.assertEqual(reserved['permit_sha256'], digest(permit))
        self.assertEqual(reserved['request_sha256'], permit['request_sha256'])
        self.assertEqual(reserved['output'], str(output.resolve()))

    def test_01_invalid_project_precedes_every_effect(self):
        # Cases 1..3: missing/foreign/malformed, before permit.resolve and every other effect.
        test = self
        class Bomb:
            def resolve(self):
                test.effects.append(('FORBIDDEN_PERMIT_RESOLVE',))
                raise AssertionError('Permit touched before project rejection')
            def mkdir(self, *args, **kwargs):
                test.effects.append(('FORBIDDEN_OUTPUT_MKDIR',))
                raise AssertionError('Output touched before project rejection')
        for label, project in [('missing', None), ('foreign', 'aiproject-FOREIGN52'),
                                ('malformed', PROJECT + '\n')]:
            with self.subTest(SYNTHETIC=label):
                self.effects.clear()
                with self.assertRaisesRegex(self.m.ProviderError, '^PROJECT_NOT_CONFIGURED$'):
                    if project is None: self.m.execute(Bomb(), Bomb())
                    else: self.m.execute(Bomb(), Bomb(), project_id=project)
                self.assertEqual(self.effects, [])
                self.assertEqual(self.requests, [])

    def test_02_valid_project_reaches_actual_callsite_with_payload(self):
        # Case 4: actual execute/admit/write_new/decode_response, fresh synthetic FS/transport.
        path, output, permit = self.fresh_permit()
        self.assertEqual(self.m.execute(path, output, project_id=PROJECT), 0)
        self.assertEqual(len(self.requests), 3)
        for payload, actual_project in self.requests:
            self.assertEqual(actual_project, PROJECT)
            self.assertEqual(payload['model'], MODEL)
            self.assertEqual(payload['max_completion_tokens'], 1500)
            self.assertNotIn('max_tokens', payload)
            self.assertEqual(payload['response_format'], {'type': 'json_object'})
            self.assertEqual([payload['n'], payload['stream'], payload['store']], [1, False, False])
            self.assertEqual([m['role'] for m in payload['messages']], ['system', 'user'])
        self.assertEqual([digest(p) for p, _ in self.requests], permit['request_sha256'])
        self.assert_reservation_intact(path, output, permit)
        result = json.loads((output / 'result.json').read_bytes())
        self.assertTrue(result['completed_three'])
        self.assertEqual(len(result['outcomes']), 3)

    def assert_first_stop(self, outcome, expected_error):
        self.outcome = outcome
        path, output, permit = self.fresh_permit()
        self.assertEqual(self.m.execute(path, output, project_id=PROJECT), 2)
        self.assertEqual(len(self.requests), 1)
        self.assertEqual(self.requests[0][1], PROJECT)
        self.assert_reservation_intact(path, output, permit)
        self.assertTrue((output / '1-attempt.json').exists())
        self.assertFalse((output / '2-attempt.json').exists())
        self.assertFalse((output / '3-attempt.json').exists())
        terminal = json.loads((output / '1-terminal.json').read_bytes())
        self.assertEqual(terminal['error'], expected_error)
        self.assertEqual(terminal['status'], 'REJECTED_OR_UNKNOWN_NO_RETRY')
        result = json.loads((output / 'result.json').read_bytes())
        self.assertFalse(result['completed_three'])
        self.assertEqual(len(result['outcomes']), 1)

    def test_03_first_synthetic_refusal_stops_and_preserves_reservation(self):
        # Case 5: no next case/retry/release of reserved requests.
        self.assert_first_stop('refusal', 'SYNTHETIC_PROVIDER_REFUSAL52')

    def test_04_first_synthetic_unknown_stops_and_preserves_reservation(self):
        # Case 6: unknown is not a refund or a replay grant.
        self.assert_first_stop('unknown', 'TRANSPORT_OUTCOME_UNKNOWN_NO_RETRY')

if __name__ == '__main__':
    def deny_network(*args, **kwargs): raise AssertionError('REAL_NETWORK_DENIED_SYNTHETIC52')
    with patch.object(socket, 'socket', deny_network), patch.object(socket, 'create_connection', deny_network):
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(ProjectCaller52)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print('PRIVATE_INERT_PROJECT_CALLER_PASS; SYNTHETIC; methods=4; cases=6; real_network=0; real_key_lookup=0')
    raise SystemExit(0 if result.wasSuccessful() else 1)
