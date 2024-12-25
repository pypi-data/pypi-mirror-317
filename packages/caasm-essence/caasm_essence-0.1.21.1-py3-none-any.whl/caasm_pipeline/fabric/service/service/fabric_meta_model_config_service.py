from typing import Dict, List, Set

import pymongo
from bson import ObjectId
from caasm_persistence.handler.storage.mongo import MongoHandler
from caasm_persistence_base.handler.storage.model.response import UpdateResponse, DeleteResponse
from caasm_persistence_base.schema.base import ObjectIdField
from caasm_tool.util import get_now

from caasm_pipeline.fabric.service.schema.runtime import fabric_model_config_schema, fabric_config_schema


class FabricModelConfigService(MongoHandler):
    DEFAULT_SCHEMA = fabric_model_config_schema
    DEFAULT_TABLE = "fabric.meta_model_config"

    def save_fabric_model_config_service(
        self, asset_type_id, fabric_policy=None, adapter_confidence=None, field_global_policy=None
    ):
        mapper = {
            "asset_type_id": asset_type_id,
            "fabric_policy": fabric_policy,
            "adapter_confidence": adapter_confidence,
            "field_global_policy": field_global_policy,
        }
        return self.save_direct(mapper)

    def update_fabric_model_config_service(self, asset_type_id, fabric_policy=None):
        condition = self.build_fabric_meta_model_config_condition(asset_type_id=asset_type_id)
        values = {}
        values.update({"fabric_policy": fabric_policy}) if fabric_policy else ...
        if not values:
            return UpdateResponse(flag=True)
        return self.update_direct(condition, values=values)

    def find_fabric_meta_model_config(self, asset_type_ids=None, fields=None, sort_fields=None):
        query = self.build_fabric_meta_model_config_condition(asset_type_ids=asset_type_ids)
        return self.find(condition=query, fields=fields, sort_fields=sort_fields)

    def get_fabric_meta_model_config(
        self, fabric_config_id=None, asset_type_id=None, asset_type_ids=None, fields=None, need_dict=False
    ):
        query = self.build_fabric_meta_model_config_condition(
            fabric_config_id=fabric_config_id, asset_type_ids=asset_type_ids, asset_type_id=asset_type_id
        )
        _get_method = self.get_direct if need_dict else self.get
        return _get_method(condition=query, fields=fields)

    def get_fabric_meta_model_config_count(self, fabric_config_id=None, asset_type_id=None, asset_type_ids=None):
        query = self.build_fabric_meta_model_config_condition(
            fabric_config_id=fabric_config_id, asset_type_ids=asset_type_ids, asset_type_id=asset_type_id
        )
        return self.count(condition=query)

    def upsert_model_fabric_config(self, values, asset_type_id=None):
        condition = self.build_fabric_meta_model_config_condition(asset_type_id=asset_type_id)
        values = {"$set": values}
        return self.find_and_modify(condition, values, simple_values=False, upsert=True)

    def delete_model_fabric(self, fabric_config_id=None, asset_type_id=None):
        condition = self.build_fabric_meta_model_config_condition(
            fabric_config_id=fabric_config_id, asset_type_id=asset_type_id
        )
        return self.delete_one(condition=condition)

    @classmethod
    def build_fabric_meta_model_config_condition(
        cls, fabric_config_id=None, fabric_config_ids=None, asset_type_id=None, asset_type_ids=None
    ):
        query = {}

        _id_condition = cls.build_id_ids_condition(data_id=fabric_config_id, data_ids=fabric_config_ids)
        _asset_type_condition = cls.build_id_ids_condition(data_id=asset_type_id, data_ids=asset_type_ids)

        if _id_condition:
            query["_id"] = _id_condition

        if _asset_type_condition:
            query["asset_type_id"] = _asset_type_condition

        return query


