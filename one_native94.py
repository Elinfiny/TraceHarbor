"""Concrete dormant hosted ONE integration. No live admission is installed.

Trusted reviewed source is the boundary, not Python attributes or a sandbox.
The inert helper cannot register a native context or verify a provider JWT.
"""
from dataclasses import dataclass, field
from decimal import Decimal
import base64
import hashlib
import http.client
import importlib.metadata
import json
import math
import os
from pathlib import Path
import re
import ssl
import sys
import time
from nebius import HTTPBoundary, ProviderError, decode_response, MAX_RESPONSE
import one_backend91 as git

REPO = 'Elinfiny/TraceHarbor'
REPO_ID = 1391430317
OWNER_ID = 273768139
ISSUER = 'https://token.actions.githubusercontent.com'
WORKFLOW = '.github/workflows/traceharbor-one94.yml'
JOB = 'one94'
OPERATION = 'TRACEHARBOR_NATIVE_ONE94_V1'
NAMESPACE = 'refs/tags/traceharbor-native-one94-consumed/'
MESSAGE = 'TraceHarbor native ONE94 ATTEMPTING_CONSUMED'
API_VERSION = '2022-11-28'
DEPENDENCIES = {'PyJWT': '2.15.1', 'cryptography': '50.0.2', 'cffi': '2.1.1', 'pycparser': '3.11'}

# Each is a separately reviewed PROTECTED runtime input, not a JSON/env switch.
# No service, key, mount, signer, grant, dependency or permission is installed94.
REVIEWED_CONFIGURATION = None
PROTECTED_ADMISSION = None
PROTECTED_CAPTURE = None
QUALIFIED_DEPENDENCY_CLOSURE = None
_CURRENT = None
_ENTRY_ATTEMPTED = False


@dataclass(frozen=True)
class ReviewedConfiguration94:
    source: str
    workflow_sha: str
    audience: str
    subject: str
    oidc_hostname: str
    oidc_path: str
    oidc_api_version: str
    payload_path: str
    input_path: str
    ref: str = 'refs/heads/main'
    window_seconds: int = 300


class Window94:
    """Single shared monotonic window, original-before-guard, sticky primary."""
    def __init__(self, seconds, capture, *, clock=time.monotonic, wall=None):
        if type(seconds) is not int or not 1 <= seconds <= 300:
            raise ProviderError('WINDOW94')
        self.clock, self.capture = clock, capture
        self.started = clock()
        self.wall_anchor = time.time() if wall is None else wall
        self.deadline = self.started + seconds
        self.primary, self.secondary = None, []
        self.originals = []

    def fail(self, code):
        if self.primary is None: self.primary = code
        else: self.secondary.append(('CODE', code))

    def retain(self, stage, kind, value):
        self.originals.append((stage, kind, value))
        try:
            if self.capture is None: raise ProviderError('PROTECTED_CAPTURE_UNBOUND94')
            self.capture.retain(stage, kind, value)
            return True
        except Exception as error:
            self.originals.append((stage, 'CAPTURE_EXCEPTION', error))
            self.secondary.append((stage, error))
            return False

    def check(self, stage):
        if self.primary: raise ProviderError(self.primary)
        try:
            now = self.clock()
            if type(now) not in (int, float) or not math.isfinite(now) or now >= self.deadline:
                raise TimeoutError('ABSOLUTE_WINDOW94')
        except Exception as original:
            self.retain(stage, 'EXCEPTION', original)
            self.fail('ABSOLUTE_WINDOW_UNKNOWN94')
            raise ProviderError(self.primary) from None
        return min(30.0, self.deadline-now)

    def wall_now(self):
        self.check('WALL_ANCHOR94')
        return self.wall_anchor + self.clock()-self.started

    def invoke(self, stage, call, kind='OBJECT'):
        self.check('PRE_INVOKE_'+stage)
        try: value = call()
        except Exception as original:
            if isinstance(original, http.client.IncompleteRead):
                self.retain(stage, 'PARTIAL', original.partial[:MAX_RESPONSE+1])
            self.retain(stage, 'EXCEPTION', original)
            self.fail('CALL_UNKNOWN94_'+stage)
            raise ProviderError(self.primary) from None
        if not self.retain(stage, kind, value):
            self.fail('PRIVATE_CAPTURE_UNKNOWN94')
            raise ProviderError(self.primary) from None
        self.check('POST_RETURN_'+stage)
        return value


