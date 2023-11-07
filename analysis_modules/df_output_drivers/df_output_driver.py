import pandas as pd
import math
import os
# self-made modules
from analysis_modules.params_monitor import ResourcesOperation, SysLog, OutputParams
from basic_operation import IoMethods, count_sep_num, get_nth_chunk_df
from analysis_modules.df_processing import NullProcessing


class DfOutputDriver(object):
    def __init__(self, output_params: OutputParams):
        self.log = SysLog()
        self.output_file = output_params.output_file
        self.output_path = output_params.output_path
        self.output_encoding = output_params.output_encoding
        self.overwrite = output_params.overwrite
        self.if_sep = output_params.if_sep
        self.chunksize = output_params.chunksize
        self.only_one_chunk = output_params.only_one_chunk

        self.iom = IoMethods(self.output_encoding)
        
    def init_basic_output_params(self, output_file="", output_path="", output_encoding="", overwrite:bool=None,
                                 if_sep:bool=None, only_one_chunk:bool=None):
        if output_file != "":
            self.output_file = output_file
        if os.path.isabs(output_path):
            self.output_path = output_path
        if output_encoding != "":
            self.output_encoding = output_encoding
        if overwrite is not None and type(overwrite) is bool:
            self.overwrite = overwrite
        if if_sep is not None and type(if_sep) is bool:
            self.if_sep = if_sep
        if only_one_chunk is not None and type(only_one_chunk) is bool:
            self.only_one_chunk = only_one_chunk
        IoMethods.mkdir_if_no_dir(self.output_path)
        return

    def drop_empty_lines_from_df(self, df):
        df, empty_lines_count = NullProcessing.drop_empty_lines(df)
        return df

    def set_file_extension(self, file_name, extends: str=".csv") -> str:
        # 规定文件拓展名
        extension = self.iom.get_file_extension(file_name)
        file_name = self.iom.get_main_file_name(file_name)
        # 只有excel目前有多种导出拓展名
        if extends == '.xlsx':
            if extension in ['.xls', '.xlsx', '.xltx', '.xlsm', '.xlt', '.xltm', '.xlam', '.xla']:
                file_name = file_name + extension
                return file_name

        file_name = file_name + extends
        
        return file_name

    def count_sep_num(self, df:pd.DataFrame) -> int:
        # 将DF拆分成多个小excel或者csv
        pieces_count = count_sep_num(df, self.chunksize)
        return pieces_count
    
    def decide_sep_or_add(self, output_file:str, if_sep:bool=None, only_one_chunk:bool=None, chunk_no:int=""):
        """
        chunk_no is int and if_sep is False -> 循环添加
        chunk_no is int and if_sep is True -> 循环切片
        chunk_no is "" and if_sep is False -> 整体导入整体导出
        chunk_no is "" and if_sep is True -> 外部调用该函数进行切片, 按照整体导入导出理解
        """
        if if_sep is True and type(chunk_no) is int:
            # chunk_no is int and if_sep is True -> 循环切片
            if only_one_chunk is True and chunk_no > 0:
                # 只取第一个
                self.log.show_log(f"[ONLY ONE SEPARATION AS EXAMPLE] one example output under the path: {self.output_path}")
                return None
            output_file = IoMethods.get_main_file_name(output_file)
            new_file = output_file + f"_{str(chunk_no)}_slice"
            return new_file
        elif if_sep is False and type(chunk_no) is int:
            # chunk_no is int and if_sep is False -> 循环添加
            if chunk_no > 0:
                self.overwrite = False
        # chunk_no is "" and if_sep is True -> 外部调用该函数进行切片, 按照整体导入导出理解
        # chunk_no is "" and if_sep is False -> 整体导入整体导出
        return output_file
    
    def get_nth_chunk_df(self, df: pd.DataFrame, nth_chunk: int) -> pd.DataFrame:
        nth_chunk_df = get_nth_chunk_df(df, nth_chunk, self.chunksize)
        return nth_chunk_df
    
    def mkdir_sep_path(self, output_params: OutputParams, output_file, output_path=""):
        if output_path == "":
            output_path = output_params.output_path
        folder = IoMethods.get_main_file_name(output_file)
        output_path = IoMethods.join_path(output_path, folder)
        return output_path
    
    