'use strict';
/* Source strings only enter textContent. No HTML injection, eval, or external requests. */
let dossier = null;
let requestSequence = 0;
let evolutionSeed = null;
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
function render(data, options = {}) {
  if (data.schema === 'traceharbor.evolution.v1') { renderEvolution(data, options); return; }
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
function showCitations(parent, citations, contrary = false) {
  if (!citations.length) parent.append(node('p', 'None cited; absence is not proof.', 'small muted'));
  citations.forEach(c => {
    const quote = node('div', undefined, 'citation ' + (contrary ? 'contrary' : ''));
    quote.append(node('p', c.quote), evidenceLink(c.source_id, `${c.source_id}/${c.event_id}`));
    parent.append(quote);
  });
}
function evolutionRequest(includeCapture, includeContrary = false) {
  if (!evolutionSeed) throw new Error('Load the synthetic evolution scenario first.');
  const before = evolutionSeed.before;
  const after = {...before, sources: [...before.sources]};
  if (includeCapture) after.sources.push(evolutionSeed.captured_source);
  if (includeContrary) after.sources.push(evolutionSeed.contrary_source);
  return JSON.stringify({schema: 'traceharbor.evolution-request.v1', before, after,
    expected_before_sha256: evolutionSeed.expected_before_sha256});
}
function renderEvolution(data, {focusSummary = false} = {}) {
  dossier = data; byId('export').disabled = false;
  const root = byId('result'); root.replaceChildren();
  const review = card(data.delta.added_sources.length ? 'What changed the conclusion?' : 'The next useful check');
  review.classList.add('evolution-review');
  review.firstElementChild.id = 'evolution-review-heading';
  review.setAttribute('aria-labelledby', 'evolution-review-heading');
  const summary = node('div', undefined, 'evolution-summary');
  summary.id = 'evolution-summary'; summary.tabIndex = -1;
  summary.setAttribute('role', 'status'); summary.setAttribute('aria-live', 'polite');
  summary.setAttribute('aria-atomic', 'true');
  summary.append(node('span', data.after.rule_outcome.replaceAll('_', ' '), 'badge'),
    node('p', 'Analysis status: ' + data.after.analysis.status.replaceAll('_', ' '), 'small'),
    node('p', data.after.why));
  review.append(summary);
  review.append(node('span', 'DETERMINISTIC SYNTHETIC RULE · NO AI CALL', 'badge'),
    node('p', data.after.next_check.proposal), node('p', 'Proposal only · no command or remediation executes.', 'small muted'));
  showCitations(review, data.after.next_check.basis);
  if (evolutionSeed && evolutionSeed.expected_before_sha256 === data.expected_before_sha256) {
    if (!data.delta.added_sources.length) {
      const add = node('button', 'Add captured verification →', 'primary'); add.id = 'add-evolution-source';
      add.addEventListener('click', () => run(() => evolutionRequest(true), '/evolution', {focusEvolutionSummary: true}));
      review.append(add, node('p', 'Reveals one synthetic source: the exact configuration diff and two matched replay records. It runs no check.', 'small muted'));
    } else if (!data.after.evidence.sources.some(s => s.id === evolutionSeed.contrary_source.id)) {
      const conflict = node('button', 'Review a conflicting capture', 'secondary'); conflict.id = 'add-evolution-conflict';
      conflict.addEventListener('click', () => run(() => evolutionRequest(true, true), '/evolution', {focusEvolutionSummary: true}));
      review.append(conflict);
    }
  }
  root.append(review);
  const comparison = node('div', undefined, 'columns evolution-comparison'); comparison.id = 'evolution-comparison';
  for (const [key, title] of [['before', 'Before · initial evidence'], ['after', 'After · current evidence']]) {
    const snapshot = data[key], section = card(title);
    section.append(node('span', snapshot.rule_outcome.replaceAll('_', ' '), 'badge'), node('p', snapshot.why));
    snapshot.analysis.hypotheses.forEach(h => {
      section.append(node('h3', h.label), node('h3', 'Supporting evidence'));
      showCitations(section, h.supports);
      section.append(node('h3', 'Contrary evidence · retained'));
      showCitations(section, h.contradicts, true);
    });
    if (!snapshot.analysis.hypotheses.length) section.append(node('p', 'No causal hypothesis. Missing evidence remains explicit.', 'small muted'));
    section.append(node('p', `${snapshot.evidence.sources.length} sources · ${snapshot.evidence.warnings.length} timestamp flags`, 'small muted'));
    comparison.append(section);
  }
  root.append(comparison);
  const delta = card('Evidence delta · append-only review');
  delta.append(node('p', data.delta.explanation), node('p', `Conclusion changed: ${data.delta.conclusion_changed ? 'yes' : 'no'} · edited sources: 0 · removed sources: 0`, 'small muted'));
  data.delta.added_sources.forEach(s => {
    delta.append(node('h3', 'Added source: ' + s.source_id), node('p', s.source_sha256, 'hash'));
    showCitations(delta, s.citations);
  });
  if (!data.delta.added_sources.length) delta.append(node('p', 'No source added yet. The comparison correctly stays unknown.'));
  root.append(delta);
  const inspector = card('Source inspector · all current evidence');
  data.after.evidence.sources.forEach(s => {
    const details = node('details'); details.id = 'source-' + s.id; details.tabIndex = -1;
    details.append(node('summary', `${s.id} · ${s.kind}`), node('p', s.title), node('p', s.sha256, 'hash'), node('pre', JSON.stringify(s.raw, null, 2)));
    inspector.append(details);
  });
  const timeline = card('Evidence timeline · correlation is not causation');
  data.after.evidence.timeline.forEach(e => {
    const row = node('article', undefined, 'event');
    row.append(node('time', e.timestamp || `TIME ${e.timestamp_state.toUpperCase()}`), node('p', e.text));
    e.occurrences.forEach(o => row.append(evidenceLink(o.source_id, `${o.source_id}/${o.event_id}`)));
    if (e.timestamp_state !== 'known') row.append(node('p', e.timestamp_candidates.join(' / '), 'small muted'));
    timeline.append(row);
  });
  root.append(inspector, timeline, node('p', data.verification.limits, 'small muted'), node('p', 'Dossier SHA-256 ' + data.dossier_sha256, 'hash'));
  // Only an explicit Add/Review action requests focus; initial load/import never does.
  if (focusSummary && data.delta.added_sources.length) {
    summary.focus({preventScroll: true});
    summary.scrollIntoView({behavior: 'auto', block: 'start'});
  }
}
async function run(load, endpoint = '/analyze', {focusEvolutionSummary = false} = {}) {
  const sequence = ++requestSequence;
  if (endpoint !== '/evolution') evolutionSeed = null;
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
    render(data, {focusSummary: focusEvolutionSummary});
    const imported = endpoint === '/verify';
    const providerRecord = data.schema === 'traceharbor.provider-record.v1';
    const evolution = data.schema === 'traceharbor.evolution.v1';
    document.querySelector('.mode').textContent = providerRecord ? 'IMPORTED RECORD · LIVE ORIGIN NOT ATTESTED' : evolution ? 'EVIDENCE EVOLUTION · DETERMINISTIC · NO AI CALL' : 'DEMONSTRATION · NO AI CALLS';
    byId('notice').textContent = imported ? 'Imported dossier verified. This browser made no AI call; file integrity does not authenticate its origin.' : evolution ? 'Evidence review ready. Added sources and contrary evidence remain visible. No check or AI call was executed.' : 'Demo result ready. No AI call or remediation was performed.';
  } catch (error) {
    if (sequence !== requestSequence) return;
    byId('notice').className = 'error'; byId('notice').textContent = error.message || 'Import failed.';
  }
}
byId('evolution').addEventListener('click', () => {
  const sequence = requestSequence + 1;
  document.querySelectorAll('[data-case]').forEach(b => b.setAttribute('aria-pressed', 'false'));
  run(async () => {
    const response = await fetch('/scenarios/evolution.json');
    if (!response.ok) throw new Error('Evolution scenario unavailable.');
    const scenario = await response.json();
    if (sequence !== requestSequence) throw new Error('Superseded scenario load.');
    evolutionSeed = scenario;
    return evolutionRequest(false);
  }, '/evolution');
});
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
  const a = node('a'); a.href = url; a.download = (dossier.evidence || dossier.after.evidence).case_id + '-dossier.json'; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
