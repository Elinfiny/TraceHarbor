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
ADMISSION_SHA256='2592213d24b21f4d33049d1ccf6880f50a092d0dcceef2f1407763250ca58d52'
MODULE_SHA256='0a4d002bc89c92fe72359ece0be63d031305fbe81c39c811dc1026c8df052911'
ADMISSION_PATH=Path('/var/data/traceharbor-staging/actual-initial004.json')
def admission():
 if os.environ.get('RENDER')!='true' or os.environ.get('RENDER_EXTERNAL_HOSTNAME')!=r.HOST:raise Refusal('EXACT_RENDER_HOST')
 if hashlib.sha256((Path(__file__).parent/'release_integration68.py').read_bytes()).hexdigest()!=MODULE_SHA256:raise Refusal('INTEGRATION_SOURCE_PIN')
 private_dir(ADMISSION_PATH.parent);data=read(ADMISSION_PATH,65536)
 if hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()!=ADMISSION_SHA256:raise Refusal('ACTUAL_ADMISSION_PIN')
 c,e=data['config'],data['evidence'];r.ADMITTED_CONFIG_SHA256=digest(c);r.ADMITTED_CAPTURE_SHA256=digest(e);r.ADMITTED_EVIDENCE_SHA256=digest(e);r.WORKER_ENTRY=Path(__file__).resolve();r.WORKER_ADMISSION_PATH=ADMISSION_PATH
 r.qualify(c,e,pin=digest(c),capture_pin=digest(e),source_root=Path(__file__).parent)
 return c,e

CREDIT004_PATH=Path('/var/data/traceharbor-staging/actual-recovery004.json')
CREDIT004_SHA256='f03d2e517c07c85084e5980d6253dbf9cf5f91bfb67d95be511452a6c00970c1'
def credit_admission004():
 if os.environ.get('RENDER')!='true'or os.environ.get('RENDER_EXTERNAL_HOSTNAME')!=r.HOST:raise Refusal('EXACT_CREDIT67_RENDER_HOST')
 data=read(CREDIT004_PATH,65536)
 if digest(data)!=CREDIT004_SHA256 or data.get('schema')!='traceharbor.recovery004.contract.v1':raise Refusal('EXACT_PRIVATE_CREDIT67_CONTRACT')
 r.checked_manifest(Path(__file__).parent,data['source_pins'])
 return data['policy']

def main():
 c,e=admission()
 if len(sys.argv)==3 and sys.argv[1]=='--credit-worker004':
  import credit_scope004,credit_runtime004
  if Path(sys.argv[2])!=credit_scope004.ROOT:raise Refusal('EXACT004_WORKER_ROOT')
  p=credit_admission004()
  if p['release_config']!=c:raise Refusal('SAME_ORIGINAL_ALLOCATION_CONFIG_REQUIRED')
  return credit_runtime004.worker(c,p)
 if len(sys.argv)!=1:raise Refusal('OLD_WORKERS_AND_ADMISSION_FLAGS_CLOSED')
 if not r.STATE.exists():raise Refusal('ORIGINAL_CONSUMED_STATE_REQUIRED_NO_REPROVISION')
 server=r.build_server(c,e,port=int(os.environ['PORT']),platform_port=os.environ['PORT'])
 try:
  import recovery004
  recovery004.wire(server,c)
  print('TraceHarbor004 configured; no automatic grant, capture, AI or billing',flush=True)
  server.serve_forever()
 finally:server.server_close()
if __name__=='__main__':main()
