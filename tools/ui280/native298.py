"""Pinned native materializer. Expectations != observed facts != release proof.
No IO/import side effects. External provider provenance is verified by caller298.js.
"""
import os,json,hashlib,stat,time,pwd,re,resource
MASTER='libfile_f67b07d0a4288191b60f3469d264f99c';AUDITOR_ANCHOR='libfile_f87a6a307f70819194e0af0fa453afd1';AUDITOR_CURRENT='libfile_779cb59e1cd08191a438c5537497f60d'
def need(x,msg):
 if not x:raise RuntimeError(msg)
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def safeint(x,lo=1,hi=9007199254740991):need(type(x)is int and lo<=x<=hi,'TYPED_INTEGER');return x
def receipt(x,stable):
 need(isinstance(x,dict)and x.get('stable')==stable,'RECEIPT_REFERENCE');safeint(x.get('version'),2);need(x.get('raw_sha256')not in['1'*64,'2'*64],'LEGACY_FIXTURE_NOT_NATIVE')
 for k in ['raw_sha256','self_sha256']:need(re.fullmatch('[0-9a-f]{64}',x.get(k,''))is not None,'RECEIPT_HASH')
def verify_external(a,pins):
 need(a.get('schema')=='TRACE298_PREPUBLICATION_V1'and a.get('state')=='ADMITTED_ONCE','PREPUBLICATION_NOT_ADMITTED')
 need(a.get('source_pins')==pins and a.get('parent')=='d502e3b79735ff065b7d9d936c8330ff14bd21a0','SOURCE_VECTOR_PARENT')
 e=a.get('evidence',{});receipt(e.get('master'),MASTER);receipt(e.get('auditor_current'),AUDITOR_CURRENT)
 need(e.get('auditor_identity_anchor')==AUDITOR_ANCHOR,'AUDITOR_CHAIN')
 need(e['auditor_current'].get('source_vector_sha256')==digest(pins)and e['master'].get('source_vector_sha256')==digest(pins),'CURRENT_ADOPTION_VECTOR')
 need(e['master'].get('once_state')=='RESERVED'and e['auditor_current'].get('review_selector')and e['auditor_current'].get('body_sha256'),'CURRENT_ONCE_AND_REVIEW')
 b=a.get('budget',{});need(b.get('whole_resident_cap')==536870912 and b.get('worker_physical_cap')==335544320 and b.get('swap_max')==0 and b.get('resident_domain')=='ONE_ADMITTED_GITHUB_JOB_CONTROLLER_WORKER_AND_MANAGER','RESIDENT_DOMAIN_BUDGET')
 need(a.get('free_existing_host')is True and a.get('sandbox_required')is True,'PROSPECTIVE_AUTH_REQUIREMENTS')
 need(re.fullmatch('[A-Z0-9_-]{8,96}',a.get('effect_id',''))is not None,'NEW_EFFECT_ID')
 return a
def safe_file(filename,limit=268435456,read=False):
 need(os.path.isabs(filename)and all(x not in ['','.','..']for x in filename[1:].split('/')),'PATH')
 real=os.path.realpath(filename);need(os.path.isabs(real),'REALPATH');current=''
 for part in real[1:].split('/'):
  current+='/'+part;s=os.lstat(current);need(not stat.S_ISLNK(s.st_mode)and s.st_uid==0 and not(s.st_mode&0o022),'ROOT_COMPONENT_DRIFT')
 fd=os.open(real,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK);start=time.monotonic();h=hashlib.sha256();n=0;data=bytearray()
 try:
  pre=os.fstat(fd);need(stat.S_ISREG(pre.st_mode)and 0<pre.st_size<=limit,'FILE_SIZE_TYPE')
  while True:
   need(time.monotonic()-start<5,'HASH5S');chunk=os.read(fd,8192)
   if not chunk:break
   n+=len(chunk);need(n<=limit,'FILE_BOUND');h.update(chunk)
   if read and len(data)<65536:data.extend(chunk[:65536-len(data)])
  post=os.fstat(fd);need(n==pre.st_size and(pre.st_dev,pre.st_ino,pre.st_size,pre.st_mtime_ns)==(post.st_dev,post.st_ino,post.st_size,post.st_mtime_ns),'FILE_DRIFT')
  return {'path':filename,'realpath':real,'bytes':n,'sha256':h.hexdigest(),'uid':pre.st_uid,'mode':stat.S_IMODE(pre.st_mode),'data':bytes(data)if read else None}
 finally:os.close(fd)
