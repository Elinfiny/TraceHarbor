"""Portable SOURCE171 qualification only. No native constructor, registry,
provider call, key, crypto operation or counter. All ports below are explicit
neutral fixtures. Run from any extracted archive, with --evidence DIR.
"""
import argparse,ast,base64,copy,hashlib,importlib.util,json,pathlib,runpy,tempfile,time,types,traceback
D=pathlib.Path(__file__).resolve().parent
can=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode();sha=lambda b:hashlib.sha256(b).hexdigest()
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
N=load('QUALIFICATION171_ONLY_NO_BOOTSTRAP',D/'native127.py');G=N.g;B=N.b170;W=G.w171;I=load('QUALIFICATION171_INGRESS_NO_CRYPTO',D.parent/'offline103/ingress.py')
rows=[];budgets=[]
def check(name,fn):
 fn();rows.append({'case':name,'status':'PASS','realm':'NEUTRAL_QUALIFICATION_NOT_LIVE_PROOF'})
def refuses(fn):
 try:fn()
 except (ValueError,KeyError,TypeError,UnicodeError,TimeoutError,RuntimeError,AssertionError,PermissionError):return
 raise AssertionError('Required refusal absent')
def ctx():return {'repository':'Elinfiny/TraceHarbor','repository_id':1391430317,'actor_id':273768139,'run_id':77,'attempt':1,'source_sha':'f'*40,'nonce':'7'*32,'certificate_sha256':'6'*64,'expires_utc':int(time.time())+840}
def metadata():return {'artifact_digest':'4'*64,'artifact_bytes':123,'retention_days':1,'custody_sha256':'5'*64}
def paired(raw,phase,provider=None):
 oid=B.oid(raw);now=int(time.time()*1000);context={'domain':'EXPLICIT_NEUTRAL_QUALIFICATION171_NOT_AUTHORITY','source_sha':'f'*40}
 req={'schema':'TRACE118_HOST_REQUEST','seq':2,'context':context,'op':'github_fetch','args':{'url':'https://api.github.com/repos/Elinfiny/TraceHarbor/git/blobs/'+oid},'issued_utc_ms':now,'deadline_utc_ms':now+15000,'inventory_call_id':phase+'/blob/proof','inventory_sha256':'f'*64};req['request_digest']=sha(can(req))
 original=copy.deepcopy(provider)if provider is not None else {'isError':False,'structuredContent':{'content':raw.decode('utf-8')}}
 ret={'schema':'TRACE118_HOST_RETURN','seq':2,'context':context,'op':'github_fetch','request_digest':req['request_digest'],'original_result':{'schema':'TRACE152_AUTHENTIC_READ_PAIR','value':original,'current':{'qualification_current':True},'native_authority':False},'transport_error':None,'late':False}
 created={'identity':{'context_sha256':sha(can(context)),'operation':'github_create_blob','seq':1,'tool':'github_create_blob','call_id':'c'*64},'original':{'isError':False,'structuredContent':{'sha':oid}}};return [req,ret,created,{'oid':oid,'bytes':len(raw),'sha256':sha(raw)},B.PAIRS[phase],now]
def native_consumer(raw,phase,macro,provider=None):
 req,ret,created,pins,active,now=paired(raw,phase,provider);before=can(ret)
 with tempfile.TemporaryDirectory(prefix='qualification171_only_')as home:
  root=pathlib.Path(home);(root/'2.request.original.json').write_bytes(can(req));(root/'2.return.original.json').write_bytes(can(ret));cp=root/'create.json';cp.write_bytes(can(created));ref={'identity':created['identity'],'path':str(cp),'bytes':len(can(created)),'sha256':sha(can(created))};macro.originals={phase+'/blob':{'canonical':ref,'value':{'sha':pins['oid']}}};macro.active={'name':active}
  port=types.SimpleNamespace(ledger=types.SimpleNamespace(root=root,seq=2),config={'capture_directory':str(root)},macro=macro,canonical127=types.SimpleNamespace(io=types.SimpleNamespace(read=lambda p:pathlib.Path(p).read_bytes())))
  port.verify_reference=lambda r:N.NativePort127.verify_reference(port,r);refresh=[];port.refresh_authority152=lambda current,scope,**kw:refresh.append((current,scope));port.bridge=lambda op,args:N.normalizer127(ret['original_result'],op)
  proof=N.NativePort127.invoke(port,req['inventory_call_id'],'github_fetch',req['args']);assert G.b170.verify170(proof,raw) and can(ret)==before and json.loads((root/'2.return.original.json').read_bytes())==ret and len(refresh)==1
  budgets.append({'phase':phase,'raw':len(raw),'request':len(can(req)),'original_return':len(can(ret)),'canonical':len(can({'identity':created['identity'],'original':ret['original_result']})),'derived_projection':len(can(proof))});return proof
