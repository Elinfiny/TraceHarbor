"""Native-only, separately approved AV operation. Import never runs an encoder.
One durable reservation; errors/UNKNOWN retain every file, with no retry/delete.
"""
import hashlib,json,os,re,subprocess,sys,wave
from pathlib import Path
import recovery67 as r
import credit_scope67 as scope
H=lambda b:hashlib.sha256(b).hexdigest()
MARKS=('runtime-rendered','story-start','supported','citation','conflicted','exported','reimported','historical','story-end')
ENV={'PATH':'/usr/bin:/bin','LANG':'C','PYTHONDONTWRITEBYTECODE':'1'}

def caption_time(ms):
    sec,ms=divmod(ms,1000);mins,sec=divmod(sec,60);hours,mins=divmod(mins,60)
    return f'{hours:02}:{mins:02}:{sec:02},{ms:03}'
def shifted_captions(raw):
    blocks=raw.decode('utf8').strip().split('\n\n')
    if len(blocks)!=31:raise r.Refusal('ORIGINAL_PHRASE_COUNT')
    out=['1\n00:00:00,000 --> 00:00:06,000\nActual server result for synthetic input.\nOrigin and causal meaning are not independently attested.', '2\n00:00:06,000 --> 00:00:12,000\nOne admitted request. No retry or remediation.\nThe synthetic walkthrough follows.']
    pattern=r'(\d\d):(\d\d):(\d\d),(\d{3})'
    def shift(m):
        h,mn,s,ms=map(int,m.groups());v=((h*60+mn)*60+s)*1000+ms+12000
        if v>176000:raise r.Refusal('CAPTION_BOUND')
        return caption_time(v)
    for n,block in enumerate(blocks,3):
        rows=block.split('\n');rows[0]=str(n);rows[1]=re.sub(pattern,shift,rows[1]);out.append('\n'.join(rows))
    return ('\n\n'.join(out)+'\n').encode()
def audio_plan(edl):
    if edl['target']['seconds']!=164 or len(edl['cues'])!=9:raise r.Refusal('EDL_SHAPE')
    rows=[]
    for c in edl['cues']:
        start,end=c['sourcePCMstart_frame'],c['sourcePCMend_frame'];hold=c['hold'];gap=hold['original_source_gap_frames'];pad=hold['new_pad_frames']
        rows.append({'start':start,'end':end,'sha256':c['PCMsha256'],'gap':gap,'pad':pad})
    frames=192000+sum(x['end']-x['start']+x['gap']+x['pad']for x in rows)
    if frames!=2816000:raise r.Refusal('EDL_176_BOUND')
    return rows

def prepare_audio(voice,edl,output):
    # Reuse original speech byte-for-byte. This function runs only after AV reservation.
    with wave.open(str(voice),'rb')as f:
        if (f.getnchannels(),f.getsampwidth(),f.getframerate(),f.getnframes())!=(1,2,16000,1736960):raise r.Refusal('VOICE_FORMAT')
        pcm=f.readframes(f.getnframes())
    out=bytearray(192000*2)
    for c in audio_plan(edl):
        speech=pcm[c['start']*2:c['end']*2];gap=pcm[c['end']*2:(c['end']+c['gap'])*2]
        if H(speech)!=c['sha256']or any(gap):raise r.Refusal('VOICE_RANGE_OR_GAP')
        out.extend(speech);out.extend(gap);out.extend(bytes(c['pad']*2))
    if len(out)!=5632000:raise r.Refusal('PCM_BOUND')
    fd=os.open(output,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'wb')as raw:
        with wave.open(raw,'wb')as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(16000);f.writeframes(out)
        raw.flush();os.fsync(raw.fileno())

def gate(root,original,p):
    from types import SimpleNamespace
    m=SimpleNamespace(root=root,original=original,config=scope.contract()['release_config'],p=p,clock=__import__('time').time)
    scope.authority(m)
    if r.witness(original)!=p['original_capture_sha256']:raise r.Refusal('ORIGINAL84_DRIFT')
    terminal=r.read(root/'full/terminal.json')
    if terminal['state']!='CAPTURED_NOT_AV_VERIFIED'or not 224<=terminal['elapsed']<=230:raise r.Refusal('FULL_NOT_CAPTURED')
    if r.read(root/'native/qualified.json')['state']!='PASS'or not(root/'e2e-result.json').exists():raise r.Refusal('MEDIA_OR_AI_NOT_VERIFIED')
    native=r.read(root/'native/qualified.json',65536)
    import worker_scope67 as w
    if native.get('probe',{}).get('worker',{}).get('identity')!=w.identity():raise r.Refusal('NATIVE_IDENTITY_DRIFT')
    result=r.r.runtime_service.verify_runtime_result(r.read(root/'e2e-result.json',65536))
    ledger=scope.ledger(m);slot=r.read(ledger.path/'slot-002.json');terminal_AI=r.read(ledger.path/'terminal-002.json')
    if slot['request_sha256']!=p['request_sha256']or terminal_AI['state']!='VERIFIED_RECORD_SEMANTICS_NOT_VERIFIED':raise r.Refusal('NEW_SLOT002_NOT_VERIFIED')
    if any((root/('mark-'+n+'.json')).exists()for n in ('flow-failed','runtime-failed')):raise r.Refusal('FLOW_FAILED')
    marks={n:r.read(root/('mark-'+n+'.json'))for n in MARKS}
    if marks['runtime-rendered']['elapsed']>52:raise r.Refusal('LATE_RUNTIME')
    return terminal,marks

