from ._tools import *
from ._re import *

def get_models_from_modelspy(path):
    """从模型文件中读取所有模型"""
    result = []
    for _ in read_file_list(path):
        result.extend(PATT_MODEL.findall(_.strip()))
    return result
