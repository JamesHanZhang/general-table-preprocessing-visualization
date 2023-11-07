from analysis_modules import *
from basic_operation import *

# 初始化
start_time = start_program()
import_params, output_params, basic_process_params = IntegrateParams.get_params_from_settings()
dc = DfCreation()
do = DfOutput()
sql_driver = SqlOutput()
bp = BasicProcessing()

input_path ="D:\\CODE-PROJECTS\\PYTHON-PROJECTS\\DATA-ANALYSIS-PROJECT\\input_dataset\\batch_examples"
# 直接以generator的形式读取，适合大数据
df_reader = dc.circular_import_data(import_params,input_path=input_path, if_batch=True)
pos = 0
for chunk in df_reader:
    do.output_on_extension(chunk, output_params, 'test.xlsx', chunk_no=pos, if_sep=True)
    sql_driver.output_as_sql_control(chunk, output_params, table_name='temp_table',if_sep=True,chunk_no=pos)
    pos+=1

df = dc.fully_import_data(import_params, input_path=input_path, if_batch=True)
output_file = "test.csv"
do.output_on_extension(df, output_params, output_file)
sql_driver.output_as_sql_control(df, output_params, table_name='temp_tablex', if_sep=True)


end_program(start_time)