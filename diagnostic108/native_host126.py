"""Source-pinned solewriter host IPC adapter118, distinct from runner authority.

Import is inert. The code-mode bridge invokes actual enabled tools. This holder
accepts planned data/original returns only; no eval, arbitrary command, PAT,
cookie, HTTP or native capability transfer. Read-only qualification never CASes.
"""
import os,sys,pathlib,json,hashlib,time,subprocess,copy,zipfile,io,stat,re,base64,selectors,termios
OWN='libfile_3ee8270f03d8819188e1de1f75c3d824';OWNER=273768139;REPO='Elinfiny/TraceHarbor'
MAX_FRAME=1048576;WRITER='e839e90d6a61ceb21ab32dd8c78f27ab63a346e8e5ec0c4d12a1356db4fe3436'
READ_PR='https://api.github.com/repos/Elinfiny/TraceHarbor/pulls/18'
OPS={'github_fetch','github_create_blob','github_create_tree','github_create_commit','github_create_ref','github_fetch_workflow_run_artifacts','github_download_workflow_artifact','library_replace','library_materialize','github_fetch_workflow_run_jobs'}
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
  self.root=pathlib.Path(root);self.root.mkdir(mode=0o700,exist_ok=False);self.context=copy.deepcopy(context);self.deadline_ms=deadline_ms;self.parent_mono=time.monotonic()+max(0,(deadline_ms/1000-time.time()));self.phase_mono=self.parent_mono;self.seq=0;self.pending=None;self.failed=False
 def bind_phase(self,end):
  if self.failed or self.pending is not None or not time.monotonic()<end<=self.parent_mono:raise HostUnknown('Actual earlier phase required')
  self.phase_mono=end
 def remaining(self):return min(self.phase_mono-time.monotonic(),self.parent_mono-time.monotonic(),self.deadline_ms/1000-time.time())
 def request(self,op,args):
  if self.failed or self.pending is not None or op not in OPS or self.remaining()<=0:raise HostUnknown('Holder phase/sequence/op unavailable')
  if self.context['domain']=='READONLY_QUALIFICATION118' and (op!='github_fetch' or args!={'url':READ_PR}):raise ValueError('Read-only exact PR18 route')
  self.seq+=1
  frame={'schema':'TRACE118_HOST_REQUEST','seq':self.seq,'context':self.context,'op':op,'args':args,'deadline_utc_ms':min(self.deadline_ms,int((time.time()+self.remaining())*1000)),'phase_deadline_mono':self.phase_mono}
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
   if self.remaining()<=0 or int(time.time()*1000)>=p['deadline_utc_ms'] or value.get('late') is True:raise HostUnknown('Late original remains UNKNOWN')
   if value.get('transport_error') is not None:raise HostUnknown('Tool transport exception preserved')
   result=normalizer(value['original_result'],p['op']);self.pending=None
   put(self.root/f'{seq}.accepted.json',can({'seq':seq,'request_sha256':p['request_digest'],'original_frame_sha256':sha(raw),'original_result_sha256':sha(can(value['original_result'])),'domain':self.context['domain'],'normalized_kind':p['op'],'native_authority':False}))
   return result
  except BaseException:
   self.failed=True;raise
 def unknown_stream(self,raw,event,error=None):
  self.failed=True
  put(self.root/f'{self.seq}.partial.original.bin',raw)
  put(self.root/f'{self.seq}.stream-UNKNOWN.json',can({'seq':self.seq,'event':event,'exception_class':error,'raw_bytes':len(raw),'raw_sha256':sha(raw),'status':'UNKNOWN_NO_RETRY'}))
  raise HostUnknown('Bounded original IPC remains UNKNOWN; no retry')
class StdioBridge:
 def __init__(self,ledger,input_fd=None,output=None):self.ledger=ledger;self.input_fd=sys.stdin.fileno() if input_fd is None else input_fd;self.output=sys.stdout.buffer if output is None else output
 def bind_phase(self,end):self.ledger.bind_phase(end)
 def __call__(self,op,args):
  frame=self.ledger.request(op,args);raw=bytearray();chunks=0;fd=self.input_fd;blocking=os.get_blocking(fd);attrs=termios.tcgetattr(fd) if os.isatty(fd) else None;primary=None;cleanup=[]
  try:
   if attrs is not None:
    temporary=copy.deepcopy(attrs);temporary[3]&=~(termios.ICANON|termios.ECHO);termios.tcsetattr(fd,termios.TCSANOW,temporary)
   os.set_blocking(fd,False)
   self.output.write(can(frame)+b'\n');self.output.flush()
   with selectors.DefaultSelector() as selector:
    selector.register(fd,selectors.EVENT_READ)
    while True:
     remaining=min(self.ledger.remaining(),frame['deadline_utc_ms']/1000-time.time())
     if remaining<=0:self.ledger.unknown_stream(bytes(raw),'DEADLINE')
     if not selector.select(remaining):self.ledger.unknown_stream(bytes(raw),'DEADLINE')
     try:chunk=os.read(fd,min(65536,MAX_FRAME+2-len(raw)))
     except BlockingIOError:continue
     except BaseException as exc:
      put(self.ledger.root/f'{frame["seq"]}.read-exception.original.json',can({'exception_class':type(exc).__name__,'errno':getattr(exc,'errno',None)}))
      self.ledger.unknown_stream(bytes(raw),'READ_EXCEPTION',type(exc).__name__)
     chunks+=1;put(self.ledger.root/f'{frame["seq"]}.chunk{chunks}.original.bin',chunk)
     # Every chunk, including EOF, is durable before parse or late guard.
     if not chunk:self.ledger.unknown_stream(bytes(raw),'EOF')
     raw.extend(chunk)
     if len(raw)>MAX_FRAME+1:self.ledger.unknown_stream(bytes(raw),'OVERSIZE')
     if b'\n' in raw:
      if not raw.endswith(b'\n') or raw.count(b'\n')!=1:self.ledger.unknown_stream(bytes(raw),'MULTIPLE_OR_PARTIAL_FRAME')
      return self.ledger.accept(bytes(raw[:-1]))
  except BaseException as exc:primary=exc;self.ledger.failed=True;raise
  finally:
   # Borrowed descriptors are restored exactly once; never closed or killed.
   try:os.set_blocking(fd,blocking)
   except BaseException as exc:cleanup.append({'blocking_restore':type(exc).__name__})
   if attrs is not None:
    try:termios.tcsetattr(fd,termios.TCSANOW,attrs)
    except BaseException as exc:cleanup.append({'termios_restore':type(exc).__name__})
   put(self.ledger.root/f'{frame["seq"]}.fd-restoration.json',can({'blocking':blocking,'termios_borrowed':attrs is not None,'primary_exception':type(primary).__name__ if primary else None,'cleanup_errors':cleanup,'restore_attempts':1}))
   if cleanup:
    self.ledger.failed=True
    if primary is None:raise HostUnknown('FD cleanup UNKNOWN; no next operation')
def selfhash(doc):
 c=copy.deepcopy(doc);c['self_sha256']=None;return sha(can(c))
def check_checkpoint(path,library_id,version,expected_sha=None):
 p=pathlib.Path(path);raw=p.read_bytes();d=strict(raw)
 if library_id!=OWN or os.getxattr(p,'user.library-file-id').decode()!=OWN or int(os.getxattr(p,'user.library-file-version').decode())!=version or selfhash(d)!=d['self_sha256'] or expected_sha is not None and sha(raw)!=expected_sha or d['ownership']['owner']!='TraceHarbor V1' or d['ownership']['duplicate_trace_route_owners']!=0:raise ValueError('Actual current owned preimage/self/allattrs required')
 return d,raw
ORIGINAL_WRITER_SHA256='008f194ac2d4cd93e946949bb2a926acb58690adb1815734601cd9808e73550f'
def private_regular(path):
 p=pathlib.Path(path);st=p.lstat()
 if p.is_symlink() or not stat.S_ISREG(st.st_mode) or st.st_uid!=os.getuid() or st.st_mode&0o077:raise ValueError('Exact owned private regular source/reference')
 return p
def validate_transfer_layout(binding,holder=None):
 layout=binding['transfer_layout'];roots={}
 if set(layout)!={'private','transfer','holder_parent'}:raise ValueError('Exact reviewed disjoint layout')
 for role,expected in layout.items():
  path=pathlib.Path(expected['path']);st=path.lstat()
  if not path.is_absolute() or path.resolve()!=path or path.is_symlink() or not stat.S_ISDIR(st.st_mode) or (st.st_dev,st.st_ino,st.st_uid)!=(expected['dev'],expected['ino'],expected['uid']) or st.st_uid!=os.getuid() or expected['type']!='directory':raise ValueError('Same positively identified owned directory, no aliases/adoption')
  if role!='transfer' and st.st_mode&0o077:raise ValueError('Protected binding/holder roots remain0700')
  roots[role]=path
 for role,path in roots.items():
  for other,another in roots.items():
   if role!=other and (path==another or path.is_relative_to(another)):raise ValueError('Transfer and protected roots must be disjoint, never ancestors/descendants')
 if str(roots['private'])!=binding['binding_root']:raise ValueError('Actual CURRENT private binding root')
 if holder is not None and pathlib.Path(holder)!=roots['holder_parent']/'holder':raise ValueError('Exact reviewed holder locator')
 return roots
