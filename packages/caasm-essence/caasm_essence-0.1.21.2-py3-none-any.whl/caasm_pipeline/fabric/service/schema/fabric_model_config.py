from marshmallow_enum import EnumField
from caasm_persistence_base.schema.base import (
    DocumentSchema,
    fields,
    ObjectIdField,
    BaseSchema,
    DateTimeField,
    TimeBaseNoneSchema,
)
from caasm_pipeline.fabric.service.entity.fabric_meta_model_config import (
    OneselfFieldPolicyEntity,
    UniqueIdentificationPolicy,
    AdapterConfidence,
    FieldGlobalPolicy,
    FieldPolicy,
    FabricModelConfig,
    FabricPolicy,
    FabricPolicyGroup,
    FieldPolicyConfig,
    FabricConfigEntity,
    OneselfFieldConfigEntity,
    FieldSourceEntity,
    FabricStageEntity,
)
from caasm_pipeline.fabric.service.constants.fabric import (
    FabricGlobalPolicyEnum,
    GlobalFieldPolicyEnum,
    OneselfFieldPolicyEnum,
    FabricCIDREnum,
)


class FabricPolicySchema(BaseSchema):
    entity_define = FabricPolicy

    name = fields.String(description="策略名称", load_default=None)
    src_field = fields.String(description="源字段", load_default=None)
    dst_field = fields.String(description="目的字段", load_default=None)
    setting = fields.Dict(description="配置信息", load_default=None)


class FieldSourceSchema(BaseSchema):
    entity_define = FieldSourceEntity

    name = fields.String(description="字段名称", load_default=None)
    display_name = fields.String(description="显示名称", load_default=None)
    type = fields.String(description="字段类型", load_default=None)


class FabricPolicyGroupSchema(BaseSchema):
    entity_define = FabricPolicyGroup

    name = EnumField(FabricGlobalPolicyEnum, description="策略", by_value=True, allow_none=True)
    src_field = fields.String(description="源字段", allow_none=True, load_default=None)
    src_fields = fields.List(fields.Nested(FieldSourceSchema), load_default=[])
    dst_field = fields.String(description="目的字段", load_default=None)
    cidr = EnumField(FabricCIDREnum, description="CIDR选项", load_default=FabricCIDREnum.MULTI_CIDR, allow_none=True)
    id_segment = fields.List(fields.String(description="IP内网网段"), load_default=[], allow_none=True)


class UniqueIdentificationPolicySchema(BaseSchema):
    entity_define = UniqueIdentificationPolicy

    policy_label = fields.String(description="策略名称", load_default="")
    policy_value = fields.String(description="策略值", load_default="")
    policy = fields.List(fields.String(description="策略方法或字段ID"), load_default=list)


class AdapterConfidenceSchema(BaseSchema):
    entity_define = AdapterConfidence

    adapter_name = fields.String(description="适配器名称", load_default="")
    confidence = fields.Int(description="确信度", load_default=0)


class FieldGlobalPolicySchema(BaseSchema):
    entity_define = FieldGlobalPolicy

    label = fields.String(description="策略名称,用于展示", load_default="选择策略")
    value = EnumField(GlobalFieldPolicyEnum, description="策略", load_default=GlobalFieldPolicyEnum.ELECT, by_value=True)
    policy_description = fields.String(description="策略描述", load_default="")


class FieldPolicySchema(BaseSchema):
    entity_define = FieldPolicy

    field_id = fields.String(description="字段ID", load_default=None)
    field_adapter_confidence = fields.List(fields.Nested(AdapterConfidenceSchema), load_default=list)
    field_policy = fields.List(fields.Nested(FieldGlobalPolicySchema), load_default=list)


class FabricModelConfigSchema(DocumentSchema):
    entity_define = FabricModelConfig

    asset_type_id = ObjectIdField(description="资产类型ID")
    is_modify = fields.Bool(description="是否修改", load_default=False)
    modify_time = DateTimeField(load_default=None, description="修改时间")
    modify_username = fields.String(description="修改用户名", load_default=None)
    fabric_policy = fields.Nested(FabricPolicySchema, load_default=None, allow_none=True)
    adapter_confidence = fields.List(fields.Nested(AdapterConfidenceSchema), load_default=None, allow_none=True)
    field_global_policy = fields.List(fields.Nested(FieldGlobalPolicySchema), load_default=None, allow_none=True)


class FieldGlobalConfigSchema(BaseSchema):
    entity_define = FieldPolicyConfig

    adapter = fields.List(fields.Nested(AdapterConfidenceSchema), load_default=[], allow_none=True)
    policy = fields.Nested(FieldGlobalPolicySchema, load_default=None, allow_none=True)


class OneselfFiledPolicySchema(BaseSchema):
    entity_define = OneselfFieldPolicyEntity

    label = fields.String(description="策略名称", required=False, allow_none=True)
    value = EnumField(
        OneselfFieldPolicyEnum,
        by_value=True,
        description="策略类型",
        allow_none=True,
        load_default=OneselfFieldPolicyEnum.ELECT,
    )
    policy_description = fields.String(description="策略描述", required=False, allow_none=True)


class FieldOneselfConfigSchema(TimeBaseNoneSchema):
    entity_define = OneselfFieldConfigEntity

    type = fields.String(description="类型", load_default=None, allow_none=True)
    type_name = fields.String(description="类型名称", load_default=None, allow_none=True)
    internal = fields.Bool(description="是否内置", load_default=True, allow_none=True)
    name = fields.String(description="显示名称", allow_none=False)
    full_name = fields.String(allow_none=False)
    description = fields.String(description="描述信息", load_default="", allow_none=True)
    equation = fields.String(load_default=None, allow_none=True)
    adapter = fields.List(fields.Nested(AdapterConfidenceSchema), load_default=[], allow_none=True)
    policy = fields.Nested(OneselfFiledPolicySchema, load_default=None, allow_none=True)


class FabricStageSchema(BaseSchema):
    entity_define = FabricStageEntity

    stage_id = ObjectIdField(description="阶段ID")
    stage_name = fields.String(description="阶段名称", load_default=None, allow_none=True)


class FabricConfigSchema(DocumentSchema):
    entity_define = FabricConfigEntity

    master_id = ObjectIdField(description="主阶段ID", load_default=None, allow_none=True)
    stage_name = fields.String(description="阶段名称", load_default=None, allow_none=True)
    asset_type_id = ObjectIdField(description="资产类型ID")
    asset_type = fields.String(description="资产类型", load_default=None, allow_none=True)
    is_modify = fields.Bool(description="是否修改", load_default=False, allow_none=True)
    modify_time = DateTimeField(load_default=None, description="修改时间")
    modify_username = fields.String(description="修改用户名", load_default=None, allow_none=True)
    is_master = fields.Bool(description="是否融合主阶段", load_default=False)
    stage_ids = fields.List(ObjectIdField(description="阶段Ids"), load_default=[], allow_none=True)
    fabric_stages = fields.List(fields.Nested(FabricStageSchema), load_default=[], allow_none=True)
    fabric_policy = fields.Nested(FabricPolicyGroupSchema, load_default=None, allow_none=True)
    fabric_adapter = fields.List(fields.Nested(AdapterConfidenceSchema), load_default=None, allow_none=True)
    global_field_config = fields.Nested(FieldGlobalConfigSchema, load_default=None, allow_none=True)
    oneself_field_config = fields.List(fields.Nested(FieldOneselfConfigSchema), load_default=[], allow_none=True)
