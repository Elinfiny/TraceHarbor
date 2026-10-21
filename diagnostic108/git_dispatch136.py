"""PRIVATE H136_GIT_CREATE_DISPATCH prospective DATA validators.
No import dispatches, mints authority, reads tokens, or creates native handles.
Owner actor273768139 remains mandatory; actual connector event identity UNKNOWN.
"""
import re,json,math,os,pathlib,hashlib,importlib.util
_ts146=importlib.util.spec_from_file_location("trace146_git_timing",pathlib.Path(__file__).with_name("timing146.py"));t146=importlib.util.module_from_spec(_ts146);_ts146.loader.exec_module(t146)
REPO='Elinfiny/TraceHarbor';OWNER=273768139;RID=1391430317
PREFIX='traceharbor/once136/v1/'
WORKFLOW='.github/workflows/traceharbor-counter136.yml'
RX=re.compile(r'traceharbor/once136/v1/([a-f0-9]{40})-([a-f0-9]{64})-([a-f0-9]{64})-([1-9][0-9]{0,11})-([1-9][0-9]{0,11})')
def parse136(branch):
 if type(branch) is not str:raise TypeError('Exact branch text')
 m=RX.fullmatch(branch)
 if m is None:raise ValueError('Only versioned protected launch namespace')
 source,manifest,once,expires,cutoff=m.groups()
 if int(cutoff)<int(expires):raise ValueError('Original expiry no reset')
 return {'source_sha':source,'manifest_sha256':manifest,'once_receipt_sha256':once,'once_expires_utc':expires,'coordinator_cutoff_utc':cutoff}
def branch136(values):
 if type(values) is not dict or set(values)!={'source_sha','manifest_sha256','once_receipt_sha256','once_expires_utc','coordinator_cutoff_utc'}:raise ValueError('Closed five nonsecret source runtime values')
 b=PREFIX+'-'.join(str(values[k]) for k in ('source_sha','manifest_sha256','once_receipt_sha256','once_expires_utc','coordinator_cutoff_utc'))
 if parse136(b)!={k:str(v) for k,v in values.items()} or len(b.split('/')[-1])>255:raise ValueError('Canonical complete ref encoding')
 return b
def args136(values):
 return {'repository_full_name':REPO,'branch_name':branch136(values),'sha':values['source_sha']}
def binding136(args):
 if type(args) is not dict or set(args)!={'repository_full_name','branch_name','sha'} or args['repository_full_name']!=REPO:raise ValueError('Exact supported create_branch-only arguments')
 v=parse136(args['branch_name'])
 if args['sha']!=v['source_sha']:raise ValueError('Exact immutable source ref')
 return dict(v,branch=args['branch_name'],workflow_path=WORKFLOW,expected_actor_id=OWNER,repository_id=RID,event='create')
def absent_original136(original):
 if type(original) is not dict or original.get('isError') is not True:raise ValueError('Actual missing original required; existing ref cannot be adopted')
 v=original.get('structuredContent',{})
 if v.get('error_code')!='NOT_FOUND' or str(v.get('error_data',{}).get('status'))!='404':raise ValueError('Only authentic current404 absence, not access refusal')
 return {'absent':True}
def created136(value,args):
 binding136(args)
 if type(value) is not dict or value!={'branch':args['branch_name']}:raise ValueError('Actual connector returns branch-only; no fabricated SHA/run')
 return value
def ref136(value,args):
 binding136(args)
 if type(value) is not dict or value.get('ref')!='refs/heads/'+args['branch_name'] or value.get('object',{}).get('type')!='commit' or value['object'].get('sha')!=args['sha']:raise ValueError('Authenticated exact created-ref immutable SHA')
 return value
def run136(run,binding,status=None):
 if type(run) is not dict or type(run.get('id')) is not int or run['id']<=0 or run.get('run_attempt')!=1 or run.get('head_sha')!=binding['source_sha'] or run.get('head_branch')!=binding['branch'] or run.get('event')!='create' or run.get('path')!=WORKFLOW or run.get('actor',{}).get('id')!=OWNER or run.get('repository',{}).get('id')!=RID:raise ValueError('Exact create run/ref/source/workflow/Owner/attempt')
 if 'triggering_actor' in run and run['triggering_actor'].get('id')!=OWNER:raise ValueError('No alternate triggering actor')
 if status is not None and run.get('status')!=status:raise ValueError('Actual expected run state')
 return run
