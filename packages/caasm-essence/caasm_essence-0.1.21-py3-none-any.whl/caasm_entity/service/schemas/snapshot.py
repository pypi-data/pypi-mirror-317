from caasm_persistence_base.schema.base import fields, DocumentSchema, EnumField, ObjectIdField

from caasm_entity.service.constants.snapshot import SnapshotRecordStatus
from caasm_entity.service.entities.snapshot import SnapshotRecord, MetaFieldSnapshotRecord, MetaModelSnapshotRecord
from caasm_meta_model.service.schemas.meta_model import MetaFieldSchema


class SnapshotRecordSchema(DocumentSchema):
    entity_define = SnapshotRecord

    size = fields.Int(load_default=None)
    date = fields.Str(load_default=None)
    status = EnumField(SnapshotRecordStatus, by_value=True, load_default=None)
    start_time = fields.DateTime(load_default=None)
    finish_time = fields.DateTime(load_default=None)
    finished = fields.Boolean(load_default=False)
    latest = fields.Boolean(load_default=False)
    deleted = fields.Boolean(load_default=False)


class MetaFieldSnapshotRecordSchema(DocumentSchema):
    entity_define = MetaFieldSnapshotRecord

    model_id = ObjectIdField(load_default=None)
    date = fields.Str(load_default=None)
    meta_fields = fields.Nested(MetaFieldSchema, many=True, load_default=list)


class MetaModelSnapshotRecordSchema(DocumentSchema):
    entity_define = MetaModelSnapshotRecord

    category = fields.Str(load_default=None)
    date = fields.Str(load_default=None)
    meta_model_ids = fields.List(ObjectIdField, load_default=list)
