"""NEW123 actual modified entrypoints with explicitly SYNTHETIC originals.
Never imports/reruns old test suites or allocates a native capability.
"""
import pathlib,json,hashlib,importlib.util,tempfile,copy,sys,base64,datetime,time,io,zipfile,os
C=pathlib.Path(__file__).resolve().parents[1];P=C.parent;W=P.parent
spec=importlib.util.spec_from_file_location('subject123',C/'diagnostic108/host_transport118.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
pins=json.load(open(C/'qualification123/pins.json'))
for n,pin in pins['source_files'].items():assert (C/n).stat().st_size==pin['bytes'] and h.sha((C/n).read_bytes())==pin['sha256']
ctx=json.load(open(P/'inert-context123.json'))
def sub(root,name):p=root/name;p.mkdir(mode=0o700);return p
def refused(f,kind=Exception):
 try:f()
 except kind as e:return type(e).__name__
 raise AssertionError('Expected actual entrypoint refusal')
def run(c):return {'id':1230001,'head_sha':c['source_sha'],'run_attempt':1,'actor':{'id':h.OWNER},'repository':{'id':1391430317},'event':'workflow_dispatch','status':'in_progress','run_started_at':datetime.datetime.fromtimestamp(c['parent_expires_utc']-850,datetime.timezone.utc).isoformat()}
def descriptor(c):return {'phase':'admit','source_sha':c['source_sha'],'once_receipt_sha256':c['once_receipt_sha256'],'run_id':1230001,'attempt':1,'expires_utc':c['parent_expires_utc']}
def delivery(c):
 b=b'SYNTHETIC_123_NOT_VENDOR_NOT_ENCRYPTION';return {'context':{'repository':h.REPO,'repository_id':1391430317,'actor_id':h.OWNER,'run_id':1230001,'attempt':1,'source_sha':c['source_sha'],'expires_utc':c['parent_expires_utc'],'nonce':'67'*16,'certificate_sha256':'78'*32},'ciphertext_base64':base64.b64encode(b).decode(),'ciphertext_sha256':h.sha(b),'artifact_digest':'89'*32,'artifact_bytes':1024,'retention_days':1,'custody_sha256':'90'*32}
class DriverFixture:
 def __init__(self,root):
  self.root=root;self.synthetic_clock123=h.SyntheticClock123();self.parent_mono=1000.;self.phase_mono=235.;self.config={'deadline_utc_ms':1900000};c=copy.deepcopy(ctx);c['parent_expires_utc']=1900;self.c=c;self._macro122=h.source_only_macro122(c,sub(root,'macro'));self.calls=[];self.late=False
  p=self._macro122.prepare(h.MacroStep122.PRE_DISPATCH);self.cas_checkpoint(self.current_checkpoint_version,p['payload']);self._macro122.bind_run_original(h.can(run(c)));self._macro122.bind_admit(descriptor(c));self.calls=[]
 @property
 def current_checkpoint_version(self):return self._macro122.snapshot()['version']
 def remaining(self):return min(self.phase_mono-self.synthetic_clock123.monotonic(),self.parent_mono-self.synthetic_clock123.monotonic(),self.config['deadline_utc_ms']/1000-self.synthetic_clock123.time())
 def bind_phase(self,end):
  assert self.synthetic_clock123.monotonic()<end<=self.parent_mono;self.phase_mono=end
 def deadline(self):
  if self.remaining()<=0:raise h.HostUnknown('Synthetic actual phase deadline')
 def cas_checkpoint(self,version,payload):
  m=self._macro122;d={'scope':'SYNTHETIC_SOURCE_ONLY','payload':payload,'self_sha256':None};d['self_sha256']=h.selfhash(d);raw=h.can(d);r={'status':'succeeded','library_file_id':h.OWN,'version':version+1,'file_id':'file_SYNTHETIC123_'+str(version+1),'sha256':h.sha(raw),'self_sha256':d['self_sha256'],'wholebyte_self_allattrs':'PASS'};m.journal_original(h.can(r),raw);self.calls.append('CAS');self.synthetic_clock123.elapse(200 if self.late else .01);return r
 def call(self,tool,args):
  m=self._macro122;m.begin_git(tool,args);kind=tool.removeprefix('github_create_')
  if kind=='blob':raw=base64.b64decode(args['content']);r={'sha':h._gitblob122(raw),'size':len(raw),'encoding':'base64','content':args['content']}
  elif kind=='tree':r={'sha':hashlib.sha1(h.can(args)).hexdigest(),'truncated':False,'tree':copy.deepcopy(self.c['baseline_entries'])+args['tree_elements']}
  elif kind=='commit':r={'sha':hashlib.sha1(h.can(args)).hexdigest(),'author':{'id':h.OWNER},'committer':{'id':h.OWNER},'parents':[{'sha':args['parent_sha']}],'commit':{'tree':{'sha':args['tree_sha']}}}
  else:r={'ref':'refs/heads/'+args['branch_name'],'object':{'sha':args['sha'],'type':'commit'}}
  m.git_original(h.can(r),h.can(r));self.synthetic_clock123.elapse(.01);self.calls.append(tool);return r
def case1(root):
 t=DriverFixture(sub(root,'driver'));h.advance_macro_phase122(t,h.MacroPhase122.ADMIT);closed=t._phase_lifecycle123.snapshot();assert closed['closed']==['ADMIT'] and closed['active'] is None
 t.synthetic_clock123.elapse(140);assert t.remaining()<0 and t.parent_mono-t.synthetic_clock123.monotonic()>610
 t._phase_lifecycle123.begin_recipient();t._macro122.bind_delivery_original(h.can(delivery(t.c)));t.synthetic_clock123.elapse(1);t._phase_lifecycle123.mark_validated_original();t._phase_lifecycle123.close()
 h.advance_macro_phase122(t,h.MacroPhase122.ENCRYPTED);h.advance_macro_phase122(t,h.MacroPhase122.CONSUMED)
 t._controller_safe123=h.ControllerSafeObservation123(h._CONTROLLER_SAFE_SEAL123,t,t._macro122,{'SAFE':'YES','consumer':'STOPPED','cleanup':'COMPLETE','T':None,'scope':'SYNTHETIC_SOURCE_ONLY'});h.advance_macro_phase122(t,h.MacroPhase122.TERMINAL)
 assert t._macro122.snapshot()['cursor']==16 and len([x for x in t.calls if x=='CAS'])==15 and len([x for x in t.calls if x.startswith('github_')])==12
 return {'actual_modified_driver':'advance_macro_phase122','closed':t._phase_lifecycle123.snapshot()['closed'],'original_parent_unchanged':[t.parent_mono,t.config['deadline_utc_ms']],'old_closed_deadline_passed_next_parent_admission':'PASS','synthetic_scope_only':True}
def case2(root):
 r=[];t=DriverFixture(sub(root,'unfinished'));l=h.PhaseLifecycle123(t,t._macro122);l.begin(h.MacroPhase122.ADMIT);r.append(refused(lambda:l.begin(h.MacroPhase122.ENCRYPTED),h.HostUnknown));r.append(refused(l.close,h.HostUnknown));assert not t.calls
 a=DriverFixture(sub(root,'late'));a.late=True;r.append(refused(lambda:h.advance_macro_phase122(a,h.MacroPhase122.ADMIT),h.HostUnknown));assert len(a.calls)==1 and a._macro122.snapshot()['first_unknown'] is not None;r.append(refused(lambda:h.advance_macro_phase122(a,h.MacroPhase122.ENCRYPTED),h.HostUnknown));assert len(a.calls)==1
 b=DriverFixture(sub(root,'reorder'));r.append(refused(lambda:h.advance_macro_phase122(b,h.MacroPhase122.ENCRYPTED),h.HostUnknown));assert not b.calls
 return {'unfinished_late_reorder_UNKNOWN_nofollowon':r,'actual_entrypoint_effects':0}
def case3(root):
 r=[]
 for name,mono,wall in [('insufficient',181.,1000.),('wall_expired',100.,1900.),('mono_expired',1000.,1000.)]:
  t=DriverFixture(sub(root,name));t.synthetic_clock123.mono_value=mono;t.synthetic_clock123.wall_value=wall;r.append(refused(lambda:h.advance_macro_phase122(t,h.MacroPhase122.ADMIT),h.HostUnknown));assert not t.calls
 t=DriverFixture(sub(root,'sourceonly_unknown'));refused(lambda:t._macro122.unknown('SYNTHETIC'),h.HostUnknown);r.append(refused(lambda:h.advance_macro_phase122(t,h.MacroPhase122.ADMIT),h.HostUnknown));assert not t.calls
 return {'original_parent_wall_mono_insufficient_UNKNOWN_refusals':r}
class ArtifactFixture(h.HostTransport):
 def __init__(self,root,variant='valid'):
  self.variant=variant;self.config={'domain':'SOURCE_ONLY123','run_id':1230001,'deadline_utc_ms':int(time.time()+180)*1000};self.source=ctx['source_sha'];self.parent_mono=time.monotonic()+180;self.phase_mono=self.parent_mono;self.counts={'GitGET':0,'Gitwrites':0,'CAS':0,'materialize':0};self.reserved=set();self.apply_count=0;self.library_args=None
  private=sub(root,'private');transfer=sub(root,'transfer');parent=sub(root,'host');self.root=sub(parent,'holder');layout={role:{'path':str(p),'dev':p.stat().st_dev,'ino':p.stat().st_ino,'uid':p.stat().st_uid,'type':'directory'} for role,p in [('private',private),('transfer',transfer),('holder_parent',parent)]};self.config['writer_binding']={'binding_root':str(private),'transfer_layout':layout};self.layout=layout
  self.public={'context':dict(delivery(dict(ctx,parent_expires_utc=self.config['deadline_utc_ms']//1000))['context'])};self.public['context']['source_sha']=self.source
  buff=io.BytesIO()
  with zipfile.ZipFile(buff,'w',zipfile.ZIP_DEFLATED) as z:z.writestr('recipient-public.json',h.can(self.public))
  self.raw=buff.getvalue();self.bridge=self.synthetic_bridge
 def synthetic_bridge(self,op,args):
  if op=='github_fetch':return run(dict(ctx,parent_expires_utc=self.config['deadline_utc_ms']//1000))
  if op=='github_fetch_workflow_run_artifacts':return {'total_count':1,'artifacts':[{'id':123,'name':'traceharbor-recipient104-1230001-1','expired':False,'size_in_bytes':len(self.raw),'workflow_run':{'id':1230001,'head_sha':self.source},'digest':'sha256:'+h.sha(self.raw)}]}
  if op=='github_download_workflow_artifact':return {'file_id':'file_SYNTHETIC123_ARTIFACT','file_name':'recipient118.zip','library_file_id':'libfile_SYNTHETIC123_ARTIFACT'}
  assert op=='library_materialize';self.library_args=args;destination=pathlib.Path(args['destination']['directory']);path=destination/'recipient118.zip'
  if self.variant=='symlink':path.symlink_to(pathlib.Path(self.layout['private']['path'])/'not-read')
  else:path.write_bytes(self.raw)
  return {'file_id':'file_WRONG' if self.variant=='wrongref' else 'file_SYNTHETIC123_ARTIFACT','file_name':'recipient118.zip','library_file_id':'libfile_SYNTHETIC123_ARTIFACT','workspace_path':str(self.root/'not-read') if self.variant=='wrongpath' else str(path),'xattrs':[{'name':'user.library-file-version','value':'0'}]}
 def apply_attrs(self,path,metadata):
  self.apply_count+=1;os.setxattr(path,'user.library-file-id',metadata['library_file_id'].encode())
  for x in metadata['xattrs']:os.setxattr(path,x['name'],x['value'].encode())
def case4(root):
 t=ArtifactFixture(sub(root,'artifact'));r=t.authenticated_artifact_zip(1230001,'traceharbor-recipient104-1230001-1',time.monotonic()+30,8192);d=pathlib.Path(t.library_args['destination']['directory']);transfer=pathlib.Path(t.layout['transfer']['path']);assert d.parent==transfer and not d.is_relative_to(t.root) and t.apply_count==1 and r['zip_bytes']==t.raw
 for role in ['private','holder_parent']:assert pathlib.Path(t.layout[role]['path']).stat().st_mode&0o777==0o700
 return {'actual_modified_artifact_entrypoint':'PASS','destination':d.name,'disjoint':True,'all_fixture_refs':'SYNTHETIC_NOT_PROVIDER','native_effects':0}
def case5(root):
 r=[]
 for variant in ['wrongref','wrongpath','symlink']:
  t=ArtifactFixture(sub(root,variant),variant);r.append(refused(lambda:t.authenticated_artifact_zip(1230001,'traceharbor-recipient104-1230001-1',time.monotonic()+30,8192)));assert t.apply_count==0
 r.append(refused(lambda:h.normalizer({'structuredContent':{'transfers':[{},{}]}},'library_materialize'),h.HostUnknown))
 return {'actual_ref_path_symlink_multiple_before_bytes_refusals':r,'native_effects':0}
def case8(root):
 t=object.__new__(h.HostTransport);t._checkpoint=W/'trace123-transfers/admin-readback436/TraceHarbor_V1_checkpoint.json';t._version=436;t.config={'direction_number':123,'writer_binding':json.load(open(P/'binding123.json'))};cfg=t.config
 actual=h.current_binding(t._checkpoint,436,cfg);assert actual['number']==123 and actual['direction']['id'].startswith('V28-TRACE-123-')
 r=[refused(lambda:h.current_binding(t._checkpoint,436,cfg,require_plan=True,payload={'phase':'PUBLISH_INTENT'}),ValueError),refused(lambda:h.bind_reviewed_macro122(t,sub(root,'no_runtime_release')),ValueError)]
 return {'actual_current_direction123_nonmacro_strict_and_no_runtime_release':r,'administrative_producer_actual_proof':'ONLY_AFTER_ALL8CASES; NOTCLAIMED_HERE'}
if __name__=='__main__':
 number=int(sys.argv[1]);assert number in (1,2,3,4,5,8)
 with tempfile.TemporaryDirectory(prefix='trace123-case'+str(number)+'-') as d:result=globals()['case'+str(number)](pathlib.Path(d))
 print(json.dumps({'NEW123case':number,'PASS':True,'scope':'SYNTHETIC_SOURCE_ONLY_ACTUAL_MODIFIED_ENTRYPOINTS','result':result,'native_effects':0},sort_keys=True))
