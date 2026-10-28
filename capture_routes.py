"""Routes on the SAME future server; no listener, auth enrollment or capture on import.
No route is admitted without a separately reviewed capture pin, trusted server
identity verifier and finite sink. Public judging access never grants admin capture.
"""
import json,hashlib
from pathlib import Path
from release_policy import Refusal
CAPTURE_RELEASE_SHA256=None
class CaptureRoutes:
    def __init__(self,*,pin=None,authorize=None,sink=None):self.pin=pin;self.authorize=authorize;self.sink=sink
    def enabled(self):return CAPTURE_RELEASE_SHA256 is not None and self.pin==CAPTURE_RELEASE_SHA256 and callable(self.authorize) and self.sink is not None
    def route(self,h):
        if not h.path.startswith('/private-capture/'):return False
        host=h.headers.get_all('Host',[]);origin=h.headers.get_all('Origin',[])
        expected=getattr(h.server,'edge_policy',None)
        expected_host=expected.host if expected else f'127.0.0.1:{h.server.server_port}'
        expected_origin='https://'+expected_host if expected else 'http://'+expected_host
        if not self.enabled() or not h.allowed() or host!=[expected_host] or (h.command=='POST' and origin!=[expected_origin]) or not self.authorize(h):h.error(403,'Private capture is not admitted.');return True
        if h.command=='GET' and h.path=='/private-capture/admission':h.respond(200,json.dumps({'capture':True,'classification':'SYNTHETIC_ONLY','secureContext':True}).encode());return True
        if h.command=='GET' and h.path in {'/private-capture/controller.js','/private-capture/'}:
            name='capture_controller.js' if h.path.endswith('.js') else 'capture.html';kind='text/javascript; charset=utf-8' if name.endswith('.js') else 'text/html; charset=utf-8';h.respond(200,(Path(__file__).parent/'web'/name).read_bytes(),kind);return True
        try:
            lengths=h.headers.get_all('Content-Length',[])
            if h.command!='POST' or len(lengths)!=1 or h.headers.get_all('Transfer-Encoding',[]):raise Refusal('CAPTURE_HEADERS')
            length=int(lengths[0])
            if not 1<=length<=1048576:raise Refusal('CAPTURE_CHUNK_BOUND')
            h.connection.settimeout(5);body=h.rfile.read(length)
            if len(body)!=length:raise Refusal('CAPTURE_TRUNCATED')
            if h.path=='/private-capture/chunk':
                if h.headers.get('Content-Type')!='application/octet-stream' or len(h.headers.get_all('X-Chunk-Sequence',[]))!=1 or len(h.headers.get_all('X-Chunk-SHA256',[]))!=1:raise Refusal('CAPTURE_HEADERS')
                value=self.sink.append(int(h.headers['X-Chunk-Sequence']),body,h.headers['X-Chunk-SHA256'])
            elif h.path=='/private-capture/finish':
                if length>1024 or h.headers.get('Content-Type')!='application/json':raise Refusal('CAPTURE_FINISH_BOUND')
                x=json.loads(body)
                if type(x)is not dict or set(x)!={'elapsed','reason','custody'}:raise Refusal('CAPTURE_FINISH_SHAPE')
                value=self.sink.finish(x['elapsed'],x['reason'],x['custody'])
            else:raise Refusal('CAPTURE_ROUTE')
            h.respond(200,json.dumps(value).encode())
        except Exception:h.error(400,'Private capture refused; no automatic retry.')
        return True
