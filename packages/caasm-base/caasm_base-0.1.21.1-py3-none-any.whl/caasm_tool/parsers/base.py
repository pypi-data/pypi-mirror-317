import abc
import logging
import traceback
from functools import cached_property

from caasm_tool.util import restore, extract

log = logging.getLogger()


class CaasmBaseFileParser(abc.ABC):
    _ASSET_TYPE_FIELD = "base.asset_type"
    _MODEL_NAME_FIELD = "base.model_name"
    _EMPTY_VALUES = ("", None, [], {})

    def __init__(self):
        self.context = {}

    @staticmethod
    def get_parser_name():
        raise NotImplementedError

    @staticmethod
    def get_category():
        raise NotImplementedError

    @staticmethod
    def get_model_name():
        raise NotImplementedError

    @staticmethod
    def get_data_type():
        raise NotImplementedError

    @classmethod
    def get_asset_type(cls, record):
        raise NotImplementedError

    def parse(self, file_content):
        raise NotImplementedError

    def clean(self, data):
        return data

    def ignore(self, data):
        """
        过滤
        :param data:
        :return:
        """
        pass

    def handle(self, file_content):
        return self.handle_common(file_content)

    def handle_common(self, file_content):
        result = []
        for info in self.parse(file_content):
            if not info:
                continue
            temp_info = info
            if not isinstance(temp_info, list):
                temp_info = [temp_info]
            try:
                cleaned_info = []
                for _info in temp_info:
                    _cleaned_info = self.clean(_info)
                    if self.ignore(_cleaned_info):
                        continue
                    self.other_operations(_cleaned_info)
                    self.clean_system(_cleaned_info, _info)
                    cleaned_info.append(_cleaned_info)
            except Exception as e:
                log.warning(f"Clean file({self.__class__}) single row error({e}), detail is {traceback.format_exc()}")
            else:
                result.extend(cleaned_info)
        result = self.clean_result(result)
        return result

    def clean_system(self, new_info, old_info):
        asset_type = self.get_asset_type(old_info)
        _asset_type_field = self._ASSET_TYPE_FIELD
        self.restore(_asset_type_field, asset_type, new_info) if not self.extract(new_info, _asset_type_field) else ...
        self.restore(self._MODEL_NAME_FIELD, self.get_model_name(), new_info)

    def clean_result(self, result):
        return result

    @classmethod
    def restore(cls, field, value, record):
        restore(field, value, record) if value not in cls._EMPTY_VALUES else ...

    @classmethod
    def extract(cls, record, field):
        return extract(record, field)

    def other_operations(self, _cleaned_info):
        pass


class ConvertMixIn(object):
    _PARSE_METHOD_PREFIX = "_parse_"

    def execute_convert_row(self, row):
        result = {}
        for callback in self.parse_methods:
            try:
                callback(row, result)
            except Exception as e:
                log.error(f"{callback} execute failed row({row})，error({e}) detail is {traceback.format_exc()}")
        return result

    @cached_property
    def parse_methods(self):
        result = []
        for name in dir(self):
            if not name.startswith(self._PARSE_METHOD_PREFIX):
                continue
            callback = getattr(self, name, None)
            if not callable(callback):
                continue
            result.append(callback)
        return result
