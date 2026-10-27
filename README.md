# TraceHarbor

An incident evidence desk for synthetic cases. Inspect a timeline, compare hypotheses,
follow exact citations, see what remains unknown, and export a verifiable dossier.
Remediation is always a proposal; this application cannot execute it.

## Current delivery — 25 October 2026

TraceHarbor has two distinct paths:

- **Offline evidence desk:** complete, missing and conflicting synthetic cases,
  timelines, exact quotations, dossier export and verified reimport. This path is
  deterministic, makes no model calls and needs no key, account or payment.
- **Recorded NVIDIA/Nebius result:** the first verified provider record came from
  one separately admitted runtime call to `nvidia/Nemotron-3_5-Lightning` through
  Nebius Token Factory. Its result is **unknown**, with empty hypotheses and empty
  remediation. That is valid abstention and an inconclusive result, not a proven
  cause or a deterministic reference verdict.

The exact integration source is commit
`b6ba287704350a304dc6a57760a4103def57d2eb`:
https://github.com/Elinfiny/TraceHarbor/tree/b6ba287704350a304dc6a57760a4103def57d2eb.
The actual native execution is
https://github.com/Elinfiny/TraceHarbor/actions/runs/40206978963,
job https://github.com/Elinfiny/TraceHarbor/actions/runs/40206978963/job/121209913696.
The create event used the repository owner, attempt 1 and that exact source commit.
The job passed its eight pre-secret contract checks, made one request and finished
successfully. HTTP 200 returned 10,630 bytes; reported usage was 1,929 prompt and 1,046
completion tokens, 2,975 total. These are execution facts, not a general model-quality
or causal-validity claim. The four admitted requests are consumed. **Do not rerun
the 190, 200, 214 or 220 workflows/profiles or the archived three-request probe.**
No further inference is part of installation, importing or testing the recorded result.

### Download and run the key-free test build

For installation, use the **delivery commit containing [this README](README.md)
and the [bundled record](examples/recorded/provider_record228.json)**. In that
immutable delivery commit view, choose **Code → Download ZIP**, extract into an
empty directory and change into the directory containing `app.py`, `fixtures/`,
`references/`, `web/` and `examples/`. The earlier `b6ba287…` source link documents
runtime provenance; that commit does not contain the bundled recorded-result file
and is not the delivery download. Obtain the delivery commit hash and its
immutable raw/archive URLs from the actual published commit, never a prospective
self-hash. Use Python 3.12 or later; no package installation, SDK, model weights,
API key or provider payment is needed.
The repository archive is source, not a hosted inference endpoint. Its bytes have
not been newly downloaded or installation-qualified for this update. The separately
accepted `TraceHarbor_OFFLINE_Testbuild175.zip` is a different archive
(102,974 bytes; SHA-256
`e6eb713a79483a41872e8e19bb04898b25a7f6e0f2367169f061d504f962218f`).
Do not present that ZIP as identical to GitHub's source archive; its exact public
binary download URL has not been verified. At the accepted integration commit above, all 19 offline source files match the
accepted175 build. This documentation correction changes the README hash; the
other 18 whole-file hashes remain unchanged. The original README is recoverable
from its archived content and the retained preimage.

In a separately permitted browser environment:

```sh
python3 -B app.py serve --port 8787
```

Open `http://127.0.0.1:8787`, select Full, Missing or Conflicting, inspect exact
citations and export/reimport a dossier. This is a user installation instruction,
not evidence of a new preview, visual QA or permission to bypass a host restriction.
The existing offline CLI also works without starting a server:

```sh
python3 -B app.py analyze fixtures/missing.json
```

For a create-only file export, add `--out` with an absent output filename. Existing
files are intentionally not overwritten. Unknown or contradictory evidence must
remain visible; remediation stays a proposal and cannot execute changes.

### Inspect the real recorded result without another API call

Use the [unchanged provider record](examples/recorded/provider_record228.json) in
this source tree. The relative link resolves within the selected commit; use the
same immutable commit view when downloading the source and record.
The record is 6,426 bytes with SHA-256
`49fda59baa5c0dfeadfd64a12fc28ff4c208da9e01881c68587ef62d259bfc47`.
Save the original bytes, then choose **Verify imported dossier** in the desk.
The existing `/verify` path applies `live_service.verify_import`; importing the
saved result makes no inference call and needs no expiring provider credit.
For an offline terminal check with the unchanged application verifier:

```sh
python3 -B -c 'import json; from pathlib import Path; from live_service import verify_import; d=verify_import(json.loads(Path("examples/recorded/provider_record228.json").read_text(encoding="utf-8"))); print(json.dumps({"mode":d["mode"],"status":d["analysis"]["status"],"semantic_reference":d["verification"]["semantic_reference"]},sort_keys=True,separators=(",",":")))'
```

