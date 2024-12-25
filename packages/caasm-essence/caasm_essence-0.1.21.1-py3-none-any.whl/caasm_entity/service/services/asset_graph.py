from caasm_entity.service.schemas.asset_graph import Node, Relationship
from caasm_persistence.handler.storage.orientdb import OrientDBHandler, auto_close


class EntityGraphHandler(OrientDBHandler):
    def __init__(self, category, date=None, *args, **kwargs):
        from caasm_entity.service.runtime import snapshot_record_service

        self._category = category
        self._date = date or snapshot_record_service.get_latest_useful_date()
        super(EntityGraphHandler, self).__init__(*args, **kwargs)

    @auto_close
    def create_registry(self, auto_close=True):
        self.create(Node.registry)
        self.create(Relationship.registry)

    def include_registry(self):
        self.include(Node.registry)
        self.include(Relationship.registry)

    @property
    def default_space(self):
        return f"{self._category}_graph_{self._date}"
