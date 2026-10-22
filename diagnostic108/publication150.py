"""Prepared publication protocol. CLI owns one helper invocation; imports have no effects.
Only source-owned caller frames may use the native bridge. Pure validators are
also used by explicitly PRIVATE_SOURCE_ONLY fixtures, never as native authority.
"""
from pathlib import Path
import os,stat,json,hashlib,copy,subprocess,sys,time
OWN='libfile_3ee8270f03d8819188e1de1f75c3d824';MAX=67108864;REASON='Actual independently admitted grouped phase consumed before first effect'
can=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
sha=lambda b:hashlib.sha256(b).hexdigest()
def closed(x,keys):
 if type(x) is not dict or set(x)!=set(keys):raise ValueError('Closed publication150 shape')
 return x
def stable150(path,limit):
 p=Path(path)
 if not p.is_absolute() or p.resolve()!=p or any(x.is_symlink() for x in [p,*p.parents]):raise ValueError('Absolute nofollow file')
 a=p.lstat()
 if not stat.S_ISREG(a.st_mode) or a.st_uid!=os.getuid() or a.st_nlink!=1 or a.st_mode&0o027 or a.st_size>limit:raise ValueError('Owned regular0640-or-stricter bounded file')
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  b=os.fstat(fd);out=[];size=0
  while True:
   chunk=os.read(fd,1048576)
   if not chunk:break
   size+=len(chunk)
   if size>limit:raise ValueError('Complete bounded file')
   out.append(chunk)
  c=os.fstat(fd)
 finally:os.close(fd)
 d=p.lstat();ident=lambda s:(s.st_dev,s.st_ino,s.st_uid,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns)
 if not ident(a)==ident(b)==ident(c)==ident(d):raise ValueError('Stable EOF identity')
 return b''.join(out)
def contract150(x):
 closed(x,{'schema','route','helpers','helper_seconds','polls','internal_reserved_operations'})
 if x['schema']!='TRACE150_UNIFORM_PREPARED_V1' or x['route']!='PREPARED_ONLY' or x['helper_seconds']!=12 or x['polls']!=8 or x['internal_reserved_operations']!=['prepare','transfer','finalize','metadata']:raise ValueError('Exact finite prepared contract')
 closed(x['helpers'],{'library_upload.py','library_hosted_apps.py','library_file_transfer.py'});parents=set()
 for name,pin in x['helpers'].items():
  closed(pin,{'path','bytes','sha256'});p=Path(pin['path']);parents.add(p.parent)
  if p.name!=name or len(stable150(p,33554432))!=pin['bytes'] or sha(stable150(p,33554432))!=pin['sha256']:raise ValueError('Current unchanged whole helper pin')
 if len(parents)!=1:raise ValueError('One private helper directory')
 return x
def precheck150(config,args):
 contract150(config['publication150']);closed(args,{'library_file_id','file','expected_current_version','version_reason'})
 v=args['expected_current_version'];roles=config['path_roles'];p=Path(args['file']);transfer=Path(roles['transfer'])
 if args['library_file_id']!=OWN or type(v) is not int or v<=0 or args['version_reason']!=REASON or p!=transfer/('group127-upload-'+str(v))/'TraceHarbor_V1_checkpoint.json':raise ValueError('One exact owned conditional replacement')
 for k in ('private','transfer','holder_parent'):
  q=Path(roles[k]);s=q.lstat()
  if q.resolve()!=q or q.is_symlink() or not stat.S_ISDIR(s.st_mode) or s.st_uid!=os.getuid() or s.st_mode&0o077:raise ValueError('Owned disjoint roles')
 roots=[Path(roles[k]) for k in ('private','transfer','holder_parent')]
 if any(a==b or a.is_relative_to(b) or b.is_relative_to(a) for i,a in enumerate(roots) for b in roots[i+1:]):raise ValueError('Disjoint publication roles')
 envelope=__import__('runpy').run_path(str(Path(__file__).resolve().parent/'envelope158.py'));d,raw=envelope['publication_checkpoint158'](p,v)
 if envelope['self_hash158'](d)!=d['self_sha256'] or d['ownership']['owner']!='TraceHarbor V1' or d['ownership']['duplicate_trace_route_owners']!=0:raise ValueError('Whole self and sole ownership')
 if os.getxattr(p,'user.library-file-id').decode()!=OWN or os.getxattr(p,'user.library-file-version').decode()!=str(v):raise ValueError('Positive upload identity/current expectedversion')
 return {'path':str(p),'bytes':len(raw),'sha256':sha(raw),'self_sha256':d['self_sha256'],'expected_current_version':v,'request_sha256':sha(can(args))}
def validate_item150(output,args):
 closed(output,{'results'})
 if type(output['results']) is not list or len(output['results'])!=1:raise ValueError('Exactly one ordered peritem result')
 x=output['results'][0];required={'local_path','purpose','status','file_id','library_file_id','file_name','local_metadata_applied','path','current_version_number'};closed(x,required)
 if x['status']!='succeeded' or x['local_path']!=args['file'] or x['purpose']!='replace_library_file' or x['library_file_id']!=OWN or x['current_version_number']!=args['expected_current_version']+1 or x['file_name']!='TraceHarbor_V1_checkpoint.json' or x['path']!='/TraceHarbor_V1_checkpoint.json' or x['local_metadata_applied'] is not True or not isinstance(x['file_id'],str) or not x['file_id'].startswith('file_'):raise ValueError('Actual exact succeeded peritem expectedversion')
 return copy.deepcopy(x)
