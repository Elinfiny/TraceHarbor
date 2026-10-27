#!/usr/bin/env python3
"""Build the pinned TraceHarbor 175 offline subset; Python 3.12+ stdlib only."""
import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import sys
import zipfile

SOURCE_COMMIT = 'a999b347e9efa3296d02e255e6741a474853bff0'
SOURCE_TREE = '4fae2da1170f30f585a1afcb598717abe103cd1f'
PINS = {'LICENSE': {'blob': '5fd6e0433878a3202ffe231344b0e8fabd4fe6fb',
             'bytes': 1081,
             'mode': '100644',
             'sha256': '2b7b8c54f44d0332b027baf0d0c8df4042d315516645266649bdb355a218004b'},
 'README.md': {'blob': '8079fdba94990ddc62437167604b000aa8292cb5',
               'bytes': 9809,
               'mode': '100644',
               'sha256': '865e934f9021700b7405d8dbabc6676a574f35489f6b11f01b7e68b0b8928ff5'},
 'VIDEO_SCRIPT.md': {'blob': '029aa133a8298997ea4dcc3f58bbdb4abc0b223c',
                     'bytes': 2151,
                     'mode': '100644',
                     'sha256': '6797c070b763f17b5a49dd779140fa210c6b89fa8b866ec2982163a835523d52'},
 'adapters.py': {'blob': '30943982158a0fe376682ad3362b8cc8c4d9a5bc',
                 'bytes': 4015,
                 'mode': '100644',
                 'sha256': '8f43a7277cd68d19eeba081b1ba2d9370ae608e6b3a332d0246d2b0969e08cd1'},
 'app.py': {'blob': '03987f0d2e1c770dd74e5058ee5a36afd2792c22',
            'bytes': 4650,
            'mode': '100644',
            'sha256': '5518b22b8e8a3745a20f4fe65734b558c0e09b04da2e55efd5922da1184d9445'},
 'core.py': {'blob': '9fbfac2f3d1c4d02a847835e6c3a0aaed156b408',
             'bytes': 7606,
             'mode': '100644',
             'sha256': 'fd82f5ef30590b251954e17e9b179678c610b4b2b4349e28ba0340d4f48ab816'},
 'fixtures/complete.json': {'blob': 'c69567289ed45fe2afb07bf2bf82f36f802c8ca6',
                            'bytes': 1719,
                            'mode': '100644',
                            'sha256': 'b0abb0e5d42b8508e4fd8ebf92289a9576b94c27003fd77399ad0ff5288f06f6'},
 'fixtures/contradictory.json': {'blob': 'a8a734643b966f31ec8deebb6507a29277faf574',
                                 'bytes': 2683,
                                 'mode': '100644',
                                 'sha256': '9ae9b920e93037914bf05fcd4954bb5ec6504c376f74fb0e65f6b94f83f4b330'},
 'fixtures/missing.json': {'blob': '01ad3c3b97071ee2cd01a7d0e0c527d3116e591c',
                           'bytes': 1393,
                           'mode': '100644',
                           'sha256': 'b96afa3a7ce4837771b03f742b09a7582c9e0d86f648e74115ef88b1a31d67f3'},
 'live_service.py': {'blob': '0311bd2bc2d8693788977edffe358502af9a671e',
                     'bytes': 4121,
                     'mode': '100644',
                     'sha256': '93671023e6727184217c29faad2b3ba2c04dbc66e57841cfba2b8c5fd9deae56'},
 'output.schema.json': {'blob': '6877a794514bc0d234bd25f1a80e9c0614c3d45d',
                        'bytes': 17189,
                        'mode': '100644',
                        'sha256': 'a7b4ce73a452c3530533b3c713d016f1157df672907d2f16687bdfe6d0e3c513'},
 'references/expectations.json': {'blob': '0bf48ed7e6a9121f1d4d5bcd34d6bec2cad2d286',
                                  'bytes': 1308,
                                  'mode': '100644',
                                  'sha256': '20997989f5e5c7c37fa80ed032e27d8012036f26719d2291c1c805889dc9a163'},
 'release/QA_EVIDENCE170.md': {'blob': '867039256e9b3ca092516455ee5553fe50cba039',
                               'bytes': 2271,
                               'mode': '100644',
                               'sha256': 'a24c1db3b56159be6b43f58d4b758aa52874ed87f65ed0b9105cb557b0dd0684'},
 'release/READINESS170.json': {'blob': '5ce0696755cc3bf0c01242ebf67fa87cc1db25d6',
                               'bytes': 5425,
                               'mode': '100644',
                               'sha256': 'e76a92e121e9a57a1d5f42e8a0fe28afdb27ea447189847c7d670469928de848'},
 'service.py': {'blob': 'c58be8b923818a87fe5cc2f544b2ddaefbde8edc',
                'bytes': 4693,
                'mode': '100644',
                'sha256': 'de05c2a3cc0ac6afd2e98b867dea4617c52534c69d15b5d9bbfaf490c85f94c4'},
 'verifier.py': {'blob': '8a0ac08f3a4e476d7c56e23cfebe0ef793e50dd8',
                 'bytes': 4493,
                 'mode': '100644',
                 'sha256': '6ef90062e4d6e8af7c81457965d5f36c2905815e25685ccb316ba01b7b23a290'},
 'web/app.js': {'blob': '75dc0fd668b67886e8126e67eb09e742422177a9',
                'bytes': 7594,
                'mode': '100644',
                'sha256': 'a7a47f3df7329b9bab7fe642383ea7000647d70a599b3688544742c8872b4040'},
 'web/index.html': {'blob': '3c0af71b20d51fa6a858a1267ba79402c36c0301',
                    'bytes': 2162,
                    'mode': '100644',
                    'sha256': '9ef4315840b7c43e9461129c48907d07a7592a0c91a8dd1ee22b961a338bdf31'},
 'web/style.css': {'blob': '9d805e0cd8d3fe28a86591f5e45e8ec8525b42f2',
                   'bytes': 4100,
                   'mode': '100644',
                   'sha256': '911467e25c63dc9985642d5a613bfdaa1f306b7d04b753863d734dd8b5833144'}}
