"""Private release integration; import, qualification and default startup dispatch nothing.

The immutable accepted product modules remain untouched. A source-bound configuration, existing funded-attempt authority and actual
proxy/operator evidence are mandatory. Provider inference access remains unproved
until the one intended recorded request; no new billing activation is performed. This
first phase admits only the NEW already-counted request, once inside the 256-call
allocation. The remaining 255 are held; old or UNKNOWN requests cannot enter.
"""
import hashlib
import hmac
import json
import math
import ipaddress
import os
import re
import stat
import subprocess
import sys
import threading
import time
from http.cookies import SimpleCookie
from pathlib import Path
from urllib.parse import parse_qs

import release_policy
import runtime_service
import edge_policy
import capture_routes
from edge_adapter import EdgeHandler
from quota_ledger import Ledger, exclusive, private_dir, read
from release_policy import Refusal, canonical, digest, validate_config
from reviewed_runtime import ReviewedSession
from render_preflight import StagingServer

ADMITTED_CONFIG_SHA256 = None
ADMITTED_CAPTURE_SHA256 = None
ADMITTED_EVIDENCE_SHA256 = None
NEW_REQUEST = '81f50ab6b607f969d213375529c4f48da022e45514ed3831f1132318e63f43d5'
SOURCE_COMMIT = 'f6e5744a6c32523922480f0e81252a34dba0ddd3'
HOST = 'traceharbor.onrender.com'
STATE = Path('/var/data/traceharbor-release68')
VENDOR = Path('/var/data/traceharbor-staging/install65/vendor/nemotron-input-counter-v0.2.1')
COOKIE = '__Host-traceharbor-operator68'
WORKER_WALL_SECONDS = 45
WORKER_ENTRY = Path(__file__).resolve()
WORKER_ADMISSION_PATH = None


def checked_manifest(path, pins):
    root = Path(path)
    for name, expected in pins.items():
        p = root / name
        if Path(name).is_absolute() or '..' in Path(name).parts or p.is_symlink():
            raise Refusal('SOURCE_PATH')
        data = p.read_bytes()
        if len(data) != expected['bytes'] or hashlib.sha256(data).hexdigest() != expected['sha256']:
            raise Refusal('SOURCE_DRIFT')


def qualify(config, evidence, *, pin, capture_pin, source_root):
    """Data-only gate: never inspect a credential, create state, count or bind."""
    validate_config(config)
    if ADMITTED_CONFIG_SHA256 is None or pin != ADMITTED_CONFIG_SHA256 or pin != digest(config):
        raise Refusal('ACTUAL_RELEASE_BINDING_REQUIRED')
    if ADMITTED_CAPTURE_SHA256 is None or capture_pin != ADMITTED_CAPTURE_SHA256:
        raise Refusal('ACTUAL_CAPTURE_BINDING_REQUIRED')
    if ADMITTED_EVIDENCE_SHA256 is None or digest(evidence) != ADMITTED_EVIDENCE_SHA256:
        raise Refusal('ACTUAL_EVIDENCE_BINDING_REQUIRED')
    expected = {'schema', 'service', 'host', 'baseline_commit', 'proxy_peers',
                'proxy_observation_sha256', 'operator_verifier', 'funded_attempt_admitted',
                'funded_attempt_receipt_sha256', 'source_pins', 'counter_certificate',
                'prior_effects_sha256', 'capture_authority_id', 'AI_authority_id'}
    if type(evidence) is not dict or set(evidence) != expected:
        raise Refusal('ACTUAL_RELEASE_EVIDENCE_SHAPE')
    if (evidence['schema'] != 'traceharbor.actual-release68.v1' or
        evidence['service'] != 'srv-dbh6hgh42hec73c3g9m0' or
        evidence['host'] != config['public_hostname'] or evidence['host'] != HOST or
        evidence['baseline_commit'] != SOURCE_COMMIT or
        evidence['prior_effects_sha256'] != config['prior_effects_sha256'] or
        evidence['AI_authority_id'] != 'TRACEHARBOR-LIVE67-AI256-INCLUSIVE-APPROVED' or
        evidence['capture_authority_id'] != 'TRACEHARBOR-LIVE67-NATIVE-CAPTURE164-APPROVED'):
        raise Refusal('ACTUAL_RELEASE_IDENTITY')
    if evidence['funded_attempt_admitted'] is not True:
        raise Refusal('FUNDED_ATTEMPT_NOT_ADMITTED')
    if evidence['operator_verifier'] != 'NATIVE_RENDER_OWNER_SINGLE_USE_SESSION':
        raise Refusal('ACTUAL_OPERATOR_VERIFIER_REQUIRED')
    for name in ('proxy_observation_sha256', 'funded_attempt_receipt_sha256'):
        if type(evidence[name]) is not str or not re.fullmatch('[a-f0-9]{64}', evidence[name]):
            raise Refusal('ACTUAL_PROVIDER_RECEIPT_REQUIRED')
    if not evidence['proxy_peers'] or type(evidence['proxy_peers']) is not list:
        raise Refusal('ACTUAL_PROXY_OBSERVATION_REQUIRED')
    certificate = evidence['counter_certificate']
    expected_certificate = {'count': 1169, 'request_sha256': NEW_REQUEST,
                            'template_sha256': release_policy.TEMPLATE,
                            'tokenizer_revision': release_policy.REVISION}
    if certificate != expected_certificate:
        raise Refusal('ACCEPTED_COUNTER_CERTIFICATE_REQUIRED')
    checked_manifest(source_root, evidence['source_pins'])
    policy = edge_policy.EdgePolicy(config, proxy_peers=evidence['proxy_peers'], reviewed_pin=pin)
    return policy


