# self-made modules
import analysis_modules.default_properties as prop
from analysis_modules.sql_output_drivers.mysql_output_driver import MySqlOutputDriver
from analysis_modules.params_monitor import OutputParams

class GBaseOutputDriver(MySqlOutputDriver):
    def __init__(self, output_params: OutputParams, params_set: str=prop.DEFAULT_PARAMS_SET):
        super().__init__(output_params, params_set)