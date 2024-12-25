from typing import List, Union, Dict
from nanoid import generate

from caasm_aql.aql import AqlQuery
from caasm_tool.constants import StrEnum


class AsglEdgeDirection(StrEnum):
    NONE = 'none'
    IN = 'in'
    OUT = 'out'


class AsglElement:
    def __init__(self):
        self.id: str = generate()
        self._name: str = None
        self.type: str = None
        self.where: AqlQuery = AqlQuery()

    @property
    def name(self):
        if self._name:
            return self._name
        else:
            return self.id

    @name.setter
    def name(self, name):
        self._name = name


class AsglVertexDef(AsglElement):
    def __init__(self):
        super(AsglVertexDef, self).__init__()
        self.trait: str = None


class AsglEdgeDef(AsglElement):
    def __init__(self):
        super(AsglEdgeDef, self).__init__()
        self.direction: AsglEdgeDirection = AsglEdgeDirection.NONE


class AsglLink:
    def __init__(self):
        self.elements: List[Union[AsglEdgeDef, AsglVertexDef, AsglEdgeDef]] = list()
        self.name: str = generate()
        self.not_boolean: bool = False


class AsglQuery:
    def __init__(self):
        self.vertex_defs: Dict[str, AsglVertexDef] = dict()
        self.edge_defs: Dict[str, AsglEdgeDef] = dict()
        self.links: List[AsglLink] = list()

    def _build_identity(self, element: AsglElement, identities: Dict[str, AsglElement], identity_type_name: str):
        element_name = element.name
        element_type = element.type
        if element_name in self.vertex_defs:
            existing_identity_def: AsglElement = identities[element_name]
            if existing_identity_def.type is None:
                identities[element_name] = element
            else:
                if element_type is not None:
                    if existing_identity_def.type != element_type:
                        raise ValueError(f'{identity_type_name}{element_name}指定了不同的类型')
            if existing_identity_def.where.is_valid():
                if element.where.is_valid():
                    raise ValueError(f'{identity_type_name}{element_name}制定了不同筛选条件')
            else:
                identities[element_name].where = element.where
        else:
            identities[element_name] = element

    def build(self):
        self.vertex_defs.clear()
        self.edge_defs.clear()
        for link in self.links:
            link: AsglLink = link
            for element in link.elements:
                if isinstance(element, AsglVertexDef):
                    self._build_identity(element, self.vertex_defs, '顶点')
                elif isinstance(element, AsglEdgeDef):
                    self._build_identity(element, self.edge_defs, '边')