Expected declarations are `PROVIDER_RESPONSE_RECORD`, `unknown` and `NOT_VERIFIED`.
The record's unkeyed hashes check integrity; the JSON alone does not authenticate
a provider call. Use the separate native job/source/event evidence above for the
runtime claim. Original HTTP-body SHA-256 is
`d909b9f24b69e3b76df74a30c0a8557b4569c59ace75c8b423a0bb784189c214`;
the provider metadata's canonical parsed-response digest is
`fc5179459d2855c1379010b1f56fe43d9ad28589998207b8a840e49c3541ce5c`.
They identify different representations and must not be forced equal.
Raw response bodies, reasoning, credentials and headers are not distributed.

The promised offline functions and recorded-result import have no model-credit
expiry or judge-key requirement. A continuously available inference endpoint is
not promised. These distribution instructions do not establish final contest
eligibility. Application-GUI/video review, final entrant/rights review, video
publication and submission remain open; no final contest entry is claimed.

## Archived 27 September delivery snapshot

The collapsed snapshot below is retained as history. Its date-specific current,
inactive-integration and not-yet-live statements describe 27 September, not the
25 October result above. Its probe/admission examples are historical documentation,
**not current testing instructions or authority to reset consumed operations**.

<details>
<summary>Historical README content — not a current run procedure</summary>

## Current delivery: public source, 27 September 2026

Public source is available at https://github.com/Elinfiny/TraceHarbor. The verified
32-file publication is commit `ebf6843e4bc48316c2652d26820e8c278cf3dd86`:
https://github.com/Elinfiny/TraceHarbor/tree/ebf6843e4bc48316c2652d26820e8c278cf3dd86.
GitHub's observed **Code → Download ZIP** control provides downloadable source, not a
hosted demo; its archive bytes have not been downloaded or verified. The separately
verified offline test-build ZIP has SHA-256
`92b740d86b1766547feaa086c956a2ce992d74af5b0248aa9db05dde8300af97`.
That private build is a distinct artifact, not a verification of GitHub's Download ZIP.

The browser demo is deterministic and makes **no AI calls**. The configurable Nebius
transport and three-request runner are implemented and tested with explicitly simulated
responses. No live Nebius request has been made for this delivery. Read-only account access and the API model identifier
`nvidia/Nemotron-3_5-Lightning` were observed on 27 September 2026. Those observations
are historical, not a promise of session availability or authority to run. Model-specific
JSON-object support, trustworthy pre-inference token bounds and an effective trial-credit
spending stop remain unverified. Existing model/license/rate evidence is separate from
run admission; this update does not refresh it. This is **not yet an eligible live competition submission**.

In the historical local-preview attempt, the cloud browser rejected the local URL with `ERR_BLOCKED_BY_CLIENT` and then an
explicit URL-policy rejection. Browser visual QA is pending; local HTTP verification
passed. No physical mobile or fullscreen test is claimed. Public source publication is
complete; hosted demo delivery, video publication and contest submission remain pending.

## Run locally

Use Python 3.12 or later. Runtime and new tests use only the standard library; no SDK,
model weights, third-party JavaScript, account or network connection is needed for demo mode.

Run these commands from the extracted project root: the directory containing
`app.py`, `fixtures/`, `references/` and `web/`. The source ZIP may add an outer
folder; change into that folder first. `python` must resolve to Python 3.12 or later.
No dependency installation is required.

The following is a launch instruction for a separately permitted viewing environment;
no server or browser preview was started in this documentation review.

```sh
python app.py serve --port 8787
```

Open `http://127.0.0.1:8787` in a browser that supports local applications. The server
binds to loopback and enforces Host/Origin and a restrictive content security policy.
It intentionally exposes no endpoint that invokes a paid model.

```sh
python app.py analyze fixtures/missing.json --out missing-dossier.json
```

The CLI export is create-only; use an absent output filename. The accepted 12-test
integration evidence (not rerun here) covers transport failures, truncation,
model/usage checks, citation tampering, uncertainty, admission limits, three distinct
attempts, replay blocking and HTTP import verification. The accepted 11-test
correction set was also not rerun. Existing test commands remain available to maintainers:
`python -m unittest discover -s tests -p test_nebius_delta.py -v`.
This is separate from offline launch; it is not a required setup step.

## Use the desk

1. Select Full, Missing, or Conflicting evidence. These are handwritten reference cases.
2. Follow a citation to its source. A matching quote proves textual integrity, not causation.
3. Export the dossier. Use **Verify imported dossier** to validate it again.
4. A provider-response record is clearly marked as imported. Its hashes do not prove
   who created it or that the claimed provider invocation happened.

Inputs must be synthetic JSON, at most 256 KiB. Do not import production logs or secrets.
Unknown cases receive no automated diagnosis in demo mode. Source text, including
hostile instructions inside an event, is displayed as text and never executed.

