from typing import Dict


class Function:
    def call(self, value_list: list):
        raise NotImplementedError()

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def order(self) -> int:
        raise NotImplementedError()

    @property
    def get_param_types(self):
        raise NotImplementedError()

    @property
    def get_result_type(self):
        raise NotImplementedError()


class FunctionManager:
    def __init__(self):
        self.functions: Dict[str, Function] = dict()

    def register(self, function: Function):
        self.functions[function.name] = function

    def get(self, function_name: str):
        return self.functions.get(function_name)
