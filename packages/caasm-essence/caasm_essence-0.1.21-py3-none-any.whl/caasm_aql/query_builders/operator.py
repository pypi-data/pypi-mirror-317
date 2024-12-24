from collections import defaultdict
from typing import Dict, Set

from caasm_aql.base import AqlOperator, AqlOperatorCall
from caasm_meta_model.service.entities.meta_model import MetaFieldType


class Operator:
    def build(self, field, call: AqlOperatorCall) -> (Dict, bool):
        raise NotImplementedError()

    def build_field_compare_result(self, field, compare_field) -> (Dict, bool):
        raise NotImplementedError()

    @property
    def get_operator(self) -> AqlOperator:
        raise NotImplementedError

    @classmethod
    def get_display_name(cls):
        return ""

    @property
    def description(self):
        return ""

    @property
    def available_data_types(self) -> list:
        raise NotImplementedError()

    def unavailable_sub_data_types(self, data_type) -> Set:
        return set()

    def get_high_light(self, field, call):
        value = self.parse_high_light_value(call)
        if value is None:
            return {}
        return {"name": field.full_name, "value": value, "flag": self.get_operator.value}

    @classmethod
    def parse_high_light_value(cls, call):
        return None

    @property
    def type(self):
        return "select"

    @property
    def auto_complete(self):
        return True


class OperatorManager:
    def __init__(self):
        self._operator_map = defaultdict(dict)

    def register(self, operator: Operator):
        for data_type in operator.available_data_types:
            op = operator.get_operator
            self._operator_map[data_type][op] = operator

    def get(self, data_type, op: AqlOperator):
        op_mapper = self._operator_map.get(data_type) or self._operator_map.get(MetaFieldType.ANY)
        if not op_mapper:
            return None
        return op_mapper.get(op)

    def find_operator(self, data_type, sub_data_type=None):
        data = self._operator_map.get(data_type)

        result = {} if not data else data
        return list(result.values())
