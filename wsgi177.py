"""Fail-closed WSGI boundary for the unchanged TraceHarbor synthetic application.

No server is created. A separately admitted gateway must supply an authoritative
scheme, Host and original RAW_URI/REQUEST_URI; PEP3333 PATH_INFO alone is decoded.
"""
import sys
sys.dont_write_bytecode = True

import hashlib
from http import HTTPStatus
import json
import os
from pathlib import Path
import re
import stat
from urllib.parse import urlsplit

import app
from core import InputError, MAX_BYTES, parse_json
from service import analyze
from live_service import verify_import
from verifier import VerificationError

JSON_TYPE = 'application/json; charset=utf-8'
CSP = "default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
RESOURCE_PINS = {'fixtures/complete.json': {'bytes': 1719,
                            'sha256': 'b0abb0e5d42b8508e4fd8ebf92289a9576b94c27003fd77399ad0ff5288f06f6'},
 'fixtures/contradictory.json': {'bytes': 2683,
                                 'sha256': '9ae9b920e93037914bf05fcd4954bb5ec6504c376f74fb0e65f6b94f83f4b330'},
 'fixtures/missing.json': {'bytes': 1393,
                           'sha256': 'b96afa3a7ce4837771b03f742b09a7582c9e0d86f648e74115ef88b1a31d67f3'},
 'web/app.js': {'bytes': 7594,
                'sha256': 'a7a47f3df7329b9bab7fe642383ea7000647d70a599b3688544742c8872b4040'},
 'web/index.html': {'bytes': 2162,
                    'sha256': '9ef4315840b7c43e9461129c48907d07a7592a0c91a8dd1ee22b961a338bdf31'},
 'web/style.css': {'bytes': 4100,
                   'sha256': '911467e25c63dc9985642d5a613bfdaa1f306b7d04b753863d734dd8b5833144'}}
_STATIC_CONTRACT = {'/': ('index.html', 'text/html; charset=utf-8'),
                    '/app.js': ('app.js', 'text/javascript; charset=utf-8'),
                    '/style.css': ('style.css', 'text/css; charset=utf-8')}
_CASES_CONTRACT = frozenset(('complete', 'missing', 'contradictory'))
_HOST = re.compile(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)*')
_MEDIA = re.compile(r'application/json(?:[ \t]*;[ \t]*charset=(?:utf-8|"utf-8"))?', re.I)


class _Refusal(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message


class _ResourceError(Exception):
    pass


class BytesResponse:
    """One finite bytes chunk; exhaustion and close both release its reference."""
    def __init__(self, data):
        if type(data) is not bytes:
            raise TypeError('Response payload must be bytes.')
        self.data, self.sent, self.closed = data, False, False

    def __iter__(self):
        return self

    def __next__(self):
        if self.closed or self.sent:
            self.close()
            raise StopIteration
        self.sent = True
        return self.data

    def close(self):
        self.data, self.closed = b'', True


def _json(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False).encode('utf-8')


def _canonical_origin(origin):
    if type(origin) is not str or len(origin) > 300:
        raise ValueError('An explicit canonical HTTP(S) origin is required.')
    try:
        parsed = urlsplit(origin)
        port = parsed.port
    except ValueError:
        raise ValueError('Invalid origin configuration.') from None
    if (parsed.scheme not in ('http', 'https') or parsed.username is not None
            or parsed.password is not None or parsed.path or parsed.query or parsed.fragment
            or not parsed.hostname or len(parsed.hostname) > 253
            or not _HOST.fullmatch(parsed.hostname)
            or origin != parsed.scheme + '://' + parsed.netloc
            or parsed.netloc != parsed.hostname + (':' + str(port) if port is not None else '')
            or (port is not None and not 1 <= port <= 65535)):
        raise ValueError('Invalid origin configuration.')
    return parsed.scheme, parsed.netloc, origin


def _read_resource(path, pin):
    """Only constant app.STATIC/CASES-derived paths reach this bounded reader."""
    try:
        if path.resolve(strict=True) != path:
            raise _ResourceError()
        fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
        try:
            before = os.fstat(fd)
            if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1
                    or stat.S_IMODE(before.st_mode) != 0o644
                    or before.st_size != pin['bytes'] or before.st_size > 32768):
                raise _ResourceError()
            with os.fdopen(fd, 'rb', closefd=False) as stream:
                data = stream.read(pin['bytes'] + 1)
            after = os.fstat(fd)
            if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
                    after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                raise _ResourceError()
        finally:
            os.close(fd)
        if len(data) != pin['bytes'] or hashlib.sha256(data).hexdigest() != pin['sha256']:
            raise _ResourceError()
        return data
    except (OSError, ValueError):
        raise _ResourceError() from None


