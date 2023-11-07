from enum import Enum

def get_enum_value_list(enum_cls: Enum) -> list:
    enum_elements = [enum_element for enum_element in enum_cls]
    values=list()
    for enum_element in enum_elements:
        values.append(enum_element.value)
    return values

def get_enum_name_list(enum_cls: Enum) -> list[str]:
    enum_elements = [enum_element for enum_element in enum_cls]
    values=list()
    for enum_element in enum_elements:
        values.append(enum_element.name)
    return values
    
def turn_value_to_enum(enum_cls:Enum, value:str, error_msg="wrong value in enum"):
    try:
        value = int(value)
    except (ValueError):
        raise ValueError(error_msg)
    enum_values = get_enum_value_list(enum_cls)
    if value not in enum_values:
        raise ValueError(error_msg)
    enum_element = enum_cls(value)
    return enum_element