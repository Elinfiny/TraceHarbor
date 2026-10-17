"""Concrete private HTTPS transport; installed native admission remains absent.

TLS, DNS pinning and HTTP code are real implementations, never exercised by
this qualification. Deadline checks do not prove kernel/backend cancellation.
No environment credential/proxy access, retries, dispatch or model methods.
"""
import hashlib
import http.client
import ipaddress
import re
import socket
import ssl
import time
from dataclasses import dataclass,field
from urllib.parse import urlsplit
import native27_readback59 as a
import native27_validator42 as v

NATIVE_HOST_ROUTE = None
NATIVE_REDIRECT_POLICY = None
EXTERNAL_ADMISSION_GATE = None
nativeAdmission = None
PLAN = None
HEADER_BYTES=8192
HEADER_LINES=64
HEADER_LINE=2048
FRAMING_BYTES=8192
FRAMING_LINES=64
FRAMING_LINE=2048
BASE=v.BASE

@dataclass
class Capture:
    status: object=None
    headers: list=field(default_factory=list,repr=False)
    wire_headers: bytearray=field(default_factory=bytearray,repr=False)
    body: bytearray=field(default_factory=bytearray,repr=False)
    observed_body_bytes: int=0
    body_hasher: object=field(default_factory=hashlib.sha256,repr=False)
    eof: bool=False
    primary: object=field(default=None,repr=False)
    primary_code: object=None
    cleanup: list=field(default_factory=list,repr=False)
    header_bytes: int=0
    framing_wire: bytearray=field(default_factory=bytearray,repr=False)

class _HeaderFile:
    """Bound actual status/header wire reads BEFORE stdlib HTTP parsing."""
    def __init__(self, stream, capture, clock, deadline, sock):
        self.stream,self.capture,self.clock,self.deadline=stream,capture,clock,deadline
        self.lines=0;self.done=False;self.sock=sock
    def readline(self,size=-1):
        # Fixed protocol: reject interim1xx on its FIRST bounded original line,
        # before HTTPResponse can skip100 and enter another header block.
        remaining_time=self.deadline-self.clock()
        if remaining_time<=0:raise v.Refuse('HEADER_DEADLINE')
        self.sock.settimeout(remaining_time)
        target=self.capture.framing_wire if self.done else self.capture.wire_headers
        maximum=FRAMING_BYTES if self.done else HEADER_BYTES
        line_maximum=FRAMING_LINE if self.done else HEADER_LINE
        remaining=maximum-len(target)
        line=self.stream.readline(min(line_maximum+1,remaining+1,size if size>=0 else line_maximum+1))
        target.extend(line[:max(0,maximum+1-len(target))])  # original BEFORE guards
        if self.done:self.framing_lines=getattr(self,'framing_lines',0)+1
        else:self.lines+=1
        count=self.framing_lines if self.done else self.lines
        if len(line)>line_maximum or len(target)>maximum or count>(FRAMING_LINES if self.done else HEADER_LINES):
            raise v.Refuse('FRAMING_RESOURCE_BOUND' if self.done else 'HEADER_RESOURCE_BOUND')
        if self.clock()>=self.deadline:raise v.Refuse('HEADER_LATE')
        if self.done:return line  # bounded chunk-size/trailer framing, never unbounded
        if self.lines==1:
            match=re.fullmatch(br'HTTP/1\.[01] ([0-9]{3})(?: [^\r\n]*)?\r\n',line)
            if match is None:raise v.Refuse('STATUS_LINE_MALFORMED')
            self.capture.status=int(match.group(1))
            if not 100<=self.capture.status<=599:raise v.Refuse('STATUS_LINE_MALFORMED')
            if 100<=self.capture.status<200:raise v.Refuse('UNSUPPORTED_INTERIM_STATUS')
        elif line==b'\r\n':self.done=True
        else:
            if not line.endswith(b'\r\n') or b':' not in line:raise v.Refuse('HEADER_LINE_MALFORMED')
            key,value=line[:-2].split(b':',1)
            if re.fullmatch(br"[A-Za-z0-9!#$%&'*+.^_|~`-]+",key) is None or any(c<32 and c!=9 or c==127 for c in value):
                raise v.Refuse('HEADER_LINE_MALFORMED')
        return line
    def __getattr__(self,name):return getattr(self.stream,name)

