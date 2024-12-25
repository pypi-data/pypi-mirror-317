import abc
import logging
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from bson import ObjectId

from caasm_entity.service.runtime import entity_service
from caasm_meta_model.manager import MetaDataManager
from caasm_persistence.handler.runtime import mongo_handler
from caasm_post.handlers.base import EnforcementBaseHandler

log = logging.getLogger()


class EnforcementTmpBaseHandler(EnforcementBaseHandler, metaclass=abc.ABCMeta):
    _EMPTY_VALUES = ((), [], {}, None)

    DEFAULT_MAX_ID = "FFFFFFFFFFFFFFFFFFFFFFFF"

    def __init__(self, *args, **kwargs):
        super(EnforcementTmpBaseHandler, self).__init__(*args, **kwargs)
        self._adapter_table = None
        self._table_storage = {}
        self._buffer = []
        self.meta_data_manager = MetaDataManager()
        self.meta_data_manager.initialize()
        self.default_timeout = 60
        self.cpu_num = os.cpu_count() * 5

    def execute(self):
        offset = 0

        ## 在进行对应的后处理的时候，需要判断是否设置了关联属性，如果设置了，需要对关联属性
        if not self.judge_relation_index_exist():
            return
        mxd = ObjectId(self.DEFAULT_MAX_ID)
        future_pool = ThreadPoolExecutor(max_workers=self.cpu_num)
        thread_semaphore = threading.Semaphore(self.cpu_num)
        lock = threading.Lock()
        futures = []
        while True:
            log.debug(f"{self.get_display_name()} mxd is {mxd}")
            ## 获取资产数据
            records = self.find_tmp_adapter_data(mxd=mxd, limit=self.size)
            if not records:
                break
            mxd = records[-1]["_id"]
            for record in records:
                with thread_semaphore:
                    futures.append(future_pool.submit(self.execute_func, record, lock))
            offset += self.size

        # 等待执行结果
        try:
            for future in as_completed(
                futures,
                timeout=self.default_timeout * self.cpu_num * 2,
            ):
                try:
                    future.result(timeout=self.default_timeout * self.cpu_num)
                except TimeoutError as e:
                    log.error(f"enrich departments TimeoutError:{str(e)}")
                    future_pool.shutdown(wait=True)
        except TimeoutError as e:
            log.error(f"enrich departments TimeoutError:{str(e)}")

        self.flush_buffer(force=True)
        self.execute_after()

    def execute_func(self, record: dict, lock: threading.Lock):
        record_data = record["adapter"]
        cleaned_flag, clean_data = self.clean_adapter_data(record_data)
        if not (cleaned_flag and clean_data):
            return
        clean_data = self.filter_empty_data(clean_data)
        size_data = self.recompute_size(clean_data)
        clean_data.update(size_data) if size_data else ...
        converted_data = self.convert_data(clean_data)
        converted_data["_id"] = record["_id"]
        lock.acquire()
        try:
            self._buffer.append(converted_data)
            self.flush_buffer()
        except Exception as e:
            log.error(f"Write into db, error: {e}")
        lock.release()

    def judge_relation_index_exist(self):
        if not self.relation_category:
            return True
        relation_index = entity_service.get_no_snapshot_table(category=self.relation_category, date=self.date)
        if not relation_index:
            return False
        if not entity_service.exists(relation_index):
            return False
        return True

    def find_tmp_adapter_data(self, mxd=None, limit=None):
        fields = [f"adapter.{i}" for i in self.fields]
        condition = {"_id": {"$lt": mxd}}
        cur = mongo_handler.find_direct(
            fields=fields, condition=condition, limit=limit, table=self.tmp_adapter_table, sort_fields=self.sort_fields
        )
        return list(cur)

    def clean_adapter_data(self, data):
        return self.return_failed()

    def execute_after(self):
        pass

    def flush_buffer(self, force=False):
        if not self._buffer:
            return

        if not force:
            return

        if not (len(self._buffer) >= self.buffer_size or force):
            return

        mongo_handler.update_stream_direct(self._buffer, table=self.tmp_adapter_table)
        self._buffer.clear()

    def find_tmp_table(self):
        if self._table_storage:
            return self._table_storage
        self._table_storage = self.meta_data_manager.find_storage_table(self.category)
        return self._table_storage

    @property
    def tmp_adapter_table(self):
        if self._adapter_table:
            return self._adapter_table

        adapter_table = self.find_tmp_table()
        return adapter_table["adapter"]

    @property
    def fields(self):
        return []

    @classmethod
    def recompute_size(cls, data):
        size_result = cls.compute_size(data)
        if not size_result:
            return

        _size_res = {}
        for key, value in size_result.items():
            cls.restore(f"_size.{key}", value, _size_res)
        return _size_res

    @classmethod
    def compute_size(cls, record):
        result = {}
        for field, value in record.items():
            if not isinstance(value, (dict, list)):
                continue

            if isinstance(value, list):
                result[field + "__size"] = len(value)
                element_result = []

                if value and isinstance(value[0], dict):
                    for element_value in value:
                        element_size_result = cls.compute_size(element_value)
                        if not element_size_result:
                            continue
                        element_result.append(element_size_result)
                if element_result:
                    result[field] = element_result
            else:
                son_result = cls.compute_size(value)
                if son_result:
                    result[field] = son_result
        return result

    @classmethod
    def return_success(cls, data):
        return True, data

    @classmethod
    def return_failed(cls):
        return False, None

    @classmethod
    def filter_empty_data(cls, data):
        need_pop_keys = []
        for key, val in data.items():
            if not val and val in cls._EMPTY_VALUES:
                need_pop_keys.append(key)

        for need_pop_key in need_pop_keys:
            data.pop(need_pop_key)
        return data

    @classmethod
    def convert_data(cls, data, result=None, title=""):
        if result is None:
            result = {}

        for key, val in data.items():
            if not title:
                tmp_title = f"adapter.{key}"
            else:
                tmp_title = title + "." + key

            if isinstance(val, dict):
                cls.convert_data(val, result, title=tmp_title)
            else:
                result[tmp_title] = val

        return result

    @property
    def sort_fields(self):
        return [("_id", -1)]
