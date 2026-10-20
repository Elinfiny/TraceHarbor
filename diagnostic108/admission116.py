"""Authored116 phased host producer. Native provenance and contract fixtures are distinct types.

Native source-only implementation: external solewriter Library CAS plus GitHub
create-only admission/consumed refs are read back here. No runner-side privilege,
lease, vendor attestation or financial grant is invented. Nothing runs at import.
"""
import os,pathlib,json,hashlib,time,re,stat,base64,importlib.util
_NATIVE=object();_CONTRACT=object();_INPUT=object();_PREPARED=object()
OWNER=273768139;REPO=1391430317;WRITER='e839e90d6a61ceb21ab32dd8c78f27ab63a346e8e5ec0c4d12a1356db4fe3436'
INGRESS_SHA='b1510c25cc3763fcc54d014824581ce3d5c8bf4401de88959e85f3c5132bdc2e'
#136 exact source-bound create contract, no authority at import.
_gs136=importlib.util.spec_from_file_location('trace136_runner_git',pathlib.Path(__file__).resolve().parent/'git_dispatch136.py')
git136=importlib.util.module_from_spec(_gs136);_gs136.loader.exec_module(git136)

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

# 117 shared integration primitives. These data checks never establish native
# authority; NativeConsumedProof is allocated only by the live producer below.
from dataclasses import dataclass
import datetime
PHASES117={'checkout':20,'run_capture':10,'admit':150,'recipient_crypto':20,
 'recipient_io':5,'recipient_upload':60,'main_capture':10,'main_admit':45,
 'prequalification':200,'receive':70,'consumed':45,'mounts':10,
 'worker':170,'cleanup':10,'proof':15}
MAIN_REMAINDER117=575
AFTER_PREQUAL117=320
RECIPIENT_REMAINDER120=680
HOST_BEGIN_REMAINDER120=610

@dataclass(frozen=True)
class ParentClock:
    run_id: str
    started_utc: float
    hard_end_utc: float
    once_expires_utc: float
    coordinator_cutoff_utc: float
    observed_utc: float
    observed_mono: float
    end_mono: float
    wall: object
    mono: object
    @classmethod
    def from_run(cls,run,once_expires,cutoff,wall=time.time,mono=time.monotonic):
        now=wall();tick=mono()
        started=datetime.datetime.fromisoformat(run['run_started_at'].replace('Z','+00:00')).timestamp()
        if started>now or type(once_expires) is not int or type(cutoff) is not int or not now<once_expires<=now+900:raise ValueError('Frozen parent roots')
        end=min(started+900,once_expires,cutoff)
        if end<=now:raise TimeoutError('Expired immutable parent')
        return cls(str(run['id']),started,started+900,once_expires,cutoff,now,tick,tick+end-now,wall,mono)
    @property
    def end_utc(self):return min(self.hard_end_utc,self.once_expires_utc,self.coordinator_cutoff_utc)
    def require(self,seconds=0):
        # Both clocks constrain; wall rollback cannot extend monotonic authority.
        if min(self.end_mono-self.mono(),self.end_utc-self.wall())<seconds:raise TimeoutError('Whole parent reserve')
    def phase(self,maximum,reserve):
        self.require(maximum+reserve)
        return min(self.end_mono-reserve,self.mono()+maximum)
    def check(self,deadline,reserve=0):
        self.require(reserve)
        if self.mono()>=deadline:raise TimeoutError('Immutable phase deadline')
    def descriptor(self):
        return {'schema':'TRACE117_PARENT_CLOCK','run_id':self.run_id,'run_started_at_utc':self.started_utc,'workflow_hard_end_utc':self.hard_end_utc,'once_expires_utc':self.once_expires_utc,'coordinator_cutoff_utc':self.coordinator_cutoff_utc,'end_utc':self.end_utc,'job_limit_s':900}

class LateProviderRead(TimeoutError):
    pass

def phase_read(api,path,clock,deadline,save,missing=False):
    clock.check(deadline);before={'utc':clock.wall(),'mono':clock.mono()}
    try:
        value=api(path,deadline=deadline,missing=missing)
    except BaseException as exc:
        save({'path':path,'before':before,'after':{'utc':clock.wall(),'mono':clock.mono()},'value':None,'error':type(exc).__name__,'unknown':True})
        raise
    # Original response and times are immutable before any post-return guard.
    observation={'path':path,'before':before,'after':{'utc':clock.wall(),'mono':clock.mono()},'value':value,'error':None}
    save(observation)
    try:clock.check(deadline)
    except TimeoutError as exc:raise LateProviderRead('Late response UNKNOWN; no downstream effect') from exc
    return value

