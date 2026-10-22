"""Pure strict152 compatibility; never a typed snapshot, handle or grant.
Only preflight's actual CurrentSnapshot133 registry supplies native provenance.
Called before child consumption/clock/nonce, and identically at runtime mint.
"""
import pathlib,json,hashlib,runpy,re
ROOT=pathlib.Path(__file__).resolve().parent
A=runpy.run_path(str(ROOT/'authority152.py'))
H=runpy.run_path(str(ROOT/'prestart168.py'))
can=lambda v:json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
sha=lambda v:hashlib.sha256(v).hexdigest()
PROJECTION166='TRACE166_VERIFIED_AB_REPRESENTATION_PROJECTION_V1'
TELEMETRY166=(['created_at_utc'],['revision'],['previous_checkpoint_file_sha256'],['integrity','canonical_json_sha256'],['guard','epoch_checkpoint_counter'],['guard','material_checkpoints'],['operation','completed'],['operation','pending'],['operation','exact_next_safe_action'])
BOUNDARY166=['operation','effect_replay_boundary']
def _closed_path166(path):
 if type(path) is not list or any(type(k) is not str for k in path):return False
 if path in TELEMETRY166:return True
 if len(path)>=3 and path[:2]==BOUNDARY166:
  return re.fullmatch(r'master[0-9]+_[a-zA-Z0-9_]+',path[2]) is not None or len(path)>=4 and path[2] in ('recipient_outboxes','recipient_outbox_history_v29') and re.fullmatch(r'Master V[0-9]+',path[3]) is not None
 return False
def _value166(doc,path):
 value=doc
 for key in path:value=value[key]
 return value
def _check_values166(changes,admission,current):
 # Verify complete values, including the producer's exact full-value-reference.
 # Never parse caller text or trust a classification as permission.
 for change in changes:
  for side,doc,proof in (('A',admission,'admission_A'),('B',current,'current_B')):
   try:value=_value166(doc,change['path'])
   except KeyError:
    if change[side+'_value']!={'absent':True}:raise ValueError('Exact absent comparison value')
    continue
   raw=can(value);expected=value if len(raw)<=1024 else {'full_value_reference':{'proof_object':proof,'decoded_json_path':change['path'],'canonical_value_bytes':len(raw),'canonical_value_sha256':sha(raw),'retention':'WHOLE_AUTHENTIC_DOCUMENT_PINNED_IN_PROOF_NOT_TRUNCATED'}}
   if change[side+'_value']!=expected or change['before_sha256' if side=='A' else 'after_sha256']!=sha(raw):raise ValueError('Exact proof object/path/full value hash and size')
def representation166(admission,current,changes):
 """Pure representation check; no authentication, typed registry or capability.
 Inputs at the native producer come exclusively from verify152's actual A/B.
 RAM tests of object JSON use this layer without manufacturing provider proofs.
 """
 if type(admission) is not dict or type(current) is not dict or type(changes) is not list:raise TypeError('Whole A/B document values and comparison')
 if A['protected152'](admission)!=A['protected152'](current):raise ValueError('Closed protected152 comparison, including all unknown fields')
 if changes!=A['semantic_diff152'](admission,current):raise ValueError('Exact original producer152 semantic differences')
 _check_values166(changes,admission,current)
 normalized=[];descriptors={};decoded=[]
 for name,doc in (('admission_A',admission),('current_B',current)):
  value=doc['operation']['effect_replay_boundary']
  if type(value) not in (str,dict):raise TypeError('Only actual serialized or object JSON boundary')
  boundary=A['boundary152'](doc)
  if type(boundary) is not dict:raise TypeError('Whole decoded boundary object')
  whole=dict(doc);whole['operation']=dict(doc['operation']);whole['operation']['effect_replay_boundary']=boundary;decoded.append(whole)
  descriptors[name]={'proof_object':name,'canonical_document':{'bytes':len(can(doc)),'sha256':sha(can(doc))},'boundary_representation':'JSON_STRING' if type(value) is str else 'JSON_OBJECT','encoded_boundary':{'bytes':len(can(value)),'sha256':sha(can(value))},'decoded_boundary':{'bytes':len(can(boundary)),'sha256':sha(can(boundary))}}
 normalized=A['semantic_diff152'](*decoded);_check_values166(normalized,*decoded)
 if len(normalized)>512 or any(not _closed_path166(row['path']) for row in normalized):raise ValueError('Only closed Master histories/outboxes and root telemetry')
 return {'documents':descriptors,'original_diff_sha256':sha(can(changes)),'original_diff_count':len(changes),'normalized_differences':normalized}
