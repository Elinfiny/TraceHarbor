# Private request correction51 — SYNTHETIC qualification only

Base: `e3a18ef03140edd43d258c298f747d35fc276b1a`, tree `09b26282544315dcb849d79e3dd62b5834cd6b81`.
This candidate changes only nebius.py and adds this note and one new selected test module.

The payload replaces max_tokens=1500 with integer max_completion_tokens=1500.
The exact existing model argument, schema, messages, JSON object format, n=1,
stream=False and store=False remain unchanged. Request hashes consequently change.
Historical admissions, planned hashes, three consumed requests and .spent are never
refreshed, reused or reset by this patch.

project_request_path accepts only the explicit string aiproject-e00d73xwjm884tnvcs.
https_once defaults project_id to None and rejects absent, foreign or malformed
configuration before reading any environment value or constructing HTTP.
The only route is fixed HTTPS api.tokenfactory.nebius.com with path
/v1/chat/completions?ai_project_id=aiproject-e00d73xwjm884tnvcs.
NebiusAdapter also defaults to None, validates before model environment lookup and
passes its explicit project_id to the same transport. There is no project environment
fallback, arbitrary endpoint, default-project inference, retry or redirect.
Routing configuration does not prove credential ownership or grant any execution.

Official sources, read/reported in intake51:

- https://docs.tokenfactory.nebius.com/api-reference/inference/create-chat-completion
  independently retrieved: ai_project_id is the current-project query parameter;
  max_completion_tokens bounds generated completion tokens including reasoning.
  JSON object response format is documented. Generic documentation supports this
  request implementation; model-specific enforcement and complete JSON are unproved.
- https://nebius.com/services/token-factory/models/nvidia-nemotron-models-inference
  Auditor402 reports Nano 262K context and displayed $0.06/M input, $0.24/M output.
  Trace's direct retrieval failed; those statements are Auditor-reported here.
  They do not prove account tariff, ISO currency, enforced financial exposure or grant.
- https://github.com/nebius/token-factory-cookbook/blob/main/models/nemotron/nemotron3-nano-30b.md
  official cookbook locator independently opened; Nano capability details are
  Auditor-reported. Lowercase example IDs or regions do not replace the exact model
  or fixed endpoint in this project.

The new qualification uses actual corrected functions with SYNTHETIC evidence,
schema/core substitutes, process-environment substitute and HTTP connection/response
fakes. Network creation is denied. A fake response/decode is not a provider attestation.
Four methods contain six named subcases; no old test suite is imported or rerun.
Only PRIVATE_INERT_REQUEST_CONTRACT_PASS is admissible from the group.

live_probe.py stays byte-identical at SHA256
dde9b833db536a3385c7a082942401fae4bfe6b87e4179379cad179c435e0061.
Its existing calls omit project_id; the corrected transport therefore refuses.
The consumer itself can still read its existing environment before that call:
this patch does not qualify that consumer or alter its callers/ledger. Native bridge
and gates stay unbound. EXTERNAL_FIRST_GATE, NATIVE42_BINDING and
EXTERNAL_ADMISSION_GATE remain None; PLAN/nativeAdmission=None, inference=HOLD.

The input<=3000 proposal and output1500 are unchanged. Neither advertised 262K context
nor a local request hash proves a billable-input bound or maximum invoice. The 5USD
proposal is not changed or granted. Existing provider paid-stop/inflight/late statements
remain positive account evidence; exact Nano/key association and complete input bounds
remain for independent review. No model call, key lookup, activation, publication,
quota, billing, workflow or public application change is admitted here.
