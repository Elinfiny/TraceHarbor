"""Auditable, additive synthetic evidence review. Deterministic rules, no AI/network.

This extension does not alter v1 dossiers, the three reference cases or records.
Unkeyed hashes detect changes, not authorship or coordinated rewrites.
"""
import json
import re
from core import canonical, digest, import_package, citation, shape, MAX_BYTES
from verifier import verify_analysis

SCHEMA = 'traceharbor.evolution.v1'
MODE = 'DETERMINISTIC_SYNTHETIC_RULES_NO_AI'
LIMITS = ('Only the documented synthetic deadline/replay rule is evaluated. '
          'Quoted records and their claimed provenance are untrusted data, not independently authenticated facts. '
          'A controlled synthetic explanation is not a production diagnosis or NVIDIA inference. '
          'Unkeyed hashes do not authenticate origin or prevent a coordinated rewrite. No checks or remediation execute.')
CONTEXT = ('incident', 'worker', 'release', 'window')
COMMON = {'record', *CONTEXT}
FIELDS = {
    'observation': COMMON | {'duration_ms', 'outcome'},
    'configuration': COMMON | {'task_deadline_ms', 'approved_task_deadline_ms', 'capture_id'},
    'replay': COMMON | {'trial', 'task_deadline_ms', 'duration_ms', 'outcome', 'workload_sha256', 'harness_sha256'},
}
HASH = re.compile(r'^[0-9a-f]{64}$')


def _records(evidence):
    """Interpret a small typed data vocabulary; never execute source instructions."""
    rows = []
    for s in evidence['sources']:
        for e in s['events']:
            try:
                r = json.loads(e['text'], object_pairs_hook=_unique_pairs)
            except (ValueError, TypeError, RecursionError):
                continue
            if not isinstance(r, dict) or not isinstance(r.get('record'), str) or r['record'] not in FIELDS:
                continue
            if set(r) != FIELDS[r['record']]:
                continue
            if any(not isinstance(r[k], str) or not r[k].strip() or len(r[k]) > 160 for k in CONTEXT):
                continue
            if any(type(v) is not int or not 1 <= v <= 86_400_000
                   for k, v in r.items() if k.endswith('_ms')):
                continue
            if r['record'] in ('observation', 'replay') and r['outcome'] not in ('timeout', 'completed'):
                continue
            if r['record'] == 'configuration' and (not isinstance(r['capture_id'], str) or not r['capture_id'].strip()):
                continue
            if r['record'] == 'replay' and (not isinstance(r['trial'], str) or not r['trial'].strip()
                    or any(not isinstance(r[k], str) or not HASH.fullmatch(r[k]) for k in ('workload_sha256', 'harness_sha256'))):
                continue
            rows.append((r, citation(evidence, s['id'], e['id'])))
    return rows


