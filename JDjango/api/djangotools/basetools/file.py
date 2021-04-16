from ..common import *

__all__ = [
    'django_file_path', # 补全获取 Django 模板的全部路径
    'read_file_lists', # 列表式读取模板文件（依赖${}定位正则语法）
    'get_content', # 对 django_file_path 和 get_content 的封包
    'append_content' , # 向一个已存在的文件末尾追加 模板 文本
]

def django_file_path(file_name: str, concat: List[str]=None)->str:
    """补全模板路径"""
    # 这里的concat用于弥补中间的残缺路径（因为文件可能分类在不同的文件夹下，但均使用同一个根目录）
    if None == concat:
        concat = []
    return os.path.join(TEMPLATE_DIR, *concat, file_name) # 模板路径

def read_file_lists(r_path: str, *args, **kwargs)->List[str]:
    """列表式读取文件"""
    with open(r_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if 'replace' in kwargs and kwargs['replace']: # 替换开启
        lines = [retools.PATT_REPLACE.sub(lambda x:kwargs[x.group(1)], _) for _ in lines]
    return lines

def get_content(file_name: str, *args, **kwargs)->List[str]:
    """获取规则替换后的文件列表"""
    return read_file_lists(django_file_path(file_name, concat=kwargs.get('concat')), *args, **kwargs)

def append_content(path: str, name: str, *args, **kwargs)->None:
    """向一个已存在的文本末尾添加另一个文本的规则替换内容（模板替换语法）"""
    # 调用方式：append_content(alias_paths[0], 'renameHeader.django', concat=['admin'], replace=True, model_name=k, site_name=site_name)
    content = get_content(name, *args, **kwargs)
    append_file(path, content)
