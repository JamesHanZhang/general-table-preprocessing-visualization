

import os

# self-made modules
from basic_operation.basic_io_operation.iomethods import IoMethods

class FindChildPaths(IoMethods):
    def __init__(self, encoding):
        # 调用未绑定的父类方法
        IoMethods.__init__(self, encoding)
    @classmethod
    def files_under_archive(cls, input_path: str) -> list[str]:
        # 一层目录下的所有文件
        file_list: list[str] = [file for file in os.listdir(input_path) if
                                os.path.isfile(os.path.join(input_path, file))]
        return file_list

    @classmethod
    def archives_under_archive(cls, input_path: str) -> list[str]:
        # 一层目录下的所有文件夹
        archive_list: list[str] = [archive for archive in os.listdir(input_path) if
                                   os.path.isdir(os.path.join(input_path, archive))]
        return archive_list

    @classmethod
    def paths_under_archive(cls, input_path: str, is_file=True) -> list[str]:
        # 一层目录下的所有文件或文件夹的路径
        if is_file is True:
            files = cls.files_under_archive(input_path)
        else:  # for folders
            files = cls.archives_under_archive(input_path)

        file_paths = list()
        for each_file in files:
            file_paths.append(cls.join_path(input_path, each_file))
        return file_paths

    @classmethod
    def gain_child_folder_paths_dfs(cls, input_path: str) -> list[str]:
        # 该路径下的所有目录的路径
        folder_paths = cls.paths_under_archive(input_path, is_file=False)
        if folder_paths == []:
            return []
        for folder_path in folder_paths:
            # 通过不断深层次调用函数，一层一层嵌套来进行DFS
            children_paths = cls.gain_child_folder_paths_dfs(folder_path)
            folder_paths += children_paths
        return folder_paths

    @classmethod
    def gain_child_folder_paths_bfs(cls, input_path: str) -> list[str]:
        """
        获得所有路径下的子文件夹路径
        """
        queue_paths = cls.paths_under_archive(input_path, is_file=False)
        if queue_paths == []:
            return []

        # 注意，如果不采用.copy()，会指向同一个地址
        child_folder_paths = queue_paths.copy()
        while True:
            # 通过队列queue_paths的取数和添加来进行BFS
            if len(queue_paths) == 0:
                break
            one_path = queue_paths.pop(0)
            new_child_paths = cls.paths_under_archive(one_path, is_file=False)
            queue_paths += new_child_paths
            child_folder_paths += new_child_paths
        return child_folder_paths

    @classmethod
    def gain_child_file_paths(cls, input_path: str) -> list[str]:
        """
        获得该目录下层层嵌套的所有文件的路径
        """
        folder_paths = cls.gain_child_folder_paths_bfs(input_path)
        # 返回母文件夹下文件路径
        child_file_paths = cls.paths_under_archive(input_path, is_file=True)
        # 返回子文件夹下文件路径
        for each_path in folder_paths:
            file_paths = cls.paths_under_archive(each_path, is_file=True)
            child_file_paths += file_paths
        return child_file_paths

    @classmethod
    def gain_child_certain_type_paths(cls, input_path: str, extension: str = '.py') -> list[str]:
        """
        获得该目录下层层嵌套的所有文件的路径（指定文件类型）
        """
        child_file_paths = cls.gain_child_file_paths(input_path)
        child_files_in_type = list()
        for each_path in child_file_paths:
            each_extends = cls.get_file_extension(each_path)
            if each_extends == extension:
                child_files_in_type.append(each_path)
        return child_files_in_type

    @classmethod
    def gain_child_path_file_pairs(cls, input_path: str) -> dict[str, list[str]]:
        """
        以字典的形式返回所有路径下的子文件名称
        :return: dict[路径, 子文件列表]
        """
        folder_paths = cls.gain_child_folder_paths_dfs(input_path)
        child_path_file_pairs = dict()
        # 返回母文件夹下的文件
        child_path_file_pairs[input_path] = cls.files_under_archive(input_path)
        # 返回子文件夹下的文件路径
        for each_path in folder_paths:
            child_path_file_pairs[each_path] = cls.files_under_archive(each_path)
        return child_path_file_pairs

    @classmethod
    def gain_child_certain_type_path_file_pairs(cls, input_path: str, extension: str = '.xlsx') -> dict[str, list[str]]:
        """
        以字典的形式返回符号文件类型要求的，所有路径下的子文件名称
        如果extension=""，则返回所有文件类型的文件路径
        :return: dict[路径, 子文件列表]
        """
        child_path_file_pairs = cls.gain_child_path_file_pairs(input_path)
        if extension == "":
            return child_path_file_pairs
        
        certain_type_path_file_pairs = dict()
        for each_path in child_path_file_pairs.keys():
            certain_type_path_file_pairs[each_path] = list()
            for each_file in child_path_file_pairs[each_path]:
                each_extension = cls.get_file_extension(each_file)
                if each_extension == extension:
                    certain_type_path_file_pairs[each_path].append(each_file)

            if len(certain_type_path_file_pairs[each_path]) == 0:
                # 删除空列
                certain_type_path_file_pairs.pop(each_path, None)
        return certain_type_path_file_pairs


if __name__ == "__main__":
    input_path = "D:\\Integrated Knowledge Management\\BaiduSyncdisk\\All Knowledge Management(MD)\\Leben Plannung von ZSH"
    encoding = "utf-8"
    fbo = FindChildPaths(encoding)
    fbo.reset_encoding('utf-8')
    folders = fbo.gain_child_folder_paths_bfs(input_path)
    print(folders)