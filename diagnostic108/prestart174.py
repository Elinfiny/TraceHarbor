"""SOURCE174 explicit prospective153 contract and original118 derivation.
SOURCE_ONLY: exact153 contract; registry/mint require independent actual release.
Historical149/150/151/152 contracts/behavior delegate unchanged to prestart168.
Publication is not native admission; historical consumed152 remains refused.
"""
import pathlib,runpy,json,copy,re,ast,hashlib,os,stat
ROOT=pathlib.Path(__file__).resolve().parent
old=runpy.run_path(str(ROOT/'prestart168.py'));can=old['can'];sha=old['sha'];ORIGINAL=old['ORIGINAL']
TABLE={153:{'predecessor':152,'predecessor_state':'NATIVE152_TERMINAL','reserved_history':148}}
def contract154(value):
 if type(value)is not dict or type(value.get('direction_number'))is not int:raise TypeError('Closed explicit integer direction')
 if value['direction_number']in(149,150,151,152):return old['contract154'](value)
 expected={'schema':'TRACE174_PRESTART153_PREDECESSOR152_V1','direction_number':153,'predecessor':152,'predecessor_state':'NATIVE152_TERMINAL','reserved_history':148,'creation':'EXCLUSIVE_EMPTY_0700_BEFORE_FIRST_RX_AND_REGISTRY','consumption':'FROZEN_PARENT_CHILD_DEV_INO_UID_MODE_NO_ALIAS_BEFORE_CLOCK'}
 pins=('predecessor152_sha256','preserved151_sha256','preserved150_sha256','preserved149_sha256','reserved148_sha256')
 if set(value)!=set(expected)|set(pins)or any(type(value[k])is not type(v)or value[k]!=v for k,v in expected.items())or any(type(value[k])is not str or re.fullmatch('[a-f0-9]{64}',value[k])is None for k in pins):raise ValueError('Only explicit153 predecessor152 and all preserved slots')
 return copy.deepcopy(value)
def history154(own,config,*,before_RX):
 x=contract154(config['prestart154'])
 if x['direction_number']in(149,150,151,152):return old['history154'](own,config,before_RX=before_RX)
 if own.get('native_id')!='6acfe37b-828c-83eb-b466-7670beb64ff2'or own.get('ownership',{}).get('owner')!='TraceHarbor V1'or type(own['ownership'].get('duplicate_trace_route_owners'))is not int or own['ownership']['duplicate_trace_route_owners']!=0:raise ValueError('Exact existing sole Trace')
 for slot,key in [(152,'predecessor152_sha256'),(151,'preserved151_sha256'),(150,'preserved150_sha256'),(149,'preserved149_sha256'),(148,'reserved148_sha256')]:
  if sha(can(own.get('native'+str(slot))))!=x[key]:raise ValueError('Whole preserved history mismatch')
 if own['native152'].get('phase')!='TERMINAL':raise ValueError('Consumed152 must actually be terminal')
 if before_RX:
  if own.get('state')!='NATIVE152_TERMINAL'or 'native153'in own:raise ValueError('No consumed153/rearm or inferred predecessor')
 else:
  n=own.get('native153',{})
  if not own.get('state','').startswith('NATIVE153_')or not n.get('records')or n['records'][0].get('phase')!='RX_START':raise ValueError('Explicit153 RX lineage only')
 return x
def derive153(original,auditor_version):
 if type(original)is not str or len(original.encode())!=3827 or sha(original.encode())!=ORIGINAL or type(auditor_version)is not int or auditor_version<=0:raise ValueError('Exact008f and actual positive Auditor A only')
 pairs=[('direction118.json','direction153.json'),("'native118.records'","'native153.records'"),("'native118'","'native153'"),("'NATIVE117_TERMINAL'","'NATIVE152_TERMINAL'"),("'NATIVE118_'","'NATIVE153_'"),('CURRENT Auditor858 direction118','CURRENT Auditor'+str(auditor_version)+' direction153')]
 out=original;rows=[]
 for a,b in pairs:
  n=out.count(a)
  if n==0:raise ValueError('Missing exhaustive original118 token')
  rows.append({'before':a,'after':b,'occurrences':n});out=out.replace(a,b)
 inverse=out
 for a,b in reversed(pairs):inverse=inverse.replace(b,a)
 if inverse!=original or '118'in out or 'NATIVE151_TERMINAL'in out or 'NATIVE148_TERMINAL'in out:raise ValueError('Exhaustive inverse/original and exact predecessor')
 ast.parse(out);return out,rows

SCHEMA='TRACE174_PRESTART153_PREDECESSOR152_V1'
parent154=old['parent154'];ident154=old['ident154']

