import re

def patt_sub_only_capture_obj(patt, replace_str, old_str):
    """正则表达式sub替换仅限于捕捉内容，而不是整体替换"""
    if patt.search(old_str):
        return patt.sub(lambda x:x.group(0).replace(x.group(1), replace_str), old_str)
    else:
        return old_str

PATT_DEBUG = re.compile(r"DEBUG\s*=\s*(False|True)")
s = 'DEBUG = True\n456'

ttt = patt_sub_only_capture_obj(PATT_DEBUG, 'False', s)

print(ttt)