def project166(raw_admission,raw_current,evidence):
 """Preflight-only native call, AFTER verify152; pure calls grant nothing.
 Raw hashes/bytes/self bind both complete source-authenticated documents.
 Caller-supplied dictionaries can never install CurrentSnapshot133 entries.
 """
 docs=[]
 for raw,side in ((raw_admission,'admission_A'),(raw_current,'current_B')):
  if type(raw) is not bytes:raise TypeError('Whole original authenticated document bytes')
  proof=evidence[side][A['AUDIT']]
  if len(raw)!=proof['bytes'] or sha(raw)!=proof['sha256']:raise ValueError('Whole authentic A/B raw proof hash/size')
  doc=json.loads(raw);q=dict(doc);q['integrity']=dict(doc['integrity']);expected=q['integrity']['canonical_json_sha256'];q['integrity']['canonical_json_sha256']=None
  if expected!=proof['self_sha256'] or sha(can(q))!=expected:raise ValueError('Whole authentic A/B self hash')
  docs.append(doc)
 value=representation166(*docs,evidence['allowed_semantic_diff'])
 for side in ('admission_A','current_B'):value['documents'][side]['proof']=evidence[side][A['AUDIT']]
 result={'schema':PROJECTION166,'authority_evidence_sha256':sha(can(evidence)),**value,'native_authority':False}
 if len(can(result))>65536:raise ValueError('Whole compatibility projection exceeds fixed65536 cap; no truncation')
 require_projection166(evidence,result)
 return result
def require_projection166(evidence,projection):
 """Consume only the projection sealed inside the source-owned typed snapshot.
 This pure predicate is not an authority producer. Actual complete values were
 checked by project166; the registry, never a flag/dict, establishes provenance.
 """
 keys={'schema','authority_evidence_sha256','documents','original_diff_sha256','original_diff_count','normalized_differences','native_authority'}
 if type(projection) is not dict or set(projection)!=keys or projection['schema']!=PROJECTION166 or projection['native_authority'] is not False or len(can(projection))>65536:raise ValueError('Exact bounded source representation projection')
 changes=evidence['allowed_semantic_diff'];norm=projection['normalized_differences']
 if projection['authority_evidence_sha256']!=sha(can(evidence)) or projection['original_diff_sha256']!=sha(can(changes)) or type(projection['original_diff_count']) is not int or projection['original_diff_count']!=len(changes):raise ValueError('Actual verified comparison evidence binding')
 if type(norm) is not list or len(norm)>512 or any(type(row) is not dict or not _closed_path166(row.get('path')) or row.get('authority_classification')!='EXPLICIT_NON_AUTHORITATIVE_MASTER_HISTORY_OR_TELEMETRY' for row in norm):raise ValueError('Closed normalized difference paths, no len2 boundary waiver')
 ds=projection['documents']
 if type(ds) is not dict or set(ds)!={'admission_A','current_B'}:raise ValueError('Both whole actual document identities')
 for side in ('admission_A','current_B'):
  d=ds[side]
  if type(d) is not dict or set(d)!={'proof_object','proof','canonical_document','boundary_representation','encoded_boundary','decoded_boundary'} or d['proof_object']!=side or d['proof']!=evidence[side][A['AUDIT']] or d['boundary_representation'] not in ('JSON_STRING','JSON_OBJECT'):raise ValueError('Whole exact source-authenticated document/proof binding')
  for name in ('canonical_document','encoded_boundary','decoded_boundary'):
   pin=d[name]
   if type(pin) is not dict or set(pin)!={'bytes','sha256'} or type(pin['bytes']) is not int or not 0<pin['bytes']<=67108864 or type(pin['sha256']) is not str or re.fullmatch('[0-9a-f]{64}',pin['sha256']) is None:raise ValueError('Exact non-Boolean whole document/value pins')
 original_other=[x for x in changes if x['path'][:2]!=BOUNDARY166];normalized_other=[x for x in norm if x['path'][:2]!=BOUNDARY166]
 if original_other!=normalized_other or any(not _closed_path166(x['path']) for x in original_other):raise ValueError('Exact whole nonboundary telemetry, no unknown root permission')
 boundary=[x for x in changes if x['path'][:2]==BOUNDARY166]
 if all(d['boundary_representation']=='JSON_OBJECT' for d in ds.values()):
  if boundary!=[x for x in norm if x['path'][:2]==BOUNDARY166]:raise ValueError('Exact already-object boundary differences')
 elif boundary:
  if len(boundary)!=1 or boundary[0]['path']!=BOUNDARY166 or boundary[0]['kind'] not in ('VALUE','TYPE'):raise ValueError('Exact original serialized boundary producer representation')
  row=boundary[0]
  for label,side,hashkey in (('A','admission_A','before_sha256'),('B','current_B','after_sha256')):
   pin=ds[side]['encoded_boundary'];expected={'full_value_reference':{'proof_object':side,'decoded_json_path':BOUNDARY166,'canonical_value_bytes':pin['bytes'],'canonical_value_sha256':pin['sha256'],'retention':'WHOLE_AUTHENTIC_DOCUMENT_PINNED_IN_PROOF_NOT_TRUNCATED'}}
   if pin['bytes']<=1024 or row[label+'_value']!=expected or row[hashkey]!=pin['sha256']:raise ValueError('Exact serialized full-value-reference proof/hash/size/path binding')
  if not any(x['path'][:2]==BOUNDARY166 for x in norm) and ds['admission_A']['decoded_boundary']!=ds['current_B']['decoded_boundary']:raise ValueError('Exact equivalent decoded representation')
 elif any(x['path'][:2]==BOUNDARY166 for x in norm) or ds['admission_A']['encoded_boundary']!=ds['current_B']['encoded_boundary'] or ds['admission_A']['decoded_boundary']!=ds['current_B']['decoded_boundary']:raise ValueError('No fabricated normalized boundary differences')
 return True
