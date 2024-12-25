from typing import Optional, List

from caasm_aql.aql import AqlLogicQuery
from caasm_aql.aql_resolver import AqlResolver
from caasm_aql.asgl_plus_antlr4.AsqlPlusLexer import AsqlPlusLexer
from caasm_aql.asgl_plus_antlr4.AsqlPlusParser import AsqlPlusParser
from caasm_aql.asgl_plus_antlr4.AsqlPlusVisitor import AsqlPlusVisitor
from caasm_aql.asql_batch import AsqlBatchResolver, AsqlBatchLogicQuery
from caasm_aql.asql_field import AsqlFieldResolver, AsqlFieldLogicQuery
from caasm_aql.asql_fulltext import AsqlFulltextResolver, AsqlFulltextLogicQuery
from caasm_aql.base import AsqlPlusQueryBase, AqlLogicalGroup, Resolver, AsqlType, AsqlLogicalQueryBase


class AsqlPlusQuery:
    def __init__(self):
        self.aql: Optional[str] = None
        self.sub_queries: List[AsqlPlusQueryBase] = []

    def to_logical_group(self):
        groups = []
        for sub_query in self.sub_queries:
            sub_query: AsqlPlusQueryBase = sub_query
            groups.append(sub_query.to_logical_group())
        return AqlLogicalGroup.merge(groups)


class AsqlPlusLogicalQuery(AsqlLogicalQueryBase):
    _QUERIES = {
        AsqlType.ASQL.value: AqlLogicQuery,
        AsqlType.FIELD.value: AsqlFieldLogicQuery,
        AsqlType.FULLTEXT.value: AsqlFulltextLogicQuery,
        AsqlType.BATCH.value: AsqlBatchLogicQuery,
    }

    def __init__(self):
        super(AsqlPlusLogicalQuery, self).__init__()
        self.queries: List[AsqlLogicalQueryBase] = []

    def to_asql(self):
        asql_list = []
        for query in self.queries:
            asql_list.append(query.to_asql())
        return ";".join(asql_list)

    def to_dict(self, field_mapper=None):
        return {"type": AsqlType.ASQL_PLUS, "asql": self.to_asql()}

    @staticmethod
    def from_list(asql_list):
        if not asql_list:
            return ""
        asql_items = []
        for asql_item in asql_list:
            type_ = asql_item["type"]
            asql_items.append(AsqlPlusLogicalQuery._QUERIES[type_].from_dict(asql_item))
        return ";".join(asql_items)

    def is_empty(self):
        return all(q.is_empty() for q in self.queries)


class AsqlPlusResolver(Resolver, AsqlPlusVisitor):
    def __init__(self, as_fulltext=False):
        super(AsqlPlusResolver, self).__init__(AsqlType.ASQL_PLUS)
        self.field_resolver = AsqlFieldResolver()
        self.fulltext_resolver = AsqlFulltextResolver()
        self.asql_resolver = AqlResolver()
        self.batch_resolver = AsqlBatchResolver()
        self.query = AsqlPlusQuery()
        #   如果为true，当识别错误时，将当做全文检索条件
        self.as_fulltext = as_fulltext

    def _get_parser(self, stream):
        return AsqlPlusParser(stream)

    def _get_parser_root(self, parser):
        parser: AsqlPlusParser = parser
        return parser.asqlPlus()

    def _visit(self, tree):
        return self.visit(tree)

    def _get_result(self):
        return self.query

    def _get_lexer(self, stream):
        return AsqlPlusLexer(stream)

    def visitFieldFilter(self, ctx: AsqlPlusParser.FieldSimpleExprContext):
        statement = ctx.get_whitespaced_text()
        self.query.sub_queries.append(self.field_resolver.resolve(statement))

    def visitAqlFilter(self, ctx: AsqlPlusParser.AqlFilterContext):
        statement = ctx.get_whitespaced_text()
        self.query.sub_queries.append(self.asql_resolver.resolve(statement))

    def visitFullTextFilter(self, ctx: AsqlPlusParser.FullTextFilterContext):
        statement = ctx.getText()
        statement = statement[1 : len(statement) - 1]
        query = self.fulltext_resolver.resolve(statement)
        if not query.is_valid():
            raise ValueError(query.errors())
        self.query.sub_queries.append(query)

    def visitBatchFilter(self, ctx: AsqlPlusParser.BatchFilterContext):
        statement = ctx.get_whitespaced_text()
        query = self.batch_resolver.resolve(statement)
        if not query.is_valid():
            raise ValueError(query.errors())
        self.query.sub_queries.append(query)

    def resolve_logic_query(self, asql: str) -> Optional[AsqlPlusLogicalQuery]:
        try:
            query: AsqlPlusQuery = self.resolve(asql)
        except ValueError:
            if self.as_fulltext:
                asql = asql.replace("'", "'")
                new_asql = f"'{asql}'"
                query: AsqlPlusQuery = self.resolve(new_asql)
            else:
                raise
        logic_query = AsqlPlusLogicalQuery()
        logical_groups = []
        for q in query.sub_queries:
            logical_q = q.to_logic_query()
            logic_query.queries.append(logical_q)
            logical_groups.append(logical_q.logical_group)
        logic_query.logical_group = AqlLogicalGroup.merge(logical_groups)
        return logic_query


if __name__ == "__main__":
    resolver = AsqlPlusResolver()
    aa = resolver.resolve_logic_query('"far3fsa.af";abc=3;$.def.exists()')
    bb = aa.logical_group
    dd = 1
