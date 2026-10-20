"""PRIVATE executable provider-original SAFE delivery. No live calls on import.

Controller and runner stay separate. Only redacted DATA cross the existing
GitHub artifact/Library route. No reconstruction of a runner heap/q/producer.
"""
import base64,copy,datetime,hashlib,io,json,pathlib,re,stat,sys,time,types,weakref,zipfile
from importlib.util import spec_from_file_location,module_from_spec
ROOT=pathlib.Path(__file__).resolve().parent
s=spec_from_file_location('trace126_control_fixed',ROOT/'control126.py');ctl=module_from_spec(s);s.loader.exec_module(ctl)
can=ctl.can;sha=ctl.sha
OWNER=273768139;REPOSITORY=1391430317;REPO='Elinfiny/TraceHarbor'
_SEAL=object();_HOSTS=weakref.WeakKeyDictionary();_OBS=weakref.WeakKeyDictionary()
class NativeOriginal126:
 __slots__=('port','identity','original','raw','seal','realm','canonical')
 def __init__(self,key,port,identity,original,canonical):
  if key is not _SEAL or port not in _HOSTS:raise TypeError('Only fixed registered native host can retain actual original')
  self.port=port;self.identity=copy.deepcopy(identity);self.original=copy.deepcopy(original);self.raw=can(original);self.seal=key;self.realm='ACTUAL_NATIVE_TOOL_ORIGINAL';self.canonical=canonical
class SyntheticOriginal126:
 def __init__(self,operation,value):self.operation=operation;self.original={'structuredContent':value};self.realm='SYNTHETIC_SOURCE_ONLY'
def register_native_host126(host,host_module,current,manifest):
 raise TypeError('External module/class/currentdict registration forbidden; use fixed source bootstrap')
def bootstrap_native_host126(config_path):
 """Load exact sources itself, never accept an API/module/class from callers.
 Actual current owned source admission is checked before creating a holder.
 """
 if sys.modules.get('trace126_fixed_provider') is not sys.modules.get(__name__):raise TypeError('Exact fixed provider loader identity')
 basepath=ROOT/'host_transport118.py';raw=basepath.read_bytes()
 if sha(raw)!='dbec3c2929f09511240924f00f10e2a1fea376a255a8f2790fe9e1a8ca0f671d':raise ValueError('Accepted original source guard')
 spec=spec_from_file_location('trace126_base_source_guard',basepath);base=module_from_spec(spec);spec.loader.exec_module(base)
 cfg=base.strict(pathlib.Path(config_path).read_bytes());current=base.current_binding(cfg['current_checkpoint'],cfg['current_version'],cfg)
 if 'ADMIT_NATIVE_SAFE126_PROVIDER_DELIVERY' not in current['direction']['body']:raise PermissionError('126 private source only; no native delivery admission')
 if cfg.get('manifest_path')!=str(ROOT/'manifest.json'):raise ValueError('Fixed source-manifest path')
 manifest=base.strict((ROOT/'manifest.json').read_bytes());freeze=current['doc'][current['key']]['records'][-1]
 if freeze['payload'].get('phase')!='SOURCE_FREEZE' or freeze['payload'].get('safe126_source_manifest_sha256')!=sha(can(manifest)):raise ValueError('Actual owned fullsource/currentmanifest freeze')
 for name,pin in manifest['source_files'].items():
  if pathlib.PurePosixPath(name).is_absolute() or '..' in pathlib.PurePosixPath(name).parts:raise ValueError('Safe fixedsource path')
  data=(ROOT.parent/name).read_bytes()
  if len(data)!=pin['bytes'] or sha(data)!=pin['sha256']:raise ValueError('Whole reviewed source pin before module load')
 spec=spec_from_file_location('trace126_loaded_native_host',ROOT/'native_host126.py');module=module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
 if not __import__('os').isatty(0):raise TypeError('Actual explicit directPTY only before frameledger/writer')
 ledger=module.FrameLedger(cfg['output'],cfg['context'],cfg['deadline_utc_ms']);bridge=module.StdioBridge(ledger);host=module.NativeHostTransport126(bridge,ledger.root,cfg)
 macro=module.bind_reviewed_macro122(host,pathlib.Path(cfg['macro_journal_path']))
 _HOSTS[host]={'module':module,'class':module.NativeHostTransport126,'macro':macro,'manifest_sha256':sha(can(manifest)),'context':copy.deepcopy(host.config['context'])}
 host.initialize_provider126(manifest);return host,macro
