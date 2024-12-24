from caasm_aql.base import AqlOperator

class Op:
    op: AqlOperator = None

    def __init__(self):
        self.value = None

    def judge(self, value):
        raise NotImplementedError()
