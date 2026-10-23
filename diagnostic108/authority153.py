"""Closed A=immutable admission / B=authenticated current authority contract.
No import, pure comparison or supplied dictionary creates a native capability.
Provider originals remain separate; only source preflight installs its snapshot.
"""
import copy,json,hashlib,os,pathlib,stat,re,time
AUDIT='libfile_f87a6a307f70819194e0af0fa453afd1'
POLICY='libfile_6f69ae483b088191a1fffefca617bbd5'
ROUTE='libfile_8377022600088191993dc06bfba93b7b'
OWN='libfile_3ee8270f03d8819188e1de1f75c3d824'
IDS=(OWN,AUDIT,POLICY,ROUTE)
AUDIT_CHAT='6ad7ffbf-f990-83eb-8a66-57312f48957f'
MASTER_CHAT='6ad62106-24c8-83eb-8a6b-d100a31f25cf'
TRACE_CHAT='6acfe37b-828c-83eb-b466-7670beb64ff2'
CONTRACT='TRACE158_TWO_AUTHORITY_OBJECTS_V2'
can=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
sha=lambda b:hashlib.sha256(b).hexdigest()
def boundary152(doc):
 b=doc['operation']['effect_replay_boundary'];return json.loads(b) if isinstance(b,str) else copy.deepcopy(b)
def contract152(x):
 expected={'schema':CONTRACT,'admission_snapshot':'IMMUTABLE_BEFORE_RX','current_snapshot':'AUTHENTIC_FRESH_WHOLE_PROVIDER','policy_change':'REFUSE_ANY_WHOLE_POLICY_CHANGE','route_change':'REFUSE_ANY_WHOLE_ROUTE_CHANGE','allowed_auditor_diff':'CLOSED_MASTER_HISTORY_AND_TELEMETRY_ONLY','precreate_refresh':'PARALLEL_WITH_PRECEDING_READ_SAME15S_ALL13_CREATES','metadata_each_max':67108864,'private_each_max':33554432,'trace_metadata_envelope':__import__('runpy').run_path(str(pathlib.Path(__file__).resolve().parent/'envelope158.py'))['CONTRACT']}
 if x!=expected:raise ValueError('Exact independently reviewed152 authority contract')
 return copy.deepcopy(expected)
def proof152(path,transfer,*,private=False,original=None):
 # Explicit153 caller only. Keep the original whole provider/self/ALLattrs
 # predicates and seal its physical ancestor chain through their last read.
 from snapshot174 import Whole173
 limit=33554432 if private else 83886080 if transfer.get('library_file_id')==OWN else 67108864
 resource=Whole173(path,limit)
 try:
  result=__import__('runpy').run_path(str(pathlib.Path(__file__).resolve().parent/'envelope158.py'))['proof158'](path,transfer,private=private,original=original)
  if result[1]['sha256']!=resource.raw_sha:raise ValueError('Same physical source proof bytes')
  resource.reseal173();return result
 finally:resource.close173()
def semantic_diff152(a,b):
 changes=[]
 def walk(x,y,path):
  if type(x)!=type(y):changes.append({'path':path,'kind':'TYPE','before_sha256':sha(can(x)),'after_sha256':sha(can(y))});return
  if isinstance(x,dict):
   for k in sorted(set(x)|set(y)):
    if k not in x or k not in y:changes.append({'path':path+[k],'kind':'ADD' if k not in x else 'REMOVE','before_sha256':None if k not in x else sha(can(x[k])),'after_sha256':None if k not in y else sha(can(y[k]))})
    else:walk(x[k],y[k],path+[k])
  elif x!=y:changes.append({'path':path,'kind':'LIST' if isinstance(x,list) else 'VALUE','before_sha256':sha(can(x)),'after_sha256':sha(can(y))})
 walk(a,b,[])
 for change in changes:
  for side,doc in [('A',a),('B',b)]:
   value=doc
   try:
    for key in change['path']:value=value[key]
   except KeyError:change[side+'_value']={'absent':True};continue
   raw=can(value)
   change[side+'_value']=value if len(raw)<=1024 else {'full_value_reference':{'proof_object':'admission_A' if side=='A' else 'current_B','decoded_json_path':change['path'],'canonical_value_bytes':len(raw),'canonical_value_sha256':sha(raw),'retention':'WHOLE_AUTHENTIC_DOCUMENT_PINNED_IN_PROOF_NOT_TRUNCATED'}}
  change['authority_classification']='EXPLICIT_NON_AUTHORITATIVE_MASTER_HISTORY_OR_TELEMETRY'
 return changes
