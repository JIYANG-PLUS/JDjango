import wx.dataview as wxdv

class Url(object):
    """真正的数据行"""
    def __init__(self, 
        app: str, gen_way: str, alias: str, 
        relate_path: str, full_path: str, split_path: str, 
        app_file: str, belong_app: str, code_app_name: str, 
        url_level: str, op: bool=False
    ):
        self.op = op
        self.gen_way = gen_way
        self.app = app # 非真正的应用程序名称，而是节点名称
        self.alias = alias
        self.full_path = full_path
        self.relate_path = relate_path
        self.split_path = split_path
        self.app_file = app_file
        self.code_app_name = code_app_name
        self.belong_app = belong_app # 真实的应用程序名称
        self.url_level = url_level

    def __repr__(self):
        return 'Url: %s-%s' % (self.app, self.alias)

class App(object):
    """节点构造"""
    def __init__(self, name):
        self.name = name # 应用程序名称
        self.urls = [] # 路由集合

    def __repr__(self):
        return 'App: ' + self.name

class ShowUrlsModel(wxdv.PyDataViewModel):

    def __init__(self, data):
        wxdv.PyDataViewModel.__init__(self)
        self.data = data # 获取传递过来的渲染数据
        self.UseWeakRefs(True) # 数据节点是 弱引用 时启用

    def GetColumnCount(self):
        """返回数据总的列数"""
        return 12

    def GetColumnType(self, col):
        """设置列的类型"""
        # string 字符串；datetime 日期；bool 布尔类型复选框
        types = [
            'string', # 节点名称
            'bool', # 操作
            'string', # 路由级数
            'string', # 相对路径
            'string', # 代码生成方式
            'string', # 别名
            'string', # 全路由
            'string', # 路由拆解
            'string', # 归属应用程序
            'string', # 应用程序检索名称
            'string', # 归属文件
            'string', # 解决 BUG 的空列
        ]
        mapper = {i:_ for i,_ in enumerate(types)}
        return mapper[col] # 返回给构造器类型

    def GetChildren(self, parent, children):
        """获取所有的孩子节点数据"""
        if not parent: # 没有父节点
            for app in self.data: # 遍历节点的数据包
                children.append(self.ObjectToItem(app))
            return len(self.data)

        node = self.ItemToObject(parent) # 有父节点的情况（复杂数据结构）
        if isinstance(node, App): # 父节点类型检测
            for url in node.urls: # 取复杂数据结构的数据区域
                children.append(self.ObjectToItem(url))
            return len(node.urls)
        return 0

    def IsContainer(self, item):
        """当前节点有子节点则返回 True """
        
        if not item: # 节点
            return True
            
        node = self.ItemToObject(item)
        if isinstance(node, App): # 数据包
            return True
            
        return False # 数据行

    def GetParent(self, item):
        """返回该节点的父节点"""
        if not item:
            return wxdv.NullDataViewItem

        node = self.ItemToObject(item)
        if isinstance(node, App):
            return wxdv.NullDataViewItem
        elif isinstance(node, Url):
            for g in self.data:
                if g.name == node.app:
                    return self.ObjectToItem(g)

    def HasValue(self, item, col):
        """判断是否是有效的数据行（非展开节点）"""
        node = self.ItemToObject(item)
        if isinstance(node, App) and col > 0: # 只在第一列渲染节点数据
            return False
        return True

    def GetValue(self, item, col):
        """获取某一具体单元格的值"""
        node = self.ItemToObject(item) # 获取当前节点对象

        if isinstance(node, App):
            assert col == 0, "展开节点必须在第一列" # 再次校验
            return node.name # 节点只需要名称

        elif isinstance(node, Url): # 数据包的行
            data = [
                node.app,
                node.op,
                node.url_level,
                node.relate_path,
                node.gen_way,
                node.alias,
                node.full_path,
                node.split_path,
                node.belong_app,
                node.code_app_name,
                node.app_file,
                "", # 解决最后一列无法显示的 BUG 
            ]
            mapper = {i:_ for i, _ in enumerate(data)}
            return mapper[col]

        else:
            raise RuntimeError("未知的节点类型")

    def GetRowListValue(self, item):
        """获取焦点所在行的列表数据集（不包含 首列 和 尾列）"""
        node = self.ItemToObject(item)
        if isinstance(node, App):
            return [] # 节点返回空数据
        return [self.GetValue(item, i) for i in range(self.GetColumnCount())[1:-1]]

    def GetRowDictValue(self, item):
        """获取焦点所在行的字典数据集"""
        node = self.ItemToObject(item)
        if isinstance(node, App):
            return {}
        return {
            "app": node.app,
            "op": node.op,
            "url_level": node.url_level,
            "relate_path": node.relate_path,
            "gen_way": node.gen_way,
            "alias": node.alias,
            "full_path": node.full_path,
            "split_path": node.split_path,
            "belong_app": node.belong_app,
            "code_app_name": node.code_app_name,
            "app_file": node.app_file,
            "end_line": "",
        }


    def GetAttr(self, item, col, attr):
        """设置节点的属性"""
        node = self.ItemToObject(item)
        if isinstance(node, App):
            attr.SetColour('blue')
            attr.SetBold(True)
            return True
        return False

    def SetValue(self, value, item, col):
        """第一列不允许改变，即不存在 0 == col 的情况"""
        node = self.ItemToObject(item)
        if isinstance(node, Url):
            if col == 1:
                node.op = value
            # elif col == 2:
            #     node.relate_path = value
            pass
        return True
