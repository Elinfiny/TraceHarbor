"""Loopback-only demo server and offline CLI. No external API calls."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
import json
import sys
from core import InputError, MAX_BYTES, parse_json
from service import analyze
from live_service import verify_import
from verifier import VerificationError

ROOT = Path(__file__).resolve().parent
STATIC = {'/': ('index.html', 'text/html; charset=utf-8'), '/app.js': ('app.js', 'text/javascript; charset=utf-8'), '/style.css': ('style.css', 'text/css; charset=utf-8')}
CASES = {'complete', 'missing', 'contradictory'}

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_): pass  # Do not log imported evidence.
    def allowed(self):
        expected = f'127.0.0.1:{self.server.server_port}'
        if self.headers.get('Host') != expected: return False
        origin = self.headers.get('Origin')
        return origin is None or origin == 'http://' + expected
    def respond(self, code, body, content_type='application/json; charset=utf-8'):
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Security-Policy', "default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'")
        self.end_headers(); self.wfile.write(body)
    def error(self, code, message):
        self.respond(code, json.dumps({'error': message}).encode())
    def do_GET(self):
        if not self.allowed(): return self.error(403, 'Loopback Host/Origin required.')
        if self.path in STATIC:
            name, kind = STATIC[self.path]; return self.respond(200, (ROOT/'web'/name).read_bytes(), kind)
        if self.path.startswith('/fixtures/') and self.path[10:] in {n+'.json' for n in CASES}:
            return self.respond(200, (ROOT/'fixtures'/self.path[10:]).read_bytes())
        self.error(404, 'Not found.')
    def do_POST(self):
        if not self.allowed(): return self.error(403, 'Loopback Host/Origin required.')
        if self.path not in ('/analyze', '/verify'): return self.error(404, 'Not found.')
        if self.headers.get('Transfer-Encoding'): return self.error(400, 'Chunked uploads are not supported.')
        if self.headers.get_content_type() != 'application/json': return self.error(415, 'JSON required.')
        try: length = int(self.headers.get('Content-Length', '-1'))
        except ValueError: return self.error(400, 'Invalid Content-Length.')
        if not 1 <= length <= MAX_BYTES: return self.error(413, 'Upload must be 1..262144 bytes.')
        self.connection.settimeout(5)
        try:
            raw = self.rfile.read(length)
            if len(raw) != length: raise InputError('Truncated upload.')
            result = verify_import(parse_json(raw)) if self.path == '/verify' else analyze(raw)
            self.respond(200, json.dumps(result, ensure_ascii=False, allow_nan=False).encode())
        except (InputError, VerificationError, ValueError) as exc: self.error(400, str(exc))
        except TimeoutError: self.error(408, 'Upload timeout.')

def make_server(port=0):
    return ThreadingHTTPServer(('127.0.0.1', port), Handler)

def main():
    p = argparse.ArgumentParser(description='TraceHarbor P01: offline synthetic demonstration, no AI.')
    sub = p.add_subparsers(dest='command', required=True)
    a = sub.add_parser('analyze'); a.add_argument('file', type=Path); a.add_argument('--out', type=Path)
    s = sub.add_parser('serve'); s.add_argument('--port', type=int, default=8787)
    args = p.parse_args()
    if args.command == 'analyze':
        try:
            with args.file.open('rb') as f: result = analyze(f.read(MAX_BYTES+1))
            rendered = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
            if args.out:
                with args.out.open('x', encoding='utf-8') as out: out.write(rendered)
            else: print(rendered, end='')
        except (OSError, InputError, VerificationError) as exc:
            print('Controlled error: '+str(exc), file=sys.stderr); return 2
    else:
        server = make_server(args.port)
        print(f'TraceHarbor DEMO_NO_AI http://127.0.0.1:{server.server_port} — Ctrl+C to stop', flush=True)
        try: server.serve_forever()
        except KeyboardInterrupt: pass
        finally: server.server_close()
    return 0

if __name__ == '__main__': raise SystemExit(main())
