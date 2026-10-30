"""Distinct AUTH004. No new effect is authorized on import or by a fixture.
Credential generation/entry and native Share remain distinct protected gestures.
"""
import datetime,hashlib,math,re,time
from pathlib import Path
from quota_ledger import read,exclusive,private_dir
from release_policy import digest,Refusal
import source_extension004 as g
import worker_scope004 as w
EPOCH='TRACEHARBOR-AUTH004'
def operator_path(m):
 if m.root!=g.ROOT:raise Refusal('EXACT_AUTH004_ROOT')
 return m.root/'auth004'

def authority(m):
 import credit_scope004 as scope,render_recorded_release70 as launch
 scope.assert_parent(m);v=g.read(g.ROOT/'source004/extension004.json');s,b=v['spec'],v['bindings'];g.validate_bindings(s,b,m.clock())
 a=g.read(g.ROOT/'recovery-authority004.json');ident=w.identity()
 g.need(a=={'schema':'traceharbor.authority004.v1','scope':EPOCH,'effects':g.effects(),'spec_sha256':g.H(g.J(s)),'source_commit':b['published_commit'],'source_tree':b['published_tree'],'policy_sha256':s['policy_sha256'],'finance205_sha256':g.FINANCE,'expires':b['technical_owner']['expires']},'EXACT004_AUTHORITY')
 g.need(ident['source_commit']==b['published_commit']and launch.CREDIT004_SHA256==s['contract_sha256']and launch.ADMISSION_SHA256==s['initial_sha256']and digest(m.p)==s['policy_sha256'],'CURRENT004_SOURCE_AUTHORITY')
 g.source_check(Path(__file__).parent,s['source_pins'],runtime_required=True);g.bootstrap_readback(s);g.check_history(s['history'])
 g.need(m.p['request_sha256']==g.REQUEST and m.p['certificate']==s['counter']and m.config==m.p['release_config'],'004_REQUEST_CONFIG_BINDING')
 return a

def grant(m):raise Refusal('USE_EXACT_HASH_ONLY_ISSUE004_NO_AUTOMATIC_GRANT')

def issue_once(m,presence,reservation,credential_sha256):
 import credit_scope004 as scope
 a=authority(m);scope.idle(m);scope.ledger(m,unspent=True);scope.codec(m);w.assert_startup()
 now=m.clock();g.need(g.DEADLINE-now>=3600 and a['expires']-now>=1800,'COMPLETE_DELIVERY_TIME_REQUIRED_BEFORE004_ISSUE')
 g.need(presence.get('state')=='ACTUAL_OWNER_PRESENT_FOR_RECOVERY004'and bool(presence.get('canonical_source'))and type(presence.get('at'))in(int,float)and 0<=now-presence['at']<=120,'ACTUAL_OWNER004_PRESENT')
 g.need(reservation.get('state')=='RESERVED_NOT_DISPATCHED'and reservation.get('dispatch_count')==0 and reservation.get('max_dispatches')==1 and reservation.get('spec_sha256')==a['spec_sha256']and bool(reservation.get('canonical_source'))and reservation.get('credential_sha256')==credential_sha256,'EXACT004_GRANT_RESERVATION')
 g.need(type(credential_sha256)is str and re.fullmatch('[a-f0-9]{64}',credential_sha256),'SHA256_ONLY_NO_RAW_CREDENTIAL')
 path=operator_path(m);private_dir(path);g.need(m.operator.path==path and not any((path/n).exists()for n in('grant.json','grant-consumed.json','session.json')),'004_AUTH_ALREADY_CONSUMED_OR_PARTIAL')
 exclusive(path/'grant.json',{'scope':EPOCH,'sha256':credential_sha256,'expires':min(now+1800,a['expires']),'spec_sha256':a['spec_sha256'],'retry':False})
 return {'state':'AUTH004_HASH_ONLY_GRANT_ISSUED_ONCE','expires':min(now+1800,a['expires']),'retry':False}

def metadata_context(m):
 import credit_scope004 as scope
 a=authority(m);scope.idle(m);scope.ledger(m,unspent=True);w.assert_startup()
 g.need(m.operator.path==operator_path(m)and m.operator.remaining()>=1500 and(operator_path(m)/'grant-consumed.json').exists(),'AUTH004_SESSION_BEFORE_METADATA')
 base=m.root/'credit-observations';private_dir(base)
 g.need(not list(base.iterdir())and not(m.root/'metadata004-reserved.json').exists()and not(m.root/'metadata004-complete.json').exists(),'004_ONE_METADATA_ALREADY_USED')
 return a

def prepare_metadata(m,reservation):
 a=metadata_context(m)
 g.need(reservation.get('state')=='RESERVED_NOT_DISPATCHED'and reservation.get('dispatch_count')==0 and reservation.get('max_dispatches')==1 and reservation.get('spec_sha256')==a['spec_sha256']and bool(reservation.get('canonical_source')),'ONE_METADATA004_RESERVATION')
 # This finite preparation precedes the UI timestamp. No writes or timer here.
 return {'schema':'traceharbor.metadata004.component.v1','spec_sha256':a['spec_sha256'],'identity':w.identity(),'session_sha256':g.H(g.raw(operator_path(m)/'session.json')),'global_observation':5,'local_observation':1,'reservation':reservation}

def append_observation(m,v,component=None):
 import standard_billing004
 a=metadata_context(m);g.need(type(component)is dict and component.get('schema')=='traceharbor.metadata004.component.v1'and component.get('spec_sha256')==a['spec_sha256']and component.get('identity')==w.identity()and component.get('session_sha256')==g.H(g.raw(operator_path(m)/'session.json'))and component.get('global_observation')==5 and component.get('local_observation')==1,'PREPARED_METADATA004_COMPONENT_REQUIRED')
 z=component.get('reservation',{});g.need(z.get('state')=='RESERVED_NOT_DISPATCHED'and z.get('dispatch_count')==0 and z.get('max_dispatches')==1 and z.get('spec_sha256')==a['spec_sha256']and bool(z.get('canonical_source')),'METADATA004_ACTUAL_RESERVATION')
 standard_billing004.validate_observation(m,v,120)
 # No review/Library/provider UI pause is inserted after observation time.
 exclusive(m.root/'metadata004-reserved.json',{'state':'UNKNOWN_CONSUMED_NO_RETRY','component_sha256':digest(component),'retry':False})
 exclusive(m.root/'credit-observations'/(digest(v)+'.json'),v)
 exclusive(m.root/'metadata004-complete.json',{'state':'ONE_GLOBAL5_LOCAL1_METADATA_RETAINED','observation_sha256':digest(v),'session_sha256':component['session_sha256'],'retry':False})
 return {'state':'FRESH_METADATA004_RETAINED_NOT_INFERENCE','observation_sha256':digest(v),'retry':False}
