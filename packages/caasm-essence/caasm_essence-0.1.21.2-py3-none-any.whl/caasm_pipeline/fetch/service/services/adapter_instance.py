import re

from caasm_persistence.handler.storage.mongo import MongoHandler
from caasm_pipeline.fetch.service.schemas.runtime import adapter_instance_schema


class AdapterInstanceService(MongoHandler):
    DEFAULT_TABLE = "adapter_instance"
    DEFAULT_SCHEMA = adapter_instance_schema

    def get_adapter_instance_count(
        self,
        adapter_instance_id=None,
        name=None,
        run_status=None,
        keyword=None,
        ancestor_adapter_name=None,
        enabled=None,
        connect_status=None,
    ):
        condition = self.build_adapter_instance_condition(
            adapter_instance_id=adapter_instance_id,
            name=name,
            run_status=run_status,
            keyword=keyword,
            ancestor_adapter_name=ancestor_adapter_name,
            enabled=enabled,
            connect_status=connect_status,
        )
        return self.count(condition)

    def get_adapter_instance(self, adapter_instance_id=None, name=None, adapter_name=None, fields=None):
        condition = self.build_adapter_instance_condition(
            adapter_instance_id=adapter_instance_id, name=name, adapter_name=adapter_name
        )
        return self.get(condition=condition, fields=fields)

    def find_adapter_instance(
        self,
        adapter_name=None,
        adapter_instance_ids=None,
        enabled=None,
        trigger=None,
        trigger_ne=None,
        adapter_names=None,
        keyword=None,
        run_status=None,
        ancestor_adapter_name=None,
        connect_status=None,
        adapter_instance_id=None,
        fields=None,
        sort_fields=None,
        offset=None,
        limit=None,
        **kwargs,
    ):
        condition = self.build_adapter_instance_condition(
            adapter_instance_id=adapter_instance_id,
            run_status=run_status,
            adapter_name=adapter_name,
            adapter_instance_ids=adapter_instance_ids,
            enabled=enabled,
            trigger=trigger,
            adapter_names=adapter_names,
            keyword=keyword,
            ancestor_adapter_name=ancestor_adapter_name,
            connect_status=connect_status,
            trigger_ne=trigger_ne,
        )
        return self.find_list(
            condition=condition, fields=fields, offset=offset, limit=limit, sort_fields=sort_fields, **kwargs
        )

    def modify_adapter_instance_run_info(
        self, adapter_instance_id, run_status=None, last_sync_time=None, connect_status=None
    ):
        condition = self.build_adapter_instance_condition(adapter_instance_id=adapter_instance_id)
        values = {}

        if run_status:
            values["run_status"] = run_status

        if connect_status:
            values["connect_status"] = connect_status

        if last_sync_time:
            values["last_sync_time"] = last_sync_time

        if not values:
            return self.build_update_response(True, modified_count=0)

        return self.update_direct(condition=condition, values=values)

    def modify_adapter_instance(self, adapter_instance_id, values):
        condition = self.build_adapter_instance_condition(adapter_instance_id=adapter_instance_id)
        return self.update_direct(condition, values)

    def delete_adapter_instance(self, adapter_instance_ids=None):
        condition = self.build_adapter_instance_condition(adapter_instance_ids=adapter_instance_ids)
        if not condition:
            raise ValueError("delete condition empty")
        return self.delete_multi(condition)

    def find_adapter_instance_distinct(self, field):
        return self.find_distinct(field=field)

    @classmethod
    def build_adapter_instance_condition(
        cls,
        adapter_name=None,
        keyword=None,
        enabled=None,
        trigger=None,
        adapter_names=None,
        name=None,
        adapter_instance_id=None,
        run_status=None,
        ancestor_adapter_name=None,
        adapter_instance_ids=None,
        connect_status=None,
        trigger_ne=None,
    ):
        query_condition = {}
        _id_condition = {}
        _trigger_condition = {}

        if adapter_name:
            query_condition["adapter_name"] = adapter_name
        if adapter_instance_ids:
            _id_condition["$in"] = cls._build_ids(adapter_instance_ids)
        if adapter_instance_id:
            _id_condition["$eq"] = cls._build_id(adapter_instance_id)
        if enabled is not None:
            query_condition["enabled"] = enabled

        if trigger is not None:
            _trigger_condition["$eq"] = trigger
        if trigger_ne is not None:
            _trigger_condition["$ne"] = trigger_ne

        if _trigger_condition:
            query_condition["trigger.value"] = _trigger_condition

        if adapter_names:
            query_condition["adapter_name"] = {"$in": adapter_names}
        if name:
            query_condition["name"] = name
        if run_status:
            query_condition["run_status"] = run_status
        if ancestor_adapter_name:
            query_condition["ancestor_adapter_name"] = ancestor_adapter_name
        if connect_status:
            query_condition["connect_status"] = connect_status
        if keyword:
            keyword_re = re.compile(keyword)
            query_condition["$or"] = [
                {"name": {"$regex": keyword_re}},
                {"description": {"$regex": keyword_re}},
            ]
        if _id_condition:
            query_condition["_id"] = _id_condition

        return query_condition
