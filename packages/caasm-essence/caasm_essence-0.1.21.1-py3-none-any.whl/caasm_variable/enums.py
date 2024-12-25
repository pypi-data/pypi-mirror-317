from caasm_tool.constants import StrEnum


class VariableDataType(StrEnum):
    STR = "str"
    ARRAY = "array"
    FLOAT = "float"
    BOOL = "bool"
    INT = "int"


class VariableType(StrEnum):
    """
    变量属性
    """

    PREFAB = "prefab"
    PUBLIC = "public"
    PRIVATE = "private"
