"""Only NEW43: 4 methods /12 scenarios, no suite42 replay or network."""
import base64,copy,json,os,socket,unittest
from pathlib import Path
from unittest.mock import patch
import native27_validator42 as v
import native27_controller42 as c
import native27 as writer
CASES=[]
def frame(e):
 b=v.canonical(e);h=v.digest(b).encode();return v.BEGIN+str(len(b)).encode()+b' '+h+b'\n'+b+b'\n'+v.END+h+b'\n'
def fixture():
 b={'repository_id':v.RID,'owner_id':v.OWNER,'source':'d'*40,'workflow_sha256':'4'*64,'driver_sha256':v.digest(Path(writer.__file__).read_bytes()),'validator_sha256':v.digest(Path(v.__file__).read_bytes()),'workflow_id':4301,'first_run_id':4302,'attempt':1,'nonce':v.NONCE,'ref':v.REF,'commit':'e'*40,'tree':'f'*40}
 url='https://api.github.com'+v.BASE;person={'name':'Synthetic Public','email':'public@example.invalid','date':'2026-10-16T00:00:00Z'}
 commit={'sha':b['commit'],'node_id':'SYNTHETIC_COMMIT','url':url+'/git/commits/'+b['commit'],'html_url':'https://github.com/'+v.REPO+'/commit/'+b['commit'],'author':person,'committer':person,'tree':{'sha':b['tree'],'url':url+'/git/trees/'+b['tree']},'parents':[{'sha':b['source'],'url':url+'/git/commits/'+b['source'],'html_url':'https://github.com/'+v.REPO+'/commit/'+b['source']}],'message':v.canonical(v.manifest(b)).decode(),'verification':{'verified':False,'reason':'unsigned','signature':None,'payload':None,'verified_at':None}}
 tree={'sha':b['tree'],'url':url+'/git/trees/'+b['tree'],'tree':[{'path':'public.txt','mode':'100644','type':'blob','sha':'9'*40,'size':12,'url':url+'/git/blobs/'+'9'*40}],'truncated':False}
 ref={'ref':v.REF,'node_id':'SYNTHETIC_REF','url':url+'/git/refs/tags/traceharbor-once-qualification17/canary','object':{'type':'commit','sha':b['commit'],'url':url+'/git/commits/'+b['commit']}}
 bodies=[{'message':'Not Found','documentation_url':'https://docs.github.com/rest/git/refs#get-a-reference','status':'404'},commit,commit,tree,ref,ref,commit,tree];writer.PUBLIC42=v.Producer()
 with patch.dict(os.environ,{'Q27_PHASE':'first'},clear=True):
  for (m,path,status),obj in zip(v.expected(b),bodies):writer.capture42(m,path[len(v.BASE):],status,(json.dumps(obj,indent=1)+'\n').encode())
 log=writer.PUBLIC42.frame(b,lambda _:None)
 run={'id':4302,'run_attempt':1,'repository_id':v.RID,'owner_id':v.OWNER,'actor_id':v.OWNER,'triggering_actor_id':v.OWNER,'event':'workflow_dispatch','head_branch':'main','head_sha':b['source'],'workflow_id':4301,'path':v.WORKFLOW,'status':'in_progress','conclusion':None,'run_started_at':'2026-10-16T00:00:00Z'}
 job={'id':4310,'run_id':4302,'attempt':1,'head_sha':b['source'],'status':'completed','conclusion':'success'};vj={**job,'id':4311}
 obs={'main':b['source'],'workflow_sha256':b['workflow_sha256'],'driver_sha256':b['driver_sha256'],'validator_sha256':b['validator_sha256'],'commit':b['commit'],'tree':b['tree'],'ref_commit':b['commit'],'nonce_state':'FIRST_APPLIED_VERIFIED','second_attempt_consumed':False,'unknown_effect':False}
 return b,log,run,job,vj,obs,v.timestamp(run['run_started_at'])+27
