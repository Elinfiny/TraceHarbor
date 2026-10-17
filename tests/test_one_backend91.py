"""NEW92 only: REST reply compatibility, never an earlier consumed group."""
import base64
import copy
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import sys
import traceback
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import one_backend91 as b

def deny(event,args):
    if event in ('socket.connect','socket.connect_ex','socket.getaddrinfo','subprocess.Popen','os.system'):
        raise RuntimeError('HOST_NETWORK_AND_CHILD_DENIED92')
sys.addaudithook(deny)
BASE=Path(sys.argv[1]).resolve()
CAPTURES=[]
FIRST_ORIGINAL=[]
ENTRY_KEYS={'path','mode','type','sha','size','url'}
EVIDENCE={'observed_tree':'a3edd56e4afee71ca17ff97f373fd572a50d64cc',
          'observed_blob':'5ea4060aeee3f4469f3166c851abd499532892e1','observed_size':13060,
          'trees_docs':'https://docs.github.com/en/rest/git/trees',
          'blobs_docs':'https://docs.github.com/en/rest/git/blobs',
          'blob_envelope':'Explicit fixture/client contract; not an observed raw vendor blob reply'}

class Clock:
    def __init__(self):self.now=1000.0
    def __call__(self):return self.now

def plan(label):
    return b.SyntheticPlan('92001',b.SOURCE_PARENT,b.digest(('new-rest92-'+label).encode()),
        'a6c905b718e0770f87efc1058f1961beaee6de172c7ab31c74fdbf82774a9b95',
        'f57813253ce6f59318354e62d4bee7c6dd133ed33cfc245438d1d5a604cf43a1',
        '1e24c7eb6e3afadfbd767730c39390a9b43a97ba87ef6237407f0982056cecc4',1100)

def reply(status,value):return b.Reply(status,b.canonical(value),b.JSON_MEDIA,True)

class FakeREST92:
    def __init__(self,clock,mode='rest_lf'):
        self.clock,self.mode=clock,mode
        self.calls,self.blobs,self.trees,self.commits,self.refs=[],{},{},{},{}
        self.failure=OSError('private92-created-ref-response-lost')
        self.original_tree=None
    @staticmethod
    def url(kind,sha):return 'https://api.github.com/repos/'+b.REPO+'/git/'+kind+'/'+sha
    def request(self,method,path,body):
        self.calls.append((method,path,copy.deepcopy(body)))
        if method=='GET' and path=='':return reply(200,{'id':b.REPO_ID,'full_name':b.REPO})
        if method=='POST' and path=='/git/blobs':
            raw=base64.b64decode(body['content'],validate=True);sha=b.git_oid('blob',raw);self.blobs[sha]=raw
            return reply(201,{'sha':sha,'url':self.url('blobs',sha)})
        if method=='POST' and path=='/git/trees':
            e=body['tree'][0];sha=b.git_oid('tree',b'100644 '+e['path'].encode()+b'\0'+bytes.fromhex(e['sha']))
            self.trees[sha]=copy.deepcopy(body['tree']);return reply(201,{'sha':sha,'url':self.url('trees',sha)})
        if method=='POST' and path=='/git/commits':
            sha=hashlib.sha1(b.canonical(body)).hexdigest()
            self.commits[sha]={'sha':sha,'tree':{'sha':body['tree']},'parents':[{'sha':s} for s in body['parents']],'message':body['message']}
            return reply(201,{'sha':sha,'url':self.url('commits',sha)})
        if method=='POST' and path=='/git/refs':
            assert body['ref'].startswith(b.NAMESPACE)
            if body['ref'] in self.refs:return reply(409,{'message':'Already exists'})
            self.refs[body['ref']]=body['sha']
            if self.mode=='ambiguous_capture':raise self.failure
            return reply(201,{'ref':body['ref'],'object':{'type':'commit','sha':body['sha']}})
        if method=='GET' and path.startswith('/git/ref/'):
            ref='refs/'+path[len('/git/ref/'):];v={'ref':ref,'object':{'type':'commit','sha':self.refs[ref]}}
            if self.mode=='foreign_ref':v['object']['sha']='f'*40
            return reply(200,v)
        if method=='GET' and path.startswith('/git/commits/'):
            v=copy.deepcopy(self.commits[path.rsplit('/',1)[-1]])
            if self.mode=='foreign_parent':v['parents']=[{'sha':'e'*40}]
            return reply(200,v)
        if method=='GET' and path.startswith('/git/trees/'):
            sha=path.rsplit('/',1)[-1];entries=copy.deepcopy(self.trees[sha])
            for e in entries:
                e['size']=len(self.blobs[e['sha']]);e['url']=self.url('blobs',e['sha']);assert set(e)==ENTRY_KEYS
            v={'sha':sha,'url':self.url('trees',sha),'tree':entries,'truncated':False}
            if self.mode=='tree_size':entries[0]['size']+=1
            if self.mode=='tree_bool_size':entries[0]['size']=True
            if self.mode=='tree_mode':entries[0]['mode']='120000'
            if self.mode=='extra_entry':entries.append(copy.deepcopy(entries[0]))
            if self.mode=='tree_truncated':v['truncated']=True
            if self.mode=='foreign_url':entries[0]['url']='https://example.invalid/foreign'
            if self.mode=='semantic_tree':entries[0]['admitted']=True
            if self.mode=='late':self.clock.now=1100.0
            self.original_tree=reply(200,v)
            if self.mode=='parse_error':self.original_tree=b.Reply(200,b'{"tree":',b.JSON_MEDIA,True)
            if self.mode=='partial':self.original_tree=replace(self.original_tree,eof=False)
            return self.original_tree
        if method=='GET' and path.startswith('/git/blobs/'):
            sha=path.rsplit('/',1)[-1];raw=self.blobs[sha]
            if self.mode in ('raw','raw_partial','raw_suffix'):
                if self.mode=='raw_suffix':raw+=b'!'
                return b.Reply(200,raw,b.RAW_MEDIA,self.mode!='raw_partial')
            encoded=base64.b64encode(raw).decode();sep='\r\n' if self.mode=='base64_crlf' else '\n'
            content=sep.join(encoded[i:i+60] for i in range(0,len(encoded),60))+sep
            v={'sha':sha,'encoding':'base64','content':content,'size':len(raw),'url':self.url('blobs',sha),'node_id':'synthetic92-node-metadata'}
            if self.mode=='blob_mismatch':v['content']=base64.b64encode(raw[:-1]+b'!').decode()
            if self.mode=='bad_base64':v['content']=encoded+'!'
            if self.mode=='bad_size':v['size']+=1
            if self.mode=='bad_blob_url':v['url']='https://api.github.com/repos/foreign/repo/git/blobs/'+sha
            if self.mode=='bad_node':v['node_id']=False
            if self.mode=='bad_wrapping':v['content']=encoded[:40]+'\n'+encoded[40:]
            if self.mode=='semantic_blob':v['grant']=True
            if self.mode=='bad_utf8':return b.Reply(200,b'\xff',b.JSON_MEDIA,True)
            if self.mode=='duplicate_json':return b.Reply(200,b'{"sha":"'+sha.encode()+b'",'+b.canonical(v)[1:],b.JSON_MEDIA,True)
            if self.mode=='bad_media':return replace(reply(200,v),media_type='text/plain')
            return reply(200,v)
        raise AssertionError('UNEXPECTED_FAKE_REST92_CALL')

