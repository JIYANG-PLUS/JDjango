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
from .dialogTips import *

"""
### 使用者自定义视图模板并为此模板编辑逻辑的步骤：【后期补全】

"""

LABEL_COL_LEN = 200

class ViewGenerateDialog(wx.Dialog):

    def __init__(self, parent):

        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = '新增视图', size=(920, 600))

        # 一些控制容器
        self.labelStaticTexts = []
        self.allCtrlsWithoutType = [] # 选择参数

        self._init_UI()

        # 布局后，美化界面
        self._init_label_font()
        self._init_all_args()
        self._unshow_allctrls_withouttype()

    def _init_UI(self):
        """初始化界面布局"""
        # 总面板
        self.panel = wx.Panel(self)
        self.panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.panelSizer)

        # 分割面板（左右分割）
        self.splitWindow = wx.SplitterWindow(self.panel, -1)
        self.panelSizer.Add(self.splitWindow, 1, wx.EXPAND | wx.ALL, 2)

        # 左子面板
        self.leftPanel = wx.Panel(self.splitWindow, style=wx.SUNKEN_BORDER)
        self.leftPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftPanel.SetSizer(self.leftPanelSizer )
        
        # 右子面板
        self.rightPanel = wx.Panel(self.splitWindow, style=wx.SUNKEN_BORDER)
        self.rightPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.rightPanel.SetSizer(self.rightPanelSizer)
        
        self.splitWindow.Initialize(self.leftPanel)
        self.splitWindow.Initialize(self.rightPanel)
        self.splitWindow.SplitVertically(self.leftPanel, self.rightPanel, 520)

        self._init_left_panel()
        self._init_right_panel()

        # 模板变量
        self.views_template = ''
        self.argsStruct = {} #存放模板内容替换的所有内容

    def _unshow_allctrls_withouttype(self):
        """隐藏所有的非类型选择交互式控件"""
        for _ in self.allCtrlsWithoutType:
            _.Show(False)

    def _show_allctrls_withouttype(self):
        """显示所有的非类型选择交互式控件"""
        for _ in self.allCtrlsWithoutType:
            _.Show(True)

    def _init_left_panel(self):
        """初始化左子面板"""
        # 滚动面板
        self.leftScrollPanel = scrolledpanel.ScrolledPanel(self.leftPanel, -1)
        self.leftScrollPanel.SetupScrolling()
        leftScrollPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftScrollPanel.SetSizer(leftScrollPanelSizer)
        self.leftPanelSizer.Add(self.leftScrollPanel, 1, wx.EXPAND | wx.ALL, 2)

        # 选择文件写入路径【此处更改为选择App】
        self.selectFilePanelStaticBox = wx.StaticBox(self.leftScrollPanel, -1, '')
        self.selectFilePanel = wx.StaticBoxSizer(self.selectFilePanelStaticBox, wx.HORIZONTAL)
        leftScrollPanelSizer.Add(self.selectFilePanel, 0, wx.EXPAND | wx.ALL, 2)
        # self.selectFilePanel.SetBackgroundColour(CON_COLOR_BLACK) # CON_COLOR_PURE_WHITE

        self.labelSelectFile = wx.StaticText(self.leftScrollPanel, -1, "选择视图所属的应用程序", size=(LABEL_COL_LEN, -1))
        self.choiceSelectFile = wx.Choice(self.leftScrollPanel, -1, choices=[' ',]+get_all_apps_name())
        self.selectFilePanel.Add(self.labelSelectFile, 0, wx.EXPAND | wx.ALL, 2)
        self.selectFilePanel.Add(self.choiceSelectFile, 1, wx.EXPAND | wx.ALL, 2)
        # self.labelSelectFile.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        # 选择视图类型
        self.choiceViewTypeStaticBox = wx.StaticBox(self.leftScrollPanel, -1, '')
        self.viewTypePanel = wx.StaticBoxSizer(self.choiceViewTypeStaticBox, wx.HORIZONTAL)
        leftScrollPanelSizer.Add(self.viewTypePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelChoiceViewType = wx.StaticText(self.leftScrollPanel, -1, "选择要创建的视图类型：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_COL_LEN, -1))
        self.choiceViewType = wx.Choice(self.leftScrollPanel, -1, choices=[' ',]+CON_VIEW_CHOICES)
        self.viewTypePanel.Add(self.labelChoiceViewType, 0, wx.EXPAND | wx.ALL, 2)
        self.viewTypePanel.Add(self.choiceViewType, 1, wx.EXPAND | wx.ALL, 2)

        # 视图名称
        self.inputViewNameStaticBox = wx.StaticBox(self.leftScrollPanel, -1, '')
        self.inputViewNamePanel = wx.StaticBoxSizer(self.inputViewNameStaticBox, wx.HORIZONTAL)
        leftScrollPanelSizer.Add(self.inputViewNamePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputViewName = wx.StaticText(self.leftScrollPanel, -1, "视图名称：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_COL_LEN, -1))
        self.inputViewName = wx.TextCtrl(self.leftScrollPanel, -1, style = wx.ALIGN_LEFT)
        self.inputViewNamePanel.Add(self.labelInputViewName, 0, wx.EXPAND | wx.ALL, 2)
        self.inputViewNamePanel.Add(self.inputViewName, 1, wx.EXPAND | wx.ALL, 2)

        # 路由反向解析名称【默认取 视图名称】
        self.inputReverseViewNameStaticBox = wx.StaticBox(self.leftScrollPanel, -1, '')
        self.inputReverseViewNamePanel = wx.StaticBoxSizer(self.inputReverseViewNameStaticBox, wx.HORIZONTAL)
        leftScrollPanelSizer.Add(self.inputReverseViewNamePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputReverseViewName = wx.StaticText(self.leftScrollPanel, -1, "反向解析名称：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_COL_LEN, -1))
        self.inputReverseViewName = wx.TextCtrl(self.leftScrollPanel, -1, style = wx.ALIGN_LEFT)
        self.inputReverseViewNamePanel.Add(self.labelInputReverseViewName, 0, wx.EXPAND | wx.ALL, 2)
        self.inputReverseViewNamePanel.Add(self.inputReverseViewName, 1, wx.EXPAND | wx.ALL, 2)

        # 路由路径指定
        self.inputUrlPathStaticBox = wx.StaticBox(self.leftScrollPanel, -1, '')
        self.inputUrlPathPanel = wx.StaticBoxSizer(self.inputUrlPathStaticBox, wx.HORIZONTAL)
        leftScrollPanelSizer.Add(self.inputUrlPathPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputUrlPath = wx.StaticText(self.leftScrollPanel, -1, "路径和参数：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_COL_LEN, -1))
        self.inputUrlPath = wx.TextCtrl(self.leftScrollPanel, -1, style = wx.ALIGN_LEFT)
        self.inputUrlPathPanel.Add(self.labelInputUrlPath, 0, wx.EXPAND | wx.ALL, 2)
        self.inputUrlPathPanel.Add(self.inputUrlPath, 1, wx.EXPAND | wx.ALL, 2)

        # 路由预览
        self.inputUrlPreviewStaticBox = wx.StaticBox(self.leftScrollPanel, -1, '')
        self.inputUrlPreviewPanel = wx.StaticBoxSizer(self.inputUrlPreviewStaticBox, wx.HORIZONTAL)
        leftScrollPanelSizer.Add(self.inputUrlPreviewPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputUrlPreview = wx.StaticText(self.leftScrollPanel, -1, "路由预览：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_COL_LEN, -1))
        self.inputUrlPreview = wx.TextCtrl(self.leftScrollPanel, -1, style = wx.ALIGN_LEFT)
        self.inputUrlPreviewPanel.Add(self.labelInputUrlPreview, 0, wx.EXPAND | wx.ALL, 2)
        self.inputUrlPreviewPanel.Add(self.inputUrlPreview, 1, wx.EXPAND | wx.ALL, 2)
        self.inputUrlPreview.Enable(False)

        # 响应对象
        self.choiceReturnTypeStaticBox = wx.StaticBox(self.leftScrollPanel, -1, '')
        self.choiceReturnTypePanel = wx.StaticBoxSizer(self.choiceReturnTypeStaticBox, wx.HORIZONTAL)
        leftScrollPanelSizer.Add(self.choiceReturnTypePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelChoiceReturnType = wx.StaticText(self.leftScrollPanel, -1, "响应对象：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_COL_LEN, -1))
        self.choiceReturnType = wx.Choice(self.leftScrollPanel, -1, choices=[' ',] + CON_VIEWS_RETURN_TYPE)
        self.choiceReturnTypePanel.Add(self.labelChoiceReturnType, 0, wx.EXPAND | wx.ALL, 2)
        self.choiceReturnTypePanel.Add(self.choiceReturnType, 1, wx.EXPAND | wx.ALL, 2)

        # 快捷响应对象
        self.choiceShortcutsStaticBox = wx.StaticBox(self.leftScrollPanel, -1, '')
        self.choiceShortcutsPanel = wx.StaticBoxSizer(self.choiceShortcutsStaticBox, wx.HORIZONTAL)
        leftScrollPanelSizer.Add(self.choiceShortcutsPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelChoiceShortcuts = wx.StaticText(self.leftScrollPanel, -1, "快捷响应对象：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_COL_LEN, -1))
        self.choiceShortcuts = wx.Choice(self.leftScrollPanel, -1, choices=[' ',] + CON_VIEWS_SHORTCUTS)
        self.choiceShortcutsPanel.Add(self.labelChoiceShortcuts, 0, wx.EXPAND | wx.ALL, 2)
        self.choiceShortcutsPanel.Add(self.choiceShortcuts, 1, wx.EXPAND | wx.ALL, 2)

        # 装饰器
        self.choiceDecoratorsStaticBox = wx.StaticBox(self.leftScrollPanel, -1, '')
        self.choiceDecoratorsPanel = wx.StaticBoxSizer(self.choiceDecoratorsStaticBox, wx.HORIZONTAL)
        leftScrollPanelSizer.Add(self.choiceDecoratorsPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelChoiceDecorators = wx.StaticText(self.leftScrollPanel, -1, "装饰器：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_COL_LEN, -1))
        self.choiceDecorators = wx.Choice(self.leftScrollPanel, -1, choices=[' ',] + CON_VIEWS_DECORATORS)
        self.choiceDecoratorsPanel.Add(self.labelChoiceDecorators, 0, wx.EXPAND | wx.ALL, 2)
        self.choiceDecoratorsPanel.Add(self.choiceDecorators, 1, wx.EXPAND | wx.ALL, 2)

        # 按钮
        # self.btnRetrySelect = buttons.GenButton(self.leftScrollPanel, -1, '重新选择视图类型')
        self.btnSubmit = buttons.GenButton(self.leftScrollPanel, -1, '创建')
        # leftScrollPanelSizer.Add(self.btnRetrySelect, 0, wx.EXPAND | wx.ALL, 2)
        leftScrollPanelSizer.Add(self.btnSubmit, 0, wx.EXPAND | wx.ALL, 2)
        # self.btnRetrySelect.SetBackgroundColour(CON_COLOR_BLUE)
        # self.btnRetrySelect.SetForegroundColour(CON_COLOR_WHITE)
        self.btnSubmit.SetBackgroundColour(CON_COLOR_BLUE)
        self.btnSubmit.SetForegroundColour(CON_COLOR_WHITE)

        # 标签美化
        self.labelStaticTexts.extend([
            self.labelSelectFile,
            self.labelChoiceViewType, self.labelInputUrlPath,
            self.labelInputViewName, self.labelInputReverseViewName,
            self.labelInputUrlPreview, self.labelChoiceReturnType,
            self.labelChoiceShortcuts, self.labelChoiceDecorators,
        ])

        # 隐藏控制
        self.allCtrlsWithoutType.extend([
            self.inputViewNameStaticBox,self.labelInputViewName,self.inputViewName,
            self.inputReverseViewNameStaticBox,self.labelInputReverseViewName,self.inputReverseViewName,
            self.inputUrlPathStaticBox,self.labelInputUrlPath,self.inputUrlPath,
            self.inputUrlPreviewStaticBox,self.labelInputUrlPreview,self.inputUrlPreview,
            self.choiceReturnTypeStaticBox,self.labelChoiceReturnType,self.choiceReturnType,
            self.choiceShortcutsStaticBox,self.labelChoiceShortcuts,self.choiceShortcuts,
            self.choiceDecoratorsStaticBox,self.labelChoiceDecorators,self.choiceDecorators,
            # self.btnRetrySelect,
            self.btnSubmit,
        ])

        # 文本实时监听事件
        self.Bind(wx.EVT_TEXT, self.onInputViewName, self.inputViewName)
        self.Bind(wx.EVT_TEXT, self.onInputUrlPath, self.inputUrlPath)

        # 下拉框选择事件
        self.Bind(wx.EVT_CHOICE, self.onChoiceViewType, self.choiceViewType)

        # 选择框选择事件
        self.Bind(wx.EVT_CHOICE, self.onChoiceDecorators, self.choiceDecorators)
        self.Bind(wx.EVT_CHOICE, self.onChoiceReturnType, self.choiceReturnType)
        self.Bind(wx.EVT_CHOICE, self.onChoiceShortcuts, self.choiceShortcuts)

        # 按钮点击事件
        self.Bind(wx.EVT_BUTTON, self.onBtnSubmit, self.btnSubmit)

    def onBtnSubmit(self, e):
        """创建视图"""
        # 获取所有的值
        vchoiceSelectFile = self.choiceSelectFile.GetString(self.choiceSelectFile.GetSelection()).strip()
        vchoiceViewType = self.choiceViewType.GetString(self.choiceViewType.GetSelection()).strip()
        vinputViewName = self.inputViewName.GetValue().strip()
        vinputReverseViewName = self.inputReverseViewName.GetValue().strip()
        vinputUrlPath = self.inputUrlPath.GetValue().strip()
        vinputUrlPreview = self.inputUrlPreview.GetValue().strip()
        vchoiceReturnType = self.choiceReturnType.GetString(self.choiceReturnType.GetSelection()).strip()
        vchoiceShortcuts = self.choiceShortcuts.GetString(self.choiceShortcuts.GetSelection()).strip()
        vchoiceDecorators = self.choiceDecorators.GetString(self.choiceDecorators.GetSelection()).strip()

        if not vchoiceSelectFile:
            TipsMessageOKBox(self, '请选择视图即将写入的应用程序', '错误')
            return

        if not vchoiceViewType:
            TipsMessageOKBox(self, '无法写入空数据', '错误')
            return

        if not vinputUrlPath:
            TipsMessageOKBox(self, '请正确填写路由路径', '错误')
            return

    def onChoiceReturnType(self, e):
        """视图返回对象"""
        return_obj = self.choiceReturnType.GetString(self.choiceReturnType.GetSelection()).strip()
        if 'HttpResponse(200)' == return_obj:
            self.argsStruct['return_obj'] = "return HttpResponse('Hello World!')"
        else:
            self.argsStruct['return_obj'] = ""
        self._insert_data_to_template_by_argstruct()

    def onChoiceShortcuts(self, e):
        """视图快捷返回对象"""
        shortcut_obj = self.choiceShortcuts.GetString(self.choiceShortcuts.GetSelection()).strip()
        self.argsStruct['shortcut_obj'] = shortcut_obj
        self._insert_data_to_template_by_argstruct()

    def onChoiceDecorators(self, e):
        """选择函数装饰器"""
        decorator_type = e.GetString().strip()
        self.argsStruct['decorator'] = f'@{decorator_type}' if decorator_type and '（无）' != decorator_type else ''
        self._insert_data_to_template_by_argstruct()

    def _init_all_args(self):
        """初始化所有的交互式控件值"""
        self.choiceSelectFile.SetSelection(0)
        self.choiceViewType.SetSelection(0)
        self.inputViewName.SetValue('')
        self.inputReverseViewName.SetValue('')
        self.inputUrlPath.SetValue('')
        self.inputUrlPreview.SetValue('')
        self.choiceReturnType.SetSelection(0)
        self.choiceShortcuts.SetSelection(0)
        self.choiceDecorators.SetSelection(0)

    def onInputUrlPath(self, e):
        """路由路径指定"""
        path = self.inputUrlPath.GetValue().strip()
        if PATT_CAPTURE_URLSPATH_ARGS.search(path):
            args = [
                _ if -1 == _.find(':') else _[_.find(':')+1:] 
                for _ in PATT_CAPTURE_URLSPATH_ARGS.findall(path)
            ]
            self.argsStruct['func_args'] = args
        else:
            self.argsStruct['func_args'] = []
        self._insert_data_to_template_by_argstruct()

        # 路由预览
        # get_app_rooturl_config_by_appname
        app_name = self.choiceSelectFile.GetString(self.choiceSelectFile.GetSelection()).strip()
        
        if app_name:
            root_name = get_app_rooturl_config_by_appname(app_name)
            if root_name:
                if '/' != root_name[-1]:
                    root_name += '/'
                # 显示
                self.inputUrlPreview.SetValue('/' + root_name + path)

    def _insert_data_to_template_by_argstruct(self):
        """用模板变量填充模板"""
        temp_template = self.views_template

        # 路由函数参数填充
        if self.argsStruct.get('func_args'):
            temp_template = patt_sub_only_capture_obj_add(PATT_FUNC_ARGS, ', '+', '.join(self.argsStruct['func_args']), temp_template)

        # 路由方法名/类名
        if self.argsStruct.get('view_name'):
            temp_template = temp_template.replace('${view_name}', self.argsStruct['view_name'])

        # 装饰器
        if None != self.argsStruct.get('decorator'):
            temp_template = temp_template.replace('${decorator}', self.argsStruct['decorator'])

        # 试图返回对象
        if self.argsStruct.get('return_obj'):
            temp_template = temp_template.replace('${return}', self.argsStruct['return_obj'])

        # 试图返回快捷对象
        if self.argsStruct.get('shortcut_obj'):
            temp_template = temp_template.replace('${return}', self.argsStruct['shortcut_obj'])

        self.inputCodeReview.SetValue(temp_template)

    def onChoiceViewType(self, e):
        """选择要新建的视图类型"""
        view_type = e.GetString().strip()

        self._unshow_allctrls_withouttype() # 全部关闭，按需开启

        if not view_type:
            self.inputCodeReview.SetValue('')
            return

        if CON_VIEW_TYPE_FUNC == view_type:
            self.views_template = get_views_base_func()
            self.inputCodeReview.SetValue(self.views_template)
            # 显示本视图类型下的特殊参数设置

            self._show_allctrls_withouttype()

        elif CON_VIEW_TYPE_CLASS == view_type:
            self.views_template = get_views_base_class()
            self.inputCodeReview.SetValue(self.views_template)
            # 显示本视图类型下的特殊参数设置
            self.inputViewNameStaticBox.Show(True)
            self.labelInputViewName.Show(True)
            self.inputViewName.Show(True)
            self.inputReverseViewNameStaticBox.Show(True)
            self.labelInputReverseViewName.Show(True)
            self.inputReverseViewName.Show(True)
            self.inputUrlPathStaticBox.Show(True)
            self.labelInputUrlPath.Show(True)
            self.inputUrlPath.Show(True)
            self.inputUrlPreviewStaticBox.Show(True)
            self.labelInputUrlPreview.Show(True)
            self.inputUrlPreview.Show(True)
            self.btnSubmit.Show(True)

        else:
            self.inputCodeReview.SetValue('')

        self.leftPanel.Layout()

    def _init_right_panel(self):
        """初始化右子面板"""
        
        # 代码预览面板
        self.codeReviewPanel = wx.Panel(self.rightPanel)
        self.codeReviewPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.codeReviewPanel.SetSizer(self.codeReviewPanelSizer)
        self.rightPanelSizer.Add(self.codeReviewPanel, 1, wx.EXPAND | wx.ALL, 2)

        self.inputCodeReview = wx.TextCtrl(self.codeReviewPanel, -1, style=wx.TE_MULTILINE)
        self.codeReviewPanelSizer.Add(self.inputCodeReview, 1, wx.EXPAND | wx.ALL, 2)
        self.inputCodeReview.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False))

        # 标签美化
        self.labelStaticTexts.extend([])

    def onInputViewName(self, e):
        """视图名称监听实时输入"""
        view_name = self.inputViewName.GetValue().strip()
        self.inputReverseViewName.SetValue(view_name.lower())
        if view_name:
            self.argsStruct['view_name'] = view_name
            self._insert_data_to_template_by_argstruct() # 更新代码显示

        
    def _init_label_font(self):
        """标签提示信息字体初始化"""
        for _ in self.labelStaticTexts:
            _.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            _.SetForegroundColour(CON_COLOR_BLUE)

    def onRadiosClick(self, e):
        """"""
        # print(self.radiosPanel.GetSelection()) # 获取当前选中元素的下标
        pass

