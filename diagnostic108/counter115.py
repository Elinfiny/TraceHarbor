"""SOURCE CANDIDATE116. Phased same-host producer; no vendor imports at module load.

The consumer uses the vendor's existing stdout CLI variant: the proposed /output
file would be denied by cache-only Landlock. Stdout transport is source-accepted116; native execution still requires separate
admission. All raw counter stdout/stderr remain private and are never public streams.
"""
import hashlib,json,os,pathlib,re,stat,time
SCHEMA='COUNTER116_BOUNDING_V1'
MODE='PROTECTED_OFFLINE_COUNTER115'
CAP=65536
ARGV=('/cache/env/bin/python','/vendor/count_request.py','--request','/inputs/request.json')
PRODUCER_KIND="PHASED_NATIVE_PROVIDER_READBACK_AND_DISTINCT_CONTRACT_REALM"
PRIVATE_PINS={
 'count_request.py':(8382,'a3f4a1a37987b2a58f752880fc17ae90c330c4a87b3965a9ce56e77a4bcec23d'),
 'count_chat.py':(9078,'eb792278cd97aab83399d117e023073c3550c12c63f9697aab90e215ed506b63'),
 'served_template.jinja':(11157,'17dc9cd8a6b70ec56bc2b758f9539a113ba789b5b025105234ae3aed78a5f49d')}
TOKENIZER_PINS={
 'tokenizer.json':(17077484,'623c34567aebb18582765289fbe23d901c62704d6518d71866e0e58db892b5b7'),
 'tokenizer_config.json':(177209,'10f93eabcb9b1602fbb991d6308e787ce1df28ee9cd7a1c6d1e8c3f338b957bc'),
 'special_tokens_map.json':(563,'e9435fefd6d838fd9fcbbc44b97a8e3ff322be7f6dfb7e4fd2468586574bb52b')}
VERSIONS={'huggingface-hub':'1.24.0','jinja2':'3.1.6','tokenizers':'0.22.2','transformers':'5.14.1'}
PRIVATE_NAMES=frozenset(('counter.stdout','counter.stderr','counter.terminal.json','counter115.intent.json','counter115.ready','counter115.verified.json','beforecounter115.json','aftercounter115.json'))
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(d):return json.dumps(d,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def strict(raw):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('Duplicate counter JSON')
            out[k]=v
        return out
    if len(raw)>CAP:raise ValueError('Counter cap')
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in ()).throw(ValueError('Nonfinite')))
def validate_binding(value,expected):
    fields={'schema','source_sha','manifest_sha256','once_receipt_sha256','request_sha256','lock_sha256','runtime','run_id','absolute_deadline_utc','release_sha256','transport'}
    if type(value) is not dict or set(value)!=fields:raise ValueError('Counter binding keys')
    if value['schema']!=SCHEMA or value['transport']!='BOUNDED_PRIVATE_STDOUT':raise ValueError('Counter scope')
    for k in ('manifest_sha256','once_receipt_sha256','request_sha256','lock_sha256','release_sha256'):
        if type(value[k]) is not str or not re.fullmatch('[a-f0-9]{64}',value[k]):raise ValueError('Counter digest')
    if type(value['source_sha']) is not str or not re.fullmatch('[a-f0-9]{40}',value['source_sha']):raise ValueError('Counter source')
    if type(value['run_id']) is not str or not value['run_id'].isdigit():raise ValueError('Counter run')
    if type(value['absolute_deadline_utc']) not in (int,float) or not time.time()<value['absolute_deadline_utc']<=time.time()+180:raise ValueError('Counter expiry')
    for k,v in expected.items():
        if k not in fields or value[k]!=v:raise ValueError('Counter binding mismatch')
    return dict(value)

_PRODUCER116 = None
def producer_module(repo):
    global _PRODUCER116
    if _PRODUCER116 is None:
        import importlib.util
        s=importlib.util.spec_from_file_location('same_host_admission116',repo/'diagnostic108/admission116.py')
        m=importlib.util.module_from_spec(s);s.loader.exec_module(m);_PRODUCER116=m
    return _PRODUCER116
def input_pins():return dict(PRIVATE_PINS,**{'tokenizer/'+n:p for n,p in TOKENIZER_PINS.items()})
def prepare_host(g,x,repo,manifest,private,initializing=False):
    p=producer_module(repo)
    producer=p.NativeProducer.capture(g,x,repo,manifest,private,input_pins(),initializing=initializing)
    if initializing:return producer.initialize_recipient()
    return {'producer':producer,'custody':None,'prepared':None,'authority':None,'mounts':{},'expected':{},'binding':None,'released':False,'projected':None}
