"""
*************************************************************************
***              GENERAL-TABLE-PREPROCESSING-VISUALIZATION            ***
***                           VERSION:2.01                            ***
***                  e-mail: jameshanzhang@foxmail.com                ***
***   link: github.com/JamesHanZhang/general-table-preprocessing-visualization  ***
*************************************************************************
"""

from analysis_modules import FormatTransformation, DiffTransBatchFiles
from analysis_modules import default_properties as prop
from main.table_data_format_transform_app.mode_choices.same_struct_mode import *
from main.table_data_format_transform_app.mode_choices.mode_choices_enum import ModeChoicesDesc




def init_import_type():
    sep_line()
    extension = input("请输入该路径下的数据类型, 仅输入拓展名即可, 例如 `.csv`, `.xlsx`等;\n"
                      "如希望导入所有文件, 则请直接回车: ").strip()
    return extension

def init_diff_struct_same_params_mode():
    count = 0
    while True:
        try:
            if count == 0:
                print("\n*********请输入参数*********\n")
            else:
                print("\n*********请重新输入参数*********\n")
            count += 1
            
            log = f"您目前采用的模式为: \n{ModeChoicesDesc.SAME_PARAMS_MODE.value}\n"
            SysLog.show_log(log)
            
            params_set = init_params_set()
            params_mode = init_params_mode()
            output_mode = init_output_mode()
            input_path = init_input_path()
            output_path = init_output_path()
            import_type = init_import_type()
            
            print(f"\n######################## 您所输入的参数如下, 请重新确认 ################################\n\n"
                  f"您所输入的参数表名为: '{params_set}'\n"
                  f"您所选择的参数导入模式为: {ParamsModeDesc[params_mode.name].value}\n"
                  f"您所选择的数据导出模式为: {OutputModeDesc[output_mode.name].value}\n"
                  f"您所选择的导入路径为: {input_path}\n"
                  f"您选择希望导入的数据类型的拓展名为: {'全部' if import_type == '' else import_type}\n"
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
    return params_set, params_mode, output_mode, input_path, import_type, output_path


def run_diff_struct_same_params_mode():
    params_set, params_mode, output_mode, input_path, import_type, output_path = init_diff_struct_same_params_mode()
    print("\n\n")
    msg = f"######################## 围绕参数表'{params_set}'的数据格式转换程序开始执行 ################################\n\n"
    SysLog.show_log(msg)
    dtbf = DiffTransBatchFiles()
    dtbf.diff_trans_batch_files(params_set,params_mode,output_mode, import_type=import_type, input_path=input_path, output_path=output_path)
    msg = f"######################## 参数表'{params_set}'的数据转换进程已顺利结束执行 ################################\n\n"
    SysLog.show_log(msg)
    SysLog.show_log(prop.DISCLAIMER)
    time.sleep(3)


if __name__ == "__main__":
    run_diff_struct_same_params_mode()