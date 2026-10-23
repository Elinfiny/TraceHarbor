"""SOURCE173 candidate bounded canonical hashing and one-invocation whole FD.
No native registry, capability, cached authorization or caller-provided snapshot.
Every completion re-reads the SAME FD, EOF, full raw hash and ALL attributes.
"""
import os,stat,pathlib,json,hashlib
def canonical_sha173(value):
 """Exact compact sorted UTF8 JSON, buffered SHA input <=65536 bytes.
 Only parser-native builtin values are consumed; no caller callbacks, proof
 cache or whole canonical output buffer. Shared noncyclic values serialize
 each occurrence; an active-container cycle is refused, never cached.
 """
 h=hashlib.sha256();buffer=bytearray();active=set();limit=65536;update=h.update
 def emit(raw):
  if len(raw)>=limit:
   if buffer:update(buffer);buffer.clear()
   for offset in range(0,len(raw),limit):update(raw[offset:offset+limit])
  else:
   if len(buffer)+len(raw)>limit:update(buffer);buffer.clear()
   buffer.extend(raw)
 def string(text):
  # C escaping on bounded character chunks; UTF8 encoding preserves stdlib
  # surrogate errors and exact nonASCII/control/quote/backslash semantics.
  if len(text)<=65536:emit(json.encoder.encode_basestring(text).encode('utf-8'));return
  emit(b'"')
  for offset in range(0,len(text),65536):emit(json.encoder.encode_basestring(text[offset:offset+65536])[1:-1].encode('utf-8'))
  emit(b'"')
 def bounded_container(v):
  # A conservative encoded-byte upper bound. No full canonical document is
  # built: C encoder receives only exact builtin subtrees proven <=32768B.
  # Visits stop on the first exhausted budget; fallback retains streaming.
  remaining=32768;seen=set()
  def fits(x):
   nonlocal remaining
   kind=type(x)
   if kind is str:remaining-=6*len(x)+2
   elif kind in(dict,list,tuple):
    identity=id(x)
    if identity in seen or identity in active:raise ValueError('Circular reference detected')
    remaining-=2+2*len(x)
    if remaining<0:return False
    seen.add(identity)
    try:
     if kind is dict:
      for k,y in x.items():
       if type(k)is not str:raise TypeError('JSON document keys must be strings')
       if not fits(k)or not fits(y):return False
     else:
      for y in x:
       if not fits(y):return False
    finally:seen.remove(identity)
   elif x is None or kind is bool:remaining-=5
   elif kind is int:remaining-=max(1,x.bit_length())+2
   elif kind is float:
    if not __import__('math').isfinite(x):raise ValueError('Out of range float values are not JSON compliant')
    remaining-=32
   else:raise TypeError('Only immutable-parser builtin JSON values')
   return remaining>=0
  return fits(v)
 def feed(v):
  kind=type(v)
  if kind in(dict,list,tuple)and bounded_container(v):
   encoded=json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf-8')
   if len(encoded)>32768:raise ValueError('Conservative C subtree output bound')
   emit(encoded);return
  if kind is str:string(v)
  elif kind is dict:
   keys=list(v)
   if any(type(k)is not str for k in keys):raise TypeError('JSON document keys must be strings')
   identity=id(v)
   if identity in active:raise ValueError('Circular reference detected')
   active.add(identity)
   try:
    emit(b'{')
    for i,k in enumerate(sorted(keys)):
     if i:emit(b',')
     string(k);emit(b':');feed(v[k])
    emit(b'}')
   finally:active.remove(identity)
  elif kind in(list,tuple):
   identity=id(v)
   if identity in active:raise ValueError('Circular reference detected')
   active.add(identity)
   try:
    emit(b'[')
    for i,x in enumerate(v):
     if i:emit(b',')
     feed(x)
    emit(b']')
   finally:active.remove(identity)
  elif v is None:emit(b'null')
  elif kind is bool:emit(b'true'if v else b'false')
  elif kind is int:emit(str(v).encode('ascii'))
  elif kind is float:
   if not __import__('math').isfinite(v):raise ValueError('Out of range float values are not JSON compliant')
   emit(float.__repr__(v).encode('ascii'))
  else:raise TypeError('Only immutable-parser builtin JSON values')
 feed(value)
 if buffer:update(buffer)
 return h.hexdigest()
