"""Pure request-bound verified Gitblob projection; no effects or capability.
The native port supplies its retained actual request/return and independently
verified immediate create canonical. Provider originals are never replaced.
"""
import base64,copy,hashlib,json,re
MAX_RAW=131072
PAIRS={'admit':'ADMIT_CHAIN','encrypted':'ENCRYPTED_CHAIN','consumed':'CONSUMED_CHAIN'}
URL=re.compile(r'https://api\.github\.com/repos/Elinfiny/TraceHarbor/git/blobs/([0-9a-f]{40})\Z')
can=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
sha=lambda x:hashlib.sha256(x).hexdigest()
oid=lambda raw:hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
class BlobUnknown170(ValueError):pass
def require(ok,msg):
 if not ok:raise BlobUnknown170(msg+'; UNKNOWN_NO_RETRY')
def paired170(value):
 require(type(value)is dict and set(value)=={'schema','value','current','native_authority'}and value['schema']=='TRACE152_AUTHENTIC_READ_PAIR'and value['native_authority']is False,'Exact original pair')
 return {'source_original170':value['value'],'current_original152':value['current']}
def is_blob170(request):
 return request.get('inventory_call_id')in tuple(p+'/blob/proof'for p in PAIRS)
def read170(request,returned,create_canonical,expected,active_phase,now_ms):
 """Source projection only, with mandatory original request + prior create.
 expected comes independently from the existing holder's exact chain body.
 A supplied dictionary never creates a native host or provider receipt.
 """
 require(type(request)is dict and type(returned)is dict,'Whole actual request/return')
 call=request.get('inventory_call_id');require(call in tuple(p+'/blob/proof'for p in PAIRS),'Only exact three wholeblob proofs');phase=call.split('/')[0]
 require(active_phase==PAIRS[phase],'Actual active chain phase')
 require(request.get('schema')=='TRACE118_HOST_REQUEST'and request.get('op')=='github_fetch'and type(request.get('seq'))is int and request['seq']>1,'Exact GET/sequence')
 args=request.get('args');require(type(args)is dict and set(args)=={'url'},'Closed actual GET args');match=URL.fullmatch(args['url'])if type(args['url'])is str else None;require(match is not None,'Exact immutable repo/path/OID allowlist');wanted=match.group(1)
 pre=copy.deepcopy(request);digest=pre.pop('request_digest',None);require(digest==sha(can(pre)),'Whole actual request digest')
 require(type(request.get('context'))is dict and type(request.get('inventory_sha256'))is str and re.fullmatch('[0-9a-f]{64}',request['inventory_sha256'])is not None,'Actual source context/inventory')
 require(type(now_ms)is int and type(request.get('issued_utc_ms'))is int and type(request.get('deadline_utc_ms'))is int and request['issued_utc_ms']<=now_ms<min(request['deadline_utc_ms'],request['issued_utc_ms']+15000),'Original fresh15 no renewal')
 require(returned.get('schema')=='TRACE118_HOST_RETURN'and returned.get('seq')==request['seq']and returned.get('context')==request['context']and returned.get('op')==request['op']and returned.get('request_digest')==digest,'Actual SAME request/seq/context return')
 require(returned.get('transport_error')is None and returned.get('late')is False,'No late/uncertain tool return')
 pair=returned.get('original_result');paired170(pair);original=pair['value'];require(type(original)is dict and not original.get('isError')and not original.get('tool_throw'),'Actual successful whole provider original')
 require(type(create_canonical)is dict and set(create_canonical)=={'identity','original'},'Whole retained prior create canonical')
 ident=create_canonical['identity'];require(type(ident)is dict and ident.get('operation')=='github_create_blob'and ident.get('tool')=='github_create_blob'and ident.get('seq')==request['seq']-1 and ident.get('context_sha256')==sha(can(request['context']))and re.fullmatch('[0-9a-f]{64}',str(ident.get('call_id','')))is not None,'Immediately preceding typed create identity')
 co=create_canonical['original'];require(type(co)is dict and not co.get('isError')and not co.get('tool_throw')and type(co.get('structuredContent'))is dict and co['structuredContent'].get('sha')==wanted,'OID independent from actual create original')
 require(type(expected)is dict and set(expected)=={'oid','bytes','sha256'}and expected['oid']==wanted and type(expected['bytes'])is int and 0<=expected['bytes']<=MAX_RAW and re.fullmatch('[0-9a-f]{64}',str(expected['sha256']))is not None,'Independent exact whole body pins required')
 value=original.get('structuredContent');require(type(value)is dict,'Actual structured original')
 # Explicit REST fields are distinct from the textual content of a JSON blob.
 # Never JSON-parse/reserialize a raw content string to guess a REST envelope.
 if {'sha','size','encoding','content'}<=set(value):
  require(set(value)<={'sha','size','encoding','content','node_id','url'}and value['sha']==wanted and value['encoding']=='base64'and type(value['size'])is int and 0<=value['size']<=MAX_RAW and type(value['content'])is str,'Complete genuine REST base64 fields')
  try:raw=base64.b64decode(value['content'].replace('\n','').replace('\r',''),validate=True)
  except (ValueError,TypeError)as e:raise BlobUnknown170('Invalid REST base64; UNKNOWN_NO_RETRY')from e
  require(len(raw)==value['size'],'REST whole count');representation='EXPLICIT_REST_BASE64_FIELDS'
 else:
  require(type(value.get('content'))is str,'Whole UTF8 raw string required; no binary guessing')
  try:raw=value['content'].encode('utf-8',errors='strict')
  except UnicodeError as e:raise BlobUnknown170('Invalid/lossy UTF8; UNKNOWN_NO_RETRY')from e
  representation='RAW_UTF8_CONTENT_BYTES'
 require(len(raw)<=MAX_RAW and len(raw)==expected['bytes']and oid(raw)==wanted and sha(raw)==expected['sha256'],'Whole EOF/count/GitOID/SHA256 equal independent pins')
 provenance={'schema':'TRACE170_DERIVED_LOCAL_VERIFIED_GITBLOB','classification':'DERIVED_LOCAL_VERIFIED_NOT_PROVIDER_METADATA','representation':representation,'request_digest':digest,'seq':request['seq'],'inventory_call_id':call,'active_phase':active_phase,'provider_original_canonical_sha256':sha(can(original)),'whole_return_canonical_sha256':sha(can(returned)),'create_original_canonical_sha256':sha(can(create_canonical)),'expected_body_sha256':expected['sha256'],'raw_sha256':sha(raw),'raw_bytes':len(raw),'oid':wanted,'native_authority':False}
 return {'sha':wanted,'size':len(raw),'encoding':'base64','content':base64.b64encode(raw).decode('ascii'),'derived_local_verified170':provenance}
def verify170(proof,raw):
 require(type(raw)is bytes and len(raw)<=MAX_RAW and type(proof)is dict and set(proof)=={'sha','size','encoding','content','derived_local_verified170'},'Exact derived projection and whole expected bytes')
 p=proof['derived_local_verified170'];require(type(p)is dict and p.get('schema')=='TRACE170_DERIVED_LOCAL_VERIFIED_GITBLOB'and p.get('classification')=='DERIVED_LOCAL_VERIFIED_NOT_PROVIDER_METADATA'and p.get('native_authority')is False,'Explicit derived provenance, never a forged provider result')
 require(proof['sha']==oid(raw)==p.get('oid')and proof['size']==len(raw)==p.get('raw_bytes')and proof['encoding']=='base64'and p.get('raw_sha256')==sha(raw)==p.get('expected_body_sha256'),'Exact original wholeblob contract')
 try:decoded=base64.b64decode(proof['content'],validate=True)
 except (ValueError,TypeError)as e:raise BlobUnknown170('Derived base64 changed; UNKNOWN_NO_RETRY')from e
 require(decoded==raw,'Whole byte-identical body, not JSON-reserialized');return True
