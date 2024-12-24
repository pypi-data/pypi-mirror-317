from caasm_aql.base import AqlOperator
from caasm_aql.filter.op import Op


class NotEqualOp(Op):
    op = AqlOperator.NOT_EQUAL

    def judge(self, value):
        return value != self.value
