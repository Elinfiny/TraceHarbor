"""PRIVATE67 same-process original OIDC acquisition, no installed admission.

Mechanism: GitHub documented ACTIONS_ID_TOKEN_REQUEST_URL / REQUEST_TOKEN and
custom audience. The URL is DATA. Only reviewed exact origin policy can release
its request bearer; JWT signature + original public context remain mandatory.
No stdin, copied cryptography, SDK/action/broker, redirects, retries or dispatch.
"""
from dataclasses import dataclass,field
import re
import time
from urllib.parse import urlsplit,parse_qsl,urlencode
import native27_transport60 as t
import native27_readback59 as a
import native27_validator42 as v

_REVIEWED_REQUEST67 = None

@dataclass(frozen=True)
class RequestPolicy67:
    hostname: str
    path: str
    api_version: str
    audience: str

@dataclass(frozen=True)
class SyntheticBoundary67:
    """Explicit fixture identity, never provider-signed or registered as native."""
    token: str = field(repr=False)
    claims: dict = field(repr=False)
    expected: object
    step: object
    provider: object = field(repr=False)
    acquisition_connection: object = field(repr=False)
    redirect_policy: object = field(repr=False)


def request_target67(locator,policy):
    v.need(type(policy) is RequestPolicy67,'OIDC_POLICY67')
    # Domain restriction is project policy derived from selected issuer's
    # provider namespace, not a claim that docs authorize arbitrary subdomains.
    # Exact actual host/path must ALSO be independently reviewed before native.
    h=policy.hostname
    v.need(type(h) is str and len(h)<=253 and h==h.lower() and
      re.fullmatch(r'[a-z0-9]+(?:[a-z0-9.-]*[a-z0-9])?',h) and
      h.endswith('.actions.githubusercontent.com'),'OIDC_PROVIDER_HOST67')
    v.need(type(locator) is str and 0<len(locator)<=4096 and
      all(33<=ord(c)<=126 for c in locator),'OIDC_LOCATOR67')
    u=urlsplit(locator)
    v.need(u.scheme=='https' and u.hostname==h and u.netloc in (h,h+':443') and
      u.port in (None,443) and u.username is None and u.password is None and
      u.fragment=='','OIDC_ORIGIN67')
    v.need(type(policy.path) is str and u.path==policy.path and u.path.startswith('/') and
      not any(x in u.path for x in ('%','\\','//')) and
      all(x not in ('.','..') for x in u.path.split('/')),'OIDC_PATH67')
    v.need(type(policy.api_version) is str and 0<len(policy.api_version)<=64 and
      re.fullmatch(r'[A-Za-z0-9._-]+',policy.api_version) and
      type(policy.audience) is str and 0<len(policy.audience)<=512 and
      not any(ord(c)<33 or ord(c)>126 for c in policy.audience),'OIDC_AUDIENCE67')
    pairs=parse_qsl(u.query,keep_blank_values=True,strict_parsing=True,max_num_fields=3)
    v.need(len({k for k,value in pairs})==len(pairs) and
      set(k for k,value in pairs)<= {'api-version','audience'} and
      dict(pairs).get('api-version')==policy.api_version and
      ('audience' not in dict(pairs) or dict(pairs)['audience']==policy.audience),'OIDC_QUERY67')
    # Audience encoded once; no raw string concatenation or attacker auth URL.
    return h,u.path+'?'+urlencode([('api-version',policy.api_version),('audience',policy.audience)])


def _step67(step,expected):
    v.need(type(step) is t.ReviewedStep66 and type(expected) is t.ExpectedHost65 and
      step.workflow_sha256==expected.workflow_sha256 and
      step.job_name==expected.job_name=='readback65' and
      step.step_id=='traceharbor_readback66' and
      step.credential_variable=='TRACEHARBOR_READONLY_JOB_TOKEN' and
      (step.contents,step.actions,step.id_token)==('read','read','write'),'READONLY_STEP67')


# Private invocation binding only; this is NOT a vendor/native attestation.
_ENTRY_KEY68 = object()

