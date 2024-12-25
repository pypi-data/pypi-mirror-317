import datetime
from dataclasses import dataclass

from bson import ObjectId
from caasm_persistence_base.entity.base import DocumentEntity
from caasm_service_base.constants.adapter import AdapterFetchStatus


@dataclass
class FetchRecord(DocumentEntity):
    adapter_name: str
    adapter_instance_id: ObjectId
    index: int
    status: AdapterFetchStatus
    finished: bool
    fetch_type: str
    fetch_count: int
    latest: bool
    err_info: str
    data_deleted: bool
    start_time: datetime.datetime
    finish_time: datetime.datetime
