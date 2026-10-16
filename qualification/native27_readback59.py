"""Private readback algorithm. No installed native route or admission.

Providers retain bounded wire bytes/EOF, never reconstructed JSON. This module
contains no credential lookup, HTTP implementation, dispatcher or model caller.
The only installed entry point is explicitly synthetic qualification. A future
host must separately bind authenticated transport and exact redirect policy.
"""
import base64
from dataclasses import dataclass, field
import hashlib
import math
import re
from urllib.parse import urlsplit
import native27_validator42 as v

EXTERNAL_ADMISSION_GATE = None
NATIVE_HOST_ROUTE = None
NATIVE_REDIRECT_POLICY = None
PLAN = None
nativeAdmission = None

@dataclass(frozen=True)
class Target:
    repository: str
    run_id: int
    attempt: int
    job_id: int

@dataclass(frozen=True)
class Original:
    status: int
    headers: dict
    body: bytes
    eof: bool
    error: object = None

@dataclass(frozen=True)
class Readback:
    classification: str
    validator_receipt: dict
    source: str
    run_id: int
    job_id: int
    live_authority: bool = False
    dispatch_performed: bool = False

@dataclass
class PrivateState:
    validator: object = field(default_factory=v.Sticky, repr=False)
    originals: list = field(default_factory=list, repr=False)
    summaries: list = field(default_factory=list)
    calls: int = 0

    def fail(self, code):
        self.validator.fail(code)

    def public(self):
        return {'classification':'SYNTHETIC_ONLY', 'calls':self.calls,
                'responses':list(self.summaries),
                'first_UNKNOWN':self.validator.first_unknown,
                'native_host':None, 'redirect_binding':None,
                'nativeAdmission':None, 'PLAN':None}


def sha40(x):
    return type(x) is str and re.fullmatch('[0-9a-f]{40}',x) is not None

def integer(x):
    return type(x) is int and 0 < x <= 9223372036854775807


def preflight(target, b):
    v.need(type(target) is Target, 'TARGET_TYPE')
    v.need(target.repository == v.REPO, 'REPOSITORY_MISMATCH')
    v.need(integer(target.run_id) and target.run_id == b['first_run_id'], 'RUN_MISMATCH')
    v.need(type(target.attempt) is int and target.attempt == b['attempt'] == 1, 'ATTEMPT_MISMATCH')
    v.need(integer(target.job_id), 'JOB_MISMATCH')
    v.bindings(b)


