from abc import ABC
from enum import Enum
from io import StringIO
from typing import List, Optional

from antlr4 import InputStream, CommonTokenStream
from antlr4.tree.Tree import ParseTree

from caasm_aql.aql_error import AqlErrorListener
from caasm_tool.constants import StrEnum


class AsqlPlusType(StrEnum):
    ASQL = "asql"
    FIELD = "field"
    FULLTEXT = 'fulltext'
    BATCH = 'batch'


class AqlOperator(Enum):
    EQUAL = "="
    GREATER = ">"
    LESS = "<"
    GREATER_OR_EQUAL = ">="
    LESS_OR_EQUAL = "<="
    NOT_EQUAL = "!="


class AqlLogicalOperand(Enum):
    AND = "and"
    OR = "or"


class AqlItemType(Enum):
    GROUP = "group"
    TARGET = "target"
    FULLTEXT = "fulltext"
    BATCH = "batch"


class AsqlType(StrEnum):
    ASQL = 'asql'
    ASGL = 'asgl'
    FIELD = 'field'
    FULLTEXT = 'fulltext'
    BATCH = "batch"
    ASQL_PLUS = 'asql_plus'


class AqlExpressionType(Enum):
    SIMPLE = "simple"
    COMPLEX = "complex"


class AqlTargetType(Enum):
    INVENTORY = "inventory"
    ADAPTER = "adapter"
    FIELD = "field"


class AqlCallType(Enum):
    OPERATOR = "operator"
    METHOD = "method"
    EXPRESSION = "expression"
    LOGICAL_GROUP = "group"
    BATCH = "batch"


class AqlValueType(Enum):
    VALUE = "value"
    VARIABLE = "variable"
    FIELD = 'field'


class AqlItem:
    def __init__(self, item_type: AqlItemType):
        self.item_type: AqlItemType = item_type


class AqlLogicalGroup:
    def __init__(self):
        self.items: List[AqlItem] = list()
        self.operand: Optional[AqlLogicalOperand] = None
        self.not_boolean: Optional[bool] = None

    @staticmethod
    def merge(groups: List["AqlLogicalGroup"]):
        logical_group = AqlLogicalGroup()
        logical_group.not_boolean = False
        logical_group.operand = AqlLogicalOperand.AND
        for group in groups:
            item = AqlGroupItem()
            item.group = group
            logical_group.items.append(item)
        return logical_group


class AsqlLogicalQueryBase:
    def __init__(self):
        self.asql: Optional[str] = None
        self.logical_group: AqlLogicalGroup = None

    def to_asql(self):
        raise NotImplementedError()

    def to_dict(self, field_mapper=None):
        raise NotImplementedError()

    @staticmethod
    def from_dict(asql_item):
        return asql_item["asql"]

    def is_empty(self):
        return not self.asql and not self.logical_group


class AsqlPlusQueryBase:
    def __init__(self, type_: AsqlPlusType):
        self._type: AsqlPlusType = type_

    def to_logical_group(self) -> Optional[AqlLogicalGroup]:
        raise NotImplementedError()

    def to_logic_query(self) -> Optional[AsqlLogicalQueryBase]:
        raise NotImplementedError()

    def is_valid(self):
        return True

    def errors(self):
        return None


class AqlGroupItem(AqlItem):
    def __init__(self):
        super(AqlGroupItem, self).__init__(AqlItemType.GROUP)
        self.group: AqlLogicalGroup = AqlLogicalGroup()


class AqlValue:
    def __init__(self, value_type: AqlValueType, value):
        self.value_type: AqlValueType = value_type
        self.value = value

    def serialize(self, buffer=None):
        should_return = False
        if not buffer:
            buffer = StringIO()
            should_return = True
        if self.value_type == AqlValueType.VALUE:
            if isinstance(self.value, List):
                values = []
                buffer.write("[")
                for item in self.value:
                    if isinstance(item, AqlValue):
                        values.append(item.serialize())
                    else:
                        values.append(f"'{item}'" if isinstance(item, str) else item)
                buffer.write(", ".join(values))
                buffer.write("]")
            elif isinstance(self.value, str):
                buffer.write("'")
                buffer.write(self.value)
                buffer.write("'")
            else:
                buffer.write(str(self.value))
        elif self.value_type == AqlValueType.FIELD:
            buffer.write('$.')
            buffer.write(self.value)
        else:
            if isinstance(self.value, List):
                variables = []
                for item in self.value:
                    variables.append(f"%{item}")
                buffer.write("[")
                buffer.write(",".join(variables))
                buffer.write("]")
            else:
                buffer.write("%")
                buffer.write(self.value)
        if should_return:
            buffer.seek(0)
            return buffer.read()