def _unique_pairs(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise ValueError('Duplicate fact key.')
        result[k] = v
    return result


def _assess(evidence):
    rows = _records(evidence)
    observations = [(r, c) for r, c in rows if r['record'] == 'observation' and r['outcome'] == 'timeout']
    analysis = {'status': 'unknown', 'summary': 'Insufficient matched evidence; no causal hypothesis.',
                'hypotheses': [], 'missing_evidence': [], 'remediation': []}
    outcome = 'UNKNOWN'
    relevant, support, contrary = [], [], []
    check = 'Obtain an incident-window timeout observation with worker, release and window identifiers.'
    why = 'The typed evidence does not identify one incident context.'
    contexts = {tuple(r[k] for k in CONTEXT) for r, _ in observations}
    if len(contexts) == 1:
        context = next(iter(contexts))
        relevant = [(r, c) for r, c in rows if tuple(r[k] for k in CONTEXT) == context]
        obs = [(r, c) for r, c in relevant if r['record'] == 'observation' and r['outcome'] == 'timeout']
        configs = [(r, c) for r, c in relevant if r['record'] == 'configuration']
        replays = [(r, c) for r, c in relevant if r['record'] == 'replay']
        scope = f"{context[0]} / {context[1]} / {context[2]} / {context[3]}"
        check = ('Read the captured runtime task_deadline_ms and approved target for ' + scope +
                 '. Preserve capture provenance; then compare same-workload, same-harness deadline replays. Proposal only.')
        why = 'Timeouts alone cannot distinguish a deadline regression from slow work.'
        values = {(r['task_deadline_ms'], r['approved_task_deadline_ms']) for r, _ in configs}
        if len(values) > 1:
            outcome = 'CONFLICTED'
            support = [c for _, c in obs] + [c for r, c in configs if r['task_deadline_ms'] != r['approved_task_deadline_ms']]
            contrary = [c for r, c in configs if r['task_deadline_ms'] == r['approved_task_deadline_ms']]
            # Even when both samples differ from target, every conflicting sample stays visible.
            if not contrary:
                contrary = [c for _, c in configs]
            check = 'Reconcile capture identity, worker, release and collection provenance for the disagreeing runtime samples in ' + scope + '. Do not select a cause or change configuration.'
            why = 'Matched-context runtime samples disagree; added replay data cannot erase this contradiction.'
            analysis.update(status='conflicted', summary=why)
        elif configs:
            cfg, cc = configs[0]
            check = ('Compare two controlled synthetic replays of the identical workload and harness at '
                     f"{cfg['task_deadline_ms']} ms versus the approved {cfg['approved_task_deadline_ms']} ms. "
                     'Preserve exact input/harness hashes and outcomes. Proposal only; no command is executed.')
            why = 'A configuration difference is present; a timestamp or difference alone does not establish a causal mechanism.'
            matching = []
            for a, ac in replays:
                for b, bc in replays:
                    if (a['trial'] != b['trial'] and a['task_deadline_ms'] == cfg['task_deadline_ms']
                            and b['task_deadline_ms'] == cfg['approved_task_deadline_ms']
                            and a['task_deadline_ms'] < a['duration_ms'] <= b['task_deadline_ms']
                            and a['duration_ms'] == b['duration_ms']
                            and a['outcome'] == 'timeout' and b['outcome'] == 'completed'
                            and a['workload_sha256'] == b['workload_sha256']
                            and a['harness_sha256'] == b['harness_sha256']):
                        matching.append((ac, bc))
            adverse = [c for r, c in replays if
                       ((r['task_deadline_ms'] == cfg['approved_task_deadline_ms'] and r['outcome'] == 'timeout') or
                        (r['task_deadline_ms'] == cfg['task_deadline_ms'] and r['outcome'] == 'completed'))]
            if matching and cfg['task_deadline_ms'] != cfg['approved_task_deadline_ms']:
                support = [c for _, c in obs] + [cc, *matching[0]]
                contrary = adverse
                outcome = 'CONFLICTED' if adverse else 'SUPPORTED_SYNTHETIC_RULE'
                why = ('The matched configuration diff plus identical-workload/harness replays support a deadline mechanism in this synthetic rule. '
                       'This is conditional on the supplied data, not independently verified production causation.')
                if adverse:
                    why = 'Contrary replay outcomes remain present; do not promote the deadline explanation to a resolved cause.'
                analysis.update(status='conflicted' if adverse else 'uncertain', summary=why)
                check = ('Review capture authenticity and reproducibility with an authorized investigator. '
                         'Any production diagnosis or configuration change needs independent evidence and approval.')
    elif len(contexts) > 1:
        why = 'More than one incident context is present. Select a single incident before comparison.'
    if outcome != 'UNKNOWN':
        analysis['hypotheses'] = [{'id': 'deadline-mechanism', 'label': 'Deadline configuration mechanism in the supplied synthetic case',
                                  'assessment': 'conflicted' if outcome == 'CONFLICTED' else 'uncertain',
                                  'supports': support, 'contradicts': contrary}]
    analysis['missing_evidence'] = [check]
    verify_analysis(analysis, evidence)
    return {'rule_outcome': outcome, 'analysis': analysis,
            'why': why, 'next_check': {'proposal': check, 'execution': 'NOT_EXECUTED',
                                     'basis': [c for r, c in relevant if r['record'] in ('observation', 'configuration')]}}


def evolve(request):
    shape(request, {'schema', 'before', 'after', 'expected_before_sha256'})
    if request['schema'] != 'traceharbor.evolution-request.v1':
        raise ValueError('Unsupported evolution request.')
    if digest(request['before']) != request['expected_before_sha256']:
        raise ValueError('Before input hash changed; comparison refused.')
    before = import_package(canonical(request['before']))
    after = import_package(canonical(request['after']))
    if (before['case_id'], before['title']) != (after['case_id'], after['title']):
        raise ValueError('Comparison must retain the same incident identity and title.')
    old = {s['id']: s for s in before['sources']}
    new = {s['id']: s for s in after['sources']}
    if any(sid not in new or new[sid]['raw'] != s['raw'] for sid, s in old.items()):
        raise ValueError('Earlier evidence was edited or removed; append sources instead.')
    added = [s for s in after['sources'] if s['id'] not in old]
    a, b = _assess(before), _assess(after)
    delta = {'added_sources': [{'source_id': s['id'], 'source_sha256': s['sha256'],
                              'citations': [citation(after, s['id'], e['id']) for e in s['events']]} for s in added],
             'unchanged_source_ids': list(old), 'edited_sources': [], 'removed_sources': [],
             'before_outcome': a['rule_outcome'], 'after_outcome': b['rule_outcome'],
             'conclusion_changed': a['rule_outcome'] != b['rule_outcome'], 'explanation': b['why']}
    dossier = {'schema': SCHEMA, 'mode': MODE, 'live_api': 'NOT_ACTIVATED', 'remediation_execution': 'NOT_SUPPORTED',
               'before': {'evidence': before, **a}, 'after': {'evidence': after, **b},
               'expected_before_sha256': request['expected_before_sha256'], 'delta': delta,
               'verification': {'citation_integrity': 'PASS', 'semantic_reference': 'DOCUMENTED_SYNTHETIC_RULE_ONLY', 'limits': LIMITS}}
    dossier['dossier_sha256'] = digest(dossier)
    if len(canonical(dossier)) > MAX_BYTES:
        raise ValueError('Evolution export exceeds the 256 KiB reimport limit.')
    return dossier


def verify_evolution(dossier):
    """Rebuild both snapshots and all derived claims; reject forged deltas/quotes."""
    try:
        def raw(ev):
            return {'schema': 'traceharbor.input.v1', 'synthetic': True,
                    'case_id': ev['case_id'], 'title': ev['title'], 'sources': [s['raw'] for s in ev['sources']]}
        expected = evolve({'schema': 'traceharbor.evolution-request.v1',
                           'before': raw(dossier['before']['evidence']), 'after': raw(dossier['after']['evidence']),
                           'expected_before_sha256': dossier['expected_before_sha256']})
        if expected != dossier:
            raise ValueError('Evolution reconstruction, citation or hash mismatch.')
    except (KeyError, TypeError, AttributeError, RecursionError) as exc:
        raise ValueError('Malformed evolution dossier.') from exc
    return dossier
