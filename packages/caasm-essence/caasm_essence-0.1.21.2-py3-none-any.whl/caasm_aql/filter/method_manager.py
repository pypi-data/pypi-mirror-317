from typing import Type

from caasm_aql.filter.method import Method
from caasm_aql.filter.methods.ends import EndsMethod
from caasm_aql.filter.methods.exists import ExistsMethod
from caasm_aql.filter.methods.in_ import InMethod
from caasm_aql.filter.methods.match import MatchMethod
from caasm_aql.filter.methods.regex import RegexMethod
from caasm_aql.filter.methods.size import SizeMethod
from caasm_aql.filter.methods.starts import StartsMethod


class MethodManager:
    def __init__(self):
        self._methods = {}

    def register(self, method_cls_: Type[Method]):
        self._methods[method_cls_.METHOD] = method_cls_

    def get_method_cls(self, method_name) -> Type[Method]:
        return self._methods.get(method_name)


method_manager = MethodManager()

method_clss = [
    EndsMethod,
    ExistsMethod,
    InMethod,
    MatchMethod,
    RegexMethod,
    SizeMethod,
    StartsMethod,
]

for method_cls in method_clss:
    method_manager.register(method_cls)
