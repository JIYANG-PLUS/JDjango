import wx, json, glob, os, re
import wx.lib.buttons as buttons
from ..tools._tools import *
from .. settings import BASE_DIR, CONFIG_PATH, CONFIG_PATH
from ..tools import environment as env
from ..tools import models as toolModel
from ..miniCmd.djangoCmd import *

env_obj = env.getEnvXmlObj()

PATT_CHARS = re.compile(r'^[a-zA-Z_].*$')

class ConfigDialog(wx.Dialog):
    def __init__(self, parent, id, **kwargs):
        self.configs = get_configs(os.path.join(BASE_DIR, 'config.json'))
        self.DIRNAME = self.configs["dirname"]
        
        wx.Dialog.__init__(self, parent, id, '选项配置', size=(600, 400))

        self.panel = wx.Panel(self)
        vertical_box = wx.BoxSizer(wx.VERTICAL)
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)

        nm = wx.StaticBox(self.panel, -1, 'Django项目：') # 带边框的盒子
        static_config_box = wx.StaticBoxSizer(nm, wx.VERTICAL) # 垂直布局

        fn = wx.StaticText(self.panel, -1, "您的项目名称：") # 项目名称
        self.nm1 = wx.TextCtrl(self.panel, -1, style=wx.ALIGN_LEFT) # 输入框
        project_name = self.configs['project_name']
        self.nm1.SetValue(f"{project_name}")

        # 按钮
        self.first = wx.StaticText(self.panel, -1, "请先关闭所有占用此Django项目的程序。（否则会遇到修改权限问题）")
        self.modify = buttons.GenButton(self.panel, -1, label='修改（修改前请提前做好备份）')
        self.tip = wx.StaticText(self.panel, -1, "请确保您的项目名称在您整个项目中是独一无二的，否则本功能会严重破坏您的项目")

        horizontal_box.Add(fn, 0, wx.ALL | wx.CENTER, 5)
        horizontal_box.Add(self.nm1, 0, wx.ALL | wx.CENTER, 5)

        static_config_box.Add(horizontal_box, 0, wx.ALL | wx.CENTER, 10)

        vertical_box.Add(static_config_box, 0, wx.ALL | wx.CENTER, 5)
        vertical_box.Add(self.first, 0, wx.ALL | wx.CENTER, 5)
        vertical_box.Add(self.tip, 0, wx.ALL | wx.CENTER, 5)
        vertical_box.Add(self.modify, 0, wx.ALL | wx.CENTER, 5)

        self.panel.SetSizer(vertical_box)

        # 事件绑定
        self.Bind(wx.EVT_BUTTON, self.ButtonClick, self.modify)

    def ButtonClick(self, e):
        bId = e.GetId()
        if bId == self.modify.GetId():
            # 获取新的名称
            old_name = self.configs['project_name']
            new_name = self.nm1.GetValue().strip()

            if old_name == new_name:
                dlg = wx.MessageDialog( self, "未做任何修改", "警告", wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
                return

            if not PATT_CHARS.match(new_name):
                dlg = wx.MessageDialog( self, "请使用字母+下划线的方式命名", "错误", wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
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
                dlg.Destroy()
            except:
                """操作回退，将之前所有的改动还原"""
                pass # 待完成

class AdminCreateSimpleDialog(wx.Dialog):
    def __init__(self, parent, id, **kwargs):
        wx.Dialog.__init__(self, parent, id, '站点注册(简单配置)', size=(600, 400))

        self.font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False)

        # 面板
        self.panel = wx.Panel(self) # 最外层容器
        self.pathPanel = wx.Panel(self.panel) # 选择应用程序app
        self.panel.SetBackgroundColour('#ededed')  # 最外层容器颜色
        self.pathPanel.SetBackgroundColour('#ededed')
        # self.scroller = wx.ScrolledWindow(self.panel, -1)
        # self.scroller.SetScrollbars(1, 1, 600, -1)
        self.modelPanel = wx.Panel(self.panel) # 选择模型列表

        # 向 self.pathPanel 填充控件
        # self.btn_select_file_path = buttons.GenButton(self.pathPanel, -1, label='选择admin.py文件')
        # self.text_path = wx.TextCtrl(self.pathPanel, -1)
        # self.text_path.SetFont(self.font)
        # self.text_path.SetEditable(False)
        apps = get_configs(CONFIG_PATH)['app_names']
        self.infoChoiceApp = wx.StaticText(self.pathPanel, -1, "选择要注册的应用程序：")
        self.infoChoiceApp.SetFont(self.font)
        self.choiceApp = wx.Choice(self.pathPanel, -1, choices = [' ']+apps, style = wx.CB_SORT) # 复选框

        # 静态框里的复选框
        self.modelChoices = [
            # 置空 动态生成
        ]

        # 区域静态框
        staticBox = wx.StaticBox(self.modelPanel, -1, '选择需要在后台操作的模型对象：') # 带边框的盒子

        # 确认注册按钮
        self.btn_register = buttons.GenButton(self.panel, -1, label='确认注册')
        self.btn_register.Enable(False)
        
        # 垂直布局 和 水平布局
        panelBox = wx.BoxSizer(wx.VERTICAL)
        pathPanelBox = wx.BoxSizer(wx.HORIZONTAL) # 选择app布局
        self.staticAreaBox = wx.StaticBoxSizer(staticBox, wx.VERTICAL) # 中间实线括起部分布局
        self.staticAreaBox_1 = wx.ListBox(self.modelPanel, -1, size=(600, 250), choices = self.modelChoices, style = wx.LB_MULTIPLE | wx.LB_HSCROLL | wx.LB_ALWAYS_SB) # 存放 Models

        # 复选框 【后期从真正的models文件中读取】
        self.staticAreaBox.Add(self.staticAreaBox_1, 0, wx.LEFT, 10)

        # 路径选择填充
        pathPanelBox.Add(self.infoChoiceApp, 0, wx.EXPAND | wx.ALL, 6)
        pathPanelBox.Add(self.choiceApp, 1, wx.EXPAND | wx.ALL, 6)

        # 最外层容器填充（从上往下）
        panelBox.Add(self.pathPanel, 0, wx.EXPAND | wx.ALL, 3)
        panelBox.Add(self.modelPanel, 0, wx.EXPAND | wx.ALL, 3)
        panelBox.Add(self.btn_register, 0, wx.EXPAND | wx.ALL, 3)

        # 面板绑定布局
        self.pathPanel.SetSizer(pathPanelBox)
        self.modelPanel.SetSizer(self.staticAreaBox)
        self.panel.SetSizer(panelBox)

        # 注册事件
        self.Bind(wx.EVT_CHOICE, self.ChoiceClick, self.choiceApp) # 下拉列表值更新
        self.Bind(wx.EVT_BUTTON, self.ButtonClick, self.btn_register) # 注册按钮
        self.Bind(wx.EVT_LISTBOX, self.OnListBox1Listbox, self.staticAreaBox_1) # 多选模型列表

        # 初始化控件状态

    def OnListBox1Listbox(self, e):
        """多选列表事件"""
        bId = e.GetId()
        if bId == self.staticAreaBox_1.GetId(): # 选择项目根路径
            selects = self.staticAreaBox_1.GetSelections()
            if len(selects) > 0: self.btn_register.Enable(True)
            else: self.btn_register.Enable(False)

    def ChoiceClick(self, e):
        """下拉框选择App值更新事件"""
        key = e.GetString() # key即是app名
        self.staticAreaBox_1.Clear() # 清空
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
                    self.staticAreaBox_1.Append(' -- '.join(obj))

    def ButtonClick(self, e):
        """界面按钮点击事件"""
        bId = e.GetId()
        # if bId == self.btn_select_file_path.GetId(): # 选择admin.py所在路径
        #     self.select_adminpy(e)
        if bId == self.btn_register.GetId():
            self.onRegister(e)

    def onRegister(self, e):
        """注册管理后台模型"""
        dlg = wx.MessageDialog(None, u"确认后，选中的模型将被注册到管理后台。", u"确认注册", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            selectNames = self.staticAreaBox_1.GetStrings()
            selectIndexs = self.staticAreaBox_1.GetSelections()
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
        dlg.Destroy()

    # def select_adminpy(self, e):
    #     """获取admin.py文件所在路径"""
    #     path = get_configs(CONFIG_PATH)['dirname']
    #     dlg = wx.FileDialog(self, "选择admin.py文件", path, "", "*.py", wx.FD_OPEN)
    #     if dlg.ShowModal() == wx.ID_OK:
    #         filename = dlg.GetFilename()
    #         # 待校验：是否是当前项目下的admin.py文件
    #         self.dirname = dlg.GetDirectory()
    #         if 'admin.py' == filename:
    #             self.text_path.SetValue(f'{self.dirname}')
    #         else:
    #             pass
    #     else:
    #         pass
    #     dlg.Destroy()

class AdminRenameDialog(wx.Dialog):
    def __init__(self, parent, id, **kwargs):
        wx.Dialog.__init__(self, parent, id, '网站后台重命名', size=(300, 200))
        # 面板
        self.panel = wx.Panel(self) # 最外层容器
        self.headerPanel = wx.Panel(self.panel) # 登录界面重命名
        self.titlePanel = wx.Panel(self.panel) # 后台标题重命名
        self.locPanel = wx.Panel(self.panel) # 标题所在位置信息

        # 控件
        self.headerFlag = wx.StaticText(self.headerPanel, -1, "登录界面名称：")
        self.inputHeader = wx.TextCtrl(self.headerPanel, -1)
        self.titleFlag = wx.StaticText(self.titlePanel, -1, "后台标题名称：")
        self.inputTitle = wx.TextCtrl(self.titlePanel, -1)
        self.locFlag = wx.StaticText(self.locPanel, -1, "位置：")
        self.locTitle = wx.TextCtrl(self.locPanel, -1)
        self.btnModify = buttons.GenButton(self.panel, -1, '修改')
        self.msgName = wx.TextCtrl(self.panel, -1)
        self.locTitle.SetEditable(False)
        self.msgName.SetEditable(False)

        # 布局
        self.panelBox = wx.BoxSizer(wx.VERTICAL) # 垂直
        self.headerPanelBox = wx.BoxSizer(wx.HORIZONTAL) # 水平
        self.titlePanelBox = wx.BoxSizer(wx.HORIZONTAL) # 水平
        self.locPanelBox = wx.BoxSizer(wx.HORIZONTAL) # 水平

        # 登录界面名称： 填充
        self.headerPanelBox.Add(self.headerFlag, 0, wx.EXPAND | wx.ALL, 2)
        self.headerPanelBox.Add(self.inputHeader, 1, wx.EXPAND | wx.ALL, 2)

        # 后台标题名称： 填充
        self.titlePanelBox.Add(self.titleFlag, 0, wx.EXPAND | wx.ALL, 2)
        self.titlePanelBox.Add(self.inputTitle, 1, wx.EXPAND | wx.ALL, 2)

        # 位置：填充
        self.locPanelBox.Add(self.locFlag, 0, wx.EXPAND | wx.ALL, 2)
        self.locPanelBox.Add(self.locTitle, 1, wx.EXPAND | wx.ALL, 2)

        # 整体 填充
        self.panelBox.Add(self.headerPanel, 0, wx.EXPAND | wx.ALL, 2)
        self.panelBox.Add(self.titlePanel, 0, wx.EXPAND | wx.ALL, 2)
        self.panelBox.Add(self.locPanel, 0, wx.EXPAND | wx.ALL, 2)
        self.panelBox.Add(self.btnModify, 1, wx.EXPAND | wx.ALL, 2)
        self.panelBox.Add(self.msgName, 0, wx.EXPAND | wx.ALL, 2)

        # 面板绑定布局
        self.headerPanel.SetSizer(self.headerPanelBox)
        self.titlePanel.SetSizer(self.titlePanelBox)
        self.locPanel.SetSizer(self.locPanelBox)
        self.panel.SetSizer(self.panelBox)

        # 初始化数据
        self._init_data()

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
            wx.MessageBox(f'未做任何修改', '错误', wx.OK | wx.ICON_INFORMATION) # 提示成功

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

        self.locTitle.SetValue('本功能规划中，暂不使用')
        

class ViewGenerateDialog(wx.Dialog):
    def __init__(self, parent, id, **kwargs):
        wx.Dialog.__init__(self, parent, id, '新增视图', size=(700, 500))
        # 总面板
        self.panel = wx.Panel(self) # 最外层容器
