import datetime
import json

import bson
import marshmallow_enum
from bson import ObjectId
from marshmallow import Schema, post_load, EXCLUDE, missing
from marshmallow import ValidationError, fields

from caasm_persistence_base.entity.base import Index, IndexMeta
from caasm_tool.constants import DATETIME_FORMAT, SortType


class ObjectIdField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return bson.ObjectId(value)
        except Exception:
            raise ValidationError("invalid ObjectId `%s`" % value)

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return missing
        return value


class DateTimeField(fields.DateTime):
    def __init__(self, format=DATETIME_FORMAT, **kwargs):
        super(DateTimeField, self).__init__(format, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        if not value:  # Falsy values, e.g. '', None, [] are not valid
            raise self.make_error("invalid", input=value, obj_type=self.OBJ_TYPE)
        data_format = self.format or self.DEFAULT_FORMAT
        func = self.DESERIALIZATION_FUNCS.get(data_format)
        if func:
            try:
                return func(value)
            except (TypeError, AttributeError, ValueError) as error:
                raise self.make_error("invalid", input=value, obj_type=self.OBJ_TYPE) from error
        else:
            if isinstance(value, (datetime.datetime, datetime.date)):
                return value
            try:
                return self._make_object_from_format(value, data_format)
            except (TypeError, AttributeError, ValueError) as error:
                raise self.make_error("invalid", input=value, obj_type=self.OBJ_TYPE) from error


class BytesField(fields.Field):
    def _validate(self, value, error=ValidationError("Invalid value")):
        if not isinstance(value, bytes):
            raise ValidationError("Invalid input type.")

        if value is None or value == b"":
            raise error


EnumField = marshmallow_enum.EnumField


class BaseSchema(Schema):
    entity_define = None

    class Meta:
        unknown = EXCLUDE

    @post_load
    def to_entity(self, data, many=None, **kwargs):
        return self.entity_define(**data)

    def to_dicts(self, data, many=True):
        str_data = self.dumps(obj=data, many=many, default=self.handle_objectid)
        result = json.loads(str_data)
        return result

    @classmethod
    def handle_objectid(cls, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        raise TypeError("Unable to serialize object of type {}".format(type(obj)))


class TimeBaseSchema(BaseSchema):
    create_time = DateTimeField(load_default=datetime.datetime.now, description="创建时间")
    update_time = DateTimeField(load_default=datetime.datetime.now, description="更新时间")


class DocumentSchema(TimeBaseSchema):
    id = ObjectIdField(data_key="_id", load_default=ObjectId, description="主键ID", allow_none=True)


class TimeBaseNoneSchema(BaseSchema):
    create_time = DateTimeField(load_default=None, description="创建时间")
    update_time = DateTimeField(load_default=None, description="更新时间")


class DocumentNoneSchema(TimeBaseNoneSchema):
    id = ObjectIdField(data_key="_id", load_default=None, description="主键ID", allow_none=True)


class IndexMetaSchema(BaseSchema):
    entity_define = IndexMeta

    field = fields.Str(description="字段名称")
    sort = EnumField(SortType, by_value=True, description="排序方式")


class IndexSchema(BaseSchema):
    entity_define = Index

    name = fields.Str(description="索引名称")
    field = fields.List(fields.Nested(IndexMetaSchema()), description="索引信息")
    setting = fields.Dict(description="其他信息", load_default=dict)
