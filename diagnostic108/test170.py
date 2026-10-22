"""NEW170 bounded read-only qualification. Never native authority or live chain.
Source NativePort.invoke is used unbound on an explicitly fake qualification
port, with neutral request/return fixtures retained before pure parsing.
"""
from pathlib import Path
import json,copy,hashlib,base64,types,importlib.util,sys,tempfile,time,ast,runpy,traceback
D=Path(__file__).resolve().parent;W=Path(sys.argv[1]).resolve();can=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode();sha=lambda b:hashlib.sha256(b).hexdigest()
spec=importlib.util.spec_from_file_location('QUALIFICATION170_NO_NATIVE_BOOTSTRAP',D/'native127.py');N=importlib.util.module_from_spec(spec);spec.loader.exec_module(N);B=N.b170
rows=[]
def test(name,fn):
 fn();rows.append({'case':name,'status':'PASS','scope':'READONLY_QUALIFICATION_ONLY_NOT_NATIVE_PROOF'})
def refuses(fn):
 try:fn()
 except (ValueError,TypeError,KeyError,UnicodeError,PermissionError):return
 raise AssertionError('Strict refusal required')
def fixture(raw,phase='admit',rest=False,provider=None):
 oid=B.oid(raw);now=int(time.time()*1000);context={'domain':'EXPLICIT_QUALIFICATION_ONLY_NO_NATIVE','source_sha':'f'*40,'fixture':'170'}
 req={'schema':'TRACE118_HOST_REQUEST','seq':2,'context':context,'op':'github_fetch','args':{'url':'https://api.github.com/repos/Elinfiny/TraceHarbor/git/blobs/'+oid},'issued_utc_ms':now,'deadline_utc_ms':now+15000,'phase_deadline_utc_ms':now+15000,'inventory_call_id':phase+'/blob/proof','inventory_sha256':'f'*64};req['request_digest']=sha(can(req))
 original=copy.deepcopy(provider)if provider is not None else {'isError':False,'structuredContent':{'sha':oid,'size':len(raw),'encoding':'base64','content':base64.b64encode(raw).decode()}if rest else {'content':raw.decode('utf-8')}}
 pair={'schema':'TRACE152_AUTHENTIC_READ_PAIR','value':original,'current':{'qualification_current':True},'native_authority':False};ret={'schema':'TRACE118_HOST_RETURN','seq':2,'context':context,'op':'github_fetch','request_digest':req['request_digest'],'original_result':pair,'transport_error':None,'late':False}
 create={'identity':{'context_sha256':sha(can(context)),'operation':'github_create_blob','seq':1,'tool':'github_create_blob','call_id':'c'*64},'original':{'isError':False,'structuredContent':{'sha':oid}}};pins={'oid':oid,'bytes':len(raw),'sha256':sha(raw)};return req,ret,create,pins,B.PAIRS[phase],now

def consume(f,raw):
 req,ret,created,pins,phase,now=f;before=can(ret);decoded=B.read170(*f);assert can(ret)==before;assert N.g.b170.verify170(decoded,raw);return decoded

def actual_consumer(raw,phase,rest=False,provider=None):
 f=fixture(raw,phase,rest,provider);req,ret,created,pins,active,now=f
 with tempfile.TemporaryDirectory(prefix='qualification170_')as home:
  root=Path(home);(root/'2.request.original.json').write_bytes(can(req));(root/'2.return.original.json').write_bytes(can(ret));cp=root/'created.canonical.json';cp.write_bytes(can(created));ref={'identity':created['identity'],'path':str(cp),'bytes':cp.stat().st_size,'sha256':sha(cp.read_bytes())};p=types.SimpleNamespace(ledger=types.SimpleNamespace(root=root,seq=2),config={'capture_directory':str(root)},macro=types.SimpleNamespace(originals={phase+'/blob':{'canonical':ref,'value':{'sha':pins['oid']}}},body=lambda _: (raw,'qualification-only'),active={'name':active}),canonical127=types.SimpleNamespace(io=types.SimpleNamespace(read=lambda path:Path(path).read_bytes())))
  p.verify_reference=lambda r:N.NativePort127.verify_reference(p,r);refresh=[];p.refresh_authority152=lambda current,scope,**kw:refresh.append((current,scope));p.bridge=lambda op,args:N.normalizer127(ret['original_result'],op)
  result=N.NativePort127.invoke(p,req['inventory_call_id'],'github_fetch',req['args']);assert N.g.b170.verify170(result,raw);assert refresh==[(ret['original_result']['current'],req['inventory_call_id'])];assert json.loads((root/'2.return.original.json').read_bytes())==ret;assert p.current_original['frame']==ret
