"""Second final iteration publisher guards; no provider/native effects."""
from pathlib import Path
import runpy,unittest,json,ast
R=Path(__file__).resolve().parent
f=runpy.run_path(str(R/'test177.py'));P=runpy.run_path(str(R/'outer_publish177.py'))
class PublishGuard(f['WholeAdapter']):
 def test_no_native_admission_no_publication(self):
  t=self.ts[1];p=Path(t['workspace_path']);d=json.loads(p.read_bytes());d['operation']={'effect_replay_boundary':{'recipient_outboxes':{'TraceHarbor V1':{'id':'V29-TRACE-154-SYNTHETIC-DATA_ONLY','native_admission':False}}}};d['integrity']['canonical_json_sha256']=None;d['integrity']['canonical_json_sha256']=f['canonical_sha173'](d);p.write_text(json.dumps(d));t['size_bytes']=p.stat().st_size
  with self.assertRaises(PermissionError):P['validate_publish177'](self.original,str(self.candidate),f['CFG'],'RX_START',1)
 def test_wrong_phase_before_any_write(self):
  with self.assertRaises(ValueError):P['validate_publish177']({},str(self.candidate),{},'PUBLISH_INTENT',1)
 def test_positive_version_only(self):
  for v in (0,-1,True):
   with self.assertRaises(ValueError):P['validate_publish177']({},str(self.candidate),{},'TERMINAL',v)
class Wiring(unittest.TestCase):
 def test_future154_guard_and_compaction(self):
  self.assertIn('from guard177 import current_binding174',(R/'prestart177.py').read_text());n=(R/'native127.py').read_text();self.assertIn('from guard177 import check177',n);self.assertIn("current['number'] in (153,154)",n)
 def test_caller154_sibling_guard(self):
  s=(R/'caller177.mjs').read_text();self.assertIn('/^V29-TRACE-154-/',s);self.assertIn('TRACE177_PRESTART154_PREDECESSOR153_V1',s);self.assertIn("assert 'snapshot174' not in sys.modules",s)
 def test_actual_source_publication_origin_not_supplied(self):
  s=(R/'outer_publish177.py').read_text();self.assertIn('origin_mono=time.monotonic();origin_utc=time.time()',s);self.assertIn('ack_mono=time.monotonic();ack_utc=time.time()',s);self.assertNotIn('frame=json.loads',s)
 def test_affected_python_parse(self):
  for p in R.glob('*177.py'):ast.parse(p.read_bytes(),filename=str(p))
if __name__=='__main__':unittest.main(verbosity=2)
