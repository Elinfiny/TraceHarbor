"""New120 changed contracts only. Explicit synthetic clocks/process adapters;
case5 uses the real prepared120writer before effect; case6 closes its necessary
real publication. No NativeProducer/q/seal/counter/private authority fabricated.
"""
import pathlib,sys,json,hashlib,importlib.util,time,copy,io,os,types,contextlib,traceback,subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
host=load('host120test',ROOT/'diagnostic108/host_transport118.py');prod=load('producer120test',ROOT/'diagnostic108/admission116.py');launch=load('launch120test',ROOT/'diagnostic108/launch.py')
OUT=pathlib.Path(sys.argv[1]);OUT.mkdir(mode=0o700,exist_ok=True);G=pathlib.Path(sys.argv[3]);cfg=host.strict((G/'config.json').read_bytes())
def expect(types_,fn):
 try:fn()
 except types_ as exc:return exc
 raise AssertionError('Expected failclosed refusal absent')
class Tick:
 def __init__(self,elapsed=0):self.start=1800000000.;self.t=float(elapsed)
 def wall(self):return self.start+self.t
 def mono(self):return 1000+self.t
 def advance(self,n):assert n>=0;self.t+=n
 def clock(self):
  run={'id':123,'run_started_at':prod.datetime.datetime.fromtimestamp(self.start,prod.datetime.timezone.utc).isoformat()}
  return prod.ParentClock.from_run(run,int(self.start+900),int(self.start+900),self.wall,self.mono)
class PublicSyntheticIngress:
 can=staticmethod(prod.can)
 def __init__(self,tick):self.tick=tick;self.effects=[]
 def recipient(self,path,context):
  self.effects.append('SYNTHETIC_PUBLIC_NOT_KEY');self.tick.advance(20);path.mkdir();prod.exclusive(path/'recipient.key',b'PUBLIC_SYNTHETIC_NOT_KEY');prod.exclusive(path/'recipient.pem',b'PUBLIC_SYNTHETIC_NOT_CERTIFICATE');return context,b'PUBLIC_SYNTHETIC_NOT_CERTIFICATE'
 def put(self,path,data):self.tick.advance(2.49);prod.exclusive(path,data)
def recipient_contract(tick,name):
 clock=tick.clock();binding={'run_id':'123','source_sha':'a'*40};ingress=PublicSyntheticIngress(tick);root=OUT/name;owner=prod.OwnedIntake(root,binding,{},create=True)
 fixture=types.SimpleNamespace(clock=clock,caller=types.SimpleNamespace(ingress=ingress,binding=binding,receipt={'domain':'PUBLIC_SYNTHETIC_ADMIT_NOT_AUTHORITY'}),root=root,owner=owner)
 return fixture,ingress
class SyntheticHost:
 def __init__(self,tick):self.tick=tick;self.current_checkpoint_version=500;self.events=[];self.seq=0
 def bind_phase(self,end):self.end=end
 def cas_checkpoint(self,v,payload):
  assert v==self.current_checkpoint_version;self.tick.advance(16.862);self.current_checkpoint_version+=1;r={'version':self.current_checkpoint_version,'sha256':'b'*64,'domain':'SYNTHETIC_NOT_LIBRARY'};self.events.append({'op':'syntheticCASpair','at':self.tick.t});return r
 def pinned_checkpoint_readback(self,r):return r
 def reserve_operation(self,key,tool,args,source,end):return self.cas_checkpoint(self.current_checkpoint_version,{'phase':'SYNTHETIC_RESERVATION'})
 def call(self,tool,args):self.tick.advance(3);self.seq+=1;self.events.append({'op':tool,'at':self.tick.t});return {'sha':format(self.seq,'040x')}
 def verified_readback(self,*args):self.tick.advance(18);self.events.append({'op':'SYNTHETIC_SIX_READS','at':self.tick.t});return {'domain':'SYNTHETIC_NOT_PROVIDER_PROOF'}
