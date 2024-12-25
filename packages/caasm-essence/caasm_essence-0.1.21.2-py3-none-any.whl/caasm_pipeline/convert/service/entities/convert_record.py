import datetime
from dataclasses import dataclass

from caasm_persistence_base.entity.base import DocumentEntity

from caasm_pipeline.convert.service.constants.convert_record import AdapterConvertStatus


@dataclass
class ConvertRecord(DocumentEntity):
    adapter_name: str
    index: int
    latest: bool
    data_deleted: bool
    fetch_type: str
    status: AdapterConvertStatus
    start_time: datetime.datetime
    finish_time: datetime.datetime
