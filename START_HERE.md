# TraceHarbor — start here

TraceHarbor is an offline evidence desk for reviewing synthetic incident dossiers. Follow source citations, compare complete, missing and contradictory evidence, and export a dossier for integrity checking. Remediation remains advice for a human reviewer; the desk does not execute it.

## Run locally

Use Python 3.12 or later and the standard library, from a verified source checkout:

```sh
python app.py serve --port 8787
```

Open `http://127.0.0.1:8787/`. Use that exact loopback hostname and port because Host and Origin are validated. The offline synthetic workflow requires no API key. Do not enter production records or secrets.

A create-only command-line example requires an output path that does not exist:

```sh
python app.py analyze fixtures/missing.json --out missing-dossier.json
```

## Source and browser evidence

Canonical main: `dfd0639d8aec43cc13d4776a19138af3bd626598`, tree `f38d934627f809cd9ff747c0d09df746bd15c739`. Qualified PR45 head: `3445843b599032b3fe825f3647bd006ea7223f08`, tree `ab2ec6d56fd72dcf156001bf641c38a4b29f8da1`; the pull request remains unmerged at the last verified observation. The two versions have identical application, web and fixture bytes; the branch differs in its QA runner and workflow.

Actual hosted Chromium passed 27 checks using synthetic inputs at widths 390 and 1440. See [browser evidence](release/QA_EVIDENCE170.md) for the run, hashes, tested behavior and limits. These proposed documentation changes do not establish a new published commit or release. README.md retains older source and QA wording outside this document update.

A current GitHub Download ZIP has not been byte-verified. Historical offline archives are separate artifacts and do not prove a current public download. A persistent working demo URL, genuine Nebius/NVIDIA execution evidence and a recorded video are still missing.

## Delivery material

The [readiness checklist](release/READINESS170.json), [submission draft](SUBMISSION_DRAFT.md) and [160-second storyboard](VIDEO_SCRIPT.md) describe completed evidence and remaining work. They are preparation material, not a submission receipt. A clearly labelled hosted offline desk can be delivered independently of later live-model integration.

The [official contest rules](https://nebiusglobalaihackathon.devpost.com/rules) were reviewed on 24 October 2026: the submission deadline is 30 October, 10:00 PDT = 17:00 UTC = 19:00 Europe/Bucharest. The contest requires genuine Nebius execution with an NVIDIA open-source model; offline browser QA does not satisfy that requirement. Personal eligibility and entry declarations still require verification.
