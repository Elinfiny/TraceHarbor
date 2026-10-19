"""NEW117 changed shared integration only. Explicit synthetic provider/clock data.

No native caller/seal/q is fabricated; no Docker, vendor, crypto or counter.
The actual read_external, ParentClock, OwnedIntake, owned_creation,
run_with_cleanup, bind_mounts and local_release callsites are shared with native.
Historical116 qualification is referenced, never rerun or repinned here.
"""
import pathlib,json,hashlib,sys,os,time,importlib.util,io,contextlib,traceback,copy,types,base64
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module);return module
prod=load('qualified117shared',ROOT/'diagnostic108/admission116.py')
host=load('qualified117host',ROOT/'diagnostic108/launch.py')
OUT=pathlib.Path(sys.argv[1]);OUT.mkdir(mode=0o700)
def put(path,raw):prod.exclusive(path,raw)
def expect(kind,fn):
    try:fn()
    except kind as exc:return exc
    raise AssertionError('Required refusal absent')
class Tick:
    def __init__(self):self.now=1800000000.;self.m=1000.
    def wall(self):return self.now
    def mono(self):return self.m
    def advance(self,n):self.now+=n;self.m+=n
def domain():
    tick=Tick();run={'id':123,'run_started_at':'2027-01-15T08:00:00Z'}
    # Derive syntheticISO from the declared fixture clock, never provider data.
    run['run_started_at']=prod.datetime.datetime.fromtimestamp(tick.now,prod.datetime.timezone.utc).isoformat()
    clock=prod.ParentClock.from_run(run,int(tick.now+900),int(tick.now+900),tick.wall,tick.mono)
    data={f'input{n}':f'PUBLIC_SYNTHETIC117_{n}'.encode() for n in range(6)}
    pins={n:(len(v),prod.sha(v)) for n,v in data.items()}
    b={'source_sha':'a'*40,'manifest_sha256':'b'*64,'request_sha256':'e4b08fa3937e4c8348383a5abf934ffbf3832183fadc2907018adbc4a04a71b2','run_id':'123'}
    core={'schema':'TRACE116_ONCE_INTENT_V1','original_writer':prod.WRITER,'source_sha':b['source_sha'],'manifest_sha256':b['manifest_sha256'],'request_sha256':b['request_sha256'],'request_bytes':4935,'lock_sha256':'fcea30197a1bf1c0eaa99314dcbf26a152935ba4535c1544b97f2f5a62f2515a','inputs':{n:{'bytes':p[0],'sha256':p[1]} for n,p in pins.items()},'role':'OFFLINE_COUNTER_ONLY','max_counter_invocations':1,'model_calls':0,'spend':0,'expires_utc':int(clock.once_expires_utc),'nonce':'1'*32}
    b['once_receipt_sha256']=prod.sha(prod.can(core))
    admit=dict(b,schema='TRACE116_EXTERNAL_ONCE_V1',phase='admit',original_writer=prod.WRITER,own_library_file_id='libfile_3ee8270f03d8819188e1de1f75c3d824',own_cas_version=500,own_pinned_readback_sha256='c'*64,attempt=1,role='OFFLINE_COUNTER_ONLY',request_bytes=4935,lock_sha256=core['lock_sha256'],model_calls=0,spend=0,expires_utc=core['expires_utc'],inputs=core['inputs'],parent_clock=clock.descriptor(),once_intent=core)
    return tick,clock,data,pins,b,admit
