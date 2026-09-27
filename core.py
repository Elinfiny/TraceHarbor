"""Bounded synthetic evidence import. No network, AI, or action execution."""
from __future__ import annotations
import hashlib
import json
import re
from datetime import datetime, timezone

MAX_BYTES = 262144
MAX_SOURCES = 12
MAX_EVENTS = 200
MAX_TEXT = 8192
ID = re.compile(r'^[a-z][a-z0-9_-]{0,63}$')
KINDS = {'log', 'deployment', 'metric', 'configuration', 'runbook', 'audit'}
# A conservative accidental-secret guard, not a DLP guarantee. Synthetic data only.
SECRET = re.compile(r'-----BEGIN .*PRIVATE KEY-----|\b(?:AKIA|ASIA)[A-Z0-9]{16}\b|\b(?:sk-|ghp_)[A-Za-z0-9_-]{20,}|(?:password|api[_ -]?key|access[_ -]?token)\s*[:=]\s*\S+', re.I)

class InputError(ValueError):
    pass

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')

def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def _pairs(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise InputError('Duplicate JSON key: ' + k[:64])
        result[k] = v
    return result

def parse_json(raw):
    if not isinstance(raw, bytes) or not raw or len(raw) > MAX_BYTES:
        raise InputError('JSON must be 1..262144 bytes.')
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=_pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(InputError('Non-finite number.')))
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise InputError('Invalid UTF-8 JSON.') from exc

def shape(obj, required, optional=()):
    if not isinstance(obj, dict) or not set(required) <= set(obj) or set(obj) - set(required) - set(optional):
        raise InputError('Object fields do not match the documented schema.')

def text(value, limit=MAX_TEXT):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise InputError('Text is missing or exceeds its bound.')
    try:
        value.encode('utf-8')
    except UnicodeError as exc:
        raise InputError('Invalid Unicode text.') from exc
    if SECRET.search(value):
        raise InputError('Possible secret: synthetic data only; import refused.')
    return value

def identifier(value):
    if not isinstance(value, str) or not ID.fullmatch(value):
        raise InputError('Invalid identifier.')
    return value

def normalize_time(value):
    if value is None:
        return None
    if not isinstance(value, str) or len(value) > 40 or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})', value):
        raise InputError('Timestamp must be ISO-8601 with seconds and explicit timezone, or null.')
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)
    except (ValueError, OverflowError) as exc:
        raise InputError('Invalid timestamp.') from exc
    return dt.isoformat(timespec='microseconds' if dt.microsecond else 'seconds').replace('+00:00', 'Z')

def import_package(raw):
    data = parse_json(raw)
    shape(data, {'schema', 'synthetic', 'case_id', 'title', 'sources'})
    if data['schema'] != 'traceharbor.input.v1' or data['synthetic'] is not True:
        raise InputError('Only explicitly synthetic traceharbor.input.v1 packages are accepted.')
    identifier(data['case_id']); text(data['title'], 160)
    if not isinstance(data['sources'], list) or not 1 <= len(data['sources']) <= MAX_SOURCES:
        raise InputError('Expected 1..12 sources.')
    sources, warnings, seen_sources, count, unique = [], [], set(), 0, {}
    for source in data['sources']:
        shape(source, {'id', 'kind', 'title', 'events'})
        sid = identifier(source['id'])
        if sid in seen_sources: raise InputError('Duplicate source identifier.')
        seen_sources.add(sid)
        if not isinstance(source['kind'], str) or source['kind'] not in KINDS: raise InputError('Unsupported source kind.')
        text(source['title'], 160)
        if not isinstance(source['events'], list) or not source['events']:
            raise InputError('Each source needs events.')
        seen_events, normalized = set(), []
        for event in source['events']:
            count += 1
            if count > MAX_EVENTS: raise InputError('Maximum 200 events.')
            shape(event, {'id', 'text'}, {'timestamp', 'timestamp_alt'})
            eid = identifier(event['id'])
            if eid in seen_events: raise InputError('Duplicate event identifier inside source.')
            seen_events.add(eid); text(event['text'])
            t1, t2 = normalize_time(event.get('timestamp')), normalize_time(event.get('timestamp_alt'))
            candidates = sorted({x for x in (t1, t2) if x is not None})
            # A secondary observation is retained but never substitutes for a missing primary timestamp.
            state = 'missing' if t1 is None else ('conflict' if t2 and t1 != t2 else 'known')
            timestamp = t1 if state == 'known' else None
            if state != 'known': warnings.append({'code': 'TIMESTAMP_' + state.upper(), 'source_id': sid, 'event_id': eid, 'candidates': candidates})
            norm = {'id': eid, 'text': event['text'], 'timestamp': timestamp, 'timestamp_state': state, 'timestamp_candidates': candidates}
            normalized.append(norm)
            # Deduplicate content/time/kind across sources, preserving every citation as an occurrence.
            key = digest({'kind': source['kind'], 'text': event['text'], 'time': candidates, 'state': state})
            occurrence = {'source_id': sid, 'event_id': eid}
            if key not in unique:
                unique[key] = {'event_sha256': key, **{k: v for k, v in norm.items() if k != 'id'}, 'kind': source['kind'], 'occurrences': []}
            unique[key]['occurrences'].append(occurrence)
        sources.append({'id': sid, 'kind': source['kind'], 'title': source['title'], 'sha256': digest(source), 'raw': source, 'events': normalized})
    # Compare instants, not mixed-precision ISO strings. Unknown times stay last;
    # the hash is only a deterministic tie-breaker, never a causal ordering.
    timeline = sorted(unique.values(), key=lambda e: (
        e['timestamp'] is None,
        datetime.fromisoformat(e['timestamp'].replace('Z', '+00:00'))
        if e['timestamp'] else datetime.max.replace(tzinfo=timezone.utc),
        e['event_sha256']))
    # Raw source hashes retain duplicates and original timestamps; analysis fingerprint ignores duplicate copies only.
    fingerprint = digest(sorted({canonical({'source_id': s['id'], 'kind': s['kind'], 'title': s['title'], 'text': e['text'], 'timestamp': e['timestamp'], 'state': e['timestamp_state'], 'candidates': e['timestamp_candidates']}).decode() for s in sources for e in s['events']}))
    return {'schema': 'traceharbor.evidence.v1', 'case_id': data['case_id'], 'title': data['title'], 'synthetic': True,
            'input_sha256': hashlib.sha256(raw).hexdigest(), 'analysis_fingerprint': fingerprint,
            'sources': sources, 'timeline': timeline, 'warnings': warnings,
            'counts': {'input_events': count, 'unique_events': len(timeline), 'duplicates': count-len(timeline)}}

def citation(evidence, source_id, event_id):
    for source in evidence['sources']:
        if source['id'] == source_id:
            for event in source['events']:
                if event['id'] == event_id:
                    return {'source_id': source_id, 'event_id': event_id, 'source_sha256': source['sha256'], 'quote': event['text']}
    raise InputError('Reference event not found.')
