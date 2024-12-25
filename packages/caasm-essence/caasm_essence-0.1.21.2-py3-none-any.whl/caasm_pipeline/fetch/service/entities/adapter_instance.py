import datetime
from dataclasses import dataclass, field
from typing import Dict

from caasm_persistence_base.entity.base import DocumentEntity, BaseEntity
from caasm_service_base.constants.adapter import AdapterInstanceRunStatus, AdapterInstanceConnectionStatus

from caasm_common.service.constants.trigger import TriggerType


@dataclass
class Trigger(BaseEntity):
    type: TriggerType
    value: Dict = field(default_factory=dict)


@dataclass
class AdapterInstance(DocumentEntity):
    name: str
    adapter_name: str
    ancestor_adapter_name: str
    properties: list
    enabled: bool
    debug: bool
    connection: Dict
    trigger_type: str
    proxy: str
    trigger: Trigger
    description: str
    run_status: AdapterInstanceRunStatus
    connect_status: AdapterInstanceConnectionStatus
    last_sync_time: datetime
    is_complex: bool
