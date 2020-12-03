import os, re, json

def get_configs():
    with open('config.json', 'r', encoding='utf-8') as f:
        configs = json.load(f)
    return configs

__all__ = [
    'startapp',
]

PATT_CHARS = re.compile(r'^[a-zA-Z0-9]*$')
PATT_REPLACE = re.compile(r'[$][{](.*?)[}]')

def new_file(name, content=None):
    with open(name, 'w', encoding='utf-8') as f:
        if content: f.writelines(content)

def django_file_path(file_name):
    return os.path.join(os.getcwd(), 'djangoTemplates', file_name)

def read_file_lists(name, path, *args, **kwargs):
    f_path = os.path.dirname(path)
    r_path = os.path.join(f_path, 'djangoTemplates', name)
    with open(r_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if 'replace' in kwargs and kwargs['replace']:
        lines = [PATT_REPLACE.sub(lambda x:kwargs[x.group(1)], _) for _ in lines]
    return lines

def startapp(app_name):
    configs = get_configs()
    BASE_DIR = configs['dirname']
    if PATT_CHARS.match(app_name) and not os.path.exists(os.path.join(BASE_DIR, app_name)):
        """""""""main"""
        """"""
        os.mkdir(os.path.join(BASE_DIR, app_name))
        APP_DIR = os.path.join(BASE_DIR, app_name)
        new_file(os.path.join(APP_DIR, '__init__.py'))
        new_file(os.path.join(APP_DIR, 'admin.py'), content=read_file_lists(django_file_path('admin.django'), BASE_DIR))
        new_file(os.path.join(APP_DIR, 'apps.py'), content=read_file_lists(django_file_path('apps.django'), BASE_DIR
            , replace=True
            , app_name=app_name))
        new_file(os.path.join(APP_DIR, 'forms.py'), content=read_file_lists(django_file_path('forms.django'), BASE_DIR))
        new_file(os.path.join(APP_DIR, 'models.py'), content=read_file_lists(django_file_path('models.django'), BASE_DIR))
        new_file(os.path.join(APP_DIR, 'tests.py'), content=read_file_lists(django_file_path('tests.django'), BASE_DIR))
        new_file(os.path.join(APP_DIR, 'urls.py'), content=read_file_lists(django_file_path('urls.django'), BASE_DIR
            , replace=True
            , app_name=app_name))
        new_file(os.path.join(APP_DIR, 'views.py'), content=read_file_lists(django_file_path('views.django'), BASE_DIR))
        """"""
        """""""""templates"""
        """"""
        os.mkdir(os.path.join(APP_DIR, 'templates'))
        os.mkdir(os.path.join(APP_DIR, 'templates', app_name))
        os.mkdir(os.path.join(APP_DIR, 'templates', app_name, 'includes'))
        TEMP_DIR = os.path.join(APP_DIR, 'templates', app_name)
        new_file(os.path.join(TEMP_DIR, 'base.html'), content=read_file_lists(django_file_path('baseHtml.django'), BASE_DIR))
        new_file(os.path.join(TEMP_DIR, 'includes', 'paginator.html'), content=read_file_lists(django_file_path('paginator.django'), BASE_DIR))
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
        new_file(os.path.join(APP_DIR, 'templatetags', 'filter.py'), content=read_file_lists(django_file_path('filter.django'), BASE_DIR))
        """"""
        """""""""migrations"""
        """"""
        os.mkdir(os.path.join(APP_DIR, 'migrations'))
        new_file(os.path.join(APP_DIR, 'migrations', '__init__.py'))
        """"""
        return 0
    else:
        return 1