class AcceptedCertificate:
    """Reuse the accepted numeric proof; never rerun its counter or accept another input."""
    def __init__(self, certificate):
        self.certificate = dict(certificate)

    def count(self, payload):
        if digest(payload) != NEW_REQUEST or self.certificate['request_sha256'] != NEW_REQUEST:
            raise Refusal('FIRST_PHASE_EXACT_NEW_REQUEST_ONLY')
        return dict(self.certificate)


class OperatorSession:
    """One ephemeral internal capture grant, no Owner password or provider key.

    Enrollment is performed only by the already authenticated native Render
    operator. A public session cannot enroll itself or gain capture privileges.
    Raw grant/cookie values must never enter logs, URLs, exports or checkpoints.
    """
    def __init__(self, directory, *, clock=time.time):
        self.directory = private_dir(directory)
        self.clock = clock
        self.lock = threading.Lock()

    def consume_grant(self, raw):
        if type(raw) is not bytes or not re.fullmatch(rb'[a-f0-9]{64}', raw):
            raise Refusal('OPERATOR_GRANT_SHAPE')
        with self.lock:
            grant = read(self.directory / 'grant.json')
            if (set(grant) != {'sha256', 'expires', 'scope'} or
                grant['scope'] != 'ONE_TRACEHARBOR_CAPTURE164' or
                type(grant['expires']) not in (int, float) or not math.isfinite(grant['expires']) or self.clock() >= grant['expires'] or
                not hmac.compare_digest(hashlib.sha256(raw).hexdigest(), grant['sha256'])):
                raise Refusal('OPERATOR_GRANT_REFUSED')
            # Exclusive reservation remains consumed even if cookie delivery is lost.
            exclusive(self.directory / 'grant-consumed.json', {'scope': grant['scope'], 'retry': False})
            token = os.urandom(32).hex()
            exclusive(self.directory / 'session.json', {
                'sha256': hashlib.sha256(token.encode()).hexdigest(),
                'expires': min(grant['expires'], self.clock() + 900), 'scope': grant['scope']})
            return token

    def authorize(self, handler):
        try:
            if len(handler.headers.get_all('Cookie', [])) != 1:
                return False
            cookie = SimpleCookie(); cookie.load(handler.headers['Cookie'])
            value = cookie[COOKIE].value
            session = read(self.directory / 'session.json')
            return (len(value) == 64 and session['scope'] == 'ONE_TRACEHARBOR_CAPTURE164' and
                    self.clock() < session['expires'] and
                    hmac.compare_digest(hashlib.sha256(value.encode()).hexdigest(), session['sha256']))
        except Exception:
            return False