class ProtectedCapture94:
    """Concrete bounded writer to an AUTHENTIC installed private durable sink.

    The sink must expose put_once(sequence, bytes, absolute_deadline) and
    readback(receipt, absolute_deadline), with immutable same-channel receipts.
    PROTECTED_CAPTURE authenticates the channel, not a returned Boolean alone.
    No filesystem/memory/artifact fallback exists on the native route.
    """
    scope = 'NATIVE_PROTECTED94'
    def __init__(self, channel, window):
        self.channel, self.window = channel, window
        self.originals, self.count, self.total = [], 0, 0

    def retain(self, stage, kind, original):
        self.originals.append((stage, kind, original))
        if isinstance(original, bytes): value = {'base64':base64.b64encode(original).decode()}
        elif isinstance(original, BaseException): value = {'exception_type':type(original).__name__}
        elif type(original) is git.Reply:
            value = {'status':original.status,'media':original.media_type,'eof':original.eof,
                     'body':base64.b64encode(original.body).decode()}
        else:
            # Object identity is retained in memory; no repr of tokens/clients.
            value = {'object_type':type(original).__name__}
        raw = git.canonical({'stage':stage,'kind':kind,'value':value})
        if len(raw)>524288 or self.count>=256 or self.total+len(raw)>8388608:
            raise ProviderError('CAPTURE_BOUND94')
        if self.window.clock()>=self.window.deadline:
            raise ProviderError('CAPTURE_WINDOW94')
        receipt = self.channel.put_once(self.count, raw, self.window.deadline)
        readback = self.channel.readback(receipt, self.window.deadline)
        if readback != raw or self.window.clock()>=self.window.deadline:
            raise ProviderError('PRIVATE_DURABLE_CAPTURE_UNKNOWN94')
        self.count += 1; self.total += len(raw)


def validate_configuration94(cfg):
    if (type(cfg) is not ReviewedConfiguration94 or not git.hexid(cfg.source,40)
            or cfg.workflow_sha != cfg.source or cfg.ref!='refs/heads/main'
            or type(cfg.audience) is not str or not 1<=len(cfg.audience)<=512
            or type(cfg.subject) is not str or not 1<=len(cfg.subject)<=512
            or type(cfg.window_seconds) is not int or not 1<=cfg.window_seconds<=300
            or not Path(cfg.payload_path).is_absolute() or not Path(cfg.input_path).is_absolute()):
        raise ProviderError('REVIEWED_CONFIGURATION94')


def validate_claims94(claims, cfg, wall):
    """Pure claim equality/time checks. Data returned here is NOT authority."""
    expected={'iss':ISSUER,'aud':cfg.audience,'sub':cfg.subject,'repository':REPO,
              'repository_id':str(REPO_ID),'repository_owner_id':str(OWNER_ID),
              'actor_id':str(OWNER_ID),'event_name':'workflow_dispatch','ref':cfg.ref,
              'sha':cfg.source,'workflow_sha':cfg.workflow_sha,
              'workflow_ref':REPO+'/'+WORKFLOW+'@'+cfg.ref,'run_attempt':'1',
              'runner_environment':'github-hosted'}
    if type(claims) is not dict or any(claims.get(k)!=v for k,v in expected.items()):
        raise ProviderError('SIGNED_CONTEXT_MISMATCH94')
    # Ordinary workflow claims above are mandatory. Reusable job_workflow_*
    # claims are deliberately NOT fabricated or required for this ordinary job.
    for key in ('run_id','check_run_id'):
        value=claims.get(key)
        if type(value) not in (str,int) or not str(value).isascii() or not str(value).isdigit() or int(value)<=0:
            raise ProviderError('RUN_JOB_CLAIM94')
    if any(type(claims.get(k)) is not int for k in ('iat','nbf','exp')):
        raise ProviderError('JWT_TIME_TYPES94')
    if not (claims['nbf']<=wall<claims['exp'] and claims['iat']<=wall
            and wall-claims['iat']<=60 and 0<claims['exp']-claims['iat']<=600):
        raise ProviderError('JWT_FRESHNESS94')
    if type(claims.get('jti')) is not str or not 1<=len(claims['jti'])<=256:
        raise ProviderError('JWT_ID94')
    return {'run_id':int(claims['run_id']),'check_run_id':int(claims['check_run_id'])}


