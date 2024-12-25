from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import List, Dict

from bson import ObjectId
from caasm_persistence_base.entity.base import BaseEntity, DocumentEntity

from caasm_pipeline.fabric.service.constants.fabric import FabricGlobalPolicyEnum, FabricCIDREnum, GlobalFieldPolicyEnum, \
    OneselfFieldPolicyEnum


@dataclass
class UniqueIdentificationPolicy(BaseEntity):
    policy_label: str
    policy_value: str
    policy: list


@dataclass
class FabricPolicy(BaseEntity):
    name: str
    src_field: str
    dst_field: str
    setting: Dict


@dataclass
class FieldSourceEntity(BaseEntity):
    name: str
    display_name: str
    type: str


@dataclass
class FabricPolicyGroup(BaseEntity):
    name: FabricGlobalPolicyEnum
    src_field: str
    src_fields: List[FieldSourceEntity]
    dst_field: str
    cidr: FabricCIDREnum
    id_segment: List[str]
    name: FabricGlobalPolicyEnum


@dataclass
class AdapterConfidence(BaseEntity):
    adapter_name: str
    confidence: int


@dataclass
class FieldGlobalPolicy(BaseEntity):
    value: GlobalFieldPolicyEnum
    label: str = field(default="")
    policy_description: str = field(default="")


@dataclass
class FieldPolicy(BaseEntity):
    field_id: ObjectId
    field_adapter_confidence: List["AdapterConfidence"]
    field_policy: List["FieldGlobalPolicy"]


@dataclass
class FabricModelConfig(DocumentEntity):
    asset_type_id: ObjectId
    is_modify: bool
    modify_time: datetime.datetime
    modify_username: str
    adapter_confidence: List[AdapterConfidence]
    field_global_policy: List[FieldGlobalPolicy]
    fabric_policy: FabricPolicy


@dataclass
class OneselfFieldConfigEntity(BaseEntity):
    name: str
    full_name: str
    policy: OneselfFieldPolicyEntity
    equation: str = field(default_factory=str)
    type: str = field(default_factory=str)
    type_name: str = field(default_factory=str)
    internal: bool = field(default=False)
    description: str = field(default_factory=str)
    adapter: List[AdapterConfidence] = field(default_factory=list)
    update_time: datetime.datetime = field(default_factory=datetime.datetime.now)
    create_time: datetime.datetime = field(default_factory=datetime.datetime.now)


@dataclass
class GlobalFieldConfig(BaseEntity):
    adapter: List[AdapterConfidence]
    policy: Dict


@dataclass
class FabricStageEntity(BaseEntity):
    stage_id: ObjectId
    stage_name: str


@dataclass
class FabricConfigEntity(DocumentEntity):
    stage_name: str
    asset_type_id: ObjectId
    asset_type: str
    is_modify: bool
    modify_time: datetime.datetime
    modify_username: str
    is_master: bool
    stage_ids: List[ObjectId]
    fabric_stages: List[FabricStageEntity]
    fabric_adapter: List[AdapterConfidence]
    global_field_config: FieldPolicyConfig
    oneself_field_config: List[OneselfFieldConfigEntity]
    fabric_policy: FabricPolicyGroup
    master_id: str


@dataclass
class FieldPolicyConfig(BaseEntity):
    adapter: List[AdapterConfidence]
    policy: FieldGlobalPolicy


@dataclass
class OneselfFieldPolicyEntity(BaseEntity):
    value: OneselfFieldPolicyEnum
    label: str = field(default="")
    policy_description: str = field(default="")
