import os, json, glob, string
from ....tools._tools import *
from ....tools._re import *
from ....tools import environment as env
from ....tools import models as models_env
from ....settings import *
from typing import Dict, List
from . import config as SCONFIGS

from ..exceptions import *

def django_file_path(file_name: str, concat: List[str]=None)->str:
    """补全模板路径"""
    # 这里的concat用于弥补中间的残缺路径（因为文件可能分类在不同的文件夹下，但均使用同一个根目录）
    if None == concat:
        concat = []
    return os.path.join(TEMPLATE_DIR, *concat, file_name) # 模板路径

def read_file_lists(r_path: str, *args, **kwargs)->List[str]:
    """列表式读取文件"""
    with open(r_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if 'replace' in kwargs and kwargs['replace']: # 替换开启
        lines = [PATT_REPLACE.sub(lambda x:kwargs[x.group(1)], _) for _ in lines]
    return lines

def get_content(file_name: str, *args, **kwargs)->List[str]:
    """获取规则替换后的文件列表"""
    return read_file_lists(django_file_path(file_name, concat=kwargs.get('concat')), *args, **kwargs)

def append_content(path: str, name: str, *args, **kwargs)->None:
    """向一个已存在的文本末尾添加另一个文本的规则替换内容"""
    # 调用方式：append_content(alias_paths[0], 'renameHeader.django', concat=['admin'], replace=True, model_name=k, site_name=site_name)
    content = get_content(name, *args, **kwargs)
    append_file(path, content)

def get_list_patt_content(patt, path: str, leftCode: str='[', rightCode: str=']')->str:
    """通过正则和括号匹配算法获取列表内容区域"""
    content = read_file(path)
    obj = patt.search(content)
    if obj:
        complex_content = patt.findall(content)[0]
        return cut_content_by_doublecode(complex_content, leftCode=leftCode, rightCode=rightCode)
    else:
        return ''

def get_list_patt_content_contain_code(patt, content: str, leftCode: str='[', rightCode: str=']')->str:
    """通过正则和括号匹配算法获取列表内容区域（包含两侧括号）"""
    obj = patt.search(content)
    if obj:
        complex_content = patt.findall(content)[0]
        return leftCode + cut_content_by_doublecode(complex_content, leftCode=leftCode, rightCode=rightCode) + rightCode
    else:
        return leftCode + rightCode

def get_django_settings_path()->str:
    """获取Django路径下的settings.py的路径"""
    configs = get_configs(CONFIG_PATH)
    DIRNAME = configs["dirname"]
    DIRSETTINGS = os.path.join(DIRNAME, configs['project_name'], 'settings.py')
    return DIRSETTINGS

def get_all_py_path_by_alias(alias: List[str])->List[str]:
    """根据别名筛选文件"""
    f_path = SCONFIGS.dirname # 项目根路径
    
    search_path = os.path.join(f_path, '**', '*')
    objs = glob.glob(search_path, recursive=True)
    
    alias = [os.path.basename(_) for _ in alias] # 只取文件名（功能扩展）

    temp = []
    for _ in objs: # 取所有的 admin.py 及其别名
        if os.path.basename(_) in alias:
            temp.append(_)
    return temp # 当前项目根路径下所有的admin类型源文件路径

