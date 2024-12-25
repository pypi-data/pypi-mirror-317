from dataclasses import dataclass
from typing import Dict, List

from bson import ObjectId

from caasm_persistence_base.entity.base import DocumentEntity
from caasm_tool.constants import StrEnum


class MetaFieldType(StrEnum):
    STRING = "string"
    INT = "integer"
    FLOAT = "float"
    OBJECT = "object"
    BOOLEAN = "boolean"
    LIST = "list"
    ENUM = "enum"
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    EMAIL = "email"
    IP = "ip"
    DATETIME = "datetime"
    DATE = "date"
    TIME = "time"
    TIMESTAMP = "timestamp"
    ADAPTER = "adapter"
    RELATION = "relation"
    VERSION = "version"
    ADDRESS = "address"
    ANY = "any"


TOTAL_META_FIELD_TYPES = [i for i in list(MetaFieldType.__members__.values())]


class MetaModelType(StrEnum):
    FIELD_SET = "fieldSet"
    APPLICATION = "application"


TYPE_NAME_MAPPER = {
    MetaFieldType.STRING: "字符串",
    MetaFieldType.LIST: "列表",
    MetaFieldType.OBJECT: "键值对象",
    MetaFieldType.ENUM: "枚举",
    MetaFieldType.FLOAT: "浮点数",
    MetaFieldType.RELATION: "关系",
    MetaFieldType.ADAPTER: "适配器",
    MetaFieldType.IP: "IP地址",
    MetaFieldType.IPV6: "IPv6地址",
    MetaFieldType.IPV4: "IPv4地址",
    MetaFieldType.DATE: "日期",
    MetaFieldType.DATETIME: "时刻",
    MetaFieldType.TIME: "时间",
    MetaFieldType.TIMESTAMP: "时间戳",
    MetaFieldType.VERSION: "版本",
    MetaFieldType.ANY: "变量",
    MetaFieldType.INT: "整数",
    MetaFieldType.BOOLEAN: "布尔",
    MetaModelType.FIELD_SET: "字段集",
    MetaModelType.APPLICATION: "模型",
}


@dataclass
class Rule(DocumentEntity):
    name: str
    display_name: str
    setting: Dict


@dataclass
class MetaField(DocumentEntity):
    name: str
    display_name: str
    description: str
    type: MetaFieldType
    required: bool
    allow_null: bool
    default: any
    encrypt: bool
    encrypt_setting: Dict
    internal: bool
    unique: bool
    model_id: ObjectId
    setting: Dict
    children: List["MetaField"]
    query: str
    rules: List[Rule]
    full_name: str
    full_display_name: str
    priority: int
    hidden: bool
    is_complex: bool
    complex_full_name: str
    full_text_search: bool
    is_monitor: bool


@dataclass
class MetaModel(DocumentEntity):
    name: str
    display_name: str
    init: bool
    type: MetaModelType
    category: str
    description: str
    friends: List[ObjectId]
    internal: bool
    setting: Dict
    priority: int
    logo_id: ObjectId
    logo_name: str


@dataclass
class MetaView(DocumentEntity):
    category: str
    often_used_fields: List[str]
    necessary_fields: List[str]
    pk_field: str
    default_fields: List[str]
    charts: List[ObjectId]
