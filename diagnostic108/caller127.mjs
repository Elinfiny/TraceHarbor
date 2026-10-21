// PRIVATE INACTIVE complete caller for fixed native127 directPTY frames.
// Whole inventory tickets were committed before launch; this consumer cannot
// add a second cap, refund evidence slots or silently rearm a consumed phase.
const HANDLES=new WeakMap();
const NATIVE_CALLER_SEAL127=Symbol('source-owned-native-caller');
const PLATFORM_TOOLS127=typeof tools==='object'?tools:null;

//129 plain data only. Native opaque handles stay in HANDLES, never copied.
export const CONFIG_LIMITS129=Object.freeze({depth:64,nodes:32768,array:8192,keys:4096,utf8Bytes:2097152});
export function utf8ByteCount129(value,limit=262144){
 if(typeof value!=='string'||!Number.isSafeInteger(limit)||limit<0)throw Error('Exact UTF8 string and finite integer bound');
 let bytes=0;
 for(let i=0;i<value.length;i++){
  const unit=value.charCodeAt(i);
  if(unit<=0x7f)bytes++;
  else if(unit<=0x7ff)bytes+=2;
  else if(unit>=0xd800&&unit<=0xdbff&&i+1<value.length&&value.charCodeAt(i+1)>=0xdc00&&value.charCodeAt(i+1)<=0xdfff){bytes+=4;i++;}
  else bytes+=3; // Lone surrogate is U+FFFD, as the supported UTF8 contract.
  if(bytes>limit)throw Error('Complete bounded preflight output');
 }
 return bytes;
}
export function snapshotPlain129(input){
 const memo=new Map(),active=new Set();let nodes=0,bytes=0;
 function stringBudget(value){bytes+=utf8ByteCount129(value,CONFIG_LIMITS129.utf8Bytes);if(bytes>CONFIG_LIMITS129.utf8Bytes)throw Error('Bounded plain-config total UTF8 bytes');}
 function visit(value,depth){
  if(depth>CONFIG_LIMITS129.depth||++nodes>CONFIG_LIMITS129.nodes)throw Error('Bounded plain-config depth/nodes');
  if(value===null||typeof value==='boolean')return value;
  if(typeof value==='string'){stringBudget(value);return value;}
  if(typeof value==='number'){if(!Number.isFinite(value))throw Error('Finite plain-config number');return value;}
  if(typeof value!=='object')throw Error('No undefined/function/symbol/BigInt config values');
  if(HANDLES.has(value))throw Error('Source-owned opaque handle remains in original registry');
  if(active.has(value))throw Error('No cyclic plain config');
  if(memo.has(value))return memo.get(value);
  const array=Array.isArray(value),proto=Object.getPrototypeOf(value);
  if(proto!==(array?Array.prototype:Object.prototype))throw Error('Only exact plain object/array prototypes');
  const descriptors=Object.getOwnPropertyDescriptors(value),keys=Reflect.ownKeys(value);
  if(keys.some(k=>typeof k!=='string'))throw Error('No symbol config keys');
  const length=array?descriptors.length.value:0;
  if(array&&(!Number.isSafeInteger(length)||length<0||length>CONFIG_LIMITS129.array||keys.length!==length+1))throw Error('Bounded dense array without extra properties');
  if(!array&&keys.length>CONFIG_LIMITS129.keys)throw Error('Bounded plain-config key count');
  const copy=array?new Array(length):{};memo.set(value,copy);active.add(value);
  for(const key of keys){
   if(array&&key==='length')continue;
   if(array&&(!/^(0|[1-9][0-9]*)$/.test(key)||Number(key)>=length))throw Error('Exact dense array indices');
   const descriptor=descriptors[key];
   if(!Object.prototype.hasOwnProperty.call(descriptor,'value')||descriptor.enumerable!==true)throw Error('No accessors or hidden config properties');
   stringBudget(key);Object.defineProperty(copy,key,{value:visit(descriptor.value,depth+1),writable:true,enumerable:true,configurable:true});
  }
  active.delete(value);return copy;
 }
 return visit(input,0);
}

