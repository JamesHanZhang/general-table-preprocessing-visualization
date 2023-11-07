from analysis_modules.params_monitor import OutputParams, SysLog
from analysis_modules.drawpics.image_creation import ImageCreation
from analysis_modules import default_properties as prop
from analysis_modules import drawpics
from analysis_modules.df_processing import BasicProcessing

class GanttCreation(ImageCreation):
    def __init__(self, output_params: OutputParams):
        """
        :param df: 时间上必须满足YYYY-mm-dd的格式，或者YYYY-mm-dd h24:mi:ss的格式
        """
        super().__init__(output_params)

    def init_params(self,
                   task_col='Task',
                   start_col='Start',
                   end_col='Finish',
                   index_col='Task',
                   index_type=prop.DIVIDED_COLOR_BAR,
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
        self.index_type = index_type

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

    @SysLog().calculate_cost_time("<create gantt by factory>")
    def create_gantt_by_factory(self, df, show=True):
        # 限制输入的参数范围
        self.error_if_not_required(self.index_type, ['Resource', 'Complete'], 'index_type')
        df = BasicProcessing.change_column_names(df, self.change_names)
        fig = drawpics.ff.create_gantt(df, colors=self.colors, index_col=self.index_col,
                                       show_colorbar=self.show_colorbar, group_tasks=True, showgrid_x=True)
        if show is True:
            fig.show()
        return fig

    @SysLog().calculate_cost_time("<create gantt by timeline>")
    def create_gantt_by_timeline(self, df, show=True):
        # 限制输入的参数范围
        self.error_if_not_required(self.index_type, ['Resource', 'Completion_pct'], 'index_type')
        df = BasicProcessing.change_column_names(df, self.change_names)
        fig = drawpics.px.timeline(df, x_start='Start', x_end='Finish', y='Task', color=self.index_col)
        if show is True:
            fig.show()
        return fig



