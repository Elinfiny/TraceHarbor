"""SOURCE175 pure physical/entry qualification. No provider or native factory.
Run against explicit local neutral inputs only; every first result is retained.
"""
from pathlib import Path
import json,os,stat,sys,tempfile,runpy,traceback,time,types,hashlib,copy,unittest.mock
ROOT=Path(__file__).resolve().parent
def qualify175(own,cfg,out):
 S=runpy.run_path(str(ROOT/'snapshot174.py'));H=runpy.run_path(str(ROOT/'prestart174.py'));Whole=S['Whole173'];rows=[]
 def check(name,fn):
  t=time.monotonic()
  try:fn();r={'case':name,'status':'PASS','wall_s':time.monotonic()-t}
  except BaseException as e:r={'case':name,'status':'FAIL','exception':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()}
  rows.append(r);Path(out).write_text(json.dumps({'status':'RUNNING','rows':rows,'native_effects':0}));print(name,r['status'],flush=True)
 def refuses(fn):
  try:r=fn()
  except (ValueError,PermissionError,OSError,TypeError,KeyError):return
  if isinstance(r,Whole):r.close173()
  raise AssertionError('Required refusal absent')
 with tempfile.TemporaryDirectory(prefix='SOURCE175_DATA_ONLY_NO_NATIVE_')as td:
  root=Path(td);root.chmod(0o700);serial=[0]
  def fresh():
   serial[0]+=1;p=root/str(serial[0]);p.mkdir(mode=0o700);q=p/'leaf.json';q.write_bytes(b'{"value":"AAAA"}');q.chmod(0o600);os.setxattr(q,'user.neutral175',b'initial');return p,q
  def mutation(fn):
   p,q=fresh();s=Whole(q,33554432)
   try:fn(p,q,s);refuses(s.reseal173)
   finally:s.close173()
  check('F2_parent_mode_change_0700_to0777_refused',lambda:mutation(lambda p,q,s:p.chmod(0o777)))
  check('F2_parent_group_write_refused',lambda:mutation(lambda p,q,s:p.chmod(0o720)))
  check('F2_parent_attrs_added_refused',lambda:mutation(lambda p,q,s:os.setxattr(p,'user.F2',b'new')))
  def attrs_change(remove=False):
   p,q=fresh();os.setxattr(p,'user.F2',b'initial');s=Whole(q,33554432)
   try:
    if remove:os.removexattr(p,'user.F2')
    else:os.setxattr(p,'user.F2',b'changed')
    refuses(s.reseal173)
   finally:s.close173()
  check('F2_parent_attrs_changed_refused',attrs_change);check('F2_parent_attrs_removed_refused',lambda:attrs_change(True))
  def rename(p,q,s):p.rename(p.with_name(p.name+'_retained'));p.mkdir(mode=0o700);(p/q.name).write_bytes(s.raw);(p/q.name).chmod(0o600)
  check('F2_ancestor_rename_samebytes_replacement_refused',lambda:mutation(rename))
  def alias(p,q,s):p.rename(p.with_name(p.name+'_retained'));p.symlink_to(p.with_name(p.name+'_retained'),target_is_directory=True)
  check('F2_ancestor_symlink_alias_refused',lambda:mutation(alias))
  def sibling():
   p,q=fresh();s=Whole(q,33554432)
   try:(p/'unrelated').write_text('unrelated IO');s.reseal173()
   finally:s.close173()
  check('shared_ancestor_unrelated_child_mtime_changes_allowed',sibling)
  def unsafe():p,q=fresh();p.chmod(0o777);refuses(lambda:Whole(q,33554432))
  check('preexisting_unsafe_private_ancestor_refused',unsafe)
  check('leaf_groupwrite_refused',lambda:mutation(lambda p,q,s:q.chmod(0o660)))
  check('leaf_same_length_write_refused',lambda:mutation(lambda p,q,s:q.write_bytes(b'{"value":"BBBB"}')))
  check('leaf_growth_EOF_refused',lambda:mutation(lambda p,q,s:q.write_bytes(bytes(s.raw)+b'x')))
  check('leaf_truncate_EOF_refused',lambda:mutation(lambda p,q,s:q.write_bytes(b'{}')))
  check('leaf_attrs_drift_refused',lambda:mutation(lambda p,q,s:os.setxattr(q,'user.neutral175',b'drift')))
  check('leaf_hardlink_refused',lambda:mutation(lambda p,q,s:os.link(q,p/'alias')))
  def swap(p,q,s):q.rename(p/'retained');q.write_bytes(s.raw);q.chmod(0o600)
  check('leaf_path_swap_samebytes_refused',lambda:mutation(swap))
  check('leaf_mtime_refused',lambda:mutation(lambda p,q,s:os.utime(q,ns=(q.stat().st_atime_ns,q.stat().st_mtime_ns+1000))))
  def closefd():
   p,q=fresh();s=Whole(q,33554432);os.close(s.directories[-1]['fd'])
   try:refuses(s.reseal173)
   finally:s.close173()
  check('closed_ancestor_FD_refused_and_cleanup_deterministic',closefd)
  def leaks():
   before=len(os.listdir('/proc/self/fd'))
   for _ in range(12):
    p,q=fresh();p.chmod(0o777);refuses(lambda:Whole(q,33554432))
   assert len(os.listdir('/proc/self/fd'))==before
  check('failed_constructor_partial_dir_chain_no_FD_leaks',leaks)
  def attrserror():
   p,q=fresh();before=len(os.listdir('/proc/self/fd'));error=OSError(5,'NEUTRAL_INJECTED_ORIGINAL_XATTR_ERROR')
   with unittest.mock.patch('os.listxattr',side_effect=error):
    try:Whole(q,33554432)
    except OSError as actual:assert actual is error
    else:raise AssertionError('Missing original attribute error')
   assert len(os.listdir('/proc/self/fd'))==before
  check('unknown_ancestor_attrs_original_error_retained_no_leak',attrserror)
  def uid():
   fake=types.SimpleNamespace(st_mode=stat.S_IFDIR|0o700,st_uid=os.getuid()+100001);refuses(lambda:S['_directory_policy175']('/NEUTRAL_PRIVATE',fake,os.getuid()))
  check('ancestor_ownerpredicateunit_FOREIGN_UID_PHYSICAL_UNPROVEN',uid)
  def ABI():
   p,q=fresh();s=q.stat();v=S['_identity173'](s);assert v[3]==s.st_mode and v[5]==s.st_size and v[8]==s.st_gid
  check('historical_snapshot_identity_ABI_mode3_size5_preserved_GID_added',ABI)
  def source_entry():
   p=root/'ENTRY153_FRESH_NEUTRAL_PARENT';p.mkdir(mode=0o700);c=copy.deepcopy(cfg);c['path_roles']['holder_parent']=str(p);H['history154'](own,c,before_RX=True);receipt=H['prepare_child154'](own,c);H['check_child154'](receipt,c,empty=True);child=H['consume_child154'](receipt,c);assert (child/'originals').is_dir();H['check_child154'](receipt,c,empty=False);refuses(lambda:H['check_child154'](receipt,c,empty=True));model=copy.deepcopy(own);model['state']='NATIVE153_RX_START';model['native153']={'records':[{'phase':'RX_START','payload':{'holder_preparation154':receipt}}]};H['current_prestart154'](model,c,empty=False);assert H['binding_selector165'](model,{'direction_number':153})=={'number':153,'key':'native153'}
  check('F1_REAL_history_prepare_check_consume_nonempty_current153_before_RX_registry',source_entry)
  def partialrefuse():
   p=root/'ENTRY153_PREEXISTING_PARTIAL_NO_ADOPTION';p.mkdir(mode=0o700);(p/'holder').mkdir(mode=0o700);c=copy.deepcopy(cfg);c['path_roles']['holder_parent']=str(p);refuses(lambda:H['prepare_child154'](own,c))
  check('F1_fresh_parent_required_partial_child_never_adopted',partialrefuse)
  def lifecycle():
   p,q=fresh();before=len(os.listdir('/proc/self/fd'));s=Whole(q,33554432);s.reseal173();s.close173();s.close173();refuses(s.reseal173);assert len(os.listdir('/proc/self/fd'))==before
  check('positive_full_FD_chain_leaf_reseal_close_idempotent_no_leak',lifecycle)
  def pooled(change=False):
   parent,leaf=fresh();pool=S['_Invocation175']();resources=[];before=len(os.listdir('/proc/self/fd'))
   try:
    for i in range(4):
     q=parent/('pool'+str(i));q.write_bytes(b'NEUTRAL');q.chmod(0o600);resources.append(pool.open175(str(q),33554432))
    assert len(pool.nodes)==len(resources[0].directories)
    if change:
     parent.chmod(0o777)
     for r in resources:r.reseal173()
     refuses(pool.reseal175)
    else:
     for r in resources:r.reseal173()
     pool.reseal175()
   finally:
    for r in resources:r.close173()
    pool.close175()
   assert len(os.listdir('/proc/self/fd'))==before
  check('pooled_shared_dirs_exact_FDs_full_lastconsumer_seal_no_leak',pooled)
  check('pooled_parent_mutation_refused_at_guard_before_any_effect',lambda:pooled(True))
  def pooledfail():
   before=len(os.listdir('/proc/self/fd'));pool=S['_Invocation175']();parent,leaf=fresh();parent.chmod(0o777)
   try:refuses(lambda:pool.open175(str(leaf),33554432))
   finally:pool.close175()
   assert len(os.listdir('/proc/self/fd'))==before
  check('pooled_constructor_partial_failure_closes_all_registered_dirs',pooledfail)
  check('explicit_runtime_shared_workspace_qualified_not_private_waiver',lambda:None if S['_directory_policy175']('/workspace',os.stat('/workspace'),os.stat('/').st_uid)=='QUALIFIED_RUNTIME_SHARED_WORKSPACE_FD'else(_ for _ in()).throw(AssertionError()))
  check('all_historical149_150_151_152_dispatches_still_delegated_source_exact',lambda:None if H['old']['ORIGINAL']==H['ORIGINAL']else(_ for _ in()).throw(AssertionError()))
 result={'schema':'SOURCE175_PHYSICAL_ANCESTOR_AND_ACTUAL_PRESTART_QUALIFICATION','status':'PASS'if all(x['status']=='PASS'for x in rows)else'FAIL','cases':len(rows),'rows':rows,'native_effects':0,'physical_UID_change':'UNPROVEN; logical owner predicate unit only','shared_exception':'Only root-owned runtime /workspace0777 and root-owned sticky/tmp1777; pinned directory FD/link/identity/mode/ALLattrs, safe owned descendant mandatory. No generic writable ancestor waiver.'};Path(out).write_text(json.dumps(result));return result
if __name__=='__main__':
 result=qualify175(json.loads(Path(sys.argv[1]).read_bytes()),json.loads(Path(sys.argv[2]).read_bytes()),sys.argv[3]);print(json.dumps({'status':result['status'],'cases':result['cases']}));raise SystemExit(0 if result['status']=='PASS'else 1)
