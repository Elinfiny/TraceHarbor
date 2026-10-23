"""SOURCE177 affected contracts/integration only. Synthetic fixtures are DATA_ONLY,
never actual provider receipts, actor evidence or native capabilities.
"""
import unittest,pathlib,json,sys,copy,runpy,tempfile,os,hashlib,importlib.util,ast
ROOT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from snapshot174 import Whole173,canonical_sha173
O=runpy.run_path(str(ROOT/'outer_metadata177.py'));H=runpy.run_path(str(ROOT/'prestart177.py'));R=runpy.run_path(str(ROOT/'references177.py'))
from fixtures178 import CFG,OWN,OLDP
class Contract154(unittest.TestCase):
 def test_synthetic_closed153_predecessor_and_older_pins(self):
  self.assertEqual(H['history154'](OWN,CFG,before_RX=True)['predecessor'],153)
 def test_wrong_predecessor_phase_even_if_rehashed(self):
  d=copy.deepcopy(OWN);d['native153']['phase']='RX_START';c=copy.deepcopy(CFG);c['prestart154']['predecessor153_sha256']=H['sha'](H['can'](d['native153']))
  with self.assertRaises(ValueError):H['history154'](d,c,before_RX=True)
 def test_wrong_whole_history_pin(self):
  c=copy.deepcopy(CFG);c['prestart154']['preserved152_sha256']='f'*64
  with self.assertRaises(ValueError):H['history154'](OWN,c,before_RX=True)
 def test_existing154_cannot_rearm(self):
  d=dict(OWN,native154={})
  with self.assertRaises(ValueError):H['history154'](d,CFG,before_RX=True)
 def test_consumed153_selector_stays_closed(self):
  with self.assertRaises(ValueError):H['binding_selector165'](OWN,{'direction_number':153})
 def test_154_selector_cannot_select153(self):
  with self.assertRaises(ValueError):H['binding_selector165'](OWN,{'direction_number':154})
 def test_legacy_history_delegates_identically(self):
  previous=runpy.run_path(str(ROOT/'prestart174.py'))
  self.assertEqual(H['history154'](OWN,OLDP['static_CONFIG'],before_RX=False),previous['history154'](OWN,OLDP['static_CONFIG'],before_RX=False))
 def test_six_exact_substitutions_and_inverse(self):
  raw=OLDP['writer_preview']['full_original_source_utf8'];derived,rows=H['derive154'](raw,1234567);self.assertEqual(len(rows),6);v=derived
  for row in reversed(rows):v=v.replace(row['after'],row['before'])
  self.assertEqual(v,raw);self.assertIn("'native154'",derived);self.assertIn("'NATIVE153_TERMINAL'",derived);self.assertNotIn("'native153'",derived);ast.parse(derived)
 def test_positive_future_A_only(self):
  for v in (0,-1,True,None):
   with self.assertRaises(ValueError):H['derive154'](OLDP['writer_preview']['full_original_source_utf8'],v)
 def test_cross153_reference_rejected(self):
  with self.assertRaises(ValueError):R['selector165'](['native153','records',1,'payload','phase_intent127','context'],'context',2)
 def test_154_prior_only_reference(self):
  self.assertEqual(R['selector165'](['native154','records',1,'payload','phase_intent127','context'],'context',2)[0],'native154')
  with self.assertRaises(ValueError):R['selector165'](['native154','records',2,'payload','phase_intent127','context'],'context',2)
 def test_no_future_holder_created(self):
  self.assertFalse(pathlib.Path(CFG['path_roles']['holder_parent']).exists())
class Timing(unittest.TestCase):
 def f(self,ack=149):return {'kind':'CAS_READBACK','origin_mono':100.,'origin_utc':1000.,'ack_mono':float(ack),'ack_utc':900.+ack}
 def test_within_all_original_limits(self):self.assertTrue(O['require_timing177'](self.f(),173.999,1073.999))
 def test_readback_exact25_fails(self):
  with self.assertRaises(TimeoutError):O['require_timing177'](self.f(110),135.,1035.)
 def test_cas_exact50_fails(self):
  with self.assertRaises(TimeoutError):O['require_timing177'](self.f(150),150.,1050.)
 def test_phase_exact75_fails(self):
  with self.assertRaises(TimeoutError):O['require_timing177'](self.f(149),175.,1075.)
 def test_utc_only_late_fails(self):
  with self.assertRaises(TimeoutError):O['require_timing177'](self.f(110),111.,1035.)
 def test_clock_regression_fails(self):
  with self.assertRaises(TimeoutError):O['require_timing177'](self.f(110),109.,1011.)
