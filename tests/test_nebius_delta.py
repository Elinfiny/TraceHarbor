"""New boundary tests. All provider responses are SIMULATED; zero external calls."""
import copy
from datetime import datetime, timedelta, timezone
import http.client
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch, MagicMock
from core import canonical, digest, import_package
from service import analyze
from live_service import build_record, verify_import
from nebius import decode_response, request_for, https_once, ProviderError, ENDPOINT
import live_probe
from app import make_server

ROOT = Path(__file__).resolve().parents[1]
MODEL = 'nvidia/SIMULATED_TEST_ONLY'
RAW = (ROOT/'fixtures/missing.json').read_bytes()

def response(analysis=None):
    return {'model': MODEL, 'choices': [{'finish_reason': 'stop', 'message': {
        'content': json.dumps(analysis or analyze(RAW)['analysis'])}}],
        'usage': {'prompt_tokens': 100, 'completion_tokens': 100, 'total_tokens': 200}}

def record():
    analysis, p = decode_response(canonical(response()), MODEL)
    p['request_sha256'] = digest(request_for(import_package(RAW), MODEL))
    return build_record(RAW, analysis, p)

def admission():
    _, requests = live_probe.planned_requests(MODEL)
    return {'schema': 'traceharbor.live-admission.v1',
        'operation_id': 'TRACEHARBOR_THREE_SYNTHETIC_REQUESTS_V1', 'model': MODEL,
        'expires_utc': (datetime.now(timezone.utc)+timedelta(minutes=10)).isoformat(),
        'verified_access_evidence': 'SIMULATED_TEST_ONLY',
        'verified_credit_and_cap_evidence': 'SIMULATED_TEST_ONLY',
        'verified_model_license_evidence': 'SIMULATED_TEST_ONLY',
        'verified_token_bounds_evidence': 'SIMULATED_TEST_ONLY',
        'request_sha256': [digest(p) for p in requests], 'input_token_upper_bounds': [3000]*3,
        'input_usd_per_million': '1', 'output_usd_per_million': '1', 'max_cost_usd': '0.02'}