def validate_external(d,phase,b,pins,clock,custody=None,admit=None,reserve=195):
    verify_once_intent(d,b,pins)
    fixed=dict(b,schema='TRACE116_EXTERNAL_ONCE_V1',phase=phase,original_writer=WRITER,own_library_file_id='libfile_3ee8270f03d8819188e1de1f75c3d824',attempt=1,role='OFFLINE_COUNTER_ONLY',request_bytes=4935,lock_sha256='fcea30197a1bf1c0eaa99314dcbf26a152935ba4535c1544b97f2f5a62f2515a',model_calls=0,spend=0)
    if any(d.get(k)!=v for k,v in fixed.items()) or type(d.get('own_cas_version')) is not int or d['own_cas_version']<412 or not re.fullmatch('[a-f0-9]{64}',d.get('own_pinned_readback_sha256','')):raise ValueError('Original external writer/CAS/source')
    if d.get('expires_utc')!=clock.once_expires_utc or d.get('parent_clock')!=clock.descriptor():raise ValueError('Fixed parent clock preimage')
    if d.get('inputs')!={n:{'bytes':p[0],'sha256':p[1]} for n,p in pins.items()}:raise ValueError('Six input preimages')
    if phase=='consumed' and (custody is None or d.get('recipient_context')!=custody.context or d.get('ciphertext_receipt')!=custody.receipt or d.get('admit_sha256')!=sha(can(admit))):raise ValueError('Consumed custody/source preimage')
    clock.require(reserve if phase=='consumed' else 0)
    return d

def read_external(api,strict,phase,b,pins,clock,deadline,save,custody=None,admit=None,wait_for_admit=False,pause=None):
    prefix='/repos/Elinfiny/TraceHarbor/';ref='heads/traceharbor-counter116-'+phase+'-'+b['once_receipt_sha256']
    read=lambda path,missing=False:phase_read(api,prefix+path,clock,deadline,save,missing)
    # Only initial admit may observe actual404/None. All observations and times
    # are saved by phase_read before guards; fixed initial90s/parent never reset.
    if wait_for_admit and phase!='admit':raise ValueError('No consumed-ref readiness retry')
    pause=time.sleep if pause is None else pause
    # Fixed initial availability window: nine scheduled intervals, five
    # immutable GETs and complete validation retain an explicit15s reserve.
    started=clock.mono();validation_reserve=15 if wait_for_admit else 2;available_end=deadline-validation_reserve
    if wait_for_admit and available_end<=started:raise TimeoutError('No initial availability/validation reserve')
    observations=0
    while True:
        clock.check(deadline)
        if wait_for_admit and observations:
            target=started+(available_end-started)*observations/9
            while clock.mono()<target:
                delay=min(target-clock.mono(),deadline-clock.mono()-validation_reserve)
                if delay<=0:raise TimeoutError('Fixed availability window exhausted')
                before_pause=clock.mono();pause(delay)
                if clock.mono()<=before_pause:raise TimeoutError('Availability pause made no progress')
                clock.check(deadline)
        if deadline-clock.mono()<validation_reserve:raise TimeoutError('Five immutable reads/fullvalidation reserve')
        actual=read('git/ref/'+ref,missing=wait_for_admit and phase=='admit');observations+=1
        if actual is not None:break
        if not wait_for_admit or phase!='admit' or observations>=10:raise TimeoutError('Initial admit bounded10observations exhausted')
    if actual is None:raise ValueError('Consumed/admit immutable record absent')
    if actual['ref']!='refs/'+ref or actual['object']['type']!='commit':raise ValueError('Immutable original once ref')
    commit=read('commits/'+actual['object']['sha'])
    if commit['author']['id']!=OWNER or commit['committer']['id']!=OWNER or [p['sha'] for p in commit['parents']]!=[b['source_sha']]:raise ValueError('Owner source attribution')
    tree=read('git/trees/'+commit['commit']['tree']['sha']);base=read('git/commits/'+b['source_sha']);before=read('git/trees/'+base['tree']['sha'])
    entries=lambda t:{v['path']:{k:v[k] for k in ('mode','type','sha')} for v in t['tree']}
    left,right=entries(before),entries(tree);name='counter116-'+phase+'.json'
    if tree.get('truncated') or before.get('truncated') or name in left or set(right)!=set(left)|{name} or any(left[k]!=right[k] for k in left) or right[name]['type']!='blob' or right[name]['mode']!='100644':raise ValueError('Once exact tree delta')
    blob=read('git/blobs/'+right[name]['sha']);raw=base64.b64decode(''.join(blob['content'].split()),validate=True)
    if len(raw)>16384 or blob['size']!=len(raw) or hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=right[name]['sha']:raise ValueError('Once whole blob')
    d=validate_external(strict(raw),phase,b,pins,clock,custody,admit)
    return d,{'commit':actual['object']['sha'],'tree':commit['commit']['tree']['sha'],'descriptor_sha256':sha(raw),'received_utc':clock.wall(),'received_mono':clock.mono(),'phase_deadline_mono':deadline}

@dataclass(frozen=True)
class ContractConsumedProof:
    producer: object
    descriptor: bytes
    provenance: bytes
    custody: object
    binding: bytes
    clock: object

class NativeConsumedProof:
    __slots__=('producer','descriptor','provenance','custody','binding','clock','seal')
    def __init__(self,key,producer,descriptor,provenance,custody):
        if key is not _NATIVE or type(producer) is not NativeProducer:raise TypeError('Only actual same producer may attest consumption')
        self.seal=key;self.producer=producer;self.descriptor=can(descriptor);self.provenance=can(provenance);self.custody=custody;self.binding=can(producer.caller.binding);self.clock=producer.clock
    def __setattr__(self,name,value):
        if hasattr(self,name):raise AttributeError('Immutable original consumed proof')
        object.__setattr__(self,name,value)

