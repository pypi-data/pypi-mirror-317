from caasm_aql.query_builders.converter import ConverterManager
from caasm_aql.query_builders.es.converters.bool import BooleanConverter
from caasm_aql.query_builders.es.converters.date import DateConverter
from caasm_aql.query_builders.es.converters.datetime import DatetimeConverter
from caasm_aql.query_builders.es.converters.enum import EnumConverter
from caasm_aql.query_builders.es.converters.number import NumberConverter
from caasm_aql.query_builders.es.converters.string import StringConverter
from caasm_aql.query_builders.es.methods.ends import EndsMethod
from caasm_aql.query_builders.es.methods.exists import ExistsMethod
from caasm_aql.query_builders.es.methods.in_ import InMethod
from caasm_aql.query_builders.es.methods.match import MatchMethod
from caasm_aql.query_builders.es.methods.regex import RegexMethod
from caasm_aql.query_builders.es.methods.size import SizeGreaterThanMethod, SizeGreaterThanEqualMethod, \
    SizeLesserThanMethod, SizeLesserThanEqualMethod
from caasm_aql.query_builders.es.methods.starts import StartsMethod
from caasm_aql.query_builders.es.operators.equal import (
    EqualOperator,
    NotEqualOperator,
    EnumEqualOperator,
    EnumNotEqualOperator,
    VersionEqualOperator,
    VersionNotEqualOperator,
    RelationEqualOperator, IPV6EqualOperator, IPEqualOperator, IPv4EqualOperator,
)
from caasm_aql.query_builders.es.operators.gt import (
    GTOperator,
    GTEOperator,
    VersionGTOperator,
    VersionGTEOperator,
)
from caasm_aql.query_builders.es.operators.lt import (
    LTEOperator,
    LTOperator,
    VersionLTOperator,
    VersionLTEOperator,
)
from caasm_aql.query_builders.function import FunctionManager
from caasm_aql.query_builders.functions.days_ago import DaysAgoFunction
from caasm_aql.query_builders.functions.hours_ago import HoursAgoFunction
from caasm_aql.query_builders.functions.time_ago import TimeAgoFunction
from caasm_aql.query_builders.fuzzy_provider import FuzzyProviderManager
from caasm_aql.query_builders.method import MethodManager
from caasm_aql.query_builders.operator import OperatorManager


class QueryBuilderManager(object):
    _FUNCTION_HANDLERS = [DaysAgoFunction, HoursAgoFunction, TimeAgoFunction]
    _CONVERT_HANDLERS = [DateConverter, DatetimeConverter, StringConverter, EnumConverter, NumberConverter,
                         BooleanConverter]
    _METHOD_HANDLERS = [
        ExistsMethod,
        InMethod,
        StartsMethod,
        EndsMethod,
        RegexMethod,
        MatchMethod,
        SizeGreaterThanMethod,
        SizeGreaterThanEqualMethod,
        SizeLesserThanMethod,
        SizeLesserThanEqualMethod,
    ]
    _OPERATE_HANDLERS = [
        EqualOperator, NotEqualOperator, IPv4EqualOperator, IPV6EqualOperator, IPEqualOperator, GTOperator, GTEOperator,
        LTOperator, LTEOperator, EnumEqualOperator, EnumNotEqualOperator, VersionEqualOperator, VersionNotEqualOperator,
        VersionGTOperator, VersionGTEOperator, VersionLTOperator, VersionLTEOperator, RelationEqualOperator
    ]

    def __init__(self):
        self._function_manager = FunctionManager()
        self._converter_manager = ConverterManager()
        self._operator_manager = OperatorManager()
        self._fuzzy_provider_manager = FuzzyProviderManager()
        self._method_manager = MethodManager()
        self._register()

    def _register(self):
        self.__register_core(self._function_manager, self._FUNCTION_HANDLERS)
        self.__register_core(self._converter_manager, self._CONVERT_HANDLERS)
        self.__register_core(self._operator_manager, self._OPERATE_HANDLERS)
        self.__register_core(self._function_manager, self._FUNCTION_HANDLERS)
        self.__register_core(self._method_manager, self._METHOD_HANDLERS)

    @classmethod
    def __register_core(cls, manager_, handlers):
        for _handler in handlers:
            manager_.register(_handler())

    @property
    def method_manager(self):
        return self._method_manager

    @property
    def function_manager(self):
        return self._function_manager

    @property
    def converter_manager(self):
        return self._converter_manager

    @property
    def operator_manager(self):
        return self._operator_manager

    @property
    def fuzzy_provider_manager(self):
        return self._fuzzy_provider_manager


query_builder_manager = QueryBuilderManager()
