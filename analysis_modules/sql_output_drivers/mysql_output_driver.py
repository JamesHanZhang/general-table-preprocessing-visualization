# self-made modules
import analysis_modules.default_properties as prop
from analysis_modules.sql_output_drivers.sql_output_driver import SqlOutputDriver
from analysis_modules.params_monitor import OutputParams


class MySqlOutputDriver(SqlOutputDriver):
    def __init__(self, output_params: OutputParams, params_set: str=prop.DEFAULT_PARAMS_SET):
        super().__init__(output_params, params_set)
        
        # 不同数据库的从pandas的类型到数据库的类型的转换
        # 需要依据数据库的不同，重写的变量
        self.db_types_format = {
            'category': 'VARCHAR',
            'object': 'VARCHAR',
            'int64': 'INT',
            'int32': 'INT',
            'int16': 'INT',
            'int8': 'INT',
            'float64': 'DOUBLE',
            'float32': 'DOUBLE',
            'bool': 'BOOL',
            'datetime64': 'DATETIME',
            'timedelta64': 'VARCHAR'
        }
    
    def get_date_format_element(self, element, col, col_type):
        """
        需要依据数据库的不同，重写的函数
        如果元素为datetime64的时候，元素在sql里应该怎么写
        """
        if col_type == 'datetime64':
            # 这里可能会因为实际需要需时常改动
            element = f"STR_TO_DATE('{element}', '%Y-%m-%d %H:%i:%S')"
        elif col_type == 'timedelta64':
            element = f"\'{str(element)}\'"
        return element
    
    def construct_creation_cmd(self, columns: list[str], dtypes: dict[str, type]) -> str:
        """
        需要依据数据库的不同，重写的函数
        根据table_name, table_structure, 各列类型进行重写
        :return: 构建建表语句的内容
        """
        remark_note = f"-- TABLE {self.table_name}: table creation sql command based on database {self.database}\n\n"
        
        line_construct = list()
        var_list = self.var_list + ['timedelta64']
        for pos in range(len(columns)):
            col = columns[pos]
            if str(dtypes[col]) in var_list:
                line_construct.append(
                    f"    {col} {self.db_types_format[str(dtypes[col])]}({str(self.table_structure[col])})")
            else:
                line_construct.append(f"    {col} {self.db_types_format[str(dtypes[col])]}")
            
            try:
                # 添加注释
                line_construct[pos] += f" COMMENT '{self.column_comments[col]}'"
            except (KeyError):
                continue
                
        line_construct = ',\n'.join(line_construct)
        
        table_comment = ""
        if self.table_comment != "":
            table_comment = f" COMMENT '{self.table_comment}'"
        
        table_creation_sql = f"{remark_note}CREATE TABLE {self.table_name}(\n{line_construct}\n){table_comment};\n"
        return table_creation_sql