class _SocketFileProxy:
    def __init__(self,sock,capture,clock,deadline):self.sock,self.args=sock,(capture,clock,deadline)
    def makefile(self,*args,**kwargs):return _HeaderFile(self.sock.makefile(*args,**kwargs),*self.args,self.sock)


def _verified_connection(host,timeout,capture,clock,deadline):
    """No proxy; verify TLS hostname/certificate; connect one checked public IP.

    DNS itself has no cancellable stdlib deadline guarantee. Check its return
    against the SAME deadline and never connect after a late DNS result.
    """
    if clock()>=deadline:raise v.Refuse('DNS_DEADLINE')
    addresses=socket.getaddrinfo(host,443,type=socket.SOCK_STREAM)
    if clock()>=deadline:raise v.Refuse('DNS_LATE')
    v.need(0<len(addresses)<=16,'DNS_ADDRESS_BOUND')
    for family,kind,proto,canon,address in addresses:
        v.need(family in (socket.AF_INET,socket.AF_INET6) and ipaddress.ip_address(address[0]).is_global,
               'NONPUBLIC_TARGET')
    family,kind,proto,_,address=addresses[0]
    context=ssl.create_default_context()
    v.need(context.check_hostname and context.verify_mode==ssl.CERT_REQUIRED,'TLS_VERIFY_REQUIRED')
    connection=http.client.HTTPSConnection(host,443,timeout=timeout,context=context)
    def connect_public(_address,timeout=timeout,source_address=None):
        v.need(source_address is None,'SOURCE_ADDRESS_FORBIDDEN')
        remaining=deadline-clock();v.need(remaining>0,'CONNECT_DEADLINE')
        sock=socket.socket(family,kind,proto)
        try:
            sock.settimeout(min(timeout,remaining));sock.connect(address)
            return sock
        except Exception as primary:
            capture.primary=primary;capture.primary_code='TRANSPORT_IO_ERROR'
            try:sock.close()
            except Exception as cleanup:capture.cleanup.append(('CONNECT_SOCKET_CLOSE_ERROR',cleanup))
            raise
    connection._create_connection=connect_public
    def response(sock,**kwargs):
        return http.client.HTTPResponse(_SocketFileProxy(sock,capture,clock,deadline),**kwargs)
    connection.response_class=response
    return connection


def _endpoint(path):
    v.need(type(path) is str and len(path)<=512 and path.startswith(BASE+'/'),'ENDPOINT')
    tail=path[len(BASE):]
    patterns=(r'/actions/runs/([1-9][0-9]*)',r'/actions/runs/([1-9][0-9]*)/attempts/1/jobs\?per_page=100',
              r'/actions/jobs/([1-9][0-9]*)(?:/logs)?',r'/git/(?:commits|blobs)/[0-9a-f]{40}',
              r'/git/trees/[0-9a-f]{40}(?:\?recursive=1)?')
    for pattern in patterns:
        match=re.fullmatch(pattern,tail)
        if match:
            if match.lastindex:v.need(a.integer(int(match.group(1))),'ENDPOINT_ID')
            return tail
    v.need(tail in ('/git/ref/heads/main','/git/ref/'+v.REF[5:]),'ENDPOINT_ALLOWLIST')
    return tail


