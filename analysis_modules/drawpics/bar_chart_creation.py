
import pandas as pd
from sqlite3 import connect

# self-made modules
from analysis_modules.params_monitor import OutputParams
from analysis_modules import drawpics
from analysis_modules.drawpics.image_creation import ImageCreation
from analysis_modules.df_processing import NullProcessing

class BarChartCreation(ImageCreation):
    def __init__(self, output_params: OutputParams):
        super().__init__(output_params)

    def check_null_in_color(self, df, color):
        if color is None:
            return
        if_contains_null = NullProcessing.check_if_null_in_series(df[color])
        if if_contains_null is True:
            raise ValueError("the content of array must not contain null value in color parameter!")

    def create_simple_bar_chart(self, data_frame, x, y, title=None, color=None, show=True):
        self.check_null_in_color(data_frame, color)
        fig = drawpics.px.bar(data_frame, x, y, color=color, title=title, text_auto=True)
        if show is True:
            fig.show()
        return fig

    def create_multi_bar_charts(self, df, x, y, z,
                             title=None,
                             color=None,
                             show=True,
                             store_flag=False,
                             output_path=None):
        conn = connect(':memory:')
        df.to_sql("default_table", conn)
        df_groups = pd.read_sql(f"SELECT DISTINCT {z} FROM default_table;" ,conn)
        group_list = list(df_groups[z])

        fig_list = list()
        for each_group in group_list:
            if color is None:
                query = f"SELECT {x},{y} FROM default_table WHERE {z} = '{each_group}' ORDER BY {x} ASC;"
            else:
                query = f"SELECT {x},{y},{color} FROM default_table WHERE {z} = '{each_group}' ORDER BY {x} ASC;"
            new_title = f"{each_group} {title}"
            each_df = pd.read_sql(query, conn)
            fig = self.create_simple_bar_chart(each_df, x, y, new_title, color, show)
            fig_list.append(fig)

        # 图片保存速度慢，为减少等待，故单独分出线程运行
        if store_flag is True:
            for i in range(len(group_list)):
                output_file = f"{group_list[i]}_{title}.png"
                self.store_fig(fig_list[i], output_file, output_path)
        return




