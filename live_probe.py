"""Exactly three distinct synthetic requests, only after a reviewed admission file.

The admission file records external evidence; it is not itself provider proof.
Never delete its .spent marker, move it, or mint a replacement to resume a run.
"""
import argparse
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import json
import os
from pathlib import Path
from core import canonical, digest, import_package, parse_json
from nebius import request_for, https_once, decode_response, ProviderError
from live_service import build_record

CASES = ('complete', 'missing', 'contradictory')
ROOT = Path(__file__).resolve().parent

def planned_requests(model):
    return [(ROOT/'fixtures'/f'{name}.json').read_bytes() for name in CASES], [
        request_for(import_package((ROOT/'fixtures'/f'{name}.json').read_bytes()), model) for name in CASES]

def admit(permit, requests):
    if permit.get('schema') != 'traceharbor.live-admission.v1' or permit.get('operation_id') != 'TRACEHARBOR_THREE_SYNTHETIC_REQUESTS_V1':
        raise ValueError('Unsupported admission or operation.')
    try: expiry = datetime.fromisoformat(permit['expires_utc'].replace('Z', '+00:00'))
    except (KeyError, AttributeError, TypeError, ValueError): raise ValueError('Valid admission expiry required.') from None
    if expiry.tzinfo is None or expiry <= datetime.now(timezone.utc): raise ValueError('Admission expired.')
    for name in ('verified_access_evidence', 'verified_credit_and_cap_evidence', 'verified_model_license_evidence', 'verified_token_bounds_evidence'):
        if not isinstance(permit.get(name), str) or not permit[name].strip():
            raise ValueError('Missing externally verified evidence: '+name)
    if permit['request_sha256'] != [digest(p) for p in requests]: raise ValueError('Request digest mismatch.')
    if any(p['model'] != permit['model'] for p in requests): raise ValueError('Model mismatch.')
    bounds = permit['input_token_upper_bounds']
    if not isinstance(bounds, list) or len(bounds) != 3 or any(type(n) is not int or not 0 < n <= 3000 for n in bounds):
        raise ValueError('Three verified input token bounds of at most 3000 required.')
    prices = [Decimal(str(permit[n])) for n in ('input_usd_per_million', 'output_usd_per_million', 'max_cost_usd')]
    if any(not p.is_finite() or p < 0 for p in prices) or prices[2] <= 0:
        raise ValueError('Invalid financial admission.')
    worst = (sum(bounds)*prices[0] + 4500*prices[1])/Decimal(1000000)
    if worst > prices[2]: raise ValueError('Request budget exceeds verified cap.')
    return worst

def write_new(path, data):
    # Create-only and flushed before dependent effects. No secrets in these files.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as f:
        f.write(canonical(data)+b'\n'); f.flush(); os.fsync(f.fileno())
    directory = os.open(Path(path).parent, os.O_RDONLY)
    try: os.fsync(directory)
    finally: os.close(directory)

def execute(permit_path, output):
    permit_path = permit_path.resolve()
    permit = parse_json(permit_path.read_bytes())
    model = os.environ.get('NEBIUS_MODEL')
    raw_cases, requests = planned_requests(model)
    worst = admit(permit, requests)
    if not os.environ.get('NEBIUS_API_KEY'): raise ValueError('Credential not configured; zero requests.')
    output.mkdir(mode=0o700, parents=False, exist_ok=False)
    write_new(Path(str(permit_path)+'.spent'), {'operation_id': permit['operation_id'],
        'permit_sha256': digest(permit), 'request_sha256': permit['request_sha256'],
        'output': str(output.resolve()), 'reserved_requests': 3, 'worst_cost_usd': str(worst),
        'state': 'RESERVED_DO_NOT_REPLAY'})
    outcomes = []
    for index, (name, raw, request) in enumerate(zip(CASES, raw_cases, requests)):
        write_new(output/f'{index+1}-attempt.json', {'case': name, 'request_sha256': digest(request),
            'state': 'ATTEMPTING', 'retries': 0})
        # Failure after ATTEMPTING is unknown unless a terminal receipt exists. Never replay.
        try:
            analysis, metadata = decode_response(https_once(request), model)
            metadata['request_sha256'] = digest(request)
            record = build_record(raw, analysis, metadata)
            write_new(output/f'{name}-dossier.json', record)
            outcome = {'case': name, 'status': 'VERIFIED_RECORD', 'model': model,
                'usage': metadata['usage'], 'output_sha256': record['dossier_sha256']}
            if metadata['usage']['prompt_tokens'] > permit['input_token_upper_bounds'][index]:
                outcome['status'] = 'TOKEN_BOUND_VIOLATION_STOP'
        except (ValueError, OSError) as exc:
            # Exception text may contain source/model content; persist a safe class/code only.
            outcome = {'case': name, 'status': 'REJECTED_OR_UNKNOWN_NO_RETRY',
                'error': str(exc) if isinstance(exc, ProviderError) else type(exc).__name__}
        write_new(output/f'{index+1}-terminal.json', outcome)
        outcomes.append(outcome)
        if outcome['status'] == 'TOKEN_BOUND_VIOLATION_STOP': break
    write_new(output/'result.json', {'operation_id': permit['operation_id'], 'outcomes': outcomes,
        'completed_three': len(outcomes) == 3 and all(x['status'] == 'VERIFIED_RECORD' for x in outcomes),
        'live_proof_scope': 'local execution receipts; imported files alone are unauthenticated'})
    return 0 if len(outcomes) == 3 and all(x['status'] == 'VERIFIED_RECORD' for x in outcomes) else 2

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--admission', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try: return execute(args.admission, args.out)
    except (ValueError, OSError, KeyError, TypeError, InvalidOperation):
        print('Live probe not completed. Check admission, credentials and existing reservation; do not replay.')
        return 2

if __name__ == '__main__': raise SystemExit(main())
