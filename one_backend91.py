"""Dormant fresh-ONE Git backend with separately guarded native94 producer.

Synthetic construction is trusted test code, never native authority. Local
diagnostics and attempt markers are test protection, not cloud escrow or a
cross-runner lease. Only Git's create-only ref is the durable atomic consume.
"""
import base64
import copy
from dataclasses import dataclass
from functools import wraps
import hashlib
import json
import math
import os
from pathlib import Path
import traceback

REPO = 'Elinfiny/TraceHarbor'
REPO_ID = 1391430317
OP = 'TRACEHARBOR_FRESH_ONE_BACKEND91_V1'
NAMESPACE = 'refs/tags/traceharbor-one91-consumed/'
MESSAGE = 'TraceHarbor fresh ONE ATTEMPTING_CONSUMED91'
PATH = 'one-receipt91.json'
MODEL = 'nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B'
PROJECT = 'aiproject-e00d73xwjm884tnvcs'
SOURCE_PARENT = '1bbe743e2e0cf96837846019d60c6a7eaa58a106'
JSON_MEDIA = 'application/vnd.github+json'
RAW_MEDIA = 'application/vnd.github.raw+json'
MAX_WIRE = 65536
MAX_BLOB = 16384


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git_oid(kind, raw):
    return hashlib.sha1(kind.encode() + b' ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def hexid(value, length=64):
    return type(value) is str and len(value) == length and all(c in '0123456789abcdef' for c in value)


class Refuse(Exception):
    """Export only this constant code, never original private error text."""


def native_binding():
    """No authentic issuer/runtime/client/custody/capture/grant is installed."""
    from one_native94 import peek_context94
    return peek_context94()


class OneBackend:
    def __init__(self):
        context = native_binding()
        if context is None:
            raise Refuse('NO_AUTHENTIC_NATIVE_BINDING91')
        from one_native94 import backend_from_context94
        self._core94 = backend_from_context94(context)

    def reserve(self):
        return self._core94.reserve()

    def verify(self, receipt):
        return self._core94.verify(receipt)


@dataclass(frozen=True)
class SyntheticPlan:
    invocation: str
    source_commit: str
    nonce: str
    payload_sha256: str
    input_sha256: str
    evidence_sha256: str
    deadline_utc: int
    project: str = PROJECT
    model: str = MODEL
    origin: str = 'FRESH_SYNTHETIC'


@dataclass(frozen=True)
class Reply:
    status: int
    body: bytes
    media_type: str = JSON_MEDIA
    eof: bool = True


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise Refuse('DUPLICATE_JSON_KEY92')
            result[key] = value
        return result

    def invalid_constant(value):
        raise Refuse('NONFINITE_JSON92')

    return json.loads(raw.decode('utf-8', errors='strict'), object_pairs_hook=pairs,
                      parse_constant=invalid_constant)


def metadata(value, allowed, *, kind, sha):
    if type(value) is not dict or set(value) - set(allowed):
        raise Refuse('UNEXPECTED_SEMANTIC_FIELDS92')
    if 'url' in value and value['url'] != 'https://api.github.com/repos/' + REPO + '/git/' + kind + '/' + sha:
        raise Refuse('FOREIGN_METADATA_URL92')
    if 'node_id' in value and (type(value['node_id']) is not str or not value['node_id'].isascii()
                              or not 1 <= len(value['node_id']) <= 512):
        raise Refuse('INVALID_NODE_METADATA92')


def tree_projection(tree, blob, raw_size, expected_tree):
    metadata(tree, ('sha', 'url', 'node_id', 'tree', 'truncated'), kind='trees', sha=expected_tree)
    if (tree.get('sha') != expected_tree or tree.get('truncated') is not False
            or type(tree.get('tree')) is not list or len(tree['tree']) != 1):
        raise Refuse('TREE_SHAPE92')
    entry = tree['tree'][0]
    metadata(entry, ('path', 'mode', 'type', 'sha', 'size', 'url', 'node_id'), kind='blobs', sha=blob)
    if ('size' in entry and (type(entry['size']) is not int or entry['size'] != raw_size)):
        raise Refuse('TREE_SIZE92')
    projection = {key: entry.get(key) for key in ('path', 'mode', 'type', 'sha')}
    if projection != {'path': PATH, 'mode': '100644', 'type': 'blob', 'sha': blob}:
        raise Refuse('TREE_ENTRY92')
    calculated = git_oid('tree', b'100644 ' + PATH.encode() + b'\0' + bytes.fromhex(blob))
    if calculated != expected_tree:
        raise Refuse('TREE_OBJECT_ID92')
    return [projection]


def blob_json_bytes(blob, expected_sha, expected_size):
    metadata(blob, ('sha', 'encoding', 'content', 'size', 'url', 'node_id'), kind='blobs', sha=expected_sha)
    if (blob.get('sha') != expected_sha or blob.get('encoding') != 'base64'
            or type(blob.get('size')) is not int or blob['size'] != expected_size
            or not 0 <= blob['size'] <= MAX_BLOB or type(blob.get('content')) is not str
            or len(blob['content']) > MAX_WIRE):
        raise Refuse('BLOB_ENVELOPE92')
    encoded = blob['content'].encode('ascii', errors='strict')
    # Exact client contract: canonical base64, optionally Git-style 60-column
    # LF/CRLF wrapping and one trailing line terminator. No other whitespace.
    encoded = encoded.replace(b'\r\n', b'\n')
    if b'\r' in encoded:
        raise Refuse('BLOB_LINE_ENDING92')
    lines = encoded.split(b'\n')
    if lines and lines[-1] == b'':
        lines.pop()
    if len(lines) > 1 and (any(len(line) != 60 for line in lines[:-1]) or not 1 <= len(lines[-1]) <= 60):
        raise Refuse('BLOB_WRAPPING92')
    normalized = b''.join(lines)
    if len(normalized) > 4 * ((MAX_BLOB + 2) // 3):
        raise Refuse('BLOB_BOUND92')
    raw = base64.b64decode(normalized, validate=True)
    if base64.b64encode(raw) != normalized or len(raw) != expected_size:
        raise Refuse('BLOB_CANONICAL_BASE64_OR_SIZE92')
    return raw


class PrivateOriginals:
    """Bounded explicit local test capture, never a native credential sink."""
    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(mode=0o700, parents=True, exist_ok=False)
        os.chmod(self.directory, 0o700)
        self.originals = []
        self.total_bytes = 0
        self.metadata = []

    def retain(self, stage, kind, original):
        # Hold the actual object BEFORE conversion, classification or I/O.
        self.originals.append((stage, kind, original))
        if isinstance(original, BaseException):
            text = ''.join(traceback.format_exception(type(original), original, original.__traceback__))
        elif isinstance(original, Reply):
            text = repr((original.status, original.body))
        else:
            text = repr(original)
        raw = canonical({'stage': stage, 'kind': kind, 'private_text': text[:24000]})
        if len(self.metadata) >= 64 or len(raw) > 131072 or self.total_bytes + len(raw) > 1048576:
            raise Refuse('PRIVATE_CAPTURE_LIMIT91')
        path = self.directory / ('original-%03d.json' % len(self.metadata))
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'wb') as out:
            out.write(raw); out.flush(); os.fsync(out.fileno())
        self.total_bytes += len(raw)
        self.metadata.append({'file': path.name, 'bytes': len(raw), 'sha256': digest(raw)})

    def reserve_attempt(self, key):
        # Supplementary private local marker: same-directory restart refuses.
        # It is deliberately not represented as the remote durable consume.
        path = self.directory.parent / ('attempt91-' + key + '.json')
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'wb') as out:
            out.write(canonical({'key': key, 'state': 'ATTEMPTED_NO_RETRY'}))
            out.flush(); os.fsync(out.fileno())
        directory_fd = os.open(path.parent, os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)


