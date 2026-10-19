"""Trusted113 prequalification orchestration. Public synthetic evidence only."""
import pathlib,json,time,os,sys,hashlib,importlib.util
IMAGE='docker.io/library/python@sha256:2ed6491b93cd49272ee6de2b5a38440c3448360322c089fc23e370722d74179d'
class Stop(RuntimeError):
    pass
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def stamp(q,operation,exc=None):
    if q['primary'] is None:
        q['primary']={'operation':operation,'exception_class':'RuntimeError' if exc is None else type(exc).__name__ if type(exc).__name__ in ('ValueError','OSError','TimeoutError','GateFailure','Stop') else 'OTHER'}
def command(g,private,q,label,argv,deadline,required=True):
    # invoke writes its original return/captures before this guard. No conversion first.
    t,data=g.invoke(argv,private,label,deadline)
    q['commands'].append({'operation':label,'returncode':t['returncode'],'timed_out':t['timed_out'],'capture_failure':bool(t['capture_failures']),'primary_present':t['primary'] is not None})
    ok=t['returncode']==0 and t['primary'] is None and not t['capture_failures'] and not t['timed_out']
    if required and not ok:
        stamp(q,label);raise Stop('Trusted command stopped')
    return ok,data,t
def require(value,operation,q):
    if not value:
        stamp(q,operation);raise Stop('Qualification guard stopped')
def inspect_config(v,binding):
    h=v['HostConfig'];labels=v['Config'].get('Labels') or {}
    assert labels.get('trace113.source')==binding['source_sha'] and labels.get('trace113.once')==binding['once_receipt_sha256']
    assert v['Config']['Image']==IMAGE and v['Config']['User']=='65532:65532'
    assert h['NetworkMode']=='none' and h['ReadonlyRootfs'] is True and h['Privileged'] is False
    assert h['Memory']==1073741824 and h['MemorySwap']==1073741824 and h['PidsLimit']==64 and h['NanoCpus']==1000000000
    assert h['CapDrop']==['ALL'] and h['SecurityOpt']==['no-new-privileges:true']
    return v['State']
def cleanup(g,private,name,binding,deadline,q,native=False):
    """Fresh ownership+state before one kill; never blind rm-f or create/start replay."""
    receipt_scope = "native-cleanup" if native else "diagnostic-cleanup"
    try:
        ok,data,t=command(g,private,q,receipt_scope+'-inspect',['docker','inspect',name],min(deadline,time.monotonic()+5),False)
        if not ok:
            # Exact Docker absence is useful reconciliation, never permission to replay.
            text=data['stderr'].decode('utf-8','replace').strip()
            absent=(('No such object: '+name) in text or ('No such container: '+name) in text)
            require(absent,'cleanup-unknown',q)
            q['cleanup']='PASS_ABSENT'
            return [],True
        v=g.strict(data['stdout'])[0];state=inspect_config(v,binding)
        if state.get('Running') is True:
            command(g,private,q,receipt_scope+'-kill',['docker','kill',name],min(deadline,time.monotonic()+5))
            command(g,private,q,receipt_scope+'-wait',['docker','wait',name],min(deadline,time.monotonic()+8))
        ok,data,t=command(g,private,q,receipt_scope+'-postterminal',['docker','inspect',name],min(deadline,time.monotonic()+5))
        state=inspect_config(g.strict(data['stdout'])[0],binding)
        require(state.get('Running') is False,'cleanup-not-stopped',q)
        command(g,private,q,receipt_scope+'-remove',['docker','rm',name],min(deadline,time.monotonic()+5))
        q['cleanup']='PASS'
        return [],True
    except BaseException as exc:
        stamp(q,'cleanup-unknown',exc);q['cleanup']='UNKNOWN'
        return [g.primary('CLEANUP','CLEANUP',RuntimeError())],False
def process(g,t):
    projected=g.project_process(t)
    assert projected['terminal_observed'] is True
    return projected
