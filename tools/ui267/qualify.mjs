// Actual-app WebDriver qualification, Node built-ins only. No downloads or AI.
// Execution requires separate native Master admission before the exact CI branch.
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import net from 'node:net';
import crypto from 'node:crypto';
import {spawn, execFileSync} from 'node:child_process';
import {setTimeout as delay} from 'node:timers/promises';
import {fileURLToPath} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const arg = (name, fallback) => args.includes(name) ? args[args.indexOf(name)+1] : fallback;
const source = path.resolve(arg('--source', path.join(here, '../..')));
const output = path.resolve(arg('--out', path.join(os.tmpdir(), 'trace-ui267-result')));
const validateOnly = args.includes('--validate-only');
const selectedGroups = new Set(arg('--groups','1,2,3').split(','));
if (!selectedGroups.size || [...selectedGroups].some(g=>!['1','2','3'].includes(g))) throw new Error('Only three reviewed groups exist.');
const effectKey = 'TRACE180_UI_CORRECTED_QUALIFICATION_ATTEMPT2';
let qualifiedPython;
async function runtimeConfig282() {
  const runtime=process.env.TRACE295_RUNTIME_CONFIG; check(runtime&&path.isAbsolute(runtime),'No admitted root runtime context'); const rs=await fs.lstat(runtime); check(rs.isFile()&&!rs.isSymbolicLink()&&rs.uid===0&&(rs.mode&0o777)===0o440,'Runtime context ownership'); check(await fs.realpath(runtime)===runtime,'Runtime path redirect'); const rb=await fs.readFile(runtime); check(rb.length<=16384&&sha(rb)===process.env.TRACE295_RUNTIME_SHA,'Runtime context hash'); const c=JSON.parse(rb);
  check(c.schema==='TRACE_UI282_CONFIGURATION_V1' && c.status==='ADOPTED_SEPARATE_NATIVE_ADMISSION_REQUIRED','SOURCE_ONLY_UNADMITTED');
  // A config is not independent adoption or native effect authority. The caller
  // must prove both before a separately admitted future attempt2.
  const e=c.required_executables;
  for (const k of ['node','python3','chrome','chromedriver']) {
    const x=e[k];check(x&&x.state==='QUALIFIED'&&/^\/[A-Za-z0-9_./+-]+$/.test(x.path||'')&&!x.path.split('/').includes('..')&&/^[0-9a-f]{64}$/.test(x.sha256||''),'Unqualified exact executable '+k);
    check(sha(await fs.readFile(x.path))===x.sha256,'Executable drift '+k);
  }
  check(await fs.realpath(process.execPath)===await fs.realpath(e.node.path),'Wrong actual Node');
  check(e.chrome.path===expected.chrome_path&&e.chromedriver.path===expected.driver_path,'Browser path drift');
  qualifiedPython=e.python3.path;
}
const tag = 'review/traceharbor-v1-browser-qa-base180-162-20261023';
const expected = JSON.parse(await fs.readFile(path.join(here, 'environment.json'), 'utf8'));
const guards = JSON.parse(await fs.readFile(path.join(here, 'source-guards.json'), 'utf8'));
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const E = 'element-6066-11e4-a52e-4f735466cecf';
const result = {schema:'TRACE_UI280_CORRECTED_BROWSER_RECEIPT_V1', effect_key:effectKey,
  execution:'NOT_RUN', groups:['1_DESKTOP_REAL_FIRST_FLOW','2_CONFLICT_KEYBOARD_EXPORT_REIMPORT','3_MOBILE360_AND_DESKTOP_LAYOUT'].map(name=>({name,status:'NOT_RUN',observed:null})), browser_screenshots:0, inference_requests:0,
  session_create_attempts:0,
  selected_groups:[...selectedGroups],
  ordinary_actions_first_flow:0, measured_first_flow_ms:null,
  source_guard:'NOT_CHECKED', max_resident_sum_bytes:null,
  authority:'Environment/event checks bind provenance only, not Owner authority. External native Master admission is required before creating the exact branch.'};
const children = []; let session = null, driverURL = null, stop = null, monitor = null;
let driverLog = '', applicationLog = '';
let appURL = null;
const check = (ok, message) => {if (!ok) throw new Error(message);};

