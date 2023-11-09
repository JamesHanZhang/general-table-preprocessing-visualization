# 主要用来直接调用basic_processing的功能
# 通过函数BasicProcessing.basic_process_data调用

change_names_previously = {
    # always the first to be processed
    'activation': False,
    # key: column old name, value: column new name
    'change_names':{
        'original_name': 'new_name'
    },
}

change_names_finally = {
    # always the last to be processed
    'activation': False,
    # key: column old name, value: column new name
    'change_names':{
        'original_name': 'new_name'
    },
}

change_types_opt = {
    'activation': False,
    # key: column new name if changed else column old name, value: type in pandas as target type
    'change_types': {
        'column_name': 'type_in_pandas',
    },
    # how to turn datetime type data to object
    # 用来设置如何将datetime类型的数据转为字符串, 其数据转换必须在change_types里先提到: '列': 'object', 然后这个列是datetime类型
    'from_date_formats': {
        'column_name': '%Y-%m-%d', # date-format in pandas
    },
    # how to turn object to certain datetime type data
    # 用来设置如何将字段从字符串转为datetime数据类型, 其数据转换必须在change_types里先提到: '列': 'datetime64', 然后这个列是object类型
    'to_date_formats': {
        'column_name': '%Y-%m-%d', # date-format in pandas
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
basic_processing_order = ['change_names_previously', 'change_types_opt', 'pick_columns_opt', 'data_masking_opt', 'change_names_finally']