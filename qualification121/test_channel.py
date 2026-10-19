"""NEW121 only: disjoint layout, actual livePTY/prepared current writer,
and one necessary real administrative CAS/readback/SAMEholder closure.
Accepted120clock/error/output cases are referenced, never rerun.
"""
import pathlib,sys,json,hashlib,importlib.util,copy,os,io,contextlib,time,traceback
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('channel121host',ROOT/'diagnostic108/host_transport118.py');host=importlib.util.module_from_spec(spec);sys.modules[spec.name]=host;spec.loader.exec_module(host)
OUT=pathlib.Path(sys.argv[1]);OUT.mkdir(mode=0o700,exist_ok=True);CONFIG=pathlib.Path(sys.argv[3]);cfg=host.strict(CONFIG.read_bytes());H=pathlib.Path(cfg['output']);CAP=pathlib.Path(cfg['capture_directory'])
def expect(fn):
 try:fn()
 except (ValueError,host.HostUnknown):return
 raise AssertionError('Expected layout refusal absent')
def case1():
 binding=cfg['writer_binding'];roots=host.validate_transfer_layout(binding);actual=host.current_binding(cfg['current_checkpoint'],cfg['current_version'],cfg,True,host.strict(pathlib.Path(cfg['payload_path']).read_bytes()));assert actual['number']==121 and actual['key']=='native121'
 checked=[]
 # Only path/identity predicate fixtures. No synthetic authority/provider,
 # no smokeholder and no actual checkpoint publication in this case.
 for mode in ['overlap','wrong_inode','symlink']:
  b=copy.deepcopy(binding)
  if mode=='wrong_inode':b['transfer_layout']['transfer']['ino']+=1
  elif mode=='overlap':b['transfer_layout']['transfer']=dict(b['transfer_layout']['private'])
  else:
   link=OUT/'new-layout-symlink';link.symlink_to(roots['transfer'],target_is_directory=True);b['transfer_layout']['transfer']['path']=str(link)
  expect(lambda:host.validate_transfer_layout(b));checked.append(mode)
 marker=CAP/'preparation-metadata.json';assert marker.stat().st_mode&0o777==0o600 and json.loads(marker.read_text())['source'].startswith('actual native apply_patch')
 return {'actual_current121_binding':True,'disjoint_positively_identified_roots':True,'refusals':checked,'new_empty_capture_slots_keep0600':True,'smokeholder':0,'effects':0}
def case2():
 startup=host.strict((H/'startup.original.json').read_bytes());assert startup['isatty0'] is True and startup['isolated']==1 and startup['dont_write_bytecode']==1 and startup['source_sha256']==cfg['host_source_sha256'] and startup['config_sha256']==host.sha(CONFIG.read_bytes())
 v=cfg['current_version'];terminal=host.strict((H/f'writer-{v}.original.json').read_bytes());assert terminal['status']=='TERMINAL' and terminal['returncode']==0;receipt=host.strict(bytes.fromhex(terminal['stdout_hex']));payload=host.strict(pathlib.Path(cfg['payload_path']).read_bytes());target=pathlib.Path(receipt['candidate']);doc=host.validate_writer_output(cfg['current_checkpoint'],target,v,payload,receipt,cfg)
 transfer=host.strict((H/f'transfer-{v}.provenance.json').read_bytes());upload=pathlib.Path(transfer['upload_copy']);assert transfer['private_candidate']==str(target) and upload.read_bytes()==target.read_bytes() and transfer['sha256']==receipt['raw_sha256'] and transfer['bytes']==len(target.read_bytes())
 assert upload.is_relative_to(pathlib.Path(cfg['writer_binding']['transfer_layout']['transfer']['path'])) and not upload.is_relative_to(pathlib.Path(cfg['writer_binding']['binding_root']))
 old=host.strict(pathlib.Path(cfg['current_checkpoint']).read_bytes());assert old['native120']==doc['native120'] and old['native119']==doc['native119'];provenance=host.strict((H/f'writer-{v}.provenance.json').read_bytes());assert provenance['direction_number']==121 and provenance['current_namespace']=='native121' and provenance['actual_invoked_source_sha256']==cfg['writer_binding']['writer_sha256']
 host.validate_transfer_layout(cfg['writer_binding'],H)
 return {'actual_fd0_livePTY_before_writer':True,'direct_isolated_no_bytecode_cli':True,'actual_current121_writer_terminal':0,'private_output_and_disjoint_upload_copy_exact':True,'old120_119_immutable':True,'native_tool_effects':0,'writer_provenance':provenance,'startup':startup}
