
import pandas as pd
import numpy as np

# self-made modules
from analysis_modules.params_monitor import SysLog
from analysis_modules import default_properties as prop


class NullProcessing:
    def __init__(self):
        self.log = SysLog()
        self.null_list = prop.NULL_LIST
        self.replaceNaN = prop.REPLACE_NAN

    def replace_null_value(self, element):
        element = str(element).strip(' ')
        if element in self.null_list or pd.isna(element):
            return "NULL"
        return element
    
    def check_if_empty_line(self, df, pos, df_columns):
        df_line = df.iloc[pos]
        count_null = 0
        for column in df_columns:
            if self.replace_null_value(df_line[column]) == "NULL":
                count_null += 1
        if count_null == len(df_columns):
            return True
        return False

    @classmethod
    def drop_empty_lines(cls, df):
        nulp = cls()
        df = df.reset_index(drop=True)
        columns = df.columns.tolist()
        row_num = df.index.size
        empty_lines_count = 0
        empty_rows = list()
        for row in range(row_num):
            if_empty_line = nulp.check_if_empty_line(df, row, columns)
            if if_empty_line is True:
                empty_lines_count +=1
                empty_rows.append(row)
        df = df.drop(empty_rows)
        if empty_lines_count > 0:
            msg = "[EMPTY ROWS COUNT]: while processing, the program found {a} empty rows in dataframe.\n" \
                  "And those emtpy rows are deleted automatically.".format(a=empty_lines_count)
            SysLog.show_log(msg)
        return df, empty_lines_count

    @classmethod
    def replace_null_with_emtpy_str(cls, df):
        nulp = cls()
        df = df.reset_index(drop=True)
        columns = df.columns.tolist()
        row_num = df.index.size
        for row in range(row_num):
            for column in columns:
                if nulp.replace_null_value(df[column][row]) == "NULL":
                    df[column][row] = ""
        return df

    @classmethod
    def check_if_null_in_series(cls, series):
        series = series.reset_index(drop=True)
        null_series = series.isnull()
        if True in list(null_series):
            return True
        return False

    @classmethod
    def turn_back_null(cls, df):
        nulp = cls()
        # 将空值改回np.nan
        columns = df.columns.tolist()
        row_num = df.index.size

        # 当调用chunk时，index不变会导致位置往后推移，无法选择相对位置的数值，所以要重设index
        df = df.reset_index(drop=True)

        for each_row in range(row_num):
            for each_col in columns:
                if df[each_col][each_row] == nulp.replaceNaN:
                    df[each_col][each_row] = np.nan
        msg = f'[NULL VALUES REPLACEMENT]: previously due to the convience for column type change,\n ' \
              f'the np.nan in dataframe were replace as replaceNaN {str(nulp.replaceNaN)}. \n' \
              f'Now before the storage, it was now converted back.'
        nulp.log.show_log(msg)
        return df

    @staticmethod
    def replace_null(df):
        df = df.fillna(prop.REPLACE_NAN)
        return df