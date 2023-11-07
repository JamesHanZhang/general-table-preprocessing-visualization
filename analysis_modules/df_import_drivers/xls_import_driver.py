import pandas as pd

# self-made modules
from analysis_modules.df_import_drivers.df_import_driver import DfImportDriver
from analysis_modules.params_monitor import SysLog, ImportParams

class XlsImportDriver(DfImportDriver):
    def __init__(self, import_params: ImportParams):
        super().__init__(import_params)
        self.input_sheet = import_params.xls_import_params.input_sheet
        
    
    def init_xls_import_params(self, input_file="", input_path="", input_encoding="", quote_as_object=None,
                               input_sheet=""):
        self.init_basic_import_params(input_file, input_path, input_encoding, quote_as_object)
        if input_sheet != "":
            self.input_sheet = input_sheet

    def init_xls_reader_params(self, input_file="", input_path="", input_sheet=""):
        # 修订参数
        self.init_xls_import_params(input_file=input_file, input_path=input_path, input_sheet=input_sheet)

        full_input_path = self.iom.join_path(self.input_path, self.input_file)
        self.iom.check_if_file_exists(full_input_path)

        df = pd.read_excel(full_input_path, sheet_name=self.input_sheet, skiprows=0, nrows=10)
        # 把所有类型转为object再次进行读取，以保证得到完整数据
        self.preserves = self.decide_df_dtypes(df)
        self.df_columns = df.columns.tolist()
        return full_input_path

    @SysLog().calculate_cost_time("<import from excel>")
    def fully_import_excel(self, input_file="", input_path="",input_sheet=""):
        full_input_path = self.init_xls_reader_params(input_file, input_path, input_sheet)

        df = pd.read_excel(full_input_path, sheet_name=self.input_sheet, names=self.df_columns, dtype=self.preserves)

        msg = "[IMPORT EXCEL]: data from {a} is fully imported via excel reading method.".format(a=full_input_path)
        self.log.show_log(msg)
        return df

    @SysLog().calculate_cost_time("<excel reading generator created>")
    def circular_import_excel(self, input_file="", input_path="",input_sheet=""):
        full_input_path = self.init_xls_reader_params(input_file, input_path, input_sheet)

        msg = f"[IMPORT EXCEL]: data from {full_input_path} is imported as reader generator for " \
              f"circular import in chunk size {str(self.chunksize)}."
        self.log.show_log(msg)

        skiprows = 0
        while True:
            df = pd.read_excel(full_input_path, sheet_name=self.input_sheet, dtype=self.preserves,names=self.df_columns,
                               skiprows=skiprows, nrows=self.chunksize)
            if df.index.size == 0:
                break
            skiprows += self.chunksize
            yield df