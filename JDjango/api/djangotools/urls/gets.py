from ..common import *
from .. import basetools
from .. import config as SCONFIGS

__all__ = [
    'get_app_rooturl_config_by_appname', # 通过app名称获取根路由路径下的完整根路由路径
    'get_all_need_register_urls', # 获取所有注册名，解析依据：（include('demo.urls')）
    'get_urls_list_tree', # 获取路由的数据包列表（用于描述整个路由）
    'get_location_from_urlspy', # 通过给定参数检索出选中路由所在的位置（行，列）
]

def get_app_rooturl_config_by_appname(appname: str)->str:
    """"通过app名称获取根路由路径下的完整根路由路径
        如：path('1/2/3/', include('demo.urls')) 将按demo的app名称获取到 '1/2/3/'
    """
    CONFIG = get_configs(CONFIG_PATH)
    # 获取路由别名（仅取文件名）
    alias = [os.path.basename(_) for _ in env.getUrlsAlias()]
    assert len(alias) > 0
    root_urlpath = os.path.join(CONFIG['dirname'], CONFIG['project_name'], alias[0]) # 默认取urls.py别名
    urlpatterns = basetools.get_list_patt_content(retools.PATT_URLPATTERNS, root_urlpath).split('\n') # 截取路由 URLPATTERNS 内容区域

    temp_include = appname + '.' + alias[0].split('.')[0] # 以后缀名 .urls 进行拼接（用于正则匹配的匹配字符串）

    # 以下两个正则表达式仅仅是 单双引号 的区别
    patt_name1 = re.compile(r"\((.+?),\s*include\s*\(\s*'" + temp_include + r"'\s*\)\s*\)")
    patt_name2 = re.compile(r'\((.+?),\s*include\s*\(\s*"' + temp_include + r'"\s*\)\s*\)')

    for _ in urlpatterns: # 原则上一定会找到
        if patt_name1.search(_):
            return patt_name1.findall(_)[0].strip(string.whitespace + '"\'')
        if patt_name2.search(_):
            return patt_name2.findall(_)[0].strip(string.whitespace + '"\'')
    else:
        return '' # 可有可无的语句

def get_all_need_register_urls(config: Dict[str, object])->List[str]:
    """获取所有注册名（include('demo.urls')）如：['demo.urls',]"""
    apps = config['app_names'] # 取所有的app名称
    # 取第一个urls别名，（不带后缀名）
    alias = [os.path.basename(_).split('.')[0] for _ in env.getUrlsAlias()][0] # 仅取文件名
    return [f'{_}.{alias}' for _ in apps] # 将所有的app名拼接上路由文件名（不带后缀名）


# ====== 路由树结构返回 ====== 

class Path(object):
    def __init__(self, origin_str: str, isNode: bool=True, level: int=0, isApp: bool=False) -> None:
        super().__init__()
        self.origin_str: str = origin_str
        
        self.isNode: bool = isNode # 默认可展开节点（为 Fasle 意味着 当前路由可直接打开）
        self.node_str: str = "" # 标记 展开节点 的 节点名称

        self.isApp: bool = isApp # 是否是路由的快捷方式（决定着是否进行过深层次搜索）为True表示是一个展开节点
        self.app_name: str = "" # 归属的应用程序名称（仅记录）
        self.code_app_name: str = "" # 代码中解析的应用程序名称（用于代码自动生成）
        self.app_file: str = "" # 归属的应用程序路由文件（仅记录）
        self.app_str: str = "" # 深层次搜索的专属容器（不用于展示数据，仅用于解析数据）
        
        self.level: int = level # 路由层级（主要用于记录路由的深度）
        self.children: List[Path] = [] # 默认无父节点，Path 类型

        # 下面的几个参数路径构建、数据绑定专用
        self.relate_url = "" # 累计的相对路径
        self.split_path = [] # 累积的拆分路由

    def __repr__(self) -> str:
        return self.origin_str

