"""SOURCE177 PRIVATE REVIEW CANDIDATE: explicit154 only; historical source delegates retained. No admission/effect at import."""
'SOURCE174 closed one-invocation guard. Public output is DATA, no grant.\nOne complete canonical own-self check; no parsed object/callback accepted.\nAll consuming predicates are closed builtin JSON/source-owned pure functions.\nSameFD whole raw/EOF/ALLattrs/path reseal for own,A,config,writer,source at exit.\nNo cross-invocation cache. Historical original152 timeout is never rerun here.\n'
import pathlib, runpy, copy, re, ast, json, os, stat, sys, hashlib, time, resource, importlib.util
ROOT = pathlib.Path(__file__).resolve().parent
from snapshot174 import Whole173, canonical_sha173, self_sha173, _Invocation175
H = runpy.run_path(str(ROOT / 'prestart177.py'))
history154 = H['history154']
binding_selector165 = H['binding_selector165']
derive154 = H['derive154']
ORIGINAL = H['ORIGINAL']
can = H['can']
sha = H['sha']
derive152 = H['old']['derive152']
spec = importlib.util.spec_from_file_location('source174_exact118', ROOT / 'host_transport118.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
E = runpy.run_path(str(ROOT / 'envelope158.py'))
P = runpy.run_path(str(ROOT / 'plan127.py'))

def _validate152(doc, raw, config, static174, opened, version):
    history154 = H['old']['history154']
    binding_selector165 = H['old']['binding_selector165']
    require_plan = False
    payload = None
    _macro122 = None
    match = re.fullmatch('NATIVE152_([A-Z_]+)', doc['state'])
    if match is None or match[1] == 'TERMINAL':
        raise ValueError('No mutation of consumed152')
    selected = binding_selector165(doc, config)
    n = doc[selected['key']]
    direction = n['direction']
    binding = n['records'][0]['payload']['writer_binding']
    if len(direction['id'].encode()) > 256 or not direction['id'].startswith('V29-TRACE-152-') or direction.get('native_admission') is not True or (len(direction['body'].encode()) != direction['bytes']) or (sha(direction['body'].encode()) != direction['sha256']) or (n['records'][0]['phase'] != 'RX_START'):
        raise ValueError('Actual independent152 addressed release required')
    static = static174
    if static is None:
        raise ValueError('Exact static152')
    history154(doc, static, before_RX=False)
    base.validate_transfer_layout(binding)
    if config.get('writer_binding') != binding or binding['direction_number'] != 152 or binding['direction_id'] != direction['id'] or (binding['direction_sha256'] != direction['sha256']) or (binding['direction_bytes'] != direction['bytes']):
        raise ValueError('Immutable actual152 binding')
    root = pathlib.Path(binding['binding_root'])
    rs = root.lstat()
    if root.is_symlink() or not stat.S_ISDIR(rs.st_mode) or rs.st_uid != os.getuid() or rs.st_mode & 63:
        raise ValueError('Actual private152 root')
    original = base.private_regular(binding['original_writer_path'])
    writer = base.private_regular(root / 'admin152.py')
    auditor = pathlib.Path(binding['auditor_path'])
    if binding['writer_path'] != str(writer) or not auditor.is_relative_to(root) or auditor.is_symlink():
        raise ValueError('Original152 writer/A locator')
    source = n['source_verification']['Auditor_V28_checkpoint.json']
    aresource = opened(auditor, 67108864)
    araw = aresource.raw
    audit = base.strict(araw)
    v = dict(audit)
    v['integrity'] = dict(audit['integrity'])
    v['integrity']['canonical_json_sha256'] = None
    if type(binding['auditor_version']) is not int or binding['auditor_version'] != source['version'] or sha(araw) != source['sha256'] or (len(araw) != source['bytes']) or (canonical_sha173(v) != source['self_sha256']) or (audit['integrity']['canonical_json_sha256'] != source['self_sha256']) or (os.getxattr(auditor, 'user.library-file-id').decode() != source['library_file_id']) or (int(os.getxattr(auditor, 'user.library-file-version').decode()) != source['version']):
        raise ValueError('Whole immutable original118 A preserved152')
    boundary = audit['operation']['effect_replay_boundary']
    boundary = base.strict(boundary) if isinstance(boundary, str) else boundary
    if boundary['recipient_outboxes']['TraceHarbor V1'] != direction or doc['guard']['operation_id'] != direction['id']:
        raise ValueError('Actual addressed152 operation')
    if sha(opened(original, 33554432).raw) != ORIGINAL or binding['original_writer_sha256'] != ORIGINAL:
        raise ValueError('Original008f unchanged')
    expected, _ = derive152(opened(original, 33554432).raw.decode(), binding['auditor_version'])
    if opened(writer, 33554432).raw.decode() != expected or sha(opened(writer, 33554432).raw) != binding['writer_sha256']:
        raise ValueError('Exact explicit152/pre151 original derivation')
    result = {'number': 152, 'key': 'native152', 'binding': binding, 'direction': direction, 'original': original, 'writer': writer, 'doc': doc, 'raw': raw}
    if require_plan:
        if _macro122 is None:
            raise ValueError('Only source-owned macro plan152')
        base._check_macro122(_macro122, result, version, payload)
    pass
    return result

def _validate154(doc, raw, config, static174, opened, version):
    require_plan = False
    payload = None
    _macro122 = None
    match = re.fullmatch('NATIVE154_([A-Z_]+)', doc['state'])
    if match is None or match[1] == 'TERMINAL':
        raise ValueError('No mutation of consumed154')
    selected = binding_selector165(doc, config)
    n = doc[selected['key']]
    direction = n['direction']
    binding = n['records'][0]['payload']['writer_binding']
    if len(direction['id'].encode()) > 256 or not direction['id'].startswith('V29-TRACE-154-') or direction.get('native_admission') is not True or (len(direction['body'].encode()) != direction['bytes']) or (sha(direction['body'].encode()) != direction['sha256']) or (n['records'][0]['phase'] != 'RX_START'):
        raise ValueError('Actual independent154 addressed release required')
    static = static174
    if static is None:
        raise ValueError('Exact static154')
    history154(doc, static, before_RX=False)
    base.validate_transfer_layout(binding)
    if config.get('writer_binding') != binding or binding['direction_number'] != 154 or binding['direction_id'] != direction['id'] or (binding['direction_sha256'] != direction['sha256']) or (binding['direction_bytes'] != direction['bytes']):
        raise ValueError('Immutable actual154 binding')
    root = pathlib.Path(binding['binding_root'])
    rs = root.lstat()
    if root.is_symlink() or not stat.S_ISDIR(rs.st_mode) or rs.st_uid != os.getuid() or rs.st_mode & 63:
        raise ValueError('Actual private154 root')
    original = base.private_regular(binding['original_writer_path'])
    writer = base.private_regular(root / 'admin154.py')
    auditor = pathlib.Path(binding['auditor_path'])
    if binding['writer_path'] != str(writer) or not auditor.is_relative_to(root) or auditor.is_symlink():
        raise ValueError('Original154 writer/A locator')
    source = n['source_verification']['Auditor_V28_checkpoint.json']
    aresource = opened(auditor, 67108864)
    araw = aresource.raw
    audit = base.strict(araw)
    v = dict(audit)
    v['integrity'] = dict(audit['integrity'])
    v['integrity']['canonical_json_sha256'] = None
    if type(binding['auditor_version']) is not int or binding['auditor_version'] != source['version'] or sha(araw) != source['sha256'] or (len(araw) != source['bytes']) or (canonical_sha173(v) != source['self_sha256']) or (audit['integrity']['canonical_json_sha256'] != source['self_sha256']) or (os.getxattr(auditor, 'user.library-file-id').decode() != source['library_file_id']) or (int(os.getxattr(auditor, 'user.library-file-version').decode()) != source['version']):
        raise ValueError('Whole immutable original118 A preserved154')
    boundary = audit['operation']['effect_replay_boundary']
    boundary = base.strict(boundary) if isinstance(boundary, str) else boundary
    if boundary['recipient_outboxes']['TraceHarbor V1'] != direction or doc['guard']['operation_id'] != direction['id']:
        raise ValueError('Actual addressed154 operation')
    if sha(opened(original, 33554432).raw) != ORIGINAL or binding['original_writer_sha256'] != ORIGINAL:
        raise ValueError('Original008f unchanged')
    expected, _ = derive154(opened(original, 33554432).raw.decode(), binding['auditor_version'])
    if opened(writer, 33554432).raw.decode() != expected or sha(opened(writer, 33554432).raw) != binding['writer_sha256']:
        raise ValueError('Exact explicit154/pre153 original derivation')
    result = {'number': 154, 'key': 'native154', 'binding': binding, 'direction': direction, 'original': original, 'writer': writer, 'doc': doc, 'raw': raw}
    if require_plan:
        if _macro122 is None:
            raise ValueError('Only source-owned macro plan154')
        base._check_macro122(_macro122, result, version, payload)
    pass
    return result

def current_binding174(path, version, config_path):
    if type(path) is not str or type(version) is not int or type(config_path) is not str or (version < 1):
        raise TypeError('Only exact physical path/version/config; no supplied parsed snapshot, object subclass, hash, proof or callback')
    resources = {}
    directory_set175 = _Invocation175()

    def opened(path, cap):
        key = str(path)
        if key not in resources:
            resources[key] = directory_set175.open175(key, cap)
        elif resources[key].identity[5] > cap:
            raise ValueError('Resource cannot enlarge another role cap')
        return resources[key]
    try:
        own = opened(path, 83886080)
        if own.attrs.get('user.library-file-id') != base.OWN.encode() or own.attrs.get('user.library-file-version') != str(version).encode():
            raise ValueError('Positive expected current own ID/version')
        raw = own.raw
        doc = base.strict(raw)
        E['role158'](doc, base.OWN)
        if self_sha173(doc, base.OWN) != doc['self_sha256']:
            raise ValueError('Complete canonical own self')
        cfgresource = opened(config_path, 33554432)
        if cfgresource.identity[3] & 63:
            raise ValueError('Private static config permissions')
        static = base.strict(cfgresource.raw)
        number = static['prestart154']['direction_number']
        if type(number) is not int or number not in (152, 154):
            raise ValueError('Closed offline152 or prospective154 guard only')
        key = 'native152' if number == 152 else 'native154'
        n = doc[key]
        direction = n['direction']
        binding = n['records'][0]['payload']['writer_binding']
        config = {'direction_number': number, 'writer_binding': binding, 'config_path': config_path}
        if number == 152:
            pass
        elif static['path_roles']['config'] != config_path:
            raise ValueError('Exact source-bound154 config locator')
        mb = opened(ROOT / 'manifest.json', 33554432).raw
        P['release133'](direction, static, mb)
        for source_name, pin in base.strict(mb)['source_files'].items():
            member = pathlib.Path(source_name)
            if member.is_absolute() or '..' in member.parts:
                raise ValueError('Closed source path')
            resource = opened(ROOT.parent / member, 33554432)
            if len(resource.raw) != pin['bytes'] or resource.raw_sha != pin['sha256']:
                raise ValueError('Exact whole source pin before validation completion')
        result = (_validate154 if number == 154 else _validate152)(doc, raw, config, static, opened, version)
        for resource in resources.values():
            resource.reseal173()
        directory_set175.reseal175()
        return result
    finally:
        for resource in resources.values():
            resource.close173()
        directory_set175.close175()

def check174(path, version, config_path):
    r = current_binding174(path, version, config_path)
    return {'schema': 'TRACE177_SOURCE_GUARD_DATA', 'guard': 'PASS', 'current': r['number'], 'writer': r['binding']['writer_sha256'], 'raw_sha256': sha(r['raw']), 'bytes': len(r['raw']), 'native_authority': False}
_previous177 = runpy.run_path(str(ROOT / 'guard174.py'))
_core_binding177 = current_binding174

def current_binding174(path, version, config_path):
    cfg = json.loads(pathlib.Path(config_path).read_bytes())
    return (_core_binding177 if cfg['prestart154']['direction_number'] == 154 else _previous177['current_binding174'])(path, version, config_path)
current_binding177 = current_binding174

def check177(path, version, config_path):
    r = current_binding177(path, version, config_path)
    return {'schema': 'TRACE177_SOURCE_GUARD_DATA', 'guard': 'PASS', 'current': r['number'], 'writer': r['binding']['writer_sha256'], 'raw_sha256': sha(r['raw']), 'bytes': len(r['raw']), 'native_authority': False}
