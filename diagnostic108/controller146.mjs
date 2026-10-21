// Actual functions.exec callsite. No source-native authority is supplied here.
import {bootstrapActualCaller127,observerPlan146,drive127} from './caller127.mjs';
export async function runControlled146(preloaded){
 if(typeof notify!=='function'||typeof tools!=='object')throw Error('Supported functions.exec notification/tool surface required before allocation');
 const handle=await bootstrapActualCaller127(preloaded);
 const issued=observerPlan146(handle);
 notify({schema:'TRACE146_SOURCE_ISSUED_OBSERVER_PLAN',issued,native_authority:false});
 return await drive127(handle,tools);
}