class NewBoundaryTests(unittest.TestCase):
    def test_structured_request_treats_source_as_data(self):
        p = request_for(import_package(RAW), MODEL)
        self.assertEqual(p['response_format'], {'type': 'json_object'})
        self.assertEqual((p['n'], p['max_tokens'], p['stream'], p['store']), (1,1500,False,False))
        self.assertIn('untrusted DATA', p['messages'][0]['content'])

    def test_provider_record_roundtrip(self):
        d = record(); self.assertEqual(verify_import(json.loads(canonical(d))), d)
        self.assertEqual(d['verification']['semantic_reference'], 'NOT_VERIFIED')

    def test_tampered_quote_rejected_even_after_rehash(self):
        d = record(); d['analysis']['hypotheses'][0]['supports'][0]['quote'] += ' invented'
        d['dossier_sha256'] = digest({k:v for k,v in d.items() if k != 'dossier_sha256'})
        with self.assertRaises(ValueError): verify_import(d)

    def test_causation_claim_and_missing_uncertainty_rejected(self):
        for alteration in ('status', 'missing'):
            d = record()
            if alteration == 'status': d['analysis']['status'] = 'supported_reference'
            else: d['analysis']['missing_evidence'] = []
            with self.assertRaises(ValueError): build_record(RAW, d['analysis'], d['provider'])

    def test_truncation_refusal_tools_and_empty_rejected(self):
        variants = []
        d=response(); d['choices'][0]['finish_reason']='length'; variants.append(d)
        d=response(); d['choices'][0]['message']['refusal']='No'; variants.append(d)
        d=response(); d['choices'][0]['message']['tool_calls']=[{}]; variants.append(d)
        d=response(); d['choices'][0]['message']['content']=''; variants.append(d)
        d=response(); d['choices'][0]['message']['content']='{"bad":'; variants.append(d)
        for d in variants:
            with self.subTest(d=d), self.assertRaises(ProviderError): decode_response(canonical(d),MODEL)

    def test_model_and_usage_mismatch_rejected(self):
        for key in ('model','usage'):
            d=response()
            if key=='model': d['model']='nvidia/different'
            else: d['usage']['total_tokens']=True
            with self.assertRaises(ProviderError): decode_response(canonical(d),MODEL)

    def test_transport_no_redirect_no_retry_no_body_logging(self):
        connection=MagicMock(); connection.getresponse.return_value.status=302
        with patch('nebius.http.client.HTTPSConnection', return_value=connection), patch.dict('os.environ',{'NEBIUS_API_KEY':'synthetic-test-value'}):
            with self.assertRaisesRegex(ProviderError,'PROVIDER_HTTP_302'): https_once({})
        connection.request.assert_called_once(); connection.getresponse.return_value.read.assert_not_called()
        connection.close.assert_called_once()

    def test_transport_unknown_no_retry(self):
        connection=MagicMock(); connection.request.side_effect=TimeoutError('private message')
        with patch('nebius.http.client.HTTPSConnection', return_value=connection), patch.dict('os.environ',{'NEBIUS_API_KEY':'synthetic-test-value'}):
            with self.assertRaisesRegex(ProviderError,'^TRANSPORT_OUTCOME_UNKNOWN_NO_RETRY$'): https_once({})
        connection.request.assert_called_once()

    def test_admission_hash_expiry_cap_and_evidence(self):
        _,req=live_probe.planned_requests(MODEL)
        for field,value in [('request_sha256',[]),('expires_utc','2020-01-01T00:00:00Z'),('max_cost_usd','0.0001'),('verified_credit_and_cap_evidence',''),('input_token_upper_bounds',[3001]*3)]:
            p=admission();p[field]=value
            with self.subTest(field=field), self.assertRaises(ValueError):live_probe.admit(p,req)

    def test_three_distinct_attempts_and_spent_blocks_replay(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);p=root/'admission.json';p.write_bytes(canonical(admission()))
            def fake(req):
                evidence=json.loads(req['messages'][1]['content'])
                source=next(raw for raw in live_probe.planned_requests(MODEL)[0]
                    if json.loads(raw)['case_id']==evidence['case_id'])
                a=analyze(source)['analysis']
                if a['status']=='supported_reference':
                    a['status']='uncertain';a['missing_evidence']=['Independent causal verification.']
                    for h in a['hypotheses']:
                        if h['assessment']=='supported_reference':h['assessment']='uncertain'
                return canonical(response(a))
            with patch.dict('os.environ',{'NEBIUS_API_KEY':'synthetic-test-value','NEBIUS_MODEL':MODEL}),patch('live_probe.https_once',side_effect=fake) as send:
                self.assertEqual(live_probe.execute(p,root/'run'),0)
                self.assertEqual(send.call_count,3)
                with self.assertRaises(FileExistsError):live_probe.execute(p,root/'second')
                self.assertEqual(send.call_count,3)
            self.assertEqual(len(list((root/'run').glob('*-attempt.json'))),3)

    def test_unknown_terminal_no_automatic_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);p=root/'admission.json';p.write_bytes(canonical(admission()))
            with patch.dict('os.environ',{'NEBIUS_API_KEY':'synthetic-test-value','NEBIUS_MODEL':MODEL}),patch('live_probe.https_once',side_effect=ProviderError('TRANSPORT_OUTCOME_UNKNOWN_NO_RETRY')) as send:
                self.assertEqual(live_probe.execute(p,root/'run'),2);self.assertEqual(send.call_count,3)
            self.assertFalse(json.loads((root/'run/result.json').read_text())['completed_three'])

    def test_new_http_verify_route_and_host_guard(self):
        server=make_server();worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
        try:
            for body,expected in ((canonical(record()),200),(b'{"schema":"forged"}',400)):
                c=http.client.HTTPConnection('127.0.0.1',server.server_port)
                c.request('POST','/verify',body,{'Content-Type':'application/json'});r=c.getresponse()
                self.assertEqual(r.status,expected);r.read();c.close()
            c=http.client.HTTPConnection('127.0.0.1',server.server_port)
            c.request('POST','/verify',canonical(record()),{'Content-Type':'application/json','Origin':'https://untrusted.example'})
            r=c.getresponse();self.assertEqual(r.status,403);r.read();c.close()
        finally:server.shutdown();server.server_close();worker.join()

if __name__=='__main__':unittest.main()