def self_sha173(doc,stable):
 v=dict(doc)
 if stable=='libfile_f87a6a307f70819194e0af0fa453afd1':v['integrity']=dict(v['integrity']);v['integrity']['canonical_json_sha256']=None
 else:v['self_sha256']=None
 return canonical_sha173(v)
def _identity173(s):return (s.st_dev,s.st_ino,s.st_uid,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_gid)
def _dir_identity175(s):return (s.st_dev,s.st_ino,s.st_uid,s.st_gid,s.st_mode)
def _attrs175(fd):return {k:os.getxattr(fd,k)for k in os.listxattr(fd)}
def _directory_policy175(path,s,anchor_uid):
 mode=stat.S_IMODE(s.st_mode)
 if not stat.S_ISDIR(s.st_mode)or s.st_uid not in (os.getuid(),anchor_uid):raise ValueError('Owned or anchor-owned directory required')
 if path=='/':
  if mode&0o022:raise ValueError('Trusted root is not writable by group/other')
  return 'TRUSTED_ROOT_FD'
 if path=='/tmp'and s.st_uid==anchor_uid and mode==0o1777:return 'TRUSTED_STICKY_SHARED_TMP_FD'
 # This host explicitly supplies /workspace mode0777, owned by the root
 # anchor. It is a shared runtime mount, not the private custody boundary.
 # Every descendant link and its FD stays sealed; a following owned safe
 # directory is mandatory before opening a leaf. No generic writable waive.
 if path=='/workspace'and s.st_uid==anchor_uid and mode==0o777:return 'QUALIFIED_RUNTIME_SHARED_WORKSPACE_FD'
 if mode&0o022:raise ValueError('Unsafe private ancestor group/other write')
 return 'OWNED_SAFE_PRIVATE_BOUNDARY'if s.st_uid==os.getuid()else'ANCHOR_OWNED_SAFE_SYSTEM_DIRECTORY'
