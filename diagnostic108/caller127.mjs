// PRIVATE INACTIVE complete caller for fixed native127 directPTY frames.
// Whole inventory tickets were committed before launch; this consumer cannot
// add a second cap, refund evidence slots or silently rearm a consumed phase.
const HANDLES=new WeakMap();
const NATIVE_CALLER_SEAL127=Symbol('source-owned-native-caller');
const PLATFORM_TOOLS127=typeof tools==='object'?tools:null;
const canonical=v=>v===null||typeof v!=='object'?JSON.stringify(v):Array.isArray(v)?'['+v.map(canonical).join(',')+']':'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}';
const same=(a,b)=>canonical(a)===canonical(b);
function use(c,id,owner){const r=c.rows.get(id);if(!r||r.owner!==owner||c.used.has(id)||c.failed&&!r.closure)throw Error('Shared immutable ticket/firstUNKNOWN/no replay');c.used.add(id);return r;}
export function prepare127(preloaded,key=null){
 const p=structuredClone(preloaded),rows=p.inventory.rows;
 if(rows.length!==p.inventory.inclusive_total||new Set(rows.map(x=>x.id)).size!==rows.length||p.inventory.authority!==false)throw Error('Whole exact source-produced inventory');
 if(p.realm!=='SYNTHETIC_SOURCE_ONLY'&&(key!==NATIVE_CALLER_SEAL127||p.currentNativeAdmission?.inclusive_cap!==rows.length||p.currentNativeAdmission?.contract!=='TRACE127_PHASE_INTENT_V1'))throw Error('No native registry from supplied booleans/dicts; actual fixed preflight required');
 const h=Object.freeze({realm:p.realm}),c={p,rows:new Map(rows.map(x=>[x.id,x])),used:new Set(),failed:null,nextSeq:1,session:null,observerCell:null,observers:new Set(),lastBlob:null,lastTree:null,lastCommit:null,artifact:null,fileRef:null};HANDLES.set(h,c);return h;
}
export async function bootstrapActualCaller127(preloaded){
 if(!PLATFORM_TOOLS127)throw Error('Actual platform lexical tools unavailable; no supplied callback authority');
 const preflightDeadline128=Date.now()+PREFLIGHT128.totalMs;
 const preview=prepare127({...preloaded,realm:'SYNTHETIC_SOURCE_ONLY'}),c=HANDLES.get(preview),t=PLATFORM_TOOLS127;
 use(c,'preflight/materialize','CONTROLLER');use(c,'preflight/materialize-original','CONTROLLER');
 const original=await t.mcp__codex_apps__library_prepare_materialize({items:[{library_file_id:'libfile_3ee8270f03d8819188e1de1f75c3d824'},{library_file_id:'libfile_505e4189bc588191bcda811c4a35da79'},{library_file_id:'libfile_6f69ae483b088191a1fffefca617bbd5'}],destination:{directory:preloaded.preflightDirectory}});
 await capture(c,'preflight-materialize.original.json',original,t);
 if(original.isError)throw Error('Actual current native read refused');
 use(c,'preflight/exec','CONTROLLER');use(c,'preflight/process','CONTROLLER');// first-original ticket consumed by finite collector below

 // Immutable inline verifier first anchors code to the ACTUAL current
 // addressed admission. No executable path/hash/bool supplied by the caller
 // can register a native capability before this source-native check.
 const q=s=>"'"+String(s).replaceAll("'","'\\''")+"'";
 const code=`import pathlib,json,hashlib,runpy,sys\na=json.loads(pathlib.Path(sys.argv[1]).read_bytes())['structuredContent'];ts=a['transfers'];assert not a.get('unavailable_items') and len(ts)==3\nown=next(x for x in ts if x['library_file_id']=='libfile_3ee8270f03d8819188e1de1f75c3d824');d=json.loads(pathlib.Path(own['workspace_path']).read_bytes());k='native'+d['state'].split('_')[0][6:];ad=d[k]['direction'].get('grouped127_admission');assert ad and 'ADMIT_TRACE127_GROUPED_NATIVE' in d[k]['direction']['body']\nroot=pathlib.Path(sys.argv[2]);raw=(root/'diagnostic108/manifest.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==ad['manifest_sha256'];m=json.loads(raw)\nfor n,p in m['source_files'].items():\n f=root/n;assert not pathlib.Path(n).is_absolute() and '..' not in pathlib.Path(n).parts;b=f.read_bytes();assert len(b)==p['bytes'] and hashlib.sha256(b).hexdigest()==p['sha256']\nsys.argv=[str(root/'diagnostic108/preflight127.py'),sys.argv[1],sys.argv[3]];runpy.run_path(str(root/'diagnostic108/preflight127.py'),run_name='__main__')`;
 for(let n=0;n<3;n++)use(c,'preflight/helper-original128/'+n,'CONTROLLER');
 let r;try{r=await t.exec_command({cmd:'python -c '+q(code)+' '+q(c.p.captureDirectory+'/preflight-materialize.original.json')+' '+q(preloaded.reviewedRoot)+' '+q(preloaded.configPath),yield_time_ms:1000,max_output_tokens:4000});}catch(error){r={tool_throw:{name:error?.name,message:String(error)},status:'UNKNOWN_NO_RETRY'};}
 const verified=await collectPreflight128(r,{tools:t,deadlineUtcMs:preflightDeadline128,claim:id=>use(c,id,'CONTROLLER'),retain:(name,original)=>capture(c,name,original,t)});
 if(verified.schema!=='TRACE127_NATIVE_PREFLIGHT_ORIGINAL_V1'||verified.inventory_sha256!==preloaded.inventorySha256||!same(verified.current_admission,preloaded.currentNativeAdmission))throw Error('Actual exact whole inventory/current contract');
 const verifiedPreload={...preloaded,holderCommand:{cmd:'python '+q(preloaded.reviewedRoot+'/diagnostic108/native127.py')+' '+q(preloaded.configPath),tty:true,yield_time_ms:1000,max_output_tokens:4000}};
 const handle=prepare127(verifiedPreload,NATIVE_CALLER_SEAL127);for(const id of c.used)HANDLES.get(handle).used.add(id);return handle;
}
export function reserveObserver127(handle,index,cellId){
 const c=HANDLES.get(handle);if(!c||typeof cellId!=='string'||!cellId||!Number.isInteger(index)||index<0||index>=c.p.inventory.observer_maximum||c.observerCell&&c.observerCell!==cellId)throw Error('Exact yielded exec cell; sixteen finite observer tickets');
 c.observerCell=cellId;use(c,'observer/'+index,'OBSERVER');c.observers.add(index);
 // The ACTUAL outer caller must run this source statement before functions.wait
 // and retain that exact tool original with retainObserver127 after it returns.
 // No claim that Python can intercept arbitrary model/platform tool calls.
 return Object.freeze({cell_id:cellId,index,pre_reserved:true,yield_time_ms:1000,max_tokens:2500});
}
export async function retainObserver127(handle,ticket,original,tools){
 const c=HANDLES.get(handle);if(!c||ticket.cell_id!==c.observerCell||!c.observers.has(ticket.index))throw Error('Exact preceding wait reservation');
 use(c,'observer/'+ticket.index+'/original','OBSERVER');c.observers.delete(ticket.index);
 await capture(c,'observer-'+ticket.index+'.original.json',{identity:ticket,original},tools);return original;
}
async function capture(c,name,value,tools){
 const text=JSON.stringify(value);if(text.length>4194304)throw Error('Bounded whole original, no truncation/retry');
 return await tools.apply_patch('*** Begin Patch\n*** Add File: '+c.p.captureDirectory+'/'+name+'\n+'+text+'\n*** End Patch');
}
export function counts127(handle){const c=HANDLES.get(handle);if(!c)throw Error('Exact registry');return {whole_reserved:c.rows.size,controller_used:c.used.size,first_unknown:c.failed,current48_fit:c.rows.size<=48,native_authority:false};}
export async function launch127(handle,tools){
 const c=HANDLES.get(handle);if(!c||c.session!==null)throw Error('ONE source-bound holder');
 if(c.p.realm!=='SYNTHETIC_SOURCE_ONLY'&&tools!==PLATFORM_TOOLS127)throw Error('No supplied native tool callback');
 use(c,'holder/start','CONTROLLER');use(c,'holder/start-original','CONTROLLER');
 let original;try{original=await tools.exec_command(c.p.holderCommand);}catch(e){original={tool_throw:{name:e?.name,message:String(e)},status:'UNKNOWN_NO_RETRY'};}
 await capture(c,'holder-start.original.json',original,tools);
 if(!Number.isInteger(original.session_id)||original.exit_code!=null){c.failed={holder_start:original};throw Error('No actual live sameholder; no retry');}c.session=original.session_id;return original;
}
function guardArgs(c,f){
 const a=f.args,p=c.p,repo='Elinfiny/TraceHarbor',id=f.inventory_call_id;
 if(!p.inventory.remote_ids.includes(id)||f.inventory_sha256!==p.inventorySha256||!same(f.context,p.context)||f.seq!==c.nextSeq||f.schema!=='TRACE118_HOST_REQUEST'||Date.now()>=Math.min(f.deadline_utc_ms,p.deadlineUtcMs))throw Error('Exact source/context/inventory/sequence/original parent');
 if(f.op.startsWith('github_create_')&&a.repository_full_name!==repo)throw Error('Exact repository');
 if(f.op==='github_create_blob'&&(a.encoding!=='base64'||typeof a.content!=='string'||a.content.length>190000))throw Error('Bounded exact body');
 if(f.op==='github_create_tree'&&(a.base_tree_sha!==p.sourceTree||a.tree_elements?.length!==1||a.tree_elements[0].sha!==c.lastBlob||a.tree_elements[0].mode!=='100644'||a.tree_elements[0].type!=='blob'))throw Error('Actual preceding blob/source tree');
 if(f.op==='github_create_commit'&&(a.parent_sha!==p.sourceSha||a.tree_sha!==c.lastTree||a.additional_parent_shas?.length))throw Error('Exact source soleparent/tree');
 if(f.op==='github_create_ref'&&(a.sha!==c.lastCommit||!/^traceharbor-(counter116-(admit|consumed)-[a-f0-9]{64}|encrypted104-[a-f0-9]{32})$/.test(a.branch_name)||Object.keys(a).some(k=>!['repository_full_name','branch_name','sha'].includes(k))))throw Error('Create-only exactref, no update/force/delete');
 if(f.op==='github_fetch'&&(!a.url.startsWith('https://api.github.com/repos/'+repo+'/')||!/^https:\/\/api.github.com\/repos\/Elinfiny\/TraceHarbor\/(actions\/runs\/\d+|commits\/[a-f0-9]{40}|git\/(blobs|trees)\/[a-f0-9]{40}(\?recursive=1)?|git\/ref\/heads\/traceharbor-[a-z0-9-]+)$/.test(a.url)))throw Error('Closed run/source/returned immutable GET only');
 if(f.op==='browser_js'&&(id!=='dispatch/UI'||!same(a,p.uiDispatchArgs)))throw Error('Exact independently admitted fixed UI script; no generic browser');
 if(f.op==='library_replace'&&(a.library_file_id!=='libfile_3ee8270f03d8819188e1de1f75c3d824'||!Number.isInteger(a.expected_current_version)||!a.file.startsWith(p.transferRoot+'/group127-upload-')||!a.file.endsWith('/TraceHarbor_V1_checkpoint.json')))throw Error('Owned conditionalCAS source staging only');
 if(f.op==='library_materialize'&&(!Array.isArray(a.items)||a.items.length!==1||!a.items[0].file_id||!a.destination.directory.startsWith(p.transferRoot+'/')||a.destination.directory.includes('..')))throw Error('Pinned positive disjoint item only');
 if(['github_fetch_workflow_run_jobs','github_fetch_workflow_run_artifacts','github_download_workflow_artifact'].includes(f.op)&&a.repo_full_name!==repo)throw Error('Selected repository');
 if(f.op==='github_fetch_workflow_run_artifacts'&&!new RegExp('^traceharbor-(recipient104|safe127)-'+a.run_id+'-1$').test(a.name))throw Error('Exact name-filtered artifact, not total run inventory');
 if(f.op==='github_download_workflow_artifact'&&a.artifact_id!==c.artifact)throw Error('Only actual preceding selected artifact');
}
export async function bridge127(handle,frame,tools){
 const c=HANDLES.get(handle);if(!c||c.failed)throw Error('Exact preloaded source registry/no UNKNOWN retry');guardArgs(c,frame);
 if(c.p.realm!=='SYNTHETIC_SOURCE_ONLY'&&(tools!==PLATFORM_TOOLS127||frame!==c.nativeFrame))throw Error('Only original SAME actual source holder frame; no caller-supplied dict');
 const id=frame.inventory_call_id;
 for(const s of ['tool','canonical','callback','callback-original'])use(c,id+'/'+s,'CONTROLLER');
 let original=null,error=null;const a=frame.args;
 try{switch(frame.op){
  case 'github_fetch':original=await tools.mcp__codex_apps__github_fetch(a);break;
  case 'github_create_blob':original=await tools.mcp__codex_apps__github_create_blob(a);break;
  case 'github_create_tree':original=await tools.mcp__codex_apps__github_create_tree(a);break;
  case 'github_create_commit':original=await tools.mcp__codex_apps__github_create_commit(a);break;
  case 'github_create_ref':original=await tools.mcp__codex_apps__github_create_branch(a);break;
  case 'github_fetch_workflow_run_jobs':original=await tools.mcp__codex_apps__github_fetch_workflow_run_jobs(a);break;
  case 'github_fetch_workflow_run_artifacts':original=await tools.mcp__codex_apps__github_fetch_workflow_run_artifacts(a);break;
  case 'github_download_workflow_artifact':original=await tools.mcp__codex_apps__github_download_workflow_artifact(a);break;
  case 'library_replace':original=await tools.mcp__codex_apps__library_replace_library_file(a);break;
  case 'library_materialize':original=await tools.mcp__codex_apps__library_prepare_materialize(a);break;
  case 'browser_js':original=await tools.mcp__codex_apps__browser_js(a);break;
  default:throw Error('No arbitrary tool/new route');
 }}catch(e){error={exception_class:e?.name||'Error',message:String(e?.message||e),status:'UNKNOWN_NO_RETRY'};}
 const identity={context_sha256:c.p.contextSha256,operation:frame.op,seq:frame.seq,tool:frame.op,call_id:frame.request_digest};
 // Exactly one canonical complete native result before ALL postguards. Alias
 // consumers use this exact file/count/hash; equal bytes of othercalls differ.
 if(error&&original===null)original={tool_throw:error,status:'UNKNOWN_NO_RETRY'};
 await capture(c,frame.seq+'.canonical-native-original.json',{identity,original},tools);
 const late=Date.now()>=Math.min(frame.deadline_utc_ms,c.p.deadlineUtcMs);
 if(error||late||original?.isError)c.failed=error||{late,tool_error:original?.isError===true};
 if(!c.failed){const v=original?.structuredContent;
  if(frame.op==='github_create_blob')c.lastBlob=v?.sha;
  if(frame.op==='github_create_tree')c.lastTree=v?.sha;
  if(frame.op==='github_create_commit')c.lastCommit=v?.sha;
  if(frame.op==='github_fetch_workflow_run_artifacts'){if(v?.total_count!==1||v.artifacts?.length!==1||v.artifacts[0].name!==a.name){c.failed={artifact_identity:true};}else c.artifact=v.artifacts[0].id;}
 }
 const response={schema:'TRACE118_HOST_RETURN',seq:frame.seq,context:frame.context,op:frame.op,request_digest:frame.request_digest,original_result:original,transport_error:error,late:late||!!c.failed};
 let terminal;try{terminal=await tools.write_stdin({session_id:c.session,chars:JSON.stringify(response)+'\n',yield_time_ms:1000,max_output_tokens:4000});}catch(e){terminal={tool_throw:{name:e?.name,message:String(e)},status:'UNKNOWN_NO_RETRY'};c.failed??=terminal;}
 await capture(c,frame.seq+'.canonical-callback-original.json',terminal,tools);c.nextSeq++;
 if(c.failed)throw Error('First original/exception retained; entire phase non-retriable');return terminal;
}
export async function drive127(handle,tools){
 // Entire live method binding. No hidden poll. Each callback must return the
 // next complete source frame or the actual process terminal. An incomplete
 // output is UNKNOWN; never resend exec/callback/consumed phase to repair it.
 const c=HANDLES.get(handle);let original=await launch127(handle,tools);
 for(let n=0;n<=c.p.inventory.remote_ids.length;n++){
  if(original.exit_code!=null){use(c,'holder/terminal','CONTROLLER');use(c,'holder/terminal-original','CONTROLLER');await capture(c,'holder-terminal.original.json',original,tools);if(original.exit_code!==0)throw Error('Actual source holder nonzero');return original;}
  if(n===c.p.inventory.remote_ids.length)throw Error('Finite remote schedule exhausted before terminal; no extra poll');
  const lines=(original.output||'').trim().split('\n');if(lines.length!==1)throw Error('One exact bounded source frame, no prefix/event selection');
  const frame=JSON.parse(lines[0]);c.nativeFrame=frame;original=await bridge127(handle,frame,tools);c.nativeFrame=null;
 }
 throw Error('Finite complete macro frame schedule exhausted; no retry');
}

