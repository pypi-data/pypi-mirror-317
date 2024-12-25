import re

from caasm_persistence.handler.storage.mongo import MongoHandler

from caasm_pipeline.fabric.service.schema.runtime import field_fabric_policy_schema


class FieldFabricPolicyService(MongoHandler):
    DEFAULT_SCHEMA = field_fabric_policy_schema
    DEFAULT_TABLE = "field_fabric_policy"

    def find_field_fabric_policy(
        self,
        fabric_config_id=None,
        offset=None,
        limit=None,
        asset_type_id=None,
        full_name=None,
        full_names=None,
        keyword=None,
        fields=None,
        sort_fields=None,
    ):
        query = self.build_field_fabric_policy_condition(
            keyword=keyword,
            fabric_config_id=fabric_config_id,
            asset_type_id=asset_type_id,
            full_name=full_name,
            full_names=full_names,
        )
        return self.find(condition=query, offset=offset, limit=limit, fields=fields, sort_fields=sort_fields)

    def upsert_field_fabric_config(self, values, asset_type_id=None, full_name=None):
        condition = self.build_field_fabric_policy_condition(asset_type_id=asset_type_id, full_name=full_name)
        values = {"$set": values}
        return self.find_and_modify(condition, values, simple_values=False, upsert=True)

    def save_field_fabric_policy(self, asset_type, model_name=None, internal=None, description=None):
        entity = self.load_entity(
            asset_type=asset_type,
            model_name=model_name,
            internal=internal,
            description=description,
        )
        return self.save(entity)

    def update_field_fabric_polic(self, asset_type_id=None, **kwargs):
        condition = self.build_field_fabric_policy_condition(asset_type_id=asset_type_id)
        return self.update_multi_direct(condition, values=kwargs)

    def get_field_fabric_polic(self, asset_type_id=None, fields=None):
        condition = self.build_field_fabric_policy_condition(asset_type_id=asset_type_id)
        return self.get(condition, fields=fields)

    def get_field_fabric_policy_count(self, asset_type_id=None, keyword=None):
        condition = self.build_field_fabric_policy_condition(asset_type_id=asset_type_id, keyword=keyword)
        return self.count(condition)

    def delete_field_fabric_policy(self, asset_type_id=None, full_name=None):
        condition = self.build_field_fabric_policy_condition(asset_type_id=asset_type_id, full_name=full_name)
        return self.delete_one(condition=condition)

    def delete_fields_fabric_policy(self, fabric_config_id=None, fabric_config_ids=None):
        condition = self.build_field_fabric_policy_condition(fabric_config_id=fabric_config_id)
        return self.delete_multi(condition=condition)

    @classmethod
    def build_field_fabric_policy_condition(
        cls, full_names=None, full_name=None, asset_type_id=None, keyword=None, fabric_config_id=None
    ):
        condition = {}

        if asset_type_id:
            condition["asset_type_id"] = cls._build_id(asset_type_id)

        if full_name:
            condition["full_name"] = full_name

        if keyword:
            keyword_re = re.compile(keyword)
            condition["$or"] = [
                {"full_name": {"$regex": keyword_re}},
            ]

        if fabric_config_id:
            condition["fabric_config_id"] = cls._build_id(fabric_config_id)

        if full_names:
            condition["full_name"] = {"$in": full_names}

        return condition