def selected136(listed,binding):
 if type(listed) is not dict or type(listed.get('workflow_runs')) is not list or type(listed.get('total_count')) is not int or listed['total_count']!=len(listed['workflow_runs']) or listed['total_count']>100:raise ValueError('Whole bounded filtered run list, no partial pagination/latest guess')
 rows=[r for r in listed['workflow_runs'] if r.get('head_branch')==binding['branch'] and r.get('path')==WORKFLOW]
 if len(rows)>1:raise ValueError('Ambiguous duplicate run; no retry/adoption')
 if not rows:return None
 r=run136(rows[0],binding)
 if r.get('status') in ('queued','waiting','pending','requested'):return None
 if r.get('status')!='in_progress':raise ValueError('Already terminal or unsupported run cannot supply fresh same-invocation authority')
 return r
def event136(env):
 e=env.get('GITHUB_EVENT_NAME')
 if e=='workflow_dispatch':return e
 if e!='create' or env.get('GITHUB_REPOSITORY')!=REPO or env.get('GITHUB_REPOSITORY_ID')!=str(RID) or env.get('GITHUB_ACTOR_ID')!=str(OWNER) or env.get('GITHUB_RUN_ATTEMPT')!='1' or env.get('GITHUB_REF_TYPE')!='branch' or env.get('GITHUB_WORKFLOW_REF','').split('@')[0]!=REPO+'/'+WORKFLOW:raise PermissionError('Separate exact source create event contract, never relaxed Owner')
 ref=env.get('GITHUB_REF','')
 if not ref.startswith('refs/heads/'):raise ValueError('Branch only')
 v=parse136(ref[11:])
 if env.get('GITHUB_SHA')!=v['source_sha'] or env.get('GITHUB_WORKFLOW_SHA')!=v['source_sha']:raise ValueError('Exact workflow+source original SHA')
 return e
def env_values136(env,wall=None):
 if event136(env)!='create':raise ValueError('Create route only')
 v=parse136(env['GITHUB_REF'][11:])
 if any(env.get('TRACE135_'+k.upper())!=val for k,val in v.items()):raise ValueError('No caller edited or stale decoded runtime inputs')
 if wall is not None and (type(wall) not in (int,float) or not math.isfinite(wall) or not wall<int(v['once_expires_utc'])<=wall+t146.PARENT):raise ValueError('Source original expiry never renewed')
 return v
def run_event136(run,binding=None):
 if run.get('event')=='workflow_dispatch':
  if binding is not None:raise ValueError('Manual event cannot satisfy create source contract')
  return True
 if binding is None:raise ValueError('Create run requires exact source-owned binding, no event-only widening')
 run136(run,binding);return True
def guard136():
 import time
 v=env_values136(dict(os.environ),time.time());root=pathlib.Path(__file__).resolve().parent.parent
 raw=(root/'diagnostic108/manifest.json').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=v['manifest_sha256']:raise ValueError('Whole exact manifest')
 for name,p in json.loads(raw)['source_files'].items():
  q=pathlib.PurePosixPath(name)
  if q.is_absolute() or '..' in q.parts:raise ValueError('Safe exact source member')
  b=(root/name).read_bytes()
  if len(b)!=p['bytes'] or hashlib.sha256(b).hexdigest()!=p['sha256']:raise ValueError('Full source closure before protected init')
 print(json.dumps({'source_guard136':'PASS','native_authority':False}))
def decode_env136():
 import sys
 env=dict(os.environ);event136(env);v=parse136(env['GITHUB_REF'][11:])
 # Closed known digest/integer values only, no caller strings or shell expansion.
 target=pathlib.Path(env['GITHUB_ENV'])
 with target.open('a',encoding='utf-8') as f:
  for k,val in v.items():f.write('TRACE135_'+k.upper()+'='+val+'\n')
 print(json.dumps({'decoded_nonsecret_source_inputs':5,'native_authority':False}))
if __name__=='__main__':
 import sys
 if sys.argv[1:]==['decode-env136']:decode_env136()
 elif not sys.argv[1:]:guard136()
 else:raise ValueError('Fixed136 source command only')

