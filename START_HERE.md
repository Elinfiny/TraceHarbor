# TraceHarbor — start here

## Current delivery — 30 October 2026

TraceHarbor is submitted to the Nebius x NVIDIA Global AI Hackathon as entry 1264455. The current [README](README.md) is the primary guide to the delivered project, its exact source baseline, historical NVIDIA/Nebius execution and limitations.

- [Public project and demonstration](https://devpost.com/software/traceharbor)
- [Working synthetic evidence desk](https://traceharbor.onrender.com/)
- [Demonstration video — 2:56](https://youtu.be/x1DSpXFOWHo)
- [Complete historical provider record](examples/recorded/provider_record228.json)
- [Historical native execution](https://github.com/Elinfiny/TraceHarbor/actions/runs/40206978963)

The public desk requires no account, key or payment and makes no new model call. Start evidence evolution, add the captured verification and inspect the conflicting capture. Exact quotations and unkeyed hashes do not authenticate origin or prove production causation. The application does not execute checks or remediation.

## Run locally

Use Python 3.12 or later from this source checkout; the offline application requires only the standard library:

```sh
python3 -B app.py serve --port 8787
```

Open `http://127.0.0.1:8787/` using that exact hostname and port. Use synthetic data only. To create a dossier at an absent output path:

```sh
python3 -B app.py analyze fixtures/missing.json --out missing-dossier.json
```

Use Verify imported dossier to review the bundled historical provider record. It remains an UNKNOWN saved record, distinct from fresh inference. Refer to README for the source and execution evidence; do not rerun consumed workflows or protected runtime attempts.

## Judging access

The official judging period ends on 23 December 2026 at 20:00 UTC / 22:00 Europe/Bucharest. Code, video and the working project must remain accessible to judges through that time. The offline build provides an alternative independent of provider inference credits. This requirement does not extend private AI authority or guarantee future hosting availability.

## Preserved historical documentation

The previous start guide, including its dated preparation state and references to files not bundled in this release, remains available in the [immutable previous revision](https://github.com/Elinfiny/TraceHarbor/blob/a81a10ddc589e854a5558e01e07f1b39b94fa6f2/START_HERE.md). Those old missing-demo, missing-video and missing-execution statements are superseded by the current delivery above. They are not current instructions.
