from ..common import *
from .. import basetools

__all__ = [
    'judge_installed_library', # 判断是否注册应用程序
]

def judge_installed_library(name = 'simpleui', type=retools.PATT_INSTALLED_APPS)->bool:
    """获取已经安装的第三方库（从 INSTALL_APP 中获取判断）"""
    register_obj = basetools.get_list_patt_content(type, basetools.get_django_settings_path())
    del_comment = [retools.PATT_COMMENT.sub(' ', _) for _ in register_obj.split('\n')]
    if name in '\n'.join(del_comment):
        return True
    else:
        return False
