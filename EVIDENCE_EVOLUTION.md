# Evidence Evolution — private candidate 265

This is a deterministic synthetic workflow. It makes no NVIDIA or other AI
request and executes no investigation command or remediation. The original
three reference fixtures and recorded provider response are unchanged.

## Review the flow

In a separately permitted local application environment, run `python3 -B app.py
serve --port 8787` from this source directory. Open the printed loopback URL.
Use **Start evidence evolution**, then **Add captured verification**. The first
action loads an incomplete incident and a precisely scoped next check. The
second reveals one captured synthetic source and its before/after comparison.
**Review a conflicting capture** demonstrates why contrary evidence must keep
the conclusion open. Export and reimport the resulting dossier through the
existing controls. These are setup instructions, not evidence of visual QA.

The server's loopback binding, Host/Origin enforcement, CSP, upload limit and
non-executing remediation boundary remain unchanged. No tunnel, relaxed origin,
remote access or package installation is required or authorized by this guide.

## Data and contract

`scenarios/evolution.json` defines one independent synthetic incident. Its
`before` package uses the existing `traceharbor.input.v1` schema. The captured
source includes an explicit approved/runtime configuration difference and two
threshold-emulator replay records. The workload and harness hashes are equal
across trials; only the task deadline changes. This is documented synthetic
ground truth, not a production experiment or new provider output.

`POST /evolution` accepts exactly `schema`, `before`, `after` and
`expected_before_sha256`. Schema is `traceharbor.evolution-request.v1`. The
expected hash is SHA-256 of canonical UTF-8 `before` JSON (sorted keys, compact
separators, no terminal LF). Both packages must retain the same incident ID and
title. Existing raw sources must remain byte-equivalent as JSON values; only
new source IDs may be appended. Old-source edits/removals are rejected.

The typed event vocabulary is documented by `evolution.FIELDS`. Other source
text remains visible as untrusted data and cannot become instructions. A
configuration difference alone stays UNKNOWN. A matched diff and controlled
same-workload/harness replay pair can produce SUPPORTED_SYNTHETIC_RULE. The
analysis status remains `uncertain`, with provenance limitations, and never
claims general semantic validation. Conflicting configuration samples or
contrary replay outcomes remain CONFLICTED. No confidence percentage is made up.

The export schema `traceharbor.evolution.v1` contains both evidence snapshots,
next-check proposals, exact source/event/quote citations and an additive delta.
`POST /verify` rebuilds every derived field and verifies the whole dossier;
forged quotations/deltas, inconsistent source hashes or edits to earlier sources
fail. Complete evolution exports are bounded to the existing 256 KiB import
limit. All original `/analyze` and imported-provider paths remain available.

SHA-256 is unkeyed integrity, not authorship. A coordinated rewrite of all input
and hashes cannot be authenticated from a standalone file. Supplied capture
provenance, workload hashes and replay claims are not independently attested.
This rule is intentionally narrow; arbitrary incident text receives no general
causal diagnosis. Any live model interpretation would be a distinct, labelled,
separately admitted provider result.

## Targeted checks

`PYTHONPATH=. python3 -B -m unittest discover -s tests -p test_evolution265.py -v`
runs six targets, using only stdlib Python and an optional installed Node syntax
check. Tests use loopback HTTP only, never an inference client. No new dependency
is required. `TEST_RESULTS.json` in the candidate container records actual run
evidence, the one corrected syntax-process resource limitation, RSS and HTTP
latencies. Browser render latency and the first-30-second interaction criterion
remain unmeasured until an admitted real UI route is available.
