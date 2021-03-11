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

def set_configs(setting_path: str, configs: Dict[str, object], *args)->None:
    """填写 Django 项目 settings.py 的 数据包 configs"""

    settings = {}

    # 这里修改为直接从文本解析，摆脱对环境的依赖
    with open(setting_path, 'r', encoding='utf-8') as f:
        settings_content = f.read()

    ### 思路一：直接一个一个匹配

    # get_list_patt_content_contain_code(PATT_DATABASES, settings_content, leftCode='{', rightCode='}')





    with open(setting_path, 'r', encoding='utf-8') as f:
        text = PATT_BASE_DIR.sub('', f.read())
        exec(f"BASE_DIR = r'{args[0]}'", {}, settings)
        exec(text, {}, settings)

    configs['DATABASES'] = settings.get('DATABASES') # 数据库
    configs['DEBUG'] = settings.get("DEBUG") # 调试状态
    configs['LANGUAGE_CODE'] = settings.get("LANGUAGE_CODE") # 语言环境
    configs['TIME_ZONE'] = settings.get("TIME_ZONE") # 时区
    configs['USE_I18N'] = settings.get("USE_I18N") # 全局语言设置
    configs['USE_L10N'] = settings.get("USE_L10N")
    configs['USE_TZ'] = settings.get("USE_TZ") # 是否使用标准时区
    configs['STATIC_URL'] = settings.get("STATIC_URL") # 静态文件路径
    configs['ALLOWED_HOSTS'] = settings.get("ALLOWED_HOSTS") # 允许连接ip
    configs['X_FRAME_OPTIONS'] = settings.get("X_FRAME_OPTIONS") # 是否开启iframe
    configs['SECRET_KEY'] = settings.get("SECRET_KEY") # SECRET_KEY
    configs['CORS_ORIGIN_ALLOW_ALL'] = settings.get("CORS_ORIGIN_ALLOW_ALL") # 跨域
    temp_templates_app = settings.get("TEMPLATES")
    if temp_templates_app and len(temp_templates_app) > 0:
        try:
            configs['TEMPLATES_APP_DIRS'] = temp_templates_app[0]['APP_DIRS'] # 是否开启应用程序模板文件路径
            configs['TEMPLATES_DIRS'] = temp_templates_app[0]['DIRS'] # 默认模板路径
        except:
            configs['TEMPLATES_APP_DIRS'] = None
            configs['TEMPLATES_DIRS'] = None # 默认模板路径
    else:
        configs['TEMPLATES_APP_DIRS'] = None
        configs['TEMPLATES_DIRS'] = None # 默认模板路径