class CapturedOnceSession:
    """Serialize one exact new call only after an acknowledged native media chunk.

    A separate process owns the native wall guard. Killing it does not refund its
    durable reservation, cancel provider billing, or create retry authority.
    """
    def __init__(self, config, directory, sink, *, worker=None):
        self.config = config
        self.directory = private_dir(directory)
        self.sink = sink
        self.worker = run_worker if worker is None else worker
        self.lock = threading.Lock()

    def status(self):
        exists = (self.directory / 'e2e-reserved.json').exists()
        ready = (self.sink is not None and self.sink.bytes > 0 and not self.sink.terminal
                 and (self.directory/'capture-started.json').is_file())
        return {'schema': 'traceharbor.runtime-status.v1', 'enabled': ready and not exists,
                'new_call_cap': 1 if ready and not exists else 0,
                'state': 'ONE_RECORDED_E2E_ONLY', 'reason': 'OTHER_255_HELD',
                'mode': 'SYNTHETIC_AND_HISTORICAL_REMAIN_SEPARATE', 'retry': False}

    def dispatch(self, raw):
        _, payload, _ = runtime_service.prepare(raw)
        if digest(payload) != NEW_REQUEST:
            raise runtime_service.RuntimeRefusal('FIRST_PHASE_EXACT_NEW_REQUEST_ONLY')
        with self.lock:
            if not self.status()['enabled']:
                raise runtime_service.RuntimeRefusal('RECORDING_OR_ONCE_GATE')
            try:
                exclusive(self.directory / 'e2e-reserved.json', {
                    'request_sha256': NEW_REQUEST, 'state': 'UNKNOWN_CONSUMED_NO_RETRY',
                    'recorded_bytes_before_dispatch': self.sink.bytes,
                    'recorded_chunks_before_dispatch': self.sink.next, 'retry': False})
            except Exception:
                raise runtime_service.RuntimeRefusal('E2E_RESERVATION_UNKNOWN', consumed=True) from None
            return self.worker(raw, self.config, self.directory)


def run_worker(raw, config, directory):
    started = time.monotonic()
    command = [sys.executable, str(Path(WORKER_ENTRY).resolve()), '--worker', str(directory)]
    # Credentials stay inside the selected service and are never placed in argv/stdin.
    environment = {k: v for k, v in os.environ.items()
                   if k in {'PATH', 'LANG', 'LC_ALL', 'NEBIUS_API_KEY', 'RENDER',
                            'RENDER_EXTERNAL_HOSTNAME', 'RENDER_GIT_COMMIT'}}
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    def limits():
        import resource
        resource.setrlimit(resource.RLIMIT_CPU, (10, 10))
        resource.setrlimit(resource.RLIMIT_FSIZE, (1048576, 1048576))
    try:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL, env=environment, preexec_fn=limits)
        try:
            out, _ = process.communicate(raw, timeout=max(.01, WORKER_WALL_SECONDS-5-(time.monotonic()-started)))
        except subprocess.TimeoutExpired:
            process.kill(); process.communicate(timeout=4)
            raise Refusal('WHOLE_ATTEMPT_WALL_EXHAUSTED') from None
        if process.returncode != 0 or len(out) > runtime_service.MAX_RESULT:
            raise Refusal('WORKER_OUTCOME_UNKNOWN')
        result = runtime_service.verify_runtime_result(json.loads(out))
        exclusive(directory / 'e2e-result.json', result)
        return result
    except Exception:
        raise runtime_service.RuntimeRefusal('E2E_OUTCOME_UNKNOWN_NO_RETRY', consumed=True) from None


