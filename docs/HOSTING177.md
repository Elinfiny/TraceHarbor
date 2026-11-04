# TraceHarbor WSGI boundary177 — prepared source, no deployed service

This private candidate adds `wsgi177.py`, `tests/test_wsgi177.py` and this
document. Only their inventory entries change in `diagnostic108/manifest.json`.
The Python engine, current `app.py` loopback handler, six runtime modules, web
assets, fixtures, schema/reference data, and release175 tools remain byte-exact.
No public audience, Site, DNS, URL, account, server, deployment, paid fallback,
model execution or runtime admission is created by this source delivery.

## Entry point and explicit configuration

Python3.12+ standard library only. `wsgi177:application` is a valid WSGI callable
which deliberately returns503 before reading any body until an origin is
configured. An admitted Python gateway must call
`create_application(allowed_origin="https://traceharbor.invalid")` and expose
that returned callable. The `.invalid` address is an inert documentation/test
string, not a live site. The real single canonical origin needs separate
admission; no environment variables, keys, accounts or wildcards are consulted.
Canonical lowercase DNS/IPv4-style hosts and explicit canonical ports are
supported; IPv6 literals are not accepted in this source version.

Import sets `sys.dont_write_bytecode` before local imports. It does not call
`app.main`, instantiate an HTTPServer, open a socket, create a daemon, write
files or consult credentials. The future gateway supplies lifecycle and
server behavior; no framework/WSGI server/package installation is part of177.

## Trusted gateway boundary

Before a body read, the callable binds exact `HTTP_HOST`, optional exact
`HTTP_ORIGIN`, and authoritative `wsgi.url_scheme` to the configured origin.
Missing Origin remains allowed as in the existing handler; this is not user
authentication or provider-origin attestation. Forwarded, X-Forwarded-Host,
X-Forwarded-Proto and X-Forwarded-Port inputs are refused, not trusted.
The gateway must strip untrusted forwarding headers and independently prove
its scheme/host/proxy configuration; arbitrary client headers cannot supply it.

Standard PEP3333 PATH_INFO is decoded and cannot prove the wire request target.
This adapter therefore also requires the gateway-owned `RAW_URI` or
`REQUEST_URI` extension, equal exactly to PATH_INFO. If both exist, both must
match. HTTP_RAW_URI is not a substitute. A gateway without a trustworthy
original-target extension fails closed400 and is not yet a compatible host.
Encoded separators/aliases, dot traversal, backslashes, query strings and
nonempty SCRIPT_NAME are refused. The app is mounted at the origin root.

The future host, not this BytesIO-tested adapter, must demonstrate deadline,
concurrency, header/body size limits, complete read(n) semantics, cancellation,
TLS/proxy ownership and request framing. No socket timeout or wire-level
request-smuggling protection is claimed from the memory tests alone.

## Exact endpoints and read paths

GET: `/`, `/app.js`, `/style.css`, and the three fixed
`/fixtures/{complete,missing,contradictory}.json` routes. POST: `/analyze` and
`/verify`. No admin/debug/model/upload endpoint is added. STATIC and CASES are
reused from the unchanged app module and checked against the fixed contract.
The only direct asset reads are the three web files and three fixtures under
the imported app.ROOT, with regular-file, no-symlink, single-link, mode100644,
size and pinned SHA256 checks. No request path or imported JSON becomes a
filesystem path. The unchanged native service additionally reads its fixed
synthetic fixtures/reference data as before.

JSON media is mandatory; optional charset may only be UTF-8. Content-Length
must be a canonical positive ASCII decimal string within1..262144. Missing,
boolean-like, signed, padded, zero and oversized lengths are refused before
body access. Transfer-Encoding, terminated/chunked streams and ambiguous
duplicate CGI Content-* fields are refused. The sole input read requests
exactly the admitted length; truncation, a nonbytes return or an overlong
return is rejected. UTF-8/JSON/schema/citation/dossier validation delegates to
the existing core.parse_json, service.analyze and live_service.verify_import.
Unknown synthetic input retains the native status `unknown` and no diagnosis;
it is not relabelled as `uncertain`. Known missing/contradictory/complete cases
retain their existing uncertain/conflicted/supported_reference semantics.

Every response has exact Content-Length, nosniff, no-store and the unchanged
strict CSP: default-src none; script/style/connect self; img/base/form/frame
blocked. No CORS wildcard or reflected errors, local paths or tracebacks.
Errors are bounded generic JSON. Response iteration yields bytes, releases its
payload on exhaustion/close, and closes on start_response failure. The gateway
must still call close on early disconnect according to WSGI lifecycle rules.

## Actual qualification and remaining single host-admission step

The new unittest file invokes the real callable with synthetic BytesIO input
and captured start_response, including PEP3333 validator checks for conforming
positive environments. It checks all six GET payloads, all three native
analysis outputs, dossier export/re-import, unknown input, tampering, strict
host/origin/scheme/target/media/body guards and before-read counters, bytes
cleanup and no file-write/socket/key side effects. No HTTP server, browser,
preview, tunnel, old denied URL, GitHub job or model request is used. Exact
runtime results/first failure, if any, are in the separate producer receipt.
No175/173/QA7 campaign is rerun or promoted to current browser evidence.

The remaining host-integration step is one independently reviewed admission
of this exact source on a supported Python WSGI gateway: bind the real origin,
trusted original-target/scheme configuration, deadline/concurrency/framing,
no-paid-fallback/quota limits, exact deployment effects, canonical readback and
rollback. GitHub remains canonical; public deployment and live model proof
remain NOT_ADMITTED. No Activity Site is replaced or created for testing.

DEMO_NO_AI and synthetic evidence remain explicit. Matching quotes/checksums
do not prove causation or authenticate imported provider metadata. Native154
and financial/model/provider prerequisites remain separately gated. The
160-second storyboard is UNRECORDED; public video, eligibility/rights and
final entry remain open. This WSGI source is not a running Netcup server and
does not close the independent backup/two-full-restores/P0 gates.
