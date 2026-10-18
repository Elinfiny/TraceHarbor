"""NEW95 synthetic transport/capture regressions; never native authority."""
import base64
import contextlib
import hashlib
import http.client
import io
import json
import os
from pathlib import Path
import sys
import time
from unittest.mock import patch
import one_native94 as n

SCOPE='SINTETIC_NEW95_NOT_NATIVE_AUTHORITY'
SCOPE96='SINTETIC_NEW96_REMAINING_COVERAGE_NOT_NATIVE_AUTHORITY'

def require(value):
    if not value:raise AssertionError('NEW95_ASSERTION')

def expected(call):
    try:call()
    except n.ProviderError:return
    raise AssertionError('NEW95_EXPECTED_REFUSAL')

def canary():
    def enc(value):return base64.urlsafe_b64encode(value).rstrip(b'=')
    return b'.'.join((enc(b'{"alg":"SYNTHETIC-NO-SIGNATURE95"}'),
        enc(b'{"synthetic":"NEW95-PRIVATE-CANARY-NOT-AUTHORITY"}'),enc(b'NOT-A-SIGNATURE95')))

class Clock:
    def __init__(self):self.now=0.0
    def __call__(self):return self.now

class InertChannel95:
    classification='INERT_NOT_AUTHENTIC_DURABLE_CHANNEL95'
    def __init__(self,mode='OK'):
        self.mode=mode;self.puts=[];self.reads=[];self.capture=None
        self.original=RuntimeError('NEW95_PRIVATE_DURABLE_ERROR')
    def put_once(self,sequence,raw,deadline):
        require(self.capture.count==sequence+1 and self.capture.total>=len(raw))
        self.puts.append((sequence,raw,deadline))
        if self.mode=='PUT_UNKNOWN':raise self.original
        return sequence
    def readback(self,receipt,deadline):
        self.reads.append((receipt,deadline))
        if self.mode=='READ_UNKNOWN':raise self.original
        return self.puts[receipt][1]

class InertHTTPS95:
    def __init__(self,clock,body,status=200,mode='OK'):
        self.clock,self.body,self.status,self.mode=clock,body,status,mode
        self.timeout=None;self.sock=None;self.requests=[];self.response_closes=0;self.connection_closes=0
        self.partial=http.client.IncompleteRead(body,100)
        self.cleanup=RuntimeError(body.decode('ascii'))
    def request(self,method,path,body,headers):self.requests.append((method,path,body,headers))
    def getresponse(self):return self
    def getheader(self,name):return 'application/json'
    def read(self,limit):
        require(len(self.body)<limit)
        if self.mode=='PARTIAL':raise self.partial
        if self.mode=='LATE':self.clock.now=11.0
        return self.body
    def close(self):
        # _https closes the response, then the connection (same inert object).
        if self.response_closes==0:
            self.response_closes=1
            if self.mode=='PARTIAL':raise self.cleanup
        else:self.connection_closes+=1

def setup(body,status=200,mode='OK',channel_mode='OK'):
    clock=Clock();window=n.Window94(10,None,clock=clock,wall=2000000095)
    channel=InertChannel95(channel_mode);capture=n.ProtectedCapture94(channel,window)
    window.capture=capture;channel.capture=capture
    resource=InertHTTPS95(clock,body,status,mode);constructed=[]
    def factory(host,timeout,context):
        require(host in ('synthetic-oidc.invalid','api.github.com'));constructed.append(host)
        resource.timeout=timeout;return resource
    return window,channel,capture,resource,constructed,factory

def no_secret(channel,public,token,body):
    serialized=b'\n'.join(x[1] for x in channel.puts)+json.dumps(public,sort_keys=True).encode()
    forms={token,body,base64.b64encode(token),base64.urlsafe_b64encode(token),base64.b64encode(body),
        token.hex().encode(),body.hex().encode(),hashlib.sha256(token).hexdigest().encode(),
        hashlib.sha256(body).hexdigest().encode()}
    require(all(value not in serialized for value in forms))
    for _,raw,_ in channel.puts:
        value=json.loads(raw)
        if value.get('classification')=='PROCESS_PRIVATE_CREDENTIAL95':
            require(set(value)=={'classification','stage','kind','byte_count','status','error_type'})

def defaults():
    class Guard(dict):
        hits=0
        def __getitem__(self,key):self.hits+=1;raise AssertionError('ENV_LOOKUP95')
        def get(self,*args):self.hits+=1;raise AssertionError('ENV_LOOKUP95')
    guard=Guard()
    with patch.object(os,'environ',guard):require(n.load_context94() is None)
    require(guard.hits==0 and n._CURRENT is None and not n._ENTRY_ATTEMPTED)
    require(all(v is None for v in (n.REVIEWED_CONFIGURATION,n.PROTECTED_ADMISSION,n.PROTECTED_CAPTURE,n.QUALIFIED_DEPENDENCY_CLOSURE)))