def local_release(proof,producer,custody,binding,clock,marker,native=False):
    wanted=NativeConsumedProof if native else ContractConsumedProof
    if type(proof) is not wanted or proof.producer is not producer or proof.custody is not custody or proof.clock is not clock or proof.binding!=can(producer.caller.binding):raise TypeError('Original SAME producer consumption proof')
    if native and proof.seal is not _NATIVE:raise TypeError('No JSON/native seal')
    d=json.loads(proof.descriptor);validate_external(d,'consumed',producer.caller.binding,producer.pins,clock,custody,producer.caller.receipt,reserve=0)
    # Current worker has its own fixed170s end. Require full counter25s now.
    clock.require(25)
    if not clock.wall()+25<binding['absolute_deadline_utc']<=clock.end_utc:raise TimeoutError('Current worker full counter remainder')
    exclusive(marker,can({'binding':binding,'external_consumed_sha256':sha(proof.descriptor),'status':'CONSUMED_NO_COUNTER_PROVED'}))
    clock.require(25)
    return {'external_durable_consumption_verified':True,'native_release':native}

def error117(exc):
    return {'exception_class':type(exc).__name__,'errno':exc.errno if isinstance(exc,OSError) else None}

class CleanupFailure(RuntimeError):
    def __init__(self,receipt):self.cleanup_receipt=receipt;super().__init__('INTAKE_CLEANUP_UNKNOWN_NO_RETRY')

