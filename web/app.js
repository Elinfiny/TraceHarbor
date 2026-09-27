'use strict';
/* Source strings only enter textContent. No HTML injection, eval, or external requests. */
let dossier = null;
let requestSequence = 0;
const byId = id => document.getElementById(id);
function node(tag, value, className) {
  const element = document.createElement(tag);
  if (value !== undefined) element.textContent = String(value);
  if (className) element.className = className;
  return element;
}
function card(title) { const e = node('section', undefined, 'card'); e.append(node('h2', title)); return e; }
function list(parent, items) { const ul = node('ul'); items.forEach(t => ul.append(node('li', t))); parent.append(ul); }
function evidenceLink(sourceId, label) {
  const button = node('button', label || sourceId, 'link');
  button.addEventListener('click', () => { const target = byId('source-' + sourceId); if (target) { target.open = true; target.scrollIntoView({behavior: 'smooth', block: 'center'}); target.focus(); } });
  return button;
}
function render(data) {
  dossier = data; const root = byId('result'); root.replaceChildren(); byId('export').disabled = false;
  const ev = data.evidence, result = data.analysis;
  const overview = card(ev.title);
  overview.append(node('span', result.status.replaceAll('_', ' '), 'badge ' + result.status), node('p', result.summary));
  const counts = ev.counts;
  overview.append(node('p', `${ev.sources.length} sources · ${counts.unique_events} unique events · ${counts.duplicates} duplicates · ${ev.warnings.length} timestamp flags`, 'stats'));
  overview.append(node('p', `Citation integrity: ${data.verification.citation_integrity} · Semantic reference: ${data.verification.semantic_reference}`, 'small muted'));
  overview.append(node('p', data.verification.limits, 'small muted'));
  root.append(overview);
  const columns = node('div', undefined, 'columns');
  const timeline = card('Evidence timeline');
  timeline.append(node('p', 'UTC; entries without a reliable time are listed last. Equal timestamps imply no causal order.', 'small muted'));
  ev.timeline.forEach(event => {
    const row = node('article', undefined, 'event');
    row.append(node('time', event.timestamp || `TIME ${event.timestamp_state.toUpperCase()}`), node('p', event.text));
    if (event.timestamp_state !== 'known' && event.timestamp_candidates.length) row.append(node('p', 'Recorded candidates: ' + event.timestamp_candidates.join(' / '), 'small muted'));
    event.occurrences.forEach(o => row.append(evidenceLink(o.source_id, `${o.source_id}/${o.event_id}`)));
    timeline.append(row);
  });
  const sources = card('Source inspector');
  ev.sources.forEach(source => {
    const details = node('details'); details.id = 'source-' + source.id; details.tabIndex = -1;
    details.append(node('summary', `${source.id} · ${source.kind}`), node('p', source.title, 'small'), node('p', 'SHA-256 ' + source.sha256, 'hash'), node('pre', JSON.stringify(source.raw, null, 2)));
    sources.append(details);
  });
  columns.append(timeline, sources); root.append(columns);
  const hypotheses = card('Hypotheses & contrary evidence');
  if (!result.hypotheses.length) hypotheses.append(node('p', 'No diagnosis for an unrecognized case.'));
  result.hypotheses.forEach(h => {
    hypotheses.append(node('h3', h.label), node('p', h.assessment.replaceAll('_', ' '), 'small muted'));
    for (const side of ['supports', 'contradicts']) {
      hypotheses.append(node('h3', side === 'supports' ? 'Supporting evidence' : 'Contrary evidence'));
      if (!h[side].length) hypotheses.append(node('p', 'None cited; this does not prove absence.', 'small muted'));
      h[side].forEach(c => { const quote = node('div', undefined, 'citation ' + (side === 'contradicts' ? 'contrary' : '')); quote.append(node('p', c.quote), evidenceLink(c.source_id, `${c.source_id}/${c.event_id}`)); hypotheses.append(quote); });
    }
  });
  root.append(hypotheses);
  const missing = card('Evidence still needed');
  if (result.missing_evidence.length) list(missing, result.missing_evidence); else missing.append(node('p', 'The known synthetic reference is complete. This does not certify a real system.'));
  root.append(missing);
  const remediation = card('Remediation proposal · never executed');
  if (!result.remediation.length) remediation.append(node('p', 'No remediation generated.'));
  result.remediation.forEach(r => { remediation.append(node('h3', r.proposal), node('h3', 'Preconditions')); list(remediation, r.preconditions); remediation.append(node('h3', 'Risk'), node('p', r.risk), node('h3', 'Rollback'), node('p', r.rollback), node('h3', 'Verification')); list(remediation, r.verification); });
  root.append(remediation, node('p', 'Dossier SHA-256 ' + data.dossier_sha256, 'hash'));
}
async function run(load, endpoint = '/analyze') {
  const sequence = ++requestSequence;
  dossier = null; byId('export').disabled = true; byId('result').replaceChildren();
  document.querySelector('.mode').textContent = 'DEMONSTRATION · NO AI CALLS';
  byId('notice').className = ''; byId('notice').textContent = 'Validating synthetic evidence…';
  try {
    const raw = await load();
    if (new TextEncoder().encode(raw).length > 262144) throw new Error('Maximum input size is 256 KiB.');
    const response = await fetch(endpoint, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: raw});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Controlled analysis error.');
    if (sequence !== requestSequence) return;
    render(data);
    const imported = endpoint === '/verify';
    const providerRecord = data.schema === 'traceharbor.provider-record.v1';
    document.querySelector('.mode').textContent = providerRecord ? 'IMPORTED RECORD · LIVE ORIGIN NOT ATTESTED' : 'DEMONSTRATION · NO AI CALLS';
    byId('notice').textContent = imported ? 'Imported dossier verified. This browser made no AI call; file integrity does not authenticate its origin.' : 'Demo result ready. No AI call or remediation was performed.';
  } catch (error) {
    if (sequence !== requestSequence) return;
    byId('notice').className = 'error'; byId('notice').textContent = error.message || 'Import failed.';
  }
}
document.querySelectorAll('[data-case]').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('[data-case]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  run(async () => { const r = await fetch('/fixtures/' + button.dataset.case + '.json'); if (!r.ok) throw new Error('Fixture unavailable.'); return r.text(); });
}));
byId('upload').addEventListener('change', () => { const file = byId('upload').files[0]; if (!file) return; document.querySelectorAll('[data-case]').forEach(b => b.setAttribute('aria-pressed', 'false')); run(() => { if (file.size > 262144) throw new Error('Maximum input size is 256 KiB.'); return file.text(); }); });
byId('import-record').addEventListener('change', () => {
  const file = byId('import-record').files[0]; if (!file) return;
  document.querySelectorAll('[data-case]').forEach(b => b.setAttribute('aria-pressed', 'false'));
  run(() => { if (file.size > 262144) throw new Error('Maximum input size is 256 KiB.'); return file.text(); }, '/verify');
});
byId('export').addEventListener('click', () => {
  if (!dossier) return;
  const url = URL.createObjectURL(new Blob([JSON.stringify(dossier, null, 2) + '\n'], {type: 'application/json'}));
  const a = node('a'); a.href = url; a.download = dossier.evidence.case_id + '-dossier.json'; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
