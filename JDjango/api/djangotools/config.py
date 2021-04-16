from .common import *

# config.json 会随时变化，获取值应当是即时的

def to_direct(func):
    @wraps(func)
    def decorator():
        return func()
    return decorator() # 装饰器会一次计算并缓存，所以这里取消修饰

# 检测配置文件是否存在，不存在则新建
if os.path.exists(CONFIG_PATH) and os.path.isdir(CONFIG_PATH):
    os.mkdir(CONFIG_PATH)

def dirname()->str:
    try:
        return get_configs(CONFIG_PATH)["dirname"]
    except:
        return 'None'

def project_name()->str:
    try:
        return get_configs(CONFIG_PATH)["project_name"]
    except:
        return 'None'

def app_names()->List[str]:
    try:
        return get_configs(CONFIG_PATH)['app_names']
    except:
        return 'None'

def DATABASES()->Dict[str, Dict[str, str]]:
    try:
        return get_configs(CONFIG_PATH)['DATABASES']
    except:
        return 'None'

def DEBUG()->bool:
    try:
        return get_configs(CONFIG_PATH)['DEBUG']
    except:
        return 'None'

def SettingsPath()->str:
    PROJECT_CONFIG = get_configs(CONFIG_PATH)
    PROJECT_BASE_DIR = PROJECT_CONFIG['dirname']
    return os.path.join(PROJECT_BASE_DIR, PROJECT_CONFIG['project_name'], 'settings.py')

def UrlsPath()->str:
    """根路由的路径"""
    PROJECT_CONFIG = get_configs(CONFIG_PATH)
    PROJECT_BASE_DIR = PROJECT_CONFIG['dirname']
    return os.path.join(PROJECT_BASE_DIR, PROJECT_CONFIG['project_name'], 'urls.py')

def GetAppFilePath(app_name: str, file_name: str, suffix: str='.py', join_path: List[str]=[], point_path: str=None)->str:
    """获取 app 下的 对应文件路径
    
        file_name 只需传入文件名即可，后缀名默认为 py
    """
    PROJECT_CONFIG = get_configs(CONFIG_PATH)
    if point_path is None:
        PROJECT_BASE_DIR = PROJECT_CONFIG['dirname']
    else:
        PROJECT_BASE_DIR = point_path
    return os.path.join(PROJECT_BASE_DIR, app_name, *join_path, file_name+suffix)
