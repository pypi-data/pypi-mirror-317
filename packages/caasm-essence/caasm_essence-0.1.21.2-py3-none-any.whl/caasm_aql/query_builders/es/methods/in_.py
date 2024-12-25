from caasm_aql.base import AqlTargetType, AqlMethodCall
from caasm_aql.query_builders.method import Method
from caasm_meta_model.service.entities.meta_model import MetaFieldType


class InMethod(Method):
    def __init__(self):
        super(InMethod, self).__init__()
        self.add_param("prefix", "取值范围", "字段有效的取值范围", MetaFieldType.STRING, True)

    @property
    def get_param_types(self):
        return [MetaFieldType.LIST]

    def build(self, field, call: AqlMethodCall, target_type) -> dict:
        full_field_name = field.full_name
        if target_type == AqlTargetType.ADAPTER:
            prefix = "adapters."
        else:
            prefix = ""
        if field.complex_full_name:
            result = {
                "nested": {
                    "path": prefix + field.complex_full_name,
                    "query": {"bool": {"must": [{"terms": {prefix + full_field_name: call.param_list[0]}}]}},
                }
            }
        else:
            result = {"terms": {prefix + full_field_name: call.param_list[0]}}
        return result

    def parse_high_light_value(self, call):
        return call.param_list[0]

    @property
    def name(self) -> str:
        return "in"

    @property
    def display_name(self) -> str:
        return "in"

    @property
    def description(self):
        return "字段值在给定的数组中存在"

    @property
    def order(self) -> int:
        return 2

    @property
    def available_data_types(self):
        return [
            MetaFieldType.STRING,
            MetaFieldType.INT,
            MetaFieldType.FLOAT,
            MetaFieldType.EMAIL,
            MetaFieldType.IP,
            MetaFieldType.IPV4,
            MetaFieldType.IPV6,
            MetaFieldType.VERSION,
            MetaFieldType.ENUM,
            MetaFieldType.DATE,
            MetaFieldType.DATETIME,
            MetaFieldType.TIMESTAMP
        ]
