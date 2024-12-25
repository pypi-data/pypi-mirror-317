import datetime
from dataclasses import dataclass
from typing import List

from caasm_persistence_base.entity.base import DocumentEntity, ObjectId

from caasm_entity.service.constants.snapshot import SnapshotRecordStatus
from caasm_meta_model.service.entities.meta_model import MetaField


@dataclass
class SnapshotRecord(DocumentEntity):
    size: int
    date: str
    status: SnapshotRecordStatus
    start_time: datetime.datetime
    finish_time: datetime.datetime
    latest: bool
    finished: bool
    deleted: bool


@dataclass
class MetaFieldSnapshotRecord(DocumentEntity):
    model_id: ObjectId
    date: str
    meta_fields: List[MetaField]


@dataclass
class MetaModelSnapshotRecord(DocumentEntity):
    category: str
    date: str
    meta_model_ids: List[ObjectId]
