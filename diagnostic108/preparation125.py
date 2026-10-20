"""CURRENT125 preparation and read-only integration, never launches a holder.

The two phase levels are intentionally different. Extract the exact immutable
host administrative payload branch for read-only validation, before any writer,
IPC or native tool is available. The host itself remains byte-identical.
"""
import ast,copy,hashlib,importlib.util,json,os,pathlib,re,stat,time,types
HOST_SHA='dbec3c2929f09511240924f00f10e2a1fea376a255a8f2790fe9e1a8ca0f671d'
def can(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(raw):return hashlib.sha256(raw).hexdigest()
def load_host125(path):
 path=pathlib.Path(path)
 if sha(path.read_bytes())!=HOST_SHA:raise ValueError('Exact unchanged reviewed host')
 s=importlib.util.spec_from_file_location('current125_readonly_host',path);h=importlib.util.module_from_spec(s);s.loader.exec_module(h);return h
def actual_payload_branch125(host,cfg,payload):
 """Execute only the exact actual pinned host payload IF/ELIF AST node.

 No writer, bridge, CAS or transport method is invoked. This is a projection of
 trusted fixed source, not evaluation of payload/tool-returned source code.
 """
 raw=pathlib.Path(host.__file__).read_bytes()
 if sha(raw)!=HOST_SHA:raise ValueError('Pinned actual branch source')
 module=ast.parse(raw);cls=next(n for n in module.body if isinstance(n,ast.ClassDef) and n.name=='HostTransport');method=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='_cas_checkpoint122_body')
 branch=next(n for n in method.body if isinstance(n,ast.If) and isinstance(n.test,ast.Compare) and ast.unparse(n.test)=="payload.get('phase') == 'PUBLISH_INTENT'")
 source=ast.get_source_segment(raw.decode(),branch)
 allowed_calls={'payload.get','sha','can','_bound_macro122','ValueError','set'}
 if any(ast.unparse(n.func) not in allowed_calls for n in ast.walk(branch) if isinstance(n,ast.Call)):raise ValueError('Read-only actual branch allowlist')
 body=ast.Module(body=[copy.deepcopy(branch)],type_ignores=[]);ast.fix_missing_locations(body)
 scope={'self':types.SimpleNamespace(config=cfg),'payload':copy.deepcopy(payload),'sha':host.sha,'can':host.can,'_bound_macro122':host._bound_macro122,'ValueError':ValueError,'set':set}
 exec(compile(body,str(host.__file__)+':actual-readonly-payload-branch','exec'),{'__builtins__':{}},scope)
 return {'actual_host_sha256':HOST_SHA,'actual_payload_branch_sha256':sha(source.encode()),'writer_calls':0,'native_tool_calls':0,'result':'PASS'}
def intent125(pins,source_proof_sha256):
 return {'schema':'TRACE125_NECESSARY_PRIVATE_REVIEW_SOURCE_PUBLICATION','phase':'PUBLISH_INTENT','operation':'SOURCE_FREEZE','source_sha':'ffcc7c5223c1232f5f4dd62b96b63287637ed6e7','frozen_candidate':copy.deepcopy(pins),'new3_preparation_casesPASS':True,'source_proof_sha256':source_proof_sha256,'native_q':False,'nativeSend':0,'counter_calls':0,'model_calls':0,'spend':0,'useful_outcome':'Record complete current125 preparation integration, retained qualified caller and concrete SAFE placement/phase receipt candidate for independent review'}