def get_urlpatterns(root_url_path: str = None)->str:
    """获取路由内容列表区域"""
    if root_url_path is None:
        root_url_path = SCONFIGS.UrlsPath()
    if not os.path.exists(root_url_path): return "" # 校验路径是否存在，不存在返回空串
    urlpatterns = basetools.get_list_patt_content(
        retools.PATT_URLPATTERNS, 
        root_url_path, 
        mode = 1, # 内容模式
        content=''.join(read_file_list_del_comment(root_url_path)) # 删除所有的注释内容
    )
    return urlpatterns

def is_path_or_repath(content: str):
    """判断当前就近解析的是 path 还是 re_path

        没有匹配：返回 'null'；匹配path：返回 'path'；匹配re_path 返回 're_path'
    """
    path_index = content.find("path")
    repath_index = content.find("re_path")
    if -1 == path_index and -1 == repath_index:
        return 'null'

    path_type = None
    if -1 == path_index:
        path_type = 're_path'
    if None == path_type and -1 == repath_index:
        path_type = 'path'
    if None == path_type:
        path_type = 'path' if path_index < repath_index else 're_path'
    return path_type # 不可能出现返回 None 的情况

def seperate_same_level_paths(node: Path, content: str='')->List[Path]:
    """将一块 路由区域 平级的 路由 进行 拆解
    
        若不提供 content ，则默认从Path对象的 origin_str 属性中获取
        调用此方法会默认扩充 children 属性
    """
    paths: List[Path] = []
    if not content:
        content = node.origin_str
    while "null" != is_path_or_repath(content):
        path_type = is_path_or_repath(content) # 此处避免解析到 include() 区域
        cut_content = cut_content_by_doublecode(content[content.find(path_type):], leftCode='(', rightCode=')')
        insert_path = Path(cut_content, level=node.level+1)
        insert_path.app_file = node.app_file # 路径传递
        insert_path.app_name = node.app_name # 归属应用程序传递（此处存在BUG，若某一include展开的路由中无子路由，则会延续 A-root-urls 的名称）
        insert_path.code_app_name = node.code_app_name # 应用程序代码名称传递
        paths.append(insert_path)
        content = content[content.find(cut_content)+len(cut_content):] # 向后平移拆分，理论上最小的时间复杂度
    node.children.extend(paths)
    return paths

def _get_app_name_from_urls(file_path: str):
    """获取路由文件中的应用程序代码展示名称（app_name）"""
    content = [_.strip().strip("\n").strip() for _ in read_file_list_del_comment(file_path)]
    for _ in content:
        if _.startswith("app_name") and (2 == len(_.split("="))):
            return _.split("=")[1].strip().strip("'\"")
    else:
        return ""

def get_app_urls_by_include(include_url: str, node: Path)->List[Path]:
    """通过 include 的参数（如：demo.urls）获取子级路由"""
    if '.' not in include_url: # 本工具不支持的语法
        return []
    split_str = include_url.split('.')
    code_app_name = ""
    if len(split_str) > 2:
        site_packages_path = env.get_path_by_env_order()
        if site_packages_path:
            if "django" == split_str[0].strip().lower():
                # 如果是原生 url，路径拼接
                app_name, file_name = "django", split_str[-1]
                file_path = SCONFIGS.GetAppFilePath("django", file_name, join_path=split_str[1:-1], point_path=site_packages_path)
            else:
                return []
        else:
            return [] # 这个情况将在后续进行完善
    else:
        app_name, file_name = split_str
        file_path = SCONFIGS.GetAppFilePath(app_name, file_name)
    code_app_name = _get_app_name_from_urls(file_path)
    urlpatterns = get_urlpatterns(file_path) # 获取应用程序路由区域（默认路径一定存在，所以不做校验 错，必须校验）
    # 先做赋值，后做校验（虽然不一定有子路由，但数据一定正确，所以先填值没错；后填值也没错，但会影响操作体验）
    node.app_name = app_name # 记录应用程序名称（将从 A-root-urls 继承的名称进行覆盖，填写实际的真实名称）
    node.app_file = file_path # 记录应用程序路由文件路径
    node.app_str = urlpatterns # 记录自己负责的路由信息区域
    node.code_app_name = code_app_name
    # 校验一定在最后，否则前端渲染的数据会出错（非错，只是不好看）
    url_type = is_path_or_repath(urlpatterns)
    if 'null' == url_type:
        return []
    return seperate_same_level_paths(node, urlpatterns) # 不使用默认 origin_str 属性解析

