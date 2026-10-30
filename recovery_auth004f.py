"""Distinct AUTH004F. No new effect is authorized on import or by a fixture.
Credential generation/entry and native Share remain distinct protected gestures.
"""
import datetime,hashlib,math,re,time
from pathlib import Path
from quota_ledger import read,exclusive,private_dir
from release_policy import digest,Refusal
import source_extension115 as g
import worker_scope004f as w
EPOCH='TRACEHARBOR-AUTH004F'
def operator_path(m):
 if m.root!=g.ROOT:raise Refusal('EXACT_AUTH004F_ROOT')
 return m.root/'auth004'

def authority(m):
 import session_continuity119 as continuity
 return continuity.authority(m)

def grant(m):raise Refusal('USE_EXACT_HASH_ONLY_ISSUE004_NO_AUTOMATIC_GRANT')

def issue_once(m,presence,reservation,credential_sha256,focus):
 raise Refusal('ORIGINAL_GRANT_IMMUTABLE_USE_DISTINCT_SESSION119_BRANCH')

def metadata_context(m):
 import credit_scope004f as scope
 a=authority(m);scope.idle(m);scope.ledger(m,unspent=True);w.assert_startup()
 g.need(m.operator.path==operator_path(m)and m.operator.remaining()>=1500 and __import__('session_continuity119').has_consumed_session(m,a),'AUTH004F_SESSION_BEFORE_METADATA')
 base=m.root/'credit-observations';private_dir(base)
 g.need(not list(base.iterdir())and not(m.root/'metadata004-reserved.json').exists()and not(m.root/'metadata004-complete.json').exists(),'004_ONE_METADATA_ALREADY_USED')
 return a

def prepare_metadata(m,reservation):
 a=metadata_context(m)
 g.need(reservation.get('state')=='RESERVED_NOT_DISPATCHED'and reservation.get('dispatch_count')==0 and reservation.get('max_dispatches')==1 and reservation.get('spec_sha256')==a['spec_sha256']and bool(reservation.get('canonical_source')),'ONE_METADATA004_RESERVATION')
 # This finite preparation precedes the UI timestamp. No writes or timer here.
 return {'schema':'traceharbor.metadata004.component.v1','spec_sha256':a['spec_sha256'],'identity':w.identity(),'session_sha256':g.H(g.raw(operator_path(m)/'session.json')),'global_observation':7,'local_observation':1,'reservation':reservation}

def append_observation(m,v,component=None):
 import standard_billing004f
 a=metadata_context(m);g.need(type(component)is dict and component.get('schema')=='traceharbor.metadata004.component.v1'and component.get('spec_sha256')==a['spec_sha256']and component.get('identity')==w.identity()and component.get('session_sha256')==g.H(g.raw(operator_path(m)/'session.json'))and component.get('global_observation')==7 and component.get('local_observation')==1,'PREPARED_METADATA004_COMPONENT_REQUIRED')
 z=component.get('reservation',{});g.need(z.get('state')=='RESERVED_NOT_DISPATCHED'and z.get('dispatch_count')==0 and z.get('max_dispatches')==1 and z.get('spec_sha256')==a['spec_sha256']and bool(z.get('canonical_source')),'METADATA004_ACTUAL_RESERVATION')
 standard_billing004f.validate_observation(m,v,120)
 # No review/Library/provider UI pause is inserted after observation time.
 exclusive(m.root/'metadata004-reserved.json',{'state':'UNKNOWN_CONSUMED_NO_RETRY','component_sha256':digest(component),'retry':False})
 exclusive(m.root/'credit-observations'/(digest(v)+'.json'),v)
 exclusive(m.root/'metadata004-complete.json',{'state':'ONE_GLOBAL7_LOCAL1_METADATA_RETAINED','observation_sha256':digest(v),'session_sha256':component['session_sha256'],'retry':False})
 return {'state':'FRESH_METADATA004_RETAINED_NOT_INFERENCE','observation_sha256':digest(v),'retry':False}
