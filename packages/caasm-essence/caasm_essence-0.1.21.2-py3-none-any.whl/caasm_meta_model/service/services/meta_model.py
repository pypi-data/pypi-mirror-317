import re

from caasm_meta_model.service.schemas.runtime import meta_field_schema, meta_model_schema
from caasm_persistence.handler.storage.mongo import MongoHandler


class MetaFieldService(MongoHandler):
    DEFAULT_TABLE = "meta.field"
    DEFAULT_SCHEMA = meta_field_schema

    def find_meta_field(
        self,
        model_id=None,
        model_ids=None,
        field_ids=None,
        keyword=None,
        internal=None,
        fields=None,
        offset=None,
        limit=None,
        sort_fields=None,
    ):
        condition = self.build_query_condition(
            model_id=model_id, field_ids=field_ids, keyword=keyword, internal=internal, model_ids=model_ids
        )
        return self.find(condition, offset=offset, limit=limit, sort_fields=sort_fields, fields=fields)

    def get_meta_field(self, field_id=None, fields=None):
        condition = self.build_query_condition(field_id=field_id)
        return self.get(condition, fields=fields)

    def get_meta_field_count(self, model_id=None, keyword=None, internal=None):
        condition = self.build_query_condition(model_id=model_id, keyword=keyword, internal=internal)
        return self.count(condition)

    def delete_meta_field(self, field_ids=None, model_id=None, internal=None):
        condition = self.build_query_condition(field_ids=field_ids, model_id=model_id, internal=internal)
        return self.delete_multi(condition)

    def update_meta_field(self, field_id=None, internal=None, values=None):
        condition = self.build_query_condition(field_id=field_id, internal=internal)
        return self.update_direct(condition, values)

    @classmethod
    def build_query_condition(
        cls, model_id=None, keyword=None, internal=None, field_ids=None, model_ids=None, field_id=None
    ):
        condition = {}
        tmp_model_ids = []
        tmp_fields_ids = []

        if model_id:
            tmp_model_ids.append(model_id)

        if model_ids:
            tmp_model_ids.extend(model_ids)

        if field_id:
            tmp_fields_ids.append(field_id)

        if field_ids:
            tmp_fields_ids.extend(field_ids)

        if tmp_model_ids:
            condition["model_id"] = {"$in": cls._build_ids(tmp_model_ids)}
        if tmp_fields_ids:
            condition["_id"] = {"$in": cls._build_ids(tmp_fields_ids)}

        if internal is not None:
            condition["internal"] = internal

        if keyword:
            keyword_re = re.compile(keyword)
            condition["query"] = {"$regex": keyword_re}
        return condition


class MetaModelService(MongoHandler):
    DEFAULT_TABLE = "meta.model"
    DEFAULT_SCHEMA = meta_model_schema

    def find_total_meta_field(self, model_id=None, result=None, handled_id_set=None, meta_field_service=None):
        if result is None:
            result = []
            handled_id_set = set()
            meta_field_service = MetaFieldService()
        if model_id in handled_id_set:
            return []
        meta_model = self.get_meta_model(model_id=model_id)
        fields = list(meta_field_service.find_meta_field(model_id=meta_model.id))
        result.extend(fields)
        for friend in meta_model.friends:
            self.find_total_meta_field(friend, result, handled_id_set, meta_field_service)
        return result

    def get_meta_model(self, model_id=None, internal=None, model_type=None, name=None, fields=None, display_name=None):
        condition = self.build_query_condition(
            model_id=model_id, model_type=model_type, name=name, display_name=display_name, internal=internal
        )
        return self.get(condition, fields=fields)

    def update_meta_model(self, model_id=None, internal=None, values=None):
        condition = self.build_query_condition(model_id=model_id, internal=internal)
        return self.update_direct(condition, values)

    def get_meta_model_count(
        self, keyword=None, model_id=None, model_type=None, name=None, model_nid=None, internal=None, init=None
    ):
        condition = self.build_query_condition(
            keyword=keyword,
            model_id=model_id,
            model_type=model_type,
            name=name,
            model_nid=model_nid,
            internal=internal,
            init=init,
        )
        return self.count(condition)

    def find_meta_model(
        self,
        keyword=None,
        init=None,
        internal=None,
        names=None,
        model_type=None,
        model_ids=None,
        friends=None,
        category=None,
        fields=None,
        offset=None,
        limit=None,
        sort_fields=None,
    ):
        condition = self.build_query_condition(
            names=names,
            keyword=keyword,
            model_type=model_type,
            model_ids=model_ids,
            internal=internal,
            init=init,
            friends=friends,
            category=category,
        )
        return self.find(condition, fields=fields, offset=offset, limit=limit, sort_fields=sort_fields)

    def delete_meta_model(self, model_ids=None, model_type=None, init=None, internal=None):
        condition = self.build_query_condition(model_ids=model_ids, model_type=model_type, init=init, internal=internal)
        return self.delete_multi(condition)

    @classmethod
    def build_query_condition(
        cls,
        model_id=None,
        model_type=None,
        model_ids=None,
        display_name=None,
        name=None,
        model_nid=None,
        keyword=None,
        internal=None,
        init=None,
        friends=None,
        names=None,
        category=None,
    ):
        condition = {}
        tmp_model_ids = []

        if model_id:
            tmp_model_ids.append(model_id)
        if model_ids:
            tmp_model_ids.extend(model_ids)

        tmp_model_ids = cls._build_ids(tmp_model_ids)

        if model_nid:
            model_nid = cls._build_id(model_nid)
            if tmp_model_ids:
                tmp_model_ids.remove(model_id)

        if model_type:
            condition["type"] = model_type
        if tmp_model_ids:
            condition["_id"] = {"$in": cls._build_ids(tmp_model_ids)}
        if display_name:
            condition["display_name"] = display_name
        if name:
            condition["name"] = name
        if model_nid and not tmp_model_ids:
            condition["_id"] = {"$ne": cls._build_id(model_nid)}

        if keyword:
            keyword_reg = re.compile(keyword)
            condition["$or"] = [{"display_name": {"$regex": keyword_reg}}, {"description": {"$regex": keyword_reg}}]
        if internal is not None:
            condition["internal"] = internal
        if init is not None:
            condition["init"] = init
        if friends:
            condition["friends"] = {"$in": cls._build_ids(friends)}
        if names:
            condition["name"] = {"$in": names}

        if category:
            condition["category"] = category
        return condition
