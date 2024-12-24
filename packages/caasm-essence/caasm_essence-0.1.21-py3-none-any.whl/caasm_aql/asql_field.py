from io import StringIO
from typing import List, Optional

from caasm_aql.aql_antlr4.AqlLexer import AqlLexer
from caasm_aql.aql_antlr4.AqlParser import AqlParser
from caasm_aql.aql_antlr4.AqlVisitor import AqlVisitor
from caasm_aql.base import AsqlPlusType, AqlQueryBase, Resolver, AsqlType, AqlOperator, AqlResolveContextBase, \
    AqlTargetType, AqlValueType, AqlOperatorCall, AqlMethodCall, AqlValue, AqlTarget, \
    AqlSimpleExpression, AsqlLogicalQueryBase, AqlCall, AqlLogicalGroup, AqlTargetItem, \
    AqlLogicalOperand
from caasm_meta_model.service.entities.meta_model import MetaField


class AqlFieldTarget(AqlTarget):
    def __init__(self):
        super(AqlFieldTarget, self).__init__(AqlTargetType.FIELD)


class AqlFunction:
    def __init__(self):
        self.function: str = None
        self.param_list: List[AqlValue] = list()


class AqlSimpleFieldExpression(AqlSimpleExpression):
    def __init__(self):
        AqlSimpleExpression.__init__(self, AqlFieldTarget())


class AsqlFieldQuery(AqlQueryBase):
    def __init__(self):
        self.expression: AqlSimpleFieldExpression = None
        super(AsqlFieldQuery, self).__init__(AsqlPlusType.FIELD)

    def to_logical_group(self) -> Optional[AqlLogicalGroup]:
        logical_group = AqlLogicalGroup()
        item = AqlTargetItem()
        item.target = self.expression.target
        logical_group.operand = AqlLogicalOperand.AND
        logical_group.items.append(item)
        logical_group.not_boolean = self.expression.not_boolean
        return logical_group

    def to_logic_query(self) -> Optional[AsqlLogicalQueryBase]:
        logical_query = AsqlFieldLogicQuery()
        logical_query.expression = self.expression
        logical_query.logical_group = self.to_logical_group()
        return logical_query


class AsqlFieldResolveContext(AqlResolveContextBase):
    def __init__(self):
        super(AsqlFieldResolveContext, self).__init__()
        self.query: AsqlFieldQuery = AsqlFieldQuery()


class AsqlFieldLogicQuery(AsqlLogicalQueryBase):
    def __init__(self):
        super(AsqlFieldLogicQuery, self).__init__()
        self.expression = None

    def _convert_call(self, call: AqlCall):
        buffer = StringIO()
        if isinstance(call, AqlOperatorCall):
            operator_call: AqlOperatorCall = call
            buffer.write(" ")
            buffer.write(operator_call.operator.value)
            buffer.write(" ")
            buffer.write(self._convert_value(operator_call.value))
        elif isinstance(call, AqlMethodCall):
            method_call: AqlMethodCall = call
            buffer.write(".")
            buffer.write(method_call.method)
            buffer.write("(")
            param_list_result = list()
            for param in method_call.param_list:
                param: AqlValue = param
                param_list_result.append(self._convert_value(param))
            buffer.write(", ".join(param_list_result))
            buffer.write(")")
        buffer.seek(0)
        return buffer.read()

    def _convert_value(self, value: AqlValue):
        buffer = StringIO()
        value.serialize(buffer)
        buffer.seek(0)
        return buffer.read()

    def to_asql(self):
        if self.expression:
            expression: AqlSimpleFieldExpression = self.expression
            target = expression.target
        elif self.logical_group:
            logical_group: AqlLogicalGroup = self.logical_group
            if len(logical_group.items) != 1:
                raise ValueError()
            item = logical_group.items[0]
            if not isinstance(item, AqlTargetItem):
                raise ValueError()
            target = item.target
        else:
            raise ValueError()
        field_name: str = target.field_name
        buffer = StringIO()
        buffer.write(field_name)
        buffer.write(self._convert_call(target.call))
        buffer.seek(0)
        return buffer.read()

    def to_dict(self, field_mapper=None):
        display_name = None
        target = None
        if field_mapper:
            if self.expression:
                expression: AqlSimpleFieldExpression = self.expression
                target = expression.target
            elif self.logical_group:
                logical_group: AqlLogicalGroup = self.logical_group
                if len(logical_group.items) != 1:
                    raise ValueError()
                item = logical_group.items[0]
                if not isinstance(item, AqlTargetItem):
                    raise ValueError()
                target = item.target
            else:
                raise ValueError()
            field_name: str = target.field_name
            field: MetaField = field_mapper.get(field_name)
            if field:
                display_name = field.full_display_name
            else:
                display_name = field_name
        return {
            "type": AsqlType.FIELD,
            "asql": self.to_asql(),
            "text": f"{display_name}{self._convert_call(target.call)}" if target else display_name
        }

    @staticmethod
    def from_dict(asql_item):
        return asql_item["asql"]

    def is_empty(self):
        return not self.expression and not self.logical_group


