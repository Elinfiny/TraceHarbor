// SOURCE177 DATA-only outer RX/terminal verifier bridge. No publication, grant,
// native registry, nonce or retry. The caller retains the actual write ACK frame.
const q177=s=>"'"+String(s).replaceAll("'","'\\''")+"'";
export async function verifyOuterMetadata177(binding,tools){
 if(!binding||!['RX_START','TERMINAL','READ_ONLY_QUALIFICATION'].includes(binding.phase)||binding.native_authority!==false)throw Error('Closed metadata-only outer integration');
 const ids=['libfile_3ee8270f03d8819188e1de1f75c3d824','libfile_f87a6a307f70819194e0af0fa453afd1','libfile_6f69ae483b088191a1fffefca617bbd5','libfile_8377022600088191993dc06bfba93b7b'];
 const root=binding.captureDirectory,originalPath=root+'/outer177-four.original.json';
 const started=Date.now();
 const original=await tools.mcp__codex_apps__library_prepare_materialize({items:ids.map(id=>id===ids[0]?{library_file_id:id,file_id:binding.expected.file_id,file_name:'TraceHarbor_V1_checkpoint.json'}:{library_file_id:id}),destination:{directory:binding.destination}});
 const save=async(name,value)=>await tools.apply_patch('*** Begin Patch\n*** Add File: '+root+'/'+name+'\n+'+JSON.stringify(value)+'\n*** End Patch');
 await save('outer177-four.original.json',original);
 if(original.isError||Date.now()-started>=25000)throw Error('Actual appREAD25/error retained; no retry');
 await save('outer177-expected.json',binding.expected);await save('outer177-frame.json',binding.frame);
 const args=[binding.sourceRoot+'/diagnostic108/outer_complete177.py',originalPath,root+'/outer177-expected.json',binding.candidate,root+'/outer177-frame.json',root+'/outer177-final.json',binding.helper,binding.helperSha256];
 let r=await tools.exec_command({cmd:'python '+args.map(q177).join(' '),yield_time_ms:1000,max_output_tokens:12000});
 await save('outer177-exec0.original.json',r);
 for(let n=0;r.exit_code==null&&n<8;n++){
  if(!r.session_id||Date.now()>=binding.readbackDeadlineUtcMs)throw Error('Original readback window expired; first original retained');
  r=await tools.write_stdin({session_id:r.session_id,chars:'',yield_time_ms:1000,max_output_tokens:12000});await save('outer177-poll'+n+'.original.json',r);
 }
 if(r.exit_code!==0||r.session_id!=null||Date.now()>=binding.readbackDeadlineUtcMs)throw Error('Original full adapter failed/late; no write/read retry');
 return {schema:'TRACE177_AUTHENTIC_OUTER_EXEC_ORIGINAL',original:r,native_authority:false,retry:0};
}

export async function publishAndVerifyOuter177(binding,tools){
 if(!['RX_START','TERMINAL'].includes(binding.phase))throw Error('Exact future outer154 phase');
 const root=binding.captureDirectory;
 const appReadStart177=Date.now();
 const current=await tools.mcp__codex_apps__library_prepare_materialize({items:['libfile_3ee8270f03d8819188e1de1f75c3d824','libfile_f87a6a307f70819194e0af0fa453afd1','libfile_6f69ae483b088191a1fffefca617bbd5','libfile_8377022600088191993dc06bfba93b7b'].map(library_file_id=>({library_file_id})),destination:{directory:binding.prepublishDirectory}});
 await tools.apply_patch('*** Begin Patch\n*** Add File: '+root+'/outer177-prepublish.original.json\n+'+JSON.stringify(current)+'\n*** End Patch');
 if(current.isError||Date.now()-appReadStart177>=25000)throw Error('Actual current appREAD25/error retained before any write');
 // Completion and all authentic authority/source/history guards run in the
 // fixed source process. No externally supplied metadata clock can authorize it.
 const args=[binding.sourceRoot+'/diagnostic108/outer_publish177.py',root+'/outer177-prepublish.original.json',binding.candidate,binding.configPath,binding.phase,String(binding.expectedVersion),root+'/outer177-publication.original.json'];
 let r=await tools.exec_command({cmd:'python '+args.map(q177).join(' '),yield_time_ms:1000,max_output_tokens:12000});
 await tools.apply_patch('*** Begin Patch\n*** Add File: '+root+'/outer177-publication-exec0.original.json\n+'+JSON.stringify(r)+'\n*** End Patch');
 for(let n=0;r.exit_code==null&&n<12;n++){
  if(!r.session_id)throw Error('Publication UNKNOWN; no retry');r=await tools.write_stdin({session_id:r.session_id,chars:'',yield_time_ms:1000,max_output_tokens:12000});
  await tools.apply_patch('*** Begin Patch\n*** Add File: '+root+'/outer177-publication-poll'+n+'.original.json\n+'+JSON.stringify(r)+'\n*** End Patch');
 }
 if(r.exit_code!==0||r.session_id!=null)throw Error('Publication original failed/unknown; no second write');
 const actual=JSON.parse(r.output);
 return verifyOuterMetadata177({...binding,native_authority:false,frame:actual.frame,readbackDeadlineUtcMs:(actual.frame.ack_utc+25)*1000,expected:{...binding.expected,file_id:actual.publication.file_id,version:actual.publication.current_version_number}},tools);
}
