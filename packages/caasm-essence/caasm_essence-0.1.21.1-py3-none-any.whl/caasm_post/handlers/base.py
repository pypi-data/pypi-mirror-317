from caasm_config.config import caasm_config
from caasm_tool.util import extract, restore


class EnforcementBaseHandler(object):
    def __init__(self, category=None, date=None):
        self._category = category
        self._params = None
        self._date = date

    def initialize(self, params):
        self._params = params

    def execute(self):
        raise

    @classmethod
    def get_name(cls):
        raise NotImplementedError

    @classmethod
    def get_display_name(cls):
        return cls.get_name()

    @property
    def params(self):
        return self._params or {}

    @property
    def category(self):
        return self._category

    @property
    def date(self):
        return self._date

    @property
    def size(self):
        return self.params.get("size", 100)

    @property
    def buffer_size(self):
        return self.params.get("buffer_size", 100)

    @property
    def data_dir(self):
        return caasm_config.ROOT_DIR / "caasm_enforcement" / "data"

    @classmethod
    def extract(cls, record, field):
        return extract(record, field)

    @classmethod
    def restore(cls, field, value, record):
        restore(field, value, record)

    @property
    def relation_category(self):
        return None
