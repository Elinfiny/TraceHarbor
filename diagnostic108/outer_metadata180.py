"""Current complete metadata consumer180. Pure evidence, never native authority.
Separate native outer/phase, read-only qualification and source-administrative
contexts; original dual clocks and50/25/75 remain strict. No callback/proof port.
"""
from pathlib import Path
import json,runpy,time,math,hashlib,sys
ROOT=Path(__file__).resolve().parent
if str(ROOT)not in sys.path:sys.path.insert(0,str(ROOT))
import snapshot174 as S
assert Path(S.__file__).resolve()==ROOT/'snapshot174.py'
P=runpy.run_path(str(ROOT/'proof180.py'))
IDS=(P['OWN'],'libfile_f87a6a307f70819194e0af0fa453afd1','libfile_6f69ae483b088191a1fffefca617bbd5','libfile_8377022600088191993dc06bfba93b7b');OWN=IDS[0]
PHASES=('SOURCE_FREEZE','PRE_DISPATCH','ADMIT_CHAIN','ENCRYPTED_CHAIN','CONSUMED_CHAIN','TERMINAL')
def tuple180(original):
 if type(original)is not dict or original.get('isError')or type(original.get('structuredContent'))is not dict:raise ValueError('Successful intact original4')
 r=original['structuredContent'];r=r.get('result',r);ts=r.get('transfers')
 if type(ts)is not list or len(ts)!=4 or r.get('unavailable_items')or {t.get('library_file_id')for t in ts if type(t)is dict}!=set(IDS):raise ValueError('Entire unique four source identities')
 if len({t.get('workspace_path')for t in ts})!=4 or len({t.get('file_id')for t in ts})!=4:raise ValueError('No mixed/aliased original tuple')
 if any(type(t.get('current_version_number'))is not int or t['current_version_number']<=0 for t in ts):raise ValueError('Exact positive int nonbool source versions')
 return ts
def timing180(frame,mono,utc):
 if type(frame)is not dict or set(frame)!={'kind','origin_mono','origin_utc','ack_mono','ack_utc'}or frame['kind']not in('READ_ONLY_QUALIFICATION','CAS_READBACK','ADMIN_SOURCE_CAS'):raise ValueError('Closed distinct original timing schema')
 if any(type(v)not in(int,float)or not math.isfinite(v)for v in(mono,utc,*[frame[k]for k in frame if k!='kind'])):raise ValueError('Finite original dual clocks')
 for suffix,now in(('mono',mono),('utc',utc)):
  origin,ack=frame['origin_'+suffix],frame['ack_'+suffix]
  if not origin<=ack<=now:raise TimeoutError('Original clock regression')
  if frame['kind']!='READ_ONLY_QUALIFICATION'and(ack-origin>=50 or now-origin>=75):raise TimeoutError('Original CAS50/pair75 exceeded')
  if now-ack>=25:raise TimeoutError('Original read25 exceeded')
 return True
