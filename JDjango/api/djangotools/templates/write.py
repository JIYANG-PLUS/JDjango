from ..common import *
from ..basetools import *

__all__ = [
    'startproject', # 新建项目
    'startapp', # 新建应用程序
]

def startproject(path: str, project_name: str)->int:
    """新建项目，成功返回0，失败返回1"""
    if retools.PATT_CHARSNUMBER.match(project_name) and not os.path.exists(os.path.join(path, project_name)):
        """project_name"""
        os.mkdir(os.path.join(path, project_name))

        path = os.path.join(path, project_name)
        os.mkdir(os.path.join(path, project_name))

        PDir = os.path.join(path, project_name)
        new_file(os.path.join(PDir, '__init__.py'))
        new_file(os.path.join(PDir, 'urls.py'), content=get_content('urls.django', concat=['project']))
        new_file(os.path.join(PDir, 'asgi.py'), content=get_content('asgi.django', concat=['project'], replace=True, project_name=project_name))
        new_file(os.path.join(PDir, 'wsgi.py'), content=get_content('wsgi.django', concat=['project'], replace=True, project_name=project_name))
        new_file(os.path.join(PDir, 'settings.py'), content=get_content('settings.django', concat=['project'], replace=True, project_name=project_name, secret_key=generate_secret_key()))
        
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
    if retools.PATT_CHARSNUMBER.match(app_name) and not os.path.exists(os.path.join(PROJECT_BASE_DIR, app_name)):
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