def retain_native126(host,identity,original,canonical):
 entry=_HOSTS.get(host)
 if entry is None or type(host) is not entry['class'] or identity['context_sha256']!=sha(can(host.config['context'])):raise TypeError('Registered original native route identity')
 # The host port supplies a verified canonical raw original path/count/SHA,
 # already captured BEFORE its first deadline/normalization postguard.
 raw=host.canonical126.io.read(canonical['path']);record=json.loads(raw)
 if record!={'identity':identity,'original':original} or len(raw)!=canonical['bytes'] or sha(raw)!=canonical['sha256']:raise ValueError('Complete saved original, not memory/PID/assertedchecksum')
 return NativeOriginal126(_SEAL,host,identity,original,canonical)
def value126(packet,operation,native,host=None):
 if native:
  if type(packet) is not NativeOriginal126 or packet.seal is not _SEAL or packet.port is not host or host not in _HOSTS or packet.identity['operation']!=operation:raise TypeError('No JSON/fixture/foreign port as native original')
 else:
  if type(packet) is not SyntheticOriginal126 or packet.operation!=operation:raise TypeError('Explicit synthetic original only')
 if packet.original.get('isError') is True or type(packet.original.get('structuredContent')) is not dict:raise ValueError('Actual complete successful native original required')
 v=packet.original['structuredContent']
 if operation=='github_fetch':
  if type(v.get('content')) is not str:raise ValueError('Whole provider body')
  return strict(v['content'].encode())
 return v
def strict(raw):
 if len(raw)>65536:raise ValueError('Bounded SAFE schema')
 def pairs(rows):
  d={}
  for k,v in rows:
   if k in d:raise ValueError('Duplicate SAFE key')
   d[k]=v
  return d
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in ()).throw(ValueError('Nonfinite SAFE')))
def approved_projection126(raw,plan,realm):
 p=strict(raw)
 if set(p)!={'schema','scope','context','counter','stop_cleanup','phases','runner_proof_sha256'} or p['schema']!='TRACE126_MINIMAL_SAFE_V1' or p['scope']!=realm:raise ValueError('Exact source-produced public allowlist, no arbitrary private fields')
 expected_context={'run_id','attempt','actor_id','repository_id','source_sha','manifest_sha256','once_receipt_sha256','expires_utc','admission_sha256','custody_binding_sha256','cost_scope_sha256'}
 if set(p['context'])!=expected_context or p['context']!=plan['projection_context']:raise ValueError('Source/run/attempt/Owner/repo/once/expiry/manifest/admission/custody binding')
 for key in ('manifest_sha256','once_receipt_sha256','admission_sha256','custody_binding_sha256','cost_scope_sha256'):
  if type(p['context'][key]) is not str or not re.fullmatch('[a-f0-9]{64}',p['context'][key]):raise ValueError('Public context contains no arbitrary private values/URLs')
 if not re.fullmatch('[a-f0-9]{40}',p['context']['source_sha']) or type(p['counter']['verified']) is not bool or type(p['counter']['counter_invocations']) is not int or type(p['counter']['model_calls']) is not int:raise ValueError('Exact context/counter field types')
 if p['counter']!={'verified':True,'T':None,'counter_invocations':1,'model_calls':0} or p['stop_cleanup']!={'consumer_stopped':True,'cleanup_complete':True,'first_unknown':None}:raise ValueError('Counter Tnull/SAFE/cleanup source projection')
 if not re.fullmatch('[a-f0-9]{64}',p['runner_proof_sha256']) or set(p['phases'])!={'cleanup','proof'}:raise ValueError('Exact phase/proof associations')
 previous=None
 for name,seconds in [('cleanup',10),('proof',15)]:
  r=p['phases'][name]
  if set(r)!={'facts_sha256','begin_mono','end_mono','begin_utc','end_utc','post_io_mono','post_io_utc','seconds_cap'} or r['seconds_cap']!=seconds or not re.fullmatch('[a-f0-9]{64}',r['facts_sha256']):raise ValueError('Actual provisional facts + post-IO closure fields')
  if any(type(r[k]) not in (int,float) or not __import__('math').isfinite(r[k]) for k in ('begin_mono','end_mono','begin_utc','end_utc','post_io_mono','post_io_utc')):raise ValueError('Finite actual mono/epoch')
  if not r['begin_mono']<=r['post_io_mono']<r['end_mono']<=r['begin_mono']+seconds or not r['begin_utc']<=r['post_io_utc']<r['end_utc']<=min(r['begin_utc']+seconds,p['context']['expires_utc']):raise ValueError('Late/error/preIO/provisionalreceipt cannot releaseSAFE')
  if previous is not None and (r['begin_mono']<previous['post_io_mono'] or r['begin_utc']<previous['post_io_utc']):raise ValueError('Cleanup10 then proof15 original phase order')
  previous=r
 return p
