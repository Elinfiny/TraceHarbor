"""PRIVATE125 actual-source implementation proposal; NOT installed or activated.

Place after existing launch.finish in the SAME independently admitted runner
invocation. It consumes the already live NativeProducer and authentic output;
it neither manufactures q nor calls the counter, crypto, Docker or a provider.
The companion controller binding is an in-process candidate. Cross-process
delivery requires an independently admitted native-original adapter; a JSON
report cannot be reconstructed into this opaque object.
"""
import copy,hashlib,json,os,pathlib,stat,time
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
class NativeSafeObservation125:
 __slots__=('producer','consumed','clock','binding','proof','originals','end_mono','end_utc','seal','used','phase_receipts')
 def __init__(self,key,producer,consumed,binding,proof,originals,phase_receipts):
  if key is not _SEAL:raise TypeError('Only actual factory, never serialized SAFE')
  self.producer=producer;self.consumed=consumed;self.clock=producer.clock
  self.binding=can(binding);self.proof=can(proof);self.originals=copy.deepcopy(originals)
  self.phase_receipts=phase_receipts;self.end_mono=producer.clock.end_mono;self.end_utc=producer.clock.end_utc;self.seal=key;self.used=False
def capture_after_finish125(g,counter,repo,plan,evidence,output,terminal,approved,private,proof_path,finish_result,first_unknown,phase_receipts):
 """Original SAFE/stop/cleanup factory, called only after actual finish returned.

 All supplied data are cross-checked against existing live native identities,
 saved originals and source-owned counter reader. No dictionary grants release.
 Raw counter bytes remain in the original protected output and are not exported.
 """
 p=counter.producer_module(pathlib.Path(repo));producer=plan['producer'];consumed=plan['consumption']
 if type(phase_receipts) is not NativeSafePhases125 or not phase_receipts.active_proof(producer):raise TypeError('Actual cleanup10/proof15 same original receipts')
 for module,name in ((g,'launch.py'),(counter,'counter115.py'),(p,'admission116.py')):
  path=pathlib.Path(repo)/'diagnostic108'/name;raw=path.read_bytes()
  if pathlib.Path(module.__file__).resolve()!=path.resolve() or (len(raw),sha(raw))!=SOURCE_PINS125[name]:raise ValueError('Exact reviewed actual producer/exporter/counter source')
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
 originals.update(native_run={'sha256':sha(can(run))},provider_originals={'count':len(producer.observations),'sha256':sha(can(producer.observations))},original_parent=producer.clock.descriptor(),source_pins=copy.deepcopy(SOURCE_PINS125))
 producer.clock.require(0)
 return NativeSafeObservation125(_SEAL,producer,consumed,binding,proof,originals,phase_receipts)
class ControllerSafeBinding125:
 """Concrete SAME-process terminal-binding proposal. No runtime installation.

 A source-reviewed placement must pass the original opaque observation; no
 artifact hash, boolean, PID, fixture or constructor-by-JSON is an alternative.
 Binding does not mint a counter capability or numeric/financial grant.
 """
 __slots__=('observation','transport','macro','remaining_s','activation')
 def __init__(self,transport,macro,observation,ordinary_admin_budget_s):
  if type(observation) is not NativeSafeObservation125 or observation.seal is not _SEAL or observation.used:raise TypeError('Original unused native SAFE observation')
  state=macro.snapshot();binding=json.loads(observation.binding)
  if not observation.phase_receipts.accepts(observation.producer) or state['scope']=='SYNTHETIC_SOURCE_ONLY' or state['first_unknown'] is not None or state['cursor']!=15:raise ValueError('Actual completed CONSUMED phase without UNKNOWN')
  context=transport.config['context']
  for key in ('source_sha','run_id','once_receipt_sha256'):
   if context[key]!=binding[key]:raise ValueError('Same current run/source/once')
  if transport.parent_mono!=observation.end_mono or transport.config['deadline_utc_ms']/1000!=observation.end_utc:raise ValueError('Same ORIGINAL900 parent/epoch/once expiry')
  remaining=min(observation.end_mono-time.monotonic(),observation.end_utc-time.time())
  if type(ordinary_admin_budget_s) not in (int,float) or ordinary_admin_budget_s<=0 or remaining<=ordinary_admin_budget_s:raise TimeoutError('Ordinary terminal budget inside remaining ORIGINAL parent, never proof15')
  self.observation=observation;self.transport=transport;self.macro=macro;self.remaining_s=remaining;self.activation='PRIVATE_CANDIDATE_REQUIRES_INDEPENDENT_SOURCE_RELEASE'
  observation.used=True
 def accepts(self,transport,macro):
  return self.transport is transport and self.macro is macro and macro.snapshot()['first_unknown'] is None and time.monotonic()<self.observation.end_mono and time.time()<self.observation.end_utc

