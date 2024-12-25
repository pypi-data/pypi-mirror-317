from typing import Optional

from antlr4 import ParserRuleContext

from caasm_aql.aql import (
    AqlInventoryExpression,
    AqlAdapterExpression,
    AqlLogicQuery, AqlQuery, )
from caasm_aql.aql_antlr4.AqlParser import AqlParser
from caasm_aql.asql_field import AqlResolveContextBase, AqlSimpleFieldExpression, AsqlFieldResolver
from caasm_aql.base import AqlLogicalOperand, AsqlType, AqlQueryBase, \
    AqlComplexExpression, AqlExpressionCall, AqlExpressionType, AqlValueType, AqlValue, AqlExpression


class AqlResolveContext(AqlResolveContextBase):
    def __init__(self):
        super(AqlResolveContext, self).__init__()
        self.query: AqlQueryBase = AqlQuery()


class AqlResolver(AsqlFieldResolver):
    def __init__(self, type_: AsqlType = AsqlType.ASQL):
        super(AqlResolver, self).__init__(type_)
        self._context_stack = None

    def _get_context(self) -> AqlResolveContext:
        return self._context_stack[-1]

    def resolve_logic_query(self, aql: str) -> Optional[AqlLogicQuery]:
        expression_query: AqlQueryBase = self.resolve(aql)
        logical_group_query = AqlLogicQuery()
        logical_group = expression_query.to_logical_group()
        if logical_group:
            logical_group_query.logical_group = logical_group
            return logical_group_query
        else:
            return None

    def _init(self):
        self._context_stack = list()
        self._context_stack.append(AqlResolveContext())

    def _get_parser(self, stream):
        return AqlParser(stream)

    def _get_parser_root(self, parser):
        return parser.aql()

    def _get_result(self):
        return self._get_context().query

    def _visit(self, tree):
        self.visit(tree)

    def _fill_complex_expression(self, expression):
        if self._get_context().expr_stack:
            expression_in_stack: AqlExpression = self._get_context().expr_stack[-1]
            if expression_in_stack.aql_expression_type == AqlExpressionType.COMPLEX and isinstance(
                expression_in_stack, AqlComplexExpression
            ):
                complex_expression: AqlComplexExpression = expression_in_stack
                if complex_expression.left is None:
                    complex_expression.left = expression
                else:
                    complex_expression.right = expression

    def visitExpr(self, ctx: AqlParser.ExprContext):
        if len(ctx.children) == 3:
            if isinstance(ctx.children[0], AqlParser.ExprContext):
                complex_expression = AqlComplexExpression()
                if self._get_context().not_boolean:
                    complex_expression.not_boolean = True
                    self._get_context().not_boolean = False
                self._fill_complex_expression(complex_expression)
                self._get_context().expr_stack.append(complex_expression)
                self._get_context().current_expr = complex_expression
                result = super(AqlResolver, self).visitExpr(ctx)
                if len(self._get_context().expr_stack) == 1:
                    self._get_context().query.expression = self._get_context().expr_stack[0]
                self._get_context().expr_stack.pop()
            else:
                result = super(AqlResolver, self).visitExpr(ctx)
        else:
            result = super(AqlResolver, self).visitExpr(ctx)
        return result

    def _process_field_expr(self, ctx: ParserRuleContext, super_method):
        if len(ctx.children) == 3:
            if isinstance(ctx.children[0], AqlParser.FieldExprContext):
                complex_expression = AqlComplexExpression()
                if self._get_context().not_boolean:
                    complex_expression.not_boolean = True
                    self._get_context().not_boolean = False
                self._fill_complex_expression(complex_expression)
                self._get_context().expr_stack.append(complex_expression)
                self._get_context().current_expr = complex_expression
                result = super_method(ctx)
                if len(self._get_context().expr_stack) == 1:
                    self._get_context().query.expression = self._get_context().expr_stack[0]
                self._get_context().expr_stack.pop()
            else:
                result = super_method(ctx)
        else:
            result = super_method(ctx)
        return result

    def visitFieldExpr(self, ctx: AqlParser.FieldExprContext):
        return self._process_field_expr(ctx, super(AqlResolver, self).visitFieldExpr)

    def visitGraphElementExpr(self, ctx: AqlParser.GraphElementExprContext):
        if self.type != AsqlType.ASGL:
            raise
        return self._process_field_expr(ctx, super(AqlResolver, self).visitGraphElementExpr)

    def visitInventoryExpr(self, ctx: AqlParser.InventoryExprContext):
        if self.type != AsqlType.ASQL:
            raise
        inventory_expression = AqlInventoryExpression()
        if self._get_context().not_boolean:
            inventory_expression.not_boolean = True
            self._get_context().not_boolean = False
        self._get_context().current_expr = inventory_expression
        self._fill_complex_expression(inventory_expression)
        result = super(AqlResolver, self).visitInventoryExpr(ctx)
        self._get_context().current_expr = None
        if not self._get_context().expr_stack:
            self._get_context().query.expression = inventory_expression
        return result

    def visitAdapterExpr(self, ctx: AqlParser.AdapterExprContext):
        if self.type != AsqlType.ASQL:
            raise
        adapter_expression = AqlAdapterExpression()
        if self._get_context().not_boolean:
            adapter_expression.not_boolean = True
            self._get_context().not_boolean = False
        self._get_context().current_expr = adapter_expression
        self._fill_complex_expression(adapter_expression)
        result = super(AqlResolver, self).visitAdapterExpr(ctx)
        self._get_context().current_expr = None
        if not self._get_context().expr_stack:
            self._get_context().query.expression = adapter_expression
        return result

    # def visitGraphElementName(self, ctx: AqlParser.GraphElementNameContext):
    #     graph_element_expression: AqlGraphElementExpression = self._get_context().current_expr
    #     graph_element_expression.target.element_name = ctx.getText()
    #     return super(AqlResolver, self).visitGraphElementName(ctx)

    def visitNotBoolean(self, ctx: AqlParser.NotBooleanContext):
        self._get_context().not_boolean = True
        return super(AqlResolver, self).visitNotBoolean(ctx)

    def visitAdapterDataset(self, ctx: AqlParser.AdapterDatasetContext):
        adapter_expression: AqlAdapterExpression = self._get_context().current_expr
        adapter_expression.target.adapter_dataset = ctx.getText()
        return super(AqlResolver, self).visitAdapterDataset(ctx)

    def visitFieldAql(self, ctx: AqlParser.FieldAqlContext):
        field_expression: AqlSimpleFieldExpression = self._get_context().current_expr
        call: AqlExpressionCall = self._get_context().value_stack[-1]
        field_expression.target.call = call
        context = AqlResolveContext()
        self._context_stack.append(context)
        result = super(AqlResolver, self).visitFieldAql(ctx)
        self._context_stack.pop()
        call.query = context.query
        return result

    def visitExpressionCall(self, ctx: AqlParser.ExpressionCallContext):
        call = AqlExpressionCall()
        call.query = AqlQuery()
        self._get_context().value_stack.append(call)
        result = super(AqlResolver, self).visitExpressionCall(ctx)
        return result

    # def _visit_value(self, value):
    #     dataset_expression: AqlExpression = self._current_expr
    #     call: AqlCall = dataset_expression.call
    #     if call.call_type == AqlCallType.OPERATOR:
    #         call: AqlOperatorCall = call
    #         call.value = value
    #     else:
    #         call: AqlMethodCall = call
    #         if self._is_list:
    #             value_list = call.param_list[-1]
    #         else:
    #             value_list = call.param_list
    #         value_list.append(value)

    def visitFieldTypeName(self, ctx: AqlParser.FieldTypeNameContext):
        vv = ctx.getText()
        self._push_value(AqlValue(AqlValueType.FIELD, vv))
        return super(AqlResolver, self).visitFieldTypeName(ctx)

    # def visitListType(self, ctx: AqlParser.ListTypeContext):
    #     dataset_expression: AqlExpression = self._current_expr
    #     call: AqlCall = dataset_expression.call
    #     if call.call_type == AqlCallType.OPERATOR:
    #         call: AqlOperatorCall = call
    #         call.value = list()
    #         result = super(AqlResolver, self).visitListType(ctx)
    #     else:
    #         call: AqlMethodCall = call
    #         call.param_list.append(list())
    #         self._is_list = True
    #         result = super(AqlResolver, self).visitListType(ctx)
    #         self._is_list = False
    #     return result

    def visitAndBoolean(self, ctx: AqlParser.AndBooleanContext):
        expression: AqlComplexExpression = self._get_context().expr_stack[-1]
        expression.operand = AqlLogicalOperand.AND
        return super(AqlResolver, self).visitAndBoolean(ctx)

    def visitOrBoolean(self, ctx: AqlParser.OrBooleanContext):
        expression: AqlComplexExpression = self._get_context().expr_stack[-1]
        expression.operand = AqlLogicalOperand.OR
        return super(AqlResolver, self).visitOrBoolean(ctx)


if __name__ == "__main__":
    resolver = AqlResolver()
    aa = resolver.resolve("$.def = a() and $.bb = 1 or $.dd.(c=1 and d.ba())")
    bb = aa.to_logical_group()
    dd = 1
