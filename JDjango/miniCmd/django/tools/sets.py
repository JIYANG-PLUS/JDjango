from .common import *

__all__ = [

    'set_site_header', # 设置后台站点登录名
    'set_site_title', # 设置后台站点网站名
    'set_configs', # 填写 Django 项目 settings.py 的 数据包 configs
    
]

def set_site_header(new_name: str, mode: int=0)->None:
    """设置 获取登录界面名称"""
    # mode: 0没有，1仅一个，2多个
    # 删除所有的名称命名处
    alias_paths = get_all_py_path_by_alias(env.getAdminAlias())
    if 2 == mode:
        for _ in alias_paths:
            content = PATT_HEADER_NAME.sub('', read_file(_))
            write_file(_, content)
    # 原地修改
    if 1 == mode:
        for _ in alias_paths:
            t_content = read_file(_)
            if PATT_HEADER_NAME.search(t_content):
                write_file(_, PATT_HEADER_NAME.sub(lambda x:x.group(0).replace(x.group(1), new_name), t_content))
                break
    # 随机插入
    if mode in (0, 2):
        append_content(alias_paths[0], 'renameHeader.django', concat=['admin'], replace=True, header_name=new_name)

def set_site_title(new_name: str, mode: int=0)->None:
    """设置 获取后台标题名称 注释见set_site_header"""
    alias_paths = get_all_py_path_by_alias(env.getAdminAlias())
    if 2 == mode:
        for _ in alias_paths:
            content = PATT_TITLE_NAME.sub('', read_file(_))
            write_file(_, content)
    if 1 == mode:
        for _ in alias_paths:
            t_content = read_file(_)
            if PATT_TITLE_NAME.search(t_content):
                write_file(_, PATT_TITLE_NAME.sub(lambda x:x.group(0).replace(x.group(1), new_name), t_content))
                break
    if mode in (0, 2):
        append_content(alias_paths[0], 'renameTitle.django', concat=['admin'], replace=True, title_name=new_name)

def set_configs(setting_path: str, configs)->None:
    """填写 Django 项目 settings.py 的 数据包 configs（纯文本解析版）"""

    with open(setting_path, 'r', encoding='utf-8') as f:
        settings_content = f.read()

    configs['DATABASES'] = eval(get_list_patt_content_contain_code(PATT_DATABASES, settings_content, leftCode='{', rightCode='}')) # 数据库

    if PATT_DEBUG.search(settings_content): temp = PATT_DEBUG.findall(settings_content)[0]
    else: temp = None
    configs['DEBUG'] = convert_bool_str(temp) # 调试状态

    if PATT_LANGUAGE_CODE.search(settings_content): temp = PATT_LANGUAGE_CODE.findall(settings_content)[0]
    else: temp = None
    configs['LANGUAGE_CODE'] = temp # 语言环境

    if PATT_TIME_ZONE.search(settings_content): temp = PATT_TIME_ZONE.findall(settings_content)[0]
    else: temp = None
    configs['TIME_ZONE'] = temp # 时区

    if PATT_USE_I18N.search(settings_content): temp = PATT_USE_I18N.findall(settings_content)[0]
    else: temp = None
    configs['USE_I18N'] = convert_bool_str(temp) # 全局语言设置
    
    if PATT_USE_L10N.search(settings_content): temp = PATT_USE_L10N.findall(settings_content)[0]
    else: temp = None
    configs['USE_L10N'] = convert_bool_str(temp)

    if PATT_USE_TZ.search(settings_content): temp = PATT_USE_TZ.findall(settings_content)[0]
    else: temp = None
    configs['USE_TZ'] = convert_bool_str(temp) # 是否使用标准时区

    if PATT_STATIC_URL.search(settings_content): temp = PATT_STATIC_URL.findall(settings_content)[0]
    else: temp = None
    configs['STATIC_URL'] = temp # 静态文件路径

    if PATT_ALLOWED_HOSTS.search(settings_content): temp = PATT_ALLOWED_HOSTS.findall(settings_content)[0]
    else: temp = None
    configs['ALLOWED_HOSTS'] = eval('[' + temp + ']') # 允许连接ip

    if PATT_X_FRAME_OPTIONS.search(settings_content): temp = PATT_X_FRAME_OPTIONS.findall(settings_content)[0]
    else: temp = None
    configs['X_FRAME_OPTIONS'] = temp # 是否开启iframe

    if PATT_SECRET_KEY.search(settings_content): temp = PATT_SECRET_KEY.findall(settings_content)[0]
    else: temp = None
    configs['SECRET_KEY'] = f"{temp}" # SECRET_KEY

    if PATT_CORS_ORIGIN_ALLOW_ALL.search(settings_content): temp = PATT_CORS_ORIGIN_ALLOW_ALL.findall(settings_content)[0]
    else: temp = None
    configs['CORS_ORIGIN_ALLOW_ALL'] = convert_bool_str(temp) # 跨域

    configs['TEMPLATES'] = eval(get_list_patt_content_contain_code(PATT_TEMPLATES, settings_content)) # 模板设置

    if PATT_ROOT_URLCONF.search(settings_content): temp = PATT_ROOT_URLCONF.findall(settings_content)[0]
    else: temp = None
    configs['ROOT_URLCONF'] = temp # 跟路由路径
