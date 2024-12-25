from caasm_persistence_base.schema.base import DocumentSchema, DateTimeField, ObjectIdField
from marshmallow import fields
from marshmallow.schema import BaseSchema
from marshmallow_enum import EnumField

from caasm_pipeline.clean.service.constants.clean import AdapterProcessStatus, CleanType
from caasm_pipeline.clean.service.entities.clean import CleanRecordEntity, CleanRuleEntity, CleanRuleTrendEntity, \
    AdapterCleanRuleEntity
from caasm_pipeline.service.constants.common import Sorting


class CleanRecordSchema(DocumentSchema):
    entity_define = CleanRecordEntity

    adapter_name = fields.String(required=True)
    index = fields.Integer(required=True)
    latest = fields.Boolean(required=False, load_default=False)
    data_deleted = fields.Boolean(required=False, load_default=False)
    category = fields.String(required=True)
    status = EnumField(AdapterProcessStatus, by_value=True)
    start_time = DateTimeField(required=False, load_default=None)
    finish_time = DateTimeField(required=False, load_default=None)
    convert_table = fields.String(required=False, load_default=None)


class CleanRuleSchema(DocumentSchema):
    entity_define = CleanRuleEntity

    #   规则名称
    name = fields.String(required=True)
    #   实体大类
    category = fields.String(required=True)
    #   资产类型
    entity_type = fields.String(required=True)
    #   过滤类型
    clean_type = EnumField(CleanType, by_value=True, allow_none=True)
    #   描述信息
    description = fields.String(required=False, load_default=None, allow_none=True)
    #   如果是去重
    #   字段列表
    field_names = fields.List(fields.String, load_default=list, required=False, allow_none=True)
    #   排序字段
    sort_field = fields.String(required=False, load_default=None, allow_none=True)
    #   排序方法
    sorting = EnumField(Sorting, by_value=True, load_default=Sorting.DESCENDING, required=False, allow_none=True)
    #   如果是过滤
    #   过滤语句
    filter_asql = fields.String(required=False, load_default=None, allow_none=True)


class CleanRuleTrendSchema(BaseSchema):
    entity_define = CleanRuleTrendEntity

    date = fields.String(required=True)
    count = fields.Integer(required=True)


class CleanAdapterRuleSchema(DocumentSchema):
    entity_define = AdapterCleanRuleEntity

    #   适配器规则名称
    name = fields.String(required=True)
    #   适配器名称
    adapter_name = fields.String(required=True)
    #   规则ID
    rule_id = ObjectIdField(required=False, load_default=None)
    #   是否启用
    enabled = fields.Boolean(required=False, load_default=True)
    #   是否引用
    is_referenced = fields.Boolean(required=False, load_default=False)
    #   趋势
    trends = fields.List(fields.Nested(CleanRuleTrendSchema), load_default=list)
