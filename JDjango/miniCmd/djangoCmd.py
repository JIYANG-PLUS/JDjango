import os, json, glob
from ..tools._tools import *
from ..tools._re import *
from ..tools import environment as env
from ..tools import models as models_env
from ..settings import CONFIG_PATH, TEMPLATE_DIR
from typing import Dict, List

"""
### 关于 settings.py 的说明：
# 不允许在 settings.py 中引入任何的第三方库（尽管这是可行的行为）；
# 若想要做一些环境初始化（如：MySQL配置），请移步到同目录下的 __init__.py 文件中设置。

"""

class UnsupportDatabaseException(Exception): ...

__all__ = [

    'startproject', # 新建项目
    'startapp', # 新建应用程序

    'get_site_title', # 获取后台站点网站名
    'get_site_header', # 获取后台站点登录名
    'get_all_apps_name', # 获取所有的应用程序名
    'get_urlpatterns_content', # 获取urls.py中urlpatterns中括号内部的内容
    'get_models_path_by_appname', # 获取当前app下所有的模型文件路径
    'get_models_by_appname', # 获取当前app下的所有模型

    'set_site_header', # 设置后台站点登录名
    'set_site_title', # 设置后台站点网站名

    'write_admin_base', # 创建最基本的后台管理中心
    'judge_in_main_urls', # 判断应用程序是否均在urls.py中注册
    'fix_urls', # 修复路由
    'refresh_config', # 更新配置文件config.json
    'update_settings_DTATBASES', # 数据库引擎更换
    
]


def django_file_path(file_name: str, concat: List[str]=[])->str:
    """补全模板路径"""
    # 这里的concat用于弥补中间的残缺路径（因为文件可能分类在不同的文件夹下，只能保证根目录不变）
    if None == concat:
        concat = []
    return os.path.join(TEMPLATE_DIR, *concat, file_name) # 模板路径

