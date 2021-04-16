from ..common import *
from .. import basetools

__all__ = [
    'get_orm_code', # 获得orm模板批量生成示例
]

def get_orm_code(mode='select', *args, **kwargs):
    """获得orm模板批量生成示例"""
    file_name = ''
    mode = mode.lower()
    if 'select' == mode:
        file_name = 'select.html'
    elif 'insert' == mode:
        file_name = 'insert.html'
    elif 'delete' == mode:
        file_name = 'delete.html'
    elif 'update' == mode:
        file_name = 'update.html'
    elif 'field' == mode:
        file_name = 'field.html'
    elif 'aggregate' == mode:
        file_name = 'aggregate.html'
    elif 'tools' == mode:
        file_name = 'tools.html'
    else:
        file_name = 'join.html'
    content = basetools.get_content(file_name, concat=['orm'], replace=True, **kwargs)
    return content
