from ..common import *

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
        """列表选中监听事件事件"""
        bId = e.GetId()
        if bId == self.listBoxModels.GetId(): # 选择项目根路径
            selects = self.listBoxModels.GetSelections()
            if len(selects) > 0:
                self.btn_register.Enable(True) # 只有选择了模型才开放注册按钮
            else:
                self.btn_register.Enable(False)

    def onChoiceClick(self, e):
        """下拉框选择App值更新事件"""
        key = e.GetString() # 获取当前选中的应用程序名
        self.listBoxModels.Clear() # 清空列表内容，用于展示当前选中app下的所有模型
        already_regieter_models = get_admin_register_models()
        if key.strip():
            APP_PATH = os.path.join(get_configs(CONFIG_PATH)['dirname'], key) # 路径定位到当前app下
            if os.path.exists(APP_PATH) and os.path.isdir(APP_PATH):
                pys = glob.glob(os.path.join(APP_PATH, '**', '*.py'), recursive=True) # 先取所有归属当前app下的文件路径
                alias = [os.path.basename(_) for _ in env.getModelsAlias()] # 取所有模型别名（如：models.py）
                pathModels = [_ for _ in pys if os.path.basename(_) in alias] # 以别名为依据，过滤所有文件中可能的模型文件
                for obj in [(mo, os.path.basename(_)) for _ in pathModels for mo in toolModel.get_models_from_modelspy(_) if mo not in already_regieter_models]:
                    self.listBoxModels.Append(' ------ '.join(obj)) # 赋值的同时标注模块的来源，用 ' ------ ' 隔开

    def onButtonClick(self, e):
        """界面按钮点击事件"""
        bId = e.GetId()
        if bId == self.btn_register.GetId(): # 注册按钮点击
            self.onRegister(e)

    def onRegister(self, e):
        """注册管理后台模型"""
        dlg = wx.MessageDialog(None, u"确认后，选中的模型将被注册到管理后台。", u"确认注册", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            selectNames = self.listBoxModels.GetStrings()
            selectIndexs = self.listBoxModels.GetSelections()
            modelModels = [selectNames[_] for _ in selectIndexs] # 取出所有要注册的模型
            appName = self.choiceApp.GetStrings()[self.choiceApp.GetSelection()] # 当前选中app名

            modelFiles, models = [], [] # modelFiles 无后缀名
            for _ in modelModels:
                t1, t2 = _.split(' ------ ') # t1是模型类名，t2是t1所在的文件的文件名
                modelFiles.append(t2.split('.')[0]) # t2不取后缀名
                models.append(t1)
            classify = set(modelFiles) # 将所有的模型文件名称去重
            
            importData = {} # 构建插入数据包
            for _ in classify:
                importData[_] = []
            for _ in zip(models, modelFiles):
                importData[_[1]].append(_[0]) # 以文件名为分组依据，将模型归类到对应的文件下
           
            alias = env.getAdminAlias() # 读取admin.py的别名
            for _ in alias:
                # 下面将在所有的模块别名路径中写入注册数据【可能有点不合理】
                insert_path = os.path.join(get_configs(CONFIG_PATH)['dirname'], appName, _) # 因为 _ 别名是包含紧邻app路径之后的路径，所以理论上不管层级有多深，都可以找的到
                write_admin_base(insert_path, importData) # 写入注册代码
            wx.MessageBox(f'{"、".join(models)}注册成功！', '提示', wx.OK | wx.ICON_INFORMATION) # 提示成功
        dlg.Close(True)

class AdminRenameDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = '网站后台重命名', size=(300, 180))
        
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

        # 后台标题名称重命名
        self.headerPanel = wx.Panel(self.panel) 
        self.headerPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.headerPanel.SetSizer(self.headerPanelSizer)
        self.panelSizer.Add(self.headerPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.headerFlag = wx.StaticText(self.headerPanel, -1, "后台标题名称：")
        self.inputHeader = wx.TextCtrl(self.headerPanel, -1)
        self.headerPanelSizer.Add(self.headerFlag, 0, wx.EXPAND | wx.ALL, 2)
        self.headerPanelSizer.Add(self.inputHeader, 1, wx.EXPAND | wx.ALL, 2)

        # 登录界面名称重命名
        self.titlePanel = wx.Panel(self.panel)
        self.titlePanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.titlePanel.SetSizer(self.titlePanelSizer)
        self.panelSizer.Add(self.titlePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.titleFlag = wx.StaticText(self.titlePanel, -1, "登录界面名称：")
        self.inputTitle = wx.TextCtrl(self.titlePanel, -1)
        self.titlePanelSizer.Add(self.titleFlag, 0, wx.EXPAND | wx.ALL, 2)
        self.titlePanelSizer.Add(self.inputTitle, 1, wx.EXPAND | wx.ALL, 2)

        # 末尾按钮 和 提示信息   
        self.panelSizer.Add(self.btnModify, 1, wx.EXPAND | wx.ALL, 2)
        self.panelSizer.Add(self.msgName, 0, wx.EXPAND | wx.ALL, 2)

        # 事件监听
        self.Bind(wx.EVT_BUTTON, self.onBtnModify, self.btnModify)

    def onBtnModify(self, e):
        """确认修改，重命名"""
        value_header = self.inputHeader.GetValue().strip()
        value_title = self.inputTitle.GetValue().strip()
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
