"""One closed, source-produced inclusive inventory; source preparation only.

All tickets are committed before any original protected clock. Partitioned
consumers cannot allocate another counter or refund unused tickets. A native
admission must name this ENTIRE inventory, not just the36 provider lower bound.
"""
import json,hashlib,importlib.util,pathlib,copy
can=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
sha=lambda b:hashlib.sha256(b).hexdigest()
_s=importlib.util.spec_from_file_location('trace127_accepted_control126',pathlib.Path(__file__).with_name('control126.py'));accepted=importlib.util.module_from_spec(_s);_s.loader.exec_module(accepted)
DiskOriginalIO127=accepted.DiskOriginalIO126
PHASES=('SOURCE_FREEZE','PRE_DISPATCH','ADMIT_CHAIN','ENCRYPTED_CHAIN','CONSUMED_CHAIN','TERMINAL')
SEMANTIC=('PRE_DISPATCH','ADMIT_DESCRIPTOR','ADMIT_BLOB','ADMIT_TREE','ADMIT_COMMIT','ADMIT_REF','ENCRYPTED_BLOB','ENCRYPTED_TREE','ENCRYPTED_COMMIT','ENCRYPTED_REF','CONSUMED_DESCRIPTOR','CONSUMED_BLOB','CONSUMED_TREE','CONSUMED_COMMIT','CONSUMED_REF','TERMINAL')
FIXED={'job':900,'main':720,'worker':170,'ready':5,'cleanup':10,'proof':15,'initial_runner_admit':150,'initial_host':135,'encrypted':110,'consumed':110,'main_admit':45,'prequal':200,'recipient':25,'allchecks_reserve':680,'hostbegin_reserve':610,'postprequal_reserve':320,'collection':150}
def inventory127():
 rows=[]
 def row(id,kind,owner='HOST',closure=False):rows.append({'id':id,'kind':kind,'owner':owner,'closure':closure})
 # Each remote primitive has one canonical original saved by the controller
 # BEFORE one callback, one callback original, and two host frame facts.
 # Bounded IPC saves up to8 actual read chunks. Syscalls inside a single
 # declared source method are not platform calls; every evidence method is.
 remote=[]
 for phase in PHASES:remote.extend((phase+'/CAS',phase+'/readback'))
 remote+=['dispatch/UI','dispatch/run']
 for phase in ('admit','encrypted','consumed'):
  for kind in ('blob','tree','commit','ref'):remote.extend((phase+'/'+kind,phase+'/'+kind+'/proof'))
 remote+=['recipient/run','recipient/list','recipient/download','recipient/materialize']
 remote += ['collection/run/'+str(n) for n in range(4)]
 remote += ['safe/commit','safe/tree','safe/jobs','safe/list','safe/download','safe/materialize']
 for id in remote:
  closure=id.startswith('TERMINAL/')
  for suffix,kind,owner in [('tool','native','CONTROLLER'),('canonical','local_evidence','CONTROLLER'),('callback','callback','CONTROLLER'),('callback-original','local_evidence','CONTROLLER'),('request','local_evidence','HOST'),('return','local_evidence','HOST'),('validated','local_evidence','HOST'),('restore','local_evidence','HOST')]:row(id+'/'+suffix,kind,owner,closure)
  for n in range(8):row(id+'/chunk/'+str(n),'local_evidence','HOST',closure)
  row(id+'/canonical-reference','local_evidence','HOST',closure)
  for suffix in ('failure-partial','failure-status','failure-read','failure-duplicate'):row(id+'/'+suffix,'local_evidence','HOST',True)
 for phase in PHASES:
  for id in ('guard-before','writer','attrs-candidate','attrs-upload','attrs-readback','guard-after'):
   # helperstart + its retained terminal + source/whole verification. These
   # count underlying starts inside the holder, not merely its exec cell.
   row(phase+'/'+id,'host_start',closure=phase=='TERMINAL');row(phase+'/'+id+'/original','local_evidence',closure=phase=='TERMINAL')
  for id in ('intent','writer-input','candidate-verify','transfer-copy','readback-verify','phase-close','phase-close-readback'):row(phase+'/'+id,'local_evidence',closure=phase=='TERMINAL')
 for n in range(16):row('semantic/'+str(n),'local_evidence')
 for phase in ('admit','encrypted','consumed'):
  for kind in ('blob','tree','commit','ref'):row(phase+'/'+kind+'/pre-effect-guard','local_evidence')
 for n in range(3):row('collection/delay/'+str(n),'wait','HOST')
 row('controller/functions-exec','orchestration','CONTROLLER')
 for n in range(16):
  row('observer/'+str(n),'wait','OBSERVER');row('observer/'+str(n)+'/original','local_evidence','OBSERVER');row('observer/'+str(n)+'/intent','local_evidence','OBSERVER');row('observer/'+str(n)+'/claim-cell','orchestration','OBSERVER');row('observer/'+str(n)+'/original-cell','orchestration','OBSERVER')
 for id in ('preflight/materialize','preflight/materialize-original','preflight/exec','preflight/process','preflight/exec-original','holder/start','holder/start-original','holder/terminal','holder/terminal-original','preload/verify','source/verify','custody/guard','recipient/verify','ingress/source','ingress/openssl/0','ingress/openssl/1','ingress/openssl-original','ingress/proof','collection/begin','collection/close','safe/file-attrs','safe/file-original','safe/verify','stop/original','failure/original','closure/original'):
  row(id,'host_start' if id in ('holder/start','preflight/process','ingress/openssl/0','ingress/openssl/1') else 'native' if id in ('preflight/materialize','preflight/exec') else 'local_evidence','CONTROLLER' if id.startswith(('holder/','preflight/')) else 'HOST',id in ('failure/original','closure/original','holder/terminal','holder/terminal-original'))
 #128 source-owned additions: actual in-process helper originals and finite
 # pre-protected-clock polling/closure. ONE inventory, no cap amendment.
 for n in range(3):row('preflight/helper-original128/'+str(n),'local_evidence','CONTROLLER')
 for n in range(8):
  row('preflight/poll128/'+str(n),'native','CONTROLLER');row('preflight/poll-original128/'+str(n),'local_evidence','CONTROLLER')
 row('preflight/collection-close128','local_evidence','CONTROLLER',True)
 for id in ('recipient/verify','safe/file-original'):row(id+'/helper-original128','local_evidence','HOST')
 assert len({r['id'] for r in rows})==len(rows)
 return {'schema':'TRACE127_WHOLE_PRECOMMITTED_INVENTORY_V1','rows':rows,'inclusive_total':len(rows),'current_comparison_cap':48,'current_fit':len(rows)<=48,'proposal_only_cap':len(rows),'authority':False,'reserved_closure':sum(r['closure'] for r in rows),'observer_maximum':16,'immutable_semantic_graph':list(SEMANTIC),'phase_graph':list(PHASES),'remote_ids':remote}