for phase in B.PAIRS:
 for raw,kind in [(b'{  "neutral": 1 }\n','JSON'),(b'neutral nonJSON \xc8\x9b\n\n','UTF8')]:test('actual_unbound_NativePort_to_integrated_wholeblob_'+phase+'_'+kind,lambda raw=raw,phase=phase:actual_consumer(raw,phase))
 test('actual_unbound_REST_base64_'+phase,lambda phase=phase:actual_consumer(b'neutral REST\n',phase,True))
# Immutable real607 original, strictly READONLY replay with fixture binding.
real=json.loads((W/'real607-blob-original.json').read_bytes());provider=real.get('result',real);raw=provider['structuredContent']['content'].encode();test('real607_manifest_full_exact_UTF8_readonly_replay',lambda:actual_consumer(raw,'admit',provider=provider))
test('raw_JSON_that_looks_like_REST_is_not_reserialized',lambda:consume(fixture(b'{"sha":"looks REST","encoding":"base64","content":"QQ==","size":1}\n'),b'{"sha":"looks REST","encoding":"base64","content":"QQ==","size":1}\n'))
test('legitimate_explicit_REST_binary_lossless_not_raw_UTF8_guess',lambda:consume(fixture(b'\x00\xff\x80\n',rest=True),b'\x00\xff\x80\n'))
raw=b'{  "neutral": 2 }\n'
def negative(name,change):
 f=list(fixture(raw));change(f);refuses(lambda:B.read170(*f));test(name,lambda:None)
negative('modified_URL_OID',lambda f:f[0]['args'].update(url=f[0]['args']['url'][:-1]+'0'))
negative('wrong_repository',lambda f:f[0]['args'].update(url=f[0]['args']['url'].replace('Elinfiny/TraceHarbor','Other/Other')))
negative('wrong_path',lambda f:f[0]['args'].update(url=f[0]['args']['url'].replace('/git/blobs/','/contents/')))
negative('modified_request_digest',lambda f:f[0].update(request_digest='0'*64))
negative('modified_call_id',lambda f:f[0].update(inventory_call_id='admit/blob/other'))
negative('modified_return_request_id',lambda f:f[1].update(request_digest='0'*64))
negative('modified_return_seq',lambda f:f[1].update(seq=3))
negative('modified_create_seq',lambda f:f[2]['identity'].update(seq=0))
negative('modified_create_context',lambda f:f[2]['identity'].update(context_sha256='0'*64))
negative('modified_expected_OID',lambda f:f[3].update(oid='0'*40))
negative('modified_expected_count',lambda f:f[3].update(bytes=1))
negative('modified_expected_SHA256',lambda f:f[3].update(sha256='0'*64))
negative('missing_required_independent_binding',lambda f:f.__setitem__(3,None))
negative('wrong_active_phase',lambda f:f.__setitem__(4,'CONSUMED_CHAIN'))
negative('modified_create_original_SHA',lambda f:f[2]['original']['structuredContent'].update(sha='0'*40))
negative('tool_error',lambda f:f[1]['original_result']['value'].update(isError=True))
negative('tool_exception',lambda f:f[1]['original_result']['value'].update(tool_throw={'message':'EXPLICIT_FIXTURE'}))
negative('late_return',lambda f:f[1].update(late=True))
negative('transport_UNKNOWN',lambda f:f[1].update(transport_error={'status':'UNKNOWN_NO_RETRY'}))
negative('expired_original15',lambda f:f.__setitem__(5,f[5]+15000))
negative('missing_raw',lambda f:f[1]['original_result']['value']['structuredContent'].clear())
negative('truncated_raw',lambda f:f[1]['original_result']['value']['structuredContent'].update(content=raw[:-1].decode()))
negative('JSON_reserialization_rejected',lambda f:f[1]['original_result']['value']['structuredContent'].update(content=json.dumps(json.loads(raw))))
negative('raw_binary_instead_of_UTF8_string',lambda f:f[1]['original_result']['value']['structuredContent'].update(content=b'\xff'))
negative('invalid_UTF8_surrogate',lambda f:f[1]['original_result']['value']['structuredContent'].update(content='\ud800'))
for key,val in [('sha','0'*40),('size',1),('encoding','utf-8'),('content','*not-base64*')]:
 f=list(fixture(raw,rest=True));f[1]['original_result']['value']['structuredContent'][key]=val;test('bad_REST_'+key,lambda f=f:refuses(lambda:B.read170(*f)))
