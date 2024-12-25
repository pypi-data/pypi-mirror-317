import datetime

from caasm_persistence.handler.storage.mongo import MongoHandler

from caasm_pipeline.convert.service.constants.convert_record import AdapterConvertStatus
from caasm_pipeline.convert.service.schemas.runtime import convert_record_schema


class ConvertService(MongoHandler):
    DEFAULT_SCHEMA = convert_record_schema
    DEFAULT_TABLE = "convert.record"

    def find_convert_record(
        self,
        latest=None,
        fetch_type=None,
        adapter_names=None,
        adapter_name=None,
        convert_status=None,
        start_time_lte=None,
        start_time_gte=None,
        data_deleted=None,
        fields=None,
        sort_fields=None,
        offset=None,
        limit=None,
    ):
        condition = self.build_convert_record_condition(
            latest=latest,
            fetch_type=fetch_type,
            adapter_name=adapter_name,
            adapter_names=adapter_names,
            convert_status=convert_status,
            start_time_lte=start_time_lte,
            start_time_gte=start_time_gte,
            data_deleted=data_deleted,
        )
        return self.find(condition=condition, fields=fields, sort_fields=sort_fields, limit=limit, offset=offset)

    def start_convert(self, adapter_name, adapter_index, fetch_type):
        values = {
            "adapter_name": adapter_name,
            "index": adapter_index,
            "status": AdapterConvertStatus.CONVERTING,
            "fetch_type": fetch_type,
            "latest": False,
            "data_deleted": False,
            "start_time": datetime.datetime.now(),
        }
        convert_record = self.load_entity(**values)
        return self.save(convert_record).inserted_id

    def finish_convert(self, convert_record_id, status):
        if status == AdapterConvertStatus.SUCCESS:
            convert_record = self.get_by_id(convert_record_id)
            _query = {
                "adapter_name": convert_record.adapter_name,
                "latest": True,
                "fetch_type": convert_record.fetch_type,
            }
            _value = {"latest": False}
            self.update_multi_direct(_query, _value)

        _query = {"_id": self._build_id(convert_record_id)}
        _value = {"status": status, "finish_time": self.now}
        if status == AdapterConvertStatus.SUCCESS:
            _value["latest"] = True

        return self.update_direct(_query, _value)

    def save_convert_data(self, adapter_name, index, fetch_type, data):
        table = self.build_convert_data_table(fetch_type, adapter_name, index)
        return self.save_multi_direct(records=data, table=table)

    def find_convert_data(self, table_name, condition=None, fields=None, offset=None, limit=None):
        return self.find_direct(condition=condition, table=table_name, offset=offset, limit=limit, fields=fields)

    def mark_convert_record_data_deleted(self, adapter_name, fetch_type, index):
        condition = self.build_convert_record_condition(adapter_name=adapter_name, index=index, fetch_type=fetch_type)
        return self.update_direct(condition, {"data_deleted": True})

    @classmethod
    def extract_adapter_name(cls, table_name):
        return "_".join(table_name.split("_")[2:-1])

    @classmethod
    def extract_index(cls, table_name):
        return int(table_name.split("_")[-1])

    @classmethod
    def build_convert_data_table(cls, fetch_type, adapter_name, index):
        return f"convert_{fetch_type}_{adapter_name}_{index}"

    @classmethod
    def build_convert_record_condition(
        cls,
        latest=None,
        fetch_type=None,
        adapter_names=None,
        convert_status=None,
        start_time_lte=None,
        start_time_gte=None,
        adapter_name=None,
        index=None,
        data_deleted=None,
    ):
        condition = {}
        tmp_adapter_names = []

        if adapter_name:
            tmp_adapter_names.append(adapter_name)

        if adapter_names:
            tmp_adapter_names.extend(adapter_names)

        if latest is not None:
            condition["latest"] = latest

        if fetch_type:
            condition["fetch_type"] = fetch_type

        if tmp_adapter_names:
            condition["adapter_name"] = {"$in": tmp_adapter_names}

        if convert_status:
            condition["status"] = convert_status

        if start_time_lte or start_time_gte:
            time_condition = {}
            if start_time_gte:
                time_condition["$gte"] = start_time_gte
            if start_time_lte:
                time_condition["$lte"] = start_time_lte

            condition["start_time"] = time_condition

        if index is not None:
            condition["index"] = index

        if data_deleted is not None:
            condition["data_deleted"] = data_deleted

        return condition
