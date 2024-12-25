from typing import Dict, List

from caasm_config.config import caasm_config
from caasm_grpc_client.clients.meta_data_client import MetaDataClient
from caasm_meta_model.service.entities.meta_model import MetaFieldType


class MetaDataManager(object):
    def __init__(self):
        self._handler = MetaDataClient(caasm_config.META_DATA_RPC_ADDRESS)

    def initialize(self):
        return self._handler.initialize()

    def transform_batch(self, category, model_name, data, date=""):
        return self._handler.transform_batch(category, model_name, data, date)

    def transform_test(self, category, model_name, data, date=""):
        return self._handler.transform_test(category, model_name, data, date)

    def find_storage_table(self, category):
        return self._handler.find_storage_table(category)

    def storage_to_query_engine(self, category, date):
        return self._handler.storage_to_query_engine(category, date)

    @classmethod
    def padding_field(cls, model_display_name, model_name, field_schemas: List[Dict]):
        for field_schema in field_schemas:
            cls._padding_full_name(field_schema, model_name, model_display_name)

    @classmethod
    def _padding_full_name(
        cls, field_schema, parent_name, parent_display_name, last_field_type="", complex_full_name=None
    ):
        field_type = field_schema["type"]
        children = field_schema["children"]

        if last_field_type == MetaFieldType.LIST:
            full_name = parent_name
            full_display_name = parent_display_name
        else:
            full_name = parent_name + "." + field_schema["name"]
            full_display_name = parent_display_name + "-" + field_schema["display_name"]

        if field_type == MetaFieldType.LIST and children and children[0]["type"] == MetaFieldType.OBJECT:
            is_complex = True
            complex_full_name = full_name
        else:
            is_complex = False

        if field_type == MetaFieldType.RELATION:
            field_schema["full_text_search"] = True
            _child = cls.build_field_dict("display_value", MetaFieldType.STRING, "展示名称", full_text_search=True)
            field_schema["children"] = [_child]

        field_schema["is_complex"] = is_complex
        field_schema["full_name"] = full_name
        field_schema["full_display_name"] = full_display_name
        field_schema["complex_full_name"] = complex_full_name

        for child_schema in field_schema["children"]:
            cls._padding_full_name(
                child_schema,
                full_name,
                full_display_name,
                last_field_type=field_schema["type"],
                complex_full_name=complex_full_name,
            )

    def finish(self):
        self._handler.finish()

    @classmethod
    def build_field_dict(cls, name, field_type, display_name="", **kwargs):
        return {
            "name": name,
            "required": kwargs.get("required", False),
            "allow_null": kwargs.get("required", False),
            "encrypt": kwargs.get("required", False),
            "display_name": display_name or name,
            "type": field_type,
            "description": kwargs.get("description", ""),
            "default": kwargs.get("default", ""),
            "unique": kwargs.get("unique", False),
            "hidden": kwargs.get("hidden", False),
            "children": kwargs.get("children", []),
            "internal": kwargs.get("internal", True),
            "setting": kwargs.get("setting", {}),
            "priority": int(float(kwargs.get("priority", 0))),
            "full_text_search": kwargs.get("full_text_search", False),
        }
