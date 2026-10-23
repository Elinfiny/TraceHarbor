"""Inactive reviewed-source candidate: exact Trace metadata exception.
All return values are evidence/data, never native/provider authorization.
Only the source's authenticated materialization/readback route supplies transfer
originals. A dictionary, filename, hash or this module cannot grant that route.
"""
import os,stat,json,pathlib,hashlib,copy
OWN='libfile_3ee8270f03d8819188e1de1f75c3d824'
CHAT='6acfe37b-828c-83eb-b466-7670beb64ff2'
GENERIC=67108864;TRACE=83886080;PRIVATE=33554432
CONTRACT={'schema':'TRACE158_ROLE_BOUND_METADATA_ENVELOPE_V1','trace_checkpoint_id':OWN,'trace_native_id':CHAT,'trace_owner':'TraceHarbor V1','duplicate_owners':0,'trace_metadata_bytes':TRACE,'other_metadata_bytes':GENERIC,'private_each_bytes':PRIVATE,'IPC_bytes':1048576,'outer_terminal_bytes':2097152,'identity':'AUTHENTIC_TRANSFER_PLUS_POSITIVE_ID_ALLATTRS_WHOLE_RAW_SELF_NATIVE_OWNER','authority':'NO_GRANT_FROM_SIZE_OR_DATA','activation':'INDEPENDENT_REVIEW_CANONICAL_PUBLICATION_AND_SEPARATE_NATIVE_RELEASE'}
can=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
sha=lambda b:hashlib.sha256(b).hexdigest()
def contract158(x):
 if x!=CONTRACT:raise ValueError('Exact closed inactive158 metadata contract')
 return copy.deepcopy(CONTRACT)
def role158(doc,stable):
 trace=doc.get('native_id')==CHAT or doc.get('ownership',{}).get('owner')=='TraceHarbor V1'
 if stable==OWN:
  if doc.get('native_id')!=CHAT or doc.get('ownership',{}).get('owner')!='TraceHarbor V1' or type(doc['ownership'].get('duplicate_trace_route_owners')) is not int or doc['ownership']['duplicate_trace_route_owners']!=0:raise ValueError('Exact positive Trace native/owner/unique role')
 elif trace:raise ValueError('Foreign metadata cannot claim Trace identity')
 return TRACE if stable==OWN else GENERIC
def attributes158(p,transfer):
 if type(transfer) is not dict or not {'library_file_id','file_id','size_bytes','current_version_number','xattrs','workspace_path'}<=set(transfer) or not isinstance(transfer['library_file_id'],str) or not transfer['library_file_id'].startswith('libfile_') or not isinstance(transfer['file_id'],str) or not transfer['file_id'].startswith('file_') or type(transfer['current_version_number']) is not int or transfer['current_version_number']<0 or type(transfer['size_bytes']) is not int or type(transfer['xattrs']) is not list:raise ValueError('Complete authorized transfer original required')
 # Admission A is an exact private byte-copy, therefore its path may differ
 # from the provider workspace_path; all stable identities/pins still match.
 if os.getxattr(p,'user.library-file-id').decode()!=transfer['library_file_id'] or os.getxattr(p,'user.library-file-version').decode()!=str(transfer['current_version_number']):raise ValueError('Positive actual ID/version, not a claimed tuple')
 seen=set()
 for a in transfer['xattrs']:
  if type(a) is not dict or set(a)!={'name','value'} or a['name'] in seen or os.getxattr(p,a['name']).decode()!=a['value']:raise ValueError('Whole returned attrs exactly')
  seen.add(a['name'])
 return transfer['library_file_id']
