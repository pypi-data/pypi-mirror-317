import datetime
from typing import List

from bson import ObjectId
from caasm_persistence.handler.storage.mongo import MongoHandler
from caasm_tool.util import get_now_format

from caasm_pipeline.clean.service.constants.clean import AdapterProcessStatus, CleanType
from caasm_pipeline.clean.service.entities.clean import AdapterCleanRuleEntity
from caasm_pipeline.clean.service.schemas.runtime import clean_record_schema, clean_rule_schema, clean_adapter_rule_schema, \
    clean_rule_trend_schema
from caasm_pipeline.service.constants.common import Sorting


class CleanRecordService(MongoHandler):
    DEFAULT_TABLE = "clean.records"
    DEFAULT_SCHEMA = clean_record_schema

    def get_clean_record(
        self,
        adapter_name,
        latest=None,
        status: AdapterProcessStatus = None,
        category=None,
    ):
        return self.get(self.build_condition(adapter_name, latest, status, category))

    @staticmethod
    def build_condition(
        adapter_name=None,
        latest=None,
        status: AdapterProcessStatus = None,
        category=None,
        start_time_lte=None,
        data_deleted=None,
        index=None,
    ):
        condition = {}
        if adapter_name:
            condition["adapter_name"] = adapter_name
        if latest is not None:
            condition["latest"] = latest
        if status:
            condition["status"] = status
        if category:
            condition["category"] = category
        if start_time_lte:
            condition["start_time"] = {"$lte": start_time_lte}
        if data_deleted:
            condition["data_deleted"] = data_deleted
        if index is not None:
            condition["index"] = index
        return condition

    @staticmethod
    def build_clean_rejected_data_table(category, adapter_name, index):
        return f"clean.rejected_{category}_{adapter_name}_{index}"

    def to_rejected_data_table(self, clean_record):
        return self.build_clean_rejected_data_table(
            clean_record.category, clean_record.adapter_name, clean_record.index
        )

    def find_clean_records(
        self, adapter_name=None, latest=None, category=None, status=None, start_time_lte=None, data_deleted=None
    ):
        return self.find(
            self.build_condition(
                adapter_name=adapter_name,
                latest=latest,
                status=status,
                category=category,
                start_time_lte=start_time_lte,
                data_deleted=data_deleted,
            )
        )

    @staticmethod
    def extract_adapter_name(table: str):
        segments = table.split(".")
        if len(segments) == 2:
            segments = segments[1].split("_")
            if len(segments) > 3:
                return "_".join(segments[2:-1])
        return None

    @staticmethod
    def extract_index(table: str):
        segments = table.split(".")
        if len(segments) == 2:
            segments = segments[1].split("_")
            if len(segments) > 3:
                try:
                    return int(segments[-1])
                except ValueError:
                    return None
        return None

    def mark_record_data_deleted(self, adapter_name, category, index):
        condition = self.build_condition(
            adapter_name=adapter_name,
            category=category,
            index=index,
        )
        return self.update_multi_direct(condition, {"data_deleted": True})


