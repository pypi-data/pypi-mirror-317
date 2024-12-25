from collections import defaultdict
from typing import List

from caasm_aql.base import AqlMethodCall


class Method:
    def __init__(self):
        self._params: List[Param] = list()

    def add_param(
        self,
        name: str,
        display_name: str,
        description: str,
        data_type,
        required: bool = False,
        default=None,
    ):
        self._params.append(Param(name, display_name, description, data_type, required, default))

    def build(self, field, call: AqlMethodCall, target_type):
        raise NotImplementedError()

    def get_high_light(self, field, call):
        value = self.parse_high_light_value(call)
        if value is None:
            return {}
        return {"name": field.full_name, "value": value, "flag": self.name}

    @classmethod
    def parse_high_light_value(cls, call):
        return None

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def display_name(self) -> str:
        raise NotImplementedError()

    @property
    def order(self) -> int:
        raise NotImplementedError()

    @property
    def available_data_types(self) -> List:
        raise NotImplementedError()

    @property
    def get_param_types(self):
        raise NotImplementedError()

    @property
    def description(self):
        return ""

    @property
    def params(self):
        return self._params

    @property
    def type(self):
        return "select"

    @property
    def auto_complete(self):
        return True


class Param:
    def __init__(
        self,
        name: str,
        display_name: str,
        description: str,
        data_type,
        required: bool = False,
        default=None,
    ):
        self.name: str = name
        self.display_name: str = display_name
        self.description: str = description
        self.data_type = data_type
        self.required: bool = required
        self.default = default


class MethodManager:
    def __init__(self):
        self._method_map = defaultdict(dict)

    def register(self, method: Method):
        for data_type in method.available_data_types:
            self._method_map[data_type][method.name] = method

    def get(self, data_type, name):
        return self._method_map[data_type].get(name)

    def find_method(self, data_type):
        return list(self._method_map[data_type].values())
