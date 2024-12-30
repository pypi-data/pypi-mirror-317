from caasm_adapter_base.util.constants import ADAPTER_FETCH_MSG, AdapterFetchCode


class AdapterFetchRequestException(Exception):
    def __init__(self, code, message="", data=""):
        self.code = code
        self.message = message or ADAPTER_FETCH_MSG.get(code, "")
        self.data = data

    def __str__(self):
        return f"{self.__class__.__name__}(code='{self.code}', message='{self.message}', data='{self.data}')"

    __repr__ = __str__


class AdapterFetchApiNotSupportException(AdapterFetchRequestException):
    def __init__(self, message=""):
        super(AdapterFetchApiNotSupportException, self).__init__(AdapterFetchCode.NOT_SUPPORT_API, message)


class AdapterFetchApiParamsInvalidException(AdapterFetchRequestException):
    def __init__(self):
        super(AdapterFetchApiParamsInvalidException, self).__init__(AdapterFetchCode.API_PARAMS_INVALID)


class AdapterFetchApiRequestException(AdapterFetchRequestException):
    def __init__(self, message=""):
        super(AdapterFetchApiRequestException, self).__init__(AdapterFetchCode.API_REQUEST_ERROR, message)


class AdapterFetchApiResponseException(AdapterFetchRequestException):
    def __init__(self, message=""):
        super(AdapterFetchApiResponseException, self).__init__(AdapterFetchCode.API_RESPONSE_ERROR, message)


class AdapterFetchApiJSONException(AdapterFetchRequestException):
    def __init__(self, message=""):
        super(AdapterFetchApiJSONException, self).__init__(AdapterFetchCode.API_JSON_ERROR, message)


class AdapterFetchApiCallTimeoutException(AdapterFetchRequestException):
    def __init__(self):
        super(AdapterFetchApiCallTimeoutException, self).__init__(AdapterFetchCode.API_CALL_TIMEOUT)


class AdapterFetchAuthFailedException(AdapterFetchRequestException):
    def __init__(self):
        super(AdapterFetchAuthFailedException, self).__init__(AdapterFetchCode.API_AUTH_FAILED)
