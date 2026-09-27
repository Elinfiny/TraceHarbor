"""Provider-record extension; the accepted offline v1 verifier is unchanged."""
from core import digest, shape, text
from service import analyze, verify_dossier
from verifier import verify_analysis, VerificationError
from nebius import ENDPOINT

LIMITS = ('Quotes and evidence hashes are checked. Semantic entailment is NOT VERIFIED. '
          'Imported provider metadata is an unauthenticated record, not proof of a live call. '
          'Remediation is a proposal only.')

def verified_analysis(result, evidence):
    integrity = verify_analysis(result, evidence)
    if result['status'] == 'supported_reference' or any(
            h['assessment'] == 'supported_reference' for h in result['hypotheses']):
        raise VerificationError('A provider hypothesis cannot claim reference validation.')
    if result['status'] in ('uncertain', 'conflicted') and not result['missing_evidence']:
        raise VerificationError('Uncertainty must identify evidence still needed.')
    return integrity

def build_record(raw, analysis, provider):
    baseline = analyze(raw)
    dossier = {'schema': 'traceharbor.provider-record.v1', 'mode': 'PROVIDER_RESPONSE_RECORD',
        'live_api': 'RECORDED_NOT_INDEPENDENTLY_ATTESTED', 'remediation_execution': 'NOT_SUPPORTED',
        'baseline_dossier': baseline, 'evidence': baseline['evidence'], 'analysis': analysis,
        'provider': provider, 'verification': {
            'citation_integrity': verified_analysis(analysis, baseline['evidence']),
            'semantic_reference': 'NOT_VERIFIED', 'limits': LIMITS}}
    dossier['dossier_sha256'] = digest(dossier)
    verify_record(dossier)
    return dossier

def verify_record(dossier):
    try:
        shape(dossier, {'schema', 'mode', 'live_api', 'remediation_execution',
            'baseline_dossier', 'evidence', 'analysis', 'provider', 'verification', 'dossier_sha256'})
        expected = {'schema': 'traceharbor.provider-record.v1', 'mode': 'PROVIDER_RESPONSE_RECORD',
                    'live_api': 'RECORDED_NOT_INDEPENDENTLY_ATTESTED', 'remediation_execution': 'NOT_SUPPORTED'}
        if any(dossier[k] != v for k, v in expected.items()): raise ValueError('Record declaration mismatch.')
        verify_dossier(dossier['baseline_dossier'])
        if dossier['evidence'] != dossier['baseline_dossier']['evidence']:
            raise ValueError('Record evidence mismatch.')
        integrity = verified_analysis(dossier['analysis'], dossier['evidence'])
        if dossier['verification'] != {'citation_integrity': integrity, 'semantic_reference': 'NOT_VERIFIED', 'limits': LIMITS}:
            raise ValueError('Record verification mismatch.')
        p = dossier['provider']
        shape(p, {'endpoint', 'model', 'usage', 'response_sha256', 'request_sha256', 'finish_reason'})
        text(p['model'], 180)
        if p['endpoint'] != ENDPOINT or not p['model'].startswith('nvidia/') or p['finish_reason'] != 'stop':
            raise ValueError('Provider metadata mismatch.')
        for key in ('response_sha256', 'request_sha256'):
            if not isinstance(p[key], str) or len(p[key]) != 64 or any(c not in '0123456789abcdef' for c in p[key]):
                raise ValueError('Invalid provider digest.')
        shape(p['usage'], {'prompt_tokens', 'completion_tokens', 'total_tokens'})
        u = p['usage']
        if any(type(v) is not int or v < 0 for v in u.values()) or u['completion_tokens'] > 1500 or u['total_tokens'] != u['prompt_tokens']+u['completion_tokens']:
            raise ValueError('Invalid recorded usage.')
        if digest({k: v for k, v in dossier.items() if k != 'dossier_sha256'}) != dossier['dossier_sha256']:
            raise ValueError('Record hash mismatch.')
    except (KeyError, TypeError, AttributeError, RecursionError):
        raise ValueError('Malformed provider record.') from None
    return True

def verify_import(dossier):
    if isinstance(dossier, dict) and dossier.get('schema') == 'traceharbor.provider-record.v1':
        verify_record(dossier)
    else:
        verify_dossier(dossier)
    return dossier
