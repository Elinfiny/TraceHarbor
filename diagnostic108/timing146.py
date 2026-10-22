"""Prospective146 finite schedule. Data and validation never grant native access."""
import copy,math
SCHEMA='TRACE146_FINITE_TIMING_V1'
ZERO_COST146={'model_calls':0,'spend':0,'host_cost_bound':0}
def zero_cost146():return copy.deepcopy(ZERO_COST146)
PARENT=2340
CAS=75
DISPATCH=60
READINESS=240
RECIPIENT=90
CHAIN=210
COLLECTION=1020
RUNNER_ADMIT=285
INIT_RESERVE=max(865,RUNNER_ADMIT+685)
ADMIT_MIN=CHAIN+READINESS+RECIPIENT+CHAIN+CHAIN+COLLECTION+CAS
ENCRYPTED_MIN=CHAIN+CHAIN+COLLECTION+CAS
CONSUMED_MIN=CHAIN+COLLECTION+CAS
CONTRACT={'schema':SCHEMA,'parent_s':PARENT,'job_minutes':39,'whole_CAS_s':CAS,'provider_frame_s':15,'metadata_pair168':__import__('runpy').run_path(str(__import__('pathlib').Path(__file__).resolve().parent/'metadata168.py'))['CONTRACT'],'helpers_writer_s':10,'helpers_other_s':5,'dispatch_selection_s':DISPATCH,'ref_absence_s':15,'host_admit_s':CHAIN,'runner_admit_s':RUNNER_ADMIT,'recipient_readiness_s':READINESS,'recipient_prepare_s':RECIPIENT,'encrypted_s':CHAIN,'consumed_s':CHAIN,'consumed_readiness_s':600,'main_s':720,'worker_s':170,'prequal_s':200,'cleanup_s':10,'proof_s':15,'always_cleanup_s':60,'upload_s':60,'collection_s':COLLECTION,'collection_offsets_s':[0,300,600,900],'terminal_CAS_s':CAS,'host_admit_min_s':ADMIT_MIN,'encrypted_min_s':ENCRYPTED_MIN,'consumed_min_s':CONSUMED_MIN,'runner_init_min_s':INIT_RESERVE,'allchecks_reserve_s':680,'hostbegin_reserve_s':610,'postprequal_reserve_s':320,'late_provider':'FIRST_ORIGINAL_UNKNOWN_NO_RETRY','queue':'EXACT_CREATE_SELECTION_WITHIN60_OR_STOP'}
def validate146(x):
 if x!=CONTRACT:raise ValueError('Exact independent prospective146 timing contract required')
 return copy.deepcopy(CONTRACT)
def schedule146(contract=None):
 q=validate146(CONTRACT if contract is None else contract)
 # Controller dependency chain; collection includes the parallel runner tail,
 # not another serial720. Four observations cover a <=870s runner tail;
 # last at900 leaves120 for six provider calls and byte/identity validation.
 nodes=[('source_freeze',75,[]),('predispatch_CAS',75,['source_freeze']),('ref_absence',15,['predispatch_CAS']),('create_selection',60,['ref_absence']),('dispatch_postvalidate',15,['create_selection']),('admit',210,['dispatch_postvalidate']),('recipient_readiness',READINESS,['admit']),('recipient_prepare',90,['recipient_readiness']),('encrypted',210,['recipient_prepare']),('consumed',210,['encrypted']),('collection_join_runner',1020,['consumed']),('terminal',75,['collection_join_runner'])]
 ends={};rows=[]
 for name,duration,deps in nodes:
  start=max((ends[x] for x in deps),default=0);ends[name]=start+duration;rows.append({'name':name,'maximum_s':duration,'depends_on':deps,'earliest_start_bound_s':start,'finish_bound_s':ends[name]})
 # Explicit overlap: runner starts at create; admission waits for host.admit;
 # public acquisition overlaps encrypted/consumed; readiness is availability
 # only and returns within30s of consumed (15s cadence +15s single read).
 runner_tail=30+720+60+60
 if runner_tail>900 or ends['terminal']>q['parent_s']:raise TimeoutError('Whole finite dependency ledger does not fit')
 return {'schema':'TRACE146_CRITICAL_PATH','controller_nodes':rows,'critical_path_s':ends['terminal'],'parent_s':q['parent_s'],'slack_s':q['parent_s']-ends['terminal'],'parallel_runner_tail_after_consumed_s':runner_tail,'overlap':['runner bootstrap and selection','runner admit and host admit','public acquisition and encrypted/consumed','runner main/cleanup/upload inside collection join'],'native_authority':False}
def reject_legacy146(parent=900,init_reserve=865,dispatch_window=60):
 if parent<init_reserve+dispatch_window:raise TimeoutError('Legacy900 cannot fit865+60 before CAS/startup')
 return True
def preallocate146(config):
 validate146(config['timing_contract']);r=schedule146()
 if config['observer_contract']!={'schema':'TRACE146_DURABLE_OBSERVER_V1','maximum':40,'native_authority':False}:raise ValueError('Supported precommitted durable observer contract before holder')
 return r
class OriginalClock146:
 """One immutable dual-clock origin. No renewal API or external clock selector."""
 def __init__(self,wall,mono,parent=PARENT):
  if parent!=PARENT or not all(type(v) in (int,float) and math.isfinite(v) for v in (wall,mono)):raise ValueError('Exact finite original146 origin')
  self.origin=(wall,mono);self.end=(int(wall)+parent,mono+int(wall)+parent-wall);self.last=(wall,mono)
 def require(self,wall,mono,minimum=0):
  if wall<self.last[0] or mono<self.last[1]:raise TimeoutError('Clock rollback; no renewed parent')
  self.last=(wall,mono)
  if min(self.end[0]-wall,self.end[1]-mono)<minimum:raise TimeoutError('Original146 whole suffix reserve')
  return min(self.end[0]-wall,self.end[1]-mono)
