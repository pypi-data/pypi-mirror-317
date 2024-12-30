import abc
import logging
from collections import defaultdict

from caasm_tool.util import extract

_LOG = logging.getLogger()


class FetchBaseCleaner(object, metaclass=abc.ABCMeta):
    _DEFAULT_FETCH_TYPE = "default"
    _SORT_FIELDS = [("_id", 1)]
    _RELATION_FIELDS = ("_id", "id", "record")

    def __init__(self, adapter_name, adapter_instance_id, index, category, fetch_type, fetch_sdk, fetch_service):
        self._adapter_name = adapter_name
        self._adapter_name = adapter_name
        self._adapter_instance_id = adapter_instance_id
        self._index = index
        self._category = category
        self._fetch_type = fetch_type if fetch_type != self._DEFAULT_FETCH_TYPE else None

        self.__fetch_table_cache = None
        self._fetch_sdk = fetch_sdk
        self._fetch_service = fetch_service

    def clean(self):
        core_records = self.find_fetch_record(fields=["_id"])
        for index in range(0, len(core_records), self.size):
            condition = {"_id": {"$in": [i["_id"] for i in core_records[index : index + self.size]]}}
            fetch_records = self._fetch_sdk.find_factory(condition, table=self.fetch_table)
            new_fetch_records = self.clean_multi(fetch_records)
            if not new_fetch_records:
                continue
            self.modify_fetch_records(new_fetch_records)

    def clean_multi(self, fetch_records):
        result = []
        for fetch_record in fetch_records:
            _id = fetch_record["_id"]
            _adapter_data = fetch_record["adapter"]
            try:
                _cleaned_result = self.clean_single(_adapter_data)
            except Exception as e:
                _class_name = self.__class__.__name__
                _LOG.error(f"Fetch[{_class_name}] table({self.fetch_table}) clean error({e}). record_id is {_id}")
            else:
                if not _cleaned_result:
                    continue
                _adapter_data.update(_cleaned_result)
                result.append(fetch_record)
        return result

    def clean_single(self, detail):
        return detail

    def modify_fetch_records(self, fetch_records):
        return self._fetch_sdk.update_factory_upstream(fetch_records, table=self.fetch_table)

    def find_fetch_record(self, fields=None, relation_link=False, fetch_type=None, data_ids=None, condition=None):
        result = []
        if condition is None:
            condition = {}

        fetch_type = fetch_type or self._fetch_type
        my_condition = self._fetch_service.build_fetch_data_condition(fetch_type=fetch_type, data_ids=data_ids)
        condition.update(my_condition)

        min_id = None
        fields = self._build_fields(fields)

        while True:

            id_query = {"$gt": min_id} if min_id else {}
            if id_query:
                if "_id" in condition:
                    condition["_id"].update(id_query)
                else:
                    condition["_id"] = id_query

            tmp_fetch_records = self._fetch_sdk.find_factory(
                condition,
                self.fetch_table,
                limit=self.size,
                fields=fields,
                sort_fields=self._SORT_FIELDS,
                relation_link=relation_link,
            )
            if not tmp_fetch_records:
                break
            min_id = tmp_fetch_records[-1]["_id"]
            result.extend(tmp_fetch_records)
        return result

    def delete_fetch_records(self, records):
        self._fetch_sdk.delete_factory(records, self.fetch_table)

    def save_fetch_records(self, records):
        self._fetch_sdk.save_factory(records, self.fetch_table)

    @property
    def indexes(self):
        return ()

    @property
    def size(self):
        return 100

    @property
    def fetch_table(self):
        if not self.__fetch_table_cache:
            self.__fetch_table_cache = self._fetch_service.build_fetch_data_table(
                adapter_name=self._adapter_name,
                adapter_instance_id=self._adapter_instance_id,
                fetch_type=self._category,
                index=self._index,
            )
        return self.__fetch_table_cache

    @classmethod
    def _build_fields(cls, fields):
        return [(i if i in cls._RELATION_FIELDS else f"record.{i}") for i in fields] if fields else []


class FetchTotalBaseCleaner(FetchBaseCleaner):
    def clean(self):
        total_records = self.find_fetch_record(relation_link=True)
        id_records = [{"id": r["id"], "_id": r["_id"]} for r in total_records]
        new_records = self.build(total_records)
        self.delete_fetch_records(id_records)
        self.save_fetch_records(new_records)

    def build(self, records):
        biz_records = [record["adapter"] for record in records]
        result = []
        if not biz_records:
            return result

        new_biz_records = self.build_common(biz_records)

        for new_biz_record in new_biz_records:
            _internal_data = self.clean_internal(records[0]["internal"], new_biz_record)
            _detail = {"internal": _internal_data, "adapter": new_biz_record}
            result.append(_detail)
        return result

    def build_common(self, biz_records):
        return biz_records

    def clean_internal(self, record, new_record):
        return record


class FetchLinkBaseCleaner(FetchBaseCleaner):
    @property
    def main_fetch_type(self):
        #   外键资产，比如关联到资产的漏洞
        raise NotImplementedError

    @property
    def main_field(self):
        raise NotImplementedError

    @property
    def link_fetch_type(self):
        #   主键资产，比如资产
        raise NotImplementedError

    @property
    def link_field(self):
        #   主键资产使用的字段
        return self.main_field

    @property
    def main_field_ref(self):
        return f"adapter.{self.main_field}"

    @property
    def link_field_ref(self):
        return f"adapter.{self.link_field}"

    @property
    def dst_field(self):
        return self.main_fetch_type

    def _build_relation_mapper(self, records):
        relation_mapper = defaultdict(list)
        for record in records:
            relation_mapper[self._parse_relation_key(record)].append(record)
        return relation_mapper

    def _build_link_mapper(self, relation_ids):
        tmp_condition = {self.link_field_ref: {"$in": relation_ids}}
        fields = ["id", self.link_field_ref]
        records = self.find_fetch_record(fields=fields, condition=tmp_condition, fetch_type=self.link_fetch_type)

        link_mapper = defaultdict(list)
        for record in records:
            link_mapper[self._parse_relation_key(record)].append(record["id"])
        return link_mapper

    def _parse_relation_key(self, record):
        return extract(record, self.main_field_ref)

    def clean(self):
        records = self.find_fetch_record(fetch_type=self.main_fetch_type, fields=[self.main_field_ref])
        relation_mapper = self._build_relation_mapper(records)
        relation_keys = list(relation_mapper.keys())

        for index in range(0, len(relation_keys), self.size):
            tmp_relation_keys = relation_keys[index : index + self.size]
            link_mapper = self._build_link_mapper(tmp_relation_keys)

            total_relation_records, buffer = [], []

            for tmp_relation_key in tmp_relation_keys:
                total_relation_records.extend(relation_mapper[tmp_relation_key])

            for link_id, record_ids in link_mapper.items():
                data_ids = [i["_id"] for i in relation_mapper[link_id]]
                fetch_records = self.find_fetch_record(
                    relation_link=True,
                    fetch_type=self.main_fetch_type,
                    data_ids=data_ids,
                )

                for fetch_record in fetch_records:
                    for record_id in record_ids:
                        link = self._fetch_sdk.build_link(
                            record_id, f"adapter.{self.dst_field}", fetch_record["adapter"]
                        )
                        buffer.append(link)
            self._fetch_sdk.delete_factory(total_relation_records, table=self.fetch_table)
            self._fetch_sdk.save_core(self.fetch_table, buffer, self.size)
