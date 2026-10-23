"""PRIVATE SOURCE179: whole predicates retained, fast canonical proof and source FD instrumentation. Not canonical/native authority."""
"""SOURCE177 outer RX/terminal metadata integration; DATA only, no native capability.
Calls the accepted authority153.proof152 with one INTACT actual four original.
No provider callback, source override, fake transfer, nonce, registry or writes.
"""
import pathlib,json,runpy,sys,time,math,hashlib,traceback,os
ROOT=pathlib.Path(__file__).resolve().parent
IDS=('libfile_3ee8270f03d8819188e1de1f75c3d824','libfile_f87a6a307f70819194e0af0fa453afd1','libfile_6f69ae483b088191a1fffefca617bbd5','libfile_8377022600088191993dc06bfba93b7b')
OWN=IDS[0]
def tuple177(original):
 if type(original)is not dict or original.get('isError')or type(original.get('structuredContent'))is not dict:raise ValueError('Actual successful four-file original')
 result=original['structuredContent'];result=result.get('result',result);ts=result.get('transfers')
 if type(ts)is not list or len(ts)!=4 or result.get('unavailable_items')or {t.get('library_file_id')for t in ts if type(t)is dict}!=set(IDS):raise ValueError('One intact unique four-file original; no synthesis')
 if len({t.get('workspace_path')for t in ts})!=4 or len({t.get('file_id')for t in ts})!=4:raise ValueError('No aliased transfer paths/identities')
 for t in ts:
  if type(t.get('current_version_number'))is not int or t['current_version_number']<=0:raise ValueError('Actual positive provider versions')
 return ts
def require_timing177(frame,mono,utc):
 keys={'kind','origin_mono','origin_utc','ack_mono','ack_utc'}
 if type(frame)is not dict or set(frame)!=keys or frame['kind']not in ('CAS_READBACK','READ_ONLY_QUALIFICATION'):raise ValueError('Closed original metadata timing frame')
 values=[mono,utc,*[frame[k]for k in keys if k!='kind']]
 if any(type(v)not in(int,float)or not math.isfinite(v)for v in values):raise ValueError('Finite exact dual-clock values')
 for suffix,now in (('mono',mono),('utc',utc)):
  origin,ack=frame['origin_'+suffix],frame['ack_'+suffix]
  if not origin<=ack<=now:raise TimeoutError('Original clock regressed')
  if frame['kind']=='CAS_READBACK'and(ack-origin>=50 or now-origin>=75):raise TimeoutError('Original CAS50/phase75 exceeded; no retry/reset')
  if now-ack>=25:raise TimeoutError('Original whole readback25 exceeded; no retry/reset')
 return True
def read_frame177():
 mono=time.monotonic();utc=time.time()
 return {'kind':'READ_ONLY_QUALIFICATION','origin_mono':mono,'origin_utc':utc,'ack_mono':mono,'ack_utc':utc}
def source177():
 raw=(ROOT/'authority153.py').read_bytes()
 manifest=json.loads((ROOT/'manifest.json').read_bytes());pin=manifest['source_files']['diagnostic108/authority153.py']
 if len(raw)!=pin['bytes']or hashlib.sha256(raw).hexdigest()!=pin['sha256']:raise ValueError('Exact accepted verifier source pin')
 expected=ROOT/'snapshot174.py'
 if 'snapshot174'in sys.modules and pathlib.Path(sys.modules['snapshot174'].__file__).resolve()!=expected:raise ValueError('No preloaded snapshot shadow')
 if str(ROOT)not in sys.path:sys.path.insert(0,str(ROOT))
 import snapshot174
 if pathlib.Path(snapshot174.__file__).resolve()!=expected:raise ValueError('Exact sibling snapshot source')
 return runpy.run_path(str(ROOT/'authority153.py')),snapshot174
