from caasm_aql.base import AqlTargetType, AqlMethodCall
from caasm_aql.query_builders.method import Method
from caasm_meta_model.service.entities.meta_model import MetaFieldType


class StartsMethod(Method):
    def __init__(self):
        super(StartsMethod, self).__init__()
        self.add_param("prefix", "前缀", "用于比较的结尾前缀字符串", MetaFieldType.STRING, True)

    @property
    def get_param_types(self):
        return [MetaFieldType.STRING]

    def build(self, field, call: AqlMethodCall, target_type) -> dict:

        prefix = "adapters." if target_type == AqlTargetType.ADAPTER else ""
        query_path = prefix + self.build_query_path(field)

        if field.complex_full_name:
            result = {
                "nested": {
                    "path": prefix + field.complex_full_name,
                    "query": {"bool": {"must": [{"wildcard": {query_path: call.param_list[0] + "*"}}]}},
                }
            }
        else:
            result = {"wildcard": {query_path: call.param_list[0] + "*"}}
        return result

    @classmethod
    def build_query_path(cls, field):
        _result = field.full_name
        return _result

    @classmethod
    def parse_high_light_value(cls, call):
        return call.param_list[0]

    @property
    def name(self) -> str:
        return "starts"

    @property
    def display_name(self) -> str:
        return "startswith"

    @property
    def description(self):
        return "字符串字段的值，以给定子字符串开头"

    @property
    def order(self) -> int:
        return 2

    @property
    def available_data_types(self):
        return [MetaFieldType.STRING]

    @property
    def type(self):
        return "input"

    @property
    def auto_complete(self):
        return False
