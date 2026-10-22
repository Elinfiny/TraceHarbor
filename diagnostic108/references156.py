"""Bounded same-checkpoint NEW150 value deduplication; never authority.
Old nodes are never rewritten. Only inventory, phase context and evidence lists
have closed paths. Entire authenticated own document and each resolved body are
verified before use; A/B authority objects/directions/writers cannot be references.
"""
import json,hashlib,copy,re
OWN='libfile_3ee8270f03d8819188e1de1f75c3d824'
REF='TRACE156_SAME_CHECKPOINT_VALUE_V1'
DELTA='TRACE156_SAME_CHECKPOINT_PREFIX_APPEND_V1'
CONTRACT={'schema':'TRACE158_CLOSED_SAME_OWN_NEW150_VALUES_V2','checkpoint_id':OWN,'new_slot':150,'immutable_inventory_slot':149,'maximum_depth':16,'maximum_nodes':32768,'expanded_value_bytes':1048576,'metadata_representation_bytes':83886080,'new_rx_payload_bytes_max':65536,'addressed_body_bytes_max':16384,'direction_id_bytes_max':256,'authority_fields':'NEVER_REFERENCED','old_nodes':'VALUE_EXACT','external_targets':False}
INVENTORY=['native149','records',0,'payload','preparation','preloaded','inventory']
FIELDS={'context','previous_complete_originals','previous_complete_native_canonicals'}
can=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
sha=lambda b:hashlib.sha256(b).hexdigest()
def contract156(x):
 if type(x) is not dict or x!=CONTRACT:raise ValueError('Closed references156 contract')
 return copy.deepcopy(CONTRACT)
def selector156(path,kind,consumer):
 if type(path) is not list or any(type(k) not in (str,int) for k in path):raise ValueError('Exact typed JSON selector, never path/alias')
 if kind=='inventory':
  if path!=INVENTORY:raise ValueError('Only unchanged whole inventory in existing149')
 elif kind in FIELDS:
  if len(path)!=6 or path[:2]!=['native150','records'] or type(path[2]) is not int or not 1<=path[2]<consumer or path[3:]!=['payload','phase_intent127',kind]:raise ValueError('Only earlier NEW150 same-field selector')
 else:raise ValueError('No authority/ephemeral/general selector')
 return tuple(path)
def get156(doc,path):
 value=doc
 for key in path:
  if type(value) is dict and type(key) is str and key in value:value=value[key]
  elif type(value) is list and type(key) is int and 0<=key<len(value):value=value[key]
  else:raise ValueError('Absent or aliased selector')
 return value
def pin156(value):return {'canonical_bytes':len(can(value)),'sha256':sha(can(value))}
def _pin156(encoded,value):
 raw=can(value)
 if type(encoded.get('canonical_bytes')) is not int or not 0<len(raw)<=CONTRACT['expanded_value_bytes'] or len(raw)!=encoded['canonical_bytes'] or type(encoded.get('sha256')) is not str or sha(raw)!=encoded['sha256']:raise ValueError('Whole expanded canonical size/hash')
 return value
def ref156(doc,path,kind,consumer):
 selector156(path,kind,consumer);value=resolve156(doc,get156(doc,path),kind,consumer=path[2] if kind!='inventory' else consumer)
 return {'schema':REF,'checkpoint_id':OWN,'selector':copy.deepcopy(path),**pin156(value)}
