from caasm_aql.base import AqlOperator
from caasm_aql.filter.op import Op


class EqualOp(Op):
    op = AqlOperator.EQUAL

    def judge(self, value):
        return value == self.value
