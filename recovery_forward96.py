"""Inert preservation verifier. Hashes are custody checks, never authority."""
import hashlib,json,os,stat
from pathlib import Path
from release_policy import Refusal
J=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
H=lambda b:hashlib.sha256(b).hexdigest()
OLD=Path('/var/data/traceharbor-recovery67')
ALLOCATION=Path('/var/data/traceharbor-release68/allocation')
ROOT95_SHA='9b79c4b81b7e5eb029b72a779b1cabbe39885d2910d004277081b6d71c53b34a'
ALLOCATION95_SHA='907976d88f69067708498345599e50a7232ca13fad1575e7c6a8ae678e6fdcce'
def snapshot(root,*,exclude=()):
 p=Path(root);out={}
 if any(q.is_symlink()for q in(p,*p.parents)):raise Refusal('PRESERVATION_SYMLINK')
 for q in sorted(p.rglob('*')):
  rel=str(q.relative_to(p))
  if rel in exclude:continue
  s=q.lstat()
  if q.is_symlink()or s.st_uid!=os.getuid():raise Refusal('PRESERVATION_CUSTODY')
  if stat.S_ISREG(s.st_mode):
   if s.st_nlink!=1:raise Refusal('PRESERVATION_LINK')
   h=hashlib.sha256()
   with q.open('rb')as f:
    while b:=f.read(1048576):h.update(b)
   out[rel]={'bytes':s.st_size,'sha256':h.hexdigest(),'mode':stat.S_IMODE(s.st_mode)}
  elif stat.S_ISDIR(s.st_mode):out[rel]={'directory':True,'mode':stat.S_IMODE(s.st_mode)}
  else:raise Refusal('PRESERVATION_NODE')
 return out

def preserved():
 if H(J(snapshot(OLD)))!=ROOT95_SHA:raise Refusal('WHOLE95_IMMUTABLE_TREE_DRIFT')
 # Exactly new003 append is excluded; old001/002 and absence of terminal002 stay pinned.
 if H(J(snapshot(ALLOCATION,exclude=('slot-003.json','terminal-003.json'))))!=ALLOCATION95_SHA:raise Refusal('CONSUMED001002_DRIFT')
