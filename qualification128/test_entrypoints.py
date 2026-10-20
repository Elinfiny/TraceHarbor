"""Four NEW128 cases: Python1/2/4, Node3. No old suite/runtime execution."""
import ast,contextlib,hashlib,importlib.util,io,json,os,pathlib,stat,sys,types,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1];D=ROOT/'diagnostic108'
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=load('qualification128_helper',D/'helper_channel128.py');e=load('qualification128_export',D/'export_boundary128.py')
can=h.can128;sha=h.sha128
def one(root):
 root.mkdir(mode=0o700);helper=pathlib.Path(sys.argv[3]).resolve();hp=sha(helper.read_bytes());assert hp==json.loads((ROOT/'qualification128/pins.json').read_bytes())['supported_helper_sha256']
 metadata=root/'new-public-metadata.json';body=can({'schema':'DISPOSABLE_PUBLIC_METADATA_FIXTURE128','native_authority':False});metadata.write_bytes(body);os.chmod(metadata,0o600)
 attrs=[{'name':'user.fixture-trace128','value':'PUBLIC_METADATA_ONLY'}];identity={'phase':'LOCAL_ADMIN_FIXTURE','run':'NEW_CASE1','source':hp,'call':'ONE_EXACT_SUPPORTED_HELPER128'};protocol=io.StringIO()
 saved={k:getattr(sys,k) for k in ('argv','stdin','stdout','stderr')}
 with contextlib.redirect_stdout(protocol):
  ref=h.run_helper128(helper,hp,metadata,'libfile_disposable_trace128_metadata',attrs,identity,lambda i,o:h.retain_private128(root,i,o))
  print(json.dumps({'schema':'TRACE128_FIXTURE_STRUCTURED_RESULT','helper_original':ref,'native_authority':False}))
 result=json.loads(protocol.getvalue());assert protocol.getvalue().count('\n')==1 and result['schema']=='TRACE128_FIXTURE_STRUCTURED_RESULT'
 record=json.loads(pathlib.Path(ref['path']).read_bytes())['original'];assert record['stdout']==str(metadata)+'\n' and record['stderr']=='' and record['returncode']==0 and record['native_return']=={'kind':'SystemExit','code':0} and record['exception'] is None and record['restoration_errors']==[]
 assert record['attempts']==1 and record['restoration_attempts']==list(saved)
 assert all(getattr(sys,k) is v for k,v in saved.items()) and metadata.read_bytes()==body and os.getxattr(metadata,'user.library-file-id').decode()=='libfile_disposable_trace128_metadata'
 for attr in attrs:assert os.getxattr(metadata,attr['name']).decode()==attr['value']
 # Exact source links, distinct from dynamically executing native preflight or holder.
 pre=ast.parse((D/'preflight127.py').read_bytes());native=ast.parse((D/'native127.py').read_bytes())
 for tree in (pre,native):assert any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='run_helper128' for n in ast.walk(tree))
 assert 'runpy.run_path' not in (D/'preflight127.py').read_text() and 'runpy.run_path' not in (D/'native127.py').read_text().split(' def artifact_bytes',1)[1].split(' def provider_artifact',1)[0]
 return {'case':1,'actual_supported_helper':'PASS','complete_streams_and_terminal':'PASS','ALL_fixture_attrs_and_whole_bytes':'PASS','structured_fixture_frame':'ONE_CLEAN_RECORD','actual_native_preflight_or_holder':'NOT_RUN','helper_original':ref}
