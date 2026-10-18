"""One NEW94 inert group. No callback in this file is native authority."""
import base64
import hashlib
import http.client
import json
import os
from pathlib import Path
import sys
from types import SimpleNamespace

import one_native94 as n
import one_backend91 as g
import one_request as r

SCOPE='SINTETIC_NEW94_NOT_NATIVE_AUTHORITY'
SOURCE='51d959319c2f252c65e6b83ced8b4917c8bdef5c'
RAW_SENTINEL='PRIVATE-RESPONSE-SENTINEL94'
KEY_SENTINEL='SYNTHETIC-KEY94'

def require(value):
    if not value:raise AssertionError('NEW94_ASSERTION')

def refuses(call):
    try:call()
    except Exception:return
    raise AssertionError('NEW94_EXPECTED_REFUSAL')

class Clock:
    def __init__(self):self.now=0.0
    def __call__(self):return self.now

class InertCapture:
    def __init__(self,root):
        self.root=root;root.mkdir(mode=0o700);self.originals=[]
    def retain(self,stage,kind,original):
        self.originals.append((stage,kind,original))
        if type(original) is bytes:value={'bytes':base64.b64encode(original).decode()}
        elif type(original) is g.Reply:value={'status':original.status,'body':base64.b64encode(original.body).decode()}
        else:value={'type':type(original).__name__}
        raw=g.canonical({'scope':SCOPE,'stage':stage,'kind':kind,'value':value})
        require(len(raw)<=524288 and len(self.originals)<=256)
        path=self.root/(str(len(self.originals))+'.json')
        fd=os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
        with os.fdopen(fd,'wb') as out:out.write(raw)

class InertGit:
    def __init__(self,tamper=False):self.calls=[];self.tamper=tamper;self.blob=None;self.ref=None
    def request(self,method,path,body):
        self.calls.append((method,path,body))
        status=201 if method=='POST' else 200
        if path=='':value={'id':n.REPO_ID,'full_name':n.REPO}
        elif method=='POST' and path=='/git/blobs':
            self.raw=base64.b64decode(body['content']);self.blob=g.git_oid('blob',self.raw);value={'sha':self.blob}
        elif method=='POST' and path=='/git/trees':
            self.tree=g.git_oid('tree',b'100644 '+g.PATH.encode()+b'\0'+bytes.fromhex(self.blob));value={'sha':self.tree}
        elif method=='POST' and path=='/git/commits':
            self.commit='94'*20;self.commit_body=body;value={'sha':self.commit}
        elif method=='POST' and path=='/git/refs':
            self.ref=body['ref'];value={'ref':self.ref,'object':{'type':'commit','sha':self.commit}}
        elif path.startswith('/git/ref/'):
            value={'ref':self.ref,'object':{'type':'commit','sha':self.commit}}
        elif path.startswith('/git/commits/'):
            value={'sha':self.commit,'message':self.commit_body['message'],'tree':{'sha':self.tree},'parents':[{'sha':SOURCE}]}
        elif path.startswith('/git/trees/'):
            value={'sha':self.tree,'truncated':False,'tree':[{'path':g.PATH,'mode':'100644','type':'blob','sha':self.blob,'size':len(self.raw)}]}
        elif path.startswith('/git/blobs/'):
            raw=self.raw if not self.tamper else self.raw+b' '
            value={'sha':self.blob,'size':len(raw),'encoding':'base64','content':base64.b64encode(raw).decode()}
        else:raise AssertionError('UNEXPECTED_INERT_PATH94')
        return g.Reply(status,g.canonical(value))

