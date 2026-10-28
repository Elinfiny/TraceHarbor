"""Persistent append-only reservations; UNKNOWN and successful calls both stay spent.
No auto-bootstrap, reset, decrement, retry or restoration over existing markers.
POSIX flock serializes independent processes; O_EXCL/fsync persists before dispatch.
"""
import os,stat,json,fcntl,re,hashlib
from pathlib import Path
from contextlib import contextmanager
from release_policy import canonical,digest,validate_config,deadline,Refusal

def private_dir(p):
    p=Path(p)
    if not p.is_absolute() or os.name!='posix' or any(x.is_symlink() for x in (p,*p.parents)):raise Refusal('PRIVATE_DIRECTORY')
    s=p.stat()
    if not stat.S_ISDIR(s.st_mode) or s.st_uid!=os.getuid() or s.st_mode&0o077:raise Refusal('PRIVATE_DIRECTORY')
    return p

def syncdir(p):
    fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)

def exclusive(p,obj):
    fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'wb') as f:f.write(canonical(obj));f.flush();os.fsync(f.fileno())
    syncdir(p.parent)

def read(p,limit=4096):
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb') as f:
        s=os.fstat(f.fileno())
        if not stat.S_ISREG(s.st_mode) or s.st_uid!=os.getuid() or s.st_mode&0o077 or s.st_size>limit:raise Refusal('LEDGER_PRIVATE_FILE')
        b=f.read(limit+1)
    try:return json.loads(b)
    except Exception:raise Refusal('LEDGER_CORRUPT') from None

class ReservationUnknown(Refusal): pass

class Ledger:
    @staticmethod
    def provision(path,config):
        """Trusted future provisioning only. Never used by request handling."""
        validate_config(config);p=Path(path);private_dir(p.parent)
        os.mkdir(p,0o700) # existing allocations may NEVER be replaced
        exclusive(p/'allocation.json',{'config_sha256':digest(config),'allocation_id':config['allocation_id']})
        exclusive(p/'lock',{'schema':'traceharbor.ledger-lock.v1'})
        syncdir(p.parent)
        return Ledger(p,config)
    def __init__(self,path,config):
        self.config=dict(validate_config(config));self.path=private_dir(path)
        if read(self.path/'allocation.json')!={'config_sha256':digest(config),'allocation_id':config['allocation_id']}:raise Refusal('LEDGER_CONFIG_PIN')
        read(self.path/'lock')
    @contextmanager
    def locked(self):
        fd=os.open(self.path/'lock',os.O_RDWR|os.O_NOFOLLOW)
        try:
            fcntl.flock(fd,fcntl.LOCK_EX);yield
        finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
    def scan(self):
        names={p.name for p in self.path.iterdir()}
        if 'halt.json' in names:raise Refusal('LEDGER_SUSPENDED_VERSION_DRIFT')
        if any(n not in {'allocation.json','lock'} and not re.fullmatch(r'(?:slot|terminal)-\d{3}\.json',n) for n in names):raise Refusal('LEDGER_UNEXPECTED_FILE')
        slots=sorted(n for n in names if n.startswith('slot-'))
        if len(slots)>256 or slots!=[f'slot-{i:03}.json' for i in range(1,len(slots)+1)]:raise Refusal('LEDGER_SEQUENCE')
        total=0;requests=set()
        for n in slots:
            x=read(self.path/n)
            if set(x)!={'slot','request_sha256','reserve_nanodollars','config_sha256','state'} or x['slot']!=int(n[5:8]) or x['config_sha256']!=digest(self.config) or x['state']!='RESERVED_UNKNOWN_NO_RETRY' or not re.fullmatch('[a-f0-9]{64}',x['request_sha256']) or type(x['reserve_nanodollars']) is not int or not 360060<=x['reserve_nanodollars']<=851520 or x['request_sha256'] in requests:raise Refusal('LEDGER_CORRUPT')
            total+=x['reserve_nanodollars'];requests.add(x['request_sha256'])
        for n in names:
            if n.startswith('terminal-'):
                x=read(self.path/n);i=int(n[9:12])
                if i<1 or i>len(slots) or set(x)!={'slot','request_sha256','state'} or x['slot']!=i or x['state'] not in {'UNKNOWN_CONSUMED_NO_RETRY','VERIFIED_RECORD_SEMANTICS_NOT_VERIFIED'} or x['request_sha256']!=read(self.path/f'slot-{i:03}.json')['request_sha256']:raise Refusal('TERMINAL_CORRUPT')
        if total>self.config['budget_nanodollars']:raise Refusal('LEDGER_BUDGET_CORRUPT')
        return len(slots),total,requests
    def reserve(self,request_sha,cost,now=None):
        deadline(self.config,now)
        if not re.fullmatch('[a-f0-9]{64}',request_sha) or type(cost)is not int or not 360060<=cost<=851520:raise Refusal('RESERVATION_SHAPE')
        with self.locked():
            count,total,seen=self.scan()
            if request_sha in seen or request_sha in self.config['blocked_request_sha256']:raise Refusal('ALREADY_RESERVED_NO_RETRY')
            if count>=self.config['call_limit'] or total+cost>self.config['budget_nanodollars']:raise Refusal('QUOTA_EXHAUSTED')
            x={'slot':count+1,'request_sha256':request_sha,'reserve_nanodollars':cost,'config_sha256':digest(self.config),'state':'RESERVED_UNKNOWN_NO_RETRY'}
            try:exclusive(self.path/f'slot-{count+1:03}.json',x)
            except FileExistsError:raise Refusal('ALREADY_RESERVED_NO_RETRY') from None
            except OSError:raise ReservationUnknown('RESERVATION_UNKNOWN_NO_RETRY') from None
            return x
    def terminal(self,reservation,success):
        with self.locked():
            self.scan();i=reservation['slot'];old=read(self.path/f'slot-{i:03}.json')
            if old!=reservation:raise Refusal('RESERVATION_MISMATCH')
            exclusive(self.path/f'terminal-{i:03}.json',{'slot':i,'request_sha256':old['request_sha256'],'state':'VERIFIED_RECORD_SEMANTICS_NOT_VERIFIED' if success else 'UNKNOWN_CONSUMED_NO_RETRY'})
    def halt(self,reason):
        if reason not in {'COUNTER_USAGE_DRIFT','RELEASE_REVOKED'}:raise Refusal('HALT_REASON')
        with self.locked():exclusive(self.path/'halt.json',{'state':'CLOSED_NO_RESET','reason':reason})
    def snapshot(self):
        with self.locked():n,c,_=self.scan();return {'reserved_calls':n,'reserved_nanodollars':c,'remaining_calls':256-n,'retry':False}