def physical158(path,limit,*,private=False,expected=None):
 if limit not in (GENERIC,TRACE,PRIVATE):raise ValueError('Closed physical read ceilings')
 p=pathlib.Path(path)
 if not p.is_absolute() or p.resolve()!=p or any(q.is_symlink() for q in [p,*p.parents]):raise ValueError('Every ancestor nofollow, exact absolute path')
 s=p.lstat();ident=lambda z:(z.st_dev,z.st_ino,z.st_uid,z.st_mode,z.st_nlink,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
 if not stat.S_ISREG(s.st_mode) or s.st_uid!=os.getuid() or s.st_nlink!=1 or s.st_mode&0o022 or private and s.st_mode&0o077 or not 0<s.st_size<=limit:raise ValueError('Owned whole bounded metadata/custody file')
 if expected is not None and (s.st_dev,s.st_ino,s.st_uid,s.st_mode&0o777)!=(expected['dev'],expected['ino'],expected['uid'],expected['mode']):raise ValueError('No recreated custody adoption')
 attrs={n:os.getxattr(p,n) for n in os.listxattr(p)};fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  before=os.fstat(fd);buf=bytearray(s.st_size);view=memoryview(buf);total=0
  with os.fdopen(fd,'rb',buffering=0,closefd=False) as f:
   while total<len(buf):
    n=f.readinto(view[total:])
    if not n:raise ValueError('Incomplete whole EOF')
    total+=n
   if f.read(1):raise ValueError('Size/EOF drift')
  del view;after=os.fstat(fd)
 finally:os.close(fd)
 end=p.lstat()
 if not ident(s)==ident(before)==ident(after)==ident(end) or attrs!={n:os.getxattr(p,n) for n in os.listxattr(p)}:raise ValueError('Whole identity/EOF/attrs drift during read')
 return bytes(buf)
def read158(path,transfer,*,private=False,original=None):
 p=pathlib.Path(path);stable=attributes158(p,transfer);limit=PRIVATE if private else TRACE if stable==OWN else GENERIC
 if stable==OWN:
  if type(original) is not dict or original.get('isError') or 'structuredContent' not in original:raise ValueError('Source-captured whole actual fourfile original required for Trace exception')
  result=original['structuredContent'];result=result.get('result',result);ts=result.get('transfers',[])
  if result.get('unavailable_items') or len(ts)!=4 or {t['library_file_id'] for t in ts}!={OWN,'libfile_f87a6a307f70819194e0af0fa453afd1','libfile_6f69ae483b088191a1fffefca617bbd5','libfile_8377022600088191993dc06bfba93b7b'} or [t for t in ts if t['library_file_id']==OWN]!=[transfer]:raise ValueError('Unaltered exact tuple from source-captured original, never substituted tuple')
 raw=physical158(p,limit,private=private)
 if len(raw)!=transfer['size_bytes']:raise ValueError('Actual whole transfer size')
 d=json.loads(raw);role158(d,stable)
 h=d['integrity']['canonical_json_sha256'] if stable=='libfile_f87a6a307f70819194e0af0fa453afd1' else d['self_sha256']
 if self_hash158(d,stable)!=h:raise ValueError('Whole canonical self hash')
 # Recheck every positive attribute after full parse/self processing too.
 attributes158(p,transfer)
 return d,raw,h
def canonical_sha158(value):
 from snapshot174 import canonical_sha173
 return canonical_sha173(value)
def self_hash158(doc,stable=OWN):
 # Shallow root copy changes only the self field. Protected nested values are
 # never mutated, reserialized as a whole buffer, truncated or externalized.
 v=dict(doc)
 if stable=='libfile_f87a6a307f70819194e0af0fa453afd1':
  v['integrity']=dict(doc['integrity']);v['integrity']['canonical_json_sha256']=None
 else:v['self_sha256']=None
 return canonical_sha158(v)
def proof158(path,transfer,*,private=False,original=None):
 d,raw,h=read158(path,transfer,private=private,original=original)
 return d,{'library_file_id':transfer['library_file_id'],'file_id':transfer['file_id'],'version':transfer['current_version_number'],'bytes':len(raw),'sha256':sha(raw),'self_sha256':h,'ALLattrs':'PASS'}
def local_checkpoint158(path,version,expected_sha=None):
 p=pathlib.Path(path)
 if os.getxattr(p,'user.library-file-id').decode()!=OWN or os.getxattr(p,'user.library-file-version').decode()!=str(version):raise ValueError('Positive own expectedversion')
 raw=physical158(p,TRACE);d=json.loads(raw);role158(d,OWN)
 if self_hash158(d)!=d['self_sha256'] or expected_sha is not None and sha(raw)!=expected_sha:raise ValueError('Whole own self/expectedraw')
 return d,raw
def checkpoint_adapter158(base,path,library_id,version,expected_sha=None):
 if library_id!=base.OWN or library_id!=OWN:raise ValueError('Only exact existing118 owned checkpoint')
 p=pathlib.Path(path)
 if os.getxattr(p,'user.library-file-id').decode()!=OWN or os.getxattr(p,'user.library-file-version').decode()!=str(version):raise ValueError('Positive own expectedversion')
 raw=physical158(p,TRACE);d=base.strict(raw);role158(d,OWN)
 # Identical immutable118 parser and canonical self semantics; streaming hash
 # replaces only the allocation strategy, not the protected predicate.
 if self_hash158(d)!=d['self_sha256'] or expected_sha is not None and sha(raw)!=expected_sha or d['ownership']['owner']!='TraceHarbor V1' or d['ownership']['duplicate_trace_route_owners']!=0:raise ValueError('Immutable118 whole parser/self/owner predicate')
 return d,raw
def publication_checkpoint158(path,version):
 # Preserve the former stable150 publication-specific permission mask.
 if pathlib.Path(path).lstat().st_mode&0o027:raise ValueError('Original150 publication permissions')
 return local_checkpoint158(path,version)
