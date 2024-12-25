from marshmallow import fields

from caasm_persistence_base.schema.base import DocumentNoneSchema, ObjectIdField

from caasm_meta_model.service.entities.asset_type import AssetType


class AssetTypeSchema(DocumentNoneSchema):
    entity_define = AssetType

    name = fields.Str(description="资产类型", load_default=None)
    display_name = fields.Str(description="展示名称", load_default=None)
    model_id = ObjectIdField(description="模型ID", load_default=None, allow_none=True)
    description = fields.Str(description="描述信息", load_default=None)
    internal = fields.Boolean(description="是否内置", load_default=None)
    format_names = fields.List(fields.Str(), description="格式化字段名称列表", load_default=None)
