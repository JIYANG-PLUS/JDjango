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

    'startproject', # 新建项目
    'startapp', # 新建应用程序
    'write_admin_base', # 创建最基本的后台管理中心
    'fix_urls', # 修复路由
    'refresh_config', # 更新配置文件config.json
    'update_settings_DTATBASES', # 数据库引擎更换
    'add_oneline_to_listattr', # 利用正则，向列表中加入一组元素
    'pop_oneline_to_listattr', # 利用正则，从列表中删除一组元素
    
]


def startproject(path: str, project_name: str)->None:
    """新建项目"""
    if PATT_CHARSNUMBER.match(project_name) and not os.path.exists(os.path.join(path, project_name)):
        """project_name"""
        os.mkdir(os.path.join(path, project_name))

        path = os.path.join(path, project_name)
        os.mkdir(os.path.join(path, project_name))

        PDir = os.path.join(path, project_name)
        new_file(os.path.join(PDir, '__init__.py'))
        new_file(os.path.join(PDir, 'urls.py'), content=get_content('urls.django', concat=['project']))
        new_file(os.path.join(PDir, 'asgi.py'), content=get_content('asgi.django', concat=['project'], replace=True, project_name=project_name))
        new_file(os.path.join(PDir, 'wsgi.py'), content=get_content('wsgi.django', concat=['project'], replace=True, project_name=project_name))
        new_file(os.path.join(PDir, 'settings.py'), content=get_content('settings.django', concat=['project'], replace=True, project_name=project_name))
        
        """templates"""
        # os.mkdir(os.path.join(path, 'templates'))
        # os.mkdir(os.path.join(path, 'templates', 'includes'))
        # new_file(os.path.join(path, 'templates', 'base.html'), content=get_content('baseHtml.django'))

        """static"""
        # os.mkdir(os.path.join(path, 'static'))
        # os.mkdir(os.path.join(path, 'static', 'js'))
        # os.mkdir(os.path.join(path, 'static', 'img'))
        # os.mkdir(os.path.join(path, 'static', 'css'))

        """manage.py"""
        new_file(os.path.join(path, 'manage.py'), content=get_content('manage.django', concat=['project'], replace=True, project_name=project_name))

        return 0
    else:
        return 1

def startapp(app_name: str)->None:
    """新建应用程序"""
    configs = get_configs(CONFIG_PATH)
    PROJECT_BASE_DIR = configs['dirname']
    if PATT_CHARSNUMBER.match(app_name) and not os.path.exists(os.path.join(PROJECT_BASE_DIR, app_name)):
        """""""""main"""
        """"""
        os.mkdir(os.path.join(PROJECT_BASE_DIR, app_name))
        APP_DIR = os.path.join(PROJECT_BASE_DIR, app_name)
        new_file(os.path.join(APP_DIR, '__init__.py'))
        new_file(os.path.join(APP_DIR, 'admin.py'), content=get_content('admin.django'))
        new_file(os.path.join(APP_DIR, 'apps.py'), content=get_content('apps.django', replace=True, app_name=app_name))
        new_file(os.path.join(APP_DIR, 'forms.py'), content=get_content('forms.django'))
        new_file(os.path.join(APP_DIR, 'models.py'), content=get_content('models.django'))
        new_file(os.path.join(APP_DIR, 'controller.py'), content=get_content('controller.django'))
        new_file(os.path.join(APP_DIR, 'tests.py'), content=get_content('tests.django'))
        new_file(os.path.join(APP_DIR, 'urls.py'), content=get_content('urls.django', replace=True, app_name=app_name))
        new_file(os.path.join(APP_DIR, 'views.py'), content=get_content('views.django'))
        """"""
        """""""""templates"""
        """"""
        # os.mkdir(os.path.join(APP_DIR, 'templates'))
        # os.mkdir(os.path.join(APP_DIR, 'templates', app_name))
        # os.mkdir(os.path.join(APP_DIR, 'templates', app_name, 'includes'))
        # TEMP_DIR = os.path.join(APP_DIR, 'templates', app_name)
        # new_file(os.path.join(TEMP_DIR, 'base.html'), content=get_content('baseHtml.django'))
        # new_file(os.path.join(TEMP_DIR, 'includes', 'paginator.html'), content=get_content('paginator.django'))
        """"""
        """""""""static"""
        """"""
        # os.mkdir(os.path.join(APP_DIR, 'static'))
        # os.mkdir(os.path.join(APP_DIR, 'static', app_name))
        # os.mkdir(os.path.join(APP_DIR, 'static', app_name, 'js'))
        # os.mkdir(os.path.join(APP_DIR, 'static', app_name, 'img'))
        # os.mkdir(os.path.join(APP_DIR, 'static', app_name, 'css'))
        """"""
        """""""""templatetags"""
        """"""
        # os.mkdir(os.path.join(APP_DIR, 'templatetags'))
        # new_file(os.path.join(APP_DIR, 'templatetags', '__init__.py'))
        # new_file(os.path.join(APP_DIR, 'templatetags', 'filter.py'), content=get_content('filter.django'))
        """"""
        """""""""migrations"""
        """"""
        os.mkdir(os.path.join(APP_DIR, 'migrations'))
        new_file(os.path.join(APP_DIR, 'migrations', '__init__.py'))
        """"""
        return 0
    else:
        return 1

