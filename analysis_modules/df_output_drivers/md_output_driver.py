import pandas as pd
from tqdm import tqdm
# self-made modules
from analysis_modules.df_output_drivers.df_output_driver import DfOutputDriver
from analysis_modules.params_monitor import SysLog, OutputParams
from analysis_modules.df_processing import NullProcessing
from basic_operation import IoMethods

class MdOutputDriver(DfOutputDriver):
    def __init__(self, output_params: OutputParams):
        super().__init__(output_params)
    
    
    def init_md_output_params(self, output_file="", output_path="", output_encoding="", overwrite: bool = None,
                              if_sep: bool = None, only_one_chunk: bool = None):
        self.init_basic_output_params(output_file=output_file, output_path=output_path, output_encoding=output_encoding,
                                      overwrite=overwrite, if_sep=if_sep, only_one_chunk=only_one_chunk)
        
        IoMethods.mkdir_if_no_dir(self.output_path)
        return

    def store_as_md(self, df, full_output_path, overwrite):
        # 去掉空行
        df = self.drop_empty_lines_from_df(df)

        # 将空值替换为空字符串
        df = NullProcessing.replace_null_with_emtpy_str(df)
        # 根据overwrite判断是添加到原有文件，还是重写，当overwrite==True，则重写，False则添加到原文件下
        if overwrite is True or self.iom.check_if_file_exists(full_output_path, False) is False:
            storage_mode = 'wt'
            df.to_markdown(buf=full_output_path, mode=storage_mode, index=False)
            return
        # 如果使用storage_mode = 'a' ，是自动把全部添加到最后，不仅没有换行，而且表头还在
        # 这里写添加的部分
        str_content = df.to_markdown(buf=None, index=False)
        list_content = str_content.split("\n")
        list_content = list_content[2:]
        str_content = '\n' + '\n'.join(list_content)
        self.iom.store_file(full_output_path, str_content, overwrite=overwrite)
        return

    @SysLog().calculate_cost_time("<store as markdown>")
    def store_df_as_md(self, df, output_file="", output_path="", output_encoding="", overwrite: bool = None,
                              if_sep: bool = None, only_one_chunk: bool = None, chunk_no:int=""):
        """
        chunk_no is int and if_sep is False -> 循环添加
        chunk_no is int and if_sep is True -> 循环切片
        chunk_no is "" and if_sep is False -> 整体导入整体导出
        chunk_no is "" and if_sep is True -> 外部调用该函数进行切片, 按照整体导入导出理解
        """
        self.init_md_output_params(output_file=output_file, output_path=output_path, output_encoding=output_encoding,
                                      overwrite=overwrite, if_sep=if_sep, only_one_chunk=only_one_chunk)
        
        output_file = self.decide_sep_or_add(self.output_file, self.if_sep, self.only_one_chunk, chunk_no)
        if output_file is None:
            return
        
        # 获得参数
        extends = '.md'
        output_file = self.set_file_extension(output_file, extends)
        full_output_path = self.iom.join_path(self.output_path, output_file)
        self.store_as_md(df, full_output_path, self.overwrite)
        msg = "[MARKDOWN OUTPUT]: file created: {a}".format(a=full_output_path)
        self.log.show_log(msg)
        return

    @SysLog().calculate_cost_time("<store as markdown in pieces>")
    def sep_df_as_multi_md(self, df: pd.DataFrame, output_file="", output_path="", output_encoding="", overwrite: bool = None,
                              if_sep: bool = None, only_one_chunk: bool = None):
        """
        仅支持非循环的整体切片
        """
        self.init_md_output_params(output_file=output_file, output_path=output_path, output_encoding=output_encoding,
                                   overwrite=overwrite, if_sep=if_sep, only_one_chunk=only_one_chunk)

        pieces_count = self.count_sep_num(df)
        # 当只需要一个切片，或者切片数量只有1的时候，默认直接转正常存储
        if pieces_count == 1:
            self.store_df_as_md(df)
            return
            
        # 保证在循环过程中不会被迭代覆盖掉原来的导出名
        output_file = self.output_file
        chunk_no = 0
        for nth_chunk in tqdm(range(pieces_count), position=True, leave=True, desc="creating separation of markdown..."):
            nth_chunk_df = self.get_nth_chunk_df(df, nth_chunk)
            self.store_df_as_md(nth_chunk_df, output_file=output_file, chunk_no=chunk_no)
            chunk_no += 1
        return