def current_binding(base,version,config,require_plan=False,payload=None,_macro122=None):
 doc,raw=check_checkpoint(base,OWN,version)
 match=re.fullmatch(r'NATIVE([1-9][0-9]{0,3})_([A-Z_]+)',doc['state'])
 if match is None or match[2]=='TERMINAL':raise ValueError('No mutation of sealed historical direction')
 number=int(match[1]);key='native'+str(number);n=doc[key];direction=n['direction']
 if type(config.get('direction_number')) is not int or config['direction_number']!=number or not re.match(r'^V28-(?:TRACEHARBOR|TRACE)-'+str(number)+'-',direction['id']) or len(direction['body'].encode())!=direction['bytes'] or sha(direction['body'].encode())!=direction['sha256']:raise ValueError('Exact strict current direction/body pin')
 if not n['records'] or n['records'][0]['phase']!='RX_START':raise ValueError('Actual current owned intake required')
 binding=n['records'][0]['payload']['writer_binding']
 validate_transfer_layout(binding)
 if config.get('writer_binding')!=binding or binding['direction_number']!=number or binding['direction_id']!=direction['id'] or binding['direction_sha256']!=direction['sha256'] or binding['direction_bytes']!=direction['bytes']:raise ValueError('Config is not authority; accepted CURRENT intake binding required')
 root=pathlib.Path(binding['binding_root']);rs=root.lstat()
 if root.is_symlink() or not stat.S_ISDIR(rs.st_mode) or rs.st_uid!=os.getuid() or rs.st_mode&0o077:raise ValueError('Actual sole owned private binding root')
 original=private_regular(binding['original_writer_path']);writer=private_regular(root/('admin'+str(number)+'.py'));auditor=pathlib.Path(binding['auditor_path'])
 if binding['writer_path']!=str(writer) or not auditor.is_relative_to(root) or auditor.is_symlink():raise ValueError('Derived CURRENT writer and intake locator only')
 source=n['source_verification']['Auditor_V28_checkpoint.json'];araw=auditor.read_bytes();audit=strict(araw);copy_a=copy.deepcopy(audit);copy_a['integrity']['canonical_json_sha256']=None
 if type(binding['auditor_version']) is not int or binding['auditor_version']!=source['version'] or sha(araw)!=source['sha256'] or len(araw)!=source['bytes'] or sha(can(copy_a))!=source['self_sha256'] or audit['integrity']['canonical_json_sha256']!=source['self_sha256'] or os.getxattr(auditor,'user.library-file-id').decode()!=source['library_file_id'] or int(os.getxattr(auditor,'user.library-file-version').decode())!=source['version']:raise ValueError('Actual accepted current Auditor snapshot/fullbytes/self/identity/version')
 boundary=audit['operation']['effect_replay_boundary'];boundary=strict(boundary) if isinstance(boundary,str) else boundary;addressed=boundary['recipient_outboxes']['TraceHarbor V1']
 if addressed!=direction or doc['guard']['operation_id']!=direction['id']:raise ValueError('Current addressed direction/source route differs')
 if sha(original.read_bytes())!=ORIGINAL_WRITER_SHA256 or binding['original_writer_sha256']!=ORIGINAL_WRITER_SHA256:raise ValueError('Authentic008f original preimage')
 expected=original.read_text().replace('118',str(number)).replace("a['state']=='NATIVE117_TERMINAL'","a['state']=='NATIVE"+str(number-1)+"_TERMINAL'").replace('CURRENT Auditor858 direction'+str(number),'CURRENT Auditor'+str(binding['auditor_version'])+' direction'+str(number))
 if writer.read_text()!=expected or sha(writer.read_bytes())!=binding['writer_sha256']:raise ValueError('Only exact limited original label/predecessor/event binding adaptation; no arbitrary patch/module')
 if require_plan:
  if _macro122 is not None:
   _check_macro122(_macro122,{'number':number,'key':key,'binding':binding,'direction':direction,'original':original,'writer':writer,'doc':doc,'raw':raw},version,payload)
  else:
   if n['records'][-1]['phase']!='PUBLISH_INTENT' or n['records'][-1]['payload'].get('phase')!='SOURCE_FREEZE':raise ValueError('Current durable exact prepared operation required')
   plan=n['records'][-1]['payload']['prepared_operation']
   if config.get('prepared_operation')!=plan or plan['expected_current_version']!=version or plan['phase']!='PUBLISH_INTENT' or sha(can(payload))!=plan['payload_sha256'] or payload.get('source_sha')!=plan['source_sha'] or config['source_sha']!=plan['source_sha'] or config['host_source_sha256']!=plan['host_source_sha256'] or config['deadline_utc_ms']!=plan['deadline_utc_ms'] or config['context']!=plan['context'] or plan['direction_id']!=direction['id'] or plan['writer_sha256']!=binding['writer_sha256']:raise ValueError('Exact current phase/plan/payload/source/clock/version/path provenance before effect')
   if type(plan['phase_s']) is not int or not 0<plan['phase_s']<=plan['maximum_phase_s'] or config['phase_s']!=plan['phase_s']:raise ValueError('Immutable bounded planned phase')
 return {'number':number,'key':key,'binding':binding,'direction':direction,'original':original,'writer':writer,'doc':doc,'raw':raw}
def validate_writer_output(base,target,version,payload,receipt,config,_macro122=None):
 binding=current_binding(base,version,config,require_plan=True,payload=payload,_macro122=_macro122);a=binding['doc'];raw=pathlib.Path(target).read_bytes();c=strict(raw);key=binding['key'];b=binding['binding']
 expected_path=pathlib.Path(b['binding_root'])/('candidate'+str(version+1))/'TraceHarbor_V1_checkpoint.json'
 if pathlib.Path(target)!=expected_path or receipt['candidate']!=str(expected_path) or receipt['version']!=version+1 or receipt['preservation']!='PASS' or sha(raw)!=receipt['raw_sha256'] or selfhash(c)!=c['self_sha256'] or receipt['self_sha256']!=c['self_sha256']:raise ValueError('Exact current prepared final path/wholebytes/self/version')
 utc=c['events'][-1]['utc'];__import__('datetime').datetime.fromisoformat(utc)
 wanted=copy.deepcopy(a);n=wanted[key];n['records'].append({'phase':'PUBLISH_INTENT','payload':payload});n['phase']='PUBLISH_INTENT';n['previous_checkpoint']={'version':version,'raw_sha256':sha(binding['raw']),'self_sha256':a['self_sha256']};n['writer_sha256']=b['writer_sha256'];n['phase_history'].append({'phase':'PUBLISH_INTENT','utc':utc,'actual_own_version':version+1})
 wanted['events'].append({'phase':'PUBLISH_INTENT','utc':utc,'delivery_id':binding['direction']['id'],'own_version':version+1,'source':'CURRENT Auditor'+str(b['auditor_version'])+' direction'+str(binding['number']),'scope':'SAME_HOST_PRODUCER_COUNTER_CONTRACT_REVIEW_SOURCE'})
 wanted['guard'].update(operation_id=binding['direction']['id'],operation_state='PUBLISH_INTENT',epoch_checkpoint_counter=version+1,checkpoint_fresh='EXACT_CAS_AND_PINNED_FULLBYTE_SELF_ALLATTRS_READBACK');wanted['state']='NATIVE'+str(binding['number'])+'_PUBLISH_INTENT';wanted['self_sha256']=selfhash(wanted)
 if c!=wanted:raise ValueError('Any unrelated root/nested/history/guard/output delta is forbidden')
 return c