def _location(location):
    v.need(type(location) is str and len(location)<=8192 and not any(ord(c)<33 or ord(c)>126 for c in location),'LOCATION_TEXT')
    u=urlsplit(location)
    v.need(u.scheme=='https' and u.hostname and u.username is None and u.password is None
           and not u.fragment and u.port in (None,443),'LOCATION_HTTPS')
    host=u.hostname
    try:ipaddress.ip_address(host)
    except ValueError:pass
    else:raise v.Refuse('LITERAL_IP_FORBIDDEN')
    v.need(len(host)<=253 and '.' in host and not host.endswith(('.localhost','.local','.internal'))
           and host!='localhost' and re.fullmatch('[a-z0-9.-]+',host),'LOCATION_PUBLIC_NAME')
    return host,(u.path or '/')+('?' +u.query if u.query else '')

class _Provider:
    def __init__(self,connection_factory,credential_supplier,redirect_policy,clock,deadline,state,classification):
        self.connection_factory,self.credential_supplier=connection_factory,credential_supplier
        self.redirect_policy,self.clock,self.deadline,self.state=redirect_policy,clock,deadline,state
        self.classification=classification
        self._pending_location=None
    def _remaining(self,connection=None):
        v.need(self.state.validator.first_unknown is None,'PREVIOUS_UNKNOWN')
        remaining=self.deadline-self.clock();v.need(remaining>0,'TRANSPORT_DEADLINE')
        if connection is not None:
            connection.timeout=remaining
            if connection.sock is not None:connection.sock.settimeout(remaining)
        return remaining
    def _post(self,stage):
        v.need(self.clock()<self.deadline,stage+'_LATE')
    def get(self,path,limit,deadline):
        self._remaining();_endpoint(path)
        return self._perform('api.github.com',path,limit,deadline,True,path.endswith('/logs'))
    def download(self,location,limit,deadline):
        self._remaining()
        v.need(self._pending_location is not None and location==self._pending_location,'NO_PROVIDER_LOCATION')
        host,path=_location(location)
        v.need(self.redirect_policy is not None and self.redirect_policy(location) is True,'REDIRECT_UNBOUND60')
        self._pending_location=None  # consume once before connection; UNKNOWN cannot replay
        return self._perform(host,path,limit,deadline,False,False)
    def _perform(self,host,path,limit,deadline,authenticated,log_redirect):
        self._remaining();v.need(deadline==self.deadline,'DEADLINE_CHANGED')
        v.need(type(limit) is int and 0<limit<=v.LOG_MAX,'BODY_LIMIT')
        cap=Capture();connection=response=None
        try:
            timeout=self._remaining()
            connection=self.connection_factory(host,timeout,cap,self.clock,self.deadline)
            self._post('CONSTRUCTION');self._remaining(connection);connection.connect();self._post('CONNECT')
            headers={'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','User-Agent':'TraceHarbor-readback60'}
            if authenticated:
                # Reached only by separately admitted native factory, or explicit
                # synthetic credential supplier in tests. Never read environment.
                self._remaining(connection);token=self.credential_supplier();self._post('CUSTODY_RETURN')
                v.need(type(token) is str and 0<len(token)<=8192 and '\r' not in token and '\n' not in token,'CREDENTIAL_SHAPE')
                headers['Authorization']='Bearer '+token
            self._remaining(connection);connection.putrequest('GET',path,skip_accept_encoding=True);self._post('REQUEST')
            for key,value in headers.items():
                self._remaining(connection);connection.putheader(key,value);self._post('WRITE_HEADER')
            # No outbound token/header is persisted in captures or public receipts.
            self._remaining(connection);connection.endheaders();self._post('END_HEADERS')
            headers.clear()
            if authenticated:token=None
            self._remaining(connection);response=connection.getresponse();cap.status=response.status;self._post('STATUS')
            self._remaining(connection)
            pairs=response.getheaders()
            for key,value in pairs:
                encoded=(key+': '+value+'\r\n').encode('latin1')
                cap.header_bytes+=len(encoded)
                cap.headers.append((key[:HEADER_LINE+1],value[:HEADER_LINE+1]))
                v.need(len(cap.headers)<=HEADER_LINES and len(encoded)<=HEADER_LINE and cap.header_bytes<=HEADER_BYTES,'HEADER_RESOURCE_BOUND')
            self._post('HEADERS')
            while len(cap.body)<=limit:
                self._remaining(connection);request_count=min(8192,limit+1-len(cap.body))
                if request_count==0:break
                chunk=response.read(request_count)
                v.need(type(chunk) is bytes,'BODY_RETURN_TYPE')
                # Actual bounded bytes are retained before size/EOF/deadline guards.
                cap.observed_body_bytes+=len(chunk);cap.body_hasher.update(chunk)
                cap.body.extend(chunk[:max(0,limit+1-len(cap.body))])
                if not chunk:cap.eof=True
                self._post('BODY')
                v.need(len(chunk)<=request_count and cap.observed_body_bytes<=limit,'BODY_OVERSIZE')
                if not chunk:break
            lengths=[value for key,value in cap.headers if key.lower()=='content-length']
            v.need(len(lengths)<=1 and (not lengths or lengths[0]==str(cap.observed_body_bytes)),'BODY_EOF_LENGTH')
            v.need(cap.eof,'BODY_EOF')
            if log_redirect:
                v.need(cap.status==302,'LOG_STATUS')
                locations=[value for key,value in cap.headers if key.lower()=='location']
                v.need(len(locations)==1,'LOCATION_COUNT');_location(locations[0])
                self._pending_location=locations[0]
            else:v.need(cap.status==200,'STATUS_NOT_200_NO_REDIRECT')
        except Exception as error:
            if isinstance(error,http.client.IncompleteRead) and type(error.partial) is bytes:
                cap.observed_body_bytes+=len(error.partial);cap.body_hasher.update(error.partial)
                cap.body.extend(error.partial[:max(0,limit+1-len(cap.body))])
            cap.primary=error
            safe={'CONSTRUCTION_LATE','CONNECT_LATE','CUSTODY_RETURN_LATE','REQUEST_LATE','WRITE_HEADER_LATE','END_HEADERS_LATE','STATUS_LATE','HEADERS_LATE','BODY_LATE','TRANSPORT_DEADLINE','HEADER_RESOURCE_BOUND','FRAMING_RESOURCE_BOUND','STATUS_LINE_MALFORMED','HEADER_LINE_MALFORMED','UNSUPPORTED_INTERIM_STATUS','HEADER_DEADLINE','HEADER_LATE','BODY_OVERSIZE','BODY_RETURN_TYPE','BODY_EOF_LENGTH','BODY_EOF','LOG_STATUS','LOCATION_COUNT','LOCATION_TEXT','LOCATION_HTTPS','LITERAL_IP_FORBIDDEN','LOCATION_PUBLIC_NAME','STATUS_NOT_200_NO_REDIRECT','DNS_DEADLINE','DNS_LATE','DNS_ADDRESS_BOUND','NONPUBLIC_TARGET','TLS_VERIFY_REQUIRED','SOURCE_ADDRESS_FORBIDDEN','CONNECT_DEADLINE','CREDENTIAL_SHAPE'}
            cap.primary_code=str(error) if type(error) is v.Refuse and str(error) in safe else 'TRANSPORT_IO_ERROR'
        finally:
            # One explicit close per owned handle. stdlib may internally close
            # its socket too; no kernel-close/cancellation attestation is implied.
            for kind,resource in [('response',response),('connection',connection)]:
                if resource is None:continue
                # Timeout preparation is OPTIONAL cleanup work. Its failure
                # must never skip this handle's independently attempted close.
                try:
                    remaining=self.deadline-self.clock()
                    if remaining<=0:cap.cleanup.append((kind+'_BEFORE_CLOSE_LATE',None))
                    if connection is not None and remaining>0:
                        connection.timeout=remaining
                        if connection.sock is not None:connection.sock.settimeout(remaining)
                except Exception as error:cap.cleanup.append((kind+'_TIMEOUT_PREP_ERROR',error))
                try:resource.close()
                except Exception as error:cap.cleanup.append((kind+'_CLOSE_ERROR',error))
                # Independent post-close observation cannot prevent next handle.
                try:
                    if self.clock()>=self.deadline:cap.cleanup.append((kind+'_AFTER_CLOSE_LATE',None))
                except Exception as error:cap.cleanup.append((kind+'_POST_CLOSE_CLOCK_ERROR',error))
            self.state.originals.append(('TRANSPORT60_ORIGINAL',cap))
            if cap.primary_code or cap.cleanup:
                # Capture actual primary and cleanup BEFORE establishing first UNKNOWN.
                self.state.validator.first_unknown=self.state.validator.first_unknown or cap.primary_code or 'CLEANUP_ERROR'
                self._pending_location=None
        public_headers=dict(cap.headers)
        return a.Original(cap.status if type(cap.status) is int else 0,public_headers,bytes(cap.body),cap.eof,
                          cap.primary if cap.primary is not None else cap.cleanup if cap.cleanup else None)


