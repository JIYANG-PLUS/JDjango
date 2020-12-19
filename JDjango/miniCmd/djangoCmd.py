import os, re, json
from ..tools._tools import *
from ..settings import BASE_DIR as PROJECT_BASE_NAME

TEMPLATE_DIR = os.path.join(PROJECT_BASE_NAME, 'djangoTemplates')

__all__ = [
    'startapp',
]

PATT_CHARS = re.compile(r'^[a-zA-Z0-9]*$')
PATT_REPLACE = re.compile(r'[$][{](.*?)[}]')

def django_file_path(file_name):
    return os.path.join(PROJECT_BASE_NAME, 'djangoTemplates', file_name) # 模板路径

def read_file_lists(name, *args, **kwargs):
    r_path = os.path.join(TEMPLATE_DIR, name)
    with open(r_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if 'replace' in kwargs and kwargs['replace']:
        lines = [PATT_REPLACE.sub(lambda x:kwargs[x.group(1)], _) for _ in lines]
    return lines

def startapp(app_name):
    configs = get_configs(os.path.join(PROJECT_BASE_NAME, 'config.json'))
    BASE_DIR = configs['dirname']
    if PATT_CHARS.match(app_name) and not os.path.exists(os.path.join(BASE_DIR, app_name)):
        """""""""main"""
        """"""
        os.mkdir(os.path.join(BASE_DIR, app_name))
        APP_DIR = os.path.join(BASE_DIR, app_name)
        new_file(os.path.join(APP_DIR, '__init__.py'))
        new_file(os.path.join(APP_DIR, 'admin.py'), content=read_file_lists(django_file_path('admin.django')))
        new_file(os.path.join(APP_DIR, 'apps.py'), content=read_file_lists(django_file_path('apps.django')
            , replace=True
            , app_name=app_name))
        new_file(os.path.join(APP_DIR, 'forms.py'), content=read_file_lists(django_file_path('forms.django')))
        new_file(os.path.join(APP_DIR, 'models.py'), content=read_file_lists(django_file_path('models.django')))
        new_file(os.path.join(APP_DIR, 'tests.py'), content=read_file_lists(django_file_path('tests.django')))
        new_file(os.path.join(APP_DIR, 'urls.py'), content=read_file_lists(django_file_path('urls.django')
            , replace=True
            , app_name=app_name))
        new_file(os.path.join(APP_DIR, 'views.py'), content=read_file_lists(django_file_path('views.django')))
        """"""
        """""""""templates"""
        """"""
        os.mkdir(os.path.join(APP_DIR, 'templates'))
        os.mkdir(os.path.join(APP_DIR, 'templates', app_name))
        os.mkdir(os.path.join(APP_DIR, 'templates', app_name, 'includes'))
        TEMP_DIR = os.path.join(APP_DIR, 'templates', app_name)
        new_file(os.path.join(TEMP_DIR, 'base.html'), content=read_file_lists(django_file_path('baseHtml.django')))
        new_file(os.path.join(TEMP_DIR, 'includes', 'paginator.html'), content=read_file_lists(django_file_path('paginator.django')))
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
        new_file(os.path.join(APP_DIR, 'templatetags', 'filter.py'), content=read_file_lists(django_file_path('filter.django')))
        """"""
        """""""""migrations"""
        """"""
        os.mkdir(os.path.join(APP_DIR, 'migrations'))
        new_file(os.path.join(APP_DIR, 'migrations', '__init__.py'))
        """"""
        return 0
    else:
        return 1
