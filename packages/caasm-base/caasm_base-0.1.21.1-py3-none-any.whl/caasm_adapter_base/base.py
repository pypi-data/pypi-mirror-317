import abc
import logging
import traceback
from dataclasses import dataclass
from functools import cached_property
from typing import Optional

from caasm_service_base.constants.adapter import AdapterInnerType
from caasm_service_base.entity.adapter import Adapter


@dataclass
class Response(object):
    flag: bool
    message: str
    data: any


class BaseHandler(object):
    def __init__(self, adapter_name):
        self._adapter_name = adapter_name
        self._index = None
        self._adapter: Optional[Adapter] = None
        self._adapter_inner_type: Optional[AdapterInnerType] = None
        self._init_flag = False

    def initialize(self, *args, **kwargs):
        adapter = self._load_adapter()
        self._adapter_inner_type = adapter.adapter_inner_type
        self._adapter = adapter
        self._after_load_adapter()

    def _after_load_adapter(self):
        pass

    def handle(self, *args, **kwargs):
        try:
            result = self.handle_core(*args, **kwargs)
        except Exception as exc:
            logging.error(f"Name({self.name}) handle error({traceback.format_exc()})")
            return self.error_handle(exc)
        else:
            return result

    def _load_adapter(self):
        raise NotImplementedError()

    def finish_init(self):
        self._init_flag = True

    def error_handle(self, exc=None):
        raise exc

    def handle_core(self, *args, **kwargs):
        raise NotImplementedError

    def finish(self):
        pass

    def get_index(self):
        pass

    @classmethod
    def success(cls, data=None):
        return Response(flag=True, data=data, message="")

    @classmethod
    def failed(cls, message="", data=None):
        return Response(flag=False, data=data, message=message)

    @property
    def init_flag(self):
        return self._init_flag

    @property
    def adapter_name(self):
        return self._adapter_name

    @cached_property
    def index(self):
        return self.get_index()

    @property
    def adapter(self):
        return self._adapter

    @property
    def adapter_inner_type(self):
        return self._adapter_inner_type

    @property
    def name(self):
        return str(self.__class__)


class CategoryHandler(BaseHandler, abc.ABC):
    def __init__(self, category, adapter_name):
        super(CategoryHandler, self).__init__(adapter_name)
        self._category = category

    @property
    def category(self):
        return self._category
