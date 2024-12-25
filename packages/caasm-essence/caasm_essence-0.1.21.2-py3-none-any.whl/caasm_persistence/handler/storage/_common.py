from bson import ObjectId


class MongoCommon(object):
    @classmethod
    def _build_id(cls, data_id):
        if not isinstance(data_id, ObjectId):
            data_id = ObjectId(data_id)
        return data_id

    @classmethod
    def _build_ids(cls, data_ids):
        return [cls._build_id(data_id) for data_id in data_ids]
