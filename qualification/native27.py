"""PRIVATE_NATIVE_QUALIFICATION_ONLY; never grants model/pilot request authority.

Adapt unit17's fixed canary proposal and original-before-parse/deadline rules.
No native admission exists in this private candidate; workflow and entry are off.
Two separately admitted workflow_dispatch runs, not two jobs in one run.
Ephemeral memory is not crash-durable backup or provider cancellation.
"""
import datetime
import hashlib
import http.client
import json
import os
from pathlib import Path
import re
import time

REPO = 'Elinfiny/TraceHarbor'
RID, OWNER = 1391430317, 273768139
REF = 'refs/tags/traceharbor-once-qualification17/canary'
NONCE = 'TRACEHARBOR-NATIVE-QUALIFICATION27-20261015-01'
WORKFLOW = '.github/workflows/traceharbor-native27.yml'
BASE = '/repos/' + REPO
ORIGINALS, ERRORS = [], []  # Private originals, never printed or artifact-uploaded.
FIRST_UNKNOWN = None
DEADLINE = None
POSTS = {'/git/commits': 0, '/git/refs': 0}
VERIFIED_CONTEXT = None
PUBLIC_REF_RETURN = None
STAGE, LAST_STATUS = 'NOT_STARTED', None
EFFECT_STATE = 'NOT_ATTEMPTED'
HTTP_COUNTS = {'GET': 0, 'POST': 0}
LAST_WRITE = None


class Stop(Exception):
    pass


def require(ok, code):
    if not ok:
        error = Stop(code)
        ERRORS.append(('SEMANTIC_OR_SCHEMA', error))
        if LAST_WRITE is not None and EFFECT_STATE != 'KNOWN_REFUSAL':
            mark_unknown(code)
        raise error


def mark_unknown(stage):
    global FIRST_UNKNOWN, EFFECT_STATE
    if FIRST_UNKNOWN is None:
        FIRST_UNKNOWN = stage
    if LAST_WRITE is not None:
        EFFECT_STATE = 'UNKNOWN'


