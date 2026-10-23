"""PRIVATE SOURCE179 current whole-four metadata proof, never native authority.
Reuse exact accepted role/attrs/tuple predicates plus accepted snapshot174
canonical algorithm. Keep full raw EOF and all FD/ancestor seals. No cache,
proof override, callback, alternate transport or omitted metadata file.
"""
from pathlib import Path
import json,runpy,hashlib,time,sys,os
ROOT=Path(__file__).resolve().parent
import snapshot174 as S
assert Path(S.__file__).resolve()==ROOT/'snapshot174.py'
E=runpy.run_path(str(ROOT/'envelope158.py'))
OWN=E['OWN'];IDS={OWN,'libfile_f87a6a307f70819194e0af0fa453afd1','libfile_6f69ae483b088191a1fffefca617bbd5','libfile_8377022600088191993dc06bfba93b7b'}
def proof180(path,transfer,*,original):
    stages=[];start=time.monotonic()
    stable=E['attributes158'](Path(path),transfer)
    if type(original)is not dict or original.get('isError')or type(original.get('structuredContent'))is not dict:raise ValueError('Successful intact actual four original required')
    result=original['structuredContent'];result=result.get('result',result);ts=result.get('transfers')
    if type(ts)is not list or len(ts)!=4 or result.get('unavailable_items')or {t.get('library_file_id')for t in ts if type(t)is dict}!=IDS or not any(t is transfer for t in ts):raise ValueError('Whole exact original member identity, not copied proof')
    if any(type(t.get('current_version_number'))is not int or t['current_version_number']<=0 for t in ts):raise ValueError('Actual positive current provider versions')
    if str(Path(path))!=transfer['workspace_path']:raise ValueError('Current metadata uses its exact returned path; not private A copy')
    resource=S.Whole173(path,83886080 if stable==OWN else 67108864)
    stages.append({'stage':'physical_full_EOF_rawhash_ALLattrs_ancestor_open','role':stable,'elapsed_s':time.monotonic()-start})
    try:
        if len(resource.raw)!=transfer['size_bytes']:raise ValueError('Whole exact returned size')
        start=time.monotonic();doc=json.loads(resource.raw);E['role158'](doc,stable);stages.append({'stage':'whole_json_parse_role','role':stable,'elapsed_s':time.monotonic()-start})
        start=time.monotonic();expected=doc['integrity']['canonical_json_sha256']if stable=='libfile_f87a6a307f70819194e0af0fa453afd1'else doc['self_sha256']
        if S.self_sha173(doc,stable)!=expected:raise ValueError('Whole canonical self hash')
        stages.append({'stage':'whole_exact_snapshot174_canonical_self','role':stable,'elapsed_s':time.monotonic()-start})
        start=time.monotonic();E['attributes158'](Path(path),transfer);resource.reseal173();stages.append({'stage':'post_consumer_whole_sameFD_raw_EOF_ALLattrs_ancestors','role':stable,'elapsed_s':time.monotonic()-start})
        return doc,{'library_file_id':stable,'file_id':transfer['file_id'],'version':transfer['current_version_number'],'bytes':len(resource.raw),'sha256':resource.raw_sha,'self_sha256':expected,'ALLattrs':'PASS'},stages
    finally:resource.close173()
class SourceFreeze180:
    """One physical invocation, complete source and manifest retained to last consumer."""
    def __init__(self):
        self.resources=[];self.pool=S._Invocation175()
        try:
            mf=self.pool.open175(str(ROOT/'manifest.json'),33554432);self.resources.append(mf);m=json.loads(mf.raw)
            if m.get('source_freeze180')!={'schema':'TRACE180_COMPLETE_CURRENT_SOURCE_FREEZE_V1','self_exclusion':'ONLY_diagnostic108/manifest.json','historical179':'PRESERVED_NOT_EXECUTED_IN_180_TREE','native_authority':False}:raise ValueError('Closed current acyclic source180 regime')
            if type(m.get('source_files'))is not dict:raise ValueError('Complete current source180 pins')
            pins=m['source_files']
            for name,pin in pins.items():
                p=Path(name)
                if p.is_absolute()or'..'in p.parts or set(pin)!={'bytes','sha256'}:raise ValueError('Closed complete source member')
                f=self.pool.open175(str(ROOT.parent/p),33554432);self.resources.append(f)
                if len(f.raw)!=pin['bytes']or f.raw_sha!=pin['sha256']:raise ValueError('Whole exact frozen source pin')
            actual={str(p.relative_to(ROOT.parent))for p in ROOT.parent.rglob('*')if p.is_file()and'__pycache__'not in p.parts and p!=ROOT/'manifest.json'}
            if set(pins)!=actual:raise ValueError('No omitted or undeclared source payload')
        except BaseException:self.close180();raise
    def finish180(self):
        for f in self.resources:f.reseal173()
        self.pool.reseal175()
    def close180(self):
        for f in reversed(self.resources):f.close173()
        self.resources=[];self.pool.close175()
