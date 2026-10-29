/* Private48: sticky failure and synchronous bounded Blob custody; no capture on import.
   Limits cover application-retained work, not browser physical memory/bitrate. */
class CaptureController {
  constructor({mediaDevices,Recorder,sink,recordingGate=async()=>{const response=await fetch('/private-capture/selected',{method:'POST',credentials:'same-origin',cache:'no-store',redirect:'error',headers:{'Content-Type':'application/json'},body:JSON.stringify({phase:'TAB_SELECTED_BEFORE_RECORDER'})});if(!response.ok||(await response.json()).recording_started!==true)throw Error('NATIVE_SELECTION_NOT_ACKNOWLEDGED');},onTerminal=()=>{},onDiagnostic=()=>{},now=()=>performance.now(),timers={set:setTimeout,clear:clearTimeout}}){
    Object.assign(this,{devices:mediaDevices,Recorder,sink,recordingGate,onTerminal,onDiagnostic,now,timers});
    this.state='IDLE';this.diagnostic=null;this.startPhase='SELECTING';this.queue=Promise.resolve();this.max=25165824;this.maxPendingBytes=2097152;this.maxPendingChunks=8;
    this.bytes=0;this.seq=0;this.receivedBytes=0;this.receivedChunks=0;this.reservedBytes=0;this.reservedChunks=0;this.pendingBytes=0;this.pendingChunks=0;this.droppedBytes=0;this.failure=null;this.stoppedAt=null;this.finalizing=false;
  }
  reportDiagnostic(error,phase){
    if(this.diagnostic)return;
    const names=new Set(['EncodingError','NotSupportedError','NotReadableError','InvalidStateError','SecurityError','AbortError','UnknownError']);
    const phases=new Set(['SELECTING','RECORDING_GATE','CONSTRUCTING','STARTING','RECORDER_EVENT','UNEXPECTED_STOP']);
    const state=this.recorder?.state;
    this.diagnostic=Object.freeze({schema:'traceharbor.capture-diagnostic84.v1',error_name:names.has(error?.name)?error.name:'UnclassifiedError',phase:phases.has(phase)?phase:'UNEXPECTED_STOP',recorder_state:['inactive','recording','paused'].includes(state)?state:'unobserved',retry:false});
    // No raw message, stack, device name/ID, source text or credential values.
    // Diagnostic publication must never alter the once-only capture lifecycle.
    try{this.onDiagnostic(this.diagnostic);}catch{}
  }
  async start(admission){
    if(this.state!=='IDLE'||admission?.capture!==true||admission?.classification!=='SYNTHETIC_ONLY'||admission?.secureContext!==true)throw Error('CAPTURE_NOT_ADMITTED');
    if(!this.devices?.getDisplayMedia||!this.Recorder?.isTypeSupported('video/webm;codecs=vp8'))throw Error('RECORDER_UNQUALIFIED');
    this.state='SELECTING';
    try{
      this.stream=await this.devices.getDisplayMedia({video:true,audio:false});const tracks=this.stream.getVideoTracks();
      if(tracks.length!==1||tracks[0].getSettings?.().displaySurface!=='browser')throw Error('BROWSER_TAB_REQUIRED');
      this.startPhase='RECORDING_GATE';await this.recordingGate();this.startPhase='CONSTRUCTING';
      this.recorder=new this.Recorder(this.stream,{mimeType:'video/webm;codecs=vp8',videoBitsPerSecond:1000000});
      this.recorder.ondataavailable=e=>this.enqueue(e.data);this.recorder.onerror=e=>{this.reportDiagnostic(e?.error,'RECORDER_EVENT');this.stop('ERROR');};tracks[0].onended=()=>this.stop('CANCEL');this.recorder.onstop=()=>this.finalize();
      this.startPhase='STARTING';this.started=this.now();this.state='RECORDING';this.recorder.start(250);this.timer=this.timers.set(()=>this.stop('STOP164'),164000);
      return {state:this.state,seconds:164,bytes_limit:this.max,pending_bytes_limit:this.maxPendingBytes,pending_chunks_limit:this.maxPendingChunks,permission:'NATIVE_GRANTED_NOT_REUSABLE'};
    }catch(error){this.reportDiagnostic(error,this.startPhase);this.state='FAILED';this.stream?.getTracks().forEach(t=>t.stop());throw Error('CAPTURE_START_FAILED');}
  }
  enqueue(blob){
    if(!blob?.size)return;
    const size=blob.size;
    if(!Number.isSafeInteger(size)||size<0){this.stop('ERROR');return;}
    this.receivedBytes+=size;this.receivedChunks++;
    if(!['RECORDING','STOPPING'].includes(this.state)||this.failure){this.droppedBytes+=size;return;}
    if(size>1048576||this.reservedChunks>=700||this.reservedBytes+size>this.max||this.pendingBytes+size>this.maxPendingBytes||this.pendingChunks>=this.maxPendingChunks){this.droppedBytes+=size;this.stop('BOUND');return;}
    const seq=this.reservedChunks++;this.reservedBytes+=size;this.pendingBytes+=size;this.pendingChunks++;
    this.queue=this.queue.then(async()=>{
      try{
        if(this.failure){this.droppedBytes+=size;return;}
        const bytes=new Uint8Array(await blob.arrayBuffer());
        if(bytes.length!==size)throw Error('CHUNK_LENGTH');
        const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))).map(b=>b.toString(16).padStart(2,'0')).join('');
        const ack=await this.sink.append(seq,bytes,hash);
        if(ack.sequence!==seq||ack.bytes!==size||ack.sha256!==hash)throw Error('SINK_CUSTODY');
        this.bytes+=size;this.seq++;
      }catch{this.stop('ERROR');}
      finally{this.pendingBytes-=size;this.pendingChunks--;}
    });
  }
  stop(reason='CANCEL'){
    if(!['RECORDING','STOPPING'].includes(this.state))return;
    if(reason!=='STOP164')this.failure=this.failure||reason;
    this.reason=this.failure||reason;
    if(this.state==='STOPPING')return;
    this.stoppedAt=this.now();this.state='STOPPING';this.timers.clear(this.timer);
    try{this.recorder.stop();}catch{this.failure=this.failure||'ERROR';this.reason=this.failure;}
    this.stream.getTracks().forEach(t=>t.stop());
  }
  async finalize(){
    if(this.finalizing)return;this.finalizing=true;
    if(this.stoppedAt===null){this.reportDiagnostic(null,'UNEXPECTED_STOP');this.stoppedAt=this.now();this.failure=this.failure||'ERROR';this.reason=this.failure;this.state='STOPPING';}
    await this.queue;
    const elapsed=Math.max(0,(this.stoppedAt-this.started)/1000);
    const custody={received_bytes:this.receivedBytes,reserved_bytes:this.reservedBytes,acked_bytes:this.bytes,reserved_chunks:this.reservedChunks,acked_chunks:this.seq,pending_bytes:this.pendingBytes,pending_chunks:this.pendingChunks,dropped_bytes:this.droppedBytes,failure:this.failure!==null};
    const complete=!custody.failure&&custody.pending_bytes===0&&custody.pending_chunks===0&&custody.dropped_bytes===0&&custody.reserved_bytes===custody.acked_bytes&&custody.reserved_chunks===custody.acked_chunks;
    const reason=complete&&this.reason==='STOP164'?'STOP164':this.failure||'ERROR';
    try{this.receipt=await this.sink.finish(elapsed,reason,custody);this.state=complete&&reason==='STOP164'&&this.receipt.state==='CAPTURED_NOT_AV_VERIFIED'?'FINISHED':'FAILED';this.onTerminal(this.receipt);}
    catch{this.state='FAILED';}
  }
}
function sameOriginSink(fetcher){
  async function send(path,body,headers){const r=await fetcher(path,{method:'POST',credentials:'same-origin',cache:'no-store',redirect:'error',body,headers});if(!r.ok)throw Error('PRIVATE_SINK_REFUSED');return r.json();}
  return {append:(sequence,bytes,hash)=>send('/private-capture/chunk',bytes,{'Content-Type':'application/octet-stream','X-Chunk-Sequence':String(sequence),'X-Chunk-SHA256':hash}),finish:(elapsed,reason,custody)=>send('/private-capture/finish',JSON.stringify({elapsed,reason,custody}),{'Content-Type':'application/json'})};
}
if(typeof module!=='undefined')module.exports={CaptureController,sameOriginSink};
if(typeof document!=='undefined'){
 const start=document.getElementById('start-capture');if(start)start.addEventListener('click',async()=>{start.disabled=true;const status=document.getElementById('capture-status');let diagnosticText='';try{
 const permit={capture:document.body.dataset.captureAdmitted==='true',classification:'SYNTHETIC_ONLY',secureContext:window.isSecureContext};
 const controller=new CaptureController({onDiagnostic:d=>{diagnosticText='Recorder diagnostic: '+d.phase+' / '+d.error_name+' / '+d.recorder_state+'. ';status.textContent=diagnosticText+'No automatic retry.';},mediaDevices:navigator.mediaDevices,Recorder:window.MediaRecorder,sink:sameOriginSink(fetch),onTerminal:r=>{status.textContent=diagnosticText+(r.state==='CAPTURED_NOT_AV_VERIFIED'?'Recording retained privately; audiovisual verification remains pending.':'Partial recording retained. No automatic retry.');}});
 await controller.start(permit);status.textContent='Recording synthetic demonstration; automatic stop after 164 seconds.';
 }catch{status.textContent=diagnosticText+'Capture unavailable. No automatic retry.';}});
}
