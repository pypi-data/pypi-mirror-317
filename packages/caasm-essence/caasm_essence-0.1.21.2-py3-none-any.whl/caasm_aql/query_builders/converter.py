from typing import List, Dict


class Converter:
    """
    值转换器，做部分数据的隐式转换，如日期和时间
    """

    def convert(self, value, field):
        raise NotImplementedError()

    @property
    def available_types(self) -> List:
        raise NotImplementedError()


class ConverterManager:
    def __init__(self):
        self._converters: Dict[Converter] = dict()

    def register(self, converter: Converter):
        for data_type in converter.available_types:
            self._converters[data_type] = converter

    def get(self, data_type):
        return self._converters.get(data_type)