def case1():
 # Actual coordinator stage functions, actual immutable ParentClock, mocked
 # tools explicitly carry no Library/Git/native authority.
 t=Tick(35);clock=t.clock();clock.require(865);transport=SyntheticHost(t);observed=[];co=prod.ExternalCoordinator117(transport,observed.append,clock,'a'*40,'c'*40);co.stage('admit',{'source_sha':'a'*40,'once_receipt_sha256':'d'*64},500)
 assert abs(t.t-149.31)<.001 and clock.end_mono==1900 and transport.current_checkpoint_version==505
 # Tight runner boundary, separate explicit synthetic view of SAME run end.
 r=Tick(35);rc=r.clock();rc.require(865);initial=rc.phase(150,685);r.advance(149.999);rc.check(initial,685);fixture,ingress=recipient_contract(r,'case1-public-contract');before=r.t
 result=prod.NativeProducer.initialize_recipient(fixture)
 assert not isinstance(fixture,prod.NativeProducer) and result.exists() and r.t-before<25 and 690<900-r.t<691
 expect(TimeoutError,lambda:rc.require(725));rc.require(680)
 recipient_end=r.t;r.advance(60);r.advance(10);rc.require(prod.HOST_BEGIN_REMAINDER120);host_start=r.t
 rc.require(565);main=rc.phase(45,520);r.advance(44.999);rc.check(main,520)
 prequal=launch.prequalification_deadline120(min(rc.end_mono,r.mono()+720)-95,types.SimpleNamespace(clock=rc));r.advance(199.999);rc.check(prequal,320);prequal_end=r.t
 for name,maximum,reserve in [('receive',70,250),('consumed',45,205),('mounts',10,195),('worker',170,25),('cleanup',10,15),('proof',15,0)]:
  end=rc.phase(maximum,reserve)
  if name=='worker':
   ready=r.mono()+5;r.advance(4.999);rc.check(ready,25);r.advance(maximum-5)
  else:r.advance(maximum-.001)
  rc.check(end,reserve)
  if name=='receive':receive_end=r.t
 # Parallel host lane starts while runner mainadmit/prequal is in progress.
 h=Tick(host_start);hc=h.clock();hc.require(prod.HOST_BEGIN_REMAINDER120);lane=[]
 for name,maximum,reserve in [('artifact',60,550),('delivery',110,440),('consumed_ref',110,330)]:
  end=hc.phase(maximum,reserve);h.advance(maximum-.001);hc.check(end,reserve);lane.append({'phase':name,'finish':h.t,'remaining':900-h.t})
 assert h.t<receive_end and sum(prod.PHASES117.values())==840 and prod.MAIN_REMAINDER117==575 and rc.end_mono==hc.end_mono==1900 and 900-r.t>55
 proof={'domain':'SYNTHETIC_CLOCK_API_PUBLIC_FIXTURES_ONLY','initial_host_finish':t.t,'initial_host_CAS_pairs':5,'host_events':transport.events,'recipient_end':recipient_end,'host_start':host_start,'host_lane':lane,'prequal_end':prequal_end,'runner_receive_end':receive_end,'runner_finish':r.t,'remaining':900-r.t,'original725_refused':True,'recipient_all_operational_reserves':680,'all_monotonic_ends':1900,'local_ready_API':0,'native_runtime':False};host.put(OUT/'case1-fullpath-original.json',host.can(proof));return proof
def case2():
 t=Tick(196);fixture,ingress=recipient_contract(t,'case2-known-unfit');expect(TimeoutError,lambda:prod.NativeProducer.initialize_recipient(fixture));assert ingress.effects==[]
 t=Tick(381);clock=t.clock();expect(TimeoutError,lambda:launch.prequalification_deadline120(clock.end_mono-95,types.SimpleNamespace(clock=clock)))
 t=Tick(35);clock=t.clock();saved=[];end=clock.phase(5,0)
 def late(path,deadline,missing=False):t.advance(5.1);return {'domain':'SYNTHETIC_LATE_ORIGINAL'}
 expect(prod.LateProviderRead,lambda:prod.phase_read(late,'/SYNTHETIC_CURRENT',clock,end,saved.append));assert saved[0]['value']=={'domain':'SYNTHETIC_LATE_ORIGINAL'}
 host.put(OUT/'case2-late-original.json',host.can(saved));return {'known_unfit_before_recipient_effect':True,'prequal_unfit_refused':True,'late_original_before_guard':True,'runtime_effects':0}