def guard(stage, terminal=False):
    global STAGE
    STAGE = stage
    if time.monotonic() >= DEADLINE:
        mark_unknown(stage)
        raise Stop('UNKNOWN_STOP_NO_RETRY')
    if FIRST_UNKNOWN is not None and not terminal:
        raise Stop('UNKNOWN_STOP_NO_RETRY')


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def request(method, suffix, payload=None, public=False):
    """Single native call, no redirects, retries, PATCH, PUT or DELETE."""
    global PUBLIC_REF_RETURN, LAST_STATUS, LAST_WRITE, EFFECT_STATE
    require(method in ('GET', 'POST'), 'METHOD_REFUSED')
    guard('PRE_REQUEST_LIMIT')
    limit = 10 if os.environ.get('Q27_PHASE') == 'first' else 11
    post_limit = 2 if os.environ.get('Q27_PHASE') == 'first' else 1
    require(HTTP_COUNTS['GET'] < limit if method == 'GET' else HTTP_COUNTS['POST'] < post_limit,
            'HTTP_BOUND_EXHAUSTED')
    if method == 'POST':
        require(os.environ.get('Q27_PHASE') == 'first' or suffix == '/git/refs', 'SECOND_COMMIT_REFUSED')
        require(suffix in POSTS and POSTS[suffix] == 0, 'POST_ALREADY_CONSUMED')
        POSTS[suffix] = 1  # Consume before any request; UNKNOWN never resets this.
        LAST_WRITE, EFFECT_STATE = suffix, 'ATTEMPT_CONSUMED'
    HTTP_COUNTS[method] += 1
    raw = None if payload is None else canonical(payload)
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'TraceHarbor-qualification27',
               'X-GitHub-Api-Version': '2026-03-10'}
    if not public:
        headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    if raw is not None:
        headers['Content-Type'] = 'application/json'
    connection = response = None
    try:
        guard('PRE_REQUEST')
        connection = http.client.HTTPSConnection('api.github.com', timeout=min(15, DEADLINE-time.monotonic()))
        ORIGINALS.append(('OWNED_CONNECTION', connection))  # Ownership before postguard.
        guard('POST_ACQUIRE')
        guard('PRE_INVOKE')
        connection.request(method, BASE+suffix, body=raw, headers=headers)
        response = connection.getresponse()
        ORIGINALS.append(('RESPONSE', response))
        guard('POST_RESPONSE')
        body = response.read(65537)
        ORIGINALS.append(('RETURNED_BYTES', body, response.status))  # Before clock/parse/I/O.
        LAST_STATUS = response.status
        guard('POST_RETURN')
        require(len(body) <= 65536, 'OVERSIZED_OBSERVED_PREFIX_ONLY')
        guard('PRE_PARSE')
        parsed = json.loads(body)
        guard('POST_PARSE')
        require(isinstance(parsed, dict), 'RESPONSE_SCHEMA_NOT_OBJECT')
        answer = (response.status, parsed, body)
    except Exception as error:
        ERRORS.append(('PRIMARY', error))  # Do not stringify private exceptions/tokens.
        mark_unknown(STAGE)
        raise Stop('UNKNOWN_STOP_NO_RETRY') from None
    finally:
        if connection is not None:
            owned, connection = connection, None  # Claim close before any fallible work.
            try:
                owned.close()  # One release attempt even after deadline, not backend stop.
                guard('POST_CLEANUP')
            except Exception as error:
                ERRORS.append(('CLEANUP', error))
                mark_unknown('CLEANUP_UNKNOWN')
    guard('POST_CLEANUP_BEFORE_USE')
    status, parsed, body = answer
    if method == 'POST':
        EFFECT_STATE = ('APPLIED_UNVERIFIED' if status == 201 else
                        'KNOWN_REFUSAL' if status in (400, 401, 403, 404, 409, 422) else 'UNKNOWN')
        if EFFECT_STATE == 'UNKNOWN':
            mark_unknown('AMBIGUOUS_POST_STATUS')
            raise Stop('UNKNOWN_STOP_NO_RETRY')
    if method == 'POST' and suffix == '/git/refs':
        # This endpoint's public ref request/response contains no credential.
        PUBLIC_REF_RETURN = {'status': status, 'body': parsed}
    return status, parsed, body


def get(suffix, public=False):
    status, obj, raw = request('GET', suffix, public=public)
    require(status == 200, 'GET_NOT_200')
    return obj


def run_identity(run_id, source, workflow_id=None):
    require(re.fullmatch(r'[1-9][0-9]*', run_id) is not None, 'RUN_ID_INVALID')
    r = get('/actions/runs/'+run_id, public=True)
    require(r['id'] == int(run_id) and r['run_attempt'] == 1 and
            r['repository']['id'] == RID and r['repository']['full_name'] == REPO and
            r['head_repository']['id'] == RID and r['event'] == 'workflow_dispatch' and
            r['head_branch'] == 'main' and r['head_sha'] == source and
            r['actor']['id'] == OWNER and r['triggering_actor']['id'] == OWNER and
            r['path'] == WORKFLOW, 'NATIVE_RUN_IDENTITY_MISMATCH')
    if workflow_id is not None:
        require(r['workflow_id'] == workflow_id, 'WORKFLOW_ID_MISMATCH')
    return r


def object_readback(commit, tree, message, source):
    obj = get('/git/commits/'+commit)
    require(obj['sha'] == commit and obj['tree']['sha'] == tree and
            [p['sha'] for p in obj['parents']] == [source] and obj['message'] == message,
            'COMMIT_BODY_MISMATCH')
    require(get('/git/trees/'+tree)['sha'] == tree, 'TREE_MISMATCH')
    return obj


def ref_readback(commit):
    obj = get('/git/ref/'+REF[5:])
    require(obj['ref'] == REF and obj['object']['type'] == 'commit' and
            obj['object']['sha'] == commit, 'REF_BODY_MISMATCH')
    return obj


