from caasm_entity.service.services.entity import EntityService
from caasm_entity.service.services.snapshot import SnapshotRecordService, MetaModelSnapshotRecordService, \
    MetaFieldSnapshotRecordService

entity_service = EntityService()
snapshot_record_service = SnapshotRecordService()
meta_model_snapshot_record_service = MetaModelSnapshotRecordService()
meta_field_snapshot_record_service = MetaFieldSnapshotRecordService()
