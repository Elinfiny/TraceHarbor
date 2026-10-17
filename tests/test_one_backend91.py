"""One new four-scenario frozen harness; fake Git only, never old cases."""
import base64
import copy
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import sys
import traceback

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import one_backend91 as b


def deny_network(event, args):
    if event in ('socket.connect', 'socket.connect_ex', 'socket.getaddrinfo', 'subprocess.Popen', 'os.system'):
        raise RuntimeError('HOST_NETWORK_AND_CHILD_DENIED91')


sys.addaudithook(deny_network)
BASE = Path(sys.argv[1]).resolve()
CAPTURES = []
FIRST_ORIGINAL = []


class Clock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


def plan(label):
    return b.SyntheticPlan('91001', b.SOURCE_PARENT, b.digest(('fresh-one91-' + label).encode()),
                           'a6c905b718e0770f87efc1058f1961beaee6de172c7ab31c74fdbf82774a9b95',
                           'f57813253ce6f59318354e62d4bee7c6dd133ed33cfc245438d1d5a604cf43a1',
                           '1e24c7eb6e3afadfbd767730c39390a9b43a97ba87ef6237407f0982056cecc4', 1100)


class FakeGit:
    def __init__(self, clock, mode='normal'):
        self.clock, self.mode = clock, mode
        self.calls, self.blobs, self.trees, self.commits, self.refs = [], {}, {}, {}, {}
        self.failure = OSError('private-fake-ref-created-response-lost91')

    def request(self, method, path, body):
        self.calls.append((method, path, copy.deepcopy(body)))
        if method == 'GET' and path == '':
            return b.Reply(200, {'id': b.REPO_ID, 'full_name': b.REPO})
        if method == 'POST' and path == '/git/blobs':
            raw = base64.b64decode(body['content'], validate=True)
            sha = b.git_oid('blob', raw)
            self.blobs[sha] = raw
            return b.Reply(201, {'sha': sha})
        if method == 'POST' and path == '/git/trees':
            e = body['tree'][0]
            sha = b.git_oid('tree', b'100644 ' + e['path'].encode() + b'\0' + bytes.fromhex(e['sha']))
            self.trees[sha] = copy.deepcopy(body['tree'])
            return b.Reply(201, {'sha': sha})
        if method == 'POST' and path == '/git/commits':
            sha = hashlib.sha1(b.canonical(body)).hexdigest()
            self.commits[sha] = {'sha': sha, 'tree': {'sha': body['tree']},
                                 'parents': [{'sha': s} for s in body['parents']], 'message': body['message']}
            return b.Reply(201, {'sha': sha})
        if method == 'POST' and path == '/git/refs':
            if self.mode == 'collision' or body['ref'] in self.refs:
                return b.Reply(409, {'message': 'Ref exists'})
            self.refs[body['ref']] = body['sha']
            if self.mode == 'ambiguous':
                raise self.failure
            return b.Reply(201, {'ref': body['ref'], 'object': {'type': 'commit', 'sha': body['sha']}})
        if method == 'GET' and path.startswith('/git/ref/'):
            ref = 'refs/' + path[len('/git/ref/'):]
            value = {'ref': ref, 'object': {'type': 'commit', 'sha': self.refs[ref]}}
            if self.mode == 'foreign_ref':
                value['object']['sha'] = 'f' * 40
            return b.Reply(200, value)
        if method == 'GET' and path.startswith('/git/commits/'):
            value = copy.deepcopy(self.commits[path.rsplit('/', 1)[-1]])
            if self.mode == 'foreign_parent':
                value['parents'] = [{'sha': 'e' * 40}]
            return b.Reply(200, value)
        if method == 'GET' and path.startswith('/git/trees/'):
            sha = path.rsplit('/', 1)[-1]
            if self.mode == 'stale':
                self.clock.now = 1100.0
            return b.Reply(200, {'sha': sha, 'truncated': False, 'tree': copy.deepcopy(self.trees[sha])})
        if method == 'GET' and path.startswith('/git/blobs/'):
            sha = path.rsplit('/', 1)[-1]
            raw = self.blobs[sha]
            if self.mode == 'partial_blob':
                raw = raw[:-1]
            return b.Reply(200, {'sha': sha, 'encoding': 'base64', 'content': base64.b64encode(raw).decode()})
        raise AssertionError('UNEXPECTED_FAKE_GIT_CALL91')


