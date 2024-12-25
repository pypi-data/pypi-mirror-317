from antlr4.error.ErrorListener import ErrorListener


class AqlErrorListener(ErrorListener):
    def __init__(self, errors: list):
        self.errors = errors

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"第{line}行第{column}列出现语法错误：{msg}")
