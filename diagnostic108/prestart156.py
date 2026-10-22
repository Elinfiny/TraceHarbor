"""Explicit prospective150 AFTER consumed149; reserved148 never a predecessor.
Old149 implementation is unchanged and delegated only for historical validation.
SOURCE156 is source-only: no invocation here can create a native capability.
"""
import pathlib,runpy,copy,re,ast,json,os,stat
ROOT=pathlib.Path(__file__).resolve().parent
old=runpy.run_path(str(ROOT/'prestart154.py'));can=old['can'];sha=old['sha'];ORIGINAL=old['ORIGINAL'];SCHEMA='TRACE156_PRESTART150_PREDECESSOR149_V1'
TABLE={150:{'predecessor':149,'predecessor_state':'NATIVE149_TERMINAL','reserved_history':148}}
def contract154(value):
 if type(value) is not dict:raise ValueError('Exact explicit prestart contract object')
 if value.get('direction_number')==149:return old['contract154'](value)
 expected={'schema':SCHEMA,'direction_number':150,'predecessor':149,'predecessor_state':'NATIVE149_TERMINAL','reserved_history':148,'creation':'EXCLUSIVE_EMPTY_0700_BEFORE_FIRST_RX_AND_REGISTRY','consumption':'FROZEN_PARENT_CHILD_DEV_INO_UID_MODE_NO_ALIAS_BEFORE_CLOCK'}
 if type(value) is not dict or set(value)!=set(expected)|{'predecessor149_sha256','reserved148_sha256'} or any(value[k]!=v for k,v in expected.items()) or any(type(value[k]) is not str or re.fullmatch('[a-f0-9]{64}',value[k]) is None for k in ('predecessor149_sha256','reserved148_sha256')):raise ValueError('Closed explicit150/consumed149/reserved148')
 return copy.deepcopy(value)
def history154(own,config,*,before_RX):
 x=contract154(config['prestart154'])
 if x['direction_number']==149:return old['history154'](own,config,before_RX=before_RX)
 if own.get('native_id')!='6acfe37b-828c-83eb-b466-7670beb64ff2' or own.get('ownership',{}).get('owner')!='TraceHarbor V1' or own['ownership'].get('duplicate_trace_route_owners')!=0:raise ValueError('Existing soleTrace identity')
 if own.get('native149',{}).get('phase')!='TERMINAL' or sha(can(own.get('native149')))!=x['predecessor149_sha256'] or sha(can(own.get('native148')))!=x['reserved148_sha256']:raise ValueError('Whole consumed149/reserved148 immutable')
 if before_RX:
  if own.get('state')!='NATIVE149_TERMINAL' or 'native150' in own:raise ValueError('Explicit unused150; no149 replay')
 else:
  n=own.get('native150',{})
  if not own.get('state','').startswith('NATIVE150_') or not n.get('records') or n['records'][0]['phase']!='RX_START':raise ValueError('Actual150 RX lineage')
 return x
def derive150(original,auditor_version):
 if len(original.encode())!=3827 or sha(original.encode())!=ORIGINAL or type(auditor_version) is not int or auditor_version<=0:raise ValueError('Exact immutable008f/fresh A version')
 # Each exact original118 token is enumerated; no active149 writer is adapted.
 substitutions=[('direction118.json','direction150.json'),("'native118.records'","'native150.records'"),("'native118'","'native150'"),("'NATIVE117_TERMINAL'","'NATIVE149_TERMINAL'"),("'NATIVE118_'","'NATIVE150_'"),('CURRENT Auditor858 direction118','CURRENT Auditor'+str(auditor_version)+' direction150')]
 out=original;counts=[]
 for before,after in substitutions:
  n=out.count(before)
  if not n:raise ValueError('Original exhaustive150 substitution missing')
  counts.append({'before':before,'after':after,'occurrences':n});out=out.replace(before,after)
 if '118' in out or 'NATIVE148_TERMINAL' in out or 'NATIVE147_TERMINAL' in out:raise ValueError('No inferred predecessor')
 ast.parse(out);return out,counts
parent154=old['parent154'];ident154=old['ident154']
def prepare_child154(own,config):
 if config['prestart154']['direction_number']==149:return old['prepare_child154'](own,config)
 history154(own,config,before_RX=True);parent,before=parent154(config['path_roles']['holder_parent']);root=parent/'holder';root.mkdir(mode=0o700,exist_ok=False);after=parent.lstat();child=root.lstat()
 if ident154(before)!=ident154(after) or root.resolve()!=root or root.is_symlink() or not stat.S_ISDIR(child.st_mode) or child.st_uid!=os.getuid() or stat.S_IMODE(child.st_mode)!=0o700 or list(root.iterdir()):raise ValueError('Exclusive child drift; preserve attempt no adoption')
 return {'schema':SCHEMA,'direction_number':150,'predecessor':149,'reserved_history':148,'parent_path':str(parent),'parent':ident154(before),'child_path':str(root),'child':ident154(child),'expected_empty':True,'native_authority':False}
def check_child154(receipt,config,*,empty=True):
 if config['prestart154']['direction_number']==149:return old['check_child154'](receipt,config,empty=empty)
 if type(receipt) is not dict or set(receipt)!={'schema','direction_number','predecessor','reserved_history','parent_path','parent','child_path','child','expected_empty','native_authority'} or receipt['schema']!=SCHEMA or receipt['direction_number']!=150 or receipt['predecessor']!=149 or receipt['reserved_history']!=148 or receipt['native_authority'] is not False or receipt['expected_empty'] is not True:raise ValueError('Exact150 prepared child receipt')
 parent,ps=parent154(config['path_roles']['holder_parent']);root=parent/'holder'
 if receipt['parent_path']!=str(parent) or receipt['child_path']!=str(root) or receipt['parent']!=ident154(ps) or root.resolve()!=root or root.is_symlink():raise ValueError('Frozen parent/child alias or identity drift')
 child=root.lstat()
 if not stat.S_ISDIR(child.st_mode) or ident154(child)!=receipt['child'] or child.st_uid!=os.getuid() or stat.S_IMODE(child.st_mode)!=0o700 or empty and list(root.iterdir()):raise ValueError('Frozen child identity/mode/empty drift')
 return {'schema':SCHEMA,'prepared_receipt_sha256':sha(can(receipt)),'child_path':str(root),'child':ident154(child),'empty':empty,'native_authority':False}
