import ipaddress
from functools import cached_property

from IPy import IP

from caasm_aql.base import AqlOperator, AqlOperatorCall
from caasm_aql.query_builders.es.operators._base import ESOperator
from caasm_meta_model.service.entities.meta_model import MetaFieldType


class _EqualOperator(ESOperator):
    _CUSTOMER_DATE_TYPE_OPERATOR = [MetaFieldType.OBJECT, MetaFieldType.VERSION, MetaFieldType.ENUM, MetaFieldType.IPV4]

    @property
    def get_operator(self) -> AqlOperator:
        return AqlOperator.EQUAL

    @classmethod
    def parse_high_light_value(cls, call):
        return call.value

    @classmethod
    def get_display_name(cls):
        return "="

    @classmethod
    def description(cls):
        return "等于"


class EqualOperator(_EqualOperator):
    def _get_es_operator(self):
        return '=='


class NotEqualOperator(_EqualOperator):
    _CUSTOMER_DATE_TYPE_OPERATOR = [MetaFieldType.OBJECT, MetaFieldType.VERSION, MetaFieldType.ENUM]

    @property
    def get_operator(self) -> AqlOperator:
        return AqlOperator.NOT_EQUAL

    @classmethod
    def build_keyword_result(cls, field, call):
        call: AqlOperatorCall = call
        return {"bool": {"must_not": [super(NotEqualOperator, cls).build_keyword_result(field, call)]}}

    @classmethod
    def description(cls):
        return "不等于"

    @classmethod
    def get_display_name(cls):
        return "!="


class EnumEqualOperator(EqualOperator):

    @classmethod
    def field_name(cls, field):
        field_name = super(EnumEqualOperator, cls).field_name(field)
        return field_name + ".value"

    @cached_property
    def available_data_types(self) -> list:
        return [MetaFieldType.ENUM]


class EnumNotEqualOperator(NotEqualOperator):

    @cached_property
    def available_data_types(self) -> list:
        return [MetaFieldType.ENUM]

    @classmethod
    def field_name(cls, field):
        field_name = super(EnumNotEqualOperator, cls).field_name(field)
        return field_name + ".value"


class VersionEqualOperator(EqualOperator):

    @classmethod
    def build_keyword_result(cls, field, call):
        return {"term": {f"{field.full_name}.plain": call.value}}

    @cached_property
    def available_data_types(self) -> list:
        return [MetaFieldType.VERSION]

    @classmethod
    def field_name(cls, field):
        return f'{field.full_name}.plain'


class VersionNotEqualOperator(NotEqualOperator):
    @classmethod
    def build_keyword_result(cls, field, call):
        return {"bool": {"must_not": [super(VersionNotEqualOperator, cls).build_keyword_result(field, call)]}}

    @property
    def get_operator(self) -> AqlOperator:
        return AqlOperator.NOT_EQUAL

    @cached_property
    def available_data_types(self) -> list:
        return [MetaFieldType.VERSION]

    @classmethod
    def field_name(cls, field):
        return f'{field.full_name}.plain'


class IPv4EqualOperator(EqualOperator):
    @cached_property
    def available_data_types(self) -> list:
        return [MetaFieldType.IPV4]

    @classmethod
    def build_keyword_result(cls, field, call):
        value = cls._convert_value(call.value)
        if value:
            return {"term": {field.full_name: cls._convert_value(call.value)}}
        else:
            return None

    @classmethod
    def _convert_value(cls, value):
        try:
            ipaddress.IPv4Address(value)
            is_ipv4 = True
        except ipaddress.AddressValueError:
            is_ipv4 = False
        try:
            cidr = IP(value)
            if cidr.len() > 1:
                is_cidr = True
            else:
                is_cidr = False
        except ValueError:
            is_cidr = False
        if is_ipv4 or is_cidr:
            return value
        else:
            return None


class IPEqualOperator(EqualOperator):

    @cached_property
    def available_data_types(self) -> list:
        return [MetaFieldType.IP, MetaFieldType.IPV4]

    @classmethod
    def build_keyword_result(cls, field, call):
        value = cls._convert_value(call.value)
        if value:
            return {"term": {field.full_name: cls._convert_value(call.value)}}
        else:
            return None

    @classmethod
    def _convert_value(cls, value):
        try:
            ipaddress.IPv4Address(value)
            is_ipv4 = True
        except ipaddress.AddressValueError:
            is_ipv4 = False
        try:
            ipaddress.IPv6Address(value)
            is_ipv6 = True
        except ipaddress.AddressValueError:
            is_ipv6 = False
        try:
            cidr = IP(value)
            if cidr.len() > 1:
                is_cidr = True
            else:
                is_cidr = False
        except ValueError:
            is_cidr = False
        if is_ipv4 or is_ipv6 or is_cidr:
            return value
        else:
            return None
        # values = value.split(".")
        # _values_length = len(values)
        # _check_length = 4
        # if _values_length == _check_length:
        #     return value
        #
        # _result = []
        #
        # for index in range(_check_length):
        #     if index < _values_length:
        #         _tmp_value = values[index]
        #         _tmp_value = "0" if not _tmp_value else _tmp_value
        #         _result.append(_tmp_value)
        #     elif index < _check_length - 1:
        #         _result.append("0")
        #     elif index == _check_length - 1:
        #         _result.append("0/24")
        # return ".".join(_result)


class IPV6EqualOperator(EqualOperator):
    @cached_property
    def available_data_types(self) -> list:
        return [MetaFieldType.IPV6]

    @classmethod
    def build_keyword_result(cls, field, call):
        value = cls._convert_value(call.value)
        if value:
            return {"term": {field.full_name: cls._convert_value(call.value)}}
        else:
            return None

    @classmethod
    def _convert_value(cls, value):
        try:
            ipaddress.IPv6Address(value)
            is_ipv6 = True
        except ipaddress.AddressValueError:
            is_ipv6 = False
        if is_ipv6:
            return value
        else:
            return None


class RelationEqualOperator(EqualOperator):

    @classmethod
    def field_name(cls, field):
        field_name = super(RelationEqualOperator, cls).field_name(field)
        return field_name + ".display_value"

    @cached_property
    def available_data_types(self) -> list:
        return [MetaFieldType.RELATION]
