"""NEW119 only: explicit synthetic clock/IPC and actual necessary publication.

No historical suite, native capability, private input or runtime authority.
Case3 consumes the real prepared writer output BEFORE the real CAS. Case4
closes that same consumed publication using actual tool/holder originals.
"""
import pathlib,sys,json,hashlib,importlib.util,time,copy,io,os,contextlib,traceback
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
host=load('test119host',ROOT/'diagnostic108/host_transport118.py');prod=load('test119admit',ROOT/'diagnostic108/admission116.py')
OUT=pathlib.Path(sys.argv[1]);OUT.mkdir(mode=0o700,exist_ok=True)
def expect(types,fn):
 try:fn()
 except types as e:return e
 raise AssertionError('Expected refusal absent')
class Tick:
 def __init__(self):self.utc=1800000000.;self.m=1000.
 def wall(self):return self.utc
 def mono(self):return self.m
 def advance(self,n):self.utc+=n;self.m+=n
def domain():
 tick=Tick();run={'id':123,'run_started_at':prod.datetime.datetime.fromtimestamp(tick.utc,prod.datetime.timezone.utc).isoformat()};clock=prod.ParentClock.from_run(run,int(tick.utc+900),int(tick.utc+900),tick.wall,tick.mono)
 pins={f'fixture{n}':(1,host.sha(str(n).encode())) for n in range(6)};inputs={n:{'bytes':p[0],'sha256':p[1]} for n,p in pins.items()}
 b={'source_sha':'a'*40,'manifest_sha256':'b'*64,'run_id':'123','request_sha256':'e4b08fa3937e4c8348383a5abf934ffbf3832183fadc2907018adbc4a04a71b2'}
 core={'schema':'TRACE116_ONCE_INTENT_V1','original_writer':prod.WRITER,'source_sha':b['source_sha'],'manifest_sha256':b['manifest_sha256'],'request_sha256':b['request_sha256'],'request_bytes':4935,'lock_sha256':'fcea30197a1bf1c0eaa99314dcbf26a152935ba4535c1544b97f2f5a62f2515a','inputs':inputs,'role':'OFFLINE_COUNTER_ONLY','max_counter_invocations':1,'model_calls':0,'spend':0,'expires_utc':int(tick.utc+900),'nonce':'1'*32};b['once_receipt_sha256']=host.sha(host.can(core))
 d=dict(b,schema='TRACE116_EXTERNAL_ONCE_V1',phase='admit',original_writer=prod.WRITER,own_library_file_id=host.OWN,own_cas_version=500,own_pinned_readback_sha256='c'*64,attempt=1,role='OFFLINE_COUNTER_ONLY',request_bytes=4935,lock_sha256=core['lock_sha256'],model_calls=0,spend=0,expires_utc=core['expires_utc'],inputs=inputs,parent_clock=clock.descriptor(),once_intent=core)
 raw=host.can(d);blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();ref='refs/heads/traceharbor-counter116-admit-'+b['once_receipt_sha256']
 values=[{'ref':ref,'object':{'type':'commit','sha':'d'*40}},{'author':{'id':prod.OWNER},'committer':{'id':prod.OWNER},'parents':[{'sha':b['source_sha']}],'commit':{'tree':{'sha':'e'*40}}},{'tree':[{'path':'base','mode':'100644','type':'blob','sha':'f'*40},{'path':'counter116-admit.json','mode':'100644','type':'blob','sha':blob}]},{'tree':{'sha':'0'*40}},{'tree':[{'path':'base','mode':'100644','type':'blob','sha':'f'*40}]},{'content':prod.base64.b64encode(raw).decode(),'size':len(raw)}]
 return tick,clock,pins,b,d,values
