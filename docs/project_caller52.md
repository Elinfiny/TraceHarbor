# Private project caller integration52

Canonical caller preimage: main e3a18ef03140edd43d258c298f747d35fc276b1a,
tree09b26282544315dcb849d79e3dd62b5834cd6b81; live_probe.py6105B,
SHA256 dde9b833db536a3385c7a082942401fae4bfe6b87e4179379cad179c435e0061.
Overlay dependency: accepted PRIVATE51 nebius.py6026B, immutable SHA256
a162f41880dd7621379e93ce932f9b97a7524abf195d70b56b199a51c7fb6fcc,
from libfile_cdc20262b6fc819189e7e590922f608c@0. No51 test is rerun.

Before: execute reads permit/environment and reserves output/.spent, then omits the
project configuration when invoking https_once. With PRIVATE51 that transport refuses.
After: execute(permit_path, output, project_id=None) first calls the accepted pure
project_request_path validator, before permit.resolve/read, environment lookup,
output mkdir, .spent/attempt writes or transport. The actual callsite forwards that
same explicit project_id. CLI exposes --project-id with defaultNone and no environment
fallback. Project configuration is routing, never admission or custody authority.

All existing permit checks, request digest matching, input<=3000 bounds, original
output1500 assumption, budget arithmetic, create-only/fsynced reservation, safe error
format and first non-VERIFIED_RECORD break remain unchanged. New request payload hashes
from51 require distinct future review; old admissions/hashes/three consumed requests,
.spent markers and UNKNOWN outcomes are never changed, imported or reused.

One NEW SYNTHETIC group runs actual execute/admit/planned_requests/write_new/decode_response
against fresh temporary synthetic fixtures, permit and reservation. Core import/schema,
environment, record builder and transport dependencies are synthetic; the positive
assertion inspects all three actual callsite arguments and payloads, not merely the
final record. The absent/foreign/malformed cases reject before every dependent effect.
Separate first-refusal and first-UNKNOWN cases each preserve the synthetic reservation
and stop before attempt2. Real sockets are denied. No live key or provider call occurs.
Only PRIVATE_INERT_PROJECT_CALLER_PASS is an admissible verdict from these tests.

Exact proposed future publication delta against current main is six source paths:
nebius.py from accepted51; live_probe.py from52; tests/test_project_request51.py
from51; tests/test_project_caller52.py from52; docs/nebius_project_request51.md
from51; docs/project_caller52.md from52. These are two modifications and four
additions; this description is not a publication admission. Both immutable51 and new52 source pins must
be reviewed together; do not publish either as independently native-ready.

Native EXTERNAL_FIRST_GATE/NATIVE42_BINDING/EXTERNAL_ADMISSION_GATE stay None.
PLAN/nativeAdmission=None and inferenceHOLD; no native factory/bridge, dispatch,
workflow, model, quota, key/account association or financial activation is changed.
The 5USD proposal, input<=3000 and output1500 are unchanged proposals/bounds in their
existing scopes. Provider model enforcement, key association, complete billable input,
and native durable-once qualification remain separate gates.
