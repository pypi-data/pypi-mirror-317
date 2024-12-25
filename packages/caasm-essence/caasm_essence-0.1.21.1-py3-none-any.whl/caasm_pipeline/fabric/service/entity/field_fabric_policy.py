from dataclasses import dataclass
from typing import List

from bson import ObjectId
from caasm_persistence_base.entity.base import BaseEntity, DocumentEntity


@dataclass
class AdapterConfidence(BaseEntity):
    adapter_name: str
    confidence: int


@dataclass
class FieldPolicy(BaseEntity):
    value: str
    label: str
    policy_description: str


@dataclass
class FieldFabricPolicy(DocumentEntity):
    full_name: str
    asset_type_id: ObjectId
    fabric_config_id: ObjectId
    adapter_confidence: List["AdapterConfidence"]
    fabric_policy: List["FieldPolicy"]