def record_for(plan):
    if type(plan) is not SyntheticPlan or plan.origin != 'FRESH_SYNTHETIC':
        raise Refuse('NOT_FRESH_SYNTHETIC91')
    if (type(plan.invocation) is not str or not plan.invocation.isascii()
            or not plan.invocation.isdigit() or int(plan.invocation) <= 0
            or plan.source_commit != SOURCE_PARENT
            or not all(hexid(x) for x in (plan.nonce, plan.payload_sha256,
                                         plan.input_sha256, plan.evidence_sha256))
            or type(plan.deadline_utc) is not int
            or plan.project != PROJECT or plan.model != MODEL):
        raise Refuse('PLAN_BINDING91')
    return {'schema': 'TRACEHARBOR_FRESH_ONE_RECORD91_V1', 'operation': OP,
            'repository': REPO, 'repository_id': REPO_ID,
            'classification': 'SYNTHETIC_ALGORITHM_ONLY_NOT_NATIVE',
            'native_grant': None, 'source_commit': plan.source_commit,
            'invocation': plan.invocation, 'attempt': 1, 'nonce': plan.nonce,
            'project': plan.project, 'model': plan.model,
            'payload_sha256': plan.payload_sha256, 'input_sha256': plan.input_sha256,
            'evidence_sha256': plan.evidence_sha256, 'deadline_utc': plan.deadline_utc,
            'state': 'ATTEMPTING_CONSUMED', 'refund_or_resume': False}