def project_native(g,value,binding):
    assert type(value) is dict and value.get('schema')=='NEW112_NATIVE_GROUP_V1'
    assert value.get('binding')==dict(binding,image=IMAGE)
    cases=value.get('cases');assert type(cases) is list and len(cases)==3 and [c.get('case') for c in cases]==[1,2,3]
    assert value.get('all_pass') is True and all(c.get('pass') is True for c in cases)
    assert all(value.get(k)==0 for k in ('counter','model','install','downloaded_import'))
    a,b,c=cases
    pa=process(g,a['outcome']);assert pa['primary'] is None and pa['original_returncode']==0
    iso=pa['isolation'];assert iso['abi']>=3 and iso['restricted'] is True and iso['cache_soft_limit_raised'] is True and iso['primary'] is None and not iso['cleanup'] and iso['output_fds_closed_count']==2
    data=a['cache_write'];expected=hashlib.sha256()
    for _ in range(9):expected.update(b'x'*1048576)
    assert data=={'bytes':9437184,'sha256':expected.hexdigest(),'file_limit':[67108864,67108864],'memory_limit':[1073741824,1073741824]}
    pb=process(g,b['outcome']);assert pb['primary']['code']=='CAPTURE_FAILURE' and pb['original_returncode']==0
    stream=b['outcome']['streams']['stdout'];assert stream['available'] is True and stream['bytes']==65536 and stream['truncated'] is True
    denied=b['denial'];assert denied=={'denied':{'open_write':True,'truncate':True,'rename':True},'output_fd_present':False}
    late=process(g,c['late']);timeout=process(g,c['timeout'])
    assert late['primary'] is None and late['original_returncode']==0 and late['kill_attempts']==0
    assert timeout['primary']['code']=='DEADLINE' and timeout['original_returncode']==-9 and timeout['kill_attempts']==1
    return {'schema':'TRACE113_TYPED_NATIVE_EVIDENCE_V1','binding':dict(binding,image=IMAGE),
        'all_pass':True,'cases':[{'case':1,'pass':True,'cache_write':data,'process':pa},
        {'case':2,'pass':True,'denial':denied,'process':pb,'stdout':{k:stream[k] for k in ('available','bytes','sha256','truncated')}},
        {'case':3,'pass':True,'late':late,'timeout':timeout}],
        'declared_evidence_only':True,'authority':False}
