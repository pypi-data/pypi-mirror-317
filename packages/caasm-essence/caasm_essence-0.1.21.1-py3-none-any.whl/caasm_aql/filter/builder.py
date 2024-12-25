from timeit import timeit
from typing import List

from caasm_aql.asql_plus import AsqlPlusLogicalQuery, AsqlPlusResolver
from caasm_aql.base import AqlLogicalOperand, AqlItem, AqlItemType, AqlTargetItem, AqlTargetType, AqlCallType, \
    AqlOperatorCall, AqlGroupItem, AqlMethodCall, AqlValueType, AqlValue, AqlLogicalCall, AqlLogicalGroup
from caasm_aql.filter.filters.group import GroupFilter
from caasm_aql.filter.filters.method import MethodFilter
from caasm_aql.filter.filters.op import OpFilter
from caasm_aql.filter.method_manager import method_manager
from caasm_aql.filter.op_manager import op_manager
from caasm_render.query.base import BaseQuery
from caasm_service.runtime import variable_service, entity_service


class AsqlFilterBuilder(BaseQuery):
    def __init__(self):
        self._meta_fields = None

    def build(self, category, asql, entity_type=None):
        self._meta_fields = self.find_field_to_mapper(category, entity_type=entity_type)

        resolver: AsqlPlusResolver = AsqlPlusResolver(as_fulltext=False)
        query: AsqlPlusLogicalQuery = resolver.resolve_logic_query(asql)
        root = GroupFilter()
        root.logical_op = AqlLogicalOperand.AND
        for q in query.queries:
            root.filters.append(self._build_logical_group(q.logical_group))
        return root

    def _build_logical_group(self, logical_group: AqlLogicalGroup, parent_field_name=None):
        filter_ = GroupFilter()
        filter_.logical_op = logical_group.operand
        filter_.not_boolean = logical_group.not_boolean
        for item in logical_group.items:
            self._build_item(filter_, item, parent_field_name)
        return filter_

    def _build_item(self, group_filter: GroupFilter, item: AqlItem, parent_field_name=None):
        if item.item_type == AqlItemType.TARGET:
            item: AqlTargetItem = item
            target = item.target
            call = target.call
            if target.target_type == AqlTargetType.FIELD or target.target_type == AqlTargetType.INVENTORY:
                if call.call_type == AqlCallType.OPERATOR:
                    call: AqlOperatorCall = call
                    op_filter = OpFilter()
                    op_cls = op_manager.get_op_cls(call.operator)
                    if op_cls is None:
                        raise NotImplementedError(f"名称为：{call.operator}的操作符未实现")
                    op = op_cls()
                    op.value = self._extract_value(call.value)
                    op_filter.op = op
                    op_filter.set_meta_field(target.field_name, self._meta_fields, parent_field_name)
                    group_filter.filters.append(op_filter)
                elif call.call_type == AqlCallType.METHOD:
                    call: AqlMethodCall = call
                    method_filter = MethodFilter()
                    method_filter.set_meta_field(target.field_name, self._meta_fields, parent_field_name)
                    method_cls = method_manager.get_method_cls(call.method)
                    if method_cls is None:
                        raise NotImplementedError(f"名称为：{call.method}的函数未实现")
                    method = method_cls()
                    method.params = self._extract_value(call.param_list)
                    method_filter.method = method
                    group_filter.filters.append(method_filter)
                elif call.call_type == AqlCallType.LOGICAL_GROUP:
                    call: AqlLogicalCall = call
                    group_filter.filters.append(self._build_logical_group(call.logical_group, target.field_name))
                elif call.call_type == AqlCallType.EXPRESSION:
                    #   todo:
                    pass
        elif item.item_type == AqlItemType.GROUP:
            item: AqlGroupItem = item
            sub_group_filter = GroupFilter()
            sub_group_filter.not_boolean = item.group.not_boolean
            sub_group_filter.logical_op = item.group.operand
            for sub_item in item.group.items:
                self._build_item(sub_group_filter, sub_item)
            group_filter.filters.append(sub_group_filter)
        elif item.item_type == AqlItemType.FULLTEXT:
            raise NotImplementedError(f"不支持全文检索")
        elif item.item_type == AqlItemType.BATCH:
            raise NotImplementedError(f"不支持批量检索")

    def _extract_value(self, value):
        if isinstance(value, List):
            result = []
            for v in value:
                result.append(self._extract_value(v))
            return result
        elif isinstance(value, AqlValue):
            if value.value_type == AqlValueType.VALUE:
                return value.value
            elif value.value_type == AqlValueType.VARIABLE:
                v = variable_service.get_aql_variable(value.value)
                if v is None:
                    raise ValueError(f"名称为{value.value}的变量不存在")
                return v.data_value
            else:
                raise NotImplementedError("暂不支持字段比较")


asql_filter_builder = AsqlFilterBuilder()

if __name__ == "__main__":
    filter__ = asql_filter_builder.build(
        "asset",
        "$.network.ports.(number = 1000 and ip = '10.2.3.4') and $.base.asset_type = 'host' and $.computer.host_name.match('abc') and $.network.ips.addr.starts('10.2.')"
    )
    # data = {"base": {"asset_type": "host"}, "computer": {"host_name": "ABC"}}
    data = entity_service.get_entity("asset", "base.entity_id", "bc56e0f87f0198388e98b4f7f7253101")
    print(filter__.filter(data))
    print(timeit(lambda: filter__.filter(data), number=100000))