def consumer180(consumer,frame,doc):
 if type(consumer)is not dict or set(consumer)!={'schema','kind','phase'}or consumer['schema']!='TRACE180_METADATA_CONSUMER_V1':raise ValueError('Closed actual consumer descriptor')
 kind,phase=consumer['kind'],consumer['phase'];state=doc.get('state')
 if kind=='READ_ONLY':
  if phase!='QUALIFICATION'or frame['kind']!='READ_ONLY_QUALIFICATION'or state!='NATIVE153_TERMINAL':raise ValueError('Closed153 only actual read-only qualification')
 elif kind=='ADMIN_SOURCE':
  if phase!='ADMIN_CLOSURE'or frame['kind']!='ADMIN_SOURCE_CAS'or state!='NATIVE153_TERMINAL'or doc.get('source180',{}).get('phase')!='REPAIR_TERMINAL'or'native154'in doc:raise ValueError('Distinct source-only admin receipt, never native154 CAS')
 elif kind=='NATIVE_OUTER':
  if frame['kind']!='CAS_READBACK'or phase not in('RX_START','TERMINAL')or state!='NATIVE154_'+phase or doc.get('native154',{}).get('phase')!=phase:raise ValueError('Exact154 outerRX/TERMINAL, no153 waiver')
 elif kind=='NATIVE_PHASE':
  n=doc.get('native154',{});records=n.get('records',[])
  intent=runpy.run_path(str(ROOT/'references177.py'))['expand_intent165'](doc,records[-1]['payload']['phase_intent127'],len(records)-1)if records and'phase_intent127'in records[-1].get('payload',{})else{}
  if frame['kind']!='CAS_READBACK'or phase not in PHASES or state!='NATIVE154_PUBLISH_INTENT'or not records or records[-1].get('phase')!='PUBLISH_INTENT'or intent.get('phase')!=phase:raise ValueError('Source actual154 phase intent only, not an outer state')
 else:raise ValueError('No supplied compatibility/grant mode')
 return True
def verify180(original,expected,candidate_path,frame,consumer):
 timing180(frame,time.monotonic(),time.time());ts=tuple180(original);own_t=next(t for t in ts if t['library_file_id']==OWN)
 if type(expected)is not dict or set(expected)!={'version','file_id','bytes','sha256','self_sha256'}or type(expected['version'])is not int or expected['version']<=0:raise ValueError('Whole exact expected publication pins')
 if (own_t['current_version_number'],own_t['file_id'],own_t['size_bytes'])!=(expected['version'],expected['file_id'],expected['bytes']):raise ValueError('Stale/mixed actual positive original identity')
 freeze=P['SourceFreeze180']();resources=[];docs={};proofs={};stages=[]
 try:
  for t in ts:
   resource=S.Whole173(t['workspace_path'],83886080 if t['library_file_id']==OWN else 67108864);resources.append(resource)
   doc,pf,profile=P['proof180'](t['workspace_path'],t,original=original);docs[t['library_file_id']]=doc;proofs[t['library_file_id']]=pf;stages.extend(profile)
  candidate=S.Whole173(str(Path(candidate_path)),83886080);resources.append(candidate)
  if any(candidate.identity[:2]==r.identity[:2]for r in resources[:-1]):raise ValueError('Distinct physical candidate, no same inode/readback alias')
  ownresource=resources[next(i for i,t in enumerate(ts)if t['library_file_id']==OWN)]
  if candidate.raw!=ownresource.raw or any(proofs[OWN][k]!=expected[k]for k in expected):raise ValueError('Whole candidate bytes/hash/self/original mismatch')
  if candidate.attrs.get('user.library-file-id')!=OWN.encode()or candidate.attrs.get('user.library-file-version')!=str(expected['version']).encode():raise ValueError('Actual candidate positive identity/version')
  for a in own_t['xattrs']:
   if candidate.attrs.get(a['name'])!=a['value'].encode():raise ValueError('All exact candidate returned attributes')
  consumer180(consumer,frame,docs[OWN]);start=time.monotonic()
  for r in resources:r.reseal173()
  source_count=len(freeze.resources);freeze.finish180();stages.append({'stage':'all_source_metadata_candidate_last_consumer_seals','elapsed_s':time.monotonic()-start});mono=time.monotonic();utc=time.time();timing180(frame,mono,utc)
  return {'schema':'TRACE180_COMPLETE_CONSUMER_READBACK_V1','consumer':consumer,'proofs':proofs,'state':docs[OWN]['state'],'whole_candidate_equality':True,'all_FD_ancestor_last_consumer_seals':True,'source_freeze_files':source_count,'stage_timings':stages,'elapsed_read_mono_s':mono-frame['ack_mono'],'elapsed_read_utc_s':utc-frame['ack_utc'],'native_authority':False,'writes':0,'retry':0}
 finally:
  for r in reversed(resources):r.close173()
  freeze.close180()