class _NativeInvocation68:
    __slots__=('key','expected','step','policy','target','bindings','snapshot','state','clock','budget','permit')
    def __init__(self,key,expected,step,policy,target,bindings,state,clock,budget):
        v.need(key is _ENTRY_KEY68,'CONTEXT_CONSTRUCTION68')
        self.key=key;self.expected=expected;self.step=step;self.policy=policy
        self.target=target;self.bindings=bindings;self.state=state;self.clock=clock;self.budget=budget
        self.snapshot=_snapshot68(expected,step,policy,bindings)
        self.permit=None


def _snapshot68(expected,step,policy,bindings):
    # Public source binding only, never token/JWKS or a source of authority.
    return v.canonical({'expected':vars(expected),'step':vars(step),
                        'policy':vars(policy),'bindings':bindings})


def _native_preflight68(*,policy=None,target=None,bindings=None,state=None,clock=None,
                         budget=None,context68=None,require_context=False):
    """Single pure preflight used by EVERY native OIDC entry before effects.

    Exact installed root objects, reviewed source and readonly step authorize
    the bounded route. Caller data/context/hash alone never installs admission.
    This invocation retains no identity/token/JWKS in a process-global registry.
    """
    e=t._REVIEWED_EXPECTED65;s=t._REVIEWED_STEP66;p=_REVIEWED_REQUEST67
    if any(x is None for x in (e,s,p,t._REVIEWED_TARGET65,t._REVIEWED_BINDINGS65,
      t.NATIVE_HOST_ROUTE,t.EXTERNAL_ADMISSION_GATE,t.nativeAdmission,t.PLAN)):
        raise v.Refuse('INACTIVE68_NATIVE_ENTRY_UNBOUND')
    if require_context:v.need(context68 is not None,'NATIVE_CONNECTION_ENTRY68')
    if context68 is not None:
        v.need(type(context68) is _NativeInvocation68 and context68.key is _ENTRY_KEY68,'NATIVE_CONTEXT68')
        if state is None:state=context68.state
        if clock is None:clock=context68.clock
        if budget is None:budget=context68.budget
    if policy is None:policy=p
    if target is None:target=t._REVIEWED_TARGET65
    if bindings is None:bindings=t._REVIEWED_BINDINGS65
    rejected=[]
    if not(type(e) is t.ExpectedHost65 and t.NATIVE_HOST_ROUTE is e and
           t.EXTERNAL_ADMISSION_GATE is e and t.nativeAdmission is e):rejected.append('INSTALLED_IDENTITY')
    if not(type(p) is RequestPolicy67 and policy is p):rejected.append('POLICY_IDENTITY')
    if not(type(target) is a.Target and target is t._REVIEWED_TARGET65 and
           type(bindings) is dict and bindings is t._REVIEWED_BINDINGS65):rejected.append('TARGET_BINDING_IDENTITY')
    try:_step67(s,e)
    except Exception:rejected.append('READONLY_STEP_SOURCE')
    try:
        a.preflight(target,bindings)
        v.need(bindings['source']==e.source and bindings['workflow_sha256']==e.workflow_sha256,'REVIEWED_SOURCE68')
    except Exception:rejected.append('REVIEWED_TARGET_SOURCE')
    try:
        v.need(type(p) is RequestPolicy67 and p.audience==e.audience,'POLICY_AUDIENCE68')
        request_target67('https://'+p.hostname+p.path+'?api-version='+p.api_version,p)
    except Exception:rejected.append('INSTALLED_POLICY_SCHEMA')
    if rejected:
        if type(state) is a.PrivateState:state.originals.append(('NATIVE_PREFLIGHT_REJECTIONS68',tuple(rejected)))
        raise v.Refuse('NATIVE_BINDING68')
    clock=time.monotonic if clock is None else clock
    # An arbitrary caller callback cannot manufacture native time or be called
    # before ownership/admission has been checked.
    v.need(clock is time.monotonic,'NATIVE_CLOCK68')
    state=a.PrivateState() if state is None else state
    v.need(type(state) is a.PrivateState,'NATIVE_STATE68')
    v.need(state.validator.first_unknown is None,'PREVIOUS_UNKNOWN')
    if budget is None:
        started=clock();budget=t._Budget66(started,started+300)
    v.need(type(budget) is t._Budget66 and type(budget.started) in (int,float) and
      type(budget.deadline) in (int,float) and a.math.isfinite(budget.started) and
      a.math.isfinite(budget.deadline) and budget.deadline==budget.started+300 and
      0<budget.deadline-clock()<=300,'NATIVE_BUDGET68')
    if context68 is None:return _NativeInvocation68(_ENTRY_KEY68,e,s,p,target,bindings,state,clock,budget)
    c=context68
    v.need(c.expected is e and c.step is s and c.policy is p and c.target is target and
      c.bindings is bindings and c.state is state and c.clock is clock and c.budget is budget and
      c.snapshot==_snapshot68(e,s,p,bindings),'NATIVE_CONTEXT_DRIFT68')
    return c


