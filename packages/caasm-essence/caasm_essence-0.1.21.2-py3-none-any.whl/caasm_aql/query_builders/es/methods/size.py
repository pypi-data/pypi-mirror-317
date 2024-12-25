from caasm_aql.base import AqlMethodCall
from caasm_aql.query_builders.method import Method
from caasm_meta_model.service.entities.meta_model import MetaFieldType


class SizeGreaterThanMethod(Method):
    def __init__(self):
        super(SizeGreaterThanMethod, self).__init__()
        self.add_param("size", "数量", "用于比较的数量", MetaFieldType.INT, True)

    @property
    def name(self) -> str:
        return "size_gt"

    @property
    def display_name(self) -> str:
        return "size_gt"

    @property
    def description(self):
        return "数组类型字段，其数组值的大小，大于给定数字"

    @property
    def order(self) -> int:
        return 2

    @property
    def available_data_types(self):
        return [MetaFieldType.LIST]

    @property
    def get_param_types(self):
        return [MetaFieldType.INT]

    def build(self, field, call: AqlMethodCall, target_type) -> dict:
        full_field_name = field.full_name

        result = self.build_range(full_field_name, call.param_list[0])
        return result

    @classmethod
    def build_range(cls, field_name, value):
        return {"range": {f"_size.{field_name}__size": {cls.flag(): int(value)}}}

    @classmethod
    def flag(cls):
        return "gt"


class SizeGreaterThanEqualMethod(SizeGreaterThanMethod):
    @classmethod
    def flag(cls):
        return "gte"

    @property
    def name(self) -> str:
        return "size_gte"

    @property
    def display_name(self) -> str:
        return "size_gte"

    @property
    def description(self):
        return "数组类型字段，其数组值的大小，大于等于给定数字"


class SizeLesserThanMethod(SizeGreaterThanMethod):
    @property
    def name(self) -> str:
        return "size_lt"

    @property
    def display_name(self) -> str:
        return "size_lt"

    @classmethod
    def flag(cls):
        return "lt"

    @property
    def description(self):
        return "数组类型字段，其数组值的大小，小于给定数字"


class SizeLesserThanEqualMethod(SizeLesserThanMethod):
    @classmethod
    def flag(cls):
        return "lte"

    @property
    def name(self) -> str:
        return "size_lte"

    @property
    def display_name(self) -> str:
        return "size_lte"

    @property
    def description(self):
        return "数组类型字段，其数组值的大小，小于等于给定数字"


class SizeEqualMethod(SizeGreaterThanMethod):
    @classmethod
    def build_range(cls, field_name, value):
        return {"term": {f"_size.{field_name}__size": int(value)}}

    @property
    def name(self) -> str:
        return "size"

    @property
    def display_name(self) -> str:
        return "size"

    @property
    def description(self):
        return "数组类型字段，其数组值的大小，等于给定数字"
