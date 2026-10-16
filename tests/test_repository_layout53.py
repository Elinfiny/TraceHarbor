"""NEW private layout53 group: three cases; old51/52 test methods never run."""
import hashlib
import importlib.util
from pathlib import Path
import socket
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PINS = {
    'nebius.py': 'a162f41880dd7621379e93ce932f9b97a7524abf195d70b56b199a51c7fb6fcc',
    'live_probe.py': 'ffddb42a83b8dfe164bf2d0374f60e9cb7b1c9ee140205cd1c579a4b8af0aff3',
}
OLD_METHODS_EXECUTED = 0

def snapshot():
    return {str(p.relative_to(ROOT)): (p.stat().st_mode, hashlib.sha256(p.read_bytes()).hexdigest())
            for p in ROOT.rglob('*') if p.is_file()}

def deny_network(*args, **kwargs):
    raise AssertionError('REAL_NETWORK_DENIED_LAYOUT53')

def load_corrected_module():
    spec = importlib.util.spec_from_file_location('corrected_caller52_layout53',
                                                ROOT / 'tests/test_project_caller52.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class RepositoryLayout53(unittest.TestCase):
    def setUp(self):
        self.before = snapshot()
        self.directory_before = sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*'))
        self.corrected = load_corrected_module()
        self.old_guards = []
        def forbidden_old_method(*args, **kwargs):
            global OLD_METHODS_EXECUTED
            OLD_METHODS_EXECUTED += 1
            raise AssertionError('OLD_TEST_METHOD_REPLAY_FORBIDDEN')
        for name in vars(self.corrected.ProjectCaller52):
            if name.startswith('test_'):
                guard = patch.object(self.corrected.ProjectCaller52, name, forbidden_old_method)
                guard.start()
                self.old_guards.append(guard)
                self.addCleanup(guard.stop)
        self.fixture = self.corrected.ProjectCaller52(methodName='runTest')
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.temp_root = self.fixture.root

    def tearDown(self):
        self.fixture.doCleanups()
        self.assertFalse(self.temp_root.exists())
        self.assertEqual(snapshot(), self.before)
        self.assertEqual(sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*')), self.directory_before)
        self.assertFalse((ROOT / 'runtime').exists())
        self.assertEqual(OLD_METHODS_EXECUTED, 0)

    def test_01_actual_loader_resolves_exact_production_sources(self):
        self.assertEqual(self.corrected.BASE, ROOT)
        for name, module in [('nebius.py', self.fixture.nebius), ('live_probe.py', self.fixture.m)]:
            self.assertEqual(Path(module.__file__).resolve(), ROOT / name)
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest(), PINS[name])
        self.assertIs(self.fixture.m.project_request_path, self.fixture.nebius.project_request_path)
        self.assertFalse((ROOT / 'dependency51').exists())
        self.assertFalse((ROOT.parent / 'nebius.py').exists())
        self.assertFalse((ROOT.parent / 'live_probe.py').exists())

    def test_02_default_none_refuses_before_any_effect(self):
        touched = []
        class Bomb:
            def resolve(self):
                touched.append('permit_resolve')
                raise AssertionError('PRE_REFUSAL_EFFECT')
            def mkdir(self, *args, **kwargs):
                touched.append('output_mkdir')
                raise AssertionError('PRE_REFUSAL_EFFECT')
        with self.assertRaisesRegex(self.fixture.m.ProviderError, '^PROJECT_NOT_CONFIGURED$'):
            self.fixture.m.execute(Bomb(), Bomb())
        self.assertEqual(touched, [])
        self.assertEqual(self.fixture.effects, [])
        self.assertEqual(self.fixture.requests, [])
        self.assertEqual(sorted(p.name for p in self.temp_root.iterdir()), ['fixtures'])

    def test_03_fresh_fixtures_outside_repository_no_output_or_drift(self):
        self.assertFalse(self.temp_root.is_relative_to(ROOT))
        self.assertEqual(sorted(p.name for p in (self.temp_root / 'fixtures').iterdir()),
                         ['complete.json', 'contradictory.json', 'missing.json'])
        self.assertEqual(sorted(p.name for p in self.temp_root.iterdir()), ['fixtures'])
        self.assertEqual(snapshot(), self.before)
        self.assertEqual(self.fixture.effects, [])
        self.assertEqual(self.fixture.requests, [])
        self.assertNotIn('env', sys.modules)

if __name__ == '__main__':
    with patch.object(socket, 'socket', deny_network), patch.object(socket, 'create_connection', deny_network):
        result = unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(RepositoryLayout53))
    print('LAYOUT53; cases=3; old51_methods=0; old52_methods=' + str(OLD_METHODS_EXECUTED) +
          '; real_network=0; real_key_lookup=0; repository_writes=0; synthetic_setup_only')
    raise SystemExit(0 if result.wasSuccessful() else 1)
