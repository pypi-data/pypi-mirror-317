from dataclasses import dataclass

from caasm_persistence_base.entity.base import DocumentEntity


@dataclass
class AssetType(DocumentEntity):
    name: str
    display_name: str
    model_id: str
    internal: bool
    description: str
    format_names: list
