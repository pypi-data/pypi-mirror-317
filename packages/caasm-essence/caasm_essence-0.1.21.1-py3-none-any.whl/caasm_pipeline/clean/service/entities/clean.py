from dataclasses import dataclass
from datetime import datetime
from typing import List

from bson import ObjectId
from caasm_persistence_base.entity.base import DocumentEntity, BaseEntity

from caasm_pipeline.clean.service.constants.clean import AdapterProcessStatus, CleanType
from caasm_pipeline.service.constants.common import Sorting


@dataclass
class CleanRecordEntity(DocumentEntity):
    adapter_name: str
    index: int
    latest: bool
    data_deleted: bool
    category: str
    status: AdapterProcessStatus
    start_time: datetime
    finish_time: datetime
    #   指向的转换表
    convert_table: str


@dataclass
class CleanRuleEntity(DocumentEntity):
    #   规则名称
    name: str
    #   实体大类
    category: str
    #   资产类型
    entity_type: str
    #   过滤类型
    clean_type: CleanType
    #   描述信息
    description: str
    #   如果是去重
    #   逻辑主键字段列表
    field_names: List[str]
    #   排序字段
    sort_field: str
    #   排序方法
    sorting: Sorting
    #   如果是过滤
    #   过滤语句
    filter_asql: str


@dataclass
class CleanRuleTrendEntity(BaseEntity):
    date: str
    count: int


@dataclass
class AdapterCleanRuleEntity(DocumentEntity):
    #   适配器规则名称
    name: str
    #   适配器名称
    adapter_name: str
    #   规则ID
    rule_id: ObjectId
    #   是否启用
    enabled: bool
    #   是否被引用
    is_referenced: bool
    #   趋势
    trends: List[CleanRuleTrendEntity]


#   被清洗的数据对应的规则
@dataclass
class CleanDataRuleEntity(DocumentEntity):
    #   数据ID
    data_id: ObjectId
    #   规则ID
    rule_id: ObjectId
