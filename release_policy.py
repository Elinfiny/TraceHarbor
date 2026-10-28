"""Inactive reviewed-release policy. Integer nanodollars, no accountwide spend claim."""
import hashlib, json, re
from datetime import datetime, timezone
MODEL='nvidia/Nemotron-3_5-Lightning'
TEMPLATE='17dc9cd8a6b70ec56bc2b758f9539a113ba789b5b025105234ae3aed78a5f49d'
REVISION='a9904d24bcc1d289a1950fa9d2b978c47cf903b9'
END='2026-12-15T20:00:00+00:00'
REVIEWED_RELEASE_SHA256=None

def canonical(x): return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
def digest(x): return hashlib.sha256(canonical(x)).hexdigest()
class Refusal(ValueError): pass

def validate_config(c):
    expected={'schema':'traceharbor.release46.v1','model':MODEL,'template_sha256':TEMPLATE,
      'tokenizer_revision':REVISION,'input_limit':8192,'output_limit':1500,'call_limit':256,
      'input_nanodollars_per_token':60,'output_nanodollars_per_token':240,
      'budget_nanodollars':217989120,'deadline':END,'retry':False}
    if type(c) is not dict or set(c)!=set(expected)|{'allocation_id','public_hostname','blocked_request_sha256','prior_effects_sha256'}: raise Refusal('CONFIG_SHAPE')
    for k,v in expected.items():
        if type(c[k]) is not type(v) or c[k]!=v: raise Refusal('CONFIG_CONTRACT')
    if not re.fullmatch(r'[a-f0-9]{32}',c['allocation_id']): raise Refusal('ALLOCATION_ID')
    if type(c['blocked_request_sha256'])is not list or len(c['blocked_request_sha256'])>256 or c['blocked_request_sha256']!=sorted(set(c['blocked_request_sha256'])) or any(type(v)is not str or not re.fullmatch('[a-f0-9]{64}',v) for v in c['blocked_request_sha256']):raise Refusal('PRIOR_REPLAY_PINS')
    if type(c['prior_effects_sha256'])is not str or not re.fullmatch('[a-f0-9]{64}',c['prior_effects_sha256']):raise Refusal('PRIOR_EFFECT_LEDGER_PIN')
    h=c['public_hostname']
    if type(h)is not str or len(h)>253 or not re.fullmatch(r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}',h): raise Refusal('REAL_HOST_REQUIRED')
    return c

def deadline(c,now=None):
    if (now or datetime.now(timezone.utc))>=datetime.fromisoformat(c['deadline']): raise Refusal('RELEASE_EXPIRED')

def input_admission(payload,count,c):
    if payload.get('model')!=c['model'] or payload.get('max_completion_tokens')!=1500 or payload.get('stream',False) is not False or payload.get('n',1)!=1:raise Refusal('REQUEST_CONTRACT')
    if type(count)is not dict or set(count)!={'count','request_sha256','template_sha256','tokenizer_revision'}:raise Refusal('COUNTER_CERTIFICATE')
    if count['request_sha256']!=digest(payload) or count['template_sha256']!=c['template_sha256'] or count['tokenizer_revision']!=c['tokenizer_revision']:raise Refusal('COUNTER_PIN')
    n=count['count']
    if type(n)is not int or not 1<=n<=c['input_limit']:raise Refusal('INPUT_LIMIT')
    return n*60+1500*240
