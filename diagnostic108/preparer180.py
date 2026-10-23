"""Pure source-owned outer descriptors, no A/B or effect at import."""
from pathlib import Path
import runpy
ROOT=Path(__file__).resolve().parent
def outer_descriptors180(config,binding,expected_version):
 if type(expected_version)is not int or expected_version<=0 or binding.get('direction_number')!=154:raise ValueError('Exact actual unused154 preparation')
 h=runpy.run_path(str(ROOT/'prestart177.py'));writer=Path(binding['writer_path']);derived,_=h['derive154'](Path(binding['original_writer_path']).read_text(),binding['auditor_version'])
 if writer.read_text()!=derived:raise ValueError('Exact original writer six substitutions')
 capture=Path(config['path_roles']['capture']);transfer=Path(config['path_roles']['transfer']);root=Path(binding['binding_root'])
 base={'kind':'NATIVE_OUTER','native_authority':False,'sourceRoot':str(ROOT.parent),'helper':config['path_roles']['library_helper'],'configPath':config['path_roles']['config']}
 return {phase:dict(base,phase=phase,captureDirectory=str(capture/('outer180-RX_START'))if phase=='RX_START'else str(capture),destination=str(transfer/('outer180-'+phase+'-readback')),prepublishDirectory=str(transfer/('outer180-'+phase+'-prepublish')),expectedVersion=expected_version if phase=='RX_START'else None,candidate=str(root/('candidate'+str(expected_version+1))/'TraceHarbor_V1_checkpoint.json')if phase=='RX_START'else None)for phase in('RX_START','TERMINAL')}
