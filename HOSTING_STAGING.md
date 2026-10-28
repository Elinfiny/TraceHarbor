# Render staging

This branch preserves the 42 independently accepted private48 product source
files. `render_preflight.py` adds a Render entrypoint for synthetic analysis,
verification and evidence evolution. It does not activate the reviewed model
runtime, operator identity, capture, or any release pin.

Use the existing Hobby workspace, one Python web service (512 MB), and one
1 GB disk mounted at `/var/data`. Start with `python render_preflight.py`.
The source uses only Python's standard library. Do not attach a provider API
credential for this staging phase. Keep automatic deploys disabled.

The `/healthz` endpoint reports a staging classification, source commit,
public hostname and a hash of a persistent random marker. It does not report
private data or secret values. A matching marker after a controlled restart
can verify persistence; the first response alone does not verify restart
persistence or production readiness.

The browser must use the actual HTTPS service hostname. Synthetic POSTs
require the exact Host and Origin, HTTPS forwarding metadata, no transfer
encoding, and one Content-Length. Model and capture POSTs always refuse.
Production edge/proxy qualification and the separate reviewed runtime
admission remain required before enabling model inference.

This staging service is not the finished live judging service. Historical
provider records remain explicitly historical; do not describe them as a
fresh model response. Do not submit an incomplete service as complete.
