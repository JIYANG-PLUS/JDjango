from .. common import *
from .. import config as SCONFIGS

__all__ = [
    'get_all_py_path_by_alias', # 根据别名列表筛选文件
]


def get_all_py_path_by_alias(alias: List[str])->List[str]:
    """根据别名列表筛选文件"""
    f_path = SCONFIGS.dirname() # 项目根路径
    
    search_path = os.path.join(f_path, '**', '*')
    objs = glob.glob(search_path, recursive=True)
    
    alias = [os.path.basename(_) for _ in alias] # 只取文件名（功能扩展）

    temp = []
    for _ in objs: # 取所有的 admin.py 及其别名
        if os.path.basename(_) in alias:
            temp.append(_)
    return temp # 当前项目根路径下所有的admin类型源文件路径
