import pandas as pd

from analysis_modules.params_monitor import SysLog
from analysis_modules.df_processing.null_processing import NullProcessing
from analysis_modules import default_properties as prop
from analysis_modules.df_processing.data_masking import DataMasking
from analysis_modules.params_monitor import BasicProcessParams


class BasicProcessing:
    def __init__(self):
        self.log = SysLog()
        self.replaceNaN = prop.REPLACE_NAN

    @staticmethod
    def raise_not_found_element_error(df, pick_columns, func_name):
        columns = df.columns.tolist()
        not_found_list = list()
        for each_pick in pick_columns:
            if each_pick not in columns:
                not_found_list.append(each_pick)
        if not_found_list == list():
            return
        msg=""
        for each_col in not_found_list:
            msg+= f"[ValueError]: value {each_col} in parameters from '{func_name}' function " \
                  f"is not found in the columns from input dataframe, please check again."
        raise ValueError(msg)

    @staticmethod
    def find_repetitive_elements(input_list):
        com_list = list(set(input_list))
        repetitive_elements=dict()
        for each_col in com_list:
            each_num = input_list.count(each_col)
            if each_num > 1:
                repetitive_elements[each_col] = each_num
        return repetitive_elements

    @classmethod
    def raise_repetitive_error(cls, input_list, func_name):
        repetitive_elements = cls.find_repetitive_elements(input_list)
        if repetitive_elements == dict():
            return
        msg = ""
        for key in repetitive_elements.keys():
            msg += f"[ValueError]: value '{key}' in parameter from '{func_name}' function " \
                   f"is repeated for {repetitive_elements[key]} times, which is not allowed."
        raise ValueError(msg)

    @classmethod
    @SysLog().calculate_cost_time("<pick columns>")
    def pick_columns(cls, df, pick_columns):
        """
        :param df: dataframe
        :param pick_columns: list, columns to pick
        :return:
        """
        func_name = "pick certain columns from dataframe"
        cls.raise_repetitive_error(pick_columns, func_name)
        cls.raise_not_found_element_error(df, pick_columns, func_name)
        df = df[pick_columns]
        SysLog.show_log("[CERTAIN COLUMNS PICKED]: {0} columns picked from dataframe".format(str(pick_columns)))
        return df
    
    @staticmethod
    def turn_str_to_date_format(df: pd.DataFrame, col: str, date_format='%Y-%m-%d'):
        dtypes = df.dtypes.to_dict()
        if dtypes[col] == 'object':
            df[col] = pd.to_datetime(df[col], format=date_format)
            return df
        raise TypeError(f"type for column {col} must be object in pandas, which is now type {dtypes[col]}.")
    
    @staticmethod
    def turn_date_format_to_str(df: pd.DataFrame, col: str, date_format='%Y-%m-%d'):
        dtypes = df.dtypes.to_dict()
        if 'datetime' in str(dtypes[col]):
            df[col] = df[col].dt.strftime(date_format)
            return df
        raise TypeError(f"type for column {col} must be datetime type in pandas, which is now type {str(dtypes[col])}.")
    
    @classmethod
    def change_date_types(cls, df: pd.DataFrame, change_types, from_date_formats={}, to_date_formats={})-> tuple[pd.DataFrame, dict]:
        # 特殊情况, 时间转换, 先过一遍时间转换的需求,
        df_dtypes = df.dtypes.to_dict()
        no_date_change_types = dict()
        for column in change_types.keys():
            if 'datetime' in str(df_dtypes[column]):
                try:
                    date_format = from_date_formats[column]
                except KeyError:
                    date_format = '%Y-%m-%d'
                df = cls.turn_date_format_to_str(df, column, date_format)
            if 'datetime' in change_types[column]:
                try:
                    date_format = to_date_formats[column]
                except KeyError:
                    date_format = '%Y-%m-%d'
                df = cls.turn_str_to_date_format(df, column, date_format)
            else:
                no_date_change_types[column] = change_types[column]
        return df, no_date_change_types
    
    @classmethod
    @SysLog().calculate_cost_time("<change column types>")
    def change_column_types(cls, df, change_types, from_date_formats:dict={}, to_date_formats:dict={}) -> pd.DataFrame:
        """
        :param df: dataframe
        :param change_types: dict, key is column name, while value is target type
        :return: dataframe
        """
        repl_null = False
        columns = df.columns.tolist()
        # 先过一遍时间类型转换的需求
        df, change_types = cls.change_date_types(df, change_types, from_date_formats, to_date_formats)
        
        for column in change_types.keys():
            # 一次只修改一列类型，这样即便错误，也只针对这列进行空值转换
            if column in columns:
                change_type = dict()
                change_type[column] = change_types[column]
                try:
                    df = df.astype(change_type)
                except (ValueError) as reason:
                    try:
                        # 将np.nan替换为replaceNaN（一般情况不会遇到），一次只改一列
                        df[column] = NullProcessing.replace_null(df[column])
                        df = df.astype(change_type)
                        repl_null = True

                        msg_log = f"[ValueError]: ValueError '{reason}' may occured:\n" \
                                  f"now it tries to replace np.nan with replaceNaN {str(prop.REPLACE_NAN)} " \
                                  f"in column {column} in table \n" \
                                  f"in order to fix this problem."
                        SysLog.show_log(msg_log)
                    except (ValueError) as reason:
                        msg_log = f"[ValueError]: {reason}\n" \
                                  f"[ERROR EXPLANATION]: element in dataframe can't be converted to target type."
                        SysLog.show_log(msg_log)
                        raise ValueError(msg_log)

        msg_log = f"[COLUMN TYPE CONVERSION]: Table's column types have been changed based on following structure"
        SysLog.show_construct_log(msg_log, change_types)
        # 将replaceNaN重新替换为np.nan
        if repl_null is True:
            df = NullProcessing.turn_back_null(df)
        return df

    @classmethod
    @SysLog().calculate_cost_time("<change column names>")
    def change_column_names(cls, df, change_names):
        """
        :param df: dataframe
        :param change_names: dict, key is original name, and value is target name
        :return: dataframe
        """
        columns = df.columns.tolist()
        new_cols = list()
        for each_col in columns:
            if each_col in list(change_names.keys()):
                new_cols.append(change_names[each_col])
            else:
                new_cols.append(each_col)
        cls.raise_repetitive_error(new_cols, "change column names")
        df = df[columns]
        df.columns = new_cols
        msg_log = f"[TABLE COLUMN NAMES CONVERSION]: Table columns' names have been changed based on following structure"
        SysLog.show_construct_log(msg_log, change_names)
        return df
    
    @classmethod
    @SysLog().calculate_cost_time("<basic processing>")
    def basic_process_data(cls, df: pd.DataFrame, basic_process_params: BasicProcessParams) -> pd.DataFrame:
        dm = DataMasking()
        for func_app in basic_process_params.basic_processing_order:
            if func_app == 'change_names_previously' and basic_process_params.change_names_previously.activation is True:
                df = cls.change_column_names(df, basic_process_params.change_names_previously.change_names)
            elif func_app == 'change_names_finally' and basic_process_params.change_names_finally.activation is True:
                df = cls.change_column_names(df, basic_process_params.change_names_finally.change_names)
            elif func_app == 'change_types_opt' and basic_process_params.change_types_opt.activation is True:
                change_types = basic_process_params.change_types_opt.change_types
                from_date_formats = basic_process_params.change_types_opt.from_date_formats
                to_date_formats = basic_process_params.change_types_opt.to_date_formats
                df = cls.change_column_types(df, change_types, from_date_formats, to_date_formats)
            elif func_app == 'pick_columns_opt' and basic_process_params.pick_columns_opt.activation is True:
                df = cls.pick_columns(df, basic_process_params.pick_columns_opt.pick_columns)
            elif func_app == 'data_masking_opt' and basic_process_params.data_masking_opt.activation is True:
                df = dm.data_masking(df, basic_process_params.data_masking_opt.masking_columns, basic_process_params.data_masking_opt.masking_type)
        return df

if __name__=='__main__':
    data = {
        'Task': ['Task A', 'Task B', 'Task C', 'Task D'],
        'Start': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
        'End': ['2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08']
    }
    
    df = pd.DataFrame(data)
    print(str(df['Task'].dtype))
    df = BasicProcessing.turn_str_to_date_format(df, 'Start','%Y-%m-%d')
    df = BasicProcessing.turn_date_format_to_str(df, 'Start','%Y%m%d')
    print(df)
