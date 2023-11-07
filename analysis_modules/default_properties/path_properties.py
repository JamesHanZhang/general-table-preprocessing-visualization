import sys
import os
from basic_operation.basic_io_operation import IoMethods
from analysis_modules.default_properties.project_properties import PROJECT_NAME

def get_default_path(relative_path, project_name):
    normal_path = IoMethods.get_folder_path_under_project(relative_path, project_name)
    if normal_path is not None:
        # 当打包后，路径混乱，就找不到该路径了
        return normal_path
    # 这个时候就要调用打包后的路径
    # 获取可执行文件的路径，只有通过pyinstaller打包后才能生效
    executable_path = sys.executable
    # 获取可执行文件所在的目录
    executable_directory = os.path.dirname(executable_path)
    pyinstaller_path = IoMethods.join_path(executable_directory, relative_path)
    IoMethods.mkdir_if_no_dir(pyinstaller_path)
    return pyinstaller_path


SYS_LOG_PATH = get_default_path("log",PROJECT_NAME)
RESOURCES_PATH = get_default_path("resources",PROJECT_NAME)
INPUT_PATH = get_default_path("input_dataset",PROJECT_NAME)
OUTPUT_PATH = get_default_path("output_dataset",PROJECT_NAME)

# 如果希望所有文件都在执行文件的路径下出现
# SYS_LOG_PATH = ""
# RESOURCES_PATH = ""
# INPUT_PATH = ""
# OUTPUT_PATH = ""