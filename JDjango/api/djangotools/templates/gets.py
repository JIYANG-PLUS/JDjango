from ..common import *
from ..basetools import *

__all__ = [
    'get_views_base_func', # 获取未改动的函数视图模板内容
    'get_views_base_class', # 获取未改动的类视图模板内容
]

def get_views_base_func()->str:
    """获取未改动的函数视图模板内容"""
    return ''.join(get_content('baseFunc.django', concat=['views']))

def get_views_base_class()->str:
    """获取未改动的类视图模板内容"""
    return ''.join(get_content('baseClass.django', concat=['views']))
