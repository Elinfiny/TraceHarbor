"""Reviewed cold bootstrap. No credentials/MAC service. Default missing native
root anchor/proof fails. NONLIVE uses only a pinned explicit fake adapter.
External authenticated Master CAS/Auditor + Owner GitHub commit/event supply
authority; JSON flags or a hash argument alone are not provider authority.
"""
import os,sys,json,hashlib,stat,argparse,importlib.util,resource
PARENT='d502e3b79735ff065b7d9d936c8330ff14bd21a0'
REF='refs/heads/review/traceharbor-v1-browser-qa-base180-162-20261023'
MASTER='libfile_f67b07d0a4288191b60f3469d264f99c'
AUDITOR='libfile_f87a6a307f70819194e0af0fa453afd1'
def need(ok,reason):
 if not ok:raise RuntimeError(reason)
def canonical(obj):return json.dumps(obj,sort_keys=True,separators=(',',':')).encode()
def read_protected(filename,expected=None):
 need(os.path.isabs(filename)and all(p not in ['.','..','']for p in filename[1:].split('/')),'UNSAFE_PATH')
 current=''
 for part in filename[1:].split('/'):
  current+='/'+part;need(not os.path.islink(current),'SYMLINK_PATH')
 fd=os.open(filename,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  s=os.fstat(fd);need(stat.S_ISREG(s.st_mode)and s.st_uid==0 and stat.S_IMODE(s.st_mode)in [0o400,0o440]and s.st_size<=32768,'UNTRUSTED_PUBLISHER_OR_MUTABLE_CONTEXT')
  b=os.read(fd,32769);need(len(b)==s.st_size and len(b)<=32768,'CONTEXT_TRUNCATED')
  if expected:need(hashlib.sha256(b).hexdigest()==expected,'CONTEXT_HASH_DRIFT')
  return json.loads(b),b
 finally:os.close(fd)
def verify_push(event,env,raw_commit,expected_tree):
 need(env.get('GITHUB_ACTIONS')=='true'and env.get('RUNNER_ENVIRONMENT')=='github-hosted','NATIVE_HOSTED_CONTEXT')
 need(env.get('GITHUB_EVENT_NAME')=='push'and env.get('GITHUB_RUN_ATTEMPT')=='1','ACTUAL_PUSH_ATTEMPT1')
 need(env.get('GITHUB_REPOSITORY')=='Elinfiny/TraceHarbor'and env.get('GITHUB_ACTOR_ID')=='273768139','ACTUAL_REPO_ACTOR')
 after=env.get('GITHUB_SHA','');need(len(after)==40 and env.get('TRACE295_WORKFLOW_SHA')==after,'WORKFLOW_SOURCE_BINDING')
 need(event.get('ref')==env.get('GITHUB_REF')==REF and event.get('before')==PARENT and event.get('after')==after and all(event.get(k)is False for k in ['created','deleted','forced']),'PUSH_REF_PARENT_REPLAY_GUARD')
 need(event.get('repository',{}).get('id')==1391430317 and event.get('repository',{}).get('private')is False and event.get('sender',{}).get('id')==273768139,'NATIVE_EVENT_IDENTITY')
 need(hashlib.sha1(b'commit '+str(len(raw_commit)).encode()+b'\0'+raw_commit).hexdigest()==after,'NATIVE_GIT_OBJECT_SHA')
 header,message=raw_commit.split(b'\n\n',1);parents=[x[7:].decode()for x in header.splitlines()if x.startswith(b'parent ')];trees=[x[5:].decode()for x in header.splitlines()if x.startswith(b'tree ')]
 need(parents==[PARENT]and trees==[expected_tree],'SOLE_PARENT_OR_TREE');envelope=json.loads(message)
 need(envelope.get('schema')=='TRACE295_NATIVE_PUBLICATION_V1','PUBLICATION_RECEIPT_SCHEMA')
 return envelope
def load_module(path,pin,name):
 b=open(path,'rb').read();need(hashlib.sha256(b).hexdigest()==pin,'SOURCE_PIN_BEFORE_IMPORT');spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def verify_anchor(filename,expected,source):
 a,raw=read_protected(filename,expected);need(a.get('schema')=='TRACE298_PREPUBLICATION_V1','ANCHOR_SCHEMA298');need(a.get('source')in[source,'__NATIVE_CHECKOUT__'],'SOURCE_PARENT_ANCHOR')
 pins=a.get('source_pins',{})
 for rel,pin in pins.items():
  need(not os.path.isabs(rel)and'..'not in rel.split('/'),'UNSAFE_SOURCE_SELECTOR');p=source+'/'+rel;need(os.path.realpath(p)==p,'SOURCE_REDIRECT');need(hashlib.sha256(open(p,'rb').read()).hexdigest()==pin,'CHANGED_SOURCE_PIN')
 native=load_module(source+'/tools/ui280/native298.py',pins['tools/ui280/native298.py'],'native298');native.verify_external(a,pins);return a,raw,native
def prepare_context(args):
 source=os.path.realpath(os.path.join(os.path.dirname(__file__),'../..'));a,raw,native=verify_anchor(args.anchor,args.anchor_sha,source)
 if args.gated_worker:
  plan,praw=read_protected(args.plan);need(plan.get('binding')==args.binding and plan['admission']['native_anchor_sha256']==args.anchor_sha,'WORKER_ROOT_PLAN_BINDING');env={'GITHUB_SHA':plan['admission']['source_commit'],'GITHUB_RUN_ID':plan['admission']['run_id']}
 else:
  proof,praw=read_protected(args.commit_proof);env=dict(os.environ);publication=verify_push(proof['event'],env,proof['raw_commit_utf8'].encode(),a['tree']);need(publication.get('anchor_sha256')==args.anchor_sha and publication.get('master')==a['evidence']['master']and publication.get('auditor')==a['evidence']['auditor_current'],'GIT_NATIVE_PUBLICATION_ADMISSION_BINDING')
 c,craw=read_protected(args.derived);native.verify_derived(c,a,env,source);body=native.project_context(c,craw)
 expected=body['control']+('/derived298.json' if args.gated_worker else '/native-context298.json');need(args.derived==expected,'CONTEXT_NATIVE_LOCATION')
 if args.gated_worker:need(body==plan['admission'],'WORKER_CONTEXT_PLAN_PROJECTION')
 return a,body
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument('--controller',action='store_true');p.add_argument('--gated-worker',action='store_true');p.add_argument('--anchor',required=True);p.add_argument('--anchor-sha',required=True);p.add_argument('--commit-proof');p.add_argument('--plan');p.add_argument('--binding');p.add_argument('--derived',required=True);p.add_argument('--fixture-adapter');args=p.parse_args(argv)
 need(args.controller != args.gated_worker,'EXACT_ONE_ROLE');need(args.gated_worker or args.commit_proof,'NATIVE_COMMIT_PROOF_REQUIRED')
 if args.controller:resource.setrlimit(resource.RLIMIT_AS,(67108864,100663296))
 a,body=prepare_context(args);source=body['source'];corepath=source+'/tools/ui280/owned_supervisor295.py';core=load_module(corepath,a['source_pins']['tools/ui280/owned_supervisor295.py'],'controlled295')
 need(not args.fixture_adapter,'FAKE_ADAPTER_FORBIDDEN_NATIVE');need(os.geteuid()==0 if args.controller else os.geteuid()==body['uid'],'ACTUAL_CONTROLLER_WORKER_UID')
 if args.controller:
  verified=core.VerifiedAdmission(body,{'external_root_anchor_sha256':args.anchor_sha,'evidence':a['evidence']},core._ISSUER);result=core.dormant_pipeline(verified);print(json.dumps(result));return 0 if result['phase']=='TERMINAL'and result['process']['functional_exit']=='PASS'else 1
 return core.worker_entry(args.plan,args.binding)
if __name__=='__main__':
 try:raise SystemExit(main())
 except Exception as e:print(json.dumps({'state':'REFUSED_OR_UNKNOWN','error':type(e).__name__+':'+str(e),'real_adapters_entered':False}));raise SystemExit(3)
