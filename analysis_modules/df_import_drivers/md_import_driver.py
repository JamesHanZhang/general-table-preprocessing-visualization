import pandas as pd

from analysis_modules.df_import_drivers.csv_import_driver import CsvImportDriver
from analysis_modules.params_monitor import SysLog, ImportParams

class MdImportDriver(CsvImportDriver):
    def __init__(self, import_params: ImportParams):
        super().__init__(import_params)
        self.quote_as_object = True
        self.quote_none = True

    def init_md_import_params(self, input_file="", input_path="", input_encoding="", quote_as_object=None):
        self.init_basic_import_params(input_file, input_path, input_encoding, quote_as_object)
        return

    @SysLog().calculate_cost_time("<import from markdown(using csv reading method)>")
    def fully_import_md(self, input_file="", input_path = "", input_encoding=""):
        self.init_md_import_params(input_file, input_path, input_encoding)

        df = self.fully_import_csv(self.input_file, self.input_path, input_sep="|", input_encoding=self.input_encoding)
        df = df.dropna(
            axis=1,
            how='all'
        ).iloc[1:]
        df.columns = df.columns.str.strip()
        # strip() 每一列
        df = df.map(lambda element: element.strip() if isinstance(element, str) else element)
        msg = f"[IMPORT MARKDOWN]: data from {self.input_file} is fully imported."
        self.log.show_log(msg)
        return df
    
    @SysLog().calculate_cost_time("<markdown reading generator created (using csv reading method)>")
    def circular_import_md(self, input_file="", input_path = "", input_encoding=""):
        self.init_md_import_params(input_file, input_path, input_encoding)
        
        chunk_reader = self.circular_import_csv(self.input_file, self.input_path, input_sep="|", input_encoding=self.input_encoding)
        chunk_no = 0
        for chunk in chunk_reader:
            # 如果列数据全为空, 则去掉
            chunk = chunk.dropna(
                axis=1,
                how='all'
            )
            if chunk_no == 0:
                # 去掉 | --- | 这行
                chunk = chunk.iloc[1:]
            # 重设列名
            chunk.columns = chunk.columns.str.strip()
            # strip() 每一列
            chunk = chunk.map(lambda element: element.strip() if isinstance(element, str) else element)
            chunk_no += 1
            yield chunk