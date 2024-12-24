import logging
from collections import defaultdict
from typing import Dict

from caasm_tool.util import extract, deduplicate
from cachetools import TTLCache

from caasm_meta_model.service.entities.asset_type import AssetType
from caasm_meta_model.service.entities.meta_model import MetaModel, MetaFieldType
from caasm_meta_model.service.runtime import meta_model_service, asset_type_service, meta_field_service

log = logging.getLogger()


_local_cache = TTLCache(100, 300)


class BaseQuery(object):
    _meta_model_field_names = ["friends"]
    _asset_type_field = "base.asset_type"
    _model_sort_fields = [("priority", 1)]
    _field_sort_fields = [("priority", 1)]
    _default_pk_field = "base.entity_id"
    _meta_view_default_field = ["pk_field"]

    @classmethod
    def get_asset_type(cls, entity):
        return cls.extract(entity, cls._asset_type_field)

    @classmethod
    def find_field_to_model_mapper(cls, category, date, entity_type=None):
        key = f"{category}:{date}:{entity_type}"
        value = _local_cache.get(key)
        if not value:
            meta_models, fields = cls.find_model_and_field(category, date=date, entity_type=entity_type)
            field_mapper = defaultdict(list)
            for field in fields:
                field_mapper[field.model_id].append(field)
            value = meta_models, {meta_model.id: field_mapper[meta_model.id] for meta_model in meta_models}
            if value:
                _local_cache[key] = value
        return value

    @classmethod
    def find_field_to_list(cls, category, entity_type=None):
        meta_models, fields = cls.find_model_and_field(category, entity_type=entity_type)
        return fields

    _FIND_FIELD_TO_MAPPER_KEY = "find_field_to_mapper"

    @classmethod
    def find_field_to_mapper(cls, category, use_snapshot=True, date="", entity_type=None, model_names=None):
        key = f"{cls._FIND_FIELD_TO_MAPPER_KEY}:{category}:{use_snapshot}:{date}:{entity_type}:{model_names}"
        value = _local_cache.get(key)
        if not value:
            meta_models, fields = cls.find_model_and_field(
                category, use_snapshot, date, entity_type=entity_type, model_names=model_names
            )
            value = {field.full_name: field for field in cls.open_up_field(fields)}
            _local_cache[key] = value
        return value

    @classmethod
    def find_model(cls, category, meta_model_ids=None, model_names=None):
        if not meta_model_ids:
            meta_models = meta_model_service.find_meta_model(
                category=category, sort_fields=cls._model_sort_fields, names=model_names
            )
            meta_model_ids = []
            for meta_model in meta_models:
                meta_model_ids.append(meta_model.id)
                meta_model_ids.extend(meta_model.friends) if meta_model.friends else ...
            meta_model_ids = deduplicate(meta_model_ids)
            if not meta_model_ids:
                return []
        cur = meta_model_service.find_meta_model(model_ids=meta_model_ids, sort_fields=cls._model_sort_fields)
        return list(cur)

    @classmethod
    def extract(cls, entity_data, field):
        return extract(entity_data, field)

    @classmethod
    def find_model_and_field(cls, category, use_snapshot=True, date="", entity_type=None, model_names=None):
        if model_names:
            meta_model_ids = list(model.id for model in meta_model_service.find_meta_model(names=model_names))
        else:
            meta_model_ids = []
            if entity_type is None:
                if use_snapshot and date:
                    _meta_model_snapshot = meta_model_snapshot_record_service.get_meta_model(category, date=date)
                    if not _meta_model_snapshot:
                        log.warning(f"Not found category({category}) date({date}) meta_model snapshot")
                    else:
                        meta_model_ids = _meta_model_snapshot.meta_model_ids
            else:
                asset_type_entity: AssetType = asset_type_service.get_asset_type(name=entity_type)
                if asset_type_entity:
                    meta_model_ids.append(asset_type_entity.model_id)
                    model: MetaModel = meta_model_service.get_meta_model(asset_type_entity.model_id)
                    if model:
                        meta_model_ids.extend(model.friends)

        meta_models = cls.find_model(category, meta_model_ids=meta_model_ids)
        if not meta_models:
            return [], []

        meta_model_ids = [meta_model.id for meta_model in meta_models]
        meta_model_id_flag = set(meta_model_ids)
        fields = []
        queried_snapshot_model_id_flag = set()

        if use_snapshot and date:
            meta_model_snapshots = meta_field_snapshot_record_service.find_meta_field(meta_model_ids, date=date)
            for meta_model_snapshot in meta_model_snapshots:
                queried_snapshot_model_id_flag.add(meta_model_snapshot.model_id)
        need_requery_model_ids = list(meta_model_id_flag - queried_snapshot_model_id_flag)
        if need_requery_model_ids:
            cur = meta_field_service.find_meta_field(
                model_ids=need_requery_model_ids, sort_fields=cls._field_sort_fields
            )
            fields.extend(list(cur))

        return meta_models, fields

    @classmethod
    def open_up_field(cls, fields, result=None):
        if result is None:
            result = []

        for field in fields:
            children = field.children
            field_type = field.type

            if field_type == MetaFieldType.LIST:
                if children and children[0].type == MetaFieldType.OBJECT:
                    children = children[0].children
                else:
                    children = []

            result.append(field)
            cls.open_up_field(children, result)
        return result

    @classmethod
    def find_fields_of_entity_type(cls, category, use_snapshot=True, date="", entity_type=None):
        category_view: Dict = category_view_service.get_view(category)
        common_models = list(
            meta_model_service.find_meta_model(sort_fields=cls._model_sort_fields, names=category_view["common_models"])
        )
        entity_meta_models = []
        if entity_type is not None:
            entity_meta_model_ids = []
            asset_type_entity: AssetType = asset_type_service.get_asset_type(name=entity_type)
            if asset_type_entity:
                entity_meta_model_ids.append(asset_type_entity.model_id)
                model: MetaModel = meta_model_service.get_meta_model(asset_type_entity.model_id)
                if model:
                    entity_meta_model_ids.extend(model.friends)
            for common_model_id in [model.id for model in common_models]:
                entity_meta_model_ids.remove(common_model_id)
            entity_meta_models = cls.find_model(category, meta_model_ids=entity_meta_model_ids)
        all_model_ids = set()
        common_model_ids = set()
        entity_model_ids = set()
        for model in common_models:
            common_model_ids.add(model.id)
            all_model_ids.add(model.id)
        for model in entity_meta_models:
            if model.id not in common_model_ids:
                entity_model_ids.add(model.id)
            all_model_ids.add(model.id)

        fields = []
        cur = meta_field_service.find_meta_field(model_ids=all_model_ids, sort_fields=cls._field_sort_fields)
        fields.extend(list(cur))

        common_fields = []
        entity_fields = []

        for field in fields:
            if field.model_id in common_model_ids:
                common_fields.append(field)
            else:
                entity_fields.append(field)

        common_fields_mapper = {field.full_name: field for field in cls.open_up_field(common_fields)}
        entity_fields_mapper = {field.full_name: field for field in cls.open_up_field(entity_fields)}
        fields_mapper = dict(**common_fields_mapper, **entity_fields_mapper)
        return fields_mapper, common_fields_mapper, entity_fields_mapper, fields, common_fields, entity_fields