class SyntheticAPI:
    def __init__(self,d,b,tick,delay=1):
        self.calls=[];self.tick=tick;self.delay=delay
        raw=prod.can(d);blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        phase=d['phase'];self.ref='heads/traceharbor-counter116-'+phase+'-'+b['once_receipt_sha256']
        self.values=[{'ref':'refs/'+self.ref,'object':{'type':'commit','sha':'d'*40}}, {'author':{'id':prod.OWNER},'committer':{'id':prod.OWNER},'parents':[{'sha':b['source_sha']}],'commit':{'tree':{'sha':'e'*40}}}, {'tree':[{'path':'base','mode':'100644','type':'blob','sha':'f'*40},{'path':'counter116-'+phase+'.json','mode':'100644','type':'blob','sha':blob}],'truncated':False}, {'tree':{'sha':'0'*40}}, {'tree':[{'path':'base','mode':'100644','type':'blob','sha':'f'*40}],'truncated':False}, {'content':base64.b64encode(raw).decode(),'size':len(raw)}]
    def __call__(self,path,deadline=None,missing=False):
        assert deadline is not None and self.tick.mono()<deadline
        self.calls.append({'path':path,'deadline':deadline,'before':self.tick.mono(),'domain':'SYNTHETIC_API_NOT_PROVIDER'})
        self.tick.advance(self.delay);return copy.deepcopy(self.values[len(self.calls)-1])
def fixture_producer(root,b,pins,data,admit):
    root.mkdir();producer=types.SimpleNamespace(root=root,caller=types.SimpleNamespace(binding=b,receipt=admit),pins=pins)
    custody=prod.stage_copies(producer,root/'runtime',data,pins,{'ciphertext_sha256':'d'*64,'ciphertext_commit':'d'*40},{'realm':'SYNTHETIC_NO_CRYPTO'})
    return producer,custody
def staged_mounts(root,producer,custody,b):
    bindings={};expected={}
    for dest in host.DESTINATIONS:
        path=root/('mount-'+dest.strip('/').replace('/','_'))
        if dest in ('/output','/control','/wheels'):path.mkdir()
        else:put(path,b'PUBLIC_SYNTHETIC117_MOUNT');expected[dest]=(path.stat().st_size,prod.sha(path.read_bytes()))
        bindings[dest]=(path,dest!='/output')
    extras={}
    for n,path in custody.paths.items():extras['/vendor/'+n]=(path,True);expected['/vendor/'+n]=custody.pins[n]
    bindings.update(extras);evidence=host.prove_mounts(bindings,expected,b['source_sha'],extra=extras);q={'realm':'SYNTHETIC_NOT_NATIVE'}
    return prod.bind_mounts(producer,host,custody,evidence,bindings,q),evidence,q
def case1():
    tick,clock,data,pins,b,admit=domain();producer,custody=fixture_producer(OUT/'case1-fixture',b,pins,data,admit)
    d=dict(admit,phase='consumed',recipient_context=custody.context,ciphertext_receipt=custody.receipt,admit_sha256=prod.sha(prod.can(admit)))
    api=SyntheticAPI(d,b,tick);observed=[];deadline=clock.phase(45,205)
    got,provenance=prod.read_external(api,json.loads,'consumed',b,pins,clock,deadline,observed.append,custody,admit)
    proof=prod.ContractConsumedProof(producer,prod.can(got),prod.can(provenance),custody,prod.can(b),clock)
    put(OUT/'case1-original-reads.json',prod.can({'domain':'SYNTHETIC_NOT_PROVIDER','observations':observed}))
    assert len(observed)==len(api.calls)==6 and tick.mono()==1006 and all(c['deadline']==deadline for c in api.calls)
    prepared,evidence,q=staged_mounts(OUT/'case1-fixture',producer,custody,b)
    assert prepared.producer is producer and prepared.evidence is evidence and prepared.native_q is q
    # Native boundary rejects the synthetic proof before any effects.
    expect(TypeError,lambda:prod.native_boundary(proof,producer,evidence,q,b))
    before=len(api.calls);worker=dict(b,absolute_deadline_utc=tick.wall()+170)
    critical=tick.mono()+5
    receipt=prod.local_release(proof,producer,custody,worker,clock,producer.root/'local-consumed.json')
    clock.check(critical,25);put(producer.root/'CONTRACT_GO.json',prod.can(receipt))
    assert len(api.calls)==before and receipt['native_release'] is False
    original=(producer.root/'local-consumed.json').read_bytes()
    expect(FileExistsError,lambda:prod.local_release(proof,producer,custody,worker,clock,producer.root/'local-consumed.json'))
    assert (producer.root/'local-consumed.json').read_bytes()==original
    return {'six_reads_outside_worker':True,'one_phase_deadline':deadline,'original_read_times_saved':True,'critical_API_calls':0,'same_mount_and_q_objects':True,'native_rejected_contract':True,'once_release_immutable':True}
