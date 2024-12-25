from caasm_persistence_base.schema.base import DocumentSchema
from marshmallow import fields

from caasm_variable.service.entity.variable import Variable


class VariableSchema(DocumentSchema):
    entity_define = Variable
    name = fields.Str(required=True, description="变量名称")
    description = fields.Str(required=False, description="变量描述信息")
    data_type = fields.Str(description="更新类型", load_default=None)
    data_value = fields.Raw(required=True, description="变量值")
