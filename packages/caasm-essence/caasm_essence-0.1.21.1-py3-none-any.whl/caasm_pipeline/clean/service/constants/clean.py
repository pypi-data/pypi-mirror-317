from caasm_tool.constants import StrEnum


class CleanType(StrEnum):
    #   去重
    DEDUPLICATION = "deduplication"
    #   过滤
    FILTER = "filter"


class AdapterProcessStatus(StrEnum):
    INIT = "init"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    CANCEL = "cancel"


ADAPTER_PROCESS_STATUS_MAPPER = {
    AdapterProcessStatus.INIT: "初始化",
    AdapterProcessStatus.PROCESSING: "处理中",
    AdapterProcessStatus.SUCCESS: "成功",
    AdapterProcessStatus.FAILED: "失败",
    AdapterProcessStatus.CANCEL: "取消",
}
