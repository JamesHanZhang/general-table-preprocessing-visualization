import pandas as pd
from tqdm import tqdm
# self-made modules
from analysis_modules.df_output_drivers.df_output_driver import DfOutputDriver
from analysis_modules.params_monitor import SysLog, OutputParams
from basic_operation import IoMethods

class CsvOutputDriver(DfOutputDriver):
    def __init__(self, output_params: OutputParams):
        super().__init__(output_params)
        self.output_sep = output_params.csv_output_params.output_sep
        self.repl_to_sub_sep = output_params.csv_output_params.repl_to_sub_sep

    def store_as_csv(self, df, full_output_path, overwrite: bool):
        # 去掉空行
        df = self.drop_empty_lines_from_df(df)
        # 根据overwrite判断是添加到原有文件，还是重写，当overwrite==True，则重写，False则添加到原文件下
        if overwrite is True or self.iom.check_if_file_exists(full_output_path, False) is False:
            header = True
            storage_mode = 'w'
        else:
            header = False
            storage_mode = 'a'
        # 通过调整 lineterminator='\n' ，使得导出的数据为LF格式，即换行符为纯粹的\n的linux模式
        df.to_csv(full_output_path, mode=storage_mode, header=header, sep=self.output_sep, index=False,
                  encoding=self.output_encoding, float_format='%f', lineterminator='\n')
        return

    def init_csv_output_params(self, output_file="", output_path="", output_encoding="", overwrite:bool=None,
                                 if_sep:bool=None, only_one_chunk:bool=None, output_sep="", repl_to_sub_sep:str=None):
        self.init_basic_output_params(output_file=output_file, output_path=output_path, output_encoding=output_encoding,
                                      overwrite=overwrite, if_sep=if_sep, only_one_chunk=only_one_chunk)
        if output_sep != "":
            self.output_sep = output_sep
        if repl_to_sub_sep is not None and type(repl_to_sub_sep) is str:
            self.repl_to_sub_sep = repl_to_sub_sep

        IoMethods.mkdir_if_no_dir(self.output_path)
        return

    @SysLog().calculate_cost_time("<store as csv>")
    def store_df_as_csv(self, df: pd.DataFrame, output_file="", output_path="", output_encoding="", overwrite:bool=None,
                                 if_sep:bool=None, only_one_chunk:bool=None, output_sep="", repl_to_sub_sep:str=None,
                            chunk_no:int=""):
        """
        chunk_no is int and if_sep is False -> 循环添加
        chunk_no is int and if_sep is True -> 循环切片
        chunk_no is "" and if_sep is False -> 整体导入整体导出
        chunk_no is "" and if_sep is True -> 外部调用该函数进行切片, 按照整体导入导出理解
        """
        self.init_csv_output_params(output_file=output_file, output_path=output_path, output_encoding=output_encoding,
                                    overwrite=overwrite, if_sep=if_sep, only_one_chunk=only_one_chunk,
                                    output_sep=output_sep, repl_to_sub_sep=repl_to_sub_sep)
        output_file = self.decide_sep_or_add(self.output_file, self.if_sep, self.only_one_chunk, chunk_no)
        if output_file is None:
            return
            
        # 获得参数
        extends = '.csv'
        output_file = self.set_file_extension(output_file, extends)
        full_output_path = IoMethods.join_path(self.output_path, output_file)
        self.store_as_csv(df, full_output_path, self.overwrite)
        msg = "[CSV OUTPUT]: file created: {a}".format(a=full_output_path)
        self.log.show_log(msg)
        return

    @SysLog().calculate_cost_time("<store as csv in pieces>")
    def sep_df_as_multi_csv(self, df: pd.DataFrame,  output_file="", output_path="", output_encoding="", overwrite:bool=None,
                                 if_sep:bool=None, only_one_chunk:bool=None, output_sep="", repl_to_sub_sep:str=None):
        """
        仅支持非循环的整体切片
        """
        self.init_csv_output_params(output_file=output_file, output_path=output_path, output_encoding=output_encoding,
                                    overwrite=overwrite, if_sep=if_sep, only_one_chunk=only_one_chunk,
                                    output_sep=output_sep, repl_to_sub_sep=repl_to_sub_sep)
        
        
        pieces_count = self.count_sep_num(df)
        # 当切片数量只有1的时候，默认直接转正常存储
        if pieces_count == 1:
            self.store_df_as_csv(df)
            return
        
        # 保证在循环过程中不会被迭代覆盖掉原来的导出名
        output_file = self.output_file
        chunk_no = 0
        for nth_chunk in tqdm(range(pieces_count),position=True,leave=True,desc="creating separation of csv..."):
            nth_chunk_df = self.get_nth_chunk_df(df, nth_chunk)
            self.store_df_as_csv(nth_chunk_df, output_file=output_file, chunk_no=chunk_no)
            chunk_no += 1
        return


