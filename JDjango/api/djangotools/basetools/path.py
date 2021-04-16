from ..common import *

__all__ = [
    'get_django_settings_path', # 获取项目的 setting.py 路径
]

def get_django_settings_path()->str:
    """获取Django路径下的settings.py的路径"""
    configs = get_configs(CONFIG_PATH)
    DIRNAME = configs["dirname"]
    DIRSETTINGS = os.path.join(DIRNAME, configs['project_name'], 'settings.py')
    return DIRSETTINGS
