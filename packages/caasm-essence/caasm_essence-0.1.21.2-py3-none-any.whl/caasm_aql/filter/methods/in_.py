from caasm_aql.filter.method import Method


class InMethod(Method):
    METHOD = "in"

    def __init__(self):
        super(InMethod, self).__init__()
        self._range = None

    def call_implement(self, value):
        if self._range is None:
            self._range = self.params[0]
        return value in self._range
