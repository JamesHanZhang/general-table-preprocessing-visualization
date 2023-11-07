################# ENUM ##################
from enum import Enum, unique
@unique
class ParamsMode(Enum):
    """
    FROM_SETTING:   1. 通过_params_setting.py来设定参数, 会自动覆盖同名参数表;\n
    FROM_EXISTS:    2. 通过已经存在的resources里的参数文件来确定参数, 如该参数文件不存在则报错;\n
    FROM_BASE:      3. 通过修改resources里已经有的基本参数表BASE_PARAMS_SET来确定新的参数表;\n
    """
    # 通过_params_setting.py来设定参数, 会自动覆盖同名参数表
    FROM_SETTING = 1
    # 通过已经存在的resources里的参数文件来确定参数, 如该参数文件不存在则报错
    FROM_EXISTS = 2
    # 通过修改resources里已经有的基本参数表来确定新的参数表
    FROM_BASE = 3

@unique
class ParamsModeDesc(Enum):
    FROM_SETTING = "1. 通过`_params_setting.py`来设定参数, 会自动覆盖同名参数表;"
    FROM_EXISTS = "2. 通过已经存在的resources里的参数文件来确定参数, 如该参数文件不存在则报错;"
    FROM_BASE = "3. 通过修改resources里已经有的基本参数表BASE_PARAMS_SET来确定新的参数表;"

@unique
class OutputMode(Enum):
    """
    ACTIVATION_MODE 1 <根据激活导出模式>: 采用'output_params_setting.py'中的激活功能判断是否导出对应格式的数据;\n
                        该模式激活几个功能就导出几个文件(激活拆分功能则更多);\n
                        该模式在导出'.sql'文件时, 采用参数'table_name'确定导出的表名及文件名;\n
    EXTENSION_MODE  2 <根据拓展名导出模式>采用导出文件output_file的拓展名(例如'test.xlsx')判断是导出哪种格式数据;\n
                        模式一次仅激活一个导出功能;\n
                        该模式在导出'.sql'文件时, 默认将临时表的表名设置为导出文件的主体名(去掉拓展名);\n
    FREE_MODE       3 <自动模式>, 根据导出的文件名'output_file'是否有拓展名(例如'test.xlsx')来判断采取以上两种模式的哪种模式;\n
                        如导出的文件名没有拓展名, 即只有纯粹的文件名(例如'test'), 则激活<根据激活导出模式>;\n
                        如导出的文件名有拓展名(例如'test.xlsx'), 则激活<根据拓展名导出模式>;\n
    """
    ACTIVATION_MODE = 1
    EXTENSION_MODE = 2
    FREE_MODE = 3

@unique
class OutputModeDesc(Enum):
    ACTIVATION_MODE = "1 <根据激活导出模式>: 采用'output_params_setting.py'中的激活功能判断是否导出对应格式的数据;\n"\
                      "    该模式激活几个功能就导出几个文件(激活拆分功能则更多);\n" \
                      "    该模式在导出'.sql'文件时, 采用参数'table_name'确定导出的表名及文件名;"
    EXTENSION_MODE = "2 <根据拓展名导出模式>采用导出文件output_file的拓展名(例如'test.xlsx')判断是导出哪种格式数据;\n" \
                     "    模式一次仅激活一个导出功能;\n" \
                     "    该模式在导出'.sql'文件时, 默认将临时表的表名设置为导出文件的主体名(去掉拓展名);"
    FREE_MODE = "3 <自动模式>, 根据导出的文件名'output_file'是否有拓展名(例如'test.xlsx')来判断采取以上两种模式的哪种模式;\n" \
                "    如导出的文件名没有拓展名, 即只有纯粹的文件名(例如'test'), 则激活<根据激活导出模式>;\n" \
                "    如导出的文件名有拓展名(例如'test.xlsx'), 则激活<根据拓展名导出模式>;"
    

@unique
class GanttColor(Enum):
    # Gantt Chart Color Bar Type
    # 渐变色
    TIMELINE_GRADIENT = 'Completion_pct'
    FACTORY_GRADIENT = 'Complete'
    # 分开的颜色组
    DIVIDED_COLOR_BAR = 'Resource'

@unique
class DfType(Enum):
    # Column Types for DataFrame
    INT_TYPE = 'int64'
    FLOAT_TYPE = 'float64'
    STRING_TYPE = 'object'
    DATE_TYPE = 'datetime64[ns]'
    BOOLEAN_TYPE = 'bool'