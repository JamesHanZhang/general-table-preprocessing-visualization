

import pandas as pd
from sqlite3 import connect
import plotly.figure_factory as ff
import plotly.express as px

# self-made modules
from analysis_modules.params_monitor import OutputParams
from analysis_modules import drawpics
from analysis_modules.drawpics.image_creation import ImageCreation
from analysis_modules.df_processing import NullProcessing


class LineChartCreation(ImageCreation):
    def __init__(self, output_params: OutputParams):
        super().__init__(output_params)