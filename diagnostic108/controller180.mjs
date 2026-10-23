// Actual source180 orchestration: outer RX -> existing typed caller -> outer TERMINAL.
import {bootstrapActualCaller127,observerPlan146,drive127,outerConsumer180} from './caller180.mjs';
export async function runControlled146(preloaded){
 if(typeof notify!=='function'||typeof tools!=='object'||!preloaded?.outer180)throw Error('Actual lexical surface and complete outer180 descriptors required');
 const rx=await outerConsumer180(preloaded.outer180.RX_START,tools);
 const handle=await bootstrapActualCaller127(preloaded);const issued=observerPlan146(handle);notify({schema:'TRACE146_SOURCE_ISSUED_OBSERVER_PLAN',issued,native_authority:false});
 let original=null,error=null;
 try{original=await drive127(handle,tools);}catch(e){error={name:e?.name,message:String(e)};}
 const terminal=preloaded.outer180.TERMINAL;
 await tools.apply_patch('*** Begin Patch\n*** Add File: '+terminal.captureDirectory+'/native-terminal.original.json\n+'+JSON.stringify({schema:'TRACE180_ACTUAL_HOLDER_TERMINAL_ORIGINAL',original,error,native_authority:false})+'\n*** End Patch');
 // Source publisher obtains the real current version, builds the exact original
 // writer terminal, then completes/verifies all4 before this result returns.
 const done=await outerConsumer180(terminal,tools);if(error)throw Error('Actual native original failed; terminal metadata retained, never success/retry');
 return {original,outerRX:rx,outerTERMINAL:done,native_authority:false};
}
