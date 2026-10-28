"""Trusted private adapter for the exact inspected vendor counter, never inference.
Bundle code/dependencies must be provisioned and hash-pinned before construction.
The application cannot load code, paths, template overrides or counters from HTTP.
"""
import hashlib,json,sys
from pathlib import Path
from release_policy import Refusal,digest,TEMPLATE,REVISION
MANIFEST_SHA256='e3fe4f412b83b3ed8a79f4d7f7b8f200f0c083a5d64f38b0e789a061cebfe1d3' # must be bound to the final inspected manifest at packaging
class VendorCounter:
    def __init__(self,bundle_root):
        root=Path(bundle_root).resolve(strict=True)
        if any(x.is_symlink() for x in (Path(bundle_root),*Path(bundle_root).parents)):raise Refusal('COUNTER_PATH')
        raw=(root/'manifest.json').read_bytes()
        if MANIFEST_SHA256 is None or hashlib.sha256(raw).hexdigest()!=MANIFEST_SHA256:raise Refusal('COUNTER_MANIFEST')
        m=json.loads(raw)
        if m['version']!='0.2.1' or m['public_revision']!=REVISION:raise Refusal('COUNTER_VERSION')
        for name,pin in m['files_sha256'].items():
            path=Path(name)
            if path.is_absolute() or '..' in path.parts or (root/path).is_symlink() or hashlib.sha256((root/path).read_bytes()).hexdigest()!=pin:raise Refusal('COUNTER_ASSET_PIN')
        # No remote code, hub resolution, network or weights. Inspected local vendor
        # modules enforce all four exact dependency versions and both ID paths.
        import importlib.util
        spec=importlib.util.spec_from_file_location('count_chat',root/'count_chat.py');mod=importlib.util.module_from_spec(spec)
        prior=sys.modules.get('count_chat')
        if prior is not None:raise Refusal('COUNTER_MODULE_COLLISION')
        sys.modules['count_chat']=mod;spec.loader.exec_module(mod)
        spec2=importlib.util.spec_from_file_location('traceharbor_vendor_projection46',root/'count_request.py');projection=importlib.util.module_from_spec(spec2);spec2.loader.exec_module(projection)
        self.project=projection.project_request;self.counter=mod.LocalCounter(root/'tokenizer',root/'served_template.jinja')
    def count(self,payload):
        projection=self.project(payload);result=self.counter.count(projection['rendering_input'])
        return {'count':result['count'],'request_sha256':digest(payload),'template_sha256':TEMPLATE,'tokenizer_revision':REVISION}
