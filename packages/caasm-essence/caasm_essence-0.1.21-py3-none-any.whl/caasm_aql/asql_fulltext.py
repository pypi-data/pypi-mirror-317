from typing import Optional

from caasm_aql.base import AsqlPlusQueryBase, AsqlPlusType, AqlLogicalGroup, AqlItem, AqlItemType, AqlLogicalOperand, \
    ResolverBase, AsqlLogicalQueryBase, AsqlType


class AsqlFulltextItem(AqlItem):
    def __init__(self):
        super(AsqlFulltextItem, self).__init__(AqlItemType.FULLTEXT)
        self.fulltext = None


class AsqlFulltextLogicQuery(AsqlLogicalQueryBase):
    def __init__(self):
        super(AsqlFulltextLogicQuery, self).__init__()
        self.fulltext = None

    def to_asql(self):
        if isinstance(self.fulltext, str):
            fulltext = f"'{self.fulltext}'"
        else:
            fulltext = "\n".join(self.fulltext)
            fulltext = f"'{fulltext}'"
        return fulltext

    def to_dict(self, field_maper=None):
        if isinstance(self.fulltext, list):
            return {
                "type": AsqlType.FULLTEXT,
                "asql": self.to_asql(),
                "text": "\n".join(self.fulltext)
            }
        return {
            "type": AsqlType.FULLTEXT,
            "asql": self.to_asql(),
            "text": self.fulltext
        }

    @staticmethod
    def from_dict(asql_item):
        return asql_item['asql']

    def is_empty(self):
        return not self.fulltext


class AsqlFulltextQuery(AsqlPlusQueryBase):
    def __init__(self):
        self.fulltext = None
        super(AsqlFulltextQuery, self).__init__(AsqlPlusType.FULLTEXT)

    def to_logical_group(self) -> Optional[AqlLogicalGroup]:
        logical_group = AqlLogicalGroup()
        item = AsqlFulltextItem()
        item.fulltext = self.fulltext
        logical_group.operand = AqlLogicalOperand.AND
        logical_group.not_boolean = False
        logical_group.items.append(item)
        return logical_group

    def to_logic_query(self) -> Optional[AsqlLogicalQueryBase]:
        logic_query = AsqlFulltextLogicQuery()
        logic_query.logical_group = self.to_logical_group()
        logic_query.fulltext = self.fulltext
        return logic_query

    def is_valid(self):
        if isinstance(self.fulltext, str):
            return True
        elif isinstance(self.fulltext, list):
            return len(self.fulltext) <= 100

    def errors(self):
        return "批量全文检索不能超过100个关键字"


class AsqlFulltextResolver(ResolverBase):
    def resolve(self, asql: str):
        query = AsqlFulltextQuery()
        if "\n" in asql:
            query.fulltext = list(set(filter(lambda v: v, asql.split("\n"))))
        else:
            query.fulltext = asql
        return query

    def resolve_logic_query(self, asql: str):
        query: AsqlFulltextQuery = self.resolve(asql)
        logic_query = AsqlFulltextLogicQuery()
        logic_query.logical_group = query.to_logical_group()
        logic_query.fulltext = query.fulltext
        return logic_query
