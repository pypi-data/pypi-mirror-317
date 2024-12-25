from caasm_aql.asql_batch import AsqlBatchItem
from caasm_aql.asql_field import AqlFunction
from caasm_aql.base import AqlValueType, AqlOperatorCall, AqlMethodCall, AqlValue, AqlOperator, \
    AqlTargetType
from caasm_aql.entity_id_field_name_getter import EntityIDFieldNameGetter
from caasm_aql.field_data_type_getter import FieldDataTypeGetter
from caasm_aql.query_builders.converter import Converter
from caasm_aql.query_builders.function import Function
from caasm_aql.query_builders.method import Method
from caasm_aql.query_builders.operator import Operator
from caasm_aql.query_builders.runtime import query_builder_manager
from caasm_variable.converter import convert_variable
from caasm_variable.service.entity.variable import Variable
from caasm_variable.service.runtime import variable_service


class BaseBackend(object):
    _COMPARISON_MAPPING = {}
    _LOGICAL_MAPPING = {}

    def __init__(self, logical_model):
        self.field_data_type_getter = FieldDataTypeGetter(logical_model)
        self.entity_id_field_name_getter = EntityIDFieldNameGetter(logical_model)
        self.errors = list()
        self.variable_manager = variable_service

    def _process_batch_item(self, item, final_query, high_lights, parent_field=None):
        item: AsqlBatchItem = item
        queries = []
        if item.op == "=":
            sub_call = AqlOperatorCall()
            sub_call.operator = AqlOperator.EQUAL
        else:
            sub_call = AqlMethodCall()
            sub_call.method = item.op
        if "*" in item.fields:
            for keyword in item.keywords:
                query = {"multi_match": {"query": keyword, "fields": ["*"]}}
                queries.append(query)
        else:
            for field_name in item.fields:
                for keyword in item.keywords:
                    if item.op == "=":
                        query = {}
                        sub_call.value = AqlValue(AqlValueType.VALUE, keyword)
                        self._process_operator_call(
                            sub_call, field_name, query, None, high_lights, parent_field
                        )
                        if query:
                            queries.append(query)
                    else:
                        query = {}
                        sub_call.param_list = [AqlValue(AqlValueType.VALUE, keyword)]
                        self._process_method_call(
                            sub_call, field_name, query, AqlTargetType.INVENTORY, high_lights, parent_field
                        )
                        if query:
                            queries.append(query)
        final_query.update(
            {
                "bool": {
                    "should": queries
                }
            }
        )

    def _process_method_call(self, call, field_name, final_query, target_type, high_lights, parent_field=None):
        call: AqlMethodCall = call
        call.param_list = self._convert_value(call.param_list)

        full_field_name = f"{parent_field}.{field_name}" if parent_field else field_name
        meta_field = self.field_data_type_getter.get_data_type(full_field_name)
        if meta_field is None:
            self.errors.append(f"指定的字段{full_field_name}不存在")
            return
        method: Method = query_builder_manager.method_manager.get(meta_field.type, call.method)
        if method is None:
            self.errors.append(f"指定的函数{call.method}不存在或与该字段类型不匹配")
            return
        if method.order != len(call.param_list) + 1:
            raise ValueError(f"函数参数数量错误: {method.name}")
        #   根据参数类型进行转换
        for index, param_type in enumerate(method.get_param_types[1:]):
            converter: Converter = query_builder_manager.converter_manager.get(param_type)
            call.param_list[index] = converter.convert(call.param_list[index], meta_field)
        q = method.build(meta_field, call, target_type)
        if q:
            final_query.update(q)
        _high_light_result = method.get_high_light(meta_field, call)
        high_lights.append(_high_light_result) if _high_light_result else ...

    def _process_operator_call(
        self, call, field_name, condition, query_field_name, high_lights, parent_field=None
    ):
        call: AqlOperatorCall = call
        value_type = call.value.value_type
        if call.value.value_type != AqlValueType.FIELD:
            call.value = self._convert_value(call.value)
        if parent_field:
            full_field_name = f"{parent_field}.{field_name}"
        else:
            full_field_name = field_name
        meta_field = self.field_data_type_getter.get_data_type(full_field_name)
        if meta_field is None:
            raise ValueError(f"字段不存在{full_field_name}")
            # op: Operator = None
            # converter: Converter = None
        else:
            op: Operator = query_builder_manager.operator_manager.get(meta_field.type, call.operator)
            converter: Converter = query_builder_manager.converter_manager.get(meta_field.type)
        if converter:
            if value_type != AqlValueType.FIELD:
                call.value = converter.convert(call.value, meta_field)
        if op:
            if value_type == AqlValueType.FIELD:
                if parent_field:
                    compare_full_field_name = f"{parent_field}.{call.value.value}"
                else:
                    compare_full_field_name = call.value.value
                compare_field = self.field_data_type_getter.get_data_type(compare_full_field_name)
                if compare_field:
                    result, is_default = op.build_field_compare_result(meta_field, compare_field)
                else:
                    raise ValueError(f"要比较的字段不存在{compare_full_field_name}")
                _high_light_result = None
            else:
                result, is_default = op.build(meta_field, call)
                _high_light_result = op.get_high_light(meta_field, call)
            if result:
                if is_default:
                    condition[query_field_name] = result
                else:
                    condition.update(result)
                high_lights.append(_high_light_result) if _high_light_result else ...
        else:
            _op = self._COMPARISON_MAPPING.get(call.operator)
            if not _op:
                raise ValueError(f"未知操作符{call.operator}")
            condition[query_field_name] = {self._COMPARISON_MAPPING[call.operator]: call.value}

    def _convert_value(self, value):
        if self.errors:
            return value
        if isinstance(value, AqlValue):
            if value.value_type == AqlValueType.VALUE:
                value = value.value
            elif value.value_type == AqlValueType.FIELD:
                value = value.value
            else:
                try:
                    variable: Variable = self.variable_manager.get_aql_variable(value.value)
                    value = convert_variable(variable)
                except (ValueError, AttributeError):
                    self.errors.append(f'变量{value.value}类型转换错误')
                except Exception as ex:
                    self.errors.append(f"未找到变量{value.value}，请检查变量配置")
        if isinstance(value, list):
            for index, item in enumerate(value):
                value[index] = self._convert_value(item)
        if isinstance(value, AqlFunction):
            aql_function: AqlFunction = value
            function: Function = query_builder_manager.function_manager.get(aql_function.function)
            if function is None:
                self.errors.append(f"未找到函数{aql_function.function}，请检查函数名称")
                return
            if function.order != len(aql_function.param_list):
                self.errors.append(f"函数{aql_function.function}参数数量错误")
            aql_function.param_list = self._convert_value(aql_function.param_list)
            return function.call(aql_function.param_list)
        return value
