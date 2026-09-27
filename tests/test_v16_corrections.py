"""Targeted regressions for V16-P01-01 and V16-P01-02. No external services."""
import copy
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core import canonical,digest
from service import analyze,verify_dossier

def input_case(name='complete'):
    return json.loads((ROOT/'fixtures'/f'{name}.json').read_text())
def exported(name='complete'):
    return json.loads((ROOT/'references'/f'{name}.dossier.json').read_text())
def rehash(d):
    d['dossier_sha256']=digest({k:v for k,v in d.items() if k!='dossier_sha256'})
    return d

def replace_deploy(events):
    data=input_case();data['sources'][0]['events']=events;return analyze(canonical(data))
def event(id,stamp,text=None,**kw):
    return {'id':id,'text':text or 'Synthetic '+id,'timestamp':stamp,**kw}

class ChronologyCorrections(unittest.TestCase):
    def test_whole_before_fraction_and_fraction_order(self):
        d=replace_deploy([event('fraction','2030-01-15T12:00:00.500000Z'),event('whole','2030-01-15T12:00:00Z'),event('fine','2030-01-15T12:00:00.000001Z'),event('tenth','2030-01-15T12:00:00.100000Z')])
        times=[e['timestamp'] for e in d['evidence']['timeline'] if e['kind']=='deployment']
        self.assertEqual(times,['2030-01-15T12:00:00Z','2030-01-15T12:00:00.000001Z','2030-01-15T12:00:00.100000Z','2030-01-15T12:00:00.500000Z'])
        self.assertTrue(verify_dossier(d))

    def test_timezone_equivalence_deduplicates_without_order_claim(self):
        d=replace_deploy([event('local','2030-01-15T14:00:00.500000+02:00','Same synthetic event'),event('utc','2030-01-15T12:00:00.5Z','Same synthetic event'),event('other','2030-01-15T07:00:00.500000-05:00','Different equal-time event')])
        timeline=[e for e in d['evidence']['timeline'] if e['kind']=='deployment']
        self.assertEqual(len(timeline),2);self.assertEqual({e['timestamp'] for e in timeline},{'2030-01-15T12:00:00.500000Z'})
        self.assertEqual(d['evidence']['counts']['duplicates'],1)
        same=next(e for e in timeline if e['text']=='Same synthetic event')
        self.assertEqual({x['event_id'] for x in same['occurrences']},{'local','utc'})
        # Do not assert causal order for two distinct events with the same instant.
        self.assertTrue(verify_dossier(d))

    def test_missing_conflict_remain_unordered_after_known(self):
        d=replace_deploy([event('missing',None,timestamp_alt='2029-01-01T00:00:00Z'),event('conflict','2029-01-01T00:00:00Z',timestamp_alt='2031-01-01T00:00:00Z'),event('known','2030-01-15T12:00:00.500000Z')])
        timeline=d['evidence']['timeline'];unknown=[e for e in timeline if e['timestamp'] is None]
        self.assertEqual(timeline[-len(unknown):],unknown)
        self.assertTrue(all(e['timestamp'] is None for e in timeline if e['timestamp_state'] in {'missing','conflict'}))
        self.assertEqual({w['code'] for w in d['evidence']['warnings']},{'TIMESTAMP_MISSING','TIMESTAMP_CONFLICT'})

class ExportContractCorrections(unittest.TestCase):
    def assert_rehashed_rejected(self,d):
        rehash(d)
        with self.assertRaises(ValueError):verify_dossier(d)

    def test_each_runtime_constant_and_schema_rejected_independently(self):
        for key,value in [('mode','LIVE_AI'),('live_api','ACTIVATED'),('remediation_execution','EXECUTED'),('schema','traceharbor.dossier.v2')]:
            with self.subTest(key=key):
                d=exported();d[key]=value;self.assert_rehashed_rejected(d)

    def test_all_original_dossiers_valid_and_outputs_byte_equivalent(self):
        for name in ('complete','missing','contradictory'):
            with self.subTest(case=name):
                original=exported(name);self.assertTrue(verify_dossier(original))
                actual=analyze((ROOT/'fixtures'/f'{name}.json').read_bytes())
                self.assertEqual(actual,original)
                self.assertEqual((json.dumps(actual,ensure_ascii=False,indent=2)+'\n').encode(), (ROOT/'references'/f'{name}.dossier.json').read_bytes())

    def test_verification_claims_recomputed_and_limit_text_fixed(self):
        for key,value in [('citation_integrity','FAIL'),('semantic_reference','NOT_EVALUATED_UNKNOWN_CASE'),('limits','All real systems validated.')]:
            with self.subTest(key=key):
                d=exported();d['verification'][key]=value;self.assert_rehashed_rejected(d)
        data=input_case();data['sources'][0]['events'][0]['text']='Unrecognized synthetic event'
        d=analyze(canonical(data));self.assertEqual(d['analysis']['status'],'unknown');self.assertTrue(verify_dossier(d))
        d['verification']['semantic_reference']='PASS_KNOWN_REFERENCE_ONLY';self.assert_rehashed_rejected(d)

    def test_evidence_version_synthetic_hash_and_integer_types(self):
        edits=[lambda e:e.update(schema='traceharbor.evidence.v2'),lambda e:e.update(synthetic=False),lambda e:e.update(synthetic=1),lambda e:e.update(input_sha256='not-a-hash'),lambda e:e.update(analysis_fingerprint='0'*64),lambda e:e['counts'].update(duplicates=False),lambda e:e['counts'].update(unique_events=5.0)]
        for i,edit in enumerate(edits):
            with self.subTest(edit=i):
                d=exported();edit(d['evidence']);self.assert_rehashed_rejected(d)

    def test_malformed_missing_extra_and_wrong_types_rejected_controlled(self):
        for bad in (None,[],{},'truncated',17):
            with self.subTest(root=bad):
                with self.assertRaises(ValueError):verify_dossier(bad)
        edits=[lambda d:d.pop('analysis'),lambda d:d.update(extra=True),lambda d:d.update(evidence=None),lambda d:d.update(analysis=[]),lambda d:d.update(verification=[]),lambda d:d['verification'].pop('limits'),lambda d:d['verification'].update(extra=True),lambda d:d['evidence'].update(extra=True),lambda d:d['evidence'].update(sources={}),lambda d:d['evidence']['sources'].__setitem__(0,None),lambda d:d['evidence']['sources'][0].pop('raw'),lambda d:d['evidence'].update(timeline=None),lambda d:d['evidence'].update(warnings={}),lambda d:d['evidence'].update(counts=[]),lambda d:d['evidence']['sources'][0].update(events=[]),lambda d:d['evidence']['timeline'][0].update(text='Wrong evidence')]
        for i,edit in enumerate(edits):
            with self.subTest(edit=i):
                d=exported();edit(d);self.assert_rehashed_rejected(d)
        for value in (None,0,True,'f'*63,'G'*64):
            d=exported();d['dossier_sha256']=value
            with self.subTest(hash=value):
                with self.assertRaises(ValueError):verify_dossier(d)

if __name__=='__main__':unittest.main(verbosity=2)