const canonical=v=>v===null||typeof v!=='object'?JSON.stringify(v):Array.isArray(v)?'['+v.map(canonical).join(',')+']':'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}';
const same=(a,b)=>canonical(a)===canonical(b);
function use(c,id,owner){const r=c.rows.get(id);if(!r||r.owner!==owner||c.used.has(id)||c.failed&&!r.closure)throw Error('Shared immutable ticket/firstUNKNOWN/no replay');c.used.add(id);return r;}
export function prepare127(preloaded,key=null){
 const p=snapshotPlain129(preloaded),rows=p.inventory.rows;
 if(rows.length!==p.inventory.inclusive_total||new Set(rows.map(x=>x.id)).size!==rows.length||p.inventory.authority!==false)throw Error('Whole exact source-produced inventory');
 if(p.realm!=='SYNTHETIC_SOURCE_ONLY'&&(key!==NATIVE_CALLER_SEAL127||p.currentNativeAdmission?.inclusive_cap!==rows.length||p.currentNativeAdmission?.contract!=='TRACE133_STATIC_TYPED_RUNTIME_V2'))throw Error('No native registry from supplied booleans/dicts; actual fixed preflight required');
 const h=Object.freeze({realm:p.realm}),c={p,rows:new Map(rows.map(x=>[x.id,x])),used:new Set(),failed:null,nextSeq:1,session:null,observerCell:null,observers:new Set(),lastBlob:null,lastTree:null,lastCommit:null,artifact:null,fileRef:null};HANDLES.set(h,c);return h;
}
export async function bootstrapActualCaller127(preloaded){
 if(!PLATFORM_TOOLS127)throw Error('Actual platform lexical tools unavailable; no supplied callback authority');
 const validated129=snapshotPlain129(preloaded);
 for(const key of ['context','contextSha256','deadlineUtcMs','uiDispatchArgs'])if(Object.hasOwn(validated129,key))throw Error('No premature runtime context/clock/once in static preload');
 const preflightDeadline128=Date.now()+PREFLIGHT128.totalMs;
 const preview=prepare127({...validated129,realm:'SYNTHETIC_SOURCE_ONLY'}),c=HANDLES.get(preview),t=PLATFORM_TOOLS127;
 use(c,'preflight/materialize','CONTROLLER');use(c,'preflight/materialize-original','CONTROLLER');
 const original=await t.mcp__codex_apps__library_prepare_materialize({items:[{library_file_id:'libfile_3ee8270f03d8819188e1de1f75c3d824'},{library_file_id:'libfile_f87a6a307f70819194e0af0fa453afd1'},{library_file_id:'libfile_6f69ae483b088191a1fffefca617bbd5'}],destination:{directory:validated129.preflightDirectory}});
 await capture(c,'preflight-materialize.original.json',original,t);
 if(original.isError)throw Error('Actual current native read refused');
 use(c,'preflight/exec','CONTROLLER');use(c,'preflight/process','CONTROLLER');// first-original ticket consumed by finite collector below

 // Immutable inline verifier first anchors code to the ACTUAL current
 // addressed admission. No executable path/hash/bool supplied by the caller
 // can register a native capability before this source-native check.
 const q=s=>"'"+String(s).replaceAll("'","'\\''")+"'";
 const code=`import pathlib,json,hashlib,runpy,sys\na=json.loads(pathlib.Path(sys.argv[1]).read_bytes())['structuredContent'];a=a.get('result',a);ts=a['transfers'];assert not a.get('unavailable_items') and len(ts)==3\nown=next(x for x in ts if x['library_file_id']=='libfile_3ee8270f03d8819188e1de1f75c3d824');d=json.loads(pathlib.Path(own['workspace_path']).read_bytes());k='native'+d['state'].split('_')[0][6:];ad=d[k]['direction'].get('grouped133_admission');assert ad and ad.get('contract')=='TRACE133_STATIC_TYPED_RUNTIME_V2' and 'ADMIT_TRACE133_STATIC_TYPED_RUNTIME_V2' in d[k]['direction']['body']\nroot=pathlib.Path(sys.argv[2]);raw=(root/'diagnostic108/manifest.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==ad['manifest_sha256'];m=json.loads(raw)\nfor n,p in m['source_files'].items():\n f=root/n;assert not pathlib.Path(n).is_absolute() and '..' not in pathlib.Path(n).parts;b=f.read_bytes();assert len(b)==p['bytes'] and hashlib.sha256(b).hexdigest()==p['sha256']\nsys.argv=[str(root/'diagnostic108/preflight127.py'),sys.argv[1],sys.argv[3]];runpy.run_path(str(root/'diagnostic108/preflight127.py'),run_name='__main__')`;
 for(let n=0;n<3;n++)use(c,'preflight/helper-original128/'+n,'CONTROLLER');
 let r;try{r=await t.exec_command({cmd:'python -c '+q(code)+' '+q(c.p.captureDirectory+'/preflight-materialize.original.json')+' '+q(validated129.reviewedRoot)+' '+q(validated129.configPath),yield_time_ms:1000,max_output_tokens:4000});}catch(error){r={tool_throw:{name:error?.name,message:String(error)},status:'UNKNOWN_NO_RETRY'};}
 const verified=await collectPreflight128(r,{tools:t,deadlineUtcMs:preflightDeadline128,claim:id=>use(c,id,'CONTROLLER'),retain:(name,original)=>capture(c,name,original,t)});
 if(verified.schema!=='TRACE133_NATIVE_PREFLIGHT_ORIGINAL_V2'||verified.inventory_sha256!==validated129.inventorySha256||!same(verified.current_admission,validated129.currentNativeAdmission))throw Error('Actual exact whole inventory/current contract');
 const verifiedPreload={...validated129,context:null,contextSha256:null,deadlineUtcMs:null,uiDispatchArgs:null,sourceSha:verified.sourceSha,sourceTree:verified.sourceTree,captureDirectory:verified.captureDirectory,transferRoot:verified.transferRoot,dispatchSource133:verified.dispatchSource,directionId133:verified.directionId,staticConfigSha256:verified.staticConfigSha256,manifestSha135:verified.manifestSha135,holderCommand:{cmd:'python '+q(validated129.reviewedRoot+'/diagnostic108/native127.py')+' '+q(validated129.configPath),tty:true,yield_time_ms:1000,max_output_tokens:262144}};
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
 c.streamCutoff143=Date.now()+15000;
 let original;try{original=await tools.exec_command(c.p.holderCommand);}catch(e){original={tool_throw:{name:e?.name,message:String(e)},status:'UNKNOWN_NO_RETRY'};}
 await capture(c,'holder-start.original.json',original,tools);
 if(!Number.isInteger(original.session_id)||original.exit_code!=null){c.failed={holder_start:original};throw Error('No actual live sameholder; no retry');}c.session=original.session_id;return original;
}
function bindSourceRuntime133(c,frame){
 // This DATA comes only from the exact source holder's retained start original.
 // No exported function accepts a runtime dict to register native authority.
 const b=frame.runtime_binding133,p=c.p;
 if(c.session===null||frame!==c.nativeFrame||frame.seq!==1||frame.inventory_call_id!=='SOURCE_FREEZE/CAS'||!b||b.schema!=='TRACE133_SOURCE_RUNTIME_FRAME'||b.static_config_sha256!==p.staticConfigSha256||b.sourceSha!==p.sourceSha||b.sourceTree!==p.sourceTree||b.context?.domain!=='TRACE133_TYPED_RUNTIME'||b.context.source_sha!==p.sourceSha||b.context.direction_id!==p.directionId133||!/^[a-f0-9]{64}$/.test(b.context.once_receipt_sha256)||!/^[a-f0-9]{64}$/.test(b.context_sha256)||!same(b.context,frame.context)||!Number.isInteger(b.deadlineUtcMs)||b.deadlineUtcMs<=Date.now()||b.deadlineUtcMs>Date.now()+900000)throw Error('Actual source same invocation runtime binding; original900 only');
 if(b.manifestSha256!==p.manifestSha135||b.onceExpiresUtc!==b.deadlineUtcMs/1000||!Number.isInteger(b.coordinatorCutoffUtc)||b.coordinatorCutoffUtc<b.onceExpiresUtc)throw Error('Original source manifest/expiry/cutoff, no reset');
 const values136={source_sha:p.sourceSha,manifest_sha256:p.manifestSha135,once_receipt_sha256:b.context.once_receipt_sha256,once_expires_utc:String(b.onceExpiresUtc),coordinator_cutoff_utc:String(b.coordinatorCutoffUtc)};
 const git136=p.dispatchSource133.kind==='git_create136';
 if(b.dispatchKind136!==(git136?'git_create136':'browser135'))throw Error('Same fixed source dispatch kind');
 const expectedArgs=git136?gitCreateArgs136(p.dispatchSource133,values136):{code:renderDispatch135(p.dispatchSource133,values136)};
 if(!same(b.uiDispatchArgs,expectedArgs))throw Error('Static script plus actual newly produced once only');
 p.context=snapshotPlain129(b.context);p.contextSha256=b.context_sha256;p.deadlineUtcMs=b.deadlineUtcMs;p.uiDispatchArgs=snapshotPlain129(b.uiDispatchArgs);
}
function guardArgs(c,f){
 const a=f.args,p=c.p,repo='Elinfiny/TraceHarbor',id=f.inventory_call_id;
 if(!p.inventory.remote_ids.includes(id)||f.inventory_sha256!==p.inventorySha256||!same(f.context,p.context)||f.seq!==c.nextSeq||f.schema!=='TRACE118_HOST_REQUEST'||Date.now()>=Math.min(f.deadline_utc_ms,p.deadlineUtcMs))throw Error('Exact source/context/inventory/sequence/original parent');
 if(f.op.startsWith('github_create_')&&a.repository_full_name!==repo)throw Error('Exact repository');
 if(f.op==='github_create_blob'&&(a.encoding!=='base64'||typeof a.content!=='string'||a.content.length>190000))throw Error('Bounded exact body');
 if(f.op==='github_create_tree'&&(a.base_tree_sha!==p.sourceTree||a.tree_elements?.length!==1||a.tree_elements[0].sha!==c.lastBlob||a.tree_elements[0].mode!=='100644'||a.tree_elements[0].type!=='blob'))throw Error('Actual preceding blob/source tree');
 if(f.op==='github_create_commit'&&(a.parent_sha!==p.sourceSha||a.tree_sha!==c.lastTree||a.additional_parent_shas?.length))throw Error('Exact source soleparent/tree');
 if(f.op==='github_create_ref'&&(a.sha!==c.lastCommit||!/^traceharbor-(counter116-(admit|consumed)-[a-f0-9]{64}|encrypted104-[a-f0-9]{32})$/.test(a.branch_name)||Object.keys(a).some(k=>!['repository_full_name','branch_name','sha'].includes(k))))throw Error('Create-only exactref, no update/force/delete');
 if(f.op==='github_fetch'&&!id.startsWith('dispatch136/')&&(!a.url.startsWith('https://api.github.com/repos/'+repo+'/')||!/^https:\/\/api.github.com\/repos\/Elinfiny\/TraceHarbor\/(actions\/runs\/\d+|commits\/[a-f0-9]{40}|git\/(blobs|trees)\/[a-f0-9]{40}(\?recursive=1)?|git\/ref\/heads\/traceharbor-[a-z0-9-]+)$/.test(a.url)))throw Error('Closed run/source/returned immutable GET only');
 if(id.startsWith('dispatch136/')){
  if(p.dispatchSource133.kind!=='git_create136')throw Error('No Git dispatch via manual source');
  const ref='https://api.github.com/repos/'+repo+'/git/ref/heads/'+p.uiDispatchArgs.branch_name;
  const list='https://api.github.com/repos/'+repo+'/actions/runs?event=create&head_sha='+p.sourceSha+'&branch='+encodeURIComponent(p.uiDispatchArgs.branch_name)+'&per_page=100';
  if(id==='dispatch136/create-ref'){if(f.op!=='github_create_dispatch136'||!same(a,p.uiDispatchArgs))throw Error('Exact source create-only args');}
  else if(id==='dispatch136/ref-absence'){if(f.op!=='github_ref_absence136'||!same(a,{url:ref}))throw Error('Exact prior ref absence');}
  else if(id==='dispatch136/ref-proof'){if(f.op!=='github_fetch'||!same(a,{url:ref}))throw Error('Exact created ref proof');}
  else if(/^dispatch136\/runs\/[0-3]$/.test(id)){if(f.op!=='github_fetch'||!same(a,{url:list}))throw Error('Finite source once exact branch list');}
  else throw Error('No unknown Git dispatch source primitive');
 }
 if(['github_ref_absence136','github_create_dispatch136'].includes(f.op)&&!id.startsWith('dispatch136/'))throw Error('No new source op outside exact dispatch136 inventory');
 if(f.op==='browser_js'&&(id!=='dispatch/UI'||!same(a,p.uiDispatchArgs)))throw Error('Exact independently admitted fixed UI script; no generic browser');
 if(f.op==='library_replace'&&(a.library_file_id!=='libfile_3ee8270f03d8819188e1de1f75c3d824'||!Number.isInteger(a.expected_current_version)||!a.file.startsWith(p.transferRoot+'/group127-upload-')||!a.file.endsWith('/TraceHarbor_V1_checkpoint.json')))throw Error('Owned conditionalCAS source staging only');
 if(f.op==='library_materialize'&&(!Array.isArray(a.items)||a.items.length!==1||!a.items[0].file_id||!a.destination.directory.startsWith(p.transferRoot+'/')||a.destination.directory.includes('..')))throw Error('Pinned positive disjoint item only');
 if(['github_fetch_workflow_run_jobs','github_fetch_workflow_run_artifacts','github_download_workflow_artifact'].includes(f.op)&&a.repo_full_name!==repo)throw Error('Selected repository');
 if(f.op==='github_fetch_workflow_run_artifacts'&&!new RegExp('^traceharbor-(recipient104|safe127)-'+a.run_id+'-1$').test(a.name))throw Error('Exact name-filtered artifact, not total run inventory');
 if(f.op==='github_download_workflow_artifact'&&a.artifact_id!==c.artifact)throw Error('Only actual preceding selected artifact');
}
export async function bridge127(handle,frame,tools){
 const c=HANDLES.get(handle);if(!c||c.failed)throw Error('Exact preloaded source registry/no UNKNOWN retry');
 if(c.p.realm!=='SYNTHETIC_SOURCE_ONLY'&&(tools!==PLATFORM_TOOLS127||frame!==c.nativeFrame))throw Error('Only original SAME actual source holder frame; no caller-supplied dict');
 if(c.p.realm!=='SYNTHETIC_SOURCE_ONLY'&&c.p.context===null)bindSourceRuntime133(c,frame);
 guardArgs(c,frame);
 const id=frame.inventory_call_id;
 for(const s of ['tool','canonical','callback','callback-original'])use(c,id+'/'+s,'CONTROLLER');
 let original=null,error=null;const a=frame.args;
 try{switch(frame.op){
  case 'github_ref_absence136':original=await tools.mcp__codex_apps__github_fetch(a);break;
  case 'github_create_dispatch136':original=await tools.mcp__codex_apps__github_create_branch(a);break;
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
 const expected404136=frame.op==='github_ref_absence136'&&id==='dispatch136/ref-absence'&&original?.isError===true&&original.structuredContent?.error_code==='NOT_FOUND'&&String(original.structuredContent?.error_data?.status)==='404';
 if(error||late||original?.isError&&!expected404136)c.failed=error||{late,tool_error:original?.isError===true};
 if(!c.failed){const v=original?.structuredContent;
  if(frame.op==='github_create_blob')c.lastBlob=v?.sha;
  if(frame.op==='github_create_tree')c.lastTree=v?.sha;
  if(frame.op==='github_create_commit')c.lastCommit=v?.sha;
  if(frame.op==='github_fetch_workflow_run_artifacts'){if(v?.total_count!==1||v.artifacts?.length!==1||v.artifacts[0].name!==a.name){c.failed={artifact_identity:true};}else c.artifact=v.artifacts[0].id;}
 }
 const response={schema:'TRACE118_HOST_RETURN',seq:frame.seq,context:frame.context,op:frame.op,request_digest:frame.request_digest,original_result:original,transport_error:error,late:late||!!c.failed};
 c.streamCutoff143=Math.min(Date.now()+15000,frame.deadline_utc_ms,c.p.deadlineUtcMs);
 let terminal;try{terminal=await tools.write_stdin({session_id:c.session,chars:JSON.stringify(response)+'\n',yield_time_ms:1000,max_output_tokens:262144});}catch(e){terminal={tool_throw:{name:e?.name,message:String(e)},status:'UNKNOWN_NO_RETRY'};c.failed??=terminal;}
 await capture(c,frame.seq+'.canonical-callback-original.json',terminal,tools);c.nextSeq++;
 if(c.failed)throw Error('First original/exception retained; entire phase non-retriable');return terminal;
}
async function collectHolderStream143(handle,first,tools,window){
 const c=HANDLES.get(handle),deadline=c?.streamCutoff143;
 if(!c||c.failed||!['launch',...c.p.inventory.remote_ids].includes(window)||!Number.isInteger(deadline))throw Error('One source-owned original stream window');
 let response=first,output='',verified=null,primary=null;const chunks=new Set(),identities=[];
 try{
  for(let n=0;n<=8;n++){
   // Initial original was retained by launch/callback. Every additional
   // actual empty-input read is captured BEFORE any parse/deadline guard.
   if(n){use(c,'stream143/'+window+'/poll-original/'+(n-1),'CONTROLLER');await capture(c,'stream143-'+window.replaceAll('/','-')+'-poll-'+(n-1)+'.original.json',response,tools);}
   identities.push({index:n,chunk_id:response?.chunk_id,session_id:response?.session_id,exit_code:response?.exit_code});
   if(Date.now()>=deadline)throw Error('Original stream/phase/parent cutoff; no reset');
   if(!response||response.isError||response.tool_throw||typeof response.output!=='string'||response.original_token_count>262144||typeof response.chunk_id!=='string'||!response.chunk_id||chunks.has(response.chunk_id))throw Error('Complete bounded ordered original stream chunk');
   chunks.add(response.chunk_id);output+=response.output;utf8ByteCount129(output,262144);
   if(response.exit_code!=null){if(response.session_id!=null||response.eof===false)throw Error('Actual terminal plus EOF required');verified={...response,output};return verified;}
   if(response.session_id!==c.session||response.eof===true)throw Error('Only actual SAME live holder; no restart');
   if(output.endsWith('\n')){verified={...response,output};return verified;}
   if(n===8)throw Error('Eight precommitted source-stream reads exhausted; no retry');
   use(c,'stream143/'+window+'/poll/'+n,'CONTROLLER');
   try{response=await tools.write_stdin({session_id:c.session,chars:'',yield_time_ms:1000,max_output_tokens:262144});}
   catch(error){response={tool_throw:{name:error?.name,message:String(error)},status:'UNKNOWN_NO_RETRY'};}
  }
 }catch(error){primary={name:error?.name,message:String(error)};c.failed??=primary;throw error;}
 finally{use(c,'stream143/'+window+'/close','CONTROLLER');await capture(c,'stream143-'+window.replaceAll('/','-')+'-close.original.json',{window,deadline,identities,output,primary,complete:!!verified,initial_original:first},tools);}
}
export async function drive127(handle,tools){
 const c=HANDLES.get(handle);let original,window='launch';
 try{
  original=await launch127(handle,tools);
  for(let n=0;n<=c.p.inventory.remote_ids.length;n++){
   original=await collectHolderStream143(handle,original,tools,window);
   if(original.exit_code!=null){use(c,'holder/terminal','CONTROLLER');use(c,'holder/terminal-original','CONTROLLER');await capture(c,'holder-terminal.original.json',original,tools);if(original.exit_code!==0)throw Error('Actual source holder nonzero; original retained');return original;}
   if(n===c.p.inventory.remote_ids.length)throw Error('Finite remote schedule exhausted before terminal');
   const lines=original.output.trim().split('\n');if(lines.length!==1)throw Error('One exact complete source frame; no prefix/event selection');
   const frame=JSON.parse(lines[0]);c.nativeFrame=frame;window=frame.inventory_call_id;original=await bridge127(handle,frame,tools);c.nativeFrame=null;
  }
  throw Error('Finite complete macro stream exhausted; no retry');
 }catch(error){c.failed??={name:error?.name,message:String(error)};use(c,'controller/failure143','CONTROLLER');await capture(c,'controller-failure143.original.json',{failure:c.failed,error:{name:error?.name,message:String(error)}},tools);throw error;}
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
   if(utf8ByteCount129(output)>PREFLIGHT128.maxBytes)throw Error('Complete bounded preflight output');
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

export function renderDispatch135(source,inputs){
 const fields={'__TRACE_SOURCE135__':'source_sha','__TRACE_MANIFEST135__':'manifest_sha256','__TRACE_ONCE133__':'once_receipt_sha256','__TRACE_EXPIRES135__':'once_expires_utc','__TRACE_CUTOFF135__':'coordinator_cutoff_utc'};let code=source.script;
 for(const [token,key] of Object.entries(fields)){if(code.split(token).length!==2||typeof inputs[key]!=='string')throw Error('Exact source-owned five-input binding');code=code.replace(token,inputs[key]);}
 if(code.split('__TRACE_TAB135__').length!==2||!Number.isInteger(source.tab_id))throw Error('Exact static tab role');return code.replace('__TRACE_TAB135__',String(source.tab_id));
}

//136 pure DATA renderer; only fixed preflight/holder registry may invoke tools.
export function gitCreateArgs136(source,v){
 if(!source||Object.keys(source).sort().join(',')!=='actor_proof_sha256,expected_actor_id,kind,namespace,workflow_path'||source.kind!=='git_create136'||source.expected_actor_id!==273768139||source.namespace!=='traceharbor/once136/v1/'||source.workflow_path!=='.github/workflows/traceharbor-counter136.yml'||!/^[a-f0-9]{64}$/.test(source.actor_proof_sha256))throw Error('Independent genuine event actor proof remains mandatory');
 if(!v||Object.keys(v).sort().join(',')!=='coordinator_cutoff_utc,manifest_sha256,once_expires_utc,once_receipt_sha256,source_sha'||!/^[a-f0-9]{40}$/.test(v.source_sha)||!/^[a-f0-9]{64}$/.test(v.manifest_sha256)||!/^[a-f0-9]{64}$/.test(v.once_receipt_sha256)||!/^([1-9][0-9]{0,11})$/.test(v.once_expires_utc)||!/^([1-9][0-9]{0,11})$/.test(v.coordinator_cutoff_utc)||Number(v.coordinator_cutoff_utc)<Number(v.once_expires_utc))throw Error('Closed source native five inputs no reset');
 return {repository_full_name:'Elinfiny/TraceHarbor',branch_name:source.namespace+[v.source_sha,v.manifest_sha256,v.once_receipt_sha256,v.once_expires_utc,v.coordinator_cutoff_utc].join('-'),sha:v.source_sha};
}
