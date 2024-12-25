from caasm_pipeline.lineage.service.schemas.lineage import EntityTypeLineageMetaSchema, EntityTypeFetchMetaSchema, \
    EntityTypeMergeMetaSchema, EntityTypeConvertMetaSchema, EntityTypeFabricMetaSchema, EntityTypeLineageStageSchema, \
    EntityLineageMetaSchema, EntityFetchMetaSchema, EntityMergeMetaSchema, EntityConvertMetaSchema, \
    EntityFabricMetaSchema, EntityUpstreamSchema, EntityLineageStageSchema, ValueLineageMetaSchema, \
    ValueFetchMetaSchema, ValueMergeMetaSchema, ValueConvertMetaSchema, ValueFabricMetaSchema, ValueRowLineageSchema, \
    ValueLineageSchema, ValueLineageStageSchema

entity_type_lineage_meta_schema = EntityTypeLineageMetaSchema()
entity_type_fetch_meta_schema = EntityTypeFetchMetaSchema()
entity_type_merge_meta_schema = EntityTypeMergeMetaSchema()
entity_type_convert_meta_schema = EntityTypeConvertMetaSchema()
entity_type_fabric_meta_schema = EntityTypeFabricMetaSchema()
entity_type_lineage_stage_schema = EntityTypeLineageStageSchema(unknown="INCLUDE")

entity_lineage_meta_schema = EntityLineageMetaSchema()
entity_fetch_meta_schema = EntityFetchMetaSchema()
entity_merge_meta_schema = EntityMergeMetaSchema()
entity_convert_meta_schema = EntityConvertMetaSchema()
entity_fabric_meta_schema = EntityFabricMetaSchema()
entity_upstream_schema = EntityUpstreamSchema()
entity_lineage_stage_schema = EntityLineageStageSchema()

value_lineage_meta_schema = ValueLineageMetaSchema()
value_fetch_meta_schema = ValueFetchMetaSchema()
value_merge_meta_schema = ValueMergeMetaSchema()
value_convert_meta_schema = ValueConvertMetaSchema()
value_fabric_meta_schema = ValueFabricMetaSchema()
value_row_lineage_schema = ValueRowLineageSchema()
value_lineage_schema = ValueLineageSchema()
value_lineage_stage_schema = ValueLineageStageSchema()
