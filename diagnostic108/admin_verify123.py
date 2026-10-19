"""Closed actual123 pre-effect/readback guard. Read-only; no tool dispatch.
Invoked from the already-preloaded SAME native control cell, not frame code.
"""
import pathlib,json,hashlib,os,sys,importlib.util
def verify(config_path,seq):
 config_path=pathlib.Path(config_path);cfg=json.loads(config_path.read_bytes());root=pathlib.Path(cfg['output']);private=pathlib.Path(cfg['writer_binding']['binding_root']);host=pathlib.Path(__file__).with_name('host_transport118.py')
 sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
 if seq not in (1,2) or cfg['domain']!='NECESSARY_CURRENT123_SOURCE_FREEZE' or cfg['direction_number']!=123 or cfg['current_version']!=437 or sha(host.read_bytes())!=cfg['host_source_sha256']:raise ValueError('Exact123 current source/admin scope')
 spec=importlib.util.spec_from_file_location('actual123_guarded_host',host);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
 payload=h.strict(pathlib.Path(cfg['payload_path']).read_bytes());binding=h.current_binding(cfg['current_checkpoint'],437,cfg,require_plan=True,payload=payload);h.validate_transfer_layout(binding['binding'],root)
 startup=h.strict((root/'startup.original.json').read_bytes())
 if not startup['isatty0'] or startup['isolated']!=1 or startup['dont_write_bytecode']!=1 or startup['source_sha256']!=cfg['host_source_sha256'] or startup['config_sha256']!=sha(config_path.read_bytes()):raise ValueError('Actual directPTY/source/config before writer')
 frame=h.strict((root/(str(seq)+'.request.original.json')).read_bytes());without=dict(frame);del without['request_digest']
 if sha(can(without))!=frame['request_digest'] or frame['seq']!=seq or frame['context']!=cfg['context'] or frame['deadline_utc_ms']>cfg['deadline_utc_ms']:raise ValueError('Actual original frame digest/context/clock')
 terminal=h.strict((root/'writer-437.original.json').read_bytes());receipt=h.strict(bytes.fromhex(terminal['stdout_hex']));target=private/'candidate438/TraceHarbor_V1_checkpoint.json';upload=pathlib.Path(binding['binding']['transfer_layout']['transfer']['path'])/'own-upload-437/TraceHarbor_V1_checkpoint.json'
 if terminal['status']!='TERMINAL' or terminal['returncode']!=0 or terminal['stderr_hex'] or target.read_bytes()!=upload.read_bytes():raise ValueError('Actual writer terminal and identical original/upload output')
 h.validate_writer_output(cfg['current_checkpoint'],target,437,payload,receipt,cfg)
 provenance=h.strict((root/'writer-437.provenance.json').read_bytes());expected_command=[sys.executable,str(private/'admin123.py'),'build',cfg['current_checkpoint'],'437','PUBLISH_INTENT',str(root/'writer-437.payload.json')]
 # interpreter path can be the same executable through the original python3
 # alias; compare resolved executable identity, not a protocol/PID assertion.
 command=provenance['command']
 if pathlib.Path(command[0]).resolve()!=pathlib.Path(expected_command[0]).resolve() or command[1:]!=expected_command[1:] or provenance['actual_invoked_source_sha256']!=binding['binding']['writer_sha256'] or provenance['preimage_sha256']!=cfg['current_sha256'] or provenance['candidate_sha256']!=receipt['raw_sha256']:raise ValueError('Exact current original producer invocation/preimage/output')
 if seq==1:
  if frame['op']!='library_replace' or frame['args']['file']!=str(upload) or frame['args']['expected_current_version']!=437:raise ValueError('Exact actual CAS intent')
 else:
  cap=pathlib.Path(cfg['capture_directory']);native=h.strict((cap/'1.native-tool-original.json').read_bytes());pub=native['original_result']['structuredContent']
  if native['transport_error'] is not None or pub['status']!='succeeded' or pub['current_version_number']!=438 or pub['library_file_id']!=h.OWN:raise ValueError('Actual preceding native CAS original')
  expected={'items':[{'library_file_id':h.OWN,'file_id':pub['file_id'],'file_name':pub['file_name']}],'destination':{'directory':str(pathlib.Path(binding['binding']['transfer_layout']['transfer']['path'])/'own-readback-438')}}
  if frame['op']!='library_materialize' or frame['args']!=expected:raise ValueError('Actual returned file pinned readback only')
 return {'scope':'ACTUAL_ADMIN123_GUARD','seq':seq,'request_digest':frame['request_digest'],'context':cfg['context'],'config_sha256':sha(config_path.read_bytes()),'current_writer_sha256':binding['binding']['writer_sha256'],'whole_original_output_sha256':receipt['raw_sha256'],'native_authority':False}
if __name__=='__main__':print(json.dumps(verify(sys.argv[1],int(sys.argv[2])),sort_keys=True,separators=(',',':')))