class _JSONConnection67:
    """Reuse existing bounded HTTP/TLS/cleanup, with OIDC's JSON media type."""
    def __init__(self,connection):self._connection=connection
    @property
    def sock(self):return self._connection.sock
    @property
    def timeout(self):return self._connection.timeout
    @timeout.setter
    def timeout(self,value):self._connection.timeout=value
    def connect(self):return self._connection.connect()
    def putrequest(self,*args,**kwargs):return self._connection.putrequest(*args,**kwargs)
    def putheader(self,key,value):
        if key=='X-GitHub-Api-Version':return
        return self._connection.putheader(key,'application/json' if key=='Accept' else value)
    def endheaders(self):return self._connection.endheaders()
    def getresponse(self):return self._connection.getresponse()
    def close(self):return self._connection.close()


def _native_connection67(host,timeout,capture,clock,deadline,*,context68=None,permit68=None):
    c=_native_preflight68(clock=clock,context68=context68,require_context=True)
    v.need(host==c.policy.hostname and deadline==c.budget.deadline and
           permit68 is not None and c.permit is permit68,'NATIVE_CONNECTION_CONTEXT68')
    c.permit=None  # one constructor, only while acquisition owns the entry
    timeout=min(timeout,deadline-clock());v.need(timeout>0,'NATIVE_CONNECTION_DEADLINE68')
    return _JSONConnection67(t._verified_connection(host,timeout,capture,clock,deadline))


def acquire67(locator,policy,bearer_supplier,state,clock,budget,synthetic=None,*,context68=None):
    """One acquisition, complete bounded EOF read, raw return retained privately."""
    native_context=None
    try:
        if synthetic is None:
            native_context=_native_preflight68(policy=policy,state=state,clock=clock,
              budget=budget,context68=context68)
        else:v.need(type(synthetic) is SyntheticBoundary67,'SYNTHETIC_BOUNDARY67')
        v.need(state.validator.first_unknown is None,'PREVIOUS_UNKNOWN')
        v.need(type(budget) is t._Budget66 and budget.deadline==budget.started+300 and
          0<budget.deadline-clock()<=300,'OIDC_BUDGET67')
        host,path=request_target67(locator,policy)  # BEFORE bearer/connection
        v.need(not getattr(state,'_acquisition67_consumed',False),'OIDC_ALREADY_CONSUMED67')
        state._acquisition67_consumed=True  # before effect, no retry after UNKNOWN
        if synthetic is None:
            native_context.permit=object();permit=native_context.permit
            def connection(*args):return _native_connection67(*args,context68=native_context,permit68=permit)
        else:
            v.need(type(synthetic) is SyntheticBoundary67,'SYNTHETIC_BOUNDARY67')
            def connection(*args):return _JSONConnection67(synthetic.acquisition_connection(*args))
        wire=t._Provider(connection,bearer_supplier,None,clock,budget.deadline,state,
          'SYNTHETIC_ONLY_NOT_NATIVE' if synthetic is not None else 'OIDC_ACQUISITION67')
        raw=wire._perform(host,path,v.RECORD_MAX,budget.deadline,True,False)
        state.originals.append(('OIDC_ACQUISITION_ORIGINAL67',raw))  # BEFORE guards
        v.need(clock()<budget.deadline,'OIDC_ACQUISITION_LATE67')
        v.need(raw.status==200 and raw.error is None and raw.eof is True,'OIDC_ACQUISITION_RETURN67')
        response=v.parse(raw.body,v.RECORD_MAX)
        v.need(type(response) is dict and type(response.get('value')) is str,'OIDC_VALUE67')
        token=response['value']
        v.need(0<len(token)<=16384 and token.count('.')==2 and
          all(re.fullmatch(r'[A-Za-z0-9_-]+',part) for part in token.split('.')),'OIDC_COMPACT67')
        state.originals.append(('OIDC_TOKEN_PRIVATE67',token))
        if native_context is not None:
            _native_preflight68(policy=policy,state=state,clock=clock,budget=budget,context68=native_context)
        return token  # same-process memory only; never serialized or hashed publicly
    except Exception as error:
        state.originals.append(('ACQUISITION_PRIMARY67',error))
        state.fail(str(error) if isinstance(error,v.Refuse) else 'OIDC_ACQUISITION_EXCEPTION67')
    finally:
        if native_context is not None:native_context.permit=None


