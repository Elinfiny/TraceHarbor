"""Explicit future public adapter. Import never binds. Inactive edge pin blocks bind."""
from http.server import ThreadingHTTPServer
import app
from release_policy import digest,Refusal
class EdgeHandler(app.Handler):
    def allowed(self):
        if len(self.headers.get_all('Content-Length',[]))>1 or self.headers.get_all('Transfer-Encoding',[]):return False
        p=self.server.edge_policy
        return p.permits(hosts=self.headers.get_all('Host',[]),origins=self.headers.get_all('Origin',[]),peer=self.client_address[0],tls=False,forwarded_proto=self.headers.get_all('X-Forwarded-Proto',[]),forwarded_host=self.headers.get_all('X-Forwarded-Host',[]),mutation=self.command=='POST')

def make_reviewed_server(policy,session,*,port,platform_port):
    if digest(policy.config)!=digest(session.config):raise Refusal('EDGE_RUNTIME_CONFIG_MISMATCH')
    address=policy.validate_listener(port,platform_port)
    if not session.status()['enabled']:raise ValueError('RUNTIME_RELEASE_NOT_ADMITTED')
    server=ThreadingHTTPServer(address,EdgeHandler);server.edge_policy=policy;server.runtime_session=session
    return server
