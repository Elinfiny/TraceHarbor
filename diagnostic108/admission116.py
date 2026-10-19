"""Authored116 phased host producer. Native provenance and contract fixtures are distinct types.

Native source-only implementation: external solewriter Library CAS plus GitHub
create-only admission/consumed refs are read back here. No runner-side privilege,
lease, vendor attestation or financial grant is invented. Nothing runs at import.
"""
import os,pathlib,json,hashlib,time,re,stat,base64,importlib.util
_NATIVE=object();_CONTRACT=object();_INPUT=object();_PREPARED=object()
OWNER=273768139;REPO=1391430317;WRITER='e839e90d6a61ceb21ab32dd8c78f27ab63a346e8e5ec0c4d12a1356db4fe3436'
INGRESS_SHA='811119109f538ea90d8e0262eb6feeba43884506d14b8a9f1ef8fca45c795840'
def sha(b):return hashlib.sha256(b).hexdigest()
def can(d):return json.dumps(d,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def verify_once_intent(descriptor,binding,pins):
    """Pure integrity check, never a capability or grant without native provenance."""
    core=descriptor.get('once_intent')
    wanted={'schema':'TRACE116_ONCE_INTENT_V1','original_writer':WRITER,'source_sha':binding['source_sha'],'manifest_sha256':binding['manifest_sha256'],'request_sha256':binding['request_sha256'],'request_bytes':4935,'lock_sha256':'fcea30197a1bf1c0eaa99314dcbf26a152935ba4535c1544b97f2f5a62f2515a','inputs':{n:{'bytes':p[0],'sha256':p[1]} for n,p in pins.items()},'role':'OFFLINE_COUNTER_ONLY','max_counter_invocations':1,'model_calls':0,'spend':0}
    if type(core) is not dict or set(core)!=set(wanted)|{'expires_utc','nonce'} or any(core[k]!=v for k,v in wanted.items()) or type(core['expires_utc']) is not int or core['expires_utc']!=descriptor.get('expires_utc') or type(core['nonce']) is not str or not re.fullmatch('[0-9a-f]{32}',core['nonce']):raise ValueError('Exact externally reserved once intent')
    if sha(can(core))!=binding['once_receipt_sha256']:raise ValueError('External once intent digest mismatch')
    return True
def exclusive(path,raw,mode=0o600):
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,mode)
    with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
