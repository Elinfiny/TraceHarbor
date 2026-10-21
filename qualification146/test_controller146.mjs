// NEW changed controller paths with explicit inert fixture tools. No platform calls.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {prepare127,launch127,bridge127,collectHolderStream143,counts127,snapshotPlain129,reserveObserver127} from '../diagnostic108/caller127.mjs';
const inventory=JSON.parse(fs.readFileSync(new URL('./current_inventory146.json',import.meta.url)));
function setup(op='github_fetch',id='collection/run/0',artifactBody=null){
 const source='a'.repeat(40),context={domain:'SYNTHETIC146',source_sha:source};let calls=[],captures=[],polls=[];
 const p={realm:'SYNTHETIC_SOURCE_ONLY',inventory,inventorySha256:'1'.repeat(64),sourceSha:source,sourceTree:'b'.repeat(40),context,contextSha256:'2'.repeat(64),deadlineUtcMs:Date.now()+2340000,captureDirectory:'/SYNTHETIC146/capture',transferRoot:'/SYNTHETIC146/transfer',holderCommand:{cmd:'INERT_FIXTURE_NO_EXECUTION'}};
 const h=prepare127(p);const tools={exec_command:async()=>({session_id:99,output:'',chunk_id:'start',original_token_count:0}),apply_patch:async x=>{captures.push(x);return {};},mcp__codex_apps__github_fetch:async a=>{calls.push(a);return {structuredContent:{content:JSON.stringify(artifactBody||{id:77,status:'in_progress'})},isError:false};},write_stdin:async a=>{polls.push(a);return a.chars?{session_id:99,output:'',chunk_id:'callback',original_token_count:0}:{output:'DONE\n',exit_code:0,chunk_id:'terminal',original_token_count:1};}};
 const args=op==='github_fetch'?{url:'https://api.github.com/repos/Elinfiny/TraceHarbor/actions/runs/77'}:{repo_full_name:'Elinfiny/TraceHarbor',run_id:77,name:'traceharbor-recipient104-77-1'};
 const frame={schema:'TRACE118_HOST_REQUEST',seq:1,context,op,args,inventory_call_id:id,inventory_sha256:p.inventorySha256,deadline_utc_ms:Date.now()+15000,phase_deadline_utc_ms:Date.now()+1020000,phase_deadline_mono:5000,request_digest:'3'.repeat(64)};
 return {h,tools,frame,calls,captures,polls};
}
let n=0;
{
 const f=setup();await launch127(f.h,f.tools);const first=await bridge127(f.h,f.frame,f.tools);const result=await collectHolderStream143(f.h,first,f.tools,'collection/run/0');assert.equal(result.exit_code,0);assert.equal(f.polls.at(-1).yield_time_ms,30000);assert(f.captures.some(x=>x.includes('canonical-native-original')));assert.equal(counts127(f.h).first_unknown,null);n++;
}
{
 const body={total_count:0,artifacts:[]};const f=setup('github_fetch_workflow_run_artifacts','recipient146/list/0',body);await launch127(f.h,f.tools);await bridge127(f.h,f.frame,f.tools);assert.equal(f.calls[0].url,'https://api.github.com/repos/Elinfiny/TraceHarbor/actions/runs/77/artifacts?name=traceharbor-recipient104-77-1&per_page=100');assert.equal(counts127(f.h).first_unknown,null);n++;
}
{
 const f=setup('github_fetch_workflow_run_artifacts','recipient146/list/0',{artifacts:[]});await launch127(f.h,f.tools);await assert.rejects(()=>bridge127(f.h,f.frame,f.tools));assert.equal(f.calls.length,1);assert(f.captures.some(x=>x.includes('artifacts')));await assert.rejects(()=>bridge127(f.h,f.frame,f.tools));assert.equal(f.calls.length,1);n++;
}
{
 const f=setup();assert.throws(()=>snapshotPlain129(f.h));assert.throws(()=>reserveObserver127({...f.h},0,'clone'));n++;
}
console.log(JSON.stringify({scope:'SYNTHETIC_CHANGED_CONTROLLER_INTERFACES_ONLY',cases:n,passed:n,native_calls:0}));
