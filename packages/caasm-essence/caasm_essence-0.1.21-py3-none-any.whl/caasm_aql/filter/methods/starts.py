from caasm_aql.filter.method import Method


class StartsMethod(Method):
    METHOD = "starts"

    def __init__(self):
        super(StartsMethod, self).__init__()
        self._prefix = None

    def call_implement(self, value):
        if self._prefix is None:
            self._prefix = self.params[0]
        if not isinstance(value, str):
            return False
        return value.startswith(self._prefix)
