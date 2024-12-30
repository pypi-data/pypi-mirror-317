import json
import logging

from caasm_adapter_base.util.exception import (
    AdapterFetchApiCallTimeoutException,
    AdapterFetchApiResponseException,
    AdapterFetchApiRequestException,
    AdapterFetchRequestException,
    AdapterFetchApiJSONException,
)
from caasm_tool.clients.base import HttpClient
from caasm_tool.util import extract

log = logging.getLogger()


class FetchClient(HttpClient):
    def timeout_handle(self, *args, **kwargs):
        raise AdapterFetchApiCallTimeoutException

    def parse_json_error_handle(self, result, *args, **kwargs):
        raise AdapterFetchApiJSONException(result)

    def parse_error_handle(self, result, *args, **kwargs):
        raise AdapterFetchApiResponseException(result)

    def error_handle(self, err, *args, **kwargs):
        # 如果捕获的是AdapterFetchRequestException基类的异常，那么直接抛出
        if isinstance(err, AdapterFetchRequestException):
            raise err

        # 如果是其他异常，则先交由父类记录一下，然后统一抛除采集请求的异常
        try:
            super(FetchClient, self).error_handle(err, *args, **kwargs)
        except Exception as e:
            log.warning(f"Parent handle error({e})")
        raise AdapterFetchApiRequestException(err)


class FetchJsonResultClient(FetchClient):
    @property
    def success_flag(self):
        raise NotImplementedError

    @property
    def flag_key_name(self):
        raise NotImplementedError

    @property
    def data_key_name(self):
        raise NotImplementedError

    @property
    def error_key_name(self):
        return None

    def parse_biz_result(self, result, *args, **kwargs):
        try:
            result = json.loads(result)
        except ValueError:
            return self.parse_json_error_handle(result)
        if not self.check_biz_result(result):
            log.warning(f"{self.name}Response error. detail is {result}")
            if self.error_key_name and self.error_key_name in result:
                error = result[self.error_key_name]
                return self.parse_error_handle(error, *args, **kwargs)
            else:
                return self.parse_error_handle(result, *args, **kwargs)

        data_key_name = self.data_key_name

        if data_key_name:
            result = extract(result, data_key_name)
        try:
            result = self.clean_result(result)
        except Exception as e:
            log.warning(f"Clean result error({e})")
            return self.parse_error_handle(result, *args, **kwargs)
        else:
            return result

    def check_biz_result(self, result):
        if not result:
            return False
        if not self.flag_key_name:
            return True
        success_flag = extract(result, self.flag_key_name)
        return self.compare_flag(success_flag)

    def compare_flag(self, success_flag):
        return success_flag == self.success_flag

    def clean_result(self, result):
        return result

    def get_count(self, *args, **kwargs):
        count = 0
        try:
            data = self.handle_common(*args, **kwargs)
        except Exception as e:
            log.error(f"get count error {e}")
        else:
            count = self.extract_count(data)
        return count

    @classmethod
    def extract_count(cls, data):
        return 0


class FetchRestfulClient(FetchJsonResultClient):
    def parse_response(self, response, *args, **kwargs):
        error = self.check_response(response)
        if error:
            return self.error_handle(AdapterFetchApiRequestException(message=error), *args, **kwargs)
        try:
            result = response.json()
        except Exception as e:
            log.warning(f"parse response error({e}),code is {response.status_code},content is {response.content}")
            return self.error_handle(e, *args, **kwargs)
        else:
            return result

    @classmethod
    def check_response(cls, response):
        if response.status_code != 200:
            return f"invalid http status code({response.status_code})"
        return ""
