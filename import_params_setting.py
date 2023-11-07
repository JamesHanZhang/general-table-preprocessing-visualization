# 以下可添加绝对路径，如为空值""，则为默认导入路径input_dataset，也可添加默认路径下input_dataset的子文件夹，例如:
# 如添加子文件夹child_folder/split1，则实际路径为:../input_dataset/child_folder/split1
input_path = ""

# 导入的文件名(需携带拓展名, e.g. test.csv), 如果if_batch = True, 则采用批量导入的方式, 无需填写
input_file = "input_test.md"

# 批量导入的参数
batch_import_params = {
    # 判断是否根据导入路径批量导入数据, False表示单文件模式, 不批量导入
    # 仅支持多个同数据结构的文件导入合并为一
    'if_batch': False,
    # 设置批量导入的数据类型，例如imp_type = ".csv", 如果设置为""空值，则表示全部导入
    'import_type': '.csv',
}

# 加载时的解码格式默认值：input_encoding = "utf-8" 或者中文环境下常用"gb18030"
# 如果为""空值，则默认开启自动探测文件编码charset模式，会自动通过选取前10240bytes的数据进行校验检查
input_encoding = ""

# 确认是否直接导入（能保持数据类型），还是以字符串的形式导入（能尽量避免数据遗失）
# True: 以字符串类型导入，False: 直接导入
quote_as_object = True

# 用于判断是否通过循环读取处理数据来处理大数据，默认值为False，表示一次读取所有数据返回df
if_circular = True

# 针对if_circular is True: 每次执行chunksize条数据；另，如果导出的时候要拆分为小片数据，也是依据该值进行拆分的
chunksize = 50000


# 导入数据的记录条数, 等于几就表示从几开始增加, 默认为0, 表示从0开始增加计算
import_index_size = 0

csv_import_params = {
    'input_sep': ',',
    # CSV校验，转存转取的时候，用来限制一次IO写入的字符数，影响读取数据的速度
    'character_size': 5000000,
    # 判断是否读取csv的时候要将双引号"视为分隔符的一部分(如果贴近分隔符的话)，还是视为数据内容进行读取
    # 如为真则视为数据内容进行读取，为假则视为分隔符的一部分，默认为假
    'quote_none': False,
    # 当导入的CSV的分隔符>1位长度的时候，判断为变长分隔符，是不好导入为CSV的，需要替换为新的1位分隔符
    'sep_to_sub_multi_char_sep': ';',
    # 当导入的CSV分隔符>1位长的时候，替换为新的1位分隔符，可能内容里也有该分隔符，会导致错误，所以内容里该分隔符的部分要替换为新的符号
    'repl_to_sub_sep': '.|.'
}

xls_import_params = {
    'input_sheet': 'Sheet1'
}

# 暂时没有参数需要调整
md_import_params = {}