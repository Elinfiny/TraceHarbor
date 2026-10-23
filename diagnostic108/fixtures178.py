"""Portable SYNTHETIC DATA_ONLY fixtures; no provider provenance or native grant.
Inputs: this source tree, test_inputs178.json and exact three official helpers.
Set TRACE178_HELPERS to their private directory, or use carrier review/helpers.
Nothing reads another chat's checkpoint or starts a holder/clock/registry.
"""
from pathlib import Path
import json,runpy,copy,hashlib,os
ROOT=Path(__file__).resolve().parent
can=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
sha=lambda x:hashlib.sha256(x).hexdigest()
DATA=json.loads((ROOT/'test_inputs178.json').read_bytes())
assert DATA['scope']=='SYNTHETIC_DATA_ONLY_NOT_PROVIDER_NOT_NATIVE_AUTHORITY'
HELPERS=Path(os.environ.get('TRACE178_HELPERS',str(ROOT.parent.parent/'review/helpers'))).resolve()
CFG=copy.deepcopy(DATA['config_template'])
for name,pin in CFG['publication150']['helpers'].items():
 p=HELPERS/name;raw=p.read_bytes();assert len(raw)==pin['bytes']and sha(raw)==pin['sha256']
 assert p.is_file()and not p.is_symlink()and p.stat().st_uid==os.getuid()and p.stat().st_nlink==1
 os.chmod(p,0o600);pin['path']=str(p)
CFG['path_roles']['library_helper']=str(HELPERS/'library_file_transfer.py')
MB=(ROOT/'manifest.json').read_bytes();CFG['manifest']={'bytes':len(MB),'sha256':sha(MB)}
OWN={'SYNTHETIC_DATA_ONLY_NOT_PROVIDER':True,'native_id':'6acfe37b-828c-83eb-b466-7670beb64ff2','ownership':{'owner':'TraceHarbor V1','duplicate_trace_route_owners':0},'state':'NATIVE153_TERMINAL'}
for n in range(148,154):OWN['native'+str(n)]={'SYNTHETIC_DATA_ONLY_NOT_PROVIDER':True,'phase':'TERMINAL','records':[{'phase':'RX_START','payload':{'synthetic_slot':n}}]}
for n,key in ((153,'predecessor153_sha256'),(152,'preserved152_sha256'),(151,'preserved151_sha256'),(150,'preserved150_sha256'),(149,'preserved149_sha256'),(148,'reserved148_sha256')):CFG['prestart154'][key]=sha(can(OWN['native'+str(n)]))
OLD=copy.deepcopy(CFG);OLD['prestart154']={k:v for k,v in CFG['prestart154'].items()if not k.endswith('_sha256')}
OLD['prestart154'].update(schema='TRACE174_PRESTART153_PREDECESSOR152_V1',direction_number=153,predecessor=152,predecessor_state='NATIVE152_TERMINAL')
for n,key in ((152,'predecessor152_sha256'),(151,'preserved151_sha256'),(150,'preserved150_sha256'),(149,'preserved149_sha256'),(148,'reserved148_sha256')):OLD['prestart154'][key]=sha(can(OWN['native'+str(n)]))
OLD['references156']=runpy.run_path(str(ROOT/'references174.py'))['CONTRACT']
OLDP={'static_CONFIG':OLD,'writer_preview':{'full_original_source_utf8':DATA['public_original_writer3827']}}
def semantic_fixture178(number=154):
 """Full pure predicate data, explicitly incapable of installing registry state."""
 config=copy.deepcopy(CFG if number==154 else OLD)
 body='SYNTHETIC DATA_ONLY pure predicate fixture; NEVER AN ACTUAL OUTBOX OR GRANT'
 release={'id':'V29-TRACE-'+str(number)+'-SYNTHETIC-DATA_ONLY','recipient':'TraceHarbor V1','body':body,'bytes':len(body.encode()),'sha256':sha(body.encode()),'native_admission':True,'SYNTHETIC_DATA_ONLY_NOT_NATIVE_AUTHORITY':True}
 plan=runpy.run_path(str(ROOT/'plan127.py'));config['authority_projection_sha256']=sha(can(plan['projection133'](release)))
 release['grouped146_admission']=plan['prepare127'](config,release,MB)['proposed_admission']
 mod=runpy.run_path(str(ROOT/('compatibility177.py'if number==154 else'compatibility174.py')));a=mod.get('A')or runpy.run_path(str(ROOT/'authority153.py'))
 # Small fully hashed JSON values used only inside the pure predicate.
 doc={'SYNTHETIC_DATA_ONLY_NOT_PROVIDER':True,'guard':{},'operation':{'effect_replay_boundary':{}},'integrity':{'canonical_json_sha256':None}}
 doc['integrity']['canonical_json_sha256']=sha(can(doc));raw=can(doc)
 def proof(stable):return {'library_file_id':stable,'file_id':'file_SYNTHETIC_DATA_ONLY_'+stable,'version':1,'bytes':len(raw),'sha256':sha(raw),'self_sha256':doc['integrity']['canonical_json_sha256'],'ALLattrs':'PASS'}
 aa={k:proof(k)for k in(a['AUDIT'],a['POLICY'],a['ROUTE'])};bb=dict(aa);bb[a['OWN']]=proof(a['OWN'])
 auth={'schema':a['CONTRACT'],'admission_A':aa,'current_B':bb,'allowed_semantic_diff':[],'immutable_guard_auditor_sha256':sha(raw),'current_authority_auditor_sha256':sha(raw),'native_authority':False}
 projector=runpy.run_path(str(ROOT/'compatibility177.py'))
 projection=projector['project166'](raw,raw,auth)
 h=runpy.run_path(str(ROOT/'prestart177.py'));c=h['contract154'](config['prestart154']);ident={'dev':1,'ino':10,'uid':0,'mode':448,'type':'directory'};child=dict(ident,ino=11)
 if number==154:receipt=h['receipt_from_identities178'](config,config['path_roles']['holder_parent'],ident,child)
 else:receipt={'schema':c['schema'],'direction_number':153,'predecessor':152,'reserved_history':148,'parent_path':config['path_roles']['holder_parent'],'parent':ident,'child_path':str(Path(config['path_roles']['holder_parent'])/'holder'),'child':child,'expected_empty':True,'native_authority':False}
 pre={'schema':c['schema'],'prepared_receipt_sha256':sha(can(receipt)),'child_path':receipt['child_path'],'child':child,'empty':True,'native_authority':False}
 snap={'SYNTHETIC_DATA_ONLY_NOT_NATIVE_AUTHORITY':True,'direction':release,'ownership':'TraceHarbor V1','direction_number':number,'authority152':auth,'compatibility_projection166':projection,'compatibility165':{'history':c,'static_config_sha256':sha(can(config)),'source':config['source'],'authority_evidence_sha256':sha(can(auth)),'projection166_sha256':sha(can(projection))},'auditor_sha256':sha(raw),'source_verification':{'Auditor_V28_checkpoint.json':aa[a['AUDIT']]},'writer_sha256':'d'*64,'writer_binding':{'auditor_version':1,'direction_number':number,'direction_id':release['id'],'direction_bytes':release['bytes'],'direction_sha256':release['sha256'],'writer_sha256':'d'*64,'original_writer_sha256':h['ORIGINAL']},'current_source_verification152':bb,'own_version':1,'holder_preparation154':receipt,'prestart154':pre}
 return release,config,MB,snap