def load(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class NativeCaller:
    __slots__=('run','binding','ingress','repo','receipt','expires','seal')
    def __init__(self,key,run,binding,ingress,repo):
        if key is not _NATIVE:raise TypeError('Actual native capture only')
        self.seal=key;self.run=run;self.binding=dict(binding);self.ingress=ingress;self.repo=repo;self.receipt=None;self.expires=0
class ContractCaller:
    __slots__=('binding','seal')
    def __init__(self,binding):self.binding=dict(binding);self.seal=_CONTRACT
class InputCustody:
    __slots__=('producer','paths','pins','receipt','context','seal')
    def __init__(self,key,producer,paths,pins,receipt,context):
        if key is not _INPUT:raise TypeError('Custody producer only')
        self.seal=key;self.producer=producer;self.paths=paths;self.pins=pins;self.receipt=receipt;self.context=context
class PreparedMounts:
    __slots__=('producer','custody','evidence','mounts','native_q','seal')
    def __init__(self,key,producer,custody,evidence,mounts,native_q):
        if key is not _PREPARED:raise TypeError('Current mount proof only')
        self.seal=key;self.producer=producer;self.custody=custody;self.evidence=evidence;self.mounts=mounts;self.native_q=native_q
class NativeCounterAuthority:
    __slots__=('producer','prepared','binding','evidence','native_q','consumed','seal')
    def __init__(self,key,producer,prepared,binding):
        if key is not _NATIVE or type(producer) is not NativeProducer:raise TypeError('Native factory only')
        self.seal=key;self.producer=producer;self.prepared=prepared;self.binding=dict(binding);self.evidence=prepared.evidence;self.native_q=prepared.native_q;self.consumed=False
class ContractCounterAuthority:
    __slots__=('producer','prepared','binding','evidence','native_q','consumed','seal')
    def __init__(self,key,producer,prepared,binding):
        if key is not _CONTRACT or type(producer) is not ContractProducer:raise TypeError('Contract factory only')
        self.seal=key;self.producer=producer;self.prepared=prepared;self.binding=dict(binding);self.evidence=prepared.evidence;self.native_q=prepared.native_q;self.consumed=False
def native_boundary(cap,producer,evidence,q,binding):
    # Deliberately reject synthetic types/JSON before any provider/counter effect.
    if type(cap) is not NativeCounterAuthority or type(producer) is not NativeProducer:raise TypeError('Synthetic/data is not native authority')
    if cap.seal is not _NATIVE or cap.producer is not producer or cap.consumed is not False or cap.evidence is not evidence or cap.native_q is not q or cap.binding!=binding:raise ValueError('Current native capability identity')
    if time.time()>=binding['absolute_deadline_utc']:raise TimeoutError('Expired native capability')
    return cap
def stage_copies(producer,root,data,pins,receipt,context):
    if set(data)!=set(pins):raise ValueError('Fixed six-member set')
    root.mkdir(mode=0o700)
    paths={}
    for name,pin in sorted(pins.items()):
        b=data[name]
        if (len(b),sha(b))!=tuple(pin):raise ValueError('Intake pin')
        # Only new runtime copies get0444; original105/Library inputs untouched.
        dest=root/name;dest.parent.mkdir(mode=0o755,parents=True,exist_ok=True)
        exclusive(dest,b,0o600);os.chmod(dest,0o444)
        s=dest.stat()
        if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1 or s.st_mode&0o222:raise ValueError('Closed read-only runtime copy')
        paths[name]=dest
    os.chmod(root,0o755)
    return InputCustody(_INPUT,producer,paths,dict(pins),receipt,context)
def bind_mounts(producer,g,custody,evidence,bindings,q):
    if type(custody) is not InputCustody or custody.seal is not _INPUT or custody.producer is not producer:raise TypeError('Current input custody required')
    if not isinstance(evidence,g.HostEvidence) or evidence.key is not g._HOST_KEY or evidence.source!=producer.caller.binding['source_sha']:raise ValueError('Actual current host mount proof')
    wanted={d:{'path':str(pathlib.Path(p).absolute()),'readonly':ro} for d,(p,ro) in bindings.items()}
    if evidence.mounts!=wanted:raise ValueError('Exact current complete mount set')
    return PreparedMounts(_PREPARED,producer,custody,evidence,wanted,q)
class NativeProducer:
    __slots__=('caller','root','pins','expected','_g','used')
    def __init__(self,key,caller,root,pins,g):
        if key is not _NATIVE or type(caller) is not NativeCaller or caller.seal is not _NATIVE:raise TypeError('Actual native caller required')
        self.caller=caller;self.root=root;self.pins=pins;self.expected=dict(caller.binding);self._g=g;self.used=False
    @classmethod
    def capture(cls,g,x,repo,manifest,private,pins,initializing=False):
        # g.validate has already checked real gitHEAD/native environment/manifest.
        e=os.environ
        expected={'GITHUB_REPOSITORY':'Elinfiny/TraceHarbor','GITHUB_REPOSITORY_ID':str(REPO),'GITHUB_ACTOR_ID':str(OWNER),'GITHUB_EVENT_NAME':'workflow_dispatch','GITHUB_RUN_ATTEMPT':'1','GITHUB_SHA':x.source_sha,'GITHUB_WORKFLOW_SHA':x.source_sha}
        if any(e.get(k)!=v for k,v in expected.items()) or not re.fullmatch('[0-9]+',e.get('GITHUB_RUN_ID','')):raise ValueError('Actual native caller context')
        source=repo/'offline103/ingress.py'
        if sha(g.regular(source,131072))!=INGRESS_SHA:raise ValueError('Reviewed105 ingress source')
        ingress=load(source,'trace116_reviewed_ingress')
        run=ingress.api('/repos/Elinfiny/TraceHarbor/actions/runs/'+e['GITHUB_RUN_ID'])
        if run['id']!=int(e['GITHUB_RUN_ID']) or run['run_attempt']!=1 or run['head_sha']!=x.source_sha or run['event']!='workflow_dispatch' or run['actor']['id']!=OWNER or run['repository']['id']!=REPO or run['status']!='in_progress':raise ValueError('Current provider run readback')
        binding={'source_sha':x.source_sha,'manifest_sha256':x.manifest_sha,'once_receipt_sha256':x.once_receipt_sha,'run_id':e['GITHUB_RUN_ID'],'request_sha256':manifest['request_sha256']}
        caller=NativeCaller(_NATIVE,run,binding,ingress,repo)
        root=pathlib.Path(e['RUNNER_TEMP'])/('traceharbor-counter116-intake-'+x.once_receipt_sha)
        if initializing:root.mkdir(mode=0o700)
        s=root.lstat()
        if not stat.S_ISDIR(s.st_mode) or s.st_uid!=os.getuid() or s.st_mode&0o077:raise ValueError('Fresh owned native intake root')
        obj=cls(_NATIVE,caller,root,pins,g)
        receipt=obj.provider_once('admit')
        caller.receipt=receipt;caller.expires=receipt['expires_utc']
        return obj
    def provider_once(self,phase,custody=None):
        b=self.caller.binding;i=self.caller.ingress;prefix='/repos/Elinfiny/TraceHarbor/'
        ref='heads/traceharbor-counter116-'+phase+'-'+b['once_receipt_sha256']
        end=time.monotonic()+(90 if phase=='admit' else 0)
        while True:
            actual=i.api(prefix+'git/ref/'+ref,missing=phase=='admit')
            if actual is not None:break
            if time.monotonic()>=end:raise TimeoutError('Bounded external admission readback window')
            time.sleep(min(10,max(0,end-time.monotonic())))
        if actual['ref']!='refs/'+ref or actual['object']['type']!='commit':raise ValueError('Create-only external once ref')
        commit=i.api(prefix+'commits/'+actual['object']['sha'])
        if commit['author']['id']!=OWNER or commit['committer']['id']!=OWNER or [p['sha'] for p in commit['parents']]!=[b['source_sha']]:raise ValueError('Original Owner source attribution')
        tree=i.api(prefix+'git/trees/'+commit['commit']['tree']['sha']);base=i.api(prefix+'git/commits/'+b['source_sha']);before=i.api(prefix+'git/trees/'+base['tree']['sha'])
        entries=lambda t:{v['path']:{k:v[k] for k in ('mode','type','sha')} for v in t['tree']}
        left,right=entries(before),entries(tree);name='counter116-'+phase+'.json'
        if tree.get('truncated') or before.get('truncated') or name in left or set(right)!=set(left)|{name} or any(left[k]!=right[k] for k in left) or right[name]['type']!='blob' or right[name]['mode']!='100644':raise ValueError('Exact immutable once descriptor delta')
        blob=i.api(prefix+'git/blobs/'+right[name]['sha']);raw=base64.b64decode(blob['content'],validate=False)
        if len(raw)>16384 or blob['size']!=len(raw) or hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=right[name]['sha']:raise ValueError('Once descriptor closure')
        d=i.strict(raw)
        verify_once_intent(d,b,self.pins)
        fixed=dict(b,schema='TRACE116_EXTERNAL_ONCE_V1',phase=phase,original_writer=WRITER,own_library_file_id='libfile_3ee8270f03d8819188e1de1f75c3d824',attempt=1,role='OFFLINE_COUNTER_ONLY',request_bytes=4935,lock_sha256='fcea30197a1bf1c0eaa99314dcbf26a152935ba4535c1544b97f2f5a62f2515a',model_calls=0,spend=0)
        if any(d.get(k)!=v for k,v in fixed.items()) or type(d.get('own_cas_version')) is not int or d['own_cas_version']<408 or not re.fullmatch('[a-f0-9]{64}',d.get('own_pinned_readback_sha256','')) or type(d.get('expires_utc')) is not int or not time.time()<d['expires_utc']<=time.time()+900:raise ValueError('Current external writer/CAS/source/role descriptor')
        if d.get('inputs')!={n:{'bytes':p[0],'sha256':p[1]} for n,p in self.pins.items()}:raise ValueError('Exact six input pins')
        if phase=='consumed':
            if custody is None or d.get('recipient_context')!=custody.context or d.get('ciphertext_receipt')!=custody.receipt or d.get('admit_sha256')!=sha(can(self.caller.receipt)):raise ValueError('Durable consume actual run/intake binding')
        return d
    def initialize_recipient(self):
        # Separate source-pinned workflow init step; no opaque Python state is
        # purported to survive process exit. Main reauthenticates its own caller.
        i=self.caller.ingress;b=self.caller.binding
        c={'repository':'Elinfiny/TraceHarbor','repository_id':REPO,'actor_id':OWNER,'run_id':int(b['run_id']),'attempt':1,'source_sha':b['source_sha'],'nonce':os.urandom(16).hex(),'expires_utc':min(int(time.time())+840,self.caller.expires)}
        if c['expires_utc']-time.time()<300:raise TimeoutError('Whole fresh ingress/runtime reserve')
        c,pem=i.recipient(self.root/'fresh-recipient',c)
        i.put(self.root/'recipient-public.json',i.can({'context':c,'certificate_pem':pem.decode('ascii')}))
        i.put(self.root/'fresh-binding.json',i.can({'binding':b,'context':c,'admit_sha256':sha(can(self.caller.receipt))}))
        return self.root/'recipient-public.json'
    def receive_inputs(self,manifest):
        # Executed only in a separately admitted future native package, NEVER116.
        i=self.caller.ingress;b=self.caller.binding
        fresh=i.strict(i.read(self.root/'fresh-binding.json',8192));c=fresh['context']
        if fresh['binding']!=b or fresh['admit_sha256']!=sha(can(self.caller.receipt)) or c['source_sha']!=b['source_sha'] or c['run_id']!=int(b['run_id']) or c['attempt']!=1:raise ValueError('Fresh current116 recipient, never old105 key')
        i.context(c)
        # Existing public recipient artifact + encrypted104 create-only delivery.
        data,receipt=i.receive(c,self.root/'fresh-recipient/recipient.key',self.root/'fresh-recipient/recipient.pem',[{'name':n,'bytes':p[0],'sha256':p[1]} for n,p in self.pins.items() if not n.startswith('tokenizer/')],self.root/'quarantine',wait_seconds=90)
        for n,pin in self.pins.items():
            if n.startswith('tokenizer/'):
                data[n]=self._g.regular(pathlib.Path(os.environ['RUNNER_TEMP'])/'traceharbor-offline103/vendor'/n,pin[0])
        custody=stage_copies(self,self.root/'runtime-inputs',data,self.pins,receipt,c)
        # Old keys are never adopted. Deletion failure remains a real stop.
        (self.root/'fresh-recipient/recipient.key').unlink()
        return custody
    def bind(self,g,custody,evidence,bindings,q):return bind_mounts(self,g,custody,evidence,bindings,q)
    def issue(self,g,prepared,evidence,q,binding,readability,state):
        if self.used:raise ValueError('Already consumed producer')
        if type(prepared) is not PreparedMounts or prepared.producer is not self or prepared.evidence is not evidence or prepared.native_q is not q or g._QUAL113 is not q:raise ValueError('SAME current mount/native objects required')
        if q.get('binding')!=self.caller.binding or any(q.get(k)!='PASS' for k in ('native','inventory','native_cleanup')) or q.get('diagnostic_admitted') is not True:raise ValueError('Actual current native qualification')
        if state.get('Running') is not True or state.get('OOMKilled') is not False:raise ValueError('Current trusted host running state')
        if readability!={'uid':65532,'inputs':{n:{'bytes':p[0],'sha256':p[1]} for n,p in self.pins.items()},'binding_sha256':sha(can(binding))}:raise ValueError('Actual UID65532 worker reader closure')
        if any(binding.get(k)!=v for k,v in self.caller.binding.items()) or binding['absolute_deadline_utc']>self.caller.expires:raise ValueError('Source/run/request/once/expiry')
        return NativeCounterAuthority(_NATIVE,self,prepared,binding)
    def consume(self,cap,evidence,q,binding):
        native_boundary(cap,self,evidence,q,binding)
        self.used=True
        # External solewriter CAS+create-only consumed ref is the durable effect.
        # Runner verifies it; it does not manufacture an ACK or mutate that ref.
        receipt=self.provider_once('consumed',cap.prepared.custody)
        cap.consumed=True
        exclusive(self.root/'release-consumed.json',can({'binding':binding,'external_consumed_sha256':sha(can(receipt))}))
        return {'external_durable_consumption_verified':True,'native_release':True}
class ContractProducer:
    """Finite contract-test domain. Its types can never satisfy native_boundary."""
    def __init__(self,root,binding,pins):self.root=pathlib.Path(root);self.root.mkdir(mode=0o700);self.caller=ContractCaller(binding);self.pins=dict(pins)
    def prepare(self,data):return stage_copies(self,self.root/'runtime-inputs',data,self.pins,{'domain':'SYNTHETIC_NO_CRYPTO'},{'realm':'CONTRACT'})
    def bind(self,g,custody,evidence,bindings,q):return bind_mounts(self,g,custody,evidence,bindings,q)
    def issue(self,g,prepared,evidence,q,binding,readability,state):
        if prepared.producer is not self or prepared.evidence is not evidence or prepared.native_q is not q or q!={'realm':'SYNTHETIC_NOT_NATIVE'} or state!={'realm':'SYNTHETIC_NOT_NATIVE'} or readability!={'realm':'SYNTHETIC_NOT_NATIVE'} or binding!=self.caller.binding:raise ValueError('Current contract identities')
        return ContractCounterAuthority(_CONTRACT,self,prepared,binding)
    def consume(self,cap,evidence,q,binding):
        if type(cap) is not ContractCounterAuthority or cap.producer is not self or cap.evidence is not evidence or cap.native_q is not q or cap.binding!=binding or cap.consumed:raise ValueError('Contract stale/reused/data refused')
        if time.time()>=binding['absolute_deadline_utc']:raise TimeoutError('Contract expiry')
        cap.consumed=True;exclusive(self.root/'once-consumed.json',can({'domain':'SYNTHETIC_ONLY','binding':binding}));return {'native_release':False,'domain':'SYNTHETIC_ONLY'}
    def release(self,cap,evidence,q,binding,control):
        receipt=self.consume(cap,evidence,q,binding);exclusive(pathlib.Path(control)/'COUNTER_GO116.json',can(receipt));return receipt
