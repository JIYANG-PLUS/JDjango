from ._tools import *
import re

PATT_MODEL = re.compile(r'class\s+(.+?)\(\s*[a-zA-Z0-9]*?[.]*?Model\s*\):')

def get_models_from_modelspy(path):
    """从模型文件中读取所有模型"""
    result = []
    for _ in read_file_list(path):
        result.extend(PATT_MODEL.findall(_.strip()))
    return result
