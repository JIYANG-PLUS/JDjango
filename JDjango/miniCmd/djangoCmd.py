import os, re, json, glob
from ..tools._tools import *
from ..tools.environment import *
from ..settings import BASE_DIR as PROJECT_BASE_NAME, CONFIG_PATH

TEMPLATE_DIR = os.path.join(PROJECT_BASE_NAME, 'djangoTemplates')

__all__ = [
    'startproject',
    'startapp',
    'write_admin_base',
    'get_site_header',
    'get_site_title',
    'set_site_header',
    'set_site_title',
    'get_urlpatterns_content',
]

PATT_CHARS = re.compile(r'^[a-zA-Z0-9]*$') # 只允许数字和字母组合
PATT_REPLACE = re.compile(r'[$][{](.*?)[}]') # 定位模板替换位置
PATT_TITLE_NAME = re.compile(r'admin.site.site_title\s*=\s*[\"\'](.*?)[\"\']') # 定位后台登录名称位置
PATT_HEADER_NAME = re.compile(r'admin.site.site_header\s*=\s*[\"\'](.*?)[\"\']') # 定位后台网站名称位置
PATT_URLPATTERNS = re.compile(r'(?ms:urlpatterns\s*=\s*\[.*)') # 定位 urlpatterns 类html和xml文本不推荐使用正则

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
    if PATT_CHARS.match(project_name) and not os.path.exists(os.path.join(path, project_name)):
        """project_name"""
        os.mkdir(os.path.join(path, project_name))
        PDir = os.path.join(path, project_name)
        new_file(os.path.join(PDir, '__init__.py'))
        new_file(os.path.join(PDir, 'urls.py'), content=get_content('urls.django', concat=['project']))
        new_file(os.path.join(PDir, 'asgi.py'), content=get_content('asgi.django', concat=['project'], replace=True, project_name=project_name))
        new_file(os.path.join(PDir, 'wsgi.py'), content=get_content('wsgi.django', concat=['project'], replace=True, project_name=project_name))
        new_file(os.path.join(PDir, 'settings.py'), content=get_content('settings.django', concat=['project'], replace=True, project_name=project_name))
        
        """templates"""
        os.mkdir(os.path.join(PDir, 'templates'))
        os.mkdir(os.path.join(PDir, 'templates', 'includes'))
        new_file(os.path.join(PDir, 'base.html'), content=get_content('baseHtml.django'))

        """static"""
        os.mkdir(os.path.join(PDir, 'static'))
        os.mkdir(os.path.join(PDir, 'static', 'js'))
        os.mkdir(os.path.join(PDir, 'static', 'img'))
        os.mkdir(os.path.join(PDir, 'static', 'css'))

        """manage.py"""
        new_file(os.path.join(path, 'manage.py'), content=get_content('manage.django', concat=['project'], replace=True, project_name=project_name))

        return 0
    else:
        return 1

def startapp(app_name):
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
    for _ in _get_all_py_path(getAdminAlias()): # 逐个文件读取判断
        source = ' '.join([t.strip() for t in read_file_list_del_comment(_)])
        options.extend(PATT_HEADER_NAME.findall(source))
    return options

def set_site_header(new_name, mode=0):
    """设置 获取登录界面名称"""
    # mode: 0没有，1仅一个，2多个
    # 删除所有的名称命名处
    alias_paths = _get_all_py_path(getAdminAlias())
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
    for _ in _get_all_py_path(getAdminAlias()):
        source = ' '.join([t.strip() for t in read_file_list_del_comment(_)])
        options.extend(PATT_TITLE_NAME.findall(source))
    return options

def set_site_title(new_name, mode=0):
    """设置 获取后台标题名称 注释见set_site_header"""
    alias_paths = _get_all_py_path(getAdminAlias())
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