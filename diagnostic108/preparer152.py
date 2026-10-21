"""Prepare A before one later independently released RX147, never at import.
Requires the whole genuine provider four-file original and exact reviewed
7266 preflight helper. No native registry/holder/clock/once is created.
"""
import pathlib,json,os,copy,runpy,hashlib,ast
ROOT=pathlib.Path(__file__).resolve().parent
def prepare152(number,original,roles,original_writer,legacy_preparer):
 a=runpy.run_path(str(ROOT/'authority152.py'));can=a['can'];sha=a['sha'];root=pathlib.Path(roles['private'])
 if number!=147 or sha(pathlib.Path(legacy_preparer).read_bytes())!='06e4f54b61670787e85e8de61e47779eb487e4815fbaff6a3d8af979eed8824b':raise ValueError('Exact original reviewed preparation and unused147 only')
 ts=original['structuredContent']['transfers']
 if original.get('isError') or original['structuredContent'].get('unavailable_items') or len(ts)!=4 or {t['library_file_id'] for t in ts}!=set(a['IDS']):raise ValueError('Authentic whole current A four-file intake')
 docs={};proof={}
 for t in ts:docs[t['library_file_id']],proof[t['library_file_id']]=a['proof152'](t['workspace_path'],t)
 direction=a['boundary152'](docs[a['AUDIT']])['recipient_outboxes']['TraceHarbor V1']
 if not direction['id'].startswith('V28-TRACE-147-') or direction.get('native_admission') is not True:raise ValueError('Actual future unused147 addressed release required')
 packet=a['boundary152'](docs[a['AUDIT']])[direction['source_branch']]['release_packet'];config=packet['static_CONFIG'];manifest=(ROOT/'manifest.json').read_bytes()
 runpy.run_path(str(ROOT/'plan127.py'))['release133'](direction,config,manifest,packet['preloaded']['inventory'])
 a['compare152'](docs[a['AUDIT']],docs[a['AUDIT']],proof,proof,docs[a['ROUTE']],docs[a['ROUTE']],docs[a['POLICY']],docs[a['POLICY']],direction,config,manifest)
 own=docs[a['OWN']]
 if own['state']!='NATIVE146_TERMINAL' or 'native147' in own or own['ownership']['duplicate_trace_route_owners']!=0:raise ValueError('No consumed or renamed invocation adoption')
 original_text=pathlib.Path(original_writer).read_text()
 if sha(original_text.encode())!='008f194ac2d4cd93e946949bb2a926acb58690adb1815734601cd9808e73550f':raise ValueError('Exact original008f')
 def put(path,raw):
  fd=os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,0o600)
  with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 paths={}
 for stable,name in ((a['AUDIT'],'Auditor_admission_A.json'),(a['POLICY'],'Policy_admission_A.json'),(a['ROUTE'],'Route_admission_A.json')):
  t=next(t for t in ts if t['library_file_id']==stable);source=pathlib.Path(t['workspace_path']);target=root/name;put(target,source.read_bytes())
  for attr in os.listxattr(source):os.setxattr(target,attr,os.getxattr(source,attr))
  _,p=a['proof152'](target,t,private=True)
  if p!=proof[stable]:raise ValueError('Whole A immutable copy and metadata')
  paths[stable]=str(target)
 writer=root/'admin147.py';adapt=original_text.replace('118','147').replace("a['state']=='NATIVE117_TERMINAL'","a['state']=='NATIVE146_TERMINAL'").replace('CURRENT Auditor858 direction147','CURRENT Auditor'+str(proof[a['AUDIT']]['version'])+' direction147');ast.parse(adapt);put(writer,adapt.encode())
 legacy=runpy.run_path(str(legacy_preparer));legacyproof={'Auditor_V28_checkpoint.json':proof[a['AUDIT']]};binding=legacy['binding_before_RX'](147,direction,legacyproof,original_writer,writer,paths[a['AUDIT']],roles)
 receipt=root/'admission-A-materialize.original.json';put(receipt,can(original));authority={'schema':a['CONTRACT'],'policy_path':paths[a['POLICY']],'route_path':paths[a['ROUTE']],'proofs':{k:proof[k] for k in (a['AUDIT'],a['POLICY'],a['ROUTE'])},'materialize_original':{'path':str(receipt),'bytes':receipt.stat().st_size,'sha256':sha(receipt.read_bytes())}}
 put(root/'direction147.json',can(direction));put(root/'source-verification.json',can({'Auditor_V28_checkpoint.json':proof[a['AUDIT']]}))
 return {'writer_binding':binding,'authority_admission152':authority,'source_verification':{'Auditor_V28_checkpoint.json':proof[a['AUDIT']]},'current_sources_before_RX':proof,'native_authority':False}
