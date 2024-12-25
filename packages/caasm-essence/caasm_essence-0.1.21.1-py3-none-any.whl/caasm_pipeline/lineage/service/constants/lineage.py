from caasm_tool.constants import StrEnum


class PostSourceType(StrEnum):
    FUSION = "fusion"
    MANUAL = "manual"
    APP = "app"


class LineageStageType(StrEnum):
    FETCH = "fetch"
    MERGE = "merge"
    CONVERT = "convert"
    FABRIC = "fabric"
    ENFORCEMENT = "enforcement"
