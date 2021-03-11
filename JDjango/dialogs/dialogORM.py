import wx
import wx.html2
from .dialogTips import *
from ..tools._tools import *
from ..miniCmd import djangoCmd as djcmd
from ..settings import CONFIG_PATH

"""
### 为一键生成器添加新的ORM模板
#1 创建模板HTML文件，并在 djangoCmd.py 文件的 get_orm_code 方法中进行关联
#2 在本文件的 _init_tree 方法的 types 中添加前端显示名称（最好与HTML文件名一致）
#3 若有新的模板变量，需在 html_string 中注册，否则模板引擎将无法工作

"""

class ORMDialog(wx.Dialog):
    
    def __init__(self, parent, **kwargs):
        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = "ORM一键生成系统", size=(888, 540), style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER)

        self._init_UI()

        self._init_tree()

    def _init_UI(self):
        """初始化界面布局"""
        self.mainPanel = wx.Panel(self)
        mainPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainPanel.SetSizer(mainPanelSizer)

        self.splitWindow = wx.SplitterWindow(self.mainPanel, -1)
        self.leftPanel = wx.Panel(self.splitWindow, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanel = wx.Panel(self.splitWindow, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitWindow.Initialize(self.leftPanel)
        self.splitWindow.Initialize(self.rightPanel)
        self.splitWindow.SplitVertically(self.leftPanel, self.rightPanel, 180)
        mainPanelSizer.Add(self.splitWindow, 1, wx.EXPAND | wx.ALL, 0)

        self._init_left_panel()
        self._init_right_panel()

    def _init_left_panel(self):
        """左子面板"""
        leftPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftPanel.SetSizer(leftPanelSizer)

        self.tree = wx.TreeCtrl(self.leftPanel, -1, wx.DefaultPosition, (-1, -1)) # , wx.TR_HAS_BUTTONS
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnClickTree, self.tree)
        leftPanelSizer.Add(self.tree, 1, wx.EXPAND | wx.ALL, 2)

    def _init_right_panel(self):
        """右子面板"""
        rightPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.rightPanel.SetSizer(rightPanelSizer)

        self.browser = wx.html2.WebView.New(self.rightPanel) # style=wx.html.HW_NO_SelectION 不可选中文本
        rightPanelSizer.Add(self.browser, 1, wx.EXPAND | wx.ALL, 2)

    def OnClickTree(self, e):
        """双击树节点事件"""
        clickNodeName = self.tree.GetItemText(e.GetItem())
        if "应用程序" == clickNodeName:
            return

        parentNode = self.tree.GetItemParent(e.GetItem())
        nodeName = self.tree.GetItemText(parentNode)
        if clickNodeName not in self.untouched:

            # 各类替换值
            all_args = "name='example', ..." # 所有参数的关键字赋值语句，中间用英文逗号隔开
            foreign_attr_name = 'tempAttr' # ForeignKey 在本模型中的属性名
            foreign_model_name = 'ForeignModel' # ForeignKey 模型名称
            m2m_attr_name = 'tempAttr' # ManyToManyField 在本模型中的属性名
            m2m_model_name = 'ManyToManyModel' # ManyToManyField 模型名称

            html_string = ''.join(djcmd.get_orm_code(
                mode = clickNodeName
                , model_name = nodeName
                , all_args = all_args
                , foreign_attr_name = foreign_attr_name
                , foreign_model_name = foreign_model_name
                , m2m_attr_name = m2m_attr_name
                , m2m_model_name = m2m_model_name

            ))
            self.browser.SetPage(html_string, "") # 加载字符串
        else:
            """双击展开当前节点"""
            self.tree.Expand(e.GetItem())

    def _init_tree(self):
        """构建左-左目录树"""
        self.untouched = []

        self.root = self.tree.AddRoot("应用程序")
        app_names = get_configs(CONFIG_PATH)['app_names'] # 取所有的应用程序名

        if app_names:
            self.untouched.extend(app_names)
            types = ['SELECT', 'INSERT', 'DELETE', 'UPDATE', 'JOIN', 'FIELD', 'AGGREGATE', 'TOOLS',]
            for app_name in app_names:
                temp = self.tree.AppendItem(self.root, app_name)
                models = djcmd.get_models_by_appname(app_name) # 通过应用程序名获取所有的模型名称
                if models:
                    self.untouched.extend(models)
                    for model in models:
                        temp_model = self.tree.AppendItem(temp, model)
                        for _ in types:
                            self.tree.AppendItem(temp_model, _)
                self.tree.Expand(temp)

        self.untouched.extend([
            "应用程序",
        ])

        self.tree.Expand(self.root)
    