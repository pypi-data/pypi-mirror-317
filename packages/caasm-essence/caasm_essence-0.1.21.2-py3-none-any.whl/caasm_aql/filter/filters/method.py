from caasm_aql.filter.filters.field import FieldFilter
from caasm_aql.filter.method import Method


class MethodFilter(FieldFilter):
    def __init__(self):
        super(MethodFilter, self).__init__()
        self.method: Method = None

    def filter(self, record) -> bool:
        value = self._extract_value(record)
        if not self.method.JUDGE_NONE and value is None:
            return True
        if self._complex_field:
            for item in value:
                if self.method.call(item):
                    return True
            return False
        else:
            return self.method.call(value)
