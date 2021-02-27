import os, json, glob, string
from ....tools._tools import *
from ....tools._re import *
from ....tools import environment as env
from ....tools import models as models_env
from ....settings import CONFIG_PATH, TEMPLATE_DIR, COR_MIDDLEWARE
from typing import Dict, List

from ..exceptions import *
from .common import *

__all__ = [
    'get_views_base_func', # 获取未改动的函数视图模板内容
    'get_views_base_class', # 获取未改动的类视图模板内容
    'get_site_header', # 获取后台站点登录名
    'get_site_title', # 获取后台站点网站名
    'get_all_apps_name', # 获取所有的应用程序名
    'get_urlpatterns_content', # 获取urls.py中urlpatterns中括号内部的内容
    'get_app_rooturl_config_by_appname', # 通过app名称获取根路由路径下的路由配置
    'get_models_path_by_appname', # 获取当前app下所有的模型文件路径
    'get_models_by_appname', # 获取当前app下的所有模型
    'get_orm_code', # 获得orm模板批量生成示例

    'judge_in_main_urls', # 判断应用程序是否均在urls.py中注册
]

def get_all_apps_name()->List[str]:
    """获取所有的应用程序名"""
    return get_configs(CONFIG_PATH)['app_names']

def get_views_base_func()->str:
    """获取未改动的函数视图模板内容"""
    return ''.join(get_content('baseFunc.django', concat=['views']))

def get_views_base_class()->str:
    """获取未改动的类视图模板内容"""
    return ''.join(get_content('baseClass.django', concat=['views']))

def get_site_header()->List[str]:
    """获取登录界面名称"""
    options = []
    for _ in get_all_py_path_by_alias(env.getAdminAlias()): # 逐个文件读取判断
        source = ' '.join([t.strip() for t in read_file_list_del_comment(_)])
        options.extend(PATT_HEADER_NAME.findall(source)) # 扣出登录界面名称
    return options

def get_site_title()->List[str]:
    """获取后台标题名称 注释见get_site_header"""
    options = []
    for _ in get_all_py_path_by_alias(env.getAdminAlias()):
        source = ' '.join([t.strip() for t in read_file_list_del_comment(_)])
        options.extend(PATT_TITLE_NAME.findall(source))
    return options

def get_app_rooturl_config_by_appname(appname: str)->str:
    """"通过app名称获取跟路由路径下的路由配置"""
    CONFIG = get_configs(CONFIG_PATH)
    # 获取路由别名
    alias = [os.path.basename(_) for _ in env.getUrlsAlias()]
    assert len(alias) > 0
    # 获取根路由
    root_urlpath = os.path.join(CONFIG['dirname'], CONFIG['project_name'], alias[0]) # 默认取第一个
    urlpatterns = get_urlpatterns_content(root_urlpath).split('\n') # url内容区

    temp_include = appname + '.' + alias[0].split('.')[0]

    patt_name1 = re.compile(r"\((.+?),\s*include\s*\(\s*'" + temp_include + r"'\s*\)\s*\)")
    patt_name2 = re.compile(r'\((.+?),\s*include\s*\(\s*"' + temp_include + r'"\s*\)\s*\)')

    for _ in urlpatterns:
        if patt_name1.search(_):
            return patt_name1.findall(_)[0].strip(string.whitespace + '"\'')
        if patt_name2.search(_):
            return patt_name2.findall(_)[0].strip(string.whitespace + '"\'')

def get_all_need_register_urls(config: Dict[str, object])->List[str]:
    """获取所有注册名（include('demo.urls')）"""
    apps = config['app_names'] # 取所有的app名称
    # 取第一个urls别名，（不带后缀名）
    alias = [os.path.basename(_).split('.')[0] for _ in env.getUrlsAlias()][0] # 仅取文件名
    return [f'{_}.{alias}' for _ in apps] # 将所有的app名拼接上路由文件名（不带后缀名）

def get_models_path_by_appname(appname: str)->List[str]:
    """获取当前app下所有的模型文件路径"""
    APP_PATH = os.path.join(get_configs(CONFIG_PATH)['dirname'], appname) # 路径定位到当前app下
    models_path = []

    if os.path.exists(APP_PATH) and os.path.isdir(APP_PATH):

        pys = glob.glob(os.path.join(APP_PATH, '**', '*.py'), recursive=True) # 先取所有归属当前app下的文件路径
        alias = [os.path.basename(_) for _ in env.getModelsAlias()] # 取所有模型别名（如：models.py）
        models_path.extend([_ for _ in pys if os.path.basename(_) in alias]) # 以别名为依据，过滤所有文件中可能的模型文件

    return models_path

def get_models_by_appname(appname: str)->List[str]:
    """获取当前app下的所有模型"""
    pathModels = get_models_path_by_appname(appname)
    data = []
    
    for path in pathModels:
        data.extend(models_env.get_models_from_modelspy(path))
    
    return data

def get_orm_code(mode='select', *args, **kwargs):
    """获得orm模板批量生成示例"""
    file_name = ''
    mode = mode.lower()
    if 'select' == mode:
        file_name = 'select.html'
    elif 'insert' == mode:
        file_name = 'insert.html'
    elif 'delete' == mode:
        file_name = 'delete.html'
    elif 'update' == mode:
        file_name = 'update.html'
    elif 'field' == mode:
        file_name = 'field.html'
    elif 'aggregate' == mode:
        file_name = 'aggregate.html'
    elif 'tools' == mode:
        file_name = 'tools.html'
    else:
        file_name = 'join.html'
    content = get_content(file_name, concat=['orm'], replace=True, **kwargs)

    return content

def get_model_args_codes(app_name, model_path, model_name):
    """获取模型创建参数"""
    # 待定的功能，看情况维护，暂时不添加到工具中

def judge_in_main_urls()->List[str]:
    """判断是否注册路由（返回未注册的路由）"""
    config = get_configs(CONFIG_PATH)
    root_path = config['dirname'] # Django项目根路径
    project_name = config['project_name'] # 项目名称
    root_urlspy = os.path.join(root_path, project_name, 'urls.py') # 定位项目的主urls.py文件
    urlpatterns_content = get_urlpatterns_content(root_urlspy) # 锁定路由文本区域
    app_urls = get_all_need_register_urls(config)
    return [_ for _ in app_urls if _ not in urlpatterns_content]
