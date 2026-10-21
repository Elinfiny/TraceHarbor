"""V2 acyclic static preparation and closed release validation. No effects at import.
Runtime originals are never part of an independently published static preimage.
"""
import pathlib,json,hashlib,copy,importlib.util,sys,re,math
ROOT=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('trace133_plan_control',ROOT/'control127.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
can=c.can;sha=c.sha;V2='TRACE146_STATIC_TYPED_RUNTIME_V3';ADMISSION='grouped146_admission'
g136s=importlib.util.spec_from_file_location('trace136_plan_git',ROOT/'git_dispatch136.py');g136=importlib.util.module_from_spec(g136s);g136s.loader.exec_module(g136)
_ts146=importlib.util.spec_from_file_location('trace146_timing_'+__name__,pathlib.Path(__file__).resolve().parent/'timing146.py');t146=importlib.util.module_from_spec(_ts146);_ts146.loader.exec_module(t146)

STATIC={'prestart154','authority152','publication150','source','manifest','request','lock','private6','custody_scope','cost_scope','dispatch_source','path_roles','limits','inventory_sha256','authority_projection_sha256','workflow','timing_contract','observer_contract','artifact_contract'}
PATHS={'private','transfer','holder_parent','capture','library_helper','config','materialize_original'}
def closed(x,keys,label):
 if type(x) is not dict or set(x)!=set(keys):raise ValueError('Closed '+label)
 return x
def text(x,label):
 if type(x) is not str or not x or len(x)>262144:raise ValueError('Exact '+label)
 return x
def hexpin(x,n=64):
 if type(x) is not str or re.fullmatch('[a-f0-9]{'+str(n)+'}',x) is None:raise ValueError('Exact digest')
 return x
def pin(x):
 closed(x,{'bytes','sha256'},'whole pin');hexpin(x['sha256'])
 if type(x['bytes']) is not int or not 0<x['bytes']<=33554432:raise ValueError('Finite whole bytes')
def projection133(direction):
 if type(direction) is not dict:raise TypeError('Whole addressed direction')
 p=copy.deepcopy(direction);g=p.pop(ADMISSION,None)
 if any(k.startswith('grouped') and k.endswith('_admission') for k in p):raise ValueError('Old or duplicate computed admission')
 body=text(p.get('body'),'direction body').encode()
 if len(body)!=p.get('bytes') or sha(body)!=p.get('sha256') or p.get('recipient')!='TraceHarbor V1':raise ValueError('Exact addressed body and recipient')
 # Computed output digests cannot be copied into any other projected field.
 if g is not None:
  outputs=[v for k,v in g.items() if k.endswith('_sha256') and type(v) is str]
  def walk(x):
   if type(x) is dict:
    for k,v in x.items():walk(k);walk(v)
   elif type(x) is list:
    for v in x:walk(v)
   elif type(x) is str and any(v in x for v in outputs):raise ValueError('Computed admission repeated in projection: cycle')
  walk(p)
 return p
def static133(config,manifest_bytes,inventory=None):
 x=copy.deepcopy(closed(config,STATIC,'static configuration'));t146.preallocate146(x);
 authority152=__import__('runpy').run_path(str(ROOT/'authority152.py'));authority152['contract152'](x['authority152']);__import__('runpy').run_path(str(ROOT/'prestart154.py'))['contract154'](x['prestart154'])
 pub150=__import__('runpy').run_path(str(ROOT/'publication150.py'));pub150['contract150'](x['publication150'])
 if x['artifact_contract']!={'schema':'TRACE146_THREE_PUBLIC_ARTIFACTS_V1','logical_payload_bytes_each':8192,'provider_zip_bytes_each':65536,'maximum_artifacts':3,'retention_days':1,'billable_grant':None}:raise ValueError('Prospective failure artifact storage/cost contract')
 m=json.loads(manifest_bytes);inventory=c.inventory127() if inventory is None else inventory
 if inventory!=c.inventory127():raise ValueError('Exact whole source inventory')
 closed(x['source'],{'commit','tree','parent'},'source')
 for v in x['source'].values():hexpin(v,40)
 for k in ('manifest','request','lock'):pin(x[k])
 if x['manifest']!={'bytes':len(manifest_bytes),'sha256':sha(manifest_bytes)}:raise ValueError('Actual full manifest')
 for k,path in [('request','offline103/request.json'),('lock','offline103/requirements.lock')]:
  if x[k]!=m['source_files'][path]:raise ValueError('Canonical new request/lock source pin')
 if x['private6']!=m['counter116']['input_pins'] or len(x['private6'])!=6:raise ValueError('Exact six private pins')
 for p in x['private6'].values():pin(p)
 closed(x['custody_scope'],{'profile','root','checkpoint_key'},'custody scope')
 if x['custody_scope']['profile']!='nemotron-lightning-input-v1' or type(x['custody_scope']['checkpoint_key']) is not str or re.fullmatch(r'native[1-9][0-9]{0,3}',x['custody_scope']['checkpoint_key']) is None or int(x['custody_scope']['checkpoint_key'][6:])<132:raise ValueError('Exact independently bound source-acquisition checkpoint; no historical rewrite')
 text(x['custody_scope']['root'],'private custody root')
 closed(x['cost_scope'],{'model_calls','spend','host_cost_bound'},'API0 cost')
 if x['cost_scope']!=t146.zero_cost146() or any(type(x['cost_scope'][k]) is not int for k in x['cost_scope']):raise ValueError('Exact146 shared API0 cost contract, not a grant')
 if x['workflow']['path']==g136.WORKFLOW:
  closed(x['dispatch_source'],{'kind','expected_actor_id','actor_proof_sha256','namespace','workflow_path'},'Git create source')
  ds=x['dispatch_source']
  if ds['kind']!='git_create136' or ds['expected_actor_id']!=273768139 or ds['namespace']!=g136.PREFIX or ds['workflow_path']!=g136.WORKFLOW:raise ValueError('Exact Git source contract preserves Owner')
  hexpin(ds['actor_proof_sha256']) # future independently reviewed genuine pilot proof, currently NULL
 else:
  closed(x['dispatch_source'],{'script','script_sha256','tab_id'},'dispatch source');text(x['dispatch_source']['script'],'script');hexpin(x['dispatch_source']['script_sha256'])
  if sha(x['dispatch_source']['script'].encode())!=x['dispatch_source']['script_sha256'] or type(x['dispatch_source']['tab_id']) is not int:raise ValueError('Pinned dispatch script')
  if x['dispatch_source']['script'].count('__TRACE_ONCE133__')!=1:raise ValueError('One runtime once placeholder')
 closed(x['path_roles'],PATHS|{'library_helper_sha256'},'path roles')
 for k in PATHS:
  p=pathlib.Path(text(x['path_roles'][k],k))
  if not p.is_absolute() or '..' in p.parts:raise ValueError('Absolute unaliased role')
 hexpin(x['path_roles']['library_helper_sha256'])
 closed(x['workflow'],{'path','step_names','baseline_entries','full_tree_entries'},'workflow')
 text(x['workflow']['path'],'workflow path')
 if type(x['workflow']['step_names']) is not list or any(type(v) is not str for v in x['workflow']['step_names']):raise ValueError('Closed workflow step list')
 for k in ('baseline_entries','full_tree_entries'):
  if type(x['workflow'][k]) is not list:raise ValueError('Whole fixed tree')
  seen=set()
  for row in x['workflow'][k]:
   required={'path','mode','type','sha'};allowed=required if k=='baseline_entries' else required|{'size','url'}
   if type(row) is not dict or not required<=set(row)<=allowed:raise ValueError('Closed actual direct/recursive Git tree identity')
   text(row['path'],'source path');hexpin(row['sha'],40);path=pathlib.PurePosixPath(row['path'])
   if path.is_absolute() or '..' in path.parts or row['path'] in seen or row['type'] not in ('tree','blob') or row['mode'] not in (('040000',) if row['type']=='tree' else ('100644','100755')) or k=='baseline_entries' and '/' in row['path']:raise ValueError('Unique exact direct root/recursive source identities')
   if 'size' in row and (row['type']!='blob' or type(row['size']) is not int or row['size']<0):raise ValueError('Actual public source blob size')
   if 'url' in row and row['url']!='https://api.github.com/repos/Elinfiny/TraceHarbor/git/'+('trees/' if row['type']=='tree' else 'blobs/')+row['sha']:raise ValueError('Only immutable canonical source URLs')
   seen.add(row['path'])
 if x['workflow']['path']=='.github/workflows/traceharbor-counter135.yml':raise ValueError('V3 admits exact Git136 only; historical manual135 unchanged')
 if False:
  for marker in ('__TRACE_SOURCE135__','__TRACE_MANIFEST135__','__TRACE_ONCE133__','__TRACE_EXPIRES135__','__TRACE_CUTOFF135__','__TRACE_TAB135__'):
   if x['dispatch_source']['script'].count(marker)!=1:raise ValueError('Complete dispatch template before any runtime allocation')
  path=ROOT.parent/x['workflow']['path'];raw=path.read_bytes()
  if m['source_files'].get(x['workflow']['path'])!={'bytes':len(raw),'sha256':sha(raw)}:raise ValueError('Exact active source workflow pin')
  wf=json.loads(raw);job=wf['jobs']['counter']
  if set(wf['on'])!={'workflow_dispatch'} or set(wf['on']['workflow_dispatch']['inputs'])!=set(('source_sha','manifest_sha256','once_receipt_sha256','once_expires_utc','coordinator_cutoff_utc')) or wf['permissions']!={'contents':'read'} or job['runs-on']!='ubuntu-24.04' or job['timeout-minutes']!=t146.CONTRACT['job_minutes'] or wf['concurrency']['cancel-in-progress'] is not False or [v['name'] for v in job['steps']]!=x['workflow']['step_names']:raise ValueError('Whole source workflow/inputs/steps/runner/concurrency contract')
 if x['workflow']['path']==g136.WORKFLOW:
  raw=(ROOT.parent/g136.WORKFLOW).read_bytes();wf=json.loads(raw);job=wf['jobs']['counter']
  if m['source_files'].get(g136.WORKFLOW)!={'bytes':len(raw),'sha256':sha(raw)} or wf['on']!={'create':None} or wf['permissions']!={'contents':'read'} or job['runs-on']!='ubuntu-24.04' or job['timeout-minutes']!=t146.CONTRACT['job_minutes'] or wf['concurrency']['cancel-in-progress'] is not False or [a['name'] for a in job['steps']]!=x['workflow']['step_names']:raise ValueError('Whole exact prospective create workflow')
  guard=job['if']
  for must in ("github.event_name == 'create'","github.event.ref_type == 'branch'","github.actor_id == '273768139'","github.repository_id == '1391430317'","startsWith(github.event.ref, 'traceharbor/once136/v1/')","github.run_attempt == 1"):
   if must not in guard:raise ValueError('Source job namespace/Owner/repository/attempt not weakened')
 if x['limits']!=c.FIXED or x['inventory_sha256']!=sha(can(inventory)):raise ValueError('Whole original limits/inventory')
 hexpin(x['authority_projection_sha256']);return x
def template133(config,manifest_bytes,inventory=None):
 i=c.inventory127() if inventory is None else inventory;x=static133(config,manifest_bytes,i)
 return {'schema':'TRACE133_STATIC_PHASE_TEMPLATE','static_config_sha256':sha(can(x)),'inventory_sha256':sha(can(i)),'phases':list(c.PHASES),'semantic':list(c.SEMANTIC),'limits':copy.deepcopy(c.FIXED),'six_CAS_readback_pairs':6,'create_only_Git_primitives':12}
def prepare127(config,direction,manifest_bytes,inventory=None):
 i=c.inventory127() if inventory is None else inventory;p=projection133(direction);x=static133(config,manifest_bytes,i)
 if x['authority_projection_sha256']!=sha(can(p)):raise ValueError('Entire actual addressed scope, not a whole Auditor hash')
 t=template133(x,manifest_bytes,i)
 g={'contract':V2,'authority_projection_sha256':sha(can(p)),'static_config_sha256':sha(can(x)),'phase_template_sha256':sha(can(t)),'inventory_sha256':sha(can(i)),'manifest_sha256':sha(manifest_bytes),'inclusive_cap':i['inclusive_total'],'scope':'ONE_TYPED_UNUSED_ONCE_API0_ONLY'}
 return {'native_authority':False,'config':x,'phase_template':t,'inventory':i,'proposed_admission':g,'actual_nonce_created':False,'actual_clock_started':False}
def release133(direction,config,manifest_bytes,inventory=None):
 prepared=prepare127(config,direction,manifest_bytes,inventory)
 if direction.get(ADMISSION)!=prepared['proposed_admission']:raise PermissionError('Actual independently published exact V2 release required')
 return prepared
#135 PRIVATE prospective activation support. No import executes these methods.
ACTIVE_WORKFLOW135='.github/workflows/traceharbor-counter135.yml'
INPUTS135=('source_sha','manifest_sha256','once_receipt_sha256','once_expires_utc','coordinator_cutoff_utc')
TOKENS135={'__TRACE_SOURCE135__':'source_sha','__TRACE_MANIFEST135__':'manifest_sha256','__TRACE_ONCE133__':'once_receipt_sha256','__TRACE_EXPIRES135__':'once_expires_utc','__TRACE_CUTOFF135__':'coordinator_cutoff_utc'}
def dispatch_inputs135(config,context,cutoff):
 if context['source_sha']!=config['source']['commit'] or context['manifest_sha256']!=config['manifest']['sha256']:raise ValueError('Same source/manifest runtime context')
 for k in ('source_sha',):hexpin(context[k],40)
 for k in ('manifest_sha256','once_receipt_sha256'):hexpin(context[k])
 end=context['expires_utc']
 if type(end) is not int or type(cutoff) is not int or end<=0 or cutoff<end:raise ValueError('Original source runtime expiry/cutoff, never caller time')
 return {'source_sha':context['source_sha'],'manifest_sha256':context['manifest_sha256'],'once_receipt_sha256':context['once_receipt_sha256'],'once_expires_utc':str(end),'coordinator_cutoff_utc':str(cutoff)}
def render_dispatch135(config,context,cutoff):
 values=dispatch_inputs135(config,context,cutoff);script=config['dispatch_source']['script']
 for token,key in TOKENS135.items():
  if script.count(token)!=1:raise ValueError('One exact source-owned dispatch input placeholder')
  script=script.replace(token,values[key])
 if script.count('__TRACE_TAB135__')!=1:raise ValueError('One exact existing tab role placeholder')
 return script.replace('__TRACE_TAB135__',str(config['dispatch_source']['tab_id']))
def dispatch_contract135(config,context,cutoff,ref):
 # Official fresh workflow_dispatch API, not an exposed generic POST transport.
 # This descriptor cannot mint a native origin or execute in the browser.
 if type(ref) is not str or not re.fullmatch('refs/heads/[A-Za-z0-9_./-]+',ref) or '..' in ref:raise ValueError('Explicit admitted source ref')
 return {'schema':'TRACE135_FRESH_DISPATCH_CONTRACT_DATA_ONLY','status':'AVAILABLE_CONTRACT_ONLY_NOT_AUTHENTICATED_LAUNCH','method':'POST','url':'https://api.github.com/repos/Elinfiny/TraceHarbor/actions/workflows/traceharbor-counter135.yml/dispatches','body':{'ref':ref,'inputs':dispatch_inputs135(config,context,cutoff)},'actual_exposed_tool':'mcp__codex_apps__browser_js','actual_tool_arguments':{'code':'SOURCE_OWNED_REVIEWED_UI_SCRIPT_REQUIRED_AFTER_ORIGIN_RESTORATION'},'no_dispatch_connector':True,'native_authority':False}
def runner_guard135(env,wall):
 # Safe first-run source guard: values come from fixed workflow env, never shell
 # interpolation. Existing typed original once/admission is still checked by
 # launch127 before recipient creation/protected work.
 if env.get('GITHUB_REPOSITORY')!='Elinfiny/TraceHarbor' or env.get('GITHUB_REPOSITORY_ID')!='1391430317' or env.get('GITHUB_ACTOR_ID')!='273768139' or env.get('GITHUB_RUN_ATTEMPT')!='1' or env.get('GITHUB_EVENT_NAME')!='workflow_dispatch':raise PermissionError('Exact Owner/repository/attempt1/manual event')
 if env.get('GITHUB_WORKFLOW_REF','').split('@')[0]!='Elinfiny/TraceHarbor/'+ACTIVE_WORKFLOW135:raise ValueError('Exact reviewed active workflow path')
 values={k:env['TRACE135_'+k.upper()] for k in INPUTS135}
 hexpin(values['source_sha'],40)
 for k in ('manifest_sha256','once_receipt_sha256'):hexpin(values[k])
 if values['source_sha']!=env.get('GITHUB_SHA') or env.get('GITHUB_WORKFLOW_SHA')!=values['source_sha']:raise ValueError('Immutable selected source/workflow')
 if not re.fullmatch('[1-9][0-9]{0,11}',values['once_expires_utc']) or not re.fullmatch('[1-9][0-9]{0,11}',values['coordinator_cutoff_utc']):raise ValueError('Original integer clock inputs')
 end=min(int(values['once_expires_utc']),int(values['coordinator_cutoff_utc']))
 if type(wall) not in (int,float) or not math.isfinite(wall) or not wall<end<=wall+t146.PARENT:raise ValueError('Original future900; no reset')
 return values

def public_payload135(kind,raw,env):
 # Only already public allowlisted protocol data, never raw/private/ciphertext.
 import ssl
 if type(raw) is not bytes or not 0<len(raw)<=8192:raise ValueError('Public one-file payload <=8192')
 x=json.loads(raw);source=env['TRACE135_SOURCE_SHA'];run=int(env['GITHUB_RUN_ID']);expiry=int(env['TRACE135_ONCE_EXPIRES_UTC'])
 if kind=='recipient':
  closed(x,{'context','certificate_pem'},'PUBLIC recipient');q=closed(x['context'],{'repository','repository_id','actor_id','run_id','attempt','source_sha','nonce','expires_utc','certificate_sha256'},'PUBLIC recipient context')
  if q['repository']!='Elinfiny/TraceHarbor' or q['repository_id']!=1391430317 or q['actor_id']!=273768139 or q['run_id']!=run or q['attempt']!=1 or q['source_sha']!=source or q['expires_utc']!=expiry:raise ValueError('Actual selected public recipient context')
  hexpin(q['nonce'],32);hexpin(q['certificate_sha256']);pem=text(x['certificate_pem'],'PUBLIC certificate')
  if not pem.startswith('-----BEGIN CERTIFICATE-----') or 'PRIVATE KEY' in pem or sha(ssl.PEM_cert_to_DER_cert(pem))!=q['certificate_sha256']:raise ValueError('Only public certificate, exact DER digest')
 elif kind=='safe':
  s=importlib.util.spec_from_file_location('trace135_public_SAFE_allowlist',ROOT/'provider_safe127.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
  ctx=x.get('context',{})
  if ctx.get('actor_id')!=273768139 or ctx.get('repository_id')!=1391430317 or ctx.get('attempt')!=1 or ctx.get('run_id')!=run or ctx.get('source_sha')!=source or ctx.get('once_receipt_sha256')!=env['TRACE135_ONCE_RECEIPT_SHA256'] or ctx.get('manifest_sha256')!=env['TRACE135_MANIFEST_SHA256'] or ctx.get('expires_utc')!=expiry:raise ValueError('Actual source/once/manifest/public SAFE context')
  v.approved_projection127(raw,{'projection_context':ctx},'SOURCE_PRODUCED_PUBLIC_SAFE_DATA')
 elif kind=='failure':
  s=importlib.util.spec_from_file_location('trace146_public_failure',ROOT/'failure146.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v);v.validate_failure146(raw,v.binding146(env))
 else:raise ValueError('Only three explicitly bounded public receipt kinds')
 return x

def artifact_guard135(kind,env):
 import os,stat
 root=pathlib.Path(env['RUNNER_TEMP']);once=hexpin(env['TRACE135_ONCE_RECEIPT_SHA256']);path=root/('traceharbor-counter117-intake-'+once)/'recipient-public.json' if kind=='recipient' else root/('traceharbor-failure146/failure.json' if kind=='failure' else 'traceharbor-safe127/projection.json')
 for parent in (path,*path.parents):
  if parent.is_symlink():raise ValueError('No public upload path aliases')
 st=path.lstat()
 if path.resolve()!=path or not stat.S_ISREG(st.st_mode) or st.st_uid!=os.getuid() or st.st_nlink!=1 or st.st_mode&0o022 or not 0<st.st_size<=8192:raise ValueError('Exact owned bounded public source file')
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  a=os.fstat(fd);raw=os.read(fd,8193);extra=os.read(fd,1);b=os.fstat(fd)
 finally:os.close(fd)
 if extra or len(raw)!=st.st_size or (st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns)!=(a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns) or (a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns)!=(b.st_dev,b.st_ino,b.st_size,b.st_mtime_ns):raise ValueError('Whole stable public source EOF')
 public_payload135(kind,raw,env);return {'kind':kind,'bytes':len(raw),'sha256':sha(raw),'scope':'PUBLIC_ALLOWLIST_ONLY_NOT_FINANCIAL_HEADROOM_PROOF'}

def cli135():
 import os,time
 mode=sys.argv[1];env=dict(os.environ)
 if mode=='guard135':
  values=runner_guard135(env,time.time());mb=(ROOT/'manifest.json').read_bytes()
  if sha(mb)!=values['manifest_sha256']:raise ValueError('Whole final source manifest before recipient')
  for name,pinvalue in json.loads(mb)['source_files'].items():
   path=pathlib.Path(name)
   if path.is_absolute() or '..' in path.parts:raise ValueError('Safe source member')
   raw=(ROOT.parent/path).read_bytes()
   if len(raw)!=pinvalue['bytes'] or sha(raw)!=pinvalue['sha256']:raise ValueError('Full exact source closure before recipient')
  print(json.dumps({'guard':'PASS','native_authority':False}))
 elif mode=='artifact-failure146':
  path=pathlib.Path(env['RUNNER_TEMP'])/'traceharbor-failure146/failure.json';present=path.exists()
  if present:artifact_guard135('failure',env)
  with open(env['GITHUB_OUTPUT'],'a') as f:f.write('present='+str(present).lower()+'\n')
  print(json.dumps({'failure_only_present':present,'native_authority':False}))
 elif mode in ('artifact-recipient135','artifact-safe135'):print(json.dumps(artifact_guard135('recipient' if mode=='artifact-recipient135' else 'safe',env)))
 else:raise ValueError('Fixed135 source command')

if __name__=='__main__':
 if sys.argv[1] in ('guard135','artifact-recipient135','artifact-safe135','artifact-failure146'):cli135()
 else:
  values=json.loads(pathlib.Path(sys.argv[1]).read_bytes());print(json.dumps(prepare127(values['config'],values['direction'],(ROOT/'manifest.json').read_bytes()),sort_keys=True,separators=(',',':')))
