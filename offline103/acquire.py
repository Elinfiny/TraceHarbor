"""Source-only103 host DATA acquisition. Never imports downloaded modules."""
import argparse, hashlib, json, os, pathlib, subprocess, urllib.request, urllib.parse, zipfile, time
ACQUISITION_DEADLINE=None
def acquisition_deadline135(start_mono,start_wall,maximum,expires,reserve=680):
    import math
    if type(maximum) is not int or not 1<=maximum<=60 or type(expires) is not int or reserve!=680 or not all(math.isfinite(x) for x in (start_mono,start_wall)):raise ValueError('Original bounded public acquisition/reserve')
    end=min(start_mono+maximum,start_mono+(expires-start_wall-reserve))
    if end<=start_mono:raise TimeoutError('Public acquisition cannot consume protected680 reserve')
    return end

def digest(b): return hashlib.sha256(b).hexdigest()
def get(url, cap):
    assert urllib.parse.urlsplit(url).scheme=="https"
    assert urllib.parse.urlsplit(url).hostname in {"files.pythonhosted.org","huggingface.co"}
    class CheckedRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,req,fp,code,msg,headers,newurl):
            h=urllib.parse.urlsplit(newurl).hostname
            assert urllib.parse.urlsplit(newurl).scheme=="https" and (h=="files.pythonhosted.org" or h=="huggingface.co" or h.endswith(".hf.co") or h.endswith(".huggingface.co"))
            return super().redirect_request(req,fp,code,msg,headers,newurl)
    with urllib.request.build_opener(CheckedRedirect).open(url, timeout=min(30,max(.1,ACQUISITION_DEADLINE-time.monotonic()))) as r:
        b=r.read(cap+1); assert len(b)<=cap and time.monotonic()<ACQUISITION_DEADLINE
        final=urllib.parse.urlsplit(r.url).hostname
        assert final=="files.pythonhosted.org" or final=="huggingface.co" or final.endswith(".hf.co") or final.endswith(".huggingface.co")
    return b
def main():
    global ACQUISITION_DEADLINE
    original_mono=time.monotonic();original_wall=time.time();ACQUISITION_DEADLINE=original_mono+180
    a=argparse.ArgumentParser(); a.add_argument("--manifest",required=True); a.add_argument("--manifest-sha",required=True); a.add_argument("--source-sha",required=True); a.add_argument("--public-only",action="store_true"); a.add_argument("--maximum-seconds135",type=int);a.add_argument("--once-expires-utc135",type=int);x=a.parse_args()
    if x.maximum_seconds135 is not None:
        assert x.public_only, "Bounded135 preparation is public DATA only"
        ACQUISITION_DEADLINE=acquisition_deadline135(original_mono,original_wall,x.maximum_seconds135,x.once_expires_utc135)
    mf=pathlib.Path(x.manifest); raw=mf.read_bytes(); assert digest(raw)==x.manifest_sha
    m=json.loads(raw); assert subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()==x.source_sha
    assert os.environ["GITHUB_SHA"]==x.source_sha and os.environ["GITHUB_WORKFLOW_SHA"]==x.source_sha and os.environ["GITHUB_RUN_ATTEMPT"]=="1"
    assert os.environ["GITHUB_REPOSITORY"]=="Elinfiny/TraceHarbor" and os.environ["GITHUB_REPOSITORY_ID"]=="1391430317"
    assert os.environ["GITHUB_EVENT_NAME"]=="workflow_dispatch" and os.environ["GITHUB_ACTOR_ID"]=="273768139"
    kit=mf.parent
    for name,pin in m["source_files"].items(): assert digest((kit.parent/name).read_bytes())==pin
    assert digest((kit/"request.json").read_bytes())==m["request_sha256"]
    assert digest((kit/"requirements.lock").read_bytes())==m["lock_sha256"]
    if not x.public_only:
        assert m["private_ingress"]["state"]=="INDEPENDENTLY_ADMITTED_ENCRYPTED104", "Private counter/template ingress unbound; no download or worker"
        assert m["admission"]["state"]=="INDEPENDENTLY_ADMITTED", "No execution admission"
    root=pathlib.Path(os.environ["RUNNER_TEMP"])/"traceharbor-offline103"; root.mkdir(mode=0o700)
    for name in ["wheels","vendor","control","output"]: (root/name).mkdir(mode=0o700)
    total=0
    for w in m["wheels"]:
        b=get(w["url"],w["bytes"]); assert len(b)==w["bytes"] and digest(b)==w["sha256"]; total+=len(b); assert total<=134217728
        with (root/"wheels"/w["filename"]).open("xb") as out: out.write(b)
        with zipfile.ZipFile(root/"wheels"/w["filename"]) as z:
            assert z.testzip() is None
            for n in z.namelist(): assert ".." not in pathlib.PurePosixPath(n).parts and not n.startswith("/") and not n.endswith(".pth")
    (root/"vendor"/"tokenizer").mkdir()
    for v in m["public_tokenizer"]:
        b=get(v["url"],v["bytes"]); assert len(b)==v["bytes"] and digest(b)==v["sha256"]
        with (root/"vendor"/"tokenizer"/v["name"]).open("xb") as out: out.write(b)
    v=m["public_license"]; b=get(v["url"],v["bytes"]); assert len(b)==v["bytes"] and digest(b)==v["sha256"]
    with (root/"vendor"/"LICENSE.NVIDIA").open("xb") as out: out.write(b)
    if x.public_only:
        (root/"control"/"PUBLIC_DATA_ONLY.json").write_text(json.dumps({"worker_ready":False,"private_ingress":m["private_ingress"]["state"]})); return
    # Input transport is never guessed or encoded in dispatch. Only an independently
    # reviewed existing authenticated ingress may populate this exact private path.
    ingress=pathlib.Path(os.environ["RUNNER_TEMP"])/"traceharbor-reviewed-private-ingress"
    assert ingress.is_dir() and not ingress.is_symlink()
    receipt=pathlib.Path(os.environ["RUNNER_TEMP"])/"traceharbor-private104"/"receipt.json"
    assert receipt.is_file() and not receipt.is_symlink()
    for v in m["private_members"]:
        f=ingress/v["name"]; assert f.is_file() and not f.is_symlink(); b=f.read_bytes(); assert len(b)==v["bytes"] and digest(b)==v["sha256"]
        with (root/"vendor"/v["name"]).open("xb") as out: out.write(b)
    for d in [root/"vendor",root/"vendor"/"tokenizer",root/"wheels"]:
        os.chmod(d,0o555)
        for f in d.iterdir():
            if f.is_file():os.chmod(f,0o444)
if __name__=="__main__": main()

