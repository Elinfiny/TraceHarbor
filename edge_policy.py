"""Exact public edge mapping. Defaults cannot create a public listener."""
import ipaddress
from release_policy import validate_config,digest,Refusal
REVIEWED_EDGE_SHA256=None
class EdgePolicy:
    def __init__(self,config,*,proxy_peers=(),reviewed_pin=None):
        self.config=dict(validate_config(config));self.host=config['public_hostname'];self.origin='https://'+self.host
        self.peers=frozenset(str(ipaddress.ip_address(p)) for p in proxy_peers)
        self.pin=reviewed_pin
    def permits(self,*,hosts,origins,peer,tls,forwarded_proto=(),forwarded_host=(),mutation=False):
        if hosts!=[self.host] or len(origins)>1 or (origins and origins!=[self.origin]) or (mutation and origins!=[self.origin]):return False
        if forwarded_host and forwarded_host!=[self.host]:return False
        if tls:
            return not forwarded_proto and not forwarded_host
        try:trusted=str(ipaddress.ip_address(peer)) in self.peers
        except ValueError:return False
        return trusted and forwarded_proto==['https']
    def validate_listener(self,port,platform_port):
        if REVIEWED_EDGE_SHA256 is None or self.pin!=REVIEWED_EDGE_SHA256 or self.pin!=digest(self.config):raise Refusal('EDGE_NOT_ADMITTED')
        if type(port)is not int or not 1024<=port<=65535 or str(port)!=platform_port:raise Refusal('PORT_MAPPING')
        if not self.peers:raise Refusal('PROXY_NOT_QUALIFIED')
        return '0.0.0.0',port
