"""Exact helper, one in-process invocation, complete private original before guards.

No native capability or success can be obtained from this evidence runner.
The reviewed helper uses Python streams. No subprocess or helper patching.
"""
import hashlib,io,json,os,pathlib,runpy,stat,sys,time,traceback
STREAM_LIMIT128=1048576
HELPER_SECONDS128=10
def can128(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha128(b):return hashlib.sha256(b).hexdigest()
def exception128(exc):return {'class':type(exc).__name__,'message':str(exc),'traceback':''.join(traceback.format_exception(exc))}
def restore128(saved):
 errors=[]
 for name,value in saved.items():
  try:setattr(sys,name,value)
  except BaseException as exc:errors.append({'stream':name,'exception':exception128(exc)})
 return errors
def retain_private128(root,identity,original):
 root=pathlib.Path(root);s=root.lstat()
 if not stat.S_ISDIR(s.st_mode) or root.is_symlink() or s.st_uid!=os.getuid() or stat.S_IMODE(s.st_mode)!=0o700:raise PermissionError('Owned exact private evidence directory')
 raw=can128({'identity':identity,'original':original});path=root/(sha128(can128(identity))+'.helper-original.json')
 fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 try:
  with os.fdopen(fd,'wb') as out:
   if out.write(raw)!=len(raw):raise OSError('Incomplete original write')
 except BaseException:raise
 if path.read_bytes()!=raw:raise OSError('Complete helper original readback')
 return {'path':str(path),'bytes':len(raw),'sha256':sha128(raw)}
def run_helper128(helper,expected_sha256,path,library_id,xattrs,identity,retain):
 helper=pathlib.Path(helper)
 if sha128(helper.read_bytes())!=expected_sha256 or set(identity)!={'phase','run','source','call'} or not all(isinstance(v,str) and v for v in identity.values()):raise ValueError('Exact source/phase/run/call before helper execution')
 saved={name:getattr(sys,name) for name in ('argv','stdin','stdout','stderr')};out=io.StringIO();err=io.StringIO();started=time.monotonic();primary=None;code=None;native_return=None;restoration=[]
 try:
  sys.argv=[str(helper),'apply-xattrs',str(path),library_id];sys.stdin=io.StringIO(json.dumps(xattrs));sys.stdout=out;sys.stderr=err
  try:
   returned=runpy.run_path(str(helper),run_name='__main__');native_return={'kind':'runpy_globals','keys':sorted(returned)};code=0
  except SystemExit as exc:
   code=0 if exc.code is None else exc.code;native_return={'kind':'SystemExit','code':exc.code if isinstance(exc.code,(str,int,type(None))) else repr(exc.code)}
   if code!=0:primary=exception128(exc)
  except BaseException as exc:primary=exception128(exc)
 finally:
  # Each original binding has exactly one restoration attempt; no retries.
  restoration=restore128(saved)
 original={'identity':identity,'helper_sha256':expected_sha256,'stdout':out.getvalue(),'stderr':err.getvalue(),'native_return':native_return,'returncode':code,'exception':primary,'restoration_errors':restoration,'elapsed_s':time.monotonic()-started,'attempts':1,'restoration_attempts':list(saved)}
 reference=retain(identity,original)  # BEFORE every success/output/time guard.
 if primary or restoration or code!=0 or original['elapsed_s']>HELPER_SECONDS128 or len(original['stdout'].encode())+len(original['stderr'].encode())>STREAM_LIMIT128:raise RuntimeError('UNKNOWN helper: complete original retained; no retry or next effect')
 return reference
