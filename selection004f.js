/* One native permission attempt. No media effect on import or preparation. */
const Selection146=(()=>{
 const error=(name,where='SELECT')=>Object.assign(new Error('CAPTURE146_STOPPED_NO_RETRY'),{name,where});
 const stop=stream=>{try{for(const t of stream?.getTracks?.()||[])t.stop();}catch{}};
 class Attempt{
  constructor({devices,api,ready,now=()=>performance.now(),timers={set:(f,n)=>setTimeout(f,n),clear:i=>clearTimeout(i)},report=()=>{},onStage=()=>{}}){Object.assign(this,{devices,api,ready,now,timers,report,onStage});this.preparedAt=now();this.used=false;this.failed=false;this.raw=null;this.failureSent=false;this.timer=null;this.rejectTimer=null;this.failureReceipt=null;this.state='READY';}
  fail(e){
   if(this.failed)return;this.failed=true;this.state='FAILED_NO_RETRY';this.onStage('FAILED_NO_RETRY');this.timers.clear(this.timer);stop(this.raw);this.rejectTimer?.(e);
   if(!this.failureSent){this.failureSent=true;this.failureReceipt=Promise.resolve().then(()=>this.api.fail('select',e)).then(()=>{this.report('Capture stopped / '+e.name+' / '+e.where+'. Failure retained; no retry.');return {state:'ACKNOWLEDGED'};},()=>{this.report('Capture stopped / '+e.name+' / '+e.where+'. Failure report unconfirmed (session or transport); preserve original attempt.');return {state:'UNCONFIRMED_SESSION_OR_TRANSPORT'};});}
  }
  start(gesture){
   if(!TraceHarborFocus115.eligible())return Promise.reject(error('SecurityError'));
   if(this.used)return Promise.reject(error('InvalidStateError'));
   this.used=true;
   if(!this.ready||this.ready.state!=='PREPARED_OWNER_GESTURE_ONLY'||typeof this.ready.key!=='string'||this.ready.key.length!==64||!Number.isFinite(this.ready.lease_ms)||this.now()-this.preparedAt>=this.ready.lease_ms||gesture?.trusted!==true||gesture?.active===false){const e=error('SecurityError');this.fail(e);return Promise.reject(e);}
   this.state='NATIVE_PERMISSION_PENDING';const begun=this.now();
   const timeout=new Promise((_,reject)=>{this.rejectTimer=reject;this.timer=this.timers.set(()=>this.fail(error('TimeoutError','TIMEOUT')),120000);});
   timeout.catch(()=>{}); // Also handles a synchronous getDisplayMedia throw.
   let display;
   // This call is synchronous in the trusted click stack, BEFORE any await or
   // network request. The durable one-use reservation already exists.
   try{display=this.devices.getDisplayMedia({video:true,audio:false,preferCurrentTab:true,selfBrowserSurface:'include'});this.onStage('PICKER_REQUESTED');}
   catch(e){this.fail(error(e?.name||'NotAllowedError'));return Promise.reject(e);}
   const stream=Promise.resolve(display).then(raw=>{
    if(this.failed||this.now()-begun>120000){stop(raw);this.fail(error('TimeoutError','TIMEOUT'));throw error('TimeoutError','TIMEOUT');}
    this.raw=raw;const tracks=raw?.getVideoTracks?.()||[];
    if(tracks.length!==1||tracks[0].getSettings?.().displaySurface!=='browser'){stop(raw);throw error('SecurityError');}
    return raw;
   },e=>{throw error(['NotAllowedError','AbortError','NotReadableError','NotFoundError','InvalidStateError','SecurityError','TypeError'].includes(e?.name)?e.name:'UnknownError');});
   // An unsuccessful or delayed start ACK stops any returned stream. No other
   // tab can prepare again or obtain the one capability through status.
   const ack=Promise.resolve().then(()=>this.api.startSelection(this.ready.key)).then(v=>{this.onStage('SELECT_STARTED_SERVER_ACK');return v;});
   return Promise.race([Promise.all([stream,ack]).then(([raw])=>{
    if(this.failed||this.now()-begun>120000){stop(raw);throw error('TimeoutError','TIMEOUT');}
    this.timers.clear(this.timer);this.state='STREAM_RECEIVED';this.onStage('STREAM_GRANTED');return raw;
   }),timeout]).catch(e=>{this.fail(e);throw e;});
  }
 }
 return {Attempt,error,stop};
})();
if(typeof module!=='undefined')module.exports=Selection146;
