"""Explicit149/predecessor147 preparation and immutable prepared-directory proof.
No import, dictionary or metadata receipt creates a native source capability.
Original008f/118/7266 remain byte-for-byte originals;148 is reserved history.
"""
import pathlib,os,stat,json,copy,hashlib,ast,re
ROOT=pathlib.Path(__file__).resolve().parent
can=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
sha=lambda b:hashlib.sha256(b).hexdigest()
TABLE={149:{'predecessor':147,'predecessor_state':'NATIVE147_TERMINAL','reserved_history':148}}
SCHEMA='TRACE154_PRESTART149_PREDECESSOR147_V1'
ORIGINAL='008f194ac2d4cd93e946949bb2a926acb58690adb1815734601cd9808e73550f'
def contract154(x):
 expected={'schema':SCHEMA,'direction_number':149,'predecessor':147,'predecessor_state':'NATIVE147_TERMINAL','reserved_history':148,'creation':'EXCLUSIVE_EMPTY_0700_BEFORE_FIRST_RX_AND_REGISTRY','consumption':'FROZEN_PARENT_CHILD_DEV_INO_UID_MODE_NO_ALIAS_BEFORE_CLOCK'}
 if type(x) is not dict or set(x)!=set(expected)|{'predecessor147_sha256','reserved148_sha256'} or any(x[k]!=v for k,v in expected.items()) or any(re.fullmatch('[a-f0-9]{64}',x[k]) is None for k in ('predecessor147_sha256','reserved148_sha256')):raise ValueError('Closed explicit149/real147 predecessor/reserved148 contract')
 return copy.deepcopy(x)
def history154(own,config,*,before_RX):
 x=contract154(config['prestart154'])
 if own.get('native_id')!='6acfe37b-828c-83eb-b466-7670beb64ff2' or own.get('ownership',{}).get('owner')!='TraceHarbor V1' or own['ownership'].get('duplicate_trace_route_owners')!=0:raise ValueError('Sole current Trace identity')
 if own.get('native147',{}).get('phase')!='TERMINAL' or sha(can(own.get('native147')))!=x['predecessor147_sha256'] or sha(can(own.get('native148')))!=x['reserved148_sha256']:raise ValueError('Actual147terminal and reserved148 full history immutable')
 if before_RX:
  if own.get('state')!='NATIVE147_TERMINAL' or 'native149' in own:raise ValueError('Unused149 only; real predecessor147, never fabricated148terminal')
 else:
  n=own.get('native149',{})
  if not own.get('state','').startswith('NATIVE149_') or not n.get('records') or n['records'][0]['phase']!='RX_START':raise ValueError('Actual149 RX lineage required')
 return x
def derive149(original,auditor_version):
 raw=original.encode()
 if len(raw)!=3827 or sha(raw)!=ORIGINAL or type(auditor_version) is not int or auditor_version<=0:raise ValueError('Exact original008f and actual fresh A version')
 substitutions=[('direction118.json','direction149.json'),("'native118.records'","'native149.records'"),("'native118'","'native149'"),("'NATIVE117_TERMINAL'","'NATIVE147_TERMINAL'"),("'NATIVE118_'","'NATIVE149_'"),('CURRENT Auditor858 direction118','CURRENT Auditor'+str(auditor_version)+' direction149')]
 out=original;counts=[]
 for before,after in substitutions:
  count=out.count(before)
  if not count:raise ValueError('Exact exhaustive original adaptation token missing')
  counts.append({'before':before,'after':after,'occurrences':count});out=out.replace(before,after)
 if '118' in out or 'NATIVE148_TERMINAL' in out or 'NATIVE117_TERMINAL' in out:raise ValueError('No numeric predecessor inference or leftover binding')
 ast.parse(out);return out,counts
def parent154(parent):
 p=pathlib.Path(parent)
 if not p.is_absolute() or p.resolve()!=p or any(q.is_symlink() for q in [p,*p.parents]):raise ValueError('Unaliased absolute parent')
 s=p.lstat()
 if not stat.S_ISDIR(s.st_mode) or s.st_uid!=os.getuid() or stat.S_IMODE(s.st_mode)!=0o700:raise ValueError('Owned parent0700')
 return p,s
def ident154(s):return {'dev':s.st_dev,'ino':s.st_ino,'uid':s.st_uid,'mode':stat.S_IMODE(s.st_mode),'type':'directory'}
def prepare_child154(own,config):
 history154(own,config,before_RX=True);parent,before=parent154(config['path_roles']['holder_parent']);root=parent/'holder';root.mkdir(mode=0o700,exist_ok=False);after=parent.lstat();s=root.lstat()
 if ident154(before)!=ident154(after) or root.resolve()!=root or root.is_symlink() or not stat.S_ISDIR(s.st_mode) or s.st_uid!=os.getuid() or stat.S_IMODE(s.st_mode)!=0o700 or list(root.iterdir()):raise ValueError('Exclusive child changed; retain first attempt, never adopt/retry/delete')
 return {'schema':SCHEMA,'direction_number':149,'predecessor':147,'reserved_history':148,'parent_path':str(parent),'parent':ident154(before),'child_path':str(root),'child':ident154(s),'expected_empty':True,'native_authority':False}
