import datetime
import uuid
from typing import List, Dict

from caasm_persistence_base.handler.storage.manager import storage_manager
from caasm_persistence_base.handler.storage.model.response import (
    SaveResponse,
    SaveMultiResponse,
    UpdateResponse,
    CommonResponse,
    DeleteResponse,
)
from caasm_tool.constants import DATE_FORMAT, DATETIME_FORMAT
from caasm_tool.util import SingletonInstance


class BasePersistenceHandler(metaclass=SingletonInstance):
    DEFAULT_TABLE = None

    def __init__(self, client=None):
        self._client = client

        if not client:
            self._client = storage_manager.build_client(self.storage_type)

    @property
    def storage_type(self) -> str:
        raise NotImplementedError

    def table(self, table=None):
        if not table:
            table = self.DEFAULT_TABLE
        if not table:
            raise ValueError(f"{self.name} table define error")
        return table

    def save_direct(self, data: Dict, table=None, **kwargs) -> SaveResponse:
        raise NotImplementedError()

    def save_multi_direct(self, records: List[Dict], table=None, **kwargs) -> SaveMultiResponse:
        raise NotImplementedError()

    def update_direct(self, condition, values, table=None, **kwargs) -> UpdateResponse:
        raise NotImplementedError()

    def update_multi_direct(self, condition, values, table=None, **kwargs):
        raise NotImplementedError()

    def update_stream_direct(self, mappers: List[Dict], table=None, **kwargs) -> UpdateResponse:
        raise NotImplementedError()

    def get_direct(self, condition, fields=None, table=None):
        raise NotImplementedError()

    def delete_multi(self, condition, table=None):
        raise NotImplementedError()

    def delete_one(self, condition, table=None) -> DeleteResponse:
        raise NotImplementedError()

    def count(self, condition=None, table=None):
        raise NotImplementedError()

    def get_size(self, table=None):
        return 0

    def find_direct(
        self,
        condition=None,
        fields=None,
        sort_fields=None,
        offset=None,
        limit=None,
        table=None,
        **kwargs,
    ):
        raise NotImplementedError()

    def save_file(self, file_content: bytes, filename=None):
        raise NotImplementedError()

    def get_file(self, file_id):
        raise NotImplementedError()

    def check_file_exists(self, file_id):
        raise NotImplementedError()

    def delete_file(self, file_id):
        raise NotImplementedError()

    def drop(self, table_name=None) -> CommonResponse:
        raise NotImplementedError()

    def rename(self, ori_table_name, new_table_name, **kwargs) -> CommonResponse:
        raise NotImplementedError()

    def exists(self, ori_table_name):
        return False

    def find_distinct(self, field, condition=None, table=None, **kwargs):
        return []

    def index_is_exists(self, index_name, table=None):
        return False

    def create_index_direct(self, index_name, indices, table=None, **kwargs):
        pass

    # ########################基础属性##################

    @classmethod
    def build_delete_response(cls, flag, msg=None, deleted_count=0) -> DeleteResponse:
        return DeleteResponse(flag=flag, msg=msg, deleted_count=deleted_count)

    @classmethod
    def build_save_response(cls, flag, msg=None, inserted_id=None) -> SaveResponse:
        return SaveResponse(flag=flag, msg=msg, inserted_id=inserted_id)

    @classmethod
    def build_save_multi_response(cls, flag, msg=None, inserted_ids=None) -> SaveMultiResponse:
        return SaveMultiResponse(flag=flag, msg=msg, inserted_ids=inserted_ids)

    @classmethod
    def build_update_response(cls, flag, msg=None, modified_count=None) -> UpdateResponse:
        return UpdateResponse(flag=flag, msg=msg, modified_count=modified_count)

    @classmethod
    def build_common_response(cls, flag, msg=None, data=None) -> CommonResponse:
        return CommonResponse(flag=flag, msg=msg, data=data)

    @classmethod
    def build_snapshot_table(cls, table_flag, date=None):
        date = date or datetime.datetime.today().strftime(DATE_FORMAT)
        return f"snapshot.{table_flag}.{date}"

    def build_tmp_table(self, table_flag):
        return f"{table_flag}.{self.get_id()}"

    def get_id(self):
        return f"{datetime.date.today()}{uuid.uuid4()}".replace("-", "")

    @property
    def client(self):
        return self._client

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def now(self):
        return datetime.datetime.now().strftime(DATETIME_FORMAT)
