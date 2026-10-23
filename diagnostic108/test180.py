"""Affected actual consumer180 pure DATA_ONLY tests, no registry/effect."""
from pathlib import Path
import unittest,runpy,json,sys,os,copy,time,hashlib,tempfile,ast,subprocess
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT));F=runpy.run_path(str(ROOT/'test177.py'));O=runpy.run_path(str(ROOT/'outer_metadata180.py'));P=O['P']
def frame(kind='READ_ONLY_QUALIFICATION'):
 m=time.monotonic();u=time.time();return {'kind':kind,'origin_mono':m,'origin_utc':u,'ack_mono':m,'ack_utc':u}
def consumer(kind='READ_ONLY',phase='QUALIFICATION'):return {'schema':'TRACE180_METADATA_CONSUMER_V1','kind':kind,'phase':phase}
class ActualConsumer180(unittest.TestCase):
 def setUp(self):self.f=F['WholeAdapter']();self.f.setUp()
 def tearDown(self):self.f.tearDown()
 def verify(self,c=None,f=None):return O['verify180'](self.f.original,self.f.expected,str(self.f.candidate),f or frame(),c or consumer())
 def test_current_whole4_candidate_complete_freeze(self):
  r=self.verify();self.assertEqual(len(r['proofs']),4);self.assertTrue(r['all_FD_ancestor_last_consumer_seals']);self.assertGreater(r['source_freeze_files'],231);self.assertFalse(r['native_authority'])
 def test_closed153_never_native_CAS(self):
  with self.assertRaises(ValueError):self.verify(consumer('NATIVE_OUTER','RX_START'),frame('CAS_READBACK'))
 def test_admin_distinct_not_native(self):
  d=json.loads(Path(self.f.ts[0]['workspace_path']).read_bytes());d['source180']={'phase':'REPAIR_TERMINAL'}
  self.assertTrue(O['consumer180'](consumer('ADMIN_SOURCE','ADMIN_CLOSURE'),frame('ADMIN_SOURCE_CAS'),d))
  with self.assertRaises(ValueError):O['consumer180'](consumer('ADMIN_SOURCE','ADMIN_CLOSURE'),frame('CAS_READBACK'),d)
 def test_actual_native_outer_positive_data(self):
  for phase in('RX_START','TERMINAL'):
   self.assertTrue(O['consumer180'](consumer('NATIVE_OUTER',phase),frame('CAS_READBACK'),{'state':'NATIVE154_'+phase,'native154':{'phase':phase},'SYNTHETIC_DATA_ONLY':True}))
 def test_wrong_native_phase_refuses(self):
  with self.assertRaises(ValueError):O['consumer180'](consumer('NATIVE_OUTER','TERMINAL'),frame('CAS_READBACK'),{'state':'NATIVE154_RX_START','native154':{'phase':'RX_START'}})
 def test_tuple_copy_not_member(self):
  t=self.f.ts[0]
  with self.assertRaises(ValueError):P['proof180'](t['workspace_path'],copy.deepcopy(t),original=self.f.original)
 def test_positive_nonbool_version(self):
  self.f.ts[0]['current_version_number']=True
  with self.assertRaises(ValueError):self.verify()
 def test_missing_fourth(self):
  self.f.original['structuredContent']['transfers'].pop()
  with self.assertRaises(ValueError):self.verify()
 def test_stale_identity(self):
  self.f.expected['file_id']='file_wrong'
  with self.assertRaises(ValueError):self.verify()
 def test_false_whole_hash(self):
  self.f.expected['sha256']='f'*64
  with self.assertRaises(ValueError):self.verify()
 def test_false_whole_self(self):
  self.f.expected['self_sha256']='f'*64
  with self.assertRaises(ValueError):self.verify()
 def test_attrs(self):
  os.setxattr(self.f.ts[0]['workspace_path'],'user.library-file-version',b'999')
  with self.assertRaises(ValueError):self.verify()
 def test_source_mode(self):
  p=Path(self.f.ts[0]['workspace_path']);p.chmod(0o666)
  with self.assertRaises((ValueError,OSError)):self.verify()
 def test_symlink(self):
  p=Path(self.f.ts[0]['workspace_path']);q=p.with_suffix('.before');p.rename(q);p.symlink_to(q)
  with self.assertRaises((ValueError,OSError)):self.verify()
 def test_truncated_whole(self):
  p=Path(self.f.ts[0]['workspace_path']);p.write_bytes(p.read_bytes()[:-4]);self.f.ts[0]['size_bytes']=p.stat().st_size
  with self.assertRaises(ValueError):self.verify()
 def test_distinct_candidate_inode(self):
  self.f.candidate=Path(self.f.ts[0]['workspace_path'])
  with self.assertRaises(ValueError):self.verify()
 def test_returned_path_exact(self):
  t=self.f.ts[0]
  with self.assertRaises(ValueError):P['proof180'](str(self.f.candidate),t,original=self.f.original)
 def test_official_completion_error_retained(self):
  C=runpy.run_path(str(ROOT/'outer_complete180.py'));helper=os.environ['TRACE178_HELPERS']+'/library_file_transfer.py'
  self.f.ts[0]['workspace_path']=str(Path(self.f.ts[0]['workspace_path']).with_name('ACTUALLY_MISSING_COMPLETION180.json'))
  with self.assertRaises(RuntimeError)as e:C['complete180'](self.f.original,self.f.expected,str(self.f.candidate),frame(),consumer(),helper)
  self.assertGreater(len(e.exception.completion180_originals),0);self.assertNotEqual(e.exception.completion180_originals[0]['returncode'],0)
 def test_undeclared_source_refused(self):
  p=ROOT/'UNDECLARED180_TEST';p.write_text('DATA_ONLY')
  try:
   with self.assertRaises(ValueError):P['SourceFreeze180']()
  finally:p.unlink()
 def test_source_FD_replacement(self):
  freeze=P['SourceFreeze180']();p=ROOT/'preparer180.py';q=ROOT/'preparer180.py.held-test';raw=p.read_bytes();mode=p.stat().st_mode
  try:
   p.rename(q);p.write_bytes(raw);p.chmod(mode&0o777)
   with self.assertRaises(ValueError):freeze.finish180()
  finally:p.unlink();q.rename(p);freeze.close180()
 def test_metadata_FD_replacement(self):
  S=O['S'];p=Path(self.f.ts[0]['workspace_path']);f=S.Whole173(str(p),83886080);q=p.with_suffix('.held');raw=p.read_bytes()
  try:
   p.rename(q);p.write_bytes(raw)
   with self.assertRaises(ValueError):f.reseal173()
  finally:f.close173()
