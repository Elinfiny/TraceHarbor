"""NEW118 changed interfaces, synthetic1-3 + genuine native-tool bridge4.

No native caller/capability/q/seal is fabricated. The real fourth case consumes
actual connector and SAMEholder originals produced by the code-mode bridge.
Historical117/116/native groups are references, never rerun here.
"""
import pathlib,sys,json,hashlib,importlib.util,time,copy,io,zipfile,stat,contextlib,traceback
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
host=load('test118host',ROOT/'diagnostic108/host_transport118.py');prod=load('test118admit',ROOT/'diagnostic108/admission116.py')
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
def synthetic():
 tick=Tick();run={'id':123,'run_started_at':prod.datetime.datetime.fromtimestamp(tick.utc,prod.datetime.timezone.utc).isoformat()};clock=prod.ParentClock.from_run(run,int(tick.utc+900),int(tick.utc+900),tick.wall,tick.mono)
 pins={f'fixture{n}':(1,host.sha(str(n).encode())) for n in range(6)};inputs={n:{'bytes':p[0],'sha256':p[1]} for n,p in pins.items()}
 b={'source_sha':'a'*40,'manifest_sha256':'b'*64,'run_id':'123','request_sha256':'e4b08fa3937e4c8348383a5abf934ffbf3832183fadc2907018adbc4a04a71b2'}
 core={'schema':'TRACE116_ONCE_INTENT_V1','original_writer':prod.WRITER,'source_sha':b['source_sha'],'manifest_sha256':b['manifest_sha256'],'request_sha256':b['request_sha256'],'request_bytes':4935,'lock_sha256':'fcea30197a1bf1c0eaa99314dcbf26a152935ba4535c1544b97f2f5a62f2515a','inputs':inputs,'role':'OFFLINE_COUNTER_ONLY','max_counter_invocations':1,'model_calls':0,'spend':0,'expires_utc':int(tick.utc+900),'nonce':'1'*32};b['once_receipt_sha256']=host.sha(host.can(core))
 d=dict(b,schema='TRACE116_EXTERNAL_ONCE_V1',phase='admit',original_writer=prod.WRITER,own_library_file_id=host.OWN,own_cas_version=500,own_pinned_readback_sha256='c'*64,attempt=1,role='OFFLINE_COUNTER_ONLY',request_bytes=4935,lock_sha256=core['lock_sha256'],model_calls=0,spend=0,expires_utc=core['expires_utc'],inputs=inputs,parent_clock=clock.descriptor(),once_intent=core)
 raw=host.can(d);blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();ref='refs/heads/traceharbor-counter116-admit-'+b['once_receipt_sha256']
 values=[{'ref':ref,'object':{'type':'commit','sha':'d'*40}},{'author':{'id':prod.OWNER},'committer':{'id':prod.OWNER},'parents':[{'sha':b['source_sha']}],'commit':{'tree':{'sha':'e'*40}}},{'tree':[{'path':'base','mode':'100644','type':'blob','sha':'f'*40},{'path':'counter116-admit.json','mode':'100644','type':'blob','sha':blob}]},{'tree':{'sha':'0'*40}},{'tree':[{'path':'base','mode':'100644','type':'blob','sha':'f'*40}]},{'content':prod.base64.b64encode(raw).decode(),'size':len(raw)}]
 return tick,clock,pins,b,d,values
