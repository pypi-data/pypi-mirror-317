from enum import Enum, IntEnum

# 日期格式
DATE_FORMAT = "%Y_%m_%d"
DATE_FORMAT_1 = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATETIME_FORMAT_2 = "%Y-%m-%d %H:%M:%S%z"
DATETIME_FORMAT_3 = "%Y%m%d%H%M%S"
DATETIME_MIC_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
GMT_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
TIME_FORMAT = "%H:%M:%S"


class StrEnum(str, Enum):
    pass


class ParamType(StrEnum):
    PASSWORD = "password"
    STRING = "string"
    URL = "url"
    INTEGER = "integer"
    LIST = "list"
    FILE_ID = "file_id"
    CHOICE = "choice"


class ValidateRuleType(StrEnum):
    REG = "reg"
    ANY = "any"
    STRING = "string"
    INTEGER = "integer"
    LIST = "list"


class OperatorEnum(StrEnum):
    EQUAL = "equal"
    IN = "in"
    EMPTY = "empty"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"


class OperatorRelationType(StrEnum):
    AND = "and"
    OR = "or"


class OperatorType(StrEnum):
    SIMPLE = "simple"
    COMPLEX = "complex"


class AuthType(StrEnum):
    PASSWORD = "password"


class SortType(IntEnum):
    DESC = -1
    ASC = 1


class AqlParamsType(StrEnum):
    FIXED = "fixed"
    DYNAMIC = "dynamic"


PROTOCOL_DEFAULT_MAPPER = {
    "http": 80,
    "https": 443,
    "mysql": 3306,
    "mongodb": 27017,
}
