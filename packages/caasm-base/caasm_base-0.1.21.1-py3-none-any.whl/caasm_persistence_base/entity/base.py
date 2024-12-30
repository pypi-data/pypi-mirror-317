import datetime
from dataclasses import dataclass, asdict
from typing import Dict

from bson import ObjectId

from caasm_tool.constants import SortType


@dataclass
class BaseEntity(object):
    def as_dict(self):
        mapping = asdict(self)

        # 针对于mongo主键是_id，而python又是以下划线约定属性权限
        if "id" in mapping:
            mapping["_id"] = mapping.pop("id", None)
            if mapping["_id"] is None:
                mapping.pop("_id")
        return mapping


@dataclass
class TimeBaseEntity(BaseEntity):
    create_time: datetime.datetime
    update_time: datetime.datetime


@dataclass
class DocumentEntity(TimeBaseEntity):
    id: ObjectId


@dataclass
class IndexMeta(BaseEntity):
    field: str
    sort: SortType


@dataclass
class Index(BaseEntity):
    name: str
    field: IndexMeta
    setting: Dict
