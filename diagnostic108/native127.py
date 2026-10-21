"""Fixed native loader/port for private127 review. NO native admission127.

No external object, API dictionary, serialized proof, event selector or caller
module registers a native host. Current authenticated owned direction, exact
source manifest, whole grouped contract and whole call cap are independent gates.
"""
import base64,copy,importlib.util,io,json,os,pathlib,runpy,stat,subprocess,sys,time,types,zipfile
ROOT=pathlib.Path(__file__).resolve().parent
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
t146=load('trace146_native_timing',ROOT/'timing146.py')
g=load('trace127_fixed_integrated',ROOT/'integrated127.py');c=g.c;can=c.can;sha=c.sha
BASE_SHA='dbec3c2929f09511240924f00f10e2a1fea376a255a8f2790fe9e1a8ca0f671d'
base=load('trace127_original118',ROOT/'host_transport118.py');h154=load('trace154_explicit149_prestart',ROOT/'prestart154.py')
p150=load('trace150_publication_protocol',ROOT/'publication150.py')
preflight152=load('trace152_native_authority_preflight',ROOT/'preflight127.py')
_normalizer118=base.normalizer
def normalizer127(original,kind):
 if kind=='library_replace':return p150.normalize150(original)
 if kind=='github_fetch' and type(original) is dict and original.get('schema')=='TRACE152_AUTHENTIC_READ_PAIR':
  if set(original)!={'schema','value','current','native_authority'} or original['native_authority'] is not False:raise ValueError('Closed authentic current/proof pair')
  return {'source_value152':_normalizer118(original['value'],kind),'current_original152':original['current']}
 if kind=='library_materialize' and type(original) is dict and original.get('schema')=='TRACE152_AUTHENTIC_PHASE_READBACK':
  if set(original)!={'schema','current','native_authority'} or original['native_authority'] is not False:raise ValueError('Closed authentic whole phase current readback')
  ts=original['current'].get('structuredContent',{}).get('transfers',[])
  if len(ts)!=4 or len([t for t in ts if t['library_file_id']==base.OWN])!=1:raise ValueError('Actual unique own+current three phase readback')
  return {'source_value152':next(t for t in ts if t['library_file_id']==base.OWN),'current_original152':original['current']}
 if kind=='github_ref_absence136':
  if type(original) is not dict or set(original)!={'schema','absence','current','native_authority'} or original['schema']!='TRACE152_AUTHENTIC_COMPOUND_ORIGINAL' or original['native_authority'] is not False:raise ValueError('Whole separate authentic152 originals')
  absent=g.p133.g136.absent_original136(original['absence']);return dict(absent,current_original152=original['current'])
 if kind=='github_fetch_workflow_run_artifacts':
  if type(original) is not dict or original.get('isError') or type(original.get('structuredContent',{}).get('content')) is not str:raise ValueError('Whole original artifact REST body with total_count')
  return base.strict(original['structuredContent']['content'])
 if kind!='browser_js':return _normalizer118(original,kind)
 if type(original) is not dict or original.get('isError'):raise ValueError('Actual UI tool error')
 value=original.get('structuredContent')
 if type(value) is not dict:
  blocks=original.get('content',[])
  if len(blocks)!=1 or blocks[0].get('type')!='text':raise ValueError('Exact current source UI data result; no arbitrary text/event selector')
  value=base.strict(blocks[0]['text'])
 if set(value)!={'schema','selected_run_id','source_sha','attempt','once_receipt_sha256'} or value['schema']!='TRACE127_UI_DISPATCH_DATA' or type(value['selected_run_id']) is not int or value['selected_run_id']<=0:raise ValueError('Full source-produced actual selected UI run data')
 return value
base.normalizer=normalizer127
class ActualClock127:
 mono=staticmethod(time.monotonic);wall=staticmethod(time.time)
class CanonicalReader127:
 """Controller returned PUBLIC metadata/encrypted DATA, in fresh private0700.
 Existing phase/proof/private-input files still require their original0600 IO.
 Platform apply_patch chooses file mode; the source requires no group/world
 WRITE, own UID, singlelink, exact owned0700 parent and complete unchanged EOF.
 This source-only canonical variant is part of the new independent contract.
 """
 def __init__(self,root):self.root=pathlib.Path(root)
 def read(self,path):
  p=pathlib.Path(path);root=self.root.lstat();s=p.lstat()
  if self.root.is_symlink() or not stat.S_ISDIR(root.st_mode) or root.st_uid!=os.getuid() or root.st_mode&0o077 or p.parent!=self.root or p.is_symlink() or p.resolve()!=p or not stat.S_ISREG(s.st_mode) or s.st_uid!=os.getuid() or s.st_nlink!=1 or s.st_mode&0o022 or s.st_size>2097152:raise ValueError('Exact current controller canonical custody')
  fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
  try:
   before=os.fstat(fd);raw=os.read(fd,2097153);extra=os.read(fd,1);after=os.fstat(fd)
  finally:os.close(fd)
  end=p.lstat()
  if extra or len(raw)!=s.st_size or (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)!=(before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns) or (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns) or end.st_ino!=s.st_ino:raise ValueError('Complete stable canonical EOF')
  return raw
class Ledger127(base.FrameLedger):
 def request(self,op,args):
  if self.failed or self.pending is not None or self.remaining()<=0:raise RuntimeError('Source/phase/sequence unavailable')
  port=self.port;self.seq+=1
  frame={'schema':'TRACE118_HOST_REQUEST','seq':self.seq,'context':self.context,'op':op,'args':args,'deadline_utc_ms':min(self.deadline_ms,int((time.time()+min(15,self.remaining()))*1000)),'phase_deadline_mono':self.phase_mono,'phase_deadline_utc_ms':min(self.deadline_ms,int((time.time()+self.remaining())*1000)),'inventory_call_id':port.current_id,'inventory_sha256':sha(can(port.inventory.plan))}
  if self.seq==1:
   frame['runtime_binding133']={'schema':'TRACE133_SOURCE_RUNTIME_FRAME','static_config_sha256':sha(port.static_config133),'context_sha256':sha(can(self.context)),'context':copy.deepcopy(self.context),'deadlineUtcMs':self.deadline_ms,'sourceSha':port.source,'sourceTree':port.macro.context['source_tree'],'dispatchKind136':port.config['ui_dispatch127'].get('kind','browser135'),'uiDispatchArgs':copy.deepcopy(port.config['ui_dispatch127']['args']),'manifestSha256':port.macro.context['manifest_sha256'],'onceExpiresUtc':port.macro.context['expires_utc'],'coordinatorCutoffUtc':port.config['coordinator_cutoff_utc']}
  frame['request_digest']=sha(can(frame));raw=can(frame)
  if len(raw)>min(base.MAX_FRAME,262144):raise ValueError('Finite complete source frame within declared tool-output cap')
  base.put(self.root/(str(self.seq)+'.request.original.json'),raw);self.pending=frame;return frame
