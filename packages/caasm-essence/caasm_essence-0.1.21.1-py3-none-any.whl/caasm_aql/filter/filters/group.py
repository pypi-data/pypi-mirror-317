from typing import List, Optional

from caasm_aql.base import AqlLogicalOperand
from caasm_aql.filter.filter import AsqlFilter


class GroupFilter(AsqlFilter):
    def __init__(self):
        self.logical_op: AqlLogicalOperand = None
        self.not_boolean: Optional[bool] = None
        self.filters: List[AsqlFilter] = []

    def filter(self, record) -> bool:
        result = True
        if self.logical_op == AqlLogicalOperand.AND:
            for filter_ in self.filters:
                if not filter_.filter(record):
                    result = False
                    break
        else:
            for filter_ in self.filters:
                if filter_.filter(record):
                    result = True
                    break
        if self.not_boolean is not None:
            return (not self.not_boolean) and result
        return result