def credential_call(window):
    return n._https(window,'synthetic-oidc.invalid','GET','/synthetic95',None,
        {'Accept':'application/json','Authorization':'Bearer SYNTHETIC-REQUEST95'},16384,
        _scope95=n._CREDENTIAL_RESPONSE95)

def case1_success():
    token=canary();body=json.dumps({'value':token.decode()}).encode();w,ch,cap,res,made,factory=setup(body)
    with patch.object(n.http.client,'HTTPSConnection',factory):status,actual=credential_call(w)
    require(status==200 and actual is body and any(v is body for _,_,v in w.originals))
    require(res.response_closes==1 and res.connection_closes==1 and len(made)==1)
    require(w.primary is None and ch.puts)
    no_secret(ch,{'case':1,'status':status,'classification':SCOPE},token,body)

def case2_non200():
    token=canary();body=json.dumps({'error':token.decode()}).encode();w,ch,cap,res,made,factory=setup(body,status=401)
    with patch.object(n.http.client,'HTTPSConnection',factory):status,actual=credential_call(w)
    require(status==401 and actual is body and any(v is body for _,_,v in w.originals))
    require(len(res.requests)==1 and res.response_closes==1 and res.connection_closes==1)
    no_secret(ch,{'case':2,'status':status,'classification':SCOPE},token,body)

def case3_partial_cleanup():
    token=canary();body=json.dumps({'partial':token.decode()}).encode();w,ch,cap,res,made,factory=setup(body,mode='PARTIAL')
    with patch.object(n.http.client,'HTTPSConnection',factory):expected(lambda:credential_call(w))
    primary=w.primary;require(primary=='CALL_UNKNOWN94_HTTP_BODY')
    require(any(v is res.partial for _,_,v in w.originals) and any(v is res.cleanup for _,_,v in w.originals))
    require(any(v==body and kind=='PARTIAL' for _,kind,v in w.originals))
    error_index=next(i for i,x in enumerate(w.originals) if x[2] is res.partial)
    cleanup_index=next(i for i,x in enumerate(w.originals) if x[2] is res.cleanup)
    require(error_index<cleanup_index and res.response_closes==1 and res.connection_closes==1)
    require(w.primary==primary and ('CODE','CLEANUP_UNKNOWN94') in w.secondary)
    no_secret(ch,{'case':3,'primary':primary,'classification':SCOPE},token,body)

def case4_late():
    token=canary();body=json.dumps({'late':token.decode()}).encode();w,ch,cap,res,made,factory=setup(body,mode='LATE')
    with patch.object(n.http.client,'HTTPSConnection',factory):
        expected(lambda:credential_call(w));primary=w.primary
        require(any(v is body for _,_,v in w.originals))
        expected(lambda:credential_call(w))
    require(primary is not None and w.primary==primary and len(made)==1 and len(res.requests)==1)
    require(res.response_closes==1 and res.connection_closes==1)
    no_secret(ch,{'case':4,'primary':primary,'classification':SCOPE},token,body)

def case5_durable_unknown(modes=('PUT_UNKNOWN','READ_UNKNOWN')):
    token=canary();body=json.dumps({'never_durable':token.decode()}).encode()
    require(type(modes) is tuple and modes and all(v in ('PUT_UNKNOWN','READ_UNKNOWN') for v in modes))
    for mode in modes:
        w,ch,cap,res,made,factory=setup(body,channel_mode=mode)
        expected(lambda:w.invoke('FIRST_DURABLE95',lambda:95))
        primary=w.primary;require(primary=='PRIVATE_DURABLE_CAPTURE_UNKNOWN95')
        require(cap.durable_unknown95 and cap.count==1 and len(ch.puts)==1)
        require(any(v is ch.original for _,_,v in cap.originals))
        require(len(ch.reads)==(1 if mode=='READ_UNKNOWN' else 0))
        require(w.retain('RESPONSE_CLOSE','EXCEPTION',res.cleanup,_scope95=n._CREDENTIAL_RESPONSE95) is False)
        require(w.retain('CONNECTION_CLOSE','EXCEPTION',res.partial,_scope95=n._CREDENTIAL_RESPONSE95) is False)
        require(len(ch.puts)==1 and cap.count==1 and w.primary==primary)
        events=[(s,k,v) for s,k,v in w.originals if s in ('RESPONSE_CLOSE','CONNECTION_CLOSE')]
        require([v for s,k,v in events if k=='EXCEPTION']==[res.cleanup,res.partial])
        require([(s,k) for s,k,v in events]==[
            ('RESPONSE_CLOSE','EXCEPTION'),('RESPONSE_CLOSE','CAPTURE_EXCEPTION'),
            ('CONNECTION_CLOSE','EXCEPTION'),('CONNECTION_CLOSE','CAPTURE_EXCEPTION')])
        capture_errors=[(s,v) for s,k,v in events if k=='CAPTURE_EXCEPTION']
        require([s for s,v in capture_errors]==['RESPONSE_CLOSE','CONNECTION_CLOSE'])
        require(all(type(v) is n.ProviderError and str(v)=='PRIVATE_DURABLE_CAPTURE_LATCHED95' for s,v in capture_errors))
        require(all((s,v) in w.secondary for s,v in capture_errors))
        require(w.primary==primary and cap.count==1 and len(ch.puts)==1)
        require(len(ch.reads)==(1 if mode=='READ_UNKNOWN' else 0))
        no_secret(ch,{'case':5,'primary':primary,'mode':mode,'classification':SCOPE},token,body)

