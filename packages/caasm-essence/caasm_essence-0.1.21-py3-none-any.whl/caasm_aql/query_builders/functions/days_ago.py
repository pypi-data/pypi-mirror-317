from datetime import datetime, timedelta

import pytz

from caasm_aql.query_builders.function import Function


class DaysAgoFunction(Function):
    def call(self, value_list: list):
        days = value_list[0]
        if not isinstance(days, int):
            raise ValueError()
        return (datetime.now(pytz.timezone("Asia/Shanghai")) + timedelta(days=-days)).date().toordinal()

    @property
    def name(self) -> str:
        return "days_ago"

    @property
    def order(self) -> int:
        return 1

    @property
    def get_param_types(self):
        return [MetaDataType.INT]

    @property
    def get_result_type(self):
        return MetaDataType.DATE
