"""NEW116 bounded contract group only. Synthetic classes never become native authority."""
import pathlib,json,hashlib,sys,os,time,importlib.util,io,contextlib,traceback
ROOT=pathlib.Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def encoded(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def put(p,b):
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def stage(root,expires=None):
    root.mkdir();source='0'*40
    binding={'source_sha':source,'request_sha256':'3'*64,'once_receipt_sha256':'2'*64,'manifest_sha256':'1'*64,'run_id':'0','absolute_deadline_utc':time.time()+60 if expires is None else expires,'realm':'SYNTHETIC_CONTRACT_ONLY_NOT_A_RESERVATION'}
    names=['count_chat.py','count_request.py','served_template.jinja','tokenizer/tokenizer.json','tokenizer/tokenizer_config.json','tokenizer/special_tokens_map.json'];data={n:('PUBLIC_SYNTHETIC116:'+n).encode() for n in names};pins={n:(len(v),sha(v)) for n,v in data.items()}
    producer=prod.ContractProducer(root/'producer',binding,pins);custody=producer.prepare(data);bindings={};expected={}
    for dest in host.DESTINATIONS:
        p=root/('fixture-'+dest.strip('/').replace('/','_'))
        if dest in ('/output','/control','/wheels'):p.mkdir()
        else:put(p,b'PUBLIC_SYNTHETIC_SOURCE116');expected[dest]=(p.stat().st_size,sha(p.read_bytes()))
        bindings[dest]=(p,dest!='/output')
    extras={}
    for n,p in custody.paths.items():extras['/vendor/'+n]=(p,True);expected['/vendor/'+n]=pins[n]
    bindings.update(extras);evidence=host.prove_mounts(bindings,expected,source,extra=extras);q={'realm':'SYNTHETIC_NOT_NATIVE'};prepared=producer.bind(host,custody,evidence,bindings,q);marker={'realm':'SYNTHETIC_NOT_NATIVE'};cap=producer.issue(host,prepared,evidence,q,binding,marker,marker)
    return {'producer':producer,'custody':custody,'prepared':prepared,'bindings':bindings,'expected':expected,'extra':extras,'evidence':evidence,'q':q,'binding':binding,'cap':cap,'control':bindings['/control'][0]}
def case1():
    global staged
    staged=stage(OUT/'case1-fixture');s=staged
    try:prod.native_boundary(s['cap'],s['producer'],s['evidence'],s['q'],s['binding'])
    except TypeError:pass
    else:raise AssertionError('Synthetic crossed native boundary')
    result=s['producer'].release(s['cap'],s['evidence'],s['q'],s['binding'],s['control']);go=s['control']/'COUNTER_GO116.json';assert result['native_release'] is False and go.is_file()
    assert type(s['cap']) is prod.ContractCounterAuthority and s['cap'].producer is s['producer'] and s['prepared'].evidence is s['evidence']
    originals={'domain':'SYNTHETIC_ONLY','native_authority':False,'fixture_closed_files':{str(p.relative_to(OUT)):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in (OUT/'case1-fixture').rglob('*') if p.is_file()},'release':result};print(json.dumps(originals));return originals
def case2():
    s=staged;before=(s['control']/'COUNTER_GO116.json').read_bytes();refused=[]
    old=host.prove_mounts(s['bindings'],s['expected'],s['binding']['source_sha'],extra=s['extra'])
    unused=s['producer'].issue(host,s['prepared'],s['evidence'],s['q'],s['binding'],{'realm':'SYNTHETIC_NOT_NATIVE'},{'realm':'SYNTHETIC_NOT_NATIVE'})
    checks=[('reused',lambda:s['producer'].release(s['cap'],s['evidence'],s['q'],s['binding'],s['control'])),('wrong_same_source_object',lambda:s['producer'].consume(unused,old,s['q'],s['binding'])),('JSON_at_native_boundary',lambda:prod.native_boundary({'approved':True},s['producer'],s['evidence'],s['q'],s['binding'])),('synthetic_at_native_boundary',lambda:prod.native_boundary(s['cap'],s['producer'],s['evidence'],s['q'],s['binding']))]
    expired=stage(OUT/'expired-fixture',time.time()-1)
    checks.append(('expired_at_final_contract_boundary',lambda:expired['producer'].release(expired['cap'],expired['evidence'],expired['q'],expired['binding'],expired['control'])))
    fresh=s['producer'].issue(host,s['prepared'],s['evidence'],s['q'],s['binding'],{'realm':'SYNTHETIC_NOT_NATIVE'},{'realm':'SYNTHETIC_NOT_NATIVE'})
    checks.append(('durable_create_only_consumed',lambda:s['producer'].release(fresh,s['evidence'],s['q'],s['binding'],s['control'])))
    for name,fn in checks:
        try:fn()
        except (TypeError,ValueError,TimeoutError,FileExistsError) as e:refused.append({'check':name,'original_exception_class':type(e).__name__})
        else:raise AssertionError(name)
    assert (s['control']/'COUNTER_GO116.json').read_bytes()==before and not (expired['control']/'COUNTER_GO116.json').exists();print(json.dumps(refused));return {'refused':refused,'original_release_immutable':True,'native_release':False,'counter_child':0}
def case3():
    path=OUT/'public-read-fixture';put(path,b'PUBLIC_SYNTHETIC_READ116');events=[]
    class FaultingAdapter(bridge.NativeReadIO):
        def read(self,fd,count):
            actual=super().read(fd,count);events.append({'operation':'READ','actual_bytes_before_injected_error':len(actual),'adapter_injected_error':'OSError_EIO','kernel_read_failed':False});raise OSError(5,'PUBLIC_INJECTED_READ_FAULT')
        def close(self,fd):
            super().close(fd);events.append({'operation':'CLOSE','actual_kernel_close_returned':True,'adapter_injected_error':'OSError_EIO'});raise OSError(5,'PUBLIC_INJECTED_CLOSE_FAULT')
    try:bridge.worker_bound_read(path,100,pin=(path.stat().st_size,sha(path.read_bytes())),io=FaultingAdapter())
    except bridge.ReadCustodyFailure as e:
        original=e.read_custody;put(OUT/'case3-original-read-close.json',encoded({'original_helper_receipt':original,'actual_adapter_events':events}))
        assert original['primary']['operation']=='READ' and original['primary']['exception_class']=='OSError' and len(original['cleanup'])==1 and original['cleanup'][0]['operation']=='CLOSE' and original['close_attempts']==1 and original['unknown'] and original['retry'] is False and len(events)==2
        print(json.dumps({'receipt':original,'events':events,'fault_domain':'EXPLICIT_ADAPTER_INJECTION_NOT_KERNEL_FAILURE'}));return {'both_retained':True,'close_once':True,'next_dependency_calls':0,'fault_domain':'ADAPTER_INJECTED','receipt':original}
    raise AssertionError('Combined fault accepted')
def case4():
    private=OUT/'case4-real-process';private.mkdir();argv=[sys.executable,'-I','-c',"import sys;print('PUBLIC_SYNTHETIC_INTERFACE116');print('PUBLIC_SYNTHETIC_STDERR116',file=sys.stderr)"]
    terminal,data=host.invoke(argv,private,'new-interface116',min(END,time.monotonic()+5))
    original={'argv':argv,'terminal':terminal,'channels':{n:{'bytes':len(b),'sha256':sha(b),'hex':b.hex()} for n,b in data.items()},'actual_stdlib_process':True,'vendor_import':False,'native_counter':False};put(OUT/'case4-original-process.json',encoded(original))
    assert terminal['returncode']==0 and not terminal['primary'] and not terminal['capture_failures'] and terminal['terminal_saved'] and all(len(v)<=65536 for v in data.values());print(json.dumps(original));return {'actual_stdlib_process':True,'returncode':0,'native_counter':False,'original':original}
def case5():
    # New static finding only: an attributed descriptor must also bind the exact
    # once-intent preimage. This is synthetic digest data, NOT a reserved once.
    pins={'PUBLIC_SYNTHETIC_INPUT':(4,sha(b'TEST'))};binding={'source_sha':'0'*40,'manifest_sha256':'1'*64,'request_sha256':'3'*64}
    core={'schema':'TRACE116_ONCE_INTENT_V1','original_writer':prod.WRITER,'source_sha':binding['source_sha'],'manifest_sha256':binding['manifest_sha256'],'request_sha256':binding['request_sha256'],'request_bytes':4935,'lock_sha256':'fcea30197a1bf1c0eaa99314dcbf26a152935ba4535c1544b97f2f5a62f2515a','inputs':{n:{'bytes':p[0],'sha256':p[1]} for n,p in pins.items()},'role':'OFFLINE_COUNTER_ONLY','max_counter_invocations':1,'model_calls':0,'spend':0,'expires_utc':int(time.time())+60,'nonce':'0'*32}
    binding['once_receipt_sha256']=prod.sha(prod.can(core));descriptor={'once_intent':core,'expires_utc':core['expires_utc']};assert prod.verify_once_intent(descriptor,binding,pins) is True
    wrong=json.loads(json.dumps(descriptor));wrong['once_intent']['source_sha']='4'*40
    try:prod.verify_once_intent(wrong,binding,pins)
    except ValueError:pass
    else:raise AssertionError('Wrong once preimage accepted')
    bad=dict(binding,once_receipt_sha256='9'*64)
    try:prod.verify_once_intent(descriptor,bad,pins)
    except ValueError:pass
    else:raise AssertionError('Unbound once digest accepted')
    try:prod.native_boundary(descriptor,None,None,None,binding)
    except TypeError:pass
    else:raise AssertionError('Digest document became native authority')
    print('PUBLIC_SYNTHETIC_ONCE_INTEGRITY_DATA_ONLY');return {'exact_preimage_check':True,'wrong_digest_refused':True,'JSON_remains_non_authority':True,'live_once_minted':False,'native_calls':0}
if __name__=='__main__':
    OUT=pathlib.Path(sys.argv[1]);OUT.mkdir(mode=0o700);group=int(sys.argv[2]);assert group in (1,2);frozen=json.loads((ROOT/'qualification116/pins.json').read_text())
    for n,v in frozen['source_files'].items():assert sha((ROOT/n).read_bytes())==v['sha256']
    assert sha((ROOT/'diagnostic108/manifest.json').read_bytes())==frozen['manifest_sha256'];put(OUT/'CONSUMED.json',encoded({'group':group,'cases':[1,2,3,4] if group==1 else [1],'realm':'SYNTHETIC_CONTRACT_NOT_NATIVE','retry_of_old_effect':False}));END=time.monotonic()+45
    host=load('host_contract116',ROOT/'diagnostic108/launch.py');bridge=load('bridge_contract116',ROOT/'diagnostic108/counter115.py');prod=bridge.producer_module(ROOT);cases=[]
    functions=(case1,case2,case3,case4) if group==1 else (case5,)
    for number,fn in enumerate(functions,1):
        stdout,stderr=io.StringIO(),io.StringIO();returned=None;fault=None;start=time.monotonic()
        try:
            with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):returned=fn()
        except BaseException as e:fault={'exception_class':type(e).__name__,'message':str(e)[:300]}
        # Original in-process return/exception and stdout/stderr persist before guards.
        rawout,rawerr=stdout.getvalue().encode(),stderr.getvalue().encode();put(OUT/('case'+str(number)+'.stdout'),rawout);put(OUT/('case'+str(number)+'.stderr'),rawerr)
        original={'case':number,'kind':'IN_PROCESS_CONTRACT' if number<4 else 'REAL_STDLIB_PROCESS_INTERFACE','returned':returned,'exception':fault,'elapsed_s':time.monotonic()-start,'stdout':{'bytes':len(rawout),'sha256':sha(rawout)},'stderr':{'bytes':len(rawerr),'sha256':sha(rawerr)}};put(OUT/('case'+str(number)+'.terminal.json'),encoded(original));cases.append({'case':number,'pass':fault is None,'original':original})
        if time.monotonic()>=END:break
    result={'schema':'TRACE116_CHANGED_INTERFACE_GROUP','group':group,'source_pin_sha256':sha((ROOT/'qualification116/pins.json').read_bytes()),'cases':cases,'all_pass':len(cases)==len(functions) and all(v['pass'] for v in cases),'actual_stdlib_children':1 if group==1 else 0,'Docker':0,'native_authority':False,'native_counter':0,'vendor_import':0,'tokenizer_import':0,'crypto':0,'provider_calls':0,'old_group_replay':0};put(OUT/'result.json',encoded(result));print(json.dumps({'group':group,'all_pass':result['all_pass'],'cases':[{'case':v['case'],'pass':v['pass'],'fault':v['original']['exception']} for v in cases]}));assert result['all_pass']