class InertHTTP:
    def __init__(self,clock,mode='OK'):
        self.clock,self.mode=clock,mode;self.posts=0;self.closes=0;self.timeout=None;self.sock=None
        self.partial=http.client.IncompleteRead(b'PRIVATE-PARTIAL94',100)
        self.cleanup=RuntimeError('PRIVATE-CLEANUP94')
    def request(self,method,path,body,headers):
        require(method=='POST' and headers['Authorization']=='Bearer '+KEY_SENTINEL)
        self.posts+=1
    def getresponse(self):return self
    @property
    def status(self):return 200
    def getheader(self,name):return 'application/json' if name=='Content-Type' else None
    def read(self,limit):
        if self.mode=='PARTIAL':raise self.partial
        if self.mode=='LATE':self.clock.now=11.0
        analysis={'status':'unknown','summary':RAW_SENTINEL,'hypotheses':[],
                  'missing_evidence':['NEW94 causal evidence absent.'],'remediation':[]}
        return g.canonical({'model':r.MODEL,'choices':[{'finish_reason':'stop','message':{'content':json.dumps(analysis)}}],
                            'usage':{'prompt_tokens':31,'completion_tokens':19,'total_tokens':50}})
    def close(self):
        self.closes+=1
        if self.mode=='PARTIAL':raise self.cleanup

def fixture(root,label,mode='OK',tamper=False):
    clock=Clock();capture=InertCapture(root/label);window=n.Window94(10,capture,clock=clock,wall=2000000000)
    client=InertGit(tamper);http=InertHTTP(clock,mode)
    spec={'source':SOURCE,'invocation':'SYNTHETIC94-'+label,'nonce':hashlib.sha256(('NEW94-'+label).encode()).hexdigest(),
          'deadline_utc':2000000010}
    def factory(host,timeout):
        require(host=='api.tokenfactory.nebius.com');return http
    return window,client,capture,http,factory,spec

def scenario_default(root,raw,input_raw):
    class NoEnvironment(dict):
        lookups=0
        def __getitem__(self,key):
            self.lookups+=1;raise AssertionError('ENV_LOOKUP_BEFORE_ADMISSION94')
        def get(self,*args):
            self.lookups+=1;raise AssertionError('ENV_LOOKUP_BEFORE_ADMISSION94')
    old=os.environ;guard=NoEnvironment();os.environ=guard
    try:
        require(n.load_context94() is None and n._CURRENT is None and not n._ENTRY_ATTEMPTED)
        refuses(r.OneRequest);refuses(g.OneBackend)
        refuses(lambda:n.NativeHTTP94(SimpleNamespace(verified=True,grant={'usd':'5'})))
        require(n._CURRENT is None and guard.lookups==0)
    finally:os.environ=old
    cfg=n.ReviewedConfiguration94(SOURCE,SOURCE,'NEW94-INERT-AUD','NEW94-INERT-SUB','unused.invalid','/unused','2','/payload','/input')
    claims={'iss':n.ISSUER,'aud':cfg.audience,'sub':cfg.subject,'repository':n.REPO,'repository_id':str(n.REPO_ID),
            'repository_owner_id':str(n.OWNER_ID),'actor_id':str(n.OWNER_ID),'event_name':'workflow_dispatch',
            'ref':cfg.ref,'sha':SOURCE,'workflow_sha':SOURCE,'workflow_ref':n.REPO+'/'+n.WORKFLOW+'@'+cfg.ref,
            'run_attempt':'1','runner_environment':'github-hosted','run_id':'94001','check_run_id':'94002',
            'iat':2000000000,'nbf':2000000000,'exp':2000000300,'jti':'NEW94-INERT-JTI'}
    require(n.validate_claims94(claims,cfg,2000000001)['run_id']==94001)
    refuses(lambda:n.validate_claims94(dict(claims,sha='0'*40),cfg,2000000001))
    run={'id':94001,'run_attempt':1,'head_sha':SOURCE,'event':'workflow_dispatch','path':n.WORKFLOW,
         'actor':{'id':n.OWNER_ID},'repository':{'id':n.REPO_ID}}
    job={'id':94999,'run_id':94001,'head_sha':SOURCE,'name':n.JOB,'status':'in_progress',
         'check_run_url':'https://api.github.com/repos/'+n.REPO+'/check-runs/94002','labels':['ubuntu-24.04']}
    require(n.validate_job94(run,{'total_count':1,'jobs':[job]},claims,cfg)['check_run_id']==94002)
    require(n._CURRENT is None)

