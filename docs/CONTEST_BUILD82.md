# TraceHarbor clean contest test build

This package runs the existing offline synthetic evidence application. It does
not call an AI model. A real NVIDIA runtime through Nebius is still required
for the contest entry. No API key, admission, spend grant, native qualification
state or user evidence is distributed in this build.

Use CPython 3.12. The packaging smoke is qualified on the exact Linux/Python
version in its receipt. Other platforms and versions have not been tested.
No pip install, npm install or optional JWT/crypto package is needed for this
offline application. Internet access is unnecessary after downloading the ZIP.

Extract the ZIP into a new directory. From that directory, launch:

```sh
python3 -B app.py serve --port 8787
```

Open `http://127.0.0.1:8787` in a browser on the same machine. The server binds
only to loopback; it is not a public hosted deployment. Use Complete, Missing
and Conflicting synthetic examples, inspect timeline and sources, export a
dossier and import it for verification. Unknown synthetic inputs abstain.
Press Ctrl+C to stop. These existing UI journeys retain accepted browser QA
run 38650959852, head 8cb31005e01427f87284fa8bf80c6d1c4f96496e/tree
2fdb1fc1bd13cb906481ba7760303c33a1e5142f for byte-identical relevant product
files; they were not rerun in unit 82. Visual aesthetics, video and live
integration acceptance remain separate.

For the offline CLI:

```sh
python3 -B app.py analyze fixtures/missing.json --out new-dossier.json
```

The output must be absent. Use synthetic, nonsecret data only. Hash and citation
checks establish internal consistency, not exporter authentication or causation.

Reproduce the source build from the reviewed checkout:

```sh
python3 -B tools/contest_build82.py build --out TraceHarbor_ContestBuild82.zip
```

Explicit source allowlist, fixed ZIP_STORED bytes, sorted paths, fixed timestamps
and permissions make repeated builds from the same source bytes reproducible.
The build contains BUILD82.json source pins and an exact MANIFEST.csv covering
every other payload. The manifest does not hash itself. The original product
baseline is commit 30caddc4c730d2fef98524f67b431fa56e3daa2c/tree
639b972e8e590c9dc0faff531b11607e985de394; the builder, this guide and disabled
workflow are the distinct review overlay, not changes already merged to main.
No previous repository MANIFEST.json is copied with stale coverage.

The single new packaging qualification uses the unique unknown fixture embedded
in the builder. It extracts into an absent private root, runs the packaged CLI
once, verifies abstention and exported/imported dossier/source associations,
retains original channels before classification and never retries a failed
case. Do not replay that consumed qualification as additional evidence.

The workflow candidate outside .github/workflows remains inactive, including
its literal false job gate. It proposes one manual first-attempt Ubuntu 24.04
build with immutable checkout and no provider key, deployment, install, cache or
artifact upload. Review/promotion and an actual separate job admission are
required. Storage headroom and retention must be qualified before any future
artifact upload. Optional first runner-side pycparser acquisition needs a
distinct source-bound data-only admission: the exact official URL and SHA from
unit 81, no redirect/retry, compressed 1 MiB, expanded 32 MiB, 2048 members,
ratio 200, bounded EOF/CRC/RECORD checks, no installation/import. It is not
implemented or required by this stdlib build and cannot rearm download81.

Next real integration requires exact key/account/project custody, complete
billable input and output/reasoning bounds, all charges/late-usage protection,
a numeric authorized budget and a durable cross-run once reservation. Current
grant is null and inference remains HOLD. Project routing, credits, the server
exception and a successful offline build do not authorize a provider request.
Do not execute live_probe.py or native qualification from this build. Contest
video, English demonstration and submission proof are still pending.
