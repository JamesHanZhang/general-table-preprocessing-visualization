
# 类型转换时不识别np.nan，即用此替代np.nan
REPLACE_NAN = -9999999999999999

# NULL数据类型
# 原始NULL数据列表
ORIGINAL_NULL_LIST=['nan','NaN','None','none','NULL','null','Null','NaT','']
# 调用的NULL数据列表
NULL_LIST=list(set(ORIGINAL_NULL_LIST + [REPLACE_NAN, str(REPLACE_NAN)]))

