from dataclasses import dataclass
from typing import List

from bson import ObjectId
from caasm_persistence_base.entity.base import BaseEntity, DocumentEntity

from caasm_pipeline.lineage.service.constants.lineage import LineageStageType


#   实体类型血缘
@dataclass
class EntityTypeLineageMetaEntity(BaseEntity):
    ...


@dataclass
class EntityTypeFetchMetaEntity(EntityTypeLineageMetaEntity):
    adapter_id: ObjectId
    adapter: str
    adapter_instance_id: ObjectId
    adapter_instance_name: str
    fetch_type: str


@dataclass
class EntityTypeMergeMetaEntity(EntityTypeLineageMetaEntity):
    ...


@dataclass
class EntityTypeConvertMetaEntity(EntityTypeLineageMetaEntity):
    ...


@dataclass
class EntityTypeFabricMetaEntity(EntityTypeLineageMetaEntity):
    date: str
    category: str
    entity_type: str


@dataclass
class EntityTypeLineageStageEntity(DocumentEntity):
    table: str
    type: LineageStageType
    meta: EntityTypeLineageMetaEntity
    upstreams: List[str]


#   实体血缘
@dataclass
class EntityLineageMetaEntity(BaseEntity):
    ...


@dataclass
class EntityFetchMetaEntity(EntityLineageMetaEntity):
    adapter_id: ObjectId
    adapter: str
    adapter_instance_id: ObjectId
    adapter_instance_name: str
    fetch_type: str
    oid: ObjectId


@dataclass
class EntityMergeMetaEntity(EntityLineageMetaEntity):
    ...


@dataclass
class EntityConvertMetaEntity(EntityLineageMetaEntity):
    ...


@dataclass
class EntityFabricMetaEntity(EntityLineageMetaEntity):
    ...


@dataclass
class EntityUpstreamEntity(BaseEntity):
    table: str
    sid: str


@dataclass
class EntityLineageStageEntity(DocumentEntity):
    table: str
    #   追踪ID
    trace_id: str
    type: LineageStageType
    meta: EntityLineageMetaEntity
    upstreams: List[EntityUpstreamEntity]


#   字段值血缘（目前只有复杂字段，即子表格字段）
@dataclass
class ValueLineageMetaEntity(BaseEntity):
    ...


@dataclass
class ValueFetchMetaEntity(ValueLineageMetaEntity):
    adapter_id: ObjectId
    adapter: str
    adapter_instance_id: ObjectId
    adapter_instance_name: str
    fetch_type: str
    oid: ObjectId


@dataclass
class ValueMergeMetaEntity(ValueLineageMetaEntity):
    ...


@dataclass
class ValueConvertMetaEntity(ValueLineageMetaEntity):
    ...


@dataclass
class ValueFabricMetaEntity(ValueLineageMetaEntity):
    ...


@dataclass
class ValueRowUpstreamEntity(BaseEntity):
    #   对应顶层实体upstreams中的id
    upstream: str
    indices: List[int]


@dataclass
class ValueRowLineageEntity(BaseEntity):
    index: int
    upstreams: List[ValueRowUpstreamEntity]


@dataclass
class ValueLineageEntity(BaseEntity):
    #   list[object]类型字段名称
    field: str
    rows: List[ValueRowLineageEntity]


@dataclass
class ValueEntityUpstreamEntity(BaseEntity):
    table: str
    sid: str
    id: str


@dataclass
class ValueLineageStageEntity(DocumentEntity):
    table: str
    #   追踪ID
    trace_id: str
    type: LineageStageType
    meta: EntityLineageMetaEntity
    upstreams: List[ValueEntityUpstreamEntity]
    fields: List[ValueLineageEntity]
