from caasm_aql.filter.ops.eq import EqualOp
from caasm_aql.filter.ops.gt import GtOp
from caasm_aql.filter.ops.gte import GteOp
from caasm_aql.filter.ops.lt import LtOp
from caasm_aql.filter.ops.lte import LteOp
from caasm_aql.filter.ops.ne import NotEqualOp


class OpManager:
    def __init__(self):
        self._ops = {}

    def register(self, op_cls_):
        self._ops[op_cls_.op] = op_cls_

    def get_op_cls(self, op):
        return self._ops[op]


op_manager = OpManager()

ops = [
    EqualOp,
    GtOp,
    GteOp,
    LtOp,
    LteOp,
    NotEqualOp
]

for op_cls in ops:
    op_manager.register(op_cls)