def protected152(doc):
 """Closed explicitly non-authoritative telemetry and other-recipient history.
 Every other byte-for-value field, including unknown fields, stays protected.
 Notes cannot supersede the mandatory addressed outbox/security/role/policy.
 """
 d=copy.deepcopy(doc);d['operation']['effect_replay_boundary']=boundary152(doc)
 for k in ('created_at_utc','revision','previous_checkpoint_file_sha256'):d.pop(k,None)
 d['integrity'].pop('canonical_json_sha256',None)
 for k in ('epoch_checkpoint_counter','material_checkpoints'):d['guard'].pop(k,None)
 for k in ('completed','pending','exact_next_safe_action'):d['operation'].pop(k,None)
 b=d['operation']['effect_replay_boundary']
 for k in list(b):
  if re.fullmatch(r'master[0-9]+_[a-zA-Z0-9_]+',k):b.pop(k)
 for k in ('recipient_outboxes','recipient_outbox_history_v29'):
  if k in b:
   for recipient in list(b[k]):
    if re.fullmatch(r'Master V[0-9]+',recipient):b[k].pop(recipient)
 return d
def compare152(admission,current,proofA,proofB,routeA,routeB,policyA,policyB,direction,config,manifest_bytes):
 contract152(config['authority152'])
 if config['prestart154']['direction_number']!=153 or not direction.get('id','').startswith('V29-TRACE-153-'):raise ValueError('Explicit153 actual addressed release only')
 for pf in (proofA,proofB):
  if pf[AUDIT]['library_file_id']!=AUDIT or pf[POLICY]['library_file_id']!=POLICY or pf[ROUTE]['library_file_id']!=ROUTE or any(pf[k]['ALLattrs']!='PASS' for k in (AUDIT,POLICY,ROUTE)):raise ValueError('Exact separate authenticated A/B stable identities')
 if proofB[AUDIT]['version']<proofA[AUDIT]['version']:raise ValueError('Retired/stale current snapshot cannot replace admission')
 if policyA!=policyB or any(proofA[POLICY][k]!=proofB[POLICY][k] for k in ('version','bytes','sha256','self_sha256')):raise ValueError('Policy drift requires independent review')
 if routeA!=routeB or any(proofA[ROUTE][k]!=proofB[ROUTE][k] for k in ('version','bytes','sha256','self_sha256')):raise ValueError('Current canonical route drift')
 routes=routeB['routes']
 if routes['Auditor']!={'chat_id':AUDIT_CHAT,'checkpoint':AUDIT,'generation':13,'name':'Auditor V29','url':'https://chatgpt.com/c/'+AUDIT_CHAT} or routes['Master']!={'chat_id':MASTER_CHAT,'checkpoint':'libfile_e7751f8b04808191b584105301103a28','generation':9,'name':'Master V59','url':'https://chatgpt.com/c/'+MASTER_CHAT}:raise ValueError('Accepted actual role/generation/Master identity')
 ba=boundary152(admission);bb=boundary152(current)
 for doc,b in ((admission,ba),(current,bb)):
  ctx=b['operational_context_current']
  if doc['chat_id']!=AUDIT_CHAT or ctx['state']!='ACCEPTED' or ctx['name']!='Auditor V29' or ctx['route_generation']!=13 or ctx['native_chat_id']!=AUDIT_CHAT or ctx['own']!=AUDIT or ctx['transport_source']['route']!=routes['Auditor']:raise ValueError('Actual accepted CURRENT Auditor identity/role/generation')
  if b['recipient_outboxes']['TraceHarbor V1']!=direction or direction.get('native_admission') is not True or direction['recipient']!='TraceHarbor V1':raise ValueError('Addressed revocation/replacement/id/body/G')
  body=direction['body'].encode()
  if sha(body)!=direction['sha256'] or len(body)!=direction['bytes']:raise ValueError('Whole exact addressed body')
  packet=b[direction['source_branch']]['release_packet']
  if packet['direction']!=direction or packet['static_CONFIG']!=config or packet['phase_template']['static_config_sha256']!=sha(can(config)) or packet['preloaded']['currentNativeAdmission']!=direction['grouped146_admission'] or packet['preloaded']['inventorySha256']!=config['inventory_sha256'] or packet['source_bundle']['sha256']!=sha(packet['source_bundle']['full_source_utf8'].encode()):raise ValueError('Whole released packet/static/phase/preloaded/source exact')
  if config['manifest']!={'bytes':len(manifest_bytes),'sha256':sha(manifest_bytes)}:raise ValueError('Actual current manifest/source pin')
 packet=ba[direction['source_branch']]['release_packet'];pre=packet['preloaded'];root=pathlib.Path(__file__).resolve().parent
 if sha(can(pre['inventory']))!=config['inventory_sha256'] or pre['configPath']!=config['path_roles']['config'] or pre['captureDirectory']!=config['path_roles']['capture'] or pre['preflightDirectory']!=str(pathlib.Path(config['path_roles']['private'])/'preflight') or pre['reviewedRoot']!=str(root.parent):raise ValueError('Exact whole actual preloaded source/config/inventory roles')
 if packet['source_bundle']!=__import__('runpy').run_path(str(root/'render_controller174.py'))['render146']():raise ValueError('Whole actual source-bound lexical caller bundle')
 if packet['phase_template']!=__import__('runpy').run_path(str(root/'plan127.py'))['template133'](config,manifest_bytes,pre['inventory']):raise ValueError('Exact full actual phase template')
 if ba[direction['source_branch']]['release_packet']!=bb[direction['source_branch']]['release_packet'] or protected152(admission)!=protected152(current):raise ValueError('Unrelated-only closed semantic difference; protected authority drift')
 for k in ('epoch_checkpoint_counter','material_checkpoints'):
  if type(current['guard'][k]) is not int or current['guard'][k]<admission['guard'][k]:raise ValueError('Regressed authority telemetry')
 # No large documents or secrets are placed into runtime/IPC evidence.
 evidence={'schema':CONTRACT,'admission_A':copy.deepcopy(proofA),'current_B':copy.deepcopy(proofB),'allowed_semantic_diff':semantic_diff152(admission,current),'immutable_guard_auditor_sha256':proofA[AUDIT]['sha256'],'current_authority_auditor_sha256':proofB[AUDIT]['sha256'],'native_authority':False}
 if len(evidence['allowed_semantic_diff'])>512 or len(can(evidence))>65536:raise ValueError('Whole semantic authority proof exceeds fixed65536 evidence cap; no truncation')
 return evidence
