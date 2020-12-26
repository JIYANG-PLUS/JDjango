import os, re, json
from ..tools._tools import *
from ..settings import BASE_DIR as PROJECT_BASE_NAME

TEMPLATE_DIR = os.path.join(PROJECT_BASE_NAME, 'djangoTemplates')

__all__ = [
    'startapp',
]

PATT_CHARS = re.compile(r'^[a-zA-Z0-9]*$') # 只允许数字和字母组合
PATT_REPLACE = re.compile(r'[$][{](.*?)[}]') # 定位模板替换位置

# 补全模板路径
def django_file_path(file_name):
    return os.path.join(PROJECT_BASE_NAME, 'djangoTemplates', file_name) # 模板路径

def read_file_lists(name, *args, **kwargs):
    r_path = os.path.join(TEMPLATE_DIR, name)
    with open(r_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if 'replace' in kwargs and kwargs['replace']: # 替换开启
        lines = [PATT_REPLACE.sub(lambda x:kwargs[x.group(1)], _) for _ in lines]
    return lines

def get_content(file_name, *args, **kwargs):
    return read_file_lists(django_file_path(file_name), *args, **kwargs)

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
        new_file(os.path.join(APP_DIR, 'apps.py'), content=get_content('apps.django', replace=True
            , app_name=app_name))
        new_file(os.path.join(APP_DIR, 'forms.py'), content=get_content('forms.django'))
        new_file(os.path.join(APP_DIR, 'models.py'), content=get_content('models.django'))
        new_file(os.path.join(APP_DIR, 'tests.py'), content=get_content('tests.django'))
        new_file(os.path.join(APP_DIR, 'urls.py'), content=get_content('urls.django', replace=True
            , app_name=app_name))
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
