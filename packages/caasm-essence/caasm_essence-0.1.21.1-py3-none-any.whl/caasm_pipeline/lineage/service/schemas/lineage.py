from caasm_persistence_base.schema.base import ObjectIdField, DocumentSchema
from marshmallow import post_load, Schema, post_dump
from marshmallow.fields import String, Nested, List, Raw, Integer
from marshmallow.schema import BaseSchema
from marshmallow_enum import EnumField

from caasm_pipeline.lineage.service.constants.lineage import LineageStageType
from caasm_pipeline.lineage.service.entities.lineage import EntityTypeLineageMetaEntity, EntityTypeFetchMetaEntity, \
    EntityTypeMergeMetaEntity, EntityTypeConvertMetaEntity, EntityTypeFabricMetaEntity, EntityTypeLineageStageEntity, \
    EntityLineageMetaEntity, EntityFetchMetaEntity, EntityMergeMetaEntity, EntityConvertMetaEntity, \
    EntityFabricMetaEntity, EntityUpstreamEntity, EntityLineageStageEntity, ValueLineageMetaEntity, \
    ValueFetchMetaEntity, ValueMergeMetaEntity, ValueConvertMetaEntity, ValueFabricMetaEntity, ValueRowUpstreamEntity, \
    ValueRowLineageEntity, ValueLineageEntity, ValueEntityUpstreamEntity, ValueLineageStageEntity


#   实体类型血缘
class EntityTypeLineageMetaSchema(BaseSchema):
    entity_define = EntityTypeLineageMetaEntity


class EntityTypeFetchMetaSchema(EntityTypeLineageMetaSchema):
    entity_define = EntityTypeFetchMetaEntity

    adapter_id = ObjectIdField(required=True)
    adapter = String(required=True)
    adapter_instance_id = ObjectIdField(required=True)
    adapter_instance_name = String(required=True)
    fetch_type = String(required=True)


class EntityTypeMergeMetaSchema(EntityTypeLineageMetaSchema):
    entity_define = EntityTypeMergeMetaEntity

    ...


class EntityTypeConvertMetaSchema(EntityTypeLineageMetaSchema):
    entity_define = EntityTypeConvertMetaEntity

    ...


class EntityTypeFabricMetaSchema(EntityTypeLineageMetaSchema):
    entity_define = EntityTypeFabricMetaEntity

    date = String(required=True)
    category = String(required=True)
    entity_type = String(required=True)


