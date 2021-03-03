from ....tools._tools import *
from ....settings import CONFIG_PATH
from typing import List, Dict
from functools import wraps

# config.json 会随时变化，获取值应当是即时的

def to_direct(func):
    @wraps(func)
    def decorator():
        return func()
    return decorator()

@to_direct
def dirname()->str:
    return get_configs(CONFIG_PATH)["dirname"]

@to_direct
def project_name()->str:
    return get_configs(CONFIG_PATH)["project_name"]

@to_direct
def app_names()->List[str]:
    return get_configs(CONFIG_PATH)['app_names']

@to_direct
def DATABASES()->Dict[str, Dict[str, str]]:
    return get_configs(CONFIG_PATH)['DATABASES']

@to_direct
def DEBUG()->bool:
    return get_configs(CONFIG_PATH)['DEBUG']
