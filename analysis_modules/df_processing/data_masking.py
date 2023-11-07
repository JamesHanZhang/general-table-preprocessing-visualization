
from tqdm import tqdm
import pandas as pd
import math
# self-made modules
from analysis_modules.params_monitor import SysLog
from analysis_modules import default_properties as prop


class DataMasking:
    def __init__(self):
        self.null_list = prop.NULL_LIST
        self.masking_type_choices = ['simple']

    def sub_asterisk(self, df, col):
        row_num = df.index.size
        # 当调用chunk时，index不变会导致位置往后推移，无法选择相对位置的数值，所以要重设index
        df = df.reset_index(drop=True)
        replacement = "*"
        for row in range(row_num):
            element = df[col][row]
            if element in self.null_list or pd.isna(element):
                continue
            if len(element) == 1:
                df[col][row] = replacement
                continue
            pos = math.ceil(len(element) / 3)
            new_element = element[:pos] + replacement * len(element[pos:])
            df[col][row] = new_element
        return df
    
    def check_if_func_contains(self, masking_type):
        if masking_type not in self.masking_type_choices:
            raise TypeError(f"[TypeError] data masking type not in the masking type choices provided: {str(self.masking_type_choices)}")

    @classmethod
    @SysLog().calculate_cost_time("<data masking>")
    def data_masking(cls, df, masking_columns, masking_type="simple"):
        dma = cls()
        """
        :param df: dataframe
        :param simple_repl_cols: list type, columns need data masking
        :return: dataframe
        """
        dma.check_if_func_contains(masking_type)
        # 简单替换脱敏
        for col in tqdm(masking_columns, desc="data masking for each column..."):
            if masking_type == "simple":
                df = dma.sub_asterisk(df, col)
        SysLog.show_log(
            "[DATA MASKING]: data masking for certain columns {0} is finished.".format(str(masking_columns)))
        return df