def complete_intake(g,plan,binding,repo,manifest):
    p=producer_module(repo);custody=plan['producer'].receive_inputs(manifest)
    plan['custody']=custody
    plan['consumption']=plan['producer'].pre_worker_consume(custody)
    for name,path in custody.paths.items():
        dest='/vendor/'+name;plan['mounts'][dest]=(path,True);plan['expected'][dest]=custody.pins[name]
    for name in ('counter115.py','admission116.py'):
        path=repo/'diagnostic108'/name;raw=g.regular(path,262144)
        plan['mounts']['/driver/'+name]=(path,True);plan['expected']['/driver/'+name]=(len(raw),sha(raw))
    return plan
def bind_current_mounts(g,plan,evidence,bindings,q):
    plan['producer'].clock.require(195)
    plan['prepared']=plan['producer'].bind(g,plan['custody'],evidence,bindings,q)
def make_worker_binding(g,plan,binding,manifest,absolute):
    producer=plan['producer']
    if plan['prepared'] is None or producer.caller.expires<absolute:raise ValueError('Current mount/whole expiry required')
    b=dict(binding,schema=SCHEMA,lock_sha256=manifest['lock_sha256'],runtime=manifest['runtime']['immutable_image'],absolute_deadline_utc=absolute,release_sha256=sha(canonical(producer.caller.receipt)),transport='BOUNDED_PRIVATE_STDOUT')
    b=validate_binding(b,binding);plan['binding']=b;return b
def release_if_ready(g,plan,output,control,private,evidence,state):
    if plan['released']:return
    if output.read('counter115.ready',0,optional=True) is None:return
    critical_end=time.monotonic()+5
    raw=output.read('counter115.intent.json',8192)
    if strict(raw)!=plan['binding']:raise ValueError('Exact current intent')
    readability=strict(output.read('counter116.inputs.json',8192))
    producer=plan['producer'];producer.clock.require(25)
    if time.time()+25>=plan['binding']['absolute_deadline_utc']:raise TimeoutError('Final whole worker reserve')
    cap=producer.issue(g,plan['prepared'],evidence,g._QUAL113,plan['binding'],readability,state)
    # Same factory/class and exact evidence identity; no imported old capability.
    producer_module(pathlib.Path(__file__).parent.parent).native_boundary(cap,producer,evidence,g._QUAL113,plan['binding'])
    producer.consume(cap,evidence,g._QUAL113,plan['binding'])
    plan['authority']=cap;plan['released']=True;g._COUNTER115_RELEASED=True
    producer.clock.require(25)
    if time.time()+25>=plan['binding']['absolute_deadline_utc']:raise TimeoutError('No late GO')
    producer.clock.check(critical_end,25)
    g.send_signal(control,'COUNTER_GO116.json',{'binding_sha256':sha(canonical(plan['binding'])),'intent_sha256':sha(raw),'release_sha256':plan['binding']['release_sha256']},private)


class ReadCustodyFailure(RuntimeError):
    def __init__(self,receipt):self.read_custody=receipt;super().__init__('READ_OR_CLOSE_UNKNOWN_NO_RETRY')
class NativeReadIO:
    def parents(self,path):
        if any(p.is_symlink() for p in (path.parent,*path.parent.parents)):raise ValueError('Input ancestor link')
    def open(self,path):return os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK|os.O_CLOEXEC)
    def fstat(self,fd):return os.fstat(fd)
    def read(self,fd,count):return os.read(fd,count)
    def close(self,fd):os.close(fd)