class Reader:
    def __init__(self, provider, state, clock, deadline, redirect_policy):
        self.provider, self.state, self.clock = provider, state, clock
        self.deadline, self.redirect_policy = deadline, redirect_policy
        self.metadata_raw = {}

    def check(self):
        v.need(self.state.validator.first_unknown is None, 'PREVIOUS_UNKNOWN')
        v.need(self.clock() < self.deadline, 'DEADLINE')
        v.need(self.state.calls < 16, 'CALL_LIMIT')

    def call(self, path, limit=v.RECORD_MAX, download=False):
        self.check()
        self.state.calls += 1
        try:
            # Provider must read at most limit+1 bytes, with the SAME absolute
            # deadline, disable redirects, and return EOF/exception even if late.
            raw = (self.provider.download(path, limit, self.deadline) if download
                   else self.provider.get(path, limit, self.deadline))
        except Exception as error:
            self.state.originals.append(('EXCEPTION', error))
            self.state.fail('PROVIDER_EXCEPTION')
        # Retention precedes every post-return guard, including clock/status.
        if type(raw) is Original and type(raw.body) is bytes and len(raw.body)>limit+1:
            self.state.originals.append(('RETURN_BOUNDED_PREFIX',
                Original(raw.status,raw.headers,raw.body[:limit+1],raw.eof,raw.error),
                len(raw.body),v.digest(raw.body)))
        else:
            self.state.originals.append(('RETURN', raw))
        v.need(type(raw) is Original, 'ORIGINAL_TYPE')
        body = raw.body
        v.need(type(body) is bytes, 'BODY_TYPE')
        self.state.summaries.append({'status':raw.status if type(raw.status) is int else None,
                                     'count':len(body), 'sha256':v.digest(body),
                                     'eof':raw.eof is True, 'error':raw.error is not None})
        v.need(self.clock() < self.deadline, 'LATE_RETURN')
        v.need(len(body) <= limit, 'OVERSIZE')
        v.need(raw.error is None and raw.eof is True, 'INCOMPLETE_OR_ERROR')
        v.need(type(raw.status) is int and type(raw.headers) is dict, 'RESPONSE_SCHEMA')
        lengths=[value for key,value in raw.headers.items() if str(key).lower()=='content-length']
        v.need(len(lengths)<=1 and (not lengths or lengths[0]==str(len(body))), 'CONTENT_LENGTH')
        return raw

    def json(self, suffix):
        raw=self.call(v.BASE+suffix)
        v.need(raw.status == 200, 'METADATA_STATUS')
        self.metadata_raw[suffix]=raw.body
        return v.parse(raw.body,v.RECORD_MAX)

    def log(self, job):
        raw=self.call(v.BASE+'/actions/jobs/'+str(job)+'/logs')
        v.need(raw.status==302, 'LOG_REDIRECT_STATUS')
        locations=[value for key,value in raw.headers.items() if str(key).lower()=='location']
        v.need(len(locations)==1 and type(locations[0]) is str, 'LOCATION_SCHEMA')
        location=locations[0]
        parsed=urlsplit(location)
        v.need(parsed.scheme=='https' and parsed.hostname and parsed.username is None
               and parsed.password is None and parsed.fragment=='' and parsed.port in (None,443), 'LOCATION_URL')
        # No production allowlist exists here. Test policy is explicitly synthetic;
        # approval of a JSON field, environment claim or this hash is not admission.
        v.need(self.redirect_policy is not None and self.redirect_policy(location) is True,
               'REDIRECT_UNBOUND')
        result=self.call(location,v.LOG_MAX,download=True)
        v.need(result.status==200, 'LOG_DOWNLOAD_STATUS')  # nested redirects refused
        result.body.decode('utf-8','strict')
        return result.body


def blob_sha(body):
    return hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()