def case1():
 tick,clock,pins,b,d,values=synthetic();calls=[];observations=[];queue=[None,None]+values
 def api(path,deadline,missing=False):
  calls.append({'path':path,'deadline':deadline,'missing':missing,'domain':'SYNTHETIC_API'});tick.advance(.1);return queue.pop(0)
 deadline=clock.phase(45,775);got,proof=prod.read_external(api,json.loads,'admit',b,pins,clock,deadline,observations.append,wait_for_admit=True,pause=tick.advance)
 assert got==d and len(calls)==8 and calls[0]['missing'] is True and calls[1]['missing'] is True and all(c['deadline']==deadline for c in calls)
 host.put(OUT/'case1-original-observations.json',host.can({'synthetic_only':True,'calls':calls,'observations':observations,'provenance':proof,'private_effects':0}))
 # Missing consumed is never retried, even when the admit barrier flag is used.
 tick,clock,pins,b,d,values=synthetic();denied=[]
 def absent(path,deadline,missing=False):denied.append(path);raise PermissionError('SYNTHETIC_NON404_DENIAL')
 original=[];expect(PermissionError,lambda:prod.read_external(absent,json.loads,'admit',b,pins,clock,clock.phase(45,775),original.append,wait_for_admit=True,pause=tick.advance));assert len(denied)==1 and original[0]['error']=='PermissionError'
 expect(ValueError,lambda:prod.read_external(absent,json.loads,'consumed',b,pins,clock,clock.phase(45,205),original.append,wait_for_admit=True,pause=tick.advance));assert len(denied)==1
 tick,clock,pins,b,d,values=synthetic();count=[]
 def missing(path,deadline,missing=False):count.append(path);tick.advance(.1);return None
 expect(TimeoutError,lambda:prod.read_external(missing,json.loads,'admit',b,pins,clock,clock.phase(45,775),lambda x:None,wait_for_admit=True,pause=tick.advance));assert len(count)==10
 tick.advance(46);expect(TimeoutError,lambda:prod.read_external(missing,json.loads,'admit',b,pins,clock,1045,lambda x:None,wait_for_admit=True,pause=tick.advance));assert len(count)==10
 return {'admit404_then_complete_validation':True,'same_original45sphase':True,'max_ref_observations':10,'non404_denial_stops':True,'no_consumed_retry':True,'expired_before_read':True,'private_effects':0,'future_native_minimum_Git_reads':26,'future_initial_poll_extra_max':9,'future_native_max_Git_reads':35}
def context():return {'domain':'SYNTHETIC_HOST118','nonce':'2'*32,'source_sha':'a'*40,'run_id':None,'once_receipt_sha256':None,'host_source_sha256':host.sha((ROOT/'diagnostic108/host_transport118.py').read_bytes())}
def response(request,original=None):return {'schema':'TRACE118_HOST_RETURN','seq':request['seq'],'context':request['context'],'op':request['op'],'request_digest':request['request_digest'],'original_result':original or {'isError':False,'structuredContent':{'content':'{"synthetic":true}'}},'transport_error':None,'late':False}
def case2():
 ledger=host.FrameLedger(OUT/'case2-good',context(),int(time.time()*1000)+60000);request=ledger.request('github_fetch',{'url':host.READ_PR});raw=host.can(response(request));assert ledger.accept(raw)=={'synthetic':True}
 prior=(ledger.root/'1.return.original.json').read_bytes();expect(host.HostUnknown,lambda:ledger.accept(raw));assert ledger.failed and (ledger.root/'1.return.original.json').read_bytes()==prior
 checks=[]
 for name in ['seq','source','op','late','exception','native_error','EOF']:
  l=host.FrameLedger(OUT/('case2-'+name),context(),int(time.time()*1000)+60000);r=l.request('github_fetch',{'url':host.READ_PR});value=response(r)
  if name=='seq':value['seq']=2
  elif name=='source':value['context']=dict(value['context'],source_sha='0'*40)
  elif name=='op':value['op']='github_create_blob'
  elif name=='late':value['late']=True
  elif name=='exception':value['transport_error']={'exception_class':'SyntheticTransportException'}
  elif name=='native_error':value['original_result']['isError']=True
  if name=='EOF':expect(host.HostUnknown,l.eof)
  else:
   actual=host.can(value);expect(host.HostUnknown,lambda:l.accept(actual));assert (l.root/'1.return.original.json').read_bytes()==actual
  assert l.failed;checks.append(name)
 effects=[];cfg={'source_sha':'a'*40,'host_source_sha256':context()['host_source_sha256'],'library_helper':str(HELPER),'library_helper_sha256':host.sha(HELPER.read_bytes()),'deadline_utc_ms':int(time.time()*1000)+60000,'domain':'READONLY_QUALIFICATION118','current_checkpoint':None}
 transport=host.HostTransport(lambda op,args:effects.append(op),OUT,cfg)
 expect(ValueError,lambda:transport.cas_checkpoint(999,{'phase':'admit'}));expect(ValueError,lambda:transport.call('github_create_blob',{'repository_full_name':host.REPO,'content':'public fixture','encoding':'utf-8'}));expect(ValueError,lambda:transport.call('not_installed_tool',{}));assert effects==[]
 return {'shared_normalizer':True,'same_holder_sequence_digest_context':True,'original_retained_before_every_refusal':True,'refused':checks,'duplicate_original_immutable':True,'typed_CAS_scope_and_readonly_guards_before_mockeffect':True,'mock_effects':0,'native_authority':False}
