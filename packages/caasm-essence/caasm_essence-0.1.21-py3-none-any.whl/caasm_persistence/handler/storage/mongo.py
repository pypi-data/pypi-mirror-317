import datetime
import logging
import traceback
from typing import List, Dict

import bson
import pymongo
from bson import ObjectId
from pymongo import UpdateOne, InsertOne
from pymongo.errors import OperationFailure
from pymongo.collection import Collection

from caasm_config.config import caasm_config
from caasm_persistence_base.entity.base import IndexMeta
from caasm_persistence.handler.storage.base import BaseHandler
from caasm_persistence.handler.storage.file_ import MongoFileHandler
from caasm_persistence.handler.storage.model.constant import StorageType
from caasm_persistence_base.handler.storage.model.response import (
    SaveResponse,
    SaveMultiResponse,
    UpdateResponse,
    CommonResponse,
    DeleteResponse,
)
from caasm_tool.constants import DATETIME_FORMAT

log = logging.getLogger()


class MongoHandler(MongoFileHandler, BaseHandler):
    DEFAULT_DATABASE = ""
    MAX_NUM = 16 * 1024 * 1024

    def __init__(self, client=None, database=None):
        MongoFileHandler.__init__(self, client=client, database=database)
        BaseHandler.__init__(self, client)

    def __call__(self, client):
        self._client = client

    def convert_data_to_json(self, data, many=False):
        return self.DEFAULT_SCHEMA.to_dicts(data=data, many=many)

    @property
    def storage_type(self) -> StorageType:
        return StorageType.MONGO

    def table(self, table=None) -> Collection:
        if not table:
            table = self.DEFAULT_TABLE
        table = super(MongoHandler, self).table(table)
        return self.database()[table]

    def aggregate(self, pipeline, table=None):
        return self.table(table).aggregate(pipeline)

    def find_distinct(self, field, condition=None, table=None, **kwargs):
        cursor = self.find_direct(condition=condition, table=table)
        return cursor.distinct(field)

    def find_and_modify(
        self,
        condition,
        values,
        simple_values=True,
        upsert=False,
        return_new_flag=True,
        schema=None,
        table=None,
    ):
        update_value = self._build_update_value(values, simple_values)
        collection = self.table(table)
        data = collection.find_one_and_update(condition, update_value, upsert=upsert, return_document=return_new_flag)
        return self.schema(schema).load(data)

    @property
    def client(self):
        return self._client

    def database(self):
        db = self.DEFAULT_DATABASE
        if not db:
            db = caasm_config.mongo_default_database
        return self.client[db]

    @classmethod
    def build_client(cls):
        client = pymongo.MongoClient(**caasm_config.mongo_conn)
        return client

    def save_direct(self, data: Dict, table=None, **kwargs) -> SaveResponse:
        try:
            collection = self.table(table)
            self._build_date_time(data)
            result = collection.insert_one(data)
        except Exception as e:
            log.debug(traceback.format_exc())
            log.warning(f"save error {e}")
            return self.build_save_response(False, f"save failed {e}")
        else:
            if result.inserted_id:
                return self.build_save_response(True, inserted_id=result.inserted_id)
            return self.build_save_response(False, "not found inserted_id")

    def save_multi_direct(self, records: List[Dict], table=None, **kwargs) -> SaveMultiResponse:
        try:
            collection = self.table(table)
            self._build_data_multi_time(records)
            result = collection.insert(records)
        except Exception as e:
            log.debug(traceback.format_exc())
            log.warning(f"save error {e}")
            return self.build_save_multi_response(False, f"save multi failed {e}")
        else:
            if result:
                return self.build_save_multi_response(True, inserted_ids=result)
            return self.build_save_multi_response(False, "not found inserted_ids")

    def save_stream(self, records, table=None, filter_large_data=False, **kwargs):

        if not records:
            return
        new_records = []
        for record in records:
            if filter_large_data and len(bson.BSON.encode(record)) > self.MAX_NUM:
                continue
            try:
                new_record = InsertOne(record)
            except Exception as e:
                log.error(f"build insert stream error({e})")
            else:
                new_records.append(new_record)

        if not new_records:
            return self.build_save_multi_response(False)
        try:
            result = self.table(table).bulk_write(new_records, **kwargs)
        except Exception as e:
            log.error(f"Save stream error({e}) detail is {traceback.format_exc()}")
            return self.build_save_multi_response(False, f"save multi failed {e}")
        else:
            return self.build_save_multi_response(True) if result else self.build_save_multi_response(False)

    def update_direct(
        self, condition, values, table=None, simple_values=True, upsert=False, **kwargs
    ) -> UpdateResponse:
        try:
            update_value = self._build_update_value(values, simple_values)
            result = self.table(table).update_one(condition, update_value, upsert=upsert)
        except Exception as e:
            log.debug(traceback.format_exc())
            log.warning(f"update error {e}")
            return self.build_update_response(False, f"update failed {e}")
        else:
            return self.build_update_response(True, "", modified_count=result.modified_count)

    def update_by_id(self, id, values, table=None, simple_values=True, **kwargs) -> UpdateResponse:
        condition = {"_id": self._build_id(id)}
        return self.update_direct(condition, values, table, simple_values, **kwargs)

    def update_multi_direct(self, condition, values, table=None, simple_values=True, upsert=False, **kwargs):
        need_record_update_time = kwargs.pop("need_record_update_time", True)
        try:
            update_value = self._build_update_value(values, simple_values, need_record_update_time)
            result = self.table(table).update_many(condition, update_value, upsert=upsert)
        except Exception as e:
            log.debug(traceback.format_exc())
            log.warning(f"update error {e}")
            return self.build_update_response(False, f"update failed {e}")
        else:
            return self.build_update_response(True, "", modified_count=result.modified_count)

    def update_stream_direct(self, mappers: List[Dict], table=None, simple_values=True, **kwargs) -> UpdateResponse:
        new_documents = self._filter_empty_value(mappers)
        need_record_update_time = kwargs.pop("need_record_update_time", True)
        if not new_documents:
            return self.build_update_response(True, modified_count=0)
        try:
            key_name = kwargs.pop("field_name", "_id")
            update_condition = kwargs.pop("update_condition", False)

            stream = [
                UpdateOne(
                    {key_name: document.get(key_name) if update_condition else document.pop(key_name)},
                    self._build_update_value(
                        document,
                        simple_values=simple_values,
                        need_record_update_time=need_record_update_time,
                    ),
                    upsert=kwargs.pop("upsert", False),
                )
                for document in new_documents
            ]
            result = self.table(table).bulk_write(stream, **kwargs)
        except Exception as e:
            log.debug(traceback.format_exc())
            log.warning(f"update stream direct failed ({e})")
            return self.build_update_response(False, e)
        else:
            return self.build_update_response(True, result.modified_count)

    def update_stream_direct_by_simple(self, mappers: List[Dict], table=None, simple_values=True, **kwargs):
        mappers = self._flat_data(mappers)
        return self.update_stream_direct(mappers, table, simple_values, **kwargs)

    def get_direct(self, condition=None, fields=None, table=None):
        return self.table(table).find_one(filter=condition, projection=self._build_query_field(fields))

    def get_by_id(self, id, fields=None, table=None):
        condition = {"_id": self._build_id(id)}
        return self.get(condition, fields=fields, table=table)

    def get_by_id_direct(self, id, fields=None, table=None):
        condition = {"_id": self._build_id(id)}
        return self.get_direct(condition, fields=fields, table=table)

    def delete_multi(self, condition, table=None, limit=None):
        try:
            result = self.table(table).delete_many(condition)
        except Exception as e:
            log.warning(f"delete multi error({e},{traceback.format_exc()})")
            return self.build_delete_response(False, e)
        else:
            return self.build_delete_response(True, deleted_count=result.deleted_count if result else 0)

    def delete_one(self, condition, table=None) -> DeleteResponse:
        try:
            result = self.table(table).delete_one(condition)
        except Exception as e:
            log.debug(traceback.format_exc())
            log.warning(f"delete one error({e})")
            return self.build_delete_response(False, e)
        else:
            n = result.deleted_count
            return self.build_delete_response(True, deleted_count=n)

    def count(self, condition=None, table=None):
        return self.table(table).count(condition)

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
        if not condition:
            condition = {}
        if kwargs:
            condition.update(kwargs)
        cursor = self.table(table).find(filter=condition, projection=self._build_query_field(fields))
        if sort_fields:
            cursor = cursor.sort(sort_fields)
        if offset is not None:
            cursor = cursor.skip(offset)
        if limit is not None:
            cursor = cursor.limit(limit)
        return cursor

    def drop(self, table_name=None) -> CommonResponse:
        try:
            self.table(table_name).drop()
        except Exception as e:
            log.debug(traceback.format_exc())
            log.warning(f"drop error {e}")
            return self.build_common_response(False, e)
        else:
            return self.build_common_response(True)

    def rename(self, ori_table_name, new_table_name, **kwargs) -> CommonResponse:
        try:
            result = self.table(ori_table_name).rename(new_table_name)
        except Exception as e:
            log.debug(traceback.format_exc())
            log.warning(f"rename error {e}")
            return self.build_common_response(False, e)
        else:
            ok = result.get("ok")
            if not ok:
                return self.build_common_response(False, "rename failed ok not equal 1.0")
            return self.build_common_response(True)

    def exists(self, table_name):
        try:
            self.database().validate_collection(table_name)  # Try to validate a collection
        except OperationFailure:  # If the collection doesn't exist
            return False
        return True

    def get_id(self):
        return ObjectId()

    # 特有的方法
    @classmethod
    def _build_update_value(cls, values, simple_values=True, need_record_update_time=True):
        update_time_value = (
            {"update_time": datetime.datetime.now().strftime(DATETIME_FORMAT)} if need_record_update_time else {}
        )
        if simple_values:
            values.update(update_time_value)
            update_value = {"$set": values}
        else:
            update_value = values
            if "$set" in update_value:
                update_value["$set"].update(update_time_value)
            else:
                update_value["$set"] = update_time_value
            update_value["$set"].pop("_id", None)

        return update_value

    @classmethod
    def _filter_empty_value(cls, values):
        result = []
        for value in values:
            tmp_result = {}
            for k, v in value.items():
                if v is None:
                    continue
                tmp_result[k] = v
            if not tmp_result:
                continue
            result.append(tmp_result)
        return result

    @classmethod
    def _build_query_field(cls, fields: List[str]):
        if not fields:
            return None
        return {field: 1 for field in fields}

    def create_index(self, index_name, indexes: List[IndexMeta], collection_name=None, **kwargs):
        mongo_indexes = [(index.field, index.sort) for index in indexes]
        return self.create_index_direct(index_name, mongo_indexes, collection_name, **kwargs)

    def index_is_exists(self, index_name, table=None):
        index_names = [index["name"] for index in self.table(table).list_indexes()]
        return index_name in index_names

    def create_index_direct(self, index_name, indices, table=None, **kwargs):
        collection = self.table(table)
        collection.create_index(indices, name=index_name, **kwargs)

    def update_data_by_id(self, data_id, table=None, **kwargs):
        if not kwargs:
            return
        condition = {"_id": self._build_id(data_id)}
        return self.update_direct(condition=condition, values=kwargs, table=table)

    def update_data_by_ids(self, data_ids, table=None, **kwargs):
        if not kwargs:
            return

        condition = {"_id": {"$in": self._build_ids(data_ids)}}
        return self.update_multi_direct(condition=condition, values=kwargs, table=table)

    def _build_date_time(self, data):
        if "create_time" not in data or not data["create_time"]:
            data["create_time"] = self.now
        if "update_time" not in data or not data["update_time"]:
            data["update_time"] = self.now

    def _build_data_multi_time(self, data):
        for info in data:
            self._build_date_time(info)

    def _flat_data(self, records):
        result = []

        for record in records:
            new_record = self.__flat(record)
            result.append(new_record)
        return result

    @classmethod
    def __flat(cls, record, result=None, title=None):
        if result is None:
            result = {}
        for key, val in record.items():
            _title = f"{title}.{key}" if title else key
            if isinstance(val, dict):
                cls.__flat(val, result, _title)
            else:
                result[_title] = val
        return result

    @classmethod
    def build_id_ids_condition(cls, data_id=None, data_ids=None):
        _id_condition = {}
        if data_ids:
            _id_condition["$in"] = cls._build_ids(data_ids)

        if data_id:
            _id_condition["$eq"] = cls._build_id(data_id)
        return _id_condition

    def build_insert_operate(self, data: dict) -> InsertOne:
        return InsertOne(data)

    def build_update_operate(self, condition: dict, values: dict) -> UpdateOne:
        return UpdateOne(condition, values)
