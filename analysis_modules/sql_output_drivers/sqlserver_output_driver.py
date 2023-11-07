
# self-made modules
import analysis_modules.default_properties as prop
from analysis_modules.sql_output_drivers.sql_output_driver import SqlOutputDriver
from analysis_modules.params_monitor import OutputParams

class SqlServerOutputDriver(SqlOutputDriver):
    def __init__(self, output_params: OutputParams, params_set: str=prop.DEFAULT_PARAMS_SET):
        super().__init__(output_params, params_set)
        
        # 不同数据库的从pandas的类型到数据库的类型的转换
        # 需要依据数据库的不同，重写的变量
        self.db_types_format = {
            'category': 'NVARCHAR',
            'object': 'NVARCHAR',
            'int64': 'BIGINT',
            'int32': 'INT',
            'int16': 'SMALLINT',
            'int8': 'SMALLINT',
            'float64': 'FLOAT',
            'float32': 'REAL',
            'bool': 'BIT',
            'datetime64': 'DATETIME2',
            'timedelta64': 'TIME'
        }
    
    def get_date_format_element(self, element, col, col_type):
        """
        需要依据数据库的不同，重写的函数
        如果元素为datetime64的时候，元素在sql里应该怎么写
        """
        if col_type == 'datetime64':
            # 这里可能会因为实际需要需时常改动
            element = f"CONVERT(datetime2, '{element}')"
        elif col_type == 'timedelta64':
            element = f"CONVERT(time, '{element}', 114)"
        return element
    
    def construct_creation_cmd(self, columns: list[str], dtypes: dict[str, type]) -> str:
        """
        需要依据数据库的不同，重写的函数
        根据table_name, table_structure, 各列类型进行重写
        :return: 构建建表语句的内容
        """
        remark_note = f"-- TABLE {self.table_name}: table creation sql command based on database {self.database}\n\n"
        
        line_construct = list()
        for col in columns:
            if str(dtypes[col]) in self.var_list:
                line_construct.append(
                    f"    {col} {self.db_types_format[str(dtypes[col])]}({str(self.table_structure[col])})")
            else:
                line_construct.append(f"    {col} {self.db_types_format[str(dtypes[col])]}")
        line_construct = ',\n'.join(line_construct)
        
        table_creation_sql = f"{remark_note}CREATE TABLE {self.table_name}(\n{line_construct}\n);\n"
        self.log.show_log("[COMPLEX COMMENTS PROBLEM] the comments for sql server is complex, so that the user need to define it himself or herself.")
        return table_creation_sql