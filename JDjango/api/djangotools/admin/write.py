from ..common import *
from ..basetools import *

__all__ = [
    'set_site_header', # 设置后台站点登录名
    'set_site_title', # 设置后台标题名
    'write_admin_base', # 创建最基本的后台管理中心
]

def set_site_header(new_name: str, mode: int=0)->None:
    """设置 获取登录界面名称
        # mode: 0没有（随机插入），1仅一个（原地修改），2表示多个（全部删除后随机插入）
    """
    
    alias_paths = get_all_py_path_by_alias(env.getAdminAlias())
    if 2 == mode:
        for _ in alias_paths:
            content = retools.PATT_HEADER_NAME.sub('', read_file(_))
            write_file(_, content)
            
    if 1 == mode:
        for _ in alias_paths:
            t_content = read_file(_)
            if retools.PATT_HEADER_NAME.search(t_content):
                write_file(_, retools.PATT_HEADER_NAME.sub(lambda x:x.group(0).replace(x.group(1), new_name), t_content))
                break
            
    if mode in (0, 2):
        append_content(alias_paths[0], 'renameHeader.django', concat=['admin'], replace=True, header_name=new_name)

def set_site_title(new_name: str, mode: int=0)->None:
    """设置 获取后台标题名称 注释见set_site_header"""
    alias_paths = get_all_py_path_by_alias(env.getAdminAlias())
    if 2 == mode:
        for _ in alias_paths:
            content = retools.PATT_TITLE_NAME.sub('', read_file(_))
            write_file(_, content)
    if 1 == mode:
        for _ in alias_paths:
            t_content = read_file(_)
            if retools.PATT_TITLE_NAME.search(t_content):
                write_file(_, retools.PATT_TITLE_NAME.sub(lambda x:x.group(0).replace(x.group(1), new_name), t_content))
                break
    if mode in (0, 2):
        append_content(alias_paths[0], 'renameTitle.django', concat=['admin'], replace=True, title_name=new_name)

def write_admin_base(path: str, importData: Dict[str, List[str]])->None:
    """管理中心后台简单注册"""
    for k, v in importData.items():
        for site_name in v:
            append_content(path, 'base.django', concat=['admin'], replace=True, model_name=k, site_name=site_name)