async function atomicJSON(name, value) {
  await fs.mkdir(output, {recursive:true, mode:0o700});
  const target = path.join(output, name);
  const data = Buffer.from(JSON.stringify(value, null, 2)+'\n');
  check(data.length <= 65536, 'Receipt exceeds 64 KiB bound.');
  await fs.writeFile(target+'.new', data, {flag:'wx', mode:0o600});
  await fs.rename(target+'.new', target);
}
async function sourceCheck() {
  result.qualification_source_pin = Object.fromEntries(await Promise.all(['qualify.mjs','environment.json','source-guards.json'].map(async n=>[n,sha(await fs.readFile(path.join(here,n)))])));
  for (const row of guards.exact_runtime_files) {
    check(!path.isAbsolute(row.path) && !row.path.split('/').includes('..'), 'Unsafe source guard path.');
    const b = await fs.readFile(path.join(source, row.path));
    check(b.length === row.bytes && sha(b) === row.sha256, 'Source differs: '+row.path);
  }
  result.source_guard = 'PASS_21_EXACT_FILES';
  result.candidate265_sha256 = guards.candidate265_sha256;
}
function eventCheck() {
  check(process.env.GITHUB_ACTIONS === 'true' && process.env.RUNNER_ENVIRONMENT === 'github-hosted', 'No admitted standard hosted CI context.');
  check(os.userInfo().uid !== 0, 'Root browser execution refused; sandbox must remain intact.');
  check(process.env.GITHUB_EVENT_NAME === 'push' && process.env.GITHUB_RUN_ATTEMPT === '1', 'Only separately admitted push attempt1 is eligible.');
  const ev = JSON.parse(execFileSync(qualifiedPython, ['-B','-c',
    'import json,os;print(json.dumps(json.load(open(os.environ["GITHUB_EVENT_PATH"]))))'], {encoding:'utf8', maxBuffer:262144}));
  check(ev.ref === 'refs/heads/review/traceharbor-v1-browser-qa-base180-162-20261023' && process.env.GITHUB_REF===ev.ref && ev.before==='d502e3b79735ff065b7d9d936c8330ff14bd21a0' && ev.after===process.env.GITHUB_SHA && ev.created===false && ev.deleted===false && ev.forced===false && ev.repository.id === 1391430317 && ev.repository.private === false,
    'Wrong event ref/repository/visibility.');
  check(ev.sender.id === 273768139 && process.env.GITHUB_ACTOR_ID === '273768139', 'Wrong actual event actor.');
  check(process.env.GITHUB_REPOSITORY === 'Elinfiny/TraceHarbor' && /^[0-9a-f]{40}$/.test(process.env.GITHUB_SHA || ''), 'Unpinned source.');
  check(process.env.TRACE267_WORKFLOW_SHA === process.env.GITHUB_SHA, 'Workflow/source event commits differ.');
  result.image_environment_diagnostic={ImageVersion:process.env.ImageVersion||null,ImageOS:process.env.ImageOS||null,authoritative:false}; // Nativejobsetupverification is external acceptance gate.
  result.native_event_binding = {commit:process.env.GITHUB_SHA, workflow_commit:process.env.TRACE267_WORKFLOW_SHA,
    run_id:process.env.GITHUB_RUN_ID, attempt:1, ref:tag, image:process.env.ImageVersion};
}
function versionCheck() {
  const osRelease=execFileSync(qualifiedPython,['-I','-S','-B','-c','print(open("/etc/os-release").read())'],{encoding:'utf8',maxBuffer:8192});
  check(/^ID=ubuntu$/m.test(osRelease)&&/^VERSION_ID="24.04"$/m.test(osRelease),'Actual OS drift'); result.os_release=osRelease;
  const browser = execFileSync(expected.chrome_path, ['--version'], {encoding:'utf8', timeout:5000}).trim();
  const driver = execFileSync(expected.driver_path, ['--version'], {encoding:'utf8', timeout:5000}).trim();
  check(browser === 'Google Chrome '+expected.chrome_version, 'Chrome executable/version drift.');
  check(driver.startsWith('ChromeDriver '+expected.chrome_version+' '), 'ChromeDriver version drift.');
  check(process.version === expected.node_version, 'Node runtime drift.');
  const python = execFileSync(qualifiedPython, ['-B','-c','import sys;print(".".join(map(str,sys.version_info[:3])))'], {encoding:'utf8'}).trim();
  check(python === expected.python_version, 'Python image runtime drift.');
  result.environment = {browser, driver, browser_path:expected.chrome_path, driver_path:expected.driver_path,
    node:process.version, python, sandbox_flags_removed:false, native_setup_identity_verified:false};
}
async function freePort() {
  const server = net.createServer(); await new Promise((resolve,reject) => server.once('error',reject).listen(0,'127.0.0.1',resolve));
  const port = server.address().port; await new Promise(resolve => server.close(resolve)); return port;
}
function launch(command, options) {
  const child = spawn(command, options.args, {cwd:options.cwd || source, env:{...process.env, PYTHONDONTWRITEBYTECODE:'1'},
    stdio:['ignore','pipe','pipe'], detached:true}); children.push(child);
  child.on('error', e => {stop = new Error('Process launch failed: '+e.code);});
  child.stdout.on('data', b => {if (options.kind === 'driver') driverLog = (driverLog+b).slice(-16384);});
  child.stderr.on('data', b => {if (options.kind === 'driver') driverLog = (driverLog+b).slice(-16384); else applicationLog = (applicationLog+b).slice(-8192);});
  return child;
}

