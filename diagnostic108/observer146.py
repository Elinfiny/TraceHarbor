"""Durable OBSERVER-owned accounting only. Never constructs a native capability.
Source controller issues a plan before holder start; outer cells reserve/retain
via O_EXCL anchored records. No cross-isolate WeakMap/store mutation is used.
"""
import json,pathlib,os,stat,hashlib,re,sys
can=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
sha=lambda b:hashlib.sha256(b).hexdigest()
def put(p,x):
 fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'wb') as f:f.write(can(x));f.flush();os.fsync(f.fileno())
def owned(p,directory=False):
 s=p.lstat()
 if p.resolve()!=p or p.is_symlink() or s.st_uid!=os.getuid() or s.st_mode&(0o077 if directory else 0o022) or not (stat.S_ISDIR(s.st_mode) if directory else stat.S_ISREG(s.st_mode) and s.st_nlink==1):raise ValueError('Exact owned observer custody')
 return s
def read(p):
 before=owned(p);fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  raw=os.read(fd,1048577);extra=os.read(fd,1);after=os.fstat(fd)
 finally:os.close(fd)
 if extra or len(raw)>1048576 or len(raw)!=before.st_size or (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns):raise ValueError('Whole stable observer original')
 return json.loads(raw),raw,before
def issue(root,binding,inventory):
 root=pathlib.Path(root);s=owned(root,True)
 if set(binding)!={'source_sha','manifest_sha256','static_config_sha256','inventory_sha256','direction_id','realm'} or binding['realm'] not in ('SOURCE_ISSUED_CONTROL_DATA','HOST_ONLY_CANARY') or inventory['observer_maximum']!=40 or inventory['authority'] is not False:raise ValueError('Source-issued observer DATA plan')
 for k in ('source_sha','manifest_sha256','static_config_sha256','inventory_sha256'):
  if not re.fullmatch('[a-f0-9]{'+('40' if k=='source_sha' else '64')+'}',binding[k]):raise ValueError('Closed observer source pin')
 ids=[r['id'] for r in inventory['rows'] if r['owner']=='OBSERVER']
 expected=[f'observer/{i}'+suffix for i in range(40) for suffix in ('','/original','/intent','/claim-cell','/original-cell')]
 if ids!=expected:raise ValueError('Exact source precommitted disjoint observer80 tickets')
 plan={'schema':'TRACE146_DURABLE_OBSERVER_V1','binding':binding,'root':str(root),'root_dev':s.st_dev,'root_ino':s.st_ino,'tickets':ids,'maximum':40,'native_authority':False};put(root/'observer146-plan.json',plan)
 return {'plan_sha256':sha(can(plan)),'root':str(root),'native_authority':False}
def plan146(root,pin):
 root=pathlib.Path(root);s=owned(root,True);p,raw,ps=read(root/'observer146-plan.json')
 if sha(raw)!=pin or p['root']!=str(root) or (p['root_dev'],p['root_ino'])!=(s.st_dev,s.st_ino) or p['native_authority'] is not False:raise ValueError('No cloned plan/custody/authority')
 return root,p
