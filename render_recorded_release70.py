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
ADMISSION_SHA256='2a0d712f9f670667a93a42192fef5a37220d4a239c88a2e3cafe44cfd7647766'
MODULE_SHA256='0a4d002bc89c92fe72359ece0be63d031305fbe81c39c811dc1026c8df052911'
ADMISSION_PATH=Path('/var/data/traceharbor-staging/actual-admission146.json')
def admission():
 if os.environ.get('RENDER')!='true' or os.environ.get('RENDER_EXTERNAL_HOSTNAME')!=r.HOST:raise Refusal('EXACT_RENDER_HOST')
 if hashlib.sha256((Path(__file__).parent/'release_integration68.py').read_bytes()).hexdigest()!=MODULE_SHA256:raise Refusal('INTEGRATION_SOURCE_PIN')
 private_dir(ADMISSION_PATH.parent);data=read(ADMISSION_PATH,65536)
 if hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()!=ADMISSION_SHA256:raise Refusal('ACTUAL_ADMISSION_PIN')
 c,e=data['config'],data['evidence'];r.ADMITTED_CONFIG_SHA256=digest(c);r.ADMITTED_CAPTURE_SHA256=digest(e);r.ADMITTED_EVIDENCE_SHA256=digest(e);r.WORKER_ENTRY=Path(__file__).resolve();r.WORKER_ADMISSION_PATH=ADMISSION_PATH
 r.qualify(c,e,pin=digest(c),capture_pin=digest(e),source_root=Path(__file__).parent)
 return c,e

CREDIT67_PATH=Path('/var/data/traceharbor-staging/actual-recovery93.json')
CREDIT67_SHA256='b3b34b934e8abc98427894f11382593844756d2ce037d1dcd71100d0fc9eaa18'
def credit_admission67():
 if os.environ.get('RENDER')!='true'or os.environ.get('RENDER_EXTERNAL_HOSTNAME')!=r.HOST:raise Refusal('EXACT_CREDIT67_RENDER_HOST')
 data=read(CREDIT67_PATH,65536)
 if digest(data)!=CREDIT67_SHA256 or data.get('schema')!='traceharbor.credit67.contract.v1':raise Refusal('EXACT_PRIVATE_CREDIT67_CONTRACT')
 r.checked_manifest(Path(__file__).parent,data['source_pins'])
 return data['policy']

def main():
 c,e=admission()
 if len(sys.argv)==3 and sys.argv[1]=='--credit-worker67':
  import credit_scope67,credit_runtime67
  if Path(sys.argv[2])!=credit_scope67.ROOT:raise Refusal('EXACT_CREDIT67_WORKER')
  p=credit_admission67()
  if p['release_config']!=c:raise Refusal('SHARED_ORIGINAL_CONFIG_REQUIRED')
  return credit_runtime67.worker(c,p)
 if len(sys.argv)==3 and sys.argv[1]=='--worker':
  if Path(sys.argv[2])!=r.STATE:raise Refusal('EXACT_WORKER_STATE')
  return r.worker(r.STATE)
 if len(sys.argv)!=1:raise Refusal('NO_ADMISSION_FLAGS')
 if not r.STATE.exists():raise Refusal('ORIGINAL_EXISTING_STATE_REQUIRED_RECOVERY86')
 # Existing state is never re-provisioned, decremented or restored.
 server=r.build_server(c,e,port=int(os.environ['PORT']),platform_port=os.environ['PORT'])
 try:
  import recovery86
  recovery86.wire(server,c)
  print('TraceHarbor capture146 configured; no automatic grant/media/AI; original84 retained',flush=True)
 except Exception:
  print('TraceHarbor capture146 unavailable; public read-only retained; no retry',flush=True)
 try:
  import recovery67
  recovery67.wire(server,c)
  print('Credit67 route installed; no automatic grant/media/AI',flush=True)
 except Exception:
  print('Credit67 not admitted; existing public read-only retained',flush=True)
 try:server.serve_forever()
 finally:server.server_close()
if __name__=='__main__':main()
