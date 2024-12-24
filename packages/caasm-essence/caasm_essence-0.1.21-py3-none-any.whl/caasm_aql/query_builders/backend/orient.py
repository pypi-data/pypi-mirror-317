from typing import List

from caasm_aql.aql import AsqlOption
from caasm_aql.asgl import AsglQuery, AsglLink, AsglVertexDef, AsglEdgeDef, AsglEdgeDirection
from caasm_aql.asql_field import AqlFieldTarget
from caasm_aql.base import AqlOperator, AqlLogicalOperand, AqlComplexExpression, AqlValueType, AqlOperatorCall, \
    AqlValue, AqlSimpleExpression
from caasm_variable.converter import convert_variable
from caasm_variable.service.entity.variable import Variable
from caasm_variable.service.runtime import variable_service


class OrientGraphBuilder:
    def _build_expression(self, expression, query: AsglQuery, where_statements: List[str]):
        if isinstance(expression, AqlSimpleExpression):
            if isinstance(expression.target, AqlFieldTarget):
                if isinstance(expression.target.call, AqlOperatorCall):
                    if expression.target.call.operator == AqlOperator.EQUAL:
                        op = '='
                    elif expression.target.call.operator == AqlOperator.GREATER:
                        op = '>'
                    elif expression.target.call.operator == AqlOperator.GREATER_OR_EQUAL:
                        op = '>='
                    elif expression.target.call.operator == AqlOperator.LESS:
                        op = '<'
                    elif expression.target.call.operator == AqlOperator.LESS_OR_EQUAL:
                        op = '<='
                    else:
                        raise
                    if expression.target.call.value.value_type == AqlValueType.VALUE:
                        v = expression.target.call.value.value
                    else:
                        variable_name: str = expression.target.call.value.value
                        variable: Variable = variable_service.get_variable(name=variable_name)
                        v = convert_variable(variable)
                    if isinstance(v, str):
                        v_exp = f'"{v}"'
                    else:
                        v_exp = v
                    where_statements.append(
                        f'{expression.target.field_name}'
                        f' {op} '
                        f'{v_exp}'
                    )
        elif isinstance(expression, AqlComplexExpression):
            if expression.not_boolean:
                where_statements.append('not')
            where_statements.append('(')
            self._build_expression(expression.left, query, where_statements)
            if expression.operand == AqlLogicalOperand.AND:
                op = 'AND'
            else:
                op = 'OR'
            where_statements.append(op)
            self._build_expression(expression.right, query, where_statements)
            where_statements.append(')')

    def build(self, query: AsglQuery):
        statements = list()
        statements.append(f'MATCH ')
        links_statements = list()
        for link in query.links:
            link_statements = list()
            link: AsglLink = link
            if link.not_boolean:
                link_statements.append('NOT ')
            for element in link.elements:
                if isinstance(element, AsglVertexDef):
                    vertex_def: AsglVertexDef = element
                    vertex_statements = list()
                    vertex_statements.append(f'as:`{vertex_def.name}`')
                    if vertex_def.type:
                        vertex_statements.append(f'class:{vertex_def.type}')
                    if vertex_def.where.is_valid():
                        where_statements: List[str] = list()
                        self._build_expression(vertex_def.where.expression, query, where_statements)
                        if where_statements:
                            vertex_statements.append(
                                f'where:({" ".join(where_statements)})'
                            )
                    link_statements.append('{' + ','.join(vertex_statements) + '}')
                elif isinstance(element, AsglEdgeDef):
                    edge_statements = list()
                    edge_def: AsglEdgeDef = element
                    if edge_def.direction == AsglEdgeDirection.IN:
                        edge_statements.append('.inE')
                    elif edge_def.direction == AsglEdgeDirection.OUT:
                        edge_statements.append('.outE')
                    else:
                        edge_statements.append('.bothE')
                    edge_statements.append('(')
                    if edge_def.type:
                        edge_statements.append(f'{edge_def.type}')
                    edge_statements.append(')')
                    edge_statements.append('{')
                    edge_inner_statements = list()
                    if edge_def.name:
                        edge_inner_statements.append(f'as:`{edge_def.name}`')
                    if edge_def.where:
                        where_statements: List[str] = list()
                        self._build_expression(edge_def.where.expression, query, where_statements)
                        if where_statements:
                            edge_inner_statements.append(
                                f'where: {" ".join(where_statements)}'
                            )
                    edge_statements.append(','.join(edge_inner_statements))
                    edge_statements.append('}')
                    if edge_def.direction == AsglEdgeDirection.IN:
                        edge_statements.append('.inV()')
                    elif edge_def.direction == AsglEdgeDirection.OUT:
                        edge_statements.append('.outV()')
                    else:
                        edge_statements.append('.bothV()')
                    link_statements.append(''.join(edge_statements))
            links_statements.append(''.join(link_statements))
        statements.append(','.join(links_statements))
        return '\r\n'.join(statements)

    def build_for_view(self, query: AsglQuery):
        if not query.vertex_defs:
            raise
        root_vertex = AsglVertexDef()
        root_vertex.type = 'EntityRoot'
        link: AsglLink = query.links[0]
        link.elements.insert(0, root_vertex)
        edge = AsglEdgeDef()
        link.elements.insert(1, edge)
        statement = self.build(query)
        query.build()
        statement += f'\r\nRETURN DISTINCT `{root_vertex.name}`.entity_id as entity_id limit 10000000'
        return statement

    def build_for_entity(self, entity_id: str, query: AsglQuery, option: AsqlOption):
        if not query.vertex_defs:
            raise
        root_vertex = AsglVertexDef()
        root_vertex.type = 'EntityRoot'
        value = AqlValue(AqlValueType.VALUE, entity_id)
        call = AqlOperatorCall()
        call.value = value
        call.operator = AqlOperator.EQUAL
        target = AqlFieldTarget()
        target.call = call
        target.field_name = 'entity_id'
        exp = AqlSimpleExpression(target)
        root_vertex.where.expression = exp
        link: AsglLink = query.links[0]
        link.elements.insert(0, root_vertex)
        edge = AsglEdgeDef()
        link.elements.insert(1, edge)
        query.build()
        statement = self.build(query)
        statement += f'\r\nRETURN DISTINCT $paths LIMIT ' \
                     f'{20 if option is None or option.limit is None else option.limit}'
        return statement, {}
