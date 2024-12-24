from typing import List

from antlr4 import InputStream, CommonTokenStream
from antlr4.tree.Tree import ParseTree

from caasm_aql.base import AsqlType
from caasm_aql.aql_error import AqlErrorListener
from caasm_aql.aql_resolver import AqlResolver
from caasm_aql.asgl import AsglQuery, AsglVertexDef, AsglEdgeDef, AsglLink, AsglEdgeDirection
from caasm_aql.asgl_antlr4.AsglLexer import AsglLexer
from caasm_aql.asgl_antlr4.AsglParser import AsglParser
from caasm_aql.asgl_antlr4.AsglVisitor import AsglVisitor


class AsglResolver(AsglVisitor):
    def __init__(self):
        super(AsglResolver, self).__init__()
        self.query: AsglQuery = AsglQuery()
        self.vertex_stack: List[AsglVertexDef] = list()
        self.edge_stack: List[AsglEdgeDef] = list()
        self.current_link: AsglLink = None
        self.sub_resolver = AqlResolver(type_=AsqlType.ASGL)

    def resolve(self, asgl: str) -> AsglQuery:
        if not asgl:
            return None
        statement_stream = InputStream(asgl)
        lexer = AsglLexer(statement_stream)
        errors = list()
        aql_listener = AqlErrorListener(errors)
        lexer.addErrorListener(aql_listener)
        if errors:
            raise ValueError(errors)
        stream = CommonTokenStream(lexer)
        parser = AsglParser(stream)
        parser.addErrorListener(aql_listener)
        tree: ParseTree = parser.asgl()
        if errors:
            raise ValueError(errors)
        self.visit(tree)
        return self.query

    def visitGraphLink(self, ctx: AsglParser.GraphLinkContext):
        self.current_link = AsglLink()
        result = super(AsglResolver, self).visitGraphLink(ctx)
        self.query.links.append(self.current_link)
        self.current_link = None
        return result

    def visitVertexDef(self, ctx: AsglParser.VertexDefContext):
        vertex_def: AsglVertexDef = AsglVertexDef()
        self.vertex_stack.append(vertex_def)
        result = super(AsglResolver, self).visitVertexDef(ctx)
        self.vertex_stack.pop()
        self.current_link.elements.append(vertex_def)
        return result

    def visitVertexId(self, ctx: AsglParser.VertexIdContext):
        vertex_def: AsglVertexDef = self.vertex_stack[-1]
        vertex_def.name = ctx.getText()
        return super(AsglResolver, self).visitVertexId(ctx)

    def visitVertexType(self, ctx: AsglParser.VertexTypeContext):
        vertex_def: AsglVertexDef = self.vertex_stack[-1]
        vertex_def.type = ctx.getText()
        return super(AsglResolver, self).visitVertexType(ctx)

    def visitEdgeDef(self, ctx: AsglParser.EdgeDefContext):
        edge_def: AsglEdgeDef = AsglEdgeDef()
        self.edge_stack.append(edge_def)
        result = super(AsglResolver, self).visitEdgeDef(ctx)
        self.edge_stack.pop()
        self.current_link.elements.append(edge_def)
        return result

    def visitInEdgeDef(self, ctx: AsglParser.InEdgeDefContext):
        edge_def: AsglEdgeDef = self.edge_stack[-1]
        edge_def.direction = AsglEdgeDirection.IN
        return super(AsglResolver, self).visitInEdgeDef(ctx)

    def visitOutEdgeDef(self, ctx: AsglParser.OutEdgeDefContext):
        edge_def: AsglEdgeDef = self.edge_stack[-1]
        edge_def.direction = AsglEdgeDirection.OUT
        return super(AsglResolver, self).visitOutEdgeDef(ctx)

    def visitEdgeId(self, ctx: AsglParser.EdgeIdContext):
        edge_def: AsglEdgeDef = self.edge_stack[-1]
        edge_def.name = ctx.getText()
        return super(AsglResolver, self).visitEdgeId(ctx)

    def visitEdgeType(self, ctx: AsglParser.EdgeTypeContext):
        edge_def: AsglEdgeDef = self.edge_stack[-1]
        edge_def.type = ctx.getText()
        return super(AsglResolver, self).visitEdgeType(ctx)

    def visitVertexAql(self, ctx: AsglParser.VertexAqlContext):
        vertex_def: AsglVertexDef = self.vertex_stack[-1]
        sub_query = ctx.get_whitespaced_text()
        if '<EOF>' in sub_query:
            sub_query = sub_query.replace('<EOF>', '')
        vertex_def.where = self.sub_resolver.resolve(sub_query)
        return super(AsglResolver, self).visitVertexAql(ctx)

    def visitEdgeAql(self, ctx: AsglParser.EdgeAqlContext):
        edge_def: AsglEdgeDef = self.edge_stack[-1]
        sub_query = ctx.get_whitespaced_text()
        if '<EOF>' in sub_query:
            sub_query = sub_query.replace('<EOF>', '')
        edge_def.where = self.sub_resolver.resolve(sub_query)
        return super(AsglResolver, self).visitEdgeAql(ctx)

    def visitNotBoolean(self, ctx: AsglParser.NotBooleanContext):
        self.current_link.not_boolean = True
        return super(AsglResolver, self).visitNotBoolean(ctx)

    def visitVertextTrait(self, ctx: AsglParser.VertextTraitContext):
        vertex_def: AsglVertexDef = self.vertex_stack[-1]
        vertex_def.trait = str(ctx.getText().strip("'\""))
        return super(AsglResolver, self).visitVertextTrait(ctx)


if __name__ == '__main__':
    resolver = AsglResolver()
    q = resolver.resolve(
        """
        not (a: a : '我' abc = 1 and aaa = 'fafsda') - [b] -> (c bb = abc(1)) (d) <- [e: eeee] - (f: f) (: a) -- (f) -- ()
        """
    )
    dd = 1
