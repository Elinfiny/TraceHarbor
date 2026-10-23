"""Whole semantic producer/consumer and offline outer descriptor regressions.
All fixtures SYNTHETIC DATA_ONLY; no authentic admission or native effect.
"""
import unittest,runpy,copy,json,time,hashlib
from pathlib import Path
from fixtures178 import semantic_fixture178,CFG,can,sha,ROOT
C=runpy.run_path(str(ROOT/'compatibility177.py'));H=runpy.run_path(str(ROOT/'prestart177.py'))
class Semantic178(unittest.TestCase):
 def test_full154_producer153_validator_returns153(self):
  args=semantic_fixture178();result=C['validate165'](*args);self.assertEqual(args[3]['holder_preparation154']['predecessor'],153);self.assertEqual(result['predecessor'],153);self.assertFalse(result['native_authority'])
 def test_rehashed152_receipt_rejected_for154(self):
  r,c,m,s=semantic_fixture178();s['holder_preparation154']['predecessor']=152;s['prestart154']['prepared_receipt_sha256']=sha(can(s['holder_preparation154']))
  with self.assertRaisesRegex(ValueError,'whole154/pre153'):C['validate165'](r,c,m,s)
 def test_contract_receipt_mismatch_rejected(self):
  r,c,m,s=semantic_fixture178();c['prestart154']['predecessor']=152
  with self.assertRaises(ValueError):C['validate165'](r,c,m,s)
 def test_full_historical153_152_exact_delegation(self):
  args=semantic_fixture178(153);prior=runpy.run_path(str(ROOT/'compatibility174.py'));actual=C['validate165'](*args);self.assertEqual(actual,prior['validate165'](*args));self.assertEqual(actual['predecessor'],152)
 def test_source177_bug_reproduced_without_effect(self):
  # Exact original preimage is supplied as review history, never imported as authority.
  old=ROOT.parent.parent/'review/history177/postimages/diagnostic108/compatibility177.py'
  ns={'__file__':str(ROOT/'compatibility177.py'),'__name__':'DATA_ONLY_PREIMAGE177'};exec(compile(old.read_bytes(),str(old),'exec'),ns)
  args=semantic_fixture178()
  with self.assertRaisesRegex(ValueError,'whole152/pre151'):ns['validate165'](*args)
  r,c,m,s=args;s['holder_preparation154']['predecessor']=152;s['prestart154']['prepared_receipt_sha256']=sha(can(s['holder_preparation154']));self.assertEqual(ns['validate165'](r,c,m,s)['predecessor'],152)
 def test_pure_producer_rejects_boolean_identity(self):
  ident={'dev':True,'ino':1,'uid':0,'mode':448,'type':'directory'}
  with self.assertRaises(ValueError):H['receipt_from_identities178'](CFG,CFG['path_roles']['holder_parent'],ident,ident)
 def test_pure_producer_rejects_foreign_contract(self):
  cfg=copy.deepcopy(CFG);cfg['prestart154']['predecessor']=152
  with self.assertRaises(ValueError):H['receipt_from_identities178'](cfg,cfg['path_roles']['holder_parent'],{}, {})
 def test_pure_producer_is_shared_by_actual_producer(self):
  import ast
  tree=ast.parse((ROOT/'prestart177.py').read_bytes());f=next(x for x in tree.body if isinstance(x,ast.FunctionDef)and x.name=='prepare_child154')
  self.assertEqual(len([x for x in ast.walk(f)if isinstance(x,ast.Call)and isinstance(x.func,ast.Name)and x.func.id=='receipt_from_identities178']),1)
F=runpy.run_path(str(ROOT/'test177.py'));BASE=F['WholeAdapter']
class Outer178(unittest.TestCase):
 def setUp(self):self.f=BASE();self.f.setUp()
 def tearDown(self):self.f.tearDown()
 def phase(self,phase):
  f=self.f;p=Path(f.ts[0]['workspace_path']);d=json.loads(p.read_bytes());d['state']='NATIVE154_'+phase;d['native154']={'phase':phase,'SYNTHETIC_DATA_ONLY_NOT_NATIVE_AUTHORITY':True};d['self_sha256']=None;d['self_sha256']=F['canonical_sha173'](d);raw=can(d);p.write_bytes(raw);f.candidate.write_bytes(raw);f.ts[0]['size_bytes']=len(raw);f.expected.update(bytes=len(raw),sha256=sha(raw),self_sha256=d['self_sha256']);now=time.monotonic();utc=time.time();return {'kind':'CAS_READBACK','origin_mono':now,'origin_utc':utc,'ack_mono':now,'ack_utc':utc}
 def check(self,frame):return F['O']['verify_readback177'](self.f.original,self.f.expected,str(self.f.candidate),frame)
 def test_RX_full_completion_descriptor(self):self.assertEqual(self.check(self.phase('RX_START'))['state'],'NATIVE154_RX_START')
 def test_TERMINAL_full_completion_descriptor(self):self.assertEqual(self.check(self.phase('TERMINAL'))['state'],'NATIVE154_TERMINAL')
 def test_wrong_candidate_bytes_rejected(self):
  frame=self.phase('RX_START');self.f.expected['bytes']+=1
  with self.assertRaises(ValueError):self.check(frame)
 def test_wrong_candidate_hash_rejected(self):
  frame=self.phase('RX_START');self.f.expected['sha256']='f'*64
  with self.assertRaises(ValueError):self.check(frame)
 def test_wrong_candidate_self_rejected(self):
  frame=self.phase('TERMINAL');self.f.expected['self_sha256']='f'*64
  with self.assertRaises(ValueError):self.check(frame)
 def test_wrong_candidate_version_rejected(self):
  frame=self.phase('TERMINAL');self.f.expected['version']=2
  with self.assertRaises(ValueError):self.check(frame)
 def test_wrong_candidate_file_id_rejected(self):
  frame=self.phase('RX_START');self.f.expected['file_id']='file_SYNTHETIC_OTHER'
  with self.assertRaises(ValueError):self.check(frame)
 def test_missing_original4_rejected(self):
  frame=self.phase('TERMINAL');self.f.original['structuredContent']['transfers']=self.f.ts[:3]
  with self.assertRaises(ValueError):self.check(frame)
 def test_no_admission_RX_and_TERMINAL_refuse_before_helper(self):
  from unittest.mock import patch
  p=Path(self.f.ts[1]['workspace_path']);d=json.loads(p.read_bytes());d['operation']={'effect_replay_boundary':{'recipient_outboxes':{'TraceHarbor V1':{'id':'V29-TRACE-154-SYNTHETIC','native_admission':False}}}};d['integrity']['canonical_json_sha256']=None;d['integrity']['canonical_json_sha256']=F['canonical_sha173'](d);p.write_bytes(can(d));self.f.ts[1]['size_bytes']=p.stat().st_size
  pub=runpy.run_path(str(ROOT/'outer_publish177.py'))
  with patch('subprocess.run',side_effect=AssertionError('WRITE_HELPER_MUST_NOT_RUN'))as helper:
   for phase in('RX_START','TERMINAL'):
    with self.assertRaises(PermissionError):pub['validate_publish177'](self.f.original,str(self.f.candidate),CFG,phase,1)
   helper.assert_not_called()
if __name__=='__main__':unittest.main(verbosity=2)