class NativeFacts:
 def __init__(self,env):self.env=env
 def identity(self):
  u=int(self.env['TRACE298_CALLER_UID']);g=int(self.env['TRACE298_CALLER_GID']);p=pwd.getpwuid(u);need(u>0 and p.pw_gid==g,'PWD_IDENTITY');return {'uid':u,'gid':g,'image':self.env.get('ImageVersion'),'os':self.env.get('ImageOS'),'image_present':'ImageVersion'in self.env,'os_present':'ImageOS'in self.env,'parent_netns':os.readlink('/proc/self/ns/net'),'parent_mntns':os.readlink('/proc/self/ns/mnt')}
 def file(self,path,read=False):return safe_file(path,read=read)
def image_identity_diagnostic(native,expected,env,manifest_sha256):
 # Only the two exact identity inputs; no environment dump or coercion.
 def field(value,present):
  ty=type(value);name={str:'str',type(None):'NoneType',bool:'bool',int:'int',float:'float',list:'list',dict:'dict',tuple:'tuple',bytes:'bytes'}.get(ty,'UNSUPPORTED')
  result={'present':present is True,'type':name,'length':len(value)if ty in[str,list,dict,tuple,bytes]else None}
  if ty is str:
   if len(value)<=128:result['value']=value
   else:result.update(oversize=True,sha256=hashlib.sha256(value.encode('utf-8','surrogatepass')).hexdigest())
  elif value is None:result['value']=None
  else:result['unsupported_type']=True
  return result
 run=env.get('GITHUB_RUN_ID','');commit=env.get('GITHUB_SHA','')
 need(isinstance(run,str)and re.fullmatch('[0-9]{1,20}',run)is not None and isinstance(commit,str)and re.fullmatch('[0-9a-f]{40}',commit)is not None,'NATIVE_JOB_TYPED')
 need(type(expected['image'])is str and len(expected['image'])<=128 and re.fullmatch('[0-9a-f]{64}',manifest_sha256)is not None,'IDENTITY_DIAGNOSTIC_SOURCE')
 diag={'event':'IMAGE_IDENTITY302','ImageVersion':field(native['image'],native.get('image_present')),'ImageOS':field(native['os'],native.get('os_present')),'expectedimage':expected['image'],'requiredImageOS':'ubuntu24','image_matches':native['image']==expected['image'],'os_matches':native['os']=='ubuntu24','run':run,'commit':commit,'manifest_sha256':manifest_sha256}
 need(len(json.dumps(diag,ensure_ascii=True,separators=(',',':')).encode())<=2048,'IDENTITY_DIAGNOSTIC_BOUND')
 return diag
def materialize(a,pins,env,event,source,stage,expected,facts):
 verify_external(a,pins);need(a.get('source')in[source,'__NATIVE_CHECKOUT__']and os.path.realpath(source)==source,'SOURCE_REDIRECT');native=facts.identity();safeint(native['uid']);safeint(native['gid'])
 need(native['uid']==expected['uid']and native['gid']==expected['gid'],'UID_GID_DRIFT')
 diagnostic=image_identity_diagnostic(native,expected,env,pins['contracts/host298.json']);native['identity_diagnostic']=diagnostic
 try:need(native['image']==expected['image']and native['os']=='ubuntu24','IMAGE_DRIFT')
 except RuntimeError as error:
  error.identity_diagnostic=diagnostic;raise
 need(re.fullmatch(r'net:\[[0-9]+\]',native['parent_netns'])is not None and re.fullmatch(r'mnt:\[[0-9]+\]',native['parent_mntns'])is not None,'NAMESPACE_NATIVE')
 for rel,pin in pins.items():
  need(not os.path.isabs(rel)and'..'not in rel.split('/'),'PIN_SELECTOR');obs=facts.file(source+'/'+rel);need(obs['sha256']==pin,'SOURCE_DRIFT')
 slots={};observations={}
 for name,x in expected['slots'].items():
  o=facts.file(x['path']);need(o['realpath']==x['realpath']and o['sha256']==x['sha256'],'BINARY_DRIFT');observations[name]=o;slots[name]={'path':o['realpath'],'sha256':o['sha256']}
 # Wrapper and actual ELF are separate facts, neither is functional capacity.
 wrapper=facts.file(expected['slots']['chrome']['path'],True);need(b'chrome'in wrapper['data']and b'--no-sandbox'not in wrapper['data'],'CHROME_WRAPPER_CONTRACT')
 elf=facts.file('/opt/google/chrome/chrome',True);need(elf['data'][:4]==b'\x7fELF','CHROME_EFFECTIVE_ELF');observations['chrome_effective']={k:v for k,v in elf.items()if k!='data'}
 sha=env['GITHUB_SHA'];run=env['GITHUB_RUN_ID'];need(re.fullmatch('[0-9a-f]{40}',sha)is not None and re.fullmatch('[0-9]{1,20}',run)is not None,'NATIVE_JOB_TYPED')
 cfg={'schema':'TRACE_UI282_CONFIGURATION_V1','status':'ADOPTED_SEPARATE_NATIVE_ADMISSION_REQUIRED','required_executables':{k:{'path':expected['slots'][k]['path'],'realpath':v['path'],'sha256':v['sha256'],'state':'QUALIFIED','functional_start':'UNPROVED_UNTIL_WORKER_APP'}for k,v in slots.items()},'qualification_scope':'integrity/currentnativebinding only; executable start and browser sandbox still pre-app gates','effective_chrome':observations['chrome_effective']}
 body={'schema':'TRACE295_NATIVE_ADMISSION_V1','repository':'Elinfiny/TraceHarbor','source_commit':sha,'run_id':run,'effect_id':a['effect_id'],'uid':native['uid'],'gid':native['gid'],'manager_authority':'EXISTING_INDEPENDENTLY_ADMITTED_NO_PRIVILEGE_ESCALATION','memory_max':335544320,'swap_max':0,'virtual_as':8589934592,'whole_cap':536870912,'budget_reconciled':True,'sandbox_required':True,'source_accepted':True,'native_hosted_context':True,'parent_netns':native['parent_netns'],'parent_mntns':native['parent_mntns'],'cgroup_parent':'/trace294.slice','source':source,'out':stage+'/out','home':stage+'/out/home','control':stage+'/control','controller':stage+'/controller','gate_path':stage+'/control/release294.json','release_token':digest({'anchor':digest(a),'run':run,'commit':sha,'effect':a['effect_id']}),'binaries':slots,'approved_runtime_config':cfg,'source_pins':pins,'runtime_event':event,'native_anchor_sha256':digest(a),'native_anchor_payload':a,'native_facts':{'identity':native,'binaries':observations},'evidence':a['evidence']}
 derived={'schema':'TRACE298_DERIVED_NATIVE_CONTEXT_V1','original_anchor_sha256':digest(a),'run_id':run,'commit':sha,'source':source,'admission':body};derived['binding_sha256']=digest(derived);return derived
