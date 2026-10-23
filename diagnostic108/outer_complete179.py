"""PRIVATE179 official completion+verification; real source clocks, no write helper."""
from pathlib import Path
import json,runpy,subprocess,sys,time,os,hashlib,traceback
ROOT=Path(__file__).resolve().parent
def main():
    original_path,expected_path,candidate,frame_path,output,helper,helper_sha=sys.argv[1:8]
    started_mono=time.monotonic();started_utc=time.time();original=json.loads(Path(original_path).read_bytes());expected=json.loads(Path(expected_path).read_bytes());frame=json.loads(Path(frame_path).read_bytes());stages=[];result={};code=1
    try:
        O=runpy.run_path(str(ROOT/'outer_metadata179.py'));hp=Path(helper);raw=hp.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=helper_sha:raise ValueError('Exact official current metadata helper')
        for i,t in enumerate(O['tuple177'](original)):
            mono=time.monotonic();utc=time.time();r=subprocess.run([sys.executable,str(hp),'apply-xattrs',t['workspace_path']],input=json.dumps(t),capture_output=True,text=True,timeout=5)
            rec={'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'elapsed_mono_s':time.monotonic()-mono,'elapsed_utc_s':time.time()-utc}
            p=Path(output).with_name('source179-helper'+str(i)+'.original.json');fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
            with os.fdopen(fd,'w')as f:json.dump(rec,f)
            stages.append({'stage':'official_metadata_completion','role':t['library_file_id'],'elapsed_mono_s':rec['elapsed_mono_s'],'elapsed_utc_s':rec['elapsed_utc_s']})
            if r.returncode or rec['elapsed_mono_s']>=5 or rec['elapsed_utc_s']>=5:raise RuntimeError('First official helper error/late; no retry')
        if candidate=='AUTO_CURRENT_DISTINCT_CANDIDATE':
            mono=time.monotonic();t=next(t for t in O['tuple177'](original)if t['library_file_id']==O['OWN']);p=Path(t['workspace_path']);candidate=str(Path(output).with_name('qualification-current-candidate.json'));fd=os.open(candidate,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
            with os.fdopen(fd,'wb')as f:f.write(p.read_bytes());f.flush();os.fsync(f.fileno())
            for name in os.listxattr(p):os.setxattr(candidate,name,os.getxattr(p,name))
            stages.append({'stage':'whole_current_distinct_candidate_copy_ALLattrs','elapsed_s':time.monotonic()-mono})
        result=O['verify_readback179'](original,expected,candidate,frame);code=0
    except BaseException as e:result={'schema':'TRACE179_FIRST_COMPLETE_ORIGINAL_FAILURE','exception_class':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'native_authority':False,'retry':0}
    result.update(completion_stages=stages,source_process_start_mono=started_mono,source_process_start_utc=started_utc,source_process_finish_mono=time.monotonic(),source_process_finish_utc=time.time())
    fd=os.open(output,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'w')as f:json.dump(result,f,sort_keys=True,separators=(',',':'));f.flush();os.fsync(f.fileno())
    print(json.dumps(result));return code
if __name__=='__main__':sys.exit(main())