// SOURCE_ONLY280: physical cgroup accounting is prospective, not old-RSS conformity.
function resolveOwnedCgroup280(member, mounts, unit) {
  check(/^traceharbor-ui280-a2-[0-9]{1,20}\.service$/.test(unit),'Bad owned unit identity');
  check(member.startsWith('/') && path.posix.normalize(member)===member && member.endsWith('/'+unit),'Wrong owned membership');
  const unescape=s=>s.replace(/\\([0-7]{3})/g,(_,oct)=>String.fromCharCode(parseInt(oct,8)));
  const candidates=[];
  for(const line of mounts.trim().split('\n')) {
    const pair=line.split(' - '); if(pair.length!==2 || pair[1].split(' ')[0]!=='cgroup2')continue;
    const left=pair[0].split(' '),root=unescape(left[3]),mount=unescape(left[4]);
    if(!left[5].split(',').includes('ro'))continue;
    check(path.posix.normalize(root)===root && path.posix.normalize(mount)===mount,'Unsafe mount path');
    if(member===root || member.startsWith(root==='/'?'/':root+'/')) {
      const relative=root==='/'?member.slice(1):member.slice(root.length).replace(/^\//,'');
      const full=path.posix.join(mount,relative);check(full===mount||full.startsWith(mount+'/'),'Cgroup path escape');candidates.push(full);
    }
  }
  check(candidates.length===1,'Missing/ambiguous readonly cgroup mapping');return candidates[0];
}
function numeric280(s,name) {
 check(/^(0|[1-9][0-9]*)\s*$/.test(s),'Invalid cgroup '+name);const n=Number(s.trim());check(Number.isSafeInteger(n),'Unsafe cgroup '+name);return n;
}
let cgroup280=null,initialEvents280=null;
async function cgroupSnapshot280() {
 const names=['memory.max','memory.swap.max','memory.current','memory.peak','memory.events'];
 const values=await Promise.all(names.map(n=>fs.readFile(cgroup280+'/'+n,'utf8')));
 const snap={max:numeric280(values[0],'max'),swap:numeric280(values[1],'swap'),current:numeric280(values[2],'current'),peak:numeric280(values[3],'peak'),events:{}};
 for(const row of values[4].trim().split('\n')){const [k,v]=row.split(/\s+/);snap.events[k]=numeric280(v,'event');}
 check(snap.max>0 && snap.max<=335544320 && snap.swap===0,'Kernel budget not enforced');
 check(snap.current<=snap.max && snap.peak<=snap.max,'Cgroup charge/peak exceeded bound');
 if(initialEvents280)for(const k of ['max','oom','oom_kill'])check((snap.events[k]||0)===(initialEvents280[k]||0),'Cgroup limit/OOM event');
 return snap;
}
async function prelaunchMemory280() {
 check(process.getuid()>0,'Root browser refused');
 const membership=(await fs.readFile('/proc/self/cgroup','utf8')).trim().split('\n').filter(s=>s.startsWith('0::'));
 check(membership.length===1,'Unsupported cgroup version');
 cgroup280=resolveOwnedCgroup280(membership[0].slice(3),await fs.readFile('/proc/self/mountinfo','utf8'),process.env.TRACE280_UNIT||'');
 check(/^[0-9a-f]{32}$/.test(process.env.INVOCATION_ID||''),'No native service invocation');
 const procs=(await fs.readFile(cgroup280+'/cgroup.procs','utf8')).trim().split(/\s+/);
 check(procs.includes(String(process.pid)),'Caller escaped owned cgroup');
 const status=await fs.readFile('/proc/self/status','utf8');
 check(/^NoNewPrivs:\s+1$/m.test(status)&&/^CapEff:\s+0+$/m.test(status),'Privilege confinement missing');
 const dev=(await fs.readFile('/proc/self/net/dev','utf8')).split('\n').filter(s=>s.includes(':')).map(s=>s.split(':')[0].trim());
 check(dev.length===1&&dev[0]==='lo','External network interface present');
 check(String((await fs.stat('/proc/self/ns/net')).ino)!==process.env.TRACE280_PARENT_NETNS,'No separate network namespace');
 check((await fs.readFile('/proc/sys/kernel/unprivileged_userns_clone','utf8')).trim()==='1','Sandbox user namespace support unavailable');
 const snap=await cgroupSnapshot280();for(const k of ['max','oom','oom_kill'])check((snap.events[k]||0)===0,'Initial cgroup limit/OOM event');initialEvents280=snap.events;
 result.cgroup280={path:cgroup280,unit:process.env.TRACE280_UNIT,invocation:process.env.INVOCATION_ID,initial:snap};
 result.native_setup_identity='PENDING_INDEPENDENT_GITHUB_JOB_HEADER_READBACK';
 result.old_image_conflict={setup:'20261012.334.1',environment:'20261023.334.3',resolved:false};
}

async function residentMonitor() {
  result.cgroup280.latest=await cgroupSnapshot280();
  // Conservative sum includes shared resident pages more than once; never relax the cap.
  const table = new Map();
  for (const name of await fs.readdir('/proc')) {
    if (!/^\d+$/.test(name)) continue;
    try {
      const raw = await fs.readFile('/proc/'+name+'/status', 'utf8');
      table.set(Number(name), {ppid:Number(raw.match(/^PPid:\s+(\d+)/m)?.[1] || 0),
        rss:Number(raw.match(/^VmRSS:\s+(\d+)/m)?.[1] || 0)*1024});
    } catch {}
  }
  const wanted = new Set([process.pid]); let changed = true;
  while (changed) {changed = false; for (const [pid,r] of table) if (wanted.has(r.ppid) && !wanted.has(pid)) {wanted.add(pid); changed=true;}}
  let bytes = 0; for (const pid of wanted) bytes += table.get(pid)?.rss || 0;
  result.max_resident_sum_bytes = Math.max(result.max_resident_sum_bytes, bytes);
  result.descendant_RSS_diagnostic_exceeded_old_bound = bytes > 335544320; // Proposed kernel-accounting correction; oldfailure remains breached.
}
async function waitFor(read, predicate, label, milliseconds=8000) {
  const end = Date.now()+milliseconds; let last;
  while (Date.now() < end) {
    if (stop) throw stop;
    last = await read(); if (predicate(last)) return last; await delay(100);
  }
  throw new Error('Timed out: '+label+'; do not rerun the qualification automatically.');
}
async function command(endpoint, method='GET', body) {
  if (stop && method !== 'DELETE') throw stop;
  const res = await fetch(driverURL+endpoint, {method, headers:{'Content-Type':'application/json'},
    body:body === undefined ? undefined : JSON.stringify(body), signal:AbortSignal.timeout(8000)});
  const raw = await res.text(); check(raw.length < 262144, 'WebDriver response bound.');
  const value = JSON.parse(raw).value;
  check(res.ok && !value?.error, 'WebDriver error: '+(value?.error || res.status)); return value;
}
async function wd(endpoint, method='GET', body) {return command('/session/'+session+endpoint, method, body);}
async function observe(script) {return wd('/execute/sync','POST',{script:'return ('+script+');',args:[]});}
async function element(selector) {return (await wd('/element','POST',{using:'css selector',value:selector}))[E];}
async function click(selector) {await wd('/element/'+await element(selector)+'/click','POST',{});}
async function text(selector) {return wd('/element/'+await element(selector)+'/text');}
async function key(value) {await wd('/actions','POST',{actions:[{type:'key',id:'keyboard',actions:[{type:'keyDown',value},{type:'keyUp',value}]}]});}
async function outcome(expectedText) {
  return waitFor(() => text('#result'), s => s.includes(expectedText), expectedText);
}
async function checkNetwork() {
  const logs = await wd('/log','POST',{type:'performance'}); check(logs.length <= 5000, 'Network log count bound.');
  const urls = [];
  for (const row of logs) {
    const msg = JSON.parse(row.message).message;
    if (msg.method === 'Network.requestWillBeSent') {
      const url = msg.params.request.url;
      if (/^(data:|blob:|about:)/.test(url)) continue;
      check(new URL(url).origin === appURL, 'Unexpected browser network origin.'); urls.push(new URL(url).pathname);
    }
  }
  return [...new Set(urls)].slice(0,50);
}
async function openSession(mobile=false) {
  if (stop) throw stop;
  const chromeOptions = {binary:expected.chrome_path,
    args:['--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--disable-background-networking','--js-flags=--max-old-space-size=32'],
    prefs:{'download.default_directory':path.join(output,'downloads'),'download.prompt_for_download':false}};
  if (mobile) chromeOptions.mobileEmulation = {deviceMetrics:{width:360,height:800,pixelRatio:1,mobile:true,touch:true}};
  result.session_create_attempts++;
  const data = await command('/session','POST',{capabilities:{alwaysMatch:{browserName:'chrome',acceptInsecureCerts:false,
    'goog:chromeOptions':chromeOptions,'goog:loggingPrefs':{performance:'ALL'}}}});
  session = data.sessionId;
  check(data.capabilities.browserVersion === expected.chrome_version && data.capabilities.acceptInsecureCerts === false, 'Actual browser capability drift.');
  if (!mobile) await wd('/window/rect','POST',{width:1366,height:900});
  await wd('/url','POST',{url:appURL});
  await waitFor(() => observe('document.readyState'), v => v === 'complete', 'app document ready');
  check(await observe('typeof document.getElementById("evolution")?.onclick') !== 'undefined', 'Actual controls missing.');
  const resources = await observe('performance.getEntriesByType("resource").map(e=>new URL(e.name).pathname)');
  check(resources.includes('/app.js') && resources.includes('/style.css'), 'Real external JS/CSS did not load.');
}
async function closeSession() {if (session) {try {await wd('','DELETE');} finally {session=null;}}}
async function group(name, action) {
  const row = result.groups.find(g=>g.name===name); check(Boolean(row), 'Unknown qualification group.');
  if (!selectedGroups.has(name[0])) {row.status='SKIPPED_NO_RETEST'; return;}
  if (stop) {row.status='NOT_RUN_BLOCKED_NO_RETRY'; return;}
  try {row.observed = await action(); row.status='PASS';}
  catch (e) {row.status='FAIL'; row.error=e.message;}
}
async function layout() {
  return observe('({width:innerWidth,height:innerHeight,scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth,'+
    'cards:Array.from(document.querySelectorAll("#result .card")).slice(0,3).map(e=>({text:e.querySelector("h2")?.innerText,'+
    'width:e.getBoundingClientRect().width})),next:({text:document.querySelector(".evolution-review>p")?.innerText,'+
    'font:parseFloat(getComputedStyle(document.querySelector(".evolution-review>p")).fontSize)}),' +
    'outcomes:Array.from(document.querySelectorAll(".evolution-comparison .badge")).map(e=>e.innerText)})');
}
async function run() {
  await sourceCheck();
  if (validateOnly) {
    result.execution='SOURCE_BOUND_PLAN_CHECK_ONLY'; result.groups=guards.acceptance_groups.map(name=>({name,status:'NOT_RUN'}));
    await atomicJSON('source-bound-plan-check.json',result); return;
  }
  await prelaunchMemory280(); // Before ALL event/version subprocesses and once effects.
  await runtimeConfig282();
  eventCheck(); versionCheck();
  await fs.mkdir(output,{recursive:true,mode:0o700});
  // Once reservation remains after failure/UNKNOWN; no reset/cleanup of this file.
  await fs.writeFile(path.join(output,'ATTEMPT_UI280_ATTEMPT2.json'),JSON.stringify({effect_key:effectKey,event:result.native_event_binding}),{flag:'wx',mode:0o600});
  result.execution='ATTEMPTING_REAL_BROWSER';
  const appPort = await freePort(), driverPort = await freePort(); appURL='http://127.0.0.1:'+appPort;
  driverURL='http://127.0.0.1:'+driverPort;
  launch(qualifiedPython,{args:['-B','app.py','serve','--port',String(appPort)],kind:'app'});
  launch(expected.driver_path,{args:['--port='+driverPort,'--allowed-ips=127.0.0.1'],kind:'driver'});
  const deadline = setTimeout(()=>{stop=new Error('180 second driver deadline reached.');},180000);
  monitor=setInterval(()=>residentMonitor().catch(()=>{stop=new Error('Resident resource observation failed.');}),100);
  try {
    await waitFor(async()=>{try{return (await fetch(appURL,{signal:AbortSignal.timeout(500)})).status;}catch{return 0;}}, v=>v===200,'loopback server');
    await waitFor(async()=>{try{return (await fetch(driverURL+'/status',{signal:AbortSignal.timeout(500)})).status;}catch{return 0;}},v=>v===200,'installed ChromeDriver');
    await openSession();
    if (!selectedGroups.has('1')) {
      await click('#evolution'); await outcome('UNKNOWN'); await click('#add-evolution-source'); await outcome('SUPPORTED SYNTHETIC RULE');
      result.setup_actions_for_selected_group=2;
    }
    await group('1_DESKTOP_REAL_FIRST_FLOW',async()=>{
      const start=performance.now(); await click('#evolution'); result.ordinary_actions_first_flow++;
      await outcome('UNKNOWN');
      const before=await text('.evolution-comparison');
      await click('#add-evolution-source'); result.ordinary_actions_first_flow++;
      await outcome('SUPPORTED SYNTHETIC RULE'); result.measured_first_flow_ms=performance.now()-start;
      const after=await text('.evolution-comparison'); const allQuotes=await observe('Array.from(document.querySelectorAll("#result .citation p")).map(e=>e.innerText)');
      check((await text('.mode')).includes('DETERMINISTIC') && (await text('.mode')).includes('NO AI CALL'),'Rendered mode mislabels deterministic output as inference.');
      check(guards.fixture.support_quotes.every(q=>allQuotes.includes(q)), 'Rendered supporting source/event quotations differ.');
      check(before.includes('UNKNOWN') && after.includes('UNKNOWN') && after.includes('SUPPORTED SYNTHETIC RULE'), 'Rendered before/after outcomes missing.');
      check(result.ordinary_actions_first_flow<=2 && result.measured_first_flow_ms<=30000,'First flow action/time bound failed.');
      const first=await observe('(()=>{const card=document.querySelector(".evolution-review"),badge=Array.from(card.querySelectorAll(".badge")).find(e=>e.innerText.includes("SUPPORTED SYNTHETIC RULE")),r=badge?.getBoundingClientRect();return {text:card.innerText,quoteTop:card.querySelector(".citation")?.getBoundingClientRect().top,outcomeTop:r?.top,outcomeVisible:Boolean(r&&r.height>0&&r.top>=0&&r.bottom<=innerHeight),visible:card.getBoundingClientRect().top<innerHeight};})()');
      result.first_flow_observed={before:before.slice(0,1000),after:after.slice(0,1800),first_card:first};
      // Strict acceptance: a later card/status in JSON is not sufficient.
      check(first.visible && first.outcomeVisible && first.text.includes('SUPPORTED SYNTHETIC RULE') && (first.quoteTop===undefined || first.outcomeTop<first.quoteTop),'First card does not show the visible conclusion before long quotations.');
      return {first_flow_ms:result.measured_first_flow_ms,actions:2,before_text:before.slice(0,1000),after_text:after.slice(0,1500),network:await checkNetwork()};
    });
    await group('2_CONFLICT_KEYBOARD_EXPORT_REIMPORT',async()=>{
      await click('#add-evolution-conflict'); await outcome('CONFLICTED');
      const quotes=await observe('Array.from(document.querySelectorAll("#result .contrary p")).map(e=>e.innerText)');
      check(quotes.includes(guards.fixture.contrary_quote),'Contrary source is not rendered.');
      await click('.evolution-comparison .contrary button');
      const focus=await observe('({id:document.activeElement.id,open:document.activeElement.open})');
      check(focus.id==='source-conflicting-capture' && focus.open===true,'Source inspector focus/open behavior failed.');
      let tabCount=0; while(await observe('document.activeElement.id')!=='export' && tabCount<64) {await key('\uE004');tabCount++;}
      check(await observe('document.activeElement.id')==='export','Keyboard cannot reach export.');
      await key('\uE007');
      const downloads=path.join(output,'downloads');
      const file=await waitFor(async()=>{try{return (await fs.readdir(downloads)).filter(n=>n.endsWith('-dossier.json'))[0]||null;}catch{return null;}},v=>Boolean(v),'actual UI download');
      const full=path.join(downloads,file); const bytes=await fs.readFile(full); check(bytes.length<=262144,'Export exceeds input limit.');
      const exported=JSON.parse(bytes); check(exported.after.rule_outcome==='CONFLICTED' && exported.after.analysis.status==='conflicted','Actual UI export lost uncertainty.');
      await wd('/element/'+await element('#import-record')+'/value','POST',{text:full,value:[full]});
      await waitFor(()=>text('#notice'),v=>v.includes('Imported dossier verified'),'real file import control');
      await outcome('CONFLICTED');
      return {contrary_quote:quotes[0],source_focus:focus,keyboard_tabs:tabCount,download_sha256:sha(bytes),export_bytes:bytes.length,reimport_notice:await text('#notice'),network:await checkNetwork()};
    });
    let desktop=selectedGroups.has('3')?await layout():null;
    await closeSession(); if (selectedGroups.has('3')) await openSession(true);
    await group('3_MOBILE360_AND_DESKTOP_LAYOUT',async()=>{
      await click('#evolution'); await outcome('UNKNOWN'); await click('#add-evolution-source'); await outcome('SUPPORTED SYNTHETIC RULE');
      const mobile=await layout();
      check(mobile.width===360,'Actual mobile viewport is not 360px.');
      for (const l of [desktop,mobile]) {
        check(l.scroll<=l.client+1,'Horizontal overflow in actual rendered viewport.');
        check(l.next.text.length>0 && l.next.font>=14,'Primary next check is missing/unreadable.');
        check(l.outcomes[0]==='UNKNOWN' && ['SUPPORTED SYNTHETIC RULE','CONFLICTED'].includes(l.outcomes[1]),'Before/after outcomes missing.');
      }
      return {desktop,mobile,network:await checkNetwork()};
    });
    await residentMonitor(); if (stop) throw stop;
    result.execution=result.groups.every(g=>['PASS','SKIPPED_NO_RETEST'].includes(g.status))?(selectedGroups.size===3?'PASS_REAL_BROWSER_3_GROUPS':'PASS_REAL_BROWSER_SELECTED_GROUPS'):'FAIL_REAL_BROWSER_AFFECTED_GROUPS_ONLY';
  } finally {clearTimeout(deadline);}
}
try {await run();}
catch(e) {result.execution=session?'FAIL_OR_INDETERMINATE_REAL_BROWSER':result.session_create_attempts?'SETUP_UNKNOWN_OR_FAILED_NO_RETRY':'NOT_RUN_PREFLIGHT_OR_SETUP_BLOCKED';result.error=e.message;}
finally {
  if (monitor) clearInterval(monitor);
  try {await closeSession();} catch {}
  for (const child of children.reverse()) {try {process.kill(-child.pid,'SIGTERM');} catch {}}
  result.finished_utc=new Date().toISOString();
  if (!validateOnly) {
    result.output_logs_redacted={driver:driverLog.replaceAll(source,'SOURCE').slice(-2000),app:applicationLog.replaceAll(source,'SOURCE').slice(-1000)};
    await atomicJSON('ui267-receipt.json',result);
  }
  // Small synthetic-only receipt in native job logs; no artifact upload/action.
  console.log(JSON.stringify(result));
}
if (validateOnly ? result.execution!=='SOURCE_BOUND_PLAN_CHECK_ONLY' : !['PASS_REAL_BROWSER_3_GROUPS','PASS_REAL_BROWSER_SELECTED_GROUPS'].includes(result.execution)) process.exitCode=1;
