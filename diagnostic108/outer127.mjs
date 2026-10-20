// Concrete OUTER tool caller binding. These source methods run in the model's
// code-mode cells, outside the still-running driver isolate. Same precommitted
// inventory, disjoint OBSERVER ownership; no second cap or Python interception.
export function prepareOuter127(inventory,binding){
 if(inventory.observer_maximum!==16||inventory.authority!==false||!binding.context_sha256||!binding.capture_directory)throw Error('Exact preloaded whole inventory/binding');
 return {schema:'TRACE127_OUTER_CALLER_V1',inventory,binding,next:0,cell_id:null,pending:null,used:[],originals:[],first_unknown:null};
}
export async function claimActualWait127(state,actualYieldedCellId,tools){
 if(state.schema!=='TRACE127_OUTER_CALLER_V1'||state.first_unknown||state.pending||state.next>=16||typeof actualYieldedCellId!=='string'||!actualYieldedCellId||state.cell_id&&state.cell_id!==actualYieldedCellId)throw Error('Only SAME actual yielded exec; finite no replay');
 const n=state.next++,ids=['observer/'+n+'/claim-cell','observer/'+n+'/intent','observer/'+n];
 for(const id of ids){const row=state.inventory.rows.find(x=>x.id===id);if(!row||row.owner!=='OBSERVER'||state.used.includes(id))throw Error('Exact shared precommitted observer ticket');state.used.push(id);}
 state.cell_id=actualYieldedCellId;state.pending={index:n,cell_id:actualYieldedCellId,context_sha256:state.binding.context_sha256,pre_reserved_before_actual_wait:true};
 await tools.apply_patch('*** Begin Patch\n*** Add File: '+state.binding.capture_directory+'/observer-'+n+'.wait-intent.json\n+'+JSON.stringify(state.pending)+'\n*** End Patch');
 // Actual caller MUST store updated state using functions.store BEFORE this
 // call returns, then issue exactly functions.wait(args) in the outer tool
 // channel. No functions.wait API is invented under tools inside an exec.
 return {tool:'functions.wait',args:{cell_id:actualYieldedCellId,yield_time_ms:60000,max_tokens:4000},ticket:{...state.pending}};
}
export async function retainActualWait127(state,ticket,actualWaitOriginal,tools){
 if(!state.pending||ticket.index!==state.pending.index||ticket.cell_id!==state.cell_id||ticket.context_sha256!==state.binding.context_sha256)throw Error('Actual preceding reserved wait only');
 for(const suffix of ['original-cell','original']){const id='observer/'+ticket.index+'/'+suffix;if(state.used.includes(id)||!state.inventory.rows.some(x=>x.id===id&&x.owner==='OBSERVER'))throw Error('No duplicate observer original/cell');state.used.push(id);}
 const record={identity:ticket,original:actualWaitOriginal};
 await tools.apply_patch('*** Begin Patch\n*** Add File: '+state.binding.capture_directory+'/observer-'+ticket.index+'.canonical-original.json\n+'+JSON.stringify(record)+'\n*** End Patch');state.originals.push(record);state.pending=null;return record;
}
export const OUTER127_ACTUAL_SOURCE_SEQUENCE=Object.freeze([
 'Before original protected clock: store(outerKey,prepareOuter127(EXACT_WHOLE_INVENTORY,EXACT_BINDING)); preload all closed driver code/calls; functions.exec driver ONCE.',
 'Only after actual Script running with cell ID: in one functions.exec cell load outerKey, await claimActualWait127(state,ACTUAL_CELL_ID,tools), store updated state BEFORE returning args.',
 'Call the real functions.wait exactly with returned args in the tool channel. Never resend functions.exec/holder/callback when a wait yields.',
 'Next functions.exec cell: load state, await retainActualWait127(state,EXACT_TICKET,COMPLETE_ACTUAL_WAIT_ORIGINAL,tools), store state before any parse/postguard. Repeat only next unused finite ticket if actual cell remains running.',
 'Final caller envelope combines controller originals, exact holder terminal and outer records by shared ticket IDs; unused tickets are committed capacity, never refunded. No background or new actor.'
]);