GENERATED = ('BUILD_PROVENANCE.json', 'MANIFEST.csv', 'SHA256SUMS', 'START_HERE.md')
STAMP = (1980, 1, 1, 0, 0, 0)
MAX_ARCHIVE = 262144
START = '''# TraceHarbor — Offline Testbuild 175

Start here. This portable kit contains 19 pinned source files from commit
a999b347e9efa3296d02e255e6741a474853bff0, plus four generated release files.
BUILD_PROVENANCE.json records every selected path and its source pins.

## Run locally

Use Python 3.12 or newer. Only the Python standard library is required; no
installation, API key, account, model download or provider access is needed.
Unpack the verified ZIP into a new folder, open a terminal in that folder, run:

    python app.py serve --port 8787

Open http://127.0.0.1:8787/ on the same computer. Stop the foreground server
with Ctrl+C. This is a temporary local demo, not persistent public hosting.

## Three synthetic cases and portable dossiers

Select the complete, missing or contradictory fixture in the UI. Complete is
a known synthetic supported_reference, missing remains uncertain, and
contradictory remains conflicted. Inspect the source quotes and citations.
Export/download a dossier JSON, then use the UI import/verify control to
re-import it. The verifier rejects a changed dossier with a stale checksum.

For a file-based run (use a new output name for each command):

    python app.py analyze fixtures/complete.json --out complete-dossier.json
    python app.py analyze fixtures/missing.json --out missing-dossier.json
    python app.py analyze fixtures/contradictory.json --out contradictory-dossier.json

## Evidence and limits

DEMO_NO_AI / SYNTHETIC: this kit makes no AI-provider calls. Exact matching
quotes and checksum integrity do not establish causality, truth of a claim,
independent provider origin, or live model execution. Known synthetic reference
support is not proof about real-world events. The schema and source checks
retain uncertainty and conflict rather than replacing them with certainty.

The accepted 173 qualification covers three CLI cases and ten local HTTP
requests. All six executable modules, fixtures, reference data, schema and web
assets here are byte-identical to that qualified subset after the exact import
decoupling accepted and published in 174. No new browser, screenshot, model,
physical-device or video qualification is claimed for 175. Historical QA7
belongs to an ancestor commit, not to this kit's current source commit.

README.md and the selected release documents are unmodified historical source
documentation. Their older packaging descriptions, dates and QA boundaries
must not be treated as the inventory or current qualification of kit175.
This START_HERE and BUILD_PROVENANCE define the present portable release.

This is not a live contest-ready entry. There is no persistent hosted judge
URL, genuine Nebius/NVIDIA runtime proof, recorded/public video or completed
submission in this delivery. VIDEO_SCRIPT.md is only an unrecorded 160-second
storyboard. Eligibility, rights, provider access/cost/model capabilities and
final entry gates remain open. LICENSE is the original MIT license.
'''


def digest(data):
    return hashlib.sha256(data).hexdigest()


def owned_directory(path):
    path = Path(path).absolute()
    if path.resolve(strict=True) != path:
        raise ValueError('SOURCE_OR_OUTPUT_PARENT_SYMLINK')
    value = path.lstat()
    if not stat.S_ISDIR(value.st_mode) or value.st_uid != os.geteuid() or value.st_mode & 0o022:
        raise ValueError('DIRECTORY_OWNERSHIP_OR_MODE')
    return path