def current_prestart154(own,config,*,empty=True):
 if config['prestart154']['direction_number']==149:return old['current_prestart154'](own,config,empty=empty)
 history154(own,config,before_RX=False);return check_child154(own['native150']['records'][0]['payload']['holder_preparation154'],config,empty=empty)
def consume_child154(receipt,config):
 if config['prestart154']['direction_number']==149:return old['consume_child154'](receipt,config)
 check_child154(receipt,config,empty=True);parent,_=parent154(config['path_roles']['holder_parent']);root=parent/'holder';pfd=fd=None
 try:
  pfd=os.open(parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);fd=os.open('holder',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=pfd)
  if ident154(os.fstat(pfd))!=receipt['parent'] or ident154(os.fstat(fd))!=receipt['child'] or os.listdir(fd):raise ValueError('Frozen150 nofollow consumption identity')
  os.mkdir('originals',0o700,dir_fd=fd);os.fsync(fd)
  if ident154(parent.lstat())!=receipt['parent'] or ident154(root.lstat())!=receipt['child']:raise ValueError('Consumption moved; no clock')
  return root
 finally:
  if fd is not None:os.close(fd)
  if pfd is not None:os.close(pfd)
def current_binding154(base,path,version,config,require_plan=False,payload=None,_macro122=None):
 if config.get('direction_number')!=150:return old['current_binding154'](base,path,version,config,require_plan=require_plan,payload=payload,_macro122=_macro122)
 doc,raw=runpy.run_path(str(ROOT/'envelope158.py'))['checkpoint_adapter158'](base,path,base.OWN,version);match=re.fullmatch(r'NATIVE150_([A-Z_]+)',doc['state'])
 if match is None or match[1]=='TERMINAL':raise ValueError('No mutation of consumed150')
 n=doc['native150'];direction=n['direction'];binding=n['records'][0]['payload']['writer_binding']
 if len(direction['id'].encode())>256 or not direction['id'].startswith('V29-TRACE-150-') or direction.get('native_admission') is not True or len(direction['body'].encode())!=direction['bytes'] or sha(direction['body'].encode())!=direction['sha256'] or n['records'][0]['phase']!='RX_START':raise ValueError('Actual independent150 addressed release required')
 static=json.loads(pathlib.Path(config['config_path']).read_bytes()) if 'config_path' in config else config.get('static154')
 if static is None:raise ValueError('Exact static150')
 history154(doc,static,before_RX=False);base.validate_transfer_layout(binding)
 if config.get('writer_binding')!=binding or binding['direction_number']!=150 or binding['direction_id']!=direction['id'] or binding['direction_sha256']!=direction['sha256'] or binding['direction_bytes']!=direction['bytes']:raise ValueError('Immutable actual150 binding')
 root=pathlib.Path(binding['binding_root']);rs=root.lstat()
 if root.is_symlink() or not stat.S_ISDIR(rs.st_mode) or rs.st_uid!=os.getuid() or rs.st_mode&0o077:raise ValueError('Actual private150 root')
 original=base.private_regular(binding['original_writer_path']);writer=base.private_regular(root/'admin150.py');auditor=pathlib.Path(binding['auditor_path'])
 if binding['writer_path']!=str(writer) or not auditor.is_relative_to(root) or auditor.is_symlink():raise ValueError('Original150 writer/A locator')
 source=n['source_verification']['Auditor_V28_checkpoint.json'];araw=auditor.read_bytes();audit=base.strict(araw);v=copy.deepcopy(audit);v['integrity']['canonical_json_sha256']=None
 if type(binding['auditor_version']) is not int or binding['auditor_version']!=source['version'] or sha(araw)!=source['sha256'] or len(araw)!=source['bytes'] or sha(can(v))!=source['self_sha256'] or audit['integrity']['canonical_json_sha256']!=source['self_sha256'] or os.getxattr(auditor,'user.library-file-id').decode()!=source['library_file_id'] or int(os.getxattr(auditor,'user.library-file-version').decode())!=source['version']:raise ValueError('Whole immutable original118 A preserved150')
 boundary=audit['operation']['effect_replay_boundary'];boundary=base.strict(boundary) if isinstance(boundary,str) else boundary
 if boundary['recipient_outboxes']['TraceHarbor V1']!=direction or doc['guard']['operation_id']!=direction['id']:raise ValueError('Actual addressed150 operation')
 if sha(original.read_bytes())!=ORIGINAL or binding['original_writer_sha256']!=ORIGINAL:raise ValueError('Original008f unchanged')
 expected,_=derive150(original.read_text(),binding['auditor_version'])
 if writer.read_text()!=expected or sha(writer.read_bytes())!=binding['writer_sha256']:raise ValueError('Exact explicit150/pre149 original derivation')
 result={'number':150,'key':'native150','binding':binding,'direction':direction,'original':original,'writer':writer,'doc':doc,'raw':raw}
 if require_plan:
  if _macro122 is None:raise ValueError('Only source-owned macro plan150')
  base._check_macro122(_macro122,result,version,payload)
 return result
