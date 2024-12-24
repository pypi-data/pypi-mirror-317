import urllib.parse as urllib2

import pymongo
from caasm_persistence_base.handler.storage.manager import storage_manager

from caasm_config.config import caasm_config
from caasm_persistence.handler.storage.model.constant import StorageType

_mongo_client = pymongo.MongoClient(**caasm_config.mongo_conn)


def close_client():
    _mongo_client.close()


def build_client(storage_type, new_instance=False, **kwargs):
    if new_instance:
        return __BUILD_FUNC_MAPPER[storage_type](**kwargs)

    if storage_type not in _MAPPER:
        build_function = __BUILD_FUNC_MAPPER[storage_type]

        client = build_function(**kwargs)
        _MAPPER[storage_type] = client
    return _MAPPER[storage_type]


def build_client_to_local():
    return _mongo_client


def __build_es_client():
    import elasticsearch

    client = elasticsearch.Elasticsearch(**caasm_config.es_conn)
    return client


def __build_orient_client(default_space, initial_drop=False):
    from pyorient.ogm import Config, Graph

    host = caasm_config.orientdb_conn.get("host", "localhost")
    port = caasm_config.orientdb_conn.get("port", 2424)
    username = caasm_config.orientdb_conn.get("username", "")
    password = caasm_config.orientdb_conn.get("password", "")
    url = f"{host}:{port}"
    if default_space:
        url += f"/{default_space}"
    config = Config.from_url(url, username, password, initial_drop=initial_drop)
    return Graph(config)


def get_mongo_uri():
    uri = "mongodb://"

    mongo_conn = caasm_config.mongo_conn

    username = mongo_conn.get("username", "")
    password = mongo_conn.get("password", "")
    replicaset = mongo_conn.get("replicaset", "")
    hosts = mongo_conn.get("host", ["localhost"])

    if username:
        username = urllib2.quote_plus(username)
        uri += username
    if password:
        password = urllib2.quote_plus(password)
        uri += ":" + password

    if username or password:
        uri += "@"

    uri += ",".join(hosts)

    if replicaset:
        uri += f"/?replicaSet={replicaset}"

    return uri


_MAPPER = {}
__BUILD_FUNC_MAPPER = {
    StorageType.ES: __build_es_client,
    StorageType.MONGO: build_client_to_local,
    StorageType.ORIENTDB: __build_orient_client,
}

storage_manager.register_build_function(StorageType.ES, __build_es_client)
storage_manager.register_build_function(StorageType.MONGO, build_client_to_local)
storage_manager.register_build_function(StorageType.ORIENTDB, __build_orient_client)
