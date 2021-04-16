def patt_sub_only_capture_obj(patt: object, replace_str: str, old_str: str) -> str:
    """正则表达式sub替换仅限于捕捉内容，而不是整体替换"""
    if not isinstance(replace_str, str):
        replace_str = str(replace_str)
    if patt.search(old_str):
        return patt.sub(lambda x:x.group(0).replace(x.group(1), replace_str), old_str)
    else:
        return old_str

def patt_sub_only_capture_obj_add(patt: object, add_str: str, old_str: str) -> str:
    """正则表达式sub替换仅限于捕捉内容，替换后内容为：<原捕捉内容> + add_str """
    if patt.search(old_str):
        return patt.sub(lambda x:x.group(0).replace(x.group(1), x.group(1)+add_str), old_str)
    else:
        return old_str

def patt_sub_only_capture_obj_obtain_double(patt: object, replace_str: str, old_str: str, double_str: str='[]') -> str:
    """多个两侧括号属性，包含括号在内进行替换"""
    replace_str = f'{double_str[0]}{replace_str}{double_str[-1]}'
    if patt.search(old_str):
        return patt.sub(lambda x:x.group(0).replace(double_str[0]+x.group(1)+double_str[-1], replace_str), old_str)
    else:
        return old_str