class AsqlFieldResolver(AqlVisitor, Resolver):
    def resolve_logic_query(self, asql: str):
        expression_query: AsqlFieldQuery = self.resolve(asql)
        logical_group_query = AsqlFieldLogicQuery()
        logical_group_query.expression = expression_query.expression
        logical_group_query.logical_group = expression_query.to_logical_group()
        return logical_group_query

    def __init__(self, type_=AsqlType.FIELD):
        super(AsqlFieldResolver, self).__init__(type_)
        self._context: AsqlFieldResolveContext = None

    def _init(self):
        self._context = AsqlFieldResolveContext()

    def _get_parser(self, stream):
        return AqlParser(stream)

    def _get_parser_root(self, parser):
        parser: AqlParser = parser
        return parser.fieldSimpleExpr()

    def _visit(self, tree):
        self.visitFieldSimpleExpr(tree)

    def _get_result(self):
        return self._context.query

    def _get_context(self):
        return self._context

    def _get_lexer(self, statement_stream):
        return AqlLexer(statement_stream)

    def _fill_complex_expression(self, expression):
        self._context.query.expression = expression

    def visitFieldSimpleExpr(self, ctx: AqlParser.FieldSimpleExprContext):
        aql_simple_field_expression = AqlSimpleFieldExpression()
        if self._get_context().not_boolean:
            aql_simple_field_expression.not_boolean = True
            self._get_context().not_boolean = False
        self._get_context().current_expr = aql_simple_field_expression
        self._fill_complex_expression(aql_simple_field_expression)
        result = super(AsqlFieldResolver, self).visitFieldSimpleExpr(ctx)
        self._get_context().current_expr = None
        if not self._get_context().expr_stack:
            self._get_context().query.expression = aql_simple_field_expression
        return result

    def visitFieldName(self, ctx: AqlParser.FieldNameContext):
        dataset_expression: AqlSimpleExpression = self._get_context().current_expr
        dataset_expression.target.field_name = ctx.getText()
        return super(AsqlFieldResolver, self).visitFieldName(ctx)

    def visitOperator(self, ctx: AqlParser.OperatorContext):
        dataset_expression: AqlSimpleExpression = self._get_context().current_expr
        dataset_expression.target.call = self._get_context().value_stack[-1]
        dataset_expression.target.call.operator = AqlOperator(ctx.getText())
        return super(AsqlFieldResolver, self).visitOperator(ctx)

    def visitOperatorCall(self, ctx: AqlParser.OperatorCallContext):
        call = AqlOperatorCall()
        self._get_context().value_stack.append(call)
        result = super(AsqlFieldResolver, self).visitOperatorCall(ctx)
        self._get_context().value_stack.pop()
        return result

    def visitMethod(self, ctx: AqlParser.MethodContext):
        dataset_expression: AqlSimpleExpression = self._get_context().current_expr
        dataset_expression.target.call = self._get_context().value_stack[-1]
        dataset_expression.target.call.method = ctx.getText()
        return super(AsqlFieldResolver, self).visitMethod(ctx)

    def visitMethodCall(self, ctx: AqlParser.MethodCallContext):
        call = AqlMethodCall()
        self._get_context().value_stack.append(call)
        result = super(AsqlFieldResolver, self).visitMethodCall(ctx)
        self._get_context().value_stack.pop()
        return result

    def _push_value(self, item):
        if not self._get_context().value_stack:
            print("插入值时没找到容器！")
            return
        value = self._get_context().value_stack[-1]
        if isinstance(value, AqlValue):
            inner_value = value.value
            if isinstance(inner_value, list):
                inner_value.append(item)
        elif isinstance(value, AqlFunction):
            function: AqlFunction = value
            function.param_list.append(item)
        elif isinstance(value, AqlMethodCall):
            call: AqlMethodCall = value
            call.param_list.append(item)
        elif isinstance(value, AqlOperatorCall):
            call: AqlOperatorCall = value
            call.value = item

    def visitTextType(self, ctx: AqlParser.TextTypeContext):
        self._push_value(AqlValue(AqlValueType.VALUE, ctx.getText().strip("'\"")))
        return super(AsqlFieldResolver, self).visitTextType(ctx)

    def visitIntType(self, ctx: AqlParser.IntTypeContext):
        self._push_value(AqlValue(AqlValueType.VALUE, int(ctx.getText())))
        return super(AsqlFieldResolver, self).visitIntType(ctx)

    def visitFloatType(self, ctx: AqlParser.FloatTypeContext):
        self._push_value(AqlValue(AqlValueType.VALUE, float(ctx.getText())))
        return super(AsqlFieldResolver, self).visitFloatType(ctx)

    def visitBooleanType(self, ctx: AqlParser.BooleanTypeContext):
        self._push_value(AqlValue(AqlValueType.VALUE, ctx.getText().lower() == "true"))
        return super(AsqlFieldResolver, self).visitBooleanType(ctx)

    def visitVariable(self, ctx: AqlParser.VariableContext):
        self._push_value(AqlValue(AqlValueType.VARIABLE, ctx.getText()))
        return super(AsqlFieldResolver, self).visitVariable(ctx)

    def visitListType(self, ctx: AqlParser.ListTypeContext):
        list_ = list()
        value = AqlValue(
            AqlValueType.VALUE,
            list_
        )
        self._get_context().value_stack.append(value)
        result = super(AsqlFieldResolver, self).visitListType(ctx)
        self._get_context().value_stack.pop()
        self._push_value(AqlValue(AqlValueType.VALUE, list_))
        return result

    def visitFunctionType(self, ctx: AqlParser.FunctionTypeContext):
        function: AqlFunction = AqlFunction()
        self._get_context().value_stack.append(function)
        result = super(AsqlFieldResolver, self).visitFunctionType(ctx)
        self._get_context().value_stack.pop()
        self._push_value(function)
        return result

    def visitFunction(self, ctx: AqlParser.FunctionContext):
        function: AqlFunction = self._get_context().value_stack[-1]
        function.function = ctx.getText()
        return super(AsqlFieldResolver, self).visitFunction(ctx)


if __name__ == "__main__":
    resolver = AsqlFieldResolver()
    aa = resolver.resolve("def = a()")
    dd = 1
    resolver = AsqlFieldResolver()
    bb = resolver.resolve_logic_query("def = 1")
    a = bb.to_asql()
    dd = 1
