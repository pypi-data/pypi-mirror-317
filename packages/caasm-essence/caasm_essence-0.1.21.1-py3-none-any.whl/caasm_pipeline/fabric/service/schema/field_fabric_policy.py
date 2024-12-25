from caasm_persistence_base.schema.base import DocumentSchema, fields, ObjectIdField, BaseSchema
from caasm_pipeline.fabric.service.entity.fabric_meta_model_config import (
    AdapterConfidence,
    FieldGlobalPolicy,
)
from caasm_pipeline.fabric.service.entity.field_fabric_policy import FieldFabricPolicy


class AdapterConfidenceSchema(BaseSchema):
    entity_define = AdapterConfidence

    adapter_name = fields.String(description="适配器名称", load_default="")
    confidence = fields.Int(description="确信度", load_default=0)


class FieldGlobalPolicySchema(BaseSchema):
    entity_define = FieldGlobalPolicy

    value = fields.String(description="策略名称", load_default="")
    label = fields.String(description="策略名称", load_default="")
    policy_description = fields.String(description="策略描述", load_default="")


class FieldFabricPolicySchema(DocumentSchema):
    entity_define = FieldFabricPolicy

    fabric_config_id = ObjectIdField(description="配置ID", load_default=None)
    asset_type_id = ObjectIdField(description="资产类型ID", load_default=None)
    full_name = fields.String(description="字段名称", load_default=None)
    adapter_confidence = fields.List(fields.Nested(AdapterConfidenceSchema), load_default=None)
    fabric_policy = fields.List(fields.Nested(FieldGlobalPolicySchema), load_default=None)
