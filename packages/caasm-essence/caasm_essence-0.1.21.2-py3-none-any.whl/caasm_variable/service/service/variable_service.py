import re

from caasm_persistence.handler.storage.mongo import MongoHandler
from caasm_variable.service.entity.variable import Variable
from caasm_variable.service.schema.runtime import variable_schema


class VariableService(MongoHandler):
    DEFAULT_TABLE = "variable"
    DEFAULT_SCHEMA = variable_schema

    def get_all_variables(
        self,
        keyword=None,
        ids=None,
        name=None,
        data_type=None,
        value=None,
        description=None,
        offset=None,
        limit=None,
        sort_fields=None,
    ):
        query = self.build_condition(
            keyword=keyword, ids=ids, name=name, data_type=data_type, value=value, description=description
        )
        return self.find(query, sort_fields=sort_fields, limit=limit, offset=offset)

    def get_count(self, keyword=None, ids=None, name=None, data_type=None, value=None, description=None):
        query = self.build_condition(
            keyword=keyword, ids=ids, name=name, data_type=data_type, value=value, description=description
        )
        return self.count(query)

    def get_variable(self, ids=None, name=None, data_type=None, value=None, description=None):
        query = self.build_condition(ids=ids, name=name, data_type=data_type, value=value, description=description)
        return self.get(condition=query)

    def add_variable(self, variable: Variable):
        return self.save(variable)

    def update_variable(self, variable: Variable):
        return self.update(variable, table=self.DEFAULT_TABLE, schema=self.DEFAULT_SCHEMA)

    def delete_variables(self, variable_ids=None):
        query = self.build_condition(ids=variable_ids)
        return self.delete_multi(query)

    @classmethod
    def build_condition(cls, keyword=None, ids=None, name=None, data_type=None, value=None, description=None):
        query = {}
        if keyword:
            keyword_re = re.compile(keyword)
            query["$or"] = [
                {"name": {"$regex": keyword_re}},
                {"data_type": {"$regex": keyword_re}},
                {"data_value": {"$regex": keyword_re}},
                {"description": {"$regex": keyword_re}},
            ]
        if name:
            query["name"] = name

        if data_type:
            query["data_type"] = data_type

        if value:
            query["data_value"] = value

        if description:
            query["description"] = description

        if ids:
            query["_id"] = {"$in": cls._build_ids(ids)}

        return query

    def add_aql_variable(self, name: str, data_type, value):
        variable = self.get_variable(name=name)
        if not variable:
            variable_instance = variable_schema.load(
                {
                    "name": name,
                    "data_type": data_type,
                    "value": value,
                }
            )
            self.save(variable_instance)

    def get_aql_variable(self, name: str) -> Variable:
        if name.startswith("#"):
            name = name[1:]
        if not name:
            raise ValueError("name")

        variable = self.get_variable(name=name)
        if not variable:
            raise Exception()
        return variable