class ChainFixture171:
 """Unbound real Grouped127 body/plan/chain; every effect is local fixture."""
 def __init__(self,c,delivery):
  self.delivery=delivery;self.clock=types.SimpleNamespace(wall=time.time);self.context={'source_sha':c['source_sha'],'expires_utc':c['expires_utc'],'source_tree':'b'*40,'nonce':'9'*64,'baseline_entries':[],'manifest_sha256':'a'*64,'once_receipt_sha256':'d'*64};self.parent_wall=c['expires_utc'];self.run={'id':c['run_id']};self.plan_sha='e'*64;self.phase_receipts={};self.proofs={};self.active=None;self.calls=[];self.originals={};self.port=types.SimpleNamespace(admit_descriptor=lambda:{'source_sha':c['source_sha'],'manifest_sha256':'a'*64,'once_receipt_sha256':'d'*64,'run_id':c['run_id'],'expires_utc':c['expires_utc'],'phase':'admit'},consumed_descriptor=lambda d:N.NativePort127.consumed_descriptor(self.port,d));self.port.macro=self
 body=G.Grouped127.body;chain_plan=G.Grouped127.chain_plan
 remaining=lambda self:10000
 guard=lambda self:None
 def begin(self,name,seconds):self.active={'name':name}
 def phase_intent(self,name,ops):self.intent=copy.deepcopy(ops)
 def semantic(self,*args):pass
 def close(self):self.active=None
 def call(self,id,op,args):
  self.calls.append((id,op,copy.deepcopy(args)));phase,kind,*proof=id.split('/');raw,name=self.body(phase)
  if not proof:
   return {'sha':B.oid(base64.b64decode(args['content'],validate=True))}if kind=='blob'else {'sha':('b'if kind=='tree'else'c')*40}if kind!='ref'else {'branch':self.intent[3]['ref']}
  if kind=='blob':return native_consumer(raw,phase,self)
  if kind=='tree':return {'sha':'b'*40,'truncated':False,'tree':[{'path':name,'mode':'100644','type':'blob','sha':B.oid(raw)}]}
  if kind=='commit':return {'sha':'c'*40,'author':{'id':G.OWNER},'committer':{'id':G.OWNER},'parents':[{'sha':self.context['source_sha']}],'commit':{'tree':{'sha':'b'*40}}}
  return {'ref':'refs/heads/'+self.intent[3]['ref'],'object':{'type':'commit','sha':'c'*40}}
def runner(wire,c,expected_der,expected_pins,mutate=None):
 oid=B.oid(wire);name='traceharbor-encrypted104-'+c['nonce']+'.cms';commit='c'*40;ref='refs/heads/traceharbor-encrypted104-'+c['nonce'];calls=[];seen=[]
 def api(path,**kw):
  calls.append(path)
  if '/git/ref/'in path:return {'ref':ref,'object':{'type':'commit','sha':commit}}
  if path.endswith('/git/commits/'+commit):return {'parents':[{'sha':c['source_sha']}],'tree':{'sha':'d'*40}}
  if path.endswith('/git/commits/'+c['source_sha']):return {'tree':{'sha':'e'*40}}
  if path.endswith('/git/trees/'+'e'*40):return {'truncated':False,'tree':[]}
  if path.endswith('/git/trees/'+'d'*40):return {'truncated':False,'tree':[{'path':name,'mode':'100644','type':'blob','sha':oid}]}
  if path.endswith('/git/blobs/'+oid):
   blob={'encoding':'base64','size':len(wire),'content':base64.b64encode(wire).decode()}
   if mutate:mutate(blob)
   return blob
  raise AssertionError(path)
 def consumer(out,context,key,cert,der,pins):
  seen.append('EXPLICIT_FIXTURE_DER_CONSUMER_NOT_DECRYPT');assert der==expected_der and context==c and pins==expected_pins;return {'fixture_DER_pins_verified':True}
 oldapi,olddecrypt=I.api,I.decrypt;I.api,I.decrypt=api,consumer
 try:result,receipt=I.receive(c,'NO_REAL_KEY','NO_REAL_CERT',expected_pins,pathlib.Path('NOT_CREATED'),wait_seconds=1);assert len(seen)==1;return receipt
 finally:I.api,I.decrypt=oldapi,olddecrypt;runner.last_consumers=len(seen)