def case3():
 base=cfg['current_checkpoint'];version=cfg['current_version'];binding=host.current_binding(base,version,cfg,True,host.strict(pathlib.Path(cfg['payload_path']).read_bytes()));assert binding['number']==120 and binding['key']=='native120'
 refused=[]
 for mode in ['stale_direction','boolean_number','binding_pin','body_pin','clock','version','payload','arbitrary_path']:
  c=copy.deepcopy(cfg);payload=host.strict(pathlib.Path(cfg['payload_path']).read_bytes());v=version
  if mode=='stale_direction':c['direction_number']=119
  elif mode=='boolean_number':c['direction_number']=True
  elif mode=='binding_pin':c['writer_binding']['writer_sha256']='0'*64
  elif mode=='body_pin':c['writer_binding']['direction_sha256']='0'*64
  elif mode=='clock':c['deadline_utc_ms']+=1
  elif mode=='version':v-=1
  elif mode=='payload':payload['source_sha']='0'*40
  elif mode=='arbitrary_path':c['writer_binding']['writer_path']='/tmp/untrusted.py'
  expect((ValueError,KeyError),lambda:host.current_binding(base,v,c,True,payload));refused.append(mode)
 prior=pathlib.Path(cfg['writer_binding']['binding_root']).parent/'intake0077/readback423/TraceHarbor_V1_checkpoint.json';expect(ValueError,lambda:host.current_binding(prior,423,cfg))
 return {'current_native120_bound':True,'prior119sealed_refused':True,'before_effect_refusals':refused,'mock_effects':0,'actual_process_pin':binding['binding']['writer_sha256']}
def case4():
 results=[];original=host.subprocess.Popen
 for mode in ['terminal_error','timeout_partial','spawn_exception']:
  root=OUT/('case4-'+mode);root.mkdir(mode=0o700);effects=[];transport=host.HostTransport(lambda *x:effects.append(x),root,cfg)
  class Process:
   pid='SYNTHETIC_PROCESS_NOT_REAL_PID';returncode=17
   def communicate(self,timeout=None):
    if mode=='timeout_partial':raise subprocess.TimeoutExpired('SYNTHETIC_ONLY',timeout,output=b'partial-no-newline',stderr=b'original-stderr-prefix')
    return b'partial-writer-output',b'original-terminal-stderr'
   def poll(self):return None
  def spawn(*args,**kwargs):
   if mode=='spawn_exception':raise OSError(5,'SYNTHETIC_SPAWN_REFUSAL')
   return Process()
  host.subprocess.Popen=spawn
  try:expect(host.HostUnknown,lambda:transport.cas_checkpoint(cfg['current_version'],host.strict(pathlib.Path(cfg['payload_path']).read_bytes())))
  finally:host.subprocess.Popen=original
  record=host.strict((root/('writer-'+str(cfg['current_version'])+'.original.json')).read_bytes());assert not effects
  if mode=='timeout_partial':assert bytes.fromhex(record['stdout_hex'])==b'partial-no-newline' and bytes.fromhex(record['stderr_hex'])==b'original-stderr-prefix' and record['returncode'] is None and record['hidden_kill'] is False
  if mode=='terminal_error':assert record['returncode']==17 and bytes.fromhex(record['stderr_hex'])==b'original-terminal-stderr'
  results.append({'mode':mode,'original':record})
 host.put(OUT/'case4-injected-process-originals.json',host.can({'domain':'EXPLICIT_SYNTHETIC_PROCESS_ERRORS_NOT_NATIVE_TERMINALS','results':results}));return {'original_writer_errors_and_partial_return_retained':True,'no_effect_after_error':True,'hidden_kill_or_relaunch':False,'native_tools':0}
