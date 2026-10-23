"""SOURCE177 PRIVATE REVIEW CANDIDATE: explicit154 only; historical source delegates retained. No admission/effect at import."""
'SOURCE174 explicit prospective153 contract and original118 derivation.\nSOURCE_ONLY: exact153 contract; registry/mint require independent actual release.\nHistorical149/150/151/152 contracts/behavior delegate unchanged to prestart168.\nPublication is not native admission; historical consumed152 remains refused.\n'
import pathlib, runpy, json, copy, re, ast, hashlib, os, stat
ROOT = pathlib.Path(__file__).resolve().parent
old = runpy.run_path(str(ROOT / 'prestart168.py'))
can = old['can']
sha = old['sha']
ORIGINAL = old['ORIGINAL']
TABLE = {154: {'predecessor': 153, 'predecessor_state': 'NATIVE153_TERMINAL', 'reserved_history': 148}}
SCHEMA = 'TRACE177_PRESTART154_PREDECESSOR153_V1'
parent154 = old['parent154']
ident154 = old['ident154']

def prepare_child154(own, config):
    if config['prestart154']['direction_number'] in (149, 150, 151, 153):
        return old['prepare_child154'](own, config)
    history154(own, config, before_RX=True)
    parent, before = parent154(config['path_roles']['holder_parent'])
    root = parent / 'holder'
    root.mkdir(mode=448, exist_ok=False)
    after = parent.lstat()
    child = root.lstat()
    if ident154(before) != ident154(after) or root.resolve() != root or root.is_symlink() or (not stat.S_ISDIR(child.st_mode)) or (child.st_uid != os.getuid()) or (stat.S_IMODE(child.st_mode) != 448) or list(root.iterdir()):
        raise ValueError('Exclusive child drift; preserve attempt no adoption')
    return receipt_from_identities178(config, str(parent), ident154(before), ident154(child))

def check_child154(receipt, config, *, empty=True):
    if config['prestart154']['direction_number'] in (149, 150, 151, 153):
        return old['check_child154'](receipt, config, empty=empty)
    if type(receipt) is not dict or set(receipt) != {'schema', 'direction_number', 'predecessor', 'reserved_history', 'parent_path', 'parent', 'child_path', 'child', 'expected_empty', 'native_authority'} or receipt['schema'] != SCHEMA or (receipt['direction_number'] != 154) or (receipt['predecessor'] != 153) or (receipt['reserved_history'] != 148) or (receipt['native_authority'] is not False) or (receipt['expected_empty'] is not True):
        raise ValueError('Exact154/pre153 prepared child receipt')
    parent, ps = parent154(config['path_roles']['holder_parent'])
    root = parent / 'holder'
    if receipt['parent_path'] != str(parent) or receipt['child_path'] != str(root) or receipt['parent'] != ident154(ps) or (root.resolve() != root) or root.is_symlink():
        raise ValueError('Frozen parent/child alias or identity drift')
    child = root.lstat()
    if not stat.S_ISDIR(child.st_mode) or ident154(child) != receipt['child'] or child.st_uid != os.getuid() or (stat.S_IMODE(child.st_mode) != 448) or (empty and list(root.iterdir())):
        raise ValueError('Frozen child identity/mode/empty drift')
    return {'schema': SCHEMA, 'prepared_receipt_sha256': sha(can(receipt)), 'child_path': str(root), 'child': ident154(child), 'empty': empty, 'native_authority': False}

def current_prestart154(own, config, *, empty=True):
    if config['prestart154']['direction_number'] in (149, 150, 151, 153):
        return old['current_prestart154'](own, config, empty=empty)
    history154(own, config, before_RX=False)
    return check_child154(own['native154']['records'][0]['payload']['holder_preparation154'], config, empty=empty)

