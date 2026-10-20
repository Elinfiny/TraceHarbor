"""Redacted export is never a complete native original. No credential values in reports."""
import copy,hashlib,json,re
LABEL128='REDACTED_EXPORT_NOT_COMPLETE_TOOL_ORIGINAL'
FIELD128=('structuredContent','transfers',0,'completion_token')
def can128(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha128(b):return hashlib.sha256(b).hexdigest()
def scan128(value,path='$',depth=0):
 if depth>80:raise ValueError('Export nesting exceeded')
 if isinstance(value,dict):
  for k,v in value.items():
   if re.fullmatch(r'(?i)(completion_token|access_token|refresh_token|authorization|cookie|set-cookie|private_key|client_secret)',str(k)) and v not in (None,'',LABEL128):raise ValueError('Credential payload at '+path+'.'+str(k))
   scan128(v,path+'.'+str(k),depth+1)
 elif isinstance(value,list):
  for n,v in enumerate(value):scan128(v,path+'['+str(n)+']',depth+1)
 elif isinstance(value,str):
  if re.search(r'(?i)https?://[^\s"<>]+[?&](?:x-amz-signature|x-goog-signature|sig|signature|token|access_token)=|\bbearer\s+[A-Za-z0-9._~+/-]{12,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:ghp|gho|ghu|ghs|github_pat)_[A-Za-z0-9_]{20,}|\b(?:Cookie|Set-Cookie):\s*\S+=',value):raise ValueError('Embedded credential-shaped payload at '+path)
  stripped=value.strip()
  if stripped.startswith(('{','[','"')):
   try:decoded=json.loads(stripped)
   except (ValueError,TypeError):pass
   else:
    if decoded!=value:scan128(decoded,path+'.json',depth+1)
 return True
def project128(raw,paths=(FIELD128,)):
 original=json.loads(raw);projection=copy.deepcopy(original);changed=[]
 for path in paths:
  cursor=projection
  for key in path[:-1]:cursor=cursor[key]
  if not isinstance(cursor[path[-1]],str) or not cursor[path[-1]] or cursor[path[-1]]==LABEL128:raise ValueError('Exact nonempty opaque field required; no invented original')
  cursor[path[-1]]=LABEL128;changed.append(list(path))
 exported=can128(projection);scan128(projection)
 return exported,{'scope':LABEL128,'raw_original_bytes':len(raw),'raw_original_sha256':sha128(raw),'projection_bytes':len(exported),'projection_sha256':sha128(exported),'redacted_field_paths':changed,'raw_original_retention':'EXISTING_OWNER_PRIVATE_HISTORY; expiry/scope UNKNOWN; no revocation/deletion claim'}
