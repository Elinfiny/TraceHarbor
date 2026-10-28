"""Render staging host: synthetic functionality only; provider/admin routes closed.

This entrypoint does not activate edge_adapter or any reviewed release pin.
It never reads an API credential and cannot dispatch provider inference.
"""
import hashlib
import json
import os
import re
import stat
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

import app
import runtime_service


def hostname(value):
    if not isinstance(value, str) or len(value) > 253 or not re.fullmatch(
        r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.onrender\.com", value
    ):
        raise ValueError("Exact Render service hostname required")
    return value


def private_state(mount):
    """Create a staging marker only, never alter runtime quota/effect files."""
    mount = Path(mount)
    if os.name != "posix" or not mount.is_absolute() or mount.is_symlink():
        raise ValueError("POSIX persistent mount required")
    for p in (mount, *mount.parents):
        if p.is_symlink():
            raise ValueError("No symlink mount")
    if not mount.is_dir():
        raise ValueError("Existing persistent mount required")
    directory = mount / "traceharbor-staging"
    directory.mkdir(mode=0o700, exist_ok=True)
    info = directory.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise ValueError("Private administrator-owned staging directory required")
    marker = directory / "persistence-marker"
    try:
        fd = os.open(marker, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    except FileExistsError:
        pass
    else:
        with os.fdopen(fd, "wb") as out:
            out.write(os.urandom(32))
            out.flush()
            os.fsync(out.fileno())
        fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    fd = os.open(marker, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise ValueError("Private marker required")
        data = os.read(fd, 33)
    finally:
        os.close(fd)
    if len(data) != 32:
        raise ValueError("Incomplete staging marker; never overwrite")
    return hashlib.sha256(data).hexdigest()


class StagingHandler(app.Handler):
    def allowed(self):
        host = self.server.public_hostname
        hosts = self.headers.get_all("Host", [])
        origins = self.headers.get_all("Origin", [])
        if hosts != [host] or len(origins) > 1:
            return False
        if origins and origins != ["https://" + host]:
            return False
        if self.command == "POST" and origins != ["https://" + host]:
            return False
        if self.headers.get_all("X-Forwarded-Proto", []) != ["https"]:
            return False
        forwarded_host = self.headers.get_all("X-Forwarded-Host", [])
        if forwarded_host and forwarded_host != [host]:
            return False
        return not self.headers.get_all("Transfer-Encoding", []) and len(
            self.headers.get_all("Content-Length", [])
        ) <= 1

    def do_GET(self):
        if self.path == "/healthz":
            # Platform health checks can arrive internally without public TLS.
            # This response is public, contains no credentials or operator data.
            value = {"phase": "SYNTHETIC_STAGING_NOT_LIVE_INFERENCE",
                     "new_call_cap": 0, "capture_enabled": False,
                     "public_hostname": self.server.public_hostname,
                     "persistence_marker_sha256": self.server.persistence_marker,
                     "source_commit": self.server.source_commit}
            return self.respond(200, json.dumps(value).encode())
        if self.path.startswith("/private-capture/"):
            return self.error(403, "Operator capture is not admitted.")
        return super().do_GET()

    def do_POST(self):
        if self.path not in {"/analyze", "/verify", "/evolution"}:
            return self.error(403, "Provider inference and operator capture are not admitted.")
        return super().do_POST()


class StagingServer(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 8

    def __init__(self, *args, **kwargs):
        self.slots = threading.BoundedSemaphore(8)
        super().__init__(*args, **kwargs)

    def get_request(self):
        sock, address = super().get_request()
        sock.settimeout(5)
        return sock, address

    def process_request(self, request, client_address):
        if not self.slots.acquire(blocking=False):
            self.shutdown_request(request)
            return
        try:
            super().process_request(request, client_address)
        except BaseException:
            self.slots.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self.slots.release()


def main():
    if runtime_service.GLOBAL_NEW_CALL_CAP != 0:
        raise ValueError("Staging host requires the source-owned call cap to remain zero")
    public = hostname(os.environ.get("RENDER_EXTERNAL_HOSTNAME"))
    if os.environ.get("RENDER") != "true":
        raise ValueError("This entrypoint is restricted to the selected Render host")
    port = int(os.environ.get("PORT", "10000"))
    if not 1024 <= port <= 65535:
        raise ValueError("Invalid platform port")
    marker = private_state("/var/data")
    server = StagingServer(("0.0.0.0", port), StagingHandler)
    server.public_hostname = public
    server.persistence_marker = marker
    server.source_commit = os.environ.get("RENDER_GIT_COMMIT", "UNOBSERVED")
    print("TraceHarbor Render synthetic staging; provider calls and capture disabled", flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
