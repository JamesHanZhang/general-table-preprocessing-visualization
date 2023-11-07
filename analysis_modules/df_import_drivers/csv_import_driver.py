import pandas as pd
import re
import csv
import shlex
import os
# self-made modules
from analysis_modules.df_import_drivers.df_import_driver import DfImportDriver
from analysis_modules.params_monitor import SysLog, ImportParams

class CsvImportDriver(DfImportDriver):
    def __init__(self, import_params: ImportParams):
        super().__init__(import_params)
        self.input_sep = import_params.csv_import_params.input_sep
        self.character_size = import_params.csv_import_params.character_size
        self.quote_none = import_params.csv_import_params.quote_none
        self.sep_to_sub_multi_char_sep = import_params.csv_import_params.sep_to_sub_multi_char_sep
        self.repl_to_sub_sep = import_params.csv_import_params.repl_to_sub_sep

    def init_csv_import_params(self, input_file="", input_path="", input_encoding="", quote_as_object=None,
                               input_sep="", character_size=0, quote_none:bool=None, sep_to_sub_multi_char_sep="",
                               repl_to_sub_sep:str=None):
        self.init_basic_import_params(input_file, input_path, input_encoding,quote_as_object)
        if input_sep != "":
            self.input_sep = input_sep
        if character_size > 0:
            self.character_size = character_size
        if quote_none is not None and type(quote_none) is bool:
            self.quote_none = quote_none
        if sep_to_sub_multi_char_sep != "":
            self.sep_to_sub_multi_char_sep = sep_to_sub_multi_char_sep
        if repl_to_sub_sep is not None and type(repl_to_sub_sep) is str:
            self.repl_to_sub_sep = repl_to_sub_sep
        
    
    def decide_quote_none(self):
        if self.quote_none is True:
            # 忽视引号作为分隔符，以保证数据完整性
            quoting = csv.QUOTE_NONE
        else:
            # 不忽视引号作为分隔符，是默认值
            quoting = csv.QUOTE_MINIMAL
        return quoting

    def read_columns_from_csv(self, input_path):
        """
        return the columns in csv file.
        """
        with open(input_path, mode='r', encoding=self.input_encoding) as file:
            columns = file.readline()
            columns = columns[:-1]
            columns = columns.split(self.input_sep)
            new_columns = list()
            for each_col in columns:
                new_col = each_col.strip("\"")
                new_col = new_col.strip(" ")
                new_columns.append(new_col)
        return new_columns

    def get_preserves(self, full_input_path):
        """method for getting dict of CSV columns and return it with 'object' type as indicator."""
        new_columns = self.read_columns_from_csv(full_input_path)
        objects = ['object'] * len(new_columns)
        preserves = dict(zip(new_columns, objects))
        return preserves

    def decide_df_dtypes(self, full_input_path) -> dict[str, str]|None:
        preserves = self.get_preserves(full_input_path)
        preserves = self.get_df_dtypes_by_preserves(preserves)
        return preserves

    def split_line_with_quotes(self, line, sep):
        # 去掉换行符
        line = line.strip("\n")
        # 基于双引号作为分隔符补充的拆分
        space_replacement = "$a@c$%sa&"
        quote_replacement = "#@!&dxa&0saw2=&"
        null_replacement = "$*(3$1!$^_@@"
        # 把中间的双引号替换掉
        while True:
            if re.search(r'([^{a}]+)\"+([^{a}]+)'.format(a=sep), line) is not None:
                line = re.sub(r'([^{a}]+)\"([^{a}]+)'.format(a=sep), r'\1{a}\2'.format(a=quote_replacement), line)
            else:
                break
        if line.count("\"") % 2 != 0:
            # 说明有贴单边的双引号，容易引起歧义，需要反馈问题
            # 这种情况下导入为dataframe同样会引发歧义，所以需要存入error_lines的表内做二次处理
            return None

        # 将不带双引号的空选项转为null_replacement，否则shlex.split会把空格直接忽略，以至于跳过空值
        line = sep + line + sep
        new_line = str()
        for i in range(len(line) - 1):
            if line[i] == line[i + 1] and line[i] == sep:
                new_line += line[i] + null_replacement
            else:
                new_line += line[i]
        line = new_line[1:]

        # 将空格替换为复杂字符串，将分隔符替换为空格 - 方便使用shlex
        line = line.replace(' ', space_replacement)
        line = line.replace(sep, ' ')

        elem_list = shlex.split(line)
        res_list = list()
        for elem in elem_list:
            take_sep_back = elem.replace(' ', sep)
            take_space_back = take_sep_back.replace(space_replacement, ' ')
            take_quote_back = take_space_back.replace(quote_replacement, '\"')
            # 将空值换为None
            if take_quote_back == "" or take_quote_back == null_replacement:
                res_list.append(None)
                continue
            res_list.append(take_quote_back)
        return res_list

    def split_line(self, line):
        # quote_none 表示是否将双引号视为内容而非分隔符的补充，True表示视为内容，False表示为分隔符的补充
        if self.quote_none is False:
            field_list = self.split_line_with_quotes(line, self.input_sep)
            return field_list

        field_list = line.split(self.input_sep)
        return field_list

    def direct_raise_parse_error(self, pos: int):
        msg = "[ParseError]: ParseError detected not by read_csv, but by self made method.\n" \
              "Error tokenizing data. C error: EOF inside string starting at row {b}.\n".format(b=str(pos))
        self.log.show_log(msg)
        raise pd.errors.ParserError(msg)

    def pos_reminder(self, pos, msg):
        # 防止等待太久以为程序出了问题
        if pos % self.chunksize == 0:
            print(msg + f" for {str((pos // self.chunksize) +1)} part of data...")

    def raise_parse_error(self, full_input_path):
        # 自主搭建的CSV常无法准确识别column和各行的列数，因此需要验证一下
        # 如果column有5个，而第一行有7个，那么只有第一行的后5个会被录入，且不会报错
        # 这种情况在read_csv中比较常见，因此为了避免这种情况，追求更精确的准确性，创建该函数进行报错
        columns = self.read_columns_from_csv(full_input_path)
        col_num = len(columns)
        with open(full_input_path, mode='r+', encoding=self.input_encoding) as file:
            pos = 0
            while True:
                # 通过指针一条一条地读取
                line = file.readline()
                field_list = self.split_line(line)
                if field_list is None:
                    self.direct_raise_parse_error(pos)
                if len(field_list) != col_num:
                    self.direct_raise_parse_error(pos)
                if not line:
                    break
                # 打个标，免得等的时间太久人会着急
                self.pos_reminder(pos, "[CHECK IF DIRTY DATA EXISTS] process for checking data running")
                pos += 1
        return

    def repl_multi_char_sep(self, line: str) -> str:
        new_line = line.replace(self.sep_to_sub_multi_char_sep, self.repl_to_sub_sep)
        new_line = new_line.replace(self.input_sep, self.sep_to_sub_multi_char_sep)
        return new_line

    def create_file_if_multi_char_sep(self, full_input_path):
        # 将多字符分隔符替换成单字符
        if len(self.input_sep) <= 1:
            return full_input_path

        input_path = os.path.dirname(full_input_path)
        input_file = self.iom.get_main_file_name(full_input_path)
        repl_sep_csv = self.iom.join_path(input_path, input_file+"_repl_sep.csv")
        with open(full_input_path, mode='r+', encoding= self.input_encoding) as file:
            first_line = file.readline()
            new_first_line = self.repl_multi_char_sep(first_line)
            self.iom.store_file(repl_sep_csv, new_first_line, encoding=self.input_encoding, overwrite=True)
            part_lines = ""
            pos = 0
            while True:
                line = file.readline()
                if not line:
                    break

                # 打个标，免得等的时间太久人会着急
                self.pos_reminder(pos, "[REPLACE MULTI-CHAR-SEP WITH SINGLE-CHAR-SEP] replacement running")
                pos += 1

                new_line = self.repl_multi_char_sep(line)
                part_lines+=new_line
                if len(part_lines) > self.character_size:
                    self.iom.store_file(repl_sep_csv, part_lines, encoding=self.input_encoding, overwrite=False)
                    part_lines = ""
            if len(part_lines) != 0:
                self.iom.store_file(repl_sep_csv, part_lines, encoding=self.input_encoding, overwrite=False)

        self.log.show_log(f"[REPLACE MULTI SEP FOR CSV] when facing multi-char as sep for csv reading, "
                          f"the sep must firstly be replaced with one char sep, then it can be loaded as dataframe normally.\n"
                          f"[NEW CSV FOR SEP REPLACEMENT] new csv {repl_sep_csv} created for loading csv.")
        # 既然已经替换了分隔符，那么整体分隔符也要变
        self.input_sep = self.sep_to_sub_multi_char_sep
        return repl_sep_csv


    @SysLog().direct_show_log("[ERROR LINES EXTRACTION] error lines and correct lines are separated into 2 files for further reading.")
    def sep_out_error_lines(self, full_input_path, reason) -> str:
        """
        debug error e.g.
        pandas.errors.ParserError: Error tokenizing data. C error: Expected 66 fields in line 348, saw 68
        pandas.errors.ParserError: Error tokenizing data. C error: EOF inside string starting at row 39.
        出现问题的集中到error_csv
        没问题的集中到del_error_csv
        """
        # 将错误的行保存进导出目录下，以便统一处理
        columns = self.read_columns_from_csv(full_input_path)
        col_num = len(columns)
        input_path = os.path.dirname(full_input_path)
        input_file = self.iom.get_main_file_name(full_input_path)
        error_csv = "{a}_error_lines.csv".format(a=self.iom.join_path(input_path,input_file))
        del_error_csv = "{a}_originalcsv(error_deleted).csv".format(a=self.iom.join_path(input_path,input_file))

        with open(full_input_path, mode= 'r+', encoding = self.input_encoding) as file:
            first_line = file.readline()
            self.iom.store_file(error_csv, first_line, encoding=self.input_encoding, overwrite=True)
            # 保存不带脏数据的副本
            self.iom.store_file(del_error_csv, first_line, encoding=self.input_encoding, overwrite=True)

            part_error_lines = ""
            part_correct_lines = ""
            error_mark = False
            pos = 0
            while True:
                # 直接进入下一条
                # 通过指针一条一条地读取，返回的行末尾自带一个换行符
                line = file.readline()
                # 最后空了就停止循环
                if not line:
                    print("\nthe process for storing csv file without error lines is finished.\n"
                          "and the process file was loaded into the processing and deleted already.\n")
                    break

                # 打个标，免得等的时间太久人会着急
                self.pos_reminder(pos, "[SEPARATE ERROR LINES OUT OF CORRECT LINES] separation running")
                pos += 1

                field_list = self.split_line(line)

                # 说明出现EOF错误问题，直接保存到error lines
                if field_list is None:
                    part_error_lines += line

                # 如果字段数不匹配，则保存到error lines
                else:
                    field_num = len(field_list)
                    if field_num != col_num:
                        part_error_lines += line

                    # 如果字段数匹配，且不是头一行，则保存到副本
                    if field_num == col_num:
                        part_correct_lines += line

                if len(part_error_lines) != 0:
                    error_mark = True

                if len(part_error_lines) > self.character_size:
                    self.iom.store_file(error_csv, part_error_lines, encoding=self.input_encoding, overwrite=False)
                    part_error_lines = ""
                if len(part_correct_lines) > self.character_size:
                    self.iom.store_file(del_error_csv, part_correct_lines, encoding=self.input_encoding, overwrite=False)
                    part_correct_lines = ""
            # 循环结束后的剩余的部分
            if len(part_error_lines) != 0:
                self.iom.store_file(error_csv, part_error_lines, encoding=self.input_encoding, overwrite=False)
            if len(part_correct_lines) != 0:
                self.iom.store_file(del_error_csv, part_correct_lines, encoding=self.input_encoding, overwrite=False)

        if error_mark is False:
            self.iom.remove_file(error_csv)
            self.iom.remove_file(del_error_csv)
            del_error_csv = full_input_path
        else:
            # 保存错误
            msg = "[ParserError]: {a} \n" \
                  "And the error lines weren't processed.\n" \
                  "Those error lines were stored as {b}.".format(
                a=str(reason), b=error_csv)
            self.log.show_log(msg)
        return del_error_csv

    def init_csv_reader_params(self, input_file="", input_path="", input_encoding="", quote_as_object=None,
                               input_sep="", character_size=0, quote_none:bool=None, sep_to_sub_multi_char_sep="",
                               repl_to_sub_sep:str=None) -> str:
        # 更新参数表
        self.init_csv_import_params(input_file=input_file,input_path=input_path,input_sep=input_sep,
                                    input_encoding=input_encoding, quote_as_object=quote_as_object,
                                    character_size=character_size, quote_none=quote_none,
                                    sep_to_sub_multi_char_sep=sep_to_sub_multi_char_sep,
                                    repl_to_sub_sep=repl_to_sub_sep)

        full_input_path = self.iom.join_path(self.input_path, self.input_file)
        self.iom.check_if_file_exists(full_input_path)
        # 如果没输入input_encoding，则开启自动检测
        self.input_encoding = self.get_import_encoding(full_input_path, self.input_encoding)

        # 通过quote_as_object判断，是否把所有类型转为object再次进行读取，以保证得到完整数据
        self.preserves = self.decide_df_dtypes(full_input_path)
        # 判断是否严格判断引号为分隔符的一部分(贴近分隔符的时候)，还是视为数据内容录入
        self.quoting = self.decide_quote_none()

        try:
            # 第一行必须为准确的列数，否则会默认识别为后半部分符合HEADER列数要求的部分数据，然后后面凡是没有的则包None，就错误了，所以这里引入更敏感的parser_error发觉方法
            self.raise_parse_error(full_input_path)
        except (pd.errors.ParserError) as reason:
            # 保存无错集到del_error_csv
            full_input_path = self.sep_out_error_lines(full_input_path, reason)
        full_input_path = self.create_file_if_multi_char_sep(full_input_path)

        return full_input_path


    @SysLog().calculate_cost_time("<import from csv>")
    def fully_import_csv(self, input_file="", input_path="", input_encoding="", quote_as_object=None,
                               input_sep="", character_size=0, quote_none:bool=None, sep_to_sub_multi_char_sep="",
                               repl_to_sub_sep:str=None) -> pd.DataFrame:
        # 保证了所有参数都可修改
        full_input_path = self.init_csv_reader_params(input_file=input_file,input_path=input_path,input_sep=input_sep,
                                    input_encoding=input_encoding, quote_as_object=quote_as_object,
                                    character_size=character_size, quote_none=quote_none,
                                    sep_to_sub_multi_char_sep=sep_to_sub_multi_char_sep,
                                    repl_to_sub_sep=repl_to_sub_sep)
        
        df = pd.read_csv(full_input_path, sep=self.input_sep, encoding=self.input_encoding, dtype=self.preserves,
                         quoting=self.quoting, on_bad_lines='warn')
        msg = "[IMPORT CSV]: data from {a} is fully imported.".format(a=full_input_path)
        self.log.show_log(msg)
        return df

    @SysLog().calculate_cost_time("<csv reading generator created>")
    def circular_import_csv(self, input_file="", input_path="", input_encoding="", quote_as_object=None,
                               input_sep="", character_size=0, quote_none:bool=None, sep_to_sub_multi_char_sep="",
                               repl_to_sub_sep:str=None):
        # 保证了所有参数都可修改
        full_input_path = self.init_csv_reader_params(input_file=input_file,input_path=input_path,input_sep=input_sep,
                                    input_encoding=input_encoding, quote_as_object=quote_as_object,
                                    character_size=character_size, quote_none=quote_none,
                                    sep_to_sub_multi_char_sep=sep_to_sub_multi_char_sep,
                                    repl_to_sub_sep=repl_to_sub_sep)
        
        # generate the generator of csv reading method for importing big csv
        chunk_reader = pd.read_csv(full_input_path, sep=self.input_sep, encoding=self.input_encoding,
                                   chunksize=self.chunksize, dtype=self.preserves, quoting=self.quoting,
                                   on_bad_lines='warn')
        msg = f"[IMPORT CSV]: data from {full_input_path} is imported as reader generator for " \
              f"circular import in chunk size {str(self.chunksize)}."
        self.log.show_log(msg)
        return chunk_reader