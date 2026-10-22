"""Q168A NEW synthetic source-only target. No live replies, mint, registry,
holder bootstrap, actual parent clock, private6, provider or business calls.
All timestamps below are explicit fixture integers; never provider evidence.
"""
from pathlib import Path
import runpy,json,copy,tempfile,types,importlib.util,sys
from unittest.mock import patch
ROOT=Path(__file__).resolve().parent
M=runpy.run_path(str(ROOT/'metadata168.py'));P=runpy.run_path(str(ROOT/'publication150.py'));A=runpy.run_path(str(ROOT/'authority152.py'))
spec=importlib.util.spec_from_file_location('Q168A_FIXED_SOURCE_ONLY',ROOT/'native127.py');N=importlib.util.module_from_spec(spec);spec.loader.exec_module(N);B=N.base
rows=[]
def test(name,fn):
 fn();rows.append({'case':name,'status':'PASS','scope':'SYNTHETIC_SOURCE_ONLY_NOT_PROVIDER_EVIDENCE'})
def refuses(fn,errors=(ValueError,TimeoutError,B.HostUnknown,RuntimeError)):
 try:fn()
 except errors:return
 raise AssertionError('Expected strict refusal')
def frame(id='SOURCE_FREEZE/CAS',op='library_replace',issued=0,pair=75000):return M['frame168'](id,op,issued,2340000,75000,pair)
def pair_success():
 f=frame();assert f['deadline_utc_ms']==50000
 # Publication return at20s is now eligible; an effect has no authority merely
 # from this metadata return. New readback15s current authority is mandatory.
 assert 15000<20000<f['deadline_utc_ms'];refuses(lambda:A['require_predecessor152']('admit/blob','ADMIT_CHAIN',600,2,None))
 rb=frame('ADMIT_CHAIN/readback','library_materialize',20000);assert rb['deadline_utc_ms']==45000
 assert M['authority_fresh168'](rb,30000);assert A['require_predecessor152']('admit/blob','ADMIT_CHAIN',600,2,{'scope':'ADMIT_CHAIN/readback','seq':2,'own_version':600})=='ADMIT_CHAIN/readback'
test('publish20s_then_fresh_readback_then_next_effect',pair_success)
test('entire_pair_after75_refused',lambda:refuses(lambda:frame('SOURCE_FREEZE/readback','library_materialize',75000)))
test('publish_cannot_borrow_readback25',lambda:refuses(lambda:frame(issued=51000)))
test('metadata_readback25_does_not_extend_AB15',lambda:refuses(lambda:M['authority_fresh168'](frame('ADMIT_CHAIN/readback','library_materialize',20000),35000)))
test('stale_AB_sequence_refused',lambda:refuses(lambda:A['require_predecessor152']('admit/blob','ADMIT_CHAIN',600,2,{'scope':'ADMIT_CHAIN/readback','seq':1,'own_version':600})))
test('retired_route_refused',lambda:refuses(lambda:A['require_predecessor152']('admit/blob','ADMIT_CHAIN',600,2,{'scope':'RETIRED_ROUTE','seq':2,'own_version':600})))
args={'library_file_id':P['OWN'],'file':'/SYNTHETIC_SOURCE_ONLY/metadata.json','expected_current_version':599,'version_reason':P['REASON']}
item={'local_path':args['file'],'purpose':'replace_library_file','status':'succeeded','file_id':'file_SYNTHETIC_NOT_PROVIDER','library_file_id':P['OWN'],'file_name':'TraceHarbor_V1_checkpoint.json','local_metadata_applied':True,'path':'/TraceHarbor_V1_checkpoint.json','current_version_number':600}
test('wrong_receipt_version_refused',lambda:refuses(lambda:P['validate_item150']({'results':[dict(item,current_version_number=601)]},args)))
test('provider_refusal_retained_not_success',lambda:refuses(lambda:P['validate_item150']({'results':[dict(item,status='failed')]},args)))
def assert_git():
 f=M['frame168']('admit/blob','github_create_blob',0,2340000,210000);assert f['deadline_utc_ms']==15000 and 16000>=f['deadline_utc_ms']
test('late_Git_stays15',assert_git)
def ledger_fixture(tmp,request):
 l=object.__new__(B.FrameLedger);l.root=Path(tmp);l.context={'domain':'SYNTHETIC_SOURCE_ONLY_NOT_PROVIDER'};l.seq=1;l.pending=dict(request,schema='TRACE118_HOST_REQUEST',seq=1,context=l.context,op='github_fetch',request_digest='f'*64);l.failed=False;l.remaining=lambda:60
 return l
def ipc_cases():
 with tempfile.TemporaryDirectory(prefix='source168-fixture-')as tmp:
  l=ledger_fixture(tmp,frame());raw=B.can({'schema':'TRACE118_HOST_RETURN','seq':1,'context':l.context,'op':'github_fetch','request_digest':'f'*64,'original_result':{'structuredContent':{'content':'{"fixture_only":true}'}},'transport_error':None,'late':False})
  with patch.object(B,'time',types.SimpleNamespace(time=lambda:20.0)):
   assert l.accept(raw)=={'fixture_only':True};refuses(lambda:l.accept(raw))
  assert (Path(tmp)/'1.return.original.json').read_bytes()==raw and list(Path(tmp).glob('1.duplicate-*'))
 with tempfile.TemporaryDirectory(prefix='source168-partial-')as tmp:
  l=ledger_fixture(tmp,frame());refuses(lambda:l.unknown_stream(b'{"partial":','CANCELLED'))
  assert l.failed and (Path(tmp)/'1.partial.original.bin').read_bytes()==b'{"partial":'
  with patch.object(B,'time',types.SimpleNamespace(time=lambda:20.0)):refuses(lambda:l.accept(b'{}'))
test('original_retention_duplicate_partialIPC_cancel_UNKNOWN_refused',ipc_cases)
def end_to_end_phase_limit():
 with tempfile.TemporaryDirectory(prefix='source168-over75-')as tmp:
  l=ledger_fixture(tmp,frame('SOURCE_FREEZE/readback','library_materialize',60000));raw=B.can({'schema':'TRACE118_HOST_RETURN','seq':1,'context':l.context,'op':'github_fetch','request_digest':'f'*64,'original_result':{'structuredContent':{'content':'{}'}},'transport_error':None,'late':False})
  with patch.object(B,'time',types.SimpleNamespace(time=lambda:75.001)):refuses(lambda:l.accept(raw))
  assert l.failed and (Path(tmp)/'1.return.original.json').read_bytes()==raw
test('CAS_readback_actual_adapter_after75_preserves_then_refuses',end_to_end_phase_limit)
def postbody():
 with tempfile.TemporaryDirectory(prefix='source168-body-')as tmp:
  p=Path(tmp)/'body';p.write_bytes(b'VALIDATED_PREIMAGE_FIXTURE');p.chmod(0o600);assert P['stable150'](p,83886080)==p.read_bytes();p.unlink();target=Path(tmp)/'target';target.write_bytes(b'x');p.symlink_to(target);refuses(lambda:P['stable150'](p,83886080))
test('posthelper_whole_stable_nofollow_equivalence',postbody)
print(json.dumps({'schema':'Q168A_NEW_FIRST_SOURCE_ONLY_PYTHON','status':'PASS','cases':rows,'live_provider_replies':0,'native_bootstrap_mint_registry_clock_child':0,'old_qualifications_rerun':0},sort_keys=True))
