

import datetime
from functools import wraps
import os
# self made modules
# 底层类，尽可能不调用外包，仅以直接调用的方式调用参数，不走包调用
from analysis_modules import default_properties as prop


class SysLog:
    def __init__(self):
        self.log_path = prop.SYS_LOG_PATH
        self.time_zone = prop.TIME_ZONE
        self.start_words = prop.START_WORDS

        # decide sys_log_file path
        today = datetime.date.today()
        self.sys_log_file = "data_analysis_log_{0}.log".format(today)
        self.sys_log_path = self.join_path(self.log_path, self.sys_log_file)
        self.mk_log_dir_if_no_dir()

    @staticmethod
    def join_path(mother_path, child_path):
        if child_path != "" and child_path[0] in ['/','\\']:
            child_path = child_path[1:]
        full_path = os.path.join(mother_path, child_path)
        full_path = os.path.normpath(full_path)
        return full_path
    def get_time_slot(self):
        current_time = datetime.datetime.now()
        str_time = f"{self.time_zone}:{current_time}\n"
        return str_time

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
    def path_mkdir(path):
        # 创建路径
        try:
            os.makedirs(path)
        except FileExistsError as reason:
            pass
        finally:
            return path

    def mk_log_dir_if_no_dir(self):
        # 如果没有log的文件夹，则创建log的文件夹
        if_exists = self.check_if_path_exists(self.log_path,pop_error=False)
        if if_exists is False:
            self.path_mkdir(self.log_path)
        return

    @classmethod
    def write_log(cls, log_content) -> str:
        # 修饰符classmethod将方法转静态类后需要内部实例化，方可正常调用类内部的self数据
        log = cls()
        now = log.get_time_slot()
        content = now + str(log_content) + "\n\n"
        with open(log.sys_log_path, mode='a+', encoding='utf-8') as f:
            f.write(content)
        return content

    @classmethod
    def show_log(cls, log_content) -> None:
        content = cls.write_log(log_content)
        print(content)
        return

    @classmethod
    def show_construct_log(cls, title: str, construct_: dict) -> None:
        log = cls()
        now = log.get_time_slot()
        list_content = list()
        content = f"{now}{title}: \n" \
                  f"    | original column | target value |\n" \
                  f"    | --------------- | ------------- |"
        list_content.append(content)
        for key in construct_.keys():
            list_content.append(f"    |    '{key}'    |    '{construct_[key]}'    |")
        content = '\n'.join(list_content) + "\n"
        f = open(log.sys_log_path, mode='a+', encoding='utf-8')
        f.write(content)
        f.close()
        print(content)
        return

    def start_logging(self, func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            content = self.start_words
            with open(self.sys_log_path, mode='a+', encoding = 'utf-8') as f:
                f.write(content)
            print(content)
            return func(*args,**kwargs)
        return wrapped_func

    def direct_write_log(self, log_content):
        # 只写入Log,不展示
        def logging_decorator(func):
            @wraps(func)
            def wrapped_func(*args, **kwargs):
                self.write_log(log_content)
                return func(*args, **kwargs)
            return wrapped_func
        return logging_decorator

    def direct_show_log(self, log_content):
        # 既写入log也展示
        def logging_decorator(func):
            @wraps(func)
            def wrapped_func(*args, **kwargs):
                self.show_log(log_content)
                return func(*args, **kwargs)
            return wrapped_func
        return logging_decorator

    @classmethod
    def get_cost_time(cls, start = True, start_time=None):
        if start is True:
            start_time = datetime.datetime.now()
            return start_time
        else:
            end_time = datetime.datetime.now()
            cost_time = end_time - start_time
            return cost_time

    def calculate_cost_time(self, title="itself"):
        def logging_decorator(func):
            @wraps(func)
            def wrapped_func(*args, **kwargs):
                start_time = self.get_cost_time()
                result = func(*args, **kwargs)
                cost_time = self.get_cost_time(start=False, start_time=start_time)
                msg = f"[COST TIME] the program {title} costed time: {cost_time}"
                self.show_log(msg)
                return result
            return wrapped_func
        return logging_decorator


@SysLog().start_logging
@SysLog().direct_show_log(log_content="***************************************************\n" \
          "[PROGRAM STARTS]: program starts...")
def start_program():
    # 程序启动时候调用
    start_time = SysLog.get_cost_time(start=True)
    return start_time

def end_program(start_time):
    # 程序结束时候调用
    cost_time = SysLog.get_cost_time(start=False, start_time=start_time)
    msg = f"[THE END]: The data analysis process is successfully finished.\n" \
          f"[COST TIME]: The whole process costed time: {cost_time}\n" \
          f"***************************************************\n\n\n"
    SysLog.show_log(msg)
    return cost_time

if __name__ == '__main__':
    start_time = start_program()
    end_program(start_time)