def case1():
 tick,clock,pins,b,d,values=domain();initial=tick.mono();calls=[];observations=[];ref_observations=[]
 def api(path,deadline,missing=False):
  calls.append({'path':path,'before':tick.mono(),'deadline':deadline,'missing':missing,'domain':'SYNTHETIC_API'});tick.advance(.1)
  if '/git/ref/' in path:
   ref_observations.append(tick.mono()-initial)
   return None if tick.mono()-initial<58 else copy.deepcopy(values[0])
  tick.advance(1.9);return copy.deepcopy(values.pop(1))
 deadline=clock.phase(90,775);got,proof=prod.read_external(api,json.loads,'admit',b,pins,clock,deadline,observations.append,wait_for_admit=True,pause=tick.advance)
 assert got==d and len(ref_observations)<=10 and 58<=ref_observations[-1]<=75.2 and tick.mono()<deadline and len(calls)==len(ref_observations)+5
 assert all(c['deadline']==deadline for c in calls);assert sum(prod.PHASES117.values())==870
 host.put(OUT/'case1-delayed-original.json',host.can({'synthetic_only':True,'calls':calls,'observations':observations,'provenance':proof,'publication_at_s':58,'validation_finished_s':tick.mono()-initial,'old_fast_schedule_cannot_reach_s':2.25,'native_timing_PASS':False}))
 # Independent changed cases: non404 denial, expired, late and consumed absent.
 checks=[]
 for mode in ['denied','expired','late','consumed']:
  tick,clock,pins,b,d,values=domain();seen=[];saved=[];end=clock.phase(90 if mode!='consumed' else 45,0)
  if mode=='expired':tick.advance(91)
  def fault(path,deadline,missing=False):
   seen.append(path)
   if mode=='denied':raise PermissionError('SYNTHETIC_DENIAL')
   if mode=='late':tick.advance(91);return values[0]
   return None
  expect((PermissionError,TimeoutError),lambda:prod.read_external(fault,json.loads,'consumed' if mode=='consumed' else 'admit',b,pins,clock,end,saved.append,wait_for_admit=mode!='consumed',pause=tick.advance))
  assert len(seen)==(0 if mode=='expired' else 1)
  if mode=='late':assert saved[-1]['value']==values[0] and saved[-1]['after']['mono']>end
  checks.append({'mode':mode,'reads':len(seen),'original':saved})
 host.put(OUT/'case1-refusals-original.json',host.can({'domain':'SYNTHETIC','checks':checks}))
 return {'delayed58s_then_full_five_GETs_before90':True,'ref_observations_s':ref_observations,'fixed_schedule':True,'denied_expired_late_and_consumed_no_retry':True,'clock_total_s':870,'native_timing_PASS':False}
