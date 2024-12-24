from typing import Optional, List

from caasm_aql.asql_batch_antlr4.AsqlBatchLexer import AsqlBatchLexer
from caasm_aql.asql_batch_antlr4.AsqlBatchParser import AsqlBatchParser
from caasm_aql.asql_batch_antlr4.AsqlBatchVisitor import AsqlBatchVisitor
from caasm_aql.base import AsqlPlusQueryBase, AsqlPlusType, AqlLogicalGroup, AqlItem, AqlItemType, AqlLogicalOperand, \
    AsqlLogicalQueryBase, AsqlType, Resolver


class AsqlBatchLogicQuery(AsqlLogicalQueryBase):
    def __init__(self):
        super(AsqlBatchLogicQuery, self).__init__()
        self.fields: List[str] = []
        self._keywords: List[str] = []
        self.op: str = ""

    def to_asql(self):
        keywords = "\\n".join(self.keywords)
        if self.op == '=':
            return f"[{','.join(self.fields)}] = \"{keywords}\""
        else:
            return f"[{','.join(self.fields)}].{self.op}(\"{keywords}\")"

    def to_dict(self, field_maper=None):
        return {
            "type": AsqlType.BATCH,
            "asql": self.to_asql(),
            "text": "批量检索",
        }

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, value):
        if isinstance(value, str):
            value = value.split("\n")
        self._keywords = list(filter(lambda v: v, value))


class AsqlBatchItem(AqlItem):
    def __init__(self):
        super(AsqlBatchItem, self).__init__(AqlItemType.BATCH)
        self.fields: List[str] = []
        self.keywords: List[str] = []
        self.op: str = ""


class AsqlBatchQuery(AsqlPlusQueryBase):
    def __init__(self):
        super(AsqlBatchQuery, self).__init__(AsqlPlusType.BATCH)
        self.fields: List[str] = []
        self.keywords: List[str] = []
        self.op: str = ""

    def to_logical_group(self) -> Optional[AqlLogicalGroup]:
        logical_group = AqlLogicalGroup()
        item = AsqlBatchItem()
        item.fields = self.fields
        item.keywords = self.keywords
        item.op = self.op
        logical_group.operand = AqlLogicalOperand.AND
        logical_group.not_boolean = False
        logical_group.items.append(item)
        return logical_group

    def to_logic_query(self) -> Optional[AsqlLogicalQueryBase]:
        logic_query = AsqlBatchLogicQuery()
        logic_query.logical_group = self.to_logical_group()
        logic_query.keywords = self.keywords
        logic_query.op = self.op
        logic_query.fields = self.fields
        return logic_query

    def is_valid(self):
        return len(self.keywords) <= 100

    def errors(self):
        return "批量检索不能超过100个关键字"


class AsqlBatchResolver(AsqlBatchVisitor, Resolver):
    def resolve_logic_query(self, asql: str):
        query: AsqlBatchQuery = self.resolve(asql)
        logic_query = AsqlBatchLogicQuery()
        logic_query.keywords = query.keywords
        logic_query.op = query.op
        logic_query.fields = query.fields
        return logic_query

    def __init__(self, type_=AsqlType.FIELD):
        super(AsqlBatchResolver, self).__init__(type_)
        self.query: Optional[AsqlBatchQuery] = None

    def _init(self):
        self.query: AsqlBatchQuery = AsqlBatchQuery()
        self.query.op = "="

    def _get_parser(self, stream):
        return AsqlBatchParser(stream)

    def _get_parser_root(self, parser):
        parser: AsqlBatchParser = parser
        return parser.batchFilter()

    def _visit(self, tree):
        self.visitBatchFilter(tree)

    def _get_result(self):
        return self.query

    def _get_lexer(self, statement_stream):
        return AsqlBatchLexer(statement_stream)

    def visitFieldName(self, ctx: AsqlBatchParser.FieldNameContext):
        self.query.fields.append(ctx.getText())
        return super().visitFieldName(ctx)

    def visitBatchValue(self, ctx: AsqlBatchParser.BatchValueContext):
        value = ctx.getText()
        value = value[1:-1]
        value = value.replace("\\n", "\n")
        self.query.keywords = list(filter(lambda v: v, value.split("\n")))
        return super().visitBatchValue(ctx)

    def visitMethod(self, ctx: AsqlBatchParser.MethodContext):
        self.query.op = ctx.getText()
        return super().visitMethod(ctx)

    def visitAnyField(self, ctx: AsqlBatchParser.AnyFieldContext):
        self.query.fields.append("*")
        return super().visitAnyField(ctx)


if __name__ == "__main__":
    resolver = AsqlBatchResolver()
    bb = resolver.resolve_logic_query(
        "[network.priority_addr, network.ips.addr, network.ips.addr_v4] = \"10.2.1.21\n10.2.97.37\n10.2.224.62\"")
    a = bb.to_asql()
    c = bb.to_dict()
    dd = 1
