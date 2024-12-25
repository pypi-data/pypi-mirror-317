from caasm_tool.constants import StrEnum


class StorageType(StrEnum):
    MONGO = "mongo"
    ES = "elasticsearch"
    ORIENTDB = "orientdb"
