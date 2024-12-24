from caasm_aql.base import AqlOperator
from caasm_aql.filter.op import Op


class LtOp(Op):
    op = AqlOperator.LESS

    def judge(self, value):
        return value < self.value