for kind,content in [('github_create_blob',{'sha':'a'*40}),('github_create_tree',{'sha':'b'*40}),('github_create_commit',{'sha':'c'*40}),('github_create_ref',{'branch':'qualification-only'}),('library_materialize',{'transfers':[{'file_id':'fixture'}]})]:
 original={'isError':False,'structuredContent':content};test('unchanged_normalizer_'+kind,lambda original=original,kind=kind,content=content:(_ for _ in ()).throw(AssertionError())if N.normalizer127(original,kind)!=(content['transfers'][0]if kind=='library_materialize'else content)else None)
for phase,data in [('tree',{'sha':'b'*40,'tree':[],'truncated':False}),('commit',{'sha':'c'*40,'parents':[]}),('ref',{'ref':'refs/heads/fixture','object':{'sha':'d'*40}})]:
 original={'isError':False,'structuredContent':{'content':json.dumps(data)}};test('unchanged_fetch_'+phase,lambda original=original,data=data:(_ for _ in ()).throw(AssertionError())if N.normalizer127(original,'github_fetch')!=data else None)
# Actual future DATA_ONLY packet: no runtime factory or registry is invoked.
P=json.loads((W/'prospective152.json').read_bytes());cfg=P['static_CONFIG'];direction=P['direction'];mb=(D/'manifest.json').read_bytes();plan=runpy.run_path(str(D/'plan127.py'));test('complete_source170_packet_release133',lambda:plan['release133'](direction,cfg,mb,P['preloaded']['inventory']))
fn=next(x for x in ast.parse((D/'native127.py').read_bytes()).body if isinstance(x,ast.FunctionDef)and x.name=='bootstrap127');i=next(i for i,n in enumerate(fn.body)if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='markers'for t in n.targets));pure=compile(ast.Module(body=fn.body[i:i+2],type_ignores=[]),str(D/'native127.py'),'exec')
def marker_pred(d,c):exec(pure,{'direction':d,'static':c})
test('all_four_actual_source_bootstrap_markers_positive',lambda:marker_pred(direction,cfg))
for marker in ast.literal_eval(fn.body[i].value):
 q=copy.deepcopy(direction);q['body']=q['body'].replace(marker,'REMOVED_FOR_NEGATIVE');test('missing_'+marker,lambda q=q:refuses(lambda:marker_pred(q,cfg)))
q=copy.deepcopy(cfg);q['cost_scope']['host_cost_bound']=1;test('host_cost_nonzero_refused',lambda:refuses(lambda:marker_pred(direction,q)))
q=copy.deepcopy(direction);q['body']+=' '+q['grouped146_admission']['static_config_sha256'];q['bytes']=len(q['body'].encode());q['sha256']=sha(q['body'].encode());test('computed_G_cycle_refused',lambda:refuses(lambda:plan['release133'](q,cfg,mb)))
q=copy.deepcopy(cfg);q['authority_projection_sha256']='0'*64;test('unbound_projection_refused',lambda:refuses(lambda:plan['release133'](direction,q,mb)))
assert (D/'caller127.mjs').read_bytes()==(W.parent/'intake20261022_wake42/source168-exact/diagnostic108/caller127.mjs').read_bytes();assert 'ADMIT_TRACE146_STATIC_TYPED_RUNTIME_V3'in direction['body'];test('unchanged_caller_literal_guard_satisfied',lambda:None)
# No effect route or retry exists in this pure adapter, even after repeated errors.
source=(D/'blob170.py').read_text();assert not any(s in source for s in ['subprocess','urlopen','exec_command','mcp__','time.sleep','requests.']);test('UNKNOWN_has_no_effect_or_retry_surface',lambda:None)
out={'target':'SOURCE170_NEW_RELEVANT_QUALIFICATION_ONLY','status':'PASS','cases':len(rows),'rows':rows,'live_native_proof':False,'old_Q_reruns':0,'GitWRITE_model_crypto_holder_registry':0};(W/'Q170-first-original.json').write_bytes(can(out));print(json.dumps({'status':out['status'],'cases':len(rows),'scope':'READONLY_QUALIFICATION_NOT_NATIVE_PROOF'}))
