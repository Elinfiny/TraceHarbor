"""NEW146 changed-interface qualification only. All runtime ports are synthetic.
Local absence/custody/cleanup checks use real isolated temporary files, no private6.
"""
import unittest, pathlib,importlib.util,sys,tempfile,os,json,copy,hashlib,io,zipfile,datetime
from unittest.mock import patch
ROOT=pathlib.Path(__file__).resolve().parent.parent
def load(name,file):
 s=importlib.util.spec_from_file_location(name,ROOT/file);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
T=load('qualification146_timing','diagnostic108/timing146.py');E=load('qualification146_failure','diagnostic108/failure146.py');O=load('qualification146_observer','diagnostic108/observer146.py');B=load('qualification146_readiness','diagnostic108/readiness146.py');F=load('qualification146_compatible_fixture','qualification127/fixtures.py');g=F.g;c=F.c
def env(temp):
 source='a'*40;manifest='b'*64;once='c'*64
 return {'RUNNER_TEMP':str(temp),'GITHUB_REPOSITORY':'Elinfiny/TraceHarbor','GITHUB_REPOSITORY_ID':'1391430317','GITHUB_ACTOR_ID':'273768139','GITHUB_RUN_ID':'77','GITHUB_RUN_ATTEMPT':'1','GITHUB_SHA':source,'GITHUB_WORKFLOW_SHA':source,'TRACE135_SOURCE_SHA':source,'TRACE135_MANIFEST_SHA256':manifest,'TRACE135_ONCE_RECEIPT_SHA256':once}
class Port146(F.Port):
 def invoke(self,id,op,args):
  if op!='github_create_ref':return super().invoke(id,op,args)
  self.calls.append((id,op));self.macro.store.save(id+'/request',{'op':op,'args':args});self.effects.append((id,op,args));self.clock.advance(.01)
  value={'branch':args['branch_name']};proof={'ref':'refs/heads/'+args['branch_name'],'object':{'type':'commit','sha':args['sha']}};self.db['https://api.github.com/repos/'+g.REPO+'/git/ref/heads/'+args['branch_name']]=proof;self.retain(id,value);self.macro.store.save(id+'/return',value);return value
 def wait_recipient146(self):self.clock.advance(1)
 def collect_failure146(self,packet):return {'schema':'SYNTHETIC_FAILURE_ONLY_NOT_SAFE'}
 def run(self,status='in_progress'):
  r=super().run(status);r['updated_at']='1970-01-01T00:20:00Z';return r
def fixture146(port=Port146):
 clock=F.Clock();clock.end_mono=clock.m+T.PARENT;clock.end_utc=clock.u+T.PARENT;io=F.IO(clock);p=port(clock,io);ctx=F.context(clock);ctx.update(expires_utc=clock.end_utc,parent_mono=clock.end_mono);inv=c.Inventory127(c.inventory127(),'SYNTHETIC_SOURCE_ONLY');m=g.Grouped127(p,clock,ctx,'/SYNTHETIC146/originals',io,inv);return m,p,clock,io
