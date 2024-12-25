import logging

import arrow

from caasm_aql.query_builders.converter import Converter
from caasm_meta_model.service.entities.meta_model import MetaFieldType
from caasm_tool.constants import DATETIME_FORMAT

log = logging.getLogger()


class DatetimeConverter(Converter):
    def convert(self, value, field):
        #   返回时间戳
        try:
            return arrow.get(value).datetime.strftime(DATETIME_FORMAT)
        except Exception as e:
            log.warning(f"datetime({value}) convert error({e})")
            raise ValueError("时间格式错误.")

    @property
    def available_types(self):
        return [MetaFieldType.DATETIME]
