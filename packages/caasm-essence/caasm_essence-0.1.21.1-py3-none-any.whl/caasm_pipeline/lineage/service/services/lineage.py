from typing import List

from caasm_persistence.handler.storage.mongo import MongoHandler
from caasm_persistence_base.entity.base import BaseEntity
from marshmallow.schema import BaseSchema

from caasm_pipeline.lineage.service.schemas.runtime import entity_type_lineage_stage_schema, entity_lineage_stage_schema, \
    value_lineage_stage_schema


class EntityTypeLineageStageService(MongoHandler):
    DEFAULT_TABLE = "lineage.entity_type_stages"
    DEFAULT_SCHEMA = entity_type_lineage_stage_schema

    def get_lineage_by_upstream_table(self, table):
        condition = {"table": table}
        founds = list(self.find(condition, sort_fields=[("create_time", -1)], limit=1))
        if founds:
            return founds[0]
        else:
            return None


class EntityLineageStageService(MongoHandler):
    DEFAULT_SCHEMA = entity_lineage_stage_schema

    def _get_table(self, dst_table):
        return f"{self.DEFAULT_TABLE}.{dst_table}"

    def save_stage(self, entity: BaseEntity, dst_table, schema: BaseSchema = None, **kwargs):
        return self.save(entity, self._get_table(dst_table), schema, **kwargs)

    def save_stages(self, entities: List[BaseEntity], dst_table, schema=None):
        return self.save_multi(entities, self._get_table(dst_table), schema)


class EntityLineageFetchStageService(EntityLineageStageService):
    DEFAULT_TABLE = "lineage.entity_stages.fetch"


class EntityLineageMergeStageService(EntityLineageStageService):
    DEFAULT_TABLE = "lineage.entity_stages.merge"


class EntityLineageConvertStageService(EntityLineageStageService):
    DEFAULT_TABLE = "lineage.entity_stages.convert"


class EntityLineageFabricStageService(EntityLineageStageService):
    DEFAULT_TABLE = "lineage.entity_stages.fabric"

    def get_table(self, category, date):
        return f"{self.DEFAULT_TABLE}.{date}.{category}"


class ValueLineageStageService(EntityLineageStageService):
    DEFAULT_SCHEMA = value_lineage_stage_schema


class ValueLineageFetchStageService(ValueLineageStageService):
    DEFAULT_TABLE = "lineage.value_stages.fetch"


class ValueLineageMergeStageService(ValueLineageStageService):
    DEFAULT_TABLE = "lineage.value_stages.merge"


class ValueLineageConvertStageService(ValueLineageStageService):
    DEFAULT_TABLE = "lineage.value_stages.convert"


class ValueLineageFabricStageService(ValueLineageStageService):
    DEFAULT_TABLE = "lineage.value_stages.fabric"

    def get_table(self, category, date):
        return f"{self.DEFAULT_TABLE}.{date}.{category}"
