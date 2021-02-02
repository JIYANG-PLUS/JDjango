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

class AdminCreateSimpleDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = '站点注册(简单配置)', size=(600, 400))

        self.font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False)
        self._init_UI()

    def _init_UI(self):
        """初始化界面布局"""
        self.panel = wx.Panel(self)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(panelSizer)
        self.panel.SetBackgroundColour('#ededed')

        self.btn_register = buttons.GenButton(self.panel, -1, label='确认注册')
        self.btn_register.Enable(False)

        # 选择要操作的App
        self.pathPanel = wx.Panel(self.panel)
        pathPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.pathPanel.SetSizer(pathPanelSizer)
        self.pathPanel.SetBackgroundColour('#ededed')
        panelSizer.Add(self.pathPanel, 0, wx.EXPAND | wx.ALL, 3)

        apps = get_configs(CONFIG_PATH)['app_names'] # 列举所有的应用程序
        self.infoChoiceApp = wx.StaticText(self.pathPanel, -1, "选择要注册的应用程序：")
        self.infoChoiceApp.SetFont(self.font)
        self.choiceApp = wx.Choice(self.pathPanel, -1, choices = [' ']+apps, style = wx.CB_SORT) # 复选框
        pathPanelSizer.Add(self.infoChoiceApp, 0, wx.EXPAND | wx.ALL, 6)
        pathPanelSizer.Add(self.choiceApp, 1, wx.EXPAND | wx.ALL, 6)

        # 选择要在后台注册的模型
        self.modelPanel = wx.Panel(self.panel)
        staticBox = wx.StaticBox(self.modelPanel, -1, '选择需要在后台操作的模型对象：')
        self.selectModelsSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL) # 中间实线括起部分布局
        self.modelPanel.SetSizer(self.selectModelsSizer)
        panelSizer.Add(self.modelPanel, 0, wx.EXPAND | wx.ALL, 3)
        
        self.listBoxModels = wx.ListBox(self.modelPanel, -1, size=(600, 250), choices = [], style = wx.LB_MULTIPLE | wx.LB_HSCROLL | wx.LB_ALWAYS_SB) # 存放 Models
        self.selectModelsSizer.Add(self.listBoxModels, 0, wx.LEFT, 10)

        # 末尾确认按钮
        panelSizer.Add(self.btn_register, 0, wx.EXPAND | wx.ALL, 3)

        # 事件监听
        self.Bind(wx.EVT_CHOICE, self.onChoiceClick, self.choiceApp) # 下拉列表值更新
        self.Bind(wx.EVT_BUTTON, self.onButtonClick, self.btn_register) # 注册按钮
        self.Bind(wx.EVT_LISTBOX, self.onListBox1Listbox, self.listBoxModels) # 多选模型列表


    def onListBox1Listbox(self, e):
        """多选列表事件"""
        bId = e.GetId()
        if bId == self.listBoxModels.GetId(): # 选择项目根路径
            selects = self.listBoxModels.GetSelections()
            if len(selects) > 0: self.btn_register.Enable(True)
            else: self.btn_register.Enable(False)

    def onChoiceClick(self, e):
        """下拉框选择App值更新事件"""
        key = e.GetString() # key即是app名
        self.listBoxModels.Clear() # 清空
        if key.strip():
            # 指定赋值
            # 路径筛选
            APP_PATH = os.path.join(get_configs(CONFIG_PATH)['dirname'], key)
            if os.path.exists(APP_PATH) and os.path.isdir(APP_PATH):
                # 获取路径下的所有文件
                pys = glob.glob(os.path.join(APP_PATH, '**', '*.py'), recursive=True)
                # 读取配置文件的别名集合
                alias = [os.path.basename(_) for _ in env.getModelsAlias()] # 仅取文件名
                # 通过别名筛选即将读取解析的模型文件
                pathModels = [_ for _ in pys if os.path.basename(_) in alias]
                # 赋值的同时标注模块的来源
                for obj in [(mo, os.path.basename(_)) for _ in pathModels for mo in toolModel.get_models_from_modelspy(_)]:
                    self.listBoxModels.Append(' -- '.join(obj))

    def onButtonClick(self, e):
        """界面按钮点击事件"""
        bId = e.GetId()
        if bId == self.btn_register.GetId():
            self.onRegister(e)

    def onRegister(self, e):
        """注册管理后台模型"""
        dlg = wx.MessageDialog(None, u"确认后，选中的模型将被注册到管理后台。", u"确认注册", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            selectNames = self.listBoxModels.GetStrings()
            selectIndexs = self.listBoxModels.GetSelections()
            modelModels = [selectNames[_] for _ in selectIndexs]
            appName = self.choiceApp.GetStrings()[self.choiceApp.GetSelection()] # 当前选中应用程序名
            # 分类导入admin.py文件
            modelFiles, models = [], []
            for _ in modelModels:
                t1, t2 = _.split(' -- ')
                modelFiles.append(t2.split('.')[0])
                models.append(t1)
            classify = set(modelFiles) # 分类，组成键值对组合
            importData = {}
            for _ in classify:
                importData[_] = [] # 初始化键【模块名】
            for _ in zip(models, modelFiles):
                importData[_[1]].append(_[0])
            # 读取admin.py的别名
            alias = env.getAdminAlias()
            for _ in alias:
                # 如果路径改变，可在environment.xml中配置完整的路径别名（如 admin.py 可扩展成 myfloder/admin.py，但是要确保子路径位于该app父路径下 ）
                # 下面将在所有的模块别名路径中写入注册数据【可能有点不合理】
                write_admin_base(os.path.join(get_configs(CONFIG_PATH)['dirname'], appName, _), importData) # 写入注册代码
            wx.MessageBox(f'{"、".join(models)}注册成功！', '提示', wx.OK | wx.ICON_INFORMATION) # 提示成功
        dlg.Close(True)

class AdminRenameDialog(wx.Dialog):

    # 两个变量反了, 现只改文字,变量不变.

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = '网站后台重命名', size=(300, 200))
        
        self._init_UI()
        self._init_data()

    def _init_UI(self):
        """初始化界面布局"""
        # 最外层布局
        self.panel = wx.Panel(self)
        self.panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.panelSizer)

        self.btnModify = buttons.GenButton(self.panel, -1, '修改')
        self.msgName = wx.TextCtrl(self.panel, -1)
        self.msgName.SetEditable(False)

        # 登录界面重命名
        self.headerPanel = wx.Panel(self.panel) 
        self.headerPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.headerPanel.SetSizer(self.headerPanelSizer)
        self.panelSizer.Add(self.headerPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.headerFlag = wx.StaticText(self.headerPanel, -1, "后台标题名称：")
        self.inputHeader = wx.TextCtrl(self.headerPanel, -1)
        self.headerPanelSizer.Add(self.headerFlag, 0, wx.EXPAND | wx.ALL, 2)
        self.headerPanelSizer.Add(self.inputHeader, 1, wx.EXPAND | wx.ALL, 2)

        # 后台标题重命名
        self.titlePanel = wx.Panel(self.panel)
        self.titlePanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.titlePanel.SetSizer(self.titlePanelSizer)
        self.panelSizer.Add(self.titlePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.titleFlag = wx.StaticText(self.titlePanel, -1, "登录界面名称：")
        self.inputTitle = wx.TextCtrl(self.titlePanel, -1)
        self.titlePanelSizer.Add(self.titleFlag, 0, wx.EXPAND | wx.ALL, 2)
        self.titlePanelSizer.Add(self.inputTitle, 1, wx.EXPAND | wx.ALL, 2)

        # 标题所在位置信息
        # self.locPanel = wx.Panel(self.panel)
        # self.locPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.locPanel.SetSizer(self.locPanelSizer)
        # self.panelSizer.Add(self.locPanel, 0, wx.EXPAND | wx.ALL, 2)

        # self.locFlag = wx.StaticText(self.locPanel, -1, "位置：")
        # self.locTitle = wx.TextCtrl(self.locPanel, -1)
        # self.locPanelSizer.Add(self.locFlag, 0, wx.EXPAND | wx.ALL, 2)
        # self.locPanelSizer.Add(self.locTitle, 1, wx.EXPAND | wx.ALL, 2)
        # self.locTitle.SetEditable(False)

        # 末尾按钮 和 提示信息   
        self.panelSizer.Add(self.btnModify, 1, wx.EXPAND | wx.ALL, 2)
        self.panelSizer.Add(self.msgName, 0, wx.EXPAND | wx.ALL, 2)

        # 事件监听
        self.Bind(wx.EVT_BUTTON, self.onBtnModify, self.btnModify)

    def onBtnModify(self, e):
        """确认修改，重命名"""
        # 若没有命名过，则任选一处命名
        # 若只有一个命名，则修改本处命名
        # 若有两个及以上命名，则删除所有，再任选一处命名
        value_header = self.inputHeader.GetValue().strip() # 登录名
        value_title = self.inputTitle.GetValue().strip() # 后台名
        result = []
        if value_header and 'None' != value_header: # 只要不为空，覆盖式赋值
            headers = get_site_header()
            len_headers = len(headers)
            if len_headers > 0:
                if len_headers > 1:
                    set_site_header(value_header, mode = 2) # 若有两个及以上命名，则删除所有，再任选一处命名
                else:
                    set_site_header(value_header, mode = 1) # 若只有一个命名，则修改本处命名
            else:
                set_site_header(value_header, mode = 0) # 若没有命名过，则任选一处命名
            result.append(True)
        else:
            result.append(False)

        if value_title and 'None' != value_title:
            titles = get_site_title()
            len_titles = len(titles)
            if len_titles > 0:
                if len_titles > 1:
                    set_site_title(value_title, mode = 2) # 若有两个及以上命名，则删除所有，再任选一处命名
                else:
                    set_site_title(value_title, mode = 1) # 若只有一个命名，则修改本处命名
            else:
                set_site_title(value_title, mode = 0) # 若没有命名过，则任选一处命名
            result.append(True)
        else:
            result.append(False)
        
        if any(result):
            if result[0] and result[1]:
                wx.MessageBox(f'同步修改成功', '提示', wx.OK | wx.ICON_INFORMATION) # 提示成功
                return
            if result[0]:
                wx.MessageBox(f'仅登录界面名称修改成功', '提示', wx.OK | wx.ICON_INFORMATION) # 提示成功
                return
            if result[1]:
                wx.MessageBox(f'仅后台标题名称修改成功', '提示', wx.OK | wx.ICON_INFORMATION) # 提示成功
                return
        else:
            wx.MessageBox(f'未做任何修改', '错误', wx.OK | wx.ICON_INFORMATION)

    def _init_data(self):
        headers = get_site_header()
        len_headers = len(headers)
        if len_headers > 0:
            self.inputHeader.SetValue(f'{headers[0]}')
            if len_headers > 1:
                self.msgName.SetValue(f'警告，共有{len_headers}处设置！仅需保留一个')
            else:
                self.msgName.SetValue(f'读取正常')
        else:
            self.inputHeader.SetValue(f'None')
            self.msgName.SetValue(f'读取正常')
        titles = get_site_title()
        len_titles = len(titles)
        if len_titles > 0:
            self.inputTitle.SetValue(f'{titles[0]}')
            if len_titles > 1:
                self.msgName.SetValue(f'警告，共有{len_titles}处设置！仅需保留一个')
            else:
                self.msgName.SetValue(f'读取正常') # 此处会出现问题，当二者不在一个位置时会引发冲突
        else:
            self.inputTitle.SetValue(f'None')
            self.msgName.SetValue(f'读取正常')

        # self.locTitle.SetValue('')

class ProjectCreateDialog(wx.Dialog):

    def __init__(self, parent):

        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = '新建项目', size=(360, 150))

        self._init_UI()

    def _init_UI(self):
        """初始化界面布局"""
        # 总面板
        self.panel = wx.Panel(self)
        self.panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.panelSizer)

        # 选择路径容器
        self.pathPanel = wx.Panel(self.panel)
        self.pathPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.pathPanel.SetSizer(self.pathPanelSizer)
        self.panelSizer.Add(self.pathPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.path = wx.TextCtrl(self.pathPanel, -1, style=wx.ALIGN_LEFT)
        self.btnChoice = buttons.GenButton(self.pathPanel, -1, '选择/输入项目写入目录')
        self.pathPanelSizer.Add(self.btnChoice, 0, wx.EXPAND | wx.ALL, 2)
        self.pathPanelSizer.Add(self.path, 1, wx.EXPAND | wx.ALL, 2)

        # 项目命名
        self.namePanel = wx.Panel(self.panel)
        self.namePanelBox = wx.BoxSizer(wx.HORIZONTAL)
        self.namePanel.SetSizer(self.namePanelBox)
        self.panelSizer.Add(self.namePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.flagName = wx.StaticText(self.namePanel, -1, "项目命名：")
        self.imputName = wx.TextCtrl(self.namePanel, -1, style=wx.ALIGN_LEFT)
        self.namePanelBox.Add(self.flagName, 0, wx.EXPAND | wx.ALL, 2)
        self.namePanelBox.Add(self.imputName, 1, wx.EXPAND | wx.ALL, 2)

        # 末尾控件
        self.btnCreate = buttons.GenButton(self.panel, -1, '新建')
        self.panelSizer.Add(self.btnCreate, 1, wx.EXPAND | wx.ALL, 2)

        # 注册事件监听
        self.Bind(wx.EVT_BUTTON, self.onBtnChoice, self.btnChoice)
        self.Bind(wx.EVT_BUTTON, self.onBtnCreate, self.btnCreate)


    def onBtnChoice(self, e):
        """选择项目写入路径"""
        dlg = wx.DirDialog(self, "选择写入项目的路径", style = wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.path.SetValue(dlg.GetPath())
        dlg.Close(True)

    def onBtnCreate(self, e):
        """创建项目"""
        path = self.path.GetValue()
        name = self.imputName.GetValue()
        if not os.path.exists(path) or not os.path.isdir(path):
            wx.MessageBox(f'非法路径', '错误', wx.OK | wx.ICON_INFORMATION)
            return
        if '' == name or not PATT_CHARS.match(name):
            wx.MessageBox(f'项目名称非法', '错误', wx.OK | wx.ICON_INFORMATION)
            return
        status = startproject(path, name)
        if 0 == status:
            wx.MessageBox(f'项目{name}创建成功', '成功', wx.OK | wx.ICON_INFORMATION)
            self.Close()
        else:
            wx.MessageBox(f'项目已存在', '错误', wx.OK | wx.ICON_INFORMATION)

class SettingsDialog(wx.Dialog):
    
    def __init__(self, parent):

        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = '项目配置', size=(550, 600))

        configs = get_configs(os.path.join(BASE_DIR, 'config.json'))
        self.DIRNAME = configs["dirname"]
        self.DIRSETTINGS = os.path.join(self.DIRNAME, configs['project_name'], 'settings.py')

        # 主布局
        wholePanel = wx.Panel(self)
        wholeBox = wx.BoxSizer(wx.VERTICAL) # 垂直
        wholePanel.SetSizer(wholeBox)

        # 底部工具栏
        wholeToolsPanel = wx.Panel(wholePanel)
        wholeToolsBox = wx.BoxSizer(wx.HORIZONTAL) # 水平
        wholeToolsPanel.SetSizer(wholeToolsBox)
        self.saveConfig = buttons.GenButton(wholeToolsPanel, -1, '保存')
        wholeToolsBox.Add(self.saveConfig, 0, wx.EXPAND | wx.ALL, 2)

        labels = wx.Notebook(wholePanel)

        """数据库"""
        self.databasesPanel = wx.Panel(labels)

        """Settings"""
        self.otherPanel = scrolledpanel.ScrolledPanel(labels, -1) # 其它（可滚动面板）
        self.otherPanel.SetupScrolling() # 开启滚动条
        otherRefreshKeyPanel = wx.Panel(self.otherPanel) # SECRET_KEY
        nm = wx.StaticBox(self.otherPanel, -1, 'ALLOWED_HOSTS') # 带边框的盒子
        otherAllowedHostsPanel = wx.StaticBoxSizer(nm, wx.HORIZONTAL)
        otherDebugPanel = wx.Panel(self.otherPanel) # DEBUG
        otherIframePanel = wx.Panel(self.otherPanel) # iframe
        otherLanguageCodePanel = wx.Panel(self.otherPanel) # LANGUAGE_CODE
        otherTimeZonePanel = wx.Panel(self.otherPanel) # TIME_ZONE
        otherUseI18NPanel = wx.Panel(self.otherPanel) # USE_I18N
        otherUseL10NPanel = wx.Panel(self.otherPanel) # USE_L10N
        otherUseTzPanel = wx.Panel(self.otherPanel) # USE_TZ

        # 其它 控件
        self.btnRefreshSecretKey = buttons.GenButton(otherRefreshKeyPanel, -1, '重置SECRET_KEY') # 刷新 SECRET_KEY
        self.inputRefreshSecretKey = wx.TextCtrl(otherRefreshKeyPanel, -1, style=wx.ALIGN_LEFT) # 显示 SECRET_KEY
        self.inputRefreshSecretKey.Enable(False)
        self.radiosPanel = wx.RadioBox(otherDebugPanel, -1, "调式模式", choices=['开启', '关闭'])
        self.radiosIframePanel = wx.RadioBox(otherIframePanel, -1, "iframe模式", choices=['开启', '关闭'])
        self.radiosLanguageCodePanel = wx.RadioBox(otherLanguageCodePanel, -1, "语言环境", choices=['中文', '英文'])
        self.radiosTimeZonePanel = wx.RadioBox(otherTimeZonePanel, -1, "时区", choices=['伦敦时区', '北京时区'])
        self.radiosUseI18NPanel = wx.RadioBox(otherUseI18NPanel, -1, "国际化", choices=['开启', '关闭'])
        self.radiosUseL10NPanel = wx.RadioBox(otherUseL10NPanel, -1, "区域设置优先", choices=['开启', '关闭'])
        self.radiosUseTzPanel = wx.RadioBox(otherUseTzPanel, -1, "系统时区", choices=['开启', '关闭'])

        self.inputAllowedHosts = wx.TextCtrl(self.otherPanel, -1, style = wx.ALIGN_LEFT) # ip设置

        # 其它 布局
        otherBox = wx.BoxSizer(wx.VERTICAL)
        otherRefreshKeyBOX = wx.BoxSizer(wx.HORIZONTAL)
        otherDebugBOX = wx.BoxSizer(wx.HORIZONTAL)
        otherIframeBOX = wx.BoxSizer(wx.HORIZONTAL)
        otherLanguageCodeBOX = wx.BoxSizer(wx.HORIZONTAL)
        otherTimeZoneBOX = wx.BoxSizer(wx.HORIZONTAL)
        otherUseI18NBOX = wx.BoxSizer(wx.HORIZONTAL)
        otherUseL10NBOX = wx.BoxSizer(wx.HORIZONTAL)
        otherUseTzBOX = wx.BoxSizer(wx.HORIZONTAL)

        # 填充
        otherRefreshKeyBOX.Add(self.inputRefreshSecretKey, 1, wx.EXPAND | wx.ALL, 2)
        otherRefreshKeyBOX.Add(self.btnRefreshSecretKey, 0, wx.EXPAND | wx.ALL, 2)
        otherDebugBOX.Add(self.radiosPanel, 1, wx.EXPAND | wx.ALL, 2)
        otherIframeBOX.Add(self.radiosIframePanel, 1, wx.EXPAND | wx.ALL, 2)
        otherLanguageCodeBOX.Add(self.radiosLanguageCodePanel, 1, wx.EXPAND | wx.ALL, 2)
        otherTimeZoneBOX.Add(self.radiosTimeZonePanel, 1, wx.EXPAND | wx.ALL, 2)
        otherUseI18NBOX.Add(self.radiosUseI18NPanel, 1, wx.EXPAND | wx.ALL, 2)
        otherUseL10NBOX.Add(self.radiosUseL10NPanel, 1, wx.EXPAND | wx.ALL, 2)
        otherUseTzBOX.Add(self.radiosUseTzPanel, 1, wx.EXPAND | wx.ALL, 2)

        otherAllowedHostsPanel.Add(self.inputAllowedHosts, 1, wx.EXPAND | wx.ALL, 2)

        otherBox.Add(otherRefreshKeyPanel, 0, wx.EXPAND | wx.ALL, 2)
        otherBox.Add(otherAllowedHostsPanel, 0, wx.EXPAND | wx.ALL, 2)
        otherBox.Add(otherDebugPanel, 0, wx.EXPAND | wx.ALL, 2)
        otherBox.Add(otherLanguageCodePanel, 0, wx.EXPAND | wx.ALL, 2)
        otherBox.Add(otherTimeZonePanel, 0, wx.EXPAND | wx.ALL, 2)
        otherBox.Add(otherUseI18NPanel, 0, wx.EXPAND | wx.ALL, 2)
        otherBox.Add(otherUseL10NPanel, 0, wx.EXPAND | wx.ALL, 2)
        otherBox.Add(otherUseTzPanel, 0, wx.EXPAND | wx.ALL, 2)
        otherBox.Add(otherIframePanel, 0, wx.EXPAND | wx.ALL, 2)

        # 其它 面板绑定布局
        otherRefreshKeyPanel.SetSizer(otherRefreshKeyBOX)
        otherDebugPanel.SetSizer(otherDebugBOX)
        otherIframePanel.SetSizer(otherIframeBOX)
        otherLanguageCodePanel.SetSizer(otherLanguageCodeBOX)
        otherTimeZonePanel.SetSizer(otherTimeZoneBOX)
        otherUseI18NPanel.SetSizer(otherUseI18NBOX)
        otherUseL10NPanel.SetSizer(otherUseL10NBOX)
        otherUseTzPanel.SetSizer(otherUseTzBOX)
        self.otherPanel.SetSizer(otherBox)

        """项目重命名"""
        self.projectRenamePanel = wx.Panel(labels)
        self.renamePanel = wx.Panel(self.projectRenamePanel)
        projectRenameBox = wx.BoxSizer(wx.VERTICAL)
        renameBox = wx.BoxSizer(wx.VERTICAL)
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)

        temp = wx.StaticBox(self.renamePanel, -1, 'Django项目：') # 带边框的盒子
        static_config_box = wx.StaticBoxSizer(temp, wx.VERTICAL) # 垂直布局

        flagProjectName = wx.StaticText(self.renamePanel, -1, "您的项目名称：") # 项目名称
        self.inputProjectName = wx.TextCtrl(self.renamePanel, -1, style=wx.ALIGN_LEFT) # 输入框
        project_name = configs['project_name']
        self.inputProjectName.SetValue(f"{project_name}")

        self.flagFirst = wx.StaticText(self.renamePanel, -1, "请先关闭所有占用此Django项目的程序。（否则会遇到修改权限问题）")
        self.btnModify = buttons.GenButton(self.renamePanel, -1, label='修改（修改前请提前做好备份）')
        self.flagTip = wx.StaticText(self.renamePanel, -1, "请确保您的项目名称在您整个项目中是独一无二的，否则本功能会严重破坏您的项目")

        horizontal_box.Add(flagProjectName, 0, wx.ALL | wx.CENTER, 5)
        horizontal_box.Add(self.inputProjectName, 0, wx.ALL | wx.CENTER, 5)

        static_config_box.Add(horizontal_box, 0, wx.ALL | wx.CENTER, 10)

        renameBox.Add(static_config_box, 0, wx.ALL | wx.CENTER, 5)
        renameBox.Add(self.flagFirst, 0, wx.ALL | wx.CENTER, 5)
        renameBox.Add(self.flagTip, 0, wx.ALL | wx.CENTER, 5)
        renameBox.Add(self.btnModify, 0, wx.ALL | wx.CENTER, 5)

        projectRenameBox.Add(self.renamePanel, 1, wx.ALL | wx.CENTER, 5)

        self.renamePanel.SetSizer(renameBox)
        self.projectRenamePanel.SetSizer(projectRenameBox)

        """填充页签"""
        labels.AddPage(self.otherPanel, 'Settings')
        labels.AddPage(self.databasesPanel, '数据库')
        labels.AddPage(self.projectRenamePanel, '项目重命名')

        wholeBox.Add(labels, 1, wx.EXPAND | wx.ALL, 2) # 添加多页签
        wholeBox.Add(wholeToolsPanel, 0, wx.EXPAND | wx.ALL, 2) # 添加工具条

        # 事件监听
        self.Bind(wx.EVT_BUTTON, self.onBtnRefreshSecretKey, self.btnRefreshSecretKey)
        self.Bind(wx.EVT_BUTTON, self.onBtnModify, self.btnModify)
        self.Bind(wx.EVT_BUTTON, self.onBtnSaveConfig, self.saveConfig)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, self.radiosPanel)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, self.radiosIframePanel)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, self.radiosLanguageCodePanel)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, self.radiosTimeZonePanel)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, self.radiosUseI18NPanel)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, self.radiosUseL10NPanel)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, self.radiosUseTzPanel)

        # 基本对象
        self.DATA_SETTINGS = {}

        # 初始化同步数据
        self._init_data()

    def _init_data(self):
        CONFIGS = get_configs(CONFIG_PATH)
        # 0 开启，1关闭
        self.radiosPanel.SetSelection(0 if CONFIGS['DEBUG'] else 1)
        self.radiosIframePanel.SetSelection(0 if CONFIGS['X_FRAME_OPTIONS'] else 1)
        self.radiosLanguageCodePanel.SetSelection(0 if CONFIGS['LANGUAGE_CODE'].lower() in [_.lower() for _ in SETTINGSS['LANGUAGE_CODE'][0]] else 1)
        self.radiosTimeZonePanel.SetSelection(0 if CONFIGS['TIME_ZONE'].lower() in [_.lower() for _ in SETTINGSS['TIME_ZONE'][0]] else 1)
        self.radiosUseI18NPanel.SetSelection(0 if CONFIGS['USE_I18N'] else 1)
        self.radiosUseL10NPanel.SetSelection(0 if CONFIGS['USE_L10N'] else 1)
        self.radiosUseTzPanel.SetSelection(0 if CONFIGS['USE_TZ'] else 1)
        self.inputRefreshSecretKey.SetValue(CONFIGS['SECRET_KEY'])
        self.inputAllowedHosts.SetValue(','.join(CONFIGS['ALLOWED_HOSTS']))

    def onBtnSaveConfig(self, e):
        """保存修改"""
        try:
            CONFIGS = get_configs(CONFIG_PATH)
            content_settings = read_file(self.DIRSETTINGS)
            temp = content_settings
            if None != self.DATA_SETTINGS.get('DEBUG'):
                temp = patt_sub_only_capture_obj(PATT_DEBUG, self.DATA_SETTINGS['DEBUG'], temp)
            if None != self.DATA_SETTINGS.get('USE_I18N'):
                temp = patt_sub_only_capture_obj(PATT_USE_I18N, self.DATA_SETTINGS['USE_I18N'], temp)
            if None != self.DATA_SETTINGS.get('USE_L10N'):
                temp = patt_sub_only_capture_obj(PATT_USE_L10N, self.DATA_SETTINGS['USE_L10N'], temp)
            if None != self.DATA_SETTINGS.get('USE_TZ'):
                temp = patt_sub_only_capture_obj(PATT_USE_TZ, self.DATA_SETTINGS['USE_TZ'], temp)
            if None != self.DATA_SETTINGS.get('X_FRAME_OPTIONS'):
                if self.DATA_SETTINGS['X_FRAME_OPTIONS']: # 开启
                    if not CONFIGS['X_FRAME_OPTIONS']: # 且原文件不存在
                        TEMPLATE_DIR = os.path.join(BASE_DIR, 'djangoTemplates', 'settings', 'iframe.django')
                        # 在文件末尾添加iframe开启代码
                        write_file(self.DIRSETTINGS, temp) # 刷新
                        append_file(self.DIRSETTINGS, read_file_list(TEMPLATE_DIR))
                        temp = read_file(self.DIRSETTINGS) # 刷新
                else: # 关闭（删除）
                    temp = PATT_X_FRAME_OPTIONS.sub('', temp)
            if None != self.DATA_SETTINGS.get('LANGUAGE_CODE'):
                re_str = SETTINGSS['LANGUAGE_CODE'][self.DATA_SETTINGS['LANGUAGE_CODE']][0]
                temp = patt_sub_only_capture_obj(PATT_LANGUAGE_CODE, re_str, temp)
            if None != self.DATA_SETTINGS.get('TIME_ZONE'):
                re_str = SETTINGSS['TIME_ZONE'][self.DATA_SETTINGS['TIME_ZONE']][0]
                temp = patt_sub_only_capture_obj(PATT_TIME_ZONE, re_str, temp)
            # 写入SECRET_KEY和HOST
            temp = patt_sub_only_capture_obj(PATT_SECRET_KEY, self.inputRefreshSecretKey.GetValue(), temp)
            host_contents = [f"'{_}'" for _ in self.inputAllowedHosts.GetValue().strip().split(',') if _]
            temp = patt_sub_only_capture_obj_obtain_double(PATT_ALLOWED_HOSTS, ','.join(host_contents), temp)
            write_file(self.DIRSETTINGS, temp) # 更新settings.py文件
            refresh_config() # 更新配置文件【重要！！！】
            self.DATA_SETTINGS = {} # 防止重复确定
        except:
            wx.MessageBox(f'错误，配置文件已损坏。', '错误', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox(f'修改成功！', '成功', wx.OK | wx.ICON_INFORMATION)
        
    def onBtnModify(self, e):
        """重命名项目名称"""
        # 再次提醒
        dlgA = wx.MessageDialog(self, u"请再次确认", u"确认信息", wx.YES_NO | wx.ICON_QUESTION)
        if dlgA.ShowModal() == wx.ID_YES:
            configs = get_configs(os.path.join(BASE_DIR, 'config.json'))
            # 获取新的名称
            old_name = configs['project_name']
            new_name = self.inputProjectName.GetValue().strip()

            if old_name == new_name:
                dlg = wx.MessageDialog( self, "未做任何修改", "警告", wx.OK)
                dlg.ShowModal()
                dlg.Close(True)
                return

            if not PATT_CHARS.match(new_name):
                dlg = wx.MessageDialog( self, "请使用字母+下划线的方式命名", "错误", wx.OK)
                dlg.ShowModal()
                dlg.Close(True)
                return
            try:
                # 重命名项目（先文件，后目录）
                search_path = os.path.join(self.DIRNAME, '**', '*')
                alls = glob.glob(search_path, recursive=True)

                # 分类文件和文件夹
                files, floders = [], []
                for _ in alls:
                    if os.path.isfile(_): files.append(_)
                    else: floders.append(_)

                for p in files:
                    # 先读后写
                    if '.py' == os.path.splitext(p)[1]:
                        content = read_file(p)
                        content = content.replace(old_name.strip(), new_name)
                        write_file(p, content)

                for P in floders:
                    if old_name.strip().lower() == os.path.basename(P).strip().lower():
                        temp = os.path.join(os.path.dirname(P), new_name)
                        os.rename(P, temp)

                # 修改根目录名称
                os.rename(self.DIRNAME, os.path.join(os.path.dirname(self.DIRNAME), new_name))
                
                dlg = wx.MessageDialog( self, "修改成功，请退出所有窗口后重新打开，进行后续操作。", "成功", wx.OK)
                if dlg.ShowModal() == wx.ID_OK:
                    self.Close(True)
                dlg.ShowModal()
                dlg.Close(True)
            except:
                """操作回退，将之前所有的改动还原"""
                pass # 待完成
        dlgA.Close(True)

    def onRadioBox(self, e):
        """单选框组事件"""
        # 原则上只对需要改变的内容进行修改
        key = e.GetId()
        if key == self.radiosPanel.GetId(): # DEBUG
            self.DATA_SETTINGS['DEBUG'] = 'True' if 0 == self.radiosPanel.GetSelection() else 'False'
        elif key == self.radiosIframePanel.GetId(): # X_FRAME_OPTIONS
            self.DATA_SETTINGS['X_FRAME_OPTIONS'] = True if 0 == self.radiosIframePanel.GetSelection() else False
        elif key == self.radiosLanguageCodePanel.GetId(): # LANGUAGE_CODE
            self.DATA_SETTINGS['LANGUAGE_CODE'] = self.radiosLanguageCodePanel.GetSelection()
        elif key == self.radiosTimeZonePanel.GetId(): # TIME_ZONE
            self.DATA_SETTINGS['TIME_ZONE'] = self.radiosTimeZonePanel.GetSelection()
        elif key == self.radiosUseI18NPanel.GetId(): # USE_I18N
            self.DATA_SETTINGS['USE_I18N'] = 'True' if 0 == self.radiosUseI18NPanel.GetSelection() else 'False'
        elif key == self.radiosUseL10NPanel.GetId(): # USE_L10N
            self.DATA_SETTINGS['USE_L10N'] = 'True' if 0 == self.radiosUseL10NPanel.GetSelection() else 'False'
        elif key == self.radiosUseTzPanel.GetId(): # USE_TZ
            self.DATA_SETTINGS['USE_TZ'] = 'True' if 0 == self.radiosUseTzPanel.GetSelection() else 'False'
        
    def onBtnRefreshSecretKey(self, e):
        """刷新SECRET_KEY"""
        new_key = generate_secret_key()
        self.DATA_SETTINGS['SECRET_KEY'] = new_key
        self.inputRefreshSecretKey.SetValue(new_key)
