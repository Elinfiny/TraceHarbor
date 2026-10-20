"""One NEW127 group; each case run once after the whole final source freeze."""
import sys,json,pathlib,hashlib,copy,types,subprocess,ast
ROOT=pathlib.Path(__file__).resolve().parent.parent
for name,pin in json.loads((ROOT/'qualification127/pins.json').read_bytes()).items():
 raw=(ROOT/name).read_bytes();assert len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256'],name
from fixtures import fixture,through_consumed,refused,g,c,p,runner,Clock,IO
case=int(sys.argv[1]);assert case in range(1,9);details={}
if case==1:
 m,port,clock,io=fixture();port.pending=3;s=m.run_complete();assert s['cursor']==16 and s['first_unknown'] is None and s['scope']=='SYNTHETIC_SOURCE_ONLY';assert len(port.effects)==12 and len(port.cas_versions)==6
 assert [x[0] for x in port.cas_versions]==list(c.PHASES) and [x['name'] for x in [json.loads(io.files[r['path']])['original'] for id,r in m.store.records.items() if id.startswith('semantic/')]]==list(c.SEMANTIC)
 assert m.closed==['SOURCE_FREEZE','PRE_DISPATCH','ADMIT_CHAIN','ENCRYPTED_CHAIN','CONSUMED_CHAIN','SAFE_COLLECTION','TERMINAL'];assert m.parent_mono==1000 and m.parent_wall==1900
 assert all(m.store.io.read(r['path']) and c.sha(m.store.io.read(r['path']))==r['sha256'] for r in m.store.records.values())
 details={'semantic_transitions':16,'ownCAS_readback_pairs':6,'create_only_with_immediate_fullproofs':12,'integrated_safe_and_terminal':'SYNTHETIC_ONLY','all_originals_verified':True,'whole_inventory':m.inventory.plan['inclusive_total']}
elif case==2:
 out=[]
 for key,value in [('version',999),('wholebyte_self_allattrs','FAIL'),('intent_sha256','0'*64)]:
  m,port,clock,io=fixture();port.phase_mutation=('ADMIT_CHAIN',key,value);refused(m.run_complete);assert len(port.effects)==0 and m.failed is not None and 'ADMIT_CHAIN' in m.consumed;out.append(key)
 m,port,clock,io=fixture();original=port.admit_descriptor;port.admit_descriptor=lambda:dict(original(),source_sha='0'*40);refused(m.run_complete);assert not port.effects;out.append('source/body')
 details={'rejected_before_first_external_create':out,'consumed_intents_not_reset':True}
elif case==3:
 out={}
 for name,fault in [('partial','partial'),('late',111),('UNKNOWN',OSError('EXPLICIT_SYNTHETIC_UNKNOWN_CREATE'))]:
  m,port,clock,io=fixture();port.effect_fault=('encrypted/blob',fault);refused(m.run_complete);before=len(port.effects);first=copy.deepcopy(m.failed);refused(m.restart);refused(m.run_complete);assert len(port.effects)==before and m.failed==first and 'ENCRYPTED_CHAIN' in m.consumed and m.cursor==6 and m.safe is None
  assert any('encrypted_blob' in path for path in io.files);out[name]={'effects_before_refusal':before,'first_unknown':first,'restart_effects':0,'ready_releases':0}
 details=out
elif case==4:
 out={}
 for cap in (0,1,2,3):
  m,port,clock,io=fixture();m.inventory.test_limit=cap;refused(m.run_complete);assert not port.effects;m.store.save('closure/original',{'synthetic':'reserved closure available'});out[str(cap)]={'next_tool_calls':len(port.calls),'closure_reserved':True,'first_unknown':m.failed is not None}
 m,port,clock,io=fixture();m.inventory.test_limit=0;refused(lambda:m.inventory.claim('collection/delay/0'));assert 'collection/delay/0' not in m.inventory.claimed
 # Actual new caller JS functions execute against explicit inert tool fixtures.
 node=subprocess.run(['node',str(ROOT/'qualification127/test_caller.mjs')],capture_output=True,timeout=15);assert node.returncode==0,node.stderr.decode();out['actual_new_JS_entrypoints']={'exit_code':node.returncode,'stdout':node.stdout.decode(),'stderr':node.stderr.decode()}
 details={'evidence_callback_effect_wait_exhaustion':out,'current48_refuses_native':refused(lambda:c.Inventory127(c.inventory127(),'ACTUAL_SOURCE_PRIVATE',48))}
elif case==5:
 m,port,clock,io=through_consumed();old=copy.deepcopy(port.bound);clock.advance(111);refused(m.collect);m.begin_collection();assert port.bound['name']=='SAFE_COLLECTION' and port.bound['end_mono']>old['end_mono'] and m.parent_mono==1000 and m.parent_wall==1900;m.collect();m.terminal()
 expired,ep,ec,ei=through_consumed();ec.advance(1000);refused(expired.begin_collection)
 pending,pp,pc,pi=through_consumed();pp.pending=4;pending.begin_collection();refused(pending.collect);assert len([x for x in pp.calls if x[0].startswith('collection/run/')])==4 and pending.failed is None
 details={'stale_consumed_clock_refused':True,'separate_original_parent_interval':'PASS_SYNTHETIC','original_parent_expiry_refused':True,'pending_is_data_four_finite_observations_no_relaunch':True}
