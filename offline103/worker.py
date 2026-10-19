"""SOURCE_ONLY103: trusted container driver; no execution performed in103."""
import ctypes, errno, hashlib, json, os, pathlib, resource, socket, subprocess, sys, time
R=pathlib.Path("/output"); C=pathlib.Path("/control"); I=pathlib.Path("/inputs")
def sha(b):return hashlib.sha256(b).hexdigest()
def emit(name,data):
    with (R/name).open("x") as f:json.dump(data,f,sort_keys=True);f.flush();os.fsync(f.fileno())
def wait(name,deadline):
    while time.monotonic()<deadline:
        f=C/name
        if f.is_file():return json.loads(f.read_text())
        time.sleep(.05)
    raise TimeoutError("Read-only control gate not received")
def restrict():
    assert sys.platform=="linux" and os.uname().machine=="x86_64"
    os.closerange(3,1048576)
    allowed={"PATH":"/usr/local/bin:/usr/bin:/bin","HOME":"/cache","TMPDIR":"/cache/tmp","LANG":"C.UTF-8","PYTHONNOUSERSITE":"1","PYTHONDONTWRITEBYTECODE":"1","HF_HUB_OFFLINE":"1","TRANSFORMERS_OFFLINE":"1","HF_HUB_DISABLE_TELEMETRY":"1","HF_HOME":"/cache/hf","OMP_NUM_THREADS":"1","OPENBLAS_NUM_THREADS":"1","USE_TORCH":"0","USE_TF":"0"}
    os.environ.clear();os.environ.update(allowed);pathlib.Path("/cache/tmp").mkdir()
    resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_AS,(1073741824,1073741824));resource.setrlimit(resource.RLIMIT_FSIZE,(8388608,8388608));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    # Additional child-only seccomp filter; Docker's default filter is retained.
    class F(ctypes.Structure):_fields_=[("code",ctypes.c_ushort),("jt",ctypes.c_ubyte),("jf",ctypes.c_ubyte),("k",ctypes.c_uint)]
    class P(ctypes.Structure):_fields_=[("len",ctypes.c_ushort),("filter",ctypes.POINTER(F))]
    deny=[41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,288,299,307,425,426,427,438,101,310,311,321,303,304,298,323]
    code=[F(0x20,0,0,4),F(0x15,1,0,0xc000003e),F(0x06,0,0,0x80000000),F(0x20,0,0,0),F(0x45,0,1,0x40000000),F(0x06,0,0,0x80000000)]
    for n in deny:code.extend([F(0x15,0,1,n),F(0x06,0,0,0x00050000|errno.EPERM)])
    code.append(F(0x06,0,0,0x7fff0000));arr=(F*len(code))(*code);prog=P(len(code),arr);lib=ctypes.CDLL(None,use_errno=True)
    assert lib.prctl(38,1,0,0,0)==0 and lib.prctl(22,2,ctypes.byref(prog),0,0)==0
def run(argv,stem,deadline):
    with (R/(stem+".stdout")).open("xb") as out,(R/(stem+".stderr")).open("xb") as err:
        r=subprocess.run(argv,env=dict(os.environ),stdin=subprocess.DEVNULL,stdout=out,stderr=err,timeout=max(.1,deadline-time.monotonic()),close_fds=True)
    emit(stem+".terminal.json",{"returncode":r.returncode,"utc":time.time(),"stdout_sha256":sha((R/(stem+".stdout")).read_bytes()),"stderr_sha256":sha((R/(stem+".stderr")).read_bytes())});assert r.returncode==0
