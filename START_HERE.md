# TraceHarbor — offline test build

This public source test build uses synthetic, handwritten fixtures. It makes no model calls.
Fixture results are not real Nebius inference, visual QA or contest submission evidence.

## Start locally

1. Extract the separately published source archive. Open the extracted repository root.
2. Use Python 3.12 or later. `python --version` must show a supported version.
   No packages, SDKs, accounts, API keys or internet connection are needed for fixture mode.
3. Open a terminal in the same directory as this guide and `app.py`, then run:

```sh
python app.py serve --port 8787
```

The working directory now contains `app.py`, `fixtures/`, `references/` and `web/`.
Open `http://127.0.0.1:8787` in a separately permitted local browser. The server
binds to loopback. Stop it with Ctrl+C. No server or browser was started to package this build.
Do not use a tunnel or bypass a browser URL restriction.

Select Full, Missing or Conflicting evidence. These labels correspond to
`fixtures/complete.json`, `fixtures/missing.json` and `fixtures/contradictory.json`.
Follow citations, export a dossier, then use Verify imported dossier.
Use synthetic input only; never import secrets or production logs.

## Optional offline command-line export

From the same `TraceHarbor` working directory, with no server required:

```sh
python app.py analyze fixtures/missing.json --out missing-dossier.json
```

The output path must not already exist: export is create-only. Preserve an existing
output and choose a different absent filename for another export.

## Live integration remains inactive

Do not execute `live_probe.py` or populate `live-admission.example.json` as part of
offline setup. Its null/empty admission fields remain unchanged and refuse live admission.
No API key is included. No real approval, spending authorization or model result is supplied.
Remaining live prerequisites: model-specific JSON-object capability, verified pre-inference
token/template bounds (proposed maximum 3000 input/1500 output per case), effective credit
exhaustion/spending-stop evidence, and separately reviewed exact three-case admission.

## Release status

Public source is published at https://github.com/Elinfiny/TraceHarbor, with verified
commit `18a98b4aa6c9264e56d18e77e107dacc92eb0aed`. The separately verified offline
build has SHA-256 `92b740d86b1766547feaa086c956a2ce992d74af5b0248aa9db05dde8300af97`.
The actual public GitHub Download ZIP remains unverified; it is distinct from that offline build.
Downloadable source is not a hosted demo. Supported visual QA, actual admitted Nebius runtime
evidence, a recorded public video under three minutes and final contest submission remain pending.
`VIDEO_SCRIPT.md` is a 160-second script, not a video. `SUBMISSION_DRAFT.md` is a draft.
Existing release materials do not establish completed live inference, visual QA, video publication or contest submission.

Application, fixtures, adapters, probe, tests and LICENSE preserve the accepted offline
candidate bytes. Only publication documentation and its derived manifest differ.
This root-level guide uses the source-repository layout. The separately accepted private
offline ZIP and its original guide remain unchanged. The existing public source URL is given above.
