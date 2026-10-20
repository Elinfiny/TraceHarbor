"""V2 acyclic static preparation and closed release validation. No effects at import.
Runtime originals are never part of an independently published static preimage.
"""
import pathlib,json,hashlib,copy,importlib.util,sys,re,math
ROOT=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('trace133_plan_control',ROOT/'control127.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
can=c.can;sha=c.sha;V2='TRACE133_STATIC_TYPED_RUNTIME_V2';ADMISSION='grouped133_admission'
STATIC={'source','manifest','request','lock','private6','custody_scope','cost_scope','dispatch_source','path_roles','limits','inventory_sha256','authority_projection_sha256','workflow'}
PATHS={'private','transfer','holder_parent','capture','library_helper','config','materialize_original'}
def closed(x,keys,label):
 if type(x) is not dict or set(x)!=set(keys):raise ValueError('Closed '+label)
 return x
def text(x,label):
 if type(x) is not str or not x or len(x)>262144:raise ValueError('Exact '+label)
 return x
def hexpin(x,n=64):
 if type(x) is not str or re.fullmatch('[a-f0-9]{'+str(n)+'}',x) is None:raise ValueError('Exact digest')
 return x
def pin(x):
 closed(x,{'bytes','sha256'},'whole pin');hexpin(x['sha256'])
 if type(x['bytes']) is not int or not 0<x['bytes']<=33554432:raise ValueError('Finite whole bytes')
def projection133(direction):
 if type(direction) is not dict:raise TypeError('Whole addressed direction')
 p=copy.deepcopy(direction);g=p.pop(ADMISSION,None)
 if any(k.startswith('grouped') and k.endswith('_admission') for k in p):raise ValueError('Old or duplicate computed admission')
 body=text(p.get('body'),'direction body').encode()
 if len(body)!=p.get('bytes') or sha(body)!=p.get('sha256') or p.get('recipient')!='TraceHarbor V1':raise ValueError('Exact addressed body and recipient')
 # Computed output digests cannot be copied into any other projected field.
 if g is not None:
  outputs=[v for k,v in g.items() if k.endswith('_sha256') and type(v) is str]
  def walk(x):
   if type(x) is dict:
    for k,v in x.items():walk(k);walk(v)
   elif type(x) is list:
    for v in x:walk(v)
   elif type(x) is str and any(v in x for v in outputs):raise ValueError('Computed admission repeated in projection: cycle')
  walk(p)
 return p
def static133(config,manifest_bytes,inventory=None):
 x=copy.deepcopy(closed(config,STATIC,'static configuration'));m=json.loads(manifest_bytes);inventory=c.inventory127() if inventory is None else inventory
 if inventory!=c.inventory127():raise ValueError('Exact whole source inventory')
 closed(x['source'],{'commit','tree','parent'},'source')
 for v in x['source'].values():hexpin(v,40)
 for k in ('manifest','request','lock'):pin(x[k])
 if x['manifest']!={'bytes':len(manifest_bytes),'sha256':sha(manifest_bytes)}:raise ValueError('Actual full manifest')
 for k,path in [('request','offline103/request.json'),('lock','offline103/requirements.lock')]:
  if x[k]!=m['source_files'][path]:raise ValueError('Canonical new request/lock source pin')
 if x['private6']!=m['counter116']['input_pins'] or len(x['private6'])!=6:raise ValueError('Exact six private pins')
 for p in x['private6'].values():pin(p)
 closed(x['custody_scope'],{'profile','root','checkpoint_key'},'custody scope')
 if x['custody_scope']['profile']!='nemotron-lightning-input-v1' or x['custody_scope']['checkpoint_key']!='native132':raise ValueError('Actual retained acquisition profile')
 text(x['custody_scope']['root'],'private custody root')
 closed(x['cost_scope'],{'model_calls','spend','host_cost_bound'},'API0 cost')
 if x['cost_scope']['model_calls']!=0 or x['cost_scope']['spend']!=0 or x['cost_scope']['host_cost_bound'] is not None and (type(x['cost_scope']['host_cost_bound']) not in (int,float) or not math.isfinite(x['cost_scope']['host_cost_bound']) or x['cost_scope']['host_cost_bound']<0):raise ValueError('Cost bound, not a grant')
 closed(x['dispatch_source'],{'script','script_sha256','tab_id'},'dispatch source');text(x['dispatch_source']['script'],'script');hexpin(x['dispatch_source']['script_sha256'])
 if sha(x['dispatch_source']['script'].encode())!=x['dispatch_source']['script_sha256'] or type(x['dispatch_source']['tab_id']) is not int:raise ValueError('Pinned dispatch script')
 if x['dispatch_source']['script'].count('__TRACE_ONCE133__')!=1:raise ValueError('One runtime once placeholder, no future descriptor')
 closed(x['path_roles'],PATHS|{'library_helper_sha256'},'path roles')
 for k in PATHS:
  p=pathlib.Path(text(x['path_roles'][k],k))
  if not p.is_absolute() or '..' in p.parts:raise ValueError('Absolute unaliased role')
 hexpin(x['path_roles']['library_helper_sha256'])
 closed(x['workflow'],{'path','step_names','baseline_entries','full_tree_entries'},'workflow')
 text(x['workflow']['path'],'workflow path')
 if type(x['workflow']['step_names']) is not list or any(type(v) is not str for v in x['workflow']['step_names']):raise ValueError('Closed workflow step list')
 for k in ('baseline_entries','full_tree_entries'):
  if type(x['workflow'][k]) is not list:raise ValueError('Whole fixed tree')
  seen=set()
  for row in x['workflow'][k]:
   closed(row,{'path','mode','type','sha'},'tree leaf');text(row['path'],'leaf path');hexpin(row['sha'],40)
   if row['path'] in seen or row['mode'] not in ('100644','100755') or row['type']!='blob':raise ValueError('Unique blob leaves')
   seen.add(row['path'])
 if x['limits']!=c.FIXED or x['inventory_sha256']!=sha(can(inventory)):raise ValueError('Whole original limits/inventory')
 hexpin(x['authority_projection_sha256']);return x
def template133(config,manifest_bytes,inventory=None):
 i=c.inventory127() if inventory is None else inventory;x=static133(config,manifest_bytes,i)
 return {'schema':'TRACE133_STATIC_PHASE_TEMPLATE','static_config_sha256':sha(can(x)),'inventory_sha256':sha(can(i)),'phases':list(c.PHASES),'semantic':list(c.SEMANTIC),'limits':copy.deepcopy(c.FIXED),'six_CAS_readback_pairs':6,'create_only_Git_primitives':12}
def prepare127(config,direction,manifest_bytes,inventory=None):
 i=c.inventory127() if inventory is None else inventory;p=projection133(direction);x=static133(config,manifest_bytes,i)
 if x['authority_projection_sha256']!=sha(can(p)):raise ValueError('Entire actual addressed scope, not a whole Auditor hash')
 t=template133(x,manifest_bytes,i)
 g={'contract':V2,'authority_projection_sha256':sha(can(p)),'static_config_sha256':sha(can(x)),'phase_template_sha256':sha(can(t)),'inventory_sha256':sha(can(i)),'manifest_sha256':sha(manifest_bytes),'inclusive_cap':i['inclusive_total'],'scope':'ONE_TYPED_UNUSED_ONCE_API0_ONLY'}
 return {'native_authority':False,'config':x,'phase_template':t,'inventory':i,'proposed_admission':g,'actual_nonce_created':False,'actual_clock_started':False}
def release133(direction,config,manifest_bytes,inventory=None):
 prepared=prepare127(config,direction,manifest_bytes,inventory)
 if direction.get(ADMISSION)!=prepared['proposed_admission']:raise PermissionError('Actual independently published exact V2 release required')
 return prepared
if __name__=='__main__':
 values=json.loads(pathlib.Path(sys.argv[1]).read_bytes());print(json.dumps(prepare127(values['config'],values['direction'],(ROOT/'manifest.json').read_bytes()),sort_keys=True,separators=(',',':')))
