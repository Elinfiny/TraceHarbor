"""Private104 source candidate. Trusted OpenSSL CMS only; no live invocation104.
Future orchestration supplies authenticated provider run/artifact originals,
executes the returned four immutable Git operations once, and reconciles UNKNOWN.
"""
import argparse,base64,hashlib,json,os,pathlib,re,ssl,stat,subprocess,time,urllib.request,urllib.error,urllib.parse
NAMES=('count_chat.py','count_request.py','served_template.jinja')
CTX={'repository','repository_id','actor_id','run_id','attempt','source_sha','nonce','certificate_sha256','expires_utc'}
def can(d):return json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok):
    if not ok:raise ValueError('Private ingress validation failed')
def strict(b):
    def pairs(items):
        d={}
        for k,v in items:require(k not in d);d[k]=v
        return d
    return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda _:require(False))
def put(p,b,mode=0o600):
    fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,mode)
    with os.fdopen(fd,'wb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def read(p,cap):
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        s=os.fstat(fd);require(stat.S_ISREG(s.st_mode) and s.st_nlink==1 and s.st_size<=cap)
        b=bytearray()
        while len(b)<=cap:
            x=os.read(fd,min(65536,cap+1-len(b)))
            if not x:break
            b.extend(x)
        e=os.fstat(fd);require(len(b)<=cap and len(b)==e.st_size and (s.st_size,s.st_mtime_ns,s.st_ctime_ns)==(e.st_size,e.st_mtime_ns,e.st_ctime_ns));return bytes(b)
    finally:os.close(fd)
def command(args,timeout=20,trace=None):
    start=time.time()
    # Publisher107 only: exact CMS structure inspection can print ciphertext.
    inspection=len(args)==8 and tuple(args[:5])==('cms','-cmsout','-inform','DER','-in') and tuple(args[6:])==('-print','-noout')
    stdout_cap=1048576 if inspection else 65536
    try:
        r=subprocess.run(['openssl',*map(str,args)],stdin=subprocess.DEVNULL,capture_output=True,timeout=timeout,close_fds=True)
        receipt={'argv_operation':args[0],'returncode':r.returncode,'utc':start,'stdout':r.stdout.decode(errors='replace'),'stderr':r.stderr.decode(errors='replace')}
        for name,data in (('stdout',r.stdout),('stderr',r.stderr)):
            receipt[name+'_base64']=base64.b64encode(data).decode('ascii');receipt[name+'_bytes']=len(data);receipt[name+'_sha256']=sha(data)
    except subprocess.TimeoutExpired as exc:
        receipt={'argv_operation':args[0],'returncode':None,'utc':start,'timeout':True,'stdout':None if exc.stdout is None else exc.stdout.decode(errors='replace'),'stderr':None if exc.stderr is None else exc.stderr.decode(errors='replace')}
        for name,data in (('stdout',exc.stdout),('stderr',exc.stderr)):
            receipt[name+'_base64']=None if data is None else base64.b64encode(data).decode('ascii');receipt[name+'_bytes']=None if data is None else len(data);receipt[name+'_sha256']=None if data is None else sha(data)
        if trace is not None:trace.append(receipt)
        raise RuntimeError('OpenSSL terminal UNKNOWN') from None
    receipt['stdout_cap_bytes']=stdout_cap;receipt['stderr_cap_bytes']=65536;receipt['inspection_cap_scope']=inspection
    if trace is not None:trace.append(receipt)
    require(len(r.stdout)<=stdout_cap and len(r.stderr)<=65536)
    if r.returncode!=0:raise RuntimeError('OpenSSL rejected operation rc='+str(r.returncode))
    return r.stdout
def context(c):
    require(set(c)==CTX and c['repository']=='Elinfiny/TraceHarbor' and c['repository_id']==1391430317 and c['actor_id']==273768139 and type(c['run_id']) is int and c['run_id']>0 and type(c['attempt']) is int and c['attempt']==1)
    require(re.fullmatch('[0-9a-f]{40}',c['source_sha']) and re.fullmatch('[0-9a-f]{32}',c['nonce']) and re.fullmatch('[0-9a-f]{64}',c['certificate_sha256']) and type(c['expires_utc']) is int and time.time()<c['expires_utc']<=time.time()+900)
def fingerprint(pem):return sha(ssl.PEM_cert_to_DER_cert(pem.decode('ascii')))
def recipient(directory,c,trace=None):
    directory.mkdir(mode=0o700);key=directory/'recipient.key';cert=directory/'recipient.pem'
    # Parent is newly private, umask077; OpenSSL-created key never mounted/uploaded.
    old=os.umask(0o077)
    try:command(['req','-x509','-newkey','rsa:3072','-sha256','-noenc','-batch','-days','1','-subj','/CN=TraceHarbor-ephemeral104','-keyout',key,'-out',cert],trace=trace)
    finally:os.umask(old)
    os.chmod(key,0o600);os.chmod(cert,0o600);pem=read(cert,6000);c=dict(c,certificate_sha256=fingerprint(pem));context(c)
    return c,pem
def envelope(c,files,pins):
    context(c);require(set(files)==set(NAMES) and {p['name'] for p in pins}==set(NAMES) and len(pins)==3)
    members=[]
    for p in sorted(pins,key=lambda p:p['name']):
        b=files[p['name']];require(len(b)==p['bytes'] and sha(b)==p['sha256']);members.append({'name':p['name'],'bytes':len(b),'sha256':sha(b),'base64':base64.b64encode(b).decode()})
    b=can({'context':c,'members':members});require(len(b)<=65536);return b
def encrypt(directory,c,pem,files,pins,trace=None):
    context(c);require(fingerprint(pem)==c['certificate_sha256']);directory.mkdir(mode=0o700)
    plain=directory/'private.json';cert=directory/'public.pem';cipher=directory/'encrypted.cms'
    put(plain,envelope(c,files,pins));put(cert,pem)
    try:
        # Explicit OAEP digest AND MGF1 digest; no default RSA v1.5 fallback.
        command(['cms','-encrypt','-binary','-aes-256-gcm','-in',plain,'-outform','DER','-out',cipher,'-recip',cert,'-keyopt','rsa_padding_mode:oaep','-keyopt','rsa_oaep_md:sha256','-keyopt','rsa_mgf1_md:sha256'],trace=trace)
        b=read(cipher,131072)
        structure=command(['cms','-cmsout','-inform','DER','-in',cipher,'-print','-noout'],trace=trace)
        require(b'id-smime-ct-authEnvelopedData' in structure and b'aes-256-gcm' in structure and b'rsaesOaep' in structure and b'sha256' in structure)
        return b
    finally:plain.unlink(missing_ok=True)
def decrypt(directory,c,key,cert,cipher,pins,trace=None):
    context(c);require(fingerprint(read(cert,6000))==c['certificate_sha256']);directory.mkdir(mode=0o700)
    require(len(cipher)<=131072);enc=directory/'encrypted.cms';quarantine=directory/'UNAUTHENTICATED.private';put(enc,cipher);put(quarantine,b'')
    try:
        # OpenSSL can write before AEAD final authentication. Nothing reads this
        # quarantine until timely terminal0, and no consumer callback is invoked.
        command(['cms','-decrypt','-binary','-inform','DER','-in',enc,'-recip',cert,'-inkey',key,'-out',quarantine],trace=trace)
        raw=read(quarantine,65536);d=strict(raw);require(can(d)==raw and set(d)=={'context','members'} and d['context']==c)
        require(type(d['members']) is list and len(d['members'])==3)
        result={};expected={p['name']:p for p in pins};require(set(expected)==set(NAMES) and len(pins)==3)
        for m in d['members']:
            require(set(m)=={'name','bytes','sha256','base64'} and m['name'] in expected and m['name'] not in result and type(m['bytes']) is int and isinstance(m['base64'],str))
            b=base64.b64decode(m['base64'],validate=True);p=expected[m['name']];require(len(b)==m['bytes']==p['bytes'] and sha(b)==m['sha256']==p['sha256']);result[m['name']]=b
        context(c);require(set(result)==set(NAMES));return result
    finally:
        # Partial plaintext is UNUSED on failure; deletion is not secure erasure.
        quarantine.unlink(missing_ok=True)
def api(path,cap=262144,deadline=None,missing=False):
    require(path.startswith('/repos/Elinfiny/TraceHarbor/') and (deadline is None or time.monotonic()<deadline))
    req=urllib.request.Request('https://api.github.com'+path,headers={'Accept':'application/vnd.github+json','User-Agent':'TraceHarbor-trusted-ingress104'})
    # No credentials, no redirect, no worker code. Public repository only.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,*a,**kw):raise ValueError('Unexpected API redirect')
    try:
        with urllib.request.build_opener(NoRedirect).open(req,timeout=min(10,max(.1,deadline-time.monotonic())) if deadline else 10) as r:b=r.read(cap+1)
    except urllib.error.HTTPError as exc:
        if missing and exc.code==404:return None
        raise RuntimeError('GitHub public ingress read failed') from None
    require(len(b)<=cap);return strict(b)
def transport(c,cipher,base_tree):
    context(c);require(re.fullmatch('[0-9a-f]{40}',base_tree) and len(cipher)<=131072)
    name='traceharbor-encrypted104-'+c['nonce']+'.cms';ref='refs/heads/traceharbor-encrypted104-'+c['nonce']
    # Orchestrator maps actual preceding returned IDs to $blob/$tree/$commit.
    # These are symbolic dependencies, not fabricated provider receipts.
    return {'repository':'Elinfiny/TraceHarbor','expected_repository_id':1391430317,'source_sha':c['source_sha'],'context':c,'ciphertext_sha256':sha(cipher),'ciphertext_bytes':len(cipher),'path':name,'ref':ref,'operations':[
        {'method':'POST','endpoint':'git/blobs','body':{'content':base64.b64encode(cipher).decode(),'encoding':'base64'}},
        {'method':'POST','endpoint':'git/trees','body':{'base_tree':base_tree,'tree':[{'path':name,'mode':'100644','type':'blob','sha':'$blob'}]}},
        {'method':'POST','endpoint':'git/commits','body':{'message':'TraceHarbor ephemeral ciphertext104','parents':[c['source_sha']],'tree':'$tree'}},
        {'method':'POST','endpoint':'git/refs','body':{'ref':ref,'sha':'$commit'}}], 'mutation_policy':'Reserve attempt with expected own CAS before each write; one write each; verify actual returned immutable IDs; ref preflight ABSENT; create-if-absent only; any UNKNOWN => readonly reconcile, no resend; no force/update/delete'}
def prepare_from_artifact(public,run,artifact,artifact_zip_sha,files,pins,out,base_tree,trace=None):
    require(set(public)=={'context','certificate_pem'});c=public['context'];context(c)
    require(run['id']==c['run_id'] and run['run_attempt']==1 and run['head_sha']==c['source_sha'] and run['event']=='workflow_dispatch' and run['actor']['id']==273768139 and run['repository']['id']==1391430317 and run['status']=='in_progress')
    require(artifact['id']>0 and artifact['name']=='traceharbor-recipient104-'+str(c['run_id'])+'-1' and artifact['expired'] is False and artifact['size_in_bytes']<=8192 and artifact['workflow_run']['id']==c['run_id'] and artifact['workflow_run']['head_sha']==c['source_sha'])
    require(artifact['digest']=='sha256:'+artifact_zip_sha)
    cipher=encrypt(out,c,public['certificate_pem'].encode(),files,pins,trace);return transport(c,cipher,base_tree)
def receive(c,key,cert,pins,out,wait_seconds=360):
    context(c);require(0<wait_seconds<=360);deadline=min(time.monotonic()+wait_seconds,time.monotonic()+c['expires_utc']-time.time()-240)
    prefix='/repos/Elinfiny/TraceHarbor/';ref='heads/traceharbor-encrypted104-'+c['nonce'];found=None
    while time.monotonic()<deadline:
        found=api(prefix+'git/ref/'+ref,deadline=deadline,missing=True)
        if found is not None:break
        time.sleep(min(15,max(0,deadline-time.monotonic())))
    require(found is not None and found['ref']=='refs/'+ref and found['object']['type']=='commit')
    commit_sha=found['object']['sha'];require(re.fullmatch('[0-9a-f]{40}',commit_sha))
    commit=api(prefix+'git/commits/'+commit_sha,deadline=deadline);require([p['sha'] for p in commit['parents']]==[c['source_sha']])
    source=api(prefix+'git/commits/'+c['source_sha'],deadline=deadline)
    before=api(prefix+'git/trees/'+source['tree']['sha'],deadline=deadline);after=api(prefix+'git/trees/'+commit['tree']['sha'],deadline=deadline)
    require(not before.get('truncated') and not after.get('truncated'))
    entries=lambda x:{e['path']:{k:e[k] for k in ('mode','type','sha')} for e in x['tree']}
    a=entries(before);b=entries(after);name='traceharbor-encrypted104-'+c['nonce']+'.cms';require(name not in a and set(b)==set(a)|{name} and all(a[k]==b[k] for k in a) and b[name]['mode']=='100644' and b[name]['type']=='blob')
    blob=api(prefix+'git/blobs/'+b[name]['sha'],cap=190000,deadline=deadline);require(blob['encoding']=='base64' and blob['size']<=131072)
    cipher=base64.b64decode(''.join(blob['content'].split()),validate=True);require(len(cipher)==blob['size'] and hashlib.sha1(b'blob '+str(len(cipher)).encode()+b'\0'+cipher).hexdigest()==b[name]['sha'])
    result=decrypt(out,c,key,cert,cipher,pins);return result,{'ciphertext_commit':commit_sha,'ciphertext_sha256':sha(cipher),'ref':found['ref']}
def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['init','receive']);p.add_argument('--source-sha',required=True);p.add_argument('--manifest-sha',required=True);a=p.parse_args();os.umask(0o077)
    kit=pathlib.Path(__file__).parent;raw=read(kit/'transfer.json',65536);require(sha(raw)==a.manifest_sha);m=strict(raw)
    require(m['admission']['state']=='INDEPENDENTLY_ADMITTED' and m['private_ingress']['state']=='INDEPENDENTLY_ADMITTED_ENCRYPTED104')
    for name,pin in m['source_files'].items():require(sha(read(kit.parent/name,131072))==pin)
    e=os.environ;require(e['GITHUB_SHA']==e['GITHUB_WORKFLOW_SHA']==a.source_sha and e['GITHUB_RUN_ATTEMPT']=='1' and e['GITHUB_REPOSITORY']=='Elinfiny/TraceHarbor' and e['GITHUB_REPOSITORY_ID']=='1391430317' and e['GITHUB_ACTOR_ID']=='273768139' and e['GITHUB_EVENT_NAME']=='workflow_dispatch')
    root=pathlib.Path(e['RUNNER_TEMP'])/'traceharbor-private104'
    if a.mode=='init':
        c={'repository':'Elinfiny/TraceHarbor','repository_id':1391430317,'actor_id':273768139,'run_id':int(e['GITHUB_RUN_ID']),'attempt':1,'source_sha':a.source_sha,'nonce':os.urandom(16).hex(),'expires_utc':int(time.time())+840}
        c,pem=recipient(root,c);public={'context':c,'certificate_pem':pem.decode('ascii')};require(len(can(public))<=8192);put(root/'recipient-public.json',can(public));put(root/'context.json',can(c))
    else:
        c=strict(read(root/'context.json',8192));require(c['source_sha']==a.source_sha and c['run_id']==int(e['GITHUB_RUN_ID']))
        result,receipt=receive(c,root/'recipient.key',root/'recipient.pem',m['private_members'],root/'quarantine')
        dest=pathlib.Path(e['RUNNER_TEMP'])/'traceharbor-reviewed-private-ingress';dest.mkdir(mode=0o700)
        for name in NAMES:put(dest/name,result[name],0o444)
        os.chmod(dest,0o555);put(root/'receipt.json',can(receipt));(root/'recipient.key').unlink()
if __name__=='__main__':main()