def prepare_child154(own,config):
 if config['prestart154']['direction_number'] in (149,150,151,152):return old['prepare_child154'](own,config)
 history154(own,config,before_RX=True);parent,before=parent154(config['path_roles']['holder_parent']);root=parent/'holder';root.mkdir(mode=0o700,exist_ok=False);after=parent.lstat();child=root.lstat()
 if ident154(before)!=ident154(after) or root.resolve()!=root or root.is_symlink() or not stat.S_ISDIR(child.st_mode) or child.st_uid!=os.getuid() or stat.S_IMODE(child.st_mode)!=0o700 or list(root.iterdir()):raise ValueError('Exclusive child drift; preserve attempt no adoption')
 return {'schema':SCHEMA,'direction_number':153,'predecessor':152,'reserved_history':148,'parent_path':str(parent),'parent':ident154(before),'child_path':str(root),'child':ident154(child),'expected_empty':True,'native_authority':False}

def check_child154(receipt,config,*,empty=True):
 if config['prestart154']['direction_number'] in (149,150,151,152):return old['check_child154'](receipt,config,empty=empty)
 if type(receipt) is not dict or set(receipt)!={'schema','direction_number','predecessor','reserved_history','parent_path','parent','child_path','child','expected_empty','native_authority'} or receipt['schema']!=SCHEMA or receipt['direction_number']!=153 or receipt['predecessor']!=152 or receipt['reserved_history']!=148 or receipt['native_authority'] is not False or receipt['expected_empty'] is not True:raise ValueError('Exact152 prepared child receipt')
 parent,ps=parent154(config['path_roles']['holder_parent']);root=parent/'holder'
 if receipt['parent_path']!=str(parent) or receipt['child_path']!=str(root) or receipt['parent']!=ident154(ps) or root.resolve()!=root or root.is_symlink():raise ValueError('Frozen parent/child alias or identity drift')
 child=root.lstat()
 if not stat.S_ISDIR(child.st_mode) or ident154(child)!=receipt['child'] or child.st_uid!=os.getuid() or stat.S_IMODE(child.st_mode)!=0o700 or empty and list(root.iterdir()):raise ValueError('Frozen child identity/mode/empty drift')
 return {'schema':SCHEMA,'prepared_receipt_sha256':sha(can(receipt)),'child_path':str(root),'child':ident154(child),'empty':empty,'native_authority':False}

def current_prestart154(own,config,*,empty=True):
 if config['prestart154']['direction_number'] in (149,150,151,152):return old['current_prestart154'](own,config,empty=empty)
 history154(own,config,before_RX=False);return check_child154(own['native153']['records'][0]['payload']['holder_preparation154'],config,empty=empty)

def consume_child154(receipt,config):
 if config['prestart154']['direction_number'] in (149,150,151,152):return old['consume_child154'](receipt,config)
 check_child154(receipt,config,empty=True);parent,_=parent154(config['path_roles']['holder_parent']);root=parent/'holder';pfd=fd=None
 try:
  pfd=os.open(parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);fd=os.open('holder',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=pfd)
  if ident154(os.fstat(pfd))!=receipt['parent'] or ident154(os.fstat(fd))!=receipt['child'] or os.listdir(fd):raise ValueError('Frozen152 nofollow consumption identity')
  os.mkdir('originals',0o700,dir_fd=fd);os.fsync(fd)
  if ident154(parent.lstat())!=receipt['parent'] or ident154(root.lstat())!=receipt['child']:raise ValueError('Consumption moved; no clock')
  return root
 finally:
  if fd is not None:os.close(fd)
  if pfd is not None:os.close(pfd)

def binding_selector165(doc,config):
 if type(config) is not dict or type(config.get('direction_number')) is not int or config['direction_number']!=153:raise ValueError('Closed152 selector')
 match=re.fullmatch(r'NATIVE153_([A-Z_]+)',doc.get('state',''))
 if match is None or match[1]=='TERMINAL' or type(doc.get('native153')) is not dict:raise ValueError('No consumed/foreign152 selector')
 n=doc['native153']
 if not n.get('records') or n['records'][0].get('phase')!='RX_START':raise ValueError('Actual first152 RX selector required')
 return {'number':153,'key':'native153'}

def current_binding154(base,path,version,config,require_plan=False,payload=None,_macro122=None):
 if config.get('direction_number')!=153:return old['current_binding154'](base,path,version,config,require_plan=require_plan,payload=payload,_macro122=_macro122)
 from guard174 import current_binding174
 result=current_binding174(str(path),version,config['config_path'])
 if result['binding']!=config.get('writer_binding'):raise ValueError('Exact source-derived153 writer binding')
 if require_plan:
  if _macro122 is None:raise ValueError('Only source-owned153 macro plan')
  base._check_macro122(_macro122,result,version,payload)
 return result
