import re

from caasm_aql.filter.method import Method


class RegexMethod(Method):
    METHOD = "regex"

    def __init__(self):
        super(RegexMethod, self).__init__()
        self.regex = None

    def call_implement(self, value):
        if self.regex is None:
            self.regex = re.compile(self.params[0])
        if not isinstance(value, str):
            return False
        return bool(self.regex.match(value))