class CleanRuleService(MongoHandler):
    DEFAULT_TABLE = "clean.rules"
    DEFAULT_SCHEMA = clean_rule_schema

    def find_rules(self, rule_ids=None, category: str = None, entity_type: str = None, *args, **kwargs):
        return self.find(self.build_condition(rule_ids, category, entity_type), *args, **kwargs)

    @classmethod
    def build_condition(
        cls,
        rule_ids: List[ObjectId] = None,
        category: str = None,
        entity_type: str = None,
        rule_id: ObjectId = None,
        name: str = None,
        **kwargs,
    ):
        condition = {}
        if rule_ids is not None:
            condition["_id"] = {"$in": cls._build_ids(rule_ids)}
        if category is not None:
            condition["category"] = category
        if entity_type is not None:
            condition["entity_type"] = entity_type
        if rule_id is not None:
            condition["rule_id"] = cls._build_id(rule_id)
        if name is not None:
            condition["name"] = name
        return condition

    @classmethod
    def build_update_value(
        cls,
        name: str = None,
        category: str = None,
        entity_type: str = None,
        clean_type: CleanType = None,
        description: str = None,
        field_names: str = None,
        sort_field: str = None,
        sorting: Sorting = None,
        filter_asql: str = None,
        **kwargs,
    ) -> dict:
        values = {"update_time": get_now_format()}
        if name is not None:
            values["name"] = name
        if category is not None:
            values["category"] = category
        if entity_type is not None:
            values["entity_type"] = entity_type
        if clean_type is not None:
            values["clean_type"] = clean_type
        if description is not None:
            values["description"] = description
        if field_names is not None:
            values["field_names"] = field_names
        if sort_field is not None:
            values["sort_field"] = sort_field
        if sorting is not None:
            values["sorting"] = sorting
        if filter_asql is not None:
            values["filter_asql"] = filter_asql
        return values


class CleanAdapterRuleService(MongoHandler):
    DEFAULT_TABLE = "clean.adapter_rules"
    DEFAULT_SCHEMA = clean_adapter_rule_schema

    def find_rules(
        self,
        adapter_name=None,
        enabled=None,
        keyword=None,
        category=None,
        entity_type=None,
        adapter_rule_ids=None,
        *args,
        **kwargs,
    ):
        condition = self.build_condition(
            adapter_name=adapter_name, enabled=enabled, keyword=keyword, adapter_rule_ids=adapter_rule_ids
        )
        adapter_rules = self.find_list(condition, *args, **kwargs)
        rule_ids = []
        for adapter_rule in adapter_rules:
            adapter_rule: AdapterCleanRuleEntity = adapter_rule
            rule_ids.append(adapter_rule.rule_id)

        from caasm_pipeline.clean.service.runtime import clean_rule_service
        rules = clean_rule_service.find_rules(rule_ids=rule_ids, category=category, entity_type=entity_type)
        rules_by_id = dict((rule.id, rule) for rule in rules)
        results = []
        for adapter_rule in adapter_rules:
            results.append((adapter_rule, rules_by_id.get(adapter_rule.rule_id)))
        return results

    @staticmethod
    def build_condition(adapter_name, enabled=None, keyword=None, adapter_rule_ids=None):
        condition = {}
        if adapter_name:
            condition["adapter_name"] = adapter_name
        if enabled is not None:
            condition["enabled"] = enabled
        if keyword is not None:
            condition["name"] = {"$regex": keyword}
        if adapter_rule_ids:
            condition["_id"] = {"$in": adapter_rule_ids}
        return condition

    @classmethod
    def build_update_value(
        cls,
        adapter_name: str = None,
        enabled: bool = None,
        is_referenced: bool = None,
        rule_id: ObjectId = None,
        **kwargs,
    ) -> dict:
        values = {"update_time": get_now_format()}
        if adapter_name is not None:
            values["adapter_name"] = adapter_name
        if enabled is not None:
            values["enabled"] = enabled
        if is_referenced is not None:
            values["is_referenced"] = is_referenced
        if rule_id is not None:
            values["rule_id"] = cls._build_id(rule_id)
        return values

    def record_rejected_count(self, adapter_rule_id, date, count):
        adapter_rule: AdapterCleanRuleEntity = self.get_by_id(adapter_rule_id)
        if not adapter_rule:
            return
        trends_by_date = dict((item.date, item) for item in adapter_rule.trends)
        if date in trends_by_date:
            trends_by_date[date].count = count
        else:
            trend = clean_rule_trend_schema.load({"date": date, "count": count})
            adapter_rule.trends.append(trend)
        adapter_rule.trends.sort(key=lambda v: datetime.date.fromisoformat(v.date))
        if len(adapter_rule.trends) > 10:
            #   只保留10个最新的
            adapter_rule.trends = adapter_rule.trends[len(adapter_rule.trends) - 10:]
        self.update(adapter_rule)