class OwnedIntake:
    # Exact finite locators; no recursive enumeration/removal, no unknown adoption.
    def __init__(self,root,binding,pins,create=False,remove=os.unlink,close=os.close,read=os.read):
        self.root=pathlib.Path(root);self.binding=dict(binding);self.pins=dict(pins);self.remove=remove;self.close=close;self.read=read;self.primary=None
        if create:self.root.mkdir(mode=0o700)
        s=self.root.lstat()
        if not stat.S_ISDIR(s.st_mode) or s.st_uid!=os.getuid() or s.st_mode&0o077 or self.root.is_symlink():raise ValueError('Owned fresh intake root')
        self.anchor=(s.st_dev,s.st_ino);self.attempts={};self.created={}
        record={'schema':'TRACE117_OWNED_INTAKE','binding':self.binding,'dev':s.st_dev,'ino':s.st_ino,'uid':s.st_uid,'paths':sorted(self.secret_paths())}
        if create:exclusive(self.root/'owner117.json',can(record))
        else:
            got=self.read_small('owner117.json')
            if json.loads(got)!=record:raise ValueError('No adoption of old/unbound intake')
        journal=self.root/'cleanup117.jsonl'
        if journal.exists():
            for line in self.read_small('cleanup117.jsonl',32768).splitlines():
                row=json.loads(line);self.attempts[row['path']]=row
        created=self.root/'created117.jsonl'
        if created.exists():
            for line in self.read_small('created117.jsonl',32768).splitlines():
                row=json.loads(line);self.created[row['path']]=row
    def secret_paths(self):return {'fresh-recipient/recipient.key','quarantine/UNAUTHENTICATED.private',*('runtime-inputs/'+n for n in self.pins)}
    def capture_created(self,names):
        # Only call immediately after this producer's fresh scoped creation.
        # Existing paths cannot be rebound to a different inode on restart.
        for name in names:
            try:s=(self.root/name).lstat()
            except FileNotFoundError:continue
            if (not stat.S_ISREG(s.st_mode) and not stat.S_ISDIR(s.st_mode)) or s.st_uid!=os.getuid():raise ValueError('Created intake path type')
            row={'path':name,'dev':s.st_dev,'ino':s.st_ino,'directory':stat.S_ISDIR(s.st_mode)}
            if name in self.created:
                if self.created[name]!=row:raise ValueError('Created intake locator drift')
                continue
            fd=os.open(self.root/'created117.jsonl',os.O_WRONLY|os.O_CREAT|os.O_APPEND|os.O_NOFOLLOW,0o600)
            with os.fdopen(fd,'ab') as f:f.write(can(row)+b'\n');f.flush();os.fsync(f.fileno())
            self.created[name]=row
    def parent_fd(self,path):
        parts=pathlib.PurePosixPath(path).parts
        if not parts or any(p in ('..','.') for p in parts) or pathlib.PurePosixPath(path).is_absolute():raise ValueError('Exact relative cleanup locator')
        fd=os.open(self.root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);opened=[fd];traversed=[]
        try:
            s=os.fstat(fd)
            if (s.st_dev,s.st_ino)!=self.anchor:raise ValueError('Intake root drift')
            for name in parts[:-1]:
                fd=os.open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);opened.append(fd);traversed.append(name)
                st=os.fstat(fd);anchor=self.created.get('/'.join(traversed))
                if st.st_uid!=os.getuid() or anchor is None or (st.st_dev,st.st_ino)!=(anchor['dev'],anchor['ino']):raise ValueError('Anchored intake descendant drift')
            return fd,parts[-1],opened
        except BaseException as primary:
            cleanup=[]
            for f in reversed(opened):
                try:self.close(f)
                except BaseException as exc:cleanup.append(error117(exc))
            if isinstance(primary,FileNotFoundError) and not cleanup:raise
            raise CleanupFailure({'primary':error117(primary),'cleanup':cleanup,'unknown':True,'retry':False}) from primary
    def read_small(self,name,cap=8192):
        fd,leaf,opened=self.parent_fd(name);f=None;primary=None;cleanup=[];raw=b''
        try:
            f=os.open(leaf,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd);s=os.fstat(f)
            if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1 or s.st_size>cap:raise ValueError('Owned ledger type')
            while len(raw)<=cap:
                b=self.read(f,min(65536,cap+1-len(raw)))
                if not b:break
                raw+=b
            if len(raw)>cap or len(raw)!=s.st_size:raise ValueError('Owned ledger read')
        except BaseException as exc:primary=exc
        for n in ([f] if f is not None else [])+list(reversed(opened)):
            if n is not None:
                try:self.close(n)
                except BaseException as exc:cleanup.append(error117(exc))
        if primary or cleanup:raise CleanupFailure({'primary':error117(primary) if primary else None,'cleanup':cleanup,'unknown':True,'retry':False}) from primary
        return raw
    def log(self,row):
        fd=os.open(self.root/'cleanup117.jsonl',os.O_WRONLY|os.O_APPEND|os.O_CREAT|os.O_NOFOLLOW,0o600)
        with os.fdopen(fd,'ab') as f:f.write(can(row)+b'\n');f.flush();os.fsync(f.fileno())
        self.attempts[row['path']]=row
    def cleanup(self,stage,primary=None):
        result={'stage':stage,'primary':error117(primary) if primary else None,'cleanup':[],'paths':[],'retry':False,'secure_erase':False}
        selected=self.secret_paths() if stage!='post_receive' else {'fresh-recipient/recipient.key','quarantine/UNAUTHENTICATED.private'}
        for name in sorted(selected):
            previous=self.attempts.get(name)
            if previous:
                result['paths'].append(previous)
                if previous['status'] in ('ATTEMPTING','UNKNOWN'):result['cleanup'].append({'path':name,'status':'UNKNOWN_NO_RETRY'})
                continue
            fd=None;opened=[];row={'path':name,'stage':stage,'status':'UNKNOWN','remove_attempts':0}
            try:
                fd,leaf,opened=self.parent_fd(name)
                try:s=os.stat(leaf,dir_fd=fd,follow_symlinks=False)
                except FileNotFoundError:s=None
                if s is None:row['status']='OBSERVED_ABSENT'
                elif not stat.S_ISREG(s.st_mode) or s.st_nlink!=1 or s.st_uid!=os.getuid():raise ValueError('Refuse unknown/symlink intake descendant')
                elif name not in self.created or (s.st_dev,s.st_ino)!=(self.created[name]['dev'],self.created[name]['ino']):raise ValueError('No adoption of unanchored intake file')
                elif name=='quarantine/UNAUTHENTICATED.private':
                    # Existing105 decrypt owns its one finally-unlink attempt.
                    # Presence after return/failure is UNKNOWN, never retry it.
                    row['status']='UNKNOWN';row['delegated_to_105_finally']=True
                else:
                    row.update(status='ATTEMPTING',dev=s.st_dev,ino=s.st_ino,remove_attempts=1);self.log(dict(row))
                    self.remove(leaf,dir_fd=fd);row['status']='REMOVED'
                    try:os.stat(leaf,dir_fd=fd,follow_symlinks=False)
                    except FileNotFoundError:pass
                    else:row['status']='UNKNOWN'
            except FileNotFoundError:row['status']='OBSERVED_ABSENT'
            except BaseException as exc:
                row['error']=error117(exc);row['status']='UNKNOWN'
                if hasattr(exc,'cleanup_receipt'):row['original_fd_custody']=exc.cleanup_receipt
            finally:
                for f in reversed(opened):
                    try:self.close(f)
                    except BaseException as exc:
                        failure={'path':name,'close':error117(exc)}
                        result['cleanup'].append(failure)
                        row.setdefault('close_cleanup',[]).append(failure)
                        row['status']='UNKNOWN'
            try:self.log(row)
            except BaseException as exc:result['cleanup'].append({'path':name,'journal':error117(exc)})
            result['paths'].append(row)
            if row['status']=='UNKNOWN':result['cleanup'].append({'path':name,'status':'UNKNOWN_NO_RETRY'})
        result['unknown']=bool(result['cleanup']);result['status']='UNKNOWN' if result['unknown'] else 'PASS'
        return result

def run_with_cleanup(owner,stage,operation):
    primary=None;value=None
    try:value=operation()
    except BaseException as exc:primary=exc
    receipt=owner.cleanup(stage,primary)
    if primary is not None:
        primary.intake_cleanup=receipt;raise primary
    if receipt['unknown']:raise CleanupFailure(receipt)
    return value

def owned_creation(owner,names,operation):
    primary=None;value=None
    try:value=operation()
    except BaseException as exc:primary=exc
    try:owner.capture_created(names)
    except BaseException as exc:
        if primary is None:raise
        primary.intake_creation_cleanup=error117(exc)
    if primary is not None:raise primary
    return value


