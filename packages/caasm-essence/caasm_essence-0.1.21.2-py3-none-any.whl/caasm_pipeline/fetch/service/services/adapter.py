import re

from caasm_service_base.schema.runtime import adapter_schema

from caasm_persistence.handler.storage.mongo import MongoHandler


class AdapterService(MongoHandler):
    DEFAULT_TABLE = "adapter"
    DEFAULT_SCHEMA = adapter_schema

    def modify_adapter(self, values, name=None, latest=True):
        condition = self.build_adapter_condition(name=name, latest=latest)
        return self.update_direct(condition=condition, values=values)

    def delete_adapter(self, name=None, names=None, latest=True):
        query = self.build_adapter_condition(name=name, names=names, latest=latest)
        return self.delete_multi(query)

    def get_adapter(self, name=None, fields=None, latest=True, **kwargs):
        query = self.build_adapter_condition(name=name, latest=latest)
        return self.get(query, adapter_schema, fields=fields, **kwargs)

    def get_adapter_count(self, name=None, latest=True, adapter_instance_exists=None):
        query = self.build_adapter_condition(name=name, adapter_instance_exists=adapter_instance_exists, latest=latest)
        return self.count(query)

    def find_adapter(
        self,
        name=None,
        display_name=None,
        names=None,
        ne_names=None,
        display_names=None,
        keyword=None,
        type=None,
        adapter_inner_type=None,
        adapter_inner_type_ne=None,
        is_biz_useful=None,
        fields=None,
        sort_fields=None,
        adapter_instance_exists=None,
        category=None,
        latest=True,
        **kwargs,
    ):
        condition = self.build_adapter_condition(
            names=names,
            display_name=display_name,
            display_names=display_names,
            keyword=keyword,
            type=type,
            adapter_inner_type=adapter_inner_type,
            adapter_inner_type_ne=adapter_inner_type_ne,
            name=name,
            is_biz_useful=is_biz_useful,
            adapter_instance_exists=adapter_instance_exists,
            category=category,
            ne_names=ne_names,
            latest=latest,
        )
        return self.find_list(condition=condition, fields=fields, sort_fields=sort_fields, **kwargs)

    def find_adapter_to_mapper(self, names=None, fields=None, latest=True):
        adapter_cursor = list(self.find_adapter(names=names, fields=fields, latest=latest))
        return {adapter.name: adapter for adapter in adapter_cursor}

    @classmethod
    def build_adapter_condition(
        cls,
        name=None,
        adapter_id=None,
        names=None,
        display_name=None,
        display_names=None,
        keyword=None,
        type=None,
        adapter_inner_type=None,
        adapter_inner_type_ne=None,
        is_biz_useful=None,
        category=None,
        adapter_instance_exists=None,
        ne_names=None,
        latest=None,
    ):
        condition = {}
        _name_condition = {}

        if adapter_instance_exists:

            from caasm_pipeline.fetch.service.runtime import adapter_instance_service
            tmp_names = adapter_instance_service.find_distinct("adapter_name")
            if names:
                names.extend(tmp_names)
            else:
                names = tmp_names

        if name:
            _name_condition["$eq"] = name
        if ne_names:
            _name_condition["$nin"] = ne_names

        if display_name:
            condition["display_name"] = display_name

        if adapter_id:
            condition["_id"] = cls._build_id(adapter_id)

        if names is not None:
            _name_condition["$in"] = names

        if display_names:
            condition["display_name"] = {"$in": display_names}

        if keyword:
            keyword_re = re.compile(keyword)
            condition["$or"] = [
                {
                    "display_name": {"$regex": keyword_re},
                },
                {"description": {"$regex": keyword_re}},
            ]

        if type:
            condition["type"] = type

        _a = {}
        if adapter_inner_type:
            _a["$eq"] = adapter_inner_type
        if adapter_inner_type_ne:
            _a["$ne"] = adapter_inner_type_ne
        if _a:
            condition["adapter_inner_type"] = _a

        if is_biz_useful is not None:
            condition["is_biz_useful"] = is_biz_useful

        if _name_condition:
            condition["name"] = _name_condition

        if category:
            condition[f"fetch_setting.fetch_type_mapper.{category}"] = {"$exists": True}

        if latest is not None:
            condition["latest"] = latest

        return condition
