from caasm_tool.constants import StrEnum


class AdapterInnerType(StrEnum):
    NORMAL = "normal"
    VIRTUAL = "virtual"
    PROXY = "proxy"


class AdapterFetchType(StrEnum):
    # 同步采集任务，直接拿到结果
    DISPOSABLE = "disposable"
    # 发起采集任务，异步查询采集结果
    POLLED = "polled"
    # 常驻型，比如http、tcp等待数据传输
    PERMANENT = "permanent"


class AdapterFetchMode(StrEnum):
    DEFAULT = "default"
    COMPUTE_PAGE = "compute_page"


class AdapterFetchStatus(StrEnum):
    INIT = "init"
    FETCHING = "fetching"
    SUCCESS = "success"
    FAILED = "failed"
    CANCEL = "cancel"


ADAPTER_FETCH_STATUS_MAPPER = {
    AdapterFetchStatus.INIT: "待采集",
    AdapterFetchStatus.FETCHING: "采集中",
    AdapterFetchStatus.SUCCESS: "采集成功",
    AdapterFetchStatus.FAILED: "采集失败",
    AdapterFetchStatus.CANCEL: "取消",
}


class AdapterInstanceRunStatus(StrEnum):
    INIT = "init"
    WAIT = "wait"
    DOING = "doing"
    FAILED = "failed"
    SUCCESS = "success"


class AdapterInstanceConnectionStatus(StrEnum):
    UNKNOWN = "unknown"
    SUCCESS = "success"
    FAILED = "failed"


class AdapterRunMode(StrEnum):
    SHARE = "share"
    INDEPENDENT = "independent"