def worker_bound_read(path,cap,pin=None,io=None):
    adapter=NativeReadIO() if io is None else io
    fd=None;data=bytearray();original=None;primary=None;cleanup=[];observed=False;operation='PARENTS';close_attempts=0
    def fault(op,exc):return {'operation':op,'exception_class':type(exc).__name__ if type(exc).__name__ in ('ValueError','TypeError','OSError','PermissionError','FileNotFoundError','TimeoutError') else 'OTHER','errno':exc.errno if isinstance(exc,OSError) else None}
    try:
        adapter.parents(path);operation='OPEN';fd=adapter.open(path);operation='FSTAT_BEFORE';before=adapter.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink!=1 or before.st_size>cap:raise ValueError('Counter input object')
        operation='READ'
        while len(data)<=cap:
            block=adapter.read(fd,min(65536,cap+1-len(data)));observed=True
            if not block:break
            data.extend(block)
        operation='FSTAT_AFTER';after=adapter.fstat(fd)
        if len(data)!=after.st_size or len(data)>cap or any(getattr(before,k)!=getattr(after,k) for k in ('st_dev','st_ino','st_size','st_mtime_ns','st_ctime_ns','st_nlink')):raise ValueError('Counter input changed')
        operation='PIN'
        if pin is not None and (len(data),sha(data))!=tuple(pin):raise ValueError('Counter input pin')
    except BaseException as exc:original=exc;primary=fault(operation,exc)
    if fd is not None:
        close_attempts=1
        try:adapter.close(fd)
        except BaseException as exc:cleanup.append(fault('CLOSE',exc))
    if primary is not None or cleanup:
        receipt={'primary':primary,'cleanup':cleanup,'close_attempts':close_attempts,'read_available':observed,'bytes':len(data) if observed else None,'sha256':sha(data) if observed else None,'unknown':True,'retry':False}
        raise ReadCustodyFailure(receipt) from original
    return bytes(data)

def project_result(raw,binding):
    d=strict(raw)
    if type(d) is not dict or set(d)!={'projection','provenance','result'}:raise ValueError('Counter result envelope')
    p,v,r=d['projection'],d['provenance'],d['result']
    pk={'adapter_version','status','profile_verification_date','gateway_profile','full_request_canonical_sha256','excluded_non_rendering_fields','effective_non_rendering_extras','reasoning_effort','rendering_input','pinned_rendering_flags','limitations'}
    vk={'status','counter_version','public_artifact_revision','model','model_dir','verified_model_file_sha256','served_template','served_template_sha256','additional_local_tokenizer_files_sha256','tokenizer_class','runtime_versions','local_files_only','trust_remote_code','add_generation_prompt','add_special_tokens','profile_verification_date','scope'}
    rk={'status','count','under_3000_input_tokens','tokens','rendered_utf8_sha256','effective_request'}
    if type(p) is not dict or set(p)!=pk or type(v) is not dict or set(v)!=vk or type(r) is not dict or set(r)!=rk:raise ValueError('Fixed counter schema')
    if p['full_request_canonical_sha256']!=binding['request_sha256'] or p['adapter_version']!='0.2.1' or p['status']!='verified-local-profile' or p['profile_verification_date']!='2026-10-17' or p['pinned_rendering_flags']!={'add_generation_prompt':True,'continue_final_message':False,'add_special_tokens':False}:raise ValueError('Request provenance')
    if v['status']!=r['status'] or v['status']!='verified-local-profile' or v['public_artifact_revision']!='a9904d24bcc1d289a1950fa9d2b978c47cf903b9' or v['profile_verification_date']!='2026-10-17':raise ValueError('Exact dated counter profile')
    if v['counter_version']!='0.2.1' or v['model']!='nvidia/Nemotron-3_5-Lightning' or v['served_template_sha256']!=PRIVATE_PINS['served_template.jinja'][1] or v['verified_model_file_sha256']!={n:pin[1] for n,pin in TOKENIZER_PINS.items()} or v['runtime_versions']!=VERSIONS:raise ValueError('Counter provenance')
    if v['model_dir']!='/vendor/tokenizer' or v['served_template']!='/vendor/served_template.jinja' or v['additional_local_tokenizer_files_sha256']!={}:raise ValueError('Fixed vendor paths')
    if any(v[k] is not expected for k,expected in [('local_files_only',True),('trust_remote_code',False),('add_generation_prompt',True),('add_special_tokens',False)]):raise ValueError('Offline counter semantics')
    n=r['count'];tokens=r['tokens']
    if type(n) is not int or not 0<=n<=16384 or type(tokens) is not list or len(tokens)!=n or any(type(x) is not int or not 0<=x<2147483648 for x in tokens):raise ValueError('Counter token/count types')
    if type(r['under_3000_input_tokens']) is not bool or r['under_3000_input_tokens']!=(n<3000) or not re.fullmatch('[a-f0-9]{64}',r['rendered_utf8_sha256']):raise ValueError('Counter result consistency')
    if r['effective_request']!=p['rendering_input']:raise ValueError('Rendering projection mismatch')
    return {'schema':'COUNTER115_SAFE_PROJECTION','candidate_count':n,'strict_under3000':n<3000,'rendered_utf8_sha256':r['rendered_utf8_sha256'],'raw_sha256':sha(raw),'binding_sha256':sha(canonical(binding)),'T':None,'authority':False,'model_calls':0}