def validate165(release,config,manifest_bytes,snapshot):
 if type(snapshot) is not dict or type(release) is not dict or type(config) is not dict:raise TypeError('Whole source-produced snapshot data')
 c=H['contract154'](config['prestart154'])
 if type(c['direction_number']) is not int or c['direction_number']!=152:raise ValueError('Only explicitly admitted152, never consumed149/151')
 A['contract152'](config['authority152'])
 if snapshot.get('direction')!=release or snapshot.get('ownership')!='TraceHarbor V1' or snapshot.get('direction_number')!=152:raise ValueError('Exact source-produced direction and sole owner')
 if release.get('recipient')!='TraceHarbor V1' or release.get('native_admission') is not True or not release.get('id','').startswith('V29-TRACE-152-'):raise ValueError('Authentic separately published152 addressed release required')
 prepared=runpy.run_path(str(ROOT/'plan127.py'))['release133'](release,config,manifest_bytes)
 auth=snapshot.get('authority152')
 fields={'schema','admission_A','current_B','allowed_semantic_diff','immutable_guard_auditor_sha256','current_authority_auditor_sha256','native_authority'}
 if type(auth) is not dict or set(auth)!=fields or auth['schema']!=A['CONTRACT'] or auth['native_authority'] is not False:raise ValueError('Entire unchanged canonical V2 verified A/B evidence')
 ids={A['AUDIT'],A['POLICY'],A['ROUTE']}
 if set(auth['admission_A'])!=ids or set(auth['current_B'])!=ids|{A['OWN']}:raise ValueError('Whole actual immutableA and currentB proof sets')
 for side in ('admission_A','current_B'):
  for stable,p in auth[side].items():
   if type(p) is not dict or p.get('library_file_id')!=stable or p.get('ALLattrs')!='PASS' or type(p.get('version')) is not int or p['version']<0 or type(p.get('bytes')) is not int or p['bytes']<=0 or not isinstance(p.get('file_id'),str) or not p['file_id'].startswith('file_') or any(not isinstance(p.get(k),str) or re.fullmatch('[0-9a-f]{64}',p[k]) is None for k in ('sha256','self_sha256')):raise ValueError('Actual complete positive identity and allattrs proof data')
 provenance=snapshot.get('compatibility165');projection=snapshot.get('compatibility_projection166')
 require_projection166(auth,projection)
 if provenance!={'history':c,'static_config_sha256':sha(can(config)),'source':config['source'],'authority_evidence_sha256':sha(can(auth)),'projection166_sha256':sha(can(projection))}:raise ValueError('Exact whole history/static/source/verified authority representation from current typed preflight')
 aa=auth['admission_A'];bb=auth['current_B'];ap=aa[A['AUDIT']]
 if auth['immutable_guard_auditor_sha256']!=ap['sha256'] or snapshot.get('auditor_sha256')!=ap['sha256'] or auth['current_authority_auditor_sha256']!=bb[A['AUDIT']]['sha256'] or bb[A['AUDIT']]['version']<ap['version']:raise ValueError('Exact immutableA/currentB hash/version binding')
 for stable in (A['POLICY'],A['ROUTE']):
  if aa[stable]!=bb[stable]:raise ValueError('Whole verified policy/route drift')
 diffs=auth['allowed_semantic_diff']
 if type(diffs) is not list or len(diffs)>512 or any(type(x) is not dict or x.get('authority_classification')!='EXPLICIT_NON_AUTHORITATIVE_MASTER_HISTORY_OR_TELEMETRY' for x in diffs):raise ValueError('Closed verified152 difference evidence')
 # The original serialized diff is kept intact, alongside the closed decoded
 # representation produced from the actual authenticated documents in preflight.
 if snapshot.get('source_verification')!={'Auditor_V28_checkpoint.json':ap}:raise ValueError('Original118 immutable source proof retained')
 wb=snapshot.get('writer_binding')
 if type(wb) is not dict or wb.get('auditor_version')!=ap['version'] or wb.get('direction_number')!=152 or wb.get('direction_id')!=release['id'] or wb.get('direction_bytes')!=release['bytes'] or wb.get('direction_sha256')!=release['sha256'] or wb.get('writer_sha256')!=snapshot.get('writer_sha256') or wb.get('original_writer_sha256')!=H['ORIGINAL']:raise ValueError('Whole source-verified immutable writer152 binding')
 current=snapshot.get('current_source_verification152')
 if type(current) is not dict or {v.get('library_file_id'):v for v in current.values()}!=bb or snapshot.get('own_version')!=bb[A['OWN']]['version']:raise ValueError('Whole actual currentB snapshot proof binding')
 receipt=snapshot.get('holder_preparation154');pre=snapshot.get('prestart154')
 expected={'schema','direction_number','predecessor','reserved_history','parent_path','parent','child_path','child','expected_empty','native_authority'}
 if type(receipt) is not dict or set(receipt)!=expected or receipt['schema']!=c['schema'] or receipt['direction_number']!=152 or receipt['predecessor']!=151 or receipt['reserved_history']!=148 or receipt['expected_empty'] is not True or receipt['native_authority'] is not False:raise ValueError('Exact whole152/pre151/reserved148 frozen receipt')
 for ident in (receipt['parent'],receipt['child']):
  if type(ident) is not dict or set(ident)!={'dev','ino','uid','mode','type'} or ident['type']!='directory' or ident['mode']!=0o700 or any(type(ident[k]) is not int or ident[k]<0 for k in ('dev','ino','uid','mode')):raise ValueError('Exact frozen directory metadata, never Boolean identities')
 if receipt['parent_path']!=config['path_roles']['holder_parent'] or receipt['child_path']!=str(pathlib.Path(receipt['parent_path'])/'holder'):raise ValueError('Exact bound child locator')
 if type(pre) is not dict or set(pre)!={'schema','prepared_receipt_sha256','child_path','child','empty','native_authority'} or pre['schema']!=c['schema'] or pre['prepared_receipt_sha256']!=sha(can(receipt)) or pre['child_path']!=receipt['child_path'] or pre['child']!=receipt['child'] or pre['empty'] is not True or pre['native_authority'] is not False:raise ValueError('Full prepared receipt hash and exact source-produced prestart proof')
 # All original once/expiry/nonce/clock checks remain at mint, unmodified.
 return {'schema':'TRACE165_PURE_SNAPSHOT_COMPATIBILITY_V1','direction':152,'predecessor':151,'authority_contract':A['CONTRACT'],'static_config_sha256':sha(can(config)),'phase_template_sha256':sha(can(prepared['phase_template'])),'prepared_receipt_sha256':pre['prepared_receipt_sha256'],'native_authority':False}