def case2():
    tick,clock,data,pins,b,admit=domain();producer,custody=fixture_producer(OUT/'case2-fixture',b,pins,data,admit)
    d=dict(admit,phase='consumed',recipient_context=custody.context,ciphertext_receipt=custody.receipt,admit_sha256=prod.sha(prod.can(admit)))
    api=SyntheticAPI(d,b,tick,delay=8);observed=[];end=clock.phase(45,205)
    expect(prod.LateProviderRead,lambda:prod.read_external(api,json.loads,'consumed',b,pins,clock,end,observed.append,custody,admit))
    put(OUT/'case2-original-late-read.json',prod.can({'domain':'SYNTHETIC_NOT_PROVIDER','observations':observed}))
    assert len(observed)==6 and observed[-1]['value'] is not None and observed[-1]['after']['mono']>end
    refused=[]
    for name in ['source','ciphertext','once_preimage']:
        changed=copy.deepcopy(d)
        if name=='source':changed['source_sha']='0'*40
        elif name=='ciphertext':changed['ciphertext_receipt']['ciphertext_sha256']='0'*64
        else:changed['once_intent']['nonce']='2'*32
        expect(ValueError,lambda:prod.validate_external(changed,'consumed',b,pins,clock,custody,admit));refused.append(name)
    assert not (producer.root/'local-consumed.json').exists()
    return {'late_success_original_retained':True,'late_UNKNOWN':True,'downstream_effects':0,'retry':False,'preimages_refused':refused}
def case3():
    tick,clock,data,pins,b,admit=domain();unrelated=OUT/'old-unrelated';put(unrelated,b'PUBLIC_OLD_UNRELATED117');old=unrelated.read_bytes();calls=[]
    def remove_fault(name,dir_fd):
        calls.append(name);os.unlink(name,dir_fd=dir_fd);raise OSError(5,'EXPLICIT_ADAPTER_AFTER_ACTUAL_REMOVE')
    owner=prod.OwnedIntake(OUT/'case3-partial-init',b,pins,create=True,remove=remove_fault)
    def partial():
        (owner.root/'fresh-recipient').mkdir();put(owner.root/'fresh-recipient/recipient.key',b'PUBLIC_SYNTHETIC_KEY_FIXTURE_NOT_KEY');raise ValueError('INJECTED_INIT_PRIMARY_BEFORE_BINDING')
    def operation():return prod.owned_creation(owner,['fresh-recipient','fresh-recipient/recipient.key'],partial)
    exc=expect(ValueError,lambda:prod.run_with_cleanup(owner,'init_failure',operation));receipt=exc.intake_cleanup
    assert receipt['primary']['exception_class']=='ValueError' and receipt['unknown'] and len(calls)==1 and receipt['retry'] is False and not (owner.root/'fresh-binding.json').exists()
    again=owner.cleanup('workflow_always');assert again['unknown'] and len(calls)==1
    put(OUT/'case3-original-init-cleanup.json',prod.can({'original':receipt,'fallback':again,'domain':'EXPLICIT_ADAPTER_INJECTION_NOT_KERNEL_FAILURE'}))
    later=prod.OwnedIntake(OUT/'case3-later-mount',b,pins,create=True)
    custody=prod.owned_creation(later,['runtime-inputs',*('runtime-inputs/'+n for n in pins)],lambda:prod.stage_copies(later,later.root/'runtime-inputs',data,pins,{},{}))
    primary=OSError(5,'INJECTED_MOUNT_READ_PRIMARY');end=later.cleanup('terminal',primary)
    assert end['primary']['exception_class']=='OSError' and end['status']=='PASS' and all(not p.exists() for p in custody.paths.values())
    # A newly introduced symlink to an unrelated old path is refused, untouched.
    bad=prod.OwnedIntake(OUT/'case3-symlink-refusal',b,pins,create=True);(bad.root/'fresh-recipient').mkdir();bad.capture_created(['fresh-recipient']);(bad.root/'fresh-recipient/recipient.key').symlink_to(unrelated)
    refused=bad.cleanup('terminal',ValueError('SYNTHETIC_PRIMARY'))
    assert refused['unknown'] and unrelated.read_bytes()==old and (bad.root/'fresh-recipient/recipient.key').is_symlink()
    put(OUT/'case3-original-later-cleanup.json',prod.can({'later':end,'symlink':refused}))
    return {'partial_init_without_binding_cleaned_once':True,'primary_and_injected_remove_UNKNOWN_separate':True,'fallback_no_retry':True,'later_mount_failure_runtime_copies_removed':True,'unrelated_path_unchanged':True,'symlink_refused':True,'secure_erase':False}