def qualify_synthetic(provider, target, bindings, clock, deadline, state=None,
                      synthetic_redirect_policy=None):
    """No native provenance or authority can be returned by this test-only route."""
    state=state if state is not None else PrivateState()
    try:
        v.need(state.validator.first_unknown is None, 'PREVIOUS_UNKNOWN')
        preflight(target,bindings)
        v.need(callable(clock) and type(deadline) in (float,int) and math.isfinite(deadline), 'CLOCK')
        v.need(0 < deadline-clock() <= 300, 'WINDOW')
        r=Reader(provider,state,clock,deadline,synthetic_redirect_policy)
        b=bindings
        run=r.json('/actions/runs/'+str(target.run_id))
        v.need(run['id']==target.run_id and type(run['id']) is int
               and run['run_attempt']==target.attempt and type(run['run_attempt']) is int, 'RUN_BINDING')
        v.need(run['repository']['id']==v.RID and run['repository']['full_name']==v.REPO
               and run['repository']['owner']['id']==v.OWNER, 'RUN_REPOSITORY')
        v.need(run['status']=='completed' and run['conclusion']=='success'
               and run['head_sha']==b['source'], 'RUN_TERMINAL_SOURCE')
        # Membership in this attempt comes from the attempt-scoped endpoint;
        # job GET alone need not expose run_attempt in documented responses.
        jobs=r.json('/actions/runs/'+str(target.run_id)+'/attempts/1/jobs?per_page=100')
        v.need(type(jobs['total_count']) is int and 0 < jobs['total_count'] <= 100
               and len(jobs['jobs'])==jobs['total_count'], 'JOBS_COMPLETE')
        members=[j for j in jobs['jobs'] if type(j.get('id')) is int and j['id']==target.job_id]
        v.need(len(members)==1, 'JOB_ATTEMPT_MEMBERSHIP')
        job=r.json('/actions/jobs/'+str(target.job_id))
        for candidate in (members[0],job):
            v.need(type(candidate['id']) is int and candidate['id']==target.job_id
                   and type(candidate['run_id']) is int and candidate['run_id']==target.run_id
                   and candidate['head_sha']==b['source'] and candidate['status']=='completed'
                   and candidate['conclusion']=='success', 'JOB_BINDING')
            steps=candidate['steps']
            v.need(type(steps) is list and 0<len(steps)<=100
                   and all(s['status']=='completed' and s['conclusion']=='success' for s in steps), 'STEP_TERMINAL')
        normalized={**run,'repository_id':run['repository']['id'],
                    'owner_id':run['repository']['owner']['id'], 'actor_id':run['actor']['id'],
                    'triggering_actor_id':run['triggering_actor']['id']}
        writer={**job,'attempt':target.attempt}
        source=r.json('/git/commits/'+b['source'])
        v.need(source['sha']==b['source'] and sha40(source['tree']['sha']), 'SOURCE_COMMIT')
        tree=r.json('/git/trees/'+source['tree']['sha']+'?recursive=1')
        v.need(tree['sha']==source['tree']['sha'] and tree['truncated'] is False, 'SOURCE_TREE')
        observed={}
        for path,key in ((v.WORKFLOW,'workflow_sha256'),('qualification/native27.py','driver_sha256'),
                         ('qualification/native27_validator42.py','validator_sha256')):
            entries=[e for e in tree['tree'] if e['path']==path and e['type']=='blob']
            v.need(len(entries)==1 and sha40(entries[0]['sha']), 'SOURCE_PATH')
            entry=entries[0];obj=r.json('/git/blobs/'+entry['sha'])
            v.need(obj['encoding']=='base64' and obj['sha']==entry['sha'], 'BLOB_ENCODING')
            raw=base64.b64decode(obj['content'].replace('\n',''),validate=True)
            v.need(len(raw)<=v.RECORD_MAX and type(obj['size']) is int and obj['size']==len(raw)
                   and blob_sha(raw)==entry['sha'] and v.digest(raw)==b[key], 'SOURCE_PIN')
            observed[key]=v.digest(raw)
        main=r.json('/git/ref/heads/main');observed['main']=main['object']['sha']
        v.need(main['ref']=='refs/heads/main' and main['object']['type']=='commit'
               and observed['main']==b['source'], 'MAIN_SOURCE')
        log=r.log(target.job_id)
        commit=r.json('/git/commits/'+b['commit']);newtree=r.json('/git/trees/'+b['tree'])
        ref=r.json('/git/ref/'+v.REF[len('refs/'):])
        v.check_body(2,r.metadata_raw['/git/commits/'+b['commit']],b)
        v.check_body(3,r.metadata_raw['/git/trees/'+b['tree']],b)
        v.check_body(5,r.metadata_raw['/git/ref/'+v.REF[len('refs/'):]],b)
        observed.update(commit=commit['sha'],tree=newtree['sha'],ref_commit=ref['object']['sha'])
        now=clock();remaining=min(deadline-now,300-(now-v.timestamp(run['run_started_at'])))
        v.need(remaining>0, 'WINDOW_EXPIRED')
        receipt=v.validate(log,normalized,writer,observed,now,remaining,state.validator)
        return Readback('SYNTHETIC_ONLY_NOT_NATIVE',receipt,b['source'],target.run_id,target.job_id)
    except Exception as error:
        state.originals.append(('PRIMARY_EXCEPTION',error))
        state.fail(str(error) if isinstance(error,v.Refuse) else 'READBACK_EXCEPTION')


def native_readback(*args, **kwargs):
    # Concrete transport60 exists, but its authentic native factory is inactive.
    # Caller arguments never install authority or trigger credential lookup.
    from native27_transport60 import native_factory
    return native_factory()

if __name__=='__main__':
    raise SystemExit('INACTIVE59_NATIVE_HOST_REDIRECT_AND_ADMISSION_UNBOUND')
