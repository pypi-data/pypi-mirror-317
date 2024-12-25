import logging
from datetime import datetime
from typing import Dict, List

from cachetools import TTLCache

from caasm_aql.aql import AsqlOption, AqlSorting, AqlLogicQuery
from caasm_aql.querier import QuerierResult
from caasm_aql.queriers._base import BaseLogicalGroupQuerier
from caasm_aql.query_builders.backend.es import ESLogicalGroupQueryBuilder
from caasm_entity.service.runtime import entity_service
from caasm_meta_model.service.entities.meta_model import MetaFieldType
from caasm_persistence.handler.runtime import es_handler

log = logging.getLogger()

_local_cache = TTLCache(100, 300)


class EsQueryRegistry:
    _DEFAULT_SORT = [{"base.adapter_count": {"order": "desc"}}]

    def __init__(self):
        self._sorting_dict = {}

    def register_sorting(self, category, sorting):
        self._sorting_dict[category] = sorting

    def get_sorting(self, category):
        return self._sorting_dict.get(category, self._DEFAULT_SORT)


es_query_registry = EsQueryRegistry()


class ESLogicalGroupQuerier(BaseLogicalGroupQuerier):
    _SORT_IGNORE_DATA_TYPES = [MetaFieldType.OBJECT, MetaFieldType.RELATION]

    def _parse_aql(self, category, aql, option=None, additions=None, entity_ids=None):
        query, result = self._construct_query(aql)
        condition, high_lights, errors = self._handle_core(
            query, additions=additions, option=option, category=category, entity_ids=entity_ids
        )
        return condition, high_lights, errors

    def parse_aql(self, category, aql, option=None, additions=None, entity_ids=None):
        if not additions and not entity_ids:
            key = f"aql:{category}:{aql}"
            condition = _local_cache.get(key)
            if condition is None:
                condition, high_lights, errors = self._parse_aql(category, aql, option)
                _local_cache[key] = condition
            return condition, [], []
        else:
            return self._parse_aql(category, aql, option, additions, entity_ids)

    def _handle_core(self, query: AqlLogicQuery, additions=None, option=None, category=None, entity_ids=None):
        if additions is None:
            additions = list()
        if option is None:
            option = AsqlOption()
        if option.field_list is None:
            option.field_list = list()
            if "adapters" in option.field_list:
                option.field_list.remove("adapters")
            adapter_fields = list()
            for field in option.field_list:
                adapter_fields.append(f"adapters.{field}")
            if "adapters.base.adapter_name" not in option.field_list:
                adapter_fields.append("adapters.base.adapter_name")
            option.field_list.extend(adapter_fields)

        option.field_sorting_list = option.field_sorting_list or list()
        builder: ESLogicalGroupQueryBuilder = ESLogicalGroupQueryBuilder(self.meta_fields)

        query_condition, high_lights, errors = None, [], []
        #   查询
        try:
            query_condition = builder.build(query, category, high_lights, additions, entity_ids)
        except ValueError as ex:
            error = ex.args[0]
            errors = error if isinstance(error, list) else [error]

        return query_condition, high_lights, errors

    @classmethod
    def _is_condition_empty(cls, condition):
        if condition is None:
            return True
        if isinstance(condition, Dict):
            if not condition:
                return True
            for k, v in condition.items():
                if not cls._is_condition_empty(v):
                    return False
            return True
        elif isinstance(condition, List):
            if not condition:
                return True
            any_empty = False
            for item in condition:
                if cls._is_condition_empty(item):
                    any_empty = True
                    break
            return any_empty

    def _query(
        self,
        query: AqlLogicQuery,
        result: QuerierResult,
        category: str,
        option: [AsqlOption, None] = None,
        date: datetime = None,
        additions=None,
        entity_ids=None,
    ):
        query_condition, high_lights, errors = self._handle_core(query, additions, option, category, entity_ids)
        if errors:
            result.errors.extend(errors)
            return result

        collection_name = entity_service.get_table(category, date)
        log.debug(f"QueryCondition is {query_condition}")
        if not query.is_empty() and self._is_condition_empty(query_condition):
            #   查询不为空，，说明条件内参数有问题没生效导致
            result.count = 0
            result.data = []
        else:
            try:
                count = es_handler.count(condition=query_condition, table=collection_name)
            except Exception as e:
                log.error(f"Query count error({e})")
                count = 0
            if count:
                params = {
                    "condition": query_condition,
                    "sort_fields": self._parse_sort_field(category, option.field_sorting_list),
                }

                if option.field_list:
                    params["fields"] = option.field_list

                if option.page_index and option.page_size:
                    offset = (option.page_index - 1) * option.page_size
                    limit = option.page_size
                    params.update({"offset": offset, "limit": limit})

                log.debug(f"Aql search params  is {params}. index is {collection_name}")

                if high_lights:
                    records = es_handler.find_direct(table=collection_name, **params)
                else:
                    records = es_handler.find_direct(
                        table=collection_name, **params, highlight={"fields": {"*": {}}, "max_analyzed_offset": 900000}
                    )

                result.data = list(records)

            result.datasets = self.parse_dataset_exclude_entity(query)
            result.count = count
        result.high_lights = high_lights
        return result

    def _parse_sort_field(self, category, sort_fields):
        if sort_fields:
            tmp_sort_fields = []

            for field in sort_fields:
                meta_field = self.meta_fields.get(field.field_name)
                if not meta_field:
                    continue
                sort_field_name = self.get_sort_field_name(meta_field)
                if not sort_field_name:
                    continue
                field_sort_type = "asc" if field.sorting == AqlSorting.ASC else "desc"

                sort_field_info = {"order": field_sort_type}
                if meta_field.complex_full_name:
                    sort_field_info["nested"] = {"path": meta_field.complex_full_name}
                tmp_sort_fields.append({sort_field_name: sort_field_info})

            result = tmp_sort_fields
        else:
            result = es_query_registry.get_sorting(category)
        return result

    @classmethod
    def get_sort_field_name(cls, meta_field):
        field_type = meta_field.type
        full_field_name = meta_field.full_name

        if field_type == MetaFieldType.ENUM:
            return full_field_name + ".value"
        elif field_type == MetaFieldType.LIST:
            return f"_size.{full_field_name}__size"
        elif field_type in cls._SORT_IGNORE_DATA_TYPES:
            return None
        return full_field_name
