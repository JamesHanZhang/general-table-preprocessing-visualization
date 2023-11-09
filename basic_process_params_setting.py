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
    # 如果导入数据中有时间类型的话, 需要先转换成str才能继续执行
    # if data type for certain columns in imported data waiting for type change, it's better to turn the date type into string type firstly.
    'from_date_formats': {
        'column_name': '%Y-%m-%d', # date-format in pandas
    },
    # 如果导出的数据中有时间类型的话，需要注意希望转换成的时间结构
    # if output as datetime, you must focus on how to do the date format transformation
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