class EntityTypeLineageStageSchema(DocumentSchema):
    entity_define = EntityTypeLineageStageEntity

    table = String(required=False)
    type = EnumField(LineageStageType, by_value=True, required=True)
    meta = Raw(required=False, allow_none=True, default=dict)
    upstreams = List(String, default=list, load_default=list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._schema_mapper = {
            LineageStageType.FETCH: EntityTypeFetchMetaSchema(),
            LineageStageType.MERGE: EntityTypeMergeMetaSchema(),
            LineageStageType.CONVERT: EntityTypeConvertMetaSchema(),
            LineageStageType.FABRIC: EntityTypeFabricMetaSchema(),
        }

    @post_load
    def make_meta(self, data, many=None, **kwargs):
        try:
            stage_type = data["type"]
        except ValueError:
            return None
        meta_data = data.get("meta", {})
        schema = self._schema_mapper.get(stage_type)
        if schema is None:
            return None
        meta = schema.load(meta_data)
        data["meta"] = meta
        if "table" not in data:
            data["table"] = ""
        return data

    @post_dump
    def ser(self, data, many=None, **kwargs):
        meta_schema = self._schema_mapper.get(data["type"])
        if meta_schema is None:
            return None
        meta_data = meta_schema.dump(data["meta"])
        data["meta"] = meta_data
        return data


#   实体血缘
class EntityLineageMetaSchema(Schema):
    entity_define = EntityLineageMetaEntity


class EntityFetchMetaSchema(EntityLineageMetaSchema):
    entity_define = EntityFetchMetaEntity

    adapter_id = ObjectIdField()
    adapter = String()
    adapter_instance_id = ObjectIdField()
    adapter_instance_name = String()
    fetch_type = String()
    oid = ObjectIdField()


class EntityMergeMetaSchema(EntityLineageMetaSchema):
    entity_define = EntityMergeMetaEntity

    ...


class EntityConvertMetaSchema(EntityLineageMetaSchema):
    entity_define = EntityConvertMetaEntity

    ...


class EntityFabricMetaSchema(EntityLineageMetaSchema):
    entity_define = EntityFabricMetaEntity


class EntityUpstreamSchema(BaseSchema):
    entity_define = EntityUpstreamEntity

    table = String(required=True)
    sid = String(required=True)


class EntityLineageStageSchema(DocumentSchema):
    entity_define = EntityLineageStageEntity

    table = String(required=True)
    type = EnumField(LineageStageType, by_value=True, required=True)
    #   追踪ID，根据阶段不同使用不同字段，可能为trace_id，也可能使用entity_id
    trace_id = String(required=True)
    meta = Raw(required=False)
    upstreams = List(Nested(EntityUpstreamSchema()), default=list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._schema_mapper = {
            LineageStageType.FETCH: EntityFetchMetaSchema(),
            LineageStageType.MERGE: EntityMergeMetaSchema(),
            LineageStageType.CONVERT: EntityConvertMetaSchema(),
            LineageStageType.FABRIC: EntityFabricMetaSchema(),
        }

    @post_load
    def make_meta(self, data, many=None, **kwargs):
        try:
            stage_type = data["type"]
        except ValueError:
            return None
        meta_data = data.get("meta", {})
        meta_schema = self._schema_mapper.get(stage_type)
        if meta_schema is None:
            return None
        meta = meta_schema.load(meta_data)
        data["meta"] = meta
        if "table" not in data:
            data["table"] = ""
        return data

    @post_dump
    def ser(self, data, many=None, **kwargs):
        meta_schema = self._schema_mapper.get(data["type"])
        if meta_schema is None:
            return None
        meta_data = meta_schema.dump(data["meta"])
        data["meta"] = meta_data
        return data


#   复杂字段值血缘
class ValueLineageMetaSchema(BaseSchema):
    entity_define = ValueLineageMetaEntity

    ...


class ValueFetchMetaSchema(ValueLineageMetaSchema):
    entity_define = ValueFetchMetaEntity

    adapter_id = ObjectIdField()
    adapter = String()
    adapter_instance_id = ObjectIdField()
    adapter_instance_name = String()
    fetch_type = String()
    oid = ObjectIdField()


class ValueMergeMetaSchema(ValueLineageMetaSchema):
    entity_define = ValueMergeMetaEntity

    ...


class ValueConvertMetaSchema(ValueLineageMetaSchema):
    entity_define = ValueConvertMetaEntity

    ...


class ValueFabricMetaSchema(ValueLineageMetaSchema):
    entity_define = ValueFabricMetaEntity

    ...


class ValueRowUpstreamSchema(BaseSchema):
    entity_define = ValueRowUpstreamEntity

    #   对应顶层实体upstreams中的id
    upstream = String()
    indices = List(Integer(), load_default=list)


class ValueRowLineageSchema(BaseSchema):
    entity_define = ValueRowLineageEntity

    index = Integer()
    upstreams = List(Nested(ValueRowUpstreamSchema), load_default=list)


class ValueLineageSchema(BaseSchema):
    entity_define = ValueLineageEntity

    #   list[object]类型字段名称
    field = String()
    rows = List(Nested(ValueRowLineageSchema), load_default=list)


class ValueEntityUpstreamSchema(BaseSchema):
    entity_define = ValueEntityUpstreamEntity

    table = String()
    sid = String()
    id = String()


class ValueLineageStageSchema(DocumentSchema):
    entity_define = ValueLineageStageEntity

    table = String(allow_none=True)
    #   追踪ID
    trace_id = String()
    type = EnumField(LineageStageType, by_value=True)
    meta = Nested(EntityLineageMetaSchema())
    upstreams = List(Nested(ValueEntityUpstreamSchema), load_default=list)
    fields = List(Nested(ValueLineageSchema), load_default=list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._schema_mapper = {
            LineageStageType.FETCH: ValueFetchMetaSchema(),
            LineageStageType.MERGE: ValueMergeMetaSchema(),
            LineageStageType.CONVERT: ValueConvertMetaSchema(),
            LineageStageType.FABRIC: ValueFabricMetaSchema(),
        }

    @post_load
    def make_meta(self, data, many=None, **kwargs):
        try:
            stage_type = data["type"]
        except ValueError:
            return None
        meta_data = data.get("meta", {})
        meta_schema = self._schema_mapper.get(stage_type)
        if meta_schema is None:
            return None
        meta = meta_schema.load(meta_data)
        data["meta"] = meta
        if "table" not in data:
            data["table"] = ""
        return data

    @post_dump
    def ser(self, data, many=None, **kwargs):
        meta_schema = self._schema_mapper.get(data["type"])
        if meta_schema is None:
            return None
        meta_data = meta_schema.dump(data["meta"])
        data["meta"] = meta_data
        return data