class _Application:
    def __init__(self, allowed_origin):
        self.origin = None if allowed_origin is None else _canonical_origin(allowed_origin)
        if app.STATIC != _STATIC_CONTRACT or frozenset(app.CASES) != _CASES_CONTRACT:
            raise ValueError('Pinned application route contract changed.')
        root = Path(app.ROOT).absolute()
        self.resources = {route: (root / 'web' / name, kind, RESOURCE_PINS['web/' + name])
                          for route, (name, kind) in app.STATIC.items()}
        self.resources.update({'/fixtures/' + case + '.json':
                               (root / 'fixtures' / (case + '.json'), JSON_TYPE,
                                RESOURCE_PINS['fixtures/' + case + '.json'])
                               for case in app.CASES})

    def _dispatch(self, environ):
        if self.origin is None:
            raise _Refusal(503, 'Hosting origin has not been admitted/configured.')
        if not isinstance(environ, dict):
            raise _Refusal(400, 'Invalid gateway environment.')
        scheme, host, origin = self.origin
        if (environ.get('wsgi.url_scheme') != scheme or environ.get('HTTP_HOST') != host
                or ('HTTP_ORIGIN' in environ and environ['HTTP_ORIGIN'] != origin)
                or any(key in environ for key in ('HTTP_FORWARDED', 'HTTP_X_FORWARDED_HOST',
                                                   'HTTP_X_FORWARDED_PROTO', 'HTTP_X_FORWARDED_PORT'))):
            raise _Refusal(403, 'Configured Host, Origin and authoritative scheme required.')
        path = environ.get('PATH_INFO')
        if (type(path) is not str or len(path) > 128 or not path.startswith('/')
                or '\\' in path or '%' in path or '?' in path or '#' in path
                or any(part in ('.', '..') for part in path.split('/'))
                or environ.get('SCRIPT_NAME', '') != '' or environ.get('QUERY_STRING', '') != ''):
            raise _Refusal(404, 'Not found.')
        original = [environ[key] for key in ('RAW_URI', 'REQUEST_URI') if key in environ]
        if not original or any(type(value) is not str or value != path for value in original):
            raise _Refusal(400, 'An unambiguous authoritative original request target is required.')
        method = environ.get('REQUEST_METHOD')
        if method not in ('GET', 'POST'):
            raise _Refusal(405, 'Method not supported.')
        if method == 'GET':
            if path not in self.resources:
                raise _Refusal(404, 'Not found.')
            source, kind, pin = self.resources[path]
            return 200, _read_resource(source, pin), kind
        if path not in ('/analyze', '/verify'):
            raise _Refusal(404, 'Not found.')
        if ('HTTP_TRANSFER_ENCODING' in environ or environ.get('wsgi.input_terminated')
                or 'HTTP_CONTENT_LENGTH' in environ or 'HTTP_CONTENT_TYPE' in environ):
            raise _Refusal(400, 'Ambiguous or chunked uploads are not supported.')
        media = environ.get('CONTENT_TYPE')
        if type(media) is not str or len(media) > 128 or not _MEDIA.fullmatch(media):
            raise _Refusal(415, 'UTF-8 JSON media required.')
        length = environ.get('CONTENT_LENGTH')
        if type(length) is not str or not re.fullmatch(r'[0-9]{1,6}', length):
            if type(length) is str and length.isascii() and length.isdecimal() and len(length) > 6:
                raise _Refusal(413, 'Upload must be 1..262144 bytes.')
            raise _Refusal(400, 'Invalid Content-Length.')
        if length != str(int(length)):
            raise _Refusal(400, 'Noncanonical Content-Length.')
        length = int(length)
        if not 1 <= length <= MAX_BYTES:
            raise _Refusal(413, 'Upload must be 1..262144 bytes.')
        reader = environ.get('wsgi.input')
        if not callable(getattr(reader, 'read', None)):
            raise _Refusal(400, 'Missing bounded input stream.')
        raw = reader.read(length)
        if type(raw) is not bytes or len(raw) != length:
            raise _Refusal(400, 'Truncated or invalid bounded upload.')
        result = verify_import(parse_json(raw)) if path == '/verify' else analyze(raw)
        return 200, _json(result), JSON_TYPE

    def __call__(self, environ, start_response):
        try:
            code, payload, kind = self._dispatch(environ)
        except _Refusal as exc:
            code, payload, kind = exc.code, _json({'error': exc.message}), JSON_TYPE
        except TimeoutError:
            code, payload, kind = 408, _json({'error': 'Gateway input timed out.'}), JSON_TYPE
        except _ResourceError:
            code, payload, kind = 500, _json({'error': 'Pinned resource unavailable.'}), JSON_TYPE
        except (InputError, VerificationError, ValueError, TypeError, UnicodeError, RecursionError):
            code, payload, kind = 400, _json({'error': 'Invalid synthetic JSON or dossier.'}), JSON_TYPE
        except Exception:
            code, payload, kind = 500, _json({'error': 'Application request failed.'}), JSON_TYPE
        body = BytesResponse(payload)
        headers = [('Content-Type', kind), ('Content-Length', str(len(payload))),
                   ('X-Content-Type-Options', 'nosniff'), ('Cache-Control', 'no-store'),
                   ('Content-Security-Policy', CSP)]
        if code == 405:
            headers.append(('Allow', 'GET, POST'))
        try:
            start_response(str(code) + ' ' + HTTPStatus(code).phrase, headers)
        except BaseException:
            body.close()
            raise
        return body


def create_application(*, allowed_origin=None):
    """Explicit configuration only; no environment/key lookup or server startup."""
    return _Application(allowed_origin)


application = create_application()