def read_source(root, name, expected):
    parts = name.split('/')
    if any(x in ('', '.', '..') for x in parts) or name.startswith('/') or '\\' in name:
        raise ValueError('INVALID_SOURCE_PATH')
    directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in parts[:-1]:
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            os.close(directory)
            directory = nxt
            st = os.fstat(directory)
            if st.st_uid != os.geteuid() or st.st_mode & 0o022:
                raise ValueError('SOURCE_PARENT_OWNERSHIP_OR_MODE')
        fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory)
        try:
            before = os.fstat(fd)
            if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1
                    or stat.S_IMODE(before.st_mode) != 0o644 or before.st_uid != os.geteuid()
                    or before.st_size != expected['bytes']):
                raise ValueError('SOURCE_NOT_EXACT_REGULAR_100644_SINGLE_LINK:' + name)
            with os.fdopen(fd, 'rb', closefd=False) as source:
                data = source.read(expected['bytes'] + 1)
            after = os.fstat(fd)
            if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
                    after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                raise ValueError('SOURCE_CHANGED_DURING_READ:' + name)
        finally:
            os.close(fd)
    finally:
        os.close(directory)
    oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    if len(data) != expected['bytes'] or digest(data) != expected['sha256'] or oid != expected['blob']:
        raise ValueError('SOURCE_PIN_MISMATCH:' + name)
    return data


def build(source, output):
    if os.name != 'posix' or not all(hasattr(os, x) for x in ('O_NOFOLLOW', 'O_DIRECTORY', 'geteuid')):
        raise ValueError('BUILDER_REQUIRES_POSIX_NOFOLLOW_DIRFD_GUARDS')
    source = owned_directory(source)
    output = Path(output).absolute()
    parent = owned_directory(output.parent)
    if output == source or source in output.parents:
        raise ValueError('OUTPUT_INSIDE_SOURCE')
    if output.exists() or output.is_symlink():
        raise FileExistsError('OUTPUT_ALREADY_EXISTS')
    if len(PINS) != 19 or set(PINS) & set(GENERATED):
        raise ValueError('INVALID_COMPILED_ALLOWLIST')
    payload = {name: read_source(source, name, pin) for name, pin in sorted(PINS.items())}
    provenance = {
        'schema': 'TRACEHARBOR_OFFLINE_RELEASE175_V1', 'release': 175,
        'source_commit': SOURCE_COMMIT, 'source_tree': SOURCE_TREE, 'source_tree_files': 243,
        'source_files': PINS, 'generated_files': list(GENERATED),
        'source_count': 19, 'generated_count': 4, 'archive_member_count': 23,
        'builder_source_sha256': digest(Path(__file__).read_bytes()),
        'zip': {'compression': 'STORED', 'order': 'LEXICAL', 'timestamp': list(STAMP),
                'transport_mode': '100644', 'source_mode_domain': 'Git100644',
                'tree_is_not_archive_digest': True},
        'qualification': {'reused': 'accepted173_3CLI_10loopbackHTTP_same_executable_fixture_web_bytes',
                          'current175_browser': False, 'provider_calls': 0, 'DEMO_NO_AI': True,
                          'synthetic': True, 'hosted_judge_url': None, 'public_video': None,
                          'submission_complete': False, 'matching_quotes_prove_causality': False,
                          'matching_quotes_prove_provider_origin': False,
                          'historical_docs_are_current_release_inventory': False}}
    payload['START_HERE.md'] = START.encode()
    payload['BUILD_PROVENANCE.json'] = (json.dumps(provenance, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()
    payload['SHA256SUMS'] = ''.join(digest(data) + '  ' + name + '\n'
                                   for name, data in sorted(payload.items())).encode()
    stream = io.StringIO(newline='')
    writer = csv.writer(stream, lineterminator='\n')
    writer.writerow(['relative_path', 'size_bytes', 'sha256'])
    writer.writerows((name, len(data), digest(data)) for name, data in sorted(payload.items()))
    payload['MANIFEST.csv'] = stream.getvalue().encode()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_STORED, allowZip64=False) as archive:
        for name, data in sorted(payload.items()):
            item = zipfile.ZipInfo(name, STAMP)
            item.create_system = 3
            item.external_attr = (stat.S_IFREG | 0o644) << 16
            item.compress_type = zipfile.ZIP_STORED
            archive.writestr(item, data)
    data = buffer.getvalue()
    if len(data) > MAX_ARCHIVE:
        raise ValueError('ARCHIVE_SIZE_LIMIT')
    # The create-only final file is opened only after all input and memory checks pass.
    parent_fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        fd = os.open(output.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                     0o600, dir_fd=parent_fd)
        try:
            with os.fdopen(fd, 'wb', closefd=False) as target:
                target.write(data)
                target.flush()
                os.fsync(fd)
        finally:
            os.close(fd)
    finally:
        os.close(parent_fd)
    return {'status': 'PASS', 'release': 175, 'bytes': len(data), 'sha256': digest(data),
            'source_files': 19, 'generated_files': 4, 'members': 23}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        result = build(args.source, args.output)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)}, sort_keys=True), file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