def case2():
 checks=[]
 for mode in ['empty','partial','partialEOF','lateComplete','oversize']:
  fd,write=os.pipe();before=os.get_blocking(fd);ledger=host.FrameLedger(OUT/('case2-'+mode),{'domain':'SYNTHETIC_IO119'},int(time.time()*1000)+30000);bridge=host.StdioBridge(ledger,input_fd=fd,output=io.BytesIO());ledger.bind_phase(time.monotonic()+.03)
  payload=b'partial-no-newline' if mode in ('partial','partialEOF') else b''
  if payload:os.write(write,payload)
  if mode=='partialEOF':os.close(write);write=None
  if mode=='lateComplete':
   # Explicit synthetic selector shifts the response beyond the original phase.
   original_select=host.selectors.DefaultSelector
   class LateSelector(original_select):
    def select(self,timeout=None):
     os.write(write,b'{"late":"synthetic"}\n');time.sleep(.04);return super().select(0)
   host.selectors.DefaultSelector=LateSelector
  if mode=='oversize':
   # Explicit finite synthetic os.read adapter, not a large blocking pipe write.
   original_read=host.os.read;os.write(write,b'x')
   host.os.read=lambda f,n:b'x'*n if f==fd else original_read(f,n)
  started=time.monotonic()
  try:expect((host.HostUnknown,ValueError),lambda:bridge('github_fetch',{'url':host.READ_PR}))
  finally:
   if mode=='lateComplete':host.selectors.DefaultSelector=original_select
   if mode=='oversize':host.os.read=original_read
  assert time.monotonic()-started<1 and ledger.failed and os.get_blocking(fd)==before
  if mode in ('partial','partialEOF'):assert (ledger.root/'1.partial.original.bin').read_bytes()==payload
  first=list(ledger.root.glob('1.*'));expect(host.HostUnknown,lambda:bridge('github_fetch',{'url':host.READ_PR}));assert list(ledger.root.glob('1.*'))==first
  receipt=json.loads((ledger.root/'1.fd-restoration.json').read_text());assert receipt['restore_attempts']==1 and receipt['cleanup_errors']==[]
  checks.append({'mode':mode,'bounded':True,'restore':receipt,'raw_chunks':len(list(ledger.root.glob('1.chunk*.original.bin')))})
  os.close(fd)
  if write is not None:os.close(write)
 # A real borrowed PTY also restores termios once, on deadline UNKNOWN.
 master,slave=os.openpty();attrs=host.termios.tcgetattr(slave);blocking=os.get_blocking(slave);ledger=host.FrameLedger(OUT/'case2-termios',{'domain':'SYNTHETIC_PTY119'},int(time.time()*1000)+30000);ledger.bind_phase(time.monotonic()+.02)
 expect(host.HostUnknown,lambda:host.StdioBridge(ledger,slave,io.BytesIO())('github_fetch',{'url':host.READ_PR}));assert host.termios.tcgetattr(slave)==attrs and os.get_blocking(slave)==blocking;os.close(master);os.close(slave)
 host.put(OUT/'case2-original-checks.json',host.can({'domain':'SYNTHETIC_IO_REAL_LOCAL_FD','checks':checks,'termios_restored':True,'native_tools':0}))
 return {'bounded_partial_empty_EOF_late_oversize':True,'every_raw_chunk_preserved':True,'borrowed_FD_and_termios_restored_once':True,'no_next_operation_after_UNKNOWN':True,'native_effects':0}
def case3(root):
 cfg=host.strict((root/'config.json').read_bytes());holder=root/'genuine-holder';version=cfg['current_version'];native=host.strict((holder/f'writer-{version}.original.json').read_bytes());provenance=host.strict((holder/f'writer-{version}.provenance.json').read_bytes());writer=host.strict(bytes.fromhex(native['stdout_hex']));payload=host.strict(pathlib.Path(cfg['payload_path']).read_bytes());target=pathlib.Path(writer['candidate'])
 original,current=host.writer_sources(cfg);assert native['status']=='TERMINAL' and native['returncode']==0 and provenance['actual_invoked_source_sha256']==host.sha(current.read_bytes()) and provenance['original_source_sha256']==host.ORIGINAL_WRITER_SHA256
 actual=host.validate_writer_output(cfg['current_checkpoint'],target,version,payload,writer,cfg['writer_sha256']);effects=[]
 for mode in ['wholebyte','unscoped_delta']:
  modified=copy.deepcopy(actual)
  if mode=='unscoped_delta':modified['native118']['SYNTHETIC_UNSCOPED_DELTA']=True
  modified['self_sha256']=host.selfhash(modified);raw=host.can(modified);fixture=OUT/f'case3-{mode}.SYNTHETIC.json';host.put(fixture,raw)
  receipt=dict(writer)
  if mode=='wholebyte':raw+=b' ';fixture.write_bytes(raw)
  else:receipt.update(raw_sha256=host.sha(raw),self_sha256=modified['self_sha256'])
  expect(ValueError,lambda:host.validate_writer_output(cfg['current_checkpoint'],fixture,version,payload,receipt,cfg['writer_sha256']))
  assert not effects
 expect(ValueError,lambda:host.writer_sources(dict(cfg,writer_sha256='0'*64)));assert not effects
 return {'real_prepared_writer_terminal':0,'actual_process_sha256':provenance['actual_invoked_source_sha256'],'original_authentic_preimage_sha256':host.ORIGINAL_WRITER_SHA256,'binding_adaptation':'EXPLICIT_EXACT_DIFF_NOT_RELABELED_ORIGINAL','wholebyte_and_unscoped_delta_refused_before_mockeffect':True,'mockeffects':0,'original118_immutable':True}