def verify_derived(c,a,env,source):
 b=dict(c);stored=b.pop('binding_sha256',None);need(stored==digest(b),'DERIVED_SELF');need(c.get('original_anchor_sha256')==digest(a),'DERIVED_ORIGINAL_ANCHOR');need(c.get('source')==source and c.get('run_id')==env['GITHUB_RUN_ID']and c.get('commit')==env['GITHUB_SHA'],'STALE_DERIVED_CONTEXT');verify_external(a,c['admission']['source_pins']);return c['admission']
def publish_context(path,obj,gid):
 fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 try:
  data=canonical(obj);need(len(data)<=32768,'CONTEXT32K');os.write(fd,data);os.fsync(fd);os.fchown(fd,0,gid);os.fchmod(fd,0o440)
 finally:os.close(fd)
def require_isolation(plan,obs):
 a=plan['admission'];need(obs.get('uid')==a['uid']and obs.get('gid')==a['gid']and obs.get('cgroup')==plan['cgroup']and re.fullmatch('[0-9a-f]{32}',obs.get('invocation',''))is not None,'UNIT_IDENTITY')
 need(obs.get('memory.max')=='335544320'and obs.get('memory.swap.max')=='0'and obs.get('virtual_as')==a['virtual_as']and obs.get('virtual_as_hard')==a['virtual_as'],'OBSERVED_KERNEL_LIMITS')
 need(obs.get('sandbox')is True and obs.get('private_network')is True and obs.get('mounts_protected')is True,'OBSERVED_ISOLATION_BEFORE_APP');return True

# Opt-in299 transport: entire canonical context remains a separate sealed file.
def project_context(c,raw):
 need(raw==canonical(c) and len(raw)<=32768,'CONTEXT_CANONICAL_SIZE')
 body=json.loads(canonical(c['admission']));body['derived_context_ref']={'name':'derived298.json','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'binding_sha256':c['binding_sha256'],'original_anchor_sha256':c['original_anchor_sha256']}
 return body
def verify_transport(c,raw,admission):
 ref=admission.get('derived_context_ref',{});need(set(ref)=={'name','bytes','sha256','binding_sha256','original_anchor_sha256'} and ref.get('name')=='derived298.json','CONTEXT_REF_SHAPE')
 safeint(ref.get('bytes'),1,32768);need(len(raw)==ref['bytes'] and hashlib.sha256(raw).hexdigest()==ref['sha256'],'CONTEXT_WHOLE_RAW_BINDING')
 a=admission['native_anchor_payload'];verify_derived(c,a,{'GITHUB_RUN_ID':admission['run_id'],'GITHUB_SHA':admission['source_commit']},admission['source'])
 need(project_context(c,raw)==admission,'CONTEXT_ADMISSION_PROJECTION');return c
