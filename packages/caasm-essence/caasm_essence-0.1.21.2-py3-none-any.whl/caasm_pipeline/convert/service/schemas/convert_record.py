import datetime

from caasm_persistence_base.schema.base import DocumentSchema, DateTimeField
from marshmallow import fields
from marshmallow_enum import EnumField

from caasm_pipeline.convert.service.constants.convert_record import AdapterConvertStatus
from caasm_pipeline.convert.service.entities.convert_record import ConvertRecord


class ConvertRecordSchema(DocumentSchema):
    entity_define = ConvertRecord

    adapter_name = fields.String(description="适配器名称")
    index = fields.Int(description="索引")
    fetch_type = fields.String(load_default=None)
    latest = fields.Bool(load_default=True, description="最近标志位")
    data_deleted = fields.Bool(load_default=None)
    status = EnumField(
        AdapterConvertStatus,
        load_default=AdapterConvertStatus.WAIT,
        by_value=True,
        description="采集状态",
    )
    start_time = DateTimeField(load_default=datetime.datetime.now, allow_none=True, description="开始时间")
    finish_time = DateTimeField(load_default=None, allow_none=True, description="结束时间")
