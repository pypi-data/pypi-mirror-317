from dataclasses import dataclass
from typing import Any, List, AnyStr


@dataclass
class SaveResponse(object):
    flag: bool = False
    msg: AnyStr = ""
    inserted_id: Any = None


@dataclass
class SaveMultiResponse(object):
    flag: bool = False
    msg: AnyStr = ""
    inserted_ids: List[Any] = None


@dataclass
class UpdateResponse(object):
    flag: bool = False
    msg: AnyStr = ""
    modified_count: int = 0


@dataclass
class DeleteResponse(object):
    flag: bool = False
    msg: AnyStr = ""
    deleted_count: int = 0


@dataclass
class CommonResponse(object):
    flag: bool = False
    msg: AnyStr = ""
    data: Any = None
