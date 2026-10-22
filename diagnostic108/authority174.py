"""Closed153 dispatch; all historical authority152 behavior delegated unchanged."""
import pathlib,runpy
R=pathlib.Path(__file__).resolve().parent
old=runpy.run_path(str(R/'authority152.py'));new=runpy.run_path(str(R/'authority153.py'))
for _n,_v in old.items():
 if not _n.startswith('__'):globals()[_n]=_v
def compare152(admission,current,proofA,proofB,routeA,routeB,policyA,policyB,direction,config,manifest_bytes):
 return (new if config['prestart154'].get('direction_number')==153 else old)['compare152'](admission,current,proofA,proofB,routeA,routeB,policyA,policyB,direction,config,manifest_bytes)
def admission152(own):return (new if own.get('state','').startswith('NATIVE153_')else old)['admission152'](own)
def verify152(own,current_docs,current_proofs,config,manifest_bytes):
 return (new if config['prestart154'].get('direction_number')==153 else old)['verify152'](own,current_docs,current_proofs,config,manifest_bytes)
