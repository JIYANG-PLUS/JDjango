from ..common import *
from .judge import *
from .. import basetools

__all__ = [
    'register_for_settings_py', # 向 settings.py 文件中的列表对象增加一行注册信息
]

def register_for_settings_py(name: str, type=retools.PATT_INSTALLED_APPS)->None:
    """向 settings.py 文件中的列表对象增加一行注册信息
        name 两侧必须加引号（单双均可），如："'drf_generators'"
    """
    if not judge_installed_library(name, type=type): # type虽是内置方法，凑合吧
        basetools.add_oneline_to_listattr(basetools.get_django_settings_path(), type, name)
