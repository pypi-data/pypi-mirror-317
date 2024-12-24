from antlr4 import ParserRuleContext


class AqlAltNumContext(ParserRuleContext):
    def __init__(self, parent: ParserRuleContext = None, invoking_state_number: int = None):
        super(AqlAltNumContext, self).__init__(parent, invoking_state_number)
        self._alt_num = -1

    def getAltNumber(self):
        return self._alt_num

    def setAltNumber(self, altNumber: int):
        self._alt_num = altNumber


class AsglGetTextContext(ParserRuleContext):
    def get_whitespaced_text(self):
        if self.getChildCount() == 0:
            return self.getText()
        buffer = list()
        for child in self.getChildren():
            if hasattr(child, 'get_whitespaced_text'):
                buffer.append(child.get_whitespaced_text())
            else:
                buffer.append(child.getText())
        return ' '.join(buffer)
