from datetime import datetime, date

import pytz

from caasm_aql.query_builders.converter import Converter
from caasm_meta_model.service.entities.meta_model import MetaFieldType


class DateConverter(Converter):
    def convert(self, value, field):
        if isinstance(value, int) or isinstance(value, float):
            return datetime.fromtimestamp(value, pytz.timezone("Asia/Shanghai")).date().toordinal()
        elif isinstance(value, str):
            return date.fromisoformat(value).toordinal()
        else:
            raise ValueError("Invalid type of date.")

    @property
    def available_types(self):
        return [MetaFieldType.DATE]
