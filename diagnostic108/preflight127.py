"""Invoked only AFTER the inline caller anchored EVERY byte to native current.
No source-only127 text carries the actual admission markers required here.
"""
import sys,json,pathlib,hashlib,io,runpy,os,copy,importlib.util
ROOT=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def can(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
_spec=importlib.util.spec_from_file_location('trace128_preflight_helper',ROOT/'helper_channel128.py');helper128=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(helper128)
_a152=importlib.util.spec_from_file_location('trace152_authority_'+__name__,ROOT/'authority152.py');a152=importlib.util.module_from_spec(_a152);_a152.loader.exec_module(a152)
#133 Fixed-source current intake. A dict describing custody is never a snapshot.
_SNAP133={}
class CurrentSnapshot133:
 __slots__=()
CURRENT_METADATA_LIMIT133=67108864
PRIVATE_MEMBER_LIMIT133=33554432
def _stable_read133(path,expected=None,private=False,*,metadata=False,metadata_transfer=None,metadata_original=None):
 import stat
 p=pathlib.Path(path)
 if not p.is_absolute() or p.resolve()!=p:raise ValueError('No path aliases')
 # Every current path component is checked; no symlink ancestor traversal.
 for parent in [*reversed(p.parents),p]:
  if parent.is_symlink():raise ValueError('Nofollow every ancestor')
 if type(metadata) is not bool or metadata and private:raise ValueError('Metadata flag cannot enlarge private custody')
 if metadata:
  if metadata_transfer is None:raise ValueError('Authentic transfer required before selecting metadata envelope')
  return __import__('runpy').run_path(str(ROOT/'envelope158.py'))['read158'](path,metadata_transfer,original=metadata_original)[1]
 limit=PRIVATE_MEMBER_LIMIT133
 s=p.lstat()
 if s.st_size>limit:raise ValueError('Whole bounded metadata bytes' if metadata else 'Whole bounded custody bytes')
 if not stat.S_ISREG(s.st_mode) or s.st_uid!=os.getuid() or s.st_nlink!=1 or private and s.st_mode&0o077 or s.st_mode&0o022:raise ValueError('Owned stable regular custody')
 if expected is not None and (s.st_dev,s.st_ino,s.st_uid,s.st_mode&0o777)!=(expected['dev'],expected['ino'],expected['uid'],expected['mode']):raise ValueError('No pruned/recreated custody adoption')
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  a=os.fstat(fd);chunks=[];total=0
  while True:
   b=os.read(fd,1048576)
   if not b:break
   chunks.append(b);total+=len(b)
   if total>limit:raise ValueError('Whole bounded custody bytes')
  b=os.fstat(fd)
 finally:os.close(fd)
 end=p.lstat();ident=lambda st:(st.st_dev,st.st_ino,st.st_uid,st.st_mode,st.st_size,st.st_mtime_ns)
 if ident(s)!=ident(a) or ident(a)!=ident(b) or ident(b)!=ident(end):raise ValueError('Full original changed during read')
 return b''.join(chunks)
def custody133(own,config):
 import stat
 checkpoint_key=config['custody_scope']['checkpoint_key'];record=own[checkpoint_key]['records'][-1];proof=record['payload']['custody'];root=pathlib.Path(config['custody_scope']['root'])
 if checkpoint_key!='native132':
  original=own['native132']['records'][-1]['payload']['custody'];lineage=proof.get('lineage')
  wanted={'original_checkpoint_key':'native132','original_archive_sha256':original['archive']['sha256'],'profile_id':original['manifest']['profile_id'],'revision':original['manifest']['revision'],'recovery_direction':own[checkpoint_key]['direction']['id'],'new_stage_only':True,'oldstage_adopted':False}
  if lineage!=wanted or proof['archive']['sha256']!=original['archive']['sha256'] or proof['archive']['bytes']!=original['archive']['bytes'] or proof['manifest']!=original['manifest'] or proof['new_verified_root']==original['new_verified_root'] or proof['stage']['path']==original['stage']['path']:raise ValueError('Exact canonical recovery lineage; old pruned home never adopted/recreated')
 if proof['new_verified_root']!=str(root) or proof['manifest']['profile_id']!=config['custody_scope']['profile']:raise ValueError('Actual retained checkpoint custody origin')
 stage=proof['stage'];st=pathlib.Path(stage['path']).lstat()
 if pathlib.Path(stage['path']).resolve()!=pathlib.Path(stage['path']) or (st.st_dev,st.st_ino,st.st_uid,st.st_mode&0o777)!=(stage['dev'],stage['ino'],stage['uid'],0o700):raise ValueError('Current original acquisition stage')
 result={}
 for name,pin in config['private6'].items():
  expected=proof['six_member_locators'][name];path=root/name
  if expected['locator']!=str(path) or {k:expected[k] for k in ('bytes','sha256')}!=pin:raise ValueError('Actual source-acquired locator and pin')
  for parent in [root,path.parent]:
   ps=parent.lstat()
   if parent.resolve()!=parent or not stat.S_ISDIR(ps.st_mode) or ps.st_uid!=os.getuid() or ps.st_mode&0o077:raise ValueError('Private original root/tokenizer')
  raw=_stable_read133(path,expected,True)
  if len(raw)!=pin['bytes'] or sha(raw)!=pin['sha256']:raise ValueError('Actual six whole private pins')
  result[name]={'bytes':len(raw),'sha256':sha(raw),'dev':expected['dev'],'ino':expected['ino'],'uid':expected['uid'],'mode':expected['mode']}
 return result
def verify_current133(own,audit,proof,config,manifest_bytes,policy_version,*,current_docs152=None,current_proofs152=None):
 s=importlib.util.spec_from_file_location('trace133_current_field_plan',ROOT/'plan127.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
 key='native'+own['state'].split('_')[0][6:];n=own[key]
 if current_docs152 is None or current_proofs152 is None:raise ValueError('Separate whole authentic CURRENT B authority required')
 direction=a152.boundary152(audit)['recipient_outboxes']['TraceHarbor V1']
 if own['ownership']['owner']!='TraceHarbor V1' or own['ownership']['duplicate_trace_route_owners']!=0 or own['native_id']!=a152.TRACE_CHAT or n['direction']!=direction:raise ValueError('Actual current sole route/owner/outbox')
 p.release133(direction,config,manifest_bytes)
 if config['prestart154']['direction_number']==150:
  __import__('runpy').run_path(str(ROOT/'references156.py'))['verify_rx156'](own,p.c.inventory127())
  __import__('runpy').run_path(str(ROOT/'capacity156.py'))['require_capacity156'](own,config)
 evidence=a152.verify152(own,current_docs152,current_proofs152,config,manifest_bytes)
 __import__('runpy').run_path(str(ROOT/'prestart156.py'))['current_prestart154'](own,config,empty=True)
 return copy.deepcopy(direction),evidence
def produce133(original_path,config,*,_native_reload133=False):
 s=importlib.util.spec_from_file_location('trace133_preflight_plan',ROOT/'plan127.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
 manifest_bytes=(ROOT/'manifest.json').read_bytes();p.static133(config,manifest_bytes)
 if str(pathlib.Path(original_path))!=config['path_roles']['materialize_original']:raise ValueError('Only fixed caller actual materialize capture')
 original=json.loads(_stable_read133(original_path));result=original['structuredContent'];result=result.get('result',result);ts=result['transfers']
 IDs={'libfile_3ee8270f03d8819188e1de1f75c3d824','libfile_f87a6a307f70819194e0af0fa453afd1','libfile_6f69ae483b088191a1fffefca617bbd5','libfile_8377022600088191993dc06bfba93b7b'}
 if original.get('isError') or result.get('unavailable_items') or len(ts)!=4 or {t['library_file_id'] for t in ts}!=IDs:raise ValueError('Actual unique full current materialization original')
 docs={};proof={}
 helper=config['path_roles']['library_helper'];helper_sha=config['path_roles']['library_helper_sha256']
 if sha(_stable_read133(helper))!=helper_sha:raise ValueError('Pinned actual helper')
 for i,t in enumerate(ts):
  path=pathlib.Path(t['workspace_path'])
  if not _native_reload133:
   helper128.run_helper128(helper,helper_sha,path,t['library_file_id'],t['xattrs'],{'phase':'PREFLIGHT','run':'STATIC133','source':config['source']['commit'],'call':'preflight/'+t['library_file_id']},lambda ident,record:helper128.retain_private128(config['path_roles']['capture'],ident,record))
  d,raw,h=__import__('runpy').run_path(str(ROOT/'envelope158.py'))['read158'](path,t,original=original)
  if os.getxattr(path,'user.library-file-id').decode()!=t['library_file_id'] or int(os.getxattr(path,'user.library-file-version').decode())!=t['current_version_number']:raise ValueError('Actual stable Library ID/version')
  for a in t['xattrs']:
   if os.getxattr(path,a['name']).decode()!=a['value']:raise ValueError('ALL current returned attributes')
  docs[t['library_file_id']]=(d,t,raw);proof_key='Auditor_V28_checkpoint.json' if t['library_file_id']=='libfile_f87a6a307f70819194e0af0fa453afd1' else path.name;proof[proof_key]={'library_file_id':t['library_file_id'],'file_id':t['file_id'],'version':t['current_version_number'],'bytes':len(raw),'sha256':sha(raw),'self_sha256':h,'ALLattrs':'PASS'}
 own,ot,oraw=docs['libfile_3ee8270f03d8819188e1de1f75c3d824'];audit,at,araw=docs['libfile_f87a6a307f70819194e0af0fa453afd1'];policy,pt,praw=docs['libfile_6f69ae483b088191a1fffefca617bbd5'];key='native'+own['state'].split('_')[0][6:];n=own[key]
 current_docs152={stable:value[0] for stable,value in docs.items()};current_proofs152={t['library_file_id']:proof['Auditor_V28_checkpoint.json' if t['library_file_id']==a152.AUDIT else pathlib.Path(t['workspace_path']).name] for t in ts};direction,authority152=verify_current133(own,audit,proof,config,manifest_bytes,pt['current_version_number'],current_docs152=current_docs152,current_proofs152=current_proofs152)
 binding=n['records'][0]['payload']['writer_binding'];number=int(key[6:]);s=importlib.util.spec_from_file_location('trace133_immutable_guard',ROOT/'host_transport118.py');base=importlib.util.module_from_spec(s);s.loader.exec_module(base)
 guard_cfg={'direction_number':number,'writer_binding':binding,'config_path':config['path_roles']['config']};h154=__import__('runpy').run_path(str(ROOT/'prestart156.py'));current=h154['current_binding154'](base,ot['workspace_path'],ot['current_version_number'],guard_cfg)
 if current['direction']!=direction or current['binding']['auditor_version']!=authority152['admission_A'][a152.AUDIT]['version']:raise ValueError('Original118 immutable A and independently verified CURRENT B')
 layout=base.validate_transfer_layout(binding)
 for role in ('private','transfer','holder_parent'):
  if str(layout[role])!=config['path_roles'][role]:raise ValueError('Actual disjoint role provenance')
 if own['state'].endswith('_TERMINAL') or n['phase']!='RX_START' or len(n['records'])!=1 or any(x.get('phase')=='DISPATCH_CONSUMED' for x in n['records']):raise ValueError('No consumed/UNKNOWN invocation adoption')
 custody=custody133(own,config);snapshot=CurrentSnapshot133();_SNAP133[snapshot]={'direction':copy.deepcopy(direction),'ownership':'TraceHarbor V1','own_version':ot['current_version_number'],'current_checkpoint':ot['workspace_path'],'writer_sha256':binding['writer_sha256'],'auditor_sha256':authority152['immutable_guard_auditor_sha256'],'authority152':authority152,'custody_sha256':sha(can(custody)),'source_verification':copy.deepcopy(n['source_verification']),'current_source_verification152':proof,'writer_binding':binding,'direction_number':number,'custody':custody}
 _SNAP133[snapshot]['holder_preparation154']=copy.deepcopy(n['records'][0]['payload']['holder_preparation154']);_SNAP133[snapshot]['prestart154']=h154['current_prestart154'](own,config,empty=True)
 return snapshot
def require_snapshot133(snapshot):
 if type(snapshot) is not CurrentSnapshot133 or snapshot not in _SNAP133:raise TypeError('Actual same invocation source-produced current snapshot')
 return copy.deepcopy(_SNAP133[snapshot])
def main133():
 cfg=json.loads(pathlib.Path(sys.argv[2]).read_bytes());snapshot=produce133(sys.argv[1],cfg);x=require_snapshot133(snapshot);s=importlib.util.spec_from_file_location('trace133_preflight_output_plan',ROOT/'plan127.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
 print(json.dumps({'schema':'TRACE133_NATIVE_PREFLIGHT_ORIGINAL_V2','startup156':cfg['startup156'],'prestart154':x['prestart154'],'current_admission':x['direction'][p.ADMISSION],'inventory_sha256':cfg['inventory_sha256'],'own_version':x['own_version'],'whole_self_allattrs':'PASS','native_authority':False,'sourceSha':cfg['source']['commit'],'sourceTree':cfg['source']['tree'],'captureDirectory':cfg['path_roles']['capture'],'transferRoot':cfg['path_roles']['transfer'],'dispatchSource':cfg['dispatch_source'],'directionId':x['direction']['id'],'staticConfigSha256':sha(can(cfg)),'manifestSha135':cfg['manifest']['sha256']}))

if __name__=='__main__':main133()
