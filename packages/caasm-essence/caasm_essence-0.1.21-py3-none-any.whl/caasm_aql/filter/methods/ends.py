from caasm_aql.filter.method import Method


class EndsMethod(Method):
    METHOD = "ends"

    def __init__(self):
        super(EndsMethod, self).__init__()
        self._postfix = None

    def call_implement(self, value):
        if self._postfix is None:
            self._postfix = self.params[0]
        if not isinstance(value, str):
            return False
        return value.endswith(self._postfix)
