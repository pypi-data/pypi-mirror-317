from caasm_aql.query_builders.converter import Converter
from caasm_meta_model.service.entities.meta_model import MetaFieldType


class EnumConverter(Converter):
    _enum_rule = "enum"

    def convert(self, value, field):
        enum_rule = {}
        for rule in field.rules:
            if rule.name == self._enum_rule:
                enum_rule = rule.setting

        if isinstance(value, int):
            return value
        return enum_rule.get(value, None)

    @property
    def available_types(self):
        return [MetaFieldType.ENUM]