def admission152(own):
 key='native'+own['state'].split('_')[0][6:];n=own[key];binding=n['records'][0]['payload']['writer_binding'];a=n['records'][0]['payload']['authority_admission152']
 if a['schema']!=CONTRACT or own['native_id']!=TRACE_CHAT or own['ownership']['owner']!='TraceHarbor V1' or own['ownership']['duplicate_trace_route_owners']!=0:raise ValueError('Sole immutable RX admission152')
 ref=a['materialize_original'];p=pathlib.Path(ref['path']);s=p.lstat()
 if p.resolve()!=p or p.is_symlink() or s.st_uid!=os.getuid() or s.st_mode&0o077 or s.st_nlink!=1 or not 0<s.st_size<=33554432:raise ValueError('Immutable A materialization receipt custody')
 root=pathlib.Path(binding['binding_root'])
 if not p.is_relative_to(root) or not pathlib.Path(a['policy_path']).is_relative_to(root) or not pathlib.Path(a['route_path']).is_relative_to(root):raise ValueError('Immutable A must stay under original binding root')
 raw=p.read_bytes()
 if sha(raw)!=ref['sha256'] or len(raw)!=ref['bytes']:raise ValueError('Immutable A receipt original')
 original=json.loads(raw);ts=original['structuredContent']['transfers']
 if original.get('isError') or original['structuredContent'].get('unavailable_items') or {t['library_file_id'] for t in ts}!=set(IDS) or len(ts)!=4:raise ValueError('Whole four A source receipt')
 docs={};proof={}
 for stable,path in ((AUDIT,binding['auditor_path']),(POLICY,a['policy_path']),(ROUTE,a['route_path'])):
  transfer=next(t for t in ts if t['library_file_id']==stable);docs[stable],proof[stable]=proof152(path,transfer,private=True,original=original)
 if proof[AUDIT]!=n['source_verification']['Auditor_V28_checkpoint.json'] or proof!=a['proofs']:raise ValueError('Immutable original118 A proof, never current B substitution')
 return docs,proof
def verify152(own,current_docs,current_proofs,config,manifest_bytes):
 key='native'+own['state'].split('_')[0][6:];adocs,aproof=admission152(own);direction=own[key]['direction']
 return compare152(adocs[AUDIT],current_docs[AUDIT],aproof,current_proofs,adocs[ROUTE],current_docs[ROUTE],adocs[POLICY],current_docs[POLICY],direction,config,manifest_bytes)

def require_predecessor152(id,phase,version,seq,latest):
 expected='precreate' if id=='dispatch136/create-ref' else phase+'/readback' if id.endswith('/blob') else id.rsplit('/',1)[0]+'/'+{'tree':'blob','commit':'tree','ref':'commit'}[id.rsplit('/',1)[1]]+'/proof'
 if latest is None or latest['scope']!=expected or latest['own_version']!=version or latest['seq']!=seq:raise ValueError('Exact immediately preceding fresh152 current authorization before EVERY Git create')
 return expected
