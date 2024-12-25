import logging
import time
import traceback
from functools import wraps
from typing import List, Dict

from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers.errors import BulkIndexError

from caasm_config.config import caasm_config
from caasm_persistence.handler.storage.base import BaseHandler
from caasm_persistence.handler.storage.file_ import MongoFileHandler
from caasm_persistence.handler.storage.model.constant import StorageType
from caasm_persistence_base.handler.storage.model.response import (
    CommonResponse,
    DeleteResponse,
    UpdateResponse,
    SaveMultiResponse,
    SaveResponse,
)
from caasm_tool import log as logger
from caasm_tool.util import extract, restore

log = logging.getLogger()


def ignore_exc(success_handle, error_handle):
    def inner(func):
        @wraps(func)
        def _inner(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return success_handle(result)
            except BulkIndexError as e:
                for error in e.errors:
                    index_error = error.get("index", {})
                    logger.warning(
                        f"{func.__name__} has error. error type:[{index_error.get('error',{}).get('type', None)}],reason:[{index_error.get('error', {}).get('reason', None)}]"
                    )
                    return error_handle(e)
            except Exception as e:
                logger.warning(f"{func.__name__} handle error. detail is {traceback.format_exc()}")
                return error_handle(e)

        return _inner

    return inner


def save_error(exc):
    log.warning(exc)
    return BaseHandler.build_save_response(flag=False, msg="save failed", inserted_id=None)


def save_success(result):
    body = result.body
    insert_id = body.get("_id")
    return BaseHandler.build_save_response(True, None, inserted_id=insert_id)


def save_multi_success(result):
    return BaseHandler.build_save_multi_response(True, result, inserted_ids=None)


def save_multi_error(exc):
    log.warning(exc)
    return BaseHandler.build_save_multi_response(False, f"save multi error:{str(exc)}", inserted_ids=None)


def update_error(exc):
    log.warning(exc)
    return BaseHandler.build_update_response(False, "update error", None)


def update_success(result):
    if isinstance(result, tuple):
        modified_count = result[0]
    else:
        modified_count = result.get("updated")
    return BaseHandler.build_update_response(True, modified_count=modified_count)


def delete_error(exc):
    log.warning(exc)
    return BaseHandler.build_delete_response(
        False,
        msg="delete error",
    )


def delete_success(result):
    return BaseHandler.build_delete_response(True, deleted_count=result.get("deleted"))


def common_success(result):
    return BaseHandler.build_common_response(True)


def common_error(exc):
    log.warning(exc)
    return BaseHandler.build_common_response(False, "handle error")


class ESHandler(MongoFileHandler, BaseHandler):
    def __init__(self, es_client=None, mongo_file_client=None, **kwargs):
        MongoFileHandler.__init__(self, client=mongo_file_client, **kwargs)
        BaseHandler.__init__(self, client=es_client)
        self._request_timeout = caasm_config.db_info("elasticsearch", "request_timeout")

    @ignore_exc(success_handle=save_success, error_handle=save_error)
    def save_direct(self, data: Dict, table=None, refresh=False, **kwargs) -> SaveResponse:
        result = self.options().index(index=self.table(table), body=data, refresh=refresh, **kwargs)
        return result

    @ignore_exc(success_handle=save_multi_success, error_handle=save_multi_error)
    def save_multi_direct(self, records: List[Dict], table=None, refresh=False, **kwargs) -> SaveMultiResponse:
        table = self.table(table)
        action = [{"_index": table, "_source": record} for record in records]
        return helpers.bulk(
            self.options(),
            action,
            refresh=refresh,
            request_timeout=self._request_timeout,
        )

    @ignore_exc(success_handle=update_success, error_handle=update_error)
    def update_direct(self, condition, values, table=None, **kwargs) -> UpdateResponse:
        return self._update_core(condition, values, table, max_docs=1, **kwargs)

    def update_multi_direct(self, condition, values, table=None, **kwargs):
        return self._update_core(condition, values, table, **kwargs)

    def _update_core(self, condition, values, table=None, max_docs=None, **kwargs):
        inlines = []
        new_values = {}
        for key in values:
            import random

            while True:
                new_key = "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_", k=8))
                if new_key not in new_values:
                    break
            inlines.append(f"ctx._source.{key}=params.{new_key}")
            new_values[new_key] = values[key]

        inline = ";".join(inlines)

        body = {
            "query": condition,
            "script": {"source": inline, "params": new_values, "lang": "painless"},
        }
        return self.options().update_by_query(index=table, body=body, max_docs=max_docs)

    @ignore_exc(success_handle=update_success, error_handle=update_error)
    def update_stream_direct(self, mappers: List[Dict], table=None, **kwargs) -> UpdateResponse:
        table = self.table(table)

        actions = []
        for record in mappers:
            record_id = record.pop("_id")
            actions.append(
                {
                    "_id": record_id,
                    "_index": table,
                    "_source": {"doc": record},
                    "_op_type": "update",
                }
            )
        return helpers.bulk(self.options(), actions, request_timeout=self._request_timeout)

    def get_direct(self, condition, fields=None, table=None):
        table = self.table(table)
        response = self.options().search(query=condition, source_includes=fields, index=table, size=1)
        result = self._parse_response(response)
        if not result:
            return {}
        return result[0]

    @ignore_exc(success_handle=delete_success, error_handle=delete_error)
    def delete_multi(self, condition, table=None):
        return self.options().delete_by_query(index=self.table(table), query=condition)

    @ignore_exc(success_handle=delete_success, error_handle=delete_error)
    def delete_one(self, condition, table=None) -> DeleteResponse:
        return self.options().delete_by_query(index=self.table(table), query=condition, max_docs=1)

    def count(self, condition=None, table=None):
        index = self.table(table)
        result = self.options().count(index=index, query=condition, ignore=[404])
        return result.body.get("count", 0)

    def find_direct(
        self,
        condition=None,
        fields=None,
        sort_fields=None,
        offset=None,
        limit=None,
        table=None,
        need_ori_response=False,
        search_after=None,
        **kwargs,
    ):
        sort_info = self._parse_sort_fields(sort_fields)
        response = self.search(
            table=table,
            source_includes=fields,
            size=limit,
            from_=offset,
            query=condition,
            sort=sort_info,
            search_after=search_after,
            **kwargs,
        )
        return self._parse_response(response, need_ori_response=need_ori_response)

    def find_distinct(self, field, condition=None, table=None, **kwargs):
        inner_hits = kwargs.get("inner_hits", None)
        source_includes = kwargs.get("fields", [field])
        limit = kwargs.get("limit", None)
        offset = kwargs.get("offset", None)
        sort_fields = kwargs.get("sort_fields", None)
        if sort_fields:
            sort_fields = self._parse_sort_fields(sort_fields)

        collapse = {"field": field}

        if inner_hits:
            collapse["inner_hits"] = inner_hits
        table = self.table(table)

        count = self.count(condition, table=table)
        limit = limit or count

        response = self.search(
            query=condition,
            table=table,
            collapse=collapse,
            source_includes=source_includes,
            from_=offset,
            size=limit,
            sort=sort_fields,
        )
        result = self._parse_response(response)
        return [extract(record, field) for record in result]

    def search(self, table=None, **kwargs):
        return self.options().search(index=self.table(table), **kwargs, timeout=self._request_timeout)

    def refresh(self, table=None):
        table = self.table(table)
        if not self.exists(table):
            return
        return self.options().indices.refresh(index=table)

    def optimize(self, table, wait_for_completion=False, only_expunge_deletes=True):
        return self.options().indices.forcemerge(
            index=table,
            only_expunge_deletes=only_expunge_deletes,
            wait_for_completion=wait_for_completion,
        )

    @ignore_exc(success_handle=common_success, error_handle=common_error)
    def drop(self, table_name=None) -> CommonResponse:
        result = self.options().indices.delete(index=self.table(table_name))
        return result

    @ignore_exc(success_handle=common_success, error_handle=common_error)
    def rename(
        self,
        ori_table_name,
        new_table_name,
        wait_for_completion=True,
        refresh_time=caasm_config.ES_REINDEX_ASYNC_QUERY_WAIT,
        **kwargs,
    ) -> CommonResponse:
        drop_ori_table = kwargs.pop("drop_ori_table", True)

        res = self.options().reindex(
            source={"index": ori_table_name, "size": caasm_config.ES_REINDEX_SIZE},
            dest={"index": new_table_name},
            wait_for_completion=False,
            **kwargs,
        )
        log.debug("rename res is {}".format(res))

        if wait_for_completion:
            while True:
                task_result = self.get_task_result(task_id=res["task"])
                if task_result.get("completed"):
                    break
                time.sleep(refresh_time)
            if drop_ori_table:
                self.drop(ori_table_name)

    def get_task_result(self, task_id):
        result = self.options().tasks.get(task_id=task_id)
        return result

    def exists(self, ori_table_name):
        result = self.options().indices.exists(index=ori_table_name)
        return result

    def delete_template(self, template_name):
        return self.options().indices.delete_template(name=template_name)

    def put_template(self, template_name, **kwargs):
        return self.options().indices.put_template(name=template_name, **kwargs)

    def get_template(self, template_name, **kwargs):
        return self.options().indices.get_template(name=template_name)

    def get_size(self, table=None):
        table = self.table(table)

        result = self.options().cat.indices(index=table, bytes="b", format="json")
        if "error" in result:
            return 0
        return int(result[0]["store.size"])

    @property
    def storage_type(self) -> StorageType:
        return StorageType.ES

    @property
    def client(self) -> Elasticsearch:
        return super(ESHandler, self).client

    def options(self):
        return self.client.options(ignore_status=[404, 400], request_timeout=self._request_timeout)

    @classmethod
    def _build_script(cls, record: Dict):
        inlines = []
        for key in record:
            inlines.append(f"ctx._source.{key}=params.{key}")

        inline = ",".join(inlines)
        return {"_source": inline, "params": record, "lang": "painless"}

    @classmethod
    def _parse_sort_fields(cls, sort_fields):
        return sort_fields

    @classmethod
    def _parse_response(cls, response, need_ori_response=False, high_lights=None):
        result = []
        hits = response.body.get("hits", {}).get("hits", [])
        for hit in hits:
            if need_ori_response:
                result.append(hit)
            else:
                _source = hit["_source"]
                _id = hit["_id"]
                _source["_id"] = _id
                #   解析高亮
                highlight = extract(hit, "highlight") or {}
                real_highlights = []
                for field, field_highlights in highlight.items():
                    for field_highlight in field_highlights:
                        splits = field_highlight.split("!@##@!")
                        for split in splits:
                            if "<em>" in split:
                                real_highlights.append(split.replace("<em>", "").replace("</em>", ""))
                if real_highlights:
                    restore(
                        "base.query_content",
                        "!@##@!".join(set(real_highlights)),
                        _source,
                    )
                result.append(_source)
        return result