def case7():
 # New bounded recovery case. Earlier3/4 stopped at actual directory custody,
 # before these binding/error branches; no consumed operation is rerun.
 root=pathlib.Path(cfg['writer_binding']['binding_root']);assert root.stat().st_mode&0o077==0
 payload=host.strict(pathlib.Path(cfg['payload_path']).read_bytes());bound=host.current_binding(cfg['current_checkpoint'],cfg['current_version'],cfg,True,payload);assert bound['key']=='native120'
 checked=[]
 for mode in ['stale','boolean','source_body','clock','version','untrusted_path']:
  c=copy.deepcopy(cfg);v=cfg['current_version']
  if mode=='stale':c['direction_number']=119
  elif mode=='boolean':c['direction_number']=True
  elif mode=='source_body':c['writer_binding']['direction_sha256']='0'*64
  elif mode=='clock':c['deadline_utc_ms']+=1
  elif mode=='version':v-=1
  else:c['writer_binding']['writer_path']='/tmp/NOT_APPROVED'
  expect(ValueError,lambda:host.current_binding(cfg['current_checkpoint'],v,c,True,payload));checked.append(mode)
 original=host.subprocess.Popen;errors=[]
 for status in ['PARTIAL_TIMEOUT','TERMINAL17']:
  holder=OUT/('case7-'+status);holder.mkdir(mode=0o700);effects=[];transport=host.HostTransport(lambda *args:effects.append(args),holder,cfg)
  class InjectedProcess:
   pid='SYNTHETIC_NO_NATIVE_PID';returncode=17
   def poll(self):return None
   def communicate(self,timeout=None):
    if status=='PARTIAL_TIMEOUT':raise subprocess.TimeoutExpired('SYNTHETIC',timeout,output=b'partial-no-newline',stderr=b'stderr-prefix')
    return b'original-stdout-partial',b'original-error17'
  host.subprocess.Popen=lambda *args,**kwargs:InjectedProcess()
  try:expect(host.HostUnknown,lambda:transport.cas_checkpoint(cfg['current_version'],payload))
  finally:host.subprocess.Popen=original
  receipt=host.strict((holder/f'writer-{cfg["current_version"]}.original.json').read_bytes());assert not effects
  if status=='PARTIAL_TIMEOUT':assert bytes.fromhex(receipt['stdout_hex'])==b'partial-no-newline' and bytes.fromhex(receipt['stderr_hex'])==b'stderr-prefix' and receipt['returncode'] is None and not receipt['hidden_kill']
  else:assert receipt['returncode']==17 and bytes.fromhex(receipt['stderr_hex'])==b'original-error17'
  errors.append(receipt)
 host.put(OUT/'case7-unattempted-branch-originals.json',host.can({'domain':'EXPLICIT_SYNTHETIC_PROCESS_INJECTION','errors':errors,'prior_failed_cases_unchanged':True,'source_guard_weakened':False}))
 return {'current120_binding_after_actual_custody_correction':True,'new_unexecuted_refusals':checked,'partial_and_nonzero_originals':True,'effects':0,'old3_4rerun':False}
def case5():
 h=G/'genuine-holder';v=cfg['current_version'];terminal=host.strict((h/f'writer-{v}.original.json').read_bytes());writer=host.strict(bytes.fromhex(terminal['stdout_hex']));payload=host.strict(pathlib.Path(cfg['payload_path']).read_bytes());assert terminal['returncode']==0;target=pathlib.Path(writer['candidate']);actual=host.validate_writer_output(cfg['current_checkpoint'],target,v,payload,writer,cfg)
 original_read=pathlib.Path.read_bytes
 for mode in ['wholebyte','prior119mutation','current_nested_mutation']:
  modified=copy.deepcopy(actual)
  if mode=='prior119mutation':modified['native119']['SYNTHETIC_MUTATION']=True
  if mode=='current_nested_mutation':modified['native120']['source_verification']['SYNTHETIC_MUTATION']=True
  modified['self_sha256']=host.selfhash(modified);raw=host.can(modified);receipt=dict(writer)
  if mode=='wholebyte':raw+=b' '
  else:receipt.update(raw_sha256=host.sha(raw),self_sha256=modified['self_sha256'])
  def read(p):return raw if p==target else original_read(p)
  pathlib.Path.read_bytes=read
  try:expect(ValueError,lambda:host.validate_writer_output(cfg['current_checkpoint'],target,v,payload,receipt,cfg))
  finally:pathlib.Path.read_bytes=original_read
 assert original_read(target)==host.can(actual)
 return {'actual_current_writer_terminal':0,'exact_current_output_valid':True,'prior119_and_nested_unscoped_delta_refused':True,'wholebyte_mismatch_refused':True,'original_target_unchanged':True,'effects':0}
