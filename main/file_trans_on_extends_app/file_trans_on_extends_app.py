import time
import os
import codecs
from analysis_modules import FormatTransformation
from analysis_modules import default_properties as prop
from analysis_modules import SysLog
from analysis_modules import ParamsMode, OutputMode
from basic_operation import IoMethods
from analysis_modules import ImportParams, BasicProcessParams, OutputParams, IntegrateParams

def sep_line():
    print("****************************")

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

def init_sep(file_name, version):
    extension = IoMethods.get_file_extension(file_name)
    csv_sep = ""
    if extension == '.csv':
        sep_line()
        csv_sep = input(f"请输入您希望{version}的csv文件的分隔符, 并回车: ").strip()
        if csv_sep == "":
            raise ValueError("请正确输入分隔符!")
    return csv_sep

def init_sheet(file_name, version):
    extension = IoMethods.get_file_extension(file_name)
    if extension in ['.xls', '.xlsx', '.xltx', '.xlsm', '.xlt', '.xltm', '.xlam', '.xla']:
        sep_line()
        sheet = input(f"请输入您{version}的excel表的子表名称, 如直接回车则莫问为`Sheet1`: ").strip()
        if sheet != "":
            return sheet
        else:
            return "Sheet1"
    return None

def init_if_batch():
    sep_line()
    if_batch = input("请选择是否为批量导入同数据结构数据并合并为同一个文件(Y/N), 除非选择YES, 否则默认为单文件导入: ").strip()
    if if_batch in ['YES', 'Y', 'Yes', 'yes', 'y']:
        return True
    return False

def init_if_sep() -> tuple[bool, int]:
    sep_line()
    if_sep = input("是否需要将导出数据拆分为多个子数据? (Y/N), 除非选择YES, 否则默认为不拆分: ").strip()
    if if_sep in ['YES', 'Y', 'Yes', 'yes', 'y']:
        sep_line()
        chunksize = input('请选择每个子文件的记录上限条数, 直接回车默认为`50000`: ').strip()
        if chunksize == "":
            chunksize = 50000
        try:
            chunksize = int(chunksize)
        except ValueError:
            raise ValueError("请输入数字!")
        return True, chunksize
    return False, 50000

def init_encoding(file_name, version):
    extension = IoMethods.get_file_extension(file_name)
    if extension in ['.md', '.csv']:
        sep_line()
        if version == "导入":
            print("如不填写编码encoding, 默认为自动识别文本的编码encoding.")
        if version == "导出":
            print("如不填写编码encoding, 默认导出文本的编码encoding为中文编码: 'gb18030'")
        encoding = input(f"请输入您希望{version}的文件的编码(例如: utf-8): ").strip()
        if encoding == "":
            return encoding
        if codecs.lookup(encoding):
            return encoding.lower()
        else:
            raise ValueError("您所输入的不是正确的编码encoding, 请确认输入的编码encoding正确!")
    return ""


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

def init_file(version: str):
    sep_line()
    file_name = input(f"请输入您希望{version}的文件名(含拓展名, e.g. test.csv): ").strip()
    extension = IoMethods.get_file_extension(file_name)
    if extension not in ['.xls', '.xlsx', '.xltx', '.xlsm', '.xlt', '.xltm', '.xlam', '.xla','.csv','.md']:
        raise ValueError("文件输入不能为空, 或不能没有拓展名(.md, .csv, .xls, .xlsx等等)!")
    return file_name


start_words = """
######################## 欢迎使用数据格式转换软件 ###############################
本软件仅支持excel, markdown, csv文件的互相转换
根据文件的拓展名(例如.csv, .md, .xlsx)来判断输入输出的文件类型
########################## 请输入参数并执行程序 #################################
"""