def main():
    global DEADLINE, VERIFIED_CONTEXT, EFFECT_STATE
    DEADLINE = time.monotonic()+110
    # Future independent review must admit exact source, account usage/retention,
    # first/second once-only dispatch journals and native token permissions.
    # Inputs/context are bindings, NEVER authority or proof that a POST occurred.
    require(os.environ.get('Q27_ADMITTED') == 'REQUIRES_FUTURE_REVIEW', 'NO_NATIVE27_ADMISSION')
    require(os.environ.get('GITHUB_ACTIONS') == 'true' and os.environ.get('GITHUB_REPOSITORY') == REPO and
            os.environ.get('GITHUB_REPOSITORY_ID') == str(RID) and
            os.environ.get('GITHUB_RUN_ATTEMPT') == '1' and
            os.environ.get('GITHUB_EVENT_NAME') == 'workflow_dispatch' and
            os.environ.get('GITHUB_REF') == 'refs/heads/main', 'ENV_CONTEXT_REFUSED')
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_bytes())
    require(event['repository']['id'] == RID and not event['repository']['private'] and
            event['sender']['id'] == OWNER, 'EVENT_CONTEXT_REFUSED')
    source = os.environ['Q27_SOURCE']
    require(re.fullmatch('[0-9a-f]{40}', source) is not None and
            source == os.environ['GITHUB_SHA'] == os.environ['GITHUB_WORKFLOW_SHA'], 'SOURCE_UNBOUND')
    require(os.environ['GITHUB_WORKFLOW_REF'] == REPO+'/'+WORKFLOW+'@refs/heads/main', 'WORKFLOW_REF_REFUSED')
    require(sha(Path(WORKFLOW).read_bytes()) == os.environ['Q27_WORKFLOW_HASH'] and
            sha(Path(__file__).read_bytes()) == os.environ['Q27_DRIVER_HASH'], 'SOURCE_PIN_MISMATCH')
    phase, run_id = os.environ['Q27_PHASE'], os.environ['GITHUB_RUN_ID']
    require(phase in ('first', 'second'), 'PHASE_REFUSED')
    repo = get('')
    require(repo['id'] == RID and repo['owner']['id'] == OWNER and repo['owner']['type'] == 'User' and
            not repo['fork'] and not repo['private'], 'REPO_IDENTITY_DRIFT')
    require(get('/git/ref/heads/main')['object']['sha'] == source, 'MAIN_DRIFT')
    current = run_identity(run_id, source)
    VERIFIED_CONTEXT = {'repository_id': RID, 'source': source, 'run_id': run_id,
                        'workflow_id': current['workflow_id'], 'nonce': NONCE}
    tree = get('/git/commits/'+source)['tree']['sha']
    first_id = run_id if phase == 'first' else os.environ['Q27_FIRST_RUN']
    manifest = {'schema': 'PRIVATE_NATIVE_QUALIFICATION_ONLY', 'request_authority': None,
                'repository_id': RID, 'target': REF, 'nonce': NONCE, 'source': source,
                'workflow_sha256': os.environ['Q27_WORKFLOW_HASH'],
                'driver_sha256': os.environ['Q27_DRIVER_HASH'], 'first_run_id': first_id}
    message = canonical(manifest).decode()
    if phase == 'first':
        require(not os.environ.get('Q27_FIRST_RUN') and not os.environ.get('Q27_FIRST_COMMIT'), 'FIRST_INPUTS_REFUSED')
        status, absent, raw = request('GET', '/git/ref/'+REF[5:])
        require(status == 404 and absent.get('message') == 'Not Found', 'PREEXISTING_OR_UNQUALIFIED_REF')
        status, obj, raw = request('POST', '/git/commits', {'message': message, 'tree': tree, 'parents': [source]})
        require(status == 201, 'COMMIT_NOT_201_STOP')
        commit = obj['sha']
        object_readback(commit, tree, message, source)
    else:
        require(first_id != run_id, 'SAME_RUN_REFUSED')
        first = run_identity(first_id, source, current['workflow_id'])
        require(first['status'] == 'completed' and first['conclusion'] == 'success', 'FIRST_NOT_NATIVE_SUCCESS')
        start = datetime.datetime.fromisoformat(first['run_started_at'].replace('Z', '+00:00'))
        age = (datetime.datetime.now(datetime.timezone.utc)-start).total_seconds()
        require(0 <= age < 300, 'OVERALL_WINDOW_EXPIRED')
        DEADLINE = min(DEADLINE, time.monotonic()+300-age)
        commit = os.environ['Q27_FIRST_COMMIT']
        require(re.fullmatch('[0-9a-f]{40}', commit) is not None, 'FIRST_COMMIT_UNBOUND')
        # An independent Auditor must inspect actual first201/readbacks/logreceipt
        # before admitting dispatch2; native success alone is not a new grant.
        object_readback(commit, tree, message, source)
        ref_readback(commit)
    status, obj, raw = request('POST', '/git/refs', {'ref': REF, 'sha': commit})
    if phase == 'first':
        require(status == 201 and obj['ref'] == REF and obj['object']['sha'] == commit and
                obj['object']['type'] == 'commit', 'FIRST_NOT_EXACT_201_STOP')
    else:
        errors = obj.get('errors', [])
        exists = obj.get('message') == 'Reference already exists' or any(
            isinstance(e, dict) and e.get('resource') == 'Reference' and e.get('field') == 'ref' and
            e.get('code') == 'already_exists' for e in errors)
        require(status == 422 and exists, 'REFUSAL_NOT_EXPLICIT_ALREADY_EXISTS')
    ref_readback(commit)
    object_readback(commit, tree, message, source)
    EFFECT_STATE = 'APPLIED_VERIFIED' if phase == 'first' else 'KNOWN_ALREADY_EXISTS_VERIFIED'
    receipt = {**manifest, 'phase': phase, 'run_id': run_id, 'run_attempt': 1,
               'commit': commit, 'tree': tree, 'native_ref_status': status,
               'native_response': obj, 'scope': 'CREATE_REFUSAL_PRIMITIVE_ONLY', 'PLAN': None}
    guard('PRE_FINAL_EXPORT')
    output = canonical(receipt)
    require(len(output) <= 16384, 'PUBLIC_RECEIPT_TOO_LARGE')
    guard('PRE_LOG_WRITE')
    print(output.decode(), flush=True)
    guard('POST_FINAL_EXPORT')


