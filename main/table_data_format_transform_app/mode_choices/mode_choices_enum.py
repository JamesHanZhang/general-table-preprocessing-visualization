"""
*************************************************************************
***              GENERAL-TABLE-PREPROCESSING-VISUALIZATION            ***
***                           VERSION:2.01                            ***
***                  e-mail: jameshanzhang@foxmail.com                ***
***   link: github.com/JamesHanZhang/general-table-preprocessing-visualization  ***
*************************************************************************
"""

from enum import Enum, unique

@unique
class ModeChoices(Enum):
    # 同数据结构数据源处理
    SAME_STRUCT_MODE = 1
    # 不同数据结构同参数表处理
    SAME_PARAMS_MODE = 2
    # 不同数据结构不同参数表处理
    DIFF_PARAMS_MODE = 3
    # 批量执行参数表
    BATCH_PARAMS_MODE = 4
    
class ModeChoicesDesc(Enum):
    SAME_STRUCT_MODE = "1. <表结构一致模式> 单参数表处理模式, 常用模式, 数据源的表结构一致时采用该模式处理数据转换;"
    SAME_PARAMS_MODE = "2. <结构不一致参数一致模式> 不同表结构数据源转换, 批量模式, 将文件夹下的文件基于同一个参数表分别进行转换;\n" \
                       "    导入的文件名主体默认为导出的文件名主体以及导出的SQL表名;"
    # 不同数据结构不同参数表处理
    DIFF_PARAMS_MODE = "3. <皆不一致模式> 不同表结构数据源采用不同的参数表, 需首先挨个搭建各个数据源对应的参数表, 再批量执行;\n" \
                       "    搭建参数表基于BASE_PARAMS_SET.json表进行修改, 其各个属性的含义与`_params_setting.py`一致;"
    BATCH_PARAMS_MODE = "4. <多参数表执行模式> 输入已存在的不同的参数表名, 直接执行; 如该参数表不存在则报错;"