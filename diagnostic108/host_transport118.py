"""Source-pinned solewriter host IPC adapter118, distinct from runner authority.

Import is inert. The code-mode bridge invokes actual enabled tools. This holder
accepts planned data/original returns only; no eval, arbitrary command, PAT,
cookie, HTTP or native capability transfer. Read-only qualification never CASes.
"""
import os,sys,pathlib,json,hashlib,time,subprocess,copy,zipfile,io,stat,re,base64
OWN='libfile_3ee8270f03d8819188e1de1f75c3d824';OWNER=273768139;REPO='Elinfiny/TraceHarbor'
MAX_FRAME=1048576;WRITER='e839e90d6a61ceb21ab32dd8c78f27ab63a346e8e5ec0c4d12a1356db4fe3436'
READ_PR='https://api.github.com/repos/Elinfiny/TraceHarbor/pulls/18'
OPS={'github_fetch','github_create_blob','github_create_tree','github_create_commit','github_create_ref','github_fetch_workflow_run_artifacts','github_download_workflow_artifact','library_replace','library_materialize'}
def can(d):return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def strict(raw):
 def pairs(items):
  result={}
  for k,v in items:
   if k in result:raise ValueError('Duplicate IPC key')
   result[k]=v
  return result
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in ()).throw(ValueError('Nonfinite IPC')))
def put(p,raw):
 fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
class HostUnknown(RuntimeError):pass
def normalizer(original,kind):
 if type(original) is not dict or original.get('isError') is True:raise HostUnknown('Original tool error; no retry')
 value=original.get('structuredContent')
 if type(value) is not dict:raise HostUnknown('Missing actual structured tool return')
 if kind=='github_fetch':
  raw=value.get('content')
  if type(raw) is not str:raise HostUnknown('Missing complete provider body')
  return strict(raw)
 if kind=='library_materialize':
  value=value.get('result',value)
  if value.get('unavailable_items') or len(value.get('transfers',[]))!=1:raise HostUnknown('Pinned materialization unavailable')
  return value['transfers'][0]
 return value
def validate_zip(raw,digest):
 if len(raw)>8192 or sha(raw)!=digest:raise ValueError('Exact authenticated public archive cap/digest')
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  infos=z.infolist()
  if len(infos)!=1 or infos[0].filename!='recipient-public.json' or infos[0].file_size>8192 or infos[0].flag_bits&1 or stat.S_ISLNK(infos[0].external_attr>>16):raise ValueError('Exact closed public recipient ZIP path/type')
  data=z.read(infos[0]);assert z.testzip() is None
 return strict(data)
class FrameLedger:
 def __init__(self,root,context,deadline_ms):
  self.root=pathlib.Path(root);self.root.mkdir(mode=0o700,exist_ok=False);self.context=copy.deepcopy(context);self.deadline_ms=deadline_ms;self.seq=0;self.pending=None;self.failed=False
 def request(self,op,args):
  if self.failed or self.pending is not None or op not in OPS or int(time.time()*1000)>=self.deadline_ms:raise HostUnknown('Holder phase/sequence/op unavailable')
  if self.context['domain']=='READONLY_QUALIFICATION118' and (op!='github_fetch' or args!={'url':READ_PR}):raise ValueError('Read-only exact PR18 route')
  self.seq+=1
  frame={'schema':'TRACE118_HOST_REQUEST','seq':self.seq,'context':self.context,'op':op,'args':args,'deadline_utc_ms':self.deadline_ms}
  frame['request_digest']=sha(can(frame));raw=can(frame)
  if len(raw)>MAX_FRAME:raise ValueError('Bounded request frame')
  put(self.root/f'{self.seq}.request.original.json',raw);self.pending=frame
  return frame
 def accept(self,raw):
  # Preserve bounded original frame bytes before parsing, normalization or time.
  seq=self.seq
  try:put(self.root/f'{seq}.return.original.json',raw[:MAX_FRAME+1])
  except FileExistsError:
   self.failed=True;duplicate=self.root/f'{seq}.duplicate-{sha(raw)[:16]}.json'
   if not duplicate.exists():put(duplicate,raw[:MAX_FRAME+1])
   raise HostUnknown('Duplicate return preserved; no retry')
  try:
   if len(raw)>MAX_FRAME:raise HostUnknown('Oversized/partial IPC frame')
   value=strict(raw);p=self.pending
   if p is None or self.failed or value.get('schema')!='TRACE118_HOST_RETURN' or value.get('seq')!=p['seq'] or value.get('context')!=self.context or value.get('op')!=p['op'] or value.get('request_digest')!=p['request_digest']:raise HostUnknown('Out of order/duplicate/source/op IPC')
   if int(time.time()*1000)>=self.deadline_ms or value.get('late') is True:raise HostUnknown('Late original remains UNKNOWN')
   if value.get('transport_error') is not None:raise HostUnknown('Tool transport exception preserved')
   result=normalizer(value['original_result'],p['op']);self.pending=None
   put(self.root/f'{seq}.accepted.json',can({'seq':seq,'request_sha256':p['request_digest'],'original_frame_sha256':sha(raw),'original_result_sha256':sha(can(value['original_result'])),'domain':self.context['domain'],'normalized_kind':p['op'],'native_authority':False}))
   return result
  except BaseException:
   self.failed=True;raise
 def eof(self):
  self.failed=True;put(self.root/'EOF_UNKNOWN.json',can({'seq':self.seq,'pending':self.pending is not None,'status':'UNKNOWN_NO_RETRY'}));raise HostUnknown('Partial EOF; no effect retry')