def validate_job94(run, jobs, claims, cfg):
    identity=validate_claims94(claims,cfg,float(claims['iat']))
    if (run.get('id')!=identity['run_id'] or run.get('run_attempt')!=1
            or run.get('head_sha')!=cfg.source or run.get('event')!='workflow_dispatch'
            or run.get('path')!=WORKFLOW or run.get('actor',{}).get('id')!=OWNER_ID
            or run.get('repository',{}).get('id')!=REPO_ID):
        raise ProviderError('RUN_MEMBERSHIP94')
    if type(jobs) is not dict or jobs.get('total_count')!=1 or len(jobs.get('jobs',[]))!=1:
        raise ProviderError('ONE_JOB_NO_PAGINATION94')
    job=jobs['jobs'][0]
    if (job.get('run_id')!=identity['run_id'] or job.get('head_sha')!=cfg.source
            or job.get('name')!=JOB or job.get('status')!='in_progress'
            or job.get('check_run_url')!='https://api.github.com/repos/'+REPO+'/check-runs/'+str(identity['check_run_id'])
            or 'ubuntu-24.04' not in job.get('labels',[])):
        raise ProviderError('SIGNED_CHECK_RUN_JOB_MEMBERSHIP94')
    return identity


def _secret(name):
    value=os.environ[name]
    if type(value) is not str or not 1<=len(value)<=8192 or any(ord(c)<33 or ord(c)>126 for c in value):
        raise ProviderError('PRIVATE_CREDENTIAL_FORMAT94')
    return value


def _https(window, host, method, path, body, headers, limit):
    """Fixed-host caller; validated TLS, bounded EOF, no redirects/retry."""
    connection=response=None
    try:
        def construct():
            nonlocal connection
            connection=http.client.HTTPSConnection(host,timeout=window.check('PRE_TLS94'),context=ssl.create_default_context())
            return connection
        window.invoke('TLS_CONSTRUCT',construct)
        def timeout():
            remaining=window.check('PRE_SOCKET_TIMEOUT94')
            connection.timeout=remaining
            if connection.sock is not None:connection.sock.settimeout(remaining)
        window.invoke('SOCKET_TIMEOUT',timeout)
        window.invoke('HTTP_REQUEST',lambda:connection.request(method,path,body,headers))
        window.invoke('SOCKET_TIMEOUT',timeout)
        def receive():
            nonlocal response
            response=connection.getresponse()
            return response
        window.invoke('HTTP_RESPONSE',receive)
        status=window.invoke('HTTP_STATUS',lambda:response.status)
        media=window.invoke('HTTP_MEDIA',lambda:response.getheader('Content-Type'))
        window.invoke('SOCKET_TIMEOUT',timeout)
        raw=window.invoke('HTTP_BODY',lambda:response.read(limit+1),'BYTES')
        if (type(raw) is not bytes or len(raw)>limit or type(status) is not int
                or not 100<=status<=599 or 300<=status<400 or type(media) is not str
                or len(media)>256 or media.split(';')[0].strip() not in ('application/json',git.JSON_MEDIA)):
            window.fail('HTTP_BOUND_MEDIA_OR_REDIRECT94')
            raise ProviderError('HTTP_BOUND_OR_REDIRECT94')
        # read(limit+1) at <=limit returns complete response EOF under http.client.
        window.check('HTTP_EOF94')
    finally:
        for stage,resource in (('RESPONSE_CLOSE',response),('CONNECTION_CLOSE',connection)):
            if resource is None:continue
            try:resource.close()
            except Exception as original:
                window.retain(stage,'EXCEPTION',original);window.fail('CLEANUP_UNKNOWN94')
            if window.clock()>=window.deadline:window.fail('CLEANUP_LATE94')
    window.check('POST_HTTP_CLEANUP94')
    return status,raw


