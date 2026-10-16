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


def native_factory(*,credential_supplier=None):
    # All bindings remain None. Caller JSON/PID/env/token is never admission.
    if NATIVE_HOST_ROUTE is None or NATIVE_REDIRECT_POLICY is None or EXTERNAL_ADMISSION_GATE is None or nativeAdmission is None or PLAN is None:
        raise v.Refuse('INACTIVE60_NATIVE_ROUTE_CUSTODY_REDIRECT_ADMISSION_UNBOUND')
    # Future authentic host must install a real verifier; the current release
    # has no verifier and does not accept truthy/self-authored capability objects.
    raise v.Refuse('INACTIVE60_NO_INSTALLED_AUTHENTIC_HOST_VERIFIER')

if __name__=='__main__':
    raise SystemExit('INACTIVE60_NATIVE_ROUTE_CUSTODY_REDIRECT_ADMISSION_UNBOUND')
