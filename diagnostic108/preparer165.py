"""Metadata preparation only for a later authentic151/consumed predecessor150 release.
Current SOURCE165 is not that release. No native registration/start at import/call.
"""
import pathlib,runpy,json,os,hashlib,copy
ROOT=pathlib.Path(__file__).resolve().parent
def prepare165(number,original,roles,original_writer,legacy_preparer):
 a=runpy.run_path(str(ROOT/'authority152.py'));h=runpy.run_path(str(ROOT/'prestart165.py'));can=a['can'];sha=a['sha'];root=pathlib.Path(roles['private'])
 if number!=151 or sha(pathlib.Path(legacy_preparer).read_bytes())!='06e4f54b61670787e85e8de61e47779eb487e4815fbaff6a3d8af979eed8824b':raise ValueError('Explicit151 and exact original7266 retained')
 ts=original.get('structuredContent',{}).get('transfers',[])
 if original.get('isError') or original['structuredContent'].get('unavailable_items') or len(ts)!=4 or {t['library_file_id'] for t in ts}!=set(a['IDS']):raise ValueError('Authentic whole four-file preparation input')
 docs={};proof={}
 for t in ts:docs[t['library_file_id']],proof[t['library_file_id']]=a['proof152'](t['workspace_path'],t,original=original)
 boundary=a['boundary152'](docs[a['AUDIT']]);direction=boundary['recipient_outboxes']['TraceHarbor V1']
 if not direction['id'].startswith('V29-TRACE-151-') or direction.get('native_admission') is not True:raise ValueError('Future genuine151 addressed release required; SOURCE154 grants none')
 if len(direction['body'].encode())>16384 or len(direction['id'].encode())>256:raise ValueError('Bounded actual fresh151 addressedbody before RX')
 packet=boundary[direction['source_branch']]['release_packet'];config=packet['static_CONFIG'];manifest=(ROOT/'manifest.json').read_bytes()
 if config['path_roles']!=roles:raise ValueError('Exact independently bound151 role paths')
 runpy.run_path(str(ROOT/'plan127.py'))['release133'](direction,config,manifest,packet['preloaded']['inventory']);a['compare152'](docs[a['AUDIT']],docs[a['AUDIT']],proof,proof,docs[a['ROUTE']],docs[a['ROUTE']],docs[a['POLICY']],docs[a['POLICY']],direction,config,manifest);own=docs[a['OWN']];h['history154'](own,config,before_RX=True)
 raw=pathlib.Path(original_writer).read_bytes();adapt,derivation=h['derive151'](raw.decode(),proof[a['AUDIT']]['version']);layout={};roots={}
 for role in ('private','transfer','holder_parent'):
  path=pathlib.Path(roles[role]);q,s=h['parent154'](path);roots[role]=q;layout[role]={'path':str(q),'dev':s.st_dev,'ino':s.st_ino,'uid':s.st_uid,'type':'directory'}
 if any(x==y or x.is_relative_to(y) or y.is_relative_to(x) for i,x in enumerate(roots.values()) for j,y in enumerate(roots.values()) if i<j):raise ValueError('Three exact disjoint owned roles')
 holder=h['prepare_child154'](own,config)
 def put(path,raw):
  fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
  with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 paths={}
 for stable,name in ((a['AUDIT'],'Auditor_admission_A.json'),(a['POLICY'],'Policy_admission_A.json'),(a['ROUTE'],'Route_admission_A.json')):
  t=next(x for x in ts if x['library_file_id']==stable);source=pathlib.Path(t['workspace_path']);target=root/name;put(target,source.read_bytes())
  for attr in os.listxattr(source):os.setxattr(target,attr,os.getxattr(source,attr))
  _,p=a['proof152'](target,t,private=True)
  if p!=proof[stable]:raise ValueError('Exact whole immutable A copies and ALLattrs')
  paths[stable]=str(target)
 writer=root/'admin151.py';put(writer,adapt.encode());binding={'direction_number':151,'direction_id':direction['id'],'direction_bytes':direction['bytes'],'direction_sha256':direction['sha256'],'auditor_path':paths[a['AUDIT']],'auditor_version':proof[a['AUDIT']]['version'],'binding_root':str(root),'original_writer_path':str(pathlib.Path(original_writer)),'original_writer_sha256':h['ORIGINAL'],'writer_path':str(writer),'writer_sha256':sha(adapt.encode()),'transfer_layout':layout}
 receipt=root/'admission-A-materialize.original.json';put(receipt,can(original));authority={'schema':a['CONTRACT'],'policy_path':paths[a['POLICY']],'route_path':paths[a['ROUTE']],'proofs':{k:proof[k] for k in (a['AUDIT'],a['POLICY'],a['ROUTE'])},'materialize_original':{'path':str(receipt),'bytes':receipt.stat().st_size,'sha256':sha(receipt.read_bytes())}}
 for name,obj in [('direction151.json',direction),('source-verification.json',{'Auditor_V28_checkpoint.json':proof[a['AUDIT']]}),('holder-preparation154.json',holder)]:put(root/name,can(obj))
 h['check_child154'](holder,config,empty=True)
 return {'writer_binding':binding,'authority_admission152':authority,'source_verification':{'Auditor_V28_checkpoint.json':proof[a['AUDIT']]},'holder_preparation154':holder,'writer_derivation154':derivation,'current_sources_before_RX':proof,'native_authority':False}


def prepare_rx165(own,rx,direction,config):
 """Exact actual future RX assembler, data only; caller still must genuineCAS.
 No native entry here. Capacity recomputes wholepostimage after all fields exist.
 """
 r=runpy.run_path(str(ROOT/'references165.py'));h=runpy.run_path(str(ROOT/'prestart165.py'));h['history154'](own,config,before_RX=True)
 if direction.get('native_admission') is not True or not direction['id'].startswith('V29-TRACE-151-') or rx['writer_binding']['direction_id']!=direction['id']:raise ValueError('Genuine independent fresh151 only')
 compact=r['compact_rx165'](own,rx);model=copy.deepcopy(own);model['state']='NATIVE151_RX_START';model['native151']={'direction':direction,'records':[{'phase':'RX_START','payload':compact}],'phase_history':[{'phase':'RX','utc':'2099-12-31T23:59:59.999999+00:00','actual_own_version':9999999999999999999},{'phase':'START','utc':'2099-12-31T23:59:59.999999+00:00','actual_own_version':9999999999999999999}],'source_verification':rx['source_verification'],'current_selector':'native151.records','policy_adopted':101,'previous_checkpoint':{'version':9999999999999999999,'raw_sha256':'f'*64,'self_sha256':'f'*64},'writer_sha256':'f'*64}
 # Original008f adds two events and updatesguard/self; conservative complete
 # source-shaped additions are included, rather than subtracting an estimate.
 for phase in ('RX','START'):model['events'].append({'phase':phase,'utc':'2099-12-31T23:59:59.999999+00:00','delivery_id':direction['id'],'own_version':9999999999999999999,'source':'CURRENT Auditor9999999999999999999 direction151','scope':'SAME_HOST_PRODUCER_COUNTER_CONTRACT_REVIEW_SOURCE'})
 model['guard'].update(operation_id=direction['id'],operation_state='RX_START',epoch_checkpoint_counter=9999999999999999999,checkpoint_fresh='EXACT_CAS_AND_PINNED_FULLBYTE_SELF_ALLATTRS_READBACK');model['self_sha256']='f'*64
 capacity=runpy.run_path(str(ROOT/'capacity165.py'))['capacity165'](model,config);return {'compact_RX':compact,'whole_actual_size_preRX_capacity':capacity,'native_authority':False}
