from abc import ABC
from typing import Dict, List

from caasm_tool.util import extract

from caasm_aql.filter.filter import AsqlFilter
from caasm_meta_model.service.entities.meta_model import MetaField


class FieldFilter(AsqlFilter, ABC):
    def __init__(self):
        self._meta_field: MetaField = None
        self._complex_full_name = None
        self._complex_field = None
        self._sub_field_name = None

    def set_meta_field(self, field_name: str, meta_fields: Dict[str, MetaField], parent_field_name=None):
        if parent_field_name:
            full_field_name = f"{parent_field_name}.{field_name}"
        else:
            full_field_name = field_name
        self._meta_field = meta_fields[full_field_name]
        self._complex_full_name = self._meta_field.complex_full_name
        if self._complex_full_name:
            self._complex_field = meta_fields[self._complex_full_name]
            sub_field_name = full_field_name.replace(self._complex_full_name, "")
            self._sub_field_name = sub_field_name[1:]

    def _extract_value(self, record):
        if self._complex_full_name:
            complex_value = extract(record, self._complex_full_name)
            if complex_value is None:
                return None
            if isinstance(complex_value, List):
                result = []
                for item in complex_value:
                    if isinstance(item, Dict):
                        value = extract(item, self._sub_field_name)
                        if value is None:
                            continue
                        result.append(value)
                return result or None
            else:
                return None
        else:
            return extract(record, self._meta_field.full_name)
