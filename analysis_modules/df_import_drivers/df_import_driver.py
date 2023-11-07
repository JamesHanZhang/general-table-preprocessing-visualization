import pandas as pd
import chardet

# self-made modules
from analysis_modules.params_monitor import ResourcesOperation, SysLog, ImportParams
from basic_operation import IoMethods
from analysis_modules.df_processing import NullProcessing
class DfImportDriver(object):
    def __init__(self, import_params: ImportParams):
        # 超过15位会使用科学计数法scientific notation导致省略15位以后的数据，需要预先设置
        pd.set_option('display.float_format', '{:.2f}'.format)
        self.log = SysLog()
        self.input_file = import_params.input_file
        self.input_path = import_params.input_path
        self.input_encoding = import_params.input_encoding
        self.chunksize = import_params.chunksize
        self.quote_as_object = import_params.quote_as_object

        self.iom = IoMethods(self.input_encoding)
    
    def init_basic_import_params(self, input_file="", input_path="", input_encoding="", quote_as_object=None):
        if input_file != "":
            self.input_file = input_file
        if input_path != "":
            self.input_path = input_path
        if input_encoding != "":
            self.input_encoding = input_encoding
            self.iom = IoMethods(input_encoding)
        if quote_as_object is not None and type(quote_as_object) is bool:
            self.quote_as_object = quote_as_object
        return

    def drop_empty_lines_from_df(self, df):
        df, empty_lines_count = NullProcessing.drop_empty_lines(df)
        return df
    def get_preserves(self, df) -> dict[str, str]:
        """method for getting dict of dataframe columns and return it with 'object' type as indicator."""
        # read_excel在面对长数字数据时会出现数据丢失的情况，只能通过转换为string来实现完整的读取
        columns = df.columns.tolist()
        objects = ['object'] * len(columns)
        preserves = dict(zip(columns, objects))
        return preserves

    def get_df_dtypes_by_preserves(self, preserves):
        if self.quote_as_object is True:
            msg = "[WARNING]: we turned all datavalues into string type in case losing the precision of data."
            self.log.show_log(msg)
            return preserves
        else:
            return None

    def decide_df_dtypes(self, df) -> dict[str, str]|None:
        preserves = self.get_preserves(df)
        preserves = self.get_df_dtypes_by_preserves(preserves)
        return preserves

    

    @staticmethod
    def detect_charset(file_path, chunk_size=10240):
        detector = chardet.universaldetector.UniversalDetector()
        try:
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    detector.feed(chunk)
                    if detector.done:
                        break
        # 文件不能以text的形式读取
        except (UnicodeDecodeError, IsADirectoryError, PermissionError, FileNotFoundError):
            return

        detector.close()
        result = detector.result
        encoding = result['encoding'].lower()

        # 中文环境下常出现的问题
        if encoding in ['gbk', 'gb2312']:
            encoding = 'gb18030'
        return encoding

    def get_import_encoding(self, file_path, input_encoding):
        if input_encoding != "":
            return input_encoding
        input_encoding = self.detect_charset(file_path)

        # 重新定义应用类实例
        self.iom = IoMethods(input_encoding)

        self.log.show_log(f"[INPUT ENCODING DETECTION] file {file_path} charset detected automatically: {input_encoding}")
        return input_encoding
