"""ONE NEW61 group:3 methods/6 subcases, targeted F61 findings only."""
import io,json,pathlib,sys,socket,ssl,http.client,os,unittest
from unittest.mock import patch
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import native27_transport60 as t
import native27_readback59 as a
import native27_validator42 as v
CASES=[]

class Reply61:
    def __init__(self,harness,primary=None,cleanup=None):
        self.harness=harness;self.primary=primary;self.cleanup=cleanup;self.status=200;self.body=b'{}';self.closed=0
    def getheaders(self):return []
    def read(self,count):
        if self.primary is not None:self.harness.cleanup_phase=True;raise self.primary
        out=self.body[:count];self.body=self.body[count:]
        if not out:self.harness.cleanup_phase=True
        return out
    def close(self):
        self.closed+=1
        if self.cleanup is not None:raise self.cleanup

class Socket61:
    def __init__(self,harness,wire=None):self.harness=harness;self.wire=wire;self.stream=None;self.timeouts=[];self.setter_errors=[]
    def settimeout(self,timeout):
        self.timeouts.append(timeout)
        if self.harness.fail_setter and self.harness.cleanup_phase:
            error=OSError('PUBLIC_SYNTHETIC_TIMEOUT_'+str(len(self.setter_errors)))
            self.setter_errors.append(error);raise error
    def makefile(self,*args,**kwargs):self.stream=io.BytesIO(self.wire);return self.stream

class Connection61:
    def __init__(self,harness,cap,clock,deadline):
        self.h=harness;self.sock=Socket61(harness,harness.wire);self.timeout=None;self.closed=0
        self.cap,self.clock,self.deadline=cap,clock,deadline
    def connect(self):pass
    def putrequest(self,*args,**kwargs):pass
    def putheader(self,*args,**kwargs):pass
    def endheaders(self):pass
    def getresponse(self):
        if self.h.wire is None:return self.h.reply
        response=http.client.HTTPResponse(t._SocketFileProxy(self.sock,self.cap,self.clock,self.deadline))
        try:response.begin()
        except Exception:
            # Match real HTTPConnection ownership before getresponse returns.
            response.close();raise
        self.h.actual_response=response;return response
    def close(self):self.closed+=1

class Harness61:
    def __init__(self,fail_setter=False,primary=None,cleanup=None,wire=None):
        self.fail_setter=fail_setter;self.cleanup_phase=False;self.wire=wire
        self.state=a.PrivateState();self.clock=lambda:100.0;self.deadline=130.0
        self.connections=[];self.credentials=0;self.actual_response=None
        self.reply=Reply61(self,primary,cleanup)
    def factory(self,host,timeout,cap,clock,deadline):
        c=Connection61(self,cap,clock,deadline);self.connections.append(c);return c
    def credential(self):self.credentials+=1;return 'PUBLIC_SYNTHETIC_PLACEHOLDER'
    def reader(self):
        provider=t.synthetic_provider(self.factory,self.credential,None,self.clock,self.deadline,self.state)
        return a.Reader(provider,self.state,self.clock,self.deadline,None)
    def capture(self):return next(x[1] for x in self.state.originals if x[0]=='TRANSPORT60_ORIGINAL')
    def no_next(self,test,reader):
        count=len(self.connections)
        with test.assertRaises(v.Refuse):reader.call(v.BASE+'/actions/jobs/6110',64)
        test.assertEqual(len(self.connections),count)