def metadata126(plan,run,commit,tree,jobs,listed):
 if run['id']!=plan['run_id'] or run['run_attempt']!=1 or run['actor']['id']!=OWNER or run['repository']['id']!=REPOSITORY or run['event']!='workflow_dispatch' or run['head_sha']!=plan['source_sha'] or run['path']!=plan['workflow_path'] or run['status']!='completed' or run['conclusion']!='success':raise ValueError('Wrong/pending actual run/source/workflow/Owner/repo/attempt')
 started=datetime.datetime.fromisoformat(run['run_started_at'].replace('Z','+00:00')).timestamp();finished=datetime.datetime.fromisoformat(run['updated_at'].replace('Z','+00:00')).timestamp()
 if not started<finished<=plan['expires_utc']<=started+900:raise ValueError('Actual completed run under ORIGINAL900/once expiry')
 if commit['sha']!=plan['source_sha'] or commit['author']['id']!=OWNER or commit['committer']['id']!=OWNER or [p['sha'] for p in commit['parents']]!=[plan['source_parent']] or commit['commit']['tree']['sha']!=plan['source_tree']:raise ValueError('Exact actual reviewedsource/soleparent/tree/Owner')
 if tree.get('truncated') is not False or tree['sha']!=plan['source_tree'] or tree['tree']!=plan['full_tree_entries']:raise ValueError('Entire source tree/pins, not selected-event JSON')
 if jobs['total_count']!=len(jobs['jobs']) or len(jobs['jobs'])!=1:raise ValueError('Firstpage must contain complete exactonejob')
 job=jobs['jobs'][0]
 if job['run_id']!=plan['run_id'] or job.get('run_attempt')!=1 or job['name']!='counter' or job['status']!='completed' or job['conclusion']!='success':raise ValueError('Actual latest attempt job/source producer notsuccessful')
 if [s['name'] for s in job['steps']]!=plan['job_step_names'] or any(s['status']!='completed' or s['conclusion']!='success' for s in job['steps']):raise ValueError('Complete fixed reviewed source-step chain')
 if listed['total_count']!=1 or len(listed['artifacts'])!=1:raise ValueError('Exact selectedartifact firstpage fullcount')
 artifact=listed['artifacts'][0];name='traceharbor-safe126-'+str(plan['run_id'])+'-1'
 if artifact['name']!=name or type(artifact['id']) is not int or artifact['id']<=0 or artifact['expired'] is not False or artifact['workflow_run']['id']!=plan['run_id'] or artifact['workflow_run']['head_sha']!=plan['source_sha'] or not re.fullmatch('sha256:[a-f0-9]{64}',artifact['digest']) or not 0<artifact['size_in_bytes']<=65536:raise ValueError('Exact providerartifact identity/digest/wholebytes cap')
 return artifact
