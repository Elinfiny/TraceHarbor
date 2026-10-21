// OBSERVER-owned DATA protocol, never a native factory or a cloned live handle.
const q146=s=>"'"+s.replaceAll("'","'\"'\"'")+"'";
export async function observerCall146(helper,verb,args,tools,retain){
 if(!['issue','reserve','retain','verify'].includes(verb)||!helper.endsWith('/diagnostic108/observer146.py'))throw Error('Closed source observer helper');
 const original=await tools.exec_command({cmd:'python3 '+q146(helper)+' '+q146(verb)+' '+q146(JSON.stringify(args)),yield_time_ms:10000,max_output_tokens:4000});
 await retain(verb,original); // whole native original precedes exit/schema guards
 if(original.exit_code!==0||original.session_id!=null||original.original_token_count>4000)throw Error('Observer helper unresolved; no actual wait/replay');
 const data=JSON.parse(original.output);if(data.native_authority===true)throw Error('Observer DATA cannot grant native authority');return data;
}
export async function claimActualWait146(issued,actualCellId,actualYieldOriginal,tools,retain){
 return observerCall146(issued.helper,'reserve',{root:issued.root,plan_sha256:issued.plan_sha256,cell_id:actualCellId,yield_original:actualYieldOriginal},tools,retain);
}
export async function retainActualWait146(issued,ticket,actualWaitOriginal,tools,retain){
 return observerCall146(issued.helper,'retain',{root:issued.root,plan_sha256:issued.plan_sha256,ticket,original:actualWaitOriginal},tools,retain);
}
export const OUTER146_SEQUENCE=Object.freeze([
 'Verified source caller issues durable plan from exact admitted inventory before holder/clock. All80 OBSERVER tickets precommitted; opaque native registry unchanged.',
 'Only actual functions.exec yielded original supplies cell ID. Outer exec calls claimActualWait146 against issued anchored plan; full helper original retained BEFORE exit guards.',
 'After successful durable reservation only, call the real functions.wait in its own tool channel with returned args. There is no invented tools.functions_wait.',
 'Next outer exec calls retainActualWait146 with exact preceding ticket/full tool original, then verifies durable ledger. No attempt to mutate live HANDLES through functions.store.',
 'The caller final envelope combines disjoint controller/observer/host tickets, source runtime original and actual selected run. Observer DATA never substitutes for typed native source/SAFE authority.'
]);
