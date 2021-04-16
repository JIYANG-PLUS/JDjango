from ..common import *

__all__ = [
    'get_models_path_by_appname', # 获取当前app下所有的模型文件路径
    'get_models_by_appname', # 获取当前app下的所有模型
    'get_models_from_modelspy', # 从模型文件中读取所有模型
]

def get_models_path_by_appname(appname: str)->List[str]:
    """获取当前app下所有的模型文件路径"""
    APP_PATH = os.path.join(get_configs(CONFIG_PATH)['dirname'], appname) # 路径定位到当前app下
    models_path = []
    if os.path.exists(APP_PATH) and os.path.isdir(APP_PATH):
        pys = glob.glob(os.path.join(APP_PATH, '**', '*.py'), recursive=True) # 先取所有归属当前app下的文件路径
        alias = [os.path.basename(_) for _ in env.getModelsAlias()] # 取所有模型别名（如：models.py）
        models_path.extend([_ for _ in pys if os.path.basename(_) in alias]) # 以别名为依据，过滤所有文件中可能的模型文件
    return models_path

def get_models_from_modelspy(path):
    """从模型文件中读取所有模型"""
    result = []
    for _ in read_file_list(path):
        result.extend(retools.PATT_MODEL.findall(_.strip()))
    return result


def get_models_by_appname(appname: str)->List[str]:
    """获取当前app下的所有模型"""
    pathModels = get_models_path_by_appname(appname)
    data = []
    for path in pathModels:
        data.extend(get_models_from_modelspy(path))
    return data

