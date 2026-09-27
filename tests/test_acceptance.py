import copy
import hashlib
import http.client
import json
from pathlib import Path
import sys
import threading
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from core import InputError, MAX_BYTES, canonical, digest, import_package
from adapters import DemoAdapter, NebiusAdapter, LiveAdapterDisabled
from service import analyze, verify_dossier
from verifier import VerificationError, verify_analysis, verify_semantics
from app import make_server

def raw(name='complete'): return (ROOT/'fixtures'/f'{name}.json').read_bytes()
def obj(name='complete'): return json.loads(raw(name))

class Acceptance(unittest.TestCase):
    def test_three_semantic_reference_cases(self):
        expected = {'complete':'supported_reference','missing':'uncertain','contradictory':'conflicted'}
        for name, status in expected.items():
            with self.subTest(name=name):
                d = analyze(raw(name)); a = d['analysis']
                self.assertEqual(a['status'], status)
                self.assertEqual(d['verification']['semantic_reference'], 'PASS_KNOWN_REFERENCE_ONLY')
                self.assertEqual(a['hypotheses'][0]['id'], 'deadline-regression')
                self.assertTrue(verify_dossier(d))
        self.assertIn('runtime task_deadline_ms', analyze(raw('missing'))['analysis']['missing_evidence'][0])
        contrary = analyze(raw('contradictory'))['analysis']['hypotheses'][0]['contradicts']
        self.assertEqual([(x['source_id'],x['event_id']) for x in contrary],[('audit','a1')])

    def test_quote_correctness_is_not_semantic_proof(self):
        d = analyze(raw()); a = copy.deepcopy(d['analysis'])
        a['hypotheses'][0]['label'] = 'Disk hardware failure'
        self.assertEqual(verify_analysis(a,d['evidence']),'PASS')
        with self.assertRaises(VerificationError): verify_semantics(a,'complete')
        a=copy.deepcopy(analyze(raw('missing'))['analysis']);a['status']='supported_reference'
        with self.assertRaises(VerificationError): verify_semantics(a,'missing')

    def test_fabricated_quote_id_hash_and_malformed_response(self):
        d=analyze(raw())
        for field,value in [('quote','Invented quote.'),('source_id','nonexistent'),('event_id','nonexistent'),('source_sha256','0'*64)]:
            with self.subTest(field=field):
                a=copy.deepcopy(d['analysis']);a['hypotheses'][0]['supports'][0][field]=value
                with self.assertRaises(VerificationError):verify_analysis(a,d['evidence'])
        for bad in [None,[],{}, {'status':'uncertain'}, 'truncated response']:
            with self.subTest(bad=bad):
                with self.assertRaises(VerificationError): verify_analysis(bad,d['evidence'])

    def test_duplicate_events_do_not_double_analysis(self):
        data=obj();extra=copy.deepcopy(data['sources'][1]['events'][0]);extra['id']='m2';data['sources'][1]['events'].append(extra)
        d=analyze(canonical(data));base=analyze(raw())
        self.assertEqual(d['evidence']['counts'], {'input_events':6,'unique_events':5,'duplicates':1})
        self.assertEqual(d['evidence']['analysis_fingerprint'],base['evidence']['analysis_fingerprint'])
        self.assertEqual(d['analysis']['status'],base['analysis']['status'])
        self.assertEqual(len(d['analysis']['hypotheses'][0]['supports']),3)
        self.assertNotEqual(d['evidence']['sources'][1]['sha256'],base['evidence']['sources'][1]['sha256'])
        self.assertTrue(verify_dossier(d))

    def test_timestamp_normalization_missing_and_conflict(self):
        ev=import_package(raw('contradictory'))
        metric=next(s for s in ev['sources'] if s['id']=='metrics')['events'][0]
        self.assertEqual(metric['timestamp'],'2030-01-15T12:00:10Z')
        conflict=next(s for s in ev['sources'] if s['id']=='audit')['events'][1]
        self.assertIsNone(conflict['timestamp']);self.assertEqual(len(conflict['timestamp_candidates']),2)
        self.assertEqual(conflict['timestamp_state'],'conflict')
        self.assertIn('TIMESTAMP_MISSING',{w['code'] for w in ev['warnings']})
        self.assertIn('TIMESTAMP_CONFLICT',{w['code'] for w in ev['warnings']})
        data=obj();data['sources'][0]['events'][0]['timestamp']=None;data['sources'][0]['events'][0]['timestamp_alt']='2030-01-15T12:00:00Z'
        self.assertIsNone(import_package(canonical(data))['sources'][0]['events'][0]['timestamp'])

    def test_hostile_log_remains_data_no_actions(self):
        d=analyze(raw('contradictory'))
        self.assertEqual(d['analysis']['status'],'conflicted')
        self.assertEqual(d['remediation_execution'],'NOT_SUPPORTED')
        self.assertEqual(d['live_api'],'NOT_ACTIVATED')
        self.assertTrue(any('<img' in e['text'] for e in d['evidence']['timeline']))
        self.assertNotIn('hostile', {c['source_id'] for h in d['analysis']['hypotheses'] for side in ('supports','contradicts') for c in h[side]})
        with self.assertRaises(LiveAdapterDisabled): NebiusAdapter().analyze(d['evidence'])

    def test_unknown_case_and_spoofed_case_label_abstain(self):
        data=obj();data['sources'][0]['events'][0]['text']='A different deployment event.'
        d=analyze(canonical(data))
        self.assertEqual(d['analysis']['status'],'unknown');self.assertEqual(d['analysis']['hypotheses'],[])
        self.assertEqual(d['analysis']['remediation'],[])
        self.assertEqual(d['verification']['semantic_reference'],'NOT_EVALUATED_UNKNOWN_CASE')
        data=obj();data['sources'][0]['events'][0]['id']='renamed'
        self.assertEqual(analyze(canonical(data))['analysis']['status'],'unknown')

    def test_invalid_and_oversized_import_rejected(self):
        invalid=[b'',b'{',b'[]',b'{"x":1,"x":2}',b'{"x":NaN}',b' '* (MAX_BYTES+1),b'\xff']
        for payload in invalid:
            with self.subTest(bytes=len(payload)):
                with self.assertRaises(InputError):import_package(payload)
        edits=[lambda d:d.update(synthetic=False),lambda d:d.update(extra='unsupported'),lambda d:d['sources'][0].update(kind=[]),lambda d:d['sources'][0]['events'][0].update(timestamp='2030-01-15T12:00:00'),lambda d:d['sources'].append(copy.deepcopy(d['sources'][0])),lambda d:d['sources'][0]['events'][0].update(text='api_key='+('synthetic'+'x'*24))]
        for edit in edits:
            data=obj();edit(data)
            with self.subTest(edit=str(edit)):
                with self.assertRaises(InputError): import_package(canonical(data))

    def test_export_hashes_and_links_and_tamper(self):
        d=json.loads(json.dumps(analyze(raw())))
        self.assertEqual(d['evidence']['input_sha256'],hashlib.sha256(raw()).hexdigest())
        self.assertTrue(verify_dossier(d))
        for s in d['evidence']['sources']:self.assertEqual(s['sha256'],digest(s['raw']))
        d['evidence']['timeline'][0]['text']='Modified evidence'
        with self.assertRaises(ValueError):verify_dossier(d)
        d['dossier_sha256']=digest({k:v for k,v in d.items() if k!='dossier_sha256'})
        with self.assertRaises(ValueError):verify_dossier(d)

    def test_loopback_interface_smoke_and_guards(self):
        server=make_server(0);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            port=server.server_port
            def request(method,path,body=None,headers=None):
                conn=http.client.HTTPConnection('127.0.0.1',port,timeout=5)
                try:
                    conn.request(method,path,body=body,headers=headers or {});r=conn.getresponse();return r.status,dict(r.getheaders()),r.read()
                finally:conn.close()
            for path,needle in [('/',b'DEMONSTRATION'),('/app.js',b'textContent'),('/style.css',b'@media'),('/fixtures/complete.json',b'traceharbor.input.v1')]:
                status,headers,body=request('GET',path);self.assertEqual(status,200);self.assertIn(needle,body);self.assertIn("script-src 'self'",headers['Content-Security-Policy'])
            status,_,body=request('POST','/analyze',raw('contradictory'),{'Content-Type':'application/json'})
            self.assertEqual(status,200);self.assertEqual(json.loads(body)['analysis']['status'],'conflicted')
            self.assertEqual(request('POST','/analyze',b'{',{'Content-Type':'application/json'})[0],400)
            self.assertEqual(request('GET','/',headers={'Host':'foreign.invalid'})[0],403)
            self.assertEqual(request('POST','/analyze',raw(),{'Content-Type':'application/json','Origin':'https://foreign.invalid'})[0],403)
            self.assertEqual(request('GET','/../core.py')[0],404)
        finally:
            server.shutdown();server.server_close();thread.join(timeout=3)
        self.assertFalse(thread.is_alive())

if __name__=='__main__':unittest.main(verbosity=2)
