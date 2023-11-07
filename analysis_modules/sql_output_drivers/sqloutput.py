
import pandas as pd
import os
import time
# self-made modules
from basic_operation import IoMethods
import analysis_modules.default_properties as prop
from analysis_modules.params_monitor import OutputParams, SysLog
from analysis_modules.sql_output_drivers.oracle_output_driver import OracleOutputDriver
from analysis_modules.sql_output_drivers.mysql_output_driver import MySqlOutputDriver
from analysis_modules.sql_output_drivers.gbase_output_driver import GBaseOutputDriver
from analysis_modules.sql_output_drivers.postgresql_output_driver import PostgreSqlOutputDriver
from analysis_modules.sql_output_drivers.sqlserver_output_driver import SqlServerOutputDriver

class SqlOutput:
    def __init__(self):
        pass
    
    def init_store_output_params(self, output_params: OutputParams, params_set:str=prop.DEFAULT_PARAMS_SET, table_name="",
                                 database="", output_path="", output_encoding="", overwrite: bool = None,
                                 if_sep: bool = None, only_one_chunk: bool = None, table_comment="",
                               column_comments={}, repl_to_sub_comma:str=None):
        if table_name != "":
            output_params.sql_output_params.table_name = table_name
        if table_comment != "":
            output_params.sql_output_params.table_comment = table_comment
        if database in output_params.sql_output_params.database_options:
            output_params.sql_output_params.database = database
        if os.path.isabs(output_path):
            output_params.output_path = output_path
        if output_encoding != "":
            output_params.output_encoding = output_params.check_if_encoding(output_encoding, output_params.output_encoding)
        if overwrite is not None and type(overwrite) is bool:
            output_params.overwrite = overwrite
        if if_sep is not None and type(if_sep) is bool:
            output_params.if_sep = if_sep
        if only_one_chunk is not None and type(only_one_chunk) is bool:
            output_params.only_one_chunk = only_one_chunk
        if column_comments != {}:
            output_params.sql_output_params.column_comments = column_comments
        if repl_to_sub_comma is not None and type(repl_to_sub_comma) is str:
            output_params.sql_output_params.repl_to_sub_comma = repl_to_sub_comma
        
        self.table_name = output_params.sql_output_params.table_name
        self.table_comment = output_params.sql_output_params.table_comment
        self.database = output_params.sql_output_params.database
        self.output_encoding = output_params.output_encoding
        self.overwrite = output_params.overwrite
        self.if_sep = output_params.if_sep
        self.only_one_chunk = output_params.only_one_chunk
        self.column_comments = output_params.sql_output_params.column_comments
        self.repl_to_sub_comma = output_params.sql_output_params.repl_to_sub_comma
        
        # 如果切分, 需要建立子目录, 不能存储, 否则下次调用会反复添加子目录
        self.output_path = self.decide_output_path(self.if_sep, self.table_name, output_params.output_path)
        
        if self.database == "Oracle":
            self.sql_out_driver = OracleOutputDriver(output_params, params_set)
        elif self.database == "MySql":
            self.sql_out_driver = MySqlOutputDriver(output_params, params_set)
        elif self.database == "GBase":
            self.sql_out_driver = GBaseOutputDriver(output_params, params_set)
        elif self.database == "PostgreSql":
            self.sql_out_driver = PostgreSqlOutputDriver(output_params, params_set)
        elif self.database == "SqlServer":
            self.sql_out_driver = SqlServerOutputDriver(output_params, params_set)
        else:
            raise TypeError("[TypeError] the database you choose didn't follow the rule in the list of database choices.")
        output_params.store_output_params(params_set)
    
    @staticmethod
    def decide_output_path(if_sep, output_file, output_path):
        if if_sep is True:
            folder = IoMethods.get_main_file_name(output_file)
            output_path = IoMethods.join_path(output_path, folder)
        IoMethods.mkdir_if_no_dir(output_path)
        return output_path
    
    def count_row_num(self, df:pd.DataFrame, output_params: OutputParams, params_set:str=prop.DEFAULT_PARAMS_SET):
        output_params.sql_output_params.output_index_size += df.index.size
        output_params.store_output_params(params_set)
    
    def output_sql(self, df: pd.DataFrame, output_params: OutputParams, params_set=prop.DEFAULT_PARAMS_SET, table_name="",
                                 database="", output_path="", output_encoding="", overwrite: bool = None,
                                 if_sep: bool = None, only_one_chunk: bool = None, table_comment="",
                               column_comments={}, repl_to_sub_comma:str=None, chunk_no:int=""):
        # 将修改的参数保存
        self.init_store_output_params(output_params, params_set, table_name=table_name, database=database,
                                      output_path=output_path, output_encoding=output_encoding, overwrite=overwrite,
                                      if_sep=if_sep, only_one_chunk=only_one_chunk, table_comment=table_comment,
                                      column_comments=column_comments, repl_to_sub_comma=repl_to_sub_comma)
        # 记录条数
        self.count_row_num(df, output_params, params_set)
        
        if self.if_sep is True and type(chunk_no) is str and chunk_no=="":
            # 整体拆分
            self.sql_out_driver.sep_df_as_multi_sql(df, output_path=self.output_path)
        else:
            # 可能是循环拆分, 循环添加, 或者整体添加
            self.sql_out_driver.store_df_as_sql(df, output_path=self.output_path, if_sep=self.if_sep, chunk_no=chunk_no)
        return
    
    @staticmethod
    def get_output_file(output_params, output_file):
        if output_file != "":
            return output_file
        return output_params.output_file
    
    def output_sql_on_extension(self, df: pd.DataFrame, output_params: OutputParams, params_set=prop.DEFAULT_PARAMS_SET,
                                output_file="", database="", output_path="", output_encoding="", overwrite: bool = None,
                                 if_sep: bool = None, only_one_chunk: bool = None, table_comment="",
                               column_comments={}, repl_to_sub_comma:str=None, chunk_no:int=""):
        """
        :param output_file: 如果文件的拓展名为.sql，则自动将文件名主体作为导出的表名
        :param table_name: 自动被文件主体名覆盖
        """
        output_file = self.get_output_file(output_params, output_file)
        if IoMethods.get_file_extension(output_file) != ".sql":
            msg = f"[NameError] for sql output, file name {output_file} must contains extension '.sql' as required."
            SysLog.show_log(msg)
            return
        table_name = IoMethods.get_main_file_name(output_file)
        
        # 执行导出
        self.output_sql(df, output_params, params_set, table_name=table_name, database=database, output_path=output_path,
                        output_encoding=output_encoding, overwrite=overwrite, if_sep=if_sep, only_one_chunk=only_one_chunk,
                        table_comment=table_comment, column_comments=column_comments, repl_to_sub_comma=repl_to_sub_comma,
                        chunk_no=chunk_no)
        return
    
    def output_sql_on_activation(self, df: pd.DataFrame, output_params: OutputParams, params_set=prop.DEFAULT_PARAMS_SET, table_name="",
                                 database="", output_path="", output_encoding="", overwrite: bool = None,
                                 if_sep: bool = None, only_one_chunk: bool = None, table_comment="",
                               column_comments={}, repl_to_sub_comma:str=None, chunk_no:int=""):
        if output_params.sql_output_params.activation is True:
            # 执行导出
            self.output_sql(df, output_params, params_set, table_name=table_name, database=database,
                            output_path=output_path,
                            output_encoding=output_encoding, overwrite=overwrite, if_sep=if_sep,
                            only_one_chunk=only_one_chunk,
                            table_comment=table_comment, column_comments=column_comments,
                            repl_to_sub_comma=repl_to_sub_comma,
                            chunk_no=chunk_no)
        else:
            SysLog.show_log("[NOT ACTIVATED OUTPUT TYPE] output sql is not activated!")
        return
        
        