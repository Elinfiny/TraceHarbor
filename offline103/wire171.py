"""Pure closed CMS DER transport representation. No crypto, IO or authority.
Historical raw DER is available only through explicit historical_der104;
new source consumers accept only TRACE171_CMS_DER_UTF8_V1, never fallback.
"""
import base64,hashlib,json,re,math
SCHEMA='TRACE171_CMS_DER_UTF8_V1'
MAX_RAW=131072
CTX={'repository','repository_id','actor_id','run_id','attempt','source_sha','nonce','certificate_sha256','expires_utc'}
KEYS={'schema','context','der_bytes','der_sha256','der_base64'}
can=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf-8')
sha=lambda b:hashlib.sha256(b).hexdigest()
oid=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def require(ok):
 if not ok:raise ValueError('TRACE171_INVALID_WIRE_UNKNOWN_NO_RETRY')
def context171(c,now):
 require(type(c)is dict and set(c)==CTX and c['repository']=='Elinfiny/TraceHarbor' and type(c['repository_id'])is int and c['repository_id']==1391430317 and type(c['actor_id'])is int and c['actor_id']==273768139)
 require(type(c['run_id'])is int and c['run_id']>0 and type(c['attempt'])is int and c['attempt']==1 and type(c['expires_utc'])is int and type(now)in(int,float) and math.isfinite(now) and 0<=now<c['expires_utc'])
 for k,n in [('source_sha',40),('nonce',32),('certificate_sha256',64)]:require(type(c[k])is str and re.fullmatch('[a-f0-9]{'+str(n)+'}',c[k])is not None)
def envelope171(c,n,digest,encoded):return {'schema':SCHEMA,'context':c,'der_bytes':n,'der_sha256':digest,'der_base64':encoded}
def wire_size171(c,n):
 require(type(n)is int and 0<=n<=MAX_RAW)
 return len(can(envelope171(c,n,'f'*64,'')))+4*((n+2)//3)
def der_limit171(c,now):
 context171(c,now);lo,hi=0,MAX_RAW
 while lo<hi:
  mid=(lo+hi+1)//2
  if wire_size171(c,mid)<=MAX_RAW:lo=mid
  else:hi=mid-1
 return lo
def encode171(der,c,now):
 context171(c,now);require(type(der)is bytes and 0<len(der)<=der_limit171(c,now))
 raw=can(envelope171(c,len(der),sha(der),base64.b64encode(der).decode('ascii')));require(len(raw)==wire_size171(c,len(der)) and len(raw)<=MAX_RAW);return raw
def decode171(raw,c,now):
 context171(c,now);require(type(raw)is bytes and 0<len(raw)<=MAX_RAW)
 def pairs(items):
  d={}
  for k,v in items:require(k not in d);d[k]=v
  return d
 try:d=json.loads(raw.decode('utf-8',errors='strict'),object_pairs_hook=pairs,parse_constant=lambda _:require(False))
 except (ValueError,UnicodeError,TypeError)as e:raise ValueError('TRACE171_INVALID_JSON_UNKNOWN_NO_RETRY')from e
 require(type(d)is dict and set(d)==KEYS and d['schema']==SCHEMA);context171(d['context'],now);require(d['context']==c and can(d)==raw)
 require(type(d['der_bytes'])is int and 0<d['der_bytes']<=der_limit171(c,now) and type(d['der_sha256'])is str and re.fullmatch('[a-f0-9]{64}',d['der_sha256'])is not None and type(d['der_base64'])is str)
 try:der=base64.b64decode(d['der_base64'],validate=True)
 except (ValueError,TypeError)as e:raise ValueError('TRACE171_INVALID_BASE64_UNKNOWN_NO_RETRY')from e
 require(base64.b64encode(der).decode('ascii')==d['der_base64'] and len(der)==d['der_bytes'] and sha(der)==d['der_sha256']);return der
def pins171(raw,c,now):
 der=decode171(raw,c,now);return {'transport_schema':SCHEMA,'ciphertext_bytes':len(der),'ciphertext_sha256':sha(der),'wire_bytes':len(raw),'wire_sha256':sha(raw),'wire_gitblob':oid(raw)}
def metadata171(metadata):
 require(type(metadata)is dict and set(metadata)=={'artifact_digest','artifact_bytes','retention_days','custody_sha256'} and type(metadata['artifact_bytes'])is int and 0<metadata['artifact_bytes']<=65536 and type(metadata['retention_days'])is int and metadata['retention_days']==1)
 for k in ('artifact_digest','custody_sha256'):require(type(metadata[k])is str and re.fullmatch('[a-f0-9]{64}',metadata[k])is not None)
def delivery171(plan,metadata,now):
 require(plan.get('transport_schema')==SCHEMA);metadata171(metadata)
 raw=base64.b64decode(plan['wire_base64'],validate=True);require(base64.b64encode(raw).decode('ascii')==plan['wire_base64']);p=pins171(raw,plan['context'],now)
 require(all(type(plan.get(k))is type(v) and plan[k]==v for k,v in p.items()) and plan['operations'][0]['body']=={'content':plan['wire_base64'],'encoding':'base64'})
 der=decode171(raw,plan['context'],now);require(plan['ciphertext_base64']==base64.b64encode(der).decode('ascii'))
 return dict(metadata,context=plan['context'],ciphertext_base64=plan['ciphertext_base64'],wire_base64=plan['wire_base64'],**p)
def delivery_wire171(d,now):
 require(type(d)is dict and set(d)=={'context','ciphertext_base64','wire_base64','artifact_digest','artifact_bytes','retention_days','custody_sha256','transport_schema','ciphertext_bytes','ciphertext_sha256','wire_bytes','wire_sha256','wire_gitblob'})
 metadata171({k:d[k]for k in ('artifact_digest','artifact_bytes','retention_days','custody_sha256')})
 try:raw=base64.b64decode(d['wire_base64'],validate=True)
 except (ValueError,TypeError)as e:raise ValueError('TRACE171_DELIVERY_UNKNOWN_NO_RETRY')from e
 require(base64.b64encode(raw).decode('ascii')==d['wire_base64']);p=pins171(raw,d['context'],now);require(all(type(d[k])is type(v) and d[k]==v for k,v in p.items()));der=decode171(raw,d['context'],now)
 require(d['ciphertext_base64']==base64.b64encode(der).decode('ascii'));return raw
def receipt171(p,commit,ref):
 require(p['transport_schema']==SCHEMA and re.fullmatch('[a-f0-9]{40}',commit)is not None and type(ref)is str and ref.startswith('refs/heads/traceharbor-encrypted104-'))
 return dict(ciphertext_commit=commit,ref=ref,**{k:p[k]for k in ('transport_schema','ciphertext_bytes','ciphertext_sha256','wire_bytes','wire_sha256','wire_gitblob')})
def historical_der104(raw,bytes_pin,sha_pin,*,history_version):
 require(history_version==104 and type(raw)is bytes and 0<len(raw)<=MAX_RAW and len(raw)==bytes_pin and sha(raw)==sha_pin);return raw