def setup(label, mode='normal', same_parent=None):
    parent = same_parent or BASE / label
    parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    capture = b.PrivateOriginals(parent / ('capture-%02d' % len(CAPTURES)))
    CAPTURES.append(capture)
    clock = Clock(); client = FakeGit(clock, mode)
    backend = b.synthetic_backend(plan(label), client, capture, clock)
    return backend, client, capture, clock


def refused(call):
    try:
        call()
    except b.Refuse as error:
        return str(error)
    raise AssertionError('EXPECTED_REFUSAL91')


def ref_creates(client):
    return sum(method == 'POST' and path == '/git/refs' for method, path, _ in client.calls)


def scenario1():
    backend, client, capture, clock = setup('positive')
    receipt = backend.reserve()
    record = backend.verify(receipt)
    assert record == b.record_for(plan('positive'))
    assert record['state'] == 'ATTEMPTING_CONSUMED' and record['native_grant'] is None
    assert record['operation'] == b.OP and receipt['ref'].startswith(b.NAMESPACE)
    assert receipt['invocation'] == '91001' and receipt['source_commit'] == b.SOURCE_PARENT
    assert client.blobs[receipt['blob']] == b.canonical(record)
    assert receipt['record_sha256'] == b.digest(b.canonical(record))
    assert ref_creates(client) == 1 and len(client.refs) == 1
    assert [p for m,p,_ in client.calls if m == 'GET'] == ['', '',
            '/git/ref/' + receipt['ref'].removeprefix('refs/'),
            '/git/commits/' + receipt['commit'], '/git/trees/' + receipt['tree'], '/git/blobs/' + receipt['blob']]
    calls = len(client.calls)
    refused(backend.reserve)
    assert len(client.calls) == calls
    assert not any(m in ('PATCH', 'DELETE', 'PUT') for m,_,_ in client.calls)
    return {'fresh_record_bytes':len(b.canonical(record)), 'record_sha256':receipt['record_sha256'],
            'create_ref':1, 'full_byte_readback':True, 'native':False}


def scenario2():
    modes = ['foreign_ref', 'foreign_parent', 'partial_blob', 'stale']
    outcomes = []
    for mode in modes:
        backend, client, capture, clock = setup(mode, mode)
        code = refused(backend.reserve)
        assert ref_creates(client) == 1 and backend.first_primary and not backend._verified
        old = len(client.calls)
        assert refused(backend.reserve) == code and len(client.calls) == old
        outcomes.append({'mode':mode, 'code':code, 'no_retry':True})
    for mutation in ('partial', 'foreign', 'late'):
        backend, client, capture, clock = setup('receipt-' + mutation)
        receipt = backend.reserve(); count = len(client.calls)
        if mutation == 'partial':
            del receipt['tree']
        elif mutation == 'foreign':
            receipt['invocation'] = '91002'
        else:
            clock.now = 1100.0
        refused(lambda: backend.verify(receipt))
        assert len(client.calls) == count
    return {'remote_wrong_foreign_partial_stale':outcomes, 'receipt_before_client_refusals':3}