def e2e(der):
 c=ctx();plan=I.transport(c,der,'b'*40);delivery=W.delivery171(plan,metadata(),time.time());port=types.SimpleNamespace(source=c['source_sha'],run_id=c['run_id'],macro=types.SimpleNamespace(context={'expires_utc':c['expires_utc']}),recipient_context171=c);N.NativePort127.validate_delivery(port,delivery);m=ChainFixture171(c,delivery)
 for phase in ('admit','encrypted','consumed'):G.Grouped127.chain(m,phase)
 raw,_=m.body('encrypted');assert raw==base64.b64decode(plan['operations'][0]['body']['content']) and W.decode171(raw,c,time.time())==der
 receipt=runner(raw,c,der,[{'qualification_only':'NO_PRIVATE_PINS'}]);consumed=N.NativePort127.consumed_descriptor(m.port,delivery);assert consumed['ciphertext_receipt']==receipt and m.proofs['encrypted']['blob']==W.oid(raw)
 # Same consumed receipt hash used by unchanged actual SAFE projection plan.
 m.context.update(source_parent='a'*40,workflow_path='FIXTURE',workflow_step_names=[],full_tree_entries=[],cost_scope_sha256='8'*64);m.port.config={'ui_dispatch127':{'kind':'EXPLICIT_QUALIFICATION_ONLY'}};m.port.run_id=c['run_id'];pp=N.NativePort127.provider_plan(m.port);assert pp['projection_context']['custody_binding_sha256']==sha(can(receipt));assert len(m.calls)==24

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--evidence',type=pathlib.Path,required=True);ap.add_argument('--output',type=pathlib.Path,required=True);a=ap.parse_args();E=a.evidence.resolve();P=json.loads((E/'prospective152.json').read_bytes());c=ctx();der=b'neutral CMS-shaped DATA ONLY\x00\xff\x80\n\r\n';wire=W.encode171(der,c,time.time())
 for i,raw in enumerate([b'\x00\xff\x80\n',der,bytes(range(256))*4]):check('full_actual_source_consumers_neutral_binary_'+str(i),lambda raw=raw:e2e(raw))
 limit=W.der_limit171(c,time.time());check('exact_DER_boundary_roundtrip',lambda:e2e(b'\x80'*limit));check('DER_boundary_plus1_refused_before_create',lambda:refuses(lambda:I.transport(c,b'\x80'*(limit+1),'b'*40)))
 for n in [0,1,2,3,limit-1,limit,limit+1,131072]:assert W.wire_size171(c,n)==len(W.can(W.envelope171(c,n,'f'*64,'A'*(4*((n+2)//3)))))
 check('exact_header_dependent_closed_size_formula',lambda:None)
 bad=[];d=json.loads(wire)
 for key,val in [('schema','OLD_DER'),('der_bytes',len(der)-1),('der_bytes',True),('der_sha256','0'*64),('der_base64',base64.b64encode(der).decode()+'\n'),('der_base64','AB==')]:
  q=copy.deepcopy(d);q[key]=val;bad.append((key+str(val)[:12],can(q)))
 for key in c:
  q=copy.deepcopy(d);q['context'][key]=('WRONG'if type(c[key])is str else c[key]+1);bad.append(('context_'+key,can(q)))
 q=copy.deepcopy(d);q['context']['attempt']=True;bad.append(('boolean_attempt_not_integer',can(q)))
 bad.extend([('schema_missing',can({k:v for k,v in d.items()if k!='schema'})),('duplicatekeys',wire[:-1]+b',"schema":"'+W.SCHEMA.encode()+b'"}'),('noncanonicalJSON',b' '+wire),('trailingbytes',wire+b'{}'),('truncated',wire[:-2]),('nonUTF8',b'\xff'+wire),('raw_old_DER_no_fallback',der),('wire_oversize',b'X'*131073)])
 for name,raw in bad:
  check('decode_'+name,lambda raw=raw:refuses(lambda:W.decode171(raw,c,time.time())))
  def reject_runner(raw=raw):
   refuses(lambda:runner(raw,c,der,[]));assert runner.last_consumers==0
  check('runner_rejects_before_DER_consumer_'+name,reject_runner)
 check('expiry_exact_now_refused',lambda:refuses(lambda:W.decode171(wire,c,c['expires_utc'])))
 check('zero_DER_underflow_refused',lambda:refuses(lambda:W.encode171(b'',c,time.time())))
 q=copy.deepcopy(d);q.update(der_bytes=1,der_sha256=sha(b'\x00'),der_base64='AB==');check('noncanonical_base64_padbits_refused',lambda:refuses(lambda:W.decode171(can(q),c,time.time())))
 check('nonfinite_clock_refused',lambda:refuses(lambda:W.decode171(wire,c,float('nan'))))
 for key in ['ciphertext_base64','ciphertext_bytes','ciphertext_sha256','wire_sha256','wire_bytes','wire_gitblob','transport_schema','wire_base64','artifact_digest','artifact_bytes','retention_days','custody_sha256']:
  p=I.transport(c,der,'b'*40);delivery=W.delivery171(p,metadata(),time.time());delivery[key]=0 if type(delivery[key])is int else 'CORRUPTED';check('delivery_pin_'+key,lambda delivery=delivery:refuses(lambda:W.delivery_wire171(delivery,time.time())))
 for field in c:
  port=types.SimpleNamespace(source=c['source_sha'],run_id=c['run_id'],macro=types.SimpleNamespace(context={'expires_utc':c['expires_utc']}),recipient_context171=copy.deepcopy(c));delivery=W.delivery171(I.transport(c,der,'b'*40),metadata(),time.time());delivery['context']=copy.deepcopy(c);delivery['context'][field]='MISMATCH';check('actual_NativePort_recipient_binding_'+field,lambda port=port,delivery=delivery:refuses(lambda:N.NativePort127.validate_delivery(port,delivery)))
 for key,val in [('size',0),('encoding','utf8'),('content','bad*')]:check('runner_provider_'+key,lambda key=key,val=val:refuses(lambda:runner(wire,c,der,[],lambda b:b.update({key:val}))))
 # Changed-wire cases on the same original request-bound source consumer.
 changes=[('OID',lambda f:f[2]['original']['structuredContent'].update(sha='0'*40)),('repo',lambda f:f[0]['args'].update(url=f[0]['args']['url'].replace('Elinfiny','Other'))),('path',lambda f:f[0]['args'].update(url=f[0]['args']['url'].replace('/git/blobs/','/contents/'))),('requestseq',lambda f:f[1].update(seq=3)),('originalcreate_seq',lambda f:f[2]['identity'].update(seq=0)),('wirehash',lambda f:f[3].update(sha256='0'*64)),('wirecount',lambda f:f[3].update(bytes=1)),('404error',lambda f:f[1]['original_result']['value'].update(isError=True)),('late',lambda f:f[1].update(late=True)),('UNKNOWN',lambda f:f[1].update(transport_error={'status':'UNKNOWN_NO_RETRY'})),('truncated',lambda f:f[1]['original_result']['value']['structuredContent'].update(content=wire[:-2].decode()))]
 for phase in B.PAIRS:
  for name,change in changes:
   f=paired(wire,phase);change(f);check('requestbound_wire_'+phase+'_'+name,lambda f=f:refuses(lambda:B.read170(*f)))
 # Reuse two genuine originals without another provider GET; binding is fixture.
 for name in ['real607-blob-original.json','new-fetchblob-contract-first-original.json']:
  original=json.loads((E/name).read_bytes());original=original.get('result',original);raw=original['structuredContent']['content'].encode();macro=types.SimpleNamespace(body=lambda _:(raw,'EXPLICIT_FIXTURE'))
  check('genuine_original_readonly_'+name,lambda raw=raw,original=original,macro=macro:native_consumer(raw,'admit',macro,original))
 plan=runpy.run_path(str(D/'plan127.py'));check('whole_DATA_ONLY_acyclic_release133',lambda:plan['release133'](P['direction'],P['static_CONFIG'],(D/'manifest.json').read_bytes(),P['preloaded']['inventory']))
 fn=next(x for x in ast.parse((D/'native127.py').read_bytes()).body if isinstance(x,ast.FunctionDef)and x.name=='bootstrap127');i=next(i for i,n in enumerate(fn.body)if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='markers'for t in n.targets));pure=compile(ast.Module(body=fn.body[i:i+2],type_ignores=[]),'EXACT_SOURCE_MARKER_PREDICATE_ONLY','exec');pred=lambda d:exec(pure,{'direction':d,'static':P['static_CONFIG']});check('all4_markers_positive',lambda:pred(P['direction']))
 for marker in ast.literal_eval(fn.body[i].value):
  q=copy.deepcopy(P['direction']);q['body']=q['body'].replace(marker,'REMOVED');check('missing_'+marker,lambda q=q:refuses(lambda:pred(q)))
 q=copy.deepcopy(P['direction']);q['body']+=q['grouped146_admission']['static_config_sha256'];q['bytes']=len(q['body'].encode());q['sha256']=sha(q['body'].encode());check('G_bodycycle_refused',lambda:refuses(lambda:plan['release133'](q,P['static_CONFIG'],(D/'manifest.json').read_bytes())))
 check('explicit_historical104_only',lambda:W.historical_der104(der,len(der),sha(der),history_version=104));check('historical_not_171_fallback',lambda:refuses(lambda:W.historical_der104(der,len(der),sha(der),history_version=171)))
 # Exact unchanged caller literal predicate and unbound writer recipe, no factory.
 text=(D/'caller127.mjs').read_text();start=text.index(' const code=`')+len(' const code=`');end=text.index('`;',start);literal=text[start:end];assert '${'not in literal;tree=ast.parse(literal.replace('\\n','\n'));guard=next(n for n in ast.walk(tree)if isinstance(n,ast.Assert)and 'ADMIT_TRACE146_STATIC_TYPED_RUNTIME_V3'in ast.unparse(n));code=compile(ast.Module(body=[guard],type_ignores=[]),'CALLER_LITERAL_ONLY','exec')
 def caller(body,contract):exec(code,{'ad':{'contract':contract},'d':{'fixture':{'direction':{'body':body}}},'k':'fixture'})
 check('exact_caller_literal_positive',lambda:caller(P['direction']['body'],'TRACE146_STATIC_TYPED_RUNTIME_V3'));check('exact_caller_marker_negative',lambda:refuses(lambda:caller('REMOVED','TRACE146_STATIC_TYPED_RUNTIME_V3')));check('exact_caller_contract_negative',lambda:refuses(lambda:caller(P['direction']['body'],'WRONG')))
 h=runpy.run_path(str(D/'prestart168.py'));original=P['writer_preview']['full_original_source_utf8'];assert sha(original.encode())==h['ORIGINAL']
 for unbound in [None,0]:check('writer_unbound_actual_A_'+str(unbound),lambda unbound=unbound:refuses(lambda:h['derive152'](original,unbound)))
 assert P['runtime_bindings']=={'A':None,'B':None,'C':None,'T':None,'M':None,'runtime_CONFIG':None}
 assert all(x['request']<262144 and x['original_return']<1048576 and x['canonical']<2097152 and x['derived_projection']<1048576 for x in budgets)
 out={'status':'PASS','target':'SOURCE171_NEW_COMPLETE_PORTABLE_QUALIFICATION','cases':len(rows),'rows':rows,'boundary':{'actual_context':c,'exact_DER_max':limit,'wire_at_max':W.wire_size171(c,limit),'wire_at_DER_plus1':W.wire_size171(c,limit+1),'MAX_RAW':131072},'frame_sizes_measured':budgets,'native_provider_counter_crypto_private_keys':0,'old_Q_reruns':0,'live_proof':False};a.output.write_bytes(can(out));print(json.dumps({'status':'PASS','cases':len(rows),'DER_max':limit,'wire_max':W.wire_size171(c,limit)}))
if __name__=='__main__':main()
