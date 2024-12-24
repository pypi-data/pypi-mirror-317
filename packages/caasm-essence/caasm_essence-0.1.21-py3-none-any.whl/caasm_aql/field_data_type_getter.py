class FieldDataTypeGetter:
    def __init__(self, field_mapper):
        self.field_mapper = field_mapper

    def get_data_type(self, field_name: str):
        return self.field_mapper.get(field_name)
