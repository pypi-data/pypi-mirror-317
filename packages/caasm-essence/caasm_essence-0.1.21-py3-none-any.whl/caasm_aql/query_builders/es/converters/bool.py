from typing import List

from caasm_aql.query_builders.converter import Converter
from caasm_meta_model.service.entities.meta_model import MetaFieldType


class BooleanConverter(Converter):
    def convert(self, value, field):
        return bool(value)

    @property
    def available_types(self) -> List[MetaFieldType]:
        return [MetaFieldType.BOOLEAN]