def setup(label,mode='rest_lf'):
    parent=BASE/label;parent.mkdir(mode=0o700);capture=b.PrivateOriginals(parent/'capture');CAPTURES.append(capture)
    clock=Clock();client=FakeREST92(clock,mode)
    return b.synthetic_backend(plan(label),client,capture,clock),client,capture,clock
def refused(call):
    try:call()
    except b.Refuse as error:return str(error)
    raise AssertionError('EXPECTED_NEW92_REFUSAL')
def creates(client):return sum(m=='POST' and path=='/git/refs' for m,path,_ in client.calls)
def no_retry(backend,client,code):
    before=len(client.calls);assert refused(backend.reserve)==code and len(client.calls)==before and creates(client)==1

def scenario1():
    backend,client,capture,clock=setup('new92-rest-positive');receipt=backend.reserve();record=backend.verify(receipt)
    assert record==b.record_for(plan('new92-rest-positive')) and record['state']=='ATTEMPTING_CONSUMED'
    assert client.blobs[receipt['blob']]==b.canonical(record) and creates(client)==1
    original=client.original_tree
    assert any(obj is original for stage,kind,obj in capture.originals if stage=='READ_TREE' and kind=='RETURN')
    assert set(b.strict_json(original.body)['tree'][0])==ENTRY_KEYS
    stages=[stage for stage,kind,obj in capture.originals]
    assert stages.index('READ_TREE')<stages.index('PARSE_READ_TREE')<stages.index('TREE_PROJECT')
    assert record['native_grant'] is None and receipt['source_commit']==b.SOURCE_PARENT
    assert receipt['record_sha256']==b.digest(b.canonical(record))
    return {'metadata_fields':sorted(ENTRY_KEYS),'record_bytes':len(b.canonical(record)),'record_sha256':receipt['record_sha256'],
            'original_before_projection':True,'full_bytes_git_ids':True,'create_ref':1,'evidence':EVIDENCE}
def scenario2():
    outcomes=[]
    for mode in ('tree_size','tree_bool_size','tree_mode','extra_entry','foreign_parent','foreign_ref','blob_mismatch','tree_truncated','foreign_url','semantic_tree'):
        backend,client,capture,clock=setup('new92-semantic-'+mode,mode);code=refused(backend.reserve)
        assert creates(client)==1 and backend.first_primary and not backend._verified;no_retry(backend,client,code)
        outcomes.append({'fixture':mode,'primary':code,'no_second_create':True})
    return {'semantic_refusals':outcomes}
