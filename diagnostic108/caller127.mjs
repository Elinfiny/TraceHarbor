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
 if(p.realm!=='SYNTHETIC_SOURCE_ONLY'&&(key!==NATIVE_CALLER_SEAL127||p.currentNativeAdmission?.inclusive_cap!==rows.length||p.currentNativeAdmission?.contract!=='TRACE146_STATIC_TYPED_RUNTIME_V3'))throw Error('No native registry from supplied booleans/dicts; actual fixed preflight required');
 const h=Object.freeze({realm:p.realm}),c={p,rows:new Map(rows.map(x=>[x.id,x])),used:new Set(),failed:null,nextSeq:1,session:null,observerCell:null,observers:new Set(),lastBlob:null,lastTree:null,lastCommit:null,artifact:null,fileRef:null};HANDLES.set(h,c);return h;
}
export async function bootstrapActualCaller127(preloaded){
 if(!PLATFORM_TOOLS127)throw Error('Actual platform lexical tools unavailable; no supplied callback authority');
 const validated129=snapshotPlain129(preloaded);
 for(const key of ['context','contextSha256','deadlineUtcMs','uiDispatchArgs'])if(Object.hasOwn(validated129,key))throw Error('No premature runtime context/clock/once in static preload');
 const preflightDeadline128=Date.now()+PREFLIGHT128.totalMs;
 const preview=prepare127({...validated129,realm:'SYNTHETIC_SOURCE_ONLY'}),c=HANDLES.get(preview),t=PLATFORM_TOOLS127;
 use(c,'preflight/materialize','CONTROLLER');use(c,'preflight/materialize-original','CONTROLLER');
 const original=await t.mcp__codex_apps__library_prepare_materialize({items:[{library_file_id:'libfile_3ee8270f03d8819188e1de1f75c3d824'},{library_file_id:'libfile_f87a6a307f70819194e0af0fa453afd1'},{library_file_id:'libfile_6f69ae483b088191a1fffefca617bbd5'},{library_file_id:'libfile_8377022600088191993dc06bfba93b7b'}],destination:{directory:validated129.preflightDirectory}});
 await capture(c,'preflight-materialize.original.json',original,t);
 if(original.isError)throw Error('Actual current native read refused');
 use(c,'preflight/exec','CONTROLLER');use(c,'preflight/process','CONTROLLER');// first-original ticket consumed by finite collector below

 // Immutable inline verifier first anchors code to the ACTUAL current
 // addressed admission. No executable path/hash/bool supplied by the caller
 // can register a native capability before this source-native check.
 const q=s=>"'"+String(s).replaceAll("'","'\\''")+"'";
 const code=`import pathlib,json,hashlib,runpy,sys\ndef streamed_hash158(value):\n h=hashlib.sha256()\n for chunk in json.JSONEncoder(sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).iterencode(value):\n  for offset in range(0,len(chunk),65536):h.update(chunk[offset:offset+65536].encode())\n return h.hexdigest()\ndef read_current133(path,transfer):\n import os,stat\n p=pathlib.Path(path)\n if not p.is_absolute() or p.resolve()!=p:raise ValueError('No current path aliases')\n for parent in [*reversed(p.parents),p]:\n  if parent.is_symlink():raise ValueError('No current symlink ancestor')\n before=p.lstat();limit=83886080\n if transfer.get('library_file_id')!='libfile_3ee8270f03d8819188e1de1f75c3d824' or transfer.get('workspace_path')!=str(p) or transfer.get('size_bytes')!=before.st_size:raise ValueError('Exact lexical actual OWN transfer for preliminary read')\n if not stat.S_ISREG(before.st_mode) or before.st_uid!=os.getuid() or before.st_nlink!=1 or before.st_mode&0o022 or before.st_size>limit:raise ValueError('Bounded stable current metadata')\n fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)\n try:\n  opened=os.fstat(fd);chunks=[];total=0\n  while True:\n   b=os.read(fd,1048576)\n   if not b:break\n   total+=len(b)\n   if total>limit:raise ValueError('Whole preliminary Trace metadata80MiB not yet adopted')\n   chunks.append(b)\n  ended=os.fstat(fd)\n finally:os.close(fd)\n after=p.lstat();ident=lambda s:(s.st_dev,s.st_ino,s.st_uid,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns)\n if ident(before)!=ident(opened) or ident(opened)!=ident(ended) or ident(ended)!=ident(after):raise ValueError('Current metadata changed during read')\n return b''.join(chunks)\na=json.loads(pathlib.Path(sys.argv[1]).read_bytes())['structuredContent'];a=a.get('result',a);ts=a['transfers'];assert not a.get('unavailable_items') and len(ts)==4\nown=next(x for x in ts if x['library_file_id']=='libfile_3ee8270f03d8819188e1de1f75c3d824');rawown=read_current133(own['workspace_path'],own);d=json.loads(rawown);v=dict(d);v['self_sha256']=None;assert d.get('native_id')=='6acfe37b-828c-83eb-b466-7670beb64ff2' and d.get('ownership',{}).get('owner')=='TraceHarbor V1' and d['ownership'].get('duplicate_trace_route_owners')==0 and streamed_hash158(v)==d['self_sha256'];k='native'+d['state'].split('_')[0][6:];ad=d[k]['direction'].get('grouped146_admission');assert ad and ad.get('contract')=='TRACE146_STATIC_TYPED_RUNTIME_V3' and 'ADMIT_TRACE146_STATIC_TYPED_RUNTIME_V3' in d[k]['direction']['body']\nroot=pathlib.Path(sys.argv[2]);raw=(root/'diagnostic108/manifest.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==ad['manifest_sha256'];m=json.loads(raw)\nfor n,p in m['source_files'].items():\n f=root/n;assert not pathlib.Path(n).is_absolute() and '..' not in pathlib.Path(n).parts;b=f.read_bytes();assert len(b)==p['bytes'] and hashlib.sha256(b).hexdigest()==p['sha256']\nsys.argv=[str(root/'diagnostic108/preflight127.py'),sys.argv[1],sys.argv[3]];runpy.run_path(str(root/'diagnostic108/preflight127.py'),run_name='__main__')`;
 for(let n=0;n<3;n++)use(c,'preflight/helper-original128/'+n,'CONTROLLER');use(c,'preflight/helper-original152/route','CONTROLLER');
 let r;try{r=await t.exec_command({cmd:'python -c '+q(code)+' '+q(c.p.captureDirectory+'/preflight-materialize.original.json')+' '+q(validated129.reviewedRoot)+' '+q(validated129.configPath),yield_time_ms:1000,max_output_tokens:4000});}catch(error){r={tool_throw:{name:error?.name,message:String(error)},status:'UNKNOWN_NO_RETRY'};}
 const verified=await collectPreflight128(r,{tools:t,deadlineUtcMs:preflightDeadline128,claim:id=>use(c,id,'CONTROLLER'),retain:(name,original)=>capture(c,name,original,t)});
 if(verified.schema!=='TRACE133_NATIVE_PREFLIGHT_ORIGINAL_V2'||verified.inventory_sha256!==validated129.inventorySha256||!same(verified.current_admission,validated129.currentNativeAdmission))throw Error('Actual exact whole inventory/current contract');
 if(!/^V29-TRACE-152-/.test(verified.directionId)||verified.prestart154?.schema!=='TRACE168_PRESTART152_PREDECESSOR151_V1'||verified.prestart154.empty!==true||!/^[a-f0-9]{64}$/.test(verified.prestart154.prepared_receipt_sha256))throw Error('Actual exact152 prepared child proof before source registry/start');
 requireStartup156(verified.startup156);
 const verifiedPreload={...validated129,startup156:verified.startup156,context:null,contextSha256:null,deadlineUtcMs:null,uiDispatchArgs:null,sourceSha:verified.sourceSha,sourceTree:verified.sourceTree,captureDirectory:verified.captureDirectory,transferRoot:verified.transferRoot,dispatchSource133:verified.dispatchSource,directionId133:verified.directionId,staticConfigSha256:verified.staticConfigSha256,manifestSha135:verified.manifestSha135,holderCommand:{cmd:'python '+q(validated129.reviewedRoot+'/diagnostic108/native127.py')+' '+q(validated129.configPath),tty:true,yield_time_ms:1000,max_output_tokens:262144}};
 const handle=prepare127(verifiedPreload,NATIVE_CALLER_SEAL127);for(const id of c.used)HANDLES.get(handle).used.add(id);
 const actual=HANDLES.get(handle);use(actual,'observer146/issue','CONTROLLER');use(actual,'observer146/issue-original','CONTROLLER');
 const binding={source_sha:verified.sourceSha,manifest_sha256:verified.manifestSha135,static_config_sha256:verified.staticConfigSha256,inventory_sha256:validated129.inventorySha256,direction_id:verified.directionId,realm:'SOURCE_ISSUED_CONTROL_DATA'};
 const cmd='python3 '+q(validated129.reviewedRoot+'/diagnostic108/observer146.py')+' issue '+q(JSON.stringify({root:verified.captureDirectory,binding,inventory:{observer_maximum:40,authority:false,rows:validated129.inventory.rows.filter(r=>r.owner==='OBSERVER')}}));
 const issued=await t.exec_command({cmd,yield_time_ms:10000,max_output_tokens:4000});await capture(actual,'observer146-issue-original.json',issued,t);if(issued.exit_code!==0||issued.session_id!=null)throw Error('Durable observer issue required before holder');actual.observer146=JSON.parse(issued.output);return handle;
}
export function reserveObserver127(){throw Error('Retired live-handle observer path: use durable outer146 before actual functions.wait');}
export function retainObserver127(){throw Error('Retired cross-isolate observer path');}
export function observerPlan146(handle){const c=HANDLES.get(handle);if(!c?.observer146)throw Error('Source issued plan before holder');return {...c.observer146,helper:c.p.reviewedRoot+'/diagnostic108/observer146.py'};}
async function capture(c,name,value,tools){
 const text=JSON.stringify(value);if(text.length>4194304)throw Error('Bounded whole original, no truncation/retry');
 return await tools.apply_patch('*** Begin Patch\n*** Add File: '+c.p.captureDirectory+'/'+name+'\n+'+text+'\n*** End Patch');
}
export function counts127(handle){const c=HANDLES.get(handle);if(!c)throw Error('Exact registry');return {whole_reserved:c.rows.size,controller_used:c.used.size,first_unknown:c.failed,current48_fit:c.rows.size<=48,native_authority:false};}
export const STARTUP156=Object.freeze({schema:'TRACE156_FINITE_FIRST_FRAME_STARTUP_V1',startup_max_ms:90000,budget_source:'EXISTING_PREPARE90_WITHIN_OUTER_WORK3000',provider_frame_ms:15000,phase_CAS_ms:75000,parent_ms:2340000,outer_total_s:3600,outer_work_s:3000,outer_reserve_s:600,extra_tickets:0,renewal:false,authority:false});
export function requireStartup156(value){if(!same(value,STARTUP156))throw Error('Exact source-verified startup contract, no supplied deadline');return STARTUP156;}
export function requireFrame168(f,now){
 const parts=f.inventory_call_id?.split('/')||[],metadata=['SOURCE_FREEZE','PRE_DISPATCH','ADMIT_CHAIN','ENCRYPTED_CHAIN','CONSUMED_CHAIN','TERMINAL'].includes(parts[0])&&parts.length===2&&((parts[1]==='CAS'&&f.op==='library_replace')||(parts[1]==='readback'&&f.op==='library_materialize'));
 const k=f.frame_contract168,end=Math.min(f.phase_deadline_utc_ms,f.runtime_binding133?.deadlineUtcMs??Infinity);
 if(!Number.isInteger(f.issued_utc_ms)||!Number.isInteger(f.deadline_utc_ms)||!k||Object.keys(k).sort().join(',')!=='kind,pair_deadline_utc_ms,schema'||k.schema!=='TRACE168_METADATA_PAIR75_V1'||now<f.issued_utc_ms)throw Error('Closed source frame168 origin');
 const expected=metadata?Math.min(f.issued_utc_ms+(parts[1]==='CAS'?50000:25000),end-(parts[1]==='CAS'?25000:0)):Math.min(f.issued_utc_ms+15000,end);
 if(k.kind!==(metadata?'METADATA_PAIR':'PROVIDER15')||k.pair_deadline_utc_ms!==(metadata?f.phase_deadline_utc_ms:null)||metadata&&end-f.issued_utc_ms>75000||expected!==f.deadline_utc_ms||expected<=f.issued_utc_ms||now>=expected)throw Error('Original pair75/provider15 cutoff; no renewal');
 return f;
}
export function bindPair168(pairs,f){
 if(f.frame_contract168.kind!=='METADATA_PAIR')return;
 const [phase,step]=f.inventory_call_id.split('/'),end=f.frame_contract168.pair_deadline_utc_ms;
 if(step==='CAS'){if(pairs.has(phase))throw Error('No same-phase metadata reset');pairs.set(phase,end);}
 else if(!pairs.has(phase)||pairs.get(phase)!==end)throw Error('Readback must share original CAS pair cutoff');
}
export function requireEmittedFrame156(frame,now){
 requireFrame168(frame,now);
 if(!frame||!Number.isInteger(frame.deadline_utc_ms)||!Number.isInteger(frame.phase_deadline_utc_ms)||!frame.runtime_binding133||!Number.isInteger(frame.runtime_binding133.deadlineUtcMs)||now>=Math.min(frame.deadline_utc_ms,frame.phase_deadline_utc_ms,frame.runtime_binding133.deadlineUtcMs))throw Error('Original emitted15s/phase75/parent2340 expired; no parse bypass or reset');
 return frame;
}
export async function launch127(handle,tools){
 const c=HANDLES.get(handle);if(!c||c.session!==null||c.p.realm!=='SYNTHETIC_SOURCE_ONLY'&&!c.observer146)throw Error('ONE source-bound holder with issued observer plan');
 if(c.p.realm!=='SYNTHETIC_SOURCE_ONLY'&&tools!==PLATFORM_TOOLS127)throw Error('No supplied native tool callback');
 use(c,'holder/start','CONTROLLER');use(c,'holder/start-original','CONTROLLER');
 c.startup156=requireStartup156(c.p.startup156);c.startupOrigin156=Date.now();c.streamCutoff143=c.startupOrigin156+c.startup156.startup_max_ms;
 let original;try{original=await tools.exec_command(c.p.holderCommand);}catch(e){original={tool_throw:{name:e?.name,message:String(e)},status:'UNKNOWN_NO_RETRY'};}
 await capture(c,'holder-start.original.json',original,tools);
 if(!Number.isInteger(original.session_id)||original.exit_code!=null){c.failed={holder_start:original};throw Error('No actual live sameholder; no retry');}c.session=original.session_id;return original;
}
async function bindSourceRuntime133(c,frame,tools){
 // This DATA comes only from the exact source holder's retained start original.
 // No exported function accepts a runtime dict to register native authority.
 requireEmittedFrame156(frame,Date.now());
 const b=frame.runtime_binding133,p=c.p;
 if(c.session===null||frame!==c.nativeFrame||frame.seq!==1||frame.inventory_call_id!=='SOURCE_FREEZE/CAS'||!b||b.schema!=='TRACE133_SOURCE_RUNTIME_FRAME'||b.static_config_sha256!==p.staticConfigSha256||b.sourceSha!==p.sourceSha||b.sourceTree!==p.sourceTree||b.context?.domain!=='TRACE133_TYPED_RUNTIME'||b.context.source_sha!==p.sourceSha||b.context.direction_id!==p.directionId133||!/^[a-f0-9]{64}$/.test(b.context.once_receipt_sha256)||!/^[a-f0-9]{64}$/.test(b.context_sha256)||!same(b.context,frame.context)||!Number.isInteger(b.deadlineUtcMs)||b.deadlineUtcMs<=Date.now()||b.deadlineUtcMs>Date.now()+2340000)throw Error('Actual source same invocation runtime binding; original900 only');
 if(b.manifestSha256!==p.manifestSha135||b.onceExpiresUtc!==b.deadlineUtcMs/1000||!Number.isInteger(b.coordinatorCutoffUtc)||b.coordinatorCutoffUtc<b.onceExpiresUtc)throw Error('Original source manifest/expiry/cutoff, no reset');
 const values136={source_sha:p.sourceSha,manifest_sha256:p.manifestSha135,once_receipt_sha256:b.context.once_receipt_sha256,once_expires_utc:String(b.onceExpiresUtc),coordinator_cutoff_utc:String(b.coordinatorCutoffUtc)};
 const git136=p.dispatchSource133.kind==='git_create136';
 if(b.dispatchKind136!==(git136?'git_create136':'browser135'))throw Error('Same fixed source dispatch kind');
 const expectedArgs=git136?gitCreateArgs136(p.dispatchSource133,values136):{code:renderDispatch135(p.dispatchSource133,values136)};
 if(!same(b.uiDispatchArgs,expectedArgs))throw Error('Static script plus actual newly produced once only');
 p.context=snapshotPlain129(b.context);p.contextSha256=b.context_sha256;p.deadlineUtcMs=b.deadlineUtcMs;p.uiDispatchArgs=snapshotPlain129(b.uiDispatchArgs);use(c,'observer146/runtime','CONTROLLER');await capture(c,'observer146-runtime.json',{scope:'SOURCE_ORIGINAL_RUNTIME_DATA',source_sha:b.sourceSha,manifest_sha256:b.manifestSha256,once_receipt_sha256:b.context.once_receipt_sha256,deadline_utc_ms:b.deadlineUtcMs,dispatch_args:b.uiDispatchArgs,run_id:null},tools);
}
function guardArgs(c,f){
 requireFrame168(f,Date.now());
 c.metadataPairs168??=new Map();bindPair168(c.metadataPairs168,f);
 const a=f.args,p=c.p,repo='Elinfiny/TraceHarbor',id=f.inventory_call_id;
 if(!p.inventory.remote_ids.includes(id)||f.inventory_sha256!==p.inventorySha256||!same(f.context,p.context)||f.seq!==c.nextSeq||f.schema!=='TRACE118_HOST_REQUEST'||Date.now()>=Math.min(f.deadline_utc_ms,f.phase_deadline_utc_ms,p.deadlineUtcMs))throw Error('Exact source/context/inventory/sequence/original parent');
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
 if(f.op==='github_fetch_workflow_run_artifacts'&&!new RegExp('^traceharbor-(recipient104|safe127|failure146)-'+a.run_id+'-1$').test(a.name))throw Error('Exact name-filtered artifact, not total run inventory');
 if(f.op==='github_download_workflow_artifact'&&a.artifact_id!==c.artifact)throw Error('Only actual preceding selected artifact');
}
async function publishPrepared150(c,frame,tools){
 const phase=frame.inventory_call_id.split('/')[0],prefix='prepared150/'+phase+'/',originals=[];
 for(const id of ['process','prepare','transfer','finalize','metadata','intent','helper-original','receipt','normalize','close'])use(c,prefix+id,'CONTROLLER');
 const quote=s=>"'"+String(s).replaceAll("'","'\\''")+"'";
 const cmd='python3 '+quote(c.p.reviewedRoot+'/diagnostic108/publication150.py')+' '+quote(c.p.configPath)+' '+quote(JSON.stringify(frame.args));
 let current;try{current=await tools.exec_command({cmd,yield_time_ms:10000,max_output_tokens:16000});}catch(e){current={tool_throw:{name:e?.name,message:String(e)},status:'UNKNOWN_NO_RETRY'};}
 originals.push(current);await capture(c,'prepared150-'+phase+'-exec0.original.json',current,tools);
 const session=current?.session_id;
 for(let n=0;current?.exit_code==null&&n<8;n++){
  if(current?.session_id!==session||!Number.isInteger(session)||Date.now()>=frame.deadline_utc_ms)throw Error('Prepared helper UNKNOWN: retained first result, no secondwrite/fallback');
  use(c,prefix+'poll/'+n,'CONTROLLER');use(c,prefix+'poll-original/'+n,'CONTROLLER');
  try{current=await tools.write_stdin({session_id:session,chars:'',yield_time_ms:1000,max_output_tokens:16000});}catch(e){current={tool_throw:{name:e?.name,message:String(e)},status:'UNKNOWN_NO_RETRY'};}
  originals.push(current);await capture(c,'prepared150-'+phase+'-poll'+n+'.original.json',current,tools);
 }
 // Raw original exec identity is carried intact, never impersonated as a
 // tools.library_replace result. Native normalizer150 validates terminalEOF,
 // complete helper stdout/peritem/version/localattrs before dependent effects.
 if(current?.exit_code!==0||current.session_id!=null||current.eof===false||Date.now()>=frame.deadline_utc_ms)throw Error('Prepared terminal unknown/late: no retry/direct fallback');
 const carrier150={schema:'TRACE150_AUTHENTIC_EXEC_CARRIER',request:frame.args,exec_originals:originals};
 utf8ByteCount129(JSON.stringify(carrier150),131072); // request<=262144 + carrier<=131072 + envelope4096 < original1MiB
 return carrier150;
}
export async function bridge127(handle,frame,tools){
 const c=HANDLES.get(handle);if(!c||c.failed)throw Error('Exact preloaded source registry/no UNKNOWN retry');
 if(c.p.realm!=='SYNTHETIC_SOURCE_ONLY'&&(tools!==PLATFORM_TOOLS127||frame!==c.nativeFrame))throw Error('Only original SAME actual source holder frame; no caller-supplied dict');
 if(c.p.realm!=='SYNTHETIC_SOURCE_ONLY'&&c.p.context===null)await bindSourceRuntime133(c,frame,tools);
 guardArgs(c,frame);
 const id=frame.inventory_call_id;
 for(const s of ['tool','canonical','callback','callback-original'])use(c,id+'/'+s,'CONTROLLER');
 let original=null,error=null;const a=frame.args;
 try{switch(frame.op){
  case 'github_ref_absence136':{
   use(c,'authority152/precreate/current-tool','CONTROLLER');
   const settled=await Promise.allSettled([tools.mcp__codex_apps__github_fetch(a),tools.mcp__codex_apps__library_prepare_materialize({items:[{library_file_id:'libfile_3ee8270f03d8819188e1de1f75c3d824'},{library_file_id:'libfile_f87a6a307f70819194e0af0fa453afd1'},{library_file_id:'libfile_6f69ae483b088191a1fffefca617bbd5'},{library_file_id:'libfile_8377022600088191993dc06bfba93b7b'}],destination:{directory:c.p.transferRoot+'/authority152-current'}})]);
   original={schema:'TRACE152_AUTHENTIC_COMPOUND_ORIGINAL',absence:settled[0].status==='fulfilled'?settled[0].value:{tool_throw:{message:String(settled[0].reason)}},current:settled[1].status==='fulfilled'?settled[1].value:{tool_throw:{message:String(settled[1].reason)}},native_authority:false};break;
  }
  case 'github_create_dispatch136':original=await tools.mcp__codex_apps__github_create_branch(a);break;
  case 'github_fetch':{
   if(/^(admit|encrypted|consumed)\/(blob|tree|commit)\/proof$/.test(id)){
    use(c,'authority152/'+id+'/current-tool','CONTROLLER');
    const pair=await Promise.allSettled([tools.mcp__codex_apps__github_fetch(a),tools.mcp__codex_apps__library_prepare_materialize({items:[{library_file_id:'libfile_3ee8270f03d8819188e1de1f75c3d824'},{library_file_id:'libfile_f87a6a307f70819194e0af0fa453afd1'},{library_file_id:'libfile_6f69ae483b088191a1fffefca617bbd5'},{library_file_id:'libfile_8377022600088191993dc06bfba93b7b'}],destination:{directory:c.p.transferRoot+'/authority152-'+id.replaceAll('/','-')}})]);
    original={schema:'TRACE152_AUTHENTIC_READ_PAIR',value:pair[0].status==='fulfilled'?pair[0].value:{tool_throw:{message:String(pair[0].reason)}},current:pair[1].status==='fulfilled'?pair[1].value:{tool_throw:{message:String(pair[1].reason)}},native_authority:false};
   }else original=await tools.mcp__codex_apps__github_fetch(a);break;
  }
  case 'github_create_blob':original=await tools.mcp__codex_apps__github_create_blob(a);break;
  case 'github_create_tree':original=await tools.mcp__codex_apps__github_create_tree(a);break;
  case 'github_create_commit':original=await tools.mcp__codex_apps__github_create_commit(a);break;
  case 'github_create_ref':original=await tools.mcp__codex_apps__github_create_branch(a);break;
  case 'github_fetch_workflow_run_jobs':original=await tools.mcp__codex_apps__github_fetch_workflow_run_jobs(a);break;
  case 'github_fetch_workflow_run_artifacts':original=await tools.mcp__codex_apps__github_fetch({url:'https://api.github.com/repos/Elinfiny/TraceHarbor/actions/runs/'+a.run_id+'/artifacts?name='+encodeURIComponent(a.name)+'&per_page=100'});break;
  case 'github_download_workflow_artifact':original=await tools.mcp__codex_apps__github_download_workflow_artifact(a);break;
  case 'library_replace':original=await publishPrepared150(c,frame,tools);break;
  case 'library_materialize':{
   if(/^(ADMIT_CHAIN|ENCRYPTED_CHAIN|CONSUMED_CHAIN)\/readback$/.test(id)){
    const whole=await tools.mcp__codex_apps__library_prepare_materialize({...a,items:[...a.items,{library_file_id:'libfile_f87a6a307f70819194e0af0fa453afd1'},{library_file_id:'libfile_6f69ae483b088191a1fffefca617bbd5'},{library_file_id:'libfile_8377022600088191993dc06bfba93b7b'}]});
    original={schema:'TRACE152_AUTHENTIC_PHASE_READBACK',current:whole,native_authority:false};
   }else original=await tools.mcp__codex_apps__library_prepare_materialize(a);break;
  }
  case 'browser_js':original=await tools.mcp__codex_apps__browser_js(a);break;
  default:throw Error('No arbitrary tool/new route');
 }}catch(e){error={exception_class:e?.name||'Error',message:String(e?.message||e),status:'UNKNOWN_NO_RETRY'};}
 const identity={context_sha256:c.p.contextSha256,operation:frame.op,seq:frame.seq,tool:frame.op==='library_replace'?'exec_command':frame.op,call_id:frame.request_digest};
 // Exactly one canonical complete native result before ALL postguards. Alias
 // consumers use this exact file/count/hash; equal bytes of othercalls differ.
 if(error&&original===null)original={tool_throw:error,status:'UNKNOWN_NO_RETRY'};
 await capture(c,frame.seq+'.canonical-native-original.json',{identity,original},tools);
 let bound152=null;
 if(original?.schema?.startsWith('TRACE152_AUTHENTIC_')){try{utf8ByteCount129(JSON.stringify(original),131072);}catch(e){bound152={status:'UNKNOWN_NO_RETRY',message:String(e),whole_original_retained:true};}}
 const late=Date.now()>=Math.min(frame.deadline_utc_ms,c.p.deadlineUtcMs);
 const expected404136=frame.op==='github_ref_absence136'&&id==='dispatch136/ref-absence'&&original?.isError===true&&original.structuredContent?.error_code==='NOT_FOUND'&&String(original.structuredContent?.error_data?.status)==='404';
 if(error||late||bound152||original?.isError&&!expected404136)c.failed=error||bound152||{late,tool_error:original?.isError===true};
 if(!c.failed){const v=original?.structuredContent;
  if(/^dispatch136\/runs\/[0-3]$/.test(id)){const data=JSON.parse(v.content),matches=data.workflow_runs.filter(r=>r.head_branch===c.p.uiDispatchArgs.branch_name&&r.path==='.github/workflows/traceharbor-counter136.yml');if(matches.length===1){const run=matches[0];if(run.status==='in_progress'&&run.run_attempt===1&&run.head_sha===c.p.sourceSha&&run.actor?.id===273768139&&run.repository?.id===1391430317){use(c,'observer146/run','CONTROLLER');await capture(c,'observer146-run.json',{run_id:run.id,branch:run.head_branch,source_sha:run.head_sha,once_receipt_sha256:c.p.context.once_receipt_sha256,canonical_sequence:frame.seq},tools);}}}

  if(frame.op==='github_create_blob')c.lastBlob=v?.sha;
  if(frame.op==='github_create_tree')c.lastTree=v?.sha;
  if(frame.op==='github_create_commit')c.lastCommit=v?.sha;
  if(frame.op==='github_fetch_workflow_run_artifacts'){let av;try{av=JSON.parse(v.content);}catch{c.failed={artifact_body:true};}if(!c.failed){if(id.startsWith('recipient146/')&&av.total_count===0&&Array.isArray(av.artifacts)&&av.artifacts.length===0){}else if(av.total_count!==1||av.artifacts?.length!==1||av.artifacts[0].name!==a.name){c.failed={artifact_identity:true};}else c.artifact=av.artifacts[0].id;}}
 }
 const response={schema:'TRACE118_HOST_RETURN',seq:frame.seq,context:frame.context,op:frame.op,request_digest:frame.request_digest,original_result:original,transport_error:error,late:late||!!c.failed};
 c.streamIdle146=id.startsWith('collection/run/')?310000:id.startsWith('recipient146/')?55000:0;
 c.streamCutoff143=Math.min(Date.now()+(c.streamIdle146||15000),c.streamIdle146?frame.phase_deadline_utc_ms:frame.deadline_utc_ms,c.p.deadlineUtcMs);
 // Absolute source phase/parent is additionally bound by the next frame and
 // native holder; this ordinary collection cannot renew the runtime parent.
 let terminal;try{terminal=await tools.write_stdin({session_id:c.session,chars:JSON.stringify(response)+'\n',yield_time_ms:1000,max_output_tokens:262144});}catch(e){terminal={tool_throw:{name:e?.name,message:String(e)},status:'UNKNOWN_NO_RETRY'};c.failed??=terminal;}
 await capture(c,frame.seq+'.canonical-callback-original.json',terminal,tools);c.nextSeq++;
 if(c.failed)throw Error('First original/exception retained; entire phase non-retriable');return terminal;
}
export async function collectHolderStream143(handle,first,tools,window){
 const c=HANDLES.get(handle),deadline=c?.streamCutoff143;
 if(!c||c.failed||!['launch',...c.p.inventory.remote_ids].includes(window)||!Number.isInteger(deadline))throw Error('One source-owned original stream window');
 let response=first,output='',verified=null,primary=null;const chunks=new Set(),identities=[];
 try{
  const maximumReads=c.streamIdle146?12:8;
  for(let n=0;n<=maximumReads;n++){
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
   if(n===maximumReads)throw Error('Finite precommitted146 source-stream reads exhausted; no retry');
   use(c,'stream143/'+window+'/poll/'+n,'CONTROLLER');
   try{response=await tools.write_stdin({session_id:c.session,chars:'',yield_time_ms:c.streamIdle146?30000:1000,max_output_tokens:262144});}
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
   const frame=JSON.parse(lines[0]);if(window==='launch')requireEmittedFrame156(frame,Date.now());c.nativeFrame=frame;window=frame.inventory_call_id;original=await bridge127(handle,frame,tools);c.nativeFrame=null;
  }
  throw Error('Finite complete macro stream exhausted; no retry');
 }catch(error){c.failed??={name:error?.name,message:String(error)};use(c,'controller/failure143','CONTROLLER');await capture(c,'controller-failure143.original.json',{failure:c.failed,error:{name:error?.name,message:String(error)}},tools);throw error;}
 finally{use(c,'controller/final146','CONTROLLER');await capture(c,'controller-final146.original.json',{plan_sha256:c.observer146?.plan_sha256||null,source_sha:c.p.sourceSha,context:c.p.context,controller_used_ticket_ids:[...c.used],first_unknown:c.failed,native_authority:false},tools);}
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
