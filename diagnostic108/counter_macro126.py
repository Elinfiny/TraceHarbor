"""Complete INACTIVE singlecounter graph; no dispatch or runtime release126.

The exact58primitive lowerbound already exceeds current prospective48 before
evidence/waits. This executable planner refuses arming instead of inventing a
fit flag or silently enlarging the current grant.
"""
import importlib.util,pathlib,json
ROOT=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('trace126_macro_control',ROOT/'control126.py');ctl=importlib.util.module_from_spec(spec);spec.loader.exec_module(ctl)
FIXED_CLOCKS={'job':900,'main':720,'worker':170,'ready':5,'cleanup':10,'proof':15,'initial_runner_admit':150,'host_initial_admit':135,'main_admit':45,'prequal':200,'recipient':25,'allchecks_reserve':680,'hostbegin_reserve':610,'postprequal_reserve':320}
def whole_graph126():
 return {'prearm':[{'operation':'SOURCE_FREEZE','CAS':1,'readback':1,'before':'actual original once/clock/source/checks'}],'semantic':[{'ordinal':i,'operation':name,'CAS':1,'readback':1,'Gitcreate':int(i in range(2,10) or i in range(11,15)),'immediate_whole_created_proof_GET':int(i in range(2,10) or i in range(11,15))} for i,name in enumerate(('PRE_DISPATCH','ADMIT_DESCRIPTOR','ADMIT_BLOB','ADMIT_TREE','ADMIT_COMMIT','ADMIT_REF','ENCRYPTED_BLOB','ENCRYPTED_TREE','ENCRYPTED_COMMIT','ENCRYPTED_REF','CONSUMED_DESCRIPTOR','CONSUMED_BLOB','CONSUMED_TREE','CONSUMED_COMMIT','CONSUMED_REF','TERMINAL'))], 'protected_chain':['actualcurrent source/pins/Owner/repo/once + supportedexisting UI dispatch binding','actualselectedrun/canonicalparent/fulltree/attempt + ADMIT','freshrecipient25/allchecks680/hostbegin610 + authenticatedprivate6 delivery','completeencryptedwholeproof + durableCONSUMED BEFORE anyreadyrelease','actualsameNativeProducer/q/consumedproof/mountUID65532 + ready5 API0 + ONEofflinecounter','STOP/cleanup10 + wholecounter/SAFEvalidation/provisionalproof15 receipt + actualpostIOopaqueclosure','minimalpublicprojection ordinarypostSAFEinsideoriginal900/onceexpiry','actualcompletedprovider run/job/source/tree + selectedartifactdigest + positiveLibrarywholebytes/ALLattrs + typedHOSTSAFEfactory','ordinaryTERMINAL AFTER SAFEproof INSIDE remainingoriginal900/onceexpiry, separately budgeted']}
def prospect126():
 graph=whole_graph126();counts={'owned_CAS':17,'pinned_whole_readbacks':17,'Gitcreates':12,'immediate_whole_created_proofs':12};result=ctl.InclusiveBudget126(48).plan(counts)
 result.update(graph=graph,fixed_clocks=FIXED_CLOCKS,minimum_before_source_jobs_artifacts_captures_waits_crypto_helpers=58,native_fit=False,actual_missing_bindings=['Independentreview + actualpublishedsource/sourcefreeze/full16macrodispatcher/source-pinnedUIactuator withCURRENTMasterterminal/noinputconflict','Complete inclusivecallbudget: lowerbound58>prospective48 even before fullactualsource/delivery/guard/capture/wait costs','Observedpair19.914 makes5pairs99.570 beforeGit/helpers/guards; consumed110forecaststillUNFIT','Actualcurrent nativeq/ONEcounter/source/once/private6custody/cost/nooverage/lateusage/project facts','Currentnativeproviderfactories require new actualowned ADMIT_NATIVE_SAFE126_PROVIDER_DELIVERY + macro/source/manifest freeze; absentunder126'])
 return result
def require_whole_admission126():
 result=prospect126()
 if not result['fit']:raise RuntimeError('Whole inclusivecontrol budget UNFIT before ANY original clock/dispatch/effect: '+str(result['total'])+' >48')
 return result
