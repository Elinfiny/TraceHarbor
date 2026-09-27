/* Node DOM contract smoke: no native browser, layout, focus, or visual claim. */
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const nodes = new Map();
const created = [];
let downloaded = null;
let exported = null;
class Element {
  constructor(tag) { this.tagName = tag; this.children = []; this.handlers = {}; this.attributes = {}; this._text = ''; this.disabled = false; this.dataset = {}; created.push(this); }
  set id(value) { this._id = value; nodes.set(value, this); }
  get id() { return this._id; }
  set textContent(value) { this._text = String(value); this.children = []; }
  get textContent() { return this._text + this.children.map(e => e.textContent).join(' '); }
  append(...elements) { this.children.push(...elements); }
  replaceChildren(...elements) { this._text = ''; this.children = [...elements]; }
  addEventListener(event, handler) { this.handlers[event] = handler; }
  setAttribute(name, value) { this.attributes[name] = value; }
  scrollIntoView() { this.scrolled = true; }
  focus() { this.focused = true; }
  click() { if (this.tagName === 'a') downloaded = this.download; else return this.handlers.click?.(); }
}
for (const id of ['result','notice','export','upload']) { const n = new Element('div'); n.id = id; }
const buttons = ['complete','missing','contradictory'].map(name => { const b = new Element('button'); b.dataset.case = name; return b; });
const sandbox = {
  document: {getElementById: id => nodes.get(id), createElement: tag => new Element(tag), querySelectorAll: () => buttons},
  TextEncoder, Blob, URL: {createObjectURL: blob => {exported = blob; return 'blob:synthetic';}, revokeObjectURL: () => {}}, setTimeout: fn => fn(),
  fetch: async () => { throw new Error('Unexpected request in renderer smoke.'); }
};
vm.createContext(sandbox);
const js = fs.readFileSync(path.join(root,'web','app.js'),'utf8');
assert(!/innerHTML|outerHTML|insertAdjacentHTML|document\.write|\beval\s*\(|new Function/.test(js));
vm.runInContext(js, sandbox, {filename:'app.js'});
(async () => {
  for (const name of ['complete','missing','contradictory']) {
    const data = JSON.parse(fs.readFileSync(path.join(root,'references',name+'.dossier.json')));
    sandbox.render(data);
    const rendered = nodes.get('result').textContent;
    assert(rendered.includes(data.analysis.summary));
    assert(rendered.includes(data.evidence.sources[0].sha256));
    assert(rendered.includes('Remediation proposal'));
    const link = created.find(e => e.className === 'link' && e.textContent === 'config/c1');
    if (link && name !== 'missing') { link.click(); assert(nodes.get('source-config').open); assert(nodes.get('source-config').focused); }
    if (name === 'contradictory') {
      assert(rendered.includes('<img src=x onerror='));
      assert(rendered.includes('task_deadline_ms=5000 during the same incident window'));
      assert(!created.some(e => e.tagName === 'img'));
      assert.equal(sandbox.compromised, undefined);
    }
    nodes.get('export').click();
    assert.equal(downloaded,data.evidence.case_id+'-dossier.json');
    assert.deepEqual(JSON.parse(await exported.text()), data);
    console.log(`PASS render / evidence navigation / export: ${name}`);
  }
  await sandbox.run(async () => {throw new Error('Synthetic import error');});
  assert.equal(nodes.get('export').disabled,true);
  assert.equal(nodes.get('result').textContent,'');
  assert.equal(nodes.get('notice').textContent,'Synthetic import error');
  console.log('PASS controlled import error clears stale result and disables export');
  console.log('PASS untrusted text has no HTML execution sink');
  console.log('SCOPE: Node DOM contract smoke only; native browser/visual/accessibility validation PENDING.');
})().catch(error => {console.error(error);process.exitCode=1;});
