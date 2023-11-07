
import copy
# self-made modules
from analysis_modules import default_properties as prop
from analysis_modules.params_monitor.params_basic_setting import ParamsBasicSetting
import basic_process_params_setting as bproparams # 打包的时候要删除

# pyinstaller打包专用, 将bproparams.去掉后, 将basic_process_params_setting.py放到主程序同目录下,
# 打包后该主程序对于basic_process_params_setting.py强依赖, 可通过参数表修改程序

############################ 以下专门为pyinstaller设置 ##################################
# Relative path to the parameter script 以下打包的时候取消注释
# script_path = './basic_process_params_setting.py'
# # Execute the external parameter script
# with open(script_path, encoding='utf-8') as f:
#     exec(compile(f.read(), script_path, 'exec'))

############################ 以上专门为pyinstaller设置 ##################################

class BasicProcessParams(ParamsBasicSetting):
    def __init__(self):
        super().__init__()

        # 初始化变量
        self.basic_processing_order = bproparams.basic_processing_order
        self.change_names_previously = self.ChangeNamesPreviously()
        self.change_names_finally = self.ChangeNamesFinally()
        self.change_types_opt = self.ChangeTypesOpt()
        self.pick_columns_opt = self.PickColumnsOpt()
        self.data_masking_opt = self.DataMaskingOpt()

    def get_basic_process_params(self) -> dict:
        # 深拷贝: 完整将元素及嵌套的元素复制，确保没有共享引用;否则修改__dict__就是在修改该对象的元素
        params = copy.deepcopy(self.__dict__)
        params['change_names_previously'] = copy.deepcopy(self.change_names_previously.__dict__)
        params['change_names_finally'] = copy.deepcopy(self.change_names_finally.__dict__)
        params['change_types_opt'] = copy.deepcopy(self.change_types_opt.__dict__)
        params['pick_columns_opt'] = copy.deepcopy(self.pick_columns_opt.__dict__)
        params['data_masking_opt'] = copy.deepcopy(self.data_masking_opt.__dict__)
        return params

    def store_basic_process_params(self, params_set: str=prop.DEFAULT_PARAMS_SET):
        # 将参数保存到json参数表内
        basic_process_params_dict = self.get_basic_process_params()
        self.store_params("basic_process_params", basic_process_params_dict, params_set)

    def load_basic_process_params(self, params_set: str=prop.DEFAULT_PARAMS_SET):
        # 从json参数表里读取参数
        process_params = self.read_process_params(params_set)
        basic_process_params = process_params['basic_process_params']
        self.basic_processing_order = basic_process_params['basic_processing_order']
        
        self.change_names_previously.activation = basic_process_params['change_names_previously']['activation']
        self.change_names_previously.change_names = basic_process_params['change_names_previously']['change_names']
        
        self.change_names_finally.activation = basic_process_params['change_names_finally']['activation']
        self.change_names_finally.change_names = basic_process_params['change_names_finally']['change_names']
        
        self.change_types_opt.activation = basic_process_params['change_types_opt']['activation']
        self.change_types_opt.change_types = basic_process_params['change_types_opt']['change_types']
        
        self.pick_columns_opt.activation = basic_process_params['pick_columns_opt']['activation']
        self.pick_columns_opt.pick_columns = basic_process_params['pick_columns_opt']['pick_columns']
        
        self.data_masking_opt.activation = basic_process_params['data_masking_opt']['activation']
        self.data_masking_opt.masking_type = basic_process_params['data_masking_opt']['masking_type']
        self.data_masking_opt.masking_type_choices = basic_process_params['data_masking_opt']['masking_type_choices']
        self.data_masking_opt.masking_columns = basic_process_params['data_masking_opt']['masking_columns']

    class ChangeNamesPreviously:
        def __init__(self):
            self.activation = bproparams.change_names_previously['activation']
            self.change_names = bproparams.change_names_previously['change_names']
            
    class ChangeNamesFinally:
        def __init__(self):
            self.activation = bproparams.change_names_finally['activation']
            self.change_names = bproparams.change_names_finally['change_names']
    
    class ChangeTypesOpt:
        def __init__(self):
            self.activation = bproparams.change_types_opt['activation']
            self.change_types = bproparams.change_types_opt['change_types']
    
    class PickColumnsOpt:
        def __init__(self):
            self.activation = bproparams.pick_columns_opt['activation']
            self.pick_columns = bproparams.pick_columns_opt['pick_columns']
            
    class DataMaskingOpt:
        def __init__(self):
            self.activation = bproparams.data_masking_opt['activation']
            self.masking_type = bproparams.data_masking_opt['masking_type']
            self.masking_type_choices = bproparams.data_masking_opt['masking_type_choices']
            self.masking_columns = bproparams.data_masking_opt['masking_columns']