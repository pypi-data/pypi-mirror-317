import datetime
import logging
from dataclasses import asdict
from typing import List

from caasm_tool.constants import DATE_FORMAT_1

from caasm_entity.service.constants.snapshot import SnapshotRecordStatus
from caasm_entity.service.schemas.runtime import (
    snapshot_schema,
    meta_field_snapshot_record_schema,
    meta_model_snapshot_record_schema,
)
from caasm_persistence.handler.storage.mongo import MongoHandler

log = logging.getLogger()


class MetaModelSnapshotRecordService(MongoHandler):
    DEFAULT_SCHEMA = meta_model_snapshot_record_schema
    DEFAULT_TABLE = "snapshot.meta_model"

    def delete_meta_model(self, date=None):
        condition = self.build_meta_model_snapshot_record_condition(date=date)
        return self.delete_multi(condition)

    def get_meta_model(self, category=None, date=None):
        condition = self.build_meta_model_snapshot_record_condition(category=category, date=date)
        return self.get(condition)

    def save_meta_model_by_category(self, category, date):
        from caasm_meta_model.service.runtime import meta_model_service

        meta_models = meta_model_service.find_meta_model(category=category)
        meta_model_ids = []
        for meta_model in meta_models:
            meta_model_ids.append(meta_model.id)
            meta_model_ids.extend(meta_model.friends) if meta_model.friends else ...
        meta_model_ids = list(set(meta_model_ids))
        return self.save_meta_model(date, category, meta_model_ids)

    def save_meta_model(self, date, category, meat_model_ids):
        condition = self.build_meta_model_snapshot_record_condition(category=category, date=date)
        values = {"meta_model_ids": meat_model_ids}
        return self.update_direct(condition, values, upsert=True)

    @classmethod
    def build_meta_model_snapshot_record_condition(cls, category=None, date=None):
        condition = {}

        if category:
            condition["category"] = category
        if date:
            condition["date"] = date

        return condition


class MetaFieldSnapshotRecordService(MongoHandler):
    DEFAULT_SCHEMA = meta_field_snapshot_record_schema
    DEFAULT_TABLE = "snapshot.meta_field"

    def delete_meta_field(self, date=None):
        condition = self.build_meta_field_snapshot_record_condition(date=date)
        return self.delete_multi(condition)

    def get_meta_field(self, model_id=None, date=None):
        condition = self.build_meta_field_snapshot_record_condition(model_id=model_id, date=date)
        return self.get(condition)

    def find_meta_field(self, model_ids=None, date=None):
        condition = self.build_meta_field_snapshot_record_condition(model_ids=model_ids, date=date)
        return self.find(condition)

    def save_meta_field_by_category(self, category, date):
        from caasm_meta_model.service.runtime import meta_model_service
        from caasm_meta_model.service.runtime import meta_field_service

        models = meta_model_service.find_meta_model(category=category)
        for model in models:
            model_id = model.id
            fields = meta_model_service.find_total_meta_field(model_id=model_id)
            self.save_meta_field(date, model_id=model_id, meta_fields=fields)

            friends = model.friends or []
            for friend in friends:
                meta_fields = meta_field_service.find_meta_field(model_id=friend)
                self.save_meta_field(date, friend, meta_fields)

    def save_meta_field(self, date, model_id, meta_fields):
        condition = self.build_meta_field_snapshot_record_condition(model_id=model_id, date=date)
        meta_fields = [asdict(meta_field) for meta_field in meta_fields]
        values = {"meta_fields": meta_fields}
        return self.update_direct(condition, values, upsert=True)

    @classmethod
    def build_meta_field_snapshot_record_condition(cls, model_id=None, model_ids=None, date=None):
        condition = {}
        _id_condition = {}

        if model_id:
            _id_condition["$eq"] = cls._build_id(model_id)
        if model_ids:
            _id_condition["$in"] = cls._build_ids(model_ids)

        if _id_condition:
            condition["_id"] = _id_condition

        if date:
            condition["date"] = date

        return condition