def verify_bundle126(plan,bundle,native=False,host=None):
 """Actual modified verifier used by both fixed native port and inert cases.
 Whole native authenticity requires opaque originals plus actualsourcefreeze.
 """
 expected_keys={'run','commit','tree','jobs','artifacts','download','materialized'}
 if set(bundle)!=expected_keys:raise ValueError('Complete actual provider original chain')
 get=lambda name,op:value126(bundle[name],op,native,host)
 run=get('run','github_fetch');commit=get('commit','github_fetch');tree=get('tree','github_fetch');jobs=get('jobs','github_fetch_workflow_run_jobs');listed=get('artifacts','github_fetch_workflow_run_artifacts')
 artifact=metadata126(plan,run,commit,tree,jobs,listed)
 download=get('download','github_download_workflow_artifact');ref=download.get('file',download);material=get('materialized','library_materialize');material=material.get('result',material)
 if material.get('unavailable_items') or len(material.get('transfers',[]))!=1:raise ValueError('Pinned full per-item Library result')
 transfer=material['transfers'][0]
 for key in ('file_id','file_name'):
  if type(ref.get(key)) is not str or transfer.get(key)!=ref[key]:raise ValueError('Actual downloadedref/pinned peritem file identity')
 if not transfer.get('library_file_id') or ref.get('library_file_id') not in (None,transfer['library_file_id']):raise ValueError('Actual Library identity closure')
 if pathlib.PurePosixPath(ref['file_name']).name!=ref['file_name'] or '\\' in ref['file_name'] or ref['file_name'] in ('','.','..'):raise ValueError('No redirectURL/path fallback')
 raw=host.provider_artifact_bytes126(ref,transfer,artifact,plan) if native else bundle['materialized'].zip_bytes
 if len(raw)!=artifact['size_in_bytes'] or sha(raw)!=artifact['digest'][7:]:raise ValueError('Whole archive size/providerdigest/EOF')
 with zipfile.ZipFile(io.BytesIO(raw)) as archive:
  rows=archive.infolist()
  if len(rows)!=1 or rows[0].filename!='projection.json' or rows[0].file_size>8192 or rows[0].flag_bits&1 or stat.S_ISLNK(rows[0].external_attr>>16) or rows[0].is_dir():raise ValueError('Only exact redacted projection file')
  body=archive.read(rows[0]);assert archive.testzip() is None
 projection=approved_projection126(body,plan,'SOURCE_PRODUCED_PUBLIC_SAFE_DATA' if native else 'SYNTHETIC_SOURCE_ONLY')
 if native:
  host.deadline()
  if time.time()>=plan['expires_utc']:raise TimeoutError('Late actual originals/bytes no terminal')
 return projection
class ControllerSafeObservation126:
 __slots__=('host','macro','projection','plan','realm','seal')
 def __init__(self,key,host,macro,projection,plan):
  if key is not _SEAL or host not in _HOSTS or _HOSTS[host]['macro'] is not macro:raise TypeError('Trusted source factory registry only')
  self.host=host;self.macro=macro;self.projection=copy.deepcopy(projection);self.plan=copy.deepcopy(plan);self.realm='ACTUAL_PROVIDER_ORIGINAL_VERIFIED';self.seal=key
class SyntheticSafeObservation126:
 def __init__(self,projection):self.projection=projection;self.realm='SYNTHETIC_SOURCE_ONLY'
