import assert from 'node:assert/strict';
import {collectPreflight128,PREFLIGHT128,bootstrapActualCaller127} from '../diagnostic108/caller127.mjs';
const row=(id,output,extra={})=>({chunk_id:id,output,...extra});
async function fixture(name,first,polls,accept=false,late=false){
 const retained=[],claimed=new Set();let count=0,clock=1000,exec=0;const tools={exec_command:async()=>{exec++;throw Error('No retry');},write_stdin:async args=>{assert.equal(args.session_id,876);assert.equal(args.chars,'');if(late)clock=50000;return polls[count++]??row('exhaust-'+count,'',{session_id:876});}};
 let passed=false,error=null;
 try{const result=await collectPreflight128(first,{tools,deadlineUtcMs:46000,now:()=>clock,claim:id=>{assert(!claimed.has(id));claimed.add(id);},retain:async(name,value)=>{retained.push({name,value});}});assert.deepEqual(result,{schema:'TRACE128_SYNTHETIC'});passed=true;}catch(e){error=String(e);}
 assert.equal(passed,accept,name);assert.equal(exec,0);assert(count<=PREFLIGHT128.polls);assert(retained[0].value.original===first);assert.equal(retained.at(-1).name,'preflight-collection128.original.json');assert.equal(retained.at(-1).value.registration,false);
 return {name,accepted:passed,polls:count,complete_originals:retained.length,exec_retry:exec,error,registration:false};
}
const first=()=>row('first','{"sche',{session_id:876});
const results=[];
results.push(await fixture('SAME_SESSION_CHUNKS_TERMINAL0',first(),[row('second','ma":"TRACE128_',{session_id:876}),row('third','SYNTHETIC"}',{exit_code:0})],true));
results.push(await fixture('MALFORMED_NO_PREFIX',first(),[row('last','ma":"TRACE128_SYNTHETIC"}junk',{exit_code:0})]));
results.push(await fixture('LATE_TERMINAL_REFUSED',first(),[row('last','ma":"TRACE128_SYNTHETIC"}',{exit_code:0})],false,true));
results.push(await fixture('NONZERO_REFUSED',first(),[row('last','ma":"TRACE128_SYNTHETIC"}',{exit_code:3})]));
results.push(await fixture('EARLY_EOF_REFUSED',row('first','{}',{session_id:876,eof:true}),[]));
results.push(await fixture('DUPLICATE_CHUNK_ORDER_REFUSED',first(),[row('first','ma":"TRACE128_SYNTHETIC"}',{exit_code:0})]));
results.push(await fixture('SESSION_DRIFT_REFUSED',first(),[row('second','',{session_id:877})]));
results.push(await fixture('INCOMPLETE_FINITE_MAXIMUM',first(),[]));
results.push(await fixture('TERMINAL_EOF_FALSE_REFUSED',first(),[row('last','ma":"TRACE128_SYNTHETIC"}',{exit_code:0,eof:false})]));
await assert.rejects(bootstrapActualCaller127({}),/Actual platform lexical tools unavailable/);
console.log(JSON.stringify({case:3,scope:'EXPLICIT_SYNTHETIC_TOOLS_ACTUAL_MODIFIED_COLLECTOR',results,native_registration:0,old_cases_rerun:0}));
