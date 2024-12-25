from typing import List

from caasm_aql.filter.method import Method


class SizeMethod(Method):
    METHOD = "size"

    def __init__(self):
        super(SizeMethod, self).__init__()
        self._size = None

    def call_implement(self, value):
        if self._size is None:
            self._size = self.params[0]
        if not isinstance(value, List):
            return False
        return len(value) == self._size
