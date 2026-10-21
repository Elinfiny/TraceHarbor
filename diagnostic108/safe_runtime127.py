"""PRIVATE127 actual-source implementation proposal; NOT installed or activated.

Place after existing launch.finish in the SAME independently admitted runner
invocation. It consumes the already live NativeProducer and authentic output;
it neither manufactures q nor calls the counter, crypto, Docker or a provider.
The companion controller binding is an in-process candidate. Cross-process
delivery requires an independently admitted native-original adapter; a JSON
report cannot be reconstructed into this opaque object.
"""
import copy,hashlib,json,os,pathlib,stat,time,importlib.util
_ctl_spec127=importlib.util.spec_from_file_location("trace127_runner_control",pathlib.Path(__file__).with_name("control126.py"));_ctl127=importlib.util.module_from_spec(_ctl_spec127);_ctl_spec127.loader.exec_module(_ctl127)
SafePhases127=_ctl127.SafePhases126;DiskOriginalIO127=_ctl127.DiskOriginalIO126
_SEAL=object()
def can(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(v):return hashlib.sha256(v).hexdigest()
def identity(s):return (s.st_dev,s.st_ino,s.st_mode,s.st_uid,s.st_size,s.st_mtime_ns)
def original(path,cap=1048576):
 p=pathlib.Path(path);s=p.lstat()
 if p.is_symlink() or not stat.S_ISREG(s.st_mode) or s.st_uid!=os.getuid() or s.st_mode&0o077 or s.st_size>cap:raise ValueError('Owned bounded original only')
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  if identity(os.fstat(fd))!=identity(s):raise ValueError('Original changed before open')
  raw=os.read(fd,cap+1)
  if os.read(fd,1) or len(raw)!=s.st_size or identity(os.fstat(fd))!=identity(s):raise ValueError('Complete stable original only')
 finally:os.close(fd)
 return raw
class NativeSafeObservation127:
 __slots__=('producer','consumed','clock','binding','proof','originals','end_mono','end_utc','seal','used','phase_receipts')
 def __init__(self,key,producer,consumed,binding,proof,originals,phase_receipts):
  if key is not _SEAL:raise TypeError('Only actual factory, never serialized SAFE')
  self.producer=producer;self.consumed=consumed;self.clock=producer.clock
  self.binding=can(binding);self.proof=can(proof);self.originals=copy.deepcopy(originals)
  self.phase_receipts=phase_receipts;self.end_mono=producer.clock.end_mono;self.end_utc=producer.clock.end_utc;self.seal=key;self.used=False
def capture_after_finish127(g,counter,repo,plan,evidence,output,terminal,approved,private,proof_path,finish_result,first_unknown,phase_receipts):
 """Original SAFE/stop/cleanup factory, called only after actual finish returned.

 All supplied data are cross-checked against existing live native identities,
 saved originals and source-owned counter reader. No dictionary grants release.
 Raw counter bytes remain in the original protected output and are not exported.
 """
 p=counter.producer_module(pathlib.Path(repo));producer=plan['producer'];consumed=plan['consumption']
 if type(phase_receipts) is not SafePhases127 or not phase_receipts.active_proof(producer):raise TypeError('Actual cleanup10/proof15 same original receipts')
 if phase_receipts.realm!='ACTUAL_SOURCE_PRIVATE' or type(phase_receipts.io) is not DiskOriginalIO127 or phase_receipts.clock is not producer.clock or phase_receipts.binding!=producer.caller.binding:raise TypeError('Synthetic or foreign phase receipts cannot mint runtime observation')
 for module,name in ((g,'launch127.py'),(counter,'counter115.py'),(p,'admission116.py')):
  path=pathlib.Path(repo)/'diagnostic108'/name;raw=path.read_bytes()
  if pathlib.Path(module.__file__).resolve()!=path.resolve() or (len(raw),sha(raw))!=SOURCE_PINS127[name]:raise ValueError('Exact reviewed actual producer/exporter/counter source')
 if type(producer) is not p.NativeProducer or type(producer.caller) is not p.NativeCaller or producer._g is not g:raise TypeError('Actual SAME producer/caller/module')
 if type(consumed) is not p.NativeConsumedProof or consumed.producer is not producer or consumed.custody is not plan['custody'] or consumed.clock is not producer.clock or consumed is not producer.consumption:raise TypeError('Actual opaque SAME consumed proof')
 if producer.clock.wall is not time.time or producer.clock.mono is not time.monotonic:raise TypeError('No synthetic clock at actual SAFE boundary')
 producer.clock.require(0)
 if first_unknown is not None or finish_result['primary'] is not None or finish_result['cleanup'] or finish_result['capture_failures'] or finish_result['exit_code']!=0 or not finish_result['proof_saved']:raise ValueError('FirstUNKNOWN and cleanup cannot be relabelled SAFE')
 if not isinstance(evidence,g.HostEvidence) or evidence.key is not g._HOST_KEY or evidence.source!=producer.caller.binding['source_sha']:raise ValueError('Authentic mount evidence')
 rawproof=original(proof_path);proof=g.strict(rawproof)
 binding=producer.caller.binding
 if proof['binding']!=binding or proof['primary'] is not None or proof['cleanup'] or proof['census_refusal'] is not None or proof['qualification_approved'] is not True or proof['mount_provenance_observed'] is not True or proof['container_stopped_observed'] is not True or proof['raw_exposure_permitted'] is not True:raise ValueError('Whole actual SAFE exporter proof')
 if proof['terminal']!=g.terminal_projection(terminal) or proof['terminal']['running'] is not False:raise ValueError('Original stopped terminal')
 native=proof['qualification113']
 if native['binding']!=binding or any(native.get(k)!='PASS' for k in ('native','inventory','native_cleanup')) or native.get('diagnostic_admitted') is not True:raise ValueError('Actual same-run qualification')
 # This existing source verifies complete original counter stdout/stderr,
 # isolation, process terminal, rendering and candidate count. No new invocation.
 projected=counter.verify_host_completion(g,plan,output,terminal,approved)
 if projected['T'] is not None or projected['authority'] is not False or projected['model_calls']!=0 or projected['source_sha']!=binding['source_sha'] or proof['counter115']!=projected:raise ValueError('Tnull actual original counter closure')
 originals={}
 for name,wanted in [('primary.json',None),('original-terminal.json',terminal),('host-terminal.json',finish_result)]:
  raw=original(pathlib.Path(private)/name)
  if g.strict(raw)!=wanted:raise ValueError('Saved first primary/terminal/result differs')
  originals[name]={'bytes':len(raw),'sha256':sha(raw)}
 cleanup=producer.owner.read_small('cleanup117.jsonl')
 rows=[g.strict(line) for line in cleanup.splitlines() if line.strip()]
 latest={row['path']:row for row in rows}
 if set(latest)!=set(producer.owner.secret_paths()) or any(row.get('status') not in ('REMOVED','OBSERVED_ABSENT') for row in latest.values()):raise ValueError('Actual owned-intake cleanup completion')
 # Inspect actual cleanup receipt already returned by the existing producer.
 intake=original(pathlib.Path(private)/'intake117-cleanup.json');receipt=g.strict(intake)
 if receipt.get('unknown') is not False or receipt.get('status')!='PASS' or receipt.get('cleanup') or {row['path']:row for row in receipt['paths']}!=latest:raise ValueError('Intake cleanup not complete')
 originals.update(proof={'bytes':len(rawproof),'sha256':sha(rawproof)},consumption={'bytes':len(consumed.descriptor),'sha256':sha(consumed.descriptor)},provider_provenance={'bytes':len(consumed.provenance),'sha256':sha(consumed.provenance)},intake_cleanup={'bytes':len(intake),'sha256':sha(intake)},counter_stdout={'sha256':projected['raw_sha256']})
 run=producer.caller.run
 if str(run['id'])!=binding['run_id'] or run['head_sha']!=binding['source_sha'] or run['run_attempt']!=1 or run['actor']['id']!=p.OWNER or run['repository']['id']!=p.REPO:raise ValueError('Authentic original current run/source/Owner')
 originals.update(native_run={'sha256':sha(can(run))},provider_originals={'count':len(producer.observations),'sha256':sha(can(producer.observations))},original_parent=producer.clock.descriptor(),source_pins=copy.deepcopy(SOURCE_PINS127))
 producer.clock.require(0)
 return NativeSafeObservation127(_SEAL,producer,consumed,binding,proof,originals,phase_receipts)

def finish_with_native_safe127(g,counter,repo,plan,evidence,output,terminal,approved,private,proof_directory,first_unknown,cleanup_fn,main_end):
 """Actual source placement; cleanup once, provisional receipt post-IO closure.
 No second phase-receipt write, unlink, retry or deadline reset on any error.
 """
 producer=plan['producer'];g._SAFE127_OBSERVATION=None;phases=None
 try:
  p=counter.producer_module(pathlib.Path(repo))
  if type(producer) is not p.NativeProducer or producer._g is not g:raise TypeError('Actual SAME native producer')
  phases=SafePhases127(producer.clock,private,producer.caller.binding,main_end,DiskOriginalIO127(),'ACTUAL_SOURCE_PRIVATE')
 except BaseException as error:
  result=g.finish(private,proof_directory,output,evidence,producer.caller.binding,first_unknown,terminal,approved,cleanup_fn)
  result['capture_failures'].append(g.primary('EXPORT','OUTPUT_SCHEMA',error));result['exit_code']=1;return result
 def cleanup_once():
  phases.begin('cleanup')
  try:value=cleanup_fn()
  except BaseException as error:
   native={'exception_class':type(error).__name__,'status':'UNKNOWN_NO_RETRY'};phases.unknown('Actual cleanup exception');phases.close('cleanup',native);raise
  native={'failures':value[0],'stopped':value[1]}
  if native['failures'] or native['stopped'] is not True:phases.unknown('Actual stop/cleanup incomplete')
  if not phases.close('cleanup',native):value=(list(value[0])+[g.primary('CLEANUP','DEADLINE',TimeoutError())],value[1])
  if phases.accepts('cleanup'):phases.begin('proof')
  return value
 result=g.finish(private,proof_directory,output,evidence,producer.caller.binding,first_unknown,terminal,approved,cleanup_once)
 try:
  if not phases.active_proof():raise RuntimeError('No timely cleanup, no proof release')
  observation=capture_after_finish127(g,counter,repo,plan,evidence,output,terminal,approved,private,pathlib.Path(proof_directory)/'proof.json',result,first_unknown,phases)
  original={'finish_result':copy.deepcopy(result),'runner_proof_sha256':sha(observation.proof),'source_binding_sha256':sha(observation.binding)}
  if not phases.close('proof',original) or not phases.accepts():raise TimeoutError('Actual LAST receipt IO/close overran cleanup10/proof15')
  # Whole receipt reads above may themselves be slow: final own-phase postguard
  # precedes opaque release. Timely closure is never inferred from saved JSON.
  if producer.clock.mono()>=phases.phases['proof']['end_mono'] or producer.clock.wall()>=phases.phases['proof']['end_utc']:phases.unknown('Final proofvalidation late');raise TimeoutError('Late final proof validation')
  g._SAFE127_OBSERVATION=observation
 except BaseException as error:
  phases.unknown('First SAFE127 '+type(error).__name__);result['capture_failures'].append(g.primary('EXPORT','OUTPUT_SCHEMA',error));result['exit_code']=1
 # Existing consolidated result carries post-IO truth. Receipt files remain
 # immutable provisional facts; no recursive receipt-about-receipt fsync.
 result['safe127_phase_closure']={'first_unknown':phases.first_unknown,'phases':{n:({'post_io_mono':c.post_mono,'post_io_utc':c.post_utc,'timely':c.timely,'error':c.error} if c is not None else None) for n,c in phases.closures.items()}}
 return result
def export_public_projection127(g,plan,directory,manifest_sha256):
 """Ordinary redacted closeout AFTER protected proof, within remaining parent.
 Never exports privatecode/inputs/rawstdout/tokens/keys/URLs. Future workflow
 uploads only this fixed file; it is DATA, not self-asserted authority.
 """
 observation=g._SAFE127_OBSERVATION;producer=plan['producer']
 if type(observation) is not NativeSafeObservation127 or observation.seal is not _SEAL or observation.producer is not producer or not observation.phase_receipts.accepts():raise TypeError('Actual original runner SAFE observation only')
 consumed=json.loads(observation.consumed.descriptor);binding=producer.caller.binding
 context={'run_id':int(binding['run_id']),'attempt':1,'actor_id':273768139,'repository_id':1391430317,'source_sha':binding['source_sha'],'manifest_sha256':manifest_sha256,'once_receipt_sha256':binding['once_receipt_sha256'],'expires_utc':producer.clock.end_utc,'admission_sha256':sha(can(producer.caller.receipt)),'custody_binding_sha256':sha(can(consumed['ciphertext_receipt'])),'cost_scope_sha256':sha(can(public_cost_scope146()))}
 public={'schema':'TRACE127_MINIMAL_SAFE_V1','scope':'SOURCE_PRODUCED_PUBLIC_SAFE_DATA','context':context,'counter':{'verified':True,'T':None,'counter_invocations':1,'model_calls':0},'stop_cleanup':{'consumer_stopped':True,'cleanup_complete':True,'first_unknown':None},'phases':observation.phase_receipts.redacted(),'runner_proof_sha256':sha(observation.proof)}
 raw=can(public)
 if len(raw)>8192:raise ValueError('Minimal redacted projection cap')
 producer.clock.require(0);directory=pathlib.Path(directory);directory.mkdir(mode=0o700,exist_ok=False)
 fd=os.open(directory/'projection.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 producer.clock.require(0)
 return {'bytes':len(raw),'sha256':sha(raw),'classification':'ORDINARY_POST_SAFE_CLOSEOUT_INSIDE_REMAINING_ORIGINAL900_ONCE_NOT_PROOF15'}

SOURCE_PINS127={'launch127.py': (54299, '57d9540cb2c442829038a4639a36de2b43489ea07a5a3d1f896fd6ac75fda788'), 'counter115.py': (16288, 'cf14a494c743754f0a1aa2a88de22b228e7844500aa73e7dee7686128e8fcd4b'), 'admission116.py': (50534, '9acc7aa4960ef0c7733ae927da64108deba3838ec9198a969ac7ed26283a854b')}

def closeout127(result,output,exporter=None,retain=None):
 """Exactly once ordinary closeout even after projection O_EXCL/write/fsync.
 No cleanup invocation, retry, rewrite or unlink exists in this function.
 """
 originals={'primary':result.get('primary'),'cleanup':result.get('cleanup'),'export_exception':None,'close_exception':None,'retention_exceptions':[]}
 def message(exc):
  try:return str(exc)
  except BaseException as fault:originals['retention_exceptions'].append(fault);return 'ORIGINAL_EXCEPTION_STRING_CONVERSION_FAILED'
 def preserve(name,exc):
  # Keep the actual object/traceback BEFORE any JSON conversion can fail.
  originals[name]=exc
  if retain is not None:
   try:retain(name,{'exception_class':type(exc).__name__,'message':message(exc),'traceback':__import__('traceback').format_exception(type(exc),exc,exc.__traceback__),'primary':originals['primary'],'cleanup':originals['cleanup'],'status':'UNKNOWN_NO_RETRY'})
   except BaseException as fault:originals['retention_exceptions'].append(fault)
 try:
  if exporter is not None and result.get('exit_code')==0:
   try:result['public_projection127']=exporter()
   except BaseException as exc:
    preserve('export_exception',exc)
    result['export_error127']={'exception_class':type(exc).__name__,'message':message(exc),'status':'UNKNOWN_NO_RETRY'};result['exit_code']=1
 finally:
  if output is not None:
   try:output.close()
   except BaseException as exc:
    preserve('close_exception',exc)
    result['close_error127']={'exception_class':type(exc).__name__,'message':message(exc),'status':'UNKNOWN_NO_RETRY'};result['exit_code']=1
 result['closeout127']={'first_original_error':('PRIMARY' if originals['primary'] is not None else 'CLEANUP' if originals['cleanup'] else 'EXPORT' if originals['export_exception'] is not None else 'OUTPUT_CLOSE' if originals['close_exception'] is not None else None),'cleanup_preserved':result.get('cleanup') is originals['cleanup'],'output_close_attempts':int(output is not None),'unknown':originals['export_exception'] is not None or originals['close_exception'] is not None or bool(originals['retention_exceptions']),'retention_error_classes':[type(x).__name__ for x in originals['retention_exceptions']]}
 return originals

def public_cost_scope146():
 s=importlib.util.spec_from_file_location('trace146_SAFE_cost',pathlib.Path(__file__).with_name('timing146.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m.zero_cost146()
