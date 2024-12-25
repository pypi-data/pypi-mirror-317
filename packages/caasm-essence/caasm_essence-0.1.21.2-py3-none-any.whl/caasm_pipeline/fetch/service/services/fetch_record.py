import datetime

from caasm_adapter_base.fetcher.fetch_service_base import BaseFetchService
from caasm_service_base.constants.adapter import AdapterFetchStatus

from caasm_persistence.handler.storage.mongo import MongoHandler
from caasm_pipeline.fetch.service.schemas.runtime import fetch_record_schema


class FetchService(MongoHandler, BaseFetchService):
    DEFAULT_TABLE = "fetch.record"
    DEFAULT_SCHEMA = fetch_record_schema

    def find_fetch_record(
        self,
        adapter_name=None,
        adapter_names=None,
        latest=None,
        fetch_type=None,
        adapter_instance_id=None,
        status=None,
        start_time_gte=None,
        start_time_lte=None,
        finished=None,
        data_deleted=None,
        adapter_instance_ids=None,
        fetch_record_id=None,
        fields=None,
        sort_fields=None,
        offset=None,
        limit=None,
    ):
        query = self.build_fetch_record_condition(
            fetch_record_id=fetch_record_id,
            adapter_name=adapter_name,
            latest=latest,
            fetch_type=fetch_type,
            status=status,
            adapter_names=adapter_names,
            start_time_lte=start_time_lte,
            start_time_gte=start_time_gte,
            adapter_instance_ids=adapter_instance_ids,
            data_deleted=data_deleted,
            adapter_instance_id=adapter_instance_id,
            finished=finished,
        )
        return self.find(
            condition=query,
            fields=fields,
            sort_fields=sort_fields,
            offset=offset,
            limit=limit,
        )

    def modify_fetch_record(self, condition_finished=None, value_status=None, value_finish_time=None):
        query = self.build_fetch_record_condition(finished=condition_finished)
        values = {}
        if value_status:
            values["status"] = value_status
        if value_finish_time:
            values["finish_time"] = value_finish_time

        return self.update_multi_direct(query, values) if values else None

    def get_fetch_record_count(
        self,
        adapter_instance_ids=None,
        adapter_names=None,
        fetch_record_id=None,
        status=None,
        start_time_lte=None,
        start_time_gte=None,
    ):
        condition = self.build_fetch_record_condition(
            fetch_record_id=fetch_record_id,
            adapter_instance_ids=adapter_instance_ids,
            adapter_names=adapter_names,
            status=status,
            start_time_lte=start_time_lte,
            start_time_gte=start_time_gte,
        )
        return self.count(condition=condition)

    def get_fetch_record(self, fetch_record_id=None, fields=None):
        condition = self.build_fetch_record_condition(fetch_record_id=fetch_record_id)
        return self.get(condition=condition, fields=fields)

    def get_fetch_data_count(self, adapter_name, adapter_instance_id, fetch_type, index):
        table = self.build_fetch_data_table(
            adapter_name=adapter_name, adapter_instance_id=adapter_instance_id, fetch_type=fetch_type, index=index
        )
        return self.count(table=table)

    def finish_fetch(self, fetch_record_id, status, count, err_info=None):
        fetch_record = self.get_fetch_record(fetch_record_id, fields=["adapter_instance_id", "fetch_type"])
        if not fetch_record:
            raise ValueError(f"Not found fetch record({fetch_record_id})")

        if status == AdapterFetchStatus.SUCCESS:
            update_latest_condition = {
                "adapter_instance_id": fetch_record.adapter_instance_id,
                "latest": True,
                "fetch_type": fetch_record.fetch_type,
                "status": status,
                "finished": True,
            }
            update_latest_values = {"latest": False}
            self.update_multi_direct(update_latest_condition, update_latest_values)

        condition = self.build_fetch_record_condition(fetch_record_id=fetch_record_id)
        values = {
            "status": status,
            "finish_time": datetime.datetime.now(),
            "finished": True,
            "fetch_count": count,
            "err_info": err_info,
        }
        if status == AdapterFetchStatus.SUCCESS:
            values["latest"] = True
        return self.update_direct(condition=condition, values=values)

    def start_fetch(self, adapter_name, adapter_instance_id, index, fetch_type, start_time):
        values = {
            "adapter_name": adapter_name,
            "adapter_instance_id": adapter_instance_id,
            "index": index,
            "status": AdapterFetchStatus.FETCHING,
            "latest": False,
            "fetch_type": fetch_type,
            "data_deleted": False,
            "start_time": start_time,
        }
        fetch_record = self.load_entity(**values)
        return self.save(fetch_record).inserted_id

    def find_fetch_data(
        self,
        adapter_name=None,
        adapter_instance_id=None,
        fetch_type=None,
        index=None,
        data_type=None,
        condition=None,
        offset=None,
        limit=None,
        sort_fields=None,
        fields=None,
        table=None,
    ):
        if not table:
            table = self.build_fetch_data_table(adapter_name, adapter_instance_id, fetch_type, index)
        condition = condition or {}
        condition.update(self.build_fetch_data_condition(fetch_type=data_type))
        return self.find_direct(
            condition=condition, table=table, offset=offset, limit=limit, sort_fields=sort_fields, fields=fields
        )

    def save_fetch_data_multi(self, adapter_name, adapter_instance_id, fetch_type, index, data):
        table = self.build_fetch_data_table(adapter_name, adapter_instance_id, fetch_type, index)
        return self.save_stream(data, table=table)

    def modify_fetch_data_multi(self, adapter_name, adapter_instance_id, fetch_type, index, data):
        table = self.build_fetch_data_table(adapter_name, adapter_instance_id, fetch_type, index)
        return self.update_stream_direct(data, table=table, need_record_update_time=False)

    def delete_fetch_data(self, table, data_ids):
        condition = self.build_fetch_data_condition(data_ids=data_ids)
        return self.delete_multi(condition=condition, table=table)

    def delete_fetch_data_by_fetch_type(self, table, fetch_type):
        condition = self.build_fetch_data_condition(fetch_type=fetch_type)
        return self.delete_multi(condition=condition, table=table)

    def mark_fetch_record_data_deleted(self, adapter_name, adapter_instance_id, fetch_type, index):
        condition = self.build_fetch_record_condition(
            adapter_name=adapter_name, adapter_instance_id=adapter_instance_id, index=index, fetch_type=fetch_type
        )
        return self.update_direct(condition, {"data_deleted": True})

    def expand_asset_fetch_other_data(
        self,
        adapter_name,
        adapter_instance_id,
        index,
        fetch_type,
        asset_field,
        asset_value,
        asset_other_field,
        other_data,
    ):
        collection_name = self.build_fetch_data_table(
            adapter_name=adapter_name, adapter_instance_id=adapter_instance_id, fetch_type=fetch_type, index=index
        )
        condition = {asset_field: asset_value}
        values = {"$push": {asset_other_field: {"$each": other_data}}}

        return self.update_multi_direct(condition, values, simple_values=False, table=collection_name)

    @classmethod
    def build_fetch_data_table(cls, adapter_name, adapter_instance_id, fetch_type, index):
        return f"fetch_{fetch_type}_{adapter_name}_{adapter_instance_id}_{index}"

    @classmethod
    def extract_adapter_name(cls, table_name):
        return "_".join(table_name.split("_")[2:-2])

    @classmethod
    def extract_adapter_instance_id(cls, table_name):
        return table_name.split("_")[-2]

    @classmethod
    def extract_index(cls, table_name):
        return int(table_name.split("_")[-1])

    @classmethod
    def build_fetch_data_condition(cls, fetch_type=None, data_ids=None):
        condition = {}
        if fetch_type:
            condition["internal.fetch_type"] = fetch_type

        if data_ids:
            condition["_id"] = {"$in": cls._build_ids(data_ids)}

        return condition

    @classmethod
    def build_fetch_record_condition(
        cls,
        latest=None,
        adapter_name=None,
        fetch_type=None,
        status=None,
        fetch_record_id=None,
        adapter_names=None,
        adapter_instance_id=None,
        index=None,
        adapter_instance_ids=None,
        start_time_lte=None,
        start_time_gte=None,
        data_deleted=None,
        finished=None,
    ):
        condition = {}
        tmp_adapter_instance_ids = []
        if adapter_instance_id:
            tmp_adapter_instance_ids.append(adapter_instance_id)
        if adapter_instance_ids:
            tmp_adapter_instance_ids.extend(adapter_instance_ids)

        if index is not None:
            condition["index"] = index

        if latest is not None:
            condition["latest"] = latest
        if adapter_names:
            condition["adapter_name"] = {"$in": adapter_names}
        if adapter_name:
            condition["adapter_name"] = adapter_name
        if fetch_type:
            condition["fetch_type"] = fetch_type
        if status:
            condition["status"] = status
        if fetch_record_id:
            condition["_id"] = cls._build_id(fetch_record_id)
        if tmp_adapter_instance_ids:
            condition["adapter_instance_id"] = {"$in": cls._build_ids(tmp_adapter_instance_ids)}

        if data_deleted is not None:
            condition["data_deleted"] = data_deleted

        if start_time_lte or start_time_gte:
            time_condition = {}
            if start_time_gte:
                time_condition["$gte"] = start_time_gte
            if start_time_lte:
                time_condition["$lte"] = start_time_lte

            condition["start_time"] = time_condition

        if finished is not None:
            condition["finished"] = finished

        return condition
