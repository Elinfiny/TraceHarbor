"""PRIVATE42. Mechanical evidence checks, never independent Auditor or live grant.
No network implementation. Redirect origin contract remains unqualified/defaultNone.
"""
import base64
import datetime as dt
import hashlib
import ipaddress
import json
import re
from urllib.parse import urlsplit

REPO='Elinfiny/TraceHarbor'; RID=1391430317; OWNER=273768139
BASE='/repos/'+REPO
REF='refs/tags/traceharbor-once-qualification17/canary'
NONCE='TRACEHARBOR-NATIVE-QUALIFICATION27-20261015-01'
WORKFLOW='.github/workflows/traceharbor-native27.yml'
RECORD_MAX=65536; ENVELOPE_MAX=786432; LOG_MAX=1048576
BEGIN=b'TRACE42_BEGIN '; END=b'TRACE42_END '
SYNTHETIC_CAP=object()  # Test-only capability; never accepted for a live descriptor.

class Refuse(Exception): pass
def need(ok,code):
    if not ok: raise Refuse(code)
def digest(b): return hashlib.sha256(b).hexdigest()
def canonical(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def exact(x,keys,code='SCHEMA'):
    need(type(x) is dict and set(x)==set(keys),code)
def integer(n,minimum=0): return type(n) is int and n>=minimum
def unique(pairs):
    d={}
    for k,v in pairs:
        need(k not in d,'DUPLICATE_JSON_KEY'); d[k]=v
    return d
def reject_number(_): raise Refuse('NONINTEGER_JSON_NUMBER')
def parse(b,limit):
    need(type(b) is bytes and len(b)<=limit,'BOUNDED_BYTES')
    try:return json.loads(b.decode('utf-8','strict'),object_pairs_hook=unique,
                          parse_float=reject_number,parse_constant=reject_number)
    except Refuse:raise
    except (ValueError,UnicodeError,TypeError):raise Refuse('JSON_OR_UTF8') from None

def bindings(b):
    exact(b,['repository_id','owner_id','source','workflow_sha256','driver_sha256',
             'validator_sha256','workflow_id','first_run_id','attempt','nonce','ref','commit','tree'])
    need(type(b['repository_id']) is int and b['repository_id']==RID and
         type(b['owner_id']) is int and b['owner_id']==OWNER,'REPOSITORY_OWNER')
    need(type(b['attempt']) is int and b['attempt']==1,'ATTEMPT')
    need(integer(b['workflow_id'],1) and integer(b['first_run_id'],1),'IDS')
    for k in ['source','commit','tree']:need(type(b[k]) is str and re.fullmatch('[0-9a-f]{40}',b[k]),'SHA40')
    for k in ['workflow_sha256','driver_sha256','validator_sha256']:need(type(b[k]) is str and re.fullmatch('[0-9a-f]{64}',b[k]),'SHA256')
    need(b['nonce']==NONCE and b['ref']==REF,'ONCE_BINDING')
    return b

def manifest(b):
    return {'schema':'PRIVATE_NATIVE_QUALIFICATION_ONLY','request_authority':None,
            'repository_id':RID,'target':REF,'nonce':NONCE,'source':b['source'],
            'workflow_sha256':b['workflow_sha256'],'driver_sha256':b['driver_sha256'],
            'first_run_id':str(b['first_run_id'])}

def object_schema(x,required,optional=()):
    need(type(x) is dict and set(required)<=set(x) and set(x)<=set(required)|set(optional),'CONTEXTUAL_FIELDS')
def text(x,maximum=65536,nullable=False):
    if nullable and x is None:return
    need(type(x) is str and len(x.encode('utf-8'))<=maximum,'CONTEXTUAL_TEXT')
    need(not re.search(r'(?i)(github_pat_|gh[pousr]_|bearer\s|-----BEGIN .*PRIVATE KEY)',x),'PRIVATE_VALUE')
def sha40(x):need(type(x) is str and re.fullmatch('[0-9a-f]{40}',x) is not None,'CONTEXTUAL_SHA')
def native_url(x,documentation=False):
    text(x,2048);u=urlsplit(x)
    hosts={'docs.github.com'} if documentation else {'api.github.com','github.com'}
    need(u.scheme=='https' and u.hostname in hosts and not u.username and not u.password and
         u.port in (None,443) and not u.query and (documentation or not u.fragment),'PUBLIC_NATIVE_URL')
def descriptor(x,parent=False):
    object_schema(x,{'sha'},{'url','html_url'} if parent else {'url'});sha40(x['sha'])
    for k in ['url','html_url']:
        if k in x:native_url(x[k])
def person(x):
    object_schema(x,{'name','email','date'});text(x['name'],512);text(x['email'],512);text(x['date'],64)
    timestamp(x['date'])
def verification(x):
    object_schema(x,{'verified','reason','signature','payload'},{'verified_at'})
    need(type(x['verified']) is bool,'VERIFICATION_BOOLEAN');text(x['reason'],128)
    text(x['signature'],65536,True);text(x['payload'],65536,True)
    if 'verified_at' in x and x['verified_at'] is not None:timestamp(x['verified_at'])
def tree_entry(x):
    object_schema(x,{'path','mode','type','sha'},{'size','url'})
    text(x['path'],4096);need(x['path'] and not x['path'].startswith('/') and '\\' not in x['path'] and
         '\x00' not in x['path'] and '..' not in x['path'].split('/'),'TREE_PATH')
    need(type(x['mode']) is str and x['mode'] in ('040000','100644','100755','120000','160000'),'TREE_MODE')
    need(type(x['type']) is str and x['type'] in ('tree','blob','commit'),'TREE_TYPE');sha40(x['sha'])
    if 'size' in x:need(integer(x['size']) and x['size']<=2**63-1,'TREE_SIZE_STRICT_INTEGER')
    if 'url' in x:native_url(x['url'])
def public_shape(x,kind):
    """Context-specific native public Git schemas; reject extras, never redact.
    Optional native metadata is finite: commit node/url/html/people/verification;
    tree/ref node/url, entry size/url, parent html/url, verification verified_at.
    These are schema checks, not vendor authentication or an admission.
    """
    if kind=='absence404':
        object_schema(x,{'message'},{'documentation_url','status'});need(x['message']=='Not Found','ABSENCE_MESSAGE')
        if 'status' in x:need(type(x['status']) is str and x['status']=='404','ABSENCE_STATUS')
        if 'documentation_url' in x:native_url(x['documentation_url'],True)
    elif kind=='GitCommit':
        object_schema(x,{'sha','message','tree','parents'},{'node_id','url','html_url','author','committer','verification'})
        sha40(x['sha']);text(x['message']);descriptor(x['tree'])
        need(type(x['parents']) is list and len(x['parents'])<=16,'COMMIT_PARENTS')
        for item in x['parents']:descriptor(item,True)
        for k in ['author','committer']:
            if k in x:person(x[k])
        if 'verification' in x:verification(x['verification'])
    elif kind=='GitTree':
        object_schema(x,{'sha','tree','truncated'},{'url'});sha40(x['sha'])
        need(type(x['truncated']) is bool and type(x['tree']) is list and len(x['tree'])<=256,'TREE_SCHEMA')
        for item in x['tree']:tree_entry(item)
    elif kind=='GitRef':
        object_schema(x,{'ref','object'},{'node_id','url'});text(x['ref'],1024)
        obj=x['object'];object_schema(obj,{'type','sha'},{'url'});need(obj['type']=='commit','REF_OBJECT_TYPE');sha40(obj['sha'])
        if 'url' in obj:native_url(obj['url'])
    else:raise Refuse('PUBLIC_RECORD_KIND')
    for k in ['url','html_url']:
        if k in x:native_url(x[k])
    if 'node_id' in x:text(x['node_id'],512)


def expected(b):
    r=BASE+'/git/ref/'+REF[5:];c=BASE+'/git/commits/'+b['commit'];t=BASE+'/git/trees/'+b['tree']
    return [('GET',r,404),('POST',BASE+'/git/commits',201),('GET',c,200),('GET',t,200),
            ('POST',BASE+'/git/refs',201),('GET',r,200),('GET',c,200),('GET',t,200)]

def check_body(index,body,b):
    x=parse(body,RECORD_MAX);need(type(x) is dict,'PUBLIC_OBJECT')
    kind='absence404' if index==0 else 'GitCommit' if index in (1,2,6) else 'GitTree' if index in (3,7) else 'GitRef'
    public_shape(x,kind)
    if index==0:
        need(set(x)<={'message','documentation_url','status'} and x.get('message')=='Not Found' and
             ('status' not in x or x['status']=='404'),'ABSENCE_BODY')
    elif index in (1,2,6):
        need(x.get('sha')==b['commit'] and type(x.get('tree')) is dict and x['tree'].get('sha')==b['tree'],'COMMIT_TREE')
        need(type(x.get('parents')) is list and len(x['parents'])==1 and x['parents'][0].get('sha')==b['source'],'COMMIT_PARENT')
        need(x.get('message')==canonical(manifest(b)).decode(),'COMMIT_MANIFEST')
    elif index in (3,7):
        need(x.get('sha')==b['tree'] and type(x.get('tree')) is list and x.get('truncated') is False,'TREE_BODY')
    else:
        need(x.get('ref')==REF and type(x.get('object')) is dict and
             x['object'].get('sha')==b['commit'] and x['object'].get('type')=='commit','REF_BODY')
    return x

class Producer:
    def __init__(self):self.raw=[];self.first_unknown=None;self.overflow=[];self.emitted=False
    def capture(self,method,path,status,body):
        # Retain bounded original BEFORE any semantic, status, parse or deadline check.
        bounded=body[:RECORD_MAX+1] if type(body) is bytes else b''
        self.raw.append((method,path,status,bounded))
        if type(body) is not bytes or len(body)>RECORD_MAX:
            self.overflow.append({'observed_count':len(body) if type(body) is bytes else None,
                                  'captured_count':len(bounded),'captured_sha256':digest(bounded),'full_body':False})
            self.first_unknown=self.first_unknown or 'OVERSIZED_OBSERVED_PREFIX_ONLY'
    def frame(self,b,guard):
        need(not self.emitted,'EMIT_CONSUMED');self.emitted=True
        need(self.first_unknown is None,'FIRST_UNKNOWN');bindings(b);need(len(self.raw)==8,'RECORD_COUNT')
        records=[]
        for i,((m,p,s,raw),(em,ep,es)) in enumerate(zip(self.raw,expected(b))):
            need(type(s) is int and (m,p,s)==(em,ep,es),'RECORD_BINDING');check_body(i,raw,b)
            records.append({'ordinal':i+1,'method':m,'path':p,'status':s,'count':len(raw),
                            'sha256':digest(raw),'body_b64':base64.b64encode(raw).decode()})
        envelope=canonical({'schema':'TRACE_FIRST_PUBLIC_ORIGINALS_V1','bindings':b,'records':records})
        need(len(envelope)<=ENVELOPE_MAX,'ENVELOPE_BOUND');guard('PRE_FRAME_FINAL_GUARD')
        h=digest(envelope).encode();frame=BEGIN+str(len(envelope)).encode()+b' '+h+b'\n'+envelope+b'\n'+END+h+b'\n'
        guard('PRE_FRAME_EMIT');return frame

def decode_frame(log):
    need(type(log) is bytes and len(log)<=LOG_MAX,'LOG_BOUND');need(b'***' not in log,'MASKED_LOG')
    need(log.count(BEGIN)==1 and log.count(END)==1,'DUPLICATE_OR_MISSING_FRAME')
    # Native log timestamps are framing metadata, never part of original payload.
    all_lines=[re.sub(rb'^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d{1,9})?Z ',b'',x) for x in log.splitlines()]
    start=[i for i,x in enumerate(all_lines) if x.startswith(BEGIN)]
    need(len(start)==1 and start[0]+2<len(all_lines) and log.endswith(b'\n'),'FRAME_TRUNCATED_OR_EXTRA')
    lines=all_lines[start[0]:start[0]+3]
    need(lines[0].startswith(BEGIN) and lines[2].startswith(END),'FRAME_MARKERS')
    parts=lines[0][len(BEGIN):].split(b' ');need(len(parts)==2 and re.fullmatch(b'[0-9]+',parts[0]),'FRAME_HEADER')
    need(parts[0]==str(len(lines[1])).encode() and parts[1]==digest(lines[1]).encode() and
         lines[2]==END+parts[1],'FRAME_HASH_OR_COUNT')
    e=parse(lines[1],ENVELOPE_MAX);exact(e,['schema','bindings','records']);need(e['schema']=='TRACE_FIRST_PUBLIC_ORIGINALS_V1','ENVELOPE_SCHEMA');bindings(e['bindings'])
    need(type(e['records']) is list and len(e['records'])==8,'RECORD_COUNT')
    hashes=[]
    for i,(r,(m,p,s)) in enumerate(zip(e['records'],expected(e['bindings']))):
        exact(r,['ordinal','method','path','status','count','sha256','body_b64'])
        need(type(r['ordinal']) is int and r['ordinal']==i+1 and type(r['status']) is int and
             (r['method'],r['path'],r['status'])==(m,p,s),'RECORD_ORDER_OR_BINDING')
        need(integer(r['count']) and r['count']<=RECORD_MAX and type(r['body_b64']) is str and len(r['body_b64'])<=87384,'RECORD_BOUND')
        try:raw=base64.b64decode(r['body_b64'],validate=True)
        except (ValueError,TypeError):raise Refuse('BASE64') from None
        need(base64.b64encode(raw).decode()==r['body_b64'] and len(raw)==r['count'] and digest(raw)==r['sha256'],'ORIGINAL_COUNT_OR_HASH')
        check_body(i,raw,e['bindings']);hashes.append(r['sha256'])
    return e,hashes,digest(lines[1])

class Sticky:
    def __init__(self):self.first_unknown=None;self.originals=[];self.cleanup_errors=[]
    def retain(self,value):self.originals.append(value)
    def fail(self,code):self.first_unknown=self.first_unknown or code;raise Refuse(self.first_unknown)

def timestamp(s):
    need(type(s) is str and s.endswith('Z'),'UTC_TIMESTAMP')
    try:x=dt.datetime.fromisoformat(s[:-1]+'+00:00')
    except ValueError:raise Refuse('UTC_TIMESTAMP') from None
    return x.timestamp()

def context(b,run,job,observed,now,remaining,controller=False):
    need(type(now) in (int,float) and type(now) is not bool and type(remaining) in (int,float) and remaining>0,'CLOCK_INPUT')
    need(run.get('id')==b['first_run_id'] and type(run.get('id')) is int and
         run.get('run_attempt')==1 and type(run.get('run_attempt')) is int and
         run.get('repository_id')==RID and run.get('owner_id')==OWNER and
         run.get('actor_id')==OWNER and run.get('triggering_actor_id')==OWNER and
         run.get('event')=='workflow_dispatch' and run.get('head_branch')=='main' and
         run.get('head_sha')==b['source'] and type(run.get('workflow_id')) is int and run.get('workflow_id')==b['workflow_id'] and
         run.get('path')==WORKFLOW,'RUN_IDENTITY')
    need(run.get('status') in ('in_progress','completed'),'RUN_STATE')
    if controller:need(run.get('status')=='completed' and run.get('conclusion')=='success','FIRST_RUN_NOT_TERMINAL_SUCCESS')
    need(integer(job.get('id'),1) and type(job.get('run_id')) is int and job.get('run_id')==b['first_run_id'] and type(job.get('attempt')) is int and job.get('attempt')==1 and
         job.get('head_sha')==b['source'] and job.get('status')=='completed' and job.get('conclusion')=='success','WRITER_JOB_NOT_SUCCESS')
    need(observed.get('main')==b['source'] and observed.get('workflow_sha256')==b['workflow_sha256'] and
         observed.get('driver_sha256')==b['driver_sha256'] and observed.get('validator_sha256')==b['validator_sha256'] and
         observed.get('commit')==b['commit'] and observed.get('tree')==b['tree'] and observed.get('ref_commit')==b['commit'],'SOURCE_OR_READBACK_DRIFT')
    start=timestamp(run['run_started_at']);age=now-start
    need(0<=age<300 and remaining<=(300-age),'LATE_SKEW_OR_REMAINING')
    return age,start+300

def validate(log,run,writer_job,observed,now,remaining=1,state=None):
    state=state or Sticky()
    try:
        # Original input/exception holder is PRIVATE, never serialized into receipt.
        state.retain(('VALIDATION_INPUTS',log,run,writer_job,observed))
        need(state.first_unknown is None,'FIRST_UNKNOWN')
        need(type(log) is bytes and len(log)<=LOG_MAX,'LOG_BOUND')
        need(all(type(x) is dict for x in (run,writer_job,observed)),'METADATA_OBJECTS')
        e,hashes,h=decode_frame(log);b=e['bindings']
        age,expiry=context(b,run,writer_job,observed,now,remaining)
        r={'schema':'TRACE_READONLY_VALIDATOR_V1','verdict':'PASS','reason':'MECHANICAL_ONLY',
           'bindings':b,'original_hashes':hashes,'envelope_sha256':h,'writer_job_id':writer_job['id'],
           'writer_terminal':'completed/success','age_seconds':int(age),'expires_at':int(expiry),
           'independent_auditor':False,'native_http_vendor_attestation':False}
        need(len(canonical(r))<=4096,'RECEIPT_BOUND');return r
    except Exception as error:
        state.retain(('PRIMARY_VALIDATION_EXCEPTION',error))  # BEFORE conversion/guard.
        code=str(error) if isinstance(error,Refuse) else 'VALIDATION_INPUT_EXCEPTION'
        state.fail(code)

def fetch_job_log(api,download,job_id,state=None,origin_contract=None,synthetic_cap=None):
    """Complete callback exception boundary; fake/inactive origin gate unchanged.
    Resource cleanup belongs to injected adapters; cleanup_errors is separate and
    never replaces firstUNKNOWN. No network adapter/production origin is created.
    """
    state=state or Sticky();phase='PRE_REQUEST'
    try:
        need(state.first_unknown is None,'FIRST_UNKNOWN');need(integer(job_id,1),'JOB_ID')
        need(synthetic_cap is SYNTHETIC_CAP and type(origin_contract) is dict and
             origin_contract.get('classification')=='SYNTHETIC_ONLY','ORIGIN_CONTRACT_UNQUALIFIED')
        phase='API_CALLBACK_PRE_INVOKE'
        first=api(BASE+'/actions/jobs/'+str(job_id)+'/logs')
        state.retain(('API_ORIGINAL_RETURN',first))  # Immediately, before any use.
        phase='API_POST_RETURN'
        status,headers,_=first;need(type(status) is int and status==302,'JOBLOG_NOT_302')
        need(type(headers) is dict,'API_HEADERS_SCHEMA');loc=headers.get('Location');need(type(loc) is str,'LOCATION')
        u=urlsplit(loc);need(u.scheme=='https' and not u.username and not u.password and not u.fragment and
                            u.port in (None,443) and u.hostname in origin_contract.get('hosts',[]),'UNSAFE_LOG_ORIGIN')
        try:ipaddress.ip_address(u.hostname);raise Refuse('IP_ORIGIN')
        except ValueError:pass
        phase='DOWNLOAD_CALLBACK_PRE_INVOKE'
        response=download(loc,headers={})
        state.retain(('DOWNLOAD_ORIGINAL_RETURN',response))  # BEFORE type/clock/status.
        phase='DOWNLOAD_POST_RETURN'
        status,headers,body=response
        need(type(status) is int and status==200,'SECOND_REDIRECT_OR_STATUS')
        need(type(headers) is dict and type(body) is bytes and len(body)<=LOG_MAX,'LOG_BOUND')
        if 'Content-Length' in headers:need(headers['Content-Length']==str(len(body)),'TRUNCATED_LOG')
        body.decode('utf-8','strict');return body
    except Exception as error:
        state.retain(('PRIMARY_TRANSPORT_EXCEPTION',error))  # Raw object PRIVATE first.
        if phase=='API_CALLBACK_PRE_INVOKE':code='API_CALLBACK_EXCEPTION'
        elif phase=='DOWNLOAD_CALLBACK_PRE_INVOKE':code='DOWNLOAD_CALLBACK_EXCEPTION'
        elif isinstance(error,Refuse):code=str(error)
        else:code='TRANSPORT_SCHEMA_EXCEPTION'
        state.fail(code)  # No exception string or signed Location is exported.


if __name__=='__main__':
    raise SystemExit('INACTIVE42_NO_ADMISSION_NO_NATIVE_TRANSPORT')
