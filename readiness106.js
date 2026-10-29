/* Actual native platform checks before any fresh grant/media, on the same host. */
(()=>{
 const button=document.getElementById('readiness106'),status=document.getElementById('readiness106-status');let used=false;
 button.addEventListener('click',async()=>{
  if(used)return;used=true;button.disabled=true;const proof={schema:'traceharbor.native-readiness106.v1',streams:0,recorders:0,grants:0,AI:0};
  try{
   const health=await new Recovery86.API().get('/healthz');if(health.public_AI_enabled!==false||!/^[a-f0-9]{40}$/.test(health.source_commit))throw Error('HEALTH_BINDING');proof.source_commit=health.source_commit;proof.fetch_window_receiver=true;
   let wall,tick,cancel;
   try{await new Promise((resolve,reject)=>{wall=setTimeout(()=>reject(Error('TIMER_WALL')),1500);cancel=Recovery86.platformTimers.set(()=>reject(Error('CLEAR_FAILED')),100);Recovery86.platformTimers.clear(cancel);tick=Recovery86.platformTimers.set(resolve,0);});}
   finally{clearTimeout(wall);Recovery86.platformTimers.clear(tick);Recovery86.platformTimers.clear(cancel);}
   proof.native_timer_receivers=true;const c=document.createElement('canvas');c.width=2;c.height=2;const x=c.getContext('2d');if(!x||typeof c.captureStream!=='function')throw Error('CANVAS_UNAVAILABLE');x.fillRect(0,0,2,2);proof.canvas_2d_no_stream=true;
   proof.VP8_supported=typeof MediaRecorder==='function'&&MediaRecorder.isTypeSupported('video/webm;codecs=vp8');if(!proof.VP8_supported||typeof navigator.mediaDevices?.getDisplayMedia!=='function')throw Error('MEDIA_API_UNAVAILABLE');
   await crypto.subtle.digest('SHA-256',new Uint8Array([1,0,6]));proof.native_crypto=true;proof.state='PASS_NO_MEDIA_ENCODER_NOT_YET_QUALIFIED';
  }catch(e){proof.state='FAILED_NO_MEDIA';proof.error_name=['TypeError','ReferenceError','SecurityError','NotSupportedError'].includes(e?.name)?e.name:'UnclassifiedError';}
  status.textContent=JSON.stringify(proof,null,2);
 });
})();
