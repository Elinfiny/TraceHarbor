"""Private, inactive GUI/runtime bridge. Global new-call cap remains ZERO.

Reuses the existing nebius request/decoder/HTTPBoundary and provider-record verifier.
No env/client flag can enable it. A separate reviewed release must bind a new
request and authorize a single persistent host before these constants can change.
"""
import http.client
import os
import stat
import threading
import time
from pathlib import Path
from core import canonical, digest, import_package, shape
from live_service import build_record, verify_record, verified_analysis
import nebius

GLOBAL_NEW_CALL_CAP = 0
REVIEWED_REQUEST_SHA256 = None
MODEL = 'nvidia/Nemotron-3_5-Lightning'
MAX_REQUEST = 65536
MAX_RESULT = 262144
DEADLINE_SECONDS = 45
SCHEMA = 'traceharbor.runtime-result.v1'
LIMITS = ('Server transport metadata is not independent origin attestation. '
          'Citation integrity is not semantic entailment or production diagnosis. '
          'No remediation executes. Imported results never prove a current call.')


class RuntimeRefusal(ValueError):
    def __init__(self, code, *, consumed=False):
        super().__init__(code)
        self.code, self.consumed = code, consumed

    def public(self):
        return {'error': self.code, 'effect': 'UNKNOWN_CONSUMED_NO_RETRY' if self.consumed
                else 'KNOWN_NO_DISPATCH', 'retry': False}


def status():
    # Do not inspect credentials, storage, provider, or budget through the browser.
    configured = (type(GLOBAL_NEW_CALL_CAP) is int and GLOBAL_NEW_CALL_CAP == 1
                  and type(REVIEWED_REQUEST_SHA256) is str
                  and len(REVIEWED_REQUEST_SHA256) == 64
                  and all(c in '0123456789abcdef' for c in REVIEWED_REQUEST_SHA256))
    return {'schema': 'traceharbor.runtime-status.v1', 'enabled': configured,
            'new_call_cap': GLOBAL_NEW_CALL_CAP, 'state': 'SERVER_PREFLIGHT_REQUIRED' if configured else 'NOT_ADMITTED',
            'reason': 'NEW_CALL_CAP_ZERO' if GLOBAL_NEW_CALL_CAP == 0 else 'EXACT_REVIEWED_RELEASE_REQUIRED',
            'mode': 'SYNTHETIC_AND_HISTORICAL_REMAIN_SEPARATE', 'retry': False}


def prepare(raw):
    evidence = import_package(raw)
    payload = nebius.request_for(evidence, MODEL)
    payload['messages'][0]['content'] += (
        ' For status unknown, hypotheses and remediation MUST both be empty arrays. '
        'Do not invent a hypothesis to avoid unknown.')
    encoded = canonical(payload)
    if len(encoded) > MAX_REQUEST:
        raise RuntimeRefusal('REQUEST_TOO_LARGE')
    return evidence, payload, encoded


def _credential(environment):
    key = environment.get('NEBIUS_API_KEY')
    if type(key) is not str or not 1 <= len(key) <= 4096 or '\r' in key or '\n' in key:
        raise RuntimeRefusal('CREDENTIAL_NOT_CONFIGURED')
    return key


class _MemoryCapture:
    """Bounded process-memory originals only. Never serialize exceptions or bodies."""
    scope = 'SYNTHETIC_ONLY'

    def __init__(self):
        self.originals = []
        self.bytes_seen = 0

    def retain(self, stage, kind, value):
        if len(self.originals) >= 96:
            raise RuntimeRefusal('CAPTURE_BOUND')
        if type(value) is bytes:
            self.bytes_seen += len(value)
            if len(value) > MAX_RESULT + 1 or self.bytes_seen > 2 * (MAX_RESULT + 1):
                raise RuntimeRefusal('CAPTURE_BOUND')
        self.originals.append((stage, kind, value))


def _private_directory(value):
    if not isinstance(value, (str, Path)) or not Path(value).is_absolute():
        raise RuntimeRefusal('PRIVATE_STATE_NOT_CONFIGURED')
    directory = Path(value)
    # Only a pre-existing, administrator-owned POSIX private directory qualifies.
    # No directory creation, chmod, secret enrollment, Windows ACL assumption, or fallback.
    if os.name != 'posix' or any(p.is_symlink() for p in (directory, *directory.parents)):
        raise RuntimeRefusal('PRIVATE_STATE_NOT_QUALIFIED')
    info = directory.stat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise RuntimeRefusal('PRIVATE_STATE_NOT_QUALIFIED')
    return directory


