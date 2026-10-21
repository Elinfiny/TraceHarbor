"""Finite pre-frame startup window, distinct from original emitted request15s.
Uses existing recipient_prepare90 budget as one conservative startup ceiling in
outer work3000; not added to parent2340/critical2295 or to any armed frame/phase.
There is no effect, native origin, retry or additional inventory in this module.
"""
import copy,pathlib,runpy
CONTRACT={'schema':'TRACE156_FINITE_FIRST_FRAME_STARTUP_V1','startup_max_ms':90000,'budget_source':'EXISTING_PREPARE90_WITHIN_OUTER_WORK3000','provider_frame_ms':15000,'phase_CAS_ms':75000,'parent_ms':2340000,'outer_total_s':3600,'outer_work_s':3000,'outer_reserve_s':600,'extra_tickets':0,'renewal':False,'authority':False}
def contract156(value):
 timing=runpy.run_path(str(pathlib.Path(__file__).resolve().parent/'timing146.py'))['CONTRACT']
 if CONTRACT['startup_max_ms']!=(timing['whole_CAS_s']+timing['provider_frame_s'])*1000 or CONTRACT['startup_max_ms']!=timing['recipient_prepare_s']*1000:raise ValueError('Derived existing75+15=90 source ceiling')
 if type(value) is not dict or value!=CONTRACT:raise ValueError('Exact finite startup156; no supplied deadline/clock')
 return copy.deepcopy(CONTRACT)
def require_suffix156(elapsed_outer_s,remaining_original_parent_s=None):
 # Startup90 + original full parent2340 + administrative reserve600 <=3600.
 # Must also fit work3000. No extra cap, no parent reset, no inferred grant.
 if type(elapsed_outer_s) not in (float,int) or elapsed_outer_s<0 or elapsed_outer_s+90+2340>3000:raise TimeoutError('Original outer work suffix must fit before source start')
 if remaining_original_parent_s is not None and remaining_original_parent_s<0:raise TimeoutError('Original parent expired')
 return True
