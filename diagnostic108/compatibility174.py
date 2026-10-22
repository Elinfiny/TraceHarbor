"""Explicit153 compatibility, unchanged historical delegates."""
import pathlib,runpy
R=pathlib.Path(__file__).resolve().parent
old=runpy.run_path(str(R/'compatibility168.py'));new=runpy.run_path(str(R/'compatibility153.py'))
def validate165(release,config,manifest_bytes,snapshot):return (new if config['prestart154'].get('direction_number')==153 else old)['validate165'](release,config,manifest_bytes,snapshot)
def project166(raw_admission,raw_current,evidence):return new['project166'](raw_admission,raw_current,evidence)
