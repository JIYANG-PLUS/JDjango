from .common import *

__all__ = [
    'judge_installed_library', # 判断是否注册
]

def judge_installed_library(name = 'simpleui')->bool:
    """获取已经安装的第三方库（从 INSTALL_APP 中获取判断）"""
    install_app = get_list_patt_content(PATT_INSTALLED_APPS, get_django_settings_path())
    del_comment = [PATT_COMMENT.sub(' ', _) for _ in install_app.split('\n')]
    if name in '\n'.join(del_comment):
        return True
    else:
        return False