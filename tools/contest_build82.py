"""Reproducible, allowlisted offline contest build. Python 3.12, stdlib only."""
import argparse
import csv
import hashlib
import importlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import selectors
import stat
import subprocess
import sys
import time
import zipfile

BASE_COMMIT = '30caddc4c730d2fef98524f67b431fa56e3daa2c'
BASE_TREE = '639b972e8e590c9dc0faff531b11607e985de394'
LIMIT = 524288
FILES = (
    'LICENSE', 'README.md', 'START_HERE.md', 'SCHEMAS.md',
    'app.py', 'core.py', 'service.py', 'live_service.py', 'nebius.py',
    'adapters.py', 'verifier.py', 'live_probe.py',
    'input.schema.json', 'output.schema.json',
    'web/index.html', 'web/app.js', 'web/style.css',
    'fixtures/complete.json', 'fixtures/missing.json', 'fixtures/contradictory.json',
    'references/expectations.json',
    'tools/contest_build82.py', 'docs/CONTEST_BUILD82.md',
    'workflow_candidates/traceharbor-contest-build82.yml.disabled',
)
CASE = {
    'schema': 'traceharbor.input.v1', 'synthetic': True,
    'case_id': 'contest82-unknown-20261017-c0a2f7',
    'title': 'New isolated contest-build packaging observation',
    'sources': [
        {'id': 'harbor82', 'kind': 'log', 'title': 'Synthetic dispatch receipt',
         'events': [{'id': 'receipt82', 'text': 'Synthetic job harbor82 completed with an unexplained amber status.',
                     'timestamp': '2031-02-19T08:17:00Z'}]},
        {'id': 'metric82', 'kind': 'metric', 'title': 'Synthetic independent sample',
         'events': [{'id': 'sample82', 'text': 'Synthetic amber counter is 7; no causal configuration evidence is supplied.',
                     'timestamp': '2031-02-19T08:17:01Z'}]},
    ],
}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_name(name):
    p = PurePosixPath(name)
    if str(p) != name or p.is_absolute() or any(x in ('', '.', '..') for x in p.parts) or '\\' in name:
        raise ValueError('Unsafe build member')
    return p


def source_bytes(root, name):
    p = root
    for part in safe_name(name).parts:
        p = p / part
        if p.is_symlink():
            raise ValueError('Symlink source refused')
    st = p.stat()
    if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or st.st_size > LIMIT:
        raise ValueError('Source type or size refused')
    data = p.read_bytes()
    after = p.stat()
    identity = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns,
                          s.st_ctime_ns, s.st_mode, s.st_nlink)
    if len(data) != st.st_size or identity(after) != identity(st):
        raise ValueError('Source changed during read')
    return data


def build(root, output):
    root = root.absolute()
    if root.is_symlink() or not root.is_dir() or output.exists() or output.is_symlink():
        raise ValueError('Fresh output and owned source required')
    payload = {name: source_bytes(root, name) for name in FILES}
    pins = {name: {'bytes': len(data), 'sha256': sha(data)} for name, data in payload.items()}
    payload['BUILD82.json'] = canonical({
        'schema': 'traceharbor.contest-build82.v1', 'repository': 'Elinfiny/TraceHarbor',
        'baseline_commit': BASE_COMMIT, 'baseline_tree': BASE_TREE,
        'scope': 'DEMO_NO_AI; real NVIDIA through Nebius integration still required',
        'runtime': 'CPython 3.12; stdlib; verified platform recorded in smoke receipt',
        'new_paths': [n for n in FILES if n.startswith(('tools/', 'docs/', 'workflow_candidates/'))],
        'source_pins': pins, 'fixture_sha256': sha(canonical(CASE)),
        'excluded': 'credentials/env/admissions/databases/state/logs/cache/native qualification/reference dossier history',
        'baseline_note': 'Existing product bytes pinned to baseline; three new files are review overlay, not merged main',
    }) + b'\n'
    manifest = io.StringIO(newline='')
    writer = csv.writer(manifest, lineterminator='\n')
    writer.writerow(['path', 'bytes', 'sha256'])
    for name, data in sorted(payload.items()):
        writer.writerow([name, len(data), sha(data)])
    payload['MANIFEST.csv'] = manifest.getvalue().encode()
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_STORED) as archive:
        for name, data in sorted(payload.items()):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, data)
    raw = stream.getvalue()
    if len(raw) > LIMIT:
        raise ValueError('Build compressed size bound')
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as out:
        out.write(raw)
        out.flush()
        os.fsync(out.fileno())
    return {'status': 'BUILT_DEMO_ONLY', 'bytes': len(raw), 'sha256': sha(raw),
            'members': len(payload), 'source_files': len(FILES), 'compression': 'STORED_FIXED_METADATA'}