def synthetic_provider(connection_factory,credential_supplier,redirect_policy,clock,deadline,state):
    """Fake suppliers only; this result cannot carry native provenance."""
    return _Provider(connection_factory,credential_supplier,redirect_policy,clock,deadline,state,'SYNTHETIC_ONLY_NOT_NATIVE')


# PRIVATE65: GitHub OIDC verification and same-invocation binding. No dispatcher.
# Exact reviewed deployment/admission is deliberately absent from this candidate.
_REVIEWED_EXPECTED65 = None
_REVIEWED_TARGET65 = None
_REVIEWED_BINDINGS65 = None
_LIVE_BOUND65 = {}
_REVIEWED_STEP66 = None
ISSUER65 = 'https://token.actions.githubusercontent.com'
PYJWT_VERSION65 = '2.15.1'

@dataclass(frozen=True)
class ExpectedHost65:
    audience: str
    source: str
    workflow_path: str
    workflow_sha256: str
    run_id: int
    job_id: int
    job_name: str

@dataclass(frozen=True)
class Bound65:
    provider: object = field(repr=False)
    target: object
    bindings: object = field(repr=False)
    state: object = field(repr=False)
    expected: object
    monotonic: object = field(repr=False)
    mono_anchor: float
    wall_anchor: float
    deadline: float
    synthetic: bool
    redirect_policy: object = field(default=None,repr=False)

    def wall_now(self):
        # Validator uses UTC; transport and shared Reader use only monotonic time.
        return self.wall_anchor + (self.monotonic()-self.mono_anchor)