def write_admin_base(path: str, importData: Dict[str, List[str]])->None:
    """管理中心后台简单注册"""
    for k, v in importData.items():
        for site_name in v:
            append_content(path, 'base.django', concat=['admin'], replace=True, model_name=k, site_name=site_name)

def update_settings_DTATBASES(db_type: str, *args, **kwargs)->None:
    """更新数据库引擎"""
    if db_type not in ('sqlite', 'mysql',):
        raise UnsupportDatabaseException('暂不支持的数据库引擎')

    if 'mysql' == db_type:
        DB_TYPE_NAME = 'mysql.django'
    elif 'sqlite' == db_type:
        DB_TYPE_NAME = 'sqlite.django'
    else:
        DB_TYPE_NAME = 'sqlite.django' # 默认 SQLite3 引擎

    config = get_configs(CONFIG_PATH)
    root_path = config['dirname']
    project_name = config['project_name']
    root_settingspy = os.path.join(root_path, project_name, 'settings.py')

    DAtABASES_content = get_databases_content(root_settingspy)

    template_str = get_content(DB_TYPE_NAME, concat=['settings',], replace=True, 
        engine = kwargs['engine'], 
        database_name = kwargs['database_name'], 
        username = kwargs['username'], 
        password = kwargs['password'], 
        ip = kwargs['ip'], 
        port = kwargs['port'], 
        test = kwargs['test']
    )
    whole_text = read_file(root_settingspy)
    replace_text = whole_text.replace(DAtABASES_content, ''.join(template_str))
    write_file(root_settingspy, content=replace_text)

    refresh_config()

def fix_urls(app_url: str)->None:
    """修复路由"""
    # path('main/', include('main.urls')),
    config = get_configs(CONFIG_PATH)
    root_path = config['dirname'] # Django项目根路径
    project_name = config['project_name'] # 项目名称
    root_urlspy = os.path.join(root_path, project_name, 'urls.py') # 定位项目的主urls.py文件
    urlpatterns_content = get_urlpatterns_content(root_urlspy) # 锁定路由文本区域

    insert_str = f"path('{app_url.split('.')[0]}/', include('{app_url}')),"
    whole_text = read_file(root_urlspy)
    replace_text = whole_text.replace(urlpatterns_content, f"{urlpatterns_content}    {insert_str}\n")
    # 覆盖写入
    write_file(root_urlspy, content=replace_text)

