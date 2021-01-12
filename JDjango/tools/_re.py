import re

def patt_sub_only_capture_obj(patt, replace_str, old_str):
    """正则表达式sub替换仅限于捕捉内容，而不是整体替换"""
    if patt.search(old_str):
        return patt.sub(lambda x:x.group(0).replace(x.group(1), replace_str), old_str)
    else:
        return old_str

def patt_sub_only_capture_obj_obtain_double(patt, replace_str, old_str, double_str = '[]'):
    """多个两侧括号"""
    replace_str = f'{double_str[0]}{replace_str}{double_str[-1]}'
    if patt.search(old_str):
        return patt.sub(lambda x:x.group(0).replace(double_str[0]+x.group(1)+double_str[-1], replace_str), old_str)
    else:
        return old_str
