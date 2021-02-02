import wx, json, glob, os
import wx.lib.buttons as buttons
from wx.lib import scrolledpanel
from ..tools._tools import *
from ..tools._re import *
from ..settings import BASE_DIR, CONFIG_PATH, SETTINGSS
from ..tools import environment as env
from ..tools import models as toolModel
from ..miniCmd.djangoCmd import *
from ..constant import *

class ViewGenerateDialog(wx.Dialog):

    def __init__(self, parent):

        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = '新增视图', size=(700, 600))

        # 一些控制容器
        self.labelStaticTexts = []

        self._init_UI()

        # 布局后，美化界面
        self._init_label_font()

    def _init_UI(self):
        """初始化界面布局"""
        # 总面板
        self.panel = wx.Panel(self)
        self.panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.panelSizer)

        # 选择视图写入文件路径
        self.selectFilePanel = wx.Panel(self.panel)
        self.selectFileBox = wx.BoxSizer(wx.HORIZONTAL)
        self.selectFilePanel.SetSizer(self.selectFileBox)
        self.panelSizer.Add(self.selectFilePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.btnWritePath = buttons.GenButton(self.selectFilePanel, -1, '选择视图写入路径')
        self.filePath = wx.TextCtrl(self.selectFilePanel, -1, style=wx.ALIGN_LEFT)
        self.selectFileBox.Add(self.btnWritePath, 0, wx.EXPAND | wx.ALL, 2)
        self.selectFileBox.Add(self.filePath, 1, wx.EXPAND | wx.ALL, 2)
        self.filePath.Enable(False)

        # 选择类型视图
        self.choiceViewTypeStaticBox = wx.StaticBox(self.panel, -1, '')
        self.viewTypePanel = wx.StaticBoxSizer(self.choiceViewTypeStaticBox, wx.HORIZONTAL)
        self.panelSizer.Add(self.viewTypePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelChoiceViewType = wx.StaticText(self.panel, -1, "选择要创建的视图类型：", style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.choiceViewType = wx.Choice(self.panel, -1, choices=[' ',]+CON_VIEW_CHOICES)
        self.viewTypePanel.Add(self.labelChoiceViewType, 0, wx.EXPAND | wx.ALL, 2)
        self.viewTypePanel.Add(self.choiceViewType, 1, wx.EXPAND | wx.ALL, 2)


        # 标签美化
        self.labelStaticTexts.extend([
            self.labelChoiceViewType,
        ])





        # 代码预览面板
        self.codeReviewPanel = wx.Panel(self.panel)
        self.codeReviewPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.codeReviewPanel.SetSizer(self.codeReviewPanelSizer)
        self.panelSizer.Add(self.codeReviewPanel, 1, wx.EXPAND | wx.ALL, 2)

        self.inputCodeReview = wx.TextCtrl(self.codeReviewPanel, -1, style=wx.TE_MULTILINE)
        self.codeReviewPanelSizer.Add(self.inputCodeReview, 1, wx.EXPAND | wx.ALL, 2)

        # 函数命名
        tempWayNamePanel = wx.StaticBox(self.panel, -1, '函数/类命名')
        self.wayNamePanel = wx.StaticBoxSizer(tempWayNamePanel, wx.HORIZONTAL)
        self.panelSizer.Add(self.wayNamePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.inputWayName = wx.TextCtrl(self.panel, -1, style = wx.ALIGN_LEFT)
        self.wayNamePanel.Add(self.inputWayName, 1, wx.EXPAND | wx.ALL, 2)

        # 是否自动生成路由
        self.openUrlAliasPanel = wx.RadioBox(self.panel, -1, "自动生成路由", choices=['开启', '关闭'])
        self.openUrlAliasPanel.SetSelection(1) # 默认不开启
        self.panelSizer.Add(self.openUrlAliasPanel, 0, wx.EXPAND | wx.ALL, 2)

        # 路由别名
        tempUrlNamePanel = wx.StaticBox(self.panel, -1, '路由别名（不填写默认取函数名/类名）')
        self.urlNamePanel = wx.StaticBoxSizer(tempUrlNamePanel, wx.HORIZONTAL)
        self.panelSizer.Add(self.urlNamePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.inputUrlName = wx.TextCtrl(self.panel, -1, style = wx.ALIGN_LEFT)
        self.urlNamePanel.Add(self.inputUrlName, 1, wx.EXPAND | wx.ALL, 2)

        # 路由预览
        tempUrlViewPanel = wx.StaticBox(self.panel, -1, '路由预览')
        self.urlViewPanel = wx.StaticBoxSizer(tempUrlViewPanel, wx.HORIZONTAL)
        self.panelSizer.Add(self.urlViewPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.inputUrlView = wx.TextCtrl(self.panel, -1, style = wx.ALIGN_LEFT)
        self.urlViewPanel.Add(self.inputUrlView, 1, wx.EXPAND | wx.ALL, 2)
        self.inputUrlView.Enable(False)

        # 末尾控件
        self.btnSubmit = buttons.GenButton(self.panel, -1, '创建')
        self.panelSizer.Add(self.btnSubmit, 0, wx.EXPAND | wx.ALL, 2)

        # 事件
        self.Bind(wx.EVT_BUTTON, self.onBtnSelectPath, self.btnWritePath)
        
    def _init_label_font(self):
        """标签提示信息字体初始化"""
        for _ in self.labelStaticTexts:
            _.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            _.SetForegroundColour(CON_COLOR_BLUE)

    def onRadiosClick(self, e):
        """"""
        # print(self.radiosPanel.GetSelection()) # 获取当前选中元素的下标
        pass

    def onBtnSelectPath(self, e):
        """选择写入文件位置"""
        dirname = get_configs(CONFIG_PATH)['dirname']
        dlg = wx.FileDialog(self, "选择写入文件", dirname, "", "*.py", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            self.filePath.SetValue(os.path.join(dirname, filename))
        dlg.Close(True)