def _claims65(claims,e,b,target):
    a.preflight(target,b)
    v.need(type(e) is ExpectedHost65 and e.source==b['source'] and
           a.integer(e.run_id) and a.integer(e.job_id) and e.run_id!=target.run_id and
           type(e.audience) is str and 0<len(e.audience)<=512 and
           e.workflow_path==v.WORKFLOW and e.workflow_sha256==b['workflow_sha256'] and
           e.job_name=='readback65','HOST_EXPECTATION65')
    # GitHub does NOT sign a job_id claim. Job identity is independently joined
    # below to attempt-scoped REST membership and one exact source-reviewed job.
    required={'iss':ISSUER65,'aud':e.audience,'sub':'repo:'+v.REPO+':ref:refs/heads/main','repository':v.REPO,
      'repository_id':str(v.RID),'repository_owner_id':str(v.OWNER),
      'sha':e.source,'workflow_sha':e.source,
      'workflow_ref':v.REPO+'/'+e.workflow_path+'@refs/heads/main',
      'run_id':str(e.run_id),'run_attempt':'1','actor_id':str(v.OWNER),
      'event_name':'workflow_dispatch','ref':'refs/heads/main',
      'runner_environment':'github-hosted'}
    v.need(type(claims) is dict and all(type(claims.get(k)) is str and claims[k]==value
           for k,value in required.items()),'SIGNED_CONTEXT65')