class WholeAdapter(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix='trace177-synthetic-');self.root=pathlib.Path(self.tmp.name);os.chmod(self.root,0o700);self.ts=[]
  for i,stable in enumerate(O['IDS']):
   d={'SYNTHETIC_DATA_ONLY_NOT_PROVIDER':True}
   if i==0:d.update(native_id='6acfe37b-828c-83eb-b466-7670beb64ff2',ownership={'owner':'TraceHarbor V1','duplicate_trace_route_owners':0},state='NATIVE153_TERMINAL',native153={'phase':'TERMINAL'})
   if i==1:d['integrity']={'canonical_json_sha256':None};d['integrity']['canonical_json_sha256']=canonical_sha173(d)
   else:d['self_sha256']=None;d['self_sha256']=canonical_sha173(d)
   raw=json.dumps(d,sort_keys=True,separators=(',',':')).encode();p=self.root/('SYNTHETIC_'+str(i)+'.json');p.write_bytes(raw);os.chmod(p,0o600);os.setxattr(p,'user.library-file-id',stable.encode());os.setxattr(p,'user.library-file-version',b'1');self.ts.append(dict(library_file_id=stable,file_id='file_SYNTHETIC_DATA_ONLY_'+str(i),current_version_number=1,size_bytes=len(raw),workspace_path=str(p),xattrs=[{'name':'user.library-file-version','value':'1'}]))
  self.original={'SYNTHETIC_DATA_ONLY_NOT_PROVIDER':True,'structuredContent':{'transfers':self.ts,'unavailable_items':[]},'isError':False};raw=pathlib.Path(self.ts[0]['workspace_path']).read_bytes();doc=json.loads(raw);self.candidate=self.root/'SYNTHETIC_candidate.json';self.candidate.write_bytes(raw);os.chmod(self.candidate,0o600)
  for k in os.listxattr(self.ts[0]['workspace_path']):os.setxattr(self.candidate,k,os.getxattr(self.ts[0]['workspace_path'],k))
  self.expected=dict(version=1,file_id=self.ts[0]['file_id'],bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),self_sha256=doc['self_sha256'])
 def tearDown(self):self.tmp.cleanup()
 def check(self):return O['verify_readback177'](self.original,self.expected,str(self.candidate),O['read_frame177']())
 def test_whole_tuple_source_guard_and_candidate_no_authority(self):
  r=self.check();self.assertFalse(r['native_authority']);self.assertEqual(r['writes'],0);self.assertEqual(len(r['proofs']),4);self.assertTrue(r['all_last_consumer_FD_ancestor_seals'])
 def test_missing_tuple(self):
  self.original['structuredContent']['transfers']=self.ts[:3]
  with self.assertRaises(ValueError):self.check()
 def test_wrong_fourth_tuple(self):
  self.ts[3]['library_file_id']='libfile_SYNTHETIC_WRONG_ROLE'
  with self.assertRaises(ValueError):self.check()
 def test_copied_transfer_not_original_member(self):
  with self.assertRaises(ValueError):O['verify_readback177'](self.original,self.expected,str(self.candidate),O['read_frame177'](),trace_transfer=copy.deepcopy(self.ts[0]))
 def test_alias_transfer_path(self):
  self.ts[3]['workspace_path']=self.ts[0]['workspace_path']
  with self.assertRaises(ValueError):self.check()
 def test_provider_error_no_retry(self):
  self.original['isError']=True
  with self.assertRaises(ValueError):self.check()
 def test_wrong_self(self):
  p=pathlib.Path(self.ts[0]['workspace_path']);d=json.loads(p.read_bytes());d['self_sha256']='0'*64;p.write_text(json.dumps(d));self.ts[0]['size_bytes']=p.stat().st_size;self.expected['bytes']=p.stat().st_size
  with self.assertRaises(ValueError):self.check()
 def test_wrong_returned_attribute(self):
  os.setxattr(self.ts[0]['workspace_path'],'user.library-file-version',b'2')
  with self.assertRaises(ValueError):self.check()
 def test_symlink_leaf(self):
  path=pathlib.Path(self.ts[0]['workspace_path']);saved=path.with_suffix('.saved');path.rename(saved);path.symlink_to(saved)
  with self.assertRaises((ValueError,OSError)):self.check()
 def test_candidate_readback_alias_rejected(self):
  with self.assertRaises(ValueError):O['verify_readback177'](self.original,self.expected,self.ts[0]['workspace_path'],O['read_frame177']())
 def test_last_consumer_ancestor_drift(self):
  f=Whole173(self.ts[0]['workspace_path'],83886080)
  try:
   os.chmod(self.root,0o755)
   with self.assertRaises(ValueError):f.reseal173()
  finally:f.close173();os.chmod(self.root,0o700)
 def test_last_consumer_leaf_drift(self):
  f=Whole173(self.ts[0]['workspace_path'],83886080)
  try:
   os.setxattr(self.ts[0]['workspace_path'],'user.synthetic-drift',b'1')
   with self.assertRaises(ValueError):f.reseal173()
  finally:f.close173()
 def test_wrong_source_pin(self):
  temp=self.root/'source';temp.mkdir(mode=0o700);(temp/'authority153.py').write_text('WRONG_SOURCE');(temp/'manifest.json').write_text(json.dumps({'source_files':{'diagnostic108/authority153.py':{'bytes':1,'sha256':'0'*64}}}));(temp/'outer_metadata177.py').write_bytes((ROOT/'outer_metadata177.py').read_bytes());m=runpy.run_path(str(temp/'outer_metadata177.py'))
  with self.assertRaises(ValueError):m['source177']()
if __name__=='__main__':unittest.main(verbosity=2)