def scenario3():
    outcomes = []
    for mode in ('collision', 'ambiguous'):
        backend, client, capture, clock = setup('once-' + mode, mode)
        code = refused(backend.reserve)
        assert ref_creates(client) == 1 and not backend._verified
        count = len(client.calls)
        assert refused(backend.reserve) == code and len(client.calls) == count
        if mode == 'ambiguous':
            assert len(client.refs) == 1
            assert any(original is client.failure for _,kind,original in capture.originals if kind == 'EXCEPTION')
        # Restart with exactly the same nonce and same explicit marker parent:
        # new invocation instance cannot adopt a receipt or issue another create.
        parent = capture.directory.parent
        again_capture = b.PrivateOriginals(parent / 'restart-capture'); CAPTURES.append(again_capture)
        again = b.synthetic_backend(backend.plan, client, again_capture, clock)
        refused(again.reserve)
        assert len(client.calls) == count and ref_creates(client) == 1
        assert any(isinstance(original, FileExistsError) for _,kind,original in again_capture.originals if kind == 'EXCEPTION')
        outcomes.append({'mode':mode,'first_primary':code,'same_directory_restart_no_client':True,
                         'remote_applied':len(client.refs),'create_ref':1})
    return {'outcomes':outcomes, 'scope':'Synthetic local restart marker; no cross-runner/native claim'}


def scenario4():
    original = b.native_binding
    assert original() is None
    defaults = []
    try:
        for witness in (None, True, {'admitted':True}, plan('not-authority'), lambda: True):
            b.native_binding = lambda witness=witness: witness
            defaults.append(refused(b.OneBackend))
    finally:
        b.native_binding = original
    assert defaults[0] == 'NO_AUTHENTIC_NATIVE_BINDING91'
    assert defaults[1:] == ['NATIVE_CLIENT_AND_ISSUER_NOT_BOUND91'] * 4
    backend, client, capture, clock = setup('default-gates')
    count = len(client.calls)
    for changed in (replace(backend.plan, origin='UNKNOWN'), replace(backend.plan, source_commit='f'*40),
                    replace(backend.plan, project='foreign'), replace(backend.plan, model='foreign')):
        refused(lambda changed=changed: b.synthetic_backend(changed, client, capture, clock))
    assert len(client.calls) == count == 0
    return {'native_default_and_forged_witness_refusals':5,'wrong_plan_refusals':4,
            'credential_lookup':0,'remote_calls':0,'native_binding':None}


def main():
    BASE.mkdir(mode=0o700, parents=True, exist_ok=False)
    guard_checks = 0
    for event in ('socket.connect', 'socket.connect_ex', 'socket.getaddrinfo', 'subprocess.Popen', 'os.system'):
        try:
            sys.audit(event, ())  # Exercise the host hook without network I/O.
        except RuntimeError as error:
            assert str(error) == 'HOST_NETWORK_AND_CHILD_DENIED91'
            guard_checks += 1
    assert guard_checks == 5
    scenarios = []
    for number, case in enumerate((scenario1, scenario2, scenario3, scenario4), 1):
        try:
            value = case()
            scenarios.append({'scenario':number,'status':'PASS','receipt':value})
        except Exception as original:
            FIRST_ORIGINAL.append(original)
            raw = ''.join(traceback.format_exception(type(original), original, original.__traceback__)).encode()
            fd = os.open(BASE/'first-abort-original.txt', os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0o600)
            with os.fdopen(fd,'wb') as out:
                out.write(raw); out.flush(); os.fsync(out.fileno())
            print(json.dumps({'scenario':number,'status':'ABORT','previous':scenarios,
                              'remaining':'NOT_RUN','original_sha256':b.digest(raw)}))
            return 1
    manifest = []
    for capture in CAPTURES:
        for item in capture.metadata:
            path = capture.directory/item['file']; raw = path.read_bytes()
            assert len(raw)==item['bytes'] and b.digest(raw)==item['sha256']
            assert path.stat().st_mode & 0o777 == 0o600
            manifest.append({'path':str(path.relative_to(BASE)),**item})
    raw = b.canonical(manifest)
    fd=os.open(BASE/'capsule-manifest.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'wb') as out:
        out.write(raw);out.flush();os.fsync(out.fileno())
    print(json.dumps({'group':'ONE_BACKEND91_NEW_ONLY','status':'PASS','scenarios':scenarios,
                      'host_network_guard':'socket/DNS/subprocess denied','guard_checks':guard_checks,'native_effects':0,
                      'capsules':len(manifest),'capsule_manifest_sha256':b.digest(raw)}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