ORIGIN={'classification':'SYNTHETIC_ONLY','hosts':['logs.example.invalid']}
class Correction43(unittest.TestCase):
 def case(self,n):CASES.append(n);return self.subTest(name=n)
 def test_1_contextual_schemas(self):
  for kind in ['valid_new_full_forms','ref_email','nested_sha_email_unknown','size_bool']:
   with self.case('1_'+kind):
    f=fixture();e=v.parse(f[1].splitlines()[1],v.ENVELOPE_MAX)
    if kind=='valid_new_full_forms':
     self.assertEqual(v.decode_frame(f[1])[0]['bindings'],f[0]);self.assertTrue(base64.b64decode(e['records'][1]['body_b64']).endswith(b'\n'));continue
    r=e['records'][4 if kind=='ref_email' else 1 if kind=='nested_sha_email_unknown' else 3];body=v.parse(base64.b64decode(r['body_b64']),v.RECORD_MAX)
    if kind=='ref_email':body['email']='public@example.invalid'
    if kind=='nested_sha_email_unknown':body['author'].update(sha='0'*40,unexpected='public');body['tree']['email']='public@example.invalid'
    if kind=='size_bool':body['tree'][0]['size']=True
    raw=v.canonical(body);r.update(body_b64=base64.b64encode(raw).decode(),count=len(raw),sha256=v.digest(raw))
    with self.assertRaises(v.Refuse):v.decode_frame(frame(e))
 def test_2_api_throw(self):
  for cls in [RuntimeError,OSError,v.Refuse]:
   with self.case('2_'+cls.__name__):
    s=v.Sticky();err=cls('SYNTHETIC_PRIVATE_EXCEPTION');cleanup=OSError('SYNTHETIC_CLEANUP');s.cleanup_errors.append(cleanup);calls=[]
    def api(path):calls.append('api');raise err
    def down(*a,**k):calls.append('download');raise AssertionError('NO_DOWNLOAD')
    with self.assertRaises(v.Refuse):v.fetch_job_log(api,down,4310,state=s,origin_contract=ORIGIN,synthetic_cap=v.SYNTHETIC_CAP)
    self.assertEqual(calls,['api']);self.assertEqual(s.first_unknown,'API_CALLBACK_EXCEPTION');self.assertTrue(any(x[-1] is err for x in s.originals));self.assertIs(s.cleanup_errors[0],cleanup);self.assertNotIn(str(err),s.first_unknown)
 def test_3_download_throw(self):
  for cls in [RuntimeError,OSError,v.Refuse]:
   with self.case('3_'+cls.__name__):
    s=v.Sticky();err=cls('SYNTHETIC_PRIVATE_DOWNLOAD');calls=[];ret=(302,{'Location':'https://logs.example.invalid/ephemeral'},b'')
    def api(path):calls.append('api');return ret
    def down(url,headers):self.assertEqual(headers,{});calls.append('download');raise err
    with self.assertRaises(v.Refuse):v.fetch_job_log(api,down,4310,state=s,origin_contract=ORIGIN,synthetic_cap=v.SYNTHETIC_CAP)
    self.assertEqual(calls,['api','download']);self.assertEqual(s.first_unknown,'DOWNLOAD_CALLBACK_EXCEPTION');self.assertIs(s.originals[0][1],ret);self.assertTrue(any(x[-1] is err for x in s.originals))
 def test_4_no_next_and_end_to_end(self):
  with self.case('4_original_UNKNOWN_no_next_controller_refuses'):
   s=v.Sticky();s.first_unknown='ORIGINAL_UNKNOWN';calls=[];f=fixture()
   def deny(*a,**k):calls.append('FORBIDDEN');raise RuntimeError('NO_NEXT')
   with self.assertRaises(v.Refuse):v.fetch_job_log(deny,deny,4310,state=s,origin_contract=ORIGIN,synthetic_cap=v.SYNTHETIC_CAP)
   with self.assertRaises(v.Refuse):c.conditional_second(f[1],{},f[2],f[3],f[4],f[5],f[6],4303,state=s)
   self.assertEqual(calls,[]);self.assertEqual(s.first_unknown,'ORIGINAL_UNKNOWN')
  with self.case('4_new_export_transport_validate_controller'):
   b,log,run,job,vj,obs,now=fixture();state=v.Sticky();wire=b'2026-10-16T00:00:01Z setup\n'+b''.join(b'2026-10-16T00:00:02.123Z '+x+b'\n' for x in log.splitlines())
   def api(path):return 302,{'Location':'https://logs.example.invalid/public'},b''
   def down(url,headers):self.assertEqual(headers,{});return 200,{'Content-Length':str(len(wire))},wire
   actual=v.fetch_job_log(api,down,4310,state=state,origin_contract=ORIGIN,synthetic_cap=v.SYNTHETIC_CAP);receipt=v.validate(actual,run,job,obs,now,state=state);self.assertEqual(receipt['verdict'],'PASS');run['status']='completed';run['conclusion']='success'
   grant={'classification':'EXPLICIT_SYNTHETIC_ONLY','bindings':b,'receipt_sha256':v.digest(v.canonical(receipt)),'second_run_id':4303};desc=c.conditional_second(actual,receipt,run,job,vj,obs,now,4303,state=state,grant=grant,synthetic_cap=v.SYNTHETIC_CAP)
   self.assertFalse(desc['live_authority']);self.assertFalse(desc['dispatch_performed']);self.assertIsNone(c.EXTERNAL_ADMISSION_GATE)
   projection=v.canonical({'classification':'ACTUAL43_SYNTHETIC_PUBLIC_NOT_NATIVE','framed_log':actual.decode(),'receipt':receipt,'descriptor':desc});self.assertLessEqual(len(projection),32768);Path(os.environ['TRACE43_PROJECTION']).write_bytes(projection)
if __name__=='__main__':
 with patch.object(socket,'socket',side_effect=AssertionError('NETWORK_FORBIDDEN43')):result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Correction43))
 print(json.dumps({'classification':'NEW43_ONLY_INERT_NOT_NATIVE','methods':result.testsRun,'subcases':len(CASES),'case_names':CASES,'failures':len(result.failures),'errors':len(result.errors),'HTTP':0,'dispatch':0,'model':0,'nativeAdmission':None,'PLAN':None},sort_keys=True));raise SystemExit(0 if result.wasSuccessful() and result.testsRun==4 and len(CASES)==12 else 1)