class GitClient94:
    def __init__(self, window, token_supplier):
        self.window,self._token=window,token_supplier
    def request(self, method, path, body):
        allowed_get=(path=='' or re.fullmatch(r'/actions/runs/[1-9][0-9]*',path)
            or re.fullmatch(r'/actions/runs/[1-9][0-9]*/attempts/1/jobs\?per_page=100',path)
            or re.fullmatch(r'/git/(?:commits|trees|blobs)/[a-f0-9]{40}',path)
            or re.fullmatch(r'/git/ref/tags/traceharbor-native-one94-consumed/[a-f0-9]{64}',path))
        allowed_post=path in ('/git/blobs','/git/trees','/git/commits','/git/refs')
        if not ((method=='GET' and allowed_get) or (method=='POST' and allowed_post)):
            raise ProviderError('EXACT_GIT_ENDPOINT94')
        if method=='POST' and path=='/git/refs' and (type(body) is not dict
                or not re.fullmatch(re.escape(NAMESPACE)+r'[a-f0-9]{64}',body.get('ref',''))):
            raise ProviderError('NATIVE_NAMESPACE94')
        token=self._token()  # Never retained/serialized. Called only after signature checks.
        data=None if body is None else git.canonical(body)
        status,raw=_https(self.window,'api.github.com',method,'/repos/'+REPO+path,data,
            {'Accept':git.JSON_MEDIA,'X-GitHub-Api-Version':API_VERSION,
             'Authorization':'Bearer '+token,'Content-Type':'application/json'},git.MAX_WIRE)
        token=None
        return git.Reply(status,raw,git.JSON_MEDIA,True)


def _oidc94(cfg, window):
    QUALIFIED_DEPENDENCY_CLOSURE.assert_verified_installed(DEPENDENCIES)
    if any(importlib.metadata.version(name)!=version for name,version in DEPENDENCIES.items()):
        raise ProviderError('PINNED_VERIFIER_CLOSURE94')
    # Reuse67's pure exact origin/query policy; its readonly admission/acquire
    # entry is NOT called, relaxed or given a contents-write job identity.
    qualification=str(Path(__file__).resolve().parent/'qualification')
    if qualification not in sys.path:sys.path.insert(0,qualification)
    from native27_oidc67 import RequestPolicy67,request_target67
    policy=RequestPolicy67(cfg.oidc_hostname,cfg.oidc_path,cfg.oidc_api_version,cfg.audience)
    host,path=request_target67(os.environ['ACTIONS_ID_TOKEN_REQUEST_URL'],policy)
    bearer=_secret('ACTIONS_ID_TOKEN_REQUEST_TOKEN')
    status,raw=_https(window,host,'GET',path,None,{'Accept':'application/json','Authorization':'Bearer '+bearer},16384)
    bearer=None
    if status!=200:raise ProviderError('OIDC_ACQUISITION_HTTP94')
    value=window.invoke('PARSE_OIDC_ACQUISITION',lambda:git.strict_json(raw))
    token=value.get('value')
    if type(token) is not str or not 1<=len(token)<=16384 or token.count('.')!=2:
        raise ProviderError('OIDC_TOKEN_SHAPE94')
    # Same selected signature library/API/issuer and JOSE checks as verifier65.
    # Separate94 audience input avoids assigning readonly65/67 module globals.
    import jwt
    status,jwks_raw=_https(window,'token.actions.githubusercontent.com','GET','/.well-known/jwks',None,{'Accept':'application/json'},65536)
    if status!=200:raise ProviderError('JWKS_HTTP94')
    jwks=window.invoke('PARSE_JWKS',lambda:git.strict_json(jwks_raw))
    header=window.invoke('JOSE_HEADER',lambda:jwt.get_unverified_header(token))
    if (header.get('alg')!='RS256' or type(header.get('kid')) is not str or not 1<=len(header['kid'])<=256
            or any(k in header for k in ('jku','x5u','crit')) or type(jwks.get('keys')) is not list or not 1<=len(jwks['keys'])<=16):
        raise ProviderError('OIDC_JOSE_JWKS94')
    keys=[k for k in jwks['keys'] if k.get('kid')==header['kid'] and k.get('kty')=='RSA'
          and k.get('use','sig')=='sig' and k.get('alg','RS256')=='RS256']
    if len(keys)!=1:raise ProviderError('OIDC_SIGNING_KEY94')
    key=window.invoke('JWT_KEY',lambda:jwt.PyJWK.from_dict(keys[0],algorithm='RS256'))
    claims=window.invoke('PROVIDER_SIGNATURE',lambda:jwt.decode(token,key,algorithms=['RS256'],
        issuer=ISSUER,audience=cfg.audience,leeway=0,options={'strict_aud':True,
        'require':['iss','aud','sub','exp','iat','nbf','jti','repository','repository_id',
                   'repository_owner_id','sha','workflow_sha','workflow_ref','run_id','run_attempt',
                   'actor_id','event_name','ref','runner_environment','check_run_id']}))
    window.invoke('SIGNED_ORDINARY_CLAIMS',lambda:validate_claims94(claims,cfg,window.wall_now()))
    return claims


