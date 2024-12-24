import copy
from copy import deepcopy

from caasm_aql.aql import (
    AqlAddition,
)
from caasm_aql.asql_batch import AsqlBatchItem
from caasm_aql.asql_fulltext import AsqlFulltextItem
from caasm_aql.base import AqlLogicalOperand, AqlGroupItem, AqlLogicalCall, AqlTargetItem, AqlTargetType, AqlCallType, \
    AqlCall, AqlOperatorCall, AqlMethodCall
from caasm_aql.query_builders.backend._base import BaseBackend
from caasm_aql.query_builders.converter import Converter
from caasm_aql.query_builders.es.util import merge_query
from caasm_aql.query_builders.fuzzy_provider import FuzzyProvider
from caasm_aql.query_builders.runtime import query_builder_manager


class ESLogicalGroupQueryBuilder(BaseBackend):
    _LOGICAL_MAPPING = {AqlLogicalOperand.AND: "must", AqlLogicalOperand.OR: "should"}
    _COMPARISON_MAPPING = {}

    def build(self, query, category, high_lights, additions=None, entity_ids=None):
        if additions is None:
            additions = []
        if not query:
            return None
        # if query.aql:
        #     # 说明不是标准的aql语句，走的是特殊查询
        #     fuzzy_provider: FuzzyProvider = manager.fuzzy_provider_manager.get(category)
        #     return fuzzy_provider.provide(query.aql, self._make_additions(additions))
        return self._construct_query(query, category, high_lights, additions, entity_ids)

    def _make_additions(self, additions):
        _conditions = []
        if not additions:
            return _conditions

        for addition in additions:
            addition: AqlAddition = addition
            meta_field = self.field_data_type_getter.get_data_type(addition.field)
            if not meta_field:
                continue
            converter: Converter = query_builder_manager.converter_manager.get(meta_field.type)
            if not converter:
                continue
            v = converter.convert(addition.value, meta_field)
            _conditions.append({"term": {addition.field: v}})
        return _conditions

    def _make_entity_ids(self, entity_ids, entity_id_field_name: str):
        _conditions = []
        if entity_ids is None:
            return _conditions
        _conditions.append({'terms': {entity_id_field_name: entity_ids}})
        return _conditions

    def _construct_query(self, query, category, high_lights, additions=None, entity_ids=None):
        final_query = {}
        result = {"bool": final_query}
        if query.logical_group:
            self._convert_dataset_logical_group(query.logical_group, final_query, category, high_lights)
            if self.errors:
                raise ValueError(self.errors)
        if additions:
            _conditions = self._make_additions(additions)
            if _conditions:
                if "must" not in final_query:
                    final_query["must"] = _conditions
                else:
                    final_query["must"].extend(_conditions)
        if entity_ids is not None:
            _conditions = self._make_entity_ids(entity_ids, self.entity_id_field_name_getter.get_entity_id_field_name())
            if _conditions:
                if "must" not in final_query:
                    final_query["must"] = _conditions
                else:
                    final_query["must"].extend(_conditions)

        if not final_query:
            return None
        return result

    def _convert_field_logical_group(self, logical_group, final_query, high_lights, category, parent_field=None):
        parent_query = final_query
        if self.errors:
            return final_query
        if logical_group.not_boolean:
            condition = {}
            final_query["must_not"] = [condition]
            final_query = condition
        else:
            condition = {}
            final_query["must"] = [condition]
            final_query = condition
        group_conditions = []
        operand = self._LOGICAL_MAPPING[logical_group.operand]
        final_query["bool"] = {operand: group_conditions}
        for item in logical_group.items:
            if isinstance(item, AqlGroupItem):
                group_item: AqlGroupItem = item
                group = group_item.group
                group_condition = {}

                group_conditions.append(group_condition)
                self._convert_field_logical_group(group, group_condition, high_lights, category, parent_field)

                tmp_condition = copy.deepcopy(group_condition)

                if group.not_boolean:
                    tmp_operand = "must_not"
                else:
                    tmp_operand = "must"
                group_condition.pop(tmp_operand)
                group_condition["bool"] = {tmp_operand: tmp_condition.pop(tmp_operand)}

            elif isinstance(item, AqlTargetItem):
                target_item: AqlTargetItem = item
                target_type = target_item.target.target_type

                item_condition = {}
                group_conditions.append(item_condition)
                field_name: str = target_item.target.field_name
                query_field_name: str = target_item.target.field_name
                call: AqlCall = target_item.target.call

                if call.call_type == AqlCallType.OPERATOR and isinstance(call, AqlOperatorCall):
                    self._process_operator_call(
                        call, field_name, item_condition, query_field_name, high_lights, parent_field
                    )
                elif call.call_type == AqlCallType.METHOD and isinstance(call, AqlMethodCall):
                    self._process_method_call(
                        call, field_name, item_condition, target_type, high_lights, parent_field
                    )
                else:
                    raise ValueError()

        self._merge_parent_query(parent_query, operand)

    @classmethod
    def _merge_parent_query(cls, parent_query, operand):

        sub_queries = parent_query["must"][0]["bool"][operand]
        if operand != "should":
            parent_query["must"][0]["bool"][operand] = merge_query(sub_queries)

    def _convert_dataset_logical_group(self, logical_group, final_query, category, high_lights=None):
        if self.errors:
            return final_query
        if not logical_group:
            return final_query
        if logical_group.not_boolean:
            condition = {}
            final_query["must_not"] = [condition]
            final_query = condition
        else:
            condition = {}
            final_query["must"] = [condition]
            final_query = condition

        group_conditions = []
        final_query["bool"] = {self._LOGICAL_MAPPING[logical_group.operand]: group_conditions}

        for item in logical_group.items:
            if isinstance(item, AqlGroupItem):
                group_item: AqlGroupItem = item
                group = group_item.group
                group_condition = {}

                group_conditions.append(group_condition)
                self._convert_dataset_logical_group(group, group_condition, category, high_lights)

                tmp_condition = copy.deepcopy(group_condition)

                if group.not_boolean:
                    tmp_operand = "must_not"
                else:
                    tmp_operand = "must"
                if tmp_operand in group_condition:
                    group_condition.pop(tmp_operand)
                if tmp_operand in tmp_condition:
                    group_condition["bool"] = {tmp_operand: tmp_condition.pop(tmp_operand)}

            elif isinstance(item, AqlTargetItem):
                target_item: AqlTargetItem = item
                target_type = target_item.target.target_type

                item_condition = {}
                group_conditions.append(item_condition)
                field_name: str = target_item.target.field_name
                query_field_name: str = target_item.target.field_name
                call: AqlCall = target_item.target.call

                if call.call_type == AqlCallType.OPERATOR and isinstance(call, AqlOperatorCall):
                    self._process_operator_call(call, field_name, item_condition, query_field_name, high_lights)
                elif call.call_type == AqlCallType.METHOD and isinstance(call, AqlMethodCall):
                    self._process_method_call(call, field_name, item_condition, target_type, high_lights)
                else:
                    call: AqlLogicalCall = call
                    field_query = {}
                    self._convert_field_logical_group(
                        call.logical_group, field_query, high_lights, category, field_name
                    )
                    item_condition["bool"] = field_query
                if target_type == AqlTargetType.ADAPTER:
                    sub_query = deepcopy(item_condition)
                    item_condition.clear()
                    item_condition["bool"] = {
                        "must": [
                            {
                                "nested": {
                                    "path": "adapters",
                                    "query": {
                                        "bool": {
                                            "must": [
                                                sub_query,
                                                {"term": {"adapters.adapter_name": target_item.target.adapter_dataset}},
                                            ]
                                        }
                                    },
                                }
                            }
                        ]
                    }
            elif isinstance(item, AsqlBatchItem):
                item_condition = {}
                batch_item: AsqlBatchItem = item
                self._process_batch_item(batch_item, item_condition, high_lights)
                if item_condition:
                    group_conditions.append(item_condition)
            elif isinstance(item, AsqlFulltextItem):
                fulltext_item: AsqlFulltextItem = item
                fuzzy_provider: FuzzyProvider = query_builder_manager.fuzzy_provider_manager.get(category)
                group_conditions.append(fuzzy_provider.provide(fulltext_item.fulltext, []))
