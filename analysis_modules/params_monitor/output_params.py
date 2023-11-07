
import copy
# self-made modules
from analysis_modules import default_properties as prop
from analysis_modules.params_monitor.import_params import ImportParams
from analysis_modules.params_monitor.params_basic_setting import ParamsBasicSetting
import output_params_setting as oparams # 打包的时候要去掉

# pyinstaller打包专用, 将oparams.去掉后, 将output_params_setting.py放到主程序同目录下, 打包后该主程序对于output_params_setting.py强依赖, 可通过参数表修改程序

############################ 以下专门为pyinstaller设置 ##################################
# Relative path to the parameter script 以下打包的时候取消注释
# script_path = './output_params_setting.py'
# # Execute the external parameter script
# with open(script_path, encoding='utf-8') as f:
#     exec(compile(f.read(), script_path, 'exec'))


############################ 以上专门为pyinstaller设置 ##################################

class OutputParams(ParamsBasicSetting):
    def __init__(self):
        super().__init__()

        # 初始化变量
        self.output_path = self.get_abspath(prop.OUTPUT_PATH, oparams.output_path)
        self.output_file = oparams.output_file
        self.output_encoding = self.get_encoding(oparams.output_encoding, prop.DEFAULT_ENCODING)
        self.if_sep = self.check_if_type(oparams.if_sep, 'if_sep')
        self.only_one_chunk = self.check_if_type(oparams.only_one_chunk, 'only_one_chunk')
        # 只有在if_sep为False的情况下，才可以调整overwrite
        self.overwrite = self.check_if_type(oparams.overwrite, 'overwrite') if oparams.if_sep is False else True
        self.get_params_from_import_params()
        self.md_output_params = self.MdOutputParams()
        self.csv_output_params = self.CsvOutputParams()
        self.xls_output_params = self.XlsOutputParams()
        self.sql_output_params = self.SqlOutputParams()
        
    def get_params_from_import_params(self):
        import_params = ImportParams()
        self.chunksize = import_params.chunksize

    def get_output_params(self) -> dict:
        # 深拷贝: 完整将元素及嵌套的元素复制，确保没有共享引用;否则修改__dict__就是在修改该对象的元素
        params = copy.deepcopy(self.__dict__)
        params['md_output_params'] = copy.deepcopy(self.md_output_params.__dict__)
        params['csv_output_params'] = copy.deepcopy(self.csv_output_params.__dict__)
        params['xls_output_params'] = copy.deepcopy(self.xls_output_params.__dict__)
        params['sql_output_params'] = copy.deepcopy(self.sql_output_params.__dict__)
        return params

    def store_output_params(self, params_set: str=prop.DEFAULT_PARAMS_SET):
        # 将参数保存到json参数表内
        output_params_dict = self.get_output_params()
        self.store_params("output_params", output_params_dict, params_set)

    def load_output_params(self, params_set: str=prop.DEFAULT_PARAMS_SET):
        # 从json参数表里读取参数
        process_params = self.read_process_params(params_set)
        output_params = process_params['output_params']
        self.output_path = output_params['output_path']
        self.output_file = output_params['output_file']
        self.output_encoding = output_params['output_encoding']
        self.chunksize = output_params['chunksize']
        self.if_sep = output_params['if_sep']
        self.only_one_chunk = output_params['only_one_chunk']
        self.overwrite = output_params['overwrite']
        
        # md params
        self.md_output_params.activation = output_params['md_output_params']['activation']
        self.md_output_params.output_index_size = output_params['md_output_params']['output_index_size']

        # csv params
        self.csv_output_params.activation = output_params['csv_output_params']['activation']
        self.csv_output_params.output_sep = output_params['csv_output_params']['output_sep']
        self.csv_output_params.repl_to_sub_sep = output_params['csv_output_params']['repl_to_sub_sep']
        self.csv_output_params.output_index_size = output_params['csv_output_params']['output_index_size']
        
        # xls params
        self.xls_output_params.activation = output_params['xls_output_params']['activation']
        self.xls_output_params.output_sheet = output_params['xls_output_params']['output_sheet']
        self.xls_output_params.output_index_size = output_params['xls_output_params']['output_index_size']
        
        # sql params
        self.sql_output_params.activation = output_params['sql_output_params']['activation']
        self.sql_output_params.table_name = output_params['sql_output_params']['table_name']
        self.sql_output_params.table_comment = output_params['sql_output_params']['table_comment']
        self.sql_output_params.table_structure = output_params['sql_output_params']['table_structure']
        self.sql_output_params.column_comments = output_params['sql_output_params']['column_comments']
        self.sql_output_params.database = output_params['sql_output_params']['database']
        self.sql_output_params.database_options = output_params['sql_output_params']['database_options']
        self.sql_output_params.repl_to_sub_comma = output_params['sql_output_params']['repl_to_sub_comma']
        self.sql_output_params.output_index_size = output_params['sql_output_params']['output_index_size']

    class CsvOutputParams:
        def __init__(self):
            self.activation = oparams.csv_output_params['activation']
            self.output_sep = oparams.csv_output_params['output_sep']
            self.repl_to_sub_sep = oparams.csv_output_params['repl_to_sub_sep']
            self.output_index_size = oparams.csv_output_params['output_index_size']

    class XlsOutputParams:
        def __init__(self):
            self.activation = oparams.xls_output_params['activation']
            self.output_sheet = oparams.xls_output_params['output_sheet']
            self.output_index_size = oparams.xls_output_params['output_index_size']
    
    class MdOutputParams:
        def __init__(self):
            self.activation = oparams.md_output_params['activation']
            self.output_index_size = oparams.md_output_params['output_index_size']

    class SqlOutputParams:
        def __init__(self):
            self.activation = oparams.sql_output_params['activation']
            self.table_name = oparams.sql_output_params['table_name']
            self.table_comment = oparams.sql_output_params['table_comment']
            self.table_structure = oparams.sql_output_params['table_structure']
            self.column_comments = oparams.sql_output_params['column_comments']
            self.database = oparams.sql_output_params['database']
            self.database_options = oparams.sql_output_params['database_options']
            self.repl_to_sub_comma = oparams.sql_output_params['repl_to_sub_comma']
            self.output_index_size = oparams.sql_output_params['output_index_size']
