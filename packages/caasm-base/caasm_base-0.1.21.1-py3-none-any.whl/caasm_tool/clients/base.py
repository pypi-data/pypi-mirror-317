import logging
import traceback
from functools import cached_property
from typing import Dict

import requests
from requests import Session
from requests.exceptions import ConnectTimeout, ReadTimeout

from caasm_tool.util import build_url

log = logging.getLogger()


class HttpClient(object):
    METHOD = None
    URL = None
    TIMEOUT = 60
    SSL_VERIFY = False
    STREAM = False

    def __init__(self, connection, session=None):
        self._connection = connection
        self._session = session or requests.Session()

    def handle_common(self, *args, **kwargs):
        headers = self.build_request_header(*args, **kwargs)
        params = self.build_request_params(*args, **kwargs)
        json_data = self.build_request_json(*args, **kwargs)
        request_url = self.build_request_url(*args, **kwargs)
        data = self.build_request_data(*args, **kwargs)
        cookies = self.build_request_cookies(*args, **kwargs)
        auth = self.build_request_auth(*args, **kwargs)

        # 发送请求
        request_data = {
            "request_url": request_url,
            "params": params,
            "json_data": json_data,
            "form_data": data,
            "headers": headers,
            "cookies": cookies,
            "auth": auth,
        }
        response = self.send_request(**request_data)
        return self.parse_response(response, *args, **kwargs)

    def handle(self, *args, **kwargs):
        try:
            result = self.handle_common(*args, **kwargs)
        except (ConnectTimeout, ReadTimeout):
            return self.timeout_handle(*args, **kwargs)
        except Exception as e:
            return self.error_handle(e, *args, **kwargs)
        else:
            return self.parse_biz_result(result, *args, **kwargs)

    def send_request(self, request_url, params, json_data, form_data, headers, cookies, auth):
        return self._session.request(
            self.METHOD,
            request_url,
            params=params,
            json=json_data,
            headers=headers,
            data=form_data,
            timeout=self.TIMEOUT,
            verify=self.SSL_VERIFY,
            proxies=self.proxy,
            cookies=cookies,
            auth=auth,
            stream=self.STREAM,
        )

    def parse_response(self, response, *args, **kwargs):
        return response.text

    def parse_biz_result(self, result, *args, **kwargs):
        return result

    def build_request_header(self, *args, **kwargs):
        pass

    def build_request_params(self, *args, **kwargs):
        pass

    def build_request_json(self, *args, **kwargs):
        pass

    def build_request_data(self, *args, **kwargs):
        pass

    def build_request_cookies(self, *args, **kwargs):
        pass

    def build_request_auth(self, *args, **kwargs):
        pass

    def build_request_url(self, *args, **kwargs):
        return self.build_url(self.address, self.URL)

    def build_url(self, address=None, url=None):
        if not address:
            address = self.address
        if not url:
            url = self.URL
        return build_url(address=address, url=url)

    def error_handle(self, err, *args, **kwargs):
        """
        失败处理，不属于（业务解析、超时范围内的处理）
        """
        log.warning(f"{self.name} Request Error({err}) Data({args, kwargs}) Detail({traceback.format_exc()})")

    def timeout_handle(self, *args, **kwargs):
        """
        请求、或者响应超时
        """
        log.warning("Request timeout")

    @property
    def address(self) -> str:
        return self._connection.get("address")

    @property
    def connection(self) -> Dict:
        return self._connection

    @property
    def debug(self):
        return self.connection.get("debug")

    @cached_property
    def proxy(self):
        proxy = self.connection.get("proxy")
        if not proxy:
            return None
        return {"http": proxy, "https": proxy}

    @property
    def session(self) -> Session:
        return self._session

    @property
    def name(self) -> str:
        return self.__class__.__name__
