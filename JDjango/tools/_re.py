import re

# 正则表达式对象
__all__ = [
    # 属性
    'PATT_BASE_DIR',
    'PATT_INSTALLED_APPS',
    'PATT_MIDDLEWARE',
    'PATT_SECRET_KEY',
    'PATT_DEBUG',
    'PATT_ALLOWED_HOSTS',
    'PATT_X_FRAME_OPTIONS',
    'PATT_LANGUAGE_CODE',
    'PATT_TIME_ZONE',
    'PATT_USE_I18N',
    'PATT_USE_L10N',
    'PATT_USE_TZ',
    'PATT_CORS_ORIGIN_ALLOW_ALL',
    'PATT_CHARS',
    'PATT_CHARSNUMBER',
    'PATT_REPLACE',
    'PATT_TITLE_NAME',
    'PATT_HEADER_NAME',
    'PATT_URLPATTERNS',
    'PATT_DAtABASES',
    'PATT_MODEL',
    'PATT_CHARS_REVERSED',
    'PATT_DIGITS_WHOLE',
    'PATT_DIGITS_REVERSED',
    'PATT_CAPTURE_URLSPATH_ARGS',
    'PATT_FUNC_ARGS',
    'PATT_COMMENT',
    # 方法
    'patt_sub_only_capture_obj', # 正则表达式sub替换仅限于捕捉内容，而不是整体替换
    'patt_sub_only_capture_obj_add', # 正则表达式sub替换仅限于捕捉内容，替换后内容为：<原捕捉内容> + add_str 
    'patt_sub_only_capture_obj_obtain_double', # 多个两侧括号属性，保留括号替换
]

PATT_BASE_DIR = re.compile(r'BASE_DIR\s*=\s*os.path.dirname\s*\(\s*os.path.dirname\s*\(\s*os.path.abspath\s*\(\s*__file__\s*\)\s*\)\s*\)')
PATT_INSTALLED_APPS = re.compile(r"(?ms:INSTALLED_APPS\s.*?=\s.*?\[.*?\])")
PATT_MIDDLEWARE = re.compile(r"(?ms:MIDDLEWARE\s.*?=\s.*?\[.*?\])")
PATT_SECRET_KEY = re.compile(r"SECRET_KEY\s*=\s*[\'\"](.*?)[\'\"]")
PATT_DEBUG = re.compile(r"DEBUG\s*=\s*(False|True)")
PATT_ALLOWED_HOSTS = re.compile(r"ALLOWED_HOSTS\s*=\s*\[([\'\"]*.*?[\'\"]*)\]")
PATT_X_FRAME_OPTIONS = re.compile(r"X_FRAME_OPTIONS\s*=\s*'ALLOWALL'")
PATT_LANGUAGE_CODE = re.compile(r"LANGUAGE_CODE\s*=\s*'(.*?)'")
PATT_TIME_ZONE = re.compile(r"TIME_ZONE\s*=\s*'(.*?)'")
PATT_USE_I18N = re.compile(r"USE_I18N\s*=\s*(False|True)")
PATT_USE_L10N = re.compile(r"USE_L10N\s*=\s*(False|True)")
PATT_USE_TZ = re.compile(r"USE_TZ\s*=\s*(False|True)")
PATT_CORS_ORIGIN_ALLOW_ALL = re.compile(r"CORS_ORIGIN_ALLOW_ALL\s*=\s*(False|True)")
PATT_CHARS = re.compile(r'^[a-zA-Z_]*$')
PATT_CHARS_REVERSED = re.compile(r'[^a-zA-Z_]+')
PATT_DIGITS_WHOLE = re.compile(r'^[1-9][0-9]*$')
PATT_DIGITS_REVERSED = re.compile(r'[^0-9]+')
PATT_CHARSNUMBER = re.compile(r'^[a-zA-Z0-9]*$')
PATT_REPLACE = re.compile(r'[$][{](.*?)[}]') # 模板定位替换语法
PATT_TITLE_NAME = re.compile(r'admin.site.site_title\s*=\s*[\"\'](.*?)[\"\']')
PATT_HEADER_NAME = re.compile(r'admin.site.site_header\s*=\s*[\"\'](.*?)[\"\']')
PATT_URLPATTERNS = re.compile(r'(?ms:urlpatterns\s*=\s*\[.*)')
PATT_DAtABASES = re.compile(r'(?ms:DATABASES\s*=\s*\{.*)')
PATT_MODEL = re.compile(r'class\s+(.+?)\(\s*[a-zA-Z0-9]*?[.]*?Model\s*\):') # 定位模型类
PATT_CAPTURE_URLSPATH_ARGS = re.compile(r'<(.+?)>') # 捕捉路由参数信息
PATT_FUNC_ARGS = re.compile(r'def\s+.+?\((.*?)\)')
PATT_COMMENT = re.compile(r'(\s*#.*?$)') # 注释


def patt_sub_only_capture_obj(patt: object, replace_str: str, old_str: str) -> str:
    """正则表达式sub替换仅限于捕捉内容，而不是整体替换"""
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
    """多个两侧括号属性，保留括号替换"""
    replace_str = f'{double_str[0]}{replace_str}{double_str[-1]}'
    if patt.search(old_str):
        return patt.sub(lambda x:x.group(0).replace(double_str[0]+x.group(1)+double_str[-1], replace_str), old_str)
    else:
        return old_str
