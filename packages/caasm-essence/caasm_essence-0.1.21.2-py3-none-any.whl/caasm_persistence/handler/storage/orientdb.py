from functools import wraps

from caasm_persistence.handler.storage.model.constant import StorageType
from caasm_persistence.handler.storage.runtime import build_client


def auto_close(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
        finally:
            self.finish() if "auto_close" in kwargs and kwargs["auto_close"] else ...
        return result

    return inner


class OrientDBHandler(object):
    def __init__(self, initial_drop=False):
        self._graph = build_client(
            self.storage_type, new_instance=True, default_space=self.default_space, initial_drop=initial_drop
        )

    @auto_close
    def create(self, registry):
        self.graph.create_all(registry)

    def include(self, registry):
        self.graph.include(registry)

    def create_batch(self):
        return self._graph.batch()

    @auto_close
    def drop(self, **kwargs):
        try:
            return self._graph.drop(self.default_space)
        except Exception as e:
            pass

    @property
    def default_space(self):
        raise NotImplementedError

    @property
    def storage_type(self) -> StorageType:
        return StorageType.ORIENTDB

    @property
    def client(self):
        return self._graph.client

    @property
    def graph(self):
        return self._graph

    def finish(self):
        self.client.db_close()
