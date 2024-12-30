from collections import defaultdict

import nanoid

from caasm_persistence_base.handler.storage.base import BasePersistenceHandler
from caasm_tool.util import restore


class RecordType(object):
    CORE = "core"
    LINK = "link"


class BaseSDK(object):
    _DEFAULT_SORT_FIELDS = [("_id", 1)]
    _INDEXES = [
        ("idx_id_type", [("id", 1), ("type", 1)]),
        ("idx_type", [("type", 1)]),
    ]

    def __init__(self, persistence_handler):
        self._persistence_handler: BasePersistenceHandler = persistence_handler

    def update_factory_upstream(self, records, table):
        if not records:
            return
        self.delete_factory(records, table)
        self.save_factory(records, table)

    def delete_factory(self, records, table):
        if not records:
            return
        self._delete_link_record(records, table)
        self._delete_loop_by_id(records, table)

    def get_factory_count(self, table, condition=None):
        query_condition = self._build_core_query(condition)
        return self._persistence_handler.count(query_condition, table=table)

    def find_factory(
        self, condition, table, fields=None, sort_fields=None, offset=None, limit=None, relation_link=True
    ):
        query_condition = self._build_core_query(condition)
        cursor = self._persistence_handler.find_direct(
            query_condition,
            table=table,
            fields=fields,
            sort_fields=sort_fields,
            offset=offset,
            limit=limit,
        )
        records = list(cursor)
        if relation_link:
            record_ids = [record["id"] for record in records]
            link_record_mapper = self._find_link_record(record_ids, table=table)
            result = self._extract_biz_record(records)
            for biz_record in result:
                for key, values in link_record_mapper[biz_record["id"]].items():
                    restore(key, values, biz_record)
        else:
            result = self._extract_biz_record(records)
        return result

    @classmethod
    def _extract_biz_record(cls, records):
        result = []
        for record in records:
            biz_record = record["record"] if "record" in record else record
            biz_record["_id"] = record["_id"]
            if "id" in record:
                biz_record["id"] = record["id"]
            result.append(biz_record)
        return result

    def _find_link_record(self, record_ids, table, size=100, fields=None):
        if not record_ids:
            return []
        query = {"id": {"$in": record_ids}, "type": RecordType.LINK}

        result = defaultdict(lambda: defaultdict(list))
        link_records = self._find_loop(query, table=table, fields=fields, size=size)
        for link_record in link_records:
            key = link_record["key"]
            record_id = link_record["id"]
            record = link_record["record"]
            result[record_id][key].append(record)
        return result

    def _delete_link_record(self, records, table, size=100):
        condition = {"_id": {"$in": [record["_id"] for record in records]}}
        fields = ["id"]
        core_records = self.find_factory(condition, table=table, fields=fields, relation_link=False)

        if not core_records:
            return
        record_ids = [i["id"] for i in core_records]
        condition = {"id": {"$in": record_ids}, "type": RecordType.LINK}
        link_records = self._find_loop(condition, table, size=size, fields=["_id"])

        self._delete_loop_by_id(link_records, table)

    def _delete_loop_by_id(self, records, table, size=1000):
        for index in range(0, len(records), size):
            ids = [i["_id"] for i in records[index : index + size]]
            self._persistence_handler.delete_multi({"_id": {"$in": ids}}, table=table)

    def save_factory(self, data, table, size=100):
        buffer = []

        for info in data:
            info.pop("_id", None)
            self._merge_link(info, buffer)
        self.save_core(table, buffer, size)

    def create_factory_index(self, table):
        for index_name, index in self._INDEXES:
            if self._persistence_handler.index_is_exists(index_name, table):
                continue
            self._persistence_handler.create_index_direct(index_name, index, table=table)

    def save_core(self, table, buffer, size):
        length = len(buffer)
        for index in range(0, length, size):
            self._persistence_handler.save_multi_direct(records=buffer[index : index + size], table=table)

    @classmethod
    def _merge_link(cls, info, buffer, storage=None, title=None, record_id=None):
        push_flag = False
        if storage is None:
            push_flag = True
            storage = {}
        if record_id is None:
            record_id = nanoid.generate()

        for key, val in info.items():
            if isinstance(val, dict):
                subject = f"{title}.{key}" if title else key
                next_storage = storage.setdefault(key, {})
                cls._merge_link(val, buffer, next_storage, title=subject, record_id=record_id)
            elif isinstance(val, list) and val and isinstance(val[0], dict):
                subject = f"{title}.{key}" if title else key
                for sub_val in val:
                    buffer.append(cls.build_link(record_id, subject, sub_val))
            else:
                storage[key] = val
        if push_flag:
            buffer.append(cls._build_core(record_id, storage))

    @classmethod
    def _build_core_query(cls, condition):
        query = {"type": RecordType.CORE}
        if condition is None:
            return query

        if "_id" in condition:
            query["_id"] = condition.get("_id")
        filter_keys = ("id", "_id")
        for key, val in condition.items():
            if key in filter_keys:
                query[key] = val
            else:
                query[f"record.{key}"] = val

        return query

    @classmethod
    def build_link(cls, record_id, record_key, record):
        return cls._build_basic(record_id, RecordType.LINK, record, record_key)

    @classmethod
    def _build_core(cls, record_id, record):
        return cls._build_basic(record_id, RecordType.CORE, record)

    @classmethod
    def _build_basic(cls, record_id, record_type, record, record_key=None):
        result = {"type": record_type, "record": record, "id": record_id}
        if record_key:
            result["key"] = record_key
        return result

    def _find_loop(self, condition, table, fields=None, size=100):
        result = []
        min_id = None
        while True:
            if min_id:
                condition["_id"] = {"$gt": min_id}
            cursor = self._persistence_handler.find_direct(
                condition=condition,
                limit=size,
                sort_fields=self._DEFAULT_SORT_FIELDS,
                table=table,
                fields=fields,
            )
            tmp_result = list(cursor)
            if not tmp_result:
                break
            result.extend(tmp_result)
            min_id = tmp_result[-1]["_id"]
        return result
