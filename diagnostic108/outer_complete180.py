"""Fixed official completion + real consumer180; no write/native capability.
The native TERMINAL caller uses stdout captured by its existing attrs-readback
ticket. Outer/admin/qualification callers retain one exact receipt file.
"""
from pathlib import Path
import json,runpy,subprocess,sys,time,os,hashlib,traceback
ROOT=Path(__file__).resolve().parent
HELPERS={'library_file_transfer.py':(15513,'8c7f5663d04ab4eb651c89c1b012014c8fe12b579a1069a72a677c67750a3e8b'),'library_hosted_apps.py':(15837,'7958642b88cde925aaca036989de1028c0864eb6d82a9cb175ebf9380cb9677b'),'library_upload.py':(44876,'5bc473dadefe1f68ee8797baaed19d6662642d0ea4bcba128fa12938faa0d767')}
def complete180(original,expected,candidate,frame,consumer,helper,*,capture_path=None):
 O=runpy.run_path(str(ROOT/'outer_metadata180.py'));S=O['S'];pool=S._Invocation175();resources=[];completions=[];started=time.monotonic()
 try:
  for name,(size,pin)in HELPERS.items():
   f=pool.open175(str(Path(helper).parent/name),33554432);resources.append(f)
   if len(f.raw)!=size or f.raw_sha!=pin or f.identity[3]&0o027:raise ValueError('Exact current official helper, safe permissions/FD/ancestors')
  for t in O['tuple180'](original):
   m=time.monotonic();u=time.time();p=subprocess.run([sys.executable,helper,'apply-xattrs',t['workspace_path']],input=json.dumps(t),capture_output=True,text=True,timeout=5)
   rec={'library_file_id':t['library_file_id'],'file_id':t['file_id'],'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'elapsed_mono_s':time.monotonic()-m,'elapsed_utc_s':time.time()-u};completions.append(rec)
   if p.returncode or rec['elapsed_mono_s']>=5 or rec['elapsed_utc_s']>=5:raise RuntimeError('First official completion error/late, no proof/native success')
  if candidate=='AUTO_CURRENT_DISTINCT_CANDIDATE':
   if consumer!={'schema':'TRACE180_METADATA_CONSUMER_V1','kind':'READ_ONLY','phase':'QUALIFICATION'}:raise ValueError('Auto copy only qualified read-only context')
   if type(capture_path)is not str:raise ValueError('Exact local original capture path required')
   t=next(t for t in O['tuple180'](original)if t['library_file_id']==O['OWN']);src=Path(t['workspace_path']);candidate=str(Path(capture_path).with_name('qualification-candidate.json'))
   fd=os.open(candidate,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
   with os.fdopen(fd,'wb')as f:f.write(src.read_bytes());f.flush();os.fsync(f.fileno())
   for name in os.listxattr(src):os.setxattr(candidate,name,os.getxattr(src,name))
  result=O['verify180'](original,expected,candidate,frame,consumer)
  for f in resources:f.reseal173()
  pool.reseal175();mono=time.monotonic();utc=time.time();O['timing180'](frame,mono,utc)
  result.update(official_completions=completions,official_helpers_all_FD_ancestor_last_seals=True,elapsed_read_mono_s=mono-frame['ack_mono'],elapsed_read_utc_s=utc-frame['ack_utc'],completion_and_consumer_s=mono-started)
  return result
 except BaseException as e:
  e.completion180_originals=completions;raise
 finally:
  for f in reversed(resources):f.close173()
  pool.close175()
def main():
 if sys.argv[1]=='origin':
  m=time.monotonic();u=time.time();frame={'kind':'READ_ONLY_QUALIFICATION','origin_mono':m,'origin_utc':u,'ack_mono':m,'ack_utc':u};fd=os.open(sys.argv[2],os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
  with os.fdopen(fd,'w')as f:json.dump(frame,f)
  print(json.dumps(frame),flush=True);return 0
 if sys.argv[1]=='native-terminal':
  _,canonical,candidate,expected,frame,helper=sys.argv[1:7];wrapper=json.loads(Path(canonical).read_bytes());original=wrapper['original']
  if original.get('schema')!='TRACE180_AUTHENTIC_TERMINAL_READBACK'or original.get('native_authority')is not False or wrapper.get('identity',{}).get('operation')!='library_materialize':raise ValueError('Actual canonical terminal call only')
  result=complete180(original['current'],json.loads(expected),candidate,json.loads(frame),{'schema':'TRACE180_METADATA_CONSUMER_V1','kind':'NATIVE_PHASE','phase':'TERMINAL'},helper)
  print(json.dumps(result),flush=True);return 0
 op,ep,candidate,fp,cp,output,helper=sys.argv[1:8];code=1
 try:
  original=json.loads(Path(op).read_bytes());expected=json.loads(Path(ep).read_bytes());frame=json.loads(Path(fp).read_bytes());consumer=json.loads(Path(cp).read_bytes())
  result=complete180(original,expected,candidate,frame,consumer,helper,capture_path=op);code=0
 except BaseException as e:result={'schema':'TRACE180_FIRST_CONSUMER_FAILURE','exception_class':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'official_completions':getattr(e,'completion180_originals',[]),'native_authority':False,'retry':0}
 if output!='STDOUT_EXISTING_SOURCE_HOST_RECORD':
  fd=os.open(output,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
  with os.fdopen(fd,'w')as f:json.dump(result,f,sort_keys=True,separators=(',',':'));f.flush();os.fsync(f.fileno())
 print(json.dumps(result),flush=True);return code
if __name__=='__main__':sys.exit(main())