def read_file_lists(r_path: str, *args, **kwargs)->List[str]:
    """列表式读取文件"""
    with open(r_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if 'replace' in kwargs and kwargs['replace']: # 替换开启
        lines = [PATT_REPLACE.sub(lambda x:kwargs[x.group(1)], _) for _ in lines]
    return lines

def get_content(file_name, *args, **kwargs):
    """获取规则替换后的文件列表"""
    return read_file_lists(django_file_path(file_name, concat=kwargs.get('concat')), *args, **kwargs)

def append_content(path: str, name: str, *args, **kwargs)->None:
    """向一个已存在的文本末尾添加另一个文本的规则替换内容"""
    # 调用：append_content(alias_paths[0], 'renameHeader.django', concat=['admin'], replace=True, model_name=k, site_name=site_name)
    content = get_content(name, *args, **kwargs)
    append_file(path, content)

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
        os.mkdir(os.path.join(path, 'templates'))
        os.mkdir(os.path.join(path, 'templates', 'includes'))
        new_file(os.path.join(path, 'templates', 'base.html'), content=get_content('baseHtml.django'))

        """static"""
        os.mkdir(os.path.join(path, 'static'))
        os.mkdir(os.path.join(path, 'static', 'js'))
        os.mkdir(os.path.join(path, 'static', 'img'))
        os.mkdir(os.path.join(path, 'static', 'css'))

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
        os.mkdir(os.path.join(APP_DIR, 'templates'))
        os.mkdir(os.path.join(APP_DIR, 'templates', app_name))
        os.mkdir(os.path.join(APP_DIR, 'templates', app_name, 'includes'))
        TEMP_DIR = os.path.join(APP_DIR, 'templates', app_name)
        new_file(os.path.join(TEMP_DIR, 'base.html'), content=get_content('baseHtml.django'))
        new_file(os.path.join(TEMP_DIR, 'includes', 'paginator.html'), content=get_content('paginator.django'))
        """"""
        """""""""static"""
        """"""
        os.mkdir(os.path.join(APP_DIR, 'static'))
        os.mkdir(os.path.join(APP_DIR, 'static', app_name))
        os.mkdir(os.path.join(APP_DIR, 'static', app_name, 'js'))
        os.mkdir(os.path.join(APP_DIR, 'static', app_name, 'img'))
        os.mkdir(os.path.join(APP_DIR, 'static', app_name, 'css'))
        """"""
        """""""""templatetags"""
        """"""
        os.mkdir(os.path.join(APP_DIR, 'templatetags'))
        new_file(os.path.join(APP_DIR, 'templatetags', '__init__.py'))
        new_file(os.path.join(APP_DIR, 'templatetags', 'filter.py'), content=get_content('filter.django'))
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

def _get_all_py_path_by_alias(alias: List[str])->List[str]:
    """根据别名筛选文件"""
    f_path = get_configs(CONFIG_PATH)["dirname"] # 项目根路径
    
    search_path = os.path.join(f_path, '**', '*')
    objs = glob.glob(search_path, recursive=True)
    
    alias = [os.path.basename(_) for _ in alias] # 只取文件名（功能扩展）

    temp = []
    for _ in objs: # 取所有的 admin.py 及其别名
        if os.path.basename(_) in alias:
            temp.append(_)
    return temp # 当前项目根路径下所有的admin类型源文件路径

def get_site_header()->List[str]:
    """获取登录界面名称"""
    options = []
    for _ in _get_all_py_path_by_alias(env.getAdminAlias()): # 逐个文件读取判断
        source = ' '.join([t.strip() for t in read_file_list_del_comment(_)])
        options.extend(PATT_HEADER_NAME.findall(source)) # 扣出登录界面名称
    return options

def set_site_header(new_name: str, mode: int=0)->None:
    """设置 获取登录界面名称"""
    # mode: 0没有，1仅一个，2多个
    # 删除所有的名称命名处
    alias_paths = _get_all_py_path_by_alias(env.getAdminAlias())
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

def get_site_title()->List[str]:
    """获取后台标题名称 注释见get_site_header"""
    options = []
    for _ in _get_all_py_path_by_alias(env.getAdminAlias()):
        source = ' '.join([t.strip() for t in read_file_list_del_comment(_)])
        options.extend(PATT_TITLE_NAME.findall(source))
    return options

def set_site_title(new_name: str, mode: int=0)->None:
    """设置 获取后台标题名称 注释见set_site_header"""
    alias_paths = _get_all_py_path_by_alias(env.getAdminAlias())
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

def get_urlpatterns_content(path: str)->str:
    """获取urlpatterns列表内容区域"""
    content = read_file(path)
    obj = PATT_URLPATTERNS.search(content)
    if obj:
        complex_content = PATT_URLPATTERNS.findall(content)[0]
        return cut_content_by_doublecode(complex_content)
    else:
        return ''

def get_databases_content(path: str)->str:
    """获取DATABASE配置信息"""
    content = read_file(path)
    obj = PATT_DAtABASES.search(content)
    if obj:
        complex_content = PATT_DAtABASES.findall(content)[0]
        return cut_content_by_doublecode(complex_content, leftCode='{', rightCode='}')
    else:
        return ''

def update_settings_DTATBASES(db_type: str, *args, **kwargs)->None:
    """更新数据库引擎"""
    if db_type not in ('sqlite', 'mysql',):
        raise UnsupportDatabaseException('暂不支持的数据库引擎')

    if 'mysql' == db_type:
        DB_TYPE_NAME = 'mysql.django'
    elif 'sqlite' == db_type:
        DB_TYPE_NAME = 'sqlite.django'

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

def get_all_need_register_urls(config: Dict[str, object])->List[str]:
    """获取所有注册名（include('demo.urls')）"""
    apps = config['app_names'] # 取所有的app名称
    # 取第一个urls别名，（不带后缀名）
    alias = [os.path.basename(_).split('.')[0] for _ in env.getUrlsAlias()][0] # 仅取文件名
    return [f'{_}.{alias}' for _ in apps] # 将所有的app名拼接上路由文件名（不带后缀名）

def judge_in_main_urls()->List[str]:
    """判断是否注册路由（返回位注册的路由）"""
    config = get_configs(CONFIG_PATH)
    root_path = config['dirname'] # Django项目根路径
    project_name = config['project_name'] # 项目名称
    root_urlspy = os.path.join(root_path, project_name, 'urls.py') # 定位项目的主urls.py文件
    urlpatterns_content = get_urlpatterns_content(root_urlspy) # 锁定路由文本区域
    app_urls = get_all_need_register_urls(config)
    return [_ for _ in app_urls if _ not in urlpatterns_content]

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

def get_all_apps_name()->List[str]:
    """获取所有的应用程序名"""
    return get_configs(CONFIG_PATH)['app_names']

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
