"""Executable compact16 semantic chain and bounded ordinary SAFE delivery.

No module import performs an effect. The native constructor is only the fixed
source bootstrap; synthetic port/clock/IO are never convertible to runtime.
"""
import base64,copy,datetime,hashlib,importlib.util,json,pathlib,re,sys,time
ROOT=pathlib.Path(__file__).resolve().parent
def load(name,file):
 s=importlib.util.spec_from_file_location(name,ROOT/file);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
c=load('trace127_integrated_control','control127.py');can=c.can;sha=c.sha
OWNER=273768139;REPO='Elinfiny/TraceHarbor';REPOSITORY=1391430317
_SEAL=object();_NATIVE={}
class Pending127(RuntimeError):pass
def context127(x):
 required={'source_sha','source_tree','source_parent','manifest_sha256','once_receipt_sha256','expires_utc','parent_mono','initial_version','direction_id','direction_sha256','writer_sha256','auditor_sha256','nonce','route','baseline_entries','full_tree_entries','cost_scope_sha256','custody_binding_sha256','workflow_path','workflow_step_names'}
 if set(x)!=required:raise ValueError('Closed source/parent/tree/body/nonce/once/route/authority context')
 for k in ('source_sha','source_tree','source_parent'):
  if not re.fullmatch('[a-f0-9]{40}',x[k]):raise ValueError('Exact source Git pins')
 for k in ('manifest_sha256','once_receipt_sha256','direction_sha256','writer_sha256','auditor_sha256','cost_scope_sha256','custody_binding_sha256'):
  if not re.fullmatch('[a-f0-9]{64}',x[k]):raise ValueError('Exact authority/custody/cost pins')
 if not re.fullmatch('[a-f0-9]{64}',x['nonce']) or x['route']!='EXISTING_GITHUB_LIBRARY_DIRECTPTY' or x['initial_version']<=0:raise ValueError('Unused prebound nonce/route/version')
 return copy.deepcopy(x)
