"""Recovery86, source-only until admitted native launch. Import performs no I/O.
Original capture84 and operator files are never written. Only the already approved
E2E marker and allocation in ORIGINAL are used by the existing captured worker.
"""
import hashlib,hmac,io,json,math,os,re,stat,subprocess,sys,threading,time,shutil
from pathlib import Path
from http.cookies import SimpleCookie
from urllib.parse import parse_qs
import credit_runtime67 as r
import credit_scope67 as scope
from quota_ledger import read,exclusive,private_dir,Ledger
from release_policy import canonical,digest,Refusal
POLICY_SHA256='5a5b6f318e1b7e5049c1e9b75c402b11f63c0f7f17f65553f9096fb9928bc354'
COOKIE='__Host-traceharbor-recovery96'
PHASES=('vp8','vp9','select','native','full')
NAMES={'TypeError','ReferenceError','EncodingError','NotSupportedError','NotReadableError','InvalidStateError','SecurityError','AbortError','UnknownError','OverconstrainedError','TimeoutError','NotAllowedError','NotFoundError'}

def policy():return scope.contract()

def regular(p):
    s=p.lstat()
    if not stat.S_ISREG(s.st_mode) or s.st_uid!=os.getuid() or s.st_mode&0o077:raise Refusal('PRIVATE_REGULAR_FILE')
    return s

def binary_once(p,data):
    fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'wb')as f:f.write(data);f.flush();os.fsync(f.fileno())
    fd=os.open(p.parent,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)

def witness(original):
    return digest({'selected':read(original/'capture-started.json'),'terminal':read(original/'capture/terminal.json'),'custody':read(original/'capture/custody.json')})

class Operator:
    def __init__(self,path,ttl,clock=time.time,*,scope_id='CREDIT67_ONLY'):self.path=path;self.ttl=ttl;self.clock=clock;self.lock=threading.Lock();self.scope_id=scope_id
    def consume(self,raw):
        if not isinstance(raw,bytes)or not re.fullmatch(rb'[a-f0-9]{64}',raw):raise Refusal('GRANT_SHAPE')
        with self.lock:
            g=read(self.path/'grant.json')
            if g['scope']!=self.scope_id or self.clock()>=g['expires'] or not hmac.compare_digest(hashlib.sha256(raw).hexdigest(),g['sha256']):raise Refusal('GRANT_REFUSED')
            exclusive(self.path/'grant-consumed.json',{'scope':self.scope_id,'retry':False})
            token=os.urandom(32).hex();exclusive(self.path/'session.json',{'sha256':hashlib.sha256(token.encode()).hexdigest(),'scope':self.scope_id,'expires':min(g['expires'],self.clock()+self.ttl)})
            return token
    def authorize(self,h):
        try:
            if len(h.headers.get_all('Cookie',[]))!=1:return False
            header=h.headers['Cookie']
            if sum(x.split('=',1)[0].strip()==COOKIE for x in header.split(';'))!=1:return False
            c=SimpleCookie();c.load(header);v=c[COOKIE].value;s=read(self.path/'session.json')
            return len(v)==64 and s['scope']==self.scope_id and self.clock()<s['expires'] and hmac.compare_digest(hashlib.sha256(v.encode()).hexdigest(),s['sha256'])
        except Exception:return False
    def remaining(self):
        try:return max(0,read(self.path/'session.json')['expires']-self.clock())
        except Exception:return 0

class Sink:
    def __init__(self,path,phase,maximum,clock=time.time):
        self.path=path;self.phase=phase;self.maximum=maximum;self.clock=clock;self.started=clock();self.bytes=0;self.next=0;self.terminal=False;self.lock=threading.Lock()
    def append(self,sequence,data,sha):
        with self.lock:
            if self.terminal or type(sequence)is not int or sequence!=self.next or sequence>=700 or not data or len(data)>1048576 or self.bytes+len(data)>self.maximum or hashlib.sha256(data).hexdigest()!=sha:raise Refusal('CUSTODY_BOUND')
            binary_once(self.path/f'chunk-{sequence:05d}.webm',data)
            exclusive(self.path/f'chunk-{sequence:05d}.json',{'sequence':sequence,'bytes':len(data),'sha256':sha})
            self.next+=1;self.bytes+=len(data);return {'sequence':sequence,'bytes':len(data),'sha256':sha}
    def close(self,value):
        with self.lock:
            if self.terminal:raise Refusal('PHASE_ALREADY_TERMINAL')
            self.terminal=True;exclusive(self.path/'terminal.json',value);return value

