"""Source-bound first-recorded-request launcher. No secret/pin activation via HTTP/env flags.
Actual nonsecret admission data stays private; exact immutable source and its
native Render deployment must be reconciled before the Owner's native picker.
Default product modules stay cap0. Public requests cannot become capture operators.
"""
import hashlib,json,os,sys
from pathlib import Path
import release_integration68 as r
from quota_ledger import read,private_dir,exclusive
from release_policy import digest,Refusal
ADMISSION_SHA256='b6006c891a18321fbf52f2982b623c4c017c570dd03d636f08d1876b0fb380e6'
MODULE_SHA256='d617a2caee3ffa5fa7bdb00498118b5b26e13243b20b4f7bf51596b04b43f667'
ADMISSION_PATH=Path('/var/data/traceharbor-staging/actual-admission74.json')
def admission():
 if os.environ.get('RENDER')!='true' or os.environ.get('RENDER_EXTERNAL_HOSTNAME')!=r.HOST:raise Refusal('EXACT_RENDER_HOST')
 if hashlib.sha256((Path(__file__).parent/'release_integration68.py').read_bytes()).hexdigest()!=MODULE_SHA256:raise Refusal('INTEGRATION_SOURCE_PIN')
 private_dir(ADMISSION_PATH.parent);data=read(ADMISSION_PATH,65536)
 if hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()!=ADMISSION_SHA256:raise Refusal('ACTUAL_ADMISSION_PIN')
 c,e=data['config'],data['evidence'];r.ADMITTED_CONFIG_SHA256=digest(c);r.ADMITTED_CAPTURE_SHA256=digest(e);r.ADMITTED_EVIDENCE_SHA256=digest(e);r.WORKER_ENTRY=Path(__file__).resolve();r.WORKER_ADMISSION_PATH=ADMISSION_PATH
 r.qualify(c,e,pin=digest(c),capture_pin=digest(e),source_root=Path(__file__).parent)
 return c,e
def main():
 c,e=admission()
 if len(sys.argv)==3 and sys.argv[1]=='--worker':
  if Path(sys.argv[2])!=r.STATE:raise Refusal('EXACT_WORKER_STATE')
  return r.worker(r.STATE)
 if len(sys.argv)!=1:raise Refusal('NO_ADMISSION_FLAGS')
 if not r.STATE.exists():
  grant=r.provision_once(c,e)
  fd=os.open(r.STATE/'operator/native-grant.txt',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
  with os.fdopen(fd,'w')as f:f.write(grant);f.flush();os.fsync(f.fileno())
  del grant
 # Existing state is never re-provisioned, decremented or restored.
 server=r.build_server(c,e,port=int(os.environ['PORT']),platform_port=os.environ['PORT'])
 print('TraceHarbor: one operator-recorded E2E configured; public AI and other255held; no retry',flush=True)
 try:server.serve_forever()
 finally:server.server_close()
if __name__=='__main__':main()
