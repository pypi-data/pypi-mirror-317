from functools import cached_property

from caasm_aql.base import AqlOperator
from caasm_aql.query_builders.es.operators._base import ESOperator
from caasm_meta_model.service.entities.meta_model import MetaFieldType


class GTOperator(ESOperator):
    _flag = "gt"
    _CUSTOMER_DATE_TYPE_OPERATOR = [
        MetaFieldType.IP, MetaFieldType.IPV4, MetaFieldType.IPV6, MetaFieldType.STRING, MetaFieldType.LIST,
        MetaFieldType.OBJECT, MetaFieldType.VERSION, MetaFieldType.ENUM,
    ]

    @classmethod
    def build_keyword_result(cls, field, call):
        return {"range": {cls.field_name(field): {cls._flag: call.value}}}

    @property
    def get_operator(self) -> AqlOperator:
        return AqlOperator.GREATER

    @classmethod
    def description(cls):
        return "大于"

    @classmethod
    def get_display_name(cls):
        return ">"

    @property
    def auto_complete(self):
        return False


class GTEOperator(GTOperator):
    _flag = "gte"

    @property
    def get_operator(self) -> AqlOperator:
        return AqlOperator.GREATER_OR_EQUAL

    @classmethod
    def description(self):
        return "大于等于"

    @classmethod
    def get_display_name(cls):
        return ">="


class VersionGTOperator(GTOperator):
    _front_flag = "gte"

    @cached_property
    def available_data_types(self) -> list:
        return [MetaFieldType.VERSION]

    @classmethod
    def build_keyword_result(cls, field, call):
        value = str(call.value)
        values = value.split(".")
        sub_conditions = cls.build_sub_conditions(field, values)
        return {"bool": {"must": sub_conditions}}

    @classmethod
    def build_sub_conditions(cls, field, values):
        result = []
        _compare_index = len(values) - 1
        for _index, _value in enumerate(values):
            if _index < _compare_index:
                _flag = cls._front_flag
            else:
                _flag = cls._flag

            result.append({"range": {cls.field_name(field) + f".v{_index}": {_flag: int(_value)}}})
        return result


class VersionGTEOperator(VersionGTOperator):
    _flag = "gte"
    _like_flag = "gte"

    @property
    def get_operator(self) -> AqlOperator:
        return AqlOperator.GREATER_OR_EQUAL

    @cached_property
    def available_data_types(self) -> list:
        return [MetaFieldType.VERSION]

    @classmethod
    def description(cls):
        return "大于等于"

    @classmethod
    def get_display_name(cls):
        return ">="
