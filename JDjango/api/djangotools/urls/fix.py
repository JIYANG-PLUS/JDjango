from ..common import *
from ..basetools import *

__all__ = [
    'fix_urls', # 修复路由
]

def fix_urls(app_url: str)->None:
    """修复路由"""
    # 参照模板：path('main/', include('main.urls')),
    config = get_configs(CONFIG_PATH)
    root_path = config['dirname'] # Django项目根路径
    project_name = config['project_name'] # 项目名称
    root_urlspy = os.path.join(root_path, project_name, 'urls.py') # 定位项目的主urls.py文件
    urlpatterns_content = get_list_patt_content(retools.PATT_URLPATTERNS, root_urlspy) # 锁定路由文本区域

    insert_str = f"path('{app_url.split('.')[0]}/', include('{app_url}')),"
    whole_text = read_file(root_urlspy)
    replace_text = whole_text.replace(urlpatterns_content, f"{urlpatterns_content}    {insert_str}\n")
    # 覆盖写入
    write_file(root_urlspy, content=replace_text)