def consume_child154(receipt, config):
    if config['prestart154']['direction_number'] in (149, 150, 151, 153):
        return old['consume_child154'](receipt, config)
    check_child154(receipt, config, empty=True)
    parent, _ = parent154(config['path_roles']['holder_parent'])
    root = parent / 'holder'
    pfd = fd = None
    try:
        pfd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        fd = os.open('holder', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=pfd)
        if ident154(os.fstat(pfd)) != receipt['parent'] or ident154(os.fstat(fd)) != receipt['child'] or os.listdir(fd):
            raise ValueError('Frozen154 nofollow consumption identity')
        os.mkdir('originals', 448, dir_fd=fd)
        os.fsync(fd)
        if ident154(parent.lstat()) != receipt['parent'] or ident154(root.lstat()) != receipt['child']:
            raise ValueError('Consumption moved; no clock')
        return root
    finally:
        if fd is not None:
            os.close(fd)
        if pfd is not None:
            os.close(pfd)

def binding_selector165(doc, config):
    if type(config) is not dict or type(config.get('direction_number')) is not int or config['direction_number'] != 154:
        raise ValueError('Closed154 selector')
    match = re.fullmatch('NATIVE154_([A-Z_]+)', doc.get('state', ''))
    if match is None or match[1] == 'TERMINAL' or type(doc.get('native154')) is not dict:
        raise ValueError('No consumed/foreign154 selector')
    n = doc['native154']
    if not n.get('records') or n['records'][0].get('phase') != 'RX_START':
        raise ValueError('Actual first154 RX selector required')
    return {'number': 154, 'key': 'native154'}

def current_binding154(base, path, version, config, require_plan=False, payload=None, _macro122=None):
    if config.get('direction_number') != 154:
        return old['current_binding154'](base, path, version, config, require_plan=require_plan, payload=payload, _macro122=_macro122)
    from guard177 import current_binding174
    result = current_binding174(str(path), version, config['config_path'])
    if result['binding'] != config.get('writer_binding'):
        raise ValueError('Exact source-derived154 writer binding')
    if require_plan:
        if _macro122 is None:
            raise ValueError('Only source-owned154 macro plan')
        base._check_macro122(_macro122, result, version, payload)
    return result
_previous177 = runpy.run_path(str(ROOT / 'prestart174.py'))

def contract154(value):
    if type(value) is not dict or type(value.get('direction_number')) is not int:
        raise TypeError('Closed integer direction')
    if value['direction_number'] != 154:
        return _previous177['contract154'](value)
    expected = {'schema': 'TRACE177_PRESTART154_PREDECESSOR153_V1', 'direction_number': 154, 'predecessor': 153, 'predecessor_state': 'NATIVE153_TERMINAL', 'reserved_history': 148, 'creation': 'EXCLUSIVE_EMPTY_0700_BEFORE_FIRST_RX_AND_REGISTRY', 'consumption': 'FROZEN_PARENT_CHILD_DEV_INO_UID_MODE_NO_ALIAS_BEFORE_CLOCK'}
    pins = ('predecessor153_sha256', 'preserved152_sha256', 'preserved151_sha256', 'preserved150_sha256', 'preserved149_sha256', 'reserved148_sha256')
    if set(value) != set(expected) | set(pins) or any((type(value[k]) is not type(v) or value[k] != v for k, v in expected.items())) or any((type(value[k]) is not str or re.fullmatch('[a-f0-9]{64}', value[k]) is None for k in pins)):
        raise ValueError('Explicit154 exact153 predecessor and complete older pins')
    return copy.deepcopy(value)