def _provider_json65(provider,state,path,clock,deadline):
    reader=a.Reader(provider,state,clock,deadline,None)
    return reader.json(path)


def _host_context65(provider,state,e,b,clock,deadline):
    # Every raw public REST return retained by Reader before parse/clock/schema.
    run=_provider_json65(provider,state,'/actions/runs/'+str(e.run_id),clock,deadline)
    v.need(type(run['id']) is int and run['id']==e.run_id and run['run_attempt']==1 and
      run['head_sha']==e.source and run['path']==e.workflow_path and
      run['repository']['id']==v.RID and run['repository']['full_name']==v.REPO and
      run['repository']['owner']['id']==v.OWNER and run['actor']['id']==v.OWNER and
      run['triggering_actor']['id']==v.OWNER and run['event']=='workflow_dispatch' and
      run['head_branch']=='main' and run['status']=='in_progress','HOST_RUN65')
    jobs=_provider_json65(provider,state,'/actions/runs/'+str(e.run_id)+'/attempts/1/jobs?per_page=100',clock,deadline)
    v.need(type(jobs['total_count']) is int and 0<jobs['total_count']<=100 and
           len(jobs['jobs'])==jobs['total_count'],'HOST_JOB_LIST65')
    named=[j for j in jobs['jobs'] if j.get('name')==e.job_name]
    v.need(len(named)==1 and named[0]['id']==e.job_id,'HOST_JOB_MEMBERSHIP65')
    job=_provider_json65(provider,state,'/actions/jobs/'+str(e.job_id),clock,deadline)
    for j in (named[0],job):
        v.need(type(j['id']) is int and j['id']==e.job_id and j['run_id']==e.run_id and
          j['head_sha']==e.source and j['name']==e.job_name and
          j['status']=='in_progress','HOST_JOB65')
    commit=_provider_json65(provider,state,'/git/commits/'+e.source,clock,deadline)
    v.need(commit['sha']==e.source and a.sha40(commit['tree']['sha']),'HOST_COMMIT65')
    tree=_provider_json65(provider,state,'/git/trees/'+commit['tree']['sha']+'?recursive=1',clock,deadline)
    v.need(tree['sha']==commit['tree']['sha'] and tree['truncated'] is False,'HOST_TREE65')
    entries=[x for x in tree['tree'] if x['path']==e.workflow_path and x['type']=='blob']
    v.need(len(entries)==1 and a.sha40(entries[0]['sha']),'HOST_SOURCE65')
    obj=_provider_json65(provider,state,'/git/blobs/'+entries[0]['sha'],clock,deadline)
    raw=a.base64.b64decode(obj['content'].replace('\n',''),validate=True)
    v.need(obj['encoding']=='base64' and obj['size']==len(raw)<=v.RECORD_MAX and
      obj['sha']==entries[0]['sha']==a.blob_sha(raw) and v.digest(raw)==e.workflow_sha256,
      'HOST_WORKFLOW65')
    # Exact hash is necessary but not sole authority: signed claims + genuine
    # independent REST join above are also mandatory. Reviewed source must give
    # id-token:write only to readback65; native66 must independently verify this.


class _Public65:
    """No token supplier is available to pre-custody public metadata reads."""
    def __init__(self,p):self.p=p
    def get(self,path,limit,deadline):
        _endpoint(path)
        return self.p._perform('api.github.com',path,limit,deadline,False,False)