@dataclass(frozen=True)
class NativePlan94:
    source_commit: str
    invocation: str
    nonce: str
    deadline_utc: int


@dataclass
class _Context94:
    configuration: object
    window: object
    git_client: object
    capture: object
    grant: object = field(repr=False)
    claims: dict = field(repr=False)
    plan: object
    phase: str = 'READY'
    backend: object = None


def record_data94(plan, grant_receipt, *, classification, started_utc):
    """Pure record bytes. A record or classification string is never authority."""
    from one_request import MODEL,PAYLOAD_SHA256,INPUT_SHA256,EVIDENCE_SHA256
    return {'schema':'TRACEHARBOR_NATIVE_ONE_RECORD94_V1','operation':OPERATION,
        'repository':REPO,'repository_id':REPO_ID,'classification':classification,
        'source_commit':plan.source_commit,'invocation':plan.invocation,'attempt':1,
        'nonce':plan.nonce,'project':git.PROJECT,'model':MODEL,'payload_sha256':PAYLOAD_SHA256,
        'input_sha256':INPUT_SHA256,'evidence_sha256':EVIDENCE_SHA256,
        'actual_numeric_grant':grant_receipt,'started_utc':started_utc,'deadline_utc':plan.deadline_utc,
        'state':'ATTEMPTING_CONSUMED','refund_or_resume':False}


class _NativeGitCore94(git._GitRecordCore):
    def _fail(self, code):
        self.window.fail(code)
        super()._fail(self.window.primary)


def validate_context94(context):
    if (type(context) is not _Context94 or context is not _CURRENT
            or context.phase not in ('READY','EXECUTING') or context.window.clock is not time.monotonic):
        raise ProviderError('NO_REGISTERED_VERIFIED_NATIVE_INVOCATION94')
    context.window.check('NATIVE_CONTEXT94')
    PROTECTED_ADMISSION.assert_current(context.grant,context.claims,context.configuration,context.window.deadline)
    PROTECTED_CAPTURE.assert_authenticated(context.capture.channel,context.configuration,context.window.deadline)
    return context


def peek_context94():
    return _CURRENT if _CURRENT is not None and _CURRENT.phase in ('READY','EXECUTING') else None