def synthetic_verify126(plan,bundle):return SyntheticSafeObservation126(verify_bundle126(plan,bundle,False))
def collect_native126(host,macro,plan):
 entry=_HOSTS.get(host)
 if entry is None or type(host) is not entry['class'] or entry['macro'] is not macro:raise TypeError('No forgedmethod/API/foreignmodule/PID/JSONfactory')
 state=macro.snapshot()
 if state['scope']!='PRIVATE_JOURNAL_PLAN' or state['cursor']!=15 or state['first_unknown'] is not None:raise ValueError('Actual current completed consumed macro required')
 if plan!=host.config['safe126_provider_plan'] or plan['projection_context']['once_receipt_sha256']!=host.config['context']['once_receipt_sha256'] or plan['source_sha']!=host.source or plan['run_id']!=host.config['run_id'] or plan['expires_utc']!=host.config['deadline_utc_ms']/1000:raise ValueError('Current source/admission/cost/custody/once/sourcefreeze plan binding')
 origin=host.provider_original126;url='https://api.github.com/repos/Elinfiny/TraceHarbor/'
 bundle={'run':origin('github_fetch',{'url':url+'actions/runs/'+str(plan['run_id'])}),'commit':origin('github_fetch',{'url':url+'commits/'+plan['source_sha']}),'tree':origin('github_fetch',{'url':url+'git/trees/'+plan['source_tree']+'?recursive=1'}),'jobs':origin('github_fetch_workflow_run_jobs',{'repo_full_name':REPO,'run_id':plan['run_id']}),'artifacts':origin('github_fetch_workflow_run_artifacts',{'repo_full_name':REPO,'run_id':plan['run_id'],'name':'traceharbor-safe126-'+str(plan['run_id'])+'-1'})}
 artifact=metadata126(plan,value126(bundle['run'],'github_fetch',True,host),value126(bundle['commit'],'github_fetch',True,host),value126(bundle['tree'],'github_fetch',True,host),value126(bundle['jobs'],'github_fetch_workflow_run_jobs',True,host),value126(bundle['artifacts'],'github_fetch_workflow_run_artifacts',True,host))
 bundle['download']=origin('github_download_workflow_artifact',{'repo_full_name':REPO,'artifact_id':artifact['id'],'file_name':'safe126.zip'});download=value126(bundle['download'],'github_download_workflow_artifact',True,host);ref=download.get('file',download)
 if type(ref) is not dict or not ref.get('file_id') or type(ref.get('file_name')) is not str or pathlib.PurePosixPath(ref['file_name']).name!=ref['file_name'] or '\\' in ref['file_name']:raise ValueError('Actual reusable file ref only; no URLs')
 destination=host.prepare_safe_destination126(plan)
 bundle['materialized']=origin('library_materialize',{'items':[{k:ref[k] for k in ('library_file_id','file_id','file_name') if k in ref}],'destination':{'directory':str(destination)}})
 projection=verify_bundle126(plan,bundle,True,host);observation=ControllerSafeObservation126(_SEAL,host,macro,projection,plan);_OBS[host]=observation;return observation
def require_native_terminal126(host,macro):
 # Deliberately never reads host._safe_api*. No arbitrary getter/method callback.
 entry=_HOSTS.get(host);observation=_OBS.get(host)
 if entry is None or type(host) is not entry['class'] or type(observation) is not ControllerSafeObservation126 or observation.seal is not _SEAL or observation.host is not host or observation.macro is not macro or entry['macro'] is not macro:raise TypeError('Exact registered host/typed provider-original factory observation')
 if macro.snapshot()['scope']!='PRIVATE_JOURNAL_PLAN' or macro.snapshot()['first_unknown'] is not None or macro.snapshot()['cursor']!=15:raise ValueError('No synthetic/UNKNOWN/foreign macro terminal')
 if time.time()>=observation.plan['expires_utc'] or time.monotonic()>=host.parent_mono:raise TimeoutError('Original parent/epoch/onceexpired')
 return observation