def _write_exclusive(path, value):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as out:
        out.write(canonical(value)); out.flush(); os.fsync(out.fileno())
    fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def verify_runtime_result(value):
    shape(value, {'schema', 'mode', 'record', 'attempt', 'limits', 'dossier_sha256'})
    if value['schema'] != SCHEMA or value['mode'] != 'SERVER_RUNTIME_RECORD_ORIGIN_UNATTESTED':
        raise ValueError('Unsupported runtime record.')
    verify_record(value['record'])
    if value['record']['provider']['model'] != MODEL:
        raise ValueError('Runtime model mismatch.')
    if value['attempt'] != {'request_attempted': True, 'retry': False,
                            'origin': 'NOT_INDEPENDENTLY_ATTESTED', 'deadline_seconds': DEADLINE_SECONDS}:
        raise ValueError('Runtime declaration mismatch.')
    if value['limits'] != LIMITS or len(canonical(value)) > MAX_RESULT:
        raise ValueError('Runtime bounds mismatch.')
    if digest({k: v for k, v in value.items() if k != 'dossier_sha256'}) != value['dossier_sha256']:
        raise ValueError('Runtime hash mismatch.')
    return value


class RuntimeSession:
    """One process + exclusive persistent marker, never account-wide exactly-once.

    Production uses only the fixed HTTPS transport. `_factory`/`_environment` are
    trusted Python test dependencies, never request parameters or UI settings.
    All current production paths refuse BEFORE credential access or reservation.
    """
    def __init__(self, *, _factory=None, _environment=None, _state_directory=None):
        self._factory = http.client.HTTPSConnection if _factory is None else _factory
        self._environment = os.environ if _environment is None else _environment
        self._directory = _state_directory
        self._lock = threading.Lock()
        self._attempted = False

    def dispatch(self, raw):
        with self._lock:
            if type(GLOBAL_NEW_CALL_CAP) is not int or GLOBAL_NEW_CALL_CAP != 1:
                raise RuntimeRefusal('NEW_CALL_CAP_ZERO')
            if self._attempted:
                raise RuntimeRefusal('ALREADY_RESERVED_NO_RETRY', consumed=True)
            try:
                evidence, payload, encoded = prepare(raw)
                if type(REVIEWED_REQUEST_SHA256) is not str or digest(payload) != REVIEWED_REQUEST_SHA256:
                    raise RuntimeRefusal('EXACT_REQUEST_NOT_ADMITTED')
                key = _credential(self._environment)
                directory = _private_directory(self._directory or self._environment.get('NEBIUS_RUNTIME_STATE_DIR'))
                self._attempted = True  # Reservation I/O can be ambiguous even without a surviving file.
                try:
                    _write_exclusive(directory/'runtime-once-v1.json', {
                        'state': 'RESERVED_UNKNOWN_NO_RETRY', 'request_sha256': digest(payload),
                        'model': MODEL, 'new_call_reservation': 1})
                except FileExistsError:
                    raise RuntimeRefusal('ALREADY_RESERVED_NO_RETRY', consumed=True) from None
                except OSError:
                    raise RuntimeRefusal('RESERVATION_UNKNOWN', consumed=True) from None
            except RuntimeRefusal:
                raise
            except Exception:
                raise RuntimeRefusal('PREFLIGHT_REJECTED') from None
            self._attempted = True
            capture = _MemoryCapture()
            boundary = nebius.HTTPBoundary(time.monotonic() + DEADLINE_SECONDS,
                                           capture, factory=self._factory)
            outcome, result = 'UNKNOWN_CONSUMED_NO_RETRY', None
            try:
                body = boundary.exchange(encoded, key, nebius.EXPECTED_PROJECT_ID)
                if key.encode() in body:
                    raise RuntimeRefusal('PROVIDER_SECRET_REFUSED', consumed=True)
                analysis, metadata = nebius.decode_response(body, MODEL)
                if key in canonical(analysis).decode('utf-8') or key in canonical(metadata).decode('utf-8'):
                    raise RuntimeRefusal('PROVIDER_SECRET_REFUSED', consumed=True)
                metadata['request_sha256'] = digest(payload)
                verified_analysis(analysis, evidence)
                record = build_record(raw, analysis, metadata)
                result = {'schema': SCHEMA, 'mode': 'SERVER_RUNTIME_RECORD_ORIGIN_UNATTESTED',
                    'record': record, 'attempt': {'request_attempted': True, 'retry': False,
                    'origin': 'NOT_INDEPENDENTLY_ATTESTED', 'deadline_seconds': DEADLINE_SECONDS},
                    'limits': LIMITS}
                result['dossier_sha256'] = digest(result)
                verify_runtime_result(result)
                outcome = 'VERIFIED_RECORD_SEMANTICS_NOT_VERIFIED'
            except Exception:
                # Never format provider exceptions, arbitrary status bodies, or credentials.
                result = None
            finally:
                receipt = {'state': outcome, 'request_sha256': digest(payload),
                           'request_attempted': boundary.request_attempted, 'retry': False,
                           'origin_attestation': False}
                if result is not None:
                    receipt['dossier_sha256'] = result['dossier_sha256']
                try:
                    _write_exclusive(directory/'runtime-terminal-v1.json', receipt)
                except Exception:
                    result = None  # Original reservation remains consumed, including reporting failure.
            if result is None:
                raise RuntimeRefusal('CALL_OUTCOME_UNKNOWN', consumed=True) from None
            return result


SESSION = RuntimeSession()
