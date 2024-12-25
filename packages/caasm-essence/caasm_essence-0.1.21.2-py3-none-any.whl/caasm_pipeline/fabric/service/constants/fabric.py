from caasm_tool.constants import StrEnum


class FabricGlobalPolicyEnum(StrEnum):
    """the global policy"""

    IP = "ip"
    CHOICE_FIELD = "choice_field"


FabricGlobalPolicyTranslation = {
    FabricGlobalPolicyEnum.IP: "IP融合",
    FabricGlobalPolicyEnum.CHOICE_FIELD: "字段融合",
}


class GlobalFieldPolicyEnum(StrEnum):
    """the field policy has been used to the global field"""

    ELECT = "elect"
    ADAPTER = "adapter"
    DEFAULT = "default"


GlobalFieldPolicyTranslation = {
    GlobalFieldPolicyEnum.ELECT: "选举策略",
    GlobalFieldPolicyEnum.ADAPTER: "适配器置信度策略",
    GlobalFieldPolicyEnum.DEFAULT: "不融合",
}


class OneselfFieldPolicyEnum(StrEnum):
    """the field policy has been used to the oneself field"""

    ELECT = "elect"
    ADAPTER = "adapter"
    EQUATION = "equation"


OneselfFieldPolicyTranslation = {
    OneselfFieldPolicyEnum.ELECT: "选举策略",
    OneselfFieldPolicyEnum.ADAPTER: "适配器置信度策略",
    OneselfFieldPolicyEnum.EQUATION: "字段逻辑计算",
}


class FabricCIDREnum(StrEnum):
    MULTI_CIDR = "MULTI_CIDR"
    LAN = "LAN"


FabricCIDRTranslation = {
    FabricCIDREnum.MULTI_CIDR: "指定CIDR段",
    FabricCIDREnum.LAN: "采用局域网IP段台账",
}
