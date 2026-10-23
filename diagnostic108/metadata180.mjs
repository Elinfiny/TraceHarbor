// Actual fixed source180 consumer. No registry/native grant at import.
const quote180=s=>"'"+String(s).replaceAll("'","'\\''")+"'";
const IDS180=['libfile_3ee8270f03d8819188e1de1f75c3d824','libfile_f87a6a307f70819194e0af0fa453afd1','libfile_6f69ae483b088191a1fffefca617bbd5','libfile_8377022600088191993dc06bfba93b7b'];
export function descriptor180(binding){
 if(!binding||binding.native_authority!==false||!['READ_ONLY','ADMIN_SOURCE','NATIVE_OUTER'].includes(binding.kind))throw Error('Closed current metadata consumer; no supplied grant');
 const wanted=binding.kind==='READ_ONLY'?['QUALIFICATION']:binding.kind==='ADMIN_SOURCE'?['ADMIN_CLOSURE']:['RX_START','TERMINAL'];
 if(!wanted.includes(binding.phase))throw Error('Distinct qualification/admin/native phases');
 for(const k of ['sourceRoot','captureDirectory','destination','helper'])if(typeof binding[k]!=='string'||!binding[k].startsWith('/')||binding[k].split('/').includes('..'))throw Error('Exact absolute current source/capture/helper paths');
 return {schema:'TRACE180_METADATA_CONSUMER_V1',kind:binding.kind,phase:binding.phase};
}
async function retain180(tools,path,value){return tools.apply_patch('*** Begin Patch\n*** Add File: '+path+'\n+'+JSON.stringify(value)+'\n*** End Patch');}
export function terminalText180(chunks){
 if(!Array.isArray(chunks)||!chunks.length)throw Error('Complete terminal process originals');
 let text='',session=null;const ids=new Set();
 for(let n=0;n<chunks.length;n++){
  const r=chunks[n];if(r.tool_throw||typeof r.output!=='string'||!r.chunk_id||ids.has(r.chunk_id))throw Error('Whole unique exec chunks, no prefix/tail success');ids.add(r.chunk_id);text+=r.output;
  if(n===0)session=r.session_id;
  else if(r.session_id!=null&&r.session_id!==session)throw Error('Same process only');
  if(n<chunks.length-1&&(r.exit_code!=null||r.session_id!==session))throw Error('No adopted/early terminal session');
 }
 const last=chunks.at(-1);if(last.exit_code!==0||last.session_id!=null||last.eof===false)throw Error('Actual terminal0 EOF required before dependent consumer');
 return text;
}
async function process180(tools,cmd,root,label,deadline,polls=12){
 let r;try{r=await tools.exec_command({cmd,yield_time_ms:1000,max_output_tokens:16000});}catch(e){r={tool_throw:{message:String(e)}};}
 const chunks=[r];await retain180(tools,root+'/'+label+'-exec0.original.json',r);const session=r.session_id;
 for(let n=0;r.exit_code==null&&!r.tool_throw&&n<polls;n++){
  if(r.session_id!==session||!Number.isInteger(session)||Date.now()>=deadline)throw Error('First process UNKNOWN/late; no retry');
  r=await tools.write_stdin({session_id:session,chars:'',yield_time_ms:1000,max_output_tokens:16000});chunks.push(r);await retain180(tools,root+'/'+label+'-poll'+n+'.original.json',r);
 }
 if(Date.now()>=deadline)throw Error('Original whole process deadline exceeded');
 return JSON.parse(terminalText180(chunks));
}
export async function readMetadata180(binding,tools){
 const consumer=descriptor180(binding),root=binding.captureDirectory;
 if(!binding.frame)throw Error('Original source-captured dual-clock frame required');
 const deadline=(binding.frame.ack_utc+25)*1000;
 if(consumer.kind==='READ_ONLY'&&binding.frame.kind!=='READ_ONLY_QUALIFICATION'||consumer.kind==='ADMIN_SOURCE'&&binding.frame.kind!=='ADMIN_SOURCE_CAS'||consumer.kind==='NATIVE_OUTER'&&binding.frame.kind!=='CAS_READBACK')throw Error('No native/admin clock schema substitution');
 const items=IDS180.map(id=>id===IDS180[0]&&binding.expected?{library_file_id:id,file_id:binding.expected.file_id,file_name:'TraceHarbor_V1_checkpoint.json'}:{library_file_id:id});
 const original=await tools.mcp__codex_apps__library_prepare_materialize({items,destination:{directory:binding.destination}});
 await retain180(tools,root+'/metadata180-four.original.json',original);
 // Every actual original is retained; official completion runs in the fixed driver.
 await retain180(tools,root+'/metadata180-expected.json',binding.expected);await retain180(tools,root+'/metadata180-frame.json',binding.frame);await retain180(tools,root+'/metadata180-consumer.json',consumer);
 const args=[binding.sourceRoot+'/diagnostic108/outer_complete180.py',root+'/metadata180-four.original.json',root+'/metadata180-expected.json',binding.candidate,root+'/metadata180-frame.json',root+'/metadata180-consumer.json',root+'/metadata180-result.json',binding.helper];
 const result=await process180(tools,'python '+args.map(quote180).join(' '),root,'metadata180-completion',deadline);
 if(result.schema!=='TRACE180_COMPLETE_CONSUMER_READBACK_V1'||!result.whole_candidate_equality||!result.all_FD_ancestor_last_consumer_seals||!result.official_helpers_all_FD_ancestor_last_seals||result.native_authority!==false)throw Error('Complete source180 metadata proof/completion required');
 return result;
}
export async function qualifyMetadata180(binding,tools){
 if(binding.kind!=='READ_ONLY'||binding.phase!=='QUALIFICATION'||binding.frame)throw Error('One source-owned qualification origin, no supplied reset');descriptor180(binding);
 const path=binding.captureDirectory+'/qualification-origin.json';
 const origin=await process180(tools,'python '+[binding.sourceRoot+'/diagnostic108/outer_complete180.py','origin',path].map(quote180).join(' '),binding.captureDirectory,'origin180',Date.now()+5000,2);
 return readMetadata180({...binding,frame:origin,candidate:'AUTO_CURRENT_DISTINCT_CANDIDATE'},tools);
}
export async function publishOuter180(binding,tools){
 const consumer=descriptor180(binding);if(consumer.kind!=='NATIVE_OUTER')throw Error('No generic/admin write through native outer source route');
 const root=binding.captureDirectory,started=Date.now();
 const original=await tools.mcp__codex_apps__library_prepare_materialize({items:IDS180.map(library_file_id=>({library_file_id})),destination:{directory:binding.prepublishDirectory}});
 await retain180(tools,root+'/outer180-prepublish.original.json',original);if(original.isError||Date.now()-started>=25000)throw Error('Prepublish actual appREAD/error; no write');
 const args=[binding.sourceRoot+'/diagnostic108/outer_publish180.py',root+'/outer180-prepublish.original.json',binding.phase==='TERMINAL'?'BUILD_SOURCE_TERMINAL':binding.candidate,binding.configPath,binding.phase,binding.phase==='TERMINAL'?'CURRENT_SOURCE_AFTER_HOLDER':String(binding.expectedVersion),root+'/outer180-publication.original.json'];
 const actual=await process180(tools,'python '+args.map(quote180).join(' '),root,'outer180-publish',Date.now()+50000);
 if(actual.schema!=='TRACE180_ACTUAL_OUTER_PUBLICATION_ORIGINAL'||actual.publication_verified_complete!==true||actual.original?.returncode!==0||actual.publication?.status!=='succeeded'||actual.publication.local_metadata_applied!==true)throw Error('Actual full official terminal ACK/completion original required, no tail shortcut');
 return readMetadata180({...binding,frame:actual.frame,expected:actual.expected,candidate:actual.candidate},tools);
}