class AqlTarget:
    def __init__(self, target_type: AqlTargetType):
        self.target_type: AqlTargetType = target_type
        self.field_name: Optional[str] = None
        self.call: Optional[AqlCall] = None


class AqlExpression:
    def __init__(self, aql_expression_type: AqlExpressionType):
        self.aql_expression_type: AqlExpressionType = aql_expression_type
        self.not_boolean = False


class AqlComplexExpression(AqlExpression):
    def __init__(self):
        super(AqlComplexExpression, self).__init__(AqlExpressionType.COMPLEX)
        self.operand: [AqlLogicalOperand, None] = None
        self.left: Optional[AqlExpression] = None
        self.right: Optional[AqlExpression] = None


class AqlCall:
    def __init__(self, call_type: AqlCallType):
        self.call_type: AqlCallType = call_type


class AqlLogicalCall(AqlCall):
    def __init__(self):
        super(AqlLogicalCall, self).__init__(AqlCallType.LOGICAL_GROUP)
        self.logical_group: Optional[AqlLogicalGroup] = None


class AqlExpressionCall(AqlCall):
    def __init__(self):
        super(AqlExpressionCall, self).__init__(AqlCallType.EXPRESSION)
        self.query: AqlQueryBase = None


class AqlTargetItem(AqlItem):
    def __init__(self):
        super(AqlTargetItem, self).__init__(AqlItemType.TARGET)
        self.target: AqlTarget = None


class AqlOperatorCall(AqlCall):
    def __init__(self):
        super(AqlOperatorCall, self).__init__(AqlCallType.OPERATOR)
        self.operator: [AqlOperator, None] = None
        self.value: Optional[AqlValue] = None


class AqlMethodCall(AqlCall):
    def __init__(self):
        super(AqlMethodCall, self).__init__(AqlCallType.METHOD)
        self.method: [str, None] = None
        self.param_list: List[AqlValue] = list()


class AqlSimpleExpression(AqlExpression):
    def __init__(self, target: AqlTarget):
        super(AqlSimpleExpression, self).__init__(AqlExpressionType.SIMPLE)
        self.target: AqlTarget = target


class AqlResolveContextBase:
    def __init__(self):
        self.expr_stack: list = list()
        self.current_expr: Optional[AqlExpression] = None
        self.value_stack = list()
        self.not_boolean: bool = False


