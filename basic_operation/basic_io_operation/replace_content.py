

import re
from tqdm import tqdm
from basic_operation.basic_io_operation.find_child_paths import FindChildPaths

class ReplaceContent(FindChildPaths):
    def __init__(self, encoding):
        # 使用super函数
        super().__init__(encoding)
        
    def sub_single_file_content(self, file_path:str, target:str, substitution:str) -> None:
        """
        替换内容
        target:= 正则表达式
        substitution:= 替换的内容（非正则表达式）
        """
        old_content = self.read_content(file_path)
        new_content = re.sub(target, substitution, old_content)
        self.store_file(output_path=file_path, content=new_content, overwrite=True)
        if old_content != new_content:
            print(f"substitution for file `{file_path}` is successfully done.")
        return

    def sub_paths_content(self, file_paths: list[str], target: str, substitution: str) -> None:
        """
        替换内容
        target:= 正则表达式
        substitution:= 替换的内容（非正则表达式）
        """
        for each_path in tqdm(file_paths,desc="to replace certain part of the files under archive..."):
            self.sub_single_file_content(each_path, target, substitution)
        return

    def sub_path_common_content(self, parent_path: str, target: str, substitution: str) -> None:
        """
        用来替换所有子文件的内容
        """
        file_paths = self.gain_child_file_paths(parent_path)
        self.sub_paths_content(file_paths, target, substitution)
        return

    def sub_type_path_common_content(self, parent_path: str, target: str, substitution: str, extension: str='.py')->None:
        """
        用来替换特定的文件类型（根据后缀名替换）的内容
        """
        file_paths = self.gain_child_certain_type_paths(parent_path, extension)
        self.sub_paths_content(file_paths, target, substitution)
        return

if __name__ == '__main__':
    target_content = ""
    substitution = ""
    encoding = "utf-8"
    rc = ReplaceContent(encoding)
    
    # 批量或者单文件
    if_batch = True
    
    if if_batch is True:
        parent_path = "D:\\CODE-PROJECTS\\PYTHON-PROJECTS\\general-table-preprocessing-visualization"
        extension = '.py'
        rc.sub_type_path_common_content(parent_path, target_content, substitution, extension)
    if if_batch is False:
        file_path = "D:\\CODE-PROJECTS\\PYTHON-PROJECTS\\data-format-analysis-tool\\analysis_modules\\app_entrances\\table_data_format_transform_app.py"
        rc.sub_single_file_content(file_path, target_content, substitution)