def case4():
    tick,clock,_,_,_,_=domain();table=prod.PHASES117;total=sum(table.values());assert total==825 and total<900
    originals=[];fixed=clock.end_mono
    # The same shared clock traverses the executable phases; no snapshot lease.
    for name,maximum in table.items():
        remaining=sum(list(table.values())[list(table).index(name)+1:])
        deadline=clock.phase(maximum,remaining)
        originals.append({'phase':name,'maximum_s':maximum,'future_reserve_s':remaining,'before_mono':tick.mono(),'deadline':deadline})
        tick.advance(maximum-.001);clock.check(deadline,remaining);tick.advance(.001)
        assert clock.end_mono==fixed
    assert clock.end_utc-tick.wall()==75
    run={'id':123,'run_started_at':prod.datetime.datetime.fromtimestamp(clock.started_utc,prod.datetime.timezone.utc).isoformat()}
    reopened=prod.ParentClock.from_run(run,int(clock.once_expires_utc),int(clock.coordinator_cutoff_utc),tick.wall,tick.mono)
    assert reopened.end_mono==fixed and reopened.end_utc==clock.end_utc
    expect(TimeoutError,lambda:reopened.phase(70,250))
    tick.advance(76);expect(TimeoutError,lambda:clock.require(0));expect(TimeoutError,lambda:reopened.require(0))
    # Backward wall adjustment still cannot restore the original monotonic end.
    tick.now-=500;expect(TimeoutError,lambda:clock.require(0))
    put(OUT/'case4-original-clock.json',prod.can({'synthetic':True,'originals':originals,'upper_bound_sum_s':total,'job_limit_s':900,'remaining_s':75,'native_runtime_PASS':False}))
    return {'sum_s':825,'main_s':665,'job_s':900,'arithmetic_margin_s':75,'no_deadline_reset':True,'overrun_and_reserve_refused':True,'native_timing_PASS':False,'stdlib_children':0}