def resolve156(doc,encoded,kind,*,consumer,trail=(),depth=0):
 if depth>CONTRACT['maximum_depth']:raise ValueError('Finite expansion depth/cycle')
 if type(doc) is not dict or doc.get('native_id')!='6acfe37b-828c-83eb-b466-7670beb64ff2' or doc.get('ownership',{}).get('owner')!='TraceHarbor V1':raise ValueError('Same whole owned checkpoint')
 if type(encoded) is dict and encoded.get('schema')==REF:
  if set(encoded)!={'schema','checkpoint_id','selector','canonical_bytes','sha256'} or encoded['checkpoint_id']!=OWN:raise ValueError('Closed same-own value ref')
  path=selector156(encoded['selector'],kind,consumer)
  if path in trail:raise ValueError('No cycles')
  target=get156(doc,path);value=resolve156(doc,target,kind,consumer=path[2] if kind!='inventory' else consumer,trail=trail+(path,),depth=depth+1)
  return _pin156(encoded,value)
 if type(encoded) is dict and encoded.get('schema')==DELTA:
  if kind not in ('previous_complete_originals','previous_complete_native_canonicals') or set(encoded)!={'schema','prefix','append','canonical_bytes','sha256'} or type(encoded['append']) is not list:raise ValueError('Closed evidence prefix append only')
  prefix=resolve156(doc,encoded['prefix'],kind,consumer=consumer,trail=trail,depth=depth+1)
  if type(prefix) is not list:raise ValueError('Evidence prefix list')
  return _pin156(encoded,prefix+copy.deepcopy(encoded['append']))
 expected=dict if kind in ('inventory','context') else list
 if type(encoded) is not expected:raise ValueError('Whole expanded body exact type')
 raw=can(encoded)
 if not 0<len(raw)<=CONTRACT['expanded_value_bytes']:raise ValueError('Bounded expanded value')
 nodes=0;active=set()
 def plain(x):
  nonlocal nodes
  nodes+=1
  if nodes>CONTRACT['maximum_nodes']:raise ValueError('Bounded expanded nodes')
  if type(x) in (dict,list):
   if id(x) in active:raise ValueError('No object cycles/aliases')
   active.add(id(x))
   if type(x) is dict:
    if any(type(k) is not str for k in x):raise ValueError('Plain keys')
    if x.get('schema') in (REF,DELTA):raise ValueError('No nested disguised reference')
    for v in x.values():plain(v)
   else:
    for v in x:plain(v)
   active.remove(id(x))
  elif x is not None and type(x) not in (str,int,float,bool):raise ValueError('Plain JSON only')
 plain(encoded);return copy.deepcopy(encoded)
def compact_intent156(doc,intent):
 """Original full journal intent stays full; only NEW provider postimage dedups."""
 n=doc.get('native150',{});records=n.get('records',[])
 if not records or records[0].get('phase')!='RX_START':raise ValueError('Only new150 actual RX lineage')
 index=len(records);out=copy.deepcopy(intent);previous=[(i,r['payload']['phase_intent127']) for i,r in enumerate(records) if i>0 and r.get('phase')=='PUBLISH_INTENT' and 'phase_intent127' in r.get('payload',{})]
 if previous:
  i,prior=previous[-1]
  for field in FIELDS:
   prefix=resolve156(doc,prior[field],field,consumer=i);path=['native150','records',i,'payload','phase_intent127',field]
   if field=='context':
    if prefix!=intent[field]:raise ValueError('Changed live context cannot be deduplicated')
    # Point directly to first full context, never lengthen a context chain.
    first=previous[0][0];out[field]=ref156(doc,['native150','records',first,'payload','phase_intent127',field],field,index)
   else:
    value=intent[field]
    if value[:len(prefix)]!=prefix:raise ValueError('Original evidence order/prefix drift')
    out[field]={'schema':DELTA,'prefix':ref156(doc,path,field,index),'append':copy.deepcopy(value[len(prefix):]),**pin156(value)}
 return out
def expand_intent156(doc,intent,record_index):
 out=copy.deepcopy(intent)
 for field in FIELDS:out[field]=resolve156(doc,intent[field],field,consumer=record_index)
 return out
def compact_rx156(doc,rx):
 if 'native150' in doc or doc.get('state')!='NATIVE149_TERMINAL':raise ValueError('Unused150 only; no consumed replacement')
 out=copy.deepcopy(rx);pre=out['preparation']['preloaded'];old=resolve156(doc,get156(doc,INVENTORY),'inventory',consumer=0)
 if pre['inventory']!=old:raise ValueError('Inventory exact immutable existing body')
 pre['inventory']=ref156(doc,INVENTORY,'inventory',0)
 if len(can(out))>CONTRACT['new_rx_payload_bytes_max']:raise ValueError('Bounded whole fresh compactRX')
 return out
def verify_rx156(doc,expected_inventory):
 n=doc.get('native150',{});rx=n['records'][0]['payload']
 if len(n['direction']['id'].encode())>CONTRACT['direction_id_bytes_max'] or len(n['direction']['body'].encode())>CONTRACT['addressed_body_bytes_max'] or len(can(rx))>CONTRACT['new_rx_payload_bytes_max']:raise ValueError('Bounded whole fresh150 direction/RX')
 encoded=rx['preparation']['preloaded']['inventory'];body=resolve156(doc,encoded,'inventory',consumer=0)
 if body!=expected_inventory:raise ValueError('Whole resolved inventory does not match source3255')
 return {'representation_bytes':len(can(encoded)),'expanded_body_bytes':len(can(body)),'expanded_sha256':sha(can(body)),'native_authority':False}