class AqlQueryBase(AsqlPlusQueryBase, ABC):
    def __init__(self, type_: AsqlPlusType):
        super(AqlQueryBase, self).__init__(type_)
        self.expression: [AqlExpression, None] = None

    def _convert_target(self, target: AqlTarget):
        target.call = self._convert_call(target.call)
        target_item: AqlTargetItem = AqlTargetItem()
        target_item.target = target
        return target_item

    def _convert_call(self, call: AqlCall):
        if call.call_type == AqlCallType.EXPRESSION:
            expression_call: AqlExpressionCall = call
            field_logical_group_call: AqlLogicalCall = AqlLogicalCall()
            field_logical_group_call.logical_group = expression_call.query.to_logical_group()
            return field_logical_group_call
        else:
            return call

    def _convert_expression(
            self,
            expression: AqlExpression,
            logical_group_chain: list,
            upper_operand: Optional[AqlLogicalOperand] = None,
    ):
        if logical_group_chain:
            logical_group = logical_group_chain[-1]
        else:
            logical_group = None
        if expression.aql_expression_type == AqlExpressionType.SIMPLE:
            simple_expression: AqlSimpleExpression = expression
            created = False
            if logical_group is None:
                logical_group: AqlLogicalGroup = AqlLogicalGroup()
                logical_group.operand = AqlLogicalOperand.AND
                logical_group.not_boolean = expression.not_boolean
                logical_group_chain.append(logical_group)
                created = True
            elif logical_group.items:
                if upper_operand != logical_group.operand or simple_expression.not_boolean:
                    item = AqlGroupItem()
                    item.group.operand = AqlLogicalOperand.AND
                    item.group.not_boolean = expression.not_boolean
                    logical_group.items.append(item)
                    logical_group_chain.append(item.group)
                    logical_group = item.group
                    created = True
            elif logical_group.not_boolean is False and simple_expression.not_boolean is True:
                item = AqlGroupItem()
                item.group.operand = AqlLogicalOperand.AND
                item.group.not_boolean = True
                logical_group.items.append(item)
                logical_group_chain.append(item.group)
                logical_group = item.group
                created = True
            else:
                if logical_group.not_boolean is None:
                    logical_group.not_boolean = expression.not_boolean
            logical_group.items.append(self._convert_target(simple_expression.target))
            if created:
                logical_group_chain.pop()
        else:
            complex_expression: AqlComplexExpression = expression
            created = False
            if logical_group is None:
                logical_group: AqlLogicalGroup = AqlLogicalGroup()
                logical_group.operand = complex_expression.operand
                logical_group.not_boolean = expression.not_boolean
                logical_group_chain.append(logical_group)
                created = True
            elif logical_group.not_boolean is not None or logical_group.items:
                if complex_expression.operand != logical_group.operand or complex_expression.not_boolean:
                    item = AqlGroupItem()
                    item.group.operand = complex_expression.operand
                    item.group.not_boolean = expression.not_boolean
                    logical_group.items.append(item)
                    logical_group_chain.append(item.group)
                    created = True
            else:
                if logical_group.not_boolean is None:
                    logical_group.not_boolean = expression.not_boolean
                if logical_group.operand is None:
                    logical_group.operand = complex_expression.operand
            self._convert_expression(complex_expression.left, logical_group_chain, logical_group.operand)
            self._convert_expression(complex_expression.right, logical_group_chain, logical_group.operand)
            if created:
                logical_group_chain.pop()

    def _simplify_groups(self, logical_group: AqlLogicalGroup):
        items_to_remove = list()
        for index, item in enumerate(logical_group.items):
            if isinstance(item, AqlGroupItem):
                if not item.group.items:
                    items_to_remove.append(item)
                if len(item.group.items) == 1:
                    if isinstance(item.group.items[0], AqlTargetItem):
                        if not item.group.not_boolean:
                            logical_group.items[index] = item.group.items[0]
                    else:
                        self._simplify_groups(item.group)
                else:
                    self._simplify_groups(item.group)
        for item in items_to_remove:
            logical_group.items.remove(item)


class ResolverBase:
    def resolve(self, asql: str):
        raise NotImplementedError()

    def resolve_logic_query(self, asql: str):
        raise NotImplementedError()


class Resolver(ResolverBase, ABC):
    def __init__(self, type_: AsqlType):
        self.type: AsqlType = type_

    def _init(self):
        pass

    def _get_parser(self, stream):
        raise NotImplementedError()

    def _get_parser_root(self, parser):
        raise NotImplementedError()

    def _visit(self, tree):
        raise NotImplementedError()

    def _get_result(self):
        raise NotImplementedError()

    def _get_lexer(self, stream):
        raise NotImplementedError()

    def resolve(self, asql: str):
        asql = asql or ""
        self._init()
        statement_stream = InputStream(asql)
        lexer = self._get_lexer(statement_stream)
        errors = list()
        aql_listener = AqlErrorListener(errors)
        lexer.addErrorListener(aql_listener)
        if errors:
            raise ValueError(errors)
        stream = CommonTokenStream(lexer)
        parser = self._get_parser(stream)
        parser.addErrorListener(aql_listener)
        tree: ParseTree = self._get_parser_root(parser)
        if errors:
            raise ValueError(errors)
        self._visit(tree)
        return self._get_result()


class AqlInventoryTarget(AqlTarget):
    def __init__(self):
        super(AqlInventoryTarget, self).__init__(AqlTargetType.INVENTORY)