class Corrections61(unittest.TestCase):
    def case(self,name):CASES.append(name);return self.subTest(name=name)
    def test_1_timeout_preparation(self):
        for kind in ('setter_failure_no_primary','setter_failure_preserves_primary'):
            with self.case(kind):
                primary=OSError('PUBLIC_SYNTHETIC_PRIMARY') if kind.endswith('preserves_primary') else None
                h=Harness61(True,primary);reader=h.reader()
                with self.assertRaises(v.Refuse):reader.call(v.BASE+'/actions/jobs/6110',64)
                cap=h.capture();connection=h.connections[0]
                self.assertEqual(h.reply.closed,1);self.assertEqual(connection.closed,1)
                self.assertEqual([x[0] for x in cap.cleanup],['response_TIMEOUT_PREP_ERROR','connection_TIMEOUT_PREP_ERROR'])
                self.assertEqual(len(connection.sock.setter_errors),2)
                for item,error in zip(cap.cleanup,connection.sock.setter_errors):self.assertIs(item[1],error)
                self.assertIs(cap.primary,primary)
                self.assertEqual(h.state.validator.first_unknown,'TRANSPORT_IO_ERROR' if primary else 'CLEANUP_ERROR')
                self.assertFalse(any('SYNTHETIC' in str(x) for x in [h.state.validator.first_unknown]))
                h.no_next(self,reader)
    def test_2_response_close_failure(self):
        with self.case('response_close_failure_attempts_connection_close_preserves_primary'):
            primary=OSError('PUBLIC_SYNTHETIC_PRIMARY');cleanup=OSError('PUBLIC_SYNTHETIC_CLOSE')
            h=Harness61(False,primary,cleanup);reader=h.reader()
            with self.assertRaises(v.Refuse):reader.call(v.BASE+'/actions/jobs/6110',64)
            cap=h.capture();self.assertIs(cap.primary,primary);self.assertEqual(cap.primary_code,'TRANSPORT_IO_ERROR')
            self.assertEqual(cap.cleanup[0][0],'response_CLOSE_ERROR');self.assertIs(cap.cleanup[0][1],cleanup)
            self.assertEqual(h.reply.closed,1);self.assertEqual(h.connections[0].closed,1)
            self.assertEqual(h.state.validator.first_unknown,'TRANSPORT_IO_ERROR');h.no_next(self,reader)
    def test_3_original_status_blocks(self):
        for kind in ('interim100_stops_before_later_oversize','malformed_status_original','fresh200_chunkframing_bounded'):
            with self.case(kind):
                prefix=b'HTTP/1.1 100 Continue\r\n'
                if kind.startswith('interim'):wire=prefix+b'\r\nHTTP/1.1 200 OK\r\nX: '+b'x'*(t.HEADER_BYTES+1)+b'\r\n\r\n'
                elif kind.startswith('malformed'):wire=b'HTTP/1.1 invalid\r\n\r\n'
                else:wire=b'HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\nX-Public: new61\r\n\r\n2\r\n{}\r\n0\r\n\r\n'
                h=Harness61(wire=wire);reader=h.reader()
                if kind.startswith('fresh'):
                    raw=reader.call(v.BASE+'/actions/jobs/6110',64);cap=h.capture()
                    self.assertEqual(raw.body,b'{}');self.assertTrue(raw.eof);self.assertIsNone(raw.error)
                    self.assertEqual(cap.status,200);self.assertTrue(cap.wire_headers.endswith(b'\r\n\r\n'))
                    self.assertEqual(bytes(cap.framing_wire),b'2\r\n0\r\n\r\n')
                    self.assertLessEqual(len(cap.wire_headers),t.HEADER_BYTES)
                    self.assertLessEqual(len(cap.framing_wire),t.FRAMING_BYTES)
                    self.assertIsNone(h.state.validator.first_unknown);self.assertTrue(h.actual_response.closed)
                else:
                    with self.assertRaises(v.Refuse):reader.call(v.BASE+'/actions/jobs/6110',64)
                    cap=h.capture()
                    if kind.startswith('interim'):
                        self.assertEqual(bytes(cap.wire_headers),prefix);self.assertEqual(cap.status,100)
                        self.assertEqual(h.state.validator.first_unknown,'UNSUPPORTED_INTERIM_STATUS')
                    else:
                        self.assertEqual(bytes(cap.wire_headers),b'HTTP/1.1 invalid\r\n')
                        self.assertEqual(h.state.validator.first_unknown,'STATUS_LINE_MALFORMED')
                    self.assertEqual(bytes(cap.framing_wire),b'');h.no_next(self,reader)
                self.assertEqual(len(h.connections),1);self.assertEqual(h.connections[0].closed,1)
                self.assertEqual(h.credentials,1);self.assertNotIn('PLACEHOLDER',json.dumps(h.state.public()))

if __name__=='__main__':
    def forbidden(*args,**kwargs):raise AssertionError('NATIVE_NETWORK_TLS_ENV_CREDENTIAL_FORBIDDEN61')
    with patch.object(socket,'socket',forbidden),patch.object(socket,'getaddrinfo',forbidden),patch.object(ssl,'create_default_context',forbidden),patch.object(http.client,'HTTPSConnection',forbidden),patch.object(os,'getenv',forbidden),patch.object(type(os.environ),'__getitem__',forbidden),patch.object(type(os.environ),'get',forbidden):
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Corrections61))
    status='PASS' if result.wasSuccessful() and result.testsRun==3 and len(CASES)==6 else 'FAIL'
    print(json.dumps({'status':status,'classification':'NEW61_TARGETED_FAKE_CONNECTION_ONLY_NOT_NATIVE','methods':result.testsRun,'subcases':len(CASES),'case_names':CASES,'failures':len(result.failures),'errors':len(result.errors),'socket_DNS_HTTP_TLS_env_credential_model_spend_native':0,'PLAN':None,'nativeAdmission':None},sort_keys=True))
    raise SystemExit(0 if status=='PASS' else 1)
