

import os
import codecs
import time
import json
# self-made modules
from basic_operation import IoMethods
from analysis_modules.params_monitor.sys_log import SysLog
import analysis_modules.default_properties as prop
from analysis_modules.params_monitor.resources_operation import ResourcesOperation

class ParamsBasicSetting:
    def __init__(self):
        pass
    
    def check_if_type(self, value, param_name, type=bool):
        if isinstance(value, type):
            return value
        else:
            msg = f"the parameter {param_name} you entered must be {str(type)} type!"
            print(msg)
            time.sleep(3)
            raise TypeError(msg)
    
    def check_if_encoding(self, encoding, default_encoding):
        # 如果为空则返空，有其他的处理方式
        # 如果不为空但填错，则直接写默认值
        if encoding == "":
            return encoding
        if codecs.lookup(encoding):
            return encoding.lower()
        SysLog.show_log(f"[INCORRECT ENCODING] rewrite the encoding '{encoding}' with default encoding '{default_encoding}'")
        return default_encoding.lower()
    
    def get_encoding(self, new_encoding, default_encoding):
        if new_encoding is None or new_encoding == "":
            return default_encoding.lower()
        new_encoding = self.check_if_encoding(new_encoding, default_encoding)
        return new_encoding

    def get_abspath(self, parent_path, target_path=""):
        # target_path为选填目录，绝对路径则直接采用，相对路径则接到默认目录parent_path下
        if target_path=="":
            # 没填则为默认值
            return parent_path
        elif os.path.isabs(target_path) is True:
            # 绝对路径则直接返回
            return target_path
        # 延长路径
        return IoMethods.join_path(parent_path, target_path)

    def read_process_params(self, params_set: str=prop.DEFAULT_PARAMS_SET):
        process_params = ResourcesOperation.read_resource(params_set)
        return process_params

    def store_params(self, app_name: str, params: dict, params_set: str=prop.DEFAULT_PARAMS_SET):
        ro = ResourcesOperation()
        process_params = dict()
        try:
            process_params = ro.read_resource(params_set)
        except FileNotFoundError:
            pass
        process_params[app_name] = params
        ro.store_params_as_json(params_set, process_params)
        return