class NativeProducer:
    __slots__=('caller','root','pins','expected','_g','used','clock','owner','consumption','observations','last_provenance','main_end','observation_root')
    def __init__(self,key,caller,root,pins,g):
        if key is not _NATIVE or type(caller) is not NativeCaller or caller.seal is not _NATIVE:raise TypeError('Actual native caller required')
        self.caller=caller;self.root=root;self.pins=pins;self.expected=dict(caller.binding);self._g=g;self.used=False

    @classmethod
    def capture(cls,g,x,repo,manifest,private,pins,initializing=False):
        e=os.environ
        expected={'GITHUB_REPOSITORY':'Elinfiny/TraceHarbor','GITHUB_REPOSITORY_ID':str(REPO),'GITHUB_ACTOR_ID':str(OWNER),'GITHUB_EVENT_NAME':git136.event136(os.environ),'GITHUB_RUN_ATTEMPT':'1','GITHUB_SHA':x.source_sha,'GITHUB_WORKFLOW_SHA':x.source_sha}
        if any(e.get(k)!=v for k,v in expected.items()) or not re.fullmatch('[0-9]+',e.get('GITHUB_RUN_ID','')):raise ValueError('Actual native caller context')
        if os.environ.get('GITHUB_EVENT_NAME')=='create':
            vv=git136.env_values136(dict(os.environ))
            if (vv['source_sha'],vv['manifest_sha256'],vv['once_receipt_sha256'],int(vv['once_expires_utc']),int(vv['coordinator_cutoff_utc']))!=(x.source_sha,x.manifest_sha,x.once_receipt_sha,x.once_expires_utc,x.coordinator_cutoff_utc):raise ValueError('Exact source create inputs/expiry')
        if type(x.once_expires_utc) is not int or type(x.coordinator_cutoff_utc) is not int:raise ValueError('Frozen dispatch clock inputs required')
        source=repo/'offline103/ingress.py'
        if sha(g.regular(source,131072))!=INGRESS_SHA:raise ValueError('Reviewed105 ingress source')
        ingress=load(source,'trace117_reviewed_ingress')
        # Bootstrap has one fixed deadline and original capture, before runstart
        # is known. No protected key/intake effect occurs on this bootstrap.
        now=time.time();tick=time.monotonic();deadline=min(tick+10,tick+min(x.once_expires_utc,x.coordinator_cutoff_utc)-now)
        observations=[]
        class Bootstrap:
            wall=staticmethod(time.time);mono=staticmethod(time.monotonic)
            def check(self,end):
                if time.monotonic()>=end or time.time()>=min(x.once_expires_utc,x.coordinator_cutoff_utc):raise TimeoutError('Bootstrap deadline')
        def save_initial(value):
            observations.append(value)
            target=pathlib.Path(e['RUNNER_TEMP'])/('trace117-capture-'+x.once_receipt_sha+('-init' if initializing else '-main')+'.json')
            exclusive(target,can(value))
        run=phase_read(ingress.api,'/repos/Elinfiny/TraceHarbor/actions/runs/'+e['GITHUB_RUN_ID'],Bootstrap(),deadline,save_initial)
        dispatch_binding136=git136.binding136(git136.args136(git136.env_values136(dict(e)))) if e.get('GITHUB_EVENT_NAME')=='create' else None
        if run['id']!=int(e['GITHUB_RUN_ID']) or run['run_attempt']!=1 or run['head_sha']!=x.source_sha or not git136.run_event136(run,dispatch_binding136) or run['actor']['id']!=OWNER or run['repository']['id']!=REPO or run['status']!='in_progress':raise ValueError('Current provider run readback')
        clock=ParentClock.from_run(run,x.once_expires_utc,x.coordinator_cutoff_utc)
        clock.require(865 if initializing else 565)
        binding={'source_sha':x.source_sha,'manifest_sha256':x.manifest_sha,'once_receipt_sha256':x.once_receipt_sha,'run_id':e['GITHUB_RUN_ID'],'request_sha256':manifest['request_sha256']}
        caller=NativeCaller(_NATIVE,run,binding,ingress,repo)
        root=pathlib.Path(e['RUNNER_TEMP'])/('traceharbor-counter117-intake-'+x.once_receipt_sha)
        obj=cls(_NATIVE,caller,root,pins,g);obj.clock=clock;obj.owner=None;obj.consumption=None;obj.observations=observations
        # Public provider metadata readiness precedes fresh key/private intake.
        obj.observation_root=pathlib.Path(e['RUNNER_TEMP'])/('trace118-public-admit-'+x.once_receipt_sha+('-init' if initializing else '-main'))
        obj.observation_root.mkdir(mode=0o700)
        try:
            receipt=obj.provider_once('admit',maximum=150 if initializing else 45,reserve=685 if initializing else 520,admit_wait=initializing)
            caller.receipt=receipt;caller.expires=receipt['expires_utc']
            obj.owner=OwnedIntake(root,binding,pins,create=initializing)
            if not initializing:obj.main_end=min(clock.end_mono,tick+720)
            return obj
        except BaseException as exc:
            exc.intake_cleanup=obj.owner.cleanup('capture_failure',exc) if obj.owner is not None else {'primary':error117(exc),'cleanup':[],'status':'NO_PRIVATE_INTAKE_CREATED','retry':False}
            raise
    def provider_once(self,phase,custody=None,maximum=45,reserve=195,admit_wait=False):
        deadline=self.clock.phase(maximum,reserve)
        def save(value):
            self.observations.append(value)
            exclusive(self.observation_root/('provider117-'+phase+'-'+str(len(self.observations))+'.json'),can(value))
        d,provenance=read_external(self.caller.ingress.api,self.caller.ingress.strict,phase,self.caller.binding,self.pins,self.clock,deadline,save,custody,self.caller.receipt,wait_for_admit=admit_wait)
        self.last_provenance=provenance
        return d
    def initialize_recipient(self):
        def operation():
            i=self.caller.ingress;b=self.caller.binding
            deadline=self.clock.phase(25,RECIPIENT_REMAINDER120)
            c={'repository':'Elinfiny/TraceHarbor','repository_id':REPO,'actor_id':OWNER,'run_id':int(b['run_id']),'attempt':1,'source_sha':b['source_sha'],'nonce':os.urandom(16).hex(),'expires_utc':int(self.clock.end_utc)}
            self.clock.check(deadline,RECIPIENT_REMAINDER120)
            c,pem=owned_creation(self.owner,['fresh-recipient','fresh-recipient/recipient.key','fresh-recipient/recipient.pem'],lambda:i.recipient(self.root/'fresh-recipient',c))
            self.clock.check(deadline,RECIPIENT_REMAINDER120)
            i.put(self.root/'recipient-public.json',i.can({'context':c,'certificate_pem':pem.decode('ascii')}))
            i.put(self.root/'fresh-binding.json',i.can({'binding':b,'context':c,'admit_sha256':sha(can(self.caller.receipt)),'parent_clock':self.clock.descriptor()}))
            self.clock.check(deadline,RECIPIENT_REMAINDER120)
            return self.root/'recipient-public.json'
        try:return operation()
        except BaseException as exc:exc.intake_cleanup=self.owner.cleanup('init_failure',exc);raise
    def receive_inputs(self,manifest):
        def operation():
            i=self.caller.ingress;b=self.caller.binding;deadline=self.clock.phase(70,250)
            fresh=i.strict(self.owner.read_small('fresh-binding.json'));c=fresh['context']
            if fresh['binding']!=b or fresh['admit_sha256']!=sha(can(self.caller.receipt)) or fresh['parent_clock']!=self.clock.descriptor() or c['source_sha']!=b['source_sha'] or c['run_id']!=int(b['run_id']) or c['attempt']!=1 or c['expires_utc']!=int(self.clock.end_utc):raise ValueError('Fresh current117 recipient and parent')
            i.context(c);self.clock.check(deadline,250)
            # Reviewed105 read loop uses its immutable45s deadline; crypto max20s.
            # Postreturn guard below rejects a late successful existing105 result.
            data,receipt=owned_creation(self.owner,['quarantine','quarantine/encrypted.cms','quarantine/UNAUTHENTICATED.private'],lambda:i.receive(c,self.root/'fresh-recipient/recipient.key',self.root/'fresh-recipient/recipient.pem',[{'name':n,'bytes':p[0],'sha256':p[1]} for n,p in self.pins.items() if not n.startswith('tokenizer/')],self.root/'quarantine',wait_seconds=45))
            self.clock.check(deadline,250)
            for n,pin in self.pins.items():
                if n.startswith('tokenizer/'):data[n]=self._g.regular(pathlib.Path(os.environ['RUNNER_TEMP'])/'traceharbor-offline103/vendor'/n,pin[0])
            custody=owned_creation(self.owner,['runtime-inputs','runtime-inputs/tokenizer',*('runtime-inputs/'+n for n in self.pins)],lambda:stage_copies(self,self.root/'runtime-inputs',data,self.pins,receipt,c))
            self.clock.check(deadline,250)
            return custody
        return run_with_cleanup(self.owner,'post_receive',operation)
    def pre_worker_consume(self,custody):
        if self.consumption is not None or self.used:raise ValueError('Consume only once before worker')
        self.clock.require(250)
        d=self.provider_once('consumed',custody,45,205)
        self.consumption=NativeConsumedProof(_NATIVE,self,d,self.last_provenance,custody)
        # Durable consume already happened externally. Any subsequent error is
        # CONSUMED_NO_COUNTER_PROVED, including cleanup/mount/worker failure.
        exclusive(self.root/'consumed117-proof.json',can({'status':'CONSUMED_NO_COUNTER_PROVED','descriptor_sha256':sha(can(d)),'provenance':self.last_provenance}))
        self.clock.require(195)
        return self.consumption
    def cleanup(self,stage,primary=None):return self.owner.cleanup(stage,primary)

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
        if self.used:raise ValueError('Already consumed release')
        self.used=True
        # Absolutely no API in ready->GO. Only original opaque proof and local
        # fixed-context checks plus O_EXCL/fsync; an error never refunds once.
        receipt=local_release(self.consumption,self,cap.prepared.custody,binding,self.clock,self.root/'release-consumed.json',native=True)
        cap.consumed=True
        return receipt

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



