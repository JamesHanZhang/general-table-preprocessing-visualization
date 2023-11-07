

import os
import re
import io
import sys
from tqdm import tqdm

class IoMethods(object):
    def __init__(self, encoding:str = "utf-8"):
        if encoding == "":
            self.encoding = 'utf-8'
        self.encoding = encoding

    def reset_encoding(self, encoding:str = "utf-8") -> None:
        self.encoding = encoding

    def read_content(self, full_input_path:str) -> str:
        with open(full_input_path, mode='r', encoding=self.encoding) as load_file:
            content:str = load_file.read()
        return content

    def direct_store_file(self, output_path: str, content: str, encoding="", overwrite=True) -> None:
        """
        保存文件，按照系统默认的encoding保存
        """
        if encoding != "":
            self.encoding = encoding
        if overwrite is True:
            storage_mode = 'w'
        else:
            storage_mode = 'a'
        # newline='\n' -> 保证导出脚本为UNIX格式；不设置encoding -> 保证导出脚本为ANSI格式
        try:
            file = io.open(output_path, mode=storage_mode, newline='\n')
            file.write(content)
        except (UnicodeEncodeError) as reason:
            # 假如导出有限制，那只能根据encoding导出
            file = io.open(output_path, mode=storage_mode, newline='\n', encoding=self.encoding)
            file.write(content)
        file.close()

    def store_file(self, output_path: str, content: str, encoding="", overwrite=True) -> None:
        """
        保存文件，按照指定的encoding保存
        """
        if encoding != "":
            self.encoding = encoding
        if overwrite is True:
            storage_mode = 'w'
        else:
            storage_mode = 'a'
        # newline='\n' -> 保证导出脚本为UNIX格式；
        file = io.open(output_path, mode=storage_mode, newline='\n', encoding=self.encoding)
        file.write(content)
        file.close()

    @staticmethod
    def check_if_path_exists(dir_path, pop_error=True):
        # 判断路径是否存在
        if_exists = os.path.isdir(dir_path)
        if if_exists is False and pop_error is True:
            raise FileNotFoundError(f"the path {dir_path} doesn't exist.")
        elif if_exists is False and pop_error is False:
            return False
        return True

    @staticmethod
    def check_if_file_exists(full_path, pop_error=True):
        # 判断文件是否存在
        if_exists = os.path.isfile(full_path)
        if if_exists is False and pop_error is True:
            raise FileNotFoundError("file {a} doesn't exist!".format(a=full_path))
        elif if_exists is False and pop_error is False:
            return False
        return True

    @staticmethod
    def remove_file(full_path):
        # 删除文件
        try:
            os.remove(full_path)
        except (FileNotFoundError):
            pass
        return True

    @staticmethod
    def path_mkdir(path):
        # 创建路径
        try:
            os.makedirs(path)
        except FileExistsError as reason:
            pass
        finally:
            return path

    @classmethod
    def mkdir_if_no_dir(cls, path: str):
        if_exists = cls.check_if_path_exists(path, pop_error=False)
        if if_exists is False:
            cls.path_mkdir(path)

    @staticmethod
    def join_path(mother_path, child_path) -> str:
        if child_path != "" and child_path[0] in ['/', '\\']:
            child_path = child_path[1:]
        full_path = os.path.join(mother_path, child_path)
        full_path = os.path.normpath(full_path)
        return full_path

    @staticmethod
    def get_dir_from_file_path(file_path):
        # 如果文件路径没有后缀名，则默认为路径
        if IoMethods.get_file_extension(file_path) == "":
            if file_path[-1] not in ['/','\\']:
                file_path += '\\'
        path = os.path.dirname(file_path)
        return path

    @staticmethod
    def get_file_extension(file_name):
        file_name = os.path.basename(file_name)
        extension = os.path.splitext(file_name)[1]
        return extension

    @staticmethod
    def get_main_file_name(file_name: str) -> str:
        file_name = os.path.basename(file_name)
        file_name = os.path.splitext(file_name)[0]
        return file_name
    
    @classmethod
    def get_full_file_name(cls, file_path):
        full_file_name = cls.get_main_file_name(file_path) + cls.get_file_extension(file_path)
        return full_file_name

    @staticmethod
    def get_last_folder_on_path(path: str) -> str:
        last_folder = os.path.basename(os.path.normpath(path))
        return last_folder

    @classmethod
    def search_upward_path(cls, target_folder, full_path = "") -> str|None:
        # 从当前目录往上检索，直到找到target_folder的路径，如不存在则报None
        if full_path == "":
            # 调用默认当前路径
            full_path = cls.get_current_path()
        if cls.get_last_folder_on_path(full_path) == target_folder:
            return full_path
        while True:
            last_path = full_path
            full_path = os.path.dirname(full_path)
            if last_path == full_path:
                break
            if cls.get_last_folder_on_path(full_path) == target_folder:
                return full_path
        return None
    @staticmethod
    def get_current_path():
        path = os.path.dirname(sys.path[0])
        return path

    @staticmethod
    def get_folders_on_path(path) -> list[str]:
        path = os.path.normpath(path)
        if "/" in path:
            folder_list = path.split('/')
        else:
            folder_list = path.split('\\')
        return folder_list

    @staticmethod
    def get_folder_path_under_project(child_path, project_name):
        parent_path = IoMethods.search_upward_path(project_name)
        if parent_path is None:
            return None
        full_path = IoMethods.join_path(parent_path, child_path)
        return full_path