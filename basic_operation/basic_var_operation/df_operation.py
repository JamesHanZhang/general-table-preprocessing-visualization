
import pandas as pd
import math

def count_sep_num(df :pd.DataFrame, chunksize: int) -> int:
    # 计算最多能根据chunksize分成几个切片
    size = df.index.size
    pieces_count = math.ceil(size / chunksize)
    return pieces_count

def count_exact_sep_num(df :pd.DataFrame, chunksize: int) -> int:
    # 计算能分成几片，有小数点
    size = df.index.size
    pieces_count = size / chunksize
    return pieces_count

def get_nth_chunk_df(df: pd.DataFrame, nth_chunk: int, chunksize: int) -> pd.DataFrame:
    """
    :param df: 数据
    :param nth_chunk: 第几个切片
    :param chunksize: 切片的最大记录条数
    :return: 选择特定的切片
    """
    # df.iloc[0:3,:]涵盖的index=[0,1,2]，df.iloc[3:4,:]涵盖的index=[3]
    # 且df.iloc[500:1000,:]如果index超过500但不足1000，则会把超过500的都截取到
    nth_chunk_df = df.iloc[nth_chunk *chunksize:(nth_chunk +1 ) *chunksize, :]
    return nth_chunk_df

def concat_dfs(*dfs: pd.DataFrame) -> pd.DataFrame:
    # 将多个df按顺序拼接成一个df
    dfs = list(dfs)
    df = dfs.pop(0)
    for each_df in dfs:
        frames = [df, each_df]
        df = pd.concat(frames)
        df = df.reset_index(drop=True)
    return df
    
def concat_dfs_list(dfs_list: list[pd.DataFrame]) -> pd.DataFrame:
    df = pd.concat(dfs_list)
    df = df.reset_index(drop=True)
    return df