# Private125 concrete protected-phase receipt/placement implementation.
class NativeSafePhases125:
 __slots__=('producer','clock','parent_mono','parent_utc','main_end','cleanup','proof','first_unknown','root','seal')
 def __init__(self,producer,root,main_end):
  self.producer=producer;self.clock=producer.clock;self.parent_mono=self.clock.end_mono;self.parent_utc=self.clock.end_utc;self.main_end=main_end;self.root=pathlib.Path(root);self.cleanup=None;self.proof=None;self.first_unknown=None;self.seal=_SEAL
  if self.clock.wall is not time.time or self.clock.mono is not time.monotonic:raise TypeError('Actual source clocks only')
  if type(main_end) not in (int,float) or main_end>self.parent_mono:raise ValueError('Existing actual main720 end under original900')
 def fail(self,reason):
  if self.first_unknown is None:self.first_unknown=reason
 def begin(self,name,seconds):
  if (name,seconds) not in (('cleanup',10),('proof',15)) or getattr(self,name) is not None:raise ValueError('Fixed once cleanup10 then proof15')
  if name=='proof' and (self.cleanup is None or self.cleanup.get('closed') is not True):raise ValueError('Cleanup original must close first')
  mono=time.monotonic();wall=time.time();epoch_bound=mono+max(0,self.parent_utc-wall)
  record={'phase':name,'run_source_once_binding_sha256':sha(can(self.producer.caller.binding)),'begin_mono':mono,'begin_utc':wall,'end_mono':min(mono+seconds,self.parent_mono,self.main_end,epoch_bound),'parent_mono':self.parent_mono,'parent_utc':self.parent_utc,'main_end_mono':self.main_end,'seconds_cap':seconds,'closed':False}
  setattr(self,name,record)
  if mono>=record['end_mono']:self.fail('Original protected phase expired before '+name)
  return record
 def close(self,name,original_value):
  record=getattr(self,name);mono=time.monotonic();wall=time.time()
  record.update(return_mono=mono,return_utc=wall,original_sha256=sha(can(original_value)))
  if mono>=record['end_mono'] or wall>=self.parent_utc:self.fail('Late original protected '+name)
  record['closed']=self.first_unknown is None
  path=self.root/('safe125-'+name+'-receipt.original.json');raw=can(record)
  fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
  with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
  record['saved_sha256']=sha(raw)
  return record['closed']
 def active_proof(self,producer):
  return self.seal is _SEAL and self.producer is producer and self.clock is producer.clock and self.first_unknown is None and self.cleanup is not None and self.cleanup['closed'] is True and self.proof is not None and self.proof['closed'] is False and time.monotonic()<self.proof['end_mono'] and time.time()<self.parent_utc
 def accepts(self,producer):
  if self.seal is not _SEAL or self.producer is not producer or self.clock is not producer.clock or self.parent_mono!=self.clock.end_mono or self.parent_utc!=self.clock.end_utc or self.first_unknown is not None:return False
  for name in ('cleanup','proof'):
   r=getattr(self,name)
   if r is None or r['closed'] is not True or r['return_mono']>=r['end_mono'] or r['return_utc']>=self.parent_utc:return False
   raw=original(self.root/('safe125-'+name+'-receipt.original.json'))
   wanted={k:v for k,v in r.items() if k!='saved_sha256'}
   if sha(raw)!=r['saved_sha256'] or raw!=can(wanted):return False
  return time.monotonic()<self.parent_mono and time.time()<self.parent_utc
