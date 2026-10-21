"""Build one reviewed functions.exec lexical controller from exact source files.
No import or rendering starts a native process. Output is code, never authority.
"""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
IMPORT="import {bootstrapActualCaller127,observerPlan146,drive127} from './caller127.mjs';"
def render146():
 files=['outer146.mjs','caller127.mjs','controller146.mjs'];parts=[];pins={}
 for name in files:
  raw=(ROOT/name).read_bytes();s=raw.decode();pins[name]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
  if name=='controller146.mjs':
   if s.count(IMPORT)!=1:raise ValueError('Only exact local source import may be bundled')
   s=s.replace(IMPORT,'')
  if any(line.startswith('import ') for line in s.splitlines()):raise ValueError('No unresolved or external import in actual lexical controller')
  s='\n'.join(line[7:] if line.startswith('export ') else line for line in s.splitlines());parts.append(s)
 code='\n'.join(parts)+'\nreturn {runControlled146,claimActualWait146,retainActualWait146,observerCall146};'
 return {'schema':'TRACE146_EXEC_LEXICAL_BUNDLE','full_source_utf8':code,'source_pins':pins,'bytes':len(code.encode()),'sha256':hashlib.sha256(code.encode()).hexdigest(),'binding_arguments':['tools','notify'],'native_authority':False}
if __name__=='__main__':print(json.dumps(render146(),sort_keys=True,separators=(',',':')))
