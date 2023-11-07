"""
*************************************************************************
***              GENERAL-TABLE-PREPROCESSING-VISUALIZATION            ***
***                           VERSION:2.01                            ***
***                  e-mail: jameshanzhang@foxmail.com                ***
***   link: github.com/JamesHanZhang/general-table-preprocessing-visualization  ***
*************************************************************************
"""

from main.table_data_format_transform_app.mode_choices.same_struct_mode import *
from main.table_data_format_transform_app.mode_choices.mode_choices_enum import ModeChoicesDesc

def init_params_set_list() -> list[str]:
    sep_line()
    params_sets = input("请输入需批量执行的参数表名, 以英文输入的逗号分隔(','): ").strip()
    params_sets = params_sets.split(',')
    new_params_sets = list()
    for each in params_sets:
        new_params_sets.append(each.strip())
    return new_params_sets


def init_batch_params_mode():
    count = 0
    while True:
        try:
            if count == 0:
                print("\n*********请输入参数*********\n")
            else:
                print("\n*********请重新输入参数*********\n")
            count += 1
            
            log = f"您目前采用的模式为: \n{ModeChoicesDesc.BATCH_PARAMS_MODE.value}\n"
            SysLog.show_log(log)
            
            params_sets = init_params_set_list()
            output_mode = init_output_mode()
            
            print(f"\n######################## 您所输入的参数如下, 请重新确认 ################################\n\n"
                  f"您所输入的多个参数表名为: {str(params_sets)}\n"
                  f"共计有{len(params_sets)}个参数表即将开始执行;\n"
                  f"您所选择的数据导出模式为: {OutputModeDesc[output_mode.name].value}\n"
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
    return params_sets, output_mode


def run_batch_params_mode():
    params_sets, output_mode = init_batch_params_mode()
    msg = f"######################## 围绕参数表'{str(params_sets)}'的数据格式转换程序开始执行 ################################\n\n"
    SysLog.show_log(msg)
    ft = FormatTransformation()
    ft.run_multi_params_sets(params_sets, output_mode)
    msg = f"######################## 参数表'{str(params_sets)}'的数据转换进程已顺利结束执行 ################################\n\n"
    SysLog.show_log(msg)
    SysLog.show_log(prop.DISCLAIMER)
    time.sleep(3)


if __name__ == "__main__":
    run_batch_params_mode()