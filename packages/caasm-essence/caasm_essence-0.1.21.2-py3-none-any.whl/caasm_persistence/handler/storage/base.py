from typing import List, Dict

from caasm_persistence_base.entity.base import BaseEntity
from caasm_persistence_base.handler.storage.base import BasePersistenceHandler
from caasm_persistence_base.schema.base import BaseSchema
from caasm_tool.util import SingletonInstance


class BaseHandler(BasePersistenceHandler, metaclass=SingletonInstance):
    DEFAULT_SCHEMA = None

    def schema(self, schema=None):
        if not schema:
            schema = self.DEFAULT_SCHEMA

        if not schema:
            raise ValueError(f"{self.name} schema define error")
        return schema

    def load_entity(self, schema=None, **kwargs):
        schema = self.schema(schema)
        return schema.load(kwargs)

    def dump_mapper(self, entity, schema=None):
        schema = self.schema(schema)
        return schema.dump(entity)

    # #################### 对象实体是schema，本质上调用的还是直接处理的方法   ############
    def save(self, entity: BaseEntity, table=None, schema: BaseSchema = None, **kwargs):
        schema = self.schema(schema)
        mapper: Dict = schema.dump(entity)
        return self.save_direct(data=mapper, table=table, **kwargs)

    def save_multi(self, entities: List[BaseEntity], table=None, schema=None):
        schema = self.schema(schema)
        mappers: List[Dict] = schema.dump(entities, many=True)
        return self.save_multi_direct(mappers, table)

    def get(self, condition=None, schema=None, fields=None, table=None, **kwargs):
        schema = self.schema(schema)
        data = self.get_direct(condition, fields=fields, table=table)
        if not data:
            return None
        entry = schema.load(data)
        return entry.as_dict() if kwargs.get("dict_resp") else entry

    def find_list(self, *args, **kwargs):
        return list(self.find(*args, **kwargs))

    def find(
        self,
        condition=None,
        fields=None,
        sort_fields=None,
        offset=None,
        limit=None,
        table=None,
        schema=None,
        **kwargs,
    ):
        dict_resp = kwargs.pop("dict_resp", None)
        schema = self.schema(schema)
        cursor = self.find_direct(
            condition=condition,
            fields=fields,
            sort_fields=sort_fields,
            offset=offset,
            limit=limit,
            table=table,
            **kwargs,
        )

        for record in cursor:
            yield self._build_entry(schema, record, dict_resp)

    @classmethod
    def _build_entry(cls, schema, record, dict_resp=False):
        entry = schema.load(record)
        return entry.as_dict() if dict_resp else entry

    def update(self, entity: BaseEntity, table=None, schema=None, condition=None, **kwargs):
        mapper = self.dump_mapper(entity, schema)

        query = {"_id": mapper.pop("_id", None)}
        query.update(condition) if condition else ...

        return self.update_direct(query, mapper, table, **kwargs)

    def update_stream(self, entities: List[BaseEntity], table=None, schema=None, **kwargs):
        schema = self.schema(schema)
        mappers = schema.dump(entities, many=True)
        return self.update_stream_direct(mappers, table=table, **kwargs)