def case5():
    tick,clock,data,pins,b,admit=domain();events=[];closed=[]
    def close_fault(fd):
        os.close(fd);closed.append(fd)
        if len(closed)==1:
            events.append({'operation':'CLOSE','actual_kernel_close_returned':True,'adapter_error':'EIO'})
            raise OSError(5,'EXPLICIT_ADAPTER_AFTER_ACTUAL_CLOSE')
    owner=prod.OwnedIntake(OUT/'case5-close-durable',b,pins,create=True,close=close_fault)
    (owner.root/'fresh-recipient').mkdir();put(owner.root/'fresh-recipient/recipient.key',b'PUBLIC_SYNTHETIC_NOT_KEY');owner.capture_created(['fresh-recipient','fresh-recipient/recipient.key'])
    receipt=owner.cleanup('terminal',ValueError('SYNTHETIC_PRIMARY'))
    key='fresh-recipient/recipient.key';row=next(r for r in receipt['paths'] if r['path']==key)
    assert receipt['unknown'] and row['status']=='UNKNOWN' and row['close_cleanup'] and row['remove_attempts']==1 and receipt['primary']['exception_class']=='ValueError'
    # Independent filesystem restart readback retains uncertainty; no remove retry.
    reopened=prod.OwnedIntake(owner.root,b,pins,create=False);later=reopened.cleanup('workflow_always')
    row2=next(r for r in later['paths'] if r['path']==key)
    assert row2['status']=='UNKNOWN' and row2['close_cleanup']==row['close_cleanup'] and later['unknown'] and row2['remove_attempts']==1
    reads=[];closes=[];removes=[]
    def read_fault(fd,n):
        raw=os.read(fd,n);reads.append({'actual_read_bytes':len(raw),'adapter_error':'EIO'});raise OSError(5,'EXPLICIT_ADAPTER_AFTER_READ')
    def read_close(fd):
        os.close(fd);closes.append(fd)
        if len(closes)==1:raise OSError(5,'EXPLICIT_ADAPTER_AFTER_READ_FD_CLOSE')
    def remove_fault(name,dir_fd):
        os.unlink(name,dir_fd=dir_fd);removes.append(name);raise OSError(5,'EXPLICIT_ADAPTER_AFTER_REMOVE')
    combined=prod.OwnedIntake(OUT/'case5-read-close-remove',b,pins,create=True,read=read_fault,close=read_close,remove=remove_fault)
    (combined.root/'fresh-recipient').mkdir();put(combined.root/'fresh-recipient/recipient.key',b'PUBLIC_SYNTHETIC_NOT_KEY');combined.capture_created(['fresh-recipient','fresh-recipient/recipient.key']);put(combined.root/'fresh-binding.json',b'PUBLIC_SYNTHETIC_READ117')
    error=expect(prod.CleanupFailure,lambda:prod.run_with_cleanup(combined,'init_failure',lambda:combined.read_small('fresh-binding.json')))
    fd_receipt=error.cleanup_receipt;cleanup=error.intake_cleanup
    assert fd_receipt['primary']['exception_class']=='OSError' and fd_receipt['cleanup'] and cleanup['unknown'] and len(reads)==len(removes)==1 and cleanup['retry'] is False
    put(OUT/'case5-original-durable-close.json',prod.can({'first':receipt,'reopened':later,'fd_read_primary_and_close':fd_receipt,'following_cleanup':cleanup,'events':events,'reads':reads,'domain':'EXPLICIT_ADAPTER_INJECTION_NOT_KERNEL_FAILURE'}))
    return {'close_UNKNOWN_persisted_before_restart':True,'fallback_retains_original_uncertainty':True,'remove_attempts':1,'read_close_remove_faults_separate':True,'first_primary_retained':True,'native_effects':0}

cases=[(5,case5)] if len(sys.argv)>2 and sys.argv[2]=='--case5' else list(enumerate([case1,case2,case3,case4],1));results=[]
for number,fn in cases:
    out=io.StringIO();err=io.StringIO();value=None;failure=None;start=time.monotonic()
    with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
        try:value=fn()
        except BaseException as exc:failure=type(exc).__name__;traceback.print_exc()
    stdout=out.getvalue().encode();stderr=err.getvalue().encode()
    put(OUT/f'case{number}.stdout',stdout);put(OUT/f'case{number}.stderr',stderr)
    terminal={'case':number,'domain':'SYNTHETIC_PROVIDER_CLOCK_NOT_NATIVE','returncode':0 if failure is None else 1,'exception_class':failure,'elapsed_s':time.monotonic()-start,'streams':{'stdout':{'bytes':len(stdout),'sha256':prod.sha(stdout)},'stderr':{'bytes':len(stderr),'sha256':prod.sha(stderr)}}}
    put(OUT/f'case{number}.terminal.json',prod.can(terminal));put(OUT/f'case{number}.result.json',prod.can(value))
    results.append(terminal)
    print(json.dumps({'case':number,'pass':failure is None,'exception_class':failure}),flush=True)
put(OUT/'group.json',prod.can({'schema':'NEW117_INTEGRATION_GROUP','cases':results,'all_pass':all(r['returncode']==0 for r in results),'historical116_reruns':0,'native_effects':0}))
sys.exit(0 if all(r['returncode']==0 for r in results) else 1)
