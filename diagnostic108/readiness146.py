"""Finite readonly availability hint. Never a consumed/native/SAFE capability."""
import pathlib,importlib.util,json,os,re,time,sys
ROOT=pathlib.Path(__file__).resolve().parent
def load(name,file):
 s=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def wait_ref146(api,clock,once,save,pause=time.sleep):
 end=min(clock.mono()+600,clock.end_mono-840);start=clock.mono()
 if end<=start:raise TimeoutError('Readiness plus main/cleanup/upload suffix')
 path='/repos/Elinfiny/TraceHarbor/git/ref/heads/traceharbor-counter116-consumed-'+once
 for index in range(40):
  if index:
   target=start+index*15
   if target>=end:break
   pause(max(0,target-clock.mono()))
  clock.check(end);deadline=min(end,clock.mono()+15)
  try:value=api(path,deadline=deadline,missing=True)
  except BaseException as exc:save({'index':index,'exception_class':type(exc).__name__,'status':'UNKNOWN_NO_RETRY'});raise
  save({'index':index,'original':value,'utc':clock.wall(),'mono':clock.mono(),'native_authority':False});clock.check(deadline)
  if value is None:continue
  if value.get('ref')!='refs/heads/traceharbor-counter116-consumed-'+once or value.get('object',{}).get('type')!='commit' or not re.fullmatch('[a-f0-9]{40}',value['object'].get('sha','')):raise ValueError('Exact finite consumed-ref availability hint')
  return {'schema':'TRACE146_READINESS_HINT_ONLY','native_authority':False,'typed_consumed_proof':False}
 raise TimeoutError('Finite public readiness observations exhausted')
def main():
 env=dict(os.environ);git=load('readiness146_git',ROOT/'git_dispatch136.py');v=git.env_values136(env,time.time());failure=load('readiness146_failure',ROOT/'failure146.py');failure.binding146(env)
 g=load('readiness146_admission',ROOT/'admission116.py');ingress=load('readiness146_ingress',ROOT.parent/'offline103/ingress.py');rid=env['GITHUB_RUN_ID'];run=ingress.api('/repos/Elinfiny/TraceHarbor/actions/runs/'+rid,deadline=time.monotonic()+10);git.run136(run,git.binding136(git.args136(v)),status='in_progress');clock=g.ParentClock.from_run(run,int(v['once_expires_utc']),int(v['coordinator_cutoff_utc']))
 root=failure.checked_dir146(env['RUNNER_TEMP'],'traceharbor-readiness146')
 def save(d):failure.write_once146(root/(str(d['index'])+'.json'),failure.can(d))
 r=wait_ref146(ingress.api,clock,v['once_receipt_sha256'],save);print(json.dumps(r))
if __name__=='__main__':main()
