"""SOURCE173 candidate bounded canonical hashing and one-invocation whole FD.
No native registry, capability, cached authorization or caller-provided snapshot.
Every completion re-reads the SAME FD, EOF, full raw hash and ALL attributes.
"""
import os,stat,pathlib,json,hashlib
def canonical_sha173(value):
 h=hashlib.sha256()
 def string(s):
  h.update(b'"')
  for i in range(0,len(s),65536):h.update(json.encoder.encode_basestring(s[i:i+65536])[1:-1].encode('utf-8'))
  h.update(b'"')
 def feed(v):
  if isinstance(v,str):string(v)
  elif isinstance(v,dict):
   h.update(b'{')
   for i,k in enumerate(sorted(v)):
    if not isinstance(k,str):raise TypeError('JSON document keys must be strings')
    if i:h.update(b',')
    string(k);h.update(b':');feed(v[k])
   h.update(b'}')
  elif isinstance(v,(list,tuple)):
   h.update(b'[')
   for i,x in enumerate(v):
    if i:h.update(b',')
    feed(x)
   h.update(b']')
  else:h.update(json.dumps(v,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode())
 feed(value);return h.hexdigest()
def self_sha173(doc,stable):
 v=dict(doc)
 if stable=='libfile_f87a6a307f70819194e0af0fa453afd1':v['integrity']=dict(v['integrity']);v['integrity']['canonical_json_sha256']=None
 else:v['self_sha256']=None
 return canonical_sha173(v)
def _identity173(s):return (s.st_dev,s.st_ino,s.st_uid,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
class Whole173:
 """Internal physical resource only; never accepted as authority by an API."""
 def __init__(self,path,limit):
  if limit not in (83886080,67108864,33554432):raise ValueError('Closed physical role ceiling')
  self.path=pathlib.Path(path);self.fd=None;self.closed=False
  self._path173();s=self.path.lstat()
  if not stat.S_ISREG(s.st_mode)or s.st_uid!=os.getuid()or s.st_nlink!=1 or s.st_mode&0o022 or not 0<s.st_size<=limit:raise ValueError('Owned regular bounded file')
  self.identity=_identity173(s);self.attrs={k:os.getxattr(self.path,k)for k in os.listxattr(self.path)};self.fd=os.open(self.path,os.O_RDONLY|os.O_NOFOLLOW)
  try:
   if _identity173(os.fstat(self.fd))!=self.identity:raise ValueError('Same opened FD identity')
   # One final raw buffer plus <=1MiB transient chunks; no second full buffer.
   raw=bytearray(s.st_size);v=memoryview(raw);n=0
   with os.fdopen(self.fd,'rb',buffering=0,closefd=False)as f:
    while n<len(raw):
     count=f.readinto(v[n:])
     if not count:raise ValueError('Whole EOF')
     n+=count
    if f.read(1):raise ValueError('EOF overflow')
   del v;self.raw=raw;self.raw_sha=hashlib.sha256(raw).hexdigest();self.reseal173()
  except BaseException:self.close173();raise
 def _path173(self):
  p=self.path
  if not p.is_absolute()or p.resolve()!=p or any(x.is_symlink()for x in(p,*p.parents)):raise ValueError('Exact absolute nofollow path and ancestors')
 def reseal173(self):
  if self.fd is None or self.closed:raise ValueError('No cross-invocation/closed resource adoption')
  self._path173();h=hashlib.sha256();os.lseek(self.fd,0,os.SEEK_SET);n=0
  while True:
   b=os.read(self.fd,1048576)
   if not b:break
   n+=len(b)
   if n>self.identity[5]:raise ValueError('EOF grew')
   h.update(b)
  attrs={k:os.getxattr(self.fd,k)for k in os.listxattr(self.fd)}
  if n!=self.identity[5]or h.hexdigest()!=self.raw_sha or _identity173(os.fstat(self.fd))!=self.identity or _identity173(self.path.lstat())!=self.identity or attrs!=self.attrs or {k:os.getxattr(self.path,k)for k in os.listxattr(self.path)}!=self.attrs:raise ValueError('Whole same FD/raw/PREPOST/EOF/path/ALLattrs drift')
 def close173(self):
  if self.fd is not None:os.close(self.fd);self.fd=None
  self.closed=True