def case4(root):
 cfg=host.strict((root/'config.json').read_bytes());holder=root/'genuine-holder';proof=host.strict((holder/'genuine-proof.json').read_bytes());native=[]
 assert proof['result']=='PASS' and proof['seq']==2 and proof['context']==cfg['context'] and proof['transport_counts']['CAS']==proof['transport_counts']['materialize']==1
 for seq,op in [(1,'library_replace'),(2,'library_materialize')]:
  req=host.strict((holder/f'{seq}.request.original.json').read_bytes());ret=host.strict((holder/f'{seq}.return.original.json').read_bytes());orig=host.strict((root/f'bridge-captures/{seq}.native-tool-original.json').read_bytes());assert ret['original_result']==orig['original_result'] and ret['op']==req['op']==op and ret['request_digest']==req['request_digest'] and ret['context']==req['context']==cfg['context'] and ret['late'] is False and orig['transport_error'] is None;native.append(ret)
 terminal=host.strict((root/'bridge-captures/2.same-holder-native-return.json').read_bytes());assert terminal['exit_code']==0
 pub=host.normalizer(native[0]['original_result'],'library_replace');read=host.normalizer(native[1]['original_result'],'library_materialize');assert pub['current_version_number']==read['current_version_number']==proof['receipt']['version']==cfg['current_version']+1
 assert pub['file_id']==read['file_id'] and pub['xattrs']==read['xattrs'];target=pathlib.Path(proof['receipt']['readback_path']);doc,raw=host.check_checkpoint(target,host.OWN,pub['current_version_number'],proof['receipt']['sha256'])
 candidate=pathlib.Path(cfg['writer_path']).parent/f'candidate{pub["current_version_number"]}/TraceHarbor_V1_checkpoint.json';assert candidate.read_bytes()==raw
 for path in [target,candidate]:
  for a in pub['xattrs']:assert os.getxattr(path,a['name']).decode()==a['value']
 executed=host.strict((root/'bridge-source-pin.json').read_bytes());assert executed['exact_function_source_equal'] is True and executed['file_sha256']==host.sha((ROOT/'diagnostic108/host118.mjs').read_bytes())
 return {'actual_CAS':1,'actual_pinned_readback':1,'wholebyte_self_allattrs':'PASS','same_holder_exit_code':0,'seq_operation_context_digest_closure':'PASS','version':pub['current_version_number'],'administrative_effect_only':True,'native_authority':False,'source_identical_bridge':executed}
mode=sys.argv[2];root=pathlib.Path(sys.argv[3]) if len(sys.argv)>3 else None
cases=[(1,case1),(2,case2)] if mode=='--synthetic' else [(3,lambda:case3(root))] if mode=='--prepared-writer' else [(4,lambda:case4(root))]
results=[]
for number,fn in cases:
 out=io.StringIO();err=io.StringIO();value=None;exception=None;start=time.monotonic()
 with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
  try:value=fn()
  except BaseException as exc:exception=type(exc).__name__;traceback.print_exc()
 stdout=out.getvalue().encode();stderr=err.getvalue().encode();host.put(OUT/f'case{number}.stdout',stdout);host.put(OUT/f'case{number}.stderr',stderr)
 terminal={'case':number,'returncode':0 if exception is None else 1,'exception_class':exception,'elapsed_s':time.monotonic()-start,'streams':{n:{'bytes':len(raw),'sha256':host.sha(raw)} for n,raw in [('stdout',stdout),('stderr',stderr)]}}
 host.put(OUT/f'case{number}.terminal.json',host.can(terminal));host.put(OUT/f'case{number}.result.json',host.can(value));results.append(terminal);print(json.dumps({'case':number,'pass':exception is None,'exception_class':exception}),flush=True)
sys.exit(0 if all(x['returncode']==0 for x in results) else 1)
