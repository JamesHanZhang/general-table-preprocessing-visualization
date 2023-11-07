from analysis_modules.params_monitor.import_params import ImportParams
from analysis_modules.params_monitor.output_params import OutputParams
from analysis_modules.params_monitor.basic_process_params import BasicProcessParams
from analysis_modules.params_monitor.resources_operation import ResourcesOperation
from analysis_modules.params_monitor.sys_log import SysLog
import analysis_modules.default_properties as prop
from analysis_modules.default_properties import ParamsMode

class IntegrateParams:
    def __init__(self):
        pass
    
    @staticmethod
    def init_basic_params(params_set:str=""):
        if params_set == "":
            params_set = prop.DEFAULT_PARAMS_SET
        return params_set
    
    @classmethod
    def get_params_from_settings(cls, params_set: str = prop.DEFAULT_PARAMS_SET) -> tuple[ImportParams, OutputParams, BasicProcessParams]:
        params_set = cls.init_basic_params(params_set)
        ro = ResourcesOperation()
        import_params = ImportParams()
        output_params = OutputParams()
        basic_process_params = BasicProcessParams()
        ro.remove_resources_file(params_set)
        import_params.store_import_params(params_set)
        output_params.store_output_params(params_set)
        basic_process_params.store_basic_process_params(params_set)
        SysLog.show_log(f"[PARAMS] parameters initialization from settings, params set file '{params_set}.json' is created or overwritten.")
        return import_params, output_params, basic_process_params

    @classmethod
    def get_params_from_resources(cls, params_set: str=prop.DEFAULT_PARAMS_SET) -> tuple[ImportParams, OutputParams, BasicProcessParams]:
        params_set = cls.init_basic_params(params_set)
        ro = ResourcesOperation()
        ro.check_if_params_set_exists(params_set, pop_error=True)
        import_params = ImportParams()
        output_params = OutputParams()
        basic_process_params = BasicProcessParams()
        import_params.load_import_params(params_set)
        output_params.load_output_params(params_set)
        basic_process_params.load_basic_process_params(params_set)
        SysLog.show_log(
            f"[PARAMS] parameters initialization from existing params file '{params_set}.json'.")
        return import_params, output_params, basic_process_params
    
    @classmethod
    def set_base_params_set(cls, renew:bool=False):
        """
        :param renew: 是否要更新base_params_set
        :return:
        """
        base_params_set = prop.BASE_PARAMS_SET
        ro = ResourcesOperation()
        # 只有base_params_set不存在的情况下才需要新建
        if (not ro.check_if_params_set_exists(base_params_set, pop_error=False)) or renew:
            SysLog.show_log(f"base params set file '{base_params_set}.json' doesn't exist, "
                            f"or is forced to be overwritten.")
            cls.get_params_from_settings(base_params_set)
        return
    @classmethod
    def get_params_from_base_params_set(cls, params_set: str = prop.DEFAULT_PARAMS_SET) -> tuple[ImportParams, OutputParams, BasicProcessParams]:
        params_set = cls.init_basic_params(params_set)
        base_params_set = prop.BASE_PARAMS_SET
        cls.set_base_params_set()
        import_params, output_params, basic_process_params = cls.get_params_from_resources(base_params_set)
        import_params.store_import_params(params_set)
        output_params.store_output_params(params_set)
        basic_process_params.store_basic_process_params(params_set)
        SysLog.show_log(f"[PARAMS] parameters initialization from '{base_params_set}.json', "
                        f"params set file '{params_set}.json' is created or overwritten.")
        return import_params, output_params, basic_process_params
    
    @classmethod
    def get_params(cls, params_set=prop.DEFAULT_PARAMS_SET,
                   params_mode=ParamsMode.FROM_SETTING) -> tuple[ImportParams, OutputParams, BasicProcessParams]:
                   
        """
        :param params_set: 参数表名
        :param params_import_opt: 导入参数的模式
        :return: 返回参数值
        """""
        params_set = cls.init_basic_params(params_set)
        
        if params_mode == ParamsMode.FROM_SETTING:
            import_params, output_params, basic_process_params = cls.get_params_from_settings(params_set)
        elif params_mode == ParamsMode.FROM_EXISTS:
            import_params, output_params, basic_process_params = cls.get_params_from_resources(params_set)
        elif params_mode == ParamsMode.FROM_BASE:
            import_params, output_params, basic_process_params = cls.get_params_from_base_params_set(params_set)
        else:
            raise AttributeError("params_opt must be ParamsOpt Type!")
        return import_params, output_params, basic_process_params
        
    
if __name__ == "__main__":
    # 主要用来更新base_params_set
    IntegrateParams.set_base_params_set(renew=True)