def finish_with_native_safe125(g,counter,repo,plan,evidence,output,terminal,approved,private,proof_directory,first_unknown,cleanup_fn,main_end):
 """Exact replacement call at launch's existing finish point, before extras/close.

 Cleanup is always invoked ONCE by existing finish even if proof binding fails.
 Native originals and phase receipts are saved before postguards; failures keep
 the first source primary and return exit1. No counter/model/provider dispatch.
 """
 producer=plan['producer'];g._SAFE125_OBSERVATION=None;phases=None
 try:
  p=counter.producer_module(pathlib.Path(repo))
  if type(producer) is not p.NativeProducer or producer._g is not g:raise TypeError('Actual SAME native producer only')
  phases=NativeSafePhases125(producer,private,main_end)
 except BaseException as error:
  result=g.finish(private,proof_directory,output,evidence,producer.caller.binding,first_unknown,terminal,approved,cleanup_fn)
  result['capture_failures'].append(g.primary('EXPORT','OUTPUT_SCHEMA',error));result['exit_code']=1;return result
 def cleanup_once():
  phases.begin('cleanup',10)
  try:
   value=cleanup_fn()
  except BaseException as error:
   native={'exception_class':type(error).__name__,'status':'UNKNOWN_NO_RETRY'}
   g.record(pathlib.Path(private),'safe125-cleanup-native.original.json',native);phases.fail('Actual cleanup exception');phases.close('cleanup',native);raise
  native={'failures':value[0],'stopped':value[1]}
  g.record(pathlib.Path(private),'safe125-cleanup-native.original.json',native)
  if native['failures'] or native['stopped'] is not True:phases.fail('Actual stop/cleanup not complete')
  timely=phases.close('cleanup',native)
  if not timely:value=(list(value[0])+[g.primary('CLEANUP','DEADLINE',TimeoutError())],value[1])
  if phases.cleanup['closed']:phases.begin('proof',15)
  return value
 result=g.finish(private,proof_directory,output,evidence,producer.caller.binding,first_unknown,terminal,approved,cleanup_once)
 # This exact result is still identical to existing saved host-terminal.json.
 try:
  native={'finish_result':copy.deepcopy(result),'proof_sha256':sha(original(pathlib.Path(proof_directory)/'proof.json')) if result['proof_saved'] else None}
  g.record(pathlib.Path(private),'safe125-proof-native.original.json',native)
  if phases.proof is None:raise ValueError('No timely actual cleanup, no proof authority')
  observation=capture_after_finish125(g,counter,repo,plan,evidence,output,terminal,approved,private,pathlib.Path(proof_directory)/'proof.json',result,first_unknown,phases)
  # Whole original counter/proof validation is inside this original proof15.
  if not phases.close('proof',native) or not phases.accepts(producer):raise TimeoutError('Actual cleanup10/proof15/original900/once receipts')
  observation.originals['protected_phase_receipts']={name:dict(getattr(phases,name)) for name in ('cleanup','proof')}
  g._SAFE125_OBSERVATION=observation
 except BaseException as error:
  phases.fail('SAFE observation '+type(error).__name__)
  g.record(pathlib.Path(private),'safe125-first-binding-fault.original.json',{'exception_class':type(error).__name__,'first_unknown':phases.first_unknown,'status':'UNKNOWN_NO_RETRY'})
  result['capture_failures'].append(g.primary('EXPORT','OUTPUT_SCHEMA',error));result['exit_code']=1
 return result
def install_same_process_safe125(transport,macro,runner,ordinary_admin_budget_s):
 """Only a live original runner heap can enter this proposed controller API.

 Cross-process artifact delivery is not implemented here and is never faked by
 deserializing JSON. The independent source review must admit real placement.
 """
 if getattr(runner,'_SAFE125_API',None) is not __import__('sys').modules.get(__name__):raise TypeError('Exact SAME loaded source API and runner identity')
 observation=getattr(runner,'_SAFE125_OBSERVATION',None)
 if type(observation) is not NativeSafeObservation125 or observation.producer._g is not runner or not observation.phase_receipts.accepts(observation.producer):raise TypeError('Actual unused opaque source SAFE observation')
 binding=ControllerSafeBinding125(transport,macro,observation,ordinary_admin_budget_s)
 transport._controller_safe125=binding;transport._safe_api125=runner._SAFE125_API
 return binding
def accepts_controller125(transport,macro):
 binding=getattr(transport,'_controller_safe125',None)
 if type(binding) is not ControllerSafeBinding125 or binding.observation.producer._g._SAFE125_API is not __import__('sys').modules.get(__name__):return False
 return binding.observation.phase_receipts.accepts(binding.observation.producer) and binding.accepts(transport,macro)

SOURCE_PINS125={'launch.py': (51978, 'bb5530cda403cc3363fbc65fbac883aa3348ee4a4c7ac7bc1feaed4685e35a14'), 'counter115.py': (16288, 'cf14a494c743754f0a1aa2a88de22b228e7844500aa73e7dee7686128e8fcd4b'), 'admission116.py': (49199, '2cbc361f356c51ebbe6324a1c1d0774a05620114bdb2cc7adf5ac43cc607e330')}
