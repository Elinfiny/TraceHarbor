"""SOURCE177 fixed helper completion before intact-four verifier; no network/write."""
from pathlib import Path
import json,sys,subprocess,hashlib,runpy,os,time
ROOT=Path(__file__).resolve().parent
def main():
 original_path,expected,candidate,frame,output,helper,helper_sha=sys.argv[1:8]
 raw=Path(helper).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=helper_sha:raise ValueError('Exact admitted official metadata helper')
 o=json.loads(Path(original_path).read_bytes());v=runpy.run_path(str(ROOT/'outer_metadata177.py'));ts=v['tuple177'](o);f=json.loads(Path(frame).read_bytes());v['require_timing177'](f,time.monotonic(),time.time())
 for index,t in enumerate(ts):
  p=t['workspace_path'];start=time.monotonic();r=subprocess.run([sys.executable,helper,'apply-xattrs',p],input=json.dumps(t),text=True,capture_output=True,timeout=5)
  record={'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'elapsed_s':time.monotonic()-start}
  dest=Path(output).with_name('outer177-helper'+str(index)+'.original.json');fd=os.open(dest,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
  with os.fdopen(fd,'w')as z:json.dump(record,z)
  if r.returncode or record['elapsed_s']>=5:raise RuntimeError('Original helper error/late; no retry')
  v['require_timing177'](f,time.monotonic(),time.time())
 sys.argv=[str(ROOT/'outer_metadata177.py'),original_path,expected,candidate,frame,output];return v['main177']()
if __name__=='__main__':sys.exit(main())
