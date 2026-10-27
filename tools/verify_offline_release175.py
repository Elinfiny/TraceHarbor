#!/usr/bin/env python3
"""Independently inspect pinned kit175 bytes; never extract or execute its payload."""
import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import struct
import sys
import zipfile

# Independent immutable source anchor: no import of builder or archive code.
EXPECTED = {'LICENSE': {'blob': '5fd6e0433878a3202ffe231344b0e8fabd4fe6fb',
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
BUILDER_SHA256 = 'fb33405885519c4b940f1fa2aafdcd7e473a29323936703732d0e0f66525fd94'
START_SHA256 = '5de8054691f4b1b7d852c5e3fff87bcfd270fe413f99abe18067f88217c61879'
GENERATED = {'START_HERE.md', 'BUILD_PROVENANCE.json', 'MANIFEST.csv', 'SHA256SUMS'}
MAX_ARCHIVE = 262144
MAX_MEMBER = 32768
MAX_EXPANDED = 196608


def fail(message):
    raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def no_duplicate_json(pairs):
    output = {}
    for key, value in pairs:
        if key in output:
            fail('DUPLICATE_JSON_KEY:' + key)
        output[key] = value
    return output


def verify(path):
    path = Path(path)
    before = path.lstat()
    if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1
            or before.st_size > MAX_ARCHIVE):
        fail('ARCHIVE_FILE_TYPE_OR_SIZE')
    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
    try:
        now = os.fstat(fd)
        if (now.st_dev, now.st_ino, now.st_size) != (before.st_dev, before.st_ino, before.st_size):
            fail('ARCHIVE_CHANGED_BEFORE_READ')
        with os.fdopen(fd, 'rb', closefd=False) as source:
            raw = source.read(MAX_ARCHIVE + 1)
        after = os.fstat(fd)
        if len(raw) != before.st_size or len(raw) > MAX_ARCHIVE or (
                before.st_mtime_ns, before.st_ctime_ns) != (after.st_mtime_ns, after.st_ctime_ns):
            fail('ARCHIVE_CHANGED_DURING_READ')
    finally:
        os.close(fd)
    if len(raw) < 22 or not raw.startswith(b'PK\x03\x04'):
        fail('ZIP_BOUNDARY')
    end = struct.unpack('<4s4H2LH', raw[-22:])
    if (end[0] != b'PK\x05\x06' or end[1:3] != (0, 0) or end[3] != end[4]
            or end[5] + end[6] != len(raw) - 22 or end[7] != 0):
        fail('ZIP_BOUNDARY_OR_MULTIDISK')
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        entries = archive.infolist()
        if len(entries) > 23:
            fail('MEMBER_COUNT_LIMIT')
        seen = set()
        names = []
        expanded = 0
        for entry in entries:
            name = entry.filename
            parts = name.split('/')
            if (not name or name.startswith('/') or '\\' in name or ':' in name
                    or any(p in ('', '.', '..') for p in parts) or PurePosixPath(name).is_absolute()):
                fail('UNSAFE_PATH:' + name)
            if name.casefold() in seen:
                fail('DUPLICATE_OR_CASE_COLLISION:' + name)
            seen.add(name.casefold())
            names.append(name)
            mode = entry.external_attr >> 16
            if (entry.is_dir() or stat.S_ISLNK(mode) or not stat.S_ISREG(mode)
                    or stat.S_IMODE(mode) != 0o644):
                fail('NON_REGULAR_MEMBER:' + name)
            if entry.flag_bits & 1:
                fail('ENCRYPTED_MEMBER:' + name)
            if entry.flag_bits != 0:
                fail('UNEXPECTED_MEMBER_FLAGS:' + name)
            if entry.file_size > MAX_MEMBER or entry.file_size / max(1, entry.compress_size) > 200:
                fail('MEMBER_BOUNDS:' + name)
            expanded += entry.file_size
            if expanded > MAX_EXPANDED:
                fail('AGGREGATE_BOUNDS')
            if entry.compress_type != zipfile.ZIP_STORED or entry.date_time != (1980, 1, 1, 0, 0, 0):
                fail('NONDETERMINISTIC_TRANSPORT:' + name)
            if entry.create_system != 3 or entry.extra or entry.comment:
                fail('UNEXPECTED_TRANSPORT_METADATA:' + name)
        # Each bounded read validates the original member CRC before acceptance.
        payload = {name: archive.read(name) for name in names}
        for name, data in payload.items():
            if name in EXPECTED:
                pin = EXPECTED[name]
                oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
                if len(data) != pin['bytes'] or digest(data) != pin['sha256'] or oid != pin['blob']:
                    fail('SOURCE_PIN_MISMATCH:' + name)
        if set(names) != set(EXPECTED) | GENERATED or len(names) != 23:
            fail('CLOSEDSET_MISMATCH')
        if names != sorted(names) or archive.comment or archive.testzip() is not None:
            fail('ORDER_COMMENT_OR_CRC')
        manifest_text = payload['MANIFEST.csv'].decode('utf-8')
        reader = csv.DictReader(io.StringIO(manifest_text, newline=''))
        if reader.fieldnames != ['relative_path', 'size_bytes', 'sha256']:
            fail('MANIFEST_HEADERS')
        rows = list(reader)
        declared = [row['relative_path'] for row in rows]
        if (declared != sorted(set(names) - {'MANIFEST.csv'})
                or len(rows) != 22 or len(set(declared)) != 22):
            fail('MANIFEST_CLOSEDSET')
        for row in rows:
            if set(row) != {'relative_path', 'size_bytes', 'sha256'}:
                fail('MANIFEST_ROW_FIELDS')
            data = payload[row['relative_path']]
            if row['size_bytes'] != str(len(data)) or row['sha256'] != digest(data):
                fail('MANIFEST_PIN_MISMATCH:' + row['relative_path'])
        sums = payload['SHA256SUMS'].decode('utf-8').splitlines()
        sum_names = []
        for line in sums:
            match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
            if not match or match[2] not in payload or digest(payload[match[2]]) != match[1]:
                fail('SHA256SUMS_PIN_MISMATCH')
            sum_names.append(match[2])
        if sum_names != sorted(set(names) - {'MANIFEST.csv', 'SHA256SUMS'}):
            fail('SHA256SUMS_CLOSEDSET')
        provenance = json.loads(payload['BUILD_PROVENANCE.json'], object_pairs_hook=no_duplicate_json)
        expected_provenance = {
            'schema': 'TRACEHARBOR_OFFLINE_RELEASE175_V1', 'release': 175,
            'source_commit': 'a999b347e9efa3296d02e255e6741a474853bff0',
            'source_tree': '4fae2da1170f30f585a1afcb598717abe103cd1f', 'source_tree_files': 243,
            'source_files': EXPECTED,
            'generated_files': ['BUILD_PROVENANCE.json', 'MANIFEST.csv', 'SHA256SUMS', 'START_HERE.md'],
            'source_count': 19, 'generated_count': 4, 'archive_member_count': 23,
            'builder_source_sha256': BUILDER_SHA256,
            'zip': {'compression': 'STORED', 'order': 'LEXICAL', 'timestamp': [1980, 1, 1, 0, 0, 0],
                    'transport_mode': '100644', 'source_mode_domain': 'Git100644',
                    'tree_is_not_archive_digest': True},
            'qualification': {'reused': 'accepted173_3CLI_10loopbackHTTP_same_executable_fixture_web_bytes',
                              'current175_browser': False, 'provider_calls': 0, 'DEMO_NO_AI': True,
                              'synthetic': True, 'hosted_judge_url': None, 'public_video': None,
                              'submission_complete': False, 'matching_quotes_prove_causality': False,
                              'matching_quotes_prove_provider_origin': False,
                              'historical_docs_are_current_release_inventory': False}}
        if provenance != expected_provenance:
            fail('PROVENANCE_MISMATCH')
        if digest(payload['START_HERE.md']) != START_SHA256:
            fail('START_DOCUMENT_PIN_MISMATCH')
    return {'status': 'PASS', 'release': 175, 'bytes': len(raw), 'sha256': digest(raw),
            'source_files': 19, 'generated_files': 4, 'members': 23,
            'manifest_pins': 22, 'expanded_bytes': expanded,
            'extracted_or_executed_payloads': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive')
    args = parser.parse_args()
    try:
        result = verify(args.archive)
    except (OSError, ValueError, KeyError, TypeError, UnicodeError, zipfile.BadZipFile, csv.Error) as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)}, sort_keys=True), file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
