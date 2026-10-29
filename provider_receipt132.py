"""Persist only a bounded redacted receipt of the ONE already reserved API call.
No network or worker on import. No authentication headers, secret or retry.
"""
import hashlib,json,re
from pathlib import Path
from quota_ledger import exclusive,private_dir
ROOT=Path('/var/data/traceharbor-release68')
def redact(value,key):
 if isinstance(value,dict):return {str(k)[:80]:('[REDACTED]'if re.search('authorization|cookie|api.?key|access.?token|secret|password',str(k),re.I)else redact(v,key))for k,v in value.items()}
 if isinstance(value,list):return [redact(v,key)for v in value[:32]]
 if isinstance(value,str):
  text=value.replace(key,'[REDACTED]')if key else value
  text=re.sub(r'Bearer\s+\S+','Bearer [REDACTED]',text,flags=re.I);text=re.sub(r'https?://\S+','[URL REDACTED]',text);text=re.sub(r'[\w.+-]+@[\w.-]+','[EMAIL REDACTED]',text)
  return text[:4096]
 return value if value is None or type(value)in(bool,int,float)else '[REDACTED]'
def retain(boundary,directory,key):
 directory=Path(directory)
 if directory!=ROOT:raise ValueError('EXACT_PROVIDER_RECEIPT_ROOT')
 private_dir(directory);items=boundary.vault.originals;statuses=[v for _,kind,v in items if kind=='HTTP_STATUS'];bodies=[v for _,kind,v in items if kind in('BYTES','PARTIAL')and type(v)is bytes];body=bodies[-1]if bodies else b''
 status=statuses[-1]if statuses else None;error=None
 if status!=200 and body:
  try:error=redact(json.loads(body),key)
  except Exception:error={'text':redact(body[:8192].decode('utf8','replace'),key)}
  raw=json.dumps(error,ensure_ascii=False,sort_keys=True)
  if len(raw.encode())>16384:error={'redacted_prefix':raw[:4096],'truncated':True}
 value={'schema':'traceharbor.provider-receipt132.v1','http_status':status,'request_attempted':boundary.request_attempted,'primary_error':boundary.first_primary,'body_bytes':len(body),'body_sha256':hashlib.sha256(body).hexdigest(),'error_body_redacted':error,'success_body':'ONLY_VERIFIED_RESULT_STORES_SUCCESS_BODY'if status==200 else None,'retry':False,'paid_activation':False}
 exclusive(directory/'provider-response132.json',value);return value
