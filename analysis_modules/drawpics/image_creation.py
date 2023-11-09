import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
import time


from analysis_modules.params_monitor import SysLog
from basic_operation.basic_io_operation import IoMethods
from analysis_modules.params_monitor import OutputParams

class ImageCreation:
    def __init__(self, output_params: OutputParams):
        self.log = SysLog()
        self.output_path = output_params.output_path
        self.output_types = ['.jpeg','.png','.webp','.svg','.pdf','.eps']

    def error_if_not_required(self, value, need_list, param_name):
        if value not in need_list:
            msg = f"[Attribute Error] parameter {param_name} must be one of these values: {str(need_list)}"
            print(msg)
            time.sleep(3)
            raise AttributeError(msg)
        
    @staticmethod
    def sort_df_for_pic_order(df:pd.DataFrame, sort_cols:list[str]|str, ascendings:list[bool]|bool=True):
        # ascending: True -> ascending
        # ascending: False -> descending
        if type(sort_cols) == type(ascendings) == list:
            df_sorted = df.sort_values(by=sort_cols, ascending=ascendings)
        elif type(sort_cols) == str and type(ascendings) == bool:
            df_sorted = df.sort_values(by=sort_cols, ascending=ascendings)
        else:
            raise TypeError("you must make sure when sort_cols is list[str], the ascending must be also list[bool]\n"
                            "when sort_cols is str, the ascending must be bool type.")
        return df_sorted
        
        

    @SysLog().calculate_cost_time("<store fig>")
    def store_fig(self, fig, output_file: str, output_path: str=None):
        extension = IoMethods.get_file_extension(output_file)
        self.error_if_not_required(extension, self.output_types, "output_file's extension")
        if output_path is not None:
            self.output_path = output_path
        IoMethods.mkdir_if_no_dir(self.output_path)
        full_output_path = IoMethods.join_path(self.output_path, output_file)

        fig.write_image(full_output_path)
        self.log.show_log(f'[IMAGE OUTPUT] image is stored as: {full_output_path}')
        return