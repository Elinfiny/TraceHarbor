"""Source-pinned solewriter host IPC adapter118, distinct from runner authority.

Import is inert. The code-mode bridge invokes actual enabled tools. This holder
accepts planned data/original returns only; no eval, arbitrary command, PAT,
cookie, HTTP or native capability transfer. Read-only qualification never CASes.
"""
import os,sys,pathlib,json,hashlib,time,subprocess,copy,zipfile,io,stat,re,base64,selectors,termios
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
def current_binding(base,version,config,require_plan=False,payload=None):
 doc,raw=check_checkpoint(base,OWN,version)
 match=re.fullmatch(r'NATIVE([1-9][0-9]{0,3})_([A-Z_]+)',doc['state'])
 if match is None or match[2]=='TERMINAL':raise ValueError('No mutation of sealed historical direction')
 number=int(match[1]);key='native'+str(number);n=doc[key];direction=n['direction']
 if type(config.get('direction_number')) is not int or config['direction_number']!=number or not direction['id'].startswith('V28-TRACEHARBOR-'+str(number)+'-') or len(direction['body'].encode())!=direction['bytes'] or sha(direction['body'].encode())!=direction['sha256']:raise ValueError('Exact strict current direction/body pin')
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
  if n['records'][-1]['phase']!='PUBLISH_INTENT' or n['records'][-1]['payload'].get('phase')!='SOURCE_FREEZE':raise ValueError('Current durable exact prepared operation required')
  plan=n['records'][-1]['payload']['prepared_operation']
  if config.get('prepared_operation')!=plan or plan['expected_current_version']!=version or plan['phase']!='PUBLISH_INTENT' or sha(can(payload))!=plan['payload_sha256'] or payload.get('source_sha')!=plan['source_sha'] or config['source_sha']!=plan['source_sha'] or config['host_source_sha256']!=plan['host_source_sha256'] or config['deadline_utc_ms']!=plan['deadline_utc_ms'] or config['context']!=plan['context'] or plan['direction_id']!=direction['id'] or plan['writer_sha256']!=binding['writer_sha256']:raise ValueError('Exact current phase/plan/payload/source/clock/version/path provenance before effect')
  if type(plan['phase_s']) is not int or not 0<plan['phase_s']<=plan['maximum_phase_s'] or config['phase_s']!=plan['phase_s']:raise ValueError('Immutable bounded planned phase')
 return {'number':number,'key':key,'binding':binding,'direction':direction,'original':original,'writer':writer,'doc':doc,'raw':raw}
def validate_writer_output(base,target,version,payload,receipt,config):
 binding=current_binding(base,version,config,require_plan=True,payload=payload);a=binding['doc'];raw=pathlib.Path(target).read_bytes();c=strict(raw);key=binding['key'];b=binding['binding']
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
  current=current_binding(self._checkpoint,expected_version,self.config,require_plan=True,payload=payload);original_writer=current['original'];writer_path=current['writer'];namespace=current['key']
  original=strict(self._checkpoint.read_bytes())
  if any(r.get('phase')=='PUBLISH_INTENT' and r.get('payload')==payload for r in original[namespace]['records']):raise HostUnknown('Existing exact attempt consumed; no retry')
  if payload.get('source_sha')!=self.source:raise ValueError('Current source-bound payload')
  if payload.get('phase')=='PUBLISH_INTENT':
   if sha(can(payload))!=self.config['prepared_operation']['payload_sha256']:raise ValueError('Preplanned current publication payload')
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
  candidate=validate_writer_output(self._checkpoint,target,expected_version,payload,writer,self.config)
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
  receipt=dict(pub,private_candidate_path=str(target),upload_copy_path=str(upload),sha256=writer['raw_sha256'],self_sha256=writer['self_sha256']);return self.pinned_checkpoint_readback(receipt)
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
if __name__=='__main__':sys.exit(main())
