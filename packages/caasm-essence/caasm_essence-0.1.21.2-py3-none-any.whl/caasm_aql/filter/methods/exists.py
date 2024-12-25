from caasm_aql.filter.method import Method


class ExistsMethod(Method):
    METHOD = "exists"
    JUDGE_NONE = True

    def call_implement(self, value):
        return value is not None
