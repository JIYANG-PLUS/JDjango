from ..common import *

__all__ = [
    'convert_bool_str', # 将布尔值的字符串转为True、False 或 None
]


def convert_bool_str(b_str: str)->Any:
    """将布尔值的字符串转为True、False 或 None"""
    if 'True' == b_str:
        return True
    elif 'False' == b_str:
        return False
    else:
        return None
