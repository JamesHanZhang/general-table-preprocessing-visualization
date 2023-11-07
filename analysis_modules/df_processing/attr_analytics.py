import pandas as pd
import numpy as np
from tqdm import tqdm
from analysis_modules.params_monitor import SysLog

class AttrAnalytics:
    def __init__(self):
        pass

    @staticmethod
    @SysLog().calculate_cost_time("<concat dataframes>")
    def concat_dfs(*dfs: pd.DataFrame) -> pd.DataFrame:
        """
        concat multi df together in order of the input df order.
        """
        frames = list(dfs)
        df = pd.concat(frames)
        df = df.reset_index(drop=True)
        return df

    @classmethod
    @SysLog().calculate_cost_time("<attribute creation via df and index>")
    def create_attr_by_df_pos_arg(cls, func, df: pd.DataFrame, *args, **kwargs) -> list:
        """
        :param func: function must contain at least 2 arguments in order: DataFrame, position of index
        usage: this func can also be applied to work on calculation based on both different rows and columns simultaneously
        """
        df = df.reset_index(drop=True)
        row_num = df.index.size
        new_col = list()
        for pos in tqdm(range(row_num),desc="[ATTR CREATION] new attribute is being created..."):
            new_col.append(func(df, pos, *args, **kwargs))
        return new_col

    @classmethod
    @SysLog().calculate_cost_time("<attribute creation via series processing>")
    def create_attr_by_series_arg(cls, func, df: pd.DataFrame) -> pd.Series:
        """
        :param func: function must and only contain one argument: series in pd.Series type and return one element in series
        """
        new_series = df.apply(func, axis=1)
        return new_series

    @classmethod
    @SysLog().calculate_cost_time("<attribute creation via element processing>")
    def create_attr_by_element_arg(cls, func, series: pd.Series) -> pd.Series:
        """
        to only use 1 series of dataframe to create a new attribute
        :param func: function must and only contain one argument: element in chosen series
        """
        new_series = series.apply(func)
        return new_series

    @classmethod
    @SysLog().calculate_cost_time("<row creation via same func without args>")
    def same_func_create_row(cls, func, df: pd.DataFrame) -> pd.DataFrame:
        """
        :param func: function must and only contain one argument: series in pd.Series type and return one element in series
        the series as arg in func is the series of each column of df
        therefore, in order to calculate the certain columns, you must pick the right columns to be processed.
        :return: a new row in df format waiting for concat
        """
        new_row = list(df.apply(func, axis=0))
        cols = df.columns.tolist()
        new_row_df = pd.DataFrame(columns=cols,index=[0],data=[new_row])
        return new_row_df

    @classmethod
    @SysLog().calculate_cost_time("<row creation via same func with args>")
    def same_args_func_create_row(cls, func, df: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        """
        :param func: first arg in func must be pd.Series
        :return: a new row in df format waiting for concat
        """
        df = df.reset_index(drop=True)
        cols = df.columns.tolist()
        new_row = list()
        for col in tqdm(cols,desc="[ROW CREATION] new row is being created based on columns step by step..."):
            new_row.append(func(df[col], *args, **kwargs))
        new_row_df = pd.DataFrame(columns=cols,index=[0],data=[new_row])
        return new_row_df

    @classmethod
    @SysLog().calculate_cost_time("<row creation via multi-funcs with same amount of args>")
    def multi_funcs_create_row(cls, attr_func_pairs: dict, df: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        """
        :param attr_func_pairs: dict[str,list[func, dict]], 1st arg in func must be pd.Series
        num of each func arguments must be the same.
        :return: a new row in df format waiting for concat
        """
        df = df.reset_index(drop=True)
        cols = df.columns.tolist()

        # 校验参数
        input_cols = attr_func_pairs.keys()
        not_in_cols = list(set(input_cols).difference(set(cols)))
        if len(not_in_cols) != 0:
            raise KeyError(f"the wrong attributes declared in attr_func_pairs are {str(not_in_cols)}, "
                           f"which are not in the dataframe columns.")

        # 返回的row的计算
        new_row = list()
        for col in tqdm(cols,desc="[ROW CREATION] new row is being created based on columns step by step..."):
            try:
                func = attr_func_pairs[col]
                # 如果输入的参数数量不等于某个函数所需的参数数量，则会报错，所以各个函数参数数量要保持一致
                this_col_result = func(df[col], *args, **kwargs)
            except (KeyError) as reason:
                # null value in pandas is denoted as NaN, which from numpy is np.nan
                this_col_result = np.nan
            new_row.append(this_col_result)
        new_row_df = pd.DataFrame(columns=cols,index=[0],data=[new_row])
        return new_row_df




if __name__ == "__main__":
    df = pd.DataFrame({'A': [1, 2], 'B': [10, 20]})
    print("original dataframe")
    print(df)

    #########################
    print("try AttrAnalytics.create_attr_by_df_pos_arg")
    def new_col(df, pos, num):
        res = df['A'][pos]+df['B'][pos]+num
        return res

    df['C'] = AttrAnalytics.create_attr_by_df_pos_arg(new_col, df, 100)
    print(df)
    """
        A   B    C
    0  1  10  111
    1  2  20  122
    """
    ########################
    print("try AttrAnalytics.create_attr_by_series_arg")
    def new_series(series: pd.Series) -> str:
        element = str(series.A) + " as output"
        return element

    df['D'] = AttrAnalytics.create_attr_by_series_arg(new_series, df)
    print(df)
    """
       A   B    C            D
    0  1  10  111  1 as output
    1  2  20  122  2 as output
    """
    #########################
    print("try AttrAnalytics.same_func_create_row")
    def new_row(series: pd.Series) -> int:
        element = sum(series)
        return element

    df = df.drop(columns=['D'])
    a_row = AttrAnalytics.same_func_create_row(new_row, df)
    print(f"create a new row sum the num in each column")
    print(a_row)

    ###########################
    print("try AttrAnalytics.same_args_func_create_row")
    a_row = AttrAnalytics.same_args_func_create_row(new_row,df)
    print(a_row)

    ##########################
    print("try AttrAnalytics.multi_funcs_create_row")
    def new_row(series: pd.Series, num=None) -> int:
        element = sum(series)
        return element

    def new_row_2(series: pd.Series, num) -> int:
        element = sum(series) + num
        return element

    attr_func_pairs = {
        'A': new_row,
        'B': new_row_2,
        # 'X': new_row_2
    }
    a_row = AttrAnalytics.multi_funcs_create_row(attr_func_pairs, df, 1000)
    print(a_row)
    df = AttrAnalytics.concat_dfs(df, a_row)
    print("concat")
    print(df)

    ######################################
    print("try AttrAnalytics.create_attr_by_element_arg")
    def new_element(element):
        element = element + 1000
        return element

    df['E'] = AttrAnalytics.create_attr_by_element_arg(new_element, df.A)
    print(df)
    """
       A   B    C     E
    0  1  10  111  1001
    1  2  20  122  1002
    """
