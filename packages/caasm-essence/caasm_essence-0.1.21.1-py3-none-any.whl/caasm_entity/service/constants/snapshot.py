from caasm_tool.constants import StrEnum


class SnapshotRecordStatus(StrEnum):
    INIT = "init"
    DOING = "doing"
    SUCCESS = "success"
    FAILED = "failed"
    CANCEL = "cancel"
