
from sqlite3 import connect
import pandas as pd
from analysis_modules.params_monitor import SysLog

class SqlProcessing:
    def __init__(self):
        self.conn = connect(':memory:')

    def init_table(self, df, table_name):
        df.to_sql(table_name, self.conn)
        return True

    def exe_query(self, query):
        # example: query = "SELECT * FROM test"
        result = pd.read_sql(query, self.conn)
        return result

    @SysLog().direct_show_log("[SORT ORDER]sort the order of the dataframe.")
    def sort_df(self, table_name, order_attrs: list[tuple[str, str]]) -> pd.DataFrame:
        """
        :param order_attrs: tuple inside must be like (attr_name, 'ASC') or (attr_name, 'DESC')
        """
        # 校验
        requirement = ['ASC', 'DESC', 'asc', 'desc']
        for each in order_attrs:
            if each[1] not in requirement:
                raise ValueError(f"the second part of the tuple must be chosen from list {str(requirement)}")
        # 执行
        order_part = ", ".join([f"{str(order_attr[0])} {str(order_attr[1])}" for order_attr in order_attrs])
        query = f"SELECT * FROM {table_name} ORDER BY {order_part};"
        df = self.exe_query(query)
        return df
