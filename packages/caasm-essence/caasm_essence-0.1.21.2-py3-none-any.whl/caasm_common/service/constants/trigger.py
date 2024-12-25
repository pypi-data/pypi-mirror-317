from caasm_tool.constants import StrEnum


class TriggerType(StrEnum):
    CRON = "cron"
    DATE = "date"
    INTERVAL = "interval"
