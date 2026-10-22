// NEW Q168A-JS pure source guards. Fixture timestamps, never live originals.
import {requireFrame168} from './caller127.mjs';
const rows=[];
function test(name,f){f();rows.push({case:name,status:'PASS',scope:'SYNTHETIC_SOURCE_ONLY_NOT_PROVIDER_EVIDENCE'});}
function refuse(f){let yes=false;try{f();}catch{yes=true;}if(!yes)throw Error('Expected refusal');}
const f=(op='library_replace',id='SOURCE_FREEZE/CAS',issued=0,end=75000)=>({inventory_call_id:id,op,issued_utc_ms:issued,deadline_utc_ms:Math.min(issued+(op==='library_replace'?50000:25000),end-(op==='library_replace'?25000:0)),phase_deadline_utc_ms:end,frame_contract168:{schema:'TRACE168_METADATA_PAIR75_V1',kind:'METADATA_PAIR',pair_deadline_utc_ms:end}});
test('source_metadata_success_after15_before_pair75',()=>requireFrame168(f(),20000));
test('pair75_cutoff_refused',()=>refuse(()=>requireFrame168(f('library_materialize','SOURCE_FREEZE/readback',60000),75001)));
test('caller_supplied_longer_publish_scalar_refused',()=>refuse(()=>requireFrame168({...f(),deadline_utc_ms:75000},20000)));
test('retired_metadata_route_no_longer_window',()=>refuse(()=>requireFrame168(f('library_replace','RETIRED/CAS'),20000)));
test('Git_not_promoted_to_metadata',()=>refuse(()=>requireFrame168(f('github_create_blob','admit/blob'),20000)));
test('original_before_issue_refused',()=>refuse(()=>requireFrame168(f('library_replace','SOURCE_FREEZE/CAS',10000),9000)));
console.log(JSON.stringify({schema:'Q168A_NEW_FIRST_SOURCE_ONLY_JS',status:'PASS',cases:rows,native_bootstrap_mint_registry_clock_child:0,provider_calls:0}));