def main():
    start=time.monotonic();deadline=start+170;restrict();go=wait("GO.json",min(deadline,start+30));assert time.time()<go["absolute_deadline_utc"]
    assert sys.version_info[:2]==(3,12)
    m=json.loads((I/"transfer.json").read_text());req=(I/"request.json").read_bytes();assert len(req)==4935 and sha(req)==m["request_sha256"];assert sha((I/"requirements.lock").read_bytes())==m["lock_sha256"]
    # Two harmless qualification cases, before install or downloaded imports.
    with (R/"permitted.synthetic").open("x") as f:f.write("synthetic")
    assert (R/"permitted.synthetic").read_text()=="synthetic"
    denied={}
    for name,action in [("host_file",lambda:pathlib.Path(go["host_sentinel"]).read_bytes()),("root_write",lambda:pathlib.Path("/etc/traceharbor-denied").write_text("synthetic")),("socket",lambda:socket.socket(socket.AF_INET,socket.SOCK_STREAM))]:
        try:action();raise AssertionError("Containment denied case unexpectedly succeeded")
        except (PermissionError,FileNotFoundError,OSError) as exc:denied[name]=exc.errno
    assert denied["socket"]==errno.EPERM and denied["root_write"] in [errno.EROFS,errno.EACCES,errno.EPERM]
    emit("qualification.json",{"case1_permitted_read_write":True,"case2_denial":denied,"credential_env_present":False,"counter_imported":False})
    for v in m["private_members"]:assert sha((pathlib.Path("/vendor")/v["name"]).read_bytes())==v["sha256"]
    for v in m["public_tokenizer"]:assert sha((pathlib.Path("/vendor/tokenizer")/v["name"]).read_bytes())==v["sha256"]
    intent={"external_once_receipt_sha256":go["external_once_receipt_sha256"],"source_sha":go["source_sha"],"runtime":m["runtime"]["immutable_image"],"request_sha256":sha(req),"lock_sha256":m["lock_sha256"],"counter_attempt_reserved":1,"absolute_deadline_utc":go["absolute_deadline_utc"],"output_absent":not (R/"count.json").exists()}
    assert intent["output_absent"];emit("intent.json",intent)
    with (R/"qualification.ready").open("xb"):pass
    approval=wait("INSTALL_GO.json",deadline);assert approval["intent_sha256"]==sha((R/"intent.json").read_bytes())
    run([sys.executable,"-m","venv","/cache/env"],"venv",deadline)
    py="/cache/env/bin/python"
    run([py,"-m","pip","install","--no-index","--no-deps","--require-hashes","--find-links=/wheels","-r","/inputs/requirements.lock"],"install",deadline)
    # Exactly one actual vendor CLI invocation, no sample/count repair loop.
    run([py,"/vendor/count_request.py","--request","/inputs/request.json","--output","/output/count.json"],"counter",deadline)
    raw=(R/"count.json").read_bytes();assert len(raw)<=8388608;d=json.loads(raw);v=d["result"];assert d["projection"]["full_request_canonical_sha256"]==m["request_sha256"]
    assert type(v["count"]) is int and v["count"]==len(v["tokens"]) and all(type(x) is int for x in v["tokens"])
    assert type(v["under_3000_input_tokens"]) is bool and v["under_3000_input_tokens"]==(v["count"]<3000)
    assert d["provenance"]["served_template_sha256"]==m["served_template_sha256"] and d["provenance"]["counter_version"]=="0.2.1"
    assert d["provenance"]["model"]=="nvidia/Nemotron-3_5-Lightning"
    assert d["provenance"]["verified_model_file_sha256"]=={v["name"]:v["sha256"] for v in m["public_tokenizer"]}
    for key,value in m["root_versions"].items():assert d["provenance"]["runtime_versions"][key]==value
    assert time.monotonic()<=deadline and time.time()<=go["absolute_deadline_utc"]
    emit("verified.json",{"count":v["count"],"strict_under3000":v["under_3000_input_tokens"],"result_sha256":sha(raw),"native_or_model_authority":False,"request_sha256":m["request_sha256"],"lock_sha256":m["lock_sha256"],"source_sha":go["source_sha"],"runtime":m["runtime"]["immutable_image"],"external_once_receipt_sha256":go["external_once_receipt_sha256"],"intent_sha256":approval["intent_sha256"]})
if __name__=="__main__":main()

