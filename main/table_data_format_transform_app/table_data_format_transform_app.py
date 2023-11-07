"""
*************************************************************************
***              GENERAL-TABLE-PREPROCESSING-VISUALIZATION            ***
***                           VERSION:2.01                            ***
***                  e-mail: jameshanzhang@foxmail.com                ***
***   link: github.com/JamesHanZhang/general-table-preprocessing-visualization  ***
*************************************************************************
"""

import time

from analysis_modules import default_properties as prop
from basic_operation import *
from main.table_data_format_transform_app.mode_choices import *

print(prop.SOFTWARE_EXPLANATION)

def init_mode():
    sep_line()
    msg_line = "    ***********************************************************\n"
    msg = f"请根据数字选择数据导出模式:\n" \
          f"    {ModeChoicesDesc.SAME_STRUCT_MODE.value}\n{msg_line}" \
          f"    {ModeChoicesDesc.SAME_PARAMS_MODE.value}\n{msg_line}" \
          f"    {ModeChoicesDesc.DIFF_PARAMS_MODE.value}\n{msg_line}" \
          f"    {ModeChoicesDesc.BATCH_PARAMS_MODE.value}\n{msg_line}" \
          f"其他: 如直接回车, 默认激活<表结构一致模式>;\n"
    print(msg)
    initial_mode = input("请根据数字选择您希望激活的模式: ").strip()
    if initial_mode == "":
        initial_mode = ModeChoices.SAME_STRUCT_MODE
        return initial_mode
    error_msg = "请输入正确数字选择功能!"
    initial_mode = turn_value_to_enum(ModeChoices, initial_mode, error_msg)
    return initial_mode
    
def init_entrance_mode():
    count = 0
    while True:
        try:
            if count == 0:
                print("\n*********请输入参数*********\n")
            else:
                print("\n*********请重新输入参数*********\n")
            count += 1
            
            initial_mode = init_mode()
            
            print(f"\n######################## 您所输入的参数如下, 请重新确认 ################################\n\n"
                  f"您所选择的执行模式为: {ModeChoicesDesc[initial_mode.name].value}\n"
                  f"请再次确认...")
            
            if_process = input("请选择\n`YES`: 进入模式\n`NO`: 退出\n请输入选择字母并回车: ").strip()
            if if_process in ['YES', 'Y', 'Yes', 'yes', 'y']:
                break
            if if_process in ['NO', 'N', 'No', 'no', 'n']:
                print("您选择了退出.")
                time.sleep(3)
                exit()
        except (ValueError) as reason:
            print(reason)
            continue
    return initial_mode


def run():
    initial_mode = init_entrance_mode()
    if initial_mode == ModeChoices.SAME_STRUCT_MODE:
        run_same_struct_mode()
    if initial_mode == ModeChoices.SAME_PARAMS_MODE:
        run_diff_struct_same_params_mode()
    if initial_mode == ModeChoices.DIFF_PARAMS_MODE:
        run_diff_params_mode()
    if initial_mode == ModeChoices.BATCH_PARAMS_MODE:
        run_batch_params_mode()

if __name__=="__main__":
    run()