def analysis_urlpatterns()->Path:
    """解析 urlpatterns 为数据字典

        子路由解析依据（旧Django版本不予考虑）：
            1、path()
            2、re_path()
            3、include() # 目前仅考虑 include("demo.urls") 语法，直接传对象的语法暂不考虑
        别名解析依据： name = '' 参数
        相对路径解析依据： 第一个参数
        代码生成解析依据： 第二个参数
        是否可展开节点： 是否包含 include() 参数
    """
    # 正常情况下，路由集合必须是以 path 或 re_path 开头（个性化代码除外）
    # 因此本解析引擎的工作原理如下：
    # 通过 str 类型的 find 方法 找到第一个 path 或 re_path，然后通过括号匹配算法，层层剖析

    urlpatterns = get_urlpatterns()
    root_path = Path(urlpatterns) # 根节点
    root_path.app_file = SCONFIGS.UrlsPath() # 路径显示
    # root_path.app_name = "A-root-urls" # 根节点路由的归属名称

    url_type = is_path_or_repath(urlpatterns)
    if 'null' == url_type: return None # 解析错误，空结果
    
    stack: List[Path] = []
    stack.extend(seperate_same_level_paths(root_path)) # 初始化状态（包含全部路由）

    while len(stack) > 0:
        pop_node = stack.pop()
        node_content = pop_node.origin_str
        temp_path_type = is_path_or_repath(node_content) # 当前节点是否可以继续往下解析（是否还存在 path 或 re_path 方法）
        if 'null' == temp_path_type: # 无法 继续解析 的 视为 完整路由 或 深层次路径
            if retools.PATT_INCLUDE.search(node_content): # 只支持字符串格式的 include 参数
                pop_node.isApp = True # 深入查找标记
                pop_node.node_str = node_content # （虽然不在本路由区域中是路由，但也具备节点的性质，需要存储节点信息）
                include_url = retools.PATT_INCLUDE.findall(node_content)[0].strip().strip("'\"") # 获取跳转路由
                stack.extend(get_app_urls_by_include(include_url, pop_node))
            else:
                pop_node.isNode = False # 标记出口
        else: # 否则继续拆解（本情况下一定不包含include('demo.urls')的情况）
            pop_node.node_str = node_content[:node_content.find(temp_path_type)] # 保存节点路径，用于以后的拼接和判断
            stack.extend(seperate_same_level_paths(pop_node))

    return root_path # 一切从源头查起

def _show_root(root: Path):
    """内部展示节点用"""
    data = root.children
    while len(data) > 0:
        obj: Path = data.pop()
        if obj.isNode:
            print("  "*obj.level, "：", obj.node_str[:200].replace("\n", " $ "), "isApp：", obj.isApp)
        else:
            print("  "*obj.level, "：", obj.origin_str[:200].replace("\n", " $ "), obj.isApp)
        if len(obj.children) > 0:
            data.extend(obj.children)


def get_urls_list_tree():
    """获取路由的数据包列表（用于描述整个路由）,格式具体看 Path 中的结构定义"""
    root: Path = analysis_urlpatterns() # 获取解析根路由
    # _show_root(root)
    return root


def get_location_from_urlspy()->Tuple:
    """通过给定参数检索出选中路由所在的位置（行，列）"""