def add_oneline_to_listattr(setting_path: str, patt, idata: str, indent: int=4)->None:
    """向列表变量添加行"""
    content = get_list_patt_content(PATT_MIDDLEWARE, setting_path)
    insert_data = " " * indent + f"{idata},\n"
    new_content = f"{content}{insert_data}"
    
    write_file(setting_path, read_file(setting_path).replace(content, new_content))

def pop_oneline_to_listattr(setting_path: str, patt, idata: str, indent: int=4)->None:
    """向列表变量添加行"""
    content = get_list_patt_content(PATT_MIDDLEWARE, setting_path)
    insert_data = " " * indent + f"{idata},\n"
    new_content = content.replace(insert_data, '')
    
    write_file(setting_path, read_file(setting_path).replace(content, new_content))

def refresh_config()->None:
    """初始化配置文件"""
    PROJECT_CONFIG = get_configs(CONFIG_PATH)
    PROJECT_BASE_DIR = PROJECT_CONFIG['dirname']
    DIRSETTINGS = os.path.join(PROJECT_BASE_DIR, PROJECT_CONFIG['project_name'], 'settings.py')
    # 更新配置文件
    temp_configs = {} # 全局配置文件待写入
    # 必要前缀赋值
    temp_configs['dirname'] = PROJECT_BASE_DIR # 项目路径
    temp_configs['project_name'] = os.path.basename(PROJECT_BASE_DIR) # 项目名称
    apps = os.listdir(PROJECT_BASE_DIR) # 所有的应用程序（包含主程序）
    temp_configs['app_names'] = [_ for _ in apps if os.path.exists(os.path.join(PROJECT_BASE_DIR, _, 'migrations'))] # 以迁移目录为依据进行筛选
    settings = {}
    with open(DIRSETTINGS, 'r', encoding='utf-8') as f:
        text = PATT_BASE_DIR.sub('', f.read())
        exec(f"BASE_DIR = r'{PROJECT_BASE_DIR}'", {}, settings)
        exec(text, {}, settings)
    temp_configs['DATABASES'] = settings.get('DATABASES') # 数据库
    temp_configs['DEBUG'] = settings.get("DEBUG") # 调试状态
    temp_configs['LANGUAGE_CODE'] = settings.get("LANGUAGE_CODE") # 语言环境
    temp_configs['TIME_ZONE'] = settings.get("TIME_ZONE") # 时区
    temp_configs['USE_I18N'] = settings.get("USE_I18N") # 全局语言设置
    temp_configs['USE_L10N'] = settings.get("USE_L10N")
    temp_configs['USE_TZ'] = settings.get("USE_TZ") # 是否使用标准时区
    temp_configs['STATIC_URL'] = settings.get("STATIC_URL") # 静态文件路径
    temp_configs['ALLOWED_HOSTS'] = settings.get("ALLOWED_HOSTS") # 允许连接ip
    temp_configs['X_FRAME_OPTIONS'] = settings.get("X_FRAME_OPTIONS") # 是否开启iframe
    temp_configs['SECRET_KEY'] = settings.get("SECRET_KEY") # SECRET_KEY
    temp_configs['CORS_ORIGIN_ALLOW_ALL'] = settings.get("CORS_ORIGIN_ALLOW_ALL") # 跨域
    temp_templates_app = settings.get("TEMPLATES")
    if temp_templates_app and len(temp_templates_app) > 0:
        try:
            temp_configs['TEMPLATES_APP_DIRS'] = temp_templates_app[0]['APP_DIRS'] # 是否开启应用程序模板文件路径
            temp_configs['TEMPLATES_DIRS'] = temp_templates_app[0]['DIRS'] # 默认模板路径
        except:
            temp_configs['TEMPLATES_APP_DIRS'] = None
            temp_configs['TEMPLATES_DIRS'] = None # 默认模板路径
    else:
        temp_configs['TEMPLATES_APP_DIRS'] = None
        temp_configs['TEMPLATES_DIRS'] = None # 默认模板路径

    dump_json(CONFIG_PATH, temp_configs)  # 写入配置文件
