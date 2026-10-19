"""Read-only wheel inventory; no import/extract/install. Requires exact accepted lock hashes."""
import pathlib,hashlib,json,zipfile,re,sys
def inventory(root,lock,expected_rows):
 hashes=set(re.findall(r'--hash=sha256:([0-9a-f]{64})',lock.read_text()))
 wheels=sorted(root.glob('*.whl'));assert len(wheels)==29 and len(hashes)==29
 expected={x['filename']:x for x in expected_rows};assert len(expected_rows)==len(expected)==29
 assert {p.name for p in wheels}==set(expected)
 assert len({x['sha256'] for x in expected_rows})==29 and {x['sha256'] for x in expected_rows}==hashes
 actual=set();result=[];largest=None;total=0
 for p in wheels:
  h=hashlib.sha256()
  with p.open('rb') as f:
   for b in iter(lambda:f.read(65536),b''):h.update(b)
  digest=h.hexdigest();assert digest in hashes and digest not in actual;actual.add(digest)
  assert p.stat().st_size==expected[p.name]['bytes'] and digest==expected[p.name]['sha256']
  with zipfile.ZipFile(p) as z:
   seen=set()
   for m in z.infolist():
    q=pathlib.PurePosixPath(m.filename);assert not q.is_absolute() and '..' not in q.parts and '\\' not in m.filename and m.filename not in seen and len(m.filename)<=512 and '\x00' not in m.filename;seen.add(m.filename)
    assert not m.flag_bits&1 and m.file_size<=268435456
    total+=m.file_size;assert total<=536870912
    if not m.is_dir() and (largest is None or m.file_size>largest['bytes']):
     u=hashlib.sha256()
     with z.open(m) as f:
      for b in iter(lambda:f.read(65536),b''):u.update(b)
     largest={'wheel':p.name,'member':m.filename,'bytes':m.file_size,'uncompressed_sha256':u.hexdigest()}
  result.append({'wheel':p.name,'bytes':p.stat().st_size,'sha256':h.hexdigest()})
 assert largest is not None and actual==hashes and len(actual)==29
 return {'schema':'READONLY_WHEEL_INVENTORY112_V1','wheels':result,'largest_member':largest,'total_uncompressed':total,'fits_64MiB_regular_ceiling':largest['bytes']<=67108864,'imports':0,'extracts':0,'install':0}
if __name__=='__main__':
 print(json.dumps(inventory(pathlib.Path(sys.argv[1]),pathlib.Path(sys.argv[2]),json.loads(pathlib.Path(sys.argv[3]).read_text())['wheels']),sort_keys=True))

