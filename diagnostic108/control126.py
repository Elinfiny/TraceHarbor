"""Private126 complete inclusive planning and canonical original custody.
No native operation is executed on import. Synthetic IO is a separate realm.
"""
import hashlib,json,os,pathlib,stat,time
def can(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
class InclusiveBudget126:
 def __init__(self,limit=48):
  if type(limit) is not int or not 0<limit<=48:raise ValueError('Prospective inclusive cap48, never retroactive125raise')
  self.limit=limit;self.reserved=[];self.first_unknown=None
 def reserve(self,kind,identity):
  if kind not in ('native','local_evidence','wait') or self.first_unknown is not None:raise RuntimeError('Closed call category/firstUNKNOWN')
  if len(self.reserved)>=self.limit:raise RuntimeError('Inclusive cap before call; no effect')
  if any(r['identity']==identity for r in self.reserved):raise RuntimeError('No native call identity reuse/retry')
  token={'ordinal':len(self.reserved)+1,'kind':kind,'identity':identity};self.reserved.append(token);return token
 def unknown(self,reason):
  if self.first_unknown is None:self.first_unknown=reason
 def plan(self,counts):
  if any(type(v) is not int or v<0 for v in counts.values()):raise ValueError('Whole explicit finitecounts')
  total=sum(counts.values());return {'inclusive_limit':self.limit,'counts':counts,'total':total,'fit':total<=self.limit,'authority':False}
class DiskOriginalIO126:
 realm='ACTUAL_PRIVATE_FILE_IO_NOT_NATIVE_AUTHORITY'
 def write_once(self,path,raw):
  fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
  try:
   with os.fdopen(fd,'wb',closefd=False) as f:
    f.write(raw);f.flush();os.fsync(fd)
  finally:os.close(fd)
 def read(self,path):
  p=pathlib.Path(path);s=p.lstat()
  if p.is_symlink() or p.resolve()!=p or not stat.S_ISREG(s.st_mode) or s.st_uid!=os.getuid() or s.st_mode&0o077 or s.st_nlink!=1 or s.st_size>1048576:raise ValueError('Canonical owned nonlinked bounded original')
  fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
  try:
   chunks=[];count=0
   while count<=1048576:
    b=os.read(fd,min(4096,1048577-count))
    if not b:break
    chunks.append(b);count+=len(b)
   end=os.fstat(fd)
  finally:os.close(fd)
  if (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)!=(end.st_dev,end.st_ino,end.st_size,end.st_mtime_ns):raise ValueError('Canonical original changed')
  raw=b''.join(chunks)
  if len(raw)!=s.st_size:raise ValueError('Original complete EOF')
  return raw
class CanonicalOriginals126:
 def __init__(self,root,context,budget,io):self.root=pathlib.Path(root);self.context=context;self.budget=budget;self.io=io;self.records={}
 def save(self,identity,value):
  # Equal bytes from DIFFERENT actual calls are never merged.
  if set(identity)!={'context_sha256','operation','seq','tool','call_id'} or identity['context_sha256']!=sha(can(self.context)) or type(identity['seq']) is not int or identity['seq']<=0:raise ValueError('Complete predeclared source/context/op/seq/tool/call identity')
  key=sha(can(identity));raw=can({'identity':identity,'original':value});old=self.records.get(key)
  if old is not None:
   try:actual=self.io.read(old['path'])
   except BaseException as e:self.budget.unknown('Canonical original lost '+type(e).__name__);raise
   if actual!=raw or len(actual)!=old['bytes'] or sha(actual)!=old['sha256']:self.budget.unknown('Canonical identity/content collision');raise RuntimeError('No memory-only alias/different original')
   return dict(old,alias=True)
  path=str(self.root/(key+'.original.json'));self.budget.reserve('local_evidence','capture:'+key)
  try:self.io.write_once(path,raw)
  except BaseException as e:self.budget.unknown('Original persistence '+type(e).__name__);raise
  actual=self.io.read(path)
  if actual!=raw:self.budget.unknown('Original readback mismatch');raise RuntimeError('No durable original')
  record={'identity':dict(identity),'path':path,'bytes':len(raw),'sha256':sha(raw),'alias':False};self.records[key]=record;return dict(record)
 def reference(self,identity):
  key=sha(can(identity));record=self.records.get(key)
  if record is None or record['identity']!=identity:raise RuntimeError('No canonical original captured')
  try:raw=self.io.read(record['path'])
  except BaseException as e:self.budget.unknown('Canonical original lost '+type(e).__name__);raise
  if len(raw)!=record['bytes'] or sha(raw)!=record['sha256']:self.budget.unknown('Canonical original lost/changed');raise RuntimeError('Canonical original lost/changed')
  return dict(record,alias=True)
_PHASE_SEAL126=object()
class PostIOClosure126:
 __slots__=('owner','name','facts','raw_sha256','post_mono','post_utc','error','timely','seal')
 def __init__(self,key,owner,name,facts,raw,post_mono,post_utc,error):
  if key is not _PHASE_SEAL126:raise TypeError('Actual invocation closure only')
  self.owner=owner;self.name=name;self.facts=facts;self.raw_sha256=sha(raw);self.post_mono=post_mono;self.post_utc=post_utc;self.error=error;self.seal=key
  self.timely=error is None and post_mono<facts['end_mono'] and post_utc<min(facts['end_utc'],owner.parent_utc)
class SafePhases126:
 def __init__(self,clock,root,binding,main_end,io,realm='SYNTHETIC_SOURCE_ONLY'):
  if realm!='SYNTHETIC_SOURCE_ONLY' and (type(io) is not DiskOriginalIO126 or clock.wall is not time.time or clock.mono is not time.monotonic):raise TypeError('Real clocks/IO cannot be injected')
  self.clock=clock;self.root=pathlib.Path(root);self.binding=binding;self.main_end=main_end;self.io=io;self.realm=realm;self.parent_mono=clock.end_mono;self.parent_utc=clock.end_utc;self.phases={};self.closures={};self.first_unknown=None;self.originals={}
 def unknown(self,reason):
  if self.first_unknown is None:self.first_unknown=reason
 def begin(self,name):
  if name not in ('cleanup','proof') or name in self.phases:raise ValueError('Fixed once cleanup10/proof15')
  if name=='proof' and not self.accepts('cleanup'):raise RuntimeError('Actual timely cleanup closure required')
  mono=self.clock.mono();wall=self.clock.wall();seconds=10 if name=='cleanup' else 15
  self.phases[name]={'phase':name,'binding_sha256':sha(can(self.binding)),'begin_mono':mono,'begin_utc':wall,'end_mono':min(mono+seconds,self.main_end,self.parent_mono),'end_utc':min(wall+seconds,self.parent_utc,wall+max(0,self.main_end-mono)),'parent_mono':self.parent_mono,'parent_utc':self.parent_utc,'seconds_cap':seconds,'status':'PROVISIONAL_FACTS_NOT_CLOSED_PASS'}
  if mono>=self.phases[name]['end_mono'] or wall>=self.phases[name]['end_utc']:self.unknown('Expired original '+name)
 def active_proof(self,producer=None):
  p=self.phases.get('proof');return self.first_unknown is None and p is not None and 'proof' not in self.closures and self.clock.mono()<p['end_mono'] and self.clock.wall()<p['end_utc'] and self.accepts('cleanup')
 def close(self,name,original):
  if name not in self.phases or name in self.closures:raise RuntimeError('At most ONE actual receiptwrite attempt')
  facts=dict(self.phases[name],original=original,original_bytes=len(can(original)),original_sha256=sha(can(original)));raw=can(facts)
  if len(raw)>65536:self.unknown('Receipt original exceeds finitecap');raise ValueError('Bounded phase facts')
  # Retain the actual original before IO and BEFORE any conversion/guard.
  self.originals[name]={'facts':facts,'raw':raw,'write_error':None}
  path=self.root/('safe126-'+name+'-provisional.original.json');error=None
  # Mark attempted BEFORE opening; errors never permit a secondwrite/unlink.
  self.closures[name]=None
  try:
   self.io.write_once(str(path),raw)
   observed=self.io.read(str(path))
   if observed!=raw:raise ValueError('Complete actual provisionalreceipt readback changed')
  except BaseException as e:error={'exception_class':type(e).__name__,'message':str(e)};self.originals[name]['write_error']=error
  # Both observations occur AFTER LAST write/flush/fsync/close returned or threw.
  post_mono=self.clock.mono();post_utc=self.clock.wall();closure=PostIOClosure126(_PHASE_SEAL126,self,name,facts,raw,post_mono,post_utc,error);self.closures[name]=closure
  if not closure.timely:self.unknown('Receipt POST_IO '+name+' '+('error' if error else 'late'))
  return closure.timely and self.first_unknown is None
 def accepts(self,name=None):
  if self.first_unknown is not None or self.parent_mono!=self.clock.end_mono or self.parent_utc!=self.clock.end_utc or self.clock.mono()>=self.parent_mono or self.clock.wall()>=self.parent_utc:return False
  names=[name] if name else ['cleanup','proof']
  for n in names:
   c=self.closures.get(n)
   if type(c) is not PostIOClosure126 or c.seal is not _PHASE_SEAL126 or c.owner is not self or not c.timely or c.error is not None:return False
   try:raw=self.io.read(str(self.root/('safe126-'+n+'-provisional.original.json')))
   except BaseException as e:
    self.originals['receipt-read-fault']={'phase':n,'exception_class':type(e).__name__};self.unknown('Actual receipt read/close failure');return False
   if raw!=can(c.facts) or sha(raw)!=c.raw_sha256 or c.post_mono>=c.facts['end_mono'] or c.post_utc>=c.facts['end_utc']:return False
  return self.clock.mono()<self.parent_mono and self.clock.wall()<self.parent_utc
 def redacted(self):
  if not self.accepts():raise RuntimeError('No SAFE release from JSON/provisional/preIO/late facts')
  return {n:{'facts_sha256':c.raw_sha256,'begin_mono':c.facts['begin_mono'],'end_mono':c.facts['end_mono'],'begin_utc':c.facts['begin_utc'],'end_utc':c.facts['end_utc'],'post_io_mono':c.post_mono,'post_io_utc':c.post_utc,'seconds_cap':c.facts['seconds_cap']} for n,c in self.closures.items()}
