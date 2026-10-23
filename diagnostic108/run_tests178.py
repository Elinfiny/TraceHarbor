"""One portable run, deduplicated test IDs, no historical83 or live effects."""
import unittest,runpy,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R));loader=unittest.TestLoader();cases={}
for name in('test177.py','test177_publish.py','test178.py'):
 ns=runpy.run_path(str(R/name))
 for value in ns.values():
  if isinstance(value,type)and issubclass(value,unittest.TestCase)and value is not unittest.TestCase:
   for case in loader.loadTestsFromTestCase(value):
    # PublishGuard inherits13 WholeAdapter tests; their behavior/fixture is identical.
    key=('WholeAdapter.'+case._testMethodName)if case._testMethodName in ns.get('f',{}).get('WholeAdapter',type('None',(),{})).__dict__ else type(case).__name__+'.'+case._testMethodName
    cases.setdefault(key,case)
result=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(cases.values()))
print(json.dumps({'scope':'SYNTHETIC_DATA_ONLY_NO_NATIVE_EFFECT','unique':len(cases),'executions':result.testsRun,'failures':len(result.failures),'errors':len(result.errors)}));sys.exit(not result.wasSuccessful())