def assemble125(binding,received_version,current_sha,paths,intent,context,deadline_utc_ms):
 """Pure preparation entrypoint. None deadline is PREARM_DRAFT, not authority."""
 version=received_version+1
 prepared={'phase':'PUBLISH_INTENT','payload_sha256':sha(can(intent)),'source_sha':intent['source_sha'],'host_source_sha256':HOST_SHA,'writer_sha256':binding['writer_sha256'],'direction_id':binding['direction_id'],'context':copy.deepcopy(context),'expected_current_version':version,'deadline_utc_ms':deadline_utc_ms,'phase_s':180,'maximum_phase_s':180}
 freeze={'phase':'SOURCE_FREEZE','scope':'PREPARE_EXACT_ONE_NECESSARY125_SOURCE_PUBLICATION','prepared_operation':copy.deepcopy(prepared),'source_pins':copy.deepcopy(intent['frozen_candidate']),'new3PASS':True,'native_runtime':False}
 cfg={'direction_number':125,'domain':'NECESSARY_CURRENT125_SOURCE_FREEZE','context':copy.deepcopy(context),'source_sha':intent['source_sha'],'run_id':None,'host_source_sha256':HOST_SHA,'library_helper':paths['helper'],'library_helper_sha256':paths['helper_sha256'],'writer_binding':copy.deepcopy(binding),'output':paths['holder'],'capture_directory':paths['captures'],'current_checkpoint':paths['current'],'current_version':version,'current_sha256':current_sha,'phase_s':180,'deadline_utc_ms':deadline_utc_ms,'payload_path':paths['intent'],'payload_sha256':sha(can(intent)),'prepared_operation':copy.deepcopy(prepared)}
 bundle={'mode':'ADMIN125','frames':2,'actual_current_version':version,'next_version':version+1,'context':copy.deepcopy(context),'deadline_utc_ms':deadline_utc_ms,'capture_directory':paths['captures'],'source_tree':'2c16b29e2426ca6accfe68cece4ecb589b2b46be','own_library_file_id':'libfile_3ee8270f03d8819188e1de1f75c3d824','upload_path':paths['upload'],'readback_directory':paths['readback'],'writer_sha256':binding['writer_sha256'],'config_sha256':sha(can(cfg))}
 validate125(binding,received_version,cfg,intent,freeze,bundle)
 return {'config':cfg,'intent':copy.deepcopy(intent),'freeze':freeze,'bundle':bundle,'state':'PREARM_DRAFT' if deadline_utc_ms is None else 'FIXED180_PREPARED'}
def validate125(binding,received_version,cfg,intent,freeze,bundle):
 if intent.get('phase')!='PUBLISH_INTENT' or intent.get('operation')!='SOURCE_FREEZE' or freeze.get('phase')!='SOURCE_FREEZE':raise ValueError('Intent PUBLISH_INTENT, outer freeze SOURCE_FREEZE are separate levels')
 if any(intent.get(k) is not v for k,v in [('native_q',False)]) or any(type(intent.get(k)) is not int or intent[k]!=0 for k in ('nativeSend','counter_calls','model_calls','spend')):raise ValueError('Administrative native-null/counter0 only')
 if cfg['current_version']!=received_version+1 or bundle['actual_current_version']!=cfg['current_version'] or bundle['next_version']!=cfg['current_version']+1:raise ValueError('Actual received -> freeze -> target version links')
 p=cfg['prepared_operation'];context=cfg['context'];version=cfg['current_version'];root=pathlib.Path(binding['binding_root']);layout=binding['transfer_layout'];transfer=pathlib.Path(layout['transfer']['path']);holder=pathlib.Path(layout['holder_parent']['path'])
 if p!=freeze['prepared_operation'] or p['phase']!='PUBLISH_INTENT' or p['expected_current_version']!=version or cfg['payload_sha256']!=sha(can(intent)) or p['payload_sha256']!=sha(can(intent)) or bundle['config_sha256']!=sha(can(cfg)):raise ValueError('Exact computed whole payload/config hash/current version')
 if cfg['writer_binding']!=binding or binding['direction_number']!=125 or p['direction_id']!=binding['direction_id'] or context['direction_id']!=binding['direction_id'] or context['direction_sha256']!=binding['direction_sha256'] or p['writer_sha256']!=binding['writer_sha256']:raise ValueError('Fresh current125 body/writer binding')
 if context['direction_number']!=125 or context['domain']!='NECESSARY_CURRENT125_SOURCE_FREEZE' or context['run_id'] is not None or context['once_receipt_sha256'] is not None or bundle['context']!=context or p['context']!=context:raise ValueError('Exact current125 context/native-null')
 if cfg['domain']!=context['domain'] or cfg['direction_number']!=125 or cfg['run_id'] is not None or cfg['host_source_sha256']!=HOST_SHA or context['host_source_sha256']!=HOST_SHA or p['host_source_sha256']!=HOST_SHA or not re.fullmatch('[a-f0-9]{32}',context['nonce']):raise ValueError('Fixed actual source/domain/nonce')
 if cfg['source_sha']!=intent['source_sha'] or context['source_sha']!=intent['source_sha'] or p['source_sha']!=intent['source_sha'] or bundle['writer_sha256']!=binding['writer_sha256'] or bundle['frames']!=2 or bundle['mode']!='ADMIN125':raise ValueError('Closed source/payload/twoframes/admin mode')
 if any(p[k]!=180 for k in ('phase_s','maximum_phase_s')) or cfg['phase_s']!=180 or cfg['deadline_utc_ms']!=p['deadline_utc_ms'] or bundle['deadline_utc_ms']!=cfg['deadline_utc_ms']:raise ValueError('Same ORIGINAL180, no reset')
 expected={'current_checkpoint':str(transfer/f'ordinary-readback{version}/TraceHarbor_V1_checkpoint.json'),'payload_path':str(root/'intent125.json'),'output':str(holder/'holder'),'capture_directory':str(holder/'captures'),'library_helper':str(root/'helpers/library_file_transfer.py')}
 if any(cfg[k]!=v for k,v in expected.items()) or bundle['upload_path']!=str(transfer/f'own-upload-{version}/TraceHarbor_V1_checkpoint.json') or bundle['readback_directory']!=str(transfer/f'own-readback-{version+1}') or bundle['capture_directory']!=str(holder/'captures'):raise ValueError('Exact distinct actual current private/transfer/holder paths')
 return {'result':'PASS','scope':'READONLY_PREPARATION_NOT_NATIVE_AUTHORITY','received_version':received_version,'prepared_version':version,'target_version':version+1,'payload_sha256':sha(can(intent)),'config_sha256':sha(can(cfg))}
