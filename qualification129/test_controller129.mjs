//129 only: four finite NEW cases in actual functions.exec; no provider effects.
function assert129(condition,message){if(!condition)throw Error(message);}
function refuse129(operation,label){let refused=false;try{operation();}catch{refused=true;}assert129(refused,'Expected refusal: '+label);return label;}
export async function runCase129(id,api,inventory,fixture){
 const absent={TextEncoder:typeof TextEncoder,TextDecoder:typeof TextDecoder,structuredClone:typeof structuredClone};
 assert129(absent.TextEncoder==='undefined'&&absent.TextDecoder==='undefined'&&absent.structuredClone==='undefined','Actual admitted controller absence must remain observed; no polyfill');
 if(id===1){
  const shared={tag:'nou129-șț-🧭',fraction:1234.125};const input={schema:'NEW129_PLAIN_CONFIG',nested:{enabled:false,missing:null,number:-0,small:0.125},first:shared,second:shared,array:[0,true,'română',null,{k:2}]};
  const result=api.snapshotPlain129(input);assert129(result!==input&&result.nested!==input.nested&&result.array!==input.array&&result.first!==shared&&result.first===result.second,'Independent deep copy and shared aliases');
  assert129(Object.is(result.nested.number,-0)&&result.nested.small===0.125&&result.first.fraction===1234.125&&result.nested.missing===null&&result.nested.enabled===false&&result.array[2]==='română','All values/types/fractional and negativezero preserved');
  result.first.tag='changed-copy-only';assert129(shared.tag==='nou129-șț-🧭','Input unchanged');
  const frozen=Object.freeze({frozen:true});assert129(api.snapshotPlain129(frozen).frozen===true,'Frozen plain data allowed');
  let getterCalls=0;const accessor={};Object.defineProperty(accessor,'x',{enumerable:true,get(){getterCalls++;return 1;}});const cyc={};cyc.self=cyc;const symbolKey={};symbolKey[Symbol('new129')]=1;const hidden={};Object.defineProperty(hidden,'hidden',{value:2});const sparse=new Array(1);const extra=[];extra.extra=1;
  const handle=api.prepare127({realm:'SYNTHETIC_SOURCE_ONLY',inventory:{rows:[],inclusive_total:0,authority:false}});
  const vectors=[['NaN',{x:NaN}],['positiveInfinity',{x:Infinity}],['negativeInfinity',{x:-Infinity}],['undefined',{x:undefined}],['function',{x:()=>1}],['symbolValue',{x:Symbol('value129')}],['BigInt',{x:129n}],['accessor',accessor],['customPrototype',Object.create({inherited:1})],['nullPrototype',Object.create(null)],['cycle',cyc],['symbolKey',symbolKey],['hiddenProperty',hidden],['sparseArray',sparse],['arrayExtraProperty',extra],['opaqueRegisteredHandle',{nested:handle}],['MapType',new Map([['x',1]])],['Uint8ArrayType',new Uint8Array([1,2])]];
  const rejected=vectors.map(([name,value])=>refuse129(()=>api.snapshotPlain129(value),name));assert129(getterCalls===0,'Accessor must not execute');assert129(api.counts127(handle).native_authority===false,'No opaque handle promotion');
  let deep={};for(let n=0;n<66;n++)deep={child:deep};rejected.push(refuse129(()=>api.snapshotPlain129(deep),'depthBound'));rejected.push(refuse129(()=>api.snapshotPlain129(new Array(8193).fill(null)),'arrayBound'));rejected.push(refuse129(()=>api.snapshotPlain129({text:'A'.repeat(2097153)}),'UTF8ConfigBound'));
  assert129(rejected.join('|')===fixture.case1_rejected.join('|'),'Exact precommitted case1 input inventory');
  return {case:1,actual_controller:absent,valid_plain_config:'VALUE_TYPE_ALIAS_COPY_PASS',rejected,getter_calls:getterCalls,native_registration:0,real_tools_called_by_case:0};
 }
 if(id===2){
  const results=[];
  for(const vector of fixture.utf8_vectors){
   const value=vector.text??vector.unit.repeat(vector.repeat);
   if(vector.expected_bytes>vector.limit){refuse129(()=>api.utf8ByteCount129(value,vector.limit),vector.id);results.push({id:vector.id,expected_bytes:vector.expected_bytes,limit:vector.limit,result:'OVERLIMIT_REFUSED'});}
   else{const observed=api.utf8ByteCount129(value,vector.limit);assert129(observed===vector.expected_bytes,'Exact independent UTF8 fixture '+vector.id);results.push({id:vector.id,expected_bytes:vector.expected_bytes,observed_bytes:observed});}
  }
  return {case:2,actual_controller:absent,fixture_scope:'INDEPENDENT_PUBLIC_UTF16_SCALAR_REPLACEMENT_UTF8_COUNTS',results,native_registration:0,real_tools_called_by_case:0};
 }
 if(id===3){
  const config={realm:'SYNTHETIC_SOURCE_ONLY',inventory,inventorySha256:fixture.inventory_sha256,context:{scope:'NEW129_ACTUAL_CONTROLLER_SYNTHETIC'},contextSha256:'9'.repeat(64),sourceSha:'8'.repeat(40),sourceTree:'7'.repeat(40),deadlineUtcMs:60000.875,captureDirectory:'/NEW129/SYNTHETIC_ONLY',transferRoot:'/NEW129/TRANSFER',holderCommand:{cmd:'NOT_EXECUTED'},fractional_fact:0.375};
  const handle=api.prepare127(config);config.inventory.rows[0].id='MUTATED_ORIGINAL_ONLY';const count=api.counts127(handle);assert129(count.whole_reserved===1366&&count.controller_used===0&&count.native_authority===false,'Complete source prepare inventory clone and no authority');
  const response={schema:'TRACE129_NEW_SYNTHETIC_PREFLIGHT',fraction:0.375,source:'NEW_CASE3_ONLY'};const output=JSON.stringify(response),split1=17,split2=49,retained=[],claims=new Set();let calls=0,clock=1000.125;
  const originals=[{chunk_id:'new129-c3-0',session_id:12903,output:output.slice(0,split1)},{chunk_id:'new129-c3-1',session_id:12903,output:output.slice(split1,split2)},{chunk_id:'new129-c3-2',exit_code:0,output:output.slice(split2),eof:true}];
  const synthetic={write_stdin:async args=>{assert129(args.session_id===12903&&args.chars==='','SAME synthetic session and empty finite poll');clock+=0.375;return originals[++calls];}};
  const result=await api.collectPreflight128(originals[0],{tools:synthetic,deadlineUtcMs:45000.875,now:()=>clock,claim:id=>{assert129(!claims.has(id),'Unique shared inventory ticket');claims.add(id);},retain:async(name,original)=>{retained.push({name,original});}});
  assert129(JSON.stringify(result)===output&&calls===2&&retained.length===4,'ONE complete structured JSON after terminal');
  for(let n=0;n<3;n++)assert129(retained[n].original.original===originals[n]&&retained[n].original.identity.index===n,'Exact complete first/poll original and collection order');
  for(const ticket of claims)assert129(inventory.rows.some(row=>row.id===ticket&&row.owner==='CONTROLLER'),'All existing preflight inventory includes call/original/closure '+ticket);
  assert129(retained[3].original.terminal_verified===true&&retained[3].original.registration===false&&retained[3].original.output===output,'Complete collector close original');
  return {case:3,actual_controller:absent,prepare:count,source_inventory_rows:inventory.rows.length,synthetic_polls:calls,originals:retained,tickets:[...claims],fractional_walltime_preserved:clock,native_registration:0,actual_exec_materialize_provider_CAS:0};
 }
 if(id===4){
  const base='{"schema":"NEW129_NEGATIVE"}',first=(name,output='{"schema":')=>({chunk_id:name+'-first',session_id:12904,output});const last=(name,output,extra={})=>({chunk_id:name+'-last',output,exit_code:0,...extra});
  const specs=[
   {id:'malformed',first:first('malformed'),polls:[last('malformed','"NEW129_NEGATIVE"}junk')]},
   {id:'duplicate',first:first('duplicate'),polls:[{chunk_id:'duplicate-first',output:'"NEW129_NEGATIVE"}',exit_code:0}]},
   {id:'outOfOrderContent',first:first('order'),polls:[{chunk_id:'order-reordered',session_id:12904,output:'}'},last('order','"NEW129_NEGATIVE"')]},
   {id:'sessionDrift',first:first('drift'),polls:[{chunk_id:'drift-next',session_id:12905,output:''}]},
   {id:'late',first:first('late'),polls:[last('late','"NEW129_NEGATIVE"}')],late:true},
   {id:'nonzero',first:first('nonzero'),polls:[last('nonzero','"NEW129_NEGATIVE"}',{exit_code:7})]},
   {id:'overbyte',first:first('overbyte','ă'.repeat(131073)),polls:[]},
   {id:'earlyEOF',first:{chunk_id:'eof-first',output:'{}',session_id:12904,eof:true},polls:[]},
   {id:'incompleteFinite',first:first('finite'),polls:[],exhaust:true},
   {id:'firstPrimaryAndCleanup',first:last('cleanup','not-json'),polls:[],cleanup:true}
  ];
  assert129(specs.map(s=>s.id).join('|')===fixture.case4_vectors.join('|'),'Exact precommitted negative vector inventory');const results=[];
  for(const spec of specs){
   let clock=1000.625,calls=0,caught=null;const retained=[],claims=new Set(),originals=[spec.first];
   const synthetic={write_stdin:async args=>{assert129(args.session_id===12904&&args.chars==='','SAME source session');clock=spec.late?47000.875:clock+0.125;const value=spec.polls[calls]??{chunk_id:spec.id+'-finite-'+calls,session_id:12904,output:''};calls++;originals.push(value);return value;}};
   try{await api.collectPreflight128(spec.first,{tools:synthetic,deadlineUtcMs:45000.875,now:()=>clock,claim:id=>{assert129(!claims.has(id),'No ticket replay');claims.add(id);},retain:async(name,original)=>{retained.push({name,original});if(spec.cleanup&&name==='preflight-collection128.original.json')throw Error('NEW129_SEPARATE_CLEANUP_FAILURE');}});}catch(error){caught={name:error.name,message:error.message,stack:error.stack,errors:error.errors??null};}
   assert129(caught&&calls<=8&&retained.length>=2,'Negative refuses with complete first original and finite budget '+spec.id);
   assert129(retained[0].original.original===spec.first&&retained[retained.length-1].original.primary,'First complete original and primary retained before later cleanup');
   if(spec.exhaust)assert129(calls===8,'Exactly eight precommitted polls before finite refusal');
   if(spec.cleanup)assert129(caught.name==='AggregateError'&&caught.errors.length===2&&retained[retained.length-1].original.primary.name==='SyntaxError'&&caught.errors[1].message.includes('NEW129_SEPARATE_CLEANUP_FAILURE'),'First primary and separate later cleanup retained');
   // Overbyte fixture original stays complete: record its exact size/count,
   // not a prefix as a success record. Complete original is retained in memory
   // and in this case's full structured stdout below.
   results.push({id:spec.id,polls:calls,originals:retained,error:caught,registration:false,exec_retry:0});
  }
  return {case:4,actual_controller:absent,scope:'ACTUAL_MODIFIED_COLLECTOR_EXPLICIT_SYNTHETIC_TOOLS',results,native_registration:0,actual_exec_materialize_provider_CAS:0};
 }
 throw Error('Only four precommitted cases');
}
