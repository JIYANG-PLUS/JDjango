from ....tools._tools import *
from ....settings import CONFIG_PATH
from typing import List, Dict
from functools import wraps
import os

# config.json 会随时变化，获取值应当是即时的

def to_direct(func):
    @wraps(func)
    def decorator():
        return func()
    return decorator()

# 检测配置文件是否存在，不存在则新建
if os.path.exists(CONFIG_PATH) and os.path.isdir(CONFIG_PATH):
    os.mkdir(CONFIG_PATH)

@to_direct
def dirname()->str:
    try:
        return get_configs(CONFIG_PATH)["dirname"]
    except:
        return 'None'

@to_direct
def project_name()->str:
    try:
        return get_configs(CONFIG_PATH)["project_name"]
    except:
        return 'None'

@to_direct
def app_names()->List[str]:
    try:
        return get_configs(CONFIG_PATH)['app_names']
    except:
        return 'None'

@to_direct
def DATABASES()->Dict[str, Dict[str, str]]:
    try:
        return get_configs(CONFIG_PATH)['DATABASES']
    except:
        return 'None'

@to_direct
def DEBUG()->bool:
    try:
        return get_configs(CONFIG_PATH)['DEBUG']
    except:
        return 'None'
