from abc import ABC

from caasm_aql.aql import (
    AqlLogicQuery, AqlAdapterTarget,
)
from caasm_aql.base import AqlLogicalGroup, AqlGroupItem, AqlTargetItem, AqlTargetType
from caasm_aql.aql_resolver import AqlResolver
from caasm_aql.querier import LogicalGroupQuerier
from caasm_tool.util import deduplicate


class BaseLogicalGroupQuerier(LogicalGroupQuerier, ABC):
    def __init__(self, meta_fields):
        super(BaseLogicalGroupQuerier, self).__init__(meta_fields)

    @classmethod
    def parse_dateset_exclude_inventory_by_aql(cls, aql: str):
        resolver: AqlResolver = AqlResolver()
        query: AqlLogicQuery = resolver.resolve_logic_query(aql)
        return cls.parse_dataset_exclude_entity(query)

    @classmethod
    def parse_dataset_exclude_entity(cls, query: AqlLogicQuery):
        dataset = []
        if not query or query.logical_group is None:
            return dataset
        stack = [query.logical_group]
        while stack:
            logical_group: AqlLogicalGroup = stack.pop()
            if logical_group:
                for item in logical_group.items:
                    if isinstance(item, AqlGroupItem):
                        group_item: AqlGroupItem = item
                        stack.append(group_item.group)
                    elif isinstance(item, AqlTargetItem):
                        target_item: AqlTargetItem = item
                        if target_item.target.target_type == AqlTargetType.ADAPTER:
                            adapter_target: AqlAdapterTarget = target_item.target
                            dataset.append(adapter_target.adapter_dataset)
        return deduplicate(dataset)
