import gridfs

from caasm_config.config import caasm_config
from caasm_persistence.handler import TableName
from caasm_persistence.handler.storage._common import MongoCommon
from caasm_persistence.handler.storage.model.constant import StorageType
from caasm_persistence.handler.storage.runtime import build_client
from caasm_tool.util import SingletonInstance


class MongoFileHandler(MongoCommon, metaclass=SingletonInstance):
    def __init__(self, client=None, database=None):
        self._file_client = client
        if client is None:
            self._file_client = build_client(StorageType.MONGO)
        if not database:
            database = caasm_config.mongo_default_database
        db = self._file_client[database]
        self._file_server = gridfs.GridFS(db, TableName.file.value)

    def save_file(self, file_content: bytes, filename=None):
        return self._file_server.put(file_content, filename=filename)

    def get_file(self, file_id):
        file_id = self._build_id(file_id)
        return self._file_server.get(file_id)

    def check_file_exists(self, file_id):
        return self._file_server.exists(self._build_id(file_id))

    def delete_file(self, file_id):
        return self._file_server.delete(self._build_id(file_id))
