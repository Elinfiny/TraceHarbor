"""Candidate168 closed metadata pair budget. Pure DATA; no provider/native API."""
import math
PHASES=('SOURCE_FREEZE','PRE_DISPATCH','ADMIT_CHAIN','ENCRYPTED_CHAIN','CONSUMED_CHAIN','TERMINAL')
CONTRACT={'schema':'TRACE168_METADATA_PAIR75_V1','whole_pair_ms':75000,'publish_max_ms':50000,'readback_reserved_ms':25000,'other_provider_ms':15000,'renewal':False,'authority_freshness_ms':15000}
def frame168(call_id,op,issued_ms,parent_ms,phase_ms,pair_ms=None):
 if any(type(x) is not int or x<0 for x in (issued_ms,parent_ms,phase_ms)) or issued_ms>=min(parent_ms,phase_ms):raise TimeoutError('Original finite phase/parent cutoff')
 parts=call_id.split('/');metadata=len(parts)==2 and parts[0] in PHASES and (parts[1],op) in (('CAS','library_replace'),('readback','library_materialize'))
 end=min(parent_ms,phase_ms)
 if metadata:
  if type(pair_ms) is not int or not issued_ms<pair_ms<=end or pair_ms-issued_ms>75000:raise ValueError('Original source-owned single pair deadline required')
  end=min(end,pair_ms);cap=50000 if parts[1]=='CAS' else 25000
  cutoff=min(issued_ms+cap,end-25000 if parts[1]=='CAS' else end)
 else:cutoff=min(issued_ms+15000,end)
 if cutoff<=issued_ms:raise TimeoutError('Insufficient same pair suffix reserve')
 return {'issued_utc_ms':issued_ms,'deadline_utc_ms':cutoff,'phase_deadline_utc_ms':end,'frame_contract168':{'schema':CONTRACT['schema'],'kind':'METADATA_PAIR' if metadata else 'PROVIDER15','pair_deadline_utc_ms':end if metadata else None}}
def authority_fresh168(request,now_ms):
 if type(now_ms) is not int or type(request.get('issued_utc_ms')) is not int or now_ms<request['issued_utc_ms'] or now_ms>=min(request['issued_utc_ms']+15000,request['deadline_utc_ms']):raise TimeoutError('Fresh A/B original15s unchanged before next effect')
 return True
