from datetime import datetime, timedelta

import pytz

from caasm_aql.query_builders.function import Function


class TimeAgoFunction(Function):
    def call(self, value_list: list):
        for value in value_list:
            if not isinstance(value, int):
                raise ValueError()
        return (
            datetime.now(pytz.timezone("Asia/Shanghai"))
            + timedelta(
            weeks=value_list[0],
            days=value_list[1],
            hours=value_list[2],
            minutes=value_list[3],
            seconds=value_list[4],
        )
        ).timestamp()

    @property
    def name(self) -> str:
        return "time_ago"

    @property
    def order(self) -> int:
        return 5

    @property
    def get_param_types(self):
        return [
            MetaDataType.INT,
            MetaDataType.INT,
            MetaDataType.INT,
            MetaDataType.INT,
            MetaDataType.INT,
        ]

    @property
    def get_result_type(self):
        return MetaDataType.DATETIME
