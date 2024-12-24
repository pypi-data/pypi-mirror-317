import re

from caasm_meta_model.service.schemas.runtime import asset_type_schema
from caasm_persistence.handler.storage.mongo import MongoHandler


class AssetTypeService(MongoHandler):
    DEFAULT_SCHEMA = asset_type_schema
    DEFAULT_TABLE = "asset_type"

    def find_asset_type(
        self,
        offset=None,
        limit=None,
        model_ids=None,
        asset_type_ids=None,
        name=None,
        model_id=None,
        need_unknown_type=None,
        internal=None,
        keyword=None,
        fields=None,
        sort_fields=None,
        names=None,
    ):
        query = self.build_asset_type_condition(
            name=name,
            model_id=model_id,
            model_ids=model_ids,
            internal=internal,
            keyword=keyword,
            need_unknown_type=need_unknown_type,
            asset_type_ids=asset_type_ids,
        )
        return self.find(
            condition=query,
            offset=offset,
            limit=limit,
            fields=fields,
            sort_fields=sort_fields,
        )

    def save_asset_type(
        self,
        name,
        display_name=None,
        model_id=None,
        internal=None,
        description=None,
        format_names=None,
    ):
        entity = self.load_entity(
            name=name,
            model_id=model_id,
            internal=internal,
            description=description,
            display_name=display_name,
            format_names=format_names,
        )
        return self.save(entity)

    def get_asset_type(
        self,
        model_id=None,
        asset_type_id=None,
        name=None,
        fields=None,
        internal=None,
        display_name=None,
    ):
        condition = self.build_asset_type_condition(
            model_id=model_id,
            asset_type_id=asset_type_id,
            name=name,
            display_name=display_name,
            internal=internal,
        )
        return self.get(condition, fields=fields)

    def get_asset_type_count(self, keyword=None, asset_type_id=None, need_unknown_type=None):
        condition = self.build_asset_type_condition(
            keyword=keyword,
            need_unknown_type=need_unknown_type,
            asset_type_id=asset_type_id,
        )
        return self.count(condition)

    def update_asset_type_info(
        self,
        asset_type_id=None,
        display_name=None,
        model_id=None,
        description=None,
        format_names=None,
    ):
        condition = self.build_asset_type_condition(asset_type_id=asset_type_id)
        values = {
            "display_name": display_name,
            "model_id": model_id,
            "description": description,
        }
        if format_names is not None:
            values["format_names"] = format_names
        return self.update_multi_direct(condition=condition, values=values)

    def delete_asset_type(self, asset_type_id):
        condition = self.build_asset_type_condition(asset_type_id=asset_type_id)
        return self.delete_one(condition)

    @classmethod
    def build_asset_type_condition(
        cls,
        name=None,
        keyword=None,
        model_ids=None,
        model_id=None,
        internal=None,
        description=None,
        need_unknown_type=None,
        asset_type_id=None,
        asset_type_ids=None,
        display_name=None,
        names=None,
    ):
        condition = {}

        tmp_model_ids = []
        tmp_asset_type_ids = []

        if asset_type_id:
            tmp_asset_type_ids.append(asset_type_id)

        if asset_type_ids:
            tmp_asset_type_ids.extend(asset_type_ids)

        if model_ids:
            tmp_model_ids.extend(cls._build_ids(model_ids))

        if model_id:
            tmp_model_ids.append(cls._build_id(model_id))

        if name:
            condition["name"] = name

        if description:
            condition["description"] = description

        if display_name:
            condition["display_name"] = display_name

        if internal:
            condition["internal"] = internal

        if tmp_asset_type_ids:
            condition["_id"] = {"$in": cls._build_ids(tmp_asset_type_ids)}

        if tmp_model_ids:
            if not need_unknown_type:
                condition["model_id"] = {"$in": cls._build_ids(tmp_model_ids)}
            else:
                condition["$or"] = [
                    {"model_id": {"$in": cls._build_ids(tmp_model_ids)}},
                    {"model_id": {"$exists": False}},
                ]
        else:
            if need_unknown_type:
                condition["model_id"] = {"$exists": False}
            elif need_unknown_type is False:
                condition["model_id"] = {"$exists": True}
        if keyword:
            keyword_re = re.compile(keyword)
            meta_model_cursor = MetaModelService().find_meta_model(keyword=keyword, fields=["_id"])
            or_condition = condition.pop("$or", [])
            or_condition.extend(
                [
                    {"display_name": {"$regex": keyword_re}},
                    {"description": {"$regex": keyword_re}},
                    {"model_id": {"$in": [i.id for i in meta_model_cursor]}},
                ]
            )

            condition["$or"] = or_condition
        if names:
            condition["name"] = {"$in": list(set(names))}

        return condition