def two(root):
 root.mkdir(mode=0o700);records=[];later=[]
 saved={k:getattr(sys,k) for k in ('argv','stdin','stdout','stderr')};cls=type(sys)
 fixtures=["import sys\nprint('first stdout')\nprint('first stderr',file=sys.stderr)\nraise ValueError('NEW128_FIRST_HELPER_FAILURE')\n", "import sys,types\nprint('restore fixture stdout')\nprint('restore fixture stderr',file=sys.stderr)\nclass Once128(types.ModuleType):\n def __setattr__(self,name,value):\n  if name=='stdout' and getattr(self,'_trace128_fail_once',False):\n   types.ModuleType.__setattr__(self,'_trace128_fail_once',False)\n   raise OSError('NEW128_RESTORE_FAILURE')\n  return types.ModuleType.__setattr__(self,name,value)\nsys.__class__=Once128\nsys._trace128_fail_once=True\n"]
 for index,code in enumerate(fixtures):
  fixture=root/('fixture-'+str(index)+'.py');fixture.write_text(code);identity={'phase':'EXPLICIT_SYNTHETIC_EXCEPTION_FIXTURE','run':'NEW_CASE2','source':sha(code.encode()),'call':'ONE_ATTEMPT_'+str(index)}
  def retain(i,o):
   ref=h.retain_private128(root,i,o);records.append(o);return ref
  refused=False
  try:h.run_helper128(fixture,sha(code.encode()),root/'unused','fixture128',[],identity,retain)
  except RuntimeError:refused=True
  finally:
   sys.__class__=cls
   for name,value in saved.items():setattr(sys,name,value)
   if hasattr(sys,'_trace128_fail_once'):delattr(sys,'_trace128_fail_once')
   later.append({'fixture':index,'cleanup':'SEPARATE_TEST_FIXTURE_RESTORATION','streams_restored':all(getattr(sys,k) is v for k,v in saved.items())})
  assert refused and len(records)==index+1 and records[-1]['attempts']==1
 assert records[0]['stdout']=='first stdout\n' and records[0]['stderr']=='first stderr\n' and records[0]['exception']['class']=='ValueError' and records[0]['restoration_errors']==[]
 assert records[1]['exception'] is None and records[1]['stdout']=='restore fixture stdout\n' and records[1]['stderr']=='restore fixture stderr\n' and len(records[1]['restoration_errors'])==1 and records[1]['restoration_errors'][0]['stream']=='stdout'
 assert all(r['restoration_attempts']==['argv','stdin','stdout','stderr'] for r in records) and all(x['streams_restored'] for x in later)
 (root/'separate-cleanup-original.json').write_bytes(can(later))
 return {'case':2,'complete_first_originals':len(records),'first_exception_and_later_restoration_errors':'SEPARATE_PASS','retained_cleanup':later,'helper_retry':0,'native_grant':0}
def four(root):
 root.mkdir(mode=0o700);old=pathlib.Path(sys.argv[3]);raw=old.read_bytes();assert len(raw)==126756 and sha(raw)=='3b8b16b13f378f0eaad38945a6ea2ab9517d45aecd17ac4b9e14b019c60154f9'
 with zipfile.ZipFile(io.BytesIO(raw)) as z:contents=json.loads(z.read('TraceHarbor127/CONTENTS.json'))
 reports={};changed=[];oldmap={x['relative_path']:dict(x) for x in contents['entries']};exact={'actual-ordinary-control/readback448-original.json','actual-ordinary-control/readback449-original.json'}
 assert len(oldmap)==len(contents['entries'])==94
 for row in contents['entries']:
  body=row['utf8'].encode();assert len(body)==row['size_bytes'] and sha(body)==row['sha256']
  if row['relative_path'] in exact:
   projected,report=e.project128(body);before=json.loads(body);after=json.loads(projected);before['structuredContent']['transfers'][0]['completion_token']=e.LABEL128;assert before==after
   row.update(utf8=projected.decode(),size_bytes=len(projected),sha256=sha(projected));reports[row['relative_path']]=report;changed.append(row['relative_path'])
 assert set(changed)==exact
 for row in contents['entries']:
  if row['relative_path'] not in exact:assert row==oldmap[row['relative_path']]
 source=[r for r in contents['entries'] if r['relative_path'].startswith('candidate/')];originals=[r for r in contents['entries'] if r['relative_path'].startswith('group127-1/')];assert len(originals)==24
 for row in source+originals:assert row==oldmap[row['relative_path']]
 e.scan128(contents)
 # New synthetic credential-shaped value is constructed only inside this
 # disposable test. It is never printed or exported, and grants no authority.
 refused=False
 try:e.scan128({'embedded':json.dumps({'nested':json.dumps({'completion_token':'NEW_SYNTHETIC128_'+'x'*32})})})
 except ValueError:refused=True
 assert refused and e.scan128({'source':'completion_token is a field name'})
 (root/'sanitized127-contents.json').write_bytes(can(contents));(root/'redacted-projections128.json').write_bytes(can(reports))
 return {'case':4,'exact_redactions':2,'all94_inner_counts_SHA':'PASS','all_source_and24_original_case_receipts':'BYTE_EXACT','embedded_encoded_fixture':'REFUSED','bare_field_name':'ALLOWED','raw_scope_expiry':'UNKNOWN','historical_version0':'OWNER_PRIVATE_RETAINED','new_runtime_authority':0,'sanitized_contents':{'bytes':len(can(contents)),'sha256':sha(can(contents))},'reports':reports}
if __name__=='__main__':
 case=int(sys.argv[1]);result={1:one,2:two,4:four}[case](pathlib.Path(sys.argv[2]).resolve());print(json.dumps(result,sort_keys=True,separators=(',',':')))