def case6_ordinary_and_user_agent():
    body=b'{"ordinary":"NEW95-nonsecret-public-fixture"}'
    w,ch,cap,res,made,factory=setup(body)
    client=n.GitClient94(w,lambda:'SYNTHETIC-GIT95')
    with patch.object(n.http.client,'HTTPSConnection',factory):reply=client.request('GET','',None)
    require(reply.body is body and reply.status==200 and len(res.requests)==1)
    method,path,payload,headers=res.requests[0]
    require(method=='GET' and path=='/repos/Elinfiny/TraceHarbor' and payload is None)
    require(headers['User-Agent']=='TraceHarbor/one94' and headers['X-GitHub-Api-Version']=='2022-11-28')
    require(headers['Accept']=='application/vnd.github+json' and headers['Authorization']=='Bearer SYNTHETIC-GIT95')
    require(any(json.loads(raw).get('value',{}).get('base64')==base64.b64encode(body).decode() for _,raw,_ in ch.puts))
    require(any(v is body for _,_,v in w.originals) and any(v is body for _,_,v in cap.originals))
    calls=len(res.requests)
    with patch.object(n.http.client,'HTTPSConnection',factory):
        expected(lambda:n._https(w,'api.github.com','GET','/',None,{},10,_scope95='UNKNOWN'))
    require(len(res.requests)==calls and n._CURRENT is None)

def main():
    # NEW96 exact selector; cases1-4 and old95 main are never invoked.
    root=Path(sys.argv[1]);root.mkdir(mode=0o700)
    def audit(event,args):
        if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen','os.system'):
            raise AssertionError('REAL_EFFECT_DENIED96')
    sys.addaudithook(audit);receipts=[]
    entries=(('A_PUT_UNKNOWN',lambda:case5_durable_unknown(('PUT_UNKNOWN',))),
             ('B_READ_UNKNOWN',lambda:case5_durable_unknown(('READ_UNKNOWN',))),
             ('C_ORDINARY_USER_AGENT_UNKNOWN_SCOPE',case6_ordinary_and_user_agent))
    safe_types={AssertionError:'AssertionError',n.ProviderError:'ProviderError',RuntimeError:'RuntimeError',
                TypeError:'TypeError',KeyError:'KeyError',ValueError:'ValueError',TimeoutError:'TimeoutError'}
    safe_functions={'main','require','expected','defaults','case5_durable_unknown','case6_ordinary_and_user_agent','no_secret'}
    for name,call in entries:
        started=time.monotonic();stdout=io.StringIO();stderr=io.StringIO();error=None;location=None
        try:
            with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):defaults();call()
        except BaseException as original:
            error=original
            tb=original.__traceback__
            while tb is not None:
                code=tb.tb_frame.f_code
                if code.co_filename==__file__ and code.co_name in safe_functions:
                    location={'function':code.co_name,'line':tb.tb_lineno}
                tb=tb.tb_next
        out,err=stdout.getvalue().encode(),stderr.getvalue().encode()
        for label,raw in [('stdout',out),('stderr',err)]:
            p=root/(name+'-'+label+'.bin');p.write_bytes(raw);p.chmod(0o600)
        receipt={'case':name,'classification':SCOPE96,'exit':0 if error is None else 1,
            'elapsed_seconds':time.monotonic()-started,'stdout_bytes':len(out),'stderr_bytes':len(err),
            'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest(),
            'exception_type':None if error is None else safe_types.get(type(error),'OTHER_ALLOWLISTED_CLASSIFICATION'),
            'exception_location':location,'error_classification':None if error is None else 'UNEXPECTED_CASE_ABORT96'}
        p=root/(name+'-receipt.json');p.write_text(json.dumps(receipt,sort_keys=True));p.chmod(0o600);receipts.append(receipt)
        if error is not None or out or err:
            print(json.dumps({'group':'NEW96','classification':SCOPE96,'status':'ABORT_NO_REPAIR_NO_RERUN','receipts':receipts}));return 2
    print(json.dumps({'group':'NEW96','classification':SCOPE96,'status':'PASS_INERT_REMAINING_COVERAGE_ONLY','passed':3,
        'receipts':receipts,'native_authority':False,'real_HTTP':0,'OIDC_acquisition':0,'model_calls':0,'spend_usd':'0'}));return 0

if __name__=='__main__':raise SystemExit(main())