class Whole146(unittest.TestCase):
 def test_full_terminal_near_all_changed_phase_caps_and_last_collection(self):
  class NearCaps(Port146):
   def cas(self,phase,version,payload):
    r=super().cas(phase,version,payload);self.clock.advance(74.7);return r
   def dispatch(self):
    r=super().dispatch();self.clock.advance(89.5);return r
   def invoke(self,id,op,args):
    r=super().invoke(id,op,args)
    if id.startswith(('admit/','encrypted/','consumed/')):
     self.clock.advance(14.9)
     if id.endswith('/ref/proof'):self.clock.advance(14.7)
    return r
   def wait_recipient146(self):self.clock.advance(239.5)
   def prepare_delivery(self):
    r=super().prepare_delivery();self.clock.advance(89.4);return r
   def collect_bundle(self,run):
    r=super().collect_bundle(run);self.clock.advance(119.4);return r
  m,p,k,io=fixture146(NearCaps);p.pending=3;r=m.run_complete();self.assertEqual(r['cursor'],16);self.assertGreater(k.u-1000,2200);self.assertLess(k.u,3340);self.assertIsNone(r['first_unknown'])
 def test_actual_source_dispatch_late_run_original_no_second_create(self):
  from types import SimpleNamespace
  n=load('qualification146_native_dispatch','diagnostic108/native127.py');source='a'*40;once='c'*64;args=n.g.p133.g136.args136({'source_sha':source,'manifest_sha256':'b'*64,'once_receipt_sha256':once,'once_expires_utc':'10000','coordinator_cutoff_utc':'10000'});records=[];saved=[];tick={'m':0.}
  def call(id,op,a):
   if id.endswith('ref-absence'):v={'absent':True}
   elif id.endswith('create-ref'):v={'branch':args['branch_name']}
   elif id.endswith('ref-proof'):v={'ref':'refs/heads/'+args['branch_name'],'object':{'type':'commit','sha':source}}
   else:v={'total_count':0,'workflow_runs':[]};tick['m']=61.
   records.append((id,v));return v
  obj=object.__new__(n.NativePort127);obj.source=source;obj.parent_mono=10000.;obj.phase_mono=10000.;obj.config={'ui_dispatch127':{'kind':'git_create136','args':args,'source_sha':source,'once_receipt_sha256':once}};obj.macro=SimpleNamespace(context={'once_receipt_sha256':once},remaining=lambda:10000.,call=call,store=SimpleNamespace(save=lambda *a:saved.append(a)))
  with patch.object(n.time,'monotonic',side_effect=lambda:tick['m']):
   with self.assertRaisesRegex(n.g.Pending127,'Late original'):obj.dispatch()
  self.assertEqual(sum(x[0]=='dispatch136/create-ref' for x in records),1);self.assertEqual(records[-1][0],'dispatch136/runs/0');self.assertTrue(saved)
 def test_shared_API0_cost_hash_and_actual_sparse_provider_steps(self):
  self.assertEqual(F.runner.public_cost_scope146(),T.zero_cost146());self.assertEqual(c.sha(c.can(F.runner.public_cost_scope146())),c.sha(c.can(T.zero_cost146())))
  names=['Checkout exact source146','Run fresh counter146','Bound failure-only allowlist146','Publish bounded failure-only evidence146'];allnames=['Set up job',*names,'Post '+names[0],'Complete job'];numbers=[1,2,3,4,5,26,27];steps=[{'number':n,'name':name,'status':'completed','conclusion':'skipped' if name==names[-1] else 'success'} for n,name in zip(numbers,allnames)];self.assertTrue(F.p.validate_steps127(steps,names))
  bad=copy.deepcopy(steps);bad[2]['number']=bad[1]['number']
  with self.assertRaises(ValueError):F.p.validate_steps127(bad,names)
  bad=copy.deepcopy(steps);bad[2]['conclusion']='skipped'
  with self.assertRaises(ValueError):F.p.validate_steps127(bad,names)
 def test_closed_whole_static_V3_and_no_native_admission(self):
  p=g.p133;raw=(ROOT/'diagnostic108/manifest.json').read_bytes();x=json.loads((ROOT/'qualification146/static_template146.json').read_bytes());x['manifest']={'bytes':len(raw),'sha256':c.sha(raw)};x['limits']=copy.deepcopy(c.FIXED);x['inventory_sha256']=c.sha(c.can(c.inventory127()));x['timing_contract']=copy.deepcopy(T.CONTRACT);x['workflow']['step_names']=[s['name'] for s in json.loads((ROOT/'.github/workflows/traceharbor-counter136.yml').read_bytes())['jobs']['counter']['steps']]
  body='SYNTHETIC146 PRIVATE qualification only; no native admission';direction={'recipient':'TraceHarbor V1','id':'SYNTHETIC146','body':body,'bytes':len(body.encode()),'sha256':c.sha(body.encode()),'native_admission':False};x['authority_projection_sha256']=c.sha(c.can(p.projection133(direction)));r=p.prepare127(x,direction,raw);self.assertFalse(r['native_authority']);self.assertEqual(r['proposed_admission']['contract'],'TRACE146_STATIC_TYPED_RUNTIME_V3')
  with self.assertRaises(PermissionError):p.release133(direction,x,raw)
  bad=copy.deepcopy(x);bad['artifact_contract']['maximum_artifacts']=2
  with self.assertRaises(ValueError):p.static133(bad,raw)
  bad=copy.deepcopy(x);bad['timing_contract']['parent_s']=900
  with self.assertRaises(ValueError):p.static133(bad,raw)
 def test_legacy_rejected_and_dependency_ledger_feasible(self):
  with self.assertRaises(TimeoutError):T.reject_legacy146()
  d=T.schedule146();self.assertEqual(d['critical_path_s'],2295);self.assertEqual(d['slack_s'],45);self.assertFalse(d['native_authority'])
  with self.assertRaises(ValueError):T.preallocate146({'timing_contract':dict(T.CONTRACT,parent_s=900),'observer_contract':{}})
 def test_actual_changed_grouped_call_chain_complete_terminal_fixture(self):
  m,p,k,io=fixture146();r=m.run_complete();self.assertEqual(r['cursor'],16);self.assertIsNone(r['first_unknown']);self.assertEqual(len(p.effects),12);self.assertEqual(len(p.cas_versions),6);self.assertIn('TERMINAL',m.closed);self.assertLess(k.m,2400);self.assertEqual(m.realm,'SYNTHETIC_SOURCE_ONLY')
 def test_slow_CAS_after_prior_intents_stops_before_dispatch(self):
  class Slow(Port146):
   def cas(self,phase,version,payload):
    r=super().cas(phase,version,payload)
    if phase=='PRE_DISPATCH':self.clock.advance(70)
    return r
  m,p,k,io=fixture146(Slow);m.freeze();k.advance(200)
  with self.assertRaisesRegex(TimeoutError,'downstream suffix'):m.predispatch()
  self.assertEqual(len(p.cas_versions),2);self.assertEqual(p.effects,[]);self.assertIsNone(m.run)
 def test_original_clock_refuses_rollback_and_new_origin(self):
  q=T.OriginalClock146(1000,50);q.require(1010,60)
  with self.assertRaises(TimeoutError):q.require(1009,61)
  with self.assertRaises(ValueError):T.OriginalClock146(1000,50,900)
  with self.assertRaises(TimeoutError):q.require(4000,3050)
 def test_late_created_original_retained_no_next_effect_or_restart(self):
  m,p,k,io=fixture146();m.freeze();m.predispatch();p.effect_fault=('admit/blob',220)
  with self.assertRaises(TimeoutError):m.chain('admit')
  self.assertEqual(len(p.effects),1);self.assertTrue(any('admit_blob' in f for f in io.files))
  with self.assertRaises(RuntimeError):m.restart()
 def test_real_anchored_absence_is_failure_only(self):
  with tempfile.TemporaryDirectory() as td:
   r=E.absence146(td,'c'*64);self.assertEqual(r['status'],'OBSERVED_NO_INTAKE');self.assertFalse(r['native_safe']);e=env(td);ctx=E.binding146(e);body=E.failure146(ctx,'TimeoutError',r);self.assertFalse(E.validate_failure146(E.can(body),ctx)['counter_verified'])
 def test_real_symlink_partial_and_permission_error_never_absence(self):
  with tempfile.TemporaryDirectory() as td:
   p=pathlib.Path(td)/('traceharbor-counter117-intake-'+'c'*64);p.symlink_to('/tmp',target_is_directory=True);self.assertTrue(E.absence146(td,'c'*64)['unknown']);p.unlink();p.mkdir(mode=0o700);sentinel=p/'keep';sentinel.write_text('untouched');self.assertTrue(E.absence146(td,'c'*64)['unknown']);self.assertEqual(sentinel.read_text(),'untouched')
   with patch.object(E,'anchored_temp146',side_effect=PermissionError):self.assertEqual(E.absence146(td,'c'*64)['status'],'UNKNOWN')
 def test_mismatched_owned_root_refused_no_delete(self):
  a=load('qualification146_owned_mismatch','diagnostic108/admission116.py')
  with tempfile.TemporaryDirectory() as td:
   root=pathlib.Path(td)/'owned';owner=a.OwnedIntake(root,{'run':'77'},{},create=True);sentinel=root/'keep';sentinel.write_text('valid')
   with self.assertRaises(ValueError):a.OwnedIntake(root,{'run':'78'},{},create=False)
   self.assertEqual(sentinel.read_text(),'valid')
 def test_prior_ATTEMPTING_UNKNOWN_cleanup_never_removed_again(self):
  a=load('qualification146_owned_cleanup','diagnostic108/admission116.py')
  with tempfile.TemporaryDirectory() as td:
   owner=a.OwnedIntake(pathlib.Path(td)/'owned',{'run':'77'},{},create=True,remove=lambda *a,**k:self.fail('cleanup repeated'))
   for i,n in enumerate(sorted(owner.secret_paths())):owner.attempts[n]={'path':n,'status':['ATTEMPTING','UNKNOWN'][i%2]}
   r=owner.cleanup('workflow_always');self.assertTrue(r['unknown']);self.assertTrue(all(x['status']=='UNKNOWN_NO_RETRY' for x in r['cleanup']))
 def test_launch_early_failure_retained_then_real_absence_artifact(self):
  launch=load('qualification146_launch','diagnostic108/launch127.py')
  with tempfile.TemporaryDirectory() as td:
   e=env(td)
   with patch.dict(os.environ,e,clear=True),patch.object(launch,'_main146',side_effect=TimeoutError('injected before NativeProducer construction')):
    with self.assertRaises(TimeoutError):launch.main()
   rec=json.loads((pathlib.Path(td)/'traceharbor-failure146-private/exception.json').read_bytes());self.assertIn('injected',rec['args_repr']);self.assertEqual(rec['context'],E.binding146(e));r=E.absence146(td,'c'*64);p=E.finish_cleanup146(e,r);self.assertEqual(p['cleanup_status'],'OBSERVED_NO_INTAKE');self.assertFalse(p['counter_verified'])
 def test_failure_not_SAFE_or_numeric_even_valid_archive(self):
  with tempfile.TemporaryDirectory() as td:
   ctx=E.binding146(env(td));failure=E.failure146(ctx,'TimeoutError',{'status':'UNKNOWN'});raw=E.can(failure)
   with self.assertRaises(ValueError):F.p.approved_projection127(raw,{'projection_context':ctx},'SOURCE_PRODUCED_PUBLIC_SAFE_DATA')
   plan={k:ctx[k] for k in ('source_sha','manifest_sha256','once_receipt_sha256','run_id')};out=io.BytesIO()
   with zipfile.ZipFile(out,'w') as z:z.writestr('failure.json',raw)
   got=F.p.failure_zip146(out.getvalue(),plan);self.assertIsNone(got['numeric_count']);self.assertFalse(got['counter_verified'])
 def test_failure_closed_allowlist_rejects_private_field_and_wrong_source(self):
  with tempfile.TemporaryDirectory() as td:
   ctx=E.binding146(env(td));d=E.failure146(ctx,'TimeoutError',{'status':'PASS'});d['private_key']='never'
   with self.assertRaises(ValueError):E.validate_failure146(E.can(d),ctx)
 def test_consumed_readiness_hint_positive_and_late_original(self):
  class Clock:
   def __init__(self):self.m=0;self.u=1000;self.end_mono=2340
   def mono(self):return self.m
   def wall(self):return self.u
   def check(self,end):
    if self.m>=end:raise TimeoutError('late')
  k=Clock();rows=[];values=[None,{'ref':'refs/heads/traceharbor-counter116-consumed-'+'c'*64,'object':{'type':'commit','sha':'a'*40}}]
  def pause(n):k.m+=n;k.u+=n
  r=B.wait_ref146(lambda *a,**kw:values.pop(0),k,'c'*64,rows.append,pause);self.assertFalse(r['typed_consumed_proof']);self.assertEqual(len(rows),2)
  k=Clock();rows=[]
  def late(*a,**kw):k.m=16;return None
  with self.assertRaises(TimeoutError):B.wait_ref146(late,k,'c'*64,rows.append,pause)
  self.assertEqual(len(rows),1)
 def test_durable_observer_reservation_no_cloned_plan_unreserved_or_replay(self):
  inv=c.inventory127();subset={'observer_maximum':40,'authority':False,'rows':[r for r in inv['rows'] if r['owner']=='OBSERVER']};b={'source_sha':'a'*40,'manifest_sha256':'b'*64,'static_config_sha256':'c'*64,'inventory_sha256':'d'*64,'direction_id':'SYNTHETIC146','realm':'HOST_ONLY_CANARY'}
  with tempfile.TemporaryDirectory() as td,tempfile.TemporaryDirectory() as clone:
   issued=O.issue(td,b,subset);pin=issued['plan_sha256'];r=O.reserve(td,pin,'cell7','Script running with cell ID cell7');self.assertEqual(r['ticket']['cell_id'],'cell7')
   with self.assertRaises(ValueError):O.reserve(td,pin,'cell7','Script running with cell ID cell7')
   O.retain(td,pin,r['ticket'],{'status':'completed','actual':'fixture'});self.assertEqual(O.verify(td,pin)['waits'],1)
   with self.assertRaises(FileExistsError):O.retain(td,pin,r['ticket'],{'status':'completed'})
   pathlib.Path(clone,'observer146-plan.json').write_bytes(pathlib.Path(td,'observer146-plan.json').read_bytes())
   with self.assertRaises(ValueError):O.plan146(clone,pin)
   with self.assertRaises(ValueError):O.retain(td,pin,dict(r['ticket'],index=1),{'status':'unreserved'})
 def test_parent_clock_run_origin_and_rollback(self):
  a=load('qualification146_parent','diagnostic108/admission116.py');values={'u':1010.,'m':60.};run={'id':77,'run_started_at':'1970-01-01T00:16:40Z'};q=a.ParentClock.from_run(run,3340,3340,wall=lambda:values['u'],mono=lambda:values['m']);self.assertEqual(q.descriptor()['job_limit_s'],2340);q.require(970);values['u']=1009.;values['m']=61.
  with self.assertRaises(TimeoutError):q.require(0)
if __name__=='__main__':unittest.main(verbosity=2)
