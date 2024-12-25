from enum import Enum
from io import StringIO
from typing import List, Optional

from caasm_aql.asql_field import AqlFieldTarget, AsqlFieldLogicQuery
from caasm_aql.base import AsqlPlusType, AqlLogicalGroup, AqlGroupItem, AsqlType, AqlQueryBase, \
    AqlLogicalCall, AqlTargetItem, AqlCall, AqlSimpleExpression, \
    AqlTarget, AqlTargetType, AqlInventoryTarget, AqlLogicalOperand

AQL_TYPES = [i.value for i in list(AsqlType.__members__.values())]


class AqlAdapterTarget(AqlTarget):
    def __init__(self):
        super(AqlAdapterTarget, self).__init__(AqlTargetType.ADAPTER)
        self.adapter_dataset: Optional[str] = None


class AqlInventoryExpression(AqlSimpleExpression):
    def __init__(self):
        self.target: AqlInventoryTarget = AqlInventoryTarget()
        super(AqlInventoryExpression, self).__init__(self.target)


class AqlAdapterExpression(AqlSimpleExpression):
    def __init__(self):
        self.target: AqlAdapterTarget = AqlAdapterTarget()
        super(AqlAdapterExpression, self).__init__(self.target)


class AqlLogicQuery(AsqlFieldLogicQuery):
    def __init__(self):
        super(AqlLogicQuery, self).__init__()
        self.logical_group: Optional[AqlLogicalGroup] = None

    def _convert_call(self, call: AqlCall):
        if isinstance(call, AqlLogicalCall):
            buffer = StringIO()
            logical_call: AqlLogicalCall = call
            buffer.write(".")
            buffer.write("(")
            buffer.write(self._convert_logical_group(logical_call.logical_group))
            buffer.write(")")
            buffer.seek(0)
            return buffer.read()
        else:
            return super(AqlLogicQuery, self)._convert_call(call)

    def _convert_logical_group(self, logical_group: AqlLogicalGroup):
        asql_list = list()
        if logical_group.not_boolean:
            asql_list.append("not")
        operand_list = list()
        buffer = StringIO()
        if logical_group.not_boolean and len(logical_group.items) > 1:
            buffer.write("(")
        for item in logical_group.items:
            if isinstance(item, AqlTargetItem):
                operand_list.append(self._convert_target_item(item))
            elif isinstance(item, AqlGroupItem):
                operand_list.append(self._convert_logical_group(item.group))
        buffer.write(f" {logical_group.operand.value} ".join(operand_list))
        if logical_group.not_boolean and len(logical_group.items) > 1:
            buffer.write(")")
        buffer.seek(0)
        asql_list.append(buffer.read())
        return " ".join(asql_list)

    def _convert_target_item(self, target_item: AqlTargetItem):
        target = target_item.target
        field_name: str = target.field_name
        buffer = StringIO()
        if isinstance(target, AqlInventoryTarget):
            buffer.write("$.")
            buffer.write(field_name)
        elif isinstance(target, AqlAdapterTarget):
            buffer.write("@.")
            buffer.write(target.adapter_dataset)
            buffer.write(".")
            buffer.write(field_name)
        elif isinstance(target, AqlFieldTarget):
            buffer.write(target.field_name)
        buffer.write(self._convert_call(target.call))
        buffer.seek(0)
        return buffer.read()

    def to_asql(self):
        if self.asql:
            return self.asql
        return self._convert_logical_group(self.logical_group)

    def to_dict(self, field_mapper=None):
        return {
            "type": AsqlType.ASQL,
            "asql": self.to_asql(),
            "text": self.to_asql()
        }

    def is_empty(self):
        return not self.expression and not self.logical_group


class AqlQuery(AqlQueryBase):
    def __init__(self):
        AqlQueryBase.__init__(self, AsqlPlusType.ASQL)

    def is_valid(self):
        return self.expression is not None

    def to_logical_group(self) -> Optional[AqlLogicalGroup]:
        logical_group_chain = list()
        logical_group: AqlLogicalGroup = AqlLogicalGroup()
        # logical_group.operand = AqlLogicalOperand.AND
        logical_group_chain.append(logical_group)
        self._convert_expression(self.expression, logical_group_chain)
        if logical_group_chain:
            logical_group = logical_group_chain[0]
            if logical_group.operand is None:
                logical_group.operand = AqlLogicalOperand.AND
            if logical_group.not_boolean is None:
                logical_group.not_boolean = False
            self._simplify_groups(logical_group)
            return logical_group
        else:
            return None

    def to_logic_query(self) -> Optional[AqlLogicQuery]:
        logical_group_query = AqlLogicQuery()
        logical_group = self.to_logical_group()
        if logical_group:
            logical_group_query.logical_group = logical_group
            return logical_group_query
        else:
            return None


class AqlSorting(Enum):
    ASC = "asc"
    DESC = "desc"


class AqlFieldSorting:
    def __init__(self):
        self.field_name: [str, None] = None
        self.sorting: AqlSorting = AqlSorting.ASC


class AsqlOption:
    def __init__(self):
        self.field_list: list = list()
        self.field_sorting_list: List[AqlFieldSorting] = list()
        self.entity_type: str = None
        self.page_size: int = 20
        self.page_index: int = 1
        self.limit: int = None


class AqlAddition:
    def __init__(self):
        self.field: str = None
        self.value = None


class ChildRetrieve:
    def __int__(self):
        self.field: str = None
        self.aql: str = None
        self.keyword: str = None


class AqlRelatedEntityOption:
    def __init__(self):
        self.parent_category = None
        self.entity_id = None
        self.field = None
        self.field_names = None
