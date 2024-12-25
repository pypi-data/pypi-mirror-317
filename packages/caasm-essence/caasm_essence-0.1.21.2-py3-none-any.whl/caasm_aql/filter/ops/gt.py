from caasm_aql.base import AqlOperator
from caasm_aql.filter.op import Op


class GtOp(Op):
    op = AqlOperator.GREATER

    def judge(self, value):
        return value > self.value
