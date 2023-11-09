from analysis_modules import *
from analysis_modules.default_properties import ParamsMode


start_time = start_program()
params_set = "DEFAULT"
input_file = "input_test3.csv"
import_params, output_params, basic_process_params = IntegrateParams.get_params(params_set,ParamsMode.FROM_SETTING)


# 导入表
dc = DfCreation()
df = dc.import_one_file_on_extension(import_params, params_set, input_file, if_circular=False)
print(df)
# df = df.sort_values('MINDATE')
# 作图
gantt = GanttCreation(output_params)
gantt.init_params('TABLE_AFFILIATION','MINDATE','MAXDATE','TABLE_AFFILIATION',from_date_format='%Y-%m-%d')
fig = gantt.create_gantt_by_timeline(df, sort_cols='MINDATE', ascendings=True)
gantt.store_fig(fig, "test.png")
# 结束
end_program(start_time)

