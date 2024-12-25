from caasm_aql.filter.filters.field import FieldFilter
from caasm_aql.filter.op import Op


class OpFilter(FieldFilter):
    def __init__(self):
        super(OpFilter, self).__init__()
        self.op: Op = None

    def filter(self, record) -> bool:
        value = self._extract_value(record)
        if value is None:
            return True
        if self._complex_field:
            for item in value:
                if self.op.judge(item):
                    return True
            return False
        else:
            return self.op.judge(value)