class ExternalCoordinator117:
    """Callable source for the SAME solewriter host, never the runner.

    transport is the host's supported tool bridge (not a worker, token or new
    principal). Its call/verified_readback/cas_checkpoint methods must already
    enforce current Owner authority and exact native provider guards. This
    module cannot grant private release/dispatch. Actual117 transport calls=0.
    """
    def __init__(self,transport,save,clock,source_sha,base_tree):
        self.transport=transport;self.save=save;self.clock=clock;self.source=source_sha;self.base_tree=base_tree;self.attempted=set();self.phase_end=clock.end_mono;self.counts={'GitGET':0,'Gitwrites':0,'ownCAS':0,'dispatch':0}
    def call(self,key,tool,args,write=False,reserve=0):
        if key in self.attempted:raise ValueError('No retry of attempted/UNKNOWN coordinator operation')
        self.clock.check(self.phase_end,reserve+10);self.attempted.add(key)
        self.transport.bind_phase(self.phase_end)
        before={'utc':self.clock.wall(),'mono':self.clock.mono()}
        if write:
            # Existing105 transport policy: one originalwriter expected-version
            # intent CAS and pinned readback before EACH immutable Git write.
            reservation=self.transport.reserve_operation(key,tool,args,self.source,self.clock.end_utc)
            self.save({'key':key+'-reservation-original','original':reservation});self.counts['ownCAS']+=1
            self.clock.check(self.phase_end,reserve+10)
        value=self.transport.call(tool,args)
        self.save({'key':key,'tool':tool,'args_sha256':sha(can(args)),'original':value,'before':before,'after':{'utc':self.clock.wall(),'mono':self.clock.mono()}})
        # Response is retained before guard, including successful late mutation.
        self.clock.check(self.phase_end,reserve)
        self.counts['Gitwrites' if write else 'GitGET']+=1
        return value
    def create_once_ref(self,phase,descriptor,reserve):
        if phase not in ('admit','consumed'):raise ValueError('Fixed original once phases')
        name='counter116-'+phase+'.json';raw=can(descriptor)
        if len(raw)>16384 or descriptor['source_sha']!=self.source:raise ValueError('Exact bounded once descriptor')
        # The driver consumes actual tool-return SHAs, never guessed object IDs.
        b=self.call(phase+'-blob','github_create_blob',{'repository_full_name':'Elinfiny/TraceHarbor','content':raw.decode(),'encoding':'utf-8'},True,reserve)
        t=self.call(phase+'-tree','github_create_tree',{'repository_full_name':'Elinfiny/TraceHarbor','base_tree_sha':self.base_tree,'tree_elements':[{'path':name,'mode':'100644','type':'blob','sha':b['sha']}]},True,reserve)
        c=self.call(phase+'-commit','github_create_commit',{'repository_full_name':'Elinfiny/TraceHarbor','parent_sha':self.source,'tree_sha':t['sha'],'message':'Exact counter117 '+phase+' once [skip ci]'},True,reserve)
        ref='traceharbor-counter116-'+phase+'-'+descriptor['once_receipt_sha256']
        self.call(phase+'-create-only','github_create_ref',{'repository_full_name':'Elinfiny/TraceHarbor','branch_name':ref,'sha':c['sha']},True,reserve)
        # Exact whole commit/tree/blob/ref/Owner attribution readback is mandatory
        # in the host adapter, matching read_external, before any dependent effect.
        original=self.transport.verified_readback(ref,c['sha'],t['sha'],name,raw,self.clock.end_utc)
        self.save({'key':phase+'-whole-readback','original':original})
        self.clock.check(self.phase_end,reserve);return original
    def stage(self,phase,descriptor,current_own_version,custody=None):
        if phase not in ('admit','consumed'):raise ValueError('Exact phase')
        reserve=685 if phase=='admit' else 330
        self.phase_end=self.clock.phase(135 if phase=='admit' else 110,reserve)
        self.transport.bind_phase(self.phase_end)
        # CAS reservation/readback precedes immutable consumed-ref publication.
        # A timeout is UNKNOWN, and the original reservation is never refunded.
        receipt=self.transport.cas_checkpoint(current_own_version,{'phase':phase,'source_sha':self.source,'descriptor_sha256':sha(can(descriptor)),'parent_clock':self.clock.descriptor(),'custody':custody})
        self.save({'key':phase+'-own-CAS-original','original':receipt});self.counts['ownCAS']+=1
        rb=self.transport.pinned_checkpoint_readback(receipt)
        self.save({'key':phase+'-own-pinned-readback','original':rb})
        self.clock.check(self.phase_end,reserve)
        if rb['version']!=receipt['version'] or rb['sha256']!=receipt['sha256']:raise ValueError('Exact originalwriter CAS readback')
        d=dict(descriptor,own_cas_version=rb['version'],own_pinned_readback_sha256=rb['sha256'])
        if phase=='consumed' and (not custody or d['recipient_context']!=custody['context'] or d['ciphertext_receipt']!=custody['receipt']):raise ValueError('External actual ciphertext binding')
        return self.create_once_ref(phase,d,reserve)
    def deliver_and_consume(self,ingress,run,files,pins,private_out,admit,current_own_version):
        """Concrete prospective lane while runner performs accepted prequal.

        Solewriter host adapter supplies the authenticated artifact bytes and
        original metadata, not the worker. This is a required actual adapter,
        never claimed available from a public Git fetch or invented live ACK.
        Private arguments and trace stay inside the exact admitted host scope.
        """
        self.clock.require(HOST_BEGIN_REMAINDER120)
        artifact_end=self.clock.phase(60,550)
        self.transport.bind_phase(artifact_end)
        original=self.transport.authenticated_artifact_zip(run['id'],'traceharbor-recipient104-'+str(run['id'])+'-1',artifact_end,8192)
        self.save({'key':'recipient-authenticated-original','original':original['receipt']})
        self.clock.check(artifact_end,550)
        raw=original['zip_bytes'];artifact=original['artifact']
        if len(raw)>8192 or sha(raw)!=original['zip_sha256']:raise ValueError('Whole current artifact custody')
        import zipfile,io
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            names=archive.namelist()
            if names!=['recipient-public.json'] or archive.getinfo(names[0]).file_size>8192:raise ValueError('Exact public recipient archive')
            public=ingress.strict(archive.read(names[0]))
        c=public['context']
        if c['source_sha']!=self.source or c['expires_utc']!=int(self.clock.end_utc) or c['run_id']!=run['id'] or c['attempt']!=1:raise ValueError('Same actual run parent context')
        trace=[]
        # Reviewed105 source performs all exact Owner/artifact/digest/crypto checks.
        try:plan=ingress.prepare_from_artifact(public,run,artifact,sha(raw),files,pins,private_out,self.base_tree,trace)
        finally:self.save({'key':'encrypt105-original-private','original':trace})
        self.clock.check(artifact_end,550)
        # Encryption's two20s OpenSSL maxima are included in aggregate60s.
        # 4 originalwriter CAS/readbacks +4 writes +6 whole readbacks must fit
        # the next immutable110s aggregate; late success becomes UNKNOWN.
        delivery_end=self.clock.phase(110,440);self.phase_end=delivery_end
        results={}
        mapping=[('github_create_blob',{'repository_full_name':'Elinfiny/TraceHarbor','content':plan['operations'][0]['body']['content'],'encoding':'base64'}),('github_create_tree',None),('github_create_commit',None),('github_create_ref',None)]
        for index,(tool,args) in enumerate(mapping):
            self.clock.check(delivery_end,440)
            if index==1:args={'repository_full_name':'Elinfiny/TraceHarbor','base_tree_sha':self.base_tree,'tree_elements':[{'path':plan['path'],'mode':'100644','type':'blob','sha':results[0]['sha']}]}
            if index==2:args={'repository_full_name':'Elinfiny/TraceHarbor','parent_sha':self.source,'tree_sha':results[1]['sha'],'message':'Exact fresh117 encrypted104 delivery [skip ci]'}
            if index==3:args={'repository_full_name':'Elinfiny/TraceHarbor','branch_name':plan['ref'].removeprefix('refs/heads/'),'sha':results[2]['sha']}
            results[index]=self.call('encrypted-'+str(index),tool,args,True,440)
            self.clock.check(delivery_end,440)
        rb=self.transport.verified_ciphertext_readback(plan,results,self.clock.end_utc)
        self.save({'key':'ciphertext-whole-readback-original','original':rb});self.clock.check(delivery_end,440)
        receipt={'ciphertext_commit':results[2]['sha'],'ciphertext_sha256':plan['ciphertext_sha256'],'ref':plan['ref']}
        consumed=dict(admit,phase='consumed',recipient_context=c,ciphertext_receipt=receipt,admit_sha256=sha(can(admit)))
        consume_end=self.clock.phase(110,330)
        value=self.stage('consumed',consumed,self.transport.current_checkpoint_version,{'context':c,'receipt':receipt})
        self.clock.check(consume_end,330)
        return value
    @staticmethod
    def inactive_call_order():
        return [
          'Exact independent source/budget/private custody admission; originalwriter once CAS+pinned fullbyte readback before dispatch',
          'Actual supported dispatch ONCE; preserve response; read actual run/source/actor/attempt/run_started_at under frozen onceexpiry/cutoff',
          'Build ParentClock from same actual run; stage(admit) CAS/readback -> blob/tree/source-parent commit/create-only admit ref -> whole readback within initial host135s / runner150s',
          'Authenticated current recipient artifact by actualrun/attempt/Owner/source; whole context/certificate hash and parent clock readback; no old105key',
          'Existing reviewed105 encrypt with exact3privatepins and current recipient; private crypto originals retained; blob/tree/source-parent commit/create-only encrypted104 ref; whole ciphertext readback',
          'stage(consumed) originalwriter CAS + pinned readback -> immutable consumed descriptor bound to ciphertext/context/admit -> create-only ref + whole readback BEFORE worker; no refund on later failure',
          'NativeProducer.receive_inputs -> pre_worker_consume(read_external six fixed-deadline reads) -> NativeConsumedProof SAME object -> complete actual mounts/current native qualification',
          'worker actual sixinput UID65532 intent -> local SAME proof/clock/O_EXCL/fsync -> Counter_GO within original5s workerwait, zero API there',
          'One private stdout-mode count in future separately admitted context only -> scoped once cleanup -> SAFE projection -> exact terminal/readback; no model/spend authority']


def bind_host118(bridge,private_root,config,save,current_actual_run):
    """SAME solewriter holder. JSON/run observations do not become native caps.

    The installed code-mode dispatcher enforces exact admitted operation frames;
    current118 qualification runs READONLY and invokes no private/native stage.
    """
    path=pathlib.Path(__file__).with_name('host_transport118.py')
    if sha(path.read_bytes())!=config['host_source_sha256']:raise ValueError('Exact hostsource pin')
    module=load(path,'trace118_host_transport')
    transport=module.HostTransport(bridge,private_root,config)
    clock=ParentClock.from_run(current_actual_run,config['once_expires_utc'],config['coordinator_cutoff_utc'])
    coordinator=ExternalCoordinator117(transport,save,clock,config['source_sha'],config['source_tree'])
    return coordinator,transport
