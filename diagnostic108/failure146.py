"""Bound early-failure evidence, anchored absence and distinct public failure DATA."""
import json,os,pathlib,stat,re,hashlib,traceback,time
can=lambda d:json.dumps(d,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
SCHEMA='TRACE146_FAILURE_ONLY_V1'
CLASSES={'TimeoutError','ValueError','TypeError','PermissionError','FileNotFoundError','RuntimeError','OSError','Exception','CLEANUP_UNKNOWN'}
def binding146(env):
 if env.get('GITHUB_REPOSITORY')!='Elinfiny/TraceHarbor' or env.get('GITHUB_REPOSITORY_ID')!='1391430317' or env.get('GITHUB_ACTOR_ID')!='273768139' or env.get('GITHUB_RUN_ATTEMPT')!='1':raise ValueError('Exact failure run/Owner/repository')
 b={k:env['TRACE135_'+k.upper()] for k in ('source_sha','manifest_sha256','once_receipt_sha256')}
 for k,v in b.items():
  if not re.fullmatch('[a-f0-9]{'+('40' if k=='source_sha' else '64')+'}',v):raise ValueError('Failure context digest')
 if env.get('GITHUB_SHA')!=b['source_sha'] or env.get('GITHUB_WORKFLOW_SHA')!=b['source_sha'] or not re.fullmatch('[1-9][0-9]*',env.get('GITHUB_RUN_ID','')):raise ValueError('Same source/workflow/run')
 b.update(run_id=int(env['GITHUB_RUN_ID']),attempt=1,actor_id=273768139,repository_id=1391430317)
 return b
def anchored_temp146(path):
 p=pathlib.Path(path)
 if not p.is_absolute() or p.resolve()!=p or '..' in p.parts:raise ValueError('Trusted absolute unaliased temp')
 fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY);opened=[fd]
 try:
  for part in p.parts[1:]:
   fd=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);opened.append(fd)
  s=os.fstat(fd);v=p.lstat()
  if s.st_uid!=os.getuid() or s.st_mode&0o022 or (s.st_dev,s.st_ino)!=(v.st_dev,v.st_ino):raise ValueError('Trusted temp ownership/mode/anchor')
  return os.dup(fd),(s.st_dev,s.st_ino)
 finally:
  for f in reversed(opened):os.close(f)
def absence146(temp,once):
 if not re.fullmatch('[a-f0-9]{64}',once):raise ValueError('Exact nonce digest locator')
 try:fd,anchor=anchored_temp146(temp)
 except Exception:return {'status':'UNKNOWN','unknown':True,'remove_attempts':0,'native_safe':False}
 try:
  try:s=os.stat('traceharbor-counter117-intake-'+once,dir_fd=fd,follow_symlinks=False)
  except FileNotFoundError:
   a=os.fstat(fd);b=pathlib.Path(temp).lstat()
   if (a.st_dev,a.st_ino)!=(b.st_dev,b.st_ino) or anchor!=(a.st_dev,a.st_ino):raise ValueError('Temp drift during absence observation')
   return {'status':'OBSERVED_NO_INTAKE','unknown':False,'remove_attempts':0,'scope':'FAILURE_ONLY_ANCHORED_ABSENCE','native_safe':False}
  return {'status':'PRESENT_REQUIRES_ORIGINAL_OWNED_CLEANUP','unknown':True,'remove_attempts':0,'scope':'NO_ADOPTION','native_safe':False}
 except Exception:
  return {'status':'UNKNOWN','unknown':True,'remove_attempts':0,'native_safe':False}
 finally:os.close(fd)
def write_once146(path,raw):
 fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
def checked_dir146(temp,name):
 fd,anchor=anchored_temp146(temp)
 try:
  try:os.mkdir(name,mode=0o700,dir_fd=fd)
  except FileExistsError:pass
  sub=os.open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd)
  try:
   s=os.fstat(sub)
   if s.st_uid!=os.getuid() or s.st_mode&0o077:raise ValueError('Private146 evidence directory')
  finally:os.close(sub)
 finally:os.close(fd)
 return pathlib.Path(temp)/name
def retain_exception146(env,exc):
 b=binding146(env);root=checked_dir146(env['RUNNER_TEMP'],'traceharbor-failure146-private');record={'schema':'TRACE146_ORIGINAL_EARLY_EXCEPTION','context':b,'exception_class':type(exc).__name__,'args_repr':repr(exc.args),'traceback':''.join(traceback.format_exception(type(exc),exc,exc.__traceback__)),'utc':time.time(),'retry':False}
 write_once146(root/'exception.json',can(record));return record
def failure146(context,error_class,cleanup):
 if error_class not in CLASSES:error_class='Exception'
 status=cleanup.get('status','UNKNOWN')
 if status not in ('OBSERVED_NO_INTAKE','PASS'):status='UNKNOWN'
 return {'schema':SCHEMA,'scope':'FAILURE_ONLY_NOT_SAFE','context':context,'failure_class':error_class,'cleanup_status':status,'unknown':status=='UNKNOWN','retry':False,'counter_verified':False,'numeric_count':None,'model_calls':0}
def validate_failure146(raw,context):
 if type(raw) is not bytes or not 0<len(raw)<=8192:raise ValueError('Finite failure-only body')
 d=json.loads(raw);keys={'schema','scope','context','failure_class','cleanup_status','unknown','retry','counter_verified','numeric_count','model_calls'}
 if set(d)!=keys or d['schema']!=SCHEMA or d['scope']!='FAILURE_ONLY_NOT_SAFE' or d['context']!=context or d['failure_class'] not in CLASSES or d['cleanup_status'] not in ('OBSERVED_NO_INTAKE','PASS','UNKNOWN') or d['unknown'] is not (d['cleanup_status']=='UNKNOWN') or d['retry'] is not False or d['counter_verified'] is not False or d['numeric_count'] is not None or type(d['model_calls']) is not int or d['model_calls']!=0:raise ValueError('Closed failure-only allowlist; never SAFE/numeric')
 return d
def finish_cleanup146(env,result):
 b=binding146(env);root=checked_dir146(env['RUNNER_TEMP'],'traceharbor-failure146-private');write_once146(root/'cleanup.json',can({'context':b,'cleanup':result}))
 original=root/'exception.json'
 if original.exists() or result.get('unknown'):
  s=original.lstat() if original.exists() else None
  if s is not None and (not stat.S_ISREG(s.st_mode) or s.st_nlink!=1 or s.st_uid!=os.getuid() or s.st_mode&0o077):raise ValueError('Exact original exception custody')
  e=json.loads(original.read_bytes()) if s is not None else {'context':b,'exception_class':'CLEANUP_UNKNOWN'}
  if e['context']!=b:raise ValueError('Original failure binding drift')
  public=failure146(b,e['exception_class'],result);target=checked_dir146(env['RUNNER_TEMP'],'traceharbor-failure146');write_once146(target/'failure.json',can(public));return public
 return None