class StdioBridge:
 def __init__(self,ledger):self.ledger=ledger
 def __call__(self,op,args):
  frame=self.ledger.request(op,args);sys.stdout.buffer.write(can(frame)+b'\n');sys.stdout.buffer.flush()
  raw=sys.stdin.buffer.readline(MAX_FRAME+2)
  if not raw or not raw.endswith(b'\n'):self.ledger.eof()
  return self.ledger.accept(raw.rstrip(b'\n'))
def selfhash(doc):
 c=copy.deepcopy(doc);c['self_sha256']=None;return sha(can(c))
def check_checkpoint(path,library_id,version,expected_sha=None):
 p=pathlib.Path(path);raw=p.read_bytes();d=strict(raw)
 if library_id!=OWN or os.getxattr(p,'user.library-file-id').decode()!=OWN or int(os.getxattr(p,'user.library-file-version').decode())!=version or selfhash(d)!=d['self_sha256'] or expected_sha is not None and sha(raw)!=expected_sha or d['ownership']['owner']!='TraceHarbor V1' or d['ownership']['duplicate_trace_route_owners']!=0:raise ValueError('Actual current owned preimage/self/allattrs required')
 return d,raw
def candidate_checkpoint(base,version,payload,out,source_pin):
 d,raw=check_checkpoint(base,OWN,version);c=copy.deepcopy(d)
 # This is the existing solewriter's scoped adapter journal, not a parallel
 # state/transaction/lease. No arbitrary checkpoint patch is accepted.
 allowed={'phase','source_sha','descriptor_sha256','parent_clock','custody','operation','tool','args_sha256','status'}
 if type(payload) is not dict or set(payload)-allowed or payload.get('source_sha')!=source_pin or payload.get('phase') not in ('admit','consumed','GIT_WRITE_ATTEMPT'):raise ValueError('Exact permitted own journal delta')
 if 'native118' not in d:raise ValueError('Current original118 writer scope absent')
 history=d['native118'].get('host_transport118_journal',[])
 if any(r['payload'].get('phase')==payload['phase'] and r['payload'].get('source_sha')==source_pin and (r['payload'].get('args_sha256')==payload.get('args_sha256') if payload['phase']=='GIT_WRITE_ATTEMPT' else r['payload'].get('descriptor_sha256')==payload.get('descriptor_sha256')) for r in history):raise HostUnknown('Canonical attempt already consumed; no replay')
 c['native118'].setdefault('host_transport118_journal',[]).append({'original_writer':WRITER,'payload':payload,'preimage_sha256':sha(raw),'actual_preimage_version':version,'native_authority':False})
 c['guard']['epoch_checkpoint_counter']=version+1;c['self_sha256']=selfhash(c)
 for k in d:
  if k not in ('native118','guard','self_sha256'):assert c[k]==d[k],k
 p=pathlib.Path(out);p.parent.mkdir(mode=0o700,parents=True,exist_ok=True);put(p,can(c))
 for name in os.listxattr(base):os.setxattr(p,name,os.getxattr(base,name))
 return {'candidate':str(p),'sha256':sha(p.read_bytes()),'self_sha256':c['self_sha256'],'expected_current_version':version,'writer_scope':'SAME_TRACE118_ORIGINALWRITER','preservation':'PASS'}