def history154(own, config, *, before_RX):
    c = contract154(config['prestart154'])
    if c['direction_number'] != 154:
        return _previous177['history154'](own, config, before_RX=before_RX)
    if own.get('native_id') != '6acfe37b-828c-83eb-b466-7670beb64ff2' or own.get('ownership', {}).get('owner') != 'TraceHarbor V1' or type(own['ownership'].get('duplicate_trace_route_owners')) is not int or (own['ownership']['duplicate_trace_route_owners'] != 0):
        raise ValueError('Exact sole existing Trace')
    for slot, key in ((153, 'predecessor153_sha256'), (152, 'preserved152_sha256'), (151, 'preserved151_sha256'), (150, 'preserved150_sha256'), (149, 'preserved149_sha256'), (148, 'reserved148_sha256')):
        if sha(can(own.get('native' + str(slot)))) != c[key]:
            raise ValueError('Whole immutable predecessor/history mismatch')
    if own['native153'].get('phase') != 'TERMINAL':
        raise ValueError('Actual153 terminal predecessor required')
    if before_RX:
        if own.get('state') != 'NATIVE153_TERMINAL' or 'native154' in own:
            raise ValueError('Unused154 only; consumed153 remains immutable')
    elif not own.get('state', '').startswith('NATIVE154_') or not own.get('native154', {}).get('records') or own['native154']['records'][0].get('phase') != 'RX_START':
        raise ValueError('Explicit154 RX lineage')
    return c

def _dispatch177(name, core):

    def call(*args, **kw):
        cfg = args[1] if name in ('prepare_child154', 'check_child154', 'consume_child154', 'current_prestart154', 'binding_selector165') else args[3]
        number = cfg.get('prestart154', cfg).get('direction_number')
        return (core if number == 154 else _previous177[name])(*args, **kw)
    return call
for _name in ('prepare_child154', 'check_child154', 'consume_child154', 'current_prestart154', 'binding_selector165', 'current_binding154'):
    globals()[_name] = _dispatch177(_name, globals()[_name])

def derive154(original, auditor_version):
    if type(original) is not str or len(original.encode()) != 3827 or sha(original.encode()) != ORIGINAL or (type(auditor_version) is not int) or (auditor_version <= 0):
        raise ValueError('Exact008f and actual future positive AuditorA')
    pairs = [('direction118.json', 'direction154.json'), ("'native118.records'", "'native154.records'"), ("'native118'", "'native154'"), ("'NATIVE117_TERMINAL'", "'NATIVE153_TERMINAL'"), ("'NATIVE118_'", "'NATIVE154_'"), ('CURRENT Auditor858 direction118', 'CURRENT Auditor' + str(auditor_version) + ' direction154')]
    out = original
    rows = []
    for before, after in pairs:
        count = out.count(before)
        if not count:
            raise ValueError('Missing original six-substitution token')
        out = out.replace(before, after)
        rows.append({'before': before, 'after': after, 'occurrences': count})
    inverse = out
    for before, after in reversed(pairs):
        inverse = inverse.replace(after, before)
    if inverse != original or '118' in out:
        raise ValueError('Whole exact six-substitution inverse')
    ast.parse(out)
    return (out, rows)


def receipt_from_identities178(config, parent_path, parent_identity, child_identity):
    """Pure data construction shared by actual producer and DATA_ONLY tests.
    This creates no directory, capability, admission or registry entry.
    Actual prepare_child154 performs all filesystem checks before this call.
    """
    c = contract154(config['prestart154'])
    if c['direction_number'] != 154 or parent_path != config['path_roles']['holder_parent']:
        raise ValueError('Exact154 producer contract and bound parent')
    for ident in (parent_identity, child_identity):
        if type(ident) is not dict or set(ident) != {'dev','ino','uid','mode','type'} or ident['type'] != 'directory' or ident['mode'] != 448 or any(type(ident[k]) is not int or ident[k] < 0 for k in ('dev','ino','uid','mode')):
            raise ValueError('Whole exact directory identities; data alone grants nothing')
    return {'schema': c['schema'], 'direction_number': c['direction_number'], 'predecessor': c['predecessor'], 'reserved_history': c['reserved_history'], 'parent_path': parent_path, 'parent': copy.deepcopy(parent_identity), 'child_path': str(pathlib.Path(parent_path)/'holder'), 'child': copy.deepcopy(child_identity), 'expected_empty': True, 'native_authority': False}
