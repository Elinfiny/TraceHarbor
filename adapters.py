"""Deterministic known-case demonstration. Future live adapter is deliberately inert."""
from pathlib import Path
from core import import_package, citation

ROOT = Path(__file__).resolve().parent
FIXTURES = ('complete', 'missing', 'contradictory')

class LiveAdapterDisabled(RuntimeError):
    pass

class NebiusAdapter:
    """Integration boundary only: no SDK, model ID, credential lookup or network code."""
    def analyze(self, evidence):
        raise LiveAdapterDisabled('LIVE_API_NOT_ACTIVATED: access, model and spending cap require separate verification.')

class DemoAdapter:
    def __init__(self):
        self.known = {}
        for name in FIXTURES:
            evidence = import_package((ROOT/'fixtures'/f'{name}.json').read_bytes())
            self.known[evidence['analysis_fingerprint']] = (name, {(s['id'], e['id']) for s in evidence['sources'] for e in s['events']})

    def identify(self, evidence):
        match = self.known.get(evidence['analysis_fingerprint'])
        available = {(s['id'], e['id']) for s in evidence['sources'] for e in s['events']}
        return match[0] if match and match[1] <= available else None

    def analyze(self, evidence):
        name = self.identify(evidence)
        if name is None:
            return {'status': 'unknown', 'summary': 'Unrecognized synthetic case. No intelligent diagnosis was performed.',
                    'hypotheses': [], 'missing_evidence': ['Human analysis or a separately authorized live adapter is required.'], 'remediation': []}
        c = lambda s, e: citation(evidence, s, e)
        supports = [c('metrics', 'm1'), c('worker', 'w1')]
        if name != 'missing': supports.append(c('config', 'c1'))
        contrary = [c('audit', 'a1')] if name == 'contradictory' else []
        status = {'complete': 'supported_reference', 'missing': 'uncertain', 'contradictory': 'conflicted'}[name]
        summaries = {
            'complete': 'Known demo: runtime deadline 50 ms differs from approved 5000 ms; configuration regression is supported by the reference evidence.',
            'missing': 'Known demo: timeouts are observed, but the decisive runtime configuration is absent. The cause remains uncertain.',
            'contradictory': 'Known demo: runtime samples disagree (50 ms versus 5000 ms). Resolve provenance before selecting a cause.'}
        missing = {'complete': [], 'missing': ['Obtain the runtime task_deadline_ms configuration and approved value for the incident window.'],
                   'contradictory': ['Reconcile the provenance and capture time of the conflicting runtime configuration samples.']}[name]
        return {'status': status, 'summary': summaries[name], 'hypotheses': [
            {'id': 'deadline-regression', 'label': 'Runtime task deadline configuration regression', 'assessment': status, 'supports': supports, 'contradicts': contrary},
            {'id': 'workload-latency', 'label': 'Workload latency or dependency delay', 'assessment': 'alternative_unresolved', 'supports': [c('metrics', 'm1')], 'contradicts': [c('config', 'c1')] if name == 'complete' else []}],
            'missing_evidence': missing, 'remediation': [{
                'id': 'review-deadline', 'proposal': 'Consider restoring the reviewed task deadline configuration; proposal only.',
                'preconditions': ['Resolve missing or contradictory evidence first.', 'Authorized operator verifies workload requirements and reviews the exact configuration delta.', 'Capture the existing configuration and obtain an approved change window.'],
                'risk': 'Longer deadlines may increase queue backlog or conceal a different fault.',
                'rollback': 'An authorized operator restores the captured pre-change configuration if the approved checks fail.',
                'verification': ['Compare runtime configuration with the reviewed target.', 'Observe timeout rate and queue latency against a documented baseline.', 'Stop and investigate if the expected improvement is absent.']}]}
