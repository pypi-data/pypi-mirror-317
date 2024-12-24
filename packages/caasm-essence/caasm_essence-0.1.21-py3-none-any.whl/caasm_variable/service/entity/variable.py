from dataclasses import dataclass
from caasm_persistence_base.entity.base import DocumentEntity


@dataclass
class Variable(DocumentEntity):
    name: str
    description: str
    create_time: str
    update_time: str
    data_type: any
    data_value: object
