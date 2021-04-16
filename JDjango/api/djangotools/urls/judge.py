from ..common import *
from .gets import *
from .. import basetools

__all__ = [
    'judge_in_main_urls', # 返回未注册的路由全名，如：["demo.urls",]
]

def judge_in_main_urls()->List[str]:
    """返回未注册的路由，如：["demo.urls",]"""
    config = get_configs(CONFIG_PATH)
    root_path = config['dirname'] # Django项目根路径
    project_name = config['project_name'] # 项目名称
    root_urlspy = os.path.join(root_path, project_name, 'urls.py') # 定位项目的主urls.py文件
    urlpatterns_content = basetools.get_list_patt_content(retools.PATT_URLPATTERNS, root_urlspy) # 锁定路由文本区域
    app_urls = get_all_need_register_urls(config)
    return [_ for _ in app_urls if _ not in urlpatterns_content]