class Whole173:
 """One physical invocation; FD-sealed directory chain and final leaf.
 No consumer-supplied snapshot, callback or cross-invocation authorization.
 Ancestor times/linkcounts are intentionally excluded: unrelated child IO
 changes them. Device/inode/UID/GID/mode/type/ALLattrs/link references are
 checked at open, after bytes, and after the final consumer instead.
 """
 def __init__(self,path,limit):self._init175(path,limit,None)
 def _init175(self,path,limit,pool):
  self.fd=None;self.closed=False;self.directories=[];self.pooled=pool is not None
  try:
   if limit not in (83886080,67108864,33554432):raise ValueError('Closed physical role ceiling')
   self.path=pathlib.Path(path)
   if not self.path.is_absolute()or str(self.path)!=os.path.normpath(os.fspath(path)):raise ValueError('Exact absolute normalized path')
   parts=self.path.parts[1:]
   if not parts:raise ValueError('Regular leaf required')
   if pool is None:
    rootfd=os.open('/',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);row={'fd':rootfd,'path':'/','name':None,'parent_fd':None};self.directories.append(row);self.anchor_uid=os.fstat(rootfd).st_uid;self._capture_dir175(row)
   else:
    row=pool.nodes.get('/')
    if row is None:
     rootfd=os.open('/',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);row={'fd':rootfd,'path':'/','name':None,'parent_fd':None};pool.nodes['/']=row;pool.anchor_uid=os.fstat(rootfd).st_uid
     self.anchor_uid=pool.anchor_uid;self._capture_dir175(row)
    self.anchor_uid=pool.anchor_uid;self.directories.append(row)
   parentfd=row['fd'];current=pathlib.Path('/');private_after_shared=False
   for name in parts[:-1]:
    current=current/name;key=str(current);row=None if pool is None else pool.nodes.get(key)
    if row is None:
     fd=os.open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parentfd);row={'fd':fd,'path':key,'name':name,'parent_fd':parentfd}
     if pool is not None:pool.nodes[key]=row
     self.directories.append(row);self._capture_dir175(row)
    else:self.directories.append(row)
    if row['policy']in('TRUSTED_STICKY_SHARED_TMP_FD','QUALIFIED_RUNTIME_SHARED_WORKSPACE_FD'):private_after_shared=False
    elif row['policy']=='OWNED_SAFE_PRIVATE_BOUNDARY':private_after_shared=True
    parentfd=row['fd']
   if not private_after_shared:raise ValueError('Owned safe private boundary after shared anchor required')
   self.parent_fd=parentfd;self.leaf=parts[-1];s=os.stat(self.leaf,dir_fd=parentfd,follow_symlinks=False)
   if not stat.S_ISREG(s.st_mode)or s.st_uid!=os.getuid()or s.st_nlink!=1 or s.st_mode&0o022 or not 0<s.st_size<=limit:raise ValueError('Owned regular bounded noalias leaf')
   self.identity=_identity173(s);self.fd=os.open(self.leaf,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=parentfd)
   if _identity173(os.fstat(self.fd))!=self.identity:raise ValueError('Same opened leaf FD identity')
   self.attrs=_attrs175(self.fd);self._check_dirs175()
   raw=bytearray(s.st_size);v=memoryview(raw);n=0
   with os.fdopen(self.fd,'rb',buffering=0,closefd=False)as f:
    while n<len(raw):
     count=f.readinto(v[n:])
     if not count:raise ValueError('Whole EOF')
     n+=count
    if f.read(1):raise ValueError('EOF overflow')
   del v;self.raw=raw;self.raw_sha=hashlib.sha256(raw).hexdigest();self.reseal173()
  except BaseException:self.close173();raise
 def _capture_dir175(self,row):
  s=os.fstat(row['fd']);row['identity']=_dir_identity175(s);row['attrs']=_attrs175(row['fd']);row['policy']=_directory_policy175(row['path'],s,self.anchor_uid)
  self._check_dir175(row)
 def _check_dir175(self,row):
  fd=row['fd'];s=os.fstat(fd)
  if _dir_identity175(s)!=row['identity']or _attrs175(fd)!=row['attrs']or _directory_policy175(row['path'],s,self.anchor_uid)!=row['policy']:raise ValueError('Ancestor FD owner/mode/identity/ALLattrs drift')
  link=os.stat('/',follow_symlinks=False)if row['parent_fd']is None else os.stat(row['name'],dir_fd=row['parent_fd'],follow_symlinks=False)
  if _dir_identity175(link)!=row['identity']:raise ValueError('Ancestor path reference replaced or aliased')
 def _check_dirs175(self):
  if self.pooled:return # Deferred to exact invocation last-consumer boundary; no effects occur before it.
  for row in self.directories:self._check_dir175(row)
 def reseal173(self):
  if self.fd is None or self.closed:raise ValueError('No closed/cross-invocation FD adoption')
  self._check_dirs175();h=hashlib.sha256();os.lseek(self.fd,0,os.SEEK_SET);n=0
  while True:
   b=os.read(self.fd,1048576)
   if not b:break
   n+=len(b)
   if n>self.identity[5]:raise ValueError('EOF grew')
   h.update(b)
  if n!=self.identity[5]or h.hexdigest()!=self.raw_sha or _identity173(os.fstat(self.fd))!=self.identity or _identity173(os.stat(self.leaf,dir_fd=self.parent_fd,follow_symlinks=False))!=self.identity or _attrs175(self.fd)!=self.attrs:raise ValueError('Whole same FD/raw/PREPOST/EOF/path/leafALLattrs drift')
  self._check_dirs175()
 def close173(self):
  fds=([self.fd]if self.fd is not None else[])+([]if self.pooled else[x['fd']for x in reversed(self.directories)]);self.fd=None;self.directories=[];self.closed=True
  for fd in fds:
   try:os.close(fd)
   except OSError:pass

class _Invocation175:
 """Source-owned directory FD set; never accepted from a guard caller.
 No JSON, hash, proof or authority cache. Fresh per current_binding174 call.
 Capture each shared directory at first open, keep every FD and exact link,
 verify all of them after every leaf's final raw reseal and last consumer.
 Pinned leaf bytes/self predicates and no-effect pure consumers run unchanged.
 """
 def __init__(self):self.nodes={};self.closed=False;self.anchor_uid=None
 def open175(self,path,limit):
  if self.closed:raise ValueError('Closed invocation resource')
  resource=Whole173.__new__(Whole173);resource._init175(path,limit,self);return resource
 def reseal175(self):
  if self.closed:raise ValueError('Closed invocation resource')
  for row in self.nodes.values():Whole173._check_dir175(self,row)
 def close175(self):
  nodes=list(self.nodes.values());self.nodes={};self.closed=True
  for row in reversed(nodes):
   try:os.close(row['fd'])
   except OSError:pass