def case6():
 h=G/'genuine-holder';proof=host.strict((h/'genuine-proof.json').read_bytes());assert proof['result']=='PASS' and proof['seq']==2 and proof['context']==cfg['context']
 for seq,op in [(1,'library_replace'),(2,'library_materialize')]:
  req=host.strict((h/f'{seq}.request.original.json').read_bytes());ret=host.strict((h/f'{seq}.return.original.json').read_bytes());original=host.strict((G/f'bridge-captures/{seq}.native-tool-original.json').read_bytes());assert req['op']==ret['op']==op and req['request_digest']==ret['request_digest'] and ret['original_result']==original['original_result'] and original['transport_error'] is None and ret['late'] is False and ret['context']==cfg['context']
 terminal=host.strict((G/'bridge-captures/2.same-holder-native-return.json').read_bytes());assert terminal['exit_code']==0
 path=pathlib.Path(proof['receipt']['readback_path']);doc,raw=host.check_checkpoint(path,host.OWN,proof['receipt']['version'],proof['receipt']['sha256']);assert proof['receipt']['version']==cfg['current_version']+1
 target=pathlib.Path(cfg['writer_binding']['writer_path']).parent/f'candidate{proof["receipt"]["version"]}/TraceHarbor_V1_checkpoint.json';assert target.read_bytes()==raw
 for p in [target,path]:
  for a in proof['receipt']['xattrs']:assert os.getxattr(p,a['name']).decode()==a['value']
 old=host.strict(pathlib.Path(cfg['current_checkpoint']).read_bytes());assert old['native119']==doc['native119'];pin=host.strict((G/'bridge-source-pin.json').read_bytes());assert pin['file_sha256']==host.sha((ROOT/'diagnostic108/host118.mjs').read_bytes()) and pin['exact_function_source_equal']
 return {'necessary_current120_CAS':1,'pinned_wholebyte_self_allattrs':'PASS','same_holder_exit':0,'version':proof['receipt']['version'],'sealed119_preserved':True,'administrative_only':True,'native_runtime':False}
mode=sys.argv[2];cases=[(7,case7)] if mode=='--custody-recovery' else [(1,case1),(2,case2),(3,case3),(4,case4)] if mode=='--synthetic' else [(5,case5)] if mode=='--prepared' else [(6,case6)];results=[]
for n,fn in cases:
 out=io.StringIO();err=io.StringIO();value=None;exception=None;start=time.monotonic()
 with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
  try:value=fn()
  except BaseException as exc:exception=type(exc).__name__;traceback.print_exc()
 streams={'stdout':out.getvalue().encode(),'stderr':err.getvalue().encode()}
 for channel,raw in streams.items():host.put(OUT/f'case{n}.{channel}',raw)
 terminal={'case':n,'returncode':0 if exception is None else 1,'exception_class':exception,'elapsed_s':time.monotonic()-start,'streams':{k:{'bytes':len(raw),'sha256':host.sha(raw)} for k,raw in streams.items()}};host.put(OUT/f'case{n}.terminal.json',host.can(terminal));host.put(OUT/f'case{n}.result.json',host.can(value));results.append(terminal);print(json.dumps({'case':n,'pass':exception is None,'exception_class':exception}),flush=True)
sys.exit(0 if all(x['returncode']==0 for x in results) else 1)