def worker(directory):
    directory = private_dir(directory)
    data = read(WORKER_ADMISSION_PATH or directory / 'admission.json', 65536)
    config, evidence = data['config'], data['evidence']
    # Even trusted process startup cannot bypass the source-bound trusted launch pins.
    qualify(config, evidence, pin=digest(config), capture_pin=digest(evidence),
            source_root=Path(__file__).resolve().parent)
    release_policy.REVIEWED_RELEASE_SHA256 = digest(config)
    runtime_service.GLOBAL_NEW_CALL_CAP = 256
    session = ReviewedSession(config, Ledger(directory / 'allocation', config),
                              AcceptedCertificate(evidence['counter_certificate']))
    raw = sys.stdin.buffer.read(runtime_service.MAX_REQUEST + 1)
    if len(raw) > runtime_service.MAX_REQUEST:
        raise Refusal('WORKER_INPUT_BOUND')
    result = session.dispatch(raw)
    sys.stdout.buffer.write(canonical(result)); sys.stdout.buffer.flush()


class ReleaseHandler(EdgeHandler):
    def _tls_envelope(self):
        p=self.server.edge_policy
        hosts=self.headers.get_all('Host',[]);origins=self.headers.get_all('Origin',[])
        return (hosts==[p.host] and len(origins)<=1 and (not origins or origins==[p.origin]) and
                (self.command!='POST' or origins==[p.origin]) and
                self.headers.get_all('X-Forwarded-Proto',[])==['https'] and
                self.headers.get_all('X-Forwarded-Host',[]) in ([],[p.host]) and
                not self.headers.get_all('Transfer-Encoding',[]) and
                len(self.headers.get_all('Content-Length',[]))<=1)

    def _qualify_owner_peer(self):
        # Called ONLY after a valid native Owner grant/session. Never from a
        # public flag/header alone; no CIDR wildcard or trust-all-proxies rule.
        peer=ipaddress.ip_address(self.client_address[0])
        if not peer.is_private or peer.is_loopback or peer.is_unspecified:
            raise Refusal('PRIVATE_RENDER_PEER_REQUIRED')
        peer=str(peer);policy=self.server.edge_policy
        with self.server.peer_enrollment_lock:
            if peer not in policy.peers:
                root=STATE/'qualified-proxy-peers';root.mkdir(mode=0o700,exist_ok=True);private_dir(root)
                path=root/(hashlib.sha256(peer.encode()).hexdigest()+'.json')
                value={'proxy_peer':peer,'release_config_sha256':digest(policy.config),
                       'proof':'NATIVE_OWNER_AUTHENTICATED_HTTPS_SESSION',
                       'scope':'ONE_APPROVED_CAPTURE164_AND_RECORDED_E2E'}
                if path.exists():
                    if read(path)!=value:raise Refusal('PROXY_ENROLLMENT_MISMATCH')
                else:exclusive(path,value)
                policy.peers=policy.peers|{peer}
        return True

    def _public_safe_route(self):
        # These exact routes were public in the synthetic staging release.
        # They contain no operator/session/media/provider capability. Render's
        # private ingress peers are ephemeral: do not make public assets depend
        # on a previous operator login or persist them as authenticated peers.
        # Host/Origin/TLS/framing validation still applies before this method.
        try:
            peer=ipaddress.ip_address(self.client_address[0])
            if not peer.is_private or peer.is_loopback or peer.is_unspecified:return False
        except ValueError:return False
        if self.command=='POST':return self.path in {'/analyze','/verify','/evolution'}
        if self.command!='GET':return False
        import app
        return (self.path in app.STATIC or self.path in {'/runtime/status','/scenarios/evolution.json'} or
                self.path in {'/fixtures/'+name+'.json' for name in app.CASES})

    def allowed(self):
        if not self._tls_envelope():return False
        if self._public_safe_route():return True
        if self.client_address[0] in self.server.edge_policy.peers:return True
        # This public page contains only a login form, no protected capability.
        if self.command=='GET' and self.path=='/operator/session':return True
        if self.server.operator.authorize(self):return self._qualify_owner_peer()
        return False

    def do_GET(self):
        if self.path == '/healthz':
            return self.respond(200, canonical({'phase': 'RELEASE68', 'public_AI_enabled': False,
                'other_255_held': True, 'source_commit': self.server.source_commit}))
        if not self.allowed():
            return self.error(403, 'Qualified TLS edge required.')
        if self.path == '/operator/session':
            body = (b'<!doctype html><html lang="en"><meta charset="utf-8">'
                b'<title>TraceHarbor private operator</title><h1>Private capture operator</h1>'
                b'<p>One existing-owner grant. No provider key or account password.</p>'
                b'<form method="post" action="/operator/session"><label>One-use capture grant '
                b'<input name="grant" type="password" autocomplete="off" required></label>'
                b'<button type="submit">Open private capture session</button></form></html>')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Referrer-Policy', 'same-origin')
            self.send_header('Content-Security-Policy', "default-src 'none'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers(); self.wfile.write(body); return
        if self.path == '/private-capture/' and self.server.runtime_session.sink.terminal:
            if not self.server.operator.authorize(self):
                return self.error(403,'Private capture only.')
            # A consumed/partial/unknown attempt is a read-only retained state,
            # never another recording page, retry button or implicit reset.
            return self.respond(200,b'<!doctype html><html lang="en"><meta charset="utf-8"><title>TraceHarbor retained capture</title><h1>Previous capture retained</h1><p>This capture attempt is closed. No automatic retry or new recording is admitted.</p></html>','text/html; charset=utf-8')
        if self.path == '/private-capture/controller.js':
            if not self.server.operator.authorize(self) or not self.server.capture_router.enabled():
                return self.error(403, 'Private capture not admitted.')
            return self.respond(200, (Path(__file__).parent/'capture_controller75.js').read_bytes(), 'text/javascript; charset=utf-8')
        if self.path == '/operator68.js':
            if not self.server.operator.authorize(self):
                return self.error(403, 'Private operator only.')
            return self.respond(200, (Path(__file__).parent/'operator68.js').read_bytes(), 'text/javascript; charset=utf-8')
        if self.path == '/demo68.json':
            if not self.server.operator.authorize(self):
                return self.error(403, 'Private operator only.')
            return self.respond(200, (Path(__file__).parent/'runtime_demo68.json').read_bytes())
        if self.path == '/' and self.server.operator.authorize(self):
            import app
            body = (app.ROOT/'web/index.html').read_bytes()
            body = body.replace(b'</body>', b'<script src="/operator68.js" defer></script></body>')
            return self.respond(200, body, 'text/html; charset=utf-8')
        if self.path == '/runtime/status' and not self.server.operator.authorize(self):
            return self.respond(200, canonical({'schema': 'traceharbor.runtime-status.v1',
                'enabled': False, 'new_call_cap': 0, 'reason': 'RECORDED_E2E_PENDING', 'retry': False}))
        return super().do_GET()

    def do_POST(self):
        if self.path in {'/private-capture/chunk','/private-capture/finish'} and not (STATE/'capture-started.json').is_file():
            return self.error(403,'Native selection must be durably acknowledged first.')
        if self.path == '/private-capture/selected':
            try:
                if not self.allowed() or not self.server.operator.authorize(self):raise Refusal('PRIVATE_NATIVE_SELECTION_REQUIRED')
                if self.headers.get('Content-Type')!='application/json' or len(self.headers.get_all('Content-Length',[]))!=1:raise Refusal('SELECTION_HEADERS')
                length=int(self.headers['Content-Length'])
                if not 1<=length<=128:raise Refusal('SELECTION_BOUND')
                raw=self.rfile.read(length)
                if len(raw)!=length or json.loads(raw)!={'phase':'TAB_SELECTED_BEFORE_RECORDER'}:raise Refusal('SELECTION_SHAPE')
                if self.server.runtime_session.sink.bytes or self.server.runtime_session.sink.terminal or (STATE/'e2e-reserved.json').exists():raise Refusal('ALREADY_STARTED')
                exclusive(STATE/'capture-started.json',{'id':'TRACEHARBOR-LIVE67-NATIVE-CAPTURE164-APPROVED',
                    'state':'NATIVE_TAB_SELECTED_RESERVED_UNKNOWN_NO_RETRY','seconds':164,'retry':False})
                return self.respond(200,canonical({'recording_started':True,'retry':False}))
            except Exception:return self.error(403,'Native selection refused or unknown; no automatic retry.')
        if self.path == '/operator/session':
            try:
                if (not self._tls_envelope() or self.headers.get('Content-Type') != 'application/x-www-form-urlencoded' or
                    self.headers.get_all('Transfer-Encoding', []) or
                    len(self.headers.get_all('Content-Length', [])) != 1):
                    raise Refusal('OPERATOR_HEADERS')
                length = int(self.headers['Content-Length'])
                if not 1 <= length <= 512:
                    raise Refusal('OPERATOR_BODY_BOUND')
                body = self.rfile.read(length)
                if len(body) != length:
                    raise Refusal('OPERATOR_BODY_TRUNCATED')
                form = parse_qs(body.decode('ascii'), strict_parsing=True, max_num_fields=1)
                if set(form) != {'grant'} or len(form['grant']) != 1:
                    raise Refusal('OPERATOR_BODY_SHAPE')
                token = self.server.operator.consume_grant(form['grant'][0].encode())
                self._qualify_owner_peer()
                self.send_response(303)
                self.send_header('Location', '/private-capture/')
                self.send_header('Set-Cookie', COOKIE+'='+token+'; Path=/; Secure; HttpOnly; SameSite=Strict; Max-Age=900')
                self.send_header('Cache-Control', 'no-store')
                self.send_header('Content-Length', '0')
                self.end_headers()
            except Exception:
                self.error(403, 'One-use operator session refused; no automatic retry.')
            return
        if self.path == '/runtime/analyze' and not self.server.operator.authorize(self):
            return self.error(403, 'Operator-recorded first E2E only; public judging calls remain held.')
        return super().do_POST()


def build_server(config, evidence, *, port, platform_port, directory=STATE):
    # Nothing is enrolled or bound until ALL protected gates have passed.
    policy = qualify(config, evidence, pin=digest(config), capture_pin=digest(evidence),
                     source_root=Path(__file__).resolve().parent)
    edge_policy.REVIEWED_EDGE_SHA256 = digest(config)
    address = policy.validate_listener(port, platform_port)
    directory = private_dir(directory)
    operator = OperatorSession(directory / 'operator')
    # Custody must be provisioned once by admitted setup, never reconstructed/reset.
    from capture_sink import MediaSink
    capture_path=private_dir(directory/'capture')
    consumed_capture = ((directory/'capture-started.json').exists() or
        (capture_path/'terminal.json').exists() or
        any(p.name!='custody.json' for p in capture_path.iterdir()) or
        (directory/'e2e-reserved.json').exists() or
        Ledger(directory/'allocation',config).snapshot()['reserved_calls']!=0)
    if (capture_path/'custody.json').exists() and consumed_capture:
        # Public boot must not depend on re-opening a consumed recorder. Attach
        # a permanently closed, read-only view; write no marker/quota/custody.
        expected={'schema':'traceharbor.capture48.v1','classification':'SYNTHETIC_ONLY','seconds':164,'byte_limit':25165824}
        if read(capture_path/'custody.json')!=expected:raise Refusal('RETAINED_CUSTODY_PIN')
        entries=list(capture_path.iterdir())
        for entry in entries:
            info=entry.lstat()
            if not stat.S_ISREG(info.st_mode) or info.st_uid!=os.getuid() or info.st_mode&0o077:raise Refusal('RETAINED_CAPTURE_PRIVATE_FILE')
        media=[entry for entry in entries if re.fullmatch(r'chunk-[0-9]{5}\.webm',entry.name)]
        sink=MediaSink.__new__(MediaSink);sink.path=capture_path;sink.bytes=sum(entry.stat().st_size for entry in media);sink.next=len(media);sink.terminal=True;sink.lock=threading.Lock()
    elif (capture_path/'custody.json').exists():
        # EXACTLY ONE known pre-effect repair. This is not a resume/reset API.
        # Owner-native evidence bound in the launch admission proves no picker
        # invocation; the durable state independently must still be empty.
        if ((directory/'capture-started.json').exists() or set(x.name for x in capture_path.iterdir())!={'custody.json'} or
            (directory/'e2e-reserved.json').exists() or
            Ledger(directory/'allocation',config).snapshot()['reserved_calls']!=0):
            raise Refusal('CAPTURE_OR_AI_STATE_NOT_UNSTARTED')
        expected={'schema':'traceharbor.capture48.v1','classification':'SYNTHETIC_ONLY','seconds':164,'byte_limit':25165824}
        if read(capture_path/'custody.json')!=expected:raise Refusal('UNSTARTED_CUSTODY_PIN')
        marker={'id':'TRACEHARBOR-SOURCEBOUND-E2E70-PRE_EFFECT_REPAIR_ONCE',
            'state':'KNOWN_NO_PICKER_NO_CAPTURE_NO_AI','checkpoint72_sha256':'efa1b0b0c1b261d08a501a45c3b5ac54036d6f1eb10eb81b979272d9c8f7280e',
            'quota_reset':False,'custody_rewritten':False,'retry':False}
        path=directory/'pre-effect-reattach74.json'
        if path.exists():
            if read(path)!=marker:raise Refusal('ORIGINAL_SETUP_RECEIPT_MISMATCH')
        else:exclusive(path,marker)
        # Reading an already-applied EMPTY setup receipt is not another capture.
        # A new durable native-selection marker closes this path BEFORE Recorder.start.

        sink=MediaSink.__new__(MediaSink);sink.path=capture_path;sink.bytes=0;sink.next=0;sink.terminal=False;sink.lock=threading.Lock()
    else:sink = MediaSink(capture_path, admitted=True)
    capture_routes.CAPTURE_RELEASE_SHA256 = digest(evidence)
    router = capture_routes.CaptureRoutes(pin=digest(evidence), authorize=operator.authorize, sink=sink)
    server = StagingServer(address, ReleaseHandler)
    server.edge_policy = policy
    server.operator = operator
    server.peer_enrollment_lock=threading.Lock()
    server.capture_router = router
    server.runtime_session = CapturedOnceSession(config, directory, sink)
    server.source_commit = os.environ.get('RENDER_GIT_COMMIT', 'UNOBSERVED')
    return server


def provision_once(config, evidence, directory=STATE):
    """Native-Render-owner setup only, after admission; never called from HTTP.

    The return value is an ephemeral internal grant and must stay on the native
    UI transfer path, never in an LLM response, URL, log or saved checkpoint.
    Any partial setup is retained and is NOT eligible for a blind retry.
    """
    qualify(config, evidence, pin=digest(config), capture_pin=digest(evidence),
            source_root=Path(__file__).resolve().parent)
    if os.environ.get('RENDER_EXTERNAL_HOSTNAME') != HOST or os.environ.get('RENDER') != 'true':
        raise Refusal('EXACT_NATIVE_RENDER_HOST_REQUIRED')
    directory = Path(directory)
    if directory != STATE or any(p.is_symlink() for p in (directory, *directory.parents)):
        raise Refusal('EXACT_NATIVE_PRIVATE_STATE_REQUIRED')
    directory.mkdir(mode=0o700, exist_ok=False)
    private_dir(directory)
    exclusive(directory/'admission.json', {'config': config, 'evidence': evidence})
    Ledger.provision(directory/'allocation', config)
    (directory/'operator').mkdir(mode=0o700)
    (directory/'capture').mkdir(mode=0o700)
    grant = os.urandom(32).hex()
    exclusive(directory/'operator/grant.json', {
        'sha256': hashlib.sha256(grant.encode()).hexdigest(),
        'expires': time.time()+900, 'scope':'ONE_TRACEHARBOR_CAPTURE164'})
    return grant


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--worker':
        worker(Path(sys.argv[2]))
    else:
        raise SystemExit('RELEASE68_NOT_ADMITTED: no default bind, AI, capture or enrollment')