def _verify_oidc65(token,state,clock,deadline):
    import importlib.metadata
    v.need(type(token) is str and 0<len(token)<=16384,'OIDC_INPUT65')
    state.originals.append(('OIDC_TOKEN_PRIVATE65',token))
    v.need(importlib.metadata.version('PyJWT')==PYJWT_VERSION65,'VERIFIER_VERSION65')
    # Dependency is NOT installed/imported during qualification65. This lazy
    # import is future real-host code using the established verifier, not crypto.
    import jwt
    v.need(clock()<deadline,'OIDC_DEADLINE65')
    # Bounded existing TLS/DNS/HTTP implementation, no urllib redirects/retries.
    wire=_Provider(_verified_connection,None,None,clock,deadline,state,'OIDC65')
    original=wire._perform('token.actions.githubusercontent.com','/.well-known/jwks',v.RECORD_MAX,deadline,False,False)
    state.originals.append(('JWKS_ORIGINAL65',original))
    v.need(clock()<deadline and original.error is None and original.eof and
           original.status==200,'JWKS_RETURN65')
    jwks=v.parse(original.body,v.RECORD_MAX)
    v.need(type(jwks) is dict and type(jwks.get('keys')) is list and 0<len(jwks['keys'])<=16,'JWKS_BOUND65')
    header=jwt.get_unverified_header(token)
    v.need(header.get('alg')=='RS256' and type(header.get('kid')) is str and
           0<len(header['kid'])<=256 and not any(k in header for k in ('jku','x5u','crit')),'JOSE65')
    keys=[k for k in jwks['keys'] if k.get('kid')==header['kid'] and k.get('kty')=='RSA' and
          k.get('use','sig')=='sig' and k.get('alg','RS256')=='RS256']
    v.need(len(keys)==1,'JWKS_KEY65')
    key=jwt.PyJWK.from_dict(keys[0],algorithm='RS256')
    claims=jwt.decode(token,key,algorithms=['RS256'],issuer=ISSUER65,
      audience=_REVIEWED_EXPECTED65.audience,leeway=0,
      options={'require':['iss','aud','sub','exp','iat','nbf','jti','repository','repository_id',
        'repository_owner_id','sha','workflow_sha','workflow_ref','run_id','run_attempt',
        'actor_id','event_name','ref','runner_environment'],'strict_aud':True})
    state.originals.append(('VERIFIED_OIDC_CLAIMS65',claims))
    v.need(clock()<deadline,'OIDC_LATE65')
    return claims


def _bind65(claims,e,target,bindings,public_provider,provider,state,clock,deadline,synthetic,redirect):
    from types import MappingProxyType
    try:
        v.need(state.validator.first_unknown is None,'PREVIOUS_UNKNOWN')
        _claims65(claims,e,bindings,target)
        v.need(0<deadline-clock()<=300,'BINDING_DEADLINE65')
        mono=clock();wall=time.time() if not synthetic else getattr(clock,'wall_epoch65',1792199100.0)
        v.need(type(wall) in (int,float) and a.math.isfinite(wall),'ANCHOR66')
        host_state=a.PrivateState(validator=state.validator,originals=state.originals,summaries=state.summaries)
        _host_context65(public_provider,host_state,e,bindings,clock,deadline)
        state.originals.append(('HOST_READ_COUNT65',host_state.calls))
        v.need(clock()<deadline,'HOST_LATE65')
        # Separate bounded host and target counters share the SAME sticky
        # validator/original holder/absolute deadline; no counter is reset.
        return Bound65(provider,target,MappingProxyType(dict(bindings)),state,e,clock,
                       mono,wall,deadline,synthetic,redirect)
    except Exception as error:
        state.originals.append(('BINDING_EXCEPTION65',error))
        state.fail(str(error) if isinstance(error,v.Refuse) else 'HOST_BINDING_EXCEPTION65')


def synthetic_factory65(*,claims,expected,target,bindings,provider,state,clock,deadline,redirect_policy=None):
    """Data-only fixture; NEVER signed/native and never returns live authority."""
    v.need(getattr(provider,'classification',None)=='SYNTHETIC_ONLY_NOT_NATIVE','FIXTURE_ONLY65')
    return _bind65(claims,expected,target,bindings,provider,provider,state,clock,deadline,True,redirect_policy)


