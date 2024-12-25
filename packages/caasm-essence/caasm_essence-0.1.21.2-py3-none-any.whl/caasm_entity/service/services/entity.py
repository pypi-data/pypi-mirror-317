import datetime
import time
from datetime import time

from caasm_tool.constants import DATE_FORMAT
from caasm_tool.util import get_random_number

from caasm_meta_model.service.constants.constants import CategoryType
from caasm_persistence.handler.storage.es import ESHandler


class EntityServiceRegistry:
    def __init__(self):
        self.category_types = {}

    def register_category_type(self, category, category_type: CategoryType):
        self.category_types[category] = category_type

    def get_category_type(self, category):
        return self.category_types.get(category)


class EntityService(ESHandler):

    @classmethod
    def get_id(cls):
        return f"{int(time.time() * 1000)}{get_random_number()}"

    @classmethod
    def build_snapshot_table(cls, table_flag, date=None):
        date = date or datetime.date.today().strftime(DATE_FORMAT)
        return f"snapshot.{table_flag}.{date}"

    @classmethod
    def build_tmp_table(cls, table):
        return f"{table}{cls.get_id()}"

    def get_category_size(self, category, date=None):
        table = self.get_table(category, date)
        return self.get_size(table)

    @classmethod
    def get_table(cls, category, date=None, unique_finished=True):
        from caasm_service.runtime import snapshot_record_service

        if CATEGORY_TYPE_MAPPING.get(category) == CategoryType.SNAPSHOT:
            date = date or snapshot_record_service.get_latest_useful_date()
            if date:
                return f"{category}.{date}"
            return None
        else:
            from caasm_service.runtime import unique_index_service

            if unique_finished:
                index_name: str = unique_index_service.get_index_name(category)
            else:
                index_name: str = unique_index_service.get_unfinished_index(category)
            if not index_name:
                index_name = category
            return index_name

    def get_no_snapshot_table(cls, category, date=None, unique_finished=True):
        if CATEGORY_TYPE_MAPPING.get(category) == CategoryType.SNAPSHOT:
            if date:
                return f"{category}.{date}"
            return None
        else:
            from caasm_service.runtime import unique_index_service

            if unique_finished:
                index_name: str = unique_index_service.get_index_name(category)
            else:
                index_name: str = unique_index_service.get_unfinished_index(category)
            if not index_name:
                index_name = category
            return index_name

    @classmethod
    def is_unique(cls, category):
        return CATEGORY_TYPE_MAPPING.get(category) == CategoryType.UNIQUE

    def find_entity(
        self,
        category,
        condition=None,
        date=None,
        limit=None,
        offset=None,
        search_after=None,
        fields=None,
        sort_fields=None,
        need_ori_response=False,
        unique_finished=True,
    ):
        table = self.get_table(category, date=date, unique_finished=unique_finished)
        return self.find_direct(
            limit=limit,
            offset=offset,
            search_after=search_after,
            fields=fields,
            table=table,
            sort_fields=sort_fields,
            need_ori_response=need_ori_response,
            condition=condition,
        )

    def aggr_search(self, category=None, date=None, **kwargs):
        table = self.get_table(category, date, unique_finished=True)
        return self.options().search(index=self.table(table), **kwargs)

    def find_entity_loop(self, category, date=None, condition=None, limit=50, fields=None):
        offset = 0
        result = []

        while True:
            data = self.find_entity(category, date=date, condition=condition, offset=offset, limit=limit, fields=fields)
            if not data:
                break
            result.extend(data)
            offset += limit

        return result

    def update_entity_stream_direct(self, category, date, records, unique_finished=True):
        return self.update_stream_direct(records, table=self.get_table(category, date, unique_finished))

    def refresh_entity(self, category, date=None, unique_finished=True):
        return self.refresh(self.get_table(category, date, unique_finished))

    def get_entity(self, category, field_name, field_value, date=None, fields=None, unique_finished=True):
        query = {"term": {field_name: field_value}}
        table = self.get_table(category, date, unique_finished)
        return self.get_direct(query, table=table, fields=fields)

    def get_entity_count(self, category, field_name, field_value, date=None, unique_finished=True):
        query = {"term": {field_name: field_value}}
        table = self.get_table(category, date, unique_finished=unique_finished)
        return self.count(query, table=table)

    def get_entity_by_condition(self, category, date, condition, fields=None, unique_finished=True):
        table = self.get_table(category, date, unique_finished)
        return self.get_direct(condition, table=table, fields=fields)

    def drop_entity_table(self, category, date, unique_finished=True):
        return self.drop(table_name=self.get_table(category, date, unique_finished))

    def get_count(self, category, date, condition=None):
        return self.count(condition, table=self.get_table(category, date))

    @classmethod
    def ensure_table(cls, category):
        if CATEGORY_TYPE_MAPPING.get(category) == CategoryType.SNAPSHOT:
            return
        else:
            from caasm_service.runtime import unique_index_service

            existing_index = unique_index_service.get_index_name(category, True)
            if existing_index:
                return existing_index
            else:
                new_index = unique_index_service.begin_index(category, False)
                unique_index_service.finish_index(category)
                return new_index