def scenario_record(root,raw,input_raw):
    w,gc,cap,http,factory,spec=fixture(root,'record94')
    public=n.inert_pipeline94(raw,input_raw,w,gc,cap,factory,spec)
    record=json.loads(gc.raw)
    require(record['operation']==n.OPERATION and record['source_commit']==SOURCE and record['nonce']==spec['nonce'])
    require(record['actual_numeric_grant'] is None and record['classification']=='INERT_TESTDATA_NOT_NATIVE_AUTHORITY94')
    require(gc.ref.startswith(n.NAMESPACE) and len([x for x in gc.calls if x[0]=='POST'])==4)
    require(http.posts==1 and http.closes==1 and public['verified'] is True)
    require(RAW_SENTINEL not in json.dumps(public) and KEY_SENTINEL not in json.dumps(public))
    w,gc,cap,http,factory,spec=fixture(root,'tamper94',tamper=True)
    refuses(lambda:n.inert_pipeline94(raw,input_raw,w,gc,cap,factory,spec))
    require(http.posts==0 and w.primary is not None and n._CURRENT is None)

def scenario_window(root,raw,input_raw):
    w,gc,cap,http,factory,spec=fixture(root,'partial94',mode='PARTIAL')
    boundary=n._SharedHTTP94(w,cap,factory)
    refuses(lambda:boundary.exchange(raw,KEY_SENTINEL,g.PROJECT))
    primary=w.primary
    require(primary is not None and http.posts==1 and http.closes==1)
    require(any(v is http.partial for _,_,v in cap.originals))
    require(any(v==b'PRIVATE-PARTIAL94' for _,_,v in cap.originals))
    require(any(v is http.cleanup for _,_,v in cap.originals))
    require(any(v is http.cleanup for _,v in w.secondary) or len(w.secondary)>0)
    refuses(lambda:boundary.exchange(raw,KEY_SENTINEL,g.PROJECT))
    require(w.primary==primary and http.posts==1)
    w,gc,cap,http,factory,spec=fixture(root,'late94',mode='LATE')
    refuses(lambda:n._SharedHTTP94(w,cap,factory).exchange(raw,KEY_SENTINEL,g.PROJECT))
    require(w.primary is not None and http.closes==1 and any(type(v) is bytes for _,_,v in cap.originals))

def scenario_projection(root,raw,input_raw):
    w,gc,cap,http,factory,spec=fixture(root,'input94')
    refuses(lambda:n.inert_pipeline94(raw,input_raw+b' ',w,gc,cap,factory,spec))
    require(gc.calls==[] and http.posts==0)
    require(n._CURRENT is None and all(x is None for x in
        (n.REVIEWED_CONFIGURATION,n.PROTECTED_ADMISSION,n.PROTECTED_CAPTURE,n.QUALIFIED_DEPENDENCY_CLOSURE)))
    candidate=Path(n.__file__).parent/'workflow_candidates/traceharbor-one94.yml.disabled'
    require('    if: false\n' in candidate.read_text() and '.github' not in str(candidate.relative_to(Path(n.__file__).parent)))

def main():
    root=Path(sys.argv[1]);raw=Path(sys.argv[2]).read_bytes();input_raw=Path(sys.argv[3]).read_bytes()
    def audit(event,args):
        if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen','os.system'):
            raise AssertionError('REAL_EFFECT_DENIED94')
    sys.addaudithook(audit)
    names=[]
    for fn in (scenario_default,scenario_record,scenario_window,scenario_projection):
        fn(root,raw,input_raw);names.append(fn.__name__)
    print(json.dumps({'scope':SCOPE,'group':'NEW94','scenarios':names,'passed':4,'native_authority':False,
                      'model_calls':0,'real_git_claims':0,'spend_usd':'0'}))

if __name__=='__main__':main()
