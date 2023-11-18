# 以下可添加绝对路径，如为空值""，则为默认导出路径output_dataset，也可添加默认路径下output_dataset的子文件夹，例如:
# 如添加子文件夹child_folder/split1，则实际路径为:../output_dataset/child_folder/split1
output_path = ""

# 导出的文件名, 如采用based_on_activation模式导出则不能携带拓展名, 否则必须携带拓展名
# 文件名不要有`.`, 以免被误识别为拓展名
output_file = "output_test.csv"

# 加载时的解码格式默认值：INPUT_ENCODE = "utf-8" 或者中文环境下常用"gbk", 如不填写, 导出默认为gb18030
output_encoding = "gb18030"

# 判断是否要拆分，如拆分，则按照导入的chunksize的大小进行拆分
if_sep = False

# 是否只是拆分出一个样例即可，默认为否，即拆分到底。如为真，则仅拆分出一个文件即停止，作为样例
only_one_chunk = False

# 导出是否覆盖，如不覆盖，则默认添加到同名文件的末尾，拆分的情况只允许OVERWRITE = True
overwrite = True

csv_output_params = {
    'activation': True,
    'output_sep': ',',
    # 可能内容里也有该分隔符，容易导致错误，所以内容里该分隔符的部分可以替换为新的符号
    'repl_to_sub_sep': '，',
    # 导入数据的记录条数, 等于几就表示从几开始增加, 默认为0, 表示从0开始增加计算
    'output_index_size': 0,
}

xls_output_params = {
    'activation': True,
    'output_sheet': 'Sheet1',
    # 导入数据的记录条数, 等于几就表示从几开始增加, 默认为0, 表示从0开始增加计算
    'output_index_size': 0,
}

md_output_params = {
    'activation': True,
    # 导入数据的记录条数, 等于几就表示从几开始增加, 默认为0, 表示从0开始增加计算
    'output_index_size': 0,
}

sql_output_params = {
    'activation': True,
    # 导出表的基本信息 - 表名，默认值为temp_table
    'table_name': 'table_for_temp_use',
    # 导出表的备注
    'table_comment': '临时表, 可删除',
    # 导出表的基本信息 - 各字段长度，默认为空字典，导出时自动填充数据; 如填写则会和实际数据进行比较, dict[key: str, value: int]
    'table_structure': {},
    # 导出表的各个字段的备注, dict[str, str], key: column, value: comment for column. e.g. {'col1': 'comment1', 'col2': 'comment2'}
    'column_comments': {
        # 'TABLE_AFFILIATION': '归属地'
    },
    # 选择导出的数据库类型，请注意大小写必须严格遵循下面的可选项
    'database': 'Oracle',
    # DATABASE里的可选项，作用仅为提示DATABASE里可写的数据库引擎
    'database_options': ['Oracle', 'GBase', 'MySql', 'PostgreSql', 'SqlServer', 'TdSql'],
    # 如果涉及到需要将数据从字符串转为DATETIME, 或者需要pandas里数据类型为datetime64的转为合适的DATETIME的插入语句
    # key: 列名, value: 导出数据的格式(基于database); 如仅填写key,而value为""，则表示将字符串转DATETIME, 默认转换类型为2023-11-09 13:23:44
    # 如不填写, 则默认按照格式转换的部分来判断是否在INSERT语句中转为DATETIME的语句
    # SQL SERVER 不需要填写
    'to_date_formats': {
        'column_name': 'yyyy-mm-dd hh24:mi:ss', # 以oracle为样例
    },
    # 可能内容里有半角逗号，这个在插入语句中是不被允许的，所以要替换成其他符号
    'repl_to_sub_comma': ';',
    # 导入数据的记录条数, 等于几就表示从几开始增加, 默认为0, 表示从0开始增加计算
    'output_index_size': 0,
}