def load_context94():
    global _CURRENT,_ENTRY_ATTEMPTED
    if any(x is None for x in (REVIEWED_CONFIGURATION,PROTECTED_ADMISSION,PROTECTED_CAPTURE,QUALIFIED_DEPENDENCY_CLOSURE)):
        return None  # BEFORE env, file, dependency, credential, OIDC or network lookup.
    if _CURRENT is not None:return validate_context94(_CURRENT)
    if _ENTRY_ATTEMPTED:raise ProviderError('NATIVE_ENTRY_CONSUMED_UNKNOWN94')
    _ENTRY_ATTEMPTED=True
    cfg=REVIEWED_CONFIGURATION;validate_configuration94(cfg)
    window=Window94(cfg.window_seconds,None)
    channel=PROTECTED_CAPTURE.open_authenticated(cfg,window.deadline)
    PROTECTED_CAPTURE.assert_authenticated(channel,cfg,window.deadline)
    capture=ProtectedCapture94(channel,window);window.capture=capture
    claims=window.invoke('OIDC_ACQUIRE_VERIFY',lambda:_oidc94(cfg,window))
    client=GitClient94(window,lambda:_secret('GITHUB_TOKEN'))
    run_id=int(claims['run_id'])
    run=window.invoke('RUN_ORIGINAL',lambda:client.request('GET','/actions/runs/'+str(run_id),None))
    jobs=window.invoke('JOBS_ORIGINAL',lambda:client.request('GET','/actions/runs/'+str(run_id)+'/attempts/1/jobs?per_page=100',None))
    if run.status!=200 or jobs.status!=200:raise ProviderError('JOB_METADATA_HTTP94')
    window.invoke('ACTUAL_JOB_MEMBERSHIP',lambda:validate_job94(git.strict_json(run.body),git.strict_json(jobs.body),claims,cfg))
    # Authenticated external capability remains genuinely uninstalled. No JSON
    # receipt, source hash, environment flag or callback shape substitutes for it.
    grant=PROTECTED_ADMISSION.open_verified_grant(cfg,claims,window.deadline)
    PROTECTED_ADMISSION.assert_current(grant,claims,cfg,window.deadline)
    public=PROTECTED_ADMISSION.public_receipt(grant)
    if (type(public) is not dict or set(public)!={'grant_sha256','usd','nonce','deadline_utc','entire_exposure_enforced'}
            or not git.hexid(public['grant_sha256']) or not git.hexid(public['nonce'])
            or type(public['usd']) is not str or not Decimal(public['usd']).is_finite()
            or Decimal(public['usd'])<=0 or public['entire_exposure_enforced'] is not True
            or type(public['deadline_utc']) is not int or public['deadline_utc']<window.wall_now()
            or public['deadline_utc']>int(window.wall_anchor+cfg.window_seconds)):
        raise ProviderError('VERIFIED_FINITE_GRANT_WINDOW94')
    # Tighten the original window; never start or reset a stage deadline.
    window.deadline=min(window.deadline,window.started+public['deadline_utc']-window.wall_anchor)
    window.check('ACTUAL_GRANT_WINDOW94')
    plan=NativePlan94(cfg.source,str(run_id),public['nonce'],public['deadline_utc'])
    _CURRENT=_Context94(cfg,window,client,capture,grant,claims,plan)
    return validate_context94(_CURRENT)


def backend_from_context94(context):
    c=validate_context94(context)
    if c.backend is None:
        receipt=PROTECTED_ADMISSION.public_receipt(c.grant)
        record=record_data94(c.plan,receipt,classification='NATIVE_VERIFIED_RUNTIME94',started_utc=c.window.wall_anchor)
        core=_NativeGitCore94(c.plan,record,c.git_client,c.capture,c.window.wall_now,
                             namespace=NAMESPACE,message=MESSAGE,local_marker=False)
        core.window=c.window;c.backend=core
    return c.backend


class _SharedHTTP94(HTTPBoundary):
    """Reuse unchanged nebius exchange/invoke/cleanup, distinct window/capture."""
    def __init__(self,window,capture,factory):
        self.window=window;self.deadline=window.deadline;self.clock=window.clock
        self.vault=capture;self.factory=factory;self.request_attempted=False
    @property
    def first_primary(self):return self.window.primary
    @property
    def secondary(self):return self.window.secondary
    def fail(self,code):self.window.fail(code)
    def check(self,stage):return self.window.check(stage)
    def capture(self,stage,kind,value,primary_on_failure=None):
        if not self.window.retain(stage,kind,value):
            self.window.fail(primary_on_failure or 'PRIVATE_CAPTURE_UNKNOWN94')
            raise ProviderError(self.window.primary)
    def invoke(self,stage,call,kind='OBJECT'):return self.window.invoke(stage,call,kind)


class NativeHTTP94(_SharedHTTP94):
    def __init__(self,context):
        c=validate_context94(context)
        def factory(host,timeout):
            if host!='api.tokenfactory.nebius.com':raise ProviderError('MODEL_ORIGIN94')
            return http.client.HTTPSConnection(host,timeout=timeout,context=ssl.create_default_context())
        super().__init__(c.window,c.capture,factory)