helper128=load('trace128_native_helper',ROOT/'helper_channel128.py')
class NativePort127:
 def __init__(self,key,cfg,manifest,provider):
  if key is not g._SEAL:raise TypeError('Fixed internal source loader only')
  self.config=cfg;self.manifest_sha=sha(can(manifest));self.provider=provider;self.source=cfg['source_sha'];self.parent_mono=cfg['integration_context127']['parent_mono'];self.phase_mono=self.parent_mono;self._checkpoint=pathlib.Path(cfg['current_checkpoint']);self._version=cfg['current_version'];self.root=pathlib.Path(cfg['holder_root']);self.current_id=None;self.chunk=0;self.current_original=None
  # No alternate independent host/provider call counter exists here.
  self.inventory=c.Inventory127(c.inventory127(),'ACTUAL_SOURCE_PRIVATE',cfg['native_admission127']['inclusive_cap'])
  self.canonical127=types.SimpleNamespace(io=CanonicalReader127(cfg['capture_directory']))
  self.layout=base.validate_transfer_layout(cfg['writer_binding'],self.root)
  self.ledger=Ledger127(self.root/'frames',cfg['context'],cfg['deadline_utc_ms']);self.ledger.port=self;self.bridge=base.StdioBridge(self.ledger)
  original_put=base.put
  def budgeted_put(path,raw):
   name=pathlib.Path(path).name
   suffix='request' if '.request.original.' in name else 'return' if '.return.original.' in name else 'validated' if name.endswith('.accepted.json') else 'restore' if name.endswith('.fd-restoration.json') else None
   if '.chunk' in name:
    if self.chunk>=8:
     self.inventory.claim(self.current_id+'/failure-partial');original_put(path,raw);raise RuntimeError('Eight precommitted IPC chunks exhausted; overflow original retained, no retry')
    suffix='chunk/'+str(self.chunk);self.chunk+=1
   if name.endswith('.partial.original.bin'):suffix='failure-partial'
   if name.endswith('.stream-UNKNOWN.json'):suffix='failure-status'
   if name.endswith('.read-exception.original.json'):suffix='failure-read'
   if '.duplicate-' in name:suffix='failure-duplicate'
   if suffix is None:raise RuntimeError('Unexpected unplanned frame evidence; canonical prefix preserved')
   self.inventory.claim(self.current_id+'/'+suffix);return original_put(path,raw)
  base.put=budgeted_put
 def bind(self,macro):self.macro=macro
 def bind_interval(self,phase):
  self.phase_mono=min(phase['end_mono'],self.ledger.parent_mono);self.ledger.bind_phase(self.phase_mono)
 def deadline(self):self.macro.guard()
 def invoke(self,id,op,args):
  self.current_id=id;self.chunk=0
  # Source-closed ops are encoded in caller127, including exact fixedbrowser
  # dispatch. Shared committed tickets travel with the frame; no second budget.
  if op not in base.OPS:base.OPS=tuple(base.OPS)+(op,)
  value=self.bridge(op,args)
  if type(value) is dict and set(value)=={'source_value152','current_original152'}:
   self.refresh_authority152(value['current_original152'],id,phase_readback=id.endswith('/readback'));value=value['source_value152']
  request=base.strict((self.ledger.root/(str(self.ledger.seq)+'.request.original.json')).read_bytes());frame=base.strict((self.ledger.root/(str(self.ledger.seq)+'.return.original.json')).read_bytes())
  self.current_original={'request':request,'frame':frame,'canonical_path':str(pathlib.Path(self.config['capture_directory'])/(str(request['seq'])+'.canonical-native-original.json'))}
  return value
 def helper(self,phase,role,argv,input=None):
  self.inventory.claim(phase+'/'+role);started=time.monotonic();proc=None
  try:
   proc=subprocess.Popen(argv,stdin=subprocess.PIPE if input is not None else subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
   stdout,stderr=proc.communicate(input=input,timeout=min(10 if role=='writer' else 5,max(.001,self.macro.remaining())))
   original={'status':'TERMINAL','returncode':proc.returncode,'stdout_hex':stdout.hex(),'stderr_hex':stderr.hex(),'elapsed_s':time.monotonic()-started}
  except BaseException as exc:
   original={'status':'UNKNOWN_NO_RETRY','exception_class':type(exc).__name__,'stdout_hex':(getattr(exc,'stdout',None) or b'').hex(),'stderr_hex':(getattr(exc,'stderr',None) or b'').hex(),'returncode':None if proc is None else proc.poll(),'hidden_kill':False}
  self.macro.store.save(phase+'/'+role+'/original',original)
  self.deadline()
  if original['status']!='TERMINAL' or original['returncode']!=0:raise RuntimeError('Helper original retained; never rerun')
  return bytes.fromhex(original['stdout_hex'])
 def current(self):return h154.current_binding154(base,self._checkpoint,self._version,self.config)
 def original_reference(self,id):
  self.inventory.claim(id+'/canonical-reference');seq=self.ledger.seq;request=base.strict((self.ledger.root/(str(seq)+'.request.original.json')).read_bytes());path=str(pathlib.Path(self.config['capture_directory'])/(str(seq)+'.canonical-native-original.json'));raw=self.canonical127.io.read(path);d=base.strict(raw)
  expected={'context_sha256':sha(can(self.config['context'])),'operation':request['op'],'seq':seq,'tool':'exec_command' if request['op']=='library_replace' else request['op'],'call_id':request['request_digest']}
  if d.get('identity')!=expected or request.get('inventory_call_id')!=id:raise ValueError('Canonical actual call identity, never equal-byte merge')
  if self.current_original and self.current_original['request']['seq']==seq and d.get('original')!=self.current_original['frame']['original_result']:raise ValueError('Actual complete saved native original differs')
  return {'id':id,'identity':expected,'path':path,'bytes':len(raw),'sha256':sha(raw),'canonical':True}
 def verify_reference(self,r):
  raw=self.canonical127.io.read(r['path'])
  if len(raw)!=r['bytes'] or sha(raw)!=r['sha256'] or base.strict(raw)['identity']!=r['identity']:raise ValueError('Whole prior canonical original before next consumed phase')
  return r
 def refresh_authority152(self,original152,scope,phase_readback=False):
  ts152=original152.get('structuredContent',{}).get('transfers',[])
  if original152.get('isError') or original152.get('tool_throw') or len(ts152)!=4 or {t['library_file_id'] for t in ts152}!=set(preflight152.a152.IDS):raise ValueError('Whole actual fresh current four-document original before every Git create')
  docs152={};proofs152={}
  for i,t in enumerate(ts152):
   ident={'phase':self.macro.active['name'],'run':self.macro.context['once_receipt_sha256'],'source':self.source,'call':'authority152/'+scope+'/helper-original/'+str(i)}
   helper128.run_helper128(self.config['library_helper'],self.config['library_helper_sha256'],pathlib.Path(t['workspace_path']),t['library_file_id'],t['xattrs'],ident,lambda identity,record:self.macro.store.save(ident['call'],{'identity':identity,'original':record}))
   docs152[t['library_file_id']],proofs152[t['library_file_id']]=preflight152.a152.proof152(t['workspace_path'],t)
  own152=docs152[base.OWN];version=self._version+(1 if phase_readback else 0)
  target=pathlib.Path(self.config['writer_binding']['writer_path']).parent/('candidate'+str(version))/'TraceHarbor_V1_checkpoint.json' if phase_readback else self._checkpoint
  if proofs152[base.OWN]['version']!=version or own152!=base.strict(target.read_bytes()):raise ValueError('Exact current own target whole bytes before every Git create')
  auth152=preflight152.a152.verify152(own152,docs152,proofs152,self.static152,(ROOT/'manifest.json').read_bytes());self.macro.store.save('authority152/'+scope+'/verify',auth152);self.deadline()
  request152=base.strict((self.ledger.root/(str(self.ledger.seq)+'.request.original.json')).read_bytes())
  if time.time()*1000>=request152['deadline_utc_ms']:raise TimeoutError('Whole current152 checks exceeded same original15s frame; no next create')
  self.authority152_last={'scope':scope,'seq':self.ledger.seq,'own_version':version,'authority':auth152}
 def before_effect(self,id,op,args):
  current=self.current();payload=current['doc'][current['key']]['records'][-1]['payload'];intent=payload.get('phase_intent127');phase=self.macro.active['name']
  preflight152.a152.require_predecessor152(id,phase,self._version,self.ledger.seq,getattr(self,'authority152_last',None))
  if not intent or intent['phase']!=phase or intent['plan_sha256']!=self.macro.plan_sha or phase not in self.macro.consumed or intent['context']!=self.macro.context or current['doc']['guard']['operation_id']!=self.macro.context['direction_id']:raise ValueError('Same actual consumed whole phase/current authority before EVERY Git effect')
  manifest=base.strict((ROOT/'manifest.json').read_bytes())
  if sha(can(manifest))!=self.manifest_sha:raise ValueError('Manifest drift before effect')
  for name,pin in manifest['source_files'].items():
   raw=(ROOT.parent/name).read_bytes()
   if len(raw)!=pin['bytes'] or sha(raw)!=pin['sha256']:raise ValueError('Exact source drift before individual effect')
  local=self.macro.store.records[phase+'/intent'];raw=self.macro.store.io.read(local['path'])
  if sha(raw)!=local['sha256'] or base.strict(raw)['original']!=intent:raise ValueError('No event JSON recreation/changed durable intent')
  self.macro.store.save(id+'/pre-effect-guard',{'current_version':self._version,'source_manifest_sha256':self.manifest_sha,'consumed_intent_sha256':sha(can(intent)),'tool':op,'args_sha256':sha(can(args))})
 def attrs(self,phase,role,path,metadata):
  self.helper(phase,role,[sys.executable,self.config['library_helper'],'apply-xattrs',str(path),metadata['library_file_id']],can(metadata.get('xattrs',[])))
  if os.getxattr(path,'user.library-file-id').decode()!=metadata['library_file_id']:raise ValueError('Positive actual Library identity')
  for x in metadata.get('xattrs',[]):
   if os.getxattr(path,x['name']).decode()!=x['value']:raise ValueError('ALL returned actual attrs')
 def cas(self,phase,version,payload):
  cas_start=time.monotonic()
  if version!=self._version or payload['phase_intent127']['plan_sha256']!=self.macro.plan_sha:raise ValueError('Exact whole live typed phase/version')
  current=self.current();self.helper(phase,'guard-before',[sys.executable,str(ROOT/'native127.py'),'guard',self.config['config_path'],str(self._checkpoint),str(version)])
  self.macro.store.save(phase+'/writer-input',payload)
  request=pathlib.Path(self.macro.store.records[phase+'/writer-input']['path'])
  # Canonical evidence is an identity wrapper; original producer receives a
  # separately O_EXCL serialized payload, budgeted as source evidence below.
  payloadpath=self.root/(phase+'-payload.json');c.DiskOriginalIO127().write_once(str(payloadpath),can(payload))
  writer=pathlib.Path(current['binding']['writer_path']);target=writer.parent/('candidate'+str(version+1))/'TraceHarbor_V1_checkpoint.json'
  if target.exists():raise RuntimeError('No existing candidate adoption/restart')
  stdout=self.helper(phase,'writer',[sys.executable,str(writer),'build',str(self._checkpoint),str(version),'PUBLISH_INTENT',str(payloadpath)]);r=base.strict(stdout)
  raw=target.read_bytes();d=base.strict(raw);wanted=copy.deepcopy(current['doc']);key=current['key'];utc=d['events'][-1]['utc'];n=wanted[key]
  n['records'].append({'phase':'PUBLISH_INTENT','payload':payload});n['phase']='PUBLISH_INTENT';n['previous_checkpoint']={'version':version,'raw_sha256':sha(current['raw']),'self_sha256':wanted['self_sha256']};n['writer_sha256']=current['binding']['writer_sha256'];n['phase_history'].append({'phase':'PUBLISH_INTENT','utc':utc,'actual_own_version':version+1})
  wanted['events'].append({'phase':'PUBLISH_INTENT','utc':utc,'delivery_id':current['direction']['id'],'own_version':version+1,'source':'CURRENT Auditor'+str(current['binding']['auditor_version'])+' direction'+str(current['number']),'scope':'SAME_HOST_PRODUCER_COUNTER_CONTRACT_REVIEW_SOURCE'})
  wanted['guard'].update(operation_id=current['direction']['id'],operation_state='PUBLISH_INTENT',epoch_checkpoint_counter=version+1,checkpoint_fresh='EXACT_CAS_AND_PINNED_FULLBYTE_SELF_ALLATTRS_READBACK');wanted['state']='NATIVE'+str(current['number'])+'_PUBLISH_INTENT';wanted['self_sha256']=base.selfhash(wanted)
  if r.get('candidate')!=str(target) or r.get('version')!=version+1 or r.get('raw_sha256')!=sha(raw) or r.get('self_sha256')!=d['self_sha256'] or r.get('preservation')!='PASS' or d!=wanted:raise ValueError('Exact original writer/full preservation before CAS')
  self.macro.store.save(phase+'/candidate-verify',{'bytes':len(raw),'sha256':sha(raw),'self_sha256':d['self_sha256'],'preservation':'PASS'})
  dest=self.layout['transfer']/('group127-upload-'+str(version));dest.mkdir(mode=0o700,exist_ok=False);upload=dest/target.name;c.DiskOriginalIO127().write_once(str(upload),raw)
  for attr in os.listxattr(target):os.setxattr(upload,attr,os.getxattr(target,attr))
  self.macro.store.save(phase+'/transfer-copy',{'path':str(upload),'bytes':len(raw),'sha256':sha(raw)})
  pub=self.macro.call(phase+'/CAS','library_replace',{'library_file_id':base.OWN,'file':str(upload),'expected_current_version':version,'version_reason':'Actual independently admitted grouped phase consumed before first effect'})
  if pub.get('status')!='succeeded' or pub.get('library_file_id')!=base.OWN or pub.get('current_version_number')!=version+1:raise ValueError('Actual conditional publication original')
  proof150=pub['publication150']['upload']
  if proof150['sha256']!=sha(raw) or proof150['bytes']!=len(raw) or proof150['self_sha256']!=d['self_sha256'] or proof150['expected_current_version']!=version:raise ValueError('Actual prepared upload fullbody/expectedversion')
  self.attrs(phase,'attrs-candidate',target,pub);self.attrs(phase,'attrs-upload',upload,pub)
  tr=self.macro.call(phase+'/readback','library_materialize',{'items':[{'library_file_id':base.OWN,'file_id':pub['file_id'],'file_name':pub['file_name']}],'destination':{'directory':str(self.layout['transfer']/('group127-readback-'+str(version+1)))}})
  if tr['file_id']!=pub['file_id'] or tr['current_version_number']!=version+1 or tr['library_file_id']!=base.OWN or any({a['name']:a['value'] for a in pub['xattrs']}.get(a['name'])!=a['value'] for a in tr['xattrs']):raise ValueError('Pinned peritem current CAS identity')
  path=pathlib.Path(tr['workspace_path']);expected=self.layout['transfer']/('group127-readback-'+str(version+1))/pub['file_name']
  if path!=expected or path.is_symlink() or path.resolve()!=path:raise ValueError('Only exact selected disjoint readback')
  self.attrs(phase,'attrs-readback',path,tr);check,observed=base.check_checkpoint(path,base.OWN,version+1,sha(raw))
  if observed!=raw or check!=d:raise ValueError('Wholebyte/self original producer readback')
  self.macro.store.save(phase+'/readback-verify',{'version':version+1,'file_id':pub['file_id'],'bytes':len(raw),'sha256':sha(raw),'self_sha256':d['self_sha256'],'wholebyte_self_allattrs':'PASS'})
  self._checkpoint=path;self._version=version+1
  self.helper(phase,'guard-after',[sys.executable,str(ROOT/'native127.py'),'guard',self.config['config_path'],str(path),str(version+1)])
  if time.monotonic()-cas_start>t146.CAS:raise TimeoutError('Whole146 CAS/readback cutoff; appliedCAS retained no replay')
  return {'version':version+1,'sha256':sha(raw),'wholebyte_self_allattrs':'PASS','intent_sha256':sha(can(payload['phase_intent127']))}
 def dispatch(self):
  ui=self.config['ui_dispatch127']
  if ui.get('kind')=='git_create136':
   args=ui['args'];helper=g.p133.g136;binding=helper.binding136(args)
   if ui['source_sha']!=self.source or ui['once_receipt_sha256']!=self.macro.context['once_receipt_sha256']:raise PermissionError('Same source original once, no manual conflict claim')
   url='https://api.github.com/repos/'+g.REPO+'/git/ref/heads/'+args['branch_name']
   absent=self.macro.call('dispatch136/ref-absence','github_ref_absence136',{'url':url})
   if set(absent)!={'absent','current_original152'} or absent['absent'] is not True:raise ValueError('Genuine absent ref plus authentic fresh CURRENT152')
   self.refresh_authority152(absent['current_original152'],'precreate')
   #138 conservative absolute observation origin BEFORE the one consumed create.
   observation_start=time.monotonic();observation_end=min(observation_start+60,self.phase_mono,self.parent_mono)
   if self.macro.remaining()<15+t146.DISPATCH+t146.ADMIT_MIN:raise TimeoutError('Original146 suffix immediately before sole create')
   created=self.macro.call('dispatch136/create-ref','github_create_dispatch136',args)
   helper.created136(created,args)
   proof=self.macro.call('dispatch136/ref-proof','github_fetch',{'url':url});helper.ref136(proof,args)
   self.macro.store.save('dispatch136/created-ref-original',{'created':created,'ref':proof,'binding':binding})
   import urllib.parse
   query=urllib.parse.urlencode({'event':'create','head_sha':self.source,'branch':args['branch_name'],'per_page':100})
   run=None;last_observation=None
   for n in range(4):
    if n:
     target=last_observation+15
     if target>=observation_end:raise g.Pending127('Original absolute60 create window exhausted; no later observation or replay')
     self.inventory.claim('dispatch136/delay/'+str(n-1));self.delay_until(target)
    if time.monotonic()>=observation_end:raise g.Pending127('Original absolute60 create window exhausted before read')
    listed=self.macro.call('dispatch136/runs/'+str(n),'github_fetch',{'url':'https://api.github.com/repos/'+g.REPO+'/actions/runs?'+query})
    last_observation=time.monotonic()
    # macro.call has retained the complete original before this late classification.
    if last_observation>=observation_end:raise g.Pending127('Late original retained; no classification as timely run or retry')
    run=helper.selected136(listed,binding)
    if run is not None:break
   if run is None:raise g.Pending127('Finite four actual create-run observations exhausted; ref consumed, never recreate')
   selected={'schema':'TRACE136_GIT_DISPATCH_DATA','selected_run_id':run['id'],'source_sha':self.source,'attempt':1,'once_receipt_sha256':binding['once_receipt_sha256'],'branch':binding['branch']}
   self.macro.store.save('dispatch136/selected-run-original',{'binding':binding,'selected':selected,'run':run})
  else:
   ui=self.config['ui_dispatch127']
   if ui.get('master_terminal_no_input_conflict') is not True or ui['source_sha']!=self.source or ui['once_receipt_sha256']!=self.config['integration_context127']['once_receipt_sha256'] or ui['script_sha256']!=sha(ui['args']['code'].encode()):raise PermissionError('Actual CURRENT exact UI/source/unusedonce/Master conflict evidence required')
   selected=self.macro.call('dispatch/UI','browser_js',ui['args'])
   # Actual selected run_id is supplied by the fixed preloaded UI script's
   # authenticated original result; never latest-list search or PR-filter API.
   if selected['source_sha']!=self.source or selected['attempt']!=1 or selected['once_receipt_sha256']!=self.macro.context['once_receipt_sha256']:raise ValueError('Actual selected UI source/attempt/once')
   runid=selected['selected_run_id']
   if type(runid) is not int or runid<=0:raise ValueError('Actual selected run returned by exact UI route')
   run=self.macro.call('dispatch/run','github_fetch',{'url':'https://api.github.com/repos/'+g.REPO+'/actions/runs/'+str(runid)})
  # Same genuine current run proof binds selected Git DATA; no external JSON selects a descriptor.
  descriptor=g.postdispatch133(self.runtime133,run,selected,time.time(),time.monotonic())
  self.macro.store.save('runtime132/postdispatch-bind-original',{'run':run,'selected':selected,'descriptor':descriptor,'run_canonical':self.macro.originals[('dispatch136/runs/'+str(n)) if ui.get('kind')=='git_create136' else 'dispatch/run']['canonical']})
  self.run_id=run['id'];self.selected133=copy.deepcopy(selected);self.actual_run133=copy.deepcopy(run)
  return run
 def delay_until(self,target):
  delay=target-time.monotonic()
  if delay<0:return
  if delay>300 or target>=self.phase_mono or target>=self.parent_mono:raise TimeoutError('Exact146 finite source-owned idle within unchanged interval')
  while time.monotonic()<target:
   self.deadline();time.sleep(min(30,max(0,target-time.monotonic())))
  self.deadline()
 def wait_recipient146(self):
  start=time.monotonic();runid=self.run_id
  for n,offset in enumerate((0,45,90,135,180,210)):
   if n:self.inventory.claim('recipient146/delay/'+str(n-1));self.delay_until(start+offset)
   listed=self.macro.call('recipient146/list/'+str(n),'github_fetch_workflow_run_artifacts',{'repo_full_name':g.REPO,'run_id':runid,'name':'traceharbor-recipient104-'+str(runid)+'-1'})
   if listed.get('total_count')==1 and len(listed.get('artifacts',[]))==1:return
   if listed!={'total_count':0,'artifacts':[]}:raise ValueError('Exact bounded recipient availability only')
  raise g.Pending127('Finite146 recipient readiness exhausted; no repeated counter/dispatch')
 def collect_failure146(self,packet):
  run=self.provider_value(packet,'github_fetch');plan=self.provider_plan_failure146();listed=self.packet('failure/list','github_fetch_workflow_run_artifacts',{'repo_full_name':g.REPO,'run_id':run['id'],'name':'traceharbor-failure146-'+str(run['id'])+'-1'});art=self.provider.failure_metadata146(plan,run,self.provider_value(listed,'github_fetch_workflow_run_artifacts'))
  downloaded=self.packet('failure/download','github_download_workflow_artifact',{'repo_full_name':g.REPO,'artifact_id':art['id'],'file_name':'failure146.zip'});ref=self.provider_value(downloaded,'github_download_workflow_artifact').get('file');destination=self.layout['transfer']/('failure146-'+str(run['id']));destination.mkdir(mode=0o700,exist_ok=False)
  material=self.packet('failure/materialize','library_materialize',{'items':[{k:ref[k] for k in ('library_file_id','file_id','file_name') if k in ref}],'destination':{'directory':str(destination)}});tr=self.provider_value(material,'library_materialize');tr=tr.get('result',tr)
  if len(tr['transfers'])!=1 or tr.get('unavailable_items'):raise ValueError('Exact failure artifact transfer')
  raw=self.artifact_bytes(ref,tr['transfers'][0],art,destination,'failure/file-original',65536);return self.provider.failure_zip146(raw,plan)
 def provider_plan_failure146(self):
  x=self.macro.context;return {'run_id':self.run_id,'source_sha':x['source_sha'],'manifest_sha256':x['manifest_sha256'],'once_receipt_sha256':x['once_receipt_sha256'],'dispatch_binding136':g.p133.g136.binding136(self.config['ui_dispatch127']['args'])}
 def prepare_delivery(self):
  current=self.current()
  if 'ADMIT_CURRENT_ENCRYPTED_INPUT_CUSTODY' not in current['direction']['body']:raise PermissionError('Actual private6 custody independent gate')
  self.inventory.claim('custody/guard');manifest=base.strict((ROOT/'manifest.json').read_bytes());source=ROOT.parent/'offline103/ingress.py';transfer=ROOT.parent/'offline103/transfer.json'
  if sha(source.read_bytes())!=manifest['source_files']['offline103/ingress.py']['sha256'] or sha(transfer.read_bytes())!=manifest['canonical_transfer_sha256']:raise ValueError('Unchanged reviewed ingress/private pins')
  self.inventory.claim('ingress/source');ingress=load('trace127_fixed_ingress',source);cfg=base.strict(transfer.read_bytes());runid=self.run_id
  run=self.macro.call('recipient/run','github_fetch',{'url':'https://api.github.com/repos/'+g.REPO+'/actions/runs/'+str(runid)})
  listed=self.macro.call('recipient/list','github_fetch_workflow_run_artifacts',{'repo_full_name':g.REPO,'run_id':runid,'name':'traceharbor-recipient104-'+str(runid)+'-1'})
  if listed['total_count']!=1 or len(listed['artifacts'])!=1:raise ValueError('Exact NAME-FILTERED selected recipient, not total run inventory')
  artifact=listed['artifacts'][0]
  if artifact['name']!='traceharbor-recipient104-'+str(runid)+'-1' or artifact['workflow_run']['id']!=runid or artifact['workflow_run']['head_sha']!=self.source or artifact['expired'] or not 0<artifact['size_in_bytes']<=65536:raise ValueError('Recipient context/digest cap')
  downloaded=self.macro.call('recipient/download','github_download_workflow_artifact',{'repo_full_name':g.REPO,'artifact_id':artifact['id'],'file_name':'recipient127.zip'});ref=downloaded.get('file',downloaded)
  destination=self.layout['transfer']/('recipient127-'+str(runid));destination.mkdir(mode=0o700,exist_ok=False)
  transfer=self.macro.call('recipient/materialize','library_materialize',{'items':[{k:ref[k] for k in ('library_file_id','file_id','file_name') if k in ref}],'destination':{'directory':str(destination)}})
  raw=self.artifact_bytes(ref,transfer,artifact,destination,'recipient/verify',65536)
  with zipfile.ZipFile(io.BytesIO(raw)) as archive:
   if archive.namelist()!=['recipient-public.json'] or archive.testzip() is not None:raise ValueError('Exact recipient complete CRC')
   public=base.strict(archive.read('recipient-public.json'))
  trace=[];command=ingress.command;ordinal=[0]
  # Both encryption and cms structure inspection are bounded actual starts.
  def counted_command(*args,**kwargs):
   n=ordinal[0];ordinal[0]+=1;self.inventory.claim('ingress/openssl/'+str(n));return command(*args,**kwargs)
  ingress.command=counted_command
  #135 All SIX current inputs were verified at intake. Existing encrypted
  # ingress carries exactly its THREE private members; tokenizer data is fetched
  # by the pinned public-only acquisition step, never smuggled in a3member wire.
  wanted_names={row['name'] for row in cfg['private_members']}
  if not wanted_names<=set(self.config['private_files127']):raise ValueError('Actual private member source closure')
  files={k:pathlib.Path(self.config['private_files127'][k]).read_bytes() for k in wanted_names}
  try:plan=ingress.prepare_from_artifact(public,run,artifact,sha(raw),files,cfg['private_members'],pathlib.Path(self.config['private_output127']),self.config['source_tree'],trace,dispatch_binding136=g.p133.g136.binding136(self.config['ui_dispatch127']['args']) if self.config['ui_dispatch127'].get('kind')=='git_create136' else None)
  finally:self.macro.store.save('ingress/openssl-original',{'trace':trace,'scope':'ACTUAL_EXISTING_INGRESS_ORIGINALS'})
  delivery={'context':plan['context'],'ciphertext_base64':plan['operations'][0]['body']['content'],'ciphertext_sha256':plan['ciphertext_sha256'],'artifact_digest':sha(raw),'artifact_bytes':len(raw),'retention_days':1,'custody_sha256':sha(can({'pins':cfg['private_members'],'context':plan['context'],'artifact_sha256':sha(raw)}))}
  self.macro.store.save('ingress/proof',delivery);return delivery
 def validate_delivery(self,d):
  raw=base64.b64decode(d['ciphertext_base64'],validate=True);ctx=d['context'];wanted=self.macro.context
  if not 0<len(raw)<=131072 or sha(raw)!=d['ciphertext_sha256'] or not __import__('re').fullmatch('[a-f0-9]{32}',ctx['nonce']) or ctx['source_sha']!=self.source or ctx['run_id']!=self.run_id or ctx['attempt']!=1 or ctx['expires_utc']!=wanted['expires_utc']:raise ValueError('Actual recipient/nonce/source/cipher/custody binding')
 def admit_descriptor(self):
  g.require_native_runtime133(self.runtime133)
  if self.actual_run133!=self.macro.run:raise ValueError('Actual typed run original mutated')
  expected=g.postdispatch133(self.runtime133,self.actual_run133,self.selected133,time.time(),time.monotonic())
  counter=load('trace127_fixed_counter',ROOT/'counter115.py');admission=counter.producer_module(ROOT.parent)
  binding={k:expected[k] for k in ('source_sha','manifest_sha256','once_receipt_sha256','run_id','request_sha256')}
  admission.verify_once_intent(expected,binding,counter.input_pins());return expected
 def consumed_descriptor(self,delivery):
  # Match the existing runner admission116 wire schema exactly, using the
  # original encrypted chain and current authenticated custody context.
  ctx=delivery['context'];p=self.macro.proofs['encrypted']
  return {'phase':'consumed','recipient_context':ctx,'ciphertext_receipt':{'ref':p['ref'],'ciphertext_commit':p['commit'],'ciphertext_sha256':delivery['ciphertext_sha256']},'admit_sha256':sha(self.macro.body('admit')[0])}
 def provider_value(self,packet,operation):return self.provider.value127(packet,operation,True,self)
 def packet(self,id,op,args):
  self.macro.call(id,op,args);o=self.current_original;request=o['request'];identity={'context_sha256':sha(can(self.config['context'])),'operation':op,'seq':request['seq'],'tool':'exec_command' if op=='library_replace' else op,'call_id':request['request_digest']};path=o['canonical_path'];raw=self.canonical127.io.read(path)
  canonical={'path':path,'bytes':len(raw),'sha256':sha(raw)}
  return self.provider.retain_native127(self,identity,o['frame']['original_result'],canonical)
 def observe_run(self,n):return self.packet('collection/run/'+str(n),'github_fetch',{'url':'https://api.github.com/repos/'+g.REPO+'/actions/runs/'+str(self.run_id)})
 def collect_bundle(self,run):
  p=self.provider_plan();url='https://api.github.com/repos/'+g.REPO+'/'
  b={'run':run,'commit':self.packet('safe/commit','github_fetch',{'url':url+'commits/'+p['source_sha']}),'tree':self.packet('safe/tree','github_fetch',{'url':url+'git/trees/'+p['source_tree']+'?recursive=1'}),'jobs':self.packet('safe/jobs','github_fetch_workflow_run_jobs',{'repo_full_name':g.REPO,'run_id':p['run_id']}),'artifacts':self.packet('safe/list','github_fetch_workflow_run_artifacts',{'repo_full_name':g.REPO,'run_id':p['run_id'],'name':'traceharbor-safe127-'+str(p['run_id'])+'-1'})}
  artifact=self.provider.metadata127(p,*[self.provider_value(b[k],op) for k,op in [('run','github_fetch'),('commit','github_fetch'),('tree','github_fetch'),('jobs','github_fetch_workflow_run_jobs'),('artifacts','github_fetch_workflow_run_artifacts')]])
  b['download']=self.packet('safe/download','github_download_workflow_artifact',{'repo_full_name':g.REPO,'artifact_id':artifact['id'],'file_name':'safe127.zip'});ref=self.provider_value(b['download'],'github_download_workflow_artifact').get('file');self.destination=self.layout['transfer']/('safe-artifact-'+str(p['run_id'])+'-1');self.destination.mkdir(mode=0o700,exist_ok=False)
  b['materialized']=self.packet('safe/materialize','library_materialize',{'items':[{k:ref[k] for k in ('library_file_id','file_id','file_name') if k in ref}],'destination':{'directory':str(self.destination)}});return b
 def provider_plan(self):
  x=self.macro.context;rid=self.run_id;admit,_=self.macro.body('admit');consumed,_=self.macro.body('consumed');descriptor=json.loads(consumed)
  return {'run_id':rid,'source_sha':x['source_sha'],'source_parent':x['source_parent'],'source_tree':x['source_tree'],'expires_utc':x['expires_utc'],'workflow_path':x['workflow_path'],'workflow_step_names':x['workflow_step_names'],'full_tree_entries':x['full_tree_entries'],'dispatch_binding136':g.p133.g136.binding136(self.config['ui_dispatch127']['args']) if self.config['ui_dispatch127'].get('kind')=='git_create136' else None,'projection_context':{'run_id':rid,'attempt':1,'actor_id':g.OWNER,'repository_id':g.REPOSITORY,'source_sha':x['source_sha'],'manifest_sha256':x['manifest_sha256'],'once_receipt_sha256':x['once_receipt_sha256'],'expires_utc':x['expires_utc'],'admission_sha256':sha(admit),'custody_binding_sha256':sha(can(descriptor['ciphertext_receipt'])),'cost_scope_sha256':x['cost_scope_sha256']}}
 def artifact_bytes(self,ref,tr,artifact,destination,evidence,cap):
  self.inventory.claim(evidence);path=pathlib.Path(tr['workspace_path'])
  if ref.get('file_id')!=tr['file_id'] or ref.get('file_name')!=tr['file_name'] or not tr.get('library_file_id') or ref.get('library_file_id') not in (None,tr['library_file_id']) or path!=destination/ref['file_name'] or path.is_symlink() or path.resolve()!=path:raise ValueError('Actual exact reusable ref/peritem disjoint positiveidentity')
  s=path.lstat()
  if not stat.S_ISREG(s.st_mode) or s.st_uid!=os.getuid() or s.st_nlink!=1 or not 0<s.st_size<=cap:raise ValueError('Owned regular bounded nonlink')
  # Same current helper implementation in-process: no hidden process starts.
  identity={'phase':evidence,'run':self.config['integration_context127']['once_receipt_sha256'],'source':self.source,'call':evidence+'/helper-original128'}
  helper128.run_helper128(self.config['library_helper'],self.config['library_helper_sha256'],path,tr['library_file_id'],tr['xattrs'],identity,lambda ident,record:self.macro.store.save(evidence+'/helper-original128',{'identity':ident,'original':record}))
  if os.getxattr(path,'user.library-file-id').decode()!=tr['library_file_id']:raise ValueError('Actual identity xattr')
  for x in tr['xattrs']:
   if os.getxattr(path,x['name']).decode()!=x['value']:raise ValueError('ALL attrs')
  fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
  try:
   before=os.fstat(fd);raw=os.read(fd,cap+1);extra=os.read(fd,1);after=os.fstat(fd)
  finally:os.close(fd)
  if extra or len(raw)!=s.st_size or (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns) or (before.st_dev,before.st_ino)!=(s.st_dev,s.st_ino) or path.lstat().st_ino!=s.st_ino or len(raw)!=artifact['size_in_bytes'] or artifact['digest']!='sha256:'+sha(raw):raise ValueError('Stable complete EOF/provider digest')
  self.deadline();return raw
 def provider_artifact_bytes127(self,ref,tr,artifact,plan):return self.artifact_bytes(ref,tr,artifact,self.destination,'safe/file-original',65536)
 def verify_bundle(self,bundle):
  projection=self.provider.verify_bundle127(self.provider_plan(),bundle,True,self);o=self.provider.ControllerSafeObservation127(self.provider._SEAL,self,self.macro,projection,self.provider_plan());self.provider._OBS[self]=o;return o
 def require_terminal(self,observation):
  if self.provider.require_native_terminal127(self,self.macro) is not observation:raise TypeError('Exact source registry typed provider observation')
def bootstrap127(config_path,provider):
 if sha((ROOT/'host_transport118.py').read_bytes())!=BASE_SHA:raise ValueError('Accepted immutable original guard')
 static=base.strict(pathlib.Path(config_path).read_bytes());plan=g.p133
 if static['path_roles']['config']!=str(pathlib.Path(config_path).resolve()):raise ValueError('Pinned static config role')
 preflight=load('trace133_native_current_intake',ROOT/'preflight127.py')
 snapshot=preflight.produce133(static['path_roles']['materialize_original'],static,_native_reload133=True);snap=preflight.require_snapshot133(snapshot)
 direction=snap['direction'];manifest_bytes=(ROOT/'manifest.json').read_bytes();manifest=base.strict(manifest_bytes);prepared=plan.release133(direction,static,manifest_bytes)
 markers=('ADMIT_TRACE146_STATIC_TYPED_RUNTIME_V3','ADMIT_NATIVE_SAFE127_PROVIDER_DELIVERY','ADMIT_CURRENT_ENCRYPTED_INPUT_CUSTODY','ADMIT_CURRENT_ONCE_DISPATCH_API0')
 if any(x not in direction['body'] for x in markers) or static['cost_scope']['host_cost_bound']!=0:raise PermissionError('Actual independent security/source/runtime/custody/cost gate absent')
 for name,pin in manifest['source_files'].items():
  path=pathlib.Path(name)
  if path.is_absolute() or '..' in path.parts:raise ValueError('Safe source path')
  raw=(ROOT.parent/path).read_bytes()
  if len(raw)!=pin['bytes'] or sha(raw)!=pin['sha256']:raise ValueError('Whole exact sources before clock')
 if not os.isatty(0):raise TypeError('Actual directPTY before holder')
 t146.preallocate146(static)
 observer_plan=pathlib.Path(static['path_roles']['capture'])/'observer146-plan.json'
 if not observer_plan.is_file() or observer_plan.is_symlink():raise ValueError('Source issued durable observer plan before holder/clock')
 observer=load('trace146_native_observer',ROOT/'observer146.py');capture_root=pathlib.Path(static['path_roles']['capture']);issue=base.strict(CanonicalReader127(capture_root).read(capture_root/'observer146-issue-original.json'))
 if issue.get('exit_code')!=0 or issue.get('session_id') is not None:raise ValueError('Actual issued observer helper terminal before holder')
 issued=base.strict(issue['output']);_,observed_plan=observer.plan146(capture_root,issued['plan_sha256'])
 expected_observer={'source_sha':static['source']['commit'],'manifest_sha256':sha(manifest_bytes),'static_config_sha256':sha(can(static)),'inventory_sha256':static['inventory_sha256'],'direction_id':direction['id'],'realm':'SOURCE_ISSUED_CONTROL_DATA'}
 if observed_plan['binding']!=expected_observer:raise ValueError('Exact current source-produced observer plan, no cloned runtime handle')
 # Exact identity was frozen before genuine149RX and checked by preflight
 # before any registry/start. Recheck through nofollow directory FDs at use.
 root=h154.consume_child154(snap['holder_preparation154'],static)
 wall=time.time();mono=time.monotonic();expires=int(wall)+t146.PARENT;cutoff=expires
 once={'schema':'TRACE116_ONCE_INTENT_V1','original_writer':'e839e90d6a61ceb21ab32dd8c78f27ab63a346e8e5ec0c4d12a1356db4fe3436','source_sha':static['source']['commit'],'manifest_sha256':sha(manifest_bytes),'request_sha256':static['request']['sha256'],'request_bytes':4935,'lock_sha256':static['lock']['sha256'],'inputs':copy.deepcopy(static['private6']),'role':'OFFLINE_COUNTER_ONLY','max_counter_invocations':1,'model_calls':0,'spend':0,'nonce':os.urandom(16).hex(),'expires_utc':expires}
 runtime=g._mint_runtime133(g._SEAL,direction,static,manifest_bytes,snap,once,os.urandom(32).hex(),wall,mono,cutoff);context=g.runtime_context133(runtime)
 # Static bytes are never mutated; this separate private runtime configuration
 # is source-derived after release, and never feeds the static admission hash.
 cfg={'source_sha':static['source']['commit'],'current_checkpoint':snap['current_checkpoint'],'current_version':snap['own_version'],'direction_number':snap['direction_number'],'writer_binding':snap['writer_binding'],'holder_root':str(root),'capture_directory':static['path_roles']['capture'],'library_helper':static['path_roles']['library_helper'],'library_helper_sha256':static['path_roles']['library_helper_sha256'],'config_path':str(config_path),'integration_context127':context,'native_admission127':prepared['proposed_admission'],'coordinator_cutoff_utc':cutoff,'deadline_utc_ms':int(context['expires_utc']*1000),'context':{'domain':'TRACE133_TYPED_RUNTIME','source_sha':context['source_sha'],'once_receipt_sha256':context['once_receipt_sha256'],'direction_id':context['direction_id']}}
 #134 These are source-derived runtime values from already verified static/custody.
 # No external JSON adds private paths or selects an output outside this holder.
 cfg.update(source_tree=static['source']['tree'],private_files127={name:str(pathlib.Path(static['custody_scope']['root'])/name) for name in static['private6']},private_output127=str(root/'ciphertext133'))
 if static['dispatch_source'].get('kind')=='git_create136':
  cfg['ui_dispatch127']={'kind':'git_create136','source_sha':context['source_sha'],'once_receipt_sha256':context['once_receipt_sha256'],'args':plan.g136.args136(plan.dispatch_inputs135(static,context,cutoff))}
 else:
  script=plan.render_dispatch135(static,context,cutoff)
  cfg['ui_dispatch127']={'master_terminal_no_input_conflict':direction.get('master_terminal_no_input_conflict') is True,'source_sha':context['source_sha'],'once_receipt_sha256':context['once_receipt_sha256'],'script_sha256':sha(script.encode()),'args':{'code':script}}
 host=NativePort127(g._SEAL,cfg,manifest,provider);host.runtime133=runtime;host.static_config133=can(static);host.static152=copy.deepcopy(static);clock=ActualClock127();macro=g.Grouped127(host,clock,context,root/'originals',c.DiskOriginalIO127(),host.inventory,'ACTUAL_SOURCE_PRIVATE',g._SEAL)
 macro.store.save('runtime132/once-intent-original',once);macro.store.save('runtime132/armed-context-original',{'runtime_context':context,'static_config_sha256':sha(host.static_config133),'phase_template':prepared['phase_template'],'current_whole_snapshot':snap})
 return host,macro
def main():
 if sys.argv[1]=='guard':
  static=base.strict(pathlib.Path(sys.argv[2]).read_bytes());doc,_=base.check_checkpoint(sys.argv[3],base.OWN,int(sys.argv[4]));key='native'+doc['state'].split('_')[0][6:];g.p133.release133(doc[key]['direction'],static,(ROOT/'manifest.json').read_bytes());cfg={'direction_number':int(key[6:]),'writer_binding':doc[key]['records'][0]['payload']['writer_binding'],'config_path':sys.argv[2]};current=h154.current_binding154(base,sys.argv[3],int(sys.argv[4]),cfg);print(json.dumps({'current':current['number'],'writer':current['binding']['writer_sha256'],'guard':'PASS'}));return 0
 provider=load('trace127_fixed_provider',ROOT/'provider_safe127.py');host,macro=provider.bootstrap_native_host127(sys.argv[1]);result=macro.run_complete();print(json.dumps(result));return 0
if __name__=='__main__':sys.exit(main())