def worker_ready_and_count(worker,go,manifest,deadline):
    b=validate_binding(go['counter115'],{k:go[k] for k in ('source_sha','manifest_sha256','once_receipt_sha256')})
    if manifest['mode']!='PUBLIC_INPUTS_ONLY_PRECOUNTER_DIAGNOSTIC' or any(manifest[k] is not False for k in ('counter_allowed','private_vendor_allowed','model_allowed')) or manifest['counter116']['mode']!=MODE or manifest['counter116']['activation']!='TYPED_CURRENT_NATIVE_PRODUCER_ONLY':raise ValueError('Counter mode not independently enabled')
    if deadline-time.monotonic()<25:raise TimeoutError('Counter reserve')
    for prefix,pins in [(pathlib.Path('/vendor'),PRIVATE_PINS),(pathlib.Path('/vendor/tokenizer'),TOKENIZER_PINS)]:
        for name,pin in pins.items():
            raw=worker_bound_read(prefix/name,pin[0],pin=pin)
            if (len(raw),sha(raw))!=pin:raise ValueError('Counter input pin')
    if os.getuid()!=65532:raise ValueError('Actual nonroot input reader required')
    worker.emit('counter116.inputs.json',{'uid':os.getuid(),'inputs':{n:{'bytes':p[0],'sha256':p[1]} for n,p in input_pins().items()},'binding_sha256':sha(canonical(b))})
    worker.emit('counter115.intent.json',b)
    with (worker.R/'counter115.ready').open('xb') as marker:marker.flush();os.fsync(marker.fileno())
    release=worker.wait('COUNTER_GO116.json',min(deadline-20,time.monotonic()+5))
    expected={'binding_sha256':sha(canonical(b)),'intent_sha256':sha((worker.R/'counter115.intent.json').read_bytes()),'release_sha256':b['release_sha256']}
    if release!=expected or time.time()>=b['absolute_deadline_utc']:raise ValueError('Counter release mismatch')
    if deadline-time.monotonic()<25 or time.time()+25>=b['absolute_deadline_utc']:raise TimeoutError('Postrelease worker full25s reserve')
    worker.emit('beforecounter115.json',{'stage':'BEFORE_COUNTER','closed':True})
    # ONE real call in a future independently admitted invocation; never called115.
    process=worker.run(list(ARGV),'counter',min(deadline-5,time.monotonic()+20))
    raw=worker_bound_read(worker.R/'counter.stdout',CAP)
    projection=project_result(raw,b)
    if process['original_returncode']!=0 or process['primary'] is not None or process['capture_failures']:raise ValueError('Counter original process failure')
    worker.emit('counter115.verified.json',projection);worker.emit('aftercounter115.json',{'stage':'AFTER_COUNTER','closed':True});return projection
def verify_host_completion(g,plan,output,terminal,approved):
    if not plan['released'] or g.classify_terminal(terminal,approved) is not None:raise ValueError('Counter host terminal')
    output.census();t=g.strict(output.read('counter.terminal.json',8192));p=g.project_process(t)
    if p['returncode']!=0 or p['original_returncode']!=0 or not p['terminal_observed'] or p['timed_out'] or p['primary'] is not None or p['cleanup'] or t['capture_failures']:raise ValueError('Counter custody')
    iso=p['isolation']
    if iso is None or not iso['restricted'] or iso['abi']<3 or iso['primary'] is not None or iso['cleanup'] or iso['cache_soft_limit_raised'] is not False or iso['output_fds_closed_count']!=2:raise ValueError('Counter native isolation')
    channels={}
    for ch in ('stdout','stderr'):
        raw=output.read('counter.'+ch,CAP);s=t['streams'][ch]
        if s!={'available':True,'bytes':len(raw),'sha256':sha(raw),'truncated':False}:raise ValueError('Counter fixed receipt closure')
        channels[ch]=raw
    expected=project_result(channels['stdout'],plan['binding'])
    if strict(output.read('counter115.verified.json',8192))!=expected:raise ValueError('Counter projection custody')
    plan['projected']=dict(expected,host_terminal=g.terminal_projection(terminal),source_sha=plan['binding']['source_sha'],raw_channels_public=False)
    return plan['projected']