class Inventory127:
 def __init__(self,plan,realm,admitted_cap=48):
  expected=inventory127()
  if plan!=expected:raise ValueError('Exact entire executable source inventory, no caller budget edits')
  if realm!='SYNTHETIC_SOURCE_ONLY' and (admitted_cap<expected['inclusive_total'] or admitted_cap!=expected['proposal_only_cap']):raise PermissionError('Current48 UNFIT; exact prospective inventory requires independent admission')
  self.plan=copy.deepcopy(plan);self.realm=realm;self.rows={r['id']:r for r in plan['rows']};self.claimed=set();self.first_unknown=None;self.test_limit=None
 def claim(self,id,owner='HOST'):
  r=self.rows.get(id)
  if not r or r['owner']!=owner or id in self.claimed:raise RuntimeError('No absent/foreign/duplicate ticket')
  if self.first_unknown is not None and not r['closure']:raise RuntimeError('First UNKNOWN, only original retention/closure escrow remains')
  if self.test_limit is not None and sum(not self.rows[x]['closure'] for x in self.claimed)>=self.test_limit and not r['closure']:raise RuntimeError('Inclusive evidence/wait/callback cap before call; closure escrow protected')
  self.claimed.add(id);return copy.deepcopy(r)
 def unknown(self,error):
  if self.first_unknown is None:self.first_unknown=error
 def remote_bundle(self,id):
  # Controller has no allocating budget: same exact precommitted ticket IDs.
  ids=[id+'/'+s for s in ('tool','canonical','callback','callback-original')]
  for x in ids:self.claim(x,'CONTROLLER')
  return [self.rows[x] for x in ids]
class OriginalStore127:
 def __init__(self,root,io,inventory):self.root=pathlib.Path(root);self.io=io;self.inventory=inventory;self.records={}
 def save(self,id,original,owner='HOST'):
  raw=can({'identity':id,'original':original});path=str(self.root/(sha(id.encode())+'.original.json'))
  if id in self.records:
   if self.io.read(path)!=raw:raise RuntimeError('No memory-only alias/canonical original changed')
   return self.records[id]
  self.inventory.claim(id,owner)
  try:
   self.io.write_once(path,raw)
   if self.io.read(path)!=raw:raise RuntimeError('Whole durable original readback')
  except BaseException as exc:self.inventory.unknown({'original_io_error':type(exc).__name__,'id':id});raise
  r={'id':id,'path':path,'bytes':len(raw),'sha256':sha(raw)};self.records[id]=r;return r
