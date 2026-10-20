"""Explicit inert fixtures for NEW127 group only. No runtime authority."""
import pathlib,importlib.util,sys,copy,json,base64,hashlib,datetime,io,zipfile,types
ROOT=pathlib.Path(__file__).resolve().parent.parent
def load(name,file):
 s=importlib.util.spec_from_file_location(name,ROOT/'diagnostic108'/file);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
g=load('qualification127_integrated','integrated127.py');c=g.c;p=load('qualification127_provider','provider_safe127.py');runner=load('qualification127_runner','safe_runtime127.py')
class Clock:
 def __init__(self):self.m=100.;self.u=1000.;self.end_mono=1000.;self.end_utc=1900.
 def mono(self):return self.m
 def wall(self):return self.u
 def advance(self,n):self.m+=n;self.u+=n
class IO:
 realm='SYNTHETIC_SOURCE_ONLY'
 def __init__(self,clock):self.clock=clock;self.files={};self.writes=[];self.fault=None
 def write_once(self,path,raw):
  if path in self.files:raise FileExistsError('Synthetic O_EXCL')
  self.files[path]=raw;self.writes.append(path)
  if self.fault and self.fault[0] in path:
   if isinstance(self.fault[1],Exception):raise self.fault[1]
   self.clock.advance(self.fault[1])
 def read(self,path):return self.files[path]
def context(clock):
 return {'source_sha':'a'*40,'source_tree':'b'*40,'source_parent':'c'*40,'manifest_sha256':'d'*64,'once_receipt_sha256':'e'*64,'expires_utc':1900.,'parent_mono':1000.,'initial_version':500,'direction_id':'SYNTHETIC127','direction_sha256':'f'*64,'writer_sha256':'1'*64,'auditor_sha256':'2'*64,'nonce':'3'*64,'route':'EXISTING_GITHUB_LIBRARY_DIRECTPTY','baseline_entries':[{'path':'source.py','mode':'100644','type':'blob','sha':'4'*40}],'full_tree_entries':[{'path':'source.py','mode':'100644','type':'blob','sha':'4'*40}],'cost_scope_sha256':'5'*64,'custody_binding_sha256':'6'*64,'workflow_path':'.github/workflows/traceharbor-counter127.yml','workflow_step_names':['Checkout exact reviewed source127','Initialize exact recipient','Publish recipient','Run protected counter','Cleanup','Publish SAFE DATA']}