def check_child154(receipt,config,*,empty=True):
 if type(receipt) is not dict or set(receipt)!={'schema','direction_number','predecessor','reserved_history','parent_path','parent','child_path','child','expected_empty','native_authority'} or receipt['schema']!=SCHEMA or receipt['direction_number']!=149 or receipt['predecessor']!=147 or receipt['reserved_history']!=148 or receipt['native_authority'] is not False or receipt['expected_empty'] is not True:raise ValueError('Closed prepared directory identity')
 parent,s=parent154(config['path_roles']['holder_parent']);root=parent/'holder'
 if receipt['parent_path']!=str(parent) or receipt['child_path']!=str(root) or receipt['parent']!=ident154(s) or root.resolve()!=root or root.is_symlink():raise ValueError('Prepared parent/child alias or parent identity drift')
 child=root.lstat()
 if not stat.S_ISDIR(child.st_mode) or ident154(child)!=receipt['child'] or child.st_uid!=os.getuid() or stat.S_IMODE(child.st_mode)!=0o700 or empty and list(root.iterdir()):raise ValueError('Prepared child identity/mode/emptiness drift before registry/clock')
 return {'schema':SCHEMA,'prepared_receipt_sha256':sha(can(receipt)),'child_path':str(root),'child':ident154(child),'empty':empty,'native_authority':False}
def current_prestart154(own,config,*,empty=True):
 history154(own,config,before_RX=False);receipt=own['native149']['records'][0]['payload']['holder_preparation154'];return check_child154(receipt,config,empty=empty)
def consume_child154(receipt,config):
 check_child154(receipt,config,empty=True);parent,s=parent154(config['path_roles']['holder_parent']);root=parent/'holder';pfd=fd=None
 try:
  pfd=os.open(parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);fd=os.open('holder',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=pfd)
  if ident154(os.fstat(pfd))!=receipt['parent'] or ident154(os.fstat(fd))!=receipt['child'] or os.listdir(fd):raise ValueError('Frozen source consumption point drift')
  os.mkdir('originals',0o700,dir_fd=fd);os.fsync(fd)
  if ident154(parent.lstat())!=receipt['parent'] or ident154(root.lstat())!=receipt['child']:raise ValueError('Root moved at consumption; preserve attempted originals, no clock')
  return root
 finally:
  if fd is not None:os.close(fd)
  if pfd is not None:os.close(pfd)
def current_binding154(base,path,version,config,require_plan=False,payload=None,_macro122=None):
 if config.get('direction_number')!=149:return base.current_binding(path,version,config,require_plan=require_plan,payload=payload,_macro122=_macro122)
 doc,raw=base.check_checkpoint(path,base.OWN,version);match=re.fullmatch(r'NATIVE149_([A-Z_]+)',doc['state'])
 if match is None or match[1]=='TERMINAL':raise ValueError('No mutation of sealed149')
 number=149;key='native149';n=doc[key];direction=n['direction'];binding=n['records'][0]['payload']['writer_binding']
 if not re.match(r'^V28-(?:TRACEHARBOR|TRACE)-149-',direction['id']) or len(direction['body'].encode())!=direction['bytes'] or sha(direction['body'].encode())!=direction['sha256'] or n['records'][0]['phase']!='RX_START':raise ValueError('Exact current149 addressed body and RX')
 static=json.loads(pathlib.Path(config['config_path']).read_bytes()) if 'config_path' in config else config.get('static154')
 if static is None:raise ValueError('Exact static149 history contract required')
 history154(doc,static,before_RX=False);base.validate_transfer_layout(binding)
 if config.get('writer_binding')!=binding or binding['direction_number']!=149 or binding['direction_id']!=direction['id'] or binding['direction_sha256']!=direction['sha256'] or binding['direction_bytes']!=direction['bytes']:raise ValueError('Actual accepted149 immutable binding, not config authority')
 root=pathlib.Path(binding['binding_root']);rs=root.lstat()
 if root.is_symlink() or not stat.S_ISDIR(rs.st_mode) or rs.st_uid!=os.getuid() or rs.st_mode&0o077:raise ValueError('Private current149 root')
 original=base.private_regular(binding['original_writer_path']);writer=base.private_regular(root/'admin149.py');auditor=pathlib.Path(binding['auditor_path'])
 if binding['writer_path']!=str(writer) or not auditor.is_relative_to(root) or auditor.is_symlink():raise ValueError('Actual149 writer/A locator')
 source=n['source_verification']['Auditor_V28_checkpoint.json'];araw=auditor.read_bytes();audit=base.strict(araw);v=copy.deepcopy(audit);v['integrity']['canonical_json_sha256']=None
 if type(binding['auditor_version']) is not int or binding['auditor_version']!=source['version'] or sha(araw)!=source['sha256'] or len(araw)!=source['bytes'] or sha(can(v))!=source['self_sha256'] or audit['integrity']['canonical_json_sha256']!=source['self_sha256'] or os.getxattr(auditor,'user.library-file-id').decode()!=source['library_file_id'] or int(os.getxattr(auditor,'user.library-file-version').decode())!=source['version']:raise ValueError('Original whole immutable A guard preserved for149')
 boundary=audit['operation']['effect_replay_boundary'];boundary=base.strict(boundary) if isinstance(boundary,str) else boundary
 if boundary['recipient_outboxes']['TraceHarbor V1']!=direction or doc['guard']['operation_id']!=direction['id']:raise ValueError('Actual current149 direction and operation')
 if sha(original.read_bytes())!=ORIGINAL or binding['original_writer_sha256']!=ORIGINAL:raise ValueError('Original008f unchanged')
 expected,_=derive149(original.read_text(),binding['auditor_version'])
 if writer.read_text()!=expected or sha(writer.read_bytes())!=binding['writer_sha256']:raise ValueError('Explicit149/pre147 exact derivation, no arbitrary patch')
 result={'number':149,'key':key,'binding':binding,'direction':direction,'original':original,'writer':writer,'doc':doc,'raw':raw}
 if require_plan:
  if _macro122 is None:raise ValueError('149 only exact source macro plan; no legacy prepared-operation route')
  base._check_macro122(_macro122,result,version,payload)
 return result
