import time
from analysis_modules import default_properties as prop
from analysis_modules.default_properties import ParamsMode, OutputMode
from analysis_modules.params_monitor import *
from basic_operation import IoMethods
from analysis_modules.df_import_drivers import DfCreation
from analysis_modules.df_processing import BasicProcessing
from analysis_modules.df_output_drivers import DfOutput
from analysis_modules.sql_output_drivers import SqlOutput

class FormatTransformation:
    def __init__(self):
        self.params_set = prop.DEFAULT_PARAMS_SET
        self.ro = ResourcesOperation()
        self.dc = DfCreation()
        self.bp = BasicProcessing()
        self.do = DfOutput()
        self.so = SqlOutput()
    
    
    def set_output_mode(self, output_file:str="", output_mode=OutputMode.FREE_MODE):
        """
        :param output_file: 判断是按照导出文件的拓展名来判断导出，还是 <按照激活功能activation来判断导出>
        :param output_mode: 直接根据设置判断导出的模式
        :return:
        """
        if output_mode == OutputMode.FREE_MODE:
            output_mode = OutputMode.ACTIVATION_MODE
            if output_file == "":
                output_file = self.output_params.output_file
            extension = IoMethods.get_file_extension(output_file)
            if extension != "":
                output_mode = OutputMode.EXTENSION_MODE
            return output_mode
        return output_mode
    

    def reset_params(self, params_set=prop.DEFAULT_PARAMS_SET, params_mode=ParamsMode.FROM_SETTING, output_mode=OutputMode.FREE_MODE,
                     input_file="", input_path="", output_file="", output_path="", table_name="", if_batch:bool=None,
                     if_circular:bool=None, if_sep:bool=None, only_one_chunk:bool=None, chunksize:int=0):
        """
        :param params_set: .json的参数表名称, 不加拓展名
        :param input_file: 导入文件
        :param input_path: 导入路径
        :param output_file: 导出文件名(如含拓展名, 则除非设置固定了按照激活方式, 否则自动转按照拓展名方式导出)
        :param output_path: 导出路径
        :param table_name: 导出sql的table name, 如果 based_on_activation is False, 则无效化
        :param if_batch: 是否根据文件夹批量导入(使得导入文件名无效化)
        :param if_circular: 是否循环导入(针对大文件)
        :param if_sep: 是否拆分(针对大文件)
        :param only_one_chunk: 是否只拆出第一个样例即可
        :param chunksize: 拆分/循环读取的各切片最大的记录条数
        :return: 修订公用参数并保存到.json参数表
        """
        if params_set == "":
            params_set = self.params_set
        
        self.import_params, self.output_params, self.basic_process_params = IntegrateParams.get_params(params_set, params_mode)
        self.output_mode = self.set_output_mode(output_file, output_mode)
        
        if IoMethods.get_file_extension(input_file) != "":
            self.import_params.input_file = input_file
        if input_path != "" and os.path.isabs(input_path) is True:
            self.import_params.input_path = input_path
        if if_batch is not None and type(if_batch) is bool:
            self.import_params.batch_import_params.if_batch = if_batch
        if if_circular is not None and type(if_circular) is bool:
            self.import_params.if_circular = if_circular
        if chunksize > 0:
            self.import_params.chunksize = chunksize
            self.output_params.chunksize = chunksize
        if table_name != "":
            self.output_params.sql_output_params.table_name = table_name
        if output_path != "" and os.path.isabs(output_path) is True:
            self.output_params.output_path = output_path
        if if_sep is not None and type(if_sep) is bool:
            self.output_params.if_sep = if_sep
        if only_one_chunk is not None and type(only_one_chunk) is bool:
            self.output_params.only_one_chunk = only_one_chunk
            
        if self.output_mode == OutputMode.ACTIVATION_MODE:
            if output_file != "":
                self.output_params.output_file = output_file
        else:
            extension = IoMethods.get_file_extension(output_file)
            if extension != "":
                self.output_params.output_file = output_file
            if extension == ".sql":
                self.output_params.sql_output_params.table_name = IoMethods.get_main_file_name(output_file)
                
        
        # 保存参数
        self.import_params.store_import_params(params_set)
        self.output_params.store_output_params(params_set)
    
    def process_data(self, df, params_set,chunk_no:int=""):
        # 计算记录条数
        self.dc.count_row_num(df, self.import_params, params_set)
        # 执行处理过程
        df = self.bp.basic_process_data(df, self.basic_process_params)
        if self.output_mode == OutputMode.ACTIVATION_MODE:
            self.do.output_df_on_activation(df, self.output_params, params_set, chunk_no=chunk_no)
            self.so.output_sql_on_activation(df, self.output_params, params_set, chunk_no=chunk_no)
        else:
            self.do.output_df_on_extension(df, self.output_params, params_set, chunk_no=chunk_no)
            self.so.output_sql_on_extension(df, self.output_params, params_set, chunk_no=chunk_no)
        return
    
    def run_processing_chunk_reader(self, params_set):
        chunk_reader = self.dc.fully_import_data(self.import_params, params_set)
        chunk_no = 0
        for chunk in chunk_reader:
            self.process_data(chunk, params_set, chunk_no)
            chunk_no += 1
        return
    
    def run_processing_whole_data(self, params_set):
        df = self.dc.import_one_file_on_extension(self.import_params, params_set)
        self.process_data(df, params_set)
        return
        
    
    def run_based_on_params_set(self, params_set=prop.DEFAULT_PARAMS_SET, params_mode=ParamsMode.FROM_SETTING,
                                output_mode=OutputMode.FREE_MODE, if_multi=False):
        """
        主程序入口
        :param params_set: .json的参数表名称, 不加拓展名
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
        :param if_multi: 看是不是批量跑多个参数表的程序
        """
        if params_set == "":
            params_set = self.params_set
        
        if if_multi is False:
            # 判断是否这个函数只跑一次
            start_time = start_program()
        # 执行程序
        self.import_params, self.output_params, self.basic_process_params = IntegrateParams.get_params(params_set, params_mode)
        self.output_mode = self.set_output_mode(self.output_params.output_file, output_mode)
        if_batch = self.import_params.batch_import_params.if_batch
        if_circular = self.import_params.if_circular
        
        if if_batch is False and if_circular is False:
            # 单文件全量读取并操作
            self.run_processing_whole_data(params_set)
        else:
            # 批量导入/单文件循环读取
            self.run_processing_chunk_reader(params_set)
            
        if if_multi is False:
            end_program(start_time)
            
    def create_diff_params_sets(self, params_sets: list[str]):
        """
        另: 建立多重参数表和执行多重参数表中间必须重启一次程序，因为只有开启程序才会编译代码，进程开启是不会再次编译代码的，.py文件的参数修改就不会被纳入
        所以无法建立多重参数表, 只能一个一个建立, 除非将多重参数表以.json文件的形式修改并导入
        所以这里用BASE_PARAMS_SET来直接修改参数
        """
        base_params_set = prop.BASE_PARAMS_SET
        count_num = len(params_sets)
        print("\n############## EXPLANATION ##############\n")
        msg = f"The params set will be created based on BASE_PARAMS_SET '{base_params_set}.json'.\n" \
              f"Total {count_num} params_sets waiting for creation\n\n" \
              f"根据基本参数表BASE_PARAMS_SET '{base_params_set}.json'来修改参数, 新建或覆盖参数表.\n" \
              f"总计{count_num}个参数表待建, 参数表参数含义与`_params_setting.py`一致\n" \
              f"!!!! 注意: 请勿使用IDE直接修改.json文件(会先保留在内存内导致修改无法实现), 需有保存的过程(推荐notepad++)"
        print(msg)
        print("\n############## PARAMS SETS CREATION ##############\n")
        for num in range(count_num):
            while True:
                ready = input(f"This is {num+1}th params set '{params_sets[num]}.json' setting, create params_set ready? (Y/N)\n"
                              f"这是第{num+1}个参数表'{params_sets[num]}.json'的设置\n"
                              f"是否准备完成? (完成选Y, 退出选N, 其他直接回车): ").strip()
                if ready in ['Yes','YES','Y', 'y', 'yes']:
                    break
                elif ready in ['No','NO','no','n','N']:
                    print("You choose to quit the program. \n您选择了退出.")
                    time.sleep(2)
                    exit()
            IntegrateParams.get_params(params_sets[num], params_mode=ParamsMode.FROM_BASE)
            time.sleep(1)
        return
    
    def run_multi_params_sets(self, params_sets:list[str], output_mode=OutputMode.FREE_MODE):
        """
        :param params_sets: 把参数名称集中起来跑，常用来跑不同文件的批量
        :param overwrite: 因为是不同文件的批量，肯定不能直接拿setting来填, 所以要引入文件参数表
        :param based_on_activation: 判断是按照导出文件的拓展名来判断导出，还是按照激活功能activation来判断导出
        """
        start_time = start_program()
        for params_set in params_sets:
            # 先判断有没有参数表
            self.ro.check_if_params_set_exists(params_set, pop_error=True)
            
        for params_set in params_sets:
            # 再执行参数表
            self.run_based_on_params_set(params_set, ParamsMode.FROM_EXISTS, output_mode, True)
        end_program(start_time)
    
    def create_run_multi_params_sets(self, params_sets:list[str], output_mode=OutputMode.FREE_MODE):
        self.create_diff_params_sets(params_sets)
        while True:
            if_run = input("Are you willing to execute the params_sets you just made? (Y/N): \n"
                       "您是否希望执行运行您刚设立的参数表集合? (Y/N): ").strip()
            if if_run in ['YES','Y','Yes','yes','y']:
                break
            elif if_run in ['No','NO','no','n','N']:
                print("You choose to quit the program. \n您选择了退出.")
                time.sleep(2)
                exit()
        self.run_multi_params_sets(params_sets, output_mode)
        
        
if __name__ == "__main__":
    # 单元测试
    ft = FormatTransformation()
    # ft.run_based_on_params_set(overwrite=True, based_on_activation=True)
    params_sets = ['test1','test2']
    ft.create_run_multi_params_sets(params_sets)