def commands(root):
    a=root/'av'
    filters='[0:v]trim=start=48:end=60,setpts=PTS-STARTPTS[v0];[0:v]trim=start=60:end=224,setpts=PTS-STARTPTS[v1];[v0][v1]concat=n=2:v=1:a=0,fps=15[v]'
    encode=['/usr/bin/ffmpeg','-v','error','-nostdin','-n','-threads','1','-protocol_whitelist','file,pipe','-i',str(a/'raw224.webm'),'-i',str(a/'audio176.wav'),'-i',str(a/'captions176.srt'),'-filter_complex_threads','1','-filter_complex',filters,'-map','[v]','-map','1:a','-map','2:s','-c:v','libx264','-preset','ultrafast','-threads','1','-b:v','800k','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-c:s','mov_text','-metadata:s:s:0','language=eng','-t','176','-movflags','+faststart',str(a/'final.mp4')]
    decode=['/usr/bin/ffmpeg','-v','error','-xerror','-nostdin','-threads','1','-protocol_whitelist','file,pipe','-i',str(a/'final.mp4'),'-map','0:v','-map','0:a','-f','null','-']
    probe=['/usr/bin/ffprobe','-v','error','-threads','1','-protocol_whitelist','file,pipe','-show_entries','stream=codec_type,codec_name,width,height:format=duration,size','-of','json',str(a/'final.mp4')]
    return {'encode':encode,'decode':decode,'final-probe':probe}

def bounded_child(mode,root,p):
    import worker_scope67 as w
    result,stdout=w.run(mode,'run',root/'av'/('worker113-'+mode))
    if result['pass']is not True:raise r.Refusal('AV_WORKER113_FAILED_CLOSED_NO_RETRY')
    return {'exit':0,'worker':result,'metadata':json.loads(stdout)if mode=='final-probe'else None}

def assemble(root,terminal,p):
    output=root/'av/raw224.webm';fd=os.open(output,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600);size=0;dig=hashlib.sha256()
    with os.fdopen(fd,'wb')as f:
        for i in range(terminal['chunks']):
            path=root/f'full/chunk-{i:05d}.webm';r.regular(path);data=path.read_bytes();receipt=r.read(path.with_suffix('.json'))
            if receipt['sequence']!=i or receipt['bytes']!=len(data)or receipt['sha256']!=H(data):raise r.Refusal('CHUNK_DRIFT')
            size+=len(data)
            if size>p['full_bytes']:raise r.Refusal('FULL_BYTE_BOUND')
            dig.update(data);f.write(data)
        f.flush();os.fsync(f.fileno())
    if size!=terminal['bytes']or not size:raise r.Refusal('FULL_CUSTODY_MISMATCH')
    return {'bytes':size,'sha256':dig.hexdigest()}

def render():
    p=r.policy();root=Path(p['root']);original=Path(p['original'])
    if os.environ.get('RENDER')!='true'or os.environ.get('RENDER_EXTERNAL_HOSTNAME')!=p['host']:raise r.Refusal('NATIVE_HOST')
    terminal,marks=gate(root,original,p)
    assets={name:Path(p['assets_root'])/name for name in ('voice.wav','edl.json','captions.srt')}
    for name,key in [('voice.wav','voice_sha256'),('edl.json','edl_member_sha256'),('captions.srt','captions_member_sha256')]:
        r.regular(assets[name])
        if H(assets[name].read_bytes())!=p[key]:raise r.Refusal('ASSET_PIN')
    edl=json.loads(assets['edl.json'].read_bytes());audio_plan(edl);captions=shifted_captions(assets['captions.srt'].read_bytes())
    r.exclusive(root/'av/render-reserved.json',{'id':'CREDIT-RECOVERY66-NEXT-AV176','state':'UNKNOWN_NO_RETRY','seconds':176,'retry':False})
    raw=assemble(root,terminal,p);prepare_audio(assets['voice.wav'],edl,root/'av/audio176.wav');r.binary_once(root/'av/captions176.srt',captions)
    checks={mode:bounded_child(mode,root,p)for mode in ('encode','decode','final-probe')};meta=checks['final-probe']['metadata'];streams=meta['streams'];v=[x for x in streams if x['codec_type']=='video'];a=[x for x in streams if x['codec_type']=='audio'];sub=[x for x in streams if x['codec_type']=='subtitle'];duration=float(meta['format']['duration'])
    if len(v)!=1 or v[0]['codec_name']!='h264'or(v[0]['width'],v[0]['height'])!=(1280,720)or len(a)!=1 or a[0]['codec_name']!='aac'or len(sub)!=1 or sub[0]['codec_name']!='mov_text'or not 175.75<=duration<=176.25:raise r.Refusal('FINAL_METADATA')
    final=root/'av/final.mp4';r.regular(final);size=final.stat().st_size
    if not 1<=size<=p['final_byte_limit']:raise r.Refusal('FINAL_SIZE')
    result={'state':'RENDERED_NOT_PUBLIC','bytes':size,'sha256':H(final.read_bytes()),'raw':raw,'checks':checks,'duration':duration,'captions':33,'original_speech_cues_unchanged':9,'retry':False,'public':False,'perceptual_QA':'REQUIRED_NATIVE_PRIVATE_PLAYBACK','original84_sha256':r.witness(original)}
    r.exclusive(root/'av/result.json',result);return result

def child(mode):raise r.Refusal('INTERNAL_SOURCE_BOUND_WORKER113_ENTRY_REQUIRED')
if __name__=='__main__':
    if sys.argv[1:]==['--render']:print(json.dumps(render(),sort_keys=True))
    elif len(sys.argv)==3 and sys.argv[1]=='--child':child(sys.argv[2])
    else:raise SystemExit('AV_NOT_ADMITTED_BY_DEFAULT')
