"""Pure inactive preparation. Generates no nonce, runtime marker or grant.

Exact source publication and real fresh once/current custody/cost facts are
inputs at their independently admitted boundary, never guessed from JSON.
"""
import pathlib,json,hashlib,copy,importlib.util,sys
ROOT=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('trace127_plan_control',ROOT/'control127.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
def prepare127(config,context,manifest_bytes):
 inventory=c.inventory127();ctx=copy.deepcopy(context);cfg=copy.deepcopy(config)
 if any(ctx.get(k) is None for k in ('source_sha','source_tree','manifest_sha256','once_receipt_sha256','expires_utc','initial_version')):raise ValueError('Actual new source/unusedonce context required; null template is deliberately not instantiable')
 if ctx['manifest_sha256']!=c.sha(manifest_bytes):raise ValueError('Actual final manifest bytes')
 phase_sha=c.sha(c.can({'context':ctx,'inventory':inventory,'graph':list(c.SEMANTIC),'phases':list(c.PHASES)}));cfg['integration_context127']=ctx;cfg['phase_plan_sha256127']=phase_sha;cfg['native_admission127']=None;cfg.pop('config_path',None)
 proposal={'contract':'TRACE127_PHASE_INTENT_V1','manifest_sha256':c.sha(manifest_bytes),'inclusive_cap':inventory['inclusive_total'],'phase_plan_sha256':phase_sha,'config_binding_sha256':c.sha(c.can(cfg)),'scope':'NEW_UNUSED_ONCE_API0_ONLY'}
 cfg['native_admission127']=proposal
 return {'schema':'TRACE127_INACTIVE_COMPLETE_PREPARATION_V1','native_authority':False,'current48_changed':False,'config':cfg,'proposed_independent_contract_DATA_ONLY':proposal,'inventory':inventory,'exact_entrypoint':'diagnostic108/caller127.mjs:bootstrapActualCaller127 -> drive127 -> native127.py -> provider_safe127.bootstrap -> Grouped127.run_complete','outer_entrypoint':'diagnostic108/outer127.mjs:prepareOuter127/claimActualWait127/retainActualWait127','fixed_clocks':c.FIXED,'actual_nonce_created':False,'actual_admission_markers_published':False}
if __name__=='__main__':
 values=json.loads(pathlib.Path(sys.argv[1]).read_bytes());result=prepare127(values['config'],values['context'],(ROOT/'manifest.json').read_bytes());print(json.dumps(result,sort_keys=True,separators=(',',':')))
