class AdapterFetchCode(object):
    NOT_SUPPORT_API = 10000
    API_PARAMS_INVALID = 10001
    API_AUTH_FAILED = 10002
    API_REQUEST_ERROR = 20000
    API_RESPONSE_ERROR = 20001
    API_JSON_ERROR = 20002
    API_CALL_TIMEOUT = 30000


ADAPTER_FETCH_MSG = {
    AdapterFetchCode.NOT_SUPPORT_API: "API请求不存在",
    AdapterFetchCode.API_PARAMS_INVALID: "输入参数格式错误",
    AdapterFetchCode.API_RESPONSE_ERROR: "返回结果格式错误",
    AdapterFetchCode.API_JSON_ERROR: "返回结果作为JSON解析发生格式",
    AdapterFetchCode.API_CALL_TIMEOUT: "接口请求超时",
    AdapterFetchCode.API_AUTH_FAILED: "权限认证失败",
    AdapterFetchCode.API_REQUEST_ERROR: "API请求错误，无法正常响应",
}
