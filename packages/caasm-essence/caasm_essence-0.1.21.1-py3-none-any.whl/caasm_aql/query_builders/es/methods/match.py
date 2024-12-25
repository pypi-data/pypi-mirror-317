from typing import List

from caasm_aql.base import AqlMethodCall
from caasm_aql.query_builders.method import Method
from caasm_meta_model.service.entities.meta_model import MetaFieldType, MetaField


class MatchMethod(Method):
    def __init__(self):
        super(MatchMethod, self).__init__()
        self.add_param(
            "keywords", "关键字列表", "用于匹配的关键字列表", MetaFieldType.LIST, True
        )

    @property
    def get_param_types(self):
        return [MetaFieldType.LIST]

    def build(self, field: MetaField, call: AqlMethodCall, target_type) -> dict:
        if field.complex_full_name:
            result = {
                "nested": {
                    "path": field.complex_full_name,
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "script": {
                                        "script": {
                                            "source": f"""
                                                if (doc.containsKey('{field.full_name}')){{
                                                    def value = doc['{field.full_name}'].toString();
                                                    def matchPart = '{call.param_list[0]}';
                                                    return value.contains(matchPart);
                                                }} else {{
                                                    return false;
                                                }}
                                              """
                                        }
                                    }
                                }
                            ]
                        }
                    },
                }
            }
        else:
            result = {
                "script": {
                    "script": {
                        "source": f"""
                            if (doc.containsKey('{field.full_name}')){{
                                def value = doc['{field.full_name}'].toString();
                                def matchPart = '{call.param_list[0]}';
                                return value.contains(matchPart);
                            }} else {{
                                return false;
                            }}
                          """
                    }
                }
            }
        return result

    @classmethod
    def parse_high_light_value(cls, call):
        return call.param_list[0]

    @property
    def name(self) -> str:
        return "match"

    @property
    def display_name(self) -> str:
        return "match"

    @property
    def description(self):
        return "对子字符串进行部分匹配"

    @property
    def order(self) -> int:
        return 2

    @property
    def available_data_types(self) -> List:
        return [
            MetaFieldType.STRING, MetaFieldType.EMAIL, MetaFieldType.VERSION, MetaFieldType.IP, MetaFieldType.IPV4,
            MetaFieldType.IPV6
        ]

    @property
    def type(self):
        return "input"

    @property
    def auto_complete(self):
        return False
