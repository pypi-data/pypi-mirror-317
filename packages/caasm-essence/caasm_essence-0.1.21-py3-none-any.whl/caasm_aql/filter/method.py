class Method:
    METHOD = ""
    JUDGE_NONE = False

    def __init__(self):
        self.params = []

    def call(self, value):
        try:
            return self.call_implement(value)
        except:
            return False

    def call_implement(self, value):
        raise NotImplementedError()
