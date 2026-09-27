# TraceHarbor data contracts v1

Machine-readable field contracts: `input.schema.json`, `output.schema.json` (JSON Schema 2020-12). Python enforces additional identity, timestamp, secret-pattern, cross-reference, size and integrity invariants. Schema conformance alone does not demonstrate a valid conclusion. No online schema resolver is needed or invoked.

## Input: traceharbor.input.v1

Required root keys: `schema`, `synthetic: true`, `case_id`, `title`, `sources`. Unknown properties and duplicate JSON keys are refused. IDs match `[a-z][a-z0-9_-]{0,63}`; titles are 1..160 characters.

Each source has `id`, `kind` (`log|deployment|metric|configuration|runbook|audit`), `title`, `events`. Source IDs are unique. Each event has a source-local unique `id` and nonblank `text` (1..8192 characters). `timestamp` and `timestamp_alt` are optional ISO-8601 strings or null. Accepted form is a full date/time with seconds, optional 1..6 fractional digits, and `Z` or a numeric UTC offset. A nonblank timestamp without a timezone is invalid.

Normalization to UTC preserves the instant. No primary time → `missing`, even if a secondary candidate exists. Two unequal normalized timestamps → `conflict` and no chosen timestamp. Known times sort first; unresolved events remain last with original candidates visible. The `raw` source retains the exact parsed input structure. The input byte hash is a receipt of received bytes; JSON export is not a byte-identical copy of the original encoding.

## Output: traceharbor.dossier.v1

| Field | Meaning |
|---|---|
| `mode` | Always `DEMO_NO_AI` |
| `live_api` | Always `NOT_ACTIVATED` |
| `remediation_execution` | Always `NOT_SUPPORTED` |
| `evidence` | Case label, raw input SHA-256, fingerprint, source objects, deduplicated timeline, timestamp warnings and counts |
| `analysis` | Status, summary, hypotheses, missing evidence and remediation proposals |
| `verification` | Citation integrity; bounded known-reference semantic check; explicit limitations |
| `dossier_sha256` | Canonical hash of the complete dossier with this top-level field **omitted** |

Canonical JSON is UTF-8, sorted object keys, compact separators, Unicode unescaped, no NaN/Infinity. Source SHA-256 covers the entire raw source object. Event SHA-256 covers `{kind,text,time,state}` where `time` is the ordered candidate list. The analysis fingerprint covers a sorted set of source identity/type/title and normalized event content; duplicate copies do not strengthen a conclusion. Hashes prove integrity, not external authenticity or causal truth.

Each source object has its `id`, `kind`, `title`, `sha256`, original `raw` object and normalized `events`. A normalized event carries `id`, `text`, nullable UTC `timestamp`, `timestamp_state`, and `timestamp_candidates`. A timeline event replaces `id` with `event_sha256`, adds `kind`, and preserves all `{source_id,event_id}` occurrences. Counts are input, unique and duplicate event counts.

Analysis status is `supported_reference|uncertain|conflicted|unknown`. A hypothesis contains `id`, `label`, `assessment`, `supports`, `contradicts`. Both citation lists use `{source_id,event_id,source_sha256,quote}`. Quotes are exact **full-event** text, not fuzzy or substring matches. Status `unknown` requires empty hypotheses and remediation; the missing-evidence list explains the abstention.

A remediation proposal contains `id`, `proposal`, nonempty `preconditions`, `risk`, `rollback`, and nonempty `verification`. These are advisory strings only. There is no execution endpoint, command, scheduler, actor or credential.

`verify_dossier` checks the dossier hash, reconstructs normalized evidence from exported raw sources, compares source/timeline/warning/count/fingerprint structures, verifies citations and runs the bounded semantic reference checks. It cannot establish authenticity of an imported raw input hash against bytes it was not given, nor external truth of synthetic source assertions.

## Controlled errors

CLI returns exit 2 with a concise message for malformed input, schema errors, unsafe evidence or output collision. HTTP returns JSON `{"error":"..."}`: 400 for invalid data/citations; 403 for Host/Origin violation; 404 for unknown route; 408 for upload timeout; 413 for the size bound; 415 for non-JSON uploads. Unknown valid cases are successful imports with explicit diagnostic abstention.

## C1 validation clarification (2026-09-18)

Chronological sorting compares timezone-aware instants, preserving fractional seconds without float conversion. Equal timestamps use the existing deterministic hash tie-breaker only, with no causal-order claim. Missing/conflicting timestamps still have no assigned instant and sort last.

`verify_dossier` requires the exact v1 root fields and offline constants; validates the evidence version, synthetic flag, hash formats, bounded lists and integer counts; reconstructs all normalized evidence; then recomputes citation and reference results. Exported `verification` fields must agree with those results and with the application's explicit limitation text. Missing/extra fields, incompatible declarations or malformed structures raise `ValueError` (including its validation subclasses), even if the caller recalculates the content hash.

An unkeyed SHA-256 is an integrity checksum, **not cryptographic authentication** of the author, source or claims. A self-consistent synthetic dossier is not evidence of a live model, an executed remediation, or a real incident. `input_sha256` remains a format-checked receipt of original bytes that are not embedded; it is not independently authenticated by this validator. No general semantic engine or third-party dependency is introduced.
