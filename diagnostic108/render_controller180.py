"""SOURCE177 PRIVATE REVIEW CANDIDATE: explicit154 only; historical source delegates retained. No admission/effect at import."""
"""Build one reviewed functions.exec lexical controller from exact source files.
No import or rendering starts a native process. Output is code, never authority.
"""
from pathlib import Path
import json, hashlib
ROOT = Path(__file__).resolve().parent
IMPORT = "import {bootstrapActualCaller127,observerPlan146,drive127,outerConsumer180} from './caller180.mjs';"

def render146():
    files = ['outer146.mjs', 'metadata180.mjs', 'caller180.mjs', 'controller180.mjs']
    parts = []
    pins = {}
    for name in files:
        raw = (ROOT / name).read_bytes()
        s = raw.decode()
        pins[name] = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
        if name == 'controller180.mjs':
            if s.count(IMPORT) != 1:
                raise ValueError('Only exact local source import may be bundled')
            s = s.replace(IMPORT, '')
        if name == 'caller180.mjs':
            local="import {publishOuter180,descriptor180} from './metadata180.mjs';"
            if s.count(local)!=1:raise ValueError('Exact metadata source import')
            s=s.replace(local,'')
        if any((line.startswith('import ') for line in s.splitlines())):
            raise ValueError('No unresolved or external import in actual lexical controller')
        s = '\n'.join((line[7:] if line.startswith('export ') else line for line in s.splitlines()))
        parts.append(s)
    code = '\n'.join(parts) + '\nreturn {runControlled146,claimActualWait146,retainActualWait146,observerCall146};'
    return {'schema': 'TRACE146_EXEC_LEXICAL_BUNDLE', 'full_source_utf8': code, 'source_pins': pins, 'bytes': len(code.encode()), 'sha256': hashlib.sha256(code.encode()).hexdigest(), 'binding_arguments': ['tools', 'notify'], 'native_authority': False}
if __name__ == '__main__':
    print(json.dumps(render146(), sort_keys=True, separators=(',', ':')))
