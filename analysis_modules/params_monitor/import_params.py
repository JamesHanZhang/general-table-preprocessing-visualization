
import copy
# self-made modules
from analysis_modules import default_properties as prop
from analysis_modules.params_monitor.params_basic_setting import ParamsBasicSetting
import import_params_setting as iparams # 打包的时候要去掉

# pyinstaller打包专用, 将iparams.去掉后, 将import_params_setting.py放到主程序同目录下, 打包后该主程序对于import_params_setting.py强依赖, 可通过参数表修改程序

############################ 以下专门为pyinstaller设置 ##################################
# Relative path to the parameter script 以下打包的时候取消注释
# script_path = './import_params_setting.py'
# # Execute the external parameter script
# with open(script_path, encoding='utf-8') as f:
#     exec(compile(f.read(), script_path, 'exec'))
    
############################ 以上专门为pyinstaller设置 ##################################

class ImportParams(ParamsBasicSetting):
    def __init__(self):
        super().__init__()

        # 初始化变量
        self.input_path = self.get_abspath(prop.INPUT_PATH, iparams.input_path)
        self.input_file = iparams.input_file
        self.input_encoding = self.check_if_encoding(iparams.input_encoding, prop.DEFAULT_ENCODING)
        self.quote_as_object = self.check_if_type(iparams.quote_as_object, 'quote_as_object')
        self.if_circular = self.check_if_type(iparams.if_circular, 'if_circular')
        self.chunksize = self.check_if_type(iparams.chunksize, 'chunksize', int)
        self.import_index_size = self.check_if_type(iparams.import_index_size, 'import_index_size', int)
        self.batch_import_params = self.BatchImportParams()
        self.csv_import_params = self.CsvImportParams()
        self.xls_import_params = self.XlsImportParams()
        if self.batch_import_params.if_batch is True:
            self.input_file = ""

    def get_import_params(self) -> dict:
        # 深拷贝: 完整将元素及嵌套的元素复制，确保没有共享引用;否则修改__dict__就是在修改该对象的元素
        params = copy.deepcopy(self.__dict__)
        params['batch_import_params'] = copy.deepcopy(self.batch_import_params.__dict__)
        params['csv_import_params'] = copy.deepcopy(self.csv_import_params.__dict__)
        params['xls_import_params'] = copy.deepcopy(self.xls_import_params.__dict__)
        return params

    def store_import_params(self, params_set: str=prop.DEFAULT_PARAMS_SET):
        # 将参数保存到json参数表内
        import_params_dict = self.get_import_params()
        self.store_params("import_params", import_params_dict, params_set)

    def load_import_params(self, params_set: str=prop.DEFAULT_PARAMS_SET):
        # 从json参数表里读取参数
        process_params = self.read_process_params(params_set)
        import_params = process_params['import_params']
        self.input_path = import_params['input_path']
        self.input_file = import_params['input_file']
        self.input_encoding = import_params['input_encoding']
        self.quote_as_object = import_params['quote_as_object']
        self.if_circular = import_params['if_circular']
        self.chunksize = import_params['chunksize']
        self.import_index_size = import_params['import_index_size']
        
        self.batch_import_params.if_batch = import_params['batch_import_params']['if_batch']
        self.batch_import_params.import_type = import_params['batch_import_params']['import_type']
        
        self.csv_import_params.input_sep = import_params['csv_import_params']['input_sep']
        self.csv_import_params.character_size = import_params['csv_import_params']['character_size']
        self.csv_import_params.quote_none = import_params['csv_import_params']['quote_none']
        self.csv_import_params.sep_to_sub_multi_char_sep = import_params['csv_import_params']['sep_to_sub_multi_char_sep']
        self.csv_import_params.repl_to_sub_sep = import_params['csv_import_params']['repl_to_sub_sep']
        
        self.xls_import_params.input_sheet = import_params['xls_import_params']['input_sheet']

    
    class BatchImportParams:
        def __init__(self):
            self.if_batch = iparams.batch_import_params['if_batch']
            self.import_type = iparams.batch_import_params['import_type']
            
    class CsvImportParams:
        def __init__(self):
            self.input_sep = iparams.csv_import_params['input_sep']
            self.character_size = iparams.csv_import_params['character_size']
            self.quote_none = iparams.csv_import_params['quote_none']
            self.sep_to_sub_multi_char_sep = iparams.csv_import_params['sep_to_sub_multi_char_sep']
            self.repl_to_sub_sep = iparams.csv_import_params['repl_to_sub_sep']

    class XlsImportParams:
        def __init__(self):
            self.input_sheet = iparams.xls_import_params['input_sheet']
