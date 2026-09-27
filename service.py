import re
from core import import_package, digest, canonical, shape, identifier, text, MAX_SOURCES, MAX_EVENTS
from adapters import DemoAdapter
from verifier import verify_analysis, verify_semantics

_RUNTIME = {'schema': 'traceharbor.dossier.v1', 'mode': 'DEMO_NO_AI',
            'live_api': 'NOT_ACTIVATED', 'remediation_execution': 'NOT_SUPPORTED'}
_LIMITS = 'Exact quotes do not prove conclusions. Semantic checks cover three synthetic reference cases only.'
_HASH = re.compile(r'^[0-9a-f]{64}$')


def analyze(raw):
    evidence = import_package(raw)
    adapter = DemoAdapter()
    result = adapter.analyze(evidence)
    integrity = verify_analysis(result, evidence)
    semantic = verify_semantics(result, adapter.identify(evidence))
    dossier = {**_RUNTIME, 'evidence': evidence, 'analysis': result,
               'verification': {'citation_integrity': integrity, 'semantic_reference': semantic,
                                'limits': _LIMITS}}
    dossier['dossier_sha256'] = digest(dossier)
    return dossier


def _hash_field(value):
    if not isinstance(value, str) or not _HASH.fullmatch(value):
        raise ValueError('Expected lowercase SHA-256 text.')


def _bounded_list(value, maximum, minimum=0):
    if not isinstance(value, list) or not minimum <= len(value) <= maximum:
        raise ValueError('Dossier list has an invalid type or size.')


def verify_dossier(dossier):
    """Validate the offline v1 contract and recompute evidence/verification claims.

    SHA-256 checks content integrity; an unkeyed hash does not authenticate the
    exporter or prove real-world truth. Received input bytes are not in this
    export, so input_sha256 is format-checked as a receipt, not authenticated.
    """
    try:
        shape(dossier, set(_RUNTIME) | {'evidence', 'analysis', 'verification', 'dossier_sha256'})
        for key, expected in _RUNTIME.items():
            if dossier[key] != expected:
                raise ValueError('Unsupported dossier version or runtime declaration: ' + key)
        _hash_field(dossier['dossier_sha256'])
        ev = dossier['evidence']
        shape(ev, {'schema', 'case_id', 'title', 'synthetic', 'input_sha256',
                   'analysis_fingerprint', 'sources', 'timeline', 'warnings', 'counts'})
        if ev['schema'] != 'traceharbor.evidence.v1' or ev['synthetic'] is not True:
            raise ValueError('Unsupported evidence version or synthetic declaration.')
        identifier(ev['case_id']); text(ev['title'], 160)
        for key in ('input_sha256', 'analysis_fingerprint'):
            _hash_field(ev[key])
        _bounded_list(ev['sources'], MAX_SOURCES, 1)
        _bounded_list(ev['timeline'], MAX_EVENTS, 1)
        _bounded_list(ev['warnings'], MAX_EVENTS)
        shape(ev['counts'], {'input_events', 'unique_events', 'duplicates'})
        for count in ev['counts'].values():
            # bool and 1.0 can compare equal to ints but violate the field contract.
            if type(count) is not int or not 0 <= count <= MAX_EVENTS:
                raise ValueError('Event counts must be bounded integers.')
        for source in ev['sources']:
            shape(source, {'id', 'kind', 'title', 'sha256', 'raw', 'events'})
            _bounded_list(source['events'], MAX_EVENTS, 1)
        reconstructed = import_package(canonical({
            'schema': 'traceharbor.input.v1', 'synthetic': True,
            'case_id': ev['case_id'], 'title': ev['title'],
            'sources': [s['raw'] for s in ev['sources']]}))
        # Rebuilding verifies raw structure and all nested normalized records,
        # including required fields, exact types/values, hashes and linkages.
        for key in reconstructed:
            if key != 'input_sha256' and ev[key] != reconstructed[key]:
                raise ValueError('Evidence reconstruction mismatch: ' + key)
        integrity = verify_analysis(dossier['analysis'], ev)
        semantic = verify_semantics(dossier['analysis'], DemoAdapter().identify(ev))
        shape(dossier['verification'], {'citation_integrity', 'semantic_reference', 'limits'})
        expected = {'citation_integrity': integrity, 'semantic_reference': semantic, 'limits': _LIMITS}
        if dossier['verification'] != expected:
            raise ValueError('Verification metadata contradicts the recomputed result or its limits.')
        body = {k: v for k, v in dossier.items() if k != 'dossier_sha256'}
        if digest(body) != dossier['dossier_sha256']:
            raise ValueError('Dossier hash mismatch.')
    except (KeyError, TypeError, AttributeError, RecursionError, OverflowError) as exc:
        raise ValueError('Malformed dossier.') from exc
    return True