class Recovery:
    def __init__(self,root,original,config,p,*,clock=time.time,probe=None):
        self.root=Path(root);self.original=Path(original);self.config=config;self.p=p;self.clock=clock;self.probe=probe or bounded_probe;self.lock=threading.Lock();self.sinks={};self.call=None;self.selection_timer_factory146=threading.Timer;self.selection_timer146=None
        self.assert_original()
        from recovery_auth93 import EPOCH,operator_path
        authpath=operator_path(self)
        if(self.root/'continuity105/release-complete.json').exists():
            import continuity105
            authpath=continuity105.operator_path(self)
        self.operator=Operator(authpath,min(p['session_seconds'],1800),clock,scope_id=EPOCH)
    def assert_original(self):return scope.assert_parent(self)
    def initialize(self):return scope.initialize(self)
    def phase_dir(self,phase):
        if phase not in ('select','native','full'):raise Refusal('CLOSED_OLD_PHASE')
        return self.root/phase
    def prepare106(self):raise Refusal('OLD_DIAGNOSTICS_CLOSED')
    def issue_grant_once(self):raise Refusal('ORIGINAL86_GRANT_CLOSED_NOT_REISSUED')
    def prepare113(self):raise Refusal('OLD_SCOPE_CLOSED')
    def issue_grant106_once(self):raise Refusal('SCOPE106_CLOSED_NO_REISSUE')
    def issue_grant113_once(self):raise Refusal('ORIGINAL113_GRANT_CLOSED_NO_REISSUE')
    def issue_grant67_once(self):raise Refusal('CONSUMED_OPERATOR67_GRANT_CLOSED')
    def issue_grant93_once(self):
        import recovery_auth93
        return recovery_auth93.grant(self)
    def state(self,phase):
        if phase=='select':return scope.selection_status(self)
        if phase not in('native','full'):raise Refusal('PHASE')
        d=self.root/phase
        for n in('failure.json','qualified.json','terminal.json'):
            if(d/n).exists():return read(d/n)
        return {'state':'UNKNOWN_CONSUMED_NO_RETRY'if(d/'reserved.json').exists()else'NOT_STARTED','retry':False}
    def codec(self):return scope.codec(self)
    def reserve(self,phase,codec):return scope.reserve(self,phase,codec)
    def append(self,phase,seq,data,sha):
        self.assert_original()
        if phase not in self.sinks:raise Refusal('NO_LIVE_PHASE_AFTER_RESTART')
        return self.sinks[phase].append(seq,data,sha)
    def assemble(self,phase,name='media.webm'):
        sink=self.sinks[phase];p=sink.path/name
        fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        with os.fdopen(fd,'wb')as f:
            for i in range(sink.next):
                part=sink.path/f'chunk-{i:05d}.webm';regular(part);raw=part.read_bytes();receipt=read(sink.path/f'chunk-{i:05d}.json')
                if len(raw)!=receipt['bytes']or hashlib.sha256(raw).hexdigest()!=receipt['sha256']:raise Refusal('CHUNK_DRIFT')
                f.write(raw)
            f.flush();os.fsync(f.fileno())
        return p
    def finish(self,phase,value):
        self.assert_original()
        if phase not in self.sinks:raise Refusal('NO_LIVE_PHASE')
        s=self.sinks[phase];elapsed=value.get('elapsed');reason=value.get('reason')
        if type(elapsed)not in(int,float)or not math.isfinite(elapsed)or not 0<=elapsed<=240:raise Refusal('ELAPSED')
        if phase=='full':
            custody=value.get('custody',{});keys={'received_bytes','reserved_bytes','acked_bytes','reserved_chunks','acked_chunks','pending_bytes','pending_chunks','dropped_bytes','failure'}
            complete=(set(custody)==keys and type(custody['failure'])is bool and all(type(v)is int and v>=0 for k,v in custody.items()if k!='failure') and reason=='STOP224' and 224<=elapsed<=230 and not custody['failure'] and custody['pending_bytes']==custody['pending_chunks']==custody['dropped_bytes']==0 and custody['received_bytes']==custody['reserved_bytes']==custody['acked_bytes']==s.bytes and custody['acked_chunks']==custody['reserved_chunks']==s.next and s.next>0)
            return s.close({'schema':'traceharbor.recovery86.full-terminal.v1','state':'CAPTURED_NOT_AV_VERIFIED'if complete else'PARTIAL_NO_RETRY','bytes':s.bytes,'chunks':s.next,'elapsed':elapsed,'reason':reason if complete else'ERROR','custody':custody,'retry':False,'public':False})
        if phase not in('vp8','vp9','native')or reason!='DIAGNOSTIC_DONE'or value.get('client_decoded')is not True or not 1.8<=elapsed<=6 or not s.bytes:raise Refusal('DIAGNOSTIC_NOT_COMPLETE')
        s.close({'state':'ENCODED_NOT_QUALIFIED','bytes':s.bytes,'chunks':s.next,'elapsed':elapsed,'retry':False})
        exclusive(s.path/'probe-reserved.json',{'state':'UNKNOWN_NO_RETRY'})
        path=self.assemble(phase);codec=read(s.path/'reserved.json')['codec'];result=self.probe(path,codec,self.p)
        verdict={'state':'PASS'if result.get('pass')is True else'FAIL_NO_RETRY','phase':phase,'codec':codec,'bytes':s.bytes,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'probe':result,'retry':False}
        exclusive(s.path/'qualified.json',verdict);return verdict
    def fail(self,phase,name,where):
        self.assert_original()
        if phase=='select':return scope.fail_selection(self,name,where)
        if phase not in PHASES:raise Refusal('PHASE')
        if not(self.phase_dir(phase)/'reserved.json').exists():raise Refusal('UNRESERVED_FAILURE')
        safe={'state':'FAILED_NO_RETRY','phase':phase,'error_name':name if name in NAMES else'UnclassifiedError','where':where if where in {'SELECT','CONSTRUCT','START','RECORDER_EVENT','DECODE','UPLOAD','PROBE','TIMEOUT','TRACK_ENDED','FLOW'}else'FLOW','retry':False}
        if (self.phase_dir(phase)/'failure.json').exists():return read(self.phase_dir(phase)/'failure.json')
        exclusive(self.phase_dir(phase)/'failure.json',safe)
        if phase in self.sinks and not self.sinks[phase].terminal:self.sinks[phase].close(safe)
        return safe
    def active_target(self):return self.root/'target.json'
    def arm113(self,client_id):raise Refusal('ORIGINAL113_TARGET_CLOSED')
    def arm67(self,client_id):return scope.arm(self,client_id)
    def arm(self,client_id):raise Refusal('OLD_ARM_CLOSED')
    def begin(self,client_id):return scope.begin(self,client_id)
    def mark(self,name,elapsed):
        if name not in {'runtime-rendered','runtime-failed','story-start','supported','citation','conflicted','exported','reimported','historical','story-end','flow-failed'}or type(elapsed)not in(int,float)or not math.isfinite(elapsed)or not 0<=elapsed<=230:raise Refusal('FLOW_MARK')
        exclusive(self.root/('mark-'+name+'.json'),{'name':name,'elapsed':elapsed});return {'marked':True}
    def preview(self):
        if self.state('native').get('state')!='PASS':raise Refusal('NATIVE_NOT_QUALIFIED')
        exclusive(self.root/'preview-ready.json',{'native_sha256':self.state('native')['sha256'],'browser_decoded':True});return {'ready':True}
    def ready(self):
        s=self.sinks.get('full');return bool(self.state('native').get('state')=='PASS' and self.state('full').get('state')!='FAILED_NO_RETRY' and s and not s.terminal and s.bytes>0 and (self.root/'full/reserved.json').exists() and (self.root/'preview-ready.json').exists() and self.call and self.call.status()['enabled'])
    def status(self):return scope.status(self)
    def dispatch(self,raw):
        self.assert_original()
        if not self.ready()or not(self.root/'demo-execution-reserved.json').exists():raise r.runtime_service.RuntimeRefusal('NEW_FULL_CAPTURE_ACK_REQUIRED')
        scope.credit(self,600)
        return self.call.dispatch(raw)
    def export(self,raw):
        if not 1<=len(raw)<=262144:raise Refusal('EXPORT_BOUND')
        import app
        value=json.loads(raw);app.verify_evolution(value)
        path=self.root/'exports/evolution.json';binary_once(path,raw);return {'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'retained':True}

def bounded_probe(path,codec,p,*,receipt=None):
    import worker_scope67 as w
    path=Path(path)
    if codec!='vp8':raise Refusal('RETAINED113_VP8_ONLY')
    if receipt is None:
        if path!=Path(p['root'])/'native/media.webm':raise Refusal('RETAINED113_NATIVE_OWNER_QUALIFICATION_ONLY')
        receipt=path.parent/'worker67-probe'
    worker,out=w.run('probe',str(path),receipt)
    if worker['pass']is not True:return {'pass':False,'error':'PROBE_EXECUTION_FAILED','worker':worker}
    result=parse_probe113(out,codec,p);result['worker']=worker;return result

def parse_probe113(out,codec,p):
    try:
        data=json.loads(out);videos=[x for x in data['streams']if x['codec_type']=='video'];audio=[x for x in data['streams']if x['codec_type']=='audio'];v=videos[0];frames=int(v.get('nb_read_frames','0'))
        raw_duration=data.get('format',{}).get('duration');basis='container_duration'
        if raw_duration in(None,'','N/A')or float(raw_duration)==0:
            # Matroska Duration is optional. Keep the same duration bound using
            # actual video packet timestamps; do not accept an absent clock.
            packets=[x for x in data.get('packets',[])if x.get('codec_type')=='video']
            if not 2<=len(packets)<=90:raise ValueError('PACKET_BOUND')
            pts=[float(x['pts_time'])for x in packets]
            if not all(math.isfinite(x)for x in pts)or any(b<a for a,b in zip(pts,pts[1:])):raise ValueError('PACKET_CLOCK')
            raw_tail=packets[-1].get('duration_time')
            tail=(pts[-1]-pts[-2]if pts[-1]>pts[-2]else 1/p['fps'])if raw_tail in(None,'','N/A')else float(raw_tail)
            if not math.isfinite(tail)or not 0<tail<=1:raise ValueError('PACKET_TAIL')
            duration=pts[-1]-pts[0]+tail;basis='video_packet_timestamps'
        else:duration=float(raw_duration)
        ok=len(videos)==1 and not audio and v['codec_name']==codec and v['width']==p['width'] and v['height']==p['height'] and 2<=frames<=90 and math.isfinite(duration) and 0.1<=duration<=4
        return {'pass':ok,'codec':v['codec_name'],'width':v['width'],'height':v['height'],'frames':frames,'seconds':duration,'duration_basis':basis,'audio_streams':len(audio)}
    except Exception:return {'pass':False,'error':'PROBE_SHAPE'}

def probe_child(path,codec):raise Refusal('INTERNAL_SOURCE_BOUND_WORKER113_ENTRY_REQUIRED')

def readiness_page106():
    return b'<!doctype html><html lang="en"><meta charset="utf-8"><title>TraceHarbor native readiness106</title><h1>Native browser readiness106</h1><p>Read-only platform checks. No stream, recorder, private session, AI or provider request is created.</p><button id="readiness106">Check native platform before media</button><pre id="readiness106-status">Not started.</pre><script src="/recovery67/platform106.js" defer></script><script src="/recovery67/readiness106.js" defer></script></html>'

def review_page():
    return b'<!doctype html><html lang="en"><meta charset="utf-8"><title>TraceHarbor private final review</title><body><h1>Private final review</h1><p>176 seconds: actual server result excerpt, then synthetic walkthrough. Private; no publication or submission.</p><video controls playsinline preload="metadata" src="/recovery67/final.mp4"></video><p><a href="/recovery67/final.mp4" download="TraceHarbor176.mp4">Download verified private copy</a> <a href="/recovery67/av-result">Custody and technical checks</a></p><p>Manual visual/audio review still required before public delivery.</p></body></html>'

def html_page():
    return b'''<!doctype html><html lang="en"><meta charset="utf-8"><title>TraceHarbor checked recovery</title><body><h1>Checked recording recovery</h1><p><strong>Only after explicit execution authorization:</strong> select the browser tab named TraceHarbor &#183; Recording target67. After Share, activate that target tab and remain there for about 4 minutes, with up to 6 minutes margin. Keep this controller tab open; do not reload, close tabs, stop sharing, or press Share twice. Wait for CAPTURA SALVATA PRIVAT or CAPTURA OPRITA CU EROARE on the target, then return to ChatGPT. If no terminal after 6 minutes, return without restarting.</p><p>Existing diagnostic media is retained. A distinct server certificate is required before the original native sample and full recording. No new synthetic recording or retry.</p><button id="diagnose86" disabled>Original synthetic diagnostics closed</button><button id="select86" disabled>Select TraceHarbor tab and continue</button><p id="status86" role="status">Not started.</p><video id="preview86" muted controls playsinline></video><script src="/recovery67/selection146.js" defer></script><script src="/recovery67/controller.js" defer></script></body></html>'''

class Handler(r.ReleaseHandler):
    def allowed(self):
        # Same authenticated scope on every ephemeral Render ingress peer.
        # Never enroll a peer from headers or the old operator session alone.
        protected=(self.path.startswith('/recovery67/') and
                   self.path!='/recovery67/session') or self.path=='/operator86.js'
        if protected:
            if not self._tls_envelope() or not self.server.operator67.authorize(self):
                return False
            return self._qualify_owner_peer()
        return super().allowed()

    def _qualify_owner_peer(self):
        peer=r.ipaddress.ip_address(self.client_address[0])
        if not peer.is_private or peer.is_loopback or peer.is_unspecified:raise Refusal('PRIVATE_RENDER_PEER')
        with self.server.peer_enrollment_lock:
            key=str(peer);policy=self.server.edge_policy
            if key not in policy.peers:
                root=self.server.operator67.path/'qualified-proxy-peers';root.mkdir(mode=0o700,exist_ok=True);private_dir(root);f=root/(hashlib.sha256(key.encode()).hexdigest()+'.json');v={'peer':key,'proof':'NATIVE_RECOVERY93_OWNER','config_sha256':digest(policy.config)}
                if f.exists():
                    if read(f)!=v:raise Refusal('RECOVERY_PROXY_DRIFT')
                else:exclusive(f,v)
                policy.peers=policy.peers|{key}
        return True
    def do_GET(self):
        if self.path.startswith('/recovery86/'):return self.error(403,'Old146 retained and closed.')
        if self.path in ('/operator/session','/private-capture/')or self.path.startswith('/private-capture/'):
            return self.error(403,'Original capture84 is retained and closed. No retry.')
        if self.path in('/recovery67/readiness106','/recovery67/readiness106.js','/recovery67/platform106.js'):
            peer=r.ipaddress.ip_address(self.client_address[0])
            if not self._tls_envelope()or not peer.is_private or peer.is_loopback or peer.is_unspecified:return self.error(403,'Qualified TLS required.')
            if self.path=='/recovery67/readiness106':return self.respond(200,readiness_page106(),'text/html; charset=utf-8')
            name='readiness106.js'if self.path.endswith('readiness106.js')else'recovery67_client.js'
            return self.respond(200,(Path(__file__).parent/name).read_bytes(),'text/javascript; charset=utf-8')
        if self.path=='/recovery67/session':
            if not self._tls_envelope():return self.error(403,'TLS Host/Origin required.')
            body=b'<!doctype html><html lang="en"><meta charset="utf-8"><title>TraceHarbor recovery operator</title><h1>Recovery96 operator</h1><form method="post" action="/recovery67/session"><label>One-use recovery96 grant<input name="grant" type="password" required autocomplete="off"></label><button type="submit">Open recovery session</button></form></html>'
            self.send_response(200)
            for k,v in [('Content-Type','text/html; charset=utf-8'),('Content-Length',str(len(body))),('Cache-Control','no-store'),('Referrer-Policy','same-origin'),('Content-Security-Policy',"default-src 'none'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'")]:self.send_header(k,v)
            self.end_headers();self.wfile.write(body);return
        protected=self.path.startswith('/recovery67/')or self.path=='/operator86.js'
        if protected:
            if not self.allowed()or not self.server.operator67.authorize(self):return self.error(403,'Private recovery only.')
            m=self.server.recovery67
            if self.path=='/recovery67/target113':return self.error(403,'Original113 target closed; no retry.')
            if self.path=='/recovery67/target67':
                import app
                body=(app.ROOT/'web/index.html').read_bytes().replace(b'/app.js',b'/recovery67/app.js').replace(b'</head>',b'<link rel="stylesheet" href="/recovery67/demo.css"></head>').replace(b'</body>',b'<section id="capture-controls96"><h2>Captura autorizata96</h2><p>Alege fila curenta TraceHarbor &#183; Recording target67 in dialogul Share. Dupa Share ramai AICI aproximativ4 minute, cu marja6minute. Nu inchide, nu reincarca si nu opri partajarea. Asteapta mesajul CAPTURA SALVATA PRIVAT sau CAPTURA OPRITA CU EROARE, apoi revino la ChatGPT. Nu repeta Share.</p><button id="diagnose86" disabled>Diagnostice vechi inchise</button><button id="select86" disabled>Select TraceHarbor tab and continue</button><p id="status86" role="status"></p><video id="preview86" muted playsinline style="display:none"></video></section><script src="/recovery67/selection146.js" defer></script><script src="/recovery67/controller.js" defer></script><script src="/recovery67/operator67.js" defer></script></body>');return self.respond(200,body,'text/html; charset=utf-8')
            if self.path=='/recovery67/':return self.respond(200,html_page(),'text/html; charset=utf-8')
            if self.path=='/recovery67/status':return self.respond(200,canonical(m.status()))
            if self.path=='/recovery67/runtime/status':return self.respond(200,canonical(m.status()))
            if self.path=='/recovery67/input':return self.respond(200,(Path(__file__).parent/'credit67_input.json').read_bytes())
            if self.path=='/recovery67/app.js':
                import app
                data=(app.ROOT/'web/app.js').read_bytes().replace(b"'/runtime/status'",b"'/recovery67/runtime/status'").replace(b"'/runtime/analyze'",b"'/recovery67/runtime/analyze'")
                return self.respond(200,data,'text/javascript; charset=utf-8')
            if self.path=='/recovery67/review':return self.respond(200,review_page(),'text/html; charset=utf-8')
            if self.path=='/recovery67/av-result':return self.respond(200,canonical(read(m.root/'av/result.json')))
            fixed={'/recovery67/operator67.js':('operator67.js','text/javascript'),'/recovery67/selection146.js':('selection146.js','text/javascript'),'/recovery67/controller.js':('recovery67_client.js','text/javascript'),'/operator86.js':('operator86.js','text/javascript'),'/recovery67/demo.css':('recovery86_demo.css','text/css'),'/recovery67/policy':('recovery86_policy.json','application/json'),'/recovery67/historical':('examples/recorded/provider_record228.json','application/json')}
            if self.path in fixed:
                n,kind=fixed[self.path]
                if self.path=='/recovery67/policy':
                    view=dict(m.p);view['codecs']={'vp8':m.p['codecs']['vp8']};view['diagnostic_epoch']='RETAINED113_NO_NEW_SYNTHETIC_MEDIA';view['synthetic_diagnostics_closed']=True;view['worker_profile113']=__import__('worker_scope67').PROFILE;return self.respond(200,canonical(view))
                return self.respond(200,(Path(__file__).parent/n).read_bytes(),kind+'; charset=utf-8')
            if self.path=='/recovery67/export':
                f=m.root/'exports/evolution.json';regular(f);return self.respond(200,f.read_bytes())
            if self.path in('/recovery67/native.webm','/recovery67/final.mp4'):
                f=m.root/'native/media.webm'if self.path.endswith('.webm')else m.root/'av/final.mp4';return self.media(f,'video/webm'if f.suffix=='.webm'else'video/mp4')
            return self.error(404,'Not found.')
        return super().do_GET()
    def respond(self,code,body,content_type='application/json; charset=utf-8'):
        # Local Blob preview is read-only and contains this session's own media.
        self.send_response(code)
        for k,v in [('Content-Type',content_type),('Content-Length',str(len(body))),('Cache-Control','no-store'),('X-Content-Type-Options','nosniff'),('Content-Security-Policy',"default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; media-src 'self' blob:; img-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'")]:self.send_header(k,v)
        self.end_headers();self.wfile.write(body)
    def media(self,f,kind):
        regular(f);size=f.stat().st_size
        if f.suffix=='.mp4':
            result=read(f.parent/'result.json')
            if result.get('state')!='RENDERED_NOT_PUBLIC'or size!=result['bytes']or hashlib.sha256(f.read_bytes()).hexdigest()!=result['sha256']:raise Refusal('AV_NOT_VERIFIED')
        if size>self.server.recovery67.p['full_bytes']:return self.error(413,'Media bound.')
        values=self.headers.get_all('Range',[]);start,end=0,size-1;code=200
        if values:
            match=re.fullmatch(r'bytes=(\d+)-(\d*)',values[0])if len(values)==1 else None
            if not match:return self.error(416,'Single range required.')
            start=int(match[1]);end=min(size-1,int(match[2])if match[2]else size-1);code=206
            if not 0<=start<=end<size:return self.error(416,'Range bound.')
        self.send_response(code);self.send_header('Content-Type',kind);self.send_header('Cache-Control','no-store');self.send_header('Accept-Ranges','bytes');self.send_header('Content-Length',str(end-start+1))
        if code==206:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
        self.end_headers()
        with f.open('rb')as stream:
            stream.seek(start);remaining=end-start+1
            while remaining:
                block=stream.read(min(65536,remaining))
                if not block:raise Refusal('MEDIA_TRUNCATED')
                self.wfile.write(block);remaining-=len(block)
    def do_POST(self):
        if self.path.startswith('/recovery86/'):return self.error(403,'Old146 retained and closed.')
        if self.path=='/operator/session'or self.path.startswith('/private-capture/'):
            return self.error(403,'Original capture84 retained; no retry.')
        if self.path=='/recovery67/session':
            try:
                if not self._tls_envelope()or self.headers.get('Content-Type')!='application/x-www-form-urlencoded':raise Refusal('SESSION_HEADERS')
                raw=self.body(512);form=parse_qs(raw.decode('ascii'),strict_parsing=True,max_num_fields=1)
                if set(form)!={'grant'}or len(form['grant'])!=1:raise Refusal('SESSION_FORM')
                token=self.server.operator67.consume(form['grant'][0].encode());self._qualify_owner_peer();self.send_response(303);self.send_header('Location','/recovery67/target67');self.send_header('Set-Cookie',COOKIE+'='+token+'; Secure; HttpOnly; SameSite=Strict; Path=/; Max-Age=1800');self.send_header('Content-Length','0');self.send_header('Cache-Control','no-store');self.end_headers()
            except Exception:self.error(403,'Recovery session refused; no automatic retry.')
            return
        if self.path.startswith('/recovery67/'):
            try:
                if not self.allowed()or not self.server.operator67.authorize(self):raise Refusal('RECOVERY_OWNER_REQUIRED')
                m=self.server.recovery67
                if self.path=='/recovery67/runtime/analyze':
                    if self.headers.get('Content-Type')!='application/json':raise Refusal('JSON_REQUIRED')
                    return self.respond(200,canonical(m.dispatch(self.body(262144))))
                if self.path=='/recovery67/arm67':
                    value=json.loads(self.body(1024));return self.respond(200,canonical(m.arm67(value['client_id'])))
                if self.path=='/recovery67/chunk':
                    if self.headers.get('Content-Type')!='application/octet-stream':raise Refusal('CHUNK_TYPE')
                    for key in ('X-Recovery-Phase','X-Chunk-Sequence','X-Chunk-SHA256'):
                        if len(self.headers.get_all(key,[]))!=1:raise Refusal('CHUNK_HEADERS')
                    value=m.append(self.headers['X-Recovery-Phase'],int(self.headers['X-Chunk-Sequence']),self.body(1048576),self.headers['X-Chunk-SHA256'])
                else:
                    if self.headers.get('Content-Type')!='application/json':raise Refusal('JSON_REQUIRED')
                    raw=self.body(262144 if self.path=='/recovery67/export' else 4096);x=json.loads(raw)
                    if self.path=='/recovery67/prepare67'and set(x)=={'codec'}:value=scope.prepare_selection(m,x['codec'])
                    elif self.path=='/recovery67/start67'and set(x)=={'key'}:value=scope.start_selection(m,x['key'])
                    elif self.path=='/recovery67/reserve'and set(x)=={'phase','codec'}:value=m.reserve(x['phase'],x['codec'])
                    elif self.path=='/recovery67/finish'and set(x)=={'phase','value'}:value=m.finish(x['phase'],x['value'])
                    elif self.path=='/recovery67/fail'and set(x)=={'phase','error_name','where'}:value=m.fail(x['phase'],x['error_name'],x['where'])
                    elif self.path=='/recovery67/arm'and set(x)=={'client_id'}:value=m.arm(x['client_id'])
                    elif self.path=='/recovery67/begin'and set(x)=={'client_id'}:value=m.begin(x['client_id'])
                    elif self.path=='/recovery67/mark'and set(x)=={'name','elapsed'}:value=m.mark(x['name'],x['elapsed'])
                    elif self.path=='/recovery67/preview'and x=={'decoded':True}:value=m.preview()
                    elif self.path=='/recovery67/export':value=m.export(raw)
                    else:raise Refusal('RECOVERY_ROUTE_SHAPE')
                return self.respond(200,canonical(value))
            except Exception:return self.error(403,'Recovery refused or unknown; no automatic retry.')
        return super().do_POST()
    def body(self,limit):
        if len(self.headers.get_all('Content-Length',[]))!=1 or self.headers.get_all('Transfer-Encoding',[]):raise Refusal('BODY_FRAMING')
        n=int(self.headers['Content-Length'])
        if not 1<=n<=limit:raise Refusal('BODY_BOUND')
        self.connection.settimeout(6);raw=self.rfile.read(n)
        if len(raw)!=n:raise Refusal('BODY_TRUNCATED')
        return raw

def wire(server,config):
    p=policy()
    if os.environ.get('RENDER')!='true'or os.environ.get('RENDER_EXTERNAL_HOSTNAME')!=p['host']:raise Refusal('NATIVE_HOST')
    m=Recovery(scope.ROOT,scope.ORIGINAL,config,p);m.initialize()
    r.NEW_REQUEST=p['request_sha256'];server.recovery67=m;server.operator67=m.operator;server.RequestHandlerClass=Handler;return server

if __name__=='__main__':
    if len(sys.argv)==4 and sys.argv[1]=='--probe':probe_child(sys.argv[2],sys.argv[3])
    else:raise SystemExit('RECOVERY86_NOT_ADMITTED: no default provision, grant, recorder or provider call')
