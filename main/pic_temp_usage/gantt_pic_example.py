from analysis_modules.df_import_drivers import DfCreation
from analysis_modules.params_monitor import *

# 初始化参数
start_time = start_program()
ip = IntegratedParameters()
ip.init_params()

# 导入表
dc = DfCreation()
df = dc.import_on_extension("02.input_test.csv")

# 作图
gantt = GanttCreation()
gantt.init_params('TABLE_AFFILIATION','MINDATE','MAXDATE','TABLE_AFFILIATION')
fig = gantt.create_gantt_by_factory(df)
gantt.store_fig(fig, "test.png")
# 结束
end_program(start_time)