def verify_current125(config_path,preloaded):
 """Genuine CURRENT post-freeze check; no original writer/tool/holder/CAS."""
 config_path=pathlib.Path(config_path);cfg=json.loads(config_path.read_bytes());host=load_host125(pathlib.Path(__file__).with_name('host_transport118.py'));intent=host.strict(pathlib.Path(cfg['payload_path']).read_bytes());current=host.current_binding(cfg['current_checkpoint'],cfg['current_version'],cfg,require_plan=True,payload=intent)
 record=current['doc']['native125']['records'][-1]
 if record['phase']!='PUBLISH_INTENT':raise ValueError('Actual owned freeze record phase')
 shape=validate125(cfg['writer_binding'],cfg['current_version']-1,cfg,intent,record['payload'],preloaded['bundle']);branch=actual_payload_branch125(host,cfg,intent);host.validate_transfer_layout(cfg['writer_binding'],cfg['output'])
 deadline=cfg['deadline_utc_ms']
 if not time.time()*1000<deadline:raise TimeoutError('Original180 alreadyexpired; no launch')
 root=pathlib.Path(cfg['writer_binding']['binding_root']);candidate=root/f"candidate{cfg['current_version']+1}/TraceHarbor_V1_checkpoint.json"
 absent=[candidate,pathlib.Path(preloaded['bundle']['upload_path']).parent,pathlib.Path(preloaded['bundle']['readback_directory']),pathlib.Path(cfg['output'])]
 if any(p.exists() or p.is_symlink() for p in absent):raise ValueError('No adoption of old candidate/transfer/readback/holder')
 if len({str(p) for p in absent})!=4:raise ValueError('Distinct original output paths')
 captures=pathlib.Path(cfg['capture_directory']);cs=captures.lstat()
 if captures.is_symlink() or stat.S_IMODE(cs.st_mode)!=0o700:raise ValueError('Fresh protected captures0700')
 for p in captures.iterdir():
  if p.is_symlink() or not p.is_file() or stat.S_IMODE(p.stat().st_mode)!=0o600 or p.stat().st_uid!=os.getuid():raise ValueError('Preallocated captures0600')
 return {'result':'PASS','scope':'ACTUAL_CURRENT125_READONLY_PRELAUNCH_INTEGRATION','actual_binding':'PASS','whole_preimage_sha256':sha(current['raw']),'shape':shape,'actual_branch':branch,'distinct_absent_paths':[str(p) for p in absent],'current_version':cfg['current_version'],'remaining_original180_ms':deadline-int(time.time()*1000),'writer_calls':0,'native_tool_calls':0}
