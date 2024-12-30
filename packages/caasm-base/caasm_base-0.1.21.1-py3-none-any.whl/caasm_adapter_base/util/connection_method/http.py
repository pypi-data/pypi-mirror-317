import logging
import socket
from urllib.parse import urlparse

from caasm_adapter_base.util.connection_method.base import ConnectionBaseMethod

log = logging.getLogger()


class WebApiConnectionHandle(ConnectionBaseMethod):
    METHOD_LIST = ["socket"]
    DEFAULT_METHOD = "socket"

    def __init__(self, method=None, data=None):
        super(WebApiConnectionHandle, self).__init__(data=data, method=method)
        self.method_map = {"socket": self.socket}

    def analysis_address(self):
        super(WebApiConnectionHandle, self).analysis_address()
        _url = urlparse(self.address)
        scheme = _url.scheme
        self.ip = _url.hostname
        self.port = _url.port
        if not self.port:
            if scheme == "https":
                self.port = 443
            elif scheme == "http":
                self.port = 80
            else:
                raise ValueError("input url scheme  error !,please check it!")

    def socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((self.ip, int(self.port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