def init_same_struct_mode_params():
    SysLog.show_log(start_words)
    count = 0
    while True:
        try:
            if count == 0:
                print("\n*********请输入参数*********\n")
            else:
                print("\n*********请重新输入参数*********\n")
            count += 1
            
            print("仅支持markdown, excel, csv文件之间的互相转换!")
            
            print("请输入导入文件的参数:")
            input_file = init_file("导入")
            input_sep = init_sep(input_file, "导入")
            input_encoding = init_encoding(input_file, "导入")
            input_path = init_input_path()
            
            print("\n\n请输入导出文件的参数:")
            if_sep, chunksize = init_if_sep()
            output_file = init_file("导出")
            output_sep = init_sep(output_file, '导出')
            output_encoding = init_encoding(output_file, "导出")
            output_path = init_output_path()
            
            
            input_encoding_msg = f"您所输入的导入的编码encoding为'{input_encoding}'\n" if input_encoding != "" else ""
            output_encoding_msg = f"您所输入的导出的编码encoding为'{output_encoding}'\n" if output_encoding != "" else ""
            input_sep_msg = f"您所输入的导入csv文件的分隔符为'{input_sep}'\n" if input_sep != "" else ""
            output_sep_msg = f"您所输入的导出csv文件的分隔符为'{output_sep}'\n" if output_sep != "" else ""
            if_sep_msg = f"您选择了对数据进行拆分, 各子文件的拆分记录上限为{chunksize}条记录\n" if if_sep is True else ""
            
            print(f"\n######################## 您所输入的参数如下, 请重新确认 ################################\n\n"
                  f"您所输入的导入文件名为: '{input_file}'\n{input_sep_msg}{input_encoding_msg}"
                  f"您所选择的导入路径为: {input_path}\n"
                  f"{if_sep_msg}您所输入的导出文件名为: '{output_file}'\n{output_sep_msg}{output_encoding_msg}"
                  f"您所选择的导出路径为: {output_path}\n"
                  f"请再次确认...")
            
            if_process = input("请选择\n`YES`: 执行\n`NO`: 退出\n请输入选择并回车, 其他则重新输入参数: ").strip()
            if if_process in ['YES', 'Y', 'Yes', 'yes', 'y']:
                break
            if if_process in ['NO', 'N', 'No', 'no', 'n']:
                print("您选择了退出.")
                time.sleep(3)
                exit()
        except (ValueError) as reason:
            print(reason)
            continue
    
    return input_file, input_path , input_sep, input_encoding, if_sep, chunksize, output_file, output_path, output_sep, output_encoding


def run_same_struct_mode():
    input_file, input_path , input_sep, input_encoding, if_sep, chunksize, output_file, output_path, output_sep, output_encoding = init_same_struct_mode_params()
    params_set = prop.DEFAULT_PARAMS_SET
    
    # 修改参数
    import_params, output_params, basic_process_params = IntegrateParams.get_params(params_set, ParamsMode.FROM_SETTING)
    import_params.csv_import_params.input_sep = input_sep
    import_params.input_file = input_file
    import_params.input_path = input_path
    import_params.chunksize = chunksize
    import_params.input_encoding = import_params.check_if_encoding(input_encoding, prop.DEFAULT_ENCODING)
    import_params.store_import_params(params_set)
    
    output_params.output_file = output_file
    output_params.output_path = output_path
    output_params.csv_output_params.output_sep = output_sep
    output_params.chunksize = chunksize
    output_params.if_sep = if_sep
    output_params.output_encoding = output_params.get_encoding(output_encoding, prop.DEFAULT_ENCODING)
    output_params.store_output_params(params_set)
    
    print("\n\n")
    msg = f"######################## 围绕参数表'{params_set}'的数据格式转换程序开始执行 ################################\n\n"
    SysLog.show_log(msg)
    ft = FormatTransformation()
    ft.run_based_on_params_set(params_set, ParamsMode.FROM_EXISTS, OutputMode.EXTENSION_MODE)
    import_params, output_params, basic_process_params = IntegrateParams.get_params(params_set, ParamsMode.FROM_EXISTS)
    
    msg = f"######################## 参数表'{params_set}'的数据转换进程已顺利结束执行 ################################\n\n"
    SysLog.show_log(msg)
    SysLog.show_log(f"共计转换数据量为: {import_params.import_index_size}条记录.")
    SysLog.show_log(prop.DISCLAIMER)
    time.sleep(4)


if __name__ == "__main__":
    run_same_struct_mode()