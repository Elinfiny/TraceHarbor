"""Citation integrity is separate from semantic agreement on known reference cases."""
import json
from pathlib import Path
from core import InputError, shape, text, identifier, digest

class VerificationError(ValueError):
    pass

def verify_analysis(analysis, evidence):
    try:
        shape(analysis, {'status', 'summary', 'hypotheses', 'missing_evidence', 'remediation'})
        if analysis['status'] not in {'supported_reference', 'uncertain', 'conflicted', 'unknown'}:
            raise InputError('Unknown analysis status.')
        text(analysis['summary'], 2000)
        for key in ('hypotheses', 'missing_evidence', 'remediation'):
            if not isinstance(analysis[key], list) or len(analysis[key]) > 12: raise InputError('Analysis list out of bounds.')
        for item in analysis['missing_evidence']: text(item, 2000)
        lookup = {}
        for s in evidence['sources']:
            if digest(s['raw']) != s['sha256']: raise InputError('Source hash mismatch.')
            for e in s['events']: lookup[s['id'], e['id']] = (s['sha256'], e['text'])
        ids = set()
        for h in analysis['hypotheses']:
            shape(h, {'id', 'label', 'assessment', 'supports', 'contradicts'})
            identifier(h['id']); text(h['label'], 256)
            if h['id'] in ids: raise InputError('Duplicate hypothesis id.')
            ids.add(h['id'])
            if h['assessment'] not in {'supported_reference', 'uncertain', 'conflicted', 'alternative_unresolved'}: raise InputError('Invalid assessment.')
            for side in ('supports', 'contradicts'):
                if not isinstance(h[side], list) or len(h[side]) > 30: raise InputError('Citation list out of bounds.')
                for c in h[side]:
                    shape(c, {'source_id', 'event_id', 'source_sha256', 'quote'})
                    identifier(c['source_id']); identifier(c['event_id']); text(c['quote'])
                    original = lookup.get((c['source_id'], c['event_id']))
                    if not original or original[0] != c['source_sha256'] or c['quote'] != original[1]:
                        raise InputError('Citation identifier, source hash or exact full-event quote mismatch.')
        for r in analysis['remediation']:
            shape(r, {'id', 'proposal', 'preconditions', 'risk', 'rollback', 'verification'})
            identifier(r['id'])
            for k in ('proposal', 'risk', 'rollback'): text(r[k], 2000)
            for k in ('preconditions', 'verification'):
                if not isinstance(r[k], list) or not 1 <= len(r[k]) <= 12: raise InputError('Missing remediation conditions.')
                for v in r[k]: text(v, 2000)
        if analysis['status'] == 'unknown' and (analysis['hypotheses'] or analysis['remediation']):
            raise InputError('Unknown cases must abstain.')
    except (InputError, TypeError, KeyError, AttributeError) as exc:
        raise VerificationError(str(exc)) from exc
    return 'PASS'

def verify_semantics(analysis, reference_name):
    """Bounded ground-truth checks. This is NOT a general semantic entailment engine."""
    if reference_name is None:
        if analysis['status'] != 'unknown' or analysis['hypotheses'] or analysis['remediation']:
            raise VerificationError('Unrecognized case did not abstain.')
        return 'NOT_EVALUATED_UNKNOWN_CASE'
    truth = json.loads((Path(__file__).parent/'references'/'expectations.json').read_text())[reference_name]
    hypotheses = {h['id']: h for h in analysis['hypotheses']}
    main = hypotheses.get('deadline-regression')
    if analysis['status'] != truth['status'] or not main or main['assessment'] != truth['status'] or main['label'] != truth['main_label']:
        raise VerificationError('Reference conclusion or uncertainty mismatch.')
    # These references are hand-specified from scenario truth, separate from generated citations.
    for side in ('supports', 'contradicts'):
        found = {(c['source_id'], c['event_id']) for c in main[side]}
        if found != {tuple(x) for x in truth[side]}: raise VerificationError('Reference evidence polarity mismatch.')
    required = truth['missing_contains']
    if required and not any(required in s for s in analysis['missing_evidence']):
        raise VerificationError('Required missing evidence was not requested.')
    if not required and analysis['missing_evidence']: raise VerificationError('Unexpected reference missing-evidence result.')
    return 'PASS_KNOWN_REFERENCE_ONLY'
