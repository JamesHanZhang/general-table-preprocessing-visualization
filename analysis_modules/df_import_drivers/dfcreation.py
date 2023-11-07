import os.path

import pandas as pd
import math
# self-made modules
from analysis_modules.df_import_drivers.xls_import_driver import XlsImportDriver
from analysis_modules.df_import_drivers.csv_import_driver import CsvImportDriver
from analysis_modules.df_import_drivers.md_import_driver import MdImportDriver
from basic_operation import *
from analysis_modules.params_monitor import SysLog, ImportParams
from analysis_modules import default_properties as prop

class DfCreation:
    def __init__(self):
        self.log = SysLog()
        self.csv_extensions = ['.csv']
        self.md_extensions = ['.md']
        self.xls_extensions = ['.xls', '.xlsx', '.xltx', '.xlsm', '.xlt', '.xltm', '.xlam', '.xla']
        self.supported_extensions = self.csv_extensions + self.md_extensions + self.xls_extensions
    
    def init_import_params(self, import_params: ImportParams, input_file="", input_path="", if_batch:bool=None,
                           if_circular:bool=None, import_type:str=None, input_encoding=""):
        """
        :return: 主要用来保证参数在整个类中的使用
        """
        self.input_file = import_params.input_file
        self.input_path = import_params.input_path
        self.if_batch = import_params.batch_import_params.if_batch
        self.if_circular = import_params.if_circular
        self.import_type = import_params.batch_import_params.import_type
        self.input_encoding = import_params.input_encoding
        self.chunksize = import_params.chunksize
        
        if input_file != "":
            # 确保导入的文件都能被读取
            self.input_file = input_file
        if os.path.isabs(input_path):
            self.input_path = input_path
        if if_batch is not None and type(if_batch) is bool:
            self.if_batch = if_batch
        if if_circular is not None and type(if_circular) is bool:
            self.if_circular = if_circular
        if import_type is not None and type(import_type) is str:
            self.import_type = import_type
        if input_encoding != "":
            self.input_encoding = import_params.check_if_encoding(input_encoding, import_params.input_encoding)
        return

    def check_extension(self, input_file: str) -> str:
        extension = IoMethods.get_file_extension(input_file)
        if extension not in self.supported_extensions:
            msg = "[TypeError]: the input file type is limited in these choices:" \
                  "             [Excel, CSV, MarkDown].\n" \
                  "             And the input file {a}'s extension doesn't follow the rules of these types.\n" \
                  "".format(a=input_file)
            self.log.show_log(msg)
            raise TypeError(msg)
        return extension

    def import_as_df(self, import_params: ImportParams, input_file: str="", input_path: str=""):
        self.init_import_params(import_params, input_file, input_path)
        extension = self.check_extension(self.input_file)
        if extension in self.csv_extensions:
            impdriver = CsvImportDriver(import_params)
            df = impdriver.fully_import_csv(self.input_file, self.input_path)
        elif extension in self.xls_extensions:
            impdriver = XlsImportDriver(import_params)
            df = impdriver.fully_import_excel(self.input_file, self.input_path)
        elif extension in self.md_extensions:
            impdriver = MdImportDriver(import_params)
            df = impdriver.fully_import_md(self.input_file, self.input_path)
        return df

    def import_as_df_generator(self, import_params: ImportParams, input_file: str="", input_path: str=""):
        self.init_import_params(import_params, input_file, input_path)
        extension = self.check_extension(self.input_file)
        circular_reading_types = self.csv_extensions + self.xls_extensions + self.md_extensions
        if extension in self.csv_extensions:
            impdriver = CsvImportDriver(import_params)
            chunk_reader = impdriver.circular_import_csv(self.input_file, self.input_path)
        elif extension in self.xls_extensions:
            impdriver = XlsImportDriver(import_params)
            chunk_reader = impdriver.circular_import_excel(self.input_file, self.input_path)
        elif extension in self.md_extensions:
            impdriver = MdImportDriver(import_params)
            chunk_reader = impdriver.circular_import_md(self.input_file, self.input_path)
        else:
            msg = f"only {str(circular_reading_types)} can be imported as generator for processing data piece by piece."
            raise TypeError(msg)
        return chunk_reader
    
    def init_import_entrance_params(self, import_params: ImportParams, params_set:str=prop.DEFAULT_PARAMS_SET,
                                    input_file="", input_path="", if_batch:bool=None, if_circular:bool=None,
                                    import_type:str=None, input_encoding=""):
        """
        :return: 主要用来更新import_params的参数, 并保存到参数表里
        """
        self.init_import_params(import_params, input_file=input_file, input_path=input_path, if_batch=if_batch,
                                if_circular=if_circular, import_type=import_type, input_encoding=input_encoding)
        
        # 将会影响整个导入过程的参数保存到参数表
        if IoMethods.get_file_extension(input_file) != "":
            import_params.input_file = input_file
        if os.path.isabs(input_path):
            import_params.input_path = input_path
        if if_batch is not None and type(if_batch) is bool:
            import_params.batch_import_params.if_batch = if_batch
        if import_type is not None and type(import_type) is str:
            import_params.batch_import_params.import_type = import_type
        if if_circular is not None and type(if_circular) is bool:
            import_params.if_circular = if_circular
        if input_encoding != "":
            import_params.input_encoding = import_params.check_if_encoding(input_encoding, import_params.input_encoding)
        
        import_params.store_import_params(params_set)
        return

    def import_one_file_on_extension(self, import_params: ImportParams, params_set:str=prop.DEFAULT_PARAMS_SET,
                                     input_file="", input_path="", if_circular:bool=None):
        """
        :param import_params: 参数表
        :param if_circular: 判断是否循环读取, 循环读取可用于读取大数据, 但不好画图或进行整体的数据处理
        :return: 针对单一的文件导入, 视情况 if_circular is True, 就返回生成器, 否则直接返回整张表
        """
        # 将修改的参数保存到参数表内
        self.init_import_entrance_params(import_params, params_set, input_file=input_file, input_path=input_path,
                                         if_circular=if_circular)
        
        if self.if_circular is False:
            df = self.import_as_df(import_params, input_file, input_path)
            return df
        else:
            chunk_reader = self.import_as_df_generator(import_params, input_file, input_path)
            return chunk_reader
    
    def generator_combine_multi_file_generators(self, import_params: ImportParams, params_set:str=prop.DEFAULT_PARAMS_SET, input_path="", import_type:str=None):
        """
        根据路径进行批量读取, 对各个数据源生成生成器, 适合各个数据都很大的情况, 返回以以chunksize为间隔的生成器, 以确保数据不会太大导致MemoryError
        :param import_type: 根据特定的数据类型进行读取, 例如'.csv'就是只读取csv文件, 另: ''表示全部读取, 默认值None, 表示直接调用import_params内的参数
        """
        self.init_import_entrance_params(import_params, params_set, input_path=input_path, import_type=import_type)
        path_finder = FindChildPaths(self.input_encoding)
        path_file_pairs = path_finder.gain_child_certain_type_path_file_pairs(self.input_path, self.import_type)
        
        last_df = None
        for path in path_file_pairs.keys():
            for file in path_file_pairs[path]:
                chunk_reader = self.import_as_df_generator(import_params, file, path)
                for chunk in chunk_reader:
                    df = chunk
                    if last_df is not None:
                        df = concat_dfs(last_df, df)
                    pieces = count_exact_sep_num(df, self.chunksize)
                    if pieces >= 1:
                        for nth_chunk in range(math.ceil(pieces)):
                            nth_chunk_df = get_nth_chunk_df(df, nth_chunk, self.chunksize)
                            nth_chunk_df = nth_chunk_df.reset_index(drop=True)
                            if nth_chunk_df.index.size < self.chunksize:
                                last_df = nth_chunk_df
                                break
                            yield nth_chunk_df
                        if last_df is not None and last_df.index.size == self.chunksize:
                            last_df = None
                    else:
                        last_df = df
        if last_df is not None:
            last_df = last_df.reset_index(drop=True)
            yield last_df
    
    def generator_combine_multi_file_dfs(self, import_params: ImportParams, params_set:str=prop.DEFAULT_PARAMS_SET, input_path="", import_type:str=None):
        """
        根据路径进行批量读取, 分别对各个数据源直接全量导入, 适合各个数据都不大的情况, 返回以以chunksize为间隔的生成器, 以确保数据不会太大导致MemoryError
        """
        self.init_import_entrance_params(import_params, params_set, input_path=input_path, import_type=import_type)
        path_finder = FindChildPaths(self.input_encoding)
        path_file_pairs = path_finder.gain_child_certain_type_path_file_pairs(self.input_path, self.import_type)
        
        last_df = None
        for path in path_file_pairs.keys():
            for file in path_file_pairs[path]:
                df = self.import_as_df(import_params, file, path)
                if last_df is not None:
                    # 如果上一个留下来了一部分，就合并
                    df = concat_dfs(last_df, df)
                pieces = count_exact_sep_num(df, self.chunksize)
                # 如果片超过了self.chunksize，就先导入
                if pieces >= 1:
                    for nth_chunk in range(math.ceil(pieces)):
                        nth_chunk_df = get_nth_chunk_df(df, nth_chunk, self.chunksize)
                        nth_chunk_df = nth_chunk_df.reset_index(drop=True)
                        if nth_chunk_df.index.size < self.chunksize:
                            # 取得最后一片
                            last_df = nth_chunk_df
                            break
                        yield nth_chunk_df
                    if last_df is not None and last_df.index.size == self.chunksize:
                        # 如果是刚好结束的情况，则报空
                        last_df = None
                else:
                    # 如果都不能凑成一整片，就放下一个循环
                    last_df = df
        if last_df is not None:
            # 将最后剩下的部分导入
            last_df = last_df.reset_index(drop=True)
            yield last_df
    
    def import_multi_files_as_generator(self, import_params: ImportParams, params_set:str=prop.DEFAULT_PARAMS_SET,
                                        input_path="", import_type:str=None, if_circular:bool=None):
        """
        批量读取文件形成生成器
        :param import_type: "": 全部数据类型的文件, ".csv": 仅读取csv文件; None: 采用import_params_setting.py里的默认值
        :param if_circular: True: 以循环读取的方式读取各个数据源(适用大数据), False: 以整体读取的方式读取各个数据源(适用各个数据源为小数据)
                            None: 采用import_params_setting.py里的默认值
        """
        # 将修改后的参数保存到参数表里
        self.init_import_entrance_params(import_params, params_set, input_path=input_path, import_type=import_type, if_circular=if_circular)
        if self.if_circular is True:
            # 以循环读取的方式读取各个数据源(适用大数据)
            chunk_reader = self.generator_combine_multi_file_generators(import_params, params_set, self.input_path, self.import_type)
        else:
            # 以整体读取的方式读取各个数据源(适用各个数据源为小数据)
            chunk_reader = self.generator_combine_multi_file_dfs(import_params, params_set, self.input_path, self.import_type)
        return chunk_reader
    
    def count_row_num(self, df:pd.DataFrame, import_params: ImportParams, params_set:str=prop.DEFAULT_PARAMS_SET):
        import_params.import_index_size += df.index.size
        import_params.store_import_params(params_set)
    
    def fully_import_data(self, import_params: ImportParams, params_set:str=prop.DEFAULT_PARAMS_SET, input_file="", input_path="",
                             if_batch:bool=None, import_type:str=None, if_circular:bool=None):
        """
        :param import_params:
        :param params_set:
        :param input_file: 如果if_batch为真, 则该变量无意义
        :param if_circular:
        :return: 将批量循环读取和单文件循环读取合并起来, 作为程序的入口函数
        """
        self.init_import_entrance_params(import_params, params_set,input_file=input_file, input_path=input_path, if_batch=if_batch,
                                         import_type=import_type, if_circular=if_circular)
        
        if self.if_batch is True:
            chunk_reader = self.import_multi_files_as_generator(import_params, params_set)
            return chunk_reader
        if self.if_circular is True:
            chunk_reader = self.import_one_file_on_extension(import_params, params_set)
            return chunk_reader
        # 当既非循环读取, 也不是批量读取的时候, 就是单文件的完整读取
        df = self.import_one_file_on_extension(import_params, params_set)
        return df
    
    def fully_import_whole_data_as_df(self, import_params: ImportParams, params_set:str=prop.DEFAULT_PARAMS_SET, input_file="", input_path="",
                             if_batch:bool=None, import_type:str=None, if_circular:bool=None):
        """
        :return: 用来将所有的导入数据合并为一个dataframe, 方便整体数据处理, 例如画图, 一般不适用于格式转换
        """
        self.init_import_entrance_params(import_params, params_set, input_file=input_file, input_path=input_path,
                                         if_batch=if_batch,
                                         import_type=import_type, if_circular=if_circular)
        if self.if_batch is False and self.if_circular is False:
            # 当既非循环读取, 也不是批量读取的时候, 就是单文件的完整读取
            full_df = self.import_one_file_on_extension(import_params, params_set)
            return full_df
        
        # 将所有循环读取的文件合并为一个dataframe, 可能会太大导致MemoryError, 要注意
        chunk_reader = self.fully_import_data(import_params, params_set)
        frames = list()
        for chunk in chunk_reader:
            frames.append(chunk)
        full_df = concat_dfs_list(frames)
        return full_df