def reserve(root,pin,cell,yield_original):
 root,p=plan146(root,pin)
 if type(cell) is not str or not re.fullmatch('[A-Za-z0-9_-]{1,80}',cell) or type(yield_original) is not str or ('Script running with cell ID '+cell) not in yield_original:raise ValueError('Actual yielded functions.exec cell original before wait')
 bound=root/'observer146-cell.json'
 if bound.exists():
  if read(bound)[0]['cell_id']!=cell:raise ValueError('No replacement cell/restart')
 else:put(bound,{'cell_id':cell,'yield_original':yield_original,'plan_sha256':pin})
 index=0
 while (root/f'observer146-{index}.intent.json').exists():
  if not (root/f'observer146-{index}.original.json').exists():raise ValueError('Previous actual wait unresolved; no second reservation')
  index+=1
 if index>=40:raise ValueError('Finite40 observer tickets exhausted')
 runtime=root/'observer146-runtime.json';runtime=read(runtime)[0] if runtime.exists() else {'scope':'BEFORE_FIRST_EFFECT_FRAME','once_receipt_sha256':None,'run_id':None}
 if runtime['once_receipt_sha256'] is not None:
  if runtime.get('source_sha')!=p['binding']['source_sha'] or runtime.get('manifest_sha256')!=p['binding']['manifest_sha256'] or not re.fullmatch('[a-f0-9]{64}',runtime['once_receipt_sha256']):raise ValueError('Actual source-issued runtime once/source/manifest')
  run=root/'observer146-run.json'
  if run.exists():
   r=read(run)[0]
   if r['once_receipt_sha256']!=runtime['once_receipt_sha256'] or r['source_sha']!=runtime['source_sha'] or r['branch']!=runtime['dispatch_args']['branch_name']:raise ValueError('Same source-selected run/ref/once')
   runtime=dict(runtime,run_id=r['run_id'])
 ticket={'schema':'TRACE146_WAIT_RESERVED','index':index,'cell_id':cell,'plan_sha256':pin,'source_binding':p['binding'],'runtime_binding':runtime,'ticket_ids':[f'observer/{index}'+s for s in ('/claim-cell','/intent','')],'native_authority':False}
 put(root/f'observer146-{index}.intent.json',ticket);return {'ticket':ticket,'args':{'cell_id':cell,'yield_time_ms':60000,'max_tokens':4000}}
def retain(root,pin,ticket,original):
 root,p=plan146(root,pin);index=ticket['index']
 if type(index) is not int or not 0<=index<40 or not (root/f'observer146-{index}.intent.json').exists():raise ValueError('Unreserved wait cannot mint a receipt')
 wanted=read(root/f'observer146-{index}.intent.json')[0]
 if wanted!=ticket or type(original) not in (str,dict) or ticket['native_authority'] is not False:raise ValueError('Exact reserved ticket and whole actual wait original')
 result={'identity':ticket,'original':original,'ticket_ids':[f'observer/{index}/original-cell',f'observer/{index}/original'],'native_authority':False};put(root/f'observer146-{index}.original.json',result);return result
def verify(root,pin):
 root,p=plan146(root,pin);rows=[];used=[]
 for i in range(40):
  ip=root/f'observer146-{i}.intent.json';op=root/f'observer146-{i}.original.json'
  if not ip.exists():
   if op.exists():raise ValueError('Unreserved wait receipt')
   continue
  t=read(ip)[0]
  if not op.exists():raise ValueError('Reserved wait original not retained')
  r=read(op)[0]
  if r['identity']!=t:raise ValueError('Wait identity mismatch')
  rows.append(r);used+=t['ticket_ids']+r['ticket_ids']
 if len(used)!=len(set(used)):raise ValueError('No observer ticket replay')
 terminal=root/'controller-final146.original.json';terminal=read(terminal)[0] if terminal.exists() else None
 if terminal is not None and (terminal['plan_sha256']!=pin or set(terminal['controller_used_ticket_ids'])&set(p['tickets'])):raise ValueError('Source controller/observer ownership overlap or changed plan')
 return {'schema':'TRACE146_OBSERVER_ACCOUNTING','scope':'OBSERVER_ACCOUNTING_ONLY_NOT_FULL_NATIVE_G','plan_sha256':pin,'used_ticket_ids':used,'reserved_capacity':200,'waits':len(rows),'rows':rows,'source_controller_terminal':terminal,'native_authority':False}
def main():
 q=json.loads(sys.argv[2]);op=sys.argv[1]
 if op=='issue':r=issue(q['root'],q['binding'],q['inventory'])
 elif op=='reserve':r=reserve(q['root'],q['plan_sha256'],q['cell_id'],q['yield_original'])
 elif op=='retain':r=retain(q['root'],q['plan_sha256'],q['ticket'],q['original'])
 elif op=='verify':r=verify(q['root'],q['plan_sha256'])
 else:raise ValueError('Closed observer metadata verbs')
 print(can(r).decode())
if __name__=='__main__':main()