class FabricConfigService(MongoHandler):
    DEFAULT_SCHEMA = fabric_config_schema
    DEFAULT_TABLE = "fabric.meta_config"

    @classmethod
    def build_fabric_config_sort(cls, fields: List[str]) -> Dict:
        sort_fields: List[Set] = []
        for field in fields:
            sort_fields.append((field, pymongo.DESCENDING))
        return sort_fields

    @classmethod
    def build_asset_type_condition(cls, asset_type_id=None, asset_type_ids=None):
        query = {}
        if asset_type_id:
            query["$eq"] = cls.build_id_ids_condition(asset_type_id)
        if asset_type_ids:
            query["$in"] = cls.build_id_ids_condition(asset_type_id)
        return query

    @classmethod
    def build_condition(
        cls,
        fabric_config_id=None,
        fabric_config_ids=None,
        asset_type_id=None,
        asset_type_ids=None,
        asset_type: str = None,
        **kwargs
    ):
        query = {}

        _id_condition = cls.build_id_ids_condition(data_id=fabric_config_id, data_ids=fabric_config_ids)
        _asset_type_condition = cls.build_asset_type_condition(
            asset_type_id=asset_type_id, asset_type_ids=asset_type_ids
        )

        if _id_condition:
            query["_id"] = _id_condition

        if _asset_type_condition:
            query["asset_type_id"] = _asset_type_condition
        if asset_type:
            query["asset_type"] = asset_type

        # 参数is_master
        is_master = kwargs.get("is_master", None)
        if is_master is not None:
            query["is_master"] = is_master

        return query

    def upsert_model_fabric_config(self, values, id=None):
        condition = self.build_condition(fabric_config_id=id)
        values = {"$set": values}
        return self.find_and_modify(condition, values, simple_values=False, upsert=True)

    def update_fabric_config(
        self,
        id: str,
        stage_name: str = None,
        stage_ids: List[str] = None,
        fabric_stages: List[Dict] = None,
        fabric_adapter: List[Dict] = None,
        fabric_policy: Dict = None,
        global_field_config: Dict = None,
        oneself_field_config: List[Dict] = None,
        **kwargs
    ) -> UpdateResponse:
        """更新融合配置"""
        condition = self.build_condition(fabric_config_id=id)
        entity_values: dict = {}
        entity_values["is_modify"] = True
        entity_values["modify_time"] = get_now()
        entity_values["update_time"] = get_now()
        entity_values["modify_username"] = kwargs.get("modify_username", "")

        if stage_name is not None:
            entity_values["stage_name"] = stage_name
        if stage_ids is not None:
            entity_values["stage_ids"] = [ObjectId(stage_id) for stage_id in stage_ids]
        if fabric_adapter is not None:
            entity_values["fabric_adapter"] = fabric_adapter
        if fabric_stages is not None:
            entity_values["fabric_stages"] = [
                {"stage_id": ObjectId(stage.get("stage_id", None)), "stage_name": stage.get("stage_name", "")}
                for stage in fabric_stages
            ]
        if fabric_policy is not None:
            entity_values["fabric_policy"] = fabric_policy
        if global_field_config is not None:
            entity_values["global_field_config"] = global_field_config
        if oneself_field_config is not None:
            entity_values["oneself_field_config"] = oneself_field_config
        return self.update_direct(condition, entity_values, simple_values=True, upsert=True)

    def add_last_fabric_stage(self, fabric_config_id: str, stage_config_id: str):
        condition = self.build_condition(fabric_config_id=fabric_config_id)
        fabric_config = self.find_direct(condition=condition)
        if fabric_config.fabric_stage is None:
            fabric_config.fabric_stage = [stage_config_id]
        else:
            fabric_config.fabric_stage.append(stage_config_id)
        return self.save_direct(fabric_config)

    def delete_stage_fabric(self, fabric_config_id: str, stage_config_id: str):
        condition = self.build_condition(fabric_config_id=fabric_config_id)
        fabric_config = self.find_direct(condition=condition)
        if fabric_config.fabric_stage:
            return None
        else:
            fabric_config.fabric_stage.remove(stage_config_id)
        return self.save_direct(fabric_config)

    def insert_fabric_config(self, values) -> ObjectIdField:
        fabric_entity = self.load_entity(**values)
        entity_resp = self.save(fabric_entity)
        return entity_resp.inserted_id

    def find_fabric_meta_model_config(self, asset_type_ids=None, fields=None, sort_fields=None, **kwargs):
        query = self.build_condition(asset_type_ids=asset_type_ids, **kwargs)
        sort_field = self.build_fabric_config_sort(sort_fields)
        return self.find(condition=query, fields=fields, sort_fields=sort_field)

    def get_fabric_meta_model_config(
        self, fabric_config_id=None, asset_type_id=None, asset_type_ids=None, fields=None, need_dict=False
    ):
        query = self.build_condition(
            fabric_config_id=fabric_config_id, asset_type_ids=asset_type_ids, asset_type_id=asset_type_id
        )
        _get_method = self.get_direct if need_dict else self.get
        return _get_method(condition=query, fields=fields)

    def delete_model_fabric(self, fabric_config_id=None, asset_type_id=None) -> DeleteResponse:
        condition = self.build_condition(fabric_config_id=fabric_config_id, asset_type_id=asset_type_id)
        return self.delete_one(condition=condition)
