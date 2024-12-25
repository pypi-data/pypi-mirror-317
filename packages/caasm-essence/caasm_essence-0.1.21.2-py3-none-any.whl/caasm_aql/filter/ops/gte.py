from caasm_aql.base import AqlOperator
from caasm_aql.filter.op import Op


class GteOp(Op):
    op = AqlOperator.GREATER_OR_EQUAL

    def judge(self, value):
        return value >= self.value
