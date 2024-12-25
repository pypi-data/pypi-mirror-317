from typing import List

from caasm_aql.base import AqlTargetType, AqlMethodCall
from caasm_aql.query_builders.method import Method
from caasm_meta_model.service.entities.meta_model import MetaFieldType


class EndsMethod(Method):
    def __init__(self):
        super(EndsMethod, self).__init__()
        self.add_param("postfix", "后缀", "用于比较的结尾后缀字符串", MetaFieldType.STRING, True)

    @property
    def get_param_types(self):
        return [MetaFieldType.STRING]

    def build(self, field, call: AqlMethodCall, target_type) -> dict:
        full_field_name = field.full_name
        if target_type == AqlTargetType.ADAPTER:
            prefix = "adapters."
        else:
            prefix = ""
        if len(call.param_list) != 1:
            raise ValueError('参数数量错误')
        if not isinstance(call.param_list[0], str):
            raise ValueError('参数数据类型必须为字符串')
        if field.complex_full_name:
            result = {
                "nested": {
                    "path": prefix + field.complex_full_name,
                    "query": {"bool": {"must": [{"wildcard": {prefix + full_field_name: "*" + call.param_list[0]}}]}},
                }
            }
        else:
            result = {"wildcard": {prefix + full_field_name: "*" + call.param_list[0]}}
        return result

    @classmethod
    def parse_high_light_value(cls, call):
        return call.param_list[0]

    @property
    def name(self) -> str:
        return "ends"

    @property
    def display_name(self) -> str:
        return "endswith"

    @property
    def description(self):
        return "字符串字段的值，以给定子字符串结尾"

    @property
    def order(self) -> int:
        return 2

    @property
    def available_data_types(self) -> List:
        return [MetaFieldType.STRING]

    @property
    def type(self):
        return "input"

    @property
    def auto_complete(self):
        return False
