"""SOURCE_ONLY103 host Docker launcher; only trusted host code uses daemon."""
import argparse,hashlib,json,os,pathlib,subprocess,time,uuid,signal
from boundary import Output,strict,validate_result,private_record,cleanup_once
def sha(b):return hashlib.sha256(b).hexdigest()
def docker(*args):return subprocess.check_output(["docker",*args],text=True).strip()
def main():
    a=argparse.ArgumentParser();a.add_argument("--manifest",required=True);a.add_argument("--manifest-sha",required=True);a.add_argument("--source-sha",required=True);a.add_argument("--once-receipt-sha",required=True);x=a.parse_args();mf=pathlib.Path(x.manifest);assert sha(mf.read_bytes())==x.manifest_sha;m=json.loads(mf.read_text())
    assert m["admission"]["state"]=="INDEPENDENTLY_ADMITTED" and m["private_ingress"]["state"]=="INDEPENDENTLY_ADMITTED_ENCRYPTED104"
    assert len(x.once_receipt_sha)==64 and all(c in "0123456789abcdef" for c in x.once_receipt_sha)
    root=pathlib.Path(os.environ["RUNNER_TEMP"])/"traceharbor-offline103";kit=mf.parent
    assert os.environ["GITHUB_RUN_ATTEMPT"]=="1" and os.environ["GITHUB_SHA"]==x.source_sha
    for f in [root,root/"wheels",root/"vendor",root/"control",root/"output"]:assert f.is_dir() and not f.is_symlink()
    for w in m["wheels"]:assert sha((root/"wheels"/w["filename"]).read_bytes())==w["sha256"]
    out=root/"output";output=Output(out);assert output.census()==(0,0);os.chmod(out,0o777);control=root/"control";os.chmod(control,0o755)
    sentinel=root.parent/("outside-synthetic-"+uuid.uuid4().hex);sentinel.write_text("SYNTHETIC_NOT_SECRET")
    image=m["runtime"]["immutable_image"];assert "@sha256:" in image
    name="traceharbor-offline103-"+os.environ["GITHUB_RUN_ID"];args=["create","--name",name,"--platform=linux/amd64","--network=none","--read-only","--user=65532:65532","--cap-drop=ALL","--security-opt=no-new-privileges:true","--pids-limit=64","--memory=1g","--memory-swap=1g","--cpus=1","--ulimit=cpu=120:120","--ulimit=nofile=1024:1024","--ulimit=fsize=8388608:8388608","--ipc=private","--workdir=/cache","--tmpfs=/cache:rw,exec,nosuid,nodev,size=512m,uid=65532,gid=65532,mode=700"]
    for src,dst,ro in [(root/"wheels","/wheels",True),(root/"vendor","/vendor",True),(root/"control","/control",True),(out,"/output",False),(kit/"worker.py","/driver/worker.py",True),(kit/"request.json","/inputs/request.json",True),(kit/"requirements.lock","/inputs/requirements.lock",True),(mf,"/inputs/transfer.json",True)]:
        args+=["--mount","type=bind,src="+str(src.resolve())+",dst="+dst+(",readonly" if ro else "")]
    args+=[image,"python","-I","/driver/worker.py"];cid=None;start=time.monotonic();deadline=start+170;absolute=time.time()+170;terminal=None;failure=None;approved=False;intent_raw=None;projection=None;proof_count=None;proof_qualification=None;stage="container-create"
    try:
        docker("pull","--platform=linux/amd64",image);cid=docker(*args);stage="container-start"
        docker("start",cid);pid=int(docker("inspect","-f","{{.State.Pid}}",cid));cg=[line.split(":",2)[2] for line in pathlib.Path(f"/proc/{pid}/cgroup").read_text().splitlines() if line.startswith("0::")];assert len(cg)==1
        cp=(pathlib.Path("/sys/fs/cgroup")/cg[0].lstrip("/")).resolve();assert str(cp).startswith("/sys/fs/cgroup/");cpu=cp/"cpu.stat"
        def usage():return int(dict(line.split() for line in cpu.read_text().splitlines())["usage_usec"])
        assert usage()<=120000000
        with (control/"GO.json").open("x") as f:json.dump({"absolute_deadline_utc":absolute,"host_sentinel":str(sentinel),"external_once_receipt_sha256":x.once_receipt_sha,"source_sha":x.source_sha},f)
        while time.monotonic()<deadline:
            state=json.loads(docker("inspect","-f","{{json .State}}",cid))
            if not state["Running"]:terminal=state;break
            assert usage()<=120000000,"Aggregate CPU120 exceeded"
            output.census();stage="worker-output"
            ready=output.read("qualification.ready",0,optional=True) if not approved else None
            pending_intent=output.read("intent.json",8192) if not approved and ready is not None else None
            pending_q=output.read("qualification.json",8192) if not approved and ready is not None else None
            if pending_intent is not None and pending_q is not None:
                q=strict(pending_q);intent=strict(pending_intent);assert set(q)=={"case1_permitted_read_write","case2_denial","credential_env_present","counter_imported"} and q["case1_permitted_read_write"] is True and q["credential_env_present"] is False and q["counter_imported"] is False and q["case2_denial"]["socket"]==1
                assert intent["request_sha256"]==m["request_sha256"] and intent["lock_sha256"]==m["lock_sha256"] and intent["counter_attempt_reserved"]==1 and intent["external_once_receipt_sha256"]==x.once_receipt_sha
                assert set(intent)=={"request_sha256","lock_sha256","counter_attempt_reserved","external_once_receipt_sha256","source_sha","runtime","absolute_deadline_utc","output_absent"}
                assert intent["source_sha"]==x.source_sha and intent["runtime"]==image and intent["absolute_deadline_utc"]==absolute and intent["output_absent"] is True and type(intent["counter_attempt_reserved"]) is int
                raw=pending_intent;intent_raw=raw;proof_qualification=pending_q
                with (control/"FROZEN_INTENT.json").open("xb") as f:f.write(raw)
                with (control/"INSTALL_GO.json").open("x") as f:json.dump({"intent_sha256":sha(raw)},f)
                approved=True
            output.census()
            time.sleep(.2)
        assert terminal is not None,"Wall180 exceeded"
        stage="public-result-validation"
        assert terminal is not None and not terminal.get("OOMKilled") and terminal["ExitCode"]==0 and approved
        assert time.monotonic()-start<=170 and intent_raw is not None
        output.census();projection=validate_result(output,m,x.source_sha,x.once_receipt_sha,intent_raw,absolute)
        proof_count=output.read("count.json",8388608)
        assert sha(proof_count)==projection["result_sha256"]
    except BaseException as exc:
        failure={"stage":stage,"type":type(exc).__name__,"message":str(exc)[:1024],"utc":time.time(),"monotonic":time.monotonic(),"classification":"UNKNOWN_NO_RETRY"}
        # Preserve primary before ANY cleanup; capture failure never replaces it.
        try:private_record(root,"primary.json",failure)
        except BaseException as capture:failure["primary_capture_failure"]=type(capture).__name__
    finally:
        cleanup=[]
        if cid is not None:
            try:cleanup=cleanup_once(root,cid,terminal)
            except BaseException as exc:cleanup=[{"stage":"cleanup-boundary","type":type(exc).__name__}]
        try:sentinel.unlink(missing_ok=True)
        except BaseException as exc:cleanup.append({"stage":"sentinel-cleanup","type":type(exc).__name__})
        try:output.close()
        except BaseException as exc:cleanup.append({"stage":"output-close","type":type(exc).__name__})
        try:private_record(root,"host-terminal.json",{"primary":failure,"cleanup_failures":cleanup,"container_terminal":terminal,"utc":time.time()})
        except BaseException:pass
    if failure is not None:raise RuntimeError("Original primary preserved: "+failure["stage"]+" / "+failure["type"]+" / UNKNOWN_NO_RETRY")
    if cleanup:raise RuntimeError("Cleanup incomplete; reconcile only")
    assert projection is not None and proof_count is not None and proof_qualification is not None and time.monotonic()-start<=180
    proof=pathlib.Path(os.environ["RUNNER_TEMP"])/"traceharbor-offline105-public-proof";proof.mkdir(mode=0o700)
    assert len(proof_count)+len(proof_qualification)+len(intent_raw)<=900000
    for name,data in [("count.json",proof_count),("qualification.json",proof_qualification),("intent.json",intent_raw)]:
        fd=os.open(proof/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        with os.fdopen(fd,"wb") as f:f.write(data);f.flush();os.fsync(f.fileno())
    private_record(proof,"verified.json",projection)
    private_record(proof,"binding.json",{"source_sha":x.source_sha,"once_receipt_sha256":x.once_receipt_sha,"request_sha256":m["request_sha256"],"lock_sha256":m["lock_sha256"],"runtime":image,"container_terminal":terminal,"cleanup_failures":cleanup})
    assert time.monotonic()-start<=180
    print(json.dumps(projection,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
