from ..common import *

__all__ = [
    'get_list_patt_content', # 通过正则和括号匹配算法获取列表内容区域（不包含两侧括号）
    'get_list_patt_content_contain_code', # 通过正则和括号匹配算法获取列表内容区域（包含两侧括号）
    'add_oneline_to_listattr', # 利用正则，向列表中加入一行元素
    'add_lines_to_listattr', # 利用正则，向列表中加入多行元素
    'pop_oneline_to_listattr', # 利用正则，从列表中删除一行元素
    'pop_lines_to_listattr', # 利用正则，从列表中删除多行元素
]


def get_list_patt_content(patt, path: str, leftCode: str='[', rightCode: str=']', mode=0, content="")->str:
    """通过正则和括号匹配算法获取列表内容区域（不包含两侧括号）
    
        mode：0表示处理路径，1表示处理数据
    """
    if 0 == mode:
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

def add_oneline_to_listattr(setting_path: str, patt, idata: str, indent: int=4, position:int = -1)->None:
    """向列表变量添加一行"""
    content = get_list_patt_content(patt, setting_path)
    insert_data = " " * indent + f"{idata},\n"
    if -1 == position: # 尾插
        new_content = f"{content}{insert_data}"
    else: # 头插
        new_content = f"\n{insert_data[:-1]}{content}"
    write_file(setting_path, read_file(setting_path).replace(content, new_content))

def add_lines_to_listattr(setting_path: str, patt, idatas: List[str], indent: int=4)->None:
    """向列表变量添加多行"""
    for idata in idatas:
        add_oneline_to_listattr(setting_path, patt, idata, indent)

def pop_oneline_to_listattr(setting_path: str, patt, idata: str, indent: int=4)->None:
    """向settings.py中的列表类型变量删除一指定行"""
    content = get_list_patt_content(patt, setting_path)
    insert_data = " " * indent + f"{idata},\n"
    new_content = content.replace(insert_data, '')
    write_file(setting_path, read_file(setting_path).replace(content, new_content))

def pop_lines_to_listattr(setting_path: str, patt, idatas: List[str], indent: int=4)->None:
    """向settings.py中的列表类型变量删除多指定行"""
    for idata in idatas:
        pop_oneline_to_listattr(setting_path, patt, idata, indent)