def prequalify(g,x,repo,m,private,binding,overall):
    q={'schema':'TRACE113_PREQUALIFICATION_V1','binding':dict(binding),'primary':None,
       'native':'NOT_RUN','inventory':'NOT_RUN','cleanup':'NOT_RUN','commands':[],
       'image_pull_attempts':0,'native_instances':0,'diagnostic_admitted':False,
       'native_evidence':None,'inventory_evidence':None,'host_terminal':None}
    g._QUAL113=q
    require(overall-time.monotonic()>=515,'whole-job-budget',q)
    try:
        image_deadline=min(overall-470,time.monotonic()+45)
        ok,data,t=command(g,private,q,'image-inspect',['docker','image','inspect',IMAGE],min(image_deadline,time.monotonic()+5),False)
        if not ok:
            q['image_pull_attempts']=1
            command(g,private,q,'official-image-pull',['docker','pull','--platform=linux/amd64',IMAGE],image_deadline)
            ok,data,t=command(g,private,q,'image-inspect-after',['docker','image','inspect',IMAGE],image_deadline)
        im=g.strict(data['stdout'])[0]
        require(im['Architecture']=='amd64' and im['Os']=='linux' and any(d.endswith('@'+IMAGE.split('@')[1]) for d in im['RepoDigests']),'immutable-image',q)
        require(overall-time.monotonic()>=470,'pre-native-budget',q)
        native_end=time.monotonic()+110;work=native_end-30
        name='traceharbor-qual113-'+binding['run_id']+'-'+x.once_receipt_sha[:12]
        args=['docker','create','--name',name,'--platform=linux/amd64','--network=none','--read-only','--user=65532:65532','--cap-drop=ALL','--security-opt=no-new-privileges:true',
            '--label=trace113.source='+x.source_sha,'--label=trace113.once='+x.once_receipt_sha,
            '--pids-limit=64','--memory=1g','--memory-swap=1g','--cpus=1',
            '--ulimit=cpu=120:120','--ulimit=nofile=1024:1024','--ulimit=fsize=8388608:67108864','--ipc=private','--workdir=/cache',
            '--tmpfs=/cache:rw,exec,nosuid,nodev,size=512m,uid=65532,gid=65532,mode=700',
            '--tmpfs=/output:rw,noexec,nosuid,nodev,size=8m,uid=65532,gid=65532,mode=700']
        for key,value in binding.items():
            args+=['--env','TRACE113_'+key.upper()+'='+value]
        for src,dst in [(repo/'diagnostic108/worker.py','/driver/worker.py'),(repo/'qualification113/native.py','/driver/native.py')]:
            require(src.is_file() and not src.is_symlink(),'source-mount',q)
            args+=['--mount','type=bind,src='+str(src)+',dst='+dst+',readonly']
        args += [IMAGE,'python','-I','/driver/native.py']
        q['native_instances']=1
        try:
            command(g,private,q,'native-create',args,min(work,time.monotonic()+10))
            ok,data,t=command(g,private,q,'native-inspect-before',['docker','inspect',name],min(work,time.monotonic()+5))
            v=g.strict(data['stdout'])[0];inspect_config(v,binding)
            binds=[p for p in v['Mounts'] if p['Type']=='bind']
            require(len(binds)==2 and all(p['RW'] is False for p in binds) and {p['Destination'] for p in binds}=={'/driver/worker.py','/driver/native.py'},'native-mount-proof',q)
            require(all(p['Destination'] in ('/driver/worker.py','/driver/native.py','/cache','/output') for p in v['Mounts']),'native-mount-allowlist',q)
            require(v['HostConfig']['Tmpfs']=={'/cache':'rw,exec,nosuid,nodev,size=512m,uid=65532,gid=65532,mode=700','/output':'rw,noexec,nosuid,nodev,size=8m,uid=65532,gid=65532,mode=700'},'native-tmpfs-limits',q)
            command(g,private,q,'native-start',['docker','start',name],min(work,time.monotonic()+5))
            command(g,private,q,'native-wait',['docker','wait',name],work)
            ok,data,t=command(g,private,q,'native-terminal',['docker','inspect',name],min(work,time.monotonic()+5))
            state=inspect_config(g.strict(data['stdout'])[0],binding)
            q['host_terminal']=g.terminal_projection(state)
            require(state['Running'] is False and state['OOMKilled'] is False,'native-terminal-stopped',q)
            ok,data,t=command(g,private,q,'native-public-synthetic-proof',['docker','logs',name],min(work,time.monotonic()+5))
            value=g.strict(data['stdout'])
            # A failed actual native case still yields bounded typed custody.
            failure_cases=[]
            if type(value) is dict and value.get('schema')=='NEW112_NATIVE_GROUP_V1':
                for c in value.get('cases',[])[:3]:
                    if type(c) is dict and type(c.get('case')) is int and c['case'] in (1,2,3):
                        item={'case':c['case'],'pass':c.get('pass') is True,'declared_evidence_only':True,'authority':False}
                        for key in ('outcome','late','timeout'):
                            if type(c.get(key)) is dict:
                                item[key]=g.project_process(c[key])
                        failure_cases.append(item)
            q['native_failure_evidence']={'schema':'TRACE113_TYPED_NATIVE_FAILURE_V1','cases':failure_cases,'declared_evidence_only':True,'authority':False}
            require(state['ExitCode']==0,'native-terminal-success',q)
            q['native_evidence']=project_native(g,value,binding)
            q['native']='PASS'
        finally:
            failures,stopped=cleanup(g,private,name,binding,native_end,q,True)
            require(not failures and stopped,'native-cleanup',q)
        q['native_cleanup']=q['cleanup']
        require(q['native']=='PASS' and q['cleanup']=='PASS','native-gate',q)
        require(overall-time.monotonic()>=360,'pre-acquire-budget',q)
        command(g,private,q,'public-acquire',[sys.executable,'-I',str(repo/'offline103/acquire.py'),'--manifest',str(repo/'offline103/transfer.json'),'--manifest-sha',m['canonical_transfer_sha256'],'--source-sha',x.source_sha,'--public-only'],min(overall-250,time.monotonic()+110))
        require(overall-time.monotonic()>=250,'pre-inventory-budget',q)
        inventory=load(repo/'qualification113/wheel_inventory.py','trace113_inventory')
        began=time.monotonic()
        value=inventory.inventory(pathlib.Path(os.environ['RUNNER_TEMP'])/'traceharbor-offline103/wheels',repo/'offline103/requirements.lock',m['wheels'])
        require(time.monotonic()-began<=25 and overall-time.monotonic()>=225,'inventory-deadline',q)
        q['inventory_evidence']=value;q['inventory']='FAIL'
        require(value['fits_64MiB_regular_ceiling'] is True and len(value['wheels'])==29 and value['largest_member']['bytes']<=67108864 and value['total_uncompressed']<=536870912,'inventory-gate',q)
        q['inventory']='PASS';q['diagnostic_admitted']=True
        return q
    except BaseException as exc:
        if q['native_instances'] and q['native']!='PASS':
            q['native']='FAIL' if q['host_terminal'] is not None and q['host_terminal']['observed'] else 'UNKNOWN'
        stamp(q,'prequalification',exc)
        raise
def project_state(g,q,binding):
    """This state is host-created, never a worker pathname or provenance declaration."""
    if q is None:
        return {'schema':'TRACE113_PREQUALIFICATION_V1','binding':binding,'native':'NOT_RUN','inventory':'NOT_RUN','diagnostic_admitted':False}
    assert q['binding']==binding and q['native'] in ('NOT_RUN','PASS','FAIL','UNKNOWN') and q['inventory'] in ('NOT_RUN','PASS','FAIL') and q['cleanup'] in ('NOT_RUN','PASS','PASS_ABSENT','UNKNOWN')
    assert len(q['commands'])<=40 and q['image_pull_attempts'] in (0,1) and q['native_instances'] in (0,1)
    # Values are generated by trusted source-pinned host paths with typed projections.
    return q