def scenario3():
    outcomes=[]
    for mode in ('parse_error','partial','late','capture','ambiguous_capture'):
        backend,client,capture,clock=setup('new92-failure-'+mode,mode);retain=capture.retain
        secondary=[RuntimeError('private92-secondary-1'),RuntimeError('private92-secondary-2')];raised=[]
        def fault(stage,kind,original):
            retain(stage,kind,original)
            fail=(mode=='capture' and stage=='READ_TREE') or (mode=='ambiguous_capture' and stage in ('CREATE_REF','PUBLIC_BOUNDARY_reserve'))
            if fail and len(raised)<2:
                error=secondary[len(raised)];raised.append(error);raise error
        if mode in ('capture','ambiguous_capture'):capture.retain=fault
        code=refused(backend.reserve);assert creates(client)==1 and not backend._verified
        if mode=='parse_error':assert any(isinstance(obj,json.JSONDecodeError) for _,kind,obj in capture.originals if kind=='EXCEPTION')
        if mode=='ambiguous_capture':
            assert len(client.refs)==1 and code=='CALL_UNKNOWN91_CREATE_REF'
            assert any(obj is client.failure for _,kind,obj in capture.originals if kind=='EXCEPTION')
            assert [error for _,error in backend.secondary]==secondary
        if mode=='capture':
            assert any(obj is client.original_tree for _,_,obj in capture.originals)
            assert [error for _,error in backend.secondary]==secondary[:1]
        first=backend.first_primary;no_retry(backend,client,code);assert backend.first_primary==first
        outcomes.append({'fixture':mode,'primary':code,'ordered_secondaries':len(backend.secondary),'real_original_retained':True,'create_ref':1})
    return {'failures':outcomes}
def scenario4():
    loader=b.native_binding;defaults=[]
    try:
        for witness in (None,True,{'admitted':True},plan('new92-not-authority'),lambda:True):
            b.native_binding=lambda witness=witness:witness;defaults.append(refused(b.OneBackend))
    finally:b.native_binding=loader
    assert defaults[0]=='NO_AUTHENTIC_NATIVE_BINDING91' and defaults[1:]==['NATIVE_CLIENT_AND_ISSUER_NOT_BOUND91']*4
    positives=[]
    for mode in ('raw','base64_crlf'):
        backend,client,capture,clock=setup('new92-positive-'+mode,mode);receipt=backend.reserve()
        assert backend.verify(receipt)==b.record_for(backend.plan);positives.append(mode)
    outcomes=[]
    for mode in ('bad_base64','bad_size','bad_blob_url','bad_node','bad_wrapping','semantic_blob','bad_utf8','duplicate_json','bad_media','raw_partial','raw_suffix'):
        backend,client,capture,clock=setup('new92-wire-'+mode,mode);code=refused(backend.reserve);no_retry(backend,client,code)
        outcomes.append({'fixture':mode,'primary':code})
    return {'native_witness_refusals':len(defaults),'credential_lookup':0,'native_binding':None,'transport_positive':positives,'transport_refusals':outcomes}
def main():
    BASE.mkdir(mode=0o700,parents=True,exist_ok=False);guard_checks=0
    for event in ('socket.connect','socket.connect_ex','socket.getaddrinfo','subprocess.Popen','os.system'):
        try:sys.audit(event,())
        except RuntimeError as error:
            assert str(error)=='HOST_NETWORK_AND_CHILD_DENIED92';guard_checks+=1
    assert guard_checks==5;cases=[]
    for number,case in enumerate((scenario1,scenario2,scenario3,scenario4),1):
        try:cases.append({'scenario':number,'status':'PASS','receipt':case()})
        except Exception as original:
            FIRST_ORIGINAL.append(original);raw=''.join(traceback.format_exception(type(original),original,original.__traceback__)).encode()
            fd=os.open(BASE/'first-abort-original.txt',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
            with os.fdopen(fd,'wb') as out:out.write(raw);out.flush();os.fsync(out.fileno())
            print(json.dumps({'group':'REST_SHAPE92_NEW_ONLY','scenario':number,'status':'ABORT','previous':cases,'remaining':'NOT_RUN','original_sha256':b.digest(raw)}));return 1
    manifest=[]
    for capture in CAPTURES:
        for item in capture.metadata:
            path=capture.directory/item['file'];raw=path.read_bytes();assert len(raw)==item['bytes'] and b.digest(raw)==item['sha256']
            assert path.stat().st_mode&0o777==0o600;manifest.append({'path':str(path.relative_to(BASE)),**item})
    raw=b.canonical(manifest);fd=os.open(BASE/'capsule-manifest.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'wb') as out:out.write(raw);out.flush();os.fsync(out.fileno())
    print(json.dumps({'group':'REST_SHAPE92_NEW_ONLY','status':'PASS','scenarios':cases,'guard_checks':guard_checks,'native_effects':0,
                      'capsules':len(manifest),'capsule_manifest_sha256':b.digest(raw)}));return 0
if __name__=='__main__':raise SystemExit(main())