def failure_terminal(error):
    """Sanitized failure only; never publish private body/hash/header/exception."""
    ERRORS.append(('TERMINAL', error))  # Original before clock/serialization/I/O.
    if LAST_WRITE is not None and EFFECT_STATE != 'KNOWN_REFUSAL':
        mark_unknown(STAGE)
    try:
        guard('PRE_TERMINAL_EXPORT', terminal=True)
        terminal = canonical({'scope': 'PRIVATE_NATIVE_QUALIFICATION_ONLY',
                              'state': 'STOP_NO_RETRY', 'context': VERIFIED_CONTEXT,
                              'first_unknown_stage': FIRST_UNKNOWN, 'effect_state': EFFECT_STATE,
                              'attempts': POSTS, 'http_counts': HTTP_COUNTS, 'http_status': LAST_STATUS})
        guard('PRE_TERMINAL_WRITE', terminal=True)
        print(terminal.decode(), flush=True)
        guard('POST_TERMINAL_EXPORT', terminal=True)
    except Exception as diagnostic_error:
        ERRORS.append(('TERMINAL_RETENTION', diagnostic_error))


def run_entry():
    try:
        main()
    except Exception as error:
        failure_terminal(error)
        raise SystemExit('NATIVE27_STOP_NO_RETRY_NO_NATIVE_PASS') from None


if __name__ == '__main__':
    run_entry()