class HostTransport:
 def __init__(self,bridge,root,config):
  self.bridge=bridge;self.root=pathlib.Path(root);self.config=config;self.source=config['source_sha'];self._version=None;self._checkpoint=None;self._last_verified_receipt=None;self.reserved=set();self.counts={'GitGET':0,'Gitwrites':0,'CAS':0,'materialize':0}
  rs=self.root.lstat()
  if not stat.S_ISDIR(rs.st_mode) or self.root.is_symlink() or rs.st_uid!=os.getuid() or rs.st_mode&0o077:raise ValueError('Actual owned private holder root')
  if sha(pathlib.Path(__file__).read_bytes())!=config['host_source_sha256']:raise ValueError('Actual source-pinned host transport')
  helper=pathlib.Path(config['library_helper'])
  if sha(helper.read_bytes())!=config['library_helper_sha256']:raise ValueError('Current helper source pin')
  self.helper=helper
  if config.get('current_checkpoint') is not None:
   d,raw=check_checkpoint(config['current_checkpoint'],OWN,config['current_version'],config['current_sha256']);self._checkpoint=pathlib.Path(config['current_checkpoint']);self._version=config['current_version']
 def deadline(self):
  if int(time.time()*1000)>=self.config['deadline_utc_ms']:raise HostUnknown('Fixed host parent end; no reset')
 @property
 def current_checkpoint_version(self):
  if self._version is None:raise HostUnknown('No actual own readback bound')
  return self._version
 def call(self,op,args):
  self.deadline()
  if op not in OPS:raise ValueError('Unsupported logical operation')
  if op.startswith('github_create_'):
   if args.get('repository_full_name')!=REPO or self.config.get('domain')=='READONLY_QUALIFICATION118':raise ValueError('No effect in qualification/wrong repository')
   digest=sha(can({'tool':op,'args':args}))
   if digest not in self.reserved:raise ValueError('Durable originalwriter attempt must precede effect')
   self.reserved.remove(digest);self.counts['Gitwrites']+=1
  else:self.counts['GitGET']+=int(op.startswith('github_'))
  # FrameLedger + bridge persist actual original on BOTH sides before parse.
  result=self.bridge(op,args);self.deadline();return result
 def reserve_operation(self,key,tool,args,source,end_utc):
  self.deadline()
  if source!=self.source or tool not in OPS or not tool.startswith('github_create_') or not time.time()+1<end_utc:raise ValueError('Exact scoped future write reservation')
  digest=sha(can({'tool':tool,'args':args}))
  if digest in self.reserved:raise HostUnknown('Attempt already reserved')
  receipt=self.cas_checkpoint(self.current_checkpoint_version,{'phase':'GIT_WRITE_ATTEMPT','source_sha':source,'operation':key,'tool':tool,'args_sha256':digest,'status':'CONSUMED_BEFORE_EFFECT'})
  self.reserved.add(digest);return receipt
 def cas_checkpoint(self,expected_version,payload):
  self.deadline()
  if self.config.get('domain')=='READONLY_QUALIFICATION118' or expected_version!=self.current_checkpoint_version:raise ValueError('CAS currentversion/read-only guard before any effect')
  target=self.root/('own-candidate-'+str(expected_version))/'TraceHarbor_V1_checkpoint.json';request=self.root/('writer-'+str(expected_version)+'.json')
  put(request,can({'base':str(self._checkpoint),'version':expected_version,'payload':payload,'out':str(target),'source_pin':self.source}))
  result=subprocess.run([sys.executable,str(pathlib.Path(__file__).resolve()),'--writer',str(request)],capture_output=True,timeout=min(10,max(.1,(self.config['deadline_utc_ms']-int(time.time()*1000))/1000)))
  put(self.root/('writer-'+str(expected_version)+'.original.json'),can({'returncode':result.returncode,'stdout_hex':result.stdout.hex(),'stderr_hex':result.stderr.hex()}))
  if result.returncode!=0:raise HostUnknown('Actual originalwriter terminal not0')
  writer=strict(result.stdout);original=strict(self._checkpoint.read_bytes());candidate=strict(target.read_bytes())
  if sha(target.read_bytes())!=writer['sha256'] or selfhash(candidate)!=candidate['self_sha256'] or candidate['native118']['host_transport118_journal'][-1]['payload']!=payload:raise ValueError('Writer bytes/journal/self independently required')
  for k in original:
   if k not in ('native118','guard','self_sha256') and candidate[k]!=original[k]:raise ValueError('Unscoped writer change')
  pub=self.bridge('library_replace',{'library_file_id':OWN,'file':str(target),'expected_current_version':expected_version,'version_reason':'Source-pinned same originalwriter bounded host118 attempt; no retry of UNKNOWN'})
  self.counts['CAS']+=1
  if pub.get('status')!='succeeded' or pub.get('library_file_id')!=OWN or type(pub.get('current_version_number')) is not int:raise HostUnknown('Actual Library CAS result required')
  self.apply_attrs(target,pub)
  receipt=dict(pub,sha256=writer['sha256'],self_sha256=writer['self_sha256']);return self.pinned_checkpoint_readback(receipt)
 def apply_attrs(self,path,metadata):
  q=subprocess.run([sys.executable,str(self.helper),'apply-xattrs',str(path),metadata['library_file_id']],input=json.dumps(metadata.get('xattrs',[])),capture_output=True,text=True,timeout=5)
  if q.returncode!=0:raise HostUnknown('Current Library helper failed')
  if os.getxattr(path,'user.library-file-id').decode()!=metadata['library_file_id']:raise ValueError('Library identity attr')
  for a in metadata.get('xattrs',[]):
   if os.getxattr(path,a['name']).decode()!=a['value']:raise ValueError('Complete Library attrs')
 def pinned_checkpoint_readback(self,receipt):
  if receipt is self._last_verified_receipt and self._checkpoint is not None and receipt.get('version')==self._version and receipt.get('sha256')==sha(self._checkpoint.read_bytes()):return receipt
  self.deadline();t=self.bridge('library_materialize',{'items':[{'library_file_id':OWN,'file_id':receipt['file_id'],'file_name':receipt['file_name']}],'destination':{'directory':str(self.root/('own-readback-'+str(receipt['current_version_number'])))}});self.counts['materialize']+=1
  if t.get('file_id')!=receipt['file_id'] or t.get('library_file_id')!=OWN or t.get('current_version_number')!=receipt['current_version_number'] or t.get('xattrs')!=receipt.get('xattrs'):raise HostUnknown('Pinned whole actual own readback required')
  p=pathlib.Path(t['workspace_path']);self.apply_attrs(p,t);d,raw=check_checkpoint(p,OWN,t['current_version_number'],receipt['sha256'])
  if d['self_sha256']!=receipt['self_sha256']:raise ValueError('Pinned self closure')
  self.deadline();self._checkpoint=p;self._version=t['current_version_number']
  actual=dict(receipt,version=self._version,verified_same_holder=True,readback_path=str(p));self._last_verified_receipt=actual;return actual
 def get(self,suffix):
  self.deadline();return self.call('github_fetch',{'url':'https://api.github.com/repos/Elinfiny/TraceHarbor/'+suffix})
 def verified_readback(self,ref,commit_sha,tree_sha,name,raw,end_utc):
  # Shared genuine normalizer is used by every bridge return, including mocks.
  self.deadline();ref=ref.removeprefix('refs/heads/');actual=self.get('git/ref/heads/'+ref);commit=self.get('commits/'+commit_sha)
  if actual['object']['sha']!=commit_sha or commit['author']['id']!=OWNER or commit['committer']['id']!=OWNER or [p['sha'] for p in commit['parents']]!=[self.source] or commit['commit']['tree']['sha']!=tree_sha:raise ValueError('Actual Owner/ref/source-parent/tree')
  source=self.get('git/commits/'+self.source);before=self.get('git/trees/'+source['tree']['sha']);after=self.get('git/trees/'+tree_sha)
  entries=lambda t:{e['path']:{k:e[k] for k in ['sha','mode','type']} for e in t['tree']};a,b=entries(before),entries(after)
  if before.get('truncated') or after.get('truncated') or name in a or set(b)!=set(a)|{name} or any(a[k]!=b[k] for k in a) or b[name]['mode']!='100644' or b[name]['type']!='blob':raise ValueError('Whole immutable exact oneleaf delta')
  blob=self.get('git/blobs/'+b[name]['sha']);actual_raw=base64.b64decode(''.join(blob['content'].split()),validate=True)
  if actual_raw!=raw or blob['size']!=len(raw) or hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=b[name]['sha']:raise ValueError('Actual whole immutable blob closure')
  self.deadline()
  if time.time()>=end_utc:raise HostUnknown('Late immutable readback')
  return {'ref':actual['ref'],'commit':commit_sha,'tree':tree_sha,'bytes':len(raw),'sha256':sha(raw),'GitGET_calls':6,'native_authority':False}
 def verified_ciphertext_readback(self,plan,results,end_utc):
  raw=base64.b64decode(plan['operations'][0]['body']['content'],validate=True)
  if len(raw)>131072 or sha(raw)!=plan['ciphertext_sha256']:raise ValueError('Actual prepared ciphertext')
  return self.verified_readback(plan['ref'],results[2]['sha'],results[1]['sha'],plan['path'],raw,end_utc)
 def authenticated_artifact_zip(self,run_id,name,deadline,cap):
  self.deadline()
  if cap!=8192 or run_id!=self.config['run_id'] or name!='traceharbor-recipient104-'+str(run_id)+'-1':raise ValueError('Exact actualrun artifact target')
  run=self.get('actions/runs/'+str(run_id))
  if run['head_sha']!=self.source or run['id']!=run_id or run['run_attempt']!=1 or run['actor']['id']!=OWNER or run['repository']['id']!=1391430317 or run['event']!='workflow_dispatch' or run['status']!='in_progress':raise ValueError('Actual current run context')
  original=self.call('github_fetch_workflow_run_artifacts',{'repo_full_name':REPO,'run_id':run_id,'name':name})
  items=original.get('artifacts',[])
  if original.get('total_count')!=1 or len(items)!=1:raise ValueError('Exact one current artifact; no truncated firstpage inference')
  artifact=items[0]
  if artifact['name']!=name or artifact['expired'] or artifact['size_in_bytes']>cap or artifact['workflow_run']['id']!=run_id or artifact['workflow_run']['head_sha']!=self.source or not re.fullmatch('sha256:[0-9a-f]{64}',artifact.get('digest','')):raise ValueError('Current artifact metadata/digest')
  downloaded=self.call('github_download_workflow_artifact',{'repo_full_name':REPO,'artifact_id':artifact['id'],'file_name':'recipient118.zip'})
  # Only exact reusable file references supplied by the current connector.
  ref=downloaded.get('file',downloaded)
  if type(ref) is not dict or not ref.get('file_id') or not ref.get('file_name'):raise HostUnknown('Actual reusable file reference shape required; no URL fallback')
  item={k:ref[k] for k in ['library_file_id','file_id','file_name'] if k in ref}
  transfer=self.bridge('library_materialize',{'items':[item],'destination':{'directory':str(self.root/'recipient-artifact')}})
  if transfer.get('file_id')!=ref['file_id'] or not transfer.get('library_file_id'):raise HostUnknown('Authenticated reference not materialized with Library identity')
  path=pathlib.Path(transfer['workspace_path']);self.apply_attrs(path,transfer);raw=path.read_bytes();digest=artifact['digest'][7:];public=validate_zip(raw,digest)
  if public.get('context',{}).get('run_id')!=run_id or public['context'].get('source_sha')!=self.source:raise ValueError('Actual public recipient context')
  if time.monotonic()>=deadline:raise HostUnknown('Late artifact bytes; originals retained')
  return {'zip_bytes':raw,'zip_sha256':digest,'artifact':artifact,'receipt':{'artifact_id':artifact['id'],'run_id':run_id,'bytes':len(raw),'sha256':digest,'file_id':transfer['file_id'],'library_file_id':transfer['library_file_id'],'native_authority':False}}

