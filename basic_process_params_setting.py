# 主要用来直接调用basic_processing的功能
# 通过函数BasicProcessing.basic_process_data调用
from enum import Enum, unique


@unique
class DfType(Enum):
    # Column Types for DataFrame
    # 用来提示使用者, 在系统内的数据类型是什么, 可以采用DfType.INT_TYPE.value来调用里面的值
    # 主要用来提示使用者在修改数据类型的时候，应该如何填写change_types字段内各个列想转换成对应的类型的时候，该怎么写该类型的格式数据
    INT_TYPE = 'int64'
    FLOAT_TYPE = 'float64'
    STRING_TYPE = 'object'
    DATE_TYPE = 'datetime64[ns]'
    BOOLEAN_TYPE = 'bool'


pd_date_formats = {
    # date-format in pandas
    # 在Pandas里常见的date format的格式，左边是提示，右边是如何写数据类型转换格式
    # 根据该类提示，可以to_date_format参数和from_date_formats参数所对应的格式数据有一个了解该怎么写
    '2023-11-18': '%Y-%m-%d',
    '20231118': '%Y%m%d',
    '2023-11-18 23:23:32': '%Y-%m-%d %H:%M:%S'
}

change_names_previously = {
    # always the first to be processed
    'activation': False,
    # key: column old name, value: column new name
    'change_names': {
        'original_name': 'new_name'
    },
}

change_names_finally = {
    # always the last to be processed
    'activation': False,
    # key: column old name, value: column new name
    'change_names': {
        'original_name': 'new_name'
    },
}

change_types_opt = {
    'activation': False,
    # key: column new name if changed else column old name, value: type in pandas as target type
    'change_types': {
        'column_name': 'type_in_pandas',
        # 样例1: '列名': DfType.INT_TYPE.value,
        # 样例2: '列名': 'int64',
        # 以上两个样例都可以用来指挥系统如何修改数据类型为整型INTEGER
    },
    # how to turn datetime type data to object
    # 用来设置如何将datetime类型的数据转为字符串, 其数据转换必须在change_types里先提到: '列': 'object', 然后这个列是datetime类型
    'from_date_formats': {
        'column_name': '%Y-%m-%d',  # date-format in pandas
    },
    # how to turn object to certain datetime type data
    # 用来设置如何将字段从字符串转为datetime数据类型, 其数据转换必须在change_types里先提到: '列': 'datetime64', 然后这个列是object类型
    # 注意，这里设置的是原字段内数据在字符串里的时间格式，这样才可以将其转换为时间类型，比如说原数据为2023-11-18这样的格式，那么这里就要填写'%Y-%m-%d'
    'to_date_formats': {
        'column_name': '%Y-%m-%d',  # date-format in pandas
    }
}

pick_columns_opt = {
    'activation': False,
    # list for containing the columns to be picked
    'pick_columns': [],
}

data_masking_opt = {
    'activation': False,
    # the method for data masking
    'masking_type': 'simple',
    # the choices of method you can pick to put into masking_type
    'masking_type_choices': ['simple'],
    # list for containing the columns to be masked
    'masking_columns': [],
}

# the order of functions for basic processing
basic_processing_order = ['change_names_previously', 'change_types_opt', 'pick_columns_opt', 'data_masking_opt',
                          'change_names_finally']