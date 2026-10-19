// PRIVATE inactive provider controller. Exact source is preloaded before any
// future clock. Import performs no operation and grants no native authority.
const CONTROLS126=new WeakMap();
const canonical126=v=>v===null||typeof v!=='object'?JSON.stringify(v):Array.isArray(v)?'['+v.map(canonical126).join(',')+']':'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical126(v[k])).join(',')+'}';
function reserve126(c,kind,id){if(c.firstUnknown||c.calls.length>=48||c.calls.some(x=>x.id===id))throw Error('Inclusive cap/firstUNKNOWN/no replay');const t={kind,id};c.calls.push(t);return t;}
export function prepareControl126(plan){
 if(!Number.isSafeInteger(plan.wholePlanInclusiveCalls)||plan.wholePlanInclusiveCalls>48||!Number.isSafeInteger(plan.observerMaximum)||plan.observerMaximum<0||plan.observerMaximum>6)throw Error('Prospective complete inclusive48 plan');
 const handle=Object.freeze({realm:'PRIVATE_SOURCE_ONLY_NO_NATIVE_AUTHORITY'}),c={plan:JSON.parse(JSON.stringify(plan)),calls:[],observers:[],usedObservers:new Set(),firstUnknown:null,nextSeq:1,artifactId:null,fileRef:null};
 for(let i=0;i<plan.observerMaximum;i++)c.observers.push(reserve126(c,'wait','observer-'+i));
 CONTROLS126.set(handle,c);return handle;
}
export function takeWaitTicket126(handle,index){const c=CONTROLS126.get(handle);if(!c||c.firstUnknown||!Number.isInteger(index)||!c.observers[index]||c.usedObservers.has(index))throw Error('Every actual wait needs unique PRE-reserved ticket, never resendexec');c.usedObservers.add(index);return {...c.observers[index]};}
export function controlCounts126(handle){const c=CONTROLS126.get(handle);if(!c)throw Error('Exact source controller registry');return {reserved:c.calls.length,actual_observers:c.usedObservers.size,firstUnknown:c.firstUnknown,limit:48};}
export async function bridge126(frame,handle,tools){
 const c=CONTROLS126.get(handle);if(!c)throw Error('No supplied bool/getter/API as controller');const p=c.plan,a=frame.args,repo='Elinfiny/TraceHarbor';
 if(c.firstUnknown||canonical126(frame.context)!==canonical126(p.context)||frame.seq!==c.nextSeq||Date.now()>=Math.min(p.deadline_utc_ms,frame.deadline_utc_ms))throw Error('Exact source/context/order/originalclock');
 if(['github_fetch_workflow_run_jobs','github_fetch_workflow_run_artifacts'].includes(frame.op)&&(a.repo_full_name!==repo||a.run_id!==p.runId))throw Error('Selected SAME actualrun');
 if(frame.op==='github_fetch'&&!p.allowedFetchUrls.includes(a.url))throw Error('Fixed current source/run/commit/tree URLs');
 if(frame.op==='github_fetch_workflow_run_artifacts'&&a.name!=='traceharbor-safe126-'+p.runId+'-1')throw Error('Exact selectedartifact name');
 if(frame.op==='github_download_workflow_artifact'&&(a.repo_full_name!==repo||a.artifact_id!==c.artifactId||a.file_name!=='safe126.zip'))throw Error('Actual preceding selectedartifact');
 if(frame.op==='library_materialize'&&(!c.fileRef||canonical126(a)!==canonical126({items:[c.fileRef],destination:{directory:p.transferDirectory+'/safe-artifact-'+p.runId+'-1'}})))throw Error('Actual returnedfileid/selected disjointpath');
 const id=canonical126({context:frame.context,operation:frame.op,seq:frame.seq,tool:frame.op,call_id:frame.request_digest});
 // Reserve all original-retention/callback slots BEFORE invoking the primitive.
 // Unused slots after UNKNOWN are committed; they are never refunded/reset.
 if(c.calls.length+4>48)throw Error('No full original/closure reserve');
 reserve126(c,'native',id);reserve126(c,'local_evidence','original:'+id);reserve126(c,'native','callback:'+id);reserve126(c,'local_evidence','callback-original:'+id);
 let original=null,error=null;
 try{switch(frame.op){
  case 'github_fetch':original=await tools.mcp__codex_apps__github_fetch(a);break;
  case 'github_fetch_workflow_run_jobs':original=await tools.mcp__codex_apps__github_fetch_workflow_run_jobs(a);break;
  case 'github_fetch_workflow_run_artifacts':original=await tools.mcp__codex_apps__github_fetch_workflow_run_artifacts(a);break;
  case 'github_download_workflow_artifact':original=await tools.mcp__codex_apps__github_download_workflow_artifact(a);break;
  case 'library_materialize':original=await tools.mcp__codex_apps__library_prepare_materialize(a);break;
  default:throw Error('Closed existingprimitives, no arbitrarytool/HTTP/nativewrite');
 }}catch(e){error={name:e?.name||'Error',message:String(e?.message||e),status:'UNKNOWN_NO_RETRY'};}
 // Exactly one complete original per call before any parse/deadline postguard.
 const path=p.captureDirectory+'/'+frame.seq+'.canonical-native-original.json';
 try{await tools.apply_patch('*** Begin Patch\n*** Add File: '+path+'\n+'+JSON.stringify({identity:{context:frame.context,operation:frame.op,seq:frame.seq,tool:frame.op,call_id:frame.request_digest},original,error})+'\n*** End Patch');}catch(e){c.firstUnknown={capture_error:String(e?.message||e),original,error};throw e;}
 if(error||original?.isError||Date.now()>=Math.min(p.deadline_utc_ms,frame.deadline_utc_ms)){c.firstUnknown=error||{late_or_error:true};throw Error('Original retained; no followon');}
 if(frame.op==='github_fetch_workflow_run_artifacts'){
  const v=original.structuredContent;
  if(v.total_count!==1||v.artifacts?.length!==1||v.artifacts[0].name!=='traceharbor-safe126-'+p.runId+'-1'||v.artifacts[0].workflow_run?.id!==p.runId||v.artifacts[0].expired!==false){c.firstUnknown={wrongArtifact:true};throw Error('Wrong actualartifact');}
  c.artifactId=v.artifacts[0].id;
 }
 if(frame.op==='github_download_workflow_artifact'){
  const ref=original.structuredContent.file||original.structuredContent;
  if(typeof ref.file_id!=='string'||typeof ref.file_name!=='string'||ref.file_name.includes('/')||ref.file_name.includes('\\')){c.firstUnknown={badFileRef:true};throw Error('Exact native reusablefileref');}
  c.fileRef=Object.fromEntries(['library_file_id','file_id','file_name'].filter(k=>k in ref).map(k=>[k,ref[k]]));
 }
 let terminal;
 try{terminal=await tools.write_stdin({session_id:p.holderSession,chars:JSON.stringify({schema:'TRACE118_HOST_RETURN',seq:frame.seq,context:frame.context,op:frame.op,request_digest:frame.request_digest,original_result:original,transport_error:null,late:false})+'\n',yield_time_ms:1000,max_output_tokens:2000});}catch(e){terminal={tool_throw:{name:e?.name,message:String(e?.message||e)},status:'UNKNOWN_NO_RETRY'};c.firstUnknown=terminal;}
 await tools.apply_patch('*** Begin Patch\n*** Add File: '+p.captureDirectory+'/'+frame.seq+'.canonical-callback-original.json\n+'+JSON.stringify(terminal)+'\n*** End Patch');
 if(c.firstUnknown||Date.now()>=p.deadline_utc_ms){c.firstUnknown??={late_callback:true};throw Error('Callback original retained, no nextframe');}
 c.nextSeq++;return terminal;
}
