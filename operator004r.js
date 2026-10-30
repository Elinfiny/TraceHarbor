/* One source-bound real UI macro, after full-media ACK. No media/model on import.
   All exported/imported data stays on the same service; no Owner file shuttle. */
(() => {
 const channel=new BroadcastChannel('traceharbor-recovery004r');
 const clientId=Array.from(crypto.getRandomValues(new Uint8Array(16))).map(x=>x.toString(16).padStart(2,'0')).join('');
 let started=false,clock=0,flowAborted=false,deadlineTimer;
 document.title='TraceHarbor · Recording target004r';document.body.classList.add('recovery-mode');
 const panel=document.createElement('section');panel.className='recovery-banner';panel.setAttribute('aria-label','Recording readiness');
 const line=document.createElement('p');line.textContent='Recording target ready. Live server evidence remains separate from the deterministic walkthrough.';panel.append(line);document.body.prepend(panel);
 const elapsed=()=>Math.max(0,(performance.now()-clock)/1000);
 const delay=ms=>new Promise(r=>setTimeout(r,ms));
 async function request(path,body){const response=await fetch(path,{method:body===undefined?'GET':'POST',credentials:'same-origin',cache:'no-store',redirect:'error',headers:body===undefined?{}:{'Content-Type':'application/json'},body:body===undefined?undefined:JSON.stringify(body)});if(!response.ok)throw Error('RECOVERY_FLOW_REFUSED');return response.json();}
 async function text(path){const response=await fetch(path,{credentials:'same-origin',cache:'no-store',redirect:'error'});if(!response.ok)throw Error('RECOVERY_DATA_UNAVAILABLE');return response.text();}
 async function wait(seconds){if(elapsed()>seconds+4)throw Error('FLOW_DEADLINE');await delay(Math.max(0,seconds*1000-(performance.now()-clock)));}
 async function ready(check){for(let i=0;i<100;i++){if(check())return;await delay(50);}throw Error('VIEW_NOT_READY');}
 async function mark(name){return request('/recovery004r/mark',{name,elapsed:elapsed()});}
 async function begin(){
  const s=await request('/recovery004r/status');if(!s.enabled||s.armed_id!==clientId)return;
  if(started)return;started=true;await request('/recovery004r/begin',{client_id:clientId});clock=performance.now()-s.full_elapsed*1000;channel.postMessage({type:'ROOT_ACK',id:'TRACEHARBOR-RECOVERY004R'});
  try{
   if(typeof run!=='function'||typeof runRuntime!=='function'||typeof loadRuntimeStatus!=='function')throw Error('APP_INTERFACE');
   deadlineTimer=setTimeout(()=>{flowAborted=true;mark('runtime-failed').catch(()=>{});channel.postMessage({type:'FLOW_FAILED',id:'TRACEHARBOR-RECOVERY004R'});},Math.max(0,52000-(performance.now()-clock)));
   line.textContent='ÎNREGISTRARE ÎN CURS · o singură cerere server · date sintetice · rămâi aici până la mesajul final.';
   await run(()=>text('/recovery004r/input'));await loadRuntimeStatus();document.dispatchEvent(new CustomEvent('traceharbor-stage112',{detail:'AI004_REQUESTED'}));await runRuntime();
   if(dossier?.schema!=='traceharbor.runtime-result.v1'){await mark('runtime-failed');throw Error('RUNTIME_NOT_VERIFIED');}
   document.dispatchEvent(new CustomEvent('traceharbor-stage112',{detail:'AI004_RESULT_SERVER_VERIFIED'}));clearTimeout(deadlineTimer);if(flowAborted||elapsed()>52)throw Error('RUNTIME_RENDER_TOO_LATE');await mark('runtime-rendered');line.textContent='Server record received. Origin and causal meaning are not independently attested.';
   // The twelve-second live-result excerpt is [48,60]. The unchanged nine-cue
   // walkthrough then occupies [60,224]; final export is 12+164=176 seconds.
   await wait(60);await mark('story-start');document.getElementById('evolution').click();await ready(()=>dossier?.schema==='traceharbor.evolution.v1');
   await wait(72);document.getElementById('evolution-summary')?.scrollIntoView({block:'center'});
   await wait(90);document.getElementById('add-evolution-source').click();await ready(()=>document.getElementById('add-evolution-conflict'));await mark('supported');
   await wait(115);const details=Array.from(document.querySelectorAll('details')).find(x=>/verification|runtime|deadline/i.test(x.textContent));if(!details)throw Error('SOURCE_INSPECTOR');details.open=true;details.scrollIntoView({block:'center'});await mark('citation');
   await wait(136);document.getElementById('add-evolution-conflict').click();await ready(()=>dossier?.after?.report?.outcome?.status==='CONFLICTED'||/CONFLICTED/.test(document.getElementById('result').textContent));await mark('conflicted');
   await wait(156);const exported=await request('/recovery004r/export',dossier);line.textContent='Export retained · '+exported.bytes+' bytes · checksum recorded';await mark('exported');
   await wait(176);await run(()=>text('/recovery004r/export'),'/verify');await ready(()=>dossier?.schema==='traceharbor.evolution.v1');await mark('reimported');
   await wait(192);await run(()=>text('/recovery004r/historical'),'/verify');await ready(()=>dossier?.schema==='traceharbor.provider-record.v1'||/IMPORTED RECORD/.test(document.querySelector('.mode').textContent));await mark('historical');
   await wait(214);line.textContent='Synthetic prototype. Integrity does not establish authorship, causation or production accuracy. No remediation executes.';document.getElementById('runtime-status')?.scrollIntoView({block:'center'});await mark('story-end');
  }catch{clearTimeout(deadlineTimer);line.textContent='The recorded workflow stopped. Partial evidence retained; no automatic retry.';await mark('flow-failed').catch(()=>{});channel.postMessage({type:'FLOW_FAILED',id:'TRACEHARBOR-RECOVERY004R'});}
 }
 channel.onmessage=e=>{
 if(e.data?.id==='TRACEHARBOR-RECOVERY004R'){
  if(e.data.type==='CAPTURE_STARTED'){const controls=document.getElementById('capture-controls004r');if(controls)for(const child of controls.children)if(child.id!=='phase112')child.hidden=true;}
  if(e.data.type==='CAPTURE_STARTED')line.textContent='ÎNREGISTRARE ÎN CURS. Rămâi în această filă aproximativ 4 minute; nu închide filele și nu opri partajarea.';
  if(e.data.type==='CAPTURE_FINISHED')line.textContent='CAPTURĂ SALVATĂ PRIVAT. Poți reveni la ChatGPT. Verificarea AV este încă necesară.';
  if(e.data.type==='CAPTURE_FAILED')line.textContent='CAPTURĂ OPRITĂ CU EROARE. Dovezile sunt păstrate. Revino la ChatGPT; nu apăsa Share din nou.';
 }
 if(e.data?.type==='FULL_ACK'&&e.data?.id==='TRACEHARBOR-RECOVERY004R')begin().catch(()=>{channel.postMessage({type:'FLOW_FAILED',id:'TRACEHARBOR-RECOVERY004R'});});};
 // Arming is non-media and not an AI call; only one target can arm this route.
 request('/recovery004r/status').then(async s=>{if(s.target_epoch!=='004r'||s.armed!==false||s.armed_id!==null)throw Error('DISTINCT_TARGET67_ALREADY_ARMED');for(const id of ['evolution','runtime-analyze','result'])if(!document.getElementById(id))throw Error('APP_TARGET_MISSING');await request('/recovery004r/arm004r',{client_id:clientId});document.documentElement.dataset.targetArmed004r='yes';document.dispatchEvent(new Event('traceharbor-target-ready004r'));line.textContent='Pregatit pentru Share: selecteaza aceasta fila TraceHarbor · Recording target004r si ramai aici pana la mesajul final. Filmarea dureaza aproximativ4minute; marja6minute.';}).catch(()=>{line.textContent='This view cannot arm another recording. Preserve the current attempt.';channel.close();});
})();