class ProspectiveDispatchUI:
 """Executable interface to actual mcp__codex_apps__browser_js, NOT run118.

 The future reviewed scripts must be derived from the supported Browser runtime
 documentation and actual then-current DOM. Their exact hashes and source/input
 contract are independently frozen before binding. No guessed future locators,
 browser fields, hidden HTTP endpoint or current PC dependency is assumed.
 """
 def __init__(self,browser_js,expected,save,reviewed_scripts):
  self.browser_js=browser_js;self.expected=expected;self.save=save;self.scripts=reviewed_scripts;self.attempted=False
  if set(reviewed_scripts)!={'read_current','click_dispatch','read_after'}:raise ValueError('Complete observed UI scripts required')
  for name,item in reviewed_scripts.items():
   if sha(item['code'].encode())!=item['sha256'] or item.get('from_actual_runtime_documentation_and_DOM') is not True:raise ValueError('Exact prospectively reviewed actual UI script')
 async def dispatch_once(self,current_binding,once_reservation):
  if self.attempted or current_binding!=self.expected or once_reservation.get('state')!='CONSUMED_BEFORE_EFFECT' or once_reservation.get('source_sha')!=self.expected['source_sha']:raise ValueError('Exact current UI/source/once binding')
  # browser_js is the ACTUAL native tool callable with {code}, never eval/HTTP.
  original=await self.browser_js({'code':self.scripts['read_current']['code']});self.save({'phase':'current_DOM_original','original':original})
  observation=self.scripts['read_current']['parse_observation'](original)
  if observation!={'workflow_url':self.expected['workflow_url'],'authenticated_owner':'Elinfiny','focus_conflict':False,'source_sha':self.expected['source_sha'],'inputs':self.expected['inputs'],'dispatch_matches':1,'enabled':True}:raise ValueError('Actual complete current DOM projection required')
  self.attempted=True
  result=await self.browser_js({'code':self.scripts['click_dispatch']['code']});self.save({'phase':'dispatch_original','original':result})
  after=await self.browser_js({'code':self.scripts['read_after']['code']});self.save({'phase':'after_original','original':after})
  observed=self.scripts['read_after']['parse_observation'](after)
  if observed.get('source_sha')!=self.expected['source_sha'] or type(observed.get('run_id')) is not int:raise HostUnknown('Dispatch UNKNOWN, no retry')
  return {'run_id':observed['run_id'],'source_sha':observed['source_sha'],'transport':'ACTUAL_BROWSER_JS_PROSPECTIVE','native_authority':False}

