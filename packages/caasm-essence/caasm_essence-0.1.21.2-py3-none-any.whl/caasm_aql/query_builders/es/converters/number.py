from caasm_aql.query_builders.converter import Converter
from caasm_meta_model.service.entities.meta_model import MetaFieldType


class NumberConverter(Converter):
    def convert(self, value, field):
        return float(value)

    @property
    def available_types(self):
        return [MetaFieldType.FLOAT]
