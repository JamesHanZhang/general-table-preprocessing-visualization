import pandas as pd
from tqdm import tqdm
# self-made modules
from analysis_modules.df_output_drivers.df_output_driver import DfOutputDriver
from analysis_modules.params_monitor import SysLog, OutputParams
from basic_operation import IoMethods

class XlsOutputDriver(DfOutputDriver):
    def __init__(self, output_params: OutputParams):
        super().__init__(output_params)
        self.output_sheet = output_params.xls_output_params.output_sheet
        
    def init_xls_output_params(self, output_file="", output_path="", output_encoding="", overwrite:bool=None,
                                 if_sep:bool=None, only_one_chunk:bool=None, output_sheet=""):
        self.init_basic_output_params(output_file=output_file, output_path=output_path, output_encoding=output_encoding,
                                      overwrite=overwrite, if_sep=if_sep, only_one_chunk=only_one_chunk)
        if output_sheet != "":
            self.output_sheet = output_sheet

        IoMethods.mkdir_if_no_dir(self.output_path)
        return

    def store_as_excel(self, df, full_output_path, overwrite: bool):
        # 去掉空行
        df = self.drop_empty_lines_from_df(df)
        # 根据overwrite判断是添加到原有文件，还是重写，当overwrite==True，则重写，False则添加到原文件下
        if overwrite is True or self.iom.check_if_file_exists(full_output_path, False) is False:
            df.to_excel(full_output_path, sheet_name=self.output_sheet, index=False, engine='openpyxl', float_format='%f')
        elif overwrite is False:
            # 使用ExcelWriter目前尚且不稳定，容易出现数据遗失的问题，故暂时搁置，等待未来稳定后再采用该方法
            writer = pd.ExcelWriter(full_output_path, engine='openpyxl', mode='a', if_sheet_exists="overlay")
            df.to_excel(writer, sheet_name=self.output_sheet, startrow=writer.sheets[self.output_sheet].max_row,
                        index=False, header=False, float_format='%f')
            # writer.save()
            writer.close()
        return


    @SysLog().calculate_cost_time("<store as excel>")
    def store_df_as_excel(self, df, output_file="", output_path="", output_encoding="", overwrite:bool=None,
                                 if_sep:bool=None, only_one_chunk:bool=None, output_sheet="", chunk_no:int=""):
        """
        chunk_no is int and if_sep is False -> 循环添加
        chunk_no is int and if_sep is True -> 循环切片
        chunk_no is "" and if_sep is False -> 整体导入整体导出
        chunk_no is "" and if_sep is True -> 外部调用该函数进行切片, 按照整体导入导出理解
        """
        self.init_xls_output_params(output_file=output_file, output_path=output_path, output_encoding=output_encoding,
                                   overwrite=overwrite, if_sep=if_sep, only_one_chunk=only_one_chunk, output_sheet=output_sheet)
        
        output_file = self.decide_sep_or_add(self.output_file, self.if_sep, self.only_one_chunk, chunk_no)
        if output_file is None:
            return
        
        extends = '.xlsx'
        output_file = self.set_file_extension(output_file, extends)
        full_output_path = self.iom.join_path(self.output_path, output_file)

        self.store_as_excel(df, full_output_path, self.overwrite)
        msg = "[EXCEL OUTPUT]: file created: {a}".format(a=full_output_path)
        self.log.show_log(msg)
        return

    @SysLog().calculate_cost_time("<store as excel in pieces>")
    def sep_df_as_multi_excel(self, df: pd.DataFrame, output_file="", output_path="", output_encoding="", overwrite:bool=None,
                                 if_sep:bool=None, only_one_chunk:bool=None, output_sheet=""):
        """
        仅支持非循环的整体切片
        """
        self.init_xls_output_params(output_file=output_file, output_path=output_path, output_encoding=output_encoding,
                                    overwrite=overwrite, if_sep=if_sep, only_one_chunk=only_one_chunk,
                                    output_sheet=output_sheet)

        pieces_count = self.count_sep_num(df)
        # 当切片数量只有1的时候，默认直接转正常存储
        if pieces_count == 1:
            self.store_df_as_excel(df)
            return
        
        # 保证在循环过程中不会被迭代覆盖掉原来的导出名
        output_file = self.output_file
        chunk_no = 0
        for nth_chunk in tqdm(range(pieces_count), position=True, leave=True,
                              desc="creating separation of excel..."):
            nth_chunk_df = self.get_nth_chunk_df(df, nth_chunk)
            self.store_df_as_excel(nth_chunk_df, output_file=output_file, chunk_no=chunk_no)
            chunk_no += 1
        return