def _deliver67(locator,policy,bearer_supplier,credential_supplier,target,bindings,
               state,clock,budget,synthetic=None,*,context68=None):
    """One shared acquire->verifier boundary->hostsource->Reader lifecycle."""
    try:
        if synthetic is None:
            context68=_native_preflight68(policy=policy,target=target,bindings=bindings,state=state,
              clock=clock,budget=budget,context68=context68)
        else:v.need(type(synthetic) is SyntheticBoundary67,'SYNTHETIC_BOUNDARY67')
        expected=t._REVIEWED_EXPECTED65 if synthetic is None else synthetic.expected
        step=t._REVIEWED_STEP66 if synthetic is None else synthetic.step
        _step67(step,expected)
        v.need(policy.audience==expected.audience,'REQUEST_AUDIENCE_BINDING67')
        a.preflight(target,bindings)
        token=acquire67(locator,policy,bearer_supplier,state,clock,budget,synthetic,context68=context68)
        if synthetic is None:
            _native_preflight68(policy=policy,target=target,bindings=bindings,state=state,
              clock=clock,budget=budget,context68=context68)
            # Existing native_factory performs the actual fixed issuer/JWKS/
            # PyJWT verification; no callbacks can replace it on the native route.
            bound=t.native_factory(host_token=token,target=target,bindings=bindings,
              credential_supplier=credential_supplier,state=state,budget66=budget)
        else:
            # Explicit seam for inert identity only. It cannot mint a native
            # registry entry or claim signature execution. Native path unchanged.
            v.need(type(synthetic) is SyntheticBoundary67 and token==synthetic.token,
                   'SYNTHETIC_TOKEN_BOUNDARY67')
            state.originals.append(('SYNTHETIC_VERIFIER_BOUNDARY67',synthetic.claims))
            p=synthetic.provider
            v.need(type(p) is t._Provider and p.classification=='SYNTHETIC_ONLY_NOT_NATIVE' and
              p.credential_supplier is credential_supplier,'SYNTHETIC_PROVIDER67')
            bound=t._bind65(synthetic.claims,expected,target,bindings,t._Public65(p),p,state,
              clock,budget.deadline,True,synthetic.redirect_policy)
        return a.readback65(bound)
    except Exception as error:
        state.originals.append(('DELIVERY_PRIMARY67',error))
        state.fail(str(error) if isinstance(error,v.Refuse) else 'OIDC_DELIVERY_EXCEPTION67')


def synthetic_pipeline67(*,locator,policy,bearer_supplier,credential_supplier,target,
                         bindings,state,clock,budget,boundary):
    v.need(type(boundary) is SyntheticBoundary67,'EXPLICIT_SYNTHETIC67')
    return _deliver67(locator,policy,bearer_supplier,credential_supplier,target,bindings,
                      state,clock,budget,boundary)


def native_cli67():
    # Shared admission BEFORE environment/stdin/credential/dependency/connect.
    context=_native_preflight68()
    clock=context.clock;budget=context.budget;state=context.state
    try:
        import os
        locator=os.environ['ACTIONS_ID_TOKEN_REQUEST_URL']
        request_target67(locator,context.policy)  # before request bearer
        def bearer():return os.environ['ACTIONS_ID_TOKEN_REQUEST_TOKEN']
        def readonly():return os.environ[context.step.credential_variable]
        result=_deliver67(locator,context.policy,bearer,readonly,context.target,
          context.bindings,state,clock,budget,context68=context)
        return {'classification':result.classification,'validator':result.validator_receipt,
                'live_authority':False,'dispatch_performed':False}
    except Exception as error:
        state.originals.append(('NATIVE_CLI_PRIMARY67',error))
        state.fail(str(error) if isinstance(error,v.Refuse) else 'OIDC_CLI_EXCEPTION67')
