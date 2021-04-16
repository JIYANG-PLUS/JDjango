from .common import *

class PathHelper(object):
    def __init__(self, path: Path, app: App=None) -> None:
        super().__init__()
        self.path: Path = path # 当前解析包
        self.app: App = app # 路径(/节点)归属节点，默认无

    def __repr__(self) -> str:
        return self.path.level # 返回节点深度

class UrlsListPanel(wx.Panel):

    def __init__( self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.select_row = {} # 选中行
        self._init_UI()
        self._init_listener()

    def _init_listener(self):
        """注册监听"""
        self.Bind(wxdv.EVT_DATAVIEW_ITEM_ACTIVATED, self.onItemDBClick, self.treeListData)
        self.Bind(wxdv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.onItemRightClick, self.treeListData)
        self.Bind(wxdv.EVT_DATAVIEW_SELECTION_CHANGED, self.onItemSelect, self.treeListData)
        self.Bind(wx.EVT_BUTTON, self.onBtnRefresh, self.btn_refresh)

    def _init_UI(self):
        """初始化UI界面"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self.SetBackgroundColour(CON_COLOR_MAIN)

        self.panel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(topsizer)
        topsizer.SetSizeHints(self.panel)
        sizer.Add(self.panel, 1, wx.EXPAND)

        '''
            操作工具栏
        '''
        self.toolsPanel = wx.Panel(self.panel)
        toolsPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.toolsPanel.SetSizer(toolsPanelSizer)
        topsizer.Add(self.toolsPanel, 0, wx.EXPAND | wx.ALL, 0)

        self.searcher = wx.SearchCtrl(self.toolsPanel, size=(300,-1), style=wx.TE_PROCESS_ENTER)
        self.searcher.ShowSearchButton(True)
        self.searcher.ShowCancelButton(True)
        toolsPanelSizer.Add(self.searcher, 0, wx.EXPAND | wx.ALL, 0)

        self.btn_refresh = buttons.GenButton(self.toolsPanel, -1, label='刷新')
        toolsPanelSizer.Add(self.btn_refresh, 0, wx.EXPAND | wx.ALL, 0)

        '''
            树形列表
        '''
        self.treeListData = wxdv.DataViewCtrl(self.panel,
            style = wx.BORDER_THEME
            | wxdv.DV_ROW_LINES # 斑马纹
            | wxdv.DV_HORIZ_RULES
            | wxdv.DV_VERT_RULES
            | wxdv.DV_VARIABLE_LINE_HEIGHT
            # | wxdv.DV_MULTIPLE # 多选
            | wxdv.DV_SINGLE # 单选
        )
        topsizer.Add(self.treeListData, 1, wx.EXPAND | wx.ALL, 0)

        self._init_listree_data()

    def _get_bulid_data(self)->List[App]:
        """获取构建数据
        
            构建原理：宽搜
        """
        # urls_data: Path = djangotools.get_urls_list_tree() # 获取原始的数据（根节点无实际用途）
        try:
            urls_data: Path = djangotools.get_urls_list_tree() # 获取原始的数据（根节点无实际用途）
        except Exception as e:
            print("错误：", e) # 软件调试用（本功能未稳定前，不准备删除）
            return []
        if urls_data is None: return []

        url_prefix = f'{env.getDjangoRunHost()}:{env.getDjangoRunPort()}/'

        root_app = App('A-root-urls') # 根路由的存储容器
        stack_urls: List[PathHelper] = [] # 栈
        show_nodes: List[App] = [root_app,] # 用于最终展示的节点

        # 首先初始化所有根节点的初始状态，以及节点容器（此处解决方案迸发于经验和灵感）
        for _ in urls_data.children:
            if _.isApp:
                temp_app = App(_.app_name)
                stack_urls.append(PathHelper(_, temp_app))
                show_nodes.append(temp_app)
            else:
                stack_urls.append(PathHelper(_, root_app))

        while len(stack_urls) > 0:
            pop_url: PathHelper = stack_urls.pop()
            pop_path: Path = pop_url.path
            pop_app: App = pop_url.app # 此处的作用只是为了扩展节点

            isNode: bool = pop_path.isNode
            isApp: bool = pop_path.isApp # （未用到）
            origin_str: str = pop_path.origin_str # origin_str 仅在 isNode = False 的时候有用
            node_str: str = pop_path.node_str # node_str 仅在 isNode = True 的时候有用

            '''
                获取 Url 对象的必要参数
            '''
            if not isNode: # 不是节点，定是展示行（仅此处分支插入行数据，程序的出口）
                sp_str = origin_str.split(',')
                one_path = sp_str[0].strip().strip("'\"/")# 路径片段
                if "" != one_path: one_path += "/" 
                gen_way = sp_str[1] # 代码生成方式
                alias = "" # 路径别名
                for _ in sp_str[2:]: # DJango 的 路由语法，第二个参数往后全部是关键字参数
                    try:
                        k, v = _.split('=')
                    except:
                        raise PathArgsError("请使用正确的路由语法！")
                    else:
                        if "name" == k.strip():
                            alias = v.strip().strip("'\"")
                            break
                    # 这里以后可以增加对路由参数的捕捉
                
                up_path = pop_path.relate_url + one_path # 拼接完整的相对路由
                pop_path.relate_url = up_path
                pop_path.split_path.append(one_path) # 必须加上分解路径才能完整
                url = Url(
                    pop_app.name, gen_way, alias if alias else "无", 
                    up_path, url_prefix + up_path, str(pop_path.split_path), 
                    pop_path.app_file, pop_path.app_name, pop_path.code_app_name,
                    str(pop_path.level)
                )
                pop_app.urls.append(url)
            else: # 节点的情况（分两种，一种是简单展开，一种是应用程序展开，统一处理）
                node_name = node_str[:node_str.find("include")].strip().strip(",").strip().strip("'\"/")
                if "" != node_name: node_name += "/" 
                temp_app = App(node_name)
                pop_app.urls.append(temp_app) # 树节点扩展
                for p in pop_path.children:
                    p.relate_url = pop_path.relate_url + node_name
                    p.split_path.append(node_name)
                    stack_urls.append(PathHelper(p, temp_app))
        return show_nodes

    def _init_listree_data(self):
        """初始化树形列表"""

        '''
            数据包构建
        '''
        data = self._get_bulid_data()
        self.model = ShowUrlsModel(data)
        self.treeListData.AssociateModel(self.model) # 通知控件使用该模型
        self.model.DecRef() # 渲染

        '''
            初始化列
        '''
        tr = wxdv.DataViewTextRenderer()
        col0 = wxdv.DataViewColumn("应用程序名", tr, 0)
        self.treeListData.AppendColumn(col0)
        # col0 = self.treeListData.AppendTextColumn("", 0)
        # col0.SetMinWidth(240)
        col0.SetWidth(240)
        col0.SetAlignment(wx.ALIGN_LEFT)

        insert_columns = [
            # 列名、宽度、单元格性质、对齐方式、类型
            ("操作", 44, wxdv.DATAVIEW_CELL_ACTIVATABLE, wx.ALIGN_CENTER, self.treeListData.AppendToggleColumn),
            ("路由级数", 66, wxdv.DATAVIEW_CELL_ACTIVATABLE, wx.ALIGN_CENTER, self.treeListData.AppendTextColumn),
            ("相对路由", 130, wxdv.DATAVIEW_CELL_ACTIVATABLE, wx.ALIGN_LEFT, self.treeListData.AppendTextColumn),
            ("代码生成方式", 120, wxdv.DATAVIEW_CELL_ACTIVATABLE, wx.ALIGN_LEFT, self.treeListData.AppendTextColumn),
            ("路由别名", 88, wxdv.DATAVIEW_CELL_ACTIVATABLE, wx.ALIGN_CENTER, self.treeListData.AppendTextColumn),
            ("全路由", 200, wxdv.DATAVIEW_CELL_ACTIVATABLE, wx.ALIGN_LEFT, self.treeListData.AppendTextColumn),
            ("路由拆解", 80, wxdv.DATAVIEW_CELL_ACTIVATABLE, wx.ALIGN_LEFT, self.treeListData.AppendTextColumn),
            ("归属应用程序", 120, wxdv.DATAVIEW_CELL_ACTIVATABLE, wx.ALIGN_CENTER, self.treeListData.AppendTextColumn),
            ("应用程序检索名称", 120, wxdv.DATAVIEW_CELL_ACTIVATABLE, wx.ALIGN_CENTER, self.treeListData.AppendTextColumn),
            ("归属文件", 180, wxdv.DATAVIEW_CELL_EDITABLE, wx.ALIGN_LEFT, self.treeListData.AppendTextColumn),
            # 末尾加一列空列（解决列表展示最后一列无法正常显示的BUG）
            ("", 1, wxdv.DATAVIEW_CELL_ACTIVATABLE, wx.ALIGN_CENTER, self.treeListData.AppendTextColumn),
        ]
        self._list_append_columns(insert_columns)

        # 允许排序
        for c in self.treeListData.Columns:
            c.Sortable = True
            c.Reorderable = True

        wx.CallAfter(col0.SetWidth, 240)

    def _list_append_columns(self, columns: List[object]):
        """列表添加列（从第二列开始自动添加）"""
        begin_index = 1
        for col in columns:
            col[-1](col[0], begin_index, width=col[1], mode=col[2], align=col[3])
            begin_index += 1

    def onItemDBClick(self, e):
        """双击事件"""

    def onItemRightClick(self, e):
        """右击弹出菜单"""
        self.popup_open_url = wx.NewIdRef()
        self.popup_open_view_path = wx.NewIdRef()
        self.popup_open_url_path = wx.NewIdRef()
        self.popup_modify_url = wx.NewIdRef()
        self.popup_insert_func = wx.NewIdRef()
        self.popup_get_code = wx.NewIdRef()
        self.popup_show_mvc_mtv = wx.NewIdRef()
        self.popup_open_url_path_wx = wx.NewIdRef()
        self.popup_open_view_path_wx = wx.NewIdRef()
        self.popup_open_model_path = wx.NewIdRef()

        self.Bind(wx.EVT_MENU, self.onPopupOpenUrl, id=self.popup_open_url)
        self.Bind(wx.EVT_MENU, self.onPopupOpenViewPath, id=self.popup_open_view_path)
        self.Bind(wx.EVT_MENU, self.onPopupOpenUrlPath, id=self.popup_open_url_path)
        self.Bind(wx.EVT_MENU, self.onPopupOpenUrlPathWx, id=self.popup_open_url_path_wx)
        self.Bind(wx.EVT_MENU, self.onPopupOpenViewPathWx, id=self.popup_open_view_path_wx)
        self.Bind(wx.EVT_MENU, self.onPopupModifyUrl, id=self.popup_modify_url)
        self.Bind(wx.EVT_MENU, self.onPopupInsertFunc, id=self.popup_insert_func)
        self.Bind(wx.EVT_MENU, self.onPopupGetCode, id=self.popup_get_code)
        self.Bind(wx.EVT_MENU, self.onPopupShowMvcMtv, id=self.popup_show_mvc_mtv)
        
        menu = wx.Menu()
        menu.Append(self.popup_open_url, "在浏览器中打开")
        menu.AppendSeparator()

        menuVSCode = wx.Menu()
        menuVSCode.Append(self.popup_open_view_path, "打开views文件")
        menuVSCode.Append(self.popup_open_url_path, "打开urls文件")
        menuVSCode.Append(self.popup_open_model_path, "打开models文件")
        menu.Append(wx.ID_ANY, "&Visual Studio Code", menuVSCode)

        menuWxEditor = wx.Menu()
        menuWxEditor.Append(self.popup_open_view_path_wx, "打开views文件")
        menuWxEditor.Append(self.popup_open_url_path_wx, "打开urls文件")
        menu.Append(wx.ID_ANY, "&自定义编辑器", menuWxEditor)

        menu.AppendSeparator()
        menu.Append(self.popup_modify_url, "修改路由路径")
        menu.AppendSeparator()
        menu.Append(self.popup_get_code, "代码片段")
        menu.Append(self.popup_insert_func, "插入功能")
        menu.AppendSeparator()
        menu.Append(self.popup_show_mvc_mtv, "MVC/MTV数据流概览")
        self.PopupMenu(menu)
        menu.Destroy()

    def onItemSelect(self, e):
        """行选择"""
        obj: wxdv.DataViewItem = e.GetItem() # 主要用于检测行是否正确选中数据行
        if obj.IsOk():
            self.select_row = self.model.GetRowDictValue(obj)
        else:
            self.select_row = {}

    def onBtnRefresh(self, e):
        """刷新界面"""
        self.treeListData.ClearColumns()
        self._init_listree_data()
        self.Layout()

        env_python3 = env.getPython3Env()
        if not os.path.exists(env_python3):
            RichMsgDialog.showOkMsgDialog(self, "检测到虚拟环境未绑定，数据显示可能不准确，请绑定后返回本界面刷新显示", "警告")

    def onPopupOpenUrl(self, e):
        """在浏览器中打开"""
        import webbrowser
        if self.select_row:
            webbrowser.open(self.select_row.get("full_path"))

    def onPopupOpenViewPath(self, e):
        """打开views文件"""
        if self.select_row:
            t_way = self.select_row['gen_way'].strip()
            left_code = t_way.find("(")
            if -1 == left_code:
                t_way = t_way.split(".")
            else:
                t_way = t_way[:left_code].split(".")
            if len(t_way) >= 1:
                if "as_view" == t_way[-1].strip():
                    t_way = t_way[-2].strip()
                else:
                    t_way = t_way[-1].strip()
            else:
                t_way = ""
            row, col, view_path = djangotools.get_location_from_viewspy(
                self.select_row['belong_app'],
                t_way,
            ) # 光标定位
            if view_path:
                cmd = f"code -g {view_path}:{row}:{col}"
                wx.Shell(cmd)
            else:
                RichMsgDialog.showOkMsgDialog(self, "找不到匹配项", "警告")

    def onPopupOpenUrlPath(self, e):
        """打开urls文件"""
        if self.select_row:
            row, col = 1, 0 # 光标定位：第一行，第一个字符之前
            cmd = f"code -g {self.select_row['app_file']}:{row}:{col}"
            wx.Shell(cmd)
        
    def onPopupModifyUrl(self, e): """修改路由路径"""
    def onPopupInsertFunc(self, e): """插入功能"""
    def onPopupGetCode(self, e): """代码片段"""
    def onPopupShowMvcMtv(self, e): """MVC/MTV数据流概览"""
    def onPopupOpenUrlPathWx(self, e): """自定义打开urls文件"""
    def onPopupOpenViewPathWx(self, e): """自定义打开views文件"""

