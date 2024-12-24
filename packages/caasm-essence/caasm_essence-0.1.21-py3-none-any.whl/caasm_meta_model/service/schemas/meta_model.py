from caasm_persistence_base.schema.base import EnumField, ObjectIdField, DocumentNoneSchema
from marshmallow import fields

from caasm_meta_model.service.entities.meta_model import Rule, MetaField, MetaFieldType, MetaModel, MetaModelType


class RuleSchema(DocumentNoneSchema):
    entity_define = Rule

    name = fields.String(description="规则名称", load_default=None)
    display_name = fields.String(description="展示名称", load_default=None)
    setting = fields.Dict(description="配置信息", load_default=None)


class MetaFieldSchema(DocumentNoneSchema):
    entity_define = MetaField

    name = fields.String(description="字段名称", load_default=None)
    display_name = fields.String(description="字段展示名称", load_default=None)
    description = fields.String(description="描述信息", load_default=None)
    type = EnumField(MetaFieldType, by_value=True, description="类型", load_default=None)
    required = fields.Boolean(description="是否必传", load_default=None)
    allow_null = fields.Boolean(description="是否为空", load_default=None)
    default = fields.Raw(description="默认值", load_default=None)
    encrypt = fields.Boolean(description="是否加密", load_default=None)
    encrypt_setting = fields.Dict(description="加密参数", load_default=None)
    internal = fields.Boolean(description="内置字段", load_default=None)
    unique = fields.Boolean(description="值唯一", load_default=None)
    model_id = ObjectIdField(description="模型ID", load_default=None)
    setting = fields.Dict(description="字段配置信息", load_default=None)
    children = fields.Nested("self", load_default=None, many=True)
    rules = fields.Nested(RuleSchema, load_default=None, many=True)
    hidden = fields.Boolean(description="是否隐藏字段", load_default=None)
    query = fields.String(description="查询", load_default=None)
    full_name = fields.String(description="全称", load_default=None)
    full_display_name = fields.String(description="展示全称", load_default=None)
    priority = fields.Int(description="优先级", load_default=None)
    is_complex = fields.Boolean(description="是否复杂字段", load_default=None)
    complex_full_name = fields.String(load_default=None)
    full_text_search = fields.Boolean(description="是否参与全文检索", load_default=None)
    is_monitor = fields.Boolean(description="是否监控", load_default=None)


class MetaModelSchema(DocumentNoneSchema):
    entity_define = MetaModel

    name = fields.String(description="模型名称", load_default=None)
    init = fields.Boolean(description="初始化", load_default=None)
    category = fields.String(description="标签", load_default=None)
    display_name = fields.String(description="展示名称", load_default=None)
    type = EnumField(MetaModelType, by_value=True, load_default=None)
    description = fields.String(description="描述信息", load_default=None)
    friends = fields.List(ObjectIdField(description="组合模型信息", load_default=None), load_default=None)
    internal = fields.Boolean(description="内置字段", load_default=None)
    setting = fields.Dict(description="配置信息", load_default=None)
    priority = fields.Int(description="优先级", load_default=None)
    logo_id = ObjectIdField(description="图标ID", load_default=None)
    logo_name = fields.String(description="图标名称", load_default=None)