def main():
 if sys.argv[1]=='--writer':
  request=strict(pathlib.Path(sys.argv[2]).read_bytes());print(can(candidate_checkpoint(**request)).decode());return 0
 if sys.argv[1]=='--qualify-readonly':
  cfg=strict(pathlib.Path(sys.argv[2]).read_bytes());
  if sys.stdin.isatty():
   import termios
   attrs=termios.tcgetattr(sys.stdin.fileno());attrs[3]&=~(termios.ICANON|termios.ECHO);termios.tcsetattr(sys.stdin.fileno(),termios.TCSANOW,attrs)
  ledger=FrameLedger(cfg['output'],cfg['context'],cfg['deadline_utc_ms']);bridge=StdioBridge(ledger)
  try:
   transport=HostTransport(bridge,ledger.root,cfg)
   original=transport.call('github_fetch',{'url':READ_PR})
   if original['number']!=18 or original['head']['sha']!=cfg['context']['source_sha'] or original['state']!='open':raise ValueError('Actual pinned current PR18')
   proof={'schema':'TRACE118_GENUINE_READONLY_BRIDGE','holder_pid':os.getpid(),'context':cfg['context'],'seq':ledger.seq,'actual_PR':18,'actual_head':original['head']['sha'],'actual_main':original['base']['sha'],'transport_counts':transport.counts,'public_metadata_only':True,'native_authority':False,'result':'PASS','cleanup':'NO_CHILDREN_OR_NATIVE_ARTIFACTS; holder exits0'}
   put(pathlib.Path(cfg['output'])/'genuine-proof.json',can(proof));print(can({'schema':'TRACE118_HOLDER_TERMINAL','result':'PASS','exit_code':0,'proof_sha256':sha(can(proof))}).decode());return 0
  except BaseException as exc:
   ledger.failed=True;put(pathlib.Path(cfg['output'])/'genuine-error.json',can({'exception_class':type(exc).__name__,'status':'UNKNOWN_NO_RETRY'}));print(can({'schema':'TRACE118_HOLDER_TERMINAL','result':'UNKNOWN','exit_code':1}).decode());return 1
 raise ValueError('Only fixed source commands')
if __name__=='__main__':sys.exit(main())
