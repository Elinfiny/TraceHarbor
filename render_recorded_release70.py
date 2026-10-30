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
ADMISSION_SHA256='b767ff658bd9526cadd1db1789ff740cfe723ea639ff4883328d5e57bf23f0e0'
MODULE_SHA256='0a4d002bc89c92fe72359ece0be63d031305fbe81c39c811dc1026c8df052911'
ADMISSION_PATH=Path('/var/data/traceharbor-staging/actual-initial112.json')
def admission():
 if os.environ.get('RENDER')!='true' or os.environ.get('RENDER_EXTERNAL_HOSTNAME')!=r.HOST:raise Refusal('EXACT_RENDER_HOST')
 if hashlib.sha256((Path(__file__).parent/'release_integration68.py').read_bytes()).hexdigest()!=MODULE_SHA256:raise Refusal('INTEGRATION_SOURCE_PIN')
 private_dir(ADMISSION_PATH.parent);data=read(ADMISSION_PATH,65536)
 if hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()!=ADMISSION_SHA256:raise Refusal('ACTUAL_ADMISSION_PIN')
 c,e=data['config'],data['evidence'];r.ADMITTED_CONFIG_SHA256=digest(c);r.ADMITTED_CAPTURE_SHA256=digest(e);r.ADMITTED_EVIDENCE_SHA256=digest(e);r.WORKER_ENTRY=Path(__file__).resolve();r.WORKER_ADMISSION_PATH=ADMISSION_PATH
 r.qualify(c,e,pin=digest(c),capture_pin=digest(e),source_root=Path(__file__).parent)
 return c,e

CREDIT004R_PATH=Path('/var/data/traceharbor-staging/actual-recovery112.json')
CREDIT004R_SHA256='6868f7dc45ef0d0e432672ea66a2719e2415ad69dbb7344e1761b880b204b581'
def credit_admission004r():
 if os.environ.get('RENDER')!='true'or os.environ.get('RENDER_EXTERNAL_HOSTNAME')!=r.HOST:raise Refusal('EXACT_CREDIT67_RENDER_HOST')
 data=read(CREDIT004R_PATH,65536)
 if digest(data)!=CREDIT004R_SHA256 or data.get('schema')!='traceharbor.recovery004r.contract.v1':raise Refusal('EXACT_PRIVATE_CREDIT67_CONTRACT')
 r.checked_manifest(Path(__file__).parent,data['source_pins'])
 return data['policy']

def main():
 c,e=admission()
 if len(sys.argv)==3 and sys.argv[1]=='--credit-worker004r':
  import credit_scope004r,credit_runtime004r
  if Path(sys.argv[2])!=credit_scope004r.ROOT:raise Refusal('EXACT004_WORKER_ROOT')
  p=credit_admission004r()
  if p['release_config']!=c:raise Refusal('SAME_ORIGINAL_ALLOCATION_CONFIG_REQUIRED')
  return credit_runtime004r.worker(c,p)
 if len(sys.argv)!=1:raise Refusal('OLD_WORKERS_AND_ADMISSION_FLAGS_CLOSED')
 if not r.STATE.exists():raise Refusal('ORIGINAL_CONSUMED_STATE_REQUIRED_NO_REPROVISION')
 server=r.build_server(c,e,port=int(os.environ['PORT']),platform_port=os.environ['PORT'])
 try:
  import recovery004r
  recovery004r.wire(server,c)
  print('TraceHarbor004 configured; no automatic grant, capture, AI or billing',flush=True)
  server.serve_forever()
 finally:server.server_close()
if __name__=='__main__':main()