elif case==6:
 variants={}
 for name,mutate in [('provisional',lambda x:x['phases']['proof'].update(post_io_mono=x['phases']['proof']['end_mono'])),('preIO',lambda x:x['phases']['cleanup'].update(post_io_utc=x['phases']['cleanup']['begin_utc']-1)),('privatefield',lambda x:x.update(raw_private_counter_stdout='REFUSE'))]:
  m,port,clock,io=through_consumed();port.projection_mutator=mutate;m.begin_collection();refused(m.collect);assert m.cursor==15;variants[name]='REFUSED_IN_INTEGRATED_COLLECTION'
 m,port,clock,io=fixture();m.run_complete();refused(lambda:p.require_native_terminal127(port,m));fake=types.ModuleType('Forged127');refused(lambda:p.register_native_host127(port,fake,{},{}));refused(lambda:g.Grouped127(port,clock,m.context,'/SYNTHETIC-NATIVE',io,m.inventory,'ACTUAL_SOURCE_PRIVATE'))
 # The actual protected provisional receipt implementation stays in-path.
 phase=c.accepted.SafePhases126(clock,'/SYNTHETIC127/phases',{},900,io);phase.begin('cleanup');io.fault=('cleanup',11);assert phase.close('cleanup',{'SYNTHETIC':'stop'}) is False and not phase.accepts();refused(lambda:phase.begin('proof'))
 details={'integrated_negative_projection':variants,'synthetic_to_native_and_forged_module':'REFUSED','postIO_late_cleanup_no_proof':True,'native_observations':0}
elif case==7:
 details={}
 class Output:
  def __init__(self,fail=False):self.calls=0;self.fail=fail
  def close(self):self.calls+=1;raise OSError('SYNTHETIC output.close') if self.fail else RuntimeError('unused')
 class GoodOutput(Output):
  def close(self):self.calls+=1
 for name,exc,close_fail in [('write',OSError('SYNTHETIC write'),False),('fsync',OSError('SYNTHETIC fsync'),True),('schema',ValueError('SYNTHETIC schema'),True)]:
  output=Output(True) if close_fail else GoodOutput();primary={'original':'EARLIER_PRIMARY'} if name=='schema' else None;cleanup=[];result={'primary':primary,'cleanup':cleanup,'exit_code':0};calls=[];saved=[]
  def export():calls.append('ONE');raise exc
  original=runner.closeout127(result,output,export,lambda n,v:saved.append((n,v)));assert output.calls==1 and len(calls)==1 and original['export_exception'] is exc and original['primary'] is primary and original['cleanup'] is cleanup and result['exit_code']==1
  assert result['closeout127']['first_original_error']==('PRIMARY' if primary else 'EXPORT') and len(saved)==1+int(close_fail);details[name]={'export_attempts':1,'close_attempts':1,'cleanup_calls':0,'first':result['closeout127']['first_original_error'],'error_records':len(saved)}
 # Verify actual execute() source calls this closeout and no unguarded export.
 tree=ast.parse((ROOT/'diagnostic108/launch127.py').read_bytes());execute=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='execute');calls=[x for x in ast.walk(execute) if isinstance(x,ast.Call)];assert sum(isinstance(x.func,ast.Attribute) and x.func.attr=='closeout127' for x in calls)==1
 assert not any(isinstance(x.func,ast.Attribute) and x.func.attr=='close' for x in calls);details['actual_launch_finally_binding']='ONE_FIXED_CLOSEOUT_NO_OTHER_OUTPUT_CLOSE'
elif case==8:
 out={}
 for variant in ('correct','allattrs','EOF','digest','source','once','late','pending_terminal'):
  m,port,clock,io=through_consumed()
  def mutate(plan,b):
   if variant=='allattrs':b['materialized'].fixture_file_facts['xattrs']['user.source-fixture']='DRIFT'
   elif variant=='EOF':b['materialized'].fixture_file_facts['whole_eof']=False
   elif variant=='digest':b['artifacts'].original['structuredContent']['artifacts'][0]['digest']='sha256:'+'0'*64
   elif variant=='source':v=json.loads(b['commit'].original['structuredContent']['content']);v['sha']='0'*40;b['commit'].original['structuredContent']['content']=json.dumps(v)
   elif variant=='once':pass
   elif variant=='late':clock.advance(151)
   elif variant=='pending_terminal':jobs=b['jobs'].original['structuredContent'];jobs['jobs'][0]['steps'][-1]['status']='in_progress'
  port.file_mutator=mutate
  if variant=='once':port.projection_mutator=lambda x:x['context'].update(once_receipt_sha256='0'*64)
  m.begin_collection()
  if variant=='correct':m.collect();m.terminal();assert m.cursor==16;out[variant]='PASS_NAME_FILTERED_SAFE_PLUS_SEPARATE_RECIPIENT_ALLOWED'
  else:refused(m.collect);assert m.cursor==15;out[variant]='REFUSED_BEFORE_TERMINAL'
 details={'full_integrated_provider_fixture':out,'provider_setup_post_labels':'EXPLICIT_SYNTHETIC_SUPPORTED_ROLES_NOT_LIVE_OBSERVATION','genuine_native_provider_calls':0}
print(json.dumps({'NEW127_case':case,'PASS':True,'scope':'SYNTHETIC_SOURCE_ONLY_ACTUAL_NEW_INTEGRATED_ENTRYPOINTS','live_native_holder_guard_IPC_projectfsync_counter_model_provider_requests':0,'details':details},ensure_ascii=False))