class SnapshotRecordService(MongoHandler):
    DEFAULT_TABLE = "snapshot.record"
    DEFAULT_SCHEMA = snapshot_schema
    _FINISH_STATUSES = (SnapshotRecordStatus.SUCCESS, SnapshotRecordStatus.FAILED, SnapshotRecordStatus.CANCEL)
    _DATE_SORT_FIELDS = [("date", -1)]

    def __init__(self, client=None, database=None):
        super(SnapshotRecordService, self).__init__(client, database)
        self._entry_categories = []

    def register_entry_categories(self, entry_categories: List[str]):
        self._entry_categories = entry_categories

    def get_snapshot_record_count(self, deleted=None, latest=None):
        condition = self.build_snapshot_record_condition(deleted=deleted, latest=latest)
        return self.count(condition)

    def get_latest_useful_record(self):
        cursor = self.find_snapshot_record(deleted=False, latest=True, sort_fields=self._DATE_SORT_FIELDS, limit=1)
        snapshot_records = list(cursor)
        return snapshot_records[0] if snapshot_records else None

    def get_latest_useful_date(self):
        record = self.get_latest_useful_record()
        return record.date if record else None

    def modify_snapshot_record(self, record_ids=None, **kwargs):
        condition = self.build_snapshot_record_condition(record_ids=record_ids)
        return self.update_multi_direct(condition, values=kwargs)

    def get_dates(self, asc=True):
        if asc:
            sort = [("date", 1)]
        else:
            sort = [("date", -1)]
        cursor = self.find_snapshot_record(deleted=False, latest=True, sort_fields=sort)
        dates = []
        for snapshot_record in cursor:
            dates.append(snapshot_record.date) if snapshot_record.date not in dates else ...
        return dates

    def generate_snapshot_record(self):
        date = datetime.date.today().strftime(DATE_FORMAT_1)
        snapshot = self.load_entity(date=date, status=SnapshotRecordStatus.DOING, start_time=self.now)
        snapshot.id = self.save(snapshot).inserted_id
        return self.dump_mapper(snapshot)

    def get_or_create_snapshot_record(self):
        record = self.get_latest_useful_record()
        return self.dump_mapper(record) if record else self.get_latest_useful_record()

    def get_latest_useful_date_of_category(self, category):
        dates = self.get_dates(asc=False)
        latest_date = None
        if dates:
            for date in dates:
                from caasm_entity.service.runtime import entity_service

                if entity_service.exists(entity_service.get_table(category, date)):
                    latest_date = date
                    break
        else:
            return
        return latest_date

    def find_snapshot_record(
        self,
        deleted=None,
        latest=None,
        date_lte=None,
        date_ne=None,
        offset=None,
        limit=None,
        sort_fields=None,
        finished=None,
    ):
        q = self.build_snapshot_record_condition(
            deleted=deleted,
            latest=latest,
            date_lte=date_lte,
            finished=finished,
            date_ne=date_ne,
        )
        return self.find(condition=q, offset=offset, limit=limit, sort_fields=sort_fields)

    def delete_snapshot_record(self, record_id=None):
        condition = self.build_snapshot_record_condition(record_id=record_id)
        return self.delete_one(condition)

    def start_snapshot(self, record_id):
        values = {"start_time": self.now, "status": SnapshotRecordStatus.DOING}
        condition = self.build_snapshot_record_condition(record_id, status=SnapshotRecordStatus.INIT)
        return self.update_direct(condition, values)

    def finish_snapshot(self, record_id, status):
        if status not in self._FINISH_STATUSES:
            log.warning(f"RecordId({record_id}) status({status}) is not allowed finishing")
            return

        snapshot_record = self.get_snapshot(record_id)
        if not snapshot_record:
            return

        size = self._get_snapshot_size(snapshot_record)

        if status == SnapshotRecordStatus.SUCCESS:
            condition = self.build_snapshot_record_condition(date=snapshot_record.date, latest=True)
            self.update_multi_direct(condition=condition, values={"latest": False})

        condition = self.build_snapshot_record_condition(record_id=record_id, status=SnapshotRecordStatus.DOING)
        values = {
            "status": status,
            "finished": True,
            "finish_time": self.now,
            "latest": True if status == SnapshotRecordStatus.SUCCESS else False,
            "size": size,
        }
        return self.update_direct(condition, values)

    def get_snapshot(self, record_id=None):
        condition = self.build_snapshot_record_condition(record_id)
        return self.get(condition)

    def _get_snapshot_size(self, snapshot_record):
        size = 0
        from caasm_entity.service.runtime import entity_service
        
        for category in self._entry_categories:
            size += entity_service.get_category_size(category, snapshot_record.date)
        return size

    @classmethod
    def build_snapshot_record_condition(
        cls,
        record_id=None,
        record_ids=None,
        status=None,
        status_nin=None,
        date_lte=None,
        date=None,
        latest=None,
        deleted=None,
        finished=None,
        date_ne=None,
    ):
        condition = {}

        _status_condition = {}
        _id_condition = {}
        _create_time_condition = {}
        _date_condition = {}

        if record_id:
            _id_condition["$eq"] = cls._build_id(record_id)
        if record_ids:
            _id_condition["$in"] = cls._build_ids(record_ids)

        if date_lte:
            _date_condition["$lte"] = date_lte
        if date:
            _date_condition["$eq"] = date
        if date_ne:
            _date_condition["$ne"] = date_ne

        if status:
            _status_condition["$eq"] = status
        if status_nin:
            _status_condition["$nin"] = status_nin
        if _id_condition:
            condition["_id"] = _id_condition
        if _status_condition:
            condition["status"] = _status_condition
        if _date_condition:
            condition["date"] = _date_condition
        if latest is not None:
            condition["latest"] = latest
        if deleted is not None:
            condition["deleted"] = deleted
        if finished is not None:
            condition["finished"] = finished
        return condition
