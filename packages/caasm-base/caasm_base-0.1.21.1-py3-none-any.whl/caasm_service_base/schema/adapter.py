from caasm_persistence_base.schema.base import (
    BaseSchema,
    EnumField,
    ObjectIdField,
    fields,
    DocumentSchema,
)
from caasm_service_base.constants.adapter import AdapterFetchType, AdapterFetchMode, AdapterInnerType, AdapterRunMode
from caasm_service_base.entity.adapter import (
    Adapter,
    ConnectionParam,
    FetchOther,
    FetchSetting,
    MergeSetting,
    ConvertSetting,
    FabricSetting,
    ValidateRule,
)


class ValidateRuleSchema(BaseSchema):
    entity_define = ValidateRule

    name = fields.String(description="规则名称")
    error_hint = fields.String(description="错误提示", load_default="", allow_none=True)
    setting = fields.Dict(load_default=dict, description="配置信息", allow_none=True)


class ConnectionParamSchema(BaseSchema):
    entity_define = ConnectionParam

    name = fields.String(description="参数名称")
    display_name = fields.String(description="展示名称")
    description = fields.String(load_default="", description="描述信息")
    type = fields.String(description="参数类型")
    required = fields.Boolean(load_default=True, description="是否必传")
    default = fields.Raw(load_default=None, description="默认值")
    validate_rules = fields.Nested(ValidateRuleSchema, many=True, load_default=list)
    hidden = fields.Boolean(load_default=False, description="是否隐藏")


class FetchOtherSchema(BaseSchema):
    entity_define = FetchOther

    point = fields.Str(description="采集其他入口")
    size = fields.Int(description="采集其他数量", load_default=100)
    fetch_field = fields.Str(description="采集数据中的字段")
    field = fields.Str(description="采集其他信息中的字段【与采集数据中的字段对应】")
    property_name = fields.Str(description="采集后的其他字段存入到采集数据中的字段名称")


class FetchSettingSchema(BaseSchema):
    entity_define = FetchSetting

    type = EnumField(
        AdapterFetchType,
        by_value=True,
        load_default=AdapterFetchType.DISPOSABLE,
        description="采集方式",
    )
    point = fields.String(description="采集入口", load_default="")
    mode = EnumField(
        AdapterFetchMode,
        load_default=AdapterFetchMode.DEFAULT,
        by_value=True,
        description="采集方式，【默认、计算总数后再去采集】",
    )
    count_point = fields.String(load_default="", description="当采集模式是计算总数后时，获取总数的入口")
    fetch_type_mapper = fields.Dict(
        keys=fields.Str(), values=fields.List(fields.Str()), load_default=dict, description="采集数据的类型"
    )
    condition_point = fields.String(description="额外上下文入口", load_default="")
    size = fields.Int(description="采集数量", load_default=100)
    other_fetch_mapper = fields.Dict(
        keys=fields.Str(),
        values=fields.Dict(
            keys=fields.Str(),
            values=fields.Nested(FetchOtherSchema, many=True, description="其他采集信息", load_default=list),
        ),
        load_default=dict,
    )
    cleaner_mapper = fields.Dict(
        keys=fields.Str(),
        values=fields.Dict(keys=fields.Str(), values=fields.List(fields.Str())),
        load_default=dict,
        description="清洗函数映射",
    )
    finish_point = fields.String(load_default="", description="当采集结束后时，释放内存函数")
    is_need_test_service = fields.Boolean(load_default=False, description="是否需要测试链接服务")
    test_connection_point = fields.String(description="测试网络是否畅通函数入口", load_default=str, required=False)
    test_auth_point = fields.String(description="检测auth信息是否通过函数入口", load_default="", required=False)
    worker = fields.Int(load_default=1)


class MergeSettingSchema(BaseSchema):
    entity_define = MergeSetting

    policy = fields.String(
        description="策略信息",
        load_default="caasm_adapter.merger.policy.unique:UniquePolicy",
    )
    setting = fields.Dict(keys=fields.Str(), values=fields.Dict(), description="策略配置信息", load_default=dict)
    size = fields.Int(description="合并大小", load_default=100)


class ConvertSettingSchema(BaseSchema):
    entity_define = ConvertSetting

    size = fields.Int(load_default=100, description="转换大小")
    before_executor_mapper = fields.Dict(keys=fields.Str(), description="前公共的转换器", load_default=dict)
    executor_mapper = fields.Dict(description="转换器映射表", load_default=dict)
    after_executor_mapper = fields.Dict(keys=fields.Str(), description="后公共的转换器", load_default=dict)


class FabricSettingSchema(BaseSchema):
    entity_define = FabricSetting
    choose_point_mapper = fields.Dict(
        keys=fields.Str(),
        values=fields.Str(),
        description="选择入口【针对于同一个公共属性的一堆资产选一个最合适的资产】",
        load_default=dict,
    )


class AdapterSchema(DocumentSchema):
    entity_define = Adapter

    name = fields.String(description="适配器名称", load_default="")
    display_name = fields.String(load_default="", description="展示名称")
    description = fields.String(load_default="", description="描述信息")
    type = fields.String(load_default="", description="适配器类型")
    model_id = ObjectIdField(description="模型ID", load_default=None, required=False)
    adapter_inner_type = EnumField(
        AdapterInnerType,
        load_default=AdapterInnerType.NORMAL,
        by_value=True,
        description="适配器内部类型",
    )
    properties = fields.List(fields.String(), description="适配器属性", load_default=list, allow_none=True)
    company = fields.String(load_default=str, description="供应商")
    manufacturer_id = ObjectIdField(description="厂商ID（一个厂商对应多个适配器）", load_default=None)
    priority = fields.Int(load_default=1, description="优先级")
    logo = fields.String(load_default="")
    logo_id = ObjectIdField(description="logo文件ID", load_default=None)
    version = fields.String(description="版本信息", load_default="0.1")
    connection = fields.Nested(ConnectionParamSchema, many=True, load_default=list)
    fetch_setting = fields.Nested(FetchSettingSchema, load_default=dict)
    merge_setting = fields.Nested(MergeSettingSchema, load_default=dict)
    convert_setting = fields.Nested(ConvertSettingSchema, load_default=dict)
    fabric_setting = fields.Nested(FabricSettingSchema, load_default=dict)
    is_biz_useful = fields.Boolean(load_default=None)
    latest = fields.Boolean(load_default=True)
    pseudocode = fields.String(load_default=str)
    builtin = fields.Boolean(load_default=True)
    run_mode = EnumField(AdapterRunMode, by_value=True, load_default=AdapterRunMode.SHARE)