def native_factory(*,credential_supplier=None,host_token=None,target=None,bindings=None,state=None,budget66=None):
    # Ordinary invocation stops BEFORE token supplier, dependency import or I/O.
    if any(x is None for x in (NATIVE_HOST_ROUTE,EXTERNAL_ADMISSION_GATE,nativeAdmission,PLAN,_REVIEWED_EXPECTED65)):
        raise v.Refuse('INACTIVE65_REVIEWED_HOST_AND_ADMISSION_UNBOUND')
    v.need(type(_REVIEWED_EXPECTED65) is ExpectedHost65 and
           NATIVE_HOST_ROUTE is _REVIEWED_EXPECTED65 and
           EXTERNAL_ADMISSION_GATE is _REVIEWED_EXPECTED65 and
           nativeAdmission is _REVIEWED_EXPECTED65,'REVIEWED_GATE65')
    v.need(target==_REVIEWED_TARGET65 and bindings==_REVIEWED_BINDINGS65 and
           type(target) is a.Target and type(bindings) is dict,'REVIEWED_TARGET65')
    _reviewed_step66()
    state=state if state is not None else a.PrivateState()
    clock=time.monotonic
    if budget66 is None:
        started=clock();budget66=_Budget66(started,started+300)
    v.need(type(budget66) is _Budget66 and budget66.deadline==budget66.started+300 and
           0<budget66.deadline-clock()<=300,'ABSOLUTE_BUDGET66')
    deadline=budget66.deadline
    try:
        claims=_verify_oidc65(host_token,state,clock,deadline)
        _claims65(claims,_REVIEWED_EXPECTED65,bindings,target)
        p=_Provider(_verified_connection,credential_supplier,None,clock,deadline,state,'VERIFIER_BOUND65')
        # Still no credential lookup; public source/context verification first.
        bound=_bind65(claims,_REVIEWED_EXPECTED65,target,bindings,_Public65(p),p,state,clock,deadline,False,None)
        _LIVE_BOUND65[id(bound)]=bound
        return bound
    except Exception as error:
        state.originals.append(('NATIVE_FACTORY_EXCEPTION65',error))
        state.fail(str(error) if isinstance(error,v.Refuse) else 'NATIVE_FACTORY_EXCEPTION65')

@dataclass(frozen=True)
class _Budget66:
    started: float
    deadline: float


@dataclass(frozen=True)
class ReviewedStep66:
    workflow_sha256: str
    job_name: str
    step_id: str
    credential_variable: str
    contents: str
    actions: str
    id_token: str


def _reviewed_step66():
    e=_REVIEWED_EXPECTED65;p=_REVIEWED_STEP66
    v.need(type(e) is ExpectedHost65 and type(p) is ReviewedStep66 and
      p.workflow_sha256==e.workflow_sha256 and p.job_name==e.job_name=='readback65' and
      p.step_id=='traceharbor_readback66' and p.credential_variable=='TRACEHARBOR_READONLY_JOB_TOKEN' and
      (p.contents,p.actions,p.id_token)==('read','read','write'),'REVIEWED_READONLY_STEP66')
    # A separately admitted review must derive this exact mapping from the
    # final source workflow. Ambient GITHUB_* or caller JSON never creates it.
    return p


def native_cli66():
    # Compatibility entry: same-process acquisition replaces the old stdin seam.
    from native27_oidc67 import native_cli67
    return native_cli67()


def consume_bound65(bound):
    v.need(type(bound) is Bound65,'BOUND_TYPE65')
    if bound.synthetic:
        v.need(getattr(bound.provider,'classification',None)=='SYNTHETIC_ONLY_NOT_NATIVE','FIXTURE_ONLY65')
    else:
        v.need(_LIVE_BOUND65.pop(id(bound),None) is bound,'NO_VERIFIED_INVOCATION65')
        v.need(type(bound.provider) is _Provider and bound.provider.connection_factory is _verified_connection,
               'NATIVE_PROVIDER65')
    return bound


if __name__=='__main__':
    raise SystemExit('INACTIVE60_NATIVE_ROUTE_CUSTODY_REDIRECT_ADMISSION_UNBOUND')
