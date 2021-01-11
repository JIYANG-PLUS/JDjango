import os, re, json, glob
from ..tools._tools import *
from ..tools import environment as env
from ..settings import BASE_DIR as PROJECT_BASE_NAME, CONFIG_PATH

TEMPLATE_DIR = os.path.join(PROJECT_BASE_NAME, 'djangoTemplates')
PROJECT_CONFIG = get_configs(CONFIG_PATH)
DIRNAME = PROJECT_CONFIG['dirname']
DIRSETTINGS = os.path.join(DIRNAME, PROJECT_CONFIG['project_name'], 'settings.py')

__all__ = [
    'startproject',
    'startapp',
    'write_admin_base',
    'get_site_header',
    'get_site_title',
    'set_site_header',
    'set_site_title',
    'get_urlpatterns_content',
    'judge_in_main_urls',
    'fix_urls',
    'refresh_config',
]

PATT_CHARS = re.compile(r'^[a-zA-Z0-9]*$') # 只允许数字和字母组合
PATT_REPLACE = re.compile(r'[$][{](.*?)[}]') # 定位模板替换位置
PATT_TITLE_NAME = re.compile(r'admin.site.site_title\s*=\s*[\"\'](.*?)[\"\']') # 定位后台登录名称位置
PATT_HEADER_NAME = re.compile(r'admin.site.site_header\s*=\s*[\"\'](.*?)[\"\']') # 定位后台网站名称位置
PATT_URLPATTERNS = re.compile(r'(?ms:urlpatterns\s*=\s*\[.*)') # 定位 urlpatterns 类html和xml文本不推荐使用正则
PATT_BASE_DIR = re.compile(r'BASE_DIR\s*=\s*os.path.dirname\s*\(\s*os.path.dirname\s*\(\s*os.path.abspath\s*\(\s*__file__\s*\)\s*\)\s*\)')

# 补全模板路径
def django_file_path(file_name, concat=[]):
    if None == concat:
        concat = []
    return os.path.join(TEMPLATE_DIR, *concat, file_name) # 模板路径