## Live integration: prepared, inactive

`nebius.py` implements the Token Factory chat-completions adapter. The old inert
adapter in `adapters.py` is retained for compatibility with the accepted offline contract;
the live runner uses the new module. `core.py`, `service.py`, `verifier.py`, fixtures and
reference dossiers are unchanged from the accepted base.

The new transport uses the official fixed HTTPS endpoint, reads `NEBIUS_API_KEY` and
`NEBIUS_MODEL` from a secure process environment, follows no redirects and retries no
request. No key is stored in source, a browser, an admission file or an export.
JSON-object mode is requested; the response is checked locally against the accepted
analysis contract. The selected account model must support JSON mode. A provider result
cannot claim the deterministic reference verdict. Missing evidence is required for
uncertain/conflicted results. Exact citations are verified; semantic entailment remains
**NOT_VERIFIED**. Refusals, tool calls, incomplete finish reasons, malformed JSON,
oversized responses and model/usage mismatches are rejected.

Before any live run, the operator must verify existing authentication, the exact NVIDIA
model and its license/JSON capability, current prices, usable credits and an effective
financial cap. A billing charge threshold is not a spending cap. Confirm token upper
bounds with that model's tokenizer, including chat-template overhead; character counts
are not token counts. The prepared request uses deduplicated evidence to limit size.

Copy `live-admission.example.json` into the existing secure execution workspace only
after those facts are independently established. It is valid JSON with the exact fields consumed by `live_probe.admit`, but
intentionally invalid as a live admission and cannot authorize a run as supplied.
Null expiry/evidence/model/prices/cap and empty hash/bound lists mean UNKNOWN, not zero.
The actual parser first refuses its null expiry. Do not add an `enabled` or `approved`
flag: the unchanged parser has no such gate. Keep the template disabled until a
separate reviewed admission; a successful JSON parse is not admission. Fill the actual evidence locators, exact request hashes,
three input-token bounds (each at most 3000), expiry, prices and cap. Generate the hashes
from `live_probe.planned_requests(actual_model)` after binding the exact reviewed code.
This metadata records external verification; the program does not authenticate a
provider account or certify the financial cap from a written assertion.

The proposed, NOT_ADMITTED live probe is three synthetic cases, at most 1500 completion tokens each:

```sh
python live_probe.py --admission /secure/traceharbor/admission.json --out /private/traceharbor/run-01
```

These example paths must refer to existing supported secure storage; the command is not
executed by setup. No new key, card, trial, account, billing plan or infrastructure is
required or created by this code. Do not improvise one to bypass a missing prerequisite.

The runner creates a `.spent` reservation beside the admission file before requests,
then creates an ATTEMPTING receipt before each distinct request. It never retries,
overwrites outputs or resumes an unknown attempt. Keep the reservation and output
directory together on durable private storage. Do not move/delete the marker or mint
a replacement admission to reset this operation. Concurrent invocations using the same
admission path cannot both reserve it. This is a local replay guard, not distributed CAS.
An observed input-token bound violation stops remaining requests and cannot be COMPLETE.
HTTP failures still consume an attempt; they may have incurred provider usage.

## Export, licensing and review

`traceharbor.provider-record.v1` extends the offline dossier without changing its
accepted verifier. It contains the independently rechecked base evidence, model name,
usage, request/response hashes, structured output and integrity checks. Imported records
are unauthenticated data; external execution receipts must substantiate a live claim.

MIT covers this project code and synthetic fixtures. No model weights or third-party
SDK code are bundled. Model/API terms remain separate and must be verified for the actual
selected model. The clean export excludes the original private envelope and reports.
The public source publication is identified above. Preserve the original private archive
and accepted publication commit as distinct historical baselines; neither is live-runtime
or visual-QA evidence.

## Competition materials and outstanding work

`SUBMISSION_DRAFT.md` is the English description; `VIDEO_SCRIPT.md` is a 2:40 script.
The current official rules require a Nebius runtime call and an NVIDIA open-source
model, a usable demo/test build, a public repository with an open-source license and a
video under three minutes. Current submission deadline: 30 October 2026, 17:00 UTC.
Public source is complete. Final review, live evidence, supported visual QA, a recorded
video, its publication and final contest submission remain open. Do not describe simulated
results as live.

Official sources inspected on 23 September 2026:

- https://docs.tokenfactory.nebius.com/quickstart
- https://docs.tokenfactory.nebius.com/api-reference/inference/create-chat-completion
- https://docs.tokenfactory.nebius.com/ai-models-inference/json
- https://docs.tokenfactory.nebius.com/other-capabilities/billing-new
- https://nebiusglobalaihackathon.devpost.com/rules

</details>