def _pipeline94(raw,input_raw,window,backend,boundary,key_supplier,classification):
    from one_request import validate_frozen_payload,bound_evidence,MODEL,PAYLOAD_SHA256
    from live_service import verified_analysis,build_record,verify_record
    value=window.invoke('EXACT_FROZEN_REQUEST',lambda:validate_frozen_payload(raw))
    evidence=window.invoke('FULL_BOUND_EVIDENCE',lambda:bound_evidence(input_raw,value))
    receipt=window.invoke('ATOMIC_CONSUME',backend.reserve)
    window.invoke('SAME_INVOCATION_RECEIPT',lambda:backend.verify(receipt))
    window.check('PRE_INVOKE_CREDENTIAL94')
    try:key=key_supplier()  # Presence only, never capture/serialize key itself.
    except Exception as original:
        window.retain('MODEL_CREDENTIAL','EXCEPTION',original)
        window.fail('CREDENTIAL_UNKNOWN94')
        raise ProviderError(window.primary) from None
    if not window.retain('MODEL_CREDENTIAL','PRESENCE_ONLY',bool(key)):
        window.fail('PRIVATE_CAPTURE_UNKNOWN94')
    window.check('POST_CREDENTIAL94')
    answer=boundary.exchange(raw,key,git.PROJECT);key=None
    analysis,metadata=window.invoke('MODEL_DECODE',lambda:decode_response(answer,MODEL))
    window.invoke('FULL_EVIDENCE_VERIFY',lambda:verified_analysis(analysis,evidence))
    metadata['request_sha256']=PAYLOAD_SHA256
    dossier=window.invoke('BUILD_DOSSIER',lambda:build_record(input_raw,analysis,metadata))
    window.invoke('VERIFY_DOSSIER',lambda:verify_record(dossier))
    window.check('POST_FINAL94')
    return {'classification':classification,'request_sha256':PAYLOAD_SHA256,
            'consumed':True,'verified':True,'native_model_attestation':False}


def execute_native94(context,raw,input_raw):
    c=validate_context94(context)
    if c.phase!='READY':raise ProviderError('ONE_EXECUTION_ONLY94')
    c.phase='EXECUTING'
    try:
        from one_backend91 import OneBackend
        backend=OneBackend();boundary=NativeHTTP94(c)
        def model_key():
            validate_context94(c)
            PROTECTED_ADMISSION.enforce_entire_exposure_before_post(c.grant,c.plan,c.window.deadline)
            return _secret('NEBIUS_API_KEY')
        return _pipeline94(raw,input_raw,c.window,backend,boundary,model_key,'NATIVE_RUNTIME94')
    finally:c.phase='TERMINAL_CONSUMED'


def inert_pipeline94(raw,input_raw,window,fake_git,capture,factory,spec):
    """Explicit SINTETIC data path. Cannot mint/register a native context."""
    plan=NativePlan94(spec['source'],spec['invocation'],spec['nonce'],spec['deadline_utc'])
    record=record_data94(plan,None,classification='INERT_TESTDATA_NOT_NATIVE_AUTHORITY94',started_utc=window.wall_anchor)
    backend=git._GitRecordCore(plan,record,fake_git,capture,window.wall_now,
                              namespace=NAMESPACE,message=MESSAGE,local_marker=False)
    boundary=_SharedHTTP94(window,capture,factory)
    return _pipeline94(raw,input_raw,window,backend,boundary,lambda:'SYNTHETIC-KEY94',
                       'INERT_TESTDATA_NOT_NATIVE_AUTHORITY94')


def main():
    try:
        from one_request import OneRequest
        consumer=OneRequest();c=validate_context94(consumer._context94)
        raw=c.window.invoke('LOAD_FROZEN_PAYLOAD',lambda:Path(c.configuration.payload_path).read_bytes(),'BYTES')
        source=c.window.invoke('LOAD_COMPLETE_INPUT',lambda:Path(c.configuration.input_path).read_bytes(),'BYTES')
        consumer.execute(raw,source)
        print('TRACEHARBOR_NATIVE94_COMPLETED_SOURCE_SCOPED_RECEIPT')
        return 0
    except Exception:
        print('TRACEHARBOR_NATIVE94_INACTIVE_OR_CONSUMED_UNKNOWN')
        return 2


if __name__=='__main__':raise SystemExit(main())
