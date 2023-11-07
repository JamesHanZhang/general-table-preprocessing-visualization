import pandas as pd
import time
import os
# self-made modules
from analysis_modules import default_properties as prop
from analysis_modules.df_output_drivers.csv_output_driver import CsvOutputDriver
from analysis_modules.df_output_drivers.md_output_driver import MdOutputDriver
from analysis_modules.df_output_drivers.xls_output_driver import XlsOutputDriver
from analysis_modules.params_monitor import OutputParams, SysLog
from basic_operation import IoMethods


class DfOutput(object):
    def __init__(self):
        self.csv_extensions = ['.csv']
        self.md_extensions = ['.md']
        self.xls_extensions = ['.xls', '.xlsx', '.xltx', '.xlsm', '.xlt', '.xltm', '.xlam', '.xla']
        self.supported_extensions = self.csv_extensions + self.md_extensions + self.xls_extensions
        
    def init_store_output_params(self, output_params: OutputParams, params_set:str=prop.DEFAULT_PARAMS_SET,
                                 output_file="",output_path="", output_encoding="",overwrite:bool=None,
                                 if_sep:bool=None, only_one_chunk:bool=None):
        if output_file != "":
            output_params.output_file = output_file
        if os.path.isabs(output_path):
            output_params.output_path = output_path
        if overwrite is not None and type(overwrite) is bool:
            output_params.overwrite = overwrite
        if if_sep is not None and type(if_sep) is bool:
            output_params.if_sep = if_sep
        if only_one_chunk is not None and type(only_one_chunk) is bool:
            output_params.only_one_chunk = only_one_chunk
        if output_encoding != "":
            output_params.output_encoding = output_params.check_if_encoding(output_encoding, output_params.output_encoding)
        
        self.output_file = output_params.output_file
        self.if_sep = output_params.if_sep
        self.only_one_chunk = output_params.only_one_chunk
        self.overwrite = output_params.overwrite
        self.output_encoding = output_params.output_encoding
        
        # 如果切分, 需要建立子目录, 不能存储, 否则下次调用会反复添加子目录
        self.output_path = self.decide_output_path(self.if_sep, self.output_file, output_params.output_path)
        
        self.output_params = output_params
        self.params_set = params_set
        self.output_params.store_output_params(self.params_set)
    
    @staticmethod
    def decide_output_path(if_sep, output_file, output_path):
        if if_sep is True:
            folder = IoMethods.get_main_file_name(output_file)
            output_path = IoMethods.join_path(output_path, folder)
        IoMethods.mkdir_if_no_dir(output_path)
        return output_path
    
    def count_row_num(self, df: pd.DataFrame, output_params: OutputParams, params_set, output_file):
        extension = IoMethods.get_file_extension(output_file)
        if extension in self.xls_extensions:
            output_params.xls_output_params.output_index_size += df.index.size
        elif extension in self.csv_extensions:
            output_params.csv_output_params.output_index_size += df.index.size
        elif extension in self.md_extensions:
            output_params.md_output_params.output_index_size += df.index.size
        output_params.store_output_params(params_set)
    
    @staticmethod
    def get_output_file(output_params, output_file):
        if output_file != "":
            return output_file
        return output_params.output_file
        
    def output_df_on_extension(self, df: pd.DataFrame, output_params: OutputParams, params_set=prop.DEFAULT_PARAMS_SET,
                               output_file="", output_path="", output_encoding="",overwrite:bool=None, if_sep:bool=None,
                               only_one_chunk:bool=None, chunk_no:int=""):
        """
        :param df: dataframe
        :param output_params: 参数表
        :param params_set: 参数表的名称
        :param chunk_no: "" 整存整取, int：分片循环存入
        :return:
        chunk_no is int and if_sep is False -> 切片导入，合并导出
        chunk_no is int and if_sep is True -> 切片导入，切片导出
        chunk_no is "" and if_sep is False -> 整体导入整体导出
        chunk_no is "" and if_sep is True ->  整体导入, 切片导出
        """
        output_file = self.get_output_file(output_params, output_file)
        if IoMethods.get_file_extension(output_file) not in self.supported_extensions:
            msg = f"[NameError] for xls/md/csv output, file name {output_file} must contains extension {str(self.supported_extensions)} as required."
            SysLog.show_log(msg)
            return
        
        self.init_store_output_params(output_params, params_set, output_file=output_file, output_path=output_path,
                                      output_encoding=output_encoding, overwrite=overwrite, if_sep=if_sep,
                                      only_one_chunk=only_one_chunk)
        self.count_row_num(df, self.output_params,self.params_set, output_file)
        
        extension = IoMethods.get_file_extension(self.output_file)
        if extension in self.xls_extensions:
            output_driver = XlsOutputDriver(self.output_params)
            if self.if_sep is True and type(chunk_no) is str and chunk_no=="":
                output_driver.sep_df_as_multi_excel(df, output_path=self.output_path)
            else:
                output_driver.store_df_as_excel(df, output_path=self.output_path, if_sep=self.if_sep, chunk_no=chunk_no)
        elif extension in self.csv_extensions:
            output_driver = CsvOutputDriver(self.output_params)
            if self.if_sep is True and type(chunk_no) is str and chunk_no == "":
                output_driver.sep_df_as_multi_csv(df, output_path=self.output_path)
            else:
                output_driver.store_df_as_csv(df, output_path=self.output_path, if_sep=self.if_sep, chunk_no=chunk_no)
        elif extension in self.md_extensions:
            output_driver = MdOutputDriver(self.output_params)
            if self.if_sep is True and type(chunk_no) is str and chunk_no == "":
                output_driver.sep_df_as_multi_md(df, output_path=self.output_path)
            else:
                output_driver.store_df_as_md(df, output_path=self.output_path, if_sep=self.if_sep, chunk_no=chunk_no)
        else:
            msg = f"file name must contains extension {str(self.supported_extensions)} as required."
            raise NameError(msg)
        return
    
    def check_activations(self, output_params: OutputParams):
        not_act_count = 3
        if output_params.md_output_params.activation is False:
            SysLog.show_log("[NOT ACTIVATED OUTPUT TYPE] output markdown is not activated!")
            not_act_count -= 1
        if output_params.xls_output_params.activation is False:
            SysLog.show_log("[NOT ACTIVATED OUTPUT TYPE] output excel is not activated!")
            not_act_count -= 1
        if output_params.csv_output_params.activation is False:
            SysLog.show_log("[NOT ACTIVATED OUTPUT TYPE] output csv is not activated!")
            not_act_count -= 1
        return not_act_count
    
    def output_df_on_activation(self, df: pd.DataFrame, output_params: OutputParams, params_set=prop.DEFAULT_PARAMS_SET,
                               output_file="", output_path="", output_encoding="",overwrite:bool=None, if_sep:bool=None,
                               only_one_chunk:bool=None, chunk_no:int=""):
        if self.check_activations(output_params) == 0:
            return
        # 执行程序
        output_file = self.get_output_file(output_params, output_file)
            
        output_file = IoMethods.get_main_file_name(output_file)
        output_files = list()
        if output_params.csv_output_params.activation is True:
            output_files.append(output_file+'.csv')
        if output_params.xls_output_params.activation is True:
            output_files.append(output_file + '.xlsx')
        if output_params.md_output_params.activation is True:
            output_files.append(output_file + '.md')
        for file in output_files:
            self.output_df_on_extension(df, output_params, params_set, output_file=file, output_path=output_path,
                                        output_encoding=output_encoding, overwrite=overwrite, if_sep=if_sep,
                                        only_one_chunk=only_one_chunk, chunk_no=chunk_no)