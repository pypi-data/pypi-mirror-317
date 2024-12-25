from caasm_aql.base import AqlTargetType, AqlMethodCall
from caasm_aql.query_builders.method import Method
from caasm_meta_model.service.entities.meta_model import MetaFieldType, TOTAL_META_FIELD_TYPES


class ExistsMethod(Method):
    @property
    def get_param_types(self):
        return [MetaFieldType.ANY]

    @property
    def available_data_types(self) -> list:
        return TOTAL_META_FIELD_TYPES

    @property
    def order(self) -> int:
        return 1

    @property
    def name(self):
        return "exists"

    @property
    def display_name(self) -> str:
        return "exists"

    @property
    def description(self):
        return "该字段存在"

    def build(self, field, call: AqlMethodCall, target_type: AqlTargetType) -> dict:

        field_name = self.get_field_name(field, target_type)
        if field.complex_full_name:
            result = {
                "nested": {
                    "path": self.field_prefix(target_type) + field.complex_full_name,
                    "query": {"bool": {"must": [{"exists": {"field": field_name}}]}},
                }
            }
        else:
            result = {
                "exists": {
                    "field": field_name,
                }
            }
        return result

    @classmethod
    def get_field_name(cls, field, target_type):
        full_field_name = field.full_name
        return cls.field_prefix(target_type) + full_field_name

    @classmethod
    def field_prefix(cls, target_type):
        if target_type == AqlTargetType.ADAPTER:
            prefix = "adapters."
        else:
            prefix = ""
        return prefix
