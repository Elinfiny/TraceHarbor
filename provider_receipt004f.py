"""Persist only a bounded redacted receipt of the ONE already reserved API call.
No network or worker on import. No authentication headers, secret or retry.
"""
import hashlib,json,re
from pathlib import Path
from quota_ledger import exclusive,private_dir
ROOT=Path('/var/data/traceharbor-recovery004f')
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
 value={'schema':'traceharbor.provider-receipt67.v1','http_status':status,'request_attempted':boundary.request_attempted,'primary_error':boundary.first_primary,'body_bytes':len(body),'body_sha256':hashlib.sha256(body).hexdigest(),'error_body_redacted':error,'success_body':'ONLY_VERIFIED_RESULT_STORES_SUCCESS_BODY'if status==200 else None,'retry':False,'paid_activation':False}
 exclusive(directory/'provider-response67.json',value);return value

def completion_metadata343(body, requested_model):
 """Untrusted HTTP200 metadata only: no raw text, IDs, reasoning or keys."""
 value={'schema':'traceharbor.completion-metadata343.v1','body_bytes':len(body),'body_sha256':hashlib.sha256(body).hexdigest(),'parse_state':'UNAVAILABLE','retry':False}
 if type(body)is not bytes or len(body)>262144:return value
 try:
  def unique(pairs):
   obj={}
   for k,v in pairs:
    if k in obj:raise ValueError('DUPLICATE_KEY')
    obj[k]=v
   return obj
  def no_constant(_):raise ValueError('NONFINITE_JSON')
  obj=json.loads(body,object_pairs_hook=unique,parse_constant=no_constant)
  if type(obj)is not dict:return value
  choices=obj.get('choices');value['parse_state']='JSON_OBJECT'
  value['model_matches_requested']=type(obj.get('model'))is str and obj['model']==requested_model
  if type(choices)is list:
   value['choice_count']=len(choices) if len(choices)<=128 else 'OVER_BOUND'
   if len(choices)==1 and type(choices[0])is dict:
    choice=choices[0];reason=choice.get('finish_reason');allowed={'stop','length','tool_calls','content_filter','function_call'}
    value['finish_reason']=reason if type(reason)is str and reason in allowed else ('MISSING_OR_NULL' if reason is None else 'OTHER')
    message=choice.get('message')
    if type(message)is dict:
     for name in ('content','reasoning','reasoning_content'):
      text=message.get(name)
      value[name]={'kind':'TEXT','utf8_bytes':len(text.encode()),'sha256':hashlib.sha256(text.encode()).hexdigest()}if type(text)is str else {'kind':'ABSENT_OR_NON_TEXT'}
     value['refusal_present']=bool(message.get('refusal'))
     value['tool_call_present']=bool(message.get('tool_calls')or message.get('function_call'))
  usage=obj.get('usage')
  if type(usage)is dict:
   value['usage']={k:v for k in ('prompt_tokens','completion_tokens','total_tokens')if type(v:=usage.get(k))is int and 0<=v<=1000000000}
   details=usage.get('completion_tokens_details')
   if type(details)is dict and type(n:=details.get('reasoning_tokens'))is int and 0<=n<=1000000000:value['usage']['reasoning_tokens']=n
 except (ValueError,TypeError,KeyError,AttributeError,RecursionError,UnicodeError):
  return {'schema':value['schema'],'body_bytes':value['body_bytes'],'body_sha256':value['body_sha256'],'parse_state':'MALFORMED_OR_UNSUPPORTED','retry':False}
 return value

def retain_completion343(body, directory, requested_model):
 directory=Path(directory)
 if directory!=ROOT:raise ValueError('EXACT_PROVIDER_RECEIPT_ROOT')
 private_dir(directory);value=completion_metadata343(body,requested_model)
 exclusive(directory/'provider-completion343.json',value)
 return value
