import wx, os
import wx.lib.buttons as buttons
import wx.html2
from ..tools._tools import *
from .. settings import DJANGO_DOCS_URL, LOCAL_DOCS_PATH
from ..tools import environment as env
from ..tools import models as toolModel
from ..miniCmd.djangoCmd import *

class DocumentationDialog(wx.Dialog):

    def __init__(self, parent):

        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = '帮助文档', size=(1200, 800), style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER)
        
        labels = wx.Notebook(self)
        self.officialdocs = wx.Panel(labels) # 官方文档
        self.modelsPanel = wx.Panel(labels) # 模型
        self.viewsPanel = wx.Panel(labels) # 视图
        self.urlsPanel = wx.Panel(labels) # 路由
        self.templatesPanel = wx.Panel(labels) # 模板
        self.formsPanel = wx.Panel(labels) # 表单
        self.adminsPanel = wx.Panel(labels) # 管理中心
        self.databasesPanel = wx.Panel(labels) # 数据库

        self._init_officialdocs()
        self._init_modelsPanel()
        self._init_viewsPanel()
        self._init_urlsPanel()
        self._init_templatesPanel()
        self._init_formsPanel()
        self._init_adminsPanel()
        self._init_databasesPanel()

        labels.AddPage(self.modelsPanel, '模型')
        labels.AddPage(self.viewsPanel, '视图')
        labels.AddPage(self.urlsPanel, '路由')
        labels.AddPage(self.templatesPanel, '模板')
        labels.AddPage(self.formsPanel, '表单')
        labels.AddPage(self.adminsPanel, '管理中心')
        labels.AddPage(self.databasesPanel, '数据库')
        labels.AddPage(self.officialdocs, '官方文档')

    def _init_officialdocs(self):
        """官方文档初始化"""
        self.splitOfficialdocs = wx.SplitterWindow(self.officialdocs, -1)
        self.leftPanelOfficialdocs = wx.Panel(self.splitOfficialdocs, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanelOfficialdocs = wx.Panel(self.splitOfficialdocs, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitOfficialdocs.Initialize(self.leftPanelOfficialdocs)
        self.splitOfficialdocs.Initialize(self.rightPanelOfficialdocs)
        self.rightPanelOfficialdocs.SetBackgroundColour("gray")
        self.splitOfficialdocs.SplitVertically(self.leftPanelOfficialdocs, self.rightPanelOfficialdocs, 200)

        self.leftPanelOfficialdocsSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftPanelOfficialdocsSizer.Add(self.splitOfficialdocs, 1, wx.EXPAND | wx.ALL, 0)
        self.officialdocs.SetSizer(self.leftPanelOfficialdocsSizer)

        # 左子面板  树控件
        leftPanelOfficialdocsSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftPanelOfficialdocsTree = wx.TreeCtrl(self.leftPanelOfficialdocs, -1, wx.DefaultPosition, (-1, -1))
        leftPanelOfficialdocsSizer.Add(self.leftPanelOfficialdocsTree, 1, wx.EXPAND | wx.ALL, 2)
        self.leftPanelOfficialdocs.SetSizer(leftPanelOfficialdocsSizer)
        self._init_officialdocs_tree()

        # 右子面板  HTML控件
        rightPanelOfficialdocsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.browser = wx.html2.WebView.New(self.rightPanelOfficialdocs)
        # self.browser.LoadURL(DJANGO_DOCS_URL['31']) # 加载页面
        # html_string = read_file(DJANGO_DOCS_PATH)
        # self.browser.SetPage(html_string, "") # 加载字符串
        rightPanelOfficialdocsSizer.Add(self.browser, 1, wx.EXPAND | wx.ALL, 2)
        self.rightPanelOfficialdocs.SetSizer(rightPanelOfficialdocsSizer)

        # 事件绑定
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnClickOfficalDocsTree, self.leftPanelOfficialdocsTree)

    def _init_officialdocs_tree(self):
        """构建左-左目录树"""
        self.leftPanelOfficialdocsRoot = self.leftPanelOfficialdocsTree.AddRoot(f'稳定版本')
        self.leftPanelOfficialdocsTree.AppendItem(self.leftPanelOfficialdocsRoot, "3.1版本")
        self.leftPanelOfficialdocsTree.AppendItem(self.leftPanelOfficialdocsRoot, "2.2版本")
        self.leftPanelOfficialdocsTree.AppendItem(self.leftPanelOfficialdocsRoot, "国家法律法规数据库")

        self.leftPanelOfficialdocsTree.ExpandAll() # 展开所有节点

    def OnClickOfficalDocsTree(self, e):
        """双击官方文档树控件事件"""
        nodeName = self.leftPanelModelsTree.GetItemText(e.GetItem())
        temp = {
            '3.1版本' : '31',
            '2.2版本' : '22',
            '国家法律法规数据库' : 'law',
        }
        if nodeName != f'选择版本':
            self.browser.LoadURL(DJANGO_DOCS_URL[temp[nodeName]])

    def _init_modelsPanel(self):
        """模型界面初始化"""
        self.splitModelsWindow = wx.SplitterWindow(self.modelsPanel, -1)
        self.leftPanelModels = wx.Panel(self.splitModelsWindow, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanelModels = wx.Panel(self.splitModelsWindow, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitModelsWindow.Initialize(self.leftPanelModels)
        self.splitModelsWindow.Initialize(self.rightPanelModels)
        self.rightPanelModels.SetBackgroundColour("gray")
        self.splitModelsWindow.SplitVertically(self.leftPanelModels, self.rightPanelModels, 200)

        self.modelsPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.modelsPanelSizer.Add(self.splitModelsWindow, 1, wx.EXPAND | wx.ALL, 0)
        self.modelsPanel.SetSizer(self.modelsPanelSizer)

        # 左子面板  树控件
        leftPanelModelsSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftPanelModelsTree = wx.TreeCtrl(self.leftPanelModels, -1, wx.DefaultPosition, (-1, -1))
        leftPanelModelsSizer.Add(self.leftPanelModelsTree, 1, wx.EXPAND | wx.ALL, 2)
        self.leftPanelModels.SetSizer(leftPanelModelsSizer)
        self._init_modelsPanel_tree()

        # 右子面板  HTML控件
        rightPanelModelsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.browserModels = wx.html2.WebView.New(self.rightPanelModels) # style=wx.html.HW_NO_SelectION 不可选中文本
        # self.browser.LoadURL(DJANGO_DOCS_URL['31']) # 加载页面
        # html_string = read_file(DJANGO_DOCS_PATH)
        # self.browser.SetPage(html_string, "") # 加载字符串
        rightPanelModelsSizer.Add(self.browserModels, 1, wx.EXPAND | wx.ALL, 2)
        self.rightPanelModels.SetSizer(rightPanelModelsSizer)

        # 事件绑定
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnClickModelsTree, self.leftPanelModelsTree)

    def _init_modelsPanel_tree(self):
        """构建左-左目录树"""
        self.leftPanelModelsRoot = self.leftPanelModelsTree.AddRoot(f'模型文档-个人总结')
        self.leftPanelModelsTree.AppendItem(self.leftPanelModelsRoot, "简单介绍")
        t = self.leftPanelModelsTree.AppendItem(self.leftPanelModelsRoot, "创建")
        self.leftPanelModelsTree.AppendItem(t, "一般步骤")
        zd = self.leftPanelModelsTree.AppendItem(t, "字段")
        self.leftPanelModelsTree.AppendItem(zd, "通用参数选项")
        self.leftPanelModelsTree.AppendItem(zd, "整型")
        self.leftPanelModelsTree.AppendItem(zd, "浮点型")
        self.leftPanelModelsTree.AppendItem(zd, "字符型")
        self.leftPanelModelsTree.AppendItem(zd, "日期型")
        self.leftPanelModelsTree.AppendItem(zd, "布尔型")
        self.leftPanelModelsTree.AppendItem(zd, "文件类型")
        glgx = self.leftPanelModelsTree.AppendItem(t, "关联关系")
        self.leftPanelModelsTree.AppendItem(glgx, "一对一")
        self.leftPanelModelsTree.AppendItem(glgx, "多对一")
        self.leftPanelModelsTree.AppendItem(glgx, "多对多")
        self.leftPanelModelsTree.AppendItem(self.leftPanelModelsRoot, "默认行为")
        self.leftPanelModelsTree.AppendItem(self.leftPanelModelsRoot, "管理器")
        self.leftPanelModelsTree.AppendItem(self.leftPanelModelsRoot, "使用")

        self.leftPanelModelsTree.ExpandAll() # 展开所有节点
    
    def OnClickModelsTree(self, e):
        """双击树节点事件"""
        temp = {
            '简单介绍' : 'models_introduce.html',

            '创建' : '',
            '一般步骤' : 'models_create_introduce.html',
            '字段' : '',
            '通用参数选项' : 'models_create_attrs_options.html',
            '整型' : 'models_create_attrs_integer.html',
            '浮点型' : 'models_create_attrs_float.html',
            '字符型' : 'models_create_attrs_char.html',
            '日期型' : 'models_create_attrs_date.html',
            '布尔型' : 'models_create_attrs_bool.html',
            '文件类型' : 'models_create_attrs_file.html',
            '关联关系' : '',
            '一对一' : 'models_create_relate_one2one.html',
            '多对一' : 'models_create_relate_more2one.html',
            '多对多' : 'models_create_relate_more2more.html',

            '默认行为' : 'models_create_modify_default.html',

            '管理器' : 'models_controller.html',
            '使用' : 'models_user.html',
        }
        unuse = ('模型文档-个人总结', '字段', '创建', '关联关系')
        nodeName = self.leftPanelModelsTree.GetItemText(e.GetItem())
        if nodeName not in unuse:
            self.browserModels.SetPage(read_file(os.path.join(LOCAL_DOCS_PATH, temp[nodeName])), "")

    def _init_viewsPanel(self):
        """视图界面初始化"""
        self.splitViewsWindow = wx.SplitterWindow(self.viewsPanel, -1)
        self.leftPanelViews = wx.Panel(self.splitViewsWindow, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanelViews = wx.Panel(self.splitViewsWindow, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitViewsWindow.Initialize(self.leftPanelViews)
        self.splitViewsWindow.Initialize(self.rightPanelViews)
        self.rightPanelViews.SetBackgroundColour("gray")
        self.splitViewsWindow.SplitVertically(self.leftPanelViews, self.rightPanelViews, 200)

        self.viewsPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.viewsPanelSizer.Add(self.splitViewsWindow, 1, wx.EXPAND | wx.ALL, 0)
        self.viewsPanel.SetSizer(self.viewsPanelSizer)

    def _init_urlsPanel(self):
        """路由界面初始化"""
        self.splitUrlsWindow = wx.SplitterWindow(self.urlsPanel, -1)
        self.leftPanelUrls = wx.Panel(self.splitUrlsWindow, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanelUrls = wx.Panel(self.splitUrlsWindow, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitUrlsWindow.Initialize(self.leftPanelUrls)
        self.splitUrlsWindow.Initialize(self.rightPanelUrls)
        self.rightPanelUrls.SetBackgroundColour("gray")
        self.splitUrlsWindow.SplitVertically(self.leftPanelUrls, self.rightPanelUrls, 200)

        self.urlsPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.urlsPanelSizer.Add(self.splitUrlsWindow, 1, wx.EXPAND | wx.ALL, 0)
        self.urlsPanel.SetSizer(self.urlsPanelSizer)

    def _init_templatesPanel(self):
        """模板界面初始化"""
        self.splitTemplatesWindow = wx.SplitterWindow(self.templatesPanel, -1)
        self.leftPanelTemplates = wx.Panel(self.splitTemplatesWindow, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanelTemplates = wx.Panel(self.splitTemplatesWindow, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitTemplatesWindow.Initialize(self.leftPanelTemplates)
        self.splitTemplatesWindow.Initialize(self.rightPanelTemplates)
        self.rightPanelTemplates.SetBackgroundColour("gray")
        self.splitTemplatesWindow.SplitVertically(self.leftPanelTemplates, self.rightPanelTemplates, 200)

        self.templatesPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.templatesPanelSizer.Add(self.splitTemplatesWindow, 1, wx.EXPAND | wx.ALL, 0)
        self.templatesPanel.SetSizer(self.templatesPanelSizer)

    def _init_formsPanel(self):
        """表单界面初始化"""
        self.splitFormsWindow = wx.SplitterWindow(self.formsPanel, -1)
        self.leftPanelForms = wx.Panel(self.splitFormsWindow, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanelForms = wx.Panel(self.splitFormsWindow, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitFormsWindow.Initialize(self.leftPanelForms)
        self.splitFormsWindow.Initialize(self.rightPanelForms)
        self.rightPanelForms.SetBackgroundColour("gray")
        self.splitFormsWindow.SplitVertically(self.leftPanelForms, self.rightPanelForms, 200)

        self.formsPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.formsPanelSizer.Add(self.splitFormsWindow, 1, wx.EXPAND | wx.ALL, 0)
        self.formsPanel.SetSizer(self.formsPanelSizer)

    def _init_adminsPanel(self):
        """管理中心界面初始化"""
        self.splitAdminsWindow = wx.SplitterWindow(self.adminsPanel, -1)
        self.leftPanelAdmins = wx.Panel(self.splitAdminsWindow, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanelAdmins = wx.Panel(self.splitAdminsWindow, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitAdminsWindow.Initialize(self.leftPanelAdmins)
        self.splitAdminsWindow.Initialize(self.rightPanelAdmins)
        self.rightPanelAdmins.SetBackgroundColour("gray")
        self.splitAdminsWindow.SplitVertically(self.leftPanelAdmins, self.rightPanelAdmins, 200)

        self.adminsPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.adminsPanelSizer.Add(self.splitAdminsWindow, 1, wx.EXPAND | wx.ALL, 0)
        self.adminsPanel.SetSizer(self.adminsPanelSizer)

    def _init_databasesPanel(self):
        """数据库界面初始化"""
        self.splitDatabasesWindow = wx.SplitterWindow(self.databasesPanel, -1)
        self.leftPanelDatabases = wx.Panel(self.splitDatabasesWindow, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanelDatabases = wx.Panel(self.splitDatabasesWindow, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitDatabasesWindow.Initialize(self.leftPanelDatabases)
        self.splitDatabasesWindow.Initialize(self.rightPanelDatabases)
        self.rightPanelDatabases.SetBackgroundColour("gray")
        self.splitDatabasesWindow.SplitVertically(self.leftPanelDatabases, self.rightPanelDatabases, 200)

        self.databasesPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.databasesPanelSizer.Add(self.splitDatabasesWindow, 1, wx.EXPAND | wx.ALL, 0)
        self.databasesPanel.SetSizer(self.databasesPanelSizer)
