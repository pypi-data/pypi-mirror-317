from caasm_tool.constants import StrEnum


class AdapterConvertStatus(StrEnum):
    WAIT = "init"
    CONVERTING = "converting"
    SUCCESS = "success"
    FAILED = "failed"
    CANCEL = "cancel"
