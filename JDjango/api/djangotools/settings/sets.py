from ..common import *
from ..basetools import *

__all__ = [
    'set_configs', # 纯文本解析 settings.py 文件，填充传递过来的数据包
]


def set_configs(setting_path: str, configs)->None:
    """填写 Django 项目 settings.py 的 数据包 configs（纯文本解析版）"""

    with open(setting_path, 'r', encoding='utf-8') as f:
        settings_content = f.read()

    configs['DATABASES'] = eval(get_list_patt_content_contain_code(retools.PATT_DATABASES, settings_content, leftCode='{', rightCode='}')) # 数据库

    if retools.PATT_DEBUG.search(settings_content): temp = retools.PATT_DEBUG.findall(settings_content)[0]
    else: temp = None
    configs['DEBUG'] = convert_bool_str(temp) # 调试状态

    if retools.PATT_LANGUAGE_CODE.search(settings_content): temp = retools.PATT_LANGUAGE_CODE.findall(settings_content)[0]
    else: temp = None
    configs['LANGUAGE_CODE'] = temp # 语言环境

    if retools.PATT_TIME_ZONE.search(settings_content): temp = retools.PATT_TIME_ZONE.findall(settings_content)[0]
    else: temp = None
    configs['TIME_ZONE'] = temp # 时区

    if retools.PATT_USE_I18N.search(settings_content): temp = retools.PATT_USE_I18N.findall(settings_content)[0]
    else: temp = None
    configs['USE_I18N'] = convert_bool_str(temp) # 全局语言设置
    
    if retools.PATT_USE_L10N.search(settings_content): temp = retools.PATT_USE_L10N.findall(settings_content)[0]
    else: temp = None
    configs['USE_L10N'] = convert_bool_str(temp)

    if retools.PATT_USE_TZ.search(settings_content): temp = retools.PATT_USE_TZ.findall(settings_content)[0]
    else: temp = None
    configs['USE_TZ'] = convert_bool_str(temp) # 是否使用标准时区

    if retools.PATT_STATIC_URL.search(settings_content): temp = retools.PATT_STATIC_URL.findall(settings_content)[0]
    else: temp = None
    configs['STATIC_URL'] = temp # 静态文件路径

    if retools.PATT_ALLOWED_HOSTS.search(settings_content): temp = retools.PATT_ALLOWED_HOSTS.findall(settings_content)[0]
    else: temp = None
    configs['ALLOWED_HOSTS'] = eval('[' + temp + ']') # 允许连接ip

    if retools.PATT_X_FRAME_OPTIONS.search(settings_content): temp = retools.PATT_X_FRAME_OPTIONS.findall(settings_content)[0]
    else: temp = None
    configs['X_FRAME_OPTIONS'] = temp # 是否开启iframe

    if retools.PATT_SECRET_KEY.search(settings_content): temp = retools.PATT_SECRET_KEY.findall(settings_content)[0]
    else: temp = None
    configs['SECRET_KEY'] = f"{temp}" # SECRET_KEY

    if retools.PATT_CORS_ORIGIN_ALLOW_ALL.search(settings_content): temp = retools.PATT_CORS_ORIGIN_ALLOW_ALL.findall(settings_content)[0]
    else: temp = None
    configs['CORS_ORIGIN_ALLOW_ALL'] = convert_bool_str(temp) # 跨域

    configs['TEMPLATES'] = eval(get_list_patt_content_contain_code(retools.PATT_TEMPLATES, settings_content)) # 模板设置

    if retools.PATT_ROOT_URLCONF.search(settings_content): temp = retools.PATT_ROOT_URLCONF.findall(settings_content)[0]
    else: temp = None
    configs['ROOT_URLCONF'] = temp # 跟路由路径
