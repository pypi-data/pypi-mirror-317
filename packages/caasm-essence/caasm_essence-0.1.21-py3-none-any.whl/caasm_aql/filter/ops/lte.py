from caasm_aql.base import AqlOperator
from caasm_aql.filter.op import Op


class LteOp(Op):
    op = AqlOperator.LESS_OR_EQUAL

    def judge(self, value):
        return value <= self.value
