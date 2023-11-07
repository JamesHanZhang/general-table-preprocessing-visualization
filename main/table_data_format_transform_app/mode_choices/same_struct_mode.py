"""
*************************************************************************
***              GENERAL-TABLE-PREPROCESSING-VISUALIZATION            ***
***                           VERSION:2.01                            ***
***                  e-mail: jameshanzhang@foxmail.com                ***
***   link: github.com/JamesHanZhang/general-table-preprocessing-visualization  ***
*************************************************************************
"""

import time
import os
from analysis_modules import FormatTransformation
from analysis_modules import default_properties as prop
from analysis_modules import SysLog
from analysis_modules import ParamsMode, OutputMode, ParamsModeDesc, OutputModeDesc, IntegrateParams
from basic_operation import *
from main.table_data_format_transform_app.mode_choices.mode_choices_enum import ModeChoicesDesc

def sep_line():
    print("****************************")

def init_params_set() -> str:
    sep_line()
    params_set = input(
        f"请输入参数表名(没有拓展名), 如不输入并直接回车则默认为'{prop.DEFAULT_PARAMS_SET}': ").strip()
    if params_set == "":
        params_set = prop.DEFAULT_PARAMS_SET
    return params_set

def init_params_mode() -> Enum:
    sep_line()
    print(f"请选择以下不同的参数生成及导入模式: \n{ParamsModeDesc.FROM_SETTING.value}\n"
          f"{ParamsModeDesc.FROM_EXISTS.value}\n"
          f"{ParamsModeDesc.FROM_BASE.value}\n")
    params_mode_no = input("请根据数字选择您希望激活的模式: ").strip()
    error_msg = "请输入正确数字选择功能!"
    params_mode = turn_value_to_enum(ParamsMode, params_mode_no, error_msg)
    return params_mode

def init_output_mode() -> OutputMode:
    sep_line()
    msg_line = "    ***********************************************************\n"
    msg = f"请根据数字选择数据导出模式:\n" \
          f"    {OutputModeDesc.ACTIVATION_MODE.value}\n{msg_line}" \
          f"    {OutputModeDesc.EXTENSION_MODE.value}\n{msg_line}" \
          f"    {OutputModeDesc.FREE_MODE.value}\n{msg_line}" \
          f"其他: 如直接回车, 默认激活<自动模式>;\n"
    print(msg)
    output_mode_no = input("请根据数字选择您希望激活的模式: ").strip()
    if output_mode_no == "":
        return OutputMode.FREE_MODE
    
    error_msg = "请输入正确数字选择功能!"
    output_mode = turn_value_to_enum(OutputMode, output_mode_no, error_msg)
    return output_mode

def init_input_path():
    sep_line()
    input_path = input("请输入您希望导入的不同数据结构的多个数据文件的绝对路径\n"
                       "如直接回车, 则默认采用本地`input_dataset`默认路径\n"
                       "请输入: ").strip()
    if os.path.isabs(input_path):
        return input_path
    if input_path == "":
        input_path = prop.INPUT_PATH
        return input_path
    raise ValueError("路径输入错误! 必须是绝对路径!")

def init_output_path():
    sep_line()
    output_path = input("请输入您希望的导出路径(绝对路径)\n"
                       "如直接回车, 则默认采用本地`output_dataset`默认路径\n"
                       "请输入: ").strip()
    if os.path.isabs(output_path):
        return output_path
    if output_path == "":
        output_path = prop.OUTPUT_PATH
        return output_path
    raise ValueError("路径输入错误! 必须是绝对路径!")

def init_same_struct_mode_params() -> tuple[str, ParamsMode, OutputMode]:
    count = 0
    while True:
        try:
            if count == 0:
                print("\n*********请输入参数*********\n")
            else:
                print("\n*********请重新输入参数*********\n")
            count += 1
            
            log = f"您目前采用的模式为: \n{ModeChoicesDesc.SAME_STRUCT_MODE.value}\n"
            SysLog.show_log(log)
            
            params_set = init_params_set()
            params_mode = init_params_mode()
            output_mode = init_output_mode()
            input_path = init_input_path()
            output_path = init_output_path()
            
            print(f"\n######################## 您所输入的参数如下, 请重新确认 ################################\n\n"
                  f"您所输入的参数表名为: '{params_set}'\n"
                  f"您所选择的参数导入模式为: {ParamsModeDesc[params_mode.name].value}\n"
                  f"您所选择的数据导出模式为: {OutputModeDesc[output_mode.name].value}\n"
                  f"您所选择的导入路径为: {input_path}\n"
                  f"您所选择的导出路径为: {output_path}\n"
                  f"请再次确认...")
            
            if_process = input("请选择\n`YES`: 执行\n`NO`: 退出\n请输入选择字母并回车: ").strip()
            if if_process in ['YES', 'Y', 'Yes', 'yes', 'y']:
                break
            if if_process in ['NO', 'N', 'No', 'no', 'n']:
                print("您选择了退出.")
                time.sleep(3)
                exit()
        except (ValueError) as reason:
            print(reason)
            continue

    return params_set, params_mode, output_mode, input_path, output_path

def run_same_struct_mode():
    params_set, params_mode, output_mode, input_path, output_path = init_same_struct_mode_params()
    print("\n\n")
    msg = f"######################## 围绕参数表'{params_set}'的数据格式转换程序开始执行 ################################\n\n"
    SysLog.show_log(msg)
    ft = FormatTransformation()
    ft.reset_params(params_set,params_mode,output_mode,input_path=input_path, output_path=output_path)
    ft.run_based_on_params_set(params_set, params_mode, output_mode)
    msg = f"######################## 参数表'{params_set}'的数据转换进程已顺利结束执行 ################################\n\n"
    SysLog.show_log(msg)
    import_params, output_params, basic_process_params = IntegrateParams.get_params(params_set, ParamsMode.FROM_EXISTS)
    SysLog.show_log(f"共计转换数据量为: {import_params.import_index_size}条记录.")
    SysLog.show_log(prop.DISCLAIMER)
    time.sleep(4)
    
    
if __name__ == "__main__":
    run_same_struct_mode()