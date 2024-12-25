import datetime

from caasm_persistence_base.schema.base import DocumentSchema, ObjectIdField, DateTimeField
from caasm_service_base.constants.adapter import AdapterFetchStatus
from marshmallow import fields
from marshmallow_enum import EnumField

from caasm_pipeline.fetch.service.entities.fetch_record import FetchRecord


class FetchRecordSchema(DocumentSchema):
    entity_define = FetchRecord

    adapter_name = fields.String(description="适配器名称", load_default=None)
    adapter_instance_id = ObjectIdField(description="适配器实例ID", load_default=None)
    fetch_type = fields.String(load_default=None)
    index = fields.Int(description="索引", load_default=None, allow_none=None)
    finished = fields.Bool(description="是否结束", load_default=False)
    fetch_count = fields.Int(description="采集总数", load_default=0)
    status = EnumField(
        AdapterFetchStatus,
        load_default=AdapterFetchStatus.INIT,
        by_value=True,
        description="采集状态",
    )
    start_time = DateTimeField(load_default=datetime.datetime.now, allow_none=True, description="开始时间")
    latest = fields.Bool(load_default=False, description="最近的标志位")
    finish_time = DateTimeField(load_default=None, allow_none=True, description="结束时间")
    data_deleted = fields.Bool(load_default=None, description="数据是否被删除")
    err_info = fields.String(description="错误信息详情", allow_none=True, load_default=None)
