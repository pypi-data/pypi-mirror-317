import abc
import math
import time
import traceback
from functools import wraps
from typing import Optional

import requests

from caasm_adapter_base.base import CategoryHandler
from caasm_adapter_base.fetcher.fetch_service_base import BaseFetchService
from caasm_adapter_base.sdk.adapter_fetch import BaseAdapterFetchSdk
from caasm_adapter_base.util.exception import AdapterFetchAuthFailedException, AdapterFetchRequestException
from caasm_service_base.constants.adapter import AdapterInstanceConnectionStatus, AdapterFetchStatus
from caasm_service_base.entity.adapter import Adapter
from caasm_tool.config import log
from caasm_tool.constants import StrEnum
from caasm_tool.util import load_class


class Status(StrEnum):
    EMPTY = "empty"
    HAVE_DATA = "hava_data"
    SKIP = "skip"
    ALL_FAILED = "all_failed"


def _check_async(func=None):
    def wrapper(fun):
        @wraps(fun)
        def inner(self, *args, **kwargs):
            if not self.async_flag:
                return
            return fun(self, *args, **kwargs)

        return inner

    if not func:
        return wrapper
    else:
        return wrapper(func)


class BaseFetchHandler(CategoryHandler, abc.ABC):
    def __init__(
        self,
        category,
        adapter_name,
        fetch_service: BaseFetchService,
        fetch_sdk: BaseAdapterFetchSdk,
    ):
        super().__init__(category, adapter_name)
        self._times = None
        self._wait_times = None
        self._fetch_entry = None
        self._count_entry = None
        self._condition_entry = None
        self._connection = {}
        self._session = None
        self._size = 100
        self._fetch_service: BaseFetchService = fetch_service
        self._fetch_sdk: BaseAdapterFetchSdk = fetch_sdk
        self._status = AdapterFetchStatus.INIT
        self._fetch_types = []
        self._error = None
        self._cleaner_mapper = {}
        self._adapter: Optional[Adapter] = None
        self._table_name = None
        self._connect_status = AdapterInstanceConnectionStatus.UNKNOWN

    def initialize(self):
        super().initialize()
        self._load_entry()
        self._load_cleaners()
        self._load_size()
        self._load_fetch_type()
        self._load_times()
        self._load_fetch_record()

    def _load_times(self):
        self._times = 3
        self._wait_times = 10

    def _load_fetch_type(self):
        adapter_fetch_types = self.fs.fetch_type_mapper.get(self.category)
        self._fetch_types = adapter_fetch_types
        if not self._fetch_types:
            raise ValueError(f"{self.name} Category({self.category})")

    def _load_entry(self):
        self._fetch_entry = load_class(self.fs.point)
        condition_point = self.fs.condition_point
        self._condition_entry = load_class(condition_point) if condition_point else None
        self._count_entry = load_class(self.fs.count_point) if self.fs.count_point else None

    def _load_cleaner(self, clean_meta_point, fetch_type):
        raise NotImplementedError()

    def _load_cleaners(self):
        cleaner_mapper = self.fs.cleaner_mapper.get(self.category) or {}
        for fetch_type, _clean_entry in cleaner_mapper.items():
            _cleaners = []
            for _clean_meta_point in _clean_entry:
                _cleaner = self._load_cleaner(_clean_meta_point, fetch_type)
                _cleaners.append(_cleaner)
            self._cleaner_mapper[fetch_type] = _cleaners

    def _load_size(self):
        self._size = self.fs.size

    def _load_fetch_record(self):
        raise NotImplementedError()

    def _call(self, entry, error_back=None, times=None, *args, **kwargs):
        times = times or self._times
        error = None
        while times:
            try:
                result = entry(connection=self._connection, session=self.session, *args, **kwargs)
            except Exception as e:
                error = e
                error_traceback = traceback.format_exc()
                log.error(error_traceback)
                errors = []
                if error.message:
                    if isinstance(error.message, Exception):
                        errors.append(error.message.__str__())
                    else:
                        errors.append(str(error.message))
                if error_traceback:
                    errors.append(error_traceback)
                error.message = "\n".join(errors)
            else:
                return self.success(result)
            finally:
                if error:
                    times -= 1
                    if times:
                        log.info("call error, wait next")
                        time.sleep(self._wait_times)
                        continue

                    if isinstance(error, AdapterFetchAuthFailedException):
                        self._connect_status = AdapterInstanceConnectionStatus.FAILED
                    err = error.message if isinstance(error, AdapterFetchRequestException) else f"采集失败：{error}"
                    return self.failed(err, error_back)

    def _do_loop_fetch(self, fetch_type, condition):
        index = 0
        while True:
            status = self.fetch(fetch_type, index, condition)
            if status == Status.EMPTY:
                break
            index += 1

    def _save_data(self, data):
        if not data:
            return
        self._fetch_sdk.save_factory(data, table=self._table_name, size=self._size)

    def _build_fetch_direct(self, fetch_type, page_index, condition):
        response = self._call(
            self._fetch_entry, fetch_type=fetch_type, page_index=page_index, page_size=self._size, condition=condition
        )
        if not response.flag:
            self._error = response.message
            raise ValueError(response.message)
        self._save_data(response.data)
        if not response.data:
            return Status.EMPTY
        return Status.HAVE_DATA

    def set_connection(self, connection):
        self._connection = connection

    def fetch(self, fetch_type, index, condition):
        return self._build_fetch_direct(fetch_type, index, condition)

    def _do_count_fetch(self, fetch_type, condition):
        count_response = self._call(self._count_entry, error_back=0, fetch_type=fetch_type, condition=condition)
        if not count_response.flag:
            raise ValueError(count_response.message)
        times = int(math.ceil(count_response.data / self._size))

        for index in range(times):
            self.fetch(fetch_type, index, condition)

    def _finish_fetch_hook(self):
        pass

    def _find_cleaner(self, fetch_type):
        return self._cleaner_mapper.get(fetch_type) or self._cleaner_mapper.get("default") or []

    def _record_status(self):
        pass

    def fetch_by_fetch_type(self, fetch_type):
        if self._condition_entry:
            condition = self._call(self._condition_entry, error_back={}, fetch_type=fetch_type).data
        else:
            condition = {}
        if self._count_entry:
            return self._do_count_fetch(fetch_type, condition)
        return self._do_loop_fetch(fetch_type, condition)

    def clean_by_fetch_type(self, fetch_type):
        _cleaners = self._find_cleaner(fetch_type)
        for _cleaner in _cleaners:
            _cleaner.clean()

    def fetch_all(self):
        flags = set()
        for fetch_type in self._fetch_types:
            try:
                self.fetch_by_fetch_type(fetch_type)
            except Exception as e:
                self._error = str(e)
                log.error(f"FetchType : {fetch_type} handle error({e}, {traceback.format_exc()})")
                flags.add(False)

        if len(flags) == 1 and not list(flags)[0]:
            self._status = AdapterFetchStatus.FAILED

    def clean_all(self):
        for fetch_type in self._fetch_types:
            self.clean_by_fetch_type(fetch_type)

    def handle_core(self, *args, **kwargs):
        self.fetch_all()
        self._finish_fetch_hook()
        self.clean_all()
        self._record_status()
        return self._status, self._error

    @property
    def session(self):
        if self._session is None:
            self._session = requests.Session()
        return self._session

    @property
    def fs(self):
        return self.adapter.fetch_setting

    @property
    def adapter(self):
        return self._adapter
