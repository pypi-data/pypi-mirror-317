import datetime
from dataclasses import dataclass
from typing import List, Dict

from bson import ObjectId

from caasm_persistence_base.entity.base import BaseEntity
from caasm_service_base.constants.adapter import AdapterInnerType, AdapterFetchMode, AdapterFetchType


@dataclass
class Adapter(BaseEntity):
    name: str
    display_name: str
    model_id: ObjectId
    version: str
    type: str
    is_biz_useful: bool
    priority: int
    properties: List[str]
    connection: List["ConnectionParam"]
    fetch_setting: "FetchSetting"
    merge_setting: "MergeSetting"
    convert_setting: "ConvertSetting"
    fabric_setting: "FabricSetting"
    description: str
    adapter_inner_type: AdapterInnerType
    logo: str
    logo_id: ObjectId
    create_time: datetime.datetime
    update_time: datetime.datetime
    company: str
    manufacturer_id: ObjectId
    id: ObjectId
    latest: bool
    #   生成的随机码，用于隔离存放适配器代码
    pseudocode: str
    #   是否为内建适配器
    builtin: bool
    #   运行模式
    run_mode: str


@dataclass
class ValidateRule(BaseEntity):
    name: str
    error_hint: str
    setting: Dict


@dataclass
class ConnectionParam(BaseEntity):
    name: str
    display_name: str
    description: str
    type: str
    required: bool
    default: any
    validate_rules: List[ValidateRule]
    hidden: bool


@dataclass
class FetchOther(BaseEntity):
    point: str
    size: int
    fetch_field: str
    field: str
    property_name: str


@dataclass
class FetchSetting(BaseEntity):
    type: AdapterFetchType
    mode: AdapterFetchMode
    fetch_type_mapper: Dict[str, List[str]]
    condition_point: str
    point: str
    count_point: str
    size: int
    other_fetch_mapper: Dict[str, Dict[str, FetchOther]]
    cleaner_mapper: Dict[str, Dict[str, List[str]]]
    finish_point: str
    is_need_test_service: bool
    test_connection_point: str
    test_auth_point: str
    worker: int


@dataclass
class MergeSetting(BaseEntity):
    policy: str
    setting: Dict
    size: int


@dataclass
class ConvertSetting(BaseEntity):
    size: int
    before_executor_mapper: Dict
    executor_mapper: Dict
    after_executor_mapper: Dict


@dataclass
class FabricSetting(BaseEntity):
    choose_point_mapper: Dict[str, str]
