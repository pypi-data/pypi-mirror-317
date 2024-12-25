from dataclasses import dataclass, field
from typing import Dict


@dataclass
class HandlerRequest(object):
    name: str
    params: Dict = field(default_factory=dict)
