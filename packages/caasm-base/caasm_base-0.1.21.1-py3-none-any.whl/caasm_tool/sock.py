from urllib.parse import urlparse

import socks

from caasm_tool.constants import PROTOCOL_DEFAULT_MAPPER


def get_socks5(address, proxy=None, timeout=None):
    sock = socks.socksocket()
    sock.settimeout(timeout) if timeout else ...
    _, host, port = parse_address(address)

    if proxy:
        schema, proxy_host, proxy_port = parse_address(proxy)
        if schema == "http" or "https":
            proxy_type = socks.PROXY_TYPE_HTTP
        elif schema == "socks5":
            proxy_type = socks.PROXY_TYPE_SOCKS5
        else:
            proxy_type = socks.PROXY_TYPE_SOCKS4
        sock.setproxy(proxy_type, proxy_host, proxy_port)
    sock.connect((host, port))
    return sock


def parse_address(address):
    _url = urlparse(address)
    scheme = _url.scheme
    hostname = _url.hostname
    port = _url.port
    if not port:
        port = PROTOCOL_DEFAULT_MAPPER.get(scheme)
    return scheme, hostname, port
