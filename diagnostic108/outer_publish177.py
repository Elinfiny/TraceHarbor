"""SOURCE177 guarded OUTER publication for a FUTURE independently admitted154.
Never called by repair154. One actual helper invocation; frame captured here,
not supplied by JSON. No native clock/nonce/registry and no unknown write retry.
"""
from pathlib import Path
import json,os,sys,time,runpy,subprocess,hashlib,copy,traceback
ROOT=Path(__file__).resolve().parent
O=runpy.run_path(str(ROOT/'outer_metadata177.py'))
def validate_publish177(original,candidate,config,phase,version):
 if phase not in ('RX_START','TERMINAL')or type(version)is not int or version<=0:raise ValueError('Closed outer154 phase/positive version')
 ts=O['tuple177'](original);authority,snapshot=O['source177']();docs={};proofs={}
 for t in ts:
  d,p=authority['proof152'](t['workspace_path'],t,original=original);docs[t['library_file_id']]=d;proofs[t['library_file_id']]=p
 own=docs[O['OWN']];a=runpy.run_path(str(ROOT/'authority177.py'));direction=a['boundary152'](docs[a['AUDIT']])['recipient_outboxes']['TraceHarbor V1']
 if direction.get('native_admission')is not True or not direction['id'].startswith('V29-TRACE-154-'):raise PermissionError('Separate genuine154 native admission required before publication')
 if proofs[O['OWN']]['version']!=version:raise ValueError('Actual exact current expected version')
 manifest=(ROOT/'manifest.json').read_bytes();runpy.run_path(str(ROOT/'plan127.py'))['release133'](direction,config,manifest)
 a['compare152'](docs[a['AUDIT']],docs[a['AUDIT']],proofs,proofs,docs[a['ROUTE']],docs[a['ROUTE']],docs[a['POLICY']],docs[a['POLICY']],direction,config,manifest)
 h=runpy.run_path(str(ROOT/'prestart177.py'));h['history154'](own,config,before_RX=phase=='RX_START')
 if own.get('state')=='NATIVE154_TERMINAL':raise ValueError('No repeated terminal publication')
 resource=snapshot.Whole173(str(Path(candidate)),83886080)
 try:
  p=Path(candidate);raw=resource.raw;c=json.loads(raw);E=runpy.run_path(str(ROOT/'envelope158.py'))
  if E['self_hash158'](c)!=c['self_sha256']or c.get('state')!='NATIVE154_'+phase or c.get('native154',{}).get('phase')!=phase:raise ValueError('Whole actual154 candidate/self/phase')
  for k,v in own.items():
   if k not in ('events','guard','state','self_sha256','native154')and c.get(k)!=v:raise ValueError('Every old root exact, including153')
  n=c['native154'];binding=n['records'][0]['payload']['writer_binding']
  if binding['direction_number']!=154 or n['direction']!=direction:raise ValueError('Exact actual154 candidate release')
  if p!=Path(binding['binding_root'])/('candidate'+str(version+1))/'TraceHarbor_V1_checkpoint.json':raise ValueError('Exact source-owned candidate locator')
  original_writer=Path(binding['original_writer_path']).read_text();derived,_=h['derive154'](original_writer,binding['auditor_version'])
  if Path(binding['writer_path']).read_text()!=derived or hashlib.sha256(derived.encode()).hexdigest()!=binding['writer_sha256']:raise ValueError('Exact six substitutions/source-derived writer')
  if n['records'][:-1]!=([] if phase=='RX_START'else own['native154']['records'])or n['records'][-1]['phase']!=phase:raise ValueError('One append only, no altered native154 records')
  if c['events'][:len(own['events'])]!=own['events']or len(c['events'])-len(own['events'])!=(2 if phase=='RX_START'else 1):raise ValueError('Exact event prefix and outer phase count')
  resource.reseal173()
  return binding,config['publication150']['helpers']['library_upload.py']
 finally:resource.close173()

def main():
 original_path,candidate,config_path,phase,version_text,output=sys.argv[1:7];version=int(version_text);original=json.loads(Path(original_path).read_bytes());config=json.loads(Path(config_path).read_bytes())
 complete=runpy.run_path(str(ROOT/'outer_metadata177.py'));helper_meta=config['path_roles'];hp=Path(helper_meta['library_helper']);hb=hp.read_bytes()
 if hashlib.sha256(hb).hexdigest()!=helper_meta['library_helper_sha256']:raise ValueError('Pinned official metadata helper before actual source guards')
 for i,t in enumerate(complete['tuple177'](original)):
  start=time.monotonic();r=subprocess.run([sys.executable,str(hp),'apply-xattrs',t['workspace_path']],input=json.dumps(t),capture_output=True,text=True,timeout=5);rec={'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'elapsed_s':time.monotonic()-start};rp=Path(output).with_name('outer177-prepublish-helper'+str(i)+'.original.json');fd=os.open(rp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
  with os.fdopen(fd,'w')as f:json.dump(rec,f)
  if r.returncode or rec['elapsed_s']>=5:raise RuntimeError('First helper failure before write; no retry')
 start=time.monotonic();binding,helper=validate_publish177(original,candidate,config,phase,version)
 if time.monotonic()-start>=15:raise TimeoutError('Original authority15 exceeded before CAS')
 raw=Path(helper['path']).read_bytes()
 if len(raw)!=helper['bytes']or hashlib.sha256(raw).hexdigest()!=helper['sha256']:raise ValueError('Exact current official upload helper')
 reservation=Path(binding['binding_root'])/('outer177-'+phase+'-'+str(version)+'.intent.json');request={'uploads':[{'local_path':candidate,'purpose':'replace_library_file','library_file_id':O['OWN'],'expected_current_version':version,'version_reason':'Genuine independently admitted154 exact outer '+phase}]}
 fd=os.open(reservation,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'w')as f:json.dump(request,f)
 origin_mono=time.monotonic();origin_utc=time.time()
 try:r=subprocess.run([sys.executable,helper['path']],input=json.dumps(request)+'\n',text=True,capture_output=True,timeout=50);first={'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
 except BaseException as e:first={'exception_class':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'outcome':'UNKNOWN_NO_RETRY'}
 ack_mono=time.monotonic();ack_utc=time.time();record={'schema':'TRACE177_ACTUAL_OUTER_PUBLICATION_ORIGINAL','original':first,'frame':{'kind':'CAS_READBACK','origin_mono':origin_mono,'origin_utc':origin_utc,'ack_mono':ack_mono,'ack_utc':ack_utc},'retry':0}
 fd=os.open(output,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'w')as f:json.dump(record,f)
 if first.get('returncode')!=0:raise RuntimeError('First publication error/UNKNOWN; no retry')
 rows=json.loads(first['stdout'])['results'];publication=rows[0]
 if len(rows)!=1 or publication.get('status')!='succeeded'or publication.get('library_file_id')!=O['OWN']or publication.get('current_version_number')!=version+1:raise ValueError('Actual exact conditional publication response')
 O['require_timing177'](record['frame'],time.monotonic(),time.time());record['publication']=publication;print(json.dumps(record))
if __name__=='__main__':main()