class Grouped127:
 def __init__(self,port,clock,context,root,io,inventory,realm='SYNTHETIC_SOURCE_ONLY',key=None):
  if realm!='SYNTHETIC_SOURCE_ONLY' and (key is not _SEAL or type(port).__name__!='NativePort127'):raise TypeError('No synthetic/external API as native authority')
  self.port=port;self.clock=clock;self.context=context127(context);self.realm=realm;self.inventory=inventory;self.store=c.OriginalStore127(root,io,inventory);self.cursor=0;self.version=context['initial_version'];self.consumed=set();self.closed=[];self.active=None;self.failed=None;self.originals={};self.returns={};self.run=None;self.delivery=None;self.proofs={};self.safe=None
  self.parent_mono=context['parent_mono'];self.parent_wall=context['expires_utc'];self.phase_receipts={};self.plan_sha=sha(can({'context':self.context,'inventory':inventory.plan,'graph':list(c.SEMANTIC),'phases':list(c.PHASES)}));port.bind(self)
 def now(self):return self.clock.mono(),self.clock.wall()
 def remaining(self):m,u=self.now();return min(self.parent_mono-m,self.parent_wall-u)
 def guard(self):
  if self.failed is not None:raise RuntimeError('Consumed invocation UNKNOWN; no retry/restart')
  m,u=self.now()
  if self.remaining()<=0 or self.active and (m>=self.active['end_mono'] or u>=self.active['end_utc']):raise TimeoutError('Original parent/own phase expired')
 def snapshot(self):return {'scope':self.realm if self.realm=='SYNTHETIC_SOURCE_ONLY' else 'PRIVATE_JOURNAL_PLAN','cursor':self.cursor,'first_unknown':self.failed,'version':self.version,'macro_sha256':self.plan_sha,'native_authority':False}
 def unknown(self,exc):
  if self.failed is None:
   self.failed={'exception_class':type(exc).__name__,'message':str(exc),'cursor':self.cursor,'phase':copy.deepcopy(self.active)};self.inventory.unknown(self.failed)
   self.store.save('failure/original',self.failed)
  return self.failed
 def call(self,id,op,args):
  self.guard();self.inventory.remote_bundle(id)
  if op.startswith('github_create_'):self.port.before_effect(id,op,args)
  # Actual source mapping/arguments are source-produced before the primitive;
  # preceding returned SHAs are typed live dependencies, never event selectors.
  value=None;error=None
  try:value=self.port.invoke(id,op,copy.deepcopy(args))
  except BaseException as exc:error=exc
  reference=None;reference_error=None
  try:reference=self.port.original_reference(id)
  except BaseException as exc:reference_error=exc
  self.originals[id]={'value':value,'exception':error,'canonical':reference,'reference_error':reference_error}
  # Port retains complete original before conversion/postguard. Synthetic port
  # uses the identical ticket path and explicit fixture IO instead of effects.
  if error is not None:raise error
  if reference_error is not None:raise reference_error
  self.guard();return value
 def begin(self,name,seconds=None):
  self.guard()
  if self.active is not None or name in self.consumed or name in self.closed:raise RuntimeError('No phase reset/resume')
  m,u=self.now();seconds=self.remaining() if seconds is None else seconds
  if seconds<=0:raise TimeoutError('No original parent reserve')
  self.active={'name':name,'begin_mono':m,'begin_utc':u,'end_mono':min(m+seconds,self.parent_mono),'end_utc':min(u+seconds,self.parent_wall),'parent_mono':self.parent_mono,'parent_utc':self.parent_wall}
  self.port.bind_interval(self.active)
 def close(self):
  self.guard();a=copy.deepcopy(self.active)
  if a is None:raise RuntimeError('No phase')
  key=a['name']+'/phase-close' if a['name'] in c.PHASES else 'collection/close'
  self.store.save(key,{'phase':a,'cursor':self.cursor,'original_ids':list(self.originals),'status':'PROVISIONAL_BEFORE_POST_IO'})
  self.guard();self.closed.append(a['name']);self.active=None
 def semantic(self,i,facts):
  if i!=self.cursor:raise RuntimeError('Exact16 semantic order')
  self.store.save('semantic/'+str(i),{'ordinal':i,'name':c.SEMANTIC[i],'facts':facts,'plan_sha256':self.plan_sha});self.guard();self.cursor+=1
 def phase_intent(self,name,operations):
  self.guard()
  if name in self.consumed:raise RuntimeError('Whole phase already consumed, no partial resume')
  previous=[self.store.records[x] for x in self.store.records]
  canonical=[x['canonical'] for x in self.originals.values()]
  if any(x is None for x in canonical):raise ValueError('No missing complete original before another phase')
  for r in canonical:self.port.verify_reference(r)
  for r in previous:
   raw=self.store.io.read(r['path'])
   if len(raw)!=r['bytes'] or sha(raw)!=r['sha256']:raise ValueError('All previous durable originals before next intent')
  intent={'schema':'TRACE127_PHASE_INTENT_V1','phase':name,'status':'ENTIRE_PHASE_CONSUMED_BEFORE_FIRST_EFFECT','plan_sha256':self.plan_sha,'context':self.context,'expected_current_version':self.version,'operations':copy.deepcopy(operations),'previous_complete_originals':previous,'previous_complete_native_canonicals':canonical,'parent_clock':{'mono':self.parent_mono,'utc':self.parent_wall}}
  self.store.save(name+'/intent',intent);self.consumed.add(name)
  receipt=self.port.cas(name,self.version,{'phase':'PUBLISH_INTENT','source_sha':self.context['source_sha'],'operation':'GROUPED_PHASE127','phase_intent127':intent})
  if receipt.get('version')!=self.version+1 or receipt.get('wholebyte_self_allattrs')!='PASS' or receipt.get('intent_sha256')!=sha(can(intent)):raise ValueError('Actual guarded original writer/CAS/pinned wholebyte/self/ALLattrs before effect')
  self.phase_receipts[name]=copy.deepcopy(receipt);self.version+=1;self.guard();return intent
 def freeze(self):
  self.begin('SOURCE_FREEZE');self.phase_intent('SOURCE_FREEZE',[{'role':'exact entire source/inventory/phase-plan freeze','sha256':self.plan_sha}]);self.close()
 def predispatch(self):
  self.begin('PRE_DISPATCH');self.phase_intent('PRE_DISPATCH',[{'role':'ONCE current fixed UI dispatch','source_sha':self.context['source_sha'],'once':self.context['once_receipt_sha256']}]);self.semantic(0,{'consumed_before_dispatch':True});self.close()
  self.run=self.port.dispatch()
  r=self.run
  if r['head_sha']!=self.context['source_sha'] or r['run_attempt']!=1 or r['actor']['id']!=OWNER or r['repository']['id']!=REPOSITORY or r['event']!='workflow_dispatch' or r['status']!='in_progress':raise ValueError('Actual selected current dispatch original')
  started=datetime.datetime.fromisoformat(r['run_started_at'].replace('Z','+00:00')).timestamp()
  if not 0<self.parent_wall-started<=900:raise ValueError('Original900 from actual runner start')
 def body(self,phase,resolve=True):
  if phase=='encrypted':return base64.b64decode(self.delivery['ciphertext_base64'],validate=True),'traceharbor-encrypted104-'+self.delivery['context']['nonce']+'.cms'
  body=self.port.admit_descriptor()
  if body.get('source_sha')!=self.context['source_sha'] or body.get('manifest_sha256')!=self.context['manifest_sha256'] or body.get('once_receipt_sha256')!=self.context['once_receipt_sha256'] or str(body.get('run_id'))!=str(self.run['id']) or body.get('expires_utc')!=self.parent_wall or body.get('phase')!='admit':raise ValueError('Exact descriptor source/manifest/run/once/expiry before first phase effect')
  if phase=='consumed':body.update(self.port.consumed_descriptor(self.delivery))
  receipt=self.phase_receipts.get(phase.upper()+'_CHAIN')
  if resolve and receipt is not None:body.update(own_cas_version=receipt['version'],own_pinned_readback_sha256=receipt['sha256'])
  return can(body),'counter116-'+phase+'.json'
 def chain_plan(self,phase,raw,name):
  return [{'identity':sha(can({'plan':self.plan_sha,'phase':phase,'kind':k,'ordinal':n,'nonce':self.context['nonce']})),'role':'github_create_'+k,'body_template_sha256':sha(raw),'body_template_bytes':len(raw),'body_transform':'IDENTITY' if phase=='encrypted' else 'ADD_EXACT_SAME_PHASE_CAS_VERSION_AND_RAW_SHA256','path':name,'source_parent':self.context['source_sha'],'source_tree':self.context['source_tree'],'dependency':None if n==0 else {'preceding_typed_return':n-1,'field':'sha'},'ref':('traceharbor-encrypted104-'+self.delivery['context']['nonce'] if phase=='encrypted' else 'traceharbor-counter116-'+phase+'-'+self.context['once_receipt_sha256'])} for n,k in enumerate(('blob','tree','commit','ref'))]
 def chain(self,phase):
  phase_name=phase.upper()+'_CHAIN';minimum={'admit':820,'encrypted':550,'consumed':440}[phase]
  if self.remaining()<minimum:raise TimeoutError('Original exact whole phase+reserve admission')
  self.begin(phase_name,135 if phase=='admit' else 110)
  template,name=self.body(phase,False);ops=self.chain_plan(phase,template,name);self.phase_intent(phase_name,ops);raw,name=self.body(phase)
  start={'admit':2,'encrypted':6,'consumed':11}[phase]
  if phase in ('admit','consumed'):self.semantic(start-1,{'descriptor_sha256':sha(raw),'phase_intent_sha256':sha(can(ops))})
  returns=[]
  for n,kind in enumerate(('blob','tree','commit','ref')):
   self.guard()
   args={'repository_full_name':REPO}
   if n==0:args.update(content=base64.b64encode(raw).decode(),encoding='base64')
   elif n==1:args.update(base_tree_sha=self.context['source_tree'],tree_elements=[{'path':name,'mode':'100644','type':'blob','sha':returns[0]['sha']}])
   elif n==2:args.update(parent_sha=self.context['source_sha'],tree_sha=returns[1]['sha'],message='Exact grouped127 '+phase+' once [skip ci]')
   else:args.update(branch_name=ops[n]['ref'],sha=returns[2]['sha'])
   # The precommitted operation set is immutable across all predecessor reads.
   if self.chain_plan(phase,*self.body(phase,False))!=ops:raise ValueError('Source/body/immutable planned operation drift')
   created=self.call(phase+'/'+kind,'github_create_'+kind,args)
   suffix=('git/blobs/'+created['sha'] if n==0 else 'git/trees/'+created['sha'] if n==1 else 'commits/'+created['sha'] if n==2 else 'git/ref/heads/'+ops[n]['ref'])
   proof=self.call(phase+'/'+kind+'/proof','github_fetch',{'url':'https://api.github.com/repos/'+REPO+'/'+suffix})
   if n<3 and created['sha']!=proof['sha'] or n==3 and (created['ref']!=proof['ref'] or created['object']!=proof['object']):raise ValueError('Create return/immediate whole proof differ')
   if n==0:
    want=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if proof['sha']!=want or proof['size']!=len(raw) or proof['encoding']!='base64' or base64.b64decode(''.join(proof['content'].split()),validate=True)!=raw:raise ValueError('Full body/count/GitSHA')
   elif n==1:
    expected={e['path']:e for e in self.context['baseline_entries']}
    if name in expected:raise ValueError('Create-only new leaf')
    expected[name]={'path':name,'mode':'100644','type':'blob','sha':returns[0]['sha']}
    if proof.get('truncated') is not False or len(proof['tree'])!=len(expected) or {e['path']:{k:e[k] for k in ('path','mode','type','sha')} for e in proof['tree']}!=expected:raise ValueError('Whole baseline + exact one leaf')
   elif n==2:
    if proof['author']['id']!=OWNER or proof['committer']['id']!=OWNER or [x['sha'] for x in proof['parents']]!=[self.context['source_sha']] or proof['commit']['tree']['sha']!=returns[1]['sha']:raise ValueError('Actual Owner/soleparent/tree')
   elif proof['ref']!='refs/heads/'+ops[n]['ref'] or proof['object']!={'type':'commit','sha':returns[2]['sha']}:raise ValueError('Exact create-only ref/preceding commit')
   returns.append(proof);self.semantic(start+n,{'operation':ops[n],'original':phase+'/'+kind,'proof':phase+'/'+kind+'/proof'})
  self.proofs[phase]={'blob':returns[0]['sha'],'tree':returns[1]['sha'],'commit':returns[2]['sha'],'ref':returns[3]['ref'],'body_sha256':sha(raw)};self.close()
 def begin_collection(self):
  if self.cursor!=15 or not self.closed or self.closed[-1]!='CONSUMED_CHAIN' or self.active is not None or self.failed is not None:raise ValueError('Timely consumed closure before separate collection')
  # Binding a NEW ORDINARY interval changes no previous phase end/parent once.
  self.begin('SAFE_COLLECTION',min(150,self.remaining()));self.store.save('collection/begin',self.active)
 def collect(self):
  if self.active is None or self.active['name']!='SAFE_COLLECTION':raise RuntimeError('Retained consumed110 is never the collection clock')
  start=self.active['begin_mono'];bundle=None
  for n,offset in enumerate((0,30,60,90)):
   if n:
    self.inventory.claim('collection/delay/'+str(n-1));self.port.delay_until(start+offset);self.guard()
   packet=self.port.observe_run(n)
   run=self.port.provider_value(packet,'github_fetch')
   if run.get('status')!='completed':
    if run.get('status') not in ('queued','in_progress','waiting','pending','requested'):raise ValueError('Unsupported actual pending status')
    continue
   if run.get('conclusion')!='success':raise ValueError('Completed failed whole job cannot mint SAFE')
   bundle=self.port.collect_bundle(packet);break
  if bundle is None:raise Pending127('Finite4 observations exhausted; actual pending DATA, no UNKNOWN external effect and no repeated consumed/dispatch')
  self.safe=self.port.verify_bundle(bundle);self.guard();self.close();return self.safe
 def terminal(self):
  if self.cursor!=15 or self.safe is None or self.closed[-1]!='SAFE_COLLECTION':raise ValueError('Typed source/provider SAFE required before terminal')
  self.port.require_terminal(self.safe)
  self.begin('TERMINAL');self.phase_intent('TERMINAL',[{'role':'TERMINAL_ONCE','consumed':self.proofs['consumed'],'safe_projection_sha256':sha(can(self.safe.projection))}]);self.semantic(15,{'SAFE':'SYNTHETIC_ONLY' if self.realm=='SYNTHETIC_SOURCE_ONLY' else 'ACTUAL_SOURCE_PROVIDER_ORIGINAL'});self.close();return self.snapshot()
 def run_complete(self):
  try:
   self.freeze();self.predispatch();self.chain('admit')
   if self.remaining()<680:raise TimeoutError('Actual original allchecks680/hostbegin610 required')
   self.begin('RECIPIENT',25);self.delivery=self.port.prepare_delivery();self.guard()
   # Recipient is bounded separately; its closure is native original custody
   # retained by the existing ingress, not a seventh ownCAS.
   self.port.validate_delivery(self.delivery);self.active=None
   self.chain('encrypted');self.chain('consumed');self.begin_collection();self.collect();return self.terminal()
  except Pending127 as exc:
   self.store.save('closure/original',{'state':'PENDING_DATA_NO_REPLAY','cursor':self.cursor,'message':str(exc),'entire_consumed_phases':sorted(self.consumed)});raise
  except BaseException as exc:self.unknown(exc);raise
 def restart(self):raise RuntimeError('Never reconstruct consumed phase/native heap from journal/files; new independent direction required')
