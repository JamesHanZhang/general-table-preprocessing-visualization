from tqdm import tqdm
from analysis_modules import default_properties as prop
from analysis_modules.default_properties import ParamsMode, OutputMode
from analysis_modules.app_entrances.format_transformation import FormatTransformation
from analysis_modules.params_monitor import *
from basic_operation import FindChildPaths, IoMethods


class DiffTransBatchFiles(FormatTransformation):
    def __init__(self):
        """
        根据同一个导入导出中间参数表, 批量执行同一个文件夹下的多个文件的不同转换. 转换出的文件名/表名与导入的文件一致
        """
        super().__init__()
        self.params_set = prop.DEFAULT_PARAMS_SET
        
    
    def get_batch_files_under_input_path(self, import_type=".csv") -> dict[str, list[str]]:
        input_encoding = self.import_params.input_encoding
        input_path = self.import_params.input_path
        path_finder = FindChildPaths(input_encoding)
        path_file_pairs = path_finder.gain_child_certain_type_path_file_pairs(input_path, import_type)
        return path_file_pairs
    
    @SysLog().calculate_cost_time("<running single file transformation with same params_set>")
    def run_with_input_file_as_output_file(self, params_set, params_mode:ParamsMode, output_mode:OutputMode, input_file, input_path):
        SysLog.show_log(f"[RUNNING FILE DISTINCT TRANSFORMATION] file '{input_file}' is being transfered...")
        output_file_main_part = IoMethods.get_main_file_name(input_file)
        output_extension = IoMethods.get_file_extension(self.output_params.output_file)
        # 将导入文件的名称设为导出文件的名称
        output_file = output_file_main_part + output_extension
        # 将导入文件的名称设为导出的表名
        sql_table_name = output_file_main_part
        self.reset_params(params_set, params_mode, output_mode, input_path=input_path, input_file=input_file, output_file=output_file,
                          table_name=sql_table_name)
        self.run_based_on_params_set(params_set, params_mode, output_mode, if_multi=True)
        SysLog.show_log(f"[DISTINCT TRANSFORMATION END] file '{input_file}' is successfully transfered.")
        return
        
    def diff_trans_batch_files(self, params_set="", params_mode=ParamsMode.FROM_SETTING, output_mode=OutputMode.FREE_MODE,
                               import_type="", input_path="", output_path=""):
        """
        :param params_set: 复用同一个params_set的设置
        :param params_mode:
                        FROM_SETTING:   1. 通过_params_setting.py来设定参数, 会自动覆盖同名参数表;
                        FROM_EXISTS:    2. 通过已经存在的resources里的参数文件来确定参数, 如该参数文件不存在则报错;
                        FROM_BASE:      3. 通过修改resources里已经有的基本参数表BASE_PARAMS_SET来确定新的参数表
        :param output_mode: 判断是按照导出文件的拓展名来判断导出，还是按照激活功能activation来判断导出
                        ACTIVATION_MODE <根据激活导出模式>: 采用'output_params_setting.py'中的激活功能判断是否导出对应格式的数据;
                                        该模式激活几个功能就导出几个文件(激活拆分功能则更多);
                                        该模式在导出'.sql'文件时, 采用参数'table_name'确定导出的表名及文件名;
                        EXTENSION_MODE  <根据拓展名导出模式>采用导出文件output_file的拓展名(例如'test.xlsx')判断是导出哪种格式数据;
                                        模式一次仅激活一个导出功能;
                                        该模式在导出'.sql'文件时, 默认将临时表的表名设置为导出文件的主体名(去掉拓展名);
                        FREE_MODE       <自动模式>, 根据导出的文件名'output_file'是否有拓展名(例如'test.xlsx')来判断采取以上两种模式的哪种模式;
                                        如导出的文件名没有拓展名, 即只有纯粹的文件名(例如'test'), 则激活<根据激活导出模式>;
                                        如导出的文件名有拓展名(例如'test.xlsx'), 则激活<根据拓展名导出模式>;
        :param import_type: 是否根据数据类型决定导入, 为""表示导入所有数据类型的文件
        :param input_path: 批量导入的路径, 如不填写则默认为参数表的导入路径
        :param input_path: 批量导出的路径, 如不填写则默认为参数表的导出路径
        :return: 根据导入路径批量单独转换文件(不涉及合并, 仅为每个文件单独转换), 复用同一个params_set参数表, 转换出的文件名/表名与导入的文件一致
        """
        if params_set == "":
            params_set = self.params_set
            
        start_time = start_program()
        self.reset_params(params_set, params_mode=params_mode, output_mode=output_mode, input_path=input_path, output_path=output_path)
        # 执行程序
        self.import_params, self.output_params, self.basic_process_params = IntegrateParams.get_params(params_set, params_mode)
        path_file_pairs = self.get_batch_files_under_input_path(import_type)
        for input_path in tqdm(path_file_pairs.keys(),position=True,leave=True,desc="different input paths (including child paths) running..."):
            for input_file in tqdm(path_file_pairs[input_path],position=True,leave=True,desc="differnet file transformation running..."):
                self.run_with_input_file_as_output_file(params_set, params_mode=ParamsMode.FROM_EXISTS, output_mode=output_mode,
                                                        input_file=input_file, input_path=input_path)
        end_program(start_time)
        return
    
if __name__ == "__main__":
    dtbf = DiffTransBatchFiles()
    dtbf.diff_trans_batch_files(params_mode=ParamsMode.FROM_SETTING,output_mode=OutputMode.FREE_MODE, import_type='.csv')