"""Affected binding and safe-failure cases only. Synthetic transport; no network."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
from importlib.machinery import SourceFileLoader
import io
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
def load(name, path):
    spec = importlib.util.spec_from_loader(name, SourceFileLoader(name, str(path)))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
subject = load('subject200', ROOT/'tools/app_runtime190.py')
provider = load('provider200', ROOT/'nebius.py')
from live_service import build_record, verify_record

class Response:
    def __init__(self, raw, status): self.raw, self.status = raw, status
    def getheader(self, name):
        return 'application/json' if name == 'Content-Type' else str(len(self.raw))
    def read(self, maximum): return self.raw[:maximum]
class Connection:
    def __init__(self, response, timeout=False):
        self.response, self.timeout_post = response, timeout
        self.timeout, self.sock, self.posts, self.closes = 0, None, [], 0
    def request(self, method, path, raw, headers):
        self.posts.append((method, path, raw))
        if self.timeout_post: raise TimeoutError()
    def getresponse(self): return self.response
    def close(self): self.closes += 1

class Binding200(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = (ROOT/'offline103/request.json').read_bytes()
        cls.package = subject.input_for_request(cls.raw)
        cls.wrong = (ROOT/'fixtures/complete.json').read_bytes()
        source = json.loads(cls.raw)['messages'][1]['content']
        source = json.loads(source)['sources'][0]
        cls.analysis = {'status':'uncertain', 'summary':'Only a synthetic observation is available.',
          'hypotheses':[{'id':'h200','label':'Unresolved observation','assessment':'uncertain',
            'supports':[{'source_id':source['id'],'event_id':source['events'][0]['id'],
              'source_sha256':source['sha256'],'quote':source['events'][0]['text']}],
            'contradicts':[]}], 'missing_evidence':['Independent configuration history.'], 'remediation':[]}
    def invoke(self, *, analysis=None, status=200, model=None, prompt=123, completion=11,
               timeout=False, key='synthetic-only', package=None, body=None):
        envelope={'model':model or subject.MODEL,
          'choices':[{'finish_reason':'stop','message':{'content':json.dumps(analysis or self.analysis)}}],
          'usage':{'prompt_tokens':prompt,'completion_tokens':completion,'total_tokens':prompt+completion}}
        raw=body if body is not None else json.dumps(envelope).encode()
        connection=Connection(Response(raw,status),timeout)
        calls=[]
        def factory(host,timeout):
            calls.append(host)
            return connection
        out=subject.execute(self.raw, self.package if package is None else package,
                            provider,build_record,key,{'scope':'SYNTHETIC_ONLY'},factory=factory)
        self.assertLessEqual(len(connection.posts),1)
        self.assertLessEqual(len(calls),1)
        self.assertEqual(connection.closes,1)
        return out,connection,raw
    def test_matching_actual_request_sources_make_verified_record(self):
        out,c,_=self.invoke()
        self.assertEqual(out['outcome'],'KNOWN_TERMINAL_PRODUCT_RECORD_VERIFIED')
        self.assertEqual(out['provider_record']['baseline_dossier']['evidence']['case_id'],
                         'contest82-unknown-20261017-c0a2f7')
        self.assertTrue(verify_record(out['provider_record']))
        self.assertEqual(c.posts[0][2],self.raw)
    def test_wrong_input_refused_before_transport(self):
        calls=[]
        with self.assertRaisesRegex(subject.Refusal,'^INPUT_BINDING_MISMATCH$'):
            subject.execute(self.raw,self.wrong,provider,build_record,'synthetic-only',{},
                            factory=lambda *a,**k:calls.append(1))
        self.assertEqual(calls,[])
    def test_main_wrong_input_refused_before_secret(self):
        original=subject.os.environ.get
        seen=[]
        def get(k,*a):
            if k=='NEBIUS_API_KEY': seen.append(k); raise AssertionError('Secret read before binding')
            return original(k,*a)
        def read(path):
            return self.raw if path.name=='request.json' else b'{}'
        with patch.object(subject.Path,'read_bytes',read), \
             patch.object(subject,'input_for_request',return_value=self.wrong), \
             patch.object(subject.os.environ,'get',side_effect=get), \
             patch.dict(sys.modules,{'nebius':provider}), patch('sys.stdout',new_callable=io.StringIO) as out:
            self.assertEqual(subject.main(),1)
        self.assertEqual(seen,[])
        self.assertIn('PRE_SECRET',out.getvalue())
    def test_invalid_product_preserves_validated_diagnostics(self):
        bad=json.loads(json.dumps(self.analysis));bad['status']='supported_reference'
        out,_,raw=self.invoke(analysis=bad)
        self.assertEqual(out['failure_code'],'PRODUCT_VERIFICATION_REJECTED')
        self.assertEqual(out['verification_stage'],'PRODUCT_RECORD')
        self.assertEqual(out['model_reported'],subject.MODEL)
        self.assertEqual(out['usage'],{'prompt_tokens':123,'completion_tokens':11,'total_tokens':134})
        self.assertEqual(out['raw_response_sha256'],hashlib.sha256(raw).hexdigest())
        self.assertEqual(out['billed_cost_USD'],'UNKNOWN_NOT_PROVIDER_RECONCILED')
        self.assertNotIn('provider_record',out)
        self.assertNotIn('summary',out)
    def test_altered_citation_rejected(self):
        bad=json.loads(json.dumps(self.analysis));bad['hypotheses'][0]['supports'][0]['quote']+=' changed'
        out,_,_=self.invoke(analysis=bad)
        self.assertEqual(out['failure_code'],'PRODUCT_VERIFICATION_REJECTED')
        self.assertNotIn('provider_record',out)
    def test_timeout_unknown_consumed_no_retry(self):
        out,c,_=self.invoke(timeout=True)
        self.assertEqual(out['outcome'],'UNKNOWN_CONSUMED_NO_RETRY')
        self.assertEqual(len(c.posts),1)
        self.assertNotIn('usage',out)
    def test_wrong_model_has_no_unvalidated_usage(self):
        out,_,_=self.invoke(model='nvidia/different')
        self.assertEqual(out['failure_code'],'PROVIDER_MODEL_MISMATCH')
        self.assertNotIn('usage',out)
    def test_output_limit_has_no_unvalidated_usage(self):
        out,_,_=self.invoke(completion=1501)
        self.assertEqual(out['failure_code'],'PROVIDER_TOKEN_BOUND_EXCEEDED')
        self.assertNotIn('usage',out)
    def test_input_limit_rejected_before_metadata_disclosure(self):
        out,_,_=self.invoke(prompt=2000001)
        self.assertEqual(out['failure_code'],'ACTUAL_USAGE_EXCEEDS_ADMITTED_BOUND')
        self.assertNotIn('usage',out)
    def test_http_refusal_consumes_one_request(self):
        out,_,raw=self.invoke(status=403)
        self.assertEqual(out['failure_code'],'PROVIDER_HTTP_403')
        self.assertEqual(out['raw_response_sha256'],hashlib.sha256(raw).hexdigest())
        self.assertNotIn('usage',out)
    def test_parse_failure_does_not_invent_usage(self):
        out,_,_=self.invoke(body=b'not-json')
        self.assertEqual(out['failure_code'],'PROVIDER_INVALID_JSON_OR_STRUCTURE')
        self.assertNotIn('usage',out)
    def test_no_secret_refused_before_factory(self):
        calls=[]
        with self.assertRaisesRegex(subject.Refusal,'^CREDENTIAL_REFERENCE_UNAVAILABLE$'):
            subject.execute(self.raw,self.package,provider,build_record,'',{},
                            factory=lambda *a,**k:calls.append(1))
        self.assertEqual(calls,[])
    def test_arbitrary_exception_text_never_logged(self):
        def bad(*a): raise RuntimeError('sensitive arbitrary failure detail')
        out=subject.execute(self.raw,self.package,provider,bad,'synthetic-only',{},
                            factory=lambda *a,**k:Connection(Response(json.dumps({
                              'model':subject.MODEL,'choices':[{'finish_reason':'stop','message':{'content':json.dumps(self.analysis)}}],
                              'usage':{'prompt_tokens':123,'completion_tokens':11,'total_tokens':134}}).encode(),200)))
        self.assertEqual(out['failure_code'],'APPLICATION_FAILURE')
        self.assertNotIn('sensitive arbitrary',json.dumps(out))