def normalize150(carrier):
 closed(carrier,{'schema','request','exec_originals'})
 if carrier['schema']!='TRACE150_AUTHENTIC_EXEC_CARRIER' or not 1<=len(carrier['exec_originals'])<=9:raise ValueError('Authentic bounded helper execution carrier')
 text='';session=None;seen=set()
 for n,x in enumerate(carrier['exec_originals']):
  if type(x) is not dict or x.get('tool_throw') or type(x.get('output')) is not str or not isinstance(x.get('chunk_id'),str) or x['chunk_id'] in seen or x.get('original_token_count',0)>16000:raise ValueError('Complete original exec chunk')
  seen.add(x['chunk_id']);text+=x['output']
  if len(text.encode())>65536:raise ValueError('Bounded aggregate helper output')
  if n==0:session=x.get('session_id')
  elif x.get('session_id') not in (None,session):raise ValueError('Same helper session only')
  if n<len(carrier['exec_originals'])-1 and (x.get('exit_code') is not None or x.get('session_id')!=session):raise ValueError('No early terminal or adopted session')
 last=carrier['exec_originals'][-1]
 if last.get('exit_code')!=0 or last.get('session_id') is not None or last.get('eof') is False:raise ValueError('Actual terminal0 EOF before dependent operation')
 r=json.loads(text);closed(r,{'schema','request_sha256','upload','helper_original','ordered_result','local_xattrs','effect_identity','status'})
 args=carrier['request'];h=r['helper_original'];closed(h,{'returncode','stdout','stderr','elapsed_s'})
 if r['schema']!='TRACE150_PREPARED_RESULT' or r['status']!='SUCCEEDED' or r['request_sha256']!=sha(can(args)) or h['returncode']!=0 or not 0<=h['elapsed_s']<=12:raise ValueError('Exact prepared helper terminal receipt')
 item=validate_item150(json.loads(h['stdout']),args)
 if r['ordered_result']!=item or r['effect_identity']!={'library_file_id':OWN,'file_id':item['file_id'],'version':item['current_version_number'],'request_sha256':sha(can(args))}:raise ValueError('Actual published effect identity')
 attrs=r['local_xattrs']
 if type(attrs) is not list or len({a['name'] for a in attrs})!=len(attrs) or any(set(a)!=set(('name','value')) for a in attrs):raise ValueError('Whole observed local metadata')
 m={a['name']:a['value'] for a in attrs}
 if m.get('user.library-file-id')!=OWN or m.get('user.library-file-version')!=str(item['current_version_number']):raise ValueError('Post-helper positive identity/version')
 return dict(item,xattrs=attrs,publication150={'schema':'TRACE150_VALIDATED_PREPARED_FIELDS_NOT_RAW_PROVIDER_ORIGINAL','carrier_sha256':sha(can(carrier)),'effect_identity':r['effect_identity'],'upload':r['upload']})
def put150(p,data):
 fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'wb') as f:f.write(can(data));f.flush();os.fsync(f.fileno())
def main150():
 config=json.loads(stable150(sys.argv[1],33554432));args=json.loads(sys.argv[2]);upload=precheck150(config,args);capture=Path(config['path_roles']['capture']);journal=capture/('publish150-'+str(args['expected_current_version'])+'-'+upload['request_sha256']+'.intent.json');put150(journal,{'schema':'TRACE150_WRITE_ATTEMPT_CONSUMED','request':args,'upload':upload,'route':'PREPARED_ONLY','unknown_rule':'No retry/fallback; reconcile actual current own/version and this journal'})
 request={'uploads':[{'local_path':args['file'],'purpose':'replace_library_file','library_file_id':OWN,'expected_current_version':args['expected_current_version'],'version_reason':args['version_reason']}]};start=time.monotonic();proc=subprocess.Popen([sys.executable,config['publication150']['helpers']['library_upload.py']['path']],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 try:out,err=proc.communicate(can(request),timeout=12)
 except subprocess.TimeoutExpired as e:
  put150(journal.with_suffix('.UNKNOWN.json'),{'status':'UNKNOWN_NO_RETRY','pid':proc.pid,'returncode':proc.poll(),'stdout_hex':(e.stdout or b'').hex(),'stderr_hex':(e.stderr or b'').hex(),'hidden_kill':False});raise RuntimeError('Prepared outcome UNKNOWN; no second write or fallback')
 h={'returncode':proc.returncode,'stdout':out.decode(),'stderr':err.decode(),'elapsed_s':time.monotonic()-start};put150(journal.with_suffix('.helper-original.json'),h)
 if proc.returncode!=0:raise RuntimeError('Complete original retained; no fallback')
 item=validate_item150(json.loads(h['stdout']),args);_,raw=__import__('runpy').run_path(str(Path(__file__).resolve().parent/'envelope158.py'))['publication_checkpoint158'](args['file'],item['current_version_number'])
 if sha(raw)!=upload['sha256']:raise ValueError('Upload body changed after helper')
 attrs=[{'name':n,'value':os.getxattr(args['file'],n).decode()} for n in sorted(os.listxattr(args['file']))];effect={'library_file_id':OWN,'file_id':item['file_id'],'version':item['current_version_number'],'request_sha256':upload['request_sha256']};r={'schema':'TRACE150_PREPARED_RESULT','request_sha256':upload['request_sha256'],'upload':upload,'helper_original':h,'ordered_result':item,'local_xattrs':attrs,'effect_identity':effect,'status':'SUCCEEDED'};put150(journal.with_suffix('.receipt.json'),r)
 if len(can(r))>65536:raise ValueError('Complete oversized helper receipt retained privately; no IPC truncation/retry')
 print(can(r).decode())
if __name__=='__main__':main150()
