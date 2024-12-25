from caasm_variable.enums import VariableDataType
from caasm_variable.service.entity.variable import Variable


def convert_variable(variable: Variable):
    if variable.data_type == VariableDataType.INT:
        return int(variable.data_value)
    elif variable.data_type == VariableDataType.STR:
        return variable.data_value
    elif variable.data_type == VariableDataType.FLOAT:
        return float(variable.data_value)
    elif variable.data_type == VariableDataType.BOOL:
        return bool(variable.data_value)
    elif variable.data_type == VariableDataType.ARRAY:
        return variable.data_value
    else:
        raise ValueError()