def _private_failure(call):
    @wraps(call)
    def guarded(self, *args, **kwargs):
        try:
            return call(self, *args, **kwargs)
        except Exception as original:
            self._retain('PUBLIC_BOUNDARY_' + call.__name__, 'EXCEPTION', original)
            self._fail(self.first_primary or 'BOUNDARY_UNKNOWN91')
    return guarded


class _GitRecordCore:
    """Shared exact Git protocol, not an admission or credential factory."""
    def __init__(self, plan, record, fake_git, capture, clock, *, namespace, message, local_marker):
        self.record = record
        self.plan, self._git, self.capture, self._clock = plan, fake_git, capture, clock
        self.message, self.local_marker = message, local_marker
        self.first_primary = None
        self.secondary = []  # Private actual secondary exception objects, ordered.
        self.attempted = False
        self._receipt = None
        self._verified = False
        self.key = digest(canonical({'operation': record['operation'], 'repository_id': REPO_ID, 'nonce': plan.nonce}))
        self.ref = namespace + self.key
        self.raw = canonical(self.record)
        self.blob = git_oid('blob', self.raw)
        self.tree = git_oid('tree', b'100644 ' + PATH.encode() + b'\0' + bytes.fromhex(self.blob))

    def _fail(self, code):
        if self.first_primary is None:
            self.first_primary = code
        raise Refuse(self.first_primary)

    def _retain(self, stage, kind, original):
        try:
            self.capture.retain(stage, kind, original)
            return True
        except Exception as capture_error:
            # PrivateOriginals holds the original before conversion. Preserve
            # any capture exception as a secondary, never replace a primary.
            self.capture.originals.append((stage, 'CAPTURE_FAILURE', capture_error))
            self.secondary.append((stage, capture_error))
            return False

    def _check(self, stage):
        if self.first_primary is not None:
            raise Refuse(self.first_primary)
        try:
            now = self._clock()
            if type(now) not in (int, float) or not math.isfinite(now) or now >= self.plan.deadline_utc:
                raise Refuse('ABSOLUTE_WINDOW_EXPIRED91')
        except Exception as error:
            self._retain(stage, 'EXCEPTION', error)
            self._fail('ABSOLUTE_WINDOW_UNKNOWN91')

    def _invoke(self, stage, call):
        self._check('PRE_INVOKE_' + stage)
        try:
            original = call()
        except Exception as error:
            self._retain(stage, 'EXCEPTION', error)
            self._fail('CALL_UNKNOWN91_' + stage)
        if not self._retain(stage, 'RETURN', original):
            self._fail('PRIVATE_CAPTURE_UNKNOWN92_' + stage)
        self._check('POST_RETURN_' + stage)
        return original

    def _wire(self, stage, reply, status, media_types):
        if type(reply) is not Reply or type(reply.status) is not int:
            self._fail('PARTIAL_REPLY91_' + stage)
        if reply.status != status:
            self._fail('CREATE_COLLISION_CONSUMED91' if stage == 'CREATE_REF' and reply.status == 409
                       else 'HTTP_UNKNOWN91_' + stage)
        if (type(reply.body) is not bytes or type(reply.media_type) is not str or len(reply.body) > MAX_WIRE
                or reply.eof is not True or reply.media_type not in media_types):
            self._fail('PARTIAL_BODY_OR_MEDIA92_' + stage)
        return reply.body

    def _call(self, stage, method, path, body=None, status=200):
        reply = self._invoke(stage, lambda: self._git.request(method, path, body))
        raw = self._wire(stage, reply, status, (JSON_MEDIA,))
        value = self._invoke('PARSE_' + stage, lambda: strict_json(raw))
        if type(value) is not dict:
            self._fail('JSON_OBJECT92_' + stage)
        return value

    def _blob(self, sha):
        reply = self._invoke('READ_BLOB', lambda: self._git.request('GET', '/git/blobs/' + sha, None))
        wire = self._wire('READ_BLOB', reply, 200, (JSON_MEDIA, RAW_MEDIA))
        if reply.media_type == JSON_MEDIA:
            envelope = self._invoke('PARSE_BLOB', lambda: strict_json(wire))
            raw = self._invoke('NORMALIZE_BLOB', lambda: blob_json_bytes(envelope, sha, len(self.raw)))
        else:
            raw = wire  # Explicit negotiated raw representation, never guessed.
        if len(raw) > MAX_BLOB or raw != self.raw or git_oid('blob', raw) != sha:
            self._fail('WHOLE_BLOB_BYTES92')
        return raw

    def _identity(self):
        repo = self._call('REPOSITORY', 'GET', '')
        if repo.get('id') != REPO_ID or repo.get('full_name') != REPO:
            self._fail('FOREIGN_REPOSITORY91')

    @_private_failure
    def reserve(self):
        if self.attempted or self.first_primary is not None:
            self._fail('CONSUMED_OR_UNKNOWN_NO_RETRY91')
        self.attempted = True  # Before marker, client, credential or remote call.
        if self.local_marker:
            self._invoke('LOCAL_ATTEMPT', lambda: self.capture.reserve_attempt(self.key))
        self._identity()
        blob = self._call('CREATE_BLOB', 'POST', '/git/blobs',
                          {'encoding': 'base64', 'content': base64.b64encode(self.raw).decode()}, 201)
        if blob.get('sha') != self.blob:
            self._fail('BLOB_ID91')
        entries = [{'path': PATH, 'mode': '100644', 'type': 'blob', 'sha': self.blob}]
        tree = self._call('CREATE_TREE', 'POST', '/git/trees', {'tree': entries}, 201)
        if tree.get('sha') != self.tree:
            self._fail('TREE_ID91')
        commit = self._call('CREATE_COMMIT', 'POST', '/git/commits',
                            {'message': self.message, 'tree': self.tree, 'parents': [self.plan.source_commit]}, 201)
        if not hexid(commit.get('sha'), 40):
            self._fail('COMMIT_ID91')
        # The single durable atomic transition. No update, delete, adoption,
        # preflight GET of the nonce, recovery create, or refund exists here.
        created = self._call('CREATE_REF', 'POST', '/git/refs',
                             {'ref': self.ref, 'sha': commit['sha']}, 201)
        if (created.get('ref') != self.ref or created.get('object', {}).get('type') != 'commit'
                or created['object'].get('sha') != commit['sha']):
            self._fail('CREATE_REF_AMBIGUOUS_CONSUMED91')
        self._receipt = {'schema': 'TRACEHARBOR_FRESH_ONE_RECEIPT91_V1',
                         'invocation': self.plan.invocation, 'source_commit': self.plan.source_commit,
                         'ref': self.ref, 'record_sha256': digest(self.raw),
                         'blob': self.blob, 'tree': self.tree, 'commit': commit['sha'],
                         'deadline_utc': self.plan.deadline_utc}
        self._readback()
        self._verified = True
        return copy.deepcopy(self._receipt)

    def _readback(self):
        r = self._receipt
        self._identity()
        ref = self._call('READ_REF', 'GET', '/git/ref/' + self.ref.removeprefix('refs/'))
        commit = self._call('READ_COMMIT', 'GET', '/git/commits/' + r['commit'])
        tree = self._call('READ_TREE', 'GET', '/git/trees/' + r['tree'])
        projection = self._invoke('TREE_PROJECT', lambda: tree_projection(tree, r['blob'], len(self.raw), r['tree']))
        raw = self._blob(r['blob'])
        expected = [{'path': PATH, 'mode': '100644', 'type': 'blob', 'sha': r['blob']}]
        if (ref.get('ref') != self.ref or ref.get('object', {}).get('type') != 'commit'
                or ref['object'].get('sha') != r['commit']
                or commit.get('sha') != r['commit'] or commit.get('message') != self.message
                or commit.get('tree', {}).get('sha') != r['tree']
                or [x.get('sha') for x in commit.get('parents', [])] != [self.plan.source_commit]
                or tree.get('sha') != r['tree'] or projection != expected or raw != self.raw
                or git_oid('blob', raw) != r['blob']):
            self._fail('FULL_IMMUTABLE_READBACK_MISMATCH91')
        self._check('POST_RETURN_FULL_READBACK')

    @_private_failure
    def verify(self, receipt):
        # This process-local cache never promotes serialized receipts to native
        # authority, and a new instance cannot adopt an old instance's receipt.
        self._check('PRE_RECEIPT')
        if (not self._verified or self._receipt is None or type(receipt) is not dict
                or canonical(receipt) != canonical(self._receipt)):
            self._fail('RECEIPT_INVOCATION_OR_BYTES91')
        return copy.deepcopy(self.record)


class _SyntheticBackend(_GitRecordCore):
    classification = 'SYNTHETIC_ALGORITHM_ONLY_NOT_NATIVE'
    def __init__(self, plan, fake_git, capture, clock):
        record = record_for(plan)
        if type(capture) is not PrivateOriginals:
            raise Refuse('EXPLICIT_PRIVATE_CAPTURE_REQUIRED91')
        super().__init__(plan, record, fake_git, capture, clock, namespace=NAMESPACE,
                         message=MESSAGE, local_marker=True)


def synthetic_backend(plan, fake_git, capture, clock):
    """Explicit fake-client route; callbacks cannot confer native authority."""
    return _SyntheticBackend(plan, fake_git, capture, clock)


if __name__ == '__main__':
    OneBackend()