// No capability is created by this collector. The native bootstrap alone uses
// lexical platform tools plus exact current source/admission after terminal.
export const PREFLIGHT128=Object.freeze({totalMs:45000,polls:8,maxBytes:262144});
export async function collectPreflight128(first,{tools,deadlineUtcMs,retain,claim,now=Date.now}){
 let response=first,session=null,output='',parts=0,primary=null,cleanup=null,verified=null;
 const chunks=new Set(),started=now();
 try{
  for(let index=0;index<=PREFLIGHT128.polls;index++){
   const originalTicket=index===0?'preflight/exec-original':'preflight/poll-original128/'+(index-1);
   claim(originalTicket);
   await retain(index===0?'preflight-exec.original.json':'preflight-poll128-'+(index-1)+'.original.json',{identity:{phase:'PREFLIGHT',index,session_id:session},original:response});
   if(now()>=deadlineUtcMs||now()-started>=PREFLIGHT128.totalMs||deadlineUtcMs>started+PREFLIGHT128.totalMs)throw Error('Finite preflight deadline; no native registration');
   if(!response||typeof response.output!=='string'||response.isError||response.tool_throw||response.original_token_count>4000)throw Error('Complete untruncated native preflight original');
   if(typeof response.chunk_id!=='string'||!response.chunk_id||chunks.has(response.chunk_id))throw Error('Unique ordered original chunk identity');
   chunks.add(response.chunk_id);parts++;output+=response.output;
   if(new TextEncoder().encode(output).length>PREFLIGHT128.maxBytes)throw Error('Complete bounded preflight output');
   if(response.exit_code!=null){
    if(response.exit_code!==0||response.session_id!=null||response.eof===false)throw Error('Actual terminal0 plus EOF required');
    verified=JSON.parse(output);if(!verified||Array.isArray(verified)||typeof verified!=='object')throw Error('ONE complete structured JSON record required');
    return verified;
   }
   if(!Number.isInteger(response.session_id)||response.eof===true||index===PREFLIGHT128.polls)throw Error('Finite SAME live preflight session; no exec retry');
   if(session===null)session=response.session_id;
   if(response.session_id!==session)throw Error('Preflight session drift');
   claim('preflight/poll128/'+index);
   try{response=await tools.write_stdin({session_id:session,chars:'',yield_time_ms:1000,max_output_tokens:4000});}
   catch(error){response={tool_throw:{name:error?.name,message:String(error)},status:'UNKNOWN_NO_RETRY'};}
  }
  throw Error('Finite preflight collection exhausted');
 }catch(error){primary={name:error?.name,message:String(error)};throw error;}
 finally{
  try{claim('preflight/collection-close128');await retain('preflight-collection128.original.json',{phase:'PREFLIGHT',session_id:session,parts,output,primary,terminal_verified:!!verified,registration:false});}
  catch(error){cleanup={name:error?.name,message:String(error)};if(primary)throw new AggregateError([primary,cleanup],'Preflight primary and later retention cleanup; no registration');throw error;}
 }
}
