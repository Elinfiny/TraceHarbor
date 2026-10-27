# Browser QA evidence

Evidence reviewed 24 October 2026. Canonical main is `dfd0639d8aec43cc13d4776a19138af3bd626598` (tree `f38d934627f809cd9ff747c0d09df746bd15c739`). Qualified, unmerged PR45 head is `3445843b599032b3fe825f3647bd006ea7223f08` (tree `ab2ec6d56fd72dcf156001bf641c38a4b29f8da1`). The latter contains 241 blobs; only the QA workflow and runner differ from main. This documentation proposal does not create a published commit or change either source version.

## Actual browser run

Run `40080834816`, job `120833871029`, attempt 1: **27 PASS** in hosted Chromium. Six synthetic journeys covered complete, missing and contradictory evidence at widths 390 and 1440 CSS pixels. Observed checks included 18 layouts, two keyboard cases, 60 citation clicks, three distinct downloads, six valid reimports returning 200 and six tampered reimports returning 400. Unexpected console errors, page errors, external/provider/model requests, artifact uploads and retries were zero.

Playwright/core 1.56.1; Chromium 1194 / 141.0.7390.37. Actual browser binary SHA256: `6c82af1bb96955970f0ff50884bcbd75f200222414dc136076ada667bf4628d1`.

Whole job log: 91976 bytes, SHA256 `fa6c01cc61448843e7e6e75a6b98f1c05e581637a3422bbade8c7fe4bd8345c7`. Decoded evidence JSON: 35296 bytes, SHA256 `ec4b5f47bb54ff4f88a1adfb9872422505b04dbe9012a703e08f91bcf927eb83`. These hashes identify the existing accepted evidence; no browser test was rerun for this documentation change.

Actual cleanup closed the browser, stopped the child with SIGTERM and confirmed listener 8787 absent with ECONNREFUSED. Cleanup took 24.44 ms against the 5000 ms bound, without errors or fallback. A final contexts_closed counter of zero follows two earlier context closures; it does not show leaked contexts.

## Limits

This is real browser execution with synthetic inputs at two widths. It does not establish physical-device testing, five-width coverage, live inference, persistent hosting, a byte-verified current public Download ZIP, contest qualification or full product completion. Canonical main and the qualified unmerged branch remain separate. Genuine platform/model evidence, a persistent demo and recorded submission footage are still missing. See the [readiness checklist](READINESS170.json).
