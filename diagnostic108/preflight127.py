"""Invoked only AFTER the inline caller anchored EVERY byte to native current.
No source-only127 text carries the actual admission markers required here.
"""
import sys,json,pathlib,hashlib,io,runpy,os,copy,importlib.util
ROOT=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def can(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
_spec=importlib.util.spec_from_file_location('trace128_preflight_helper',ROOT/'helper_channel128.py');helper128=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(helper128)
def main():
 original=json.loads(pathlib.Path(sys.argv[1]).read_bytes());cfg=json.loads(pathlib.Path(sys.argv[2]).read_bytes());ts=original['structuredContent']['transfers'];docs={}
 own_transfer=next(t for t in ts if t['library_file_id']=='libfile_3ee8270f03d8819188e1de1f75c3d824');initial_own=json.loads(pathlib.Path(own_transfer['workspace_path']).read_bytes());v=copy.deepcopy(initial_own);expected=v['self_sha256'];v['self_sha256']=None
 if sha(can(v))!=expected:raise ValueError('Actual owned self before helper/config execution')
 initial_key='native'+initial_own['state'].split('_')[0][6:];actual_admission=initial_own[initial_key]['direction'].get('grouped127_admission');bound_cfg=copy.deepcopy(cfg);bound_cfg['native_admission127']=None;bound_cfg.pop('config_path',None)
 if not actual_admission or actual_admission!=cfg.get('native_admission127') or actual_admission.get('config_binding_sha256')!=sha(can(bound_cfg)) or sha(pathlib.Path(cfg['library_helper']).read_bytes())!=cfg['library_helper_sha256']:raise ValueError('Whole actual source/config/helper admission before helper execution')
 for t in ts:
  path=pathlib.Path(t['workspace_path']);raw=path.read_bytes();d=json.loads(raw);v=copy.deepcopy(d)
  if t['library_file_id']=='libfile_505e4189bc588191bcda811c4a35da79':expected=v['integrity']['canonical_json_sha256'];v['integrity']['canonical_json_sha256']=None
  else:expected=v['self_sha256'];v['self_sha256']=None
  if sha(can(v))!=expected or len(raw)!=t['size_bytes']:raise ValueError('Actual whole/current self/source')
  identity={'phase':'PREFLIGHT','run':cfg['integration_context127']['once_receipt_sha256'],'source':cfg['source_sha'],'call':'preflight/'+t['library_file_id']}
  helper128.run_helper128(cfg['library_helper'],cfg['library_helper_sha256'],path,t['library_file_id'],t['xattrs'],identity,lambda ident,record:helper128.retain_private128(cfg['capture_directory'],ident,record))
  if os.getxattr(path,'user.library-file-id').decode()!=t['library_file_id']:raise ValueError('Actual identity')
  for x in t['xattrs']:
   if os.getxattr(path,x['name']).decode()!=x['value']:raise ValueError('ALL actual xattrs')
  docs[t['library_file_id']]=(d,t,raw)
 own,t,raw=docs['libfile_3ee8270f03d8819188e1de1f75c3d824'];audit,at,araw=docs['libfile_505e4189bc588191bcda811c4a35da79'];policy,pt,praw=docs['libfile_6f69ae483b088191a1fffefca617bbd5'];key='native'+own['state'].split('_')[0][6:];n=own[key]
 boundary=audit['operation']['effect_replay_boundary'];boundary=json.loads(boundary) if isinstance(boundary,str) else boundary
 if n['direction']!=boundary['recipient_outboxes']['TraceHarbor V1'] or own['ownership']['owner']!='TraceHarbor V1' or own['ownership']['duplicate_trace_route_owners']!=0 or own['native_id']!='6acfe37b-828c-83eb-b466-7670beb64ff2':raise ValueError('Current addressed ownership/no stale source')
 if pathlib.Path(cfg['current_checkpoint']).read_bytes()!=raw or cfg['current_version']!=t['current_version_number'] or pathlib.Path(cfg['writer_binding']['auditor_path']).read_bytes()!=araw or cfg['writer_binding']['auditor_version']!=at['current_version_number'] or pt['current_version_number']<101:raise ValueError('Actual current source binding changed; no rebase/retry')
 if sha(pathlib.Path(cfg['library_helper']).read_bytes())!=cfg['library_helper_sha256']:raise ValueError('Actual helper source pin')
 s=__import__('importlib.util').util.spec_from_file_location('trace127_preflight_control',ROOT/'control127.py');ctl=__import__('importlib.util').util.module_from_spec(s);s.loader.exec_module(ctl)
 admission=n['direction'].get('grouped127_admission');inventory=ctl.inventory127()
 if admission!=cfg['native_admission127'] or admission.get('inclusive_cap')!=inventory['inclusive_total'] or admission.get('contract')!='TRACE127_PHASE_INTENT_V1':raise ValueError('Actual exact independent prospective journal/cap boundary')
 print(json.dumps({'schema':'TRACE127_NATIVE_PREFLIGHT_ORIGINAL_V1','current_admission':admission,'inventory_sha256':sha(can(inventory)),'own_version':t['current_version_number'],'auditor_version':at['current_version_number'],'policy_version':pt['current_version_number'],'whole_self_allattrs':'PASS'}))
if __name__=='__main__':main()
