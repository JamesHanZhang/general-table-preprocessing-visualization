import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
from enum import Enum, unique

from analysis_modules.params_monitor import OutputParams, SysLog
from analysis_modules.drawpics.image_creation import ImageCreation
from analysis_modules import default_properties as prop
from analysis_modules import GanttColor
from analysis_modules import drawpics
from analysis_modules.df_processing import BasicProcessing
from basic_operation import *

class GanttCreation(ImageCreation):
    def __init__(self, output_params: OutputParams):
        """
        :param df: 时间上必须满足YYYY-mm-dd的格式，或者YYYY-mm-dd h24:mi:ss的格式
        """
        super().__init__(output_params)
        self.date_format_required = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d']

    def init_params(self,
                   task_col='Task',
                   start_col='Start',
                   end_col='Finish',
                   index_col='Task',
                   from_date_format = '%Y-%m-%d %H:%M:%S', # 字符串数据的导入的原始时间格式, 用来转换成标准的时间格式
                   to_date_format = '%Y-%m-%d', # 希望转换的标准时间格式, 看是按日期还是按具体的时间点
                   index_type=GanttColor.DIVIDED_COLOR_BAR.value,
                   colors=None):
        """
        :param task_col: task
        :param start_col: start date
        :param end_col: end date
        :param index_col: column for color index change
        :param index_type: ['Resource', 'Complete'] the color bar type
        :param colors: dict type, key: resource category, value: color
        :return:
        """
        self.index_col = index_col
        self.colors = colors
        self.from_date_format = from_date_format
        self.to_date_format = to_date_format
        self.error_if_not_required(self.to_date_format, self.date_format_required, 'to_date_format')
        self.index_type = index_type
        self.start_col = start_col
        self.end_col = end_col

        self.change_names = {
            task_col: 'Task',
            start_col: 'Start',
            end_col: 'Finish'
        }
        if index_col == task_col:
            self.index_col = 'Task'
            self.show_colorbar = False
        else:
            self.index_col = index_type
            self.change_names[index_col] = self.index_col
            self.show_colorbar = True
        return
    
    def turn_df_to_required(self, df: pd.DataFrame, sort_cols="", ascendings=True) -> pd.DataFrame:
        if sort_cols != "":
            df = self.sort_df_for_pic_order(df, sort_cols, ascendings)
        df = BasicProcessing.change_column_names(df, self.change_names)
        cols = ['Start','Finish']
        for col in cols:
            if 'datetime' in str(df[col].dtype):
                df = BasicProcessing.turn_date_format_to_str(df, col, self.to_date_format)
            elif 'object' in str(df[col].dtype):
                df = BasicProcessing.turn_str_to_date_format(df, col, self.from_date_format)
                df = BasicProcessing.turn_date_format_to_str(df, col, self.to_date_format)
            else:
                raise TypeError(f"column in dataframe {self.start_col} and {self.end_col} must be datetime type or object type.")
        return df

    @SysLog().calculate_cost_time("<create gantt by factory>")
    def create_gantt_by_factory(self, df, show=True, sort_cols:list[str]|str="", ascendings:list[bool]|bool=True):
        # 限制输入的参数范围
        self.error_if_not_required(self.index_type, ['Resource', 'Complete'], 'index_type')
        df = self.turn_df_to_required(df, sort_cols, ascendings)
        fig = ff.create_gantt(df, colors=self.colors, index_col=self.index_col,
                                       show_colorbar=self.show_colorbar, group_tasks=True, showgrid_x=True)
        if show is True:
            fig.show()
        return fig

    @SysLog().calculate_cost_time("<create gantt by timeline>")
    def create_gantt_by_timeline(self, df, show=True, sort_cols:list[str]|str="", ascendings:list[bool]|bool=True):
        # 限制输入的参数范围
        self.error_if_not_required(self.index_type, ['Resource', 'Completion_pct'], 'index_type')
        df = self.turn_df_to_required(df, sort_cols, ascendings)
        fig = px.timeline(df, x_start='Start', x_end='Finish', y='Task', color=self.index_col)
        if show is True:
            fig.show()
        return fig



