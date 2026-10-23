"""SOURCE176 buffered canonical equivalence and refusal regression, pure data only."""
from pathlib import Path
import json,hashlib,sys,math,random,runpy,traceback,time,unittest.mock
ROOT=Path(__file__).resolve().parent
def qualify176(output):
 S=runpy.run_path(str(ROOT/'snapshot174.py'));canonical=S['canonical_sha173'];strict=runpy.run_path(str(ROOT/'host_transport118.py'))['strict'];rows=[]
 def check(name,fn):
  try:fn();r={'case':name,'status':'PASS'}
  except BaseException as e:r={'case':name,'status':'FAIL','exception':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()}
  rows.append(r);Path(output).write_text(json.dumps({'status':'RUNNING','rows':rows}));print(name,r['status'],flush=True)
 def equal(v):assert canonical(v)==hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()
 def refuses(fn):
  try:fn()
  except (ValueError,TypeError,UnicodeError,RecursionError):return
  raise AssertionError('Expected refusal')
 for v in (None,True,False,0,-1,2**63,2**4096,0.,-0.,1e-300,1e308,5e-324,1e20,1e-7,1.2345678901234567):check('scalar_'+repr(v)[:35],lambda v=v:equal(v))
 for n in (65535,65536,65537,131071,131072,131073):
  for s,label in [('x','ascii'),('ă😀\"\\\n\x00\u2028','unicode_escape')]:check('C_escape_boundary_'+label+'_'+str(n),lambda n=n,s=s:equal(s*n))
 rng=random.Random(176)
 def floats():
  import struct
  for _ in range(1000):
   v=struct.unpack('!d',rng.getrandbits(64).to_bytes(8,'big'))[0]
   if math.isfinite(v):equal(v)
 check('1000_finite_binary64_exact_exponents_minuszero',floats)
 check('sorted_unicode_keys_nested_scalars',lambda:equal({'😀':[False,None,{'ă':'\x00\t\r\b\f'}],'a':{},'\u0000':('x',1)}))
 alias=[{'x':[1,2]}];check('repeated_alias_serialized_each_occurrence_no_cache',lambda:equal([alias,alias,{'again':alias}]))
 for kind in (list,dict):
  v=[]if kind is list else{};v.append(v)if kind is list else v.update(self=v);check('cycle_'+kind.__name__+'_refused',lambda v=v:refuses(lambda:canonical(v)))
 for v in (float('nan'),float('inf'),float('-inf'),{1:'bad'},b'bytes',set(),object(),'\ud800','\udfff'):
  check('refuse_'+type(v).__name__+'_'+str(len(rows)),lambda v=v:refuses(lambda:canonical(v)))
 class Evil(str):
  def __str__(self):raise AssertionError('callback')
 class EvilDict(dict):
  def keys(self):raise AssertionError('callback')
 for v in (Evil('x'),EvilDict(x=1)):
  check('builtin_exact_type_no_subclass_callback_'+type(v).__name__,lambda v=v:refuses(lambda:canonical(v)))
 for raw in (b'{"x":1,"x":2}',b'{"x":NaN}',b'{"x":Infinity}',b'{"x":-Infinity}',b'{} trailing',b'{}{}',b'"\xff"'):
  check('strict_parser_invalid_'+str(len(rows)),lambda raw=raw:refuses(lambda:canonical(strict(raw))))
 def huge():
  old=sys.get_int_max_str_digits();sys.set_int_max_str_digits(0)
  try:equal(10**7000+176)
  finally:sys.set_int_max_str_digits(old)
 check('huge_7001digit_integer_with_same_runtime_policy',huge)
 def bounded():
  value={'x':['x'*131073,'😀\n'*131073,list(range(10000))]};reference=hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest();real=hashlib.sha256;calls=[]
  class Observed:
   def __init__(self):self.h=real()
   def update(self,b):assert 0<len(b)<=65536;calls.append(len(b));self.h.update(b)
   def hexdigest(self):return self.h.hexdigest()
  with unittest.mock.patch.object(hashlib,'sha256',Observed):result=canonical(value)
  assert result==reference and len(calls)<100 and max(calls)<=65536
 check('bounded_SHA65536_updates_buffered_not_per_token',bounded)
 def fastpath():
  value=[{'controls':'\x00'*500,'values':[1,True,None,-0.,'😀']}for _ in range(1000)];dump=json.dumps;reference=hashlib.sha256(dump(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest();calls=[]
  def observed(v,**kw):
   text=dump(v,**kw);length=len(text.encode('utf8'));assert length<=32768;calls.append(length);return text
  with unittest.mock.patch.object(json,'dumps',observed):actual=canonical(value)
  assert actual==reference and len(calls)>1 and max(calls)<=32768
 check('C_fastpath_only_proven32768B_subtrees_not_full_document',fastpath)
 out={'schema':'SOURCE176_CANONICAL_C_EMITTER_REGRESSIONS','status':'PASS'if all(x['status']=='PASS'for x in rows)else'FAIL','cases':len(rows),'rows':rows,'native_effects':0};Path(output).write_text(json.dumps(out));return out
if __name__=='__main__':
 out=qualify176(sys.argv[1]);print(json.dumps({'status':out['status'],'cases':out['cases']}));raise SystemExit(0 if out['status']=='PASS'else 1)
