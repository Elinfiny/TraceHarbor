"""SOURCE179 affected pure regressions only. All synthetic originals DATA_ONLY.
No provider call, native capability, write helper, clock/once/registry effect.
"""
from pathlib import Path
import unittest,runpy,json,sys,os,copy,hashlib,tempfile,random,ast
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT));F=runpy.run_path(str(ROOT/'test177.py'));P=runpy.run_path(str(ROOT/'proof179.py'));O=runpy.run_path(str(ROOT/'outer_metadata179.py'))
class WholeProof179(unittest.TestCase):
 def setUp(self):self.f=F['WholeAdapter']();self.f.setUp()
 def tearDown(self):self.f.tearDown()
 def check(self):return O['verify_readback179'](self.f.original,self.f.expected,str(self.f.candidate),O['read_frame177']())
 def test_all_four_predicates_equal_accepted178(self):
  old=runpy.run_path(str(ROOT/'authority153.py'))
  for t in self.f.ts:
   d,p,_=P['proof179'](t['workspace_path'],t,original=self.f.original);before=old['proof152'](t['workspace_path'],t,original=self.f.original);self.assertEqual((d,p),before)
 def test_whole_outer_candidate_and_all_source_FDs(self):
  r=self.check();self.assertEqual(len(r['proofs']),4);self.assertTrue(r['all_last_consumer_FD_ancestor_seals']);self.assertGreater(r['source_freeze_files'],226);self.assertFalse(r['native_authority']);self.assertEqual(r['writes'],0)
 def test_corrupt_self_refuses(self):
  t=self.f.ts[0];p=Path(t['workspace_path']);d=json.loads(p.read_bytes());d['self_sha256']='f'*64;p.write_text(json.dumps(d));t['size_bytes']=p.stat().st_size
  with self.assertRaises(ValueError):P['proof179'](str(p),t,original=self.f.original)
 def test_truncated_json_refuses(self):
  t=self.f.ts[0];p=Path(t['workspace_path']);p.write_bytes(p.read_bytes()[:-5]);t['size_bytes']=p.stat().st_size
  with self.assertRaises(ValueError):P['proof179'](str(p),t,original=self.f.original)
 def test_stale_expected_version_refuses(self):
  self.f.expected['version']=2
  with self.assertRaises(ValueError):self.check()
 def test_mixed_role_attributes_refuse(self):
  t=self.f.ts[3];os.setxattr(t['workspace_path'],'user.library-file-id',self.f.ts[2]['library_file_id'].encode())
  with self.assertRaises(ValueError):P['proof179'](t['workspace_path'],t,original=self.f.original)
 def test_false_expected_hash_refuses(self):
  self.f.expected['sha256']='f'*64
  with self.assertRaises(ValueError):self.check()
 def test_false_expected_self_refuses(self):
  self.f.expected['self_sha256']='f'*64
  with self.assertRaises(ValueError):self.check()
 def test_false_file_id_refuses(self):
  self.f.expected['file_id']='file_SYNTHETIC_WRONG'
  with self.assertRaises(ValueError):self.check()
 def test_missing_fourth_refuses(self):
  self.f.original['structuredContent']['transfers']=self.f.ts[:3]
  with self.assertRaises(ValueError):self.check()
 def test_copied_original_member_refuses(self):
  t=self.f.ts[0]
  with self.assertRaises(ValueError):P['proof179'](t['workspace_path'],copy.deepcopy(t),original=self.f.original)
 def test_provider_error_refuses(self):
  self.f.original['isError']=True
  with self.assertRaises(ValueError):self.check()
 def test_symlink_refuses(self):
  t=self.f.ts[0];p=Path(t['workspace_path']);q=p.with_suffix('.old');p.rename(q);p.symlink_to(q)
  with self.assertRaises((ValueError,OSError)):P['proof179'](str(p),t,original=self.f.original)
 def test_exact_returned_path_required(self):
  t=self.f.ts[0]
  with self.assertRaises(ValueError):P['proof179'](str(self.f.candidate),t,original=self.f.original)
 def test_boolean_version_refuses(self):
  self.f.ts[0]['current_version_number']=True
  with self.assertRaises(ValueError):self.check()
 def test_negative_size_refuses(self):
  t=self.f.ts[0];t['size_bytes']=-1
  with self.assertRaises(ValueError):P['proof179'](t['workspace_path'],t,original=self.f.original)
 def test_wrong_attribute_after_completion_refuses(self):
  self.f.ts[0]['xattrs'].append({'name':'user.synthetic-required','value':'expected'})
  with self.assertRaises((ValueError,OSError)):self.check()
 def test_153_terminal_not_CAS_write_proof(self):
  frame=O['read_frame177']();frame['kind']='CAS_READBACK'
  with self.assertRaises(ValueError):O['verify_readback179'](self.f.original,self.f.expected,str(self.f.candidate),frame)
 def test_exact25_deadline_remains_failure(self):
  with self.assertRaises(TimeoutError):O['require_timing177']({'kind':'READ_ONLY_QUALIFICATION','origin_mono':0.,'origin_utc':0.,'ack_mono':0.,'ack_utc':0.},25.,25.)
 def test_all_other_metadata_cap_still64MiB(self):
  self.assertEqual(P['E']['GENERIC'],67108864);self.assertEqual(P['E']['TRACE'],83886080);self.assertEqual(P['E']['PRIVATE'],33554432)
class Canonical179(unittest.TestCase):
 def test_stdlib_equivalence_generated_nested_values(self):
  rng=random.Random(179);values=[None,True,False,0,-0.0,1.234567890123,1e-6,'ă漢字\n\u0000\\\"',{'z':1,'a':[True,None,1.2]},'x'*65537]
  for i in range(150):values.append({'index':i,'random':[rng.randint(-1000000,1000000),rng.random(),'ț'*rng.randint(0,40)],'nested':{'a':i%2==0}})
  for value in values:self.assertEqual(P['S'].canonical_sha173(value),hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest())
 def test_nonfinite_and_cycles_refuse(self):
  cyclic=[];cyclic.append(cyclic)
  for value in(float('nan'),float('inf'),cyclic):
   with self.assertRaises(ValueError):P['S'].canonical_sha173(value)
 def test_manifest_closed_complete_source_freeze(self):
  f=P['SourceFreeze179']()
  try:self.assertGreater(len(f.resources),226);f.finish179()
  finally:f.close179()
 def test_candidate_parse_and_no_write_helper(self):
  for name in('proof179.py','outer_metadata179.py','outer_complete179.py'):ast.parse((ROOT/name).read_bytes())
  self.assertNotIn('library_upload.py',(ROOT/'outer_complete179.py').read_text());self.assertNotIn('replace_library_file',(ROOT/'outer_complete179.py').read_text())
if __name__=='__main__':unittest.main(verbosity=2)
