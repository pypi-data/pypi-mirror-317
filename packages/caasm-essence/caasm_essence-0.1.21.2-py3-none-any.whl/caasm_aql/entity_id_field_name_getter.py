class EntityIDFieldNameGetter:
    def __init__(self, logical_model):
        self.logical_model = logical_model

    def get_entity_id_field_name(self):
        return "base.entity_id"