def verify_readback179(original,expected,candidate_path,frame,*,trace_transfer=None):
 """Called identically for RX_START and TERMINAL; exact positive current tuple.
 Caller-provided expected pins do not authorize native work or replace originals.
 """
 require_timing177(frame,time.monotonic(),time.time());ts=tuple177(original);transfer=next(t for t in ts if t['library_file_id']==OWN)
 if trace_transfer is not None and trace_transfer is not transfer:raise ValueError('Exact original member object, no copied/aliased tuple')
 fields={'version','file_id','bytes','sha256','self_sha256'}
 if type(expected)is not dict or set(expected)!=fields or type(expected['version'])is not int or expected['version']<=0:raise ValueError('Whole exact candidate and actual publication identity')
 if transfer['current_version_number']!=expected['version']or transfer['file_id']!=expected['file_id']or transfer['size_bytes']!=expected['bytes']:raise ValueError('Exact actual positive CAS/readback identity')
 authority,snapshot=source177();resources=[];docs={};proofs={};stages=[];freeze=None
 core=runpy.run_path(str(ROOT/'proof179.py'))
 source_start=time.monotonic();freeze=core['SourceFreeze179']();stages.append({'stage':'whole_source_freeze','elapsed_s':time.monotonic()-source_start})
 try:
  # Keep every path/FD/ancestor through ALL consumers, including candidate equality.
  for t in ts:
   cap=83886080 if t['library_file_id']==OWN else 67108864
   resources.append(snapshot.Whole173(t['workspace_path'],cap))
   d,pf,profile=core['proof179'](t['workspace_path'],t,original=original);stages.extend(profile);docs[t['library_file_id']]=d;proofs[t['library_file_id']]=pf
  candidate=snapshot.Whole173(str(pathlib.Path(candidate_path)),83886080);resources.append(candidate);actual=proofs[OWN];own=docs[OWN]
  if any(candidate.identity[:2]==r.identity[:2]for r in resources[:-1]):raise ValueError('Candidate must be a distinct physical original, never the readback alias')
  if candidate.attrs.get('user.library-file-id')!=OWN.encode()or candidate.attrs.get('user.library-file-version')!=str(expected['version']).encode():raise ValueError('Candidate positive exact Library identity/version')
  for attr in transfer['xattrs']:
   if candidate.attrs.get(attr['name'])!=attr['value'].encode():raise ValueError('ALL candidate returned attributes')
  if any(actual[k]!=expected[k]for k in ('version','file_id','bytes','sha256','self_sha256'))or candidate.raw!=resources[0 if ts[0]['library_file_id']==OWN else next(i for i,t in enumerate(ts)if t['library_file_id']==OWN)].raw:raise ValueError('Whole raw candidate bytes/self/positive original mismatch')
  if own.get('state')not in ('NATIVE154_RX_START','NATIVE154_TERMINAL','NATIVE153_TERMINAL'):raise ValueError('Closed outer state;153 terminal only read-only qualification')
  if own.get('state')=='NATIVE153_TERMINAL'and frame['kind']!='READ_ONLY_QUALIFICATION':raise ValueError('No153 rearm or write proof')
  stage=time.monotonic()
  for r in resources:r.reseal173()
  freeze.finish179();stages.append({'stage':'all_last_consumer_raw_FD_ancestor_source_seals','elapsed_s':time.monotonic()-stage})
  mono=time.monotonic();utc=time.time();require_timing177(frame,mono,utc)
  return {'schema':'TRACE179_INTACT_FOURFILE_OUTER_READBACK_V1','stage_timings':stages,'source_freeze_files':len(freeze.resources),'proof_algorithm':'SOURCE176_SNAPSHOT174_CANONICAL_EXACT_SEMANTICS_NO_AUTHORITY_GRANT','proofs':proofs,'state':own['state'],'whole_candidate_equality':True,'all_last_consumer_FD_ancestor_seals':True,'elapsed_read_mono_s':mono-frame['ack_mono'],'elapsed_read_utc_s':utc-frame['ack_utc'],'kind':frame['kind'],'native_authority':False,'writes':0,'retry':0}
 finally:
  for r in reversed(resources):r.close173()
  if freeze is not None:freeze.close179()
def main179():
 output=pathlib.Path(sys.argv[5]);started={'mono':time.monotonic(),'utc':time.time()}
 try:
  original=json.loads(pathlib.Path(sys.argv[1]).read_bytes());expected=json.loads(pathlib.Path(sys.argv[2]).read_bytes());frame=json.loads(pathlib.Path(sys.argv[4]).read_bytes());result=verify_readback179(original,expected,sys.argv[3],frame);code=0
 except BaseException as e:
  result={'schema':'TRACE177_OUTER_ORIGINAL_FAILURE','exception_class':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'started':started,'native_authority':False,'retry':0};code=1
 fd=os.open(output,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'w')as f:json.dump(result,f,sort_keys=True,separators=(',',':'))
 print(json.dumps(result));return code
if __name__=='__main__':sys.exit(main179())