def read_file_lists(r_path, *args, **kwargs):
    with open(r_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if 'replace' in kwargs and kwargs['replace']: # 替换开启
        lines = [PATT_REPLACE.sub(lambda x:kwargs[x.group(1)], _) for _ in lines]
    return lines

def get_content(file_name, *args, **kwargs):
    return read_file_lists(django_file_path(file_name, concat=kwargs.get('concat')), *args, **kwargs)

def append_content(path, name, *args, **kwargs):
    # 调用：append_content(alias_paths[0], 'renameHeader.django', concat=['admin'], replace=True, model_name=k, site_name=site_name)
    content = get_content(name, *args, **kwargs)
    append_file(path, content)

def startproject(path, project_name):
    """新建项目"""
    if PATT_CHARS.match(project_name) and not os.path.exists(os.path.join(path, project_name)):
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

def startapp(app_name):
    """新建应用程序"""
    configs = get_configs(os.path.join(PROJECT_BASE_NAME, 'config.json'))
    BASE_DIR = configs['dirname']
    if PATT_CHARS.match(app_name) and not os.path.exists(os.path.join(BASE_DIR, app_name)):
        """""""""main"""
        """"""
        os.mkdir(os.path.join(BASE_DIR, app_name))
        APP_DIR = os.path.join(BASE_DIR, app_name)
        new_file(os.path.join(APP_DIR, '__init__.py'))
        new_file(os.path.join(APP_DIR, 'admin.py'), content=get_content('admin.django'))
        new_file(os.path.join(APP_DIR, 'apps.py'), content=get_content('apps.django', replace=True, app_name=app_name))
        new_file(os.path.join(APP_DIR, 'forms.py'), content=get_content('forms.django'))
        new_file(os.path.join(APP_DIR, 'models.py'), content=get_content('models.django'))
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

def write_admin_base(path, importData):
    """管理中心后台简单注册"""
    for k, v in importData.items():
        for site_name in v:
            append_content(path, 'base.django', concat=['admin'], replace=True, model_name=k, site_name=site_name)

def _get_all_py_path(alias):
    # 遍历项目路径下的所有admin.py（包括别名）的文件，寻找注册名称信息
    # 如果没有，则默认为Django，此时前台显示None
    f_path = get_configs(CONFIG_PATH)["dirname"] # 项目根路径
    # alias 取所有的admin.py及其别名
    search_path = os.path.join(f_path, '**', '*')
    objs = glob.glob(search_path, recursive=True)
    temp = []
    for _ in objs:
        if os.path.basename(_) in alias:
            temp.append(_)
    return temp # 当前项目根路径下所有的admin类型源文件路径

def get_site_header():
    """获取登录界面名称"""
    options = []
    for _ in _get_all_py_path(env.getAdminAlias()): # 逐个文件读取判断
        source = ' '.join([t.strip() for t in read_file_list_del_comment(_)])
        options.extend(PATT_HEADER_NAME.findall(source))
    return options

def set_site_header(new_name, mode=0):
    """设置 获取登录界面名称"""
    # mode: 0没有，1仅一个，2多个
    # 删除所有的名称命名处
    alias_paths = _get_all_py_path(env.getAdminAlias())
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

def get_site_title():
    """获取后台标题名称 注释见get_site_header"""
    options = []
    for _ in _get_all_py_path(env.getAdminAlias()):
        source = ' '.join([t.strip() for t in read_file_list_del_comment(_)])
        options.extend(PATT_TITLE_NAME.findall(source))
    return options

def set_site_title(new_name, mode=0):
    """设置 获取后台标题名称 注释见set_site_header"""
    alias_paths = _get_all_py_path(env.getAdminAlias())
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

def _cut_content_by_doublecode(text, leftCode='[', rightCode=']'):
    """获取成对的中括号中的文本"""
    # 如：[asd[cvb]] 会获取到 asd[cvb]
    stack = []
    cut_text = ""
    for _ in text:
        if len(stack) > 0:
            cut_text += _
        if leftCode == _:
            stack.append(_)
        if rightCode == _:
            stack.pop()
            if 0 == len(stack):
                return cut_text[:-1]
    return ''

def get_urlpatterns_content(path):
    """获取urlpatterns列表内容区域"""
    content = read_file(path)
    obj = PATT_URLPATTERNS.search(content)
    if obj:
        complex_content = PATT_URLPATTERNS.findall(content)[0]
        return _cut_content_by_doublecode(complex_content)
    else:
        return ''

def get_all_need_register_urls(config):
    """获取所有注册名（include('demo.urls')）"""
    apps = config['app_names'] # 取所有的app名称
    # 取第一个urls别名，（不带后缀名）
    alias = [os.path.basename(_).split('.')[0] for _ in env.getUrlsAlias()][0] # 仅取文件名
    return [f'{_}.{alias}' for _ in apps] # 将所有的app名拼接上路由文件名（不带后缀名）

def judge_in_main_urls():
    """判断是否注册路由"""
    config = get_configs(CONFIG_PATH)
    root_path = config['dirname'] # Django项目根路径
    project_name = config['project_name'] # 项目名称
    root_urlspy = os.path.join(root_path, project_name, 'urls.py') # 定位项目的主urls.py文件
    urlpatterns_content = get_urlpatterns_content(root_urlspy) # 锁定路由文本区域
    app_urls = get_all_need_register_urls(config)
    return [_ for _ in app_urls if _ not in urlpatterns_content]

def fix_urls(app_url):
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

def refresh_config():
    """初始化配置文件"""
    # 更新配置文件
    temp_configs = {} # 全局配置文件待写入
    # 必要前缀赋值
    temp_configs['dirname'] = DIRNAME # 项目路径
    temp_configs['project_name'] = os.path.basename(DIRNAME) # 项目名称
    apps = os.listdir(DIRNAME) # 所有的应用程序（包含主程序）
    temp_configs['app_names'] = [_ for _ in apps if os.path.exists(os.path.join(DIRNAME, _, 'migrations'))] # 以迁移目录为依据进行筛选
    settings = {}
    with open(DIRSETTINGS, 'r', encoding='utf-8') as f:
        text = PATT_BASE_DIR.sub('', f.read())
        exec(f"BASE_DIR = r'{DIRNAME}'", {}, settings)
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
