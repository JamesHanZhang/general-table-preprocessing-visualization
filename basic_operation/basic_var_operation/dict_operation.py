"""
*****************************************
***       DATA-FORMAT-ANALYSIS-TOOL   ***
***         AUTHOR: JamesHanZhang     ***
***        jameshanzhang@foxmail.com  ***
*****************************************
"""

def get_dict(**kwargs):
    return kwargs

def reverse_dict(input_dict):
    output_dict = {value: key for key, value in input_dict.items()}
    return output_dict

def merge_dicts(*dicts):
    # 同一个键，按最后一个dict更新
    output_dict = dict()
    for each_dict in dicts:
        output_dict = output_dict | each_dict
    return output_dict