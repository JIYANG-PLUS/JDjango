from ..common import *
from .. import config as SCONFIGS

__all__ = [
    'get_location_from_viewspy', # 定位视图在文件中的位置
]

def get_location_from_viewspy(app_name: str, def_class_name: str, dirname: str=None):
    """定位视图在文件中的位置
    
        不提供 dirname 的路径，则默认是当前选中项目的根路径
    """
    if "" == app_name or "" == def_class_name:
        return (1, 0, None)
    # 取所有 视图 文件的名称/路径名称
    view_alias = env.getViewsAlias()
    if dirname is None: dirname = SCONFIGS.dirname() # 默认是项目的路径
    base_view_path = os.path.join(dirname, app_name)
    for _ in view_alias:
        view_path = os.path.join(base_view_path, _)
        for i, line in enumerate(read_file_list_del_comment(view_path)):
            patt_def = r"^def\s*" + def_class_name + r"\s*\("
            patt_class = r"^class\s*" + def_class_name + r"\s*\("
            if re.search(patt_def, line):
                return (i, 0, view_path)
            if re.search(patt_class, line):
                return (i, 0, view_path)
    return (1, 0, None)
