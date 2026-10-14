'use strict';
// This runner starts the fixture server/browser ONLY on the admitted CI surface.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const {spawn, execFileSync} = require('node:child_process');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '..');
const origin = 'http://127.0.0.1:8787';
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const report = {schema:'traceharbor.browser-qa.v1', synthetic_only:true,
  outcome:'NOT_RUN', started_utc:new Date().toISOString(), checks:[], downloads:{},
  console:[], pageerrors:[], requests:[], rejected_external:[], failures:[],
  provider_requests:0, artifact_uploads:0, retries:0};
let server, browser;
const check = (name, details) => report.checks.push({name, outcome:'PASS', ...details});
const readStream = async stream => { const chunks=[]; for await (const x of stream) chunks.push(x); return Buffer.concat(chunks); };
async function overflow(page, label, width) {
  const geometry = await page.evaluate(() => ({width:innerWidth, scrollWidth:document.documentElement.scrollWidth,
    bodyWidth:document.body.scrollWidth, height:document.documentElement.scrollHeight}));
  assert.equal(geometry.width,width);
  assert.ok(geometry.scrollWidth <= width+1, 'Horizontal overflow: '+label);
  check('layout-'+label,{geometry});
}
async function importFile(page, bytes, expectedStatus) {
  const reply = page.waitForResponse(r => r.url()===origin+'/verify' && r.request().method()==='POST');
  await page.locator('#import-record').setInputFiles({name:'synthetic-dossier.json', mimeType:'application/json', buffer:bytes});
  const response=await reply;
  assert.equal(response.status(),expectedStatus);
  if (expectedStatus===200) {
    await page.waitForFunction(() => document.querySelector('#notice').textContent.startsWith('Imported dossier verified.'));
    assert.equal(await page.locator('#export').isEnabled(),true);
  } else {
    await page.waitForFunction(() => document.querySelector('#notice').className==='error');
    assert.equal(await page.locator('#export').isEnabled(),false);
    assert.equal(await page.locator('#result').textContent(),'');
  }
  return response.json();
}
async function main() {
  assert.equal(process.env.GITHUB_ACTIONS,'true','CI-only boundary');
  assert.equal(process.env.GITHUB_REPOSITORY,'Elinfiny/TraceHarbor');
  assert.equal(process.env.GITHUB_RUN_ATTEMPT,'1','No reruns');
  assert.equal(process.env.GITHUB_EVENT_NAME,'pull_request');
  const event=JSON.parse(fs.readFileSync(process.env.GITHUB_EVENT_PATH,'utf8'));
  assert.equal(event.repository.id,1391430317); assert.equal(event.repository.private,false);
  assert.equal(event.pull_request.base.sha,process.env.QA_EXPECTED_BASE);
  report.head=execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim();
  assert.equal(report.head,process.env.QA_EXPECTED_HEAD);
  report.parent=execFileSync('git',['cat-file','-p','HEAD'],{cwd:root,encoding:'utf8'}).split('\n').filter(s=>s.startsWith('parent '));
  assert.deepEqual(report.parent,['parent '+process.env.QA_EXPECTED_BASE]);
  report.tree=execFileSync('git',['rev-parse','HEAD^{tree}'],{cwd:root,encoding:'utf8'}).trim();
  report.run_id=process.env.GITHUB_RUN_ID; report.attempt=process.env.GITHUB_RUN_ATTEMPT;
  report.playwright=require('playwright/package.json').version;
  assert.equal(report.playwright,'1.56.1');
  const lock=JSON.parse(fs.readFileSync(path.join(__dirname,'package-lock.json')));
  report.package_integrities=Object.fromEntries(Object.entries(lock.packages).filter(([key])=>key.startsWith('node_modules/')).map(([key,v])=>[key,v.integrity]));
  report.browser_builds=JSON.parse(fs.readFileSync(path.join(__dirname,'node_modules/playwright-core/browsers.json'))).browsers.filter(b=>b.name.startsWith('chromium'));
  assert.ok(report.browser_builds.every(b=>b.revision==='1194' && b.browserVersion==='141.0.7390.37'));
  server=spawn('python3',['-u','app.py','serve','--port','8787'],{cwd:root,stdio:['ignore','pipe','pipe']});
  await new Promise((resolve,reject)=>{
    const timeout=setTimeout(()=>reject(new Error('Fixture server startup deadline')),10000);
    server.once('error',e=>{clearTimeout(timeout);reject(e);});
    server.once('exit',code=>{clearTimeout(timeout);reject(new Error('Fixture server exit '+code));});
    server.stdout.once('data',chunk=>{clearTimeout(timeout);assert.ok(chunk.toString().includes('DEMO_NO_AI'));resolve();});
  });
  browser=await chromium.launch({headless:true});
  report.browser_version=browser.version(); assert.equal(report.browser_version,'141.0.7390.37');
  const statuses={complete:'supported_reference',missing:'uncertain',contradictory:'conflicted'};
  for (const width of [1440,390]) {
    const context=await browser.newContext({viewport:{width,height:1000},acceptDownloads:true,reducedMotion:'reduce'});
    await context.route('**/*',route=>{
      const url=route.request().url();
      if (new URL(url).origin===origin) return route.continue();
      report.rejected_external.push(url);return route.abort();
    });
    const page=await context.newPage();
    page.on('console',message=>report.console.push({width,type:message.type(),text:message.text(),location:message.location()}));
    page.on('pageerror',error=>report.pageerrors.push({width,message:error.message}));
    page.on('response',response=>report.requests.push({width,url:response.url(),status:response.status(),method:response.request().method()}));
    await page.goto(origin,{waitUntil:'networkidle'});
    await page.keyboard.press('Tab');assert.equal(await page.locator('.brand').evaluate(e=>e===document.activeElement),true);
    await page.keyboard.press('Tab');
    assert.equal(await page.locator('[data-case=complete]').evaluate(e=>e===document.activeElement),true);
    const focus=await page.locator('[data-case=complete]').evaluate(e=>({outline:getComputedStyle(e).outlineStyle,width:getComputedStyle(e).outlineWidth}));
    assert.notEqual(focus.outline,'none');assert.equal(focus.width,'3px');
    check('keyboard-focus',{width,focus});
    for (const [name,status] of Object.entries(statuses)) {
      const analyzed=page.waitForResponse(r=>r.url()===origin+'/analyze');
      if (name==='complete') await page.keyboard.press('Enter');
      else await page.locator('[data-case='+name+']').click();
      const response=await analyzed;assert.equal(response.status(),200);
      const data=await response.json();
      await page.waitForFunction(() => document.querySelector('#notice').textContent.startsWith('Demo result ready.'));
      assert.equal(data.analysis.status,status);assert.equal(data.verification.citation_integrity,'PASS');
      assert.equal(data.verification.semantic_reference,'PASS_KNOWN_REFERENCE_ONLY');
      assert.equal(data.mode,'DEMO_NO_AI');assert.equal(data.live_api,'NOT_ACTIVATED');
      assert.equal(data.remediation_execution,'NOT_SUPPORTED');assert.equal(data.evidence.synthetic,true);
      assert.equal(await page.locator('.badge').textContent(),status.replaceAll('_',' '));
      assert.equal(await page.locator('.event').count(),data.evidence.timeline.length);
      assert.equal(data.evidence.counts.input_events-data.evidence.counts.unique_events,data.evidence.counts.duplicates);
      assert.equal(data.evidence.timeline.reduce((n,e)=>n+e.occurrences.length,0),data.evidence.counts.input_events);
      const knownTimes=data.evidence.timeline.filter(e=>e.timestamp_state==='known').map(e=>e.timestamp);
      assert.deepEqual(knownTimes,[...knownTimes].sort());
      let linked=0;
      for (const hypothesis of data.analysis.hypotheses) for(const side of ['supports','contradicts']) for(const citation of hypothesis[side]) {
        const source=data.evidence.sources.find(s=>s.id===citation.source_id);
        assert.equal(source.sha256,citation.source_sha256);
        assert.equal(source.events.find(e=>e.id===citation.event_id).text,citation.quote);
        linked++;
      }
      const links=page.locator('.link'); const count=await links.count();
      for(let i=0;i<count;i++) {
        const link=links.nth(i);const label=await link.textContent();const id=label.split('/')[0];
        await link.click();const target=page.locator('#source-'+id);
        assert.equal(await target.evaluate(e=>e.open && e===document.activeElement),true);
      }
      const quoted=await page.locator('.citation > p').allTextContents();
      const expected=data.analysis.hypotheses.flatMap(h=>[...h.supports,...h.contradicts].map(c=>c.quote));
      assert.deepEqual(quoted,expected);
      assert.equal(await page.locator('#result img').count(),0);
      assert.equal(await page.evaluate(()=>window.compromised),undefined);
      if(name==='contradictory') assert.ok((await page.locator('#result').textContent()).includes('<img'));
      await overflow(page,width+'-'+name,width);
      const downloadPromise=page.waitForEvent('download');await page.locator('#export').click();
      const download=await downloadPromise;assert.equal(await download.failure(),null);
      const bytes=await readStream(await download.createReadStream());const downloaded=JSON.parse(bytes);
      assert.deepEqual(downloaded,data);const digest=hash(bytes);
      report.downloads[digest]={filename:download.suggestedFilename(),bytes:bytes.length,json:downloaded};
      const verified=await importFile(page,bytes,200);assert.deepEqual(verified,data);
      await overflow(page,width+'-'+name+'-import',width);
      const tampered=structuredClone(downloaded);tampered.analysis.summary+=' SYNTHETIC_TAMPER';
      const refusal=await importFile(page,Buffer.from(JSON.stringify(tampered)),400);
      assert.equal(typeof refusal.error,'string');assert.ok(refusal.error.length>0);
      await overflow(page,width+'-'+name+'-tamper',width);
      check('case-journey',{width,case:name,status,citations:linked,clicked_source_links:count,
        download_sha256:digest,download_bytes:bytes.length,verify_status:200,tamper_status:400,tamper_error:refusal.error});
    }
    await context.close();
  }
  assert.deepEqual(report.pageerrors,[]);assert.deepEqual(report.rejected_external,[]);
  // Retain every console entry. Only the deliberate verifier 400 and the
  // browser's optional favicon 404 are classified as controlled HTTP notices.
  const unexpected=report.console.filter(e=>e.type==='error' && !(
    e.text.startsWith('Failed to load resource:') && (
      (e.location.url===origin+'/verify' && e.text.includes('400')) ||
      (e.location.url===origin+'/favicon.ico' && e.text.includes('404')))));
  assert.deepEqual(unexpected,[],'Unexpected browser console errors');
  assert.ok(report.requests.every(r=>r.status<400 || (r.url===origin+'/verify' && r.status===400) || (r.url===origin+'/favicon.ico' && r.status===404)));
  check('console-network-boundary',{unexpected_errors:0,pageerrors:0,external_requests:0});
  report.outcome='PASS';
}
main().catch(error=>{report.outcome='FAIL';report.failures.push({message:error.message,stack:error.stack});process.exitCode=1;}).finally(async()=>{
  if(browser) try {await browser.close();} catch(error) {report.failures.push({cleanup:error.message});process.exitCode=1;report.outcome='FAIL';}
  if(server) server.kill('SIGTERM');
  report.finished_utc=new Date().toISOString();
  const bytes=Buffer.from(JSON.stringify(report));assert.ok(bytes.length<=25*1024*1024,'Evidence bound');
  fs.writeFileSync(path.join(__dirname,'browser-evidence.json'),bytes);
  const encoded=bytes.toString('base64');const chunks=encoded.match(/.{1,4000}/g)||[];
  console.log('TRACE_QA_SHA256 '+hash(bytes)+' '+bytes.length+' '+chunks.length);
  chunks.forEach((chunk,i)=>console.log('TRACE_QA_CHUNK '+String(i).padStart(4,'0')+' '+chunk));
  if(process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY,
    'TraceHarbor synthetic browser QA: '+report.outcome+'\n\nHead: '+report.head+'\n\nEvidence SHA-256: '+hash(bytes)+' ('+bytes.length+' bytes). JSON is in job logs; no paid artifact storage.\n');
});
