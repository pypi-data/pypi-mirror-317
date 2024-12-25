import copy
from abc import ABC
from functools import cached_property

from caasm_aql.base import AqlOperatorCall
from caasm_aql.query_builders.operator import Operator
from caasm_meta_model.service.entities.meta_model import MetaFieldType, MetaField, TOTAL_META_FIELD_TYPES


class ESOperator(Operator, ABC):
    _CUSTOMER_DATE_TYPE_OPERATOR = [
        MetaFieldType.LIST, MetaFieldType.OBJECT, MetaFieldType.VERSION, MetaFieldType.ENUM, MetaFieldType.IP,
        MetaFieldType.IPV4,
    ]
    _UNAVAILABLE_SUB_TYPES = {
        MetaFieldType.LIST: {
            MetaFieldType.OBJECT
        }
    }

    @classmethod
    def field_name(cls, field):
        return field.full_name

    @classmethod
    def build_keyword_result(cls, field, call):
        return {"term": {cls.field_name(field): call.value}}

    def get_es_operator(self):
        return self._get_es_operator()

    def _get_es_operator(self):
        return self.get_operator.value

    def unavailable_sub_data_types(self, data_type):
        return self._UNAVAILABLE_SUB_TYPES.get(data_type)

    def build_field_compare_result(self, field: MetaField, compare_field: MetaField):
        if field.complex_full_name:
            source_field: str = self.field_name(field)
            compare_field: str = self.field_name(compare_field)
            return {
                       "bool": {
                           "must": [
                               {
                                   "nested": {
                                       "path": field.complex_full_name,
                                       "query": {
                                           "bool": {
                                               "filter": {
                                                   "script": {
                                                       "script": f"""
            def v1 = null;
            if (doc['{source_field}'].size() != 0) {{
                v1 = doc['{source_field}'].value;
            }}                
            def v2 = null;
            if (doc['{compare_field}'].size() != 0) {{
                v2 = doc['{compare_field}'].value;
            }}
            if (v1 {self.get_es_operator()} v2) {{
                return true;
            }}
            return false
                                        """
                                                   }
                                               }
                                           }
                                       }
                                   }
                               }
                           ]
                       }
                   }, False
        else:
            field_name: str = self.field_name(field)
            compare_field: str = self.field_name(compare_field)
            return {
                       "bool": {
                           "filter": {
                               "script": {
                                   "script": f"""
    def v1 = null;
    if (doc['{field_name}'].size() != 0) {{
        v1 = doc['{field_name}'].value;
    }}
    def v2 = null;
    if (doc['{compare_field}'].size() != 0) {{
        v2 = doc['{compare_field}'].value;
    }} 
    return v1 {self.get_es_operator()} v2;
                               """
                               }
                           }
                       }
                   }, False

    def build(self, field, call: AqlOperatorCall) -> (dict, bool):
        result = self.build_keyword_result(field, call)
        if not result:
            return None, False

        if field.complex_full_name:
            result = {
                "nested": {
                    "path": field.complex_full_name,
                    "query": {"bool": {"must": [result]}},
                }
            }
        return result, False

    @cached_property
    def available_data_types(self) -> list:
        data_types = copy.deepcopy(TOTAL_META_FIELD_TYPES)

        for i in self._CUSTOMER_DATE_TYPE_OPERATOR:
            data_types.remove(i)
        return data_types