def smoke(archive_path, work):
    start = time.monotonic()
    deadline = start + 90
    if work.exists() or work.is_symlink():
        raise ValueError('Smoke root must be absent; no retry')
    work.mkdir(mode=0o700)
    root = work / 'clean'
    root.mkdir(mode=0o700)
    receipt = {'case_id': CASE['case_id'], 'pre_invoke_monotonic': None,
               'child_limit_seconds': 30, 'parent_deadline': deadline,
               'status': 'ATTEMPT_CONSUMED_NO_RETRY', 'provider_calls': 0}
    (work / 'ATTEMPT.json').write_bytes(canonical(receipt))
    primary = None
    cleanup_errors = []
    child = None
    stdout = bytearray()
    stderr = bytearray()
    try:
        raw = archive_path.read_bytes()
        if len(raw) > LIMIT:
            raise ValueError('Archive bound')
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            members = archive.infolist()
            if len(members) != len(FILES) + 2 or len({m.filename for m in members}) != len(members):
                raise ValueError('Unexpected members')
            data = {}
            for m in members:
                safe_name(m.filename)
                if m.filename not in set(FILES) | {'BUILD82.json', 'MANIFEST.csv'} or m.file_size > LIMIT or m.compress_type != zipfile.ZIP_STORED or stat.S_IFMT(m.external_attr >> 16) != stat.S_IFREG:
                    raise ValueError('Member policy')
                data[m.filename] = archive.read(m)  # EOF/CRC before extraction
                if time.monotonic() >= deadline - 10:
                    raise TimeoutError('Parent extraction deadline')
            rows = list(csv.DictReader(io.StringIO(data['MANIFEST.csv'].decode())))
            if len(rows) != len(data)-1 or len({r['path'] for r in rows}) != len(rows):
                raise ValueError('Manifest coverage')
            if {r['path'] for r in rows} != set(data)-{'MANIFEST.csv'}:
                raise ValueError('Manifest members')
            for row in rows:
                if int(row['bytes']) != len(data[row['path']]) or row['sha256'] != sha(data[row['path']]):
                    raise ValueError('Manifest hash')
            for name, body in data.items():
                f = root / name
                f.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
                fd = os.open(f, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                with os.fdopen(fd, 'wb') as output:
                    output.write(body)
        fixture = work / 'fresh-unknown82.json'
        fixture.write_bytes(canonical(CASE))
        fixture.chmod(0o600)
        output = work / 'dossier82.json'
        if output.exists():
            raise ValueError('Output already exists')
        command = [sys.executable, '-B', str(root/'app.py'), 'analyze', str(fixture), '--out', str(output)]
        env = {'PATH': os.defpath, 'PYTHONDONTWRITEBYTECODE': '1', 'LANG': 'C.UTF-8'}
        receipt.update({'command': command, 'fixture_sha256': sha(fixture.read_bytes()),
                        'archive_sha256': sha(raw), 'pre_invoke_monotonic': time.monotonic()})
        (work/'PRE_INVOKE.json').write_bytes(canonical(receipt))
        child = subprocess.Popen(command, cwd=root, env=env, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, umask=0o077)
        child_deadline = min(time.monotonic()+30, deadline-10)
        with selectors.DefaultSelector() as selector:
            selector.register(child.stdout, selectors.EVENT_READ, stdout)
            selector.register(child.stderr, selectors.EVENT_READ, stderr)
            while selector.get_map():
                if time.monotonic() >= child_deadline:
                    raise TimeoutError('Child deadline')
                for key, _ in selector.select(timeout=min(0.1, child_deadline-time.monotonic())):
                    block = os.read(key.fd, 16384)
                    if not block:
                        selector.unregister(key.fileobj)
                    else:
                        key.data.extend(block)
                        if len(key.data) > 131072:
                            raise ValueError('Channel bound')
        child.wait(timeout=max(0.01, child_deadline-time.monotonic()))
        receipt['post_return_monotonic'] = time.monotonic()
        receipt['returncode'] = child.returncode
        # Retain original channels and response before any success guards.
        (work/'stdout.bin').write_bytes(stdout)
        (work/'stderr.bin').write_bytes(stderr)
        (work/'RETURN.json').write_bytes(canonical(receipt))
        if output.exists():
            original = output.read_bytes()
            (work/'dossier-original.json').write_bytes(original)
        else:
            raise ValueError('No dossier output')
        if child.returncode != 0 or stderr or len(original) > 131072:
            raise ValueError('CLI failed or output bound')
        if stat.S_IMODE(output.stat().st_mode) != 0o600:
            raise ValueError('Output permissions')
        sys.path.insert(0, str(root))
        live_service = importlib.import_module('live_service')
        core = importlib.import_module('core')
        dossier = json.loads(original)
        restored = live_service.verify_import(json.loads(json.dumps(dossier)))
        if restored != dossier or dossier['mode'] != 'DEMO_NO_AI' or dossier['analysis']['status'] != 'unknown' or dossier['analysis']['hypotheses'] or dossier['analysis']['remediation']:
            raise ValueError('Abstention or roundtrip failed')
        ev = dossier['evidence']
        if ev['case_id'] != CASE['case_id'] or ev['input_sha256'] != sha(fixture.read_bytes()):
            raise ValueError('Input association')
        if [s['raw'] for s in ev['sources']] != CASE['sources'] or any(s['sha256'] != core.digest(s['raw']) for s in ev['sources']):
            raise ValueError('Source association')
        if any(n in sys.modules for n in ('jwt', 'cryptography', 'cffi', 'pycparser')):
            raise ValueError('Optional crypto imported into offline route')
        if time.monotonic() >= deadline-10:
            raise TimeoutError('Verification deadline')
        receipt.update({'status': 'PASS_CLEAN_PACKAGED_CLI_UNKNOWN_ABSTENTION_ROUNDTRIP',
                        'dossier_bytes': len(original), 'dossier_sha256': sha(original),
                        'citation_integrity': dossier['verification']['citation_integrity'],
                        'semantic_reference': dossier['verification']['semantic_reference'],
                        'source_association': 'PASS', 'output_mode': '0600',
                        'optional_crypto_imports': [], 'python': sys.version,
                        'platform': sys.platform, 'actual_cli_invocations': 1})
    except BaseException as exc:
        primary = type(exc).__name__ + ': ' + str(exc)
    finally:
        if child is not None:
            try:
                if child.poll() is None:
                    child.kill()
                child.wait(timeout=min(3, max(0.01, deadline-time.monotonic())))
                child.stdout.close()
                child.stderr.close()
            except BaseException as exc:
                cleanup_errors.append(type(exc).__name__)
        (work/'stdout.bin').write_bytes(stdout)
        (work/'stderr.bin').write_bytes(stderr)
        receipt.update({'primary_error': primary, 'cleanup_errors': cleanup_errors,
                        'elapsed_seconds': time.monotonic()-start,
                        'stdout_bytes': len(stdout), 'stderr_bytes': len(stderr),
                        'retention': 'Owned isolated root retained for exact review, no background process'})
        if primary or cleanup_errors:
            receipt['status'] = 'FAILED_CONSUMED_NO_RETRY'
        (work/'smoke82-receipt.json').write_bytes(canonical(receipt)+b'\n')
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    b = sub.add_parser('build')
    b.add_argument('--source-root', type=Path, default=Path(__file__).resolve().parents[1])
    b.add_argument('--out', required=True, type=Path)
    s = sub.add_parser('smoke')
    s.add_argument('--build', required=True, type=Path)
    s.add_argument('--work-root', required=True, type=Path)
    args = parser.parse_args()
    result = build(args.source_root, args.out) if args.command == 'build' else smoke(args.build.absolute(), args.work_root.absolute())
    print(json.dumps(result, sort_keys=True))
    return 0 if result['status'] in ('BUILT_DEMO_ONLY', 'PASS_CLEAN_PACKAGED_CLI_UNKNOWN_ABSTENTION_ROUNDTRIP') else 2


if __name__ == '__main__':
    raise SystemExit(main())