def case3():
 proof=host.strict((H/'genuine-proof.json').read_bytes());assert proof['result']=='PASS' and proof['seq']==2 and proof['context']==cfg['context'] and proof['transport_counts']['CAS']==proof['transport_counts']['materialize']==1
 originals=[]
 for seq,op in [(1,'library_replace'),(2,'library_materialize')]:
  req=host.strict((H/f'{seq}.request.original.json').read_bytes());ret=host.strict((H/f'{seq}.return.original.json').read_bytes());orig=host.strict((CAP/f'{seq}.native-tool-original.json').read_bytes());assert req['op']==ret['op']==op and req['request_digest']==ret['request_digest'] and ret['context']==cfg['context'] and ret['original_result']==orig['original_result'] and ret['late'] is False and orig['transport_error'] is None;originals.append(ret)
 terminal=host.strict((CAP/'2.same-holder-native-return.json').read_bytes());assert terminal['exit_code']==0
 receipt=proof['receipt'];assert receipt['version']==cfg['current_version']+1;pub=host.normalizer(originals[0]['original_result'],'library_replace');read=host.normalizer(originals[1]['original_result'],'library_materialize');assert pub['file_id']==read['file_id'] and pub['current_version_number']==read['current_version_number']==receipt['version'] and pub['xattrs']==read['xattrs']
 path=pathlib.Path(receipt['readback_path']);doc,raw=host.check_checkpoint(path,host.OWN,receipt['version'],receipt['sha256']);assert path==pathlib.Path(cfg['writer_binding']['transfer_layout']['transfer']['path'])/('own-readback-'+str(receipt['version']))/pub['file_name']
 for p in [path,pathlib.Path(receipt['private_candidate_path']),pathlib.Path(receipt['upload_copy_path'])]:
  assert p.read_bytes()==raw
  for a in pub['xattrs']:assert os.getxattr(p,a['name']).decode()==a['value']
 host.validate_transfer_layout(cfg['writer_binding'],H)
 for p in list(H.iterdir())+list(CAP.iterdir()):
  if p.is_file():assert p.stat().st_mode&0o777==0o600,p
 pin=host.strict((CAP/'source-pin.json').read_bytes());assert pin['exact_function_source_equal'] and pin['file_sha256']==host.sha((ROOT/'diagnostic108/host118.mjs').read_bytes())
 return {'NEW121_actual_necessary_publicationCAS':1,'actual_pinned_whole_self_ALLattrs':'PASS','same_holder_authentic_exit':0,'actual_version':receipt['version'],'disjoint_readback_no_protected_mode_change':True,'all_private_outputs_and_capture_files0600':True,'native_runtime_authority':False,'case120_6_status':'UNCHANGED_NOT_RUN'}
mode=sys.argv[2];cases=[(1,case1)] if mode=='--layout' else [(2,case2)] if mode=='--prepared' else [(3,case3)];results=[]
for n,fn in cases:
 out=io.StringIO();err=io.StringIO();value=None;exception=None;start=time.monotonic()
 with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
  try:value=fn()
  except BaseException as exc:exception=type(exc).__name__;traceback.print_exc()
 streams={'stdout':out.getvalue().encode(),'stderr':err.getvalue().encode()}
 for channel,raw in streams.items():host.put(OUT/f'case{n}.{channel}',raw)
 terminal={'case':n,'returncode':0 if exception is None else 1,'exception_class':exception,'elapsed_s':time.monotonic()-start,'streams':{k:{'bytes':len(v),'sha256':host.sha(v)} for k,v in streams.items()}};host.put(OUT/f'case{n}.terminal.json',host.can(terminal));host.put(OUT/f'case{n}.result.json',host.can(value));results.append(terminal);print(json.dumps({'NEW121case':n,'pass':exception is None,'exception_class':exception}),flush=True)
sys.exit(0 if all(x['returncode']==0 for x in results) else 1)
