from caasm_aql.filter.method import Method


class MatchMethod(Method):
    METHOD = "match"

    def __init__(self):
        super(MatchMethod, self).__init__()
        self._part = None

    def call_implement(self, value):
        if self._part is None:
            self._part = self.params[0]
        if not isinstance(value, str):
            return False
        return self._part in value