def case3():
 def archive(name='recipient-public.json',extra=False,link=False):
  out=io.BytesIO()
  with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
   info=zipfile.ZipInfo(name);info.external_attr=((stat.S_IFLNK if link else stat.S_IFREG)|0o600)<<16;z.writestr(info,host.can({'context':{'domain':'SYNTHETIC_PUBLIC_NOT_CERT_KEY','source_sha':'a'*40,'run_id':123},'certificate_pem':'PUBLIC_FIXTURE_NOT_CERTIFICATE'}))
   if extra:z.writestr('extra',b'PUBLIC_FIXTURE')
  return out.getvalue()
 valid=archive();assert host.validate_zip(valid,host.sha(valid))['context']['domain']=='SYNTHETIC_PUBLIC_NOT_CERT_KEY';host.put(OUT/'case3-public-fixture.zip',valid)
 refused=[]
 for name,raw,digest in [('digest',valid,'0'*64),('traversal',archive('../recipient-public.json'),None),('extra',archive(extra=True),None),('symlink',archive(link=True),None)]:
  expect(ValueError,lambda:host.validate_zip(raw,digest or host.sha(raw)));refused.append(name)
 return {'shared_actual_artifact_ZIP_validator':True,'wholebytes_crc_count_path_digest_cap':True,'refused':refused,'provider_artifact_authentication':'NOT_CLAIMED_FROM_FIXTURE','native_artifact_downloads':0}
def case4(root):
 config=host.strict((root/'config.json').read_bytes());proof=host.strict((root/'genuine-holder/genuine-proof.json').read_bytes());request=host.strict((root/'genuine-holder/1.request.original.json').read_bytes());returned=host.strict((root/'genuine-holder/1.return.original.json').read_bytes());native=host.strict((root/'bridge-captures/1.native-tool-original.json').read_bytes());terminal=host.strict((root/'bridge-captures/1.same-holder-native-return.json').read_bytes())
 assert proof['result']=='PASS' and proof['context']==config['context']==request['context']==returned['context'] and proof['seq']==request['seq']==returned['seq']==1 and proof['native_authority'] is False
 assert returned['original_result']==native['original_result'] and native['transport_error'] is None and returned['late'] is False and terminal['exit_code']==0
 actual=host.normalizer(native['original_result'],'github_fetch');assert actual['head']['sha']==config['context']['source_sha']=='300d46ef26d485162f3370aa682e3cc006d1224c' and actual['number']==18 and actual['state']=='open'
 executed=host.strict((root/'bridge-source-pin.json').read_bytes());assert executed['exact_function_source_equal'] is True and executed['file_sha256']==host.sha((ROOT/'diagnostic108/host118.mjs').read_bytes())
 return {'actual_native_connector_calls':1,'actual_tool':'github_fetch PR18','actual_same_holder_pid':proof['holder_pid'],'driver_bridge_tool_sameholder_original_return':True,'source_pin':executed,'actual_PR18_head':actual['head']['sha'],'holder_exit_code':0,'cleanup':'holder terminated; no child/native/private artifacts','native_authority':False,'effectful_qualification_calls':0}
HELPER=pathlib.Path(sys.argv[2]);mode=sys.argv[3] if len(sys.argv)>3 else '--synthetic';cases=[(4,lambda:case4(pathlib.Path(sys.argv[4])))] if mode=='--genuine-check' else [(1,case1),(2,case2),(3,case3)];results=[]
for number,fn in cases:
 out=io.StringIO();err=io.StringIO();value=None;exception=None;start=time.monotonic()
 with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
  try:value=fn()
  except BaseException as exc:exception=type(exc).__name__;traceback.print_exc()
 stdout=out.getvalue().encode();stderr=err.getvalue().encode();host.put(OUT/f'case{number}.stdout',stdout);host.put(OUT/f'case{number}.stderr',stderr)
 terminal={'case':number,'returncode':0 if exception is None else 1,'exception_class':exception,'elapsed_s':time.monotonic()-start,'streams':{n:{'bytes':len(raw),'sha256':host.sha(raw)} for n,raw in [('stdout',stdout),('stderr',stderr)]}}
 host.put(OUT/f'case{number}.terminal.json',host.can(terminal));host.put(OUT/f'case{number}.result.json',host.can(value));results.append(terminal);print(json.dumps({'case':number,'pass':exception is None,'exception_class':exception}),flush=True)
host.put(OUT/('genuine-case-summary.json' if mode=='--genuine-check' else 'synthetic-summary.json'),host.can({'cases':results,'all_pass':all(x['returncode']==0 for x in results),'old_groups_rerun':0}))
sys.exit(0 if all(x['returncode']==0 for x in results) else 1)
