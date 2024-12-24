from typing import List

from IPy import IP

from caasm_aql.query_builders.converter import Converter
from caasm_meta_model.service.entities.meta_model import MetaFieldType


class IpConverter(Converter):
    def convert(self, value, field):
        return IP(value).strFullsize()

    @property
    def available_types(self) -> List[MetaFieldType]:
        return [MetaFieldType.IP, MetaFieldType.IPV4, MetaFieldType.IPV6]