class Port:
 def __init__(self,clock,io):self.clock=clock;self.io=io;self.db={};self.external={};self.effects=[];self.calls=[];self.cas_versions=[];self.phase_mutation=None;self.effect_fault=None;self.projection_mutator=None;self.pending=0;self.file_mutator=None;self.bound=None
 def bind(self,macro):self.macro=macro
 def bind_interval(self,phase):self.bound=copy.deepcopy(phase)
 def before_effect(self,id,op,args):
  phase=self.macro.active['name'];r=self.macro.store.records[phase+'/intent'];raw=self.io.read(r['path']);assert c.sha(raw)==r['sha256'] and json.loads(raw)['original']['phase']==phase
  self.macro.store.save(id+'/pre-effect-guard',{'intent_sha256':r['sha256'],'tool':op,'args_sha256':c.sha(c.can(args)),'scope':'EXPLICIT_SYNTHETIC'})
 def retain(self,id,value):
  path='/SYNTHETIC127/canonical/'+id.replace('/','_')+'.json';raw=c.can({'identity':id,'original':value});self.io.write_once(path,raw);assert self.io.read(path)==raw
 def original_reference(self,id):
  self.macro.inventory.claim(id+'/canonical-reference');path='/SYNTHETIC127/canonical/'+id.replace('/','_')+'.json';raw=self.io.read(path);return {'id':id,'path':path,'bytes':len(raw),'sha256':c.sha(raw),'canonical':True}
 def verify_reference(self,r):
  raw=self.io.read(r['path']);assert len(raw)==r['bytes'] and c.sha(raw)==r['sha256'];return r
 def invoke(self,id,op,args):
  self.calls.append((id,op));self.macro.store.save(id+'/request',{'op':op,'args':args});self.clock.advance(.01)
  if id in self.external:value=copy.deepcopy(self.external[id])
  elif op.startswith('github_create_'):
   self.effects.append((id,op,args))
   if self.effect_fault and self.effect_fault[0]==id:
    fault=self.effect_fault[1]
    if isinstance(fault,Exception):self.retain(id,{'original_exception':type(fault).__name__});raise fault
    if fault=='partial':self.retain(id,{'partial_original':True});return {'partial_original':True}
    self.clock.advance(fault)
   if op=='github_create_blob':
    raw=base64.b64decode(args['content']);s=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();value={'sha':s};proof={'sha':s,'size':len(raw),'content':args['content'],'encoding':'base64'};suffix='git/blobs/'+s
   elif op=='github_create_tree':
    s=hashlib.sha1(c.can(args)).hexdigest();value={'sha':s};proof={'sha':s,'truncated':False,'tree':self.macro.context['baseline_entries']+args['tree_elements']};suffix='git/trees/'+s
   elif op=='github_create_commit':
    s=hashlib.sha1(c.can(args)).hexdigest();value={'sha':s};proof={'sha':s,'author':{'id':g.OWNER},'committer':{'id':g.OWNER},'parents':[{'sha':args['parent_sha']}],'commit':{'tree':{'sha':args['tree_sha']}}};suffix='commits/'+s
   else:value={'ref':'refs/heads/'+args['branch_name'],'object':{'type':'commit','sha':args['sha']}};proof=copy.deepcopy(value);suffix='git/ref/heads/'+args['branch_name']
   self.db['https://api.github.com/repos/'+g.REPO+'/'+suffix]=proof
  elif op=='github_fetch':value=copy.deepcopy(self.db[args['url']])
  elif op=='library_replace':value={'status':'succeeded','current_version_number':args['expected_current_version']+1,'file_id':'file_SYNTHETIC'+str(args['expected_current_version']+1)}
  elif op=='library_materialize':value={'wholebyte_self_allattrs':'PASS','version':self.macro.version+1}
  else:value={'fixture':id}
  self.retain(id,value);self.macro.store.save(id+'/return',value);return value
 def cas(self,phase,version,payload):
  self.macro.call(phase+'/CAS','library_replace',{'expected_current_version':version});self.macro.call(phase+'/readback','library_materialize',{'fixture':phase})
  self.cas_versions.append((phase,version+1));r={'version':version+1,'sha256':c.sha(c.can(payload)),'wholebyte_self_allattrs':'PASS','intent_sha256':c.sha(c.can(payload['phase_intent127']))}
  if self.phase_mutation and self.phase_mutation[0]==phase:r[self.phase_mutation[1]]=self.phase_mutation[2]
  return r
 def run(self,status='in_progress'):
  x=self.macro.context;return {'id':77,'run_attempt':1,'actor':{'id':g.OWNER},'repository':{'id':g.REPOSITORY},'event':'workflow_dispatch','head_sha':x['source_sha'],'path':x['workflow_path'],'status':status,'conclusion':'success' if status=='completed' else None,'run_started_at':'1970-01-01T00:16:40Z','updated_at':'1970-01-01T00:20:00Z'}
 def dispatch(self):
  self.macro.call('dispatch/UI','browser_js',{'code':'EXPLICIT_SYNTHETIC_NO_UI'});url='https://api.github.com/repos/'+g.REPO+'/actions/runs/77';self.db[url]=self.run();return self.macro.call('dispatch/run','github_fetch',{'url':url})
 def admit_descriptor(self):
  x=self.macro.context;return {'schema':'SYNTHETIC127_ADMIT_NOT_NATIVE','phase':'admit','source_sha':x['source_sha'],'manifest_sha256':x['manifest_sha256'],'once_receipt_sha256':x['once_receipt_sha256'],'run_id':'77','attempt':1,'expires_utc':x['expires_utc'],'model_calls':0,'spend':0}
 def prepare_delivery(self):
  raw=b'EXPLICIT_SYNTHETIC_CIPHERTEXT_NOT_ENCRYPTED';x=self.macro.context
  for id,op in [('recipient/run','github_fetch'),('recipient/list','github_fetch_workflow_run_artifacts'),('recipient/download','github_download_workflow_artifact'),('recipient/materialize','library_materialize')]:
   if op=='github_fetch':self.macro.call(id,op,{'url':'https://api.github.com/repos/'+g.REPO+'/actions/runs/77'})
   else:self.macro.call(id,op,{'fixture':'SYNTHETIC'})
  return {'ciphertext_base64':base64.b64encode(raw).decode(),'ciphertext_sha256':c.sha(raw),'context':{'nonce':'7'*32,'run_id':77,'attempt':1,'source_sha':x['source_sha'],'expires_utc':x['expires_utc']},'custody_sha256':'8'*64}
 def validate_delivery(self,d):
  assert c.sha(base64.b64decode(d['ciphertext_base64']))==d['ciphertext_sha256'] and d['context']['source_sha']==self.macro.context['source_sha']
 def consumed_descriptor(self,d):return {'phase':'consumed','recipient_context':d['context'],'ciphertext_receipt':{'ciphertext_commit':self.macro.proofs['encrypted']['commit'],'ciphertext_sha256':d['ciphertext_sha256'],'ref':self.macro.proofs['encrypted']['ref']},'admit_sha256':c.sha(self.macro.body('admit')[0])}
 def delay_until(self,target):self.clock.advance(max(0,target-self.clock.mono()))
 def packet(self,op,v):return p.SyntheticOriginal127(op,v)
 def observe_run(self,n):
  status='in_progress' if n<self.pending else 'completed';value=self.run(status);url='https://api.github.com/repos/'+g.REPO+'/actions/runs/77';self.db[url]=value;self.macro.call('collection/run/'+str(n),'github_fetch',{'url':url});return self.packet('github_fetch',{'content':json.dumps(value)})
 def provider_value(self,packet,operation):return p.value127(packet,operation,False)
 def provider_plan(self):
  x=self.macro.context;admit=self.macro.body('admit')[0];consumed=json.loads(self.macro.body('consumed')[0]);ctx={'run_id':77,'attempt':1,'actor_id':g.OWNER,'repository_id':g.REPOSITORY,'source_sha':x['source_sha'],'manifest_sha256':x['manifest_sha256'],'once_receipt_sha256':x['once_receipt_sha256'],'expires_utc':x['expires_utc'],'admission_sha256':c.sha(admit),'custody_binding_sha256':c.sha(c.can(consumed['ciphertext_receipt'])),'cost_scope_sha256':x['cost_scope_sha256']}
  return {'run_id':77,'source_sha':x['source_sha'],'source_parent':x['source_parent'],'source_tree':x['source_tree'],'expires_utc':x['expires_utc'],'workflow_path':x['workflow_path'],'workflow_step_names':x['workflow_step_names'],'full_tree_entries':x['full_tree_entries'],'projection_context':ctx}
 def collect_bundle(self,run):
  plan=self.provider_plan();phase=lambda n,start,seconds:{'facts_sha256':str(n)*64,'begin_mono':start,'end_mono':start+seconds,'begin_utc':start+900,'end_utc':start+900+seconds,'post_io_mono':start+.1,'post_io_utc':start+900+.1,'seconds_cap':seconds}
  projection={'schema':'TRACE127_MINIMAL_SAFE_V1','scope':'SYNTHETIC_SOURCE_ONLY','context':plan['projection_context'],'counter':{'verified':True,'T':None,'counter_invocations':1,'model_calls':0},'stop_cleanup':{'consumer_stopped':True,'cleanup_complete':True,'first_unknown':None},'phases':{'cleanup':phase(1,100,10),'proof':phase(2,101,15)},'runner_proof_sha256':'9'*64}
  if self.projection_mutator:self.projection_mutator(projection)
  out=io.BytesIO()
  with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_STORED) as z:z.writestr('projection.json',c.can(projection))
  raw=out.getvalue();commit={'sha':plan['source_sha'],'author':{'id':g.OWNER},'committer':{'id':g.OWNER},'parents':[{'sha':plan['source_parent']}],'commit':{'tree':{'sha':plan['source_tree']}}};tree={'sha':plan['source_tree'],'truncated':False,'tree':plan['full_tree_entries']}
  names=['Set up job',*plan['workflow_step_names'],'Post '+plan['workflow_step_names'][0],'Complete job'];jobs={'total_count':1,'jobs':[{'run_id':77,'run_attempt':1,'name':'counter','status':'completed','conclusion':'success','steps':[{'number':i+1,'name':name,'status':'completed','conclusion':'success'} for i,name in enumerate(names)]}]}
  artifacts={'total_count':1,'artifacts':[{'name':'traceharbor-safe127-77-1','id':88,'expired':False,'workflow_run':{'id':77,'head_sha':plan['source_sha']},'digest':'sha256:'+c.sha(raw),'size_in_bytes':len(raw)}]};ref={'library_file_id':'lib_SYNTHETIC127','file_id':'file_SYNTHETIC127','file_name':'safe127.zip'};tr=dict(ref,workspace_path='/SYNTHETIC127/transfer/safe127.zip',xattrs=[{'name':'user.library-file-version','value':'0'},{'name':'user.source-fixture','value':'EXPLICIT_SYNTHETIC'}])
  b={'run':run,'commit':self.packet('github_fetch',{'content':json.dumps(commit)}),'tree':self.packet('github_fetch',{'content':json.dumps(tree)}),'jobs':self.packet('github_fetch_workflow_run_jobs',jobs),'artifacts':self.packet('github_fetch_workflow_run_artifacts',artifacts),'download':self.packet('github_download_workflow_artifact',{'file':ref}),'materialized':self.packet('library_materialize',{'transfers':[tr]})}
  b['materialized'].zip_bytes=raw;b['materialized'].fixture_file_facts={'realm':'SYNTHETIC_SOURCE_ONLY','path':tr['workspace_path'],'basename':ref['file_name'],'library_file_id':tr['library_file_id'],'xattrs':{x['name']:x['value'] for x in tr['xattrs']},'regular_owned_singlelink':True,'whole_eof':True,'stable_identity':True}
  if self.file_mutator:self.file_mutator(plan,b)
  for id,key in [('safe/commit','commit'),('safe/tree','tree'),('safe/jobs','jobs'),('safe/list','artifacts'),('safe/download','download'),('safe/materialize','materialized')]:
   value=b[key].original['structuredContent'];self.external[id]=json.loads(value['content']) if b[key].operation=='github_fetch' else value
   self.macro.call(id,b[key].operation,{'fixture':'SYNTHETIC_PROVIDER_ORIGINAL'})
  return b
 def verify_bundle(self,b):return p.synthetic_verify127(self.provider_plan(),b)
 def require_terminal(self,o):
  if type(o) is not p.SyntheticSafeObservation127 or self.macro.realm!='SYNTHETIC_SOURCE_ONLY':raise TypeError('Exact synthetic observation, never runtime')
def fixture():
 clock=Clock();io=IO(clock);port=Port(clock,io);inv=c.Inventory127(c.inventory127(),'SYNTHETIC_SOURCE_ONLY');macro=g.Grouped127(port,clock,context(clock),'/SYNTHETIC127/originals',io,inv);return macro,port,clock,io
def through_consumed():
 m,p,cl,io=fixture();m.freeze();m.predispatch();m.chain('admit');m.begin('RECIPIENT',25);m.delivery=p.prepare_delivery();p.validate_delivery(m.delivery);m.active=None;m.chain('encrypted');m.chain('consumed');return m,p,cl,io
def refused(fn):
 try:fn()
 except (ValueError,TypeError,RuntimeError,TimeoutError,KeyError,FileNotFoundError,PermissionError,OSError,zipfile.BadZipFile):return True
 raise AssertionError('Expected source refusal')