class HostTransport:
 def __init__(self,bridge,root,config):
  self.bridge=bridge;self.root=pathlib.Path(root);self.config=config;self.source=config['source_sha'];self._version=None;self._checkpoint=None;self._last_verified_receipt=None;self.reserved=set();self.counts={'GitGET':0,'Gitwrites':0,'CAS':0,'materialize':0}
  rs=self.root.lstat()
  if not stat.S_ISDIR(rs.st_mode) or self.root.is_symlink() or rs.st_uid!=os.getuid() or rs.st_mode&0o077:raise ValueError('Actual owned private holder root')
  if sha(pathlib.Path(__file__).read_bytes())!=config['host_source_sha256']:raise ValueError('Actual source-pinned host transport')
  helper=pathlib.Path(config['library_helper'])
  if sha(helper.read_bytes())!=config['library_helper_sha256']:raise ValueError('Current helper source pin')
  self.layout=validate_transfer_layout(config['writer_binding'],self.root)
  self.helper=helper;self.parent_mono=time.monotonic()+max(0,config['deadline_utc_ms']/1000-time.time());self.phase_mono=self.parent_mono
  if config.get('current_checkpoint') is not None:
   d,raw=check_checkpoint(config['current_checkpoint'],OWN,config['current_version'],config['current_sha256']);self._checkpoint=pathlib.Path(config['current_checkpoint']);self._version=config['current_version']
 def bind_phase(self,end):
  if not time.monotonic()<end<=self.parent_mono:raise HostUnknown('Actual phase bounded by original host parent')
  self.phase_mono=end;self.bridge.bind_phase(end)
 def remaining(self):return min(self.phase_mono-time.monotonic(),self.parent_mono-time.monotonic(),self.config['deadline_utc_ms']/1000-time.time())
 def deadline(self):
  if self.remaining()<=0:raise HostUnknown('Fixed actual host phase/parent end; no reset')
 @property
 def current_checkpoint_version(self):
  if self._version is None:raise HostUnknown('No actual own readback bound')
  return self._version
 def call(self,op,args):
  macro=_bound_macro122(self)
  if macro is None:return self._call122_body(op,args)
  try:return self._call122_body(op,args)
  except BaseException as exc:macro[0].unknown(type(exc).__name__)
 def _call122_body(self,op,args):
  self.deadline()
  if op not in OPS:raise ValueError('Unsupported logical operation')
  if op.startswith('github_create_'):
   if args.get('repository_full_name')!=REPO or self.config.get('domain')=='READONLY_QUALIFICATION118':raise ValueError('No effect in qualification/wrong repository')
   digest=sha(can({'tool':op,'args':args}))
   if _bound_macro122(self) is not None:
    _bound_macro122(self)[0].begin_git(op,args)
   else:
    if digest not in self.reserved:raise ValueError('Durable originalwriter attempt must precede effect')
    self.reserved.remove(digest)
   self.counts['Gitwrites']+=1
  else:self.counts['GitGET']+=int(op.startswith('github_'))
  # FrameLedger + bridge persist actual original on BOTH sides before parse.
  result=self.bridge(op,args)
  if op.startswith('github_create_') and _bound_macro122(self) is not None:
   # Existing bridge retains full original before normalization/postguard.
   self.deadline()
   kind=op.removeprefix('github_create_')
   suffix=('git/blobs/'+result['sha'] if kind=='blob' else 'git/trees/'+result['sha'] if kind=='tree' else 'commits/'+result['sha'] if kind=='commit' else 'git/ref/heads/'+args['branch_name'])
   proof=self.bridge('github_fetch',{'url':'https://api.github.com/repos/Elinfiny/TraceHarbor/'+suffix});self.counts['GitGET']+=1
   _bound_macro122(self)[0].git_original(can(proof),can(result))
  self.deadline();return result
 def reserve_operation(self,key,tool,args,source,end_utc):
  self.deadline()
  if source!=self.source or tool not in OPS or not tool.startswith('github_create_') or not time.time()+1<end_utc:raise ValueError('Exact scoped future write reservation')
  digest=sha(can({'tool':tool,'args':args}))
  if digest in self.reserved:raise HostUnknown('Attempt already reserved')
  receipt=self.cas_checkpoint(self.current_checkpoint_version,{'phase':'GIT_WRITE_ATTEMPT','source_sha':source,'operation':key,'tool':tool,'args_sha256':digest,'status':'CONSUMED_BEFORE_EFFECT'})
  self.reserved.add(digest);return receipt
 def cas_checkpoint(self,expected_version,payload):
  macro=_bound_macro122(self)
  if macro is None:return self._cas_checkpoint122_body(expected_version,payload)
  try:return self._cas_checkpoint122_body(expected_version,payload)
  except BaseException as exc:macro[0].unknown(type(exc).__name__)
 def _cas_checkpoint122_body(self,expected_version,payload):
  self.deadline()
  if self.config.get('domain')=='READONLY_QUALIFICATION118' or expected_version!=self.current_checkpoint_version:raise ValueError('CAS currentversion/read-only guard before any effect')
  current=current_binding(self._checkpoint,expected_version,self.config,require_plan=True,payload=payload,_macro122=_bound_macro122(self));original_writer=current['original'];writer_path=current['writer'];namespace=current['key']
  original=strict(self._checkpoint.read_bytes())
  if any(r.get('phase')=='PUBLISH_INTENT' and r.get('payload')==payload for r in original[namespace]['records']):raise HostUnknown('Existing exact attempt consumed; no retry')
  if payload.get('source_sha')!=self.source:raise ValueError('Current source-bound payload')
  if payload.get('phase')=='PUBLISH_INTENT':
   if _bound_macro122(self) is None and sha(can(payload))!=self.config['prepared_operation']['payload_sha256']:raise ValueError('Preplanned current publication payload')
  elif payload.get('phase') not in ('admit','consumed','GIT_WRITE_ATTEMPT') or set(payload)-{'phase','source_sha','descriptor_sha256','parent_clock','custody','operation','tool','args_sha256','status'}:raise ValueError('Exact scoped external host journal payload')
  request=self.root/('writer-'+str(expected_version)+'.payload.json');put(request,can(payload))
  target=writer_path.parent/('candidate'+str(expected_version+1))/'TraceHarbor_V1_checkpoint.json'
  if target.exists():raise HostUnknown('Writer destination exists; no adoption/retry')
  command=[sys.executable,str(writer_path),'build',str(self._checkpoint),str(expected_version),'PUBLISH_INTENT',str(request)]
  before=time.monotonic()
  try:
   process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   stdout,stderr=process.communicate(timeout=min(10,max(.001,self.remaining())))
   result=subprocess.CompletedProcess(command,process.returncode,stdout,stderr)
   terminal={'returncode':result.returncode,'stdout_hex':result.stdout.hex(),'stderr_hex':result.stderr.hex(),'status':'TERMINAL','elapsed_s':time.monotonic()-before}
  except subprocess.TimeoutExpired as exc:
   put(self.root/('writer-'+str(expected_version)+'.original.json'),can({'status':'TIMEOUT_UNKNOWN','returncode':process.poll(),'pid':process.pid,'hidden_kill':False,'stdout_hex':(exc.stdout or b'').hex(),'stderr_hex':(exc.stderr or b'').hex(),'elapsed_s':time.monotonic()-before,'exception_class':type(exc).__name__}))
   raise HostUnknown('Writer timeout originals retained; no retry') from exc
  except BaseException as exc:
   put(self.root/('writer-'+str(expected_version)+'.original.json'),can({'status':'EXCEPTION_UNKNOWN','returncode':None,'exception_class':type(exc).__name__,'errno':getattr(exc,'errno',None),'elapsed_s':time.monotonic()-before}))
   raise HostUnknown('Writer exception preserved; no fabricated terminal') from exc
  put(self.root/('writer-'+str(expected_version)+'.original.json'),can(terminal));self.deadline()
  if result.returncode!=0:raise HostUnknown('Actual producer terminal not0')
  writer=strict(result.stdout)
  if writer['candidate']!=str(target) or writer['version']!=expected_version+1 or writer['preservation']!='PASS':raise ValueError('Exact original producer output locator')
  candidate=validate_writer_output(self._checkpoint,target,expected_version,payload,writer,self.config,_macro122=_bound_macro122(self))
  put(self.root/('writer-'+str(expected_version)+'.provenance.json'),can({'original_source_sha256':sha(original_writer.read_bytes()),'actual_invoked_source_sha256':sha(writer_path.read_bytes()),'direction_number':current['number'],'direction_id':current['direction']['id'],'current_namespace':namespace,'body_sha256':current['direction']['sha256'],'Auditor_version':current['binding']['auditor_version'],'command':command,'binding_adaptation':'EXACT_CURRENT_LABELS_PREDECESSOR_AUDITOR_ONLY','terminal_sha256':sha(can(terminal)),'candidate_sha256':writer['raw_sha256'],'preimage_sha256':sha(self._checkpoint.read_bytes()),'preservation':'PASS','protocol_marker':WRITER,'protocol_marker_is_process_pin':False}))
  # Never expose protected binding/holder ancestry to Library preparation.
  # Upload a fresh authenticated byte-identical staging copy in the disjoint
  # transfer area; the actual private producer output remains immutable.
  self.layout=validate_transfer_layout(current['binding'],self.root)
  upload_dir=self.layout['transfer']/('own-upload-'+str(expected_version));upload_dir.mkdir(mode=0o700,exist_ok=False)
  upload=upload_dir/'TraceHarbor_V1_checkpoint.json';put(upload,target.read_bytes())
  for name in os.listxattr(target):os.setxattr(upload,name,os.getxattr(target,name))
  if upload.read_bytes()!=target.read_bytes():raise ValueError('Exact actual producer output transfercopy')
  put(self.root/('transfer-'+str(expected_version)+'.provenance.json'),can({'private_candidate':str(target),'upload_copy':str(upload),'bytes':len(upload.read_bytes()),'sha256':sha(upload.read_bytes()),'layout':current['binding']['transfer_layout'],'expected_current_version':expected_version,'native_authority':False}))
  pub=self.bridge('library_replace',{'library_file_id':OWN,'file':str(upload),'expected_current_version':expected_version,'version_reason':'CURRENT scoped source-pinned original producer binding; necessary planned PUBLISH_INTENT; no UNKNOWN retry'})
  self.counts['CAS']+=1
  if pub.get('status')!='succeeded' or pub.get('library_file_id')!=OWN or type(pub.get('current_version_number')) is not int:raise HostUnknown('Actual Library CAS result required')
  self.apply_attrs(target,pub);self.apply_attrs(upload,pub)
  validate_transfer_layout(current['binding'],self.root)
  receipt=dict(pub,private_candidate_path=str(target),upload_copy_path=str(upload),sha256=writer['raw_sha256'],self_sha256=writer['self_sha256']);actual=self.pinned_checkpoint_readback(receipt)
  macro=_bound_macro122(self)
  if macro is not None:
   normalized=dict(actual,wholebyte_self_allattrs='PASS');macro[0].journal_original(can(normalized),self._checkpoint.read_bytes())
  return actual
 def apply_attrs(self,path,metadata):
  helper_record=self.root/('attrs-'+sha(str(path).encode())[:16]+'.original.json')
  process=subprocess.Popen([sys.executable,str(self.helper),'apply-xattrs',str(path),metadata['library_file_id']],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  try:
   out,err=process.communicate(input=json.dumps(metadata.get('xattrs',[])).encode(),timeout=min(5,max(.001,self.remaining())))
   q=subprocess.CompletedProcess(process.args,process.returncode,out,err)
   put(helper_record,can({'returncode':q.returncode,'stdout_hex':out.hex(),'stderr_hex':err.hex(),'status':'TERMINAL'}))
  except subprocess.TimeoutExpired as exc:
   put(helper_record,can({'status':'TIMEOUT_UNKNOWN','returncode':process.poll(),'pid':process.pid,'stdout_hex':(exc.stdout or b'').hex(),'stderr_hex':(exc.stderr or b'').hex(),'hidden_kill':False}))
   raise HostUnknown('Metadata helper timeout; original prefixes retained') from exc
  except BaseException as exc:
   put(helper_record,can({'status':'EXCEPTION_UNKNOWN','returncode':process.poll(),'pid':process.pid,'exception_class':type(exc).__name__}))
   raise HostUnknown('Metadata helper exception retained') from exc
  if q.returncode!=0:raise HostUnknown('Current Library helper failed')
  if os.getxattr(path,'user.library-file-id').decode()!=metadata['library_file_id']:raise ValueError('Library identity attr')
  for a in metadata.get('xattrs',[]):
   if os.getxattr(path,a['name']).decode()!=a['value']:raise ValueError('Complete Library attrs')
 def pinned_checkpoint_readback(self,receipt):
  if receipt is self._last_verified_receipt and self._checkpoint is not None and receipt.get('version')==self._version and receipt.get('sha256')==sha(self._checkpoint.read_bytes()):return receipt
  self.deadline();t=self.bridge('library_materialize',{'items':[{'library_file_id':OWN,'file_id':receipt['file_id'],'file_name':receipt['file_name']}],'destination':{'directory':str(self.layout['transfer']/('own-readback-'+str(receipt['current_version_number'])))}});self.counts['materialize']+=1
  if t.get('file_id')!=receipt['file_id'] or t.get('library_file_id')!=OWN or t.get('current_version_number')!=receipt['current_version_number'] or t.get('xattrs')!=receipt.get('xattrs'):raise HostUnknown('Pinned whole actual own readback required')
  p=pathlib.Path(t['workspace_path'])
  expected_readback=self.layout['transfer']/('own-readback-'+str(receipt['current_version_number']))/receipt['file_name']
  if p!=expected_readback or p.is_symlink():raise HostUnknown('Only actual pinned disjoint transfer destination')
  validate_transfer_layout(self.config['writer_binding'],self.root)
  self.apply_attrs(p,t);d,raw=check_checkpoint(p,OWN,t['current_version_number'],receipt['sha256'])
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
  original=self.call('github_fetch_workflow_run_artifacts',{'repo_full_name':REPO,'run_id':run_id,'name':name});items=original.get('artifacts',[])
  if original.get('total_count')!=1 or len(items)!=1:raise ValueError('Exact one current artifact')
  artifact=items[0]
  if artifact['name']!=name or artifact['expired'] or not 0<artifact['size_in_bytes']<=cap or artifact['workflow_run']['id']!=run_id or artifact['workflow_run']['head_sha']!=self.source or not re.fullmatch('sha256:[0-9a-f]{64}',artifact.get('digest','')):raise ValueError('Current artifact metadata/digest')
  downloaded=self.call('github_download_workflow_artifact',{'repo_full_name':REPO,'artifact_id':artifact['id'],'file_name':'recipient118.zip'});ref=downloaded.get('file',downloaded)
  if type(ref) is not dict or not ref.get('file_id') or type(ref.get('file_name')) is not str or pathlib.PurePath(ref['file_name']).name!=ref['file_name'] or ref['file_name'] in ('','.','..') or '\\' in ref['file_name']:raise HostUnknown('Exact reusable connectorref/basename, no URL fallback')
  layout=validate_transfer_layout(self.config['writer_binding'],self.root);destination=layout['transfer']/('recipient-artifact-'+str(run_id)+'-1')
  destination.mkdir(mode=0o700,exist_ok=False);st=destination.lstat();identity=(st.st_dev,st.st_ino,st.st_uid)
  item={k:ref[k] for k in ['library_file_id','file_id','file_name'] if k in ref}
  transfer=self.bridge('library_materialize',{'items':[item],'destination':{'directory':str(destination)}})
  # Bridge retains the native original BEFORE any guard below; no retry/adopt.
  layout=validate_transfer_layout(self.config['writer_binding'],self.root);post=destination.lstat()
  if destination.is_symlink() or not stat.S_ISDIR(post.st_mode) or (post.st_dev,post.st_ino,post.st_uid)!=identity:raise HostUnknown('Selected transfer directory identity replaced')
  if transfer.get('file_id')!=ref['file_id'] or transfer.get('file_name')!=ref['file_name'] or not transfer.get('library_file_id') or ref.get('library_file_id') is not None and transfer['library_file_id']!=ref['library_file_id']:raise HostUnknown('Returned ref/name/Library identity drift')
  path=pathlib.Path(transfer.get('workspace_path',''))
  if path!=destination/ref['file_name'] or path.is_symlink() or path.resolve()!=path:raise HostUnknown('Only exact positivelybound DISJOINT recipient destination')
  first=path.lstat()
  if not stat.S_ISREG(first.st_mode) or first.st_uid!=os.getuid() or first.st_nlink!=1 or first.st_size>cap:raise HostUnknown('Exact owned nonlinked bounded regular artifact')
  self.apply_attrs(path,transfer);fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
  try:
   before=os.fstat(fd)
   if (before.st_dev,before.st_ino,before.st_uid)!=(first.st_dev,first.st_ino,first.st_uid):raise HostUnknown('Artifact replaced beforeopen')
   raw=bytearray()
   while len(raw)<=cap:
    chunk=os.read(fd,min(4096,cap+1-len(raw)))
    if not chunk:break
    raw.extend(chunk)
   after=os.fstat(fd);end=path.lstat()
   if len(raw)>cap or len(raw)!=before.st_size or (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns) or (end.st_dev,end.st_ino)!=(after.st_dev,after.st_ino):raise HostUnknown('Artifact wholebyte/EOF/identity changed')
  finally:os.close(fd)
  raw=bytes(raw);digest=artifact['digest'][7:];public=validate_zip(raw,digest);ctx=public.get('context',{})
  if ctx.get('run_id')!=run_id or ctx.get('attempt')!=1 or ctx.get('source_sha')!=self.source or ctx.get('actor_id')!=OWNER or ctx.get('repository_id')!=1391430317 or ctx.get('repository')!=REPO or ctx.get('expires_utc')!=self.config['deadline_utc_ms']//1000:raise ValueError('Exact current recipient Owner/run/attempt/source/parent context')
  self.deadline()
  if time.monotonic()>=deadline:raise HostUnknown('Late artifact bytes; original retained')
  return {'zip_bytes':raw,'zip_sha256':digest,'artifact':artifact,'receipt':{'artifact_id':artifact['id'],'run_id':run_id,'bytes':len(raw),'sha256':digest,'file_id':transfer['file_id'],'library_file_id':transfer['library_file_id'],'disjoint_destination':str(destination),'native_authority':False}}


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

# Private122 source-reviewed finite template. Not a NativeProducer/q factory.
# This block is inert unless a later CURRENT independently admitted intake and
# durable macro SOURCE_FREEZE bind its exact bytes. JSON config is never a seal.
from enum import Enum as _Enum122

class MacroStep122(_Enum122):
 PRE_DISPATCH=0
 ADMIT=1
 ADMIT_BLOB=2
 ADMIT_TREE=3
 ADMIT_COMMIT=4
 ADMIT_REF=5
 ENCRYPTED_BLOB=6
 ENCRYPTED_TREE=7
 ENCRYPTED_COMMIT=8
 ENCRYPTED_REF=9
 CONSUMED=10
 CONSUMED_BLOB=11
 CONSUMED_TREE=12
 CONSUMED_COMMIT=13
 CONSUMED_REF=14
 TERMINAL=15

_MACRO_SEAL122=object()
_PRECEDING_NATIVE122=object()
_MACRO_CONTEXT_KEYS122=frozenset(('direction_id','direction_sha256','direction_bytes','namespace','auditor_file_id','auditor_sha256','auditor_version','writer_sha256','original_writer_sha256','host_source_sha256','manifest_sha256','source_sha','source_tree','once_receipt_sha256','attempt','owner_id','repository_id','parent_expires_utc','initial_version','baseline_entries'))
_MACRO_GRAPH122=tuple((s.name,s.value,('github_create_'+('blob','tree','commit','ref')[(s.value-2)%4] if 2<=s.value<=9 else 'github_create_'+('blob','tree','commit','ref')[(s.value-11)%4] if 11<=s.value<=14 else None)) for s in MacroStep122)

def macro_template122():
 return {'schema':'TRACE122_CLOSED_TYPED_TEMPLATE','steps':[list(s) for s in _MACRO_GRAPH122],'CAS':16,'create_only_Git':12,'dynamic_values':'Only retained preceding original returns through fixed typed methods; no JSON selector/callback/tool/path factory','native_authority':False}

def _gitblob122(raw):
 return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()

def _macro_context122(c):
 if type(c) is not dict or set(c)!=_MACRO_CONTEXT_KEYS122:raise ValueError('Closed context schema; no arbitrary selectors')
 if c['attempt']!=1 or c['owner_id']!=OWNER or c['repository_id']!=1391430317 or c['original_writer_sha256']!=ORIGINAL_WRITER_SHA256:raise ValueError('Exact original writer/Owner/repository/attempt')
 if not re.fullmatch('native[1-9][0-9]{0,3}',c['namespace']) or not re.match(r'^V28-(?:TRACEHARBOR|TRACE)-'+c['namespace'][6:]+'-',c['direction_id']):raise ValueError('Current namespace/direction')
 for key in ('direction_sha256','auditor_sha256','writer_sha256','host_source_sha256','manifest_sha256','once_receipt_sha256'):
  if not re.fullmatch('[0-9a-f]{64}',c[key]):raise ValueError('Whole context pins')
 for key in ('source_sha','source_tree'):
  if not re.fullmatch('[0-9a-f]{40}',c[key]):raise ValueError('Actual canonical commit/tree')
 if any(type(c[k]) is not int or c[k]<=0 for k in ('direction_bytes','auditor_version','parent_expires_utc','initial_version')):raise ValueError('Typed clock/version')
 entries=c['baseline_entries']
 if type(entries) is not list or len({e['path'] for e in entries})!=len(entries):raise ValueError('Whole unique baseline tree')
 for e in entries:
  if set(e)!={'path','mode','type','sha'} or '/' in e['path'] or e['path'] in ('','.','..') or not re.fullmatch('[0-9a-f]{40}',e['sha']) or (e['mode'],e['type']) not in (('100644','blob'),('100755','blob'),('040000','tree')):raise ValueError('Exact root tree entries')
 return strict(can(c))

class TypedMacro122:
 """Finite owned journal plan; seal/cursor never exported as JSON authority.

 Synthetic qualification instances cannot bind a HostTransport. Runtime release
 is absent122. Every semantic CAS/readback and every pre-effect attempt remains.
 """
 __slots__=('__ctx','__root','__inert','__cursor','__stage','__version','__unknown','__pending','__returns','__run','__admit','__delivery','__proofs','__hash','__owner','__freeze')
 def __init__(self,seal,context,root,inert,owner=None,freeze=None):
  if seal is not _MACRO_SEAL122:raise ValueError('No external dictionary/checksum/PID seal')
  self.__ctx=_macro_context122(context);self.__root=pathlib.Path(root)
  st=self.__root.lstat()
  if self.__root.is_symlink() or not stat.S_ISDIR(st.st_mode) or st.st_uid!=os.getuid() or st.st_mode&0o077:raise ValueError('Owned fresh private macro journal')
  if list(self.__root.iterdir()):raise ValueError('No adoption/replay of a prior invocation')
  self.__inert=inert;self.__owner=owner;self.__freeze=freeze;self.__cursor=0;self.__stage='READY';self.__version=context['initial_version'];self.__unknown=None;self.__pending=None;self.__returns={};self.__run=None;self.__admit=None;self.__delivery=None;self.__proofs={}
  self.__hash=sha(can({'context':self.__ctx,'template':macro_template122()}));self.__save('plan',{'context':self.__ctx,'template':macro_template122(),'macro_sha256':self.__hash,'scope':'SYNTHETIC_SOURCE_ONLY' if inert else 'PRIVATE_REVIEWED_JOURNAL_ONLY_NOT_NATIVE_CAPABILITY'})
 def __save(self,name,value):
  # put() uses O_EXCL0600: no replace/reset/ordinal refund after uncertain effect.
  put(self.__root/(name+'.json'),can(value))
 def __fail(self,reason):
  if self.__unknown is None:
   self.__unknown=reason;self.__save('FIRST_UNKNOWN',{'reason':reason,'cursor':self.__cursor,'stage':self.__stage,'native_authority':False})
  raise HostUnknown(reason)
 def __ready(self,step):
  if self.__unknown is not None:raise HostUnknown('First UNKNOWN is immutable; no dependent step/retry')
  if type(step) is not MacroStep122 or step.value!=self.__cursor or self.__stage!='READY':raise ValueError('Exact next unexecuted typed ordinal only')
 def snapshot(self):
  return {'scope':'SYNTHETIC_SOURCE_ONLY' if self.__inert else 'PRIVATE_JOURNAL_PLAN','cursor':self.__cursor,'stage':self.__stage,'version':self.__version,'first_unknown':self.__unknown,'macro_sha256':self.__hash,'native_authority':False,'NativeProducer':False,'NativeConsumedProof':False}
 def check_runtime_binding(self,transport,current,version,payload):
  if self.__inert or self.__owner is not transport:raise ValueError('Synthetic/foreign plan cannot cross effect boundary')
  c=self.__ctx;b=current['binding'];n=current['doc'][current['key']]
  if current['key']!=c['namespace'] or current['direction']['id']!=c['direction_id'] or current['direction']['sha256']!=c['direction_sha256'] or current['direction']['bytes']!=c['direction_bytes'] or b['writer_sha256']!=c['writer_sha256'] or b['auditor_version']!=c['auditor_version'] or current['doc']['native_id']!='6acfe37b-828c-83eb-b466-7670beb64ff2':raise ValueError('Same current original writer/direction/namespace only')
  source=n['source_verification']['Auditor_V28_checkpoint.json']
  if source['file_id']!=c['auditor_file_id'] or source['sha256']!=c['auditor_sha256']:raise ValueError('Same actual Auditor reference')
  if self.__freeze not in n['records'] or self.__freeze['payload'].get('macro_plan122')!={'context':c,'template':macro_template122(),'macro_sha256':self.__hash}:raise ValueError('Whole durable macro freeze required before arming')
  if version!=self.__version or self.__stage!='PREPARED' or payload!=self.__pending['payload']:raise ValueError('Exact current step/preimage/payload only')
  if transport.config['source_sha']!=c['source_sha'] or transport.config['host_source_sha256']!=c['host_source_sha256'] or transport.config['deadline_utc_ms']!=c['parent_expires_utc']*1000:raise ValueError('Original source/host/expiry; no reset')
  if time.time()>=c['parent_expires_utc']:raise HostUnknown('Parent expired; no late ACK')
  raw=(self.__root/(str(self.__cursor).zfill(2)+'-attempt.json')).read_bytes()
  if strict(raw)!=self.__pending:raise ValueError('Immutable actual attempt changed')
 def bind_run_original(self,raw,_preceding=None):
  if not self.__inert and _preceding is not _PRECEDING_NATIVE122:raise ValueError('External serialized run is not a native observation')
  if self.__cursor!=1 or self.__stage!='READY' or self.__run is not None or self.__unknown:raise ValueError('Exactly one actual dispatched-run binding after predispatch')
  self.__save('run-original',{'original_hex':raw.hex(),'scope':'SYNTHETIC' if self.__inert else 'ACTUAL_NATIVE_ORIGINAL'})
  try:
   r=strict(raw);c=self.__ctx
   if type(r['id']) is not int or r['id']<=0 or r['head_sha']!=c['source_sha'] or r['run_attempt']!=1 or r['actor']['id']!=OWNER or r['repository']['id']!=1391430317 or r['event']!='workflow_dispatch' or r['status']!='in_progress':raise ValueError('Actual run/attempt/source/Owner/event')
   started=__import__('datetime').datetime.fromisoformat(r['run_started_at'].replace('Z','+00:00')).timestamp()
   if not 0<c['parent_expires_utc']-started<=900:raise ValueError('Actual run-start parent900 cap')
   self.__run=r
  except BaseException as e:self.__fail('Invalid dispatched run original: '+type(e).__name__)
 def bind_admit(self,descriptor):
  if self.__cursor!=1 or self.__stage!='READY' or self.__run is None or self.__admit is not None:raise ValueError('Admit follows actual run only')
  d=strict(can(descriptor));c=self.__ctx
  if d.get('source_sha')!=c['source_sha'] or d.get('once_receipt_sha256')!=c['once_receipt_sha256'] or d.get('run_id')!=self.__run['id'] or d.get('attempt')!=1 or d.get('expires_utc')!=c['parent_expires_utc'] or len(can(d))>16384:raise ValueError('Exact bounded admit descriptor')
  self.__admit=d
 def bind_delivery_original(self,raw,_preceding=None):
  if not self.__inert and _preceding is not _PRECEDING_NATIVE122:raise ValueError('External serialized delivery is not preceding source execution')
  if self.__cursor!=6 or self.__stage!='READY' or 'admit' not in self.__proofs or self.__delivery is not None:raise ValueError('Current delivery only after whole admit proof')
  self.__save('delivery-original',{'original_hex':raw.hex(),'scope':'SYNTHETIC' if self.__inert else 'PRECEDING_REVIEWED_INGRESS_ORIGINAL'})
  try:
   d=strict(raw);c=self.__ctx;ctx=d['context'];body=base64.b64decode(d['ciphertext_base64'],validate=True)
   if set(d)!={'context','ciphertext_base64','ciphertext_sha256','artifact_digest','artifact_bytes','retention_days','custody_sha256'} or set(ctx)!={'repository','repository_id','actor_id','run_id','attempt','source_sha','nonce','certificate_sha256','expires_utc'} or ctx['repository']!=REPO or ctx['repository_id']!=1391430317 or ctx['actor_id']!=OWNER or ctx['run_id']!=self.__run['id'] or ctx['attempt']!=1 or ctx['source_sha']!=c['source_sha'] or ctx['expires_utc']!=c['parent_expires_utc'] or not re.fullmatch('[0-9a-f]{32}',ctx['nonce']) or not re.fullmatch('[0-9a-f]{64}',ctx['certificate_sha256']) or not 0<len(body)<=131072 or sha(body)!=d['ciphertext_sha256'] or not re.fullmatch('[0-9a-f]{64}',d['artifact_digest']) or not 0<d['artifact_bytes']<=8192 or d['retention_days']!=1 or not re.fullmatch('[0-9a-f]{64}',d['custody_sha256']):raise ValueError('Exact current recipient/ciphertext/custody/size constraints')
   self.__delivery=d
  except BaseException as e:self.__fail('Invalid preceding delivery original: '+type(e).__name__)
 def __phase(self,ordinal):return 'admit' if ordinal<=5 else 'encrypted' if ordinal<=9 else 'consumed'
 def __descriptor(self,phase):
  if self.__admit is None:raise ValueError('Missing actual admit binding')
  d=copy.deepcopy(self.__admit)
  if phase=='consumed':
   if 'encrypted' not in self.__proofs:raise ValueError('Missing preceding ciphertext whole proof')
   d.update(phase='consumed',recipient_context=self.__delivery['context'],ciphertext_receipt={'ciphertext_commit':self.__returns[8]['sha'],'ciphertext_sha256':self.__delivery['ciphertext_sha256'],'ref':self.__ref('encrypted')},admit_sha256=sha(can(self.__admit)))
  assoc=1 if phase=='admit' else 10
  receipt=self.__returns.get(assoc)
  if receipt is not None:d.update(own_cas_version=receipt['version'],own_pinned_readback_sha256=receipt['sha256'])
  return d
 def __ref(self,phase):
  suffix=self.__ctx['once_receipt_sha256']
  return 'traceharbor-counter116-'+phase+'-'+suffix if phase!='encrypted' else 'traceharbor-encrypted104-'+self.__delivery['context']['nonce']
 def __body(self,phase):
  if phase=='encrypted':
   if self.__delivery is None:raise ValueError('Missing actual recipient-bound encrypted bytes')
   return base64.b64decode(self.__delivery['ciphertext_base64'],validate=True),'traceharbor-encrypted104-'+self.__delivery['context']['nonce']+'.cms'
  return can(self.__descriptor(phase)),'counter116-'+phase+'.json'
 def __args(self,ordinal):
  phase=self.__phase(ordinal);start=2 if phase=='admit' else 6 if phase=='encrypted' else 11;kind=ordinal-start;c=self.__ctx;raw,name=self.__body(phase)
  if kind==0:return {'repository_full_name':REPO,'content':base64.b64encode(raw).decode(),'encoding':'base64'}
  if kind==1:return {'repository_full_name':REPO,'base_tree_sha':c['source_tree'],'tree_elements':[{'path':name,'mode':'100644','type':'blob','sha':self.__returns[start]['sha']}]}
  if kind==2:return {'repository_full_name':REPO,'parent_sha':c['source_sha'],'tree_sha':self.__returns[start+1]['sha'],'message':'Exact typed122 '+phase+' once [skip ci]'}
  return {'repository_full_name':REPO,'branch_name':self.__ref(phase),'sha':self.__returns[start+2]['sha']}
 def prepare(self,step):
  self.__ready(step);i=step.value;c=self.__ctx;tool=_MACRO_GRAPH122[i][2];args=self.__args(i) if tool else None
  if i==0:payload={'phase':'PUBLISH_INTENT','source_sha':c['source_sha'],'operation':'PREDISPATCH_ONCE','macro_sha256':self.__hash,'once_receipt_sha256':c['once_receipt_sha256']}
  elif i==15:
   if 'consumed' not in self.__proofs:raise ValueError('Whole consumed proof required before terminal')
   payload={'phase':'PUBLISH_INTENT','source_sha':c['source_sha'],'operation':'TERMINAL_ONCE','macro_sha256':self.__hash,'consumed_receipt_sha256':sha(can(self.__proofs['consumed']))}
  elif tool:payload={'phase':'GIT_WRITE_ATTEMPT','source_sha':c['source_sha'],'operation':step.name,'tool':tool,'args_sha256':sha(can({'tool':tool,'args':args})),'status':'CONSUMED_BEFORE_EFFECT'}
  else:
   phase='admit' if i==1 else 'consumed';payload={'phase':phase,'source_sha':c['source_sha'],'descriptor_sha256':sha(can(self.__descriptor(phase))),'parent_clock':{'run_id':self.__run['id'],'expires_utc':c['parent_expires_utc']},'custody':None if i==1 else {'sha256':self.__delivery['custody_sha256'],'context':self.__delivery['context']}}
  pending={'ordinal':i,'step':step.name,'expected_current_version':self.__version,'payload':payload,'payload_sha256':sha(can(payload)),'tool':tool,'args':args,'previous_receipts_sha256':sha(can(self.__returns)),'macro_sha256':self.__hash}
  self.__save(str(i).zfill(2)+'-attempt',pending);self.__pending=pending;self.__stage='PREPARED';return copy.deepcopy(pending)
 def journal_original(self,raw,expected_after_raw):
  if self.__unknown or self.__stage!='PREPARED':raise ValueError('No unprepared/replayed journal return')
  self.__save(str(self.__cursor).zfill(2)+'-CAS-original',{'original_hex':raw.hex()})
  try:
   r=strict(raw);d=strict(expected_after_raw)
   if r.get('status')!='succeeded' or r.get('library_file_id')!=OWN or r.get('version')!=self.__version+1 or r.get('sha256')!=sha(expected_after_raw) or r.get('self_sha256')!=selfhash(d) or d.get('self_sha256')!=selfhash(d) or r.get('wholebyte_self_allattrs')!='PASS' or type(r.get('file_id')) is not str or not r['file_id'].startswith('file_'):raise ValueError('Exact actual CAS/current final whole bytes/self/ALLattrs')
   self.__version+=1
   if self.__pending['tool'] is None:self.__returns[self.__cursor]=r;self.__cursor+=1;self.__stage='READY'
   else:self.__stage='JOURNALED'
  except BaseException as e:self.__fail('CAS original rejected: '+type(e).__name__)
 def begin_git(self,tool,args):
  if self.__unknown or self.__stage!='JOURNALED' or tool!=self.__pending['tool'] or args!=self.__pending['args']:raise ValueError('Exact journaled next create-only operation; no reorder/retry')
  if strict((self.__root/(str(self.__cursor).zfill(2)+'-attempt.json')).read_bytes())!=self.__pending:raise ValueError('Attempt bytes changed')
  self.__stage='EFFECT_ATTEMPTED';self.__save(str(self.__cursor).zfill(2)+'-effect-consumed',{'args_sha256':sha(can({'tool':tool,'args':args})),'status':'ATTEMPTED_ONCE_NO_REFUND'})
 def git_original(self,raw,created_raw=None):
  if self.__unknown or self.__stage!='EFFECT_ATTEMPTED':raise ValueError('No unattempted/repeated response')
  self.__save(str(self.__cursor).zfill(2)+'-Git-original',{'original_hex':raw.hex(),'create_return_hex':None if created_raw is None else created_raw.hex()})
  try:
   r=strict(raw);i=self.__cursor;phase=self.__phase(i);start=2 if phase=='admit' else 6 if phase=='encrypted' else 11;kind=i-start;body,name=self.__body(phase);c=self.__ctx
   if not self.__inert and created_raw is None:raise ValueError('Native create original and whole readback both required')
   if created_raw is not None:
    made=strict(created_raw)
    if kind<3 and made['sha']!=r['sha'] or kind==3 and (made['ref']!=r['ref'] or made['object']!=r['object']):raise ValueError('Readback differs from actual preceding create return')
   if kind==0:
    if r['sha']!=_gitblob122(body) or r['size']!=len(body) or base64.b64decode(''.join(r['content'].split()),validate=True)!=body or r['encoding']!='base64':raise ValueError('Whole returned blob/GitSHA/count/body')
   elif kind==1:
    expected={e['path']:e for e in c['baseline_entries']};expected[name]={'path':name,'mode':'100644','type':'blob','sha':self.__returns[start]['sha']}
    if name in {e['path'] for e in c['baseline_entries']} or r.get('truncated') or {e['path']:{k:e[k] for k in ('path','mode','type','sha')} for e in r['tree']}!=expected or len(r['tree'])!=len(expected) or not re.fullmatch('[0-9a-f]{40}',r['sha']):raise ValueError('Whole unchanged baseline+exact allowed leaf tree')
   elif kind==2:
    if r['author']['id']!=OWNER or r['committer']['id']!=OWNER or [p['sha'] for p in r['parents']]!=[c['source_sha']] or r['commit']['tree']['sha']!=self.__returns[start+1]['sha'] or not re.fullmatch('[0-9a-f]{40}',r['sha']):raise ValueError('Actual Owner/source-parent/tree commit')
   else:
    if r['ref']!='refs/heads/'+self.__ref(phase) or r['object']['type']!='commit' or r['object']['sha']!=self.__returns[start+2]['sha']:raise ValueError('Exact create-only ref and preceding actual commit')
    self.__proofs[phase]={'ref':r['ref'],'commit':r['object']['sha'],'tree':self.__returns[start+1]['sha'],'blob':self.__returns[start]['sha'],'body_sha256':sha(body),'bytes':len(body),'prior_whole_originals':True}
   self.__returns[i]=r;self.__cursor+=1;self.__stage='READY'
  except BaseException as e:self.__fail('Git original rejected: '+type(e).__name__)
 def unknown(self,reason):self.__fail('Original effect UNKNOWN: '+str(reason))

def source_only_macro122(context,root):
 # Explicit inert fixture constructor. Cannot be installed on actual transport.
 return TypedMacro122(_MACRO_SEAL122,context,root,True)

def bind_reviewed_macro122(transport,root):
 """Future current-source admission only;122 has NO native release marker.

 Does not allocate q/NativeProducer/NativeConsumedProof or dispatch permission.
 Those unchanged independent gates must still succeed on the same invocation.
 """
 current=current_binding(transport._checkpoint,transport.current_checkpoint_version,transport.config)
 d=current['direction'];n=current['doc'][current['key']];release=d.get('macro122_admission')
 if type(release) is not dict or 'ADMIT_NATIVE_TYPED_MACRO122' not in d['body'] or release.get('scope')!='JOURNAL_TEMPLATE_ONLY_NOT_NATIVE_CAPABILITY':raise ValueError('No current independent macro source admission;122 PRIVATE/INACTIVE')
 freeze=n['records'][-1]
 if freeze['phase']!='PUBLISH_INTENT' or freeze['payload'].get('phase')!='SOURCE_FREEZE':raise ValueError('Macro must freeze before arming')
 plan=freeze['payload']['macro_plan122'];context=plan['context']
 if release!={'scope':'JOURNAL_TEMPLATE_ONLY_NOT_NATIVE_CAPABILITY','host_source_sha256':sha(pathlib.Path(__file__).read_bytes()),'manifest_sha256':context['manifest_sha256'],'macro_sha256':plan['macro_sha256'],'writer_sha256':current['binding']['writer_sha256']} or plan['template']!=strict(can(macro_template122())) or plan['macro_sha256']!=sha(can({'context':context,'template':macro_template122()})) or context['initial_version']!=transport.current_checkpoint_version:raise ValueError('Whole source/manifest/template/current writer and version admission')
 value=TypedMacro122(_MACRO_SEAL122,context,root,False,transport,freeze)
 transport._macro122=value
 return value

def _check_macro122(value,current,version,payload):
 if type(value) is not tuple or len(value)!=2 or type(value[0]) is not TypedMacro122:raise ValueError('No external macro dict/config/public checksum authority')
 value[0].check_runtime_binding(value[1],current,version,payload)

def _bound_macro122(transport):
 value=getattr(transport,'_macro122',None)
 if value is None:return None
 if type(value) is not TypedMacro122:raise ValueError('Exact in-invocation typed plan only')
 return (value,transport)

class MacroPhase122(_Enum122):
 PRE_DISPATCH=(0,1,0,0)
 ADMIT=(1,6,135,685)
 ENCRYPTED=(6,10,110,440)
 CONSUMED=(10,15,110,330)
 TERMINAL=(15,16,0,0)

class SyntheticClock123:
 """Qualification clock ONLY, never usable by a runtime macro capability."""
 def __init__(self,mono=100.,wall=1000.):self.mono_value=mono;self.wall_value=wall
 def monotonic(self):return self.mono_value
 def time(self):return self.wall_value
 def elapse(self,seconds):self.mono_value+=seconds;self.wall_value+=seconds

class PhaseLifecycle123:
 __slots__=('__transport','__macro','__clock','__parent_mono','__parent_wall','__active','__closed','__failed','__last','__root')
 def __init__(self,transport,macro):
  self.__transport=transport;self.__macro=macro;self.__clock=time
  if macro.snapshot()['scope']=='SYNTHETIC_SOURCE_ONLY':
   candidate=getattr(transport,'synthetic_clock123',None)
   if type(candidate) is SyntheticClock123:self.__clock=candidate
  elif hasattr(transport,'synthetic_clock123'):raise ValueError('Synthetic clock cannot cross runtime boundary')
  self.__parent_mono=transport.parent_mono;self.__parent_wall=transport.config['deadline_utc_ms']/1000;self.__active=None;self.__closed=[];self.__failed=None;self.__last=None;self.__root=transport.root
 def parent_remaining(self):
  if self.__transport.parent_mono!=self.__parent_mono or self.__transport.config['deadline_utc_ms']/1000!=self.__parent_wall:raise HostUnknown('Original parent cannot reset')
  return min(self.__parent_mono-self.__clock.monotonic(),self.__parent_wall-self.__clock.time())
 def begin(self,phase):
  if type(phase) is not MacroPhase122 or self.__failed is not None or self.__active is not None:raise HostUnknown('Unfinished/UNKNOWN phase cannot be rescued or rebound')
  first,last,seconds,reserve=phase.value;snapshot=self.__macro.snapshot()
  if snapshot['cursor']!=first or snapshot['first_unknown'] is not None:raise HostUnknown('Exact next actual cursor and UNKNOWNnone')
  names=[p['phase'] for p in self.__closed];allowed=[] if not names else names
  expected='ADMIT' if not names and first==1 else 'PRE_DISPATCH' if not names else {'PRE_DISPATCH':'ADMIT','ADMIT':'ENCRYPTED','RECIPIENT_PREP':'ENCRYPTED','ENCRYPTED':'CONSUMED','CONSUMED':'TERMINAL'}.get(names[-1])
  if phase.name!=expected:raise HostUnknown('Finite phase order, no restart/refund')
  for closure in self.__closed:
   if strict((self.__root/closure['file']).read_bytes())!=closure['record']:raise HostUnknown('Timely previous closure replaced')
  if self.parent_remaining()<=0 or seconds and self.parent_remaining()<seconds+reserve:raise HostUnknown('Insufficient ORIGINAL parent/epoch remaining')
  if phase is MacroPhase122.TERMINAL:
   # SAFE/consumerstop/cleanup evidence is a separate source-bound observation,
   # never the caller saying True. This implementation cannot grant that gate.
   observation=getattr(self.__transport,'_controller_safe123',None)
   if snapshot['scope']=='SYNTHETIC_SOURCE_ONLY':
    if type(observation) is not ControllerSafeObservation123 or not observation.accepts(self.__transport,self.__macro):raise HostUnknown('Exact inert type only')
   else:
    _REQUIRE_TERMINAL126(self.__transport,self.__macro)
  now=self.__clock.monotonic();wall=self.__clock.time();end=min(self.__parent_mono,now+seconds) if seconds else self.__parent_mono;wallend=min(self.__parent_wall,wall+seconds) if seconds else self.__parent_wall
  self.__active={'phase':phase.name,'first':first,'last':last,'begin_mono':now,'begin_wall':wall,'end_mono':end,'end_wall':wallend,'parent_mono':self.__parent_mono,'parent_wall':self.__parent_wall};self.__last=None
  self.__transport.bind_phase(end)
  put(self.__root/('phase123-'+phase.name+'-begin.json'),can(self.__active))
 def begin_recipient(self):
  if self.__active is not None or self.__failed or not self.__closed or self.__closed[-1]['phase']!='ADMIT' or self.__macro.snapshot()['cursor']!=6 or self.__macro.snapshot()['first_unknown'] is not None:raise HostUnknown('Only completed timelyADMIT before recipient phase')
  if self.parent_remaining()<610:raise HostUnknown('Original hostbegin610 / recipient60 / reserve550')
  for closure in self.__closed:
   if strict((self.__root/closure['file']).read_bytes())!=closure['record']:raise HostUnknown('Previous timelyclosure changed')
  now=self.__clock.monotonic();wall=self.__clock.time();self.__active={'phase':'RECIPIENT_PREP','first':6,'last':6,'begin_mono':now,'begin_wall':wall,'end_mono':now+60,'end_wall':wall+60,'parent_mono':self.__parent_mono,'parent_wall':self.__parent_wall};self.__last=None;self.__transport.bind_phase(now+60);put(self.__root/'phase123-RECIPIENT_PREP-begin.json',can(self.__active))
 def mark_validated_original(self):
  if self.__active is None or self.__failed:raise HostUnknown('No open reviewed phase')
  now=self.__clock.monotonic();wall=self.__clock.time()
  if now>=self.__active['end_mono'] or wall>=self.__active['end_wall'] or self.parent_remaining()<=0:self.fail('Original/validation late in its OWN phase')
  self.__last={'mono':now,'wall':wall,'cursor':self.__macro.snapshot()['cursor']}
 def close(self):
  if self.__active is None or self.__last is None or self.__failed:raise HostUnknown('No timely completed original to close')
  a=self.__active;s=self.__macro.snapshot();now=self.__clock.monotonic();wall=self.__clock.time()
  if s['cursor']!=a['last'] or s['first_unknown'] is not None or self.__last['cursor']!=a['last'] or now>=a['end_mono'] or wall>=a['end_wall'] or self.parent_remaining()<=0:self.fail('Incomplete/late phase closure')
  record={'phase':a['phase'],'cursor':s['cursor'],'closed_mono':now,'closed_wall':wall,'last_validated_original':self.__last,'original_end_mono':a['end_mono'],'original_end_wall':a['end_wall'],'parent_mono':self.__parent_mono,'parent_wall':self.__parent_wall,'macro_sha256':s['macro_sha256'],'scope':s['scope'],'native_authority':False};name='phase123-'+a['phase']+'-CLOSED.json';put(self.__root/name,can(record));self.__closed.append({'phase':a['phase'],'file':name,'record':record});self.__active=None;self.__last=None;return copy.deepcopy(record)
 def fail(self,reason):
  if self.__failed is None:self.__failed=reason;put(self.__root/'phase123-FIRST_UNKNOWN.json',can({'reason':reason,'active':self.__active,'parent_mono':self.__parent_mono,'parent_wall':self.__parent_wall}))
  raise HostUnknown(self.__failed)
 def snapshot(self):return {'closed':[p['phase'] for p in self.__closed],'active':copy.deepcopy(self.__active),'first_unknown':self.__failed,'parent_mono':self.__parent_mono,'parent_wall':self.__parent_wall}

_CONTROLLER_SAFE_SEAL123=object()
class ControllerSafeObservation123:
 """No serialized boolean/SAFE dictionary allocates this observation.

 Runtime minting awaits independently admitted actual SAFE-return binding; the
 administrative123 holder does not mint it or consume any protectedproof clock.
 """
 __slots__=('__transport','__macro','__scope','__original')
 def __init__(self,seal,transport,macro,original):
  if seal is not _CONTROLLER_SAFE_SEAL123 or macro.snapshot()['scope']!='SYNTHETIC_SOURCE_ONLY':raise ValueError('Runtime SAFE binding not exposed/admitted123')
  if original!={'SAFE':'YES','consumer':'STOPPED','cleanup':'COMPLETE','T':None,'scope':'SYNTHETIC_SOURCE_ONLY'}:raise ValueError('Exact inert SAFE projection')
  self.__transport=transport;self.__macro=macro;self.__scope='SYNTHETIC_SOURCE_ONLY';self.__original=copy.deepcopy(original)
 def accepts(self,transport,macro):return self.__transport is transport and self.__macro is macro and macro.snapshot()['scope']==self.__scope

def advance_macro_phase122(transport,phase):
 """Actual finite driver, parent admission and timely closure are distinct.

 A CLOSED timely phase may expire while a separately bound stage proceeds;
 an unfinished/late/UNKNOWN phase is never rescued by spare parent time.
 """
 if type(phase) is not MacroPhase122:raise ValueError('Fixed typed phase only')
 bound=_bound_macro122(transport)
 if bound is None:raise ValueError('No sealed reviewed plan')
 macro=bound[0];lifecycle=getattr(transport,'_phase_lifecycle123',None)
 if lifecycle is None:lifecycle=PhaseLifecycle123(transport,macro);transport._phase_lifecycle123=lifecycle
 if type(lifecycle) is not PhaseLifecycle123:raise ValueError('No caller boolean/dict phase provenance')
 lifecycle.begin(phase)
 try:
  first,last,_,_=phase.value
  for ordinal in range(first,last):
   pending=macro.prepare(MacroStep122(ordinal));transport.cas_checkpoint(transport.current_checkpoint_version,pending['payload'])
   lifecycle.mark_validated_original()
   if pending['tool'] is not None:transport.call(pending['tool'],pending['args']);lifecycle.mark_validated_original()
   transport.deadline()
  lifecycle.close()
 except BaseException as exc:
  try:lifecycle.fail(type(exc).__name__)
  finally:macro.unknown(type(exc).__name__)
 return macro.snapshot()


def bind_current_macro_run122(transport):
 bound=_bound_macro122(transport)
 if bound is None:raise ValueError('No reviewed macro')
 actual=transport.get('actions/runs/'+str(transport.config['run_id']))
 bound[0].bind_run_original(can(actual),_PRECEDING_NATIVE122)

def prepare_macro_delivery122(transport,files,private_out):
 # Fixed existing ingress source, no caller-selected import/callback/pin set.
 # This future private operation requires a separate CURRENT custody release.
 current=current_binding(transport._checkpoint,transport.current_checkpoint_version,transport.config)
 if current['direction'].get('private_macro122_custody_admission') is not True or 'ADMIT_CURRENT_ENCRYPTED_INPUT_CUSTODY' not in current['direction']['body']:raise ValueError('No current protected custody authority;122 performs none')
 bound=_bound_macro122(transport)
 if bound is None:raise ValueError('No reviewed macro')
 repo=pathlib.Path(__file__).resolve().parents[1];m=strict((repo/'diagnostic108/manifest.json').read_bytes());source=repo/'offline103/ingress.py';transfer=repo/'offline103/transfer.json'
 if sha(source.read_bytes())!=m['source_files']['offline103/ingress.py']['sha256'] or sha(transfer.read_bytes())!=m['canonical_transfer_sha256']:raise ValueError('Exact existing reviewed ingress and input contract')
 cfg=strict(transfer.read_bytes());pins=cfg['private_members']
 import importlib.util,zipfile,io
 spec=importlib.util.spec_from_file_location('trace122_fixed_ingress',source);ingress=importlib.util.module_from_spec(spec);spec.loader.exec_module(ingress)
 lifecycle=getattr(transport,'_phase_lifecycle123',None)
 if type(lifecycle) is not PhaseLifecycle123:raise ValueError('Actual timelyclosed ADMIT lifecycle required')
 lifecycle.begin_recipient()
 end=min(transport.phase_mono,transport.parent_mono);run=transport.get('actions/runs/'+str(transport.config['run_id']));actual=transport.authenticated_artifact_zip(run['id'],'traceharbor-recipient104-'+str(run['id'])+'-1',end,8192)
 with zipfile.ZipFile(io.BytesIO(actual['zip_bytes'])) as archive:public=strict(archive.read('recipient-public.json'))
 trace=[]
 try:plan=ingress.prepare_from_artifact(public,run,actual['artifact'],actual['zip_sha256'],files,pins,pathlib.Path(private_out),transport.config['source_tree'],trace)
 finally:put(transport.root/'macro122-ingress-original.json',can({'trace':trace,'source_sha256':sha(source.read_bytes()),'native_authority':False}))
 if sha(source.read_bytes())!=m['source_files']['offline103/ingress.py']['sha256']:raise HostUnknown('Ingress source changed; no next step')
 bound[0].bind_delivery_original(can({'context':plan['context'],'ciphertext_base64':plan['operations'][0]['body']['content'],'ciphertext_sha256':plan['ciphertext_sha256'],'artifact_digest':actual['zip_sha256'],'artifact_bytes':len(actual['zip_bytes']),'retention_days':1,'custody_sha256':sha(can({'pins':pins,'context':plan['context'],'artifact':actual['receipt']}))}),_PRECEDING_NATIVE122)
 lifecycle.mark_validated_original();lifecycle.close()


def main():
 if len(sys.argv)!=3 or sys.argv[1]!='--qualify-publish-intent':raise ValueError('Only current necessary publication qualification')
 cfg=strict(pathlib.Path(sys.argv[2]).read_bytes());ledger=FrameLedger(cfg['output'],cfg['context'],cfg['deadline_utc_ms']);bridge=StdioBridge(ledger)
 try:
  fd0=os.fstat(0)
  startup={'schema':'TRACE_HOST_STARTUP','argv':sys.argv,'source_sha256':sha(pathlib.Path(__file__).read_bytes()),'config_sha256':sha(pathlib.Path(sys.argv[2]).read_bytes()),'isatty0':os.isatty(0),'isolated':sys.flags.isolated,'dont_write_bytecode':sys.flags.dont_write_bytecode,'fd0_dev':fd0.st_dev,'fd0_ino':fd0.st_ino,'fd0_mode':fd0.st_mode,'blocking0':os.get_blocking(0),'native_authority':False}
  put(ledger.root/'startup.original.json',can(startup))
  if startup['isatty0'] is not True or not stat.S_ISCHR(fd0.st_mode):raise HostUnknown('Explicit actual livePTY required BEFORE writer preparation')
  transport=HostTransport(bridge,ledger.root,cfg);transport.bind_phase(min(transport.parent_mono,ledger.parent_mono,time.monotonic()+cfg['phase_s']))
  payload=strict(pathlib.Path(cfg['payload_path']).read_bytes())
  if sha(can(payload))!=cfg['payload_sha256']:raise ValueError('Preplanned exact necessary intent')
  receipt=transport.cas_checkpoint(cfg['current_version'],payload)
  proof={'schema':'TRACE120_GENUINE_NECESSARY_PUBLISH_INTENT','holder_pid':os.getpid(),'context':cfg['context'],'seq':ledger.seq,'receipt':receipt,'transport_counts':transport.counts,'native_authority':False,'result':'PASS'}
  put(ledger.root/'genuine-proof.json',can(proof));print(can({'schema':'TRACE120_HOLDER_TERMINAL','result':'PASS','exit_code':0,'proof_sha256':sha(can(proof))}).decode());return 0
 except BaseException as exc:
  ledger.failed=True;put(ledger.root/'genuine-error.json',can({'exception_class':type(exc).__name__,'message':str(exc),'status':'UNKNOWN_NO_RETRY'}));print(can({'schema':'TRACE120_HOLDER_TERMINAL','result':'UNKNOWN','exit_code':1}).decode());return 1
# Native126 entry is fixed provider bootstrap, not the ADMIN118 CLI.

# Native126 provider-original port; inactive until a NEW actual source release.
import importlib.util as _iu126,types as _types126
_provider126=sys.modules.get('trace126_fixed_provider')
if _provider126 is None or pathlib.Path(_provider126.__file__).resolve()!=pathlib.Path(__file__).with_name('provider_safe126.py').resolve():raise TypeError('Native host must be loaded by fixed provider bootstrap')
# Capture the exact loaded source factory function ONCE, never an attribute on
# transport or a caller-supplied API/getter. No arbitrary importpath parameter.
_REQUIRE_TERMINAL126=_provider126.require_native_terminal126
class NativeHostTransport126(HostTransport):
 def initialize_provider126(self,manifest):
  current=current_binding(self._checkpoint,self.current_checkpoint_version,self.config)
  raw=pathlib.Path(__file__).with_name('provider_safe126.py').read_bytes();pin=manifest['source_files']['diagnostic108/provider_safe126.py']
  if len(raw)!=pin['bytes'] or sha(raw)!=pin['sha256']:raise ValueError('Actual owned fixedprovider sourcepin')
  if self not in _provider126._HOSTS or _provider126._HOSTS[self]['class'] is not NativeHostTransport126:raise TypeError('Only internal fixed-loader factory registration')
  self.budget126=_provider126.ctl.InclusiveBudget126(48)
  self.canonical126=_provider126.ctl.CanonicalOriginals126(self.root,self.config['context'],self.budget126,_provider126.ctl.DiskOriginalIO126())
 def provider_original126(self,op,args):
  if op not in ('github_fetch','github_fetch_workflow_run_jobs','github_fetch_workflow_run_artifacts','github_download_workflow_artifact','library_materialize'):raise ValueError('Closed existingprovider primitives only')
  self.deadline();seq=self.bridge.ledger.seq+1;callid='provider126-'+str(seq)
  self.budget126.reserve('native',callid)
  # SAME exact StdioBridge persists actual raw original before its postguards.
  if type(self.bridge) is not StdioBridge:raise TypeError('No supplied callback as native original')
  self.bridge(op,args)
  frame=strict((self.root/(str(seq)+'.return.original.json')).read_bytes());request=strict((self.root/(str(seq)+'.request.original.json')).read_bytes())
  if frame['request_digest']!=request['request_digest'] or request['op']!=op or request['args']!=args:raise HostUnknown('Exact actual original call identity')
  identity={'context_sha256':sha(can(self.config['context'])),'operation':op,'seq':seq,'tool':op,'call_id':request['request_digest']}
  canonical=self.canonical126.save(identity,frame['original_result']);packet=_provider126.retain_native126(self,identity,frame['original_result'],canonical);self.deadline();return packet
 def prepare_safe_destination126(self,plan):
  layout=validate_transfer_layout(self.config['writer_binding'],self.root);destination=layout['transfer']/('safe-artifact-'+str(plan['run_id'])+'-1');destination.mkdir(mode=0o700,exist_ok=False);s=destination.lstat();self._safe_destination126=(destination,s.st_dev,s.st_ino,s.st_uid);return destination
 def provider_artifact_bytes126(self,ref,transfer,artifact,plan):
  destination,dev,ino,uid=self._safe_destination126;layout=validate_transfer_layout(self.config['writer_binding'],self.root);s=destination.lstat()
  if destination.is_symlink() or (s.st_dev,s.st_ino,s.st_uid)!=(dev,ino,uid) or not destination.is_relative_to(layout['transfer']):raise HostUnknown('Exact actual selected disjoint transfer directory')
  path=pathlib.Path(transfer.get('workspace_path',''))
  if path!=destination/ref['file_name'] or path.is_symlink() or path.resolve()!=path:raise HostUnknown('Pinned selected actual basename/path only')
  before=path.lstat()
  if not stat.S_ISREG(before.st_mode) or before.st_uid!=os.getuid() or before.st_nlink!=1 or before.st_size>65536:raise HostUnknown('Selected bounded owned regular file')
  self.apply_attrs(path,transfer)
  fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK);parts=[];count=0
  try:
   opened=os.fstat(fd)
   if (opened.st_dev,opened.st_ino)!=(before.st_dev,before.st_ino):raise HostUnknown('Artifact changed beforeopen')
   while count<=65536:
    chunk=os.read(fd,min(4096,65537-count))
    if not chunk:break
    parts.append(chunk);count+=len(chunk)
   after=os.fstat(fd)
  finally:os.close(fd)
  end=path.lstat();raw=b''.join(parts)
  if count>65536 or count!=before.st_size or (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns) or (end.st_dev,end.st_ino)!=(after.st_dev,after.st_ino):raise HostUnknown('Complete unchanged artifact EOF')
  if os.getxattr(path,'user.library-file-id').decode()!=transfer['library_file_id']:raise HostUnknown('Actual Libraryidentity')
  for x in transfer['xattrs']:
   if os.getxattr(path,x['name']).decode()!=x['value']:raise HostUnknown('ALL actual returned attrs')
  self.deadline();return raw
