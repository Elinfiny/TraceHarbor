"""Private48 finite custody. Completion requires exact acknowledged final custody.
Partial data and unknown writes stay retained; no reset, resume or retry API.
"""
import hashlib,os,threading
from quota_ledger import private_dir,exclusive,syncdir
from release_policy import Refusal
MAX_MASTER=25165824
class MediaSink:
 def __init__(self,path,*,admitted=False):
  if admitted is not True:raise Refusal('CAPTURE_NOT_ADMITTED')
  self.path=private_dir(path);self.bytes=0;self.next=0;self.terminal=False;self.lock=threading.Lock()
  exclusive(self.path/'custody.json',{'schema':'traceharbor.capture48.v1','classification':'SYNTHETIC_ONLY','seconds':164,'byte_limit':MAX_MASTER})
 def append(self,sequence,chunk,sha256):
  with self.lock:
   if self.terminal or type(sequence)is not int or sequence>=700 or sequence!=self.next or type(chunk)is not bytes or not chunk or len(chunk)>1048576 or self.bytes+len(chunk)>MAX_MASTER or hashlib.sha256(chunk).hexdigest()!=sha256:raise Refusal('CAPTURE_BOUND_OR_SEQUENCE')
   fd=os.open(self.path/f'chunk-{sequence:05}.webm',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
   try:
    with os.fdopen(fd,'wb')as f:f.write(chunk);f.flush();os.fsync(f.fileno())
    syncdir(self.path);exclusive(self.path/f'chunk-{sequence:05}.json',{'sequence':sequence,'bytes':len(chunk),'sha256':sha256})
   except Exception:self.terminal=True;raise Refusal('CAPTURE_WRITE_UNKNOWN')from None
   self.bytes+=len(chunk);self.next+=1;return {'sequence':sequence,'bytes':len(chunk),'sha256':sha256}
 def finish(self,elapsed,reason,custody):
  with self.lock:
   if self.terminal or type(elapsed)not in{int,float}or not 0<=elapsed<=180 or reason not in{'STOP164','BOUND','CANCEL','ERROR'}:raise Refusal('CAPTURE_TERMINAL')
   keys={'received_bytes','reserved_bytes','acked_bytes','reserved_chunks','acked_chunks','pending_bytes','pending_chunks','dropped_bytes','failure'}
   if type(custody)is not dict or set(custody)!=keys or type(custody['failure'])is not bool or any(type(v)is not int or v<0 for k,v in custody.items()if k!='failure'):raise Refusal('CAPTURE_CUSTODY_SHAPE')
   complete=(reason=='STOP164'and elapsed>=164 and not custody['failure'] and custody['pending_bytes']==custody['pending_chunks']==custody['dropped_bytes']==0 and custody['received_bytes']==custody['reserved_bytes']==custody['acked_bytes']==self.bytes and custody['reserved_chunks']==custody['acked_chunks']==self.next and self.next>0)
   self.terminal=True;x={'schema':'traceharbor.capture-terminal48.v1','elapsed':elapsed,'reason':reason if reason!='STOP164'or complete else 'ERROR','bytes':self.bytes,'chunks':self.next,'client_custody':custody,'state':'CAPTURED_NOT_AV_VERIFIED'if complete else 'PARTIAL_NO_RETRY','public':False,'retry':False};exclusive(self.path/'terminal.json',x);return x
