from ..common import *
from .. import basetools

__all__ = [
    'get_site_header', # 获取后台站点登录名
    'get_site_title', # 获取后台站点网站名
    'get_admin_register_models', # 获取已经注册的后台应用
]

def get_site_header()->List[str]:
    """获取登录界面名称"""
    options = []
    for _ in basetools.get_all_py_path_by_alias(env.getAdminAlias()): # 逐个文件读取判断
        source = ' '.join([t.strip() for t in read_file_list_del_comment(_)])
        options.extend(retools.PATT_HEADER_NAME.findall(source)) # 扣出登录界面名称
    return options

def get_site_title()->List[str]:
    """获取后台标题名称 注释见get_site_header"""
    options = []
    for _ in basetools.get_all_py_path_by_alias(env.getAdminAlias()):
        source = ' '.join([t.strip() for t in read_file_list_del_comment(_)])
        options.extend(retools.PATT_TITLE_NAME.findall(source))
    return options

def get_admin_register_models()->List[str]:
    """获取已经注册的后台应用"""
    configs = get_configs(CONFIG_PATH)
    apps = configs['app_names'] # 获取所有的app名称
    admin_alias = env.getAdminAlias() # 获取所有的admin.py路径
    models = []
    for app in apps:
        for _ in admin_alias:
            temp_path = os.path.join(configs['dirname'], app, _)
            temp_models = retools.PATT_REGISTER.findall(read_file(temp_path))
            models.extend(temp_models)
    return models
