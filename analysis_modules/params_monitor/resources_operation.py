

import json
import io
import os
from os import listdir
from os.path import isfile, join
import time

# self-made modules
# 底层类，尽可能不调用外包，仅以直接调用的方式调用参数，不走包调用
from basic_operation.basic_io_operation import IoMethods
from analysis_modules import default_properties as prop


class ResourcesOperation():
    def __init__(self):
        self.iom = IoMethods('utf-8')
        self.resources_path = prop.RESOURCES_PATH

    def list_resources(self, extension:str='.json') -> list[str]:
        file_list = [file for file in listdir(self.resources_path) if isfile(join(self.resources_path, file))]
        target_list = list()
        for each_file in file_list:
            if self.iom.get_file_extension(each_file) == extension:
                target_list.append(each_file)
        
        file_name_list = []
        for each_file in target_list:
            file_name_list.append(self.iom.get_main_file_name(each_file))
        return file_name_list
    
    @classmethod
    def check_if_params_set_exists(cls, params_set, pop_error:bool=False) -> bool:
        ro = cls()
        params_sets = ro.list_resources()
        if pop_error is False:
            if params_set not in params_sets:
                return False
            return True
        if params_set not in params_sets:
            msg = f"parameters set '{params_set}.json' doesn't exist under the folder resources, so you can't import the parameters directly.\n" \
                  f"参数表'{params_set}.json' 不存在, 请检查输入的参数表名称是否正确."
            print(msg)
            time.sleep(2)
            raise FileNotFoundError(msg)
        return True

    @staticmethod
    def load_cls_as_json(cls: object) -> json:
        cls_json = json.dumps(cls.__dict__)
        return cls_json

    @classmethod
    def read_resource(cls, json_file:str) -> dict[str, dict]:
        ro = cls()
        if json_file[-5:] != ".json":
            json_file += ".json"
        full_path = IoMethods.join_path(ro.resources_path, json_file)
        # 为正常打开json文件，要明确encoding type
        with open(full_path, mode='r', encoding='utf-8') as load_file:
            json_object = json.load(load_file)
        return json_object

    @classmethod
    def store_params_as_json(cls, json_file: str, dict_content: dict) -> None:
        ro = cls()
        if json_file[-5:] != ".json":
            json_file += ".json"
        ro.iom.mkdir_if_no_dir(ro.resources_path)
        full_path = ro.iom.join_path(ro.resources_path, json_file)

        # 防止中文转义为ascii符号，要添加ensure_ascii=False,同时打开文件以encoding='utf-8'打开
        json_object = json.dumps(dict_content, indent=4, ensure_ascii=False)
        with io.open(full_path, mode='w', newline='\n', encoding='utf-8') as output_file:
            output_file.write(json_object)
        return None

    def remove_resources_file(self, json_file: str) -> bool:
        if json_file[-5:] != ".json":
            json_file += ".json"
        full_path = self.iom.join_path(self.resources_path, json_file)
        try:
            os.remove(full_path)
        except (FileNotFoundError):
            pass
        return True


if __name__=="__main__":
    # test
    # test_dict = {
    #     1: [111, 222, 333],
    #     "test": 'nice weather'
    # }
    ro = ResourcesOperation()
    # ro.store_params_as_json('test', test_dict)
    # read_output = ro.read_resource('test')
    # print(read_output)
    #
    # ro.read_resource('test_xxx')
    print(ro.list_resources())
    
    