class AsqlFilter:
    def filter(self, record) -> bool:
        raise NotImplementedError()

    def get_field_names(self):
        pass