class CurrentContracts180(unittest.TestCase):
 def test_strict25_50_75_dual_clocks(self):
  cases=[({'kind':'READ_ONLY_QUALIFICATION','origin_mono':0.,'origin_utc':0.,'ack_mono':0.,'ack_utc':0.},25.,24.),({'kind':'CAS_READBACK','origin_mono':0.,'origin_utc':0.,'ack_mono':50.,'ack_utc':49.},50.,49.),({'kind':'ADMIN_SOURCE_CAS','origin_mono':0.,'origin_utc':0.,'ack_mono':49.,'ack_utc':49.},75.,74.)]
  for f,m,u in cases:
   with self.assertRaises(TimeoutError):O['timing180'](f,m,u)
  self.assertTrue(O['timing180']({'kind':'CAS_READBACK','origin_mono':0.,'origin_utc':0.,'ack_mono':49.,'ack_utc':49.},73.,73.))
 def test_original_clock_regression(self):
  f=frame();f['ack_mono']+=1
  with self.assertRaises(TimeoutError):O['timing180'](f,time.monotonic(),time.time())
 def test_all_source_parse(self):
  for p in ROOT.glob('*.py'):ast.parse(p.read_bytes())
 def test_actual_controller_bundle_parse(self):
  bundle=runpy.run_path(str(ROOT/'render_controller180.py'))['render146']();s=bundle['full_source_utf8'];self.assertIn('await outerConsumer180(preloaded.outer180.RX_START,tools)',s);self.assertIn('TRACE180_AUTHENTIC_TERMINAL_READBACK',s)
  r=subprocess.run(['node','--input-type=module','-e','new (Object.getPrototypeOf(async function(){}).constructor)("tools","notify",'+json.dumps(s)+');'],capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr)
 def test_changed_canonical_exact_stdlib(self):
  E=runpy.run_path(str(ROOT/'envelope158.py'))
  for v in(None,True,False,0,-0.0,1.234e-6,{'ă':['漢字',1,True,None]},'x'*70001):self.assertEqual(E['canonical_sha158'](v),hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest())
 def test_semantic154_153_positive_negative(self):
  f=runpy.run_path(str(ROOT/'fixtures178.py'));K=runpy.run_path(str(ROOT/'compatibility177.py'))
  for n in(154,153):
   release,cfg,mb,snap=f['semantic_fixture178'](n);self.assertTrue(K['validate165'](release,cfg,mb,snap))
  args=f['semantic_fixture178'](153);self.assertEqual(K['validate165'](*args),runpy.run_path(str(ROOT/'compatibility174.py'))['validate165'](*args))
  release,cfg,mb,snap=f['semantic_fixture178'](154);snap['holder_preparation154']['predecessor']=152;snap['prestart154']['prepared_receipt_sha256']=f['sha'](f['can'](snap['holder_preparation154']))
  with self.assertRaises(ValueError):K['validate165'](release,cfg,mb,snap)
 def test_historical179_manifest_unchanged(self):
  self.assertEqual((ROOT/'manifest179.json').read_bytes(),(ROOT.parent.parent/'accepted156/SOURCE179/diagnostic108/manifest179.json').read_bytes())
if __name__=='__main__':unittest.main(verbosity=2)
