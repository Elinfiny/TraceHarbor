/* Source-only Recovery86 controller. No media effect on import/page load.
   All reservations precede media APIs; distinct diagnostics are not demo retries. */
const Recovery86=(()=>{
 const platformTimers=Object.freeze({set:(fn,ms)=>setTimeout(fn,ms),clear:id=>clearTimeout(id)});
 const safeNames=new Set(['TypeError','ReferenceError','EncodingError','NotSupportedError','NotReadableError','InvalidStateError','SecurityError','AbortError','UnknownError','OverconstrainedError','TimeoutError','NotAllowedError','NotFoundError']);
 const named=(name,where)=>Object.assign(new Error('RECOVERY_REFUSED_NO_RETRY'),{name:safeNames.has(name)?name:'UnknownError',where});
 const safe=e=>({error_name:safeNames.has(e?.name||e?.error_name)?(e.name||e.error_name):'UnclassifiedError',where:['SELECT','CONSTRUCT','START','RECORDER_EVENT','DECODE','UPLOAD','PROBE','TIMEOUT','TRACK_ENDED','FLOW'].includes(e?.where)?e.where:'FLOW'});
 const sleep=ms=>new Promise(r=>setTimeout(r,ms));
 const hash=async b=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',b))).map(x=>x.toString(16).padStart(2,'0')).join('');
 class API{
  constructor(fetcher=fetch){this.fetcher=fetcher.bind(typeof window==='undefined'?undefined:window);}
  async bounded(path,options){const abort=new AbortController();const timer=setTimeout(()=>abort.abort(),8000);try{const r=await this.fetcher(path,{...options,signal:abort.signal});abort.signal.throwIfAborted();const data=await r.json();return {ok:r.ok,json:async()=>data};}finally{clearTimeout(timer);}}
  async get(path){const r=await this.bounded(path,{credentials:'same-origin',cache:'no-store',redirect:'error'});if(!r.ok)throw named('UnknownError','PROBE');return r.json();}
  async post(path,x){const r=await this.bounded(path,{method:'POST',credentials:'same-origin',cache:'no-store',redirect:'error',headers:{'Content-Type':'application/json'},body:JSON.stringify(x)});if(!r.ok)throw named('UnknownError','UPLOAD');return r.json();}
  prepareSelection(codec){return this.post('/recovery004f/prepare004f',{codec});}
  startSelection(key){return this.post('/recovery004f/start004f',{key});}
  reserve(phase,codec){return this.post('/recovery004f/reserve',{phase,codec});}
  async append(phase,sequence,bytes){const sha=await hash(bytes);const r=await this.bounded('/recovery004f/chunk',{method:'POST',credentials:'same-origin',cache:'no-store',redirect:'error',headers:{'Content-Type':'application/octet-stream','X-Recovery-Phase':phase,'X-Chunk-Sequence':String(sequence),'X-Chunk-SHA256':sha},body:bytes});if(!r.ok)throw named('UnknownError','UPLOAD');const a=await r.json();if(a.sequence!==sequence||a.bytes!==bytes.length||a.sha256!==sha)throw named('UnknownError','UPLOAD');return a;}
  finish(phase,value){return this.post('/recovery004f/finish',{phase,value});}
  fail(phase,e){return this.post('/recovery004f/fail',{phase,...safe(e)});}
 }
 function probe(stream,mime,Recorder,{seconds=2,maximum=1048576,now=()=>performance.now(),timers=platformTimers}={}){
  return new Promise((resolve,reject)=>{
   let rec,timer,hardTimer,done=false,bytes=0,chunks=[],started=now(),failure=null;
   const stop=()=>{try{if(rec?.state!=='inactive')rec.stop();}catch{};};
   const fail=e=>{if(done)return;failure=failure||e;stop();finish();};
   const finish=()=>{if(done)return;done=true;timers.clear(timer);timers.clear(hardTimer);if(failure){stop();return reject(failure);}const blob=new Blob(chunks,{type:mime});if(!blob.size)return reject(named('NotReadableError','DECODE'));resolve({blob,elapsed:(now()-started)/1000});};
   try{
    rec=new Recorder(stream,{mimeType:mime,videoBitsPerSecond:800000});
    rec.ondataavailable=e=>{if(done||!e.data?.size)return;if(e.data.size>maximum||bytes+e.data.size>maximum||chunks.length>=32)return fail(named('UnknownError','UPLOAD'));bytes+=e.data.size;chunks.push(e.data);};
    rec.onerror=e=>fail(named(e?.error?.name,'RECORDER_EVENT'));rec.onstop=finish;
    started=now();rec.start(400);if(done)return;hardTimer=timers.set(()=>fail(named('TimeoutError','TIMEOUT')),6000);timer=timers.set(stop,seconds*1000);
   }catch(e){failure=named(e?.name,rec?'START':'CONSTRUCT');finish();}
  });
 }
 async function decode(source,expected,timeout=5000){
  const v=document.createElement('video');v.muted=true;v.playsInline=true;const url=typeof source==='string'?source:URL.createObjectURL(source);v.src=url;
  try{await Promise.race([new Promise((resolve,reject)=>{v.onloadeddata=resolve;v.onerror=()=>reject(named('NotReadableError','DECODE'));v.load();}),sleep(timeout).then(()=>{throw named('TimeoutError','DECODE');})]);if(v.videoWidth!==expected.width||v.videoHeight!==expected.height||v.readyState<2)throw named('NotReadableError','DECODE');return true;}
  finally{v.removeAttribute('src');v.load();if(typeof source!=='string')URL.revokeObjectURL(url);}
 }
 function canvasSource(p,video=null){
  const c=document.createElement('canvas');c.width=p.width;c.height=p.height;const x=c.getContext('2d');if(!x||!c.captureStream)throw named('NotSupportedError','CONSTRUCT');let frame=0;
  const draw=()=>{x.fillStyle='#0b141a';x.fillRect(0,0,c.width,c.height);if(video){const k=Math.min(c.width/video.videoWidth,c.height/video.videoHeight);x.drawImage(video,(c.width-video.videoWidth*k)/2,(c.height-video.videoHeight*k)/2,video.videoWidth*k,video.videoHeight*k);}else{x.fillStyle=frame++%2?'#267c66':'#b9a56b';x.fillRect(40+(frame%30)*10,60,260,200);x.fillStyle='#ffffff';x.font='28px sans-serif';x.fillText('TraceHarbor synthetic codec diagnostic',40,340);}};
  draw();const interval=setInterval(draw,1000/p.fps);const stream=c.captureStream(p.fps);return {stream,dispose:()=>{clearInterval(interval);stream.getTracks().forEach(t=>t.stop());}};
 }
 class FullRecorder{
  constructor({stream,mime,Recorder,api,p,onAck=()=>{},onTerminal=()=>{},now=()=>performance.now(),timers=platformTimers}){Object.assign(this,{stream,mime,Recorder,api,p,onAck,onTerminal,now,timers});this.state='IDLE';this.queue=Promise.resolve();this.failure=null;this.stoppedAt=null;this.finalizing=false;this.receivedBytes=0;this.reservedBytes=0;this.bytes=0;this.reservedChunks=0;this.seq=0;this.pendingBytes=0;this.pendingChunks=0;this.droppedBytes=0;}
  async start(codec){
   if(this.state!=='IDLE')throw named('InvalidStateError','START');this.state='RESERVING';
   await this.api.reserve('full',codec);this.started=this.now(); // ACK before construction/start; unknown => no retry.
   try{this.rec=new this.Recorder(this.stream,{mimeType:this.mime,videoBitsPerSecond:this.p.bitrate});this.rec.ondataavailable=e=>this.enqueue(e.data);this.rec.onerror=e=>{this.failure=this.failure||safe(named(e?.error?.name,'RECORDER_EVENT'));this.stop('ERROR');};this.rec.onstop=()=>this.finish();this.started=this.now();this.state='RECORDING';this.rec.start(400);if(this.state!=='RECORDING')return;this.timer=this.timers.set(()=>this.stop('STOP224'),this.p.full_seconds*1000);}
   catch(e){this.failure=safe(named(e?.name,'START'));this.state='STOPPING';this.stoppedAt=this.now();await this.finish();throw named(e?.name,'START');}
  }
  enqueue(blob){
   if(!blob?.size)return;const n=blob.size;this.receivedBytes+=n;
   if(!['RECORDING','STOPPING'].includes(this.state)||this.failure){this.droppedBytes+=n;return;}
   if(n>1048576||this.reservedBytes+n>this.p.full_bytes||this.pendingBytes+n>this.p.pending_bytes||this.pendingChunks>=this.p.pending_chunks||this.reservedChunks>=this.p.max_chunks){this.droppedBytes+=n;this.failure={error_name:'UnknownError',where:'UPLOAD'};return this.stop('ERROR');}
   const seq=this.reservedChunks++;this.reservedBytes+=n;this.pendingBytes+=n;this.pendingChunks++;
   this.queue=this.queue.then(async()=>{try{if(this.failure){this.droppedBytes+=n;return;}const b=new Uint8Array(await blob.arrayBuffer());if(b.length!==n)throw named('UnknownError','UPLOAD');await this.api.append('full',seq,b);this.bytes+=n;this.seq++;if(this.seq===1)this.onAck();}catch(e){this.failure=this.failure||safe(e);this.stop('ERROR');}finally{this.pendingBytes-=n;this.pendingChunks--;}});
  }
  stop(reason){if(this.state!=='RECORDING')return;if(reason!=='STOP224')this.failure=this.failure||{error_name:'UnknownError',where:'FLOW'};this.reason=reason;this.stoppedAt=this.now();this.state='STOPPING';this.timers.clear(this.timer);try{this.rec.stop();}catch{this.failure=this.failure||{error_name:'UnknownError',where:'RECORDER_EVENT'};this.finish();}}
  async finish(){
   if(this.finalizing)return;this.finalizing=true;if(this.stoppedAt===null){this.stoppedAt=this.now();this.failure=this.failure||{error_name:'UnknownError',where:'RECORDER_EVENT'};}await this.queue;
   const custody={received_bytes:this.receivedBytes,reserved_bytes:this.reservedBytes,acked_bytes:this.bytes,reserved_chunks:this.reservedChunks,acked_chunks:this.seq,pending_bytes:this.pendingBytes,pending_chunks:this.pendingChunks,dropped_bytes:this.droppedBytes,failure:this.failure!==null};
   try{const receipt=await this.api.finish('full',{elapsed:Math.max(0,(this.stoppedAt-this.started)/1000),reason:this.failure?'ERROR':this.reason,custody});this.state=receipt.state==='CAPTURED_NOT_AV_VERIFIED'?'FINISHED':'FAILED';if(this.failure)await this.api.fail('full',this.failure).catch(()=>{});this.onTerminal(receipt);}catch{this.state='FAILED';this.onTerminal({state:'UNKNOWN_NO_RETRY'});}finally{this.stream.getTracks().forEach(t=>t.stop());}
  }
 }
 function flowSignal96(data,id,full,ack){if(data?.id!==id)return;if(data.type==='ROOT_ACK')ack();if(data.type==='FLOW_FAILED')full.stop('ERROR');}
 // UI containment only. Server clock, identity, one-use and media gates remain authoritative.
 function targetGuard112({doc,button,status,now=()=>performance.now(),timers=platformTimers}){
  const out=doc.getElementById('phase112');let locked=false,expiry=null;
  const words={READY:'Pregătit pentru deschiderea selectorului.',PICKER_REQUESTED:'Alege această filă în dialog și apasă Share.',SELECT_STARTED_SERVER_ACK:'Selectorul este înregistrat; aștept partajarea filei.',STREAM_GRANTED:'Partajare acceptată; rămâi în această filă.',NATIVE_PASS_SERVER_ACK:'Proba nativă este validată.',FIRST_FULL_CHUNK_SERVER_ACK:'Înregistrare în curs. Rămâi aici aproximativ4 minute.',AI004_REQUESTED:'Demonstrația server este în curs.',AI004_RESULT_SERVER_VERIFIED:'Rezultatul serverului este afișat; înregistrarea continuă.',FINISHED:'CAPTURA SALVATA PRIVAT. Poți reveni la ChatGPT.',FAILED_NO_RETRY:'CAPTURA OPRITA CU EROARE. Nu repeta Share.',EXPIRED:'Fereastra de selecție a expirat. Nu apăsa Share și nu reîncărca.'};
  function stage(name){
   if(!Object.prototype.hasOwnProperty.call(words,name))throw named('InvalidStateError','FLOW');
   out.dataset.stage=name;out.textContent=words[name];
   if(name==='READY')locked=true;
   if(name==='PICKER_REQUESTED'){timers.clear(expiry);expiry=null;button.disabled=true;locked=true;}
   if(['FINISHED','FAILED_NO_RETRY','EXPIRED'].includes(name)){timers.clear(expiry);expiry=null;button.disabled=true;locked=false;}
  }
  function arm(ms){if(!Number.isFinite(ms)||ms<=0)throw named('TimeoutError','SELECT');locked=true;stage('READY');expiry=timers.set(()=>stage('EXPIRED'),ms);}
  doc.addEventListener('click',e=>{const link=e.target?.closest?.('a[href]');if(locked&&link?.getAttribute('href')==='/'){e.preventDefault();e.stopPropagation();status.textContent='Păstrează această filă până la mesajul final; legătura spre pagina publică este suspendată.';}},true);
  doc.defaultView?.addEventListener('beforeunload',e=>{if(locked){e.preventDefault();e.returnValue='';}});
  return {arm,stage};
 }

 function creditReady(v){return v?.state==='STANDARD_PAID_ATTEMPT_ADMITTED'&&v.admitted_attempt===true&&v.billing_mode==='STANDARD_PAID89'&&v.paid_usage_enabled===true&&v.paid_continuation_disabled===false&&v.provider_global_hardcap===false&&v.billing_status==='Active';}
 class Controller{
  constructor({api,p,devices,Recorder,source=canvasSource,decoder=decode,report=()=>{},preview=null,channel=null,onStage=()=>{}}){Object.assign(this,{api,p,devices,Recorder,source,decoder,report,preview,channel,onStage});this.state='IDLE';this.codec=null;this.usedDiagnostics=false;this.usedSelection=false;this.full=null;this.disposed=false;}
  async diagnostic(){
   if(this.usedDiagnostics||this.p.synthetic_diagnostics_closed)throw named('InvalidStateError','START');this.usedDiagnostics=true;
   for(const codec of Object.keys(this.p.codecs)){
    let src,reserved=false;
    try{await this.api.reserve(codec,codec);reserved=true;if(!this.Recorder.isTypeSupported(this.p.codecs[codec]))throw named('NotSupportedError','START');src=this.source(this.p);const result=await probe(src.stream,this.p.codecs[codec],this.Recorder);await this.decoder(result.blob,this.p);await this.api.append(codec,0,new Uint8Array(await result.blob.arrayBuffer()));const q=await this.api.finish(codec,{elapsed:result.elapsed,reason:'DIAGNOSTIC_DONE',client_decoded:true});if(q.state==='PASS'){this.codec=codec;this.state='CODEC_QUALIFIED';this.report('Distinct diagnostic106 passed: '+codec+'. Native sample remains required.');return codec;}this.report('Diagnostic retained; server qualification '+q.state+' / '+(q.probe?.error||'UNQUALIFIED')+'. No retry.');}
    catch(e){if(!reserved){this.state='FAILED';throw e;}await this.api.fail(codec,e).catch(()=>{});this.report('Codec diagnostic: '+codec+' / '+safe(e).error_name+' / '+safe(e).where+'. No repeat of this codec.');}
    finally{src?.dispose();}
   }
   this.state='FAILED';throw named('NotSupportedError','PROBE');
  }
  async prepareSelection(){
   if(this.selection||!this.codec)throw named('InvalidStateError','SELECT');
   TraceHarborFocus115.require();const requestedAt=performance.now();const ready=await this.api.prepareSelection(this.codec);const usable=ready.lease_ms-(performance.now()-requestedAt)-500;if(!Number.isFinite(usable)||usable<=0)throw named('TimeoutError','SELECT');ready.lease_ms=Math.floor(usable);
   const K=typeof module!=='undefined'?require('./selection004f.js'):Selection146;
   this.selection=new K.Attempt({devices:this.devices,api:this.api,ready,report:this.report,onStage:this.onStage});return ready;
  }
  async selectAndRun(gesture){
   if(this.usedSelection||!this.codec)throw named('InvalidStateError','SELECT');this.usedSelection=true;let raw,source,timer;let activePhase='select';const begun=performance.now();
   try{
    if(!this.selection)throw named('InvalidStateError','SELECT');
    // The prepared capability was obtained before Owner's click; start() calls
    // getDisplayMedia synchronously before its first promise/network boundary.
    raw=await this.selection.start(gesture);this.report('Partajare acceptata. Proba nativa de2secunde se verifica; ramai in aceasta fila.');const tracks=raw.getVideoTracks();
    timer=setTimeout(()=>{this.disposed=true;this.full?.stop('ERROR');raw.getTracks().forEach(t=>t.stop());source?.dispose();},this.p.native_stream_seconds*1000);
    tracks[0].onended=()=>{this.disposed=true;this.full?.stop('ERROR');source?.dispose();};
    const video=document.createElement('video');video.muted=true;video.playsInline=true;video.srcObject=raw;await video.play();await Promise.race([new Promise((resolve,reject)=>{if(video.readyState>=2&&video.videoWidth)return resolve();video.onloadeddata=resolve;video.onerror=()=>reject(named('NotReadableError','DECODE'));}),sleep(5000).then(()=>{throw named('TimeoutError','DECODE');})]);if(!video.videoWidth||!video.videoHeight)throw named('NotReadableError','DECODE');
    source=this.source(this.p,video);activePhase='native';await this.api.reserve('native',this.codec);const sample=await probe(source.stream,this.p.codecs[this.codec],this.Recorder);await this.decoder(sample.blob,this.p);await this.api.append('native',0,new Uint8Array(await sample.blob.arrayBuffer()));const q=await this.api.finish('native',{elapsed:sample.elapsed,reason:'DIAGNOSTIC_DONE',client_decoded:true});if(q.state!=='PASS')throw named('NotReadableError','PROBE');this.onStage('NATIVE_PASS_SERVER_ACK');
    // Verify authenticated SAME-service playback before spending the full demo.
    await this.decoder('/recovery004f/native.webm',this.p);if(this.preview){this.preview.src='/recovery004f/native.webm';this.preview.load();}await this.api.post('/recovery004f/preview',{decoded:true});
    if(this.disposed||tracks[0].readyState!=='live'||performance.now()-begun>120000)throw named('AbortError','TRACK_ENDED');
    activePhase='full';let acknowledged=false,repeat;
    this.full=new FullRecorder({stream:source.stream,mime:this.p.codecs[this.codec],Recorder:this.Recorder,api:this.api,p:this.p,onAck:()=>{this.onStage('FIRST_FULL_CHUNK_SERVER_ACK');this.state='RECORDING';this.channel?.postMessage({type:'CAPTURE_STARTED',id:this.p.id});this.report('Full recording active; first media fragment retained. One admitted server request may now run.');let count=0;const signal=()=>{if(!acknowledged)this.channel?.postMessage({type:'FULL_ACK',id:this.p.id});if(++count>=10){clearInterval(repeat);if(!acknowledged)this.full.stop('ERROR');}};signal();repeat=setInterval(signal,500);},onTerminal:receipt=>{clearTimeout(timer);clearInterval(repeat);source?.dispose();raw.getTracks().forEach(t=>t.stop());this.state=receipt.state==='CAPTURED_NOT_AV_VERIFIED'?'FINISHED':'FAILED';this.onStage(this.state==='FINISHED'?'FINISHED':'FAILED_NO_RETRY');this.channel?.postMessage({type:this.state==='FINISHED'?'CAPTURE_FINISHED':'CAPTURE_FAILED',id:this.p.id});this.report(receipt.state==='CAPTURED_NOT_AV_VERIFIED'?'Recording retained privately. AV verification pending.':'Partial/unknown recording retained. No automatic retry.');}});
    if(this.channel)this.channel.onmessage=e=>flowSignal96(e.data,this.p.id,this.full,()=>{acknowledged=true;});
    await this.full.start(this.codec);this.state='RECORDING';return this.full;
   }catch(e){if(activePhase==='select'){this.selection?.fail(e);}else await this.api.fail(activePhase,e).catch(()=>{});this.state='FAILED';this.onStage('FAILED_NO_RETRY');this.channel?.postMessage({type:'CAPTURE_FAILED',id:this.p.id});this.report('Recovery stopped: '+safe(e).error_name+' / '+safe(e).where+'. Retained; no automatic retry.');clearTimeout(timer);source?.dispose();raw?.getTracks().forEach(t=>t.stop());throw e;}
  }
 }
 return {API,probe,safe,FullRecorder,Controller,platformTimers,creditReady,flowSignal96,targetGuard112};
})();
if(typeof module!=='undefined')module.exports=Recovery86;
if(typeof document!=='undefined'&&document.getElementById('diagnose86')){
 (async()=>{const targetArmed004f=new Promise((resolve,reject)=>{
 let settled=false,timer;const finish=(fn,value)=>{if(settled)return;settled=true;clearTimeout(timer);document.removeEventListener('traceharbor-target-ready004f',ready);document.removeEventListener('traceharbor-target-failed004f',failed);fn(value);};
 const ready=()=>finish(resolve),failed=e=>finish(reject,Object.assign(new Error('INIT_FAILED'),{initCode416:e.detail?.code||'INIT_FAILED'}));
 document.addEventListener('traceharbor-target-ready004f',ready,{once:true});document.addEventListener('traceharbor-target-failed004f',failed,{once:true});
 timer=setTimeout(()=>finish(reject,Object.assign(new Error('INIT_WAIT_TIMEOUT'),{initCode416:'INIT_WAIT_TIMEOUT'})),30000);
 if(document.documentElement.dataset.targetInitError416)failed({detail:{code:document.documentElement.dataset.targetInitError416}});else if(document.documentElement.dataset.targetArmed004f==='yes')ready();
 });targetArmed004f.catch(()=>{});const api=new Recovery86.API();const p=await api.get('/recovery004f/policy');const status=document.getElementById('status86'),diagnose=document.getElementById('diagnose86'),select=document.getElementById('select86');const ui=Recovery86.targetGuard112({doc:document,button:select,status});document.addEventListener('traceharbor-stage112',e=>{if(['AI004_REQUESTED','AI004_RESULT_SERVER_VERIFIED'].includes(e.detail))ui.stage(e.detail);});const c=new Recovery86.Controller({api,p,onStage:name=>ui.stage(name),devices:navigator.mediaDevices,Recorder:window.MediaRecorder,report:t=>status.textContent=t,preview:document.getElementById('preview86'),channel:new BroadcastChannel('traceharbor-recovery004f')});
 if(document.getElementById('capture-controls004f'))await targetArmed004f;
 if(!document.getElementById('capture-controls004f')){select.disabled=true;status.textContent='Use the single authenticated target tab for recovery004f. No Share from this separate controller.';return;}
 const current=await api.get('/recovery004f/status');const retained=current.retained_clip_qualification;
 if(p.synthetic_diagnostics_closed){diagnose.disabled=true;c.usedDiagnostics=true;if(retained?.state==='PASS_PRIOR_NATIVE146_LINEAGE'){c.codec='vp8';c.state='CODEC_QUALIFIED';select.disabled=true;if(current.target_epoch==='004f'&&current.armed&&current.session_remaining>=1320&&Recovery86.creditReady(current.provider_readiness)&&current.phases.select.state==='NOT_STARTED'){const ready=await c.prepareSelection();ui.arm(ready.lease_ms);select.disabled=false;}status.textContent='Păstrează fila TraceHarbor · Recording target004f. Selectorul va fi deschis imediat după pregătire; apoi selectează această filă și Share.';}else{select.disabled=true;status.textContent='Existing '+(retained?.clip_bytes||43637)+' byte clip retained. Original server qualification FAILED. Distinct qualification146: '+(retained?.state||'NOT_STARTED')+'. No new synthetic recording or retry.';}}
 diagnose.addEventListener('click',async()=>{if(p.synthetic_diagnostics_closed)return;diagnose.disabled=true;try{await c.diagnostic();const s=await api.get('/recovery004f/status');select.disabled=!s.armed;}catch{status.textContent+=' Recovery closed; no native sample/full recording admitted.';}});
 select.addEventListener('click',e=>{if(select.disabled)return;if(!TraceHarborFocus115.eligible()){status.textContent='Focalizare invalida. Selectorul nu a fost pornit.';return;}select.disabled=true;void c.selectAndRun({trusted:e.isTrusted,active:navigator.userActivation?.isActive}).catch(()=>{});});
 })().catch(e=>{const name=['TypeError','AbortError','TimeoutError','SecurityError'].includes(e?.name)?e.name:'UnclassifiedError';document.getElementById('diagnose86').disabled=true;document.getElementById('select86').disabled=true;const allowed=new Set(['INIT_FAILED','INIT_WAIT_TIMEOUT','INIT_FOREGROUND_FAILED','TARGET_ALREADY_ARMED','APP_TARGET_MISSING','PROVIDER_NOT_ADMITTED','FRESH_STANDARD89_METADATA','METADATA_GUARD_REFUSED','STATUS_TIMEOUT','STATUS_TRANSPORT_ERROR','ARM_TRANSPORT_UNKNOWN','ARM_ACK_UNCONFIRMED','INIT_WINDOW_TOO_SHORT']);const raw=e?.initCode416;const code=allowed.has(raw)||/^(STATUS|ARM)_HTTP_[45][0-9]{2}$/.test(raw||'')?raw:name;const phase=document.getElementById('phase112');if(phase){phase.dataset.stage='INITIALIZATION_FAILED';phase.textContent='Pregătirea s-a oprit. Nicio captură pornită; fără reluare automată.';}document.getElementById('status86').textContent='Recovery unavailable / '+code+' / INITIALIZATION. No media started. No automatic retry.';});
}
