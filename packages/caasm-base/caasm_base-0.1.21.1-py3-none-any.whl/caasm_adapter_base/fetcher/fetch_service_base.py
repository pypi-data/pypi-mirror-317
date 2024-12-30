from typing import List, Dict


class BaseFetchService:
    @classmethod
    def build_fetch_data_condition(cls, fetch_type=None, data_ids=None):
        raise NotImplementedError()

    @classmethod
    def build_fetch_data_table(cls, adapter_name, adapter_instance_id, fetch_type, index):
        raise NotImplementedError()

    def delete_fetch_data(self, table, data_ids):
        raise NotImplementedError()

    def delete_fetch_data_by_fetch_type(self, table, fetch_type):
        raise NotImplementedError()

    def save(self, records: List[Dict], table=None, **kwargs):
        raise NotImplementedError()

    def update(self, mappers: List[Dict], table=None, simple_values=True, **kwargs):
        raise NotImplementedError()

    def drop(self, table_name=None):
        raise NotImplementedError()

    def rename(self, ori_table_name, new_table_name, **kwargs):
        raise NotImplementedError()
