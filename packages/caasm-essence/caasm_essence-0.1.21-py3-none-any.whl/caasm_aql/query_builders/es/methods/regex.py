from typing import List

from caasm_aql.base import AqlTargetType, AqlMethodCall
from caasm_aql.query_builders.method import Method
from caasm_meta_model.service.entities.meta_model import MetaFieldType


class RegexMethod(Method):
    def __init__(self):
        super(RegexMethod, self).__init__()
        self.add_param("regex", "正则表达式", "用于比较的正则表达式", MetaFieldType.STRING, True)

    @property
    def get_param_types(self):
        return [MetaFieldType.STRING]

    def build(self, field, call: AqlMethodCall, target_type) -> dict:
        _prefix = "adapters." if target_type == AqlTargetType.ADAPTER else ""
        path = self.parse_field_path(field)
        value = self.parse_value(call)

        if field.complex_full_name:
            result = {
                "nested": {
                    "path": _prefix + field.complex_full_name,
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "regexp": {path: value}
                                }
                            ]
                        }
                    },
                }
            }
        else:
            result = {"regexp": {path: value}}
        return result

    @classmethod
    def parse_field_path(cls, meta_field):
        _field_type = meta_field.type
        _result = meta_field.full_name
        if _field_type == MetaFieldType.VERSION:
            _result += ".plain"
        return _result

    @classmethod
    def parse_value(cls, call):
        return call.param_list[0]

    @classmethod
    def parse_high_light_value(cls, call):
        return call.param_list[0]

    @property
    def name(self) -> str:
        return "regex"

    @property
    def display_name(self) -> str:
        return "regex"

    @property
    def description(self):
        return "字符串类型字段，字段值满足给定的正则表达式"

    @property
    def order(self) -> int:
        return 2

    @property
    def available_data_types(self) -> List:
        return [MetaFieldType.STRING, MetaFieldType.EMAIL, MetaFieldType.VERSION, MetaFieldType.LIST]

    @property
    def type(self):
        return "input"

    @property
    def auto_complete(self):
        return False
