from .basedata import *

"""
    作用：布局
"""

class MainFrameGUI(wx.Frame, BaseData):

    def __init__(self, parent = None):
        BaseData.__init__(self)
        wx.Frame.__init__(self, parent, -1, title = CON_JDJANGO_TITLE, pos = wx.DefaultPosition, size = wx.Size(1000, 580), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
        
        self._init_UI()  # 初始化界面布局
        self._init_menu()  # 初始化菜单栏
        self._init_systoolBar() # 初始化系统工具栏
        self._init_statusbar()  # 初始化底部状态栏
        self._init_ctrls() # 初始化控制器

    def _init_UI(self):
        """面板布局"""
        self.needFonts = [] # 待设置字体的控件

        '''
            大容器（主要是描出四周的黑色边框）
        '''
        self.panel = wx.Panel(self)
        self.panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.panelSizer)
        # self.panel.SetBackgroundColour(CON_COLOR_GREY)
        self.panel.SetBackgroundColour(CON_COLOR_MAIN)

        '''
            顶部弹出信息框
        '''
        self.infoBar = wx.InfoBar(self.panel)
        self.panelSizer.Add(self.infoBar, 0, wx.EXPAND)
        ###  使用方式  ###
        # self.infoBar.ShowMessage("检测成功，具体内容详见输出窗口。", wx.ICON_INFORMATION)
        # 可选第二参数：wx.ICON_NONE、wx.ICON_INFORMATION、wx.ICON_QUESTION、wx.ICON_WARNING、wx.ICON_ERROR

        '''
            实际存储容器（控件全部在这里）
        '''
        self.midPanel = wx.Panel(self.panel)
        self.midPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.midPanel.SetSizer(self.midPanelSizer)
        self.midPanel.SetBackgroundColour('#ffffff')

        '''
            自定义工具条
        '''
        self._init_self_tools()

        '''
            输出提示面板（实时显示操作反馈信息）
        '''
        self._init_choicebook()
        self._init_labelbook()

    def _init_labelbook(self):
        """初始化标签切换控件"""
        self.auiNotebook = aui.AuiNotebook(
            self.panel,
            style = wx.aui.AUI_NB_TAB_SPLIT # 无删除按钮
                # | wx.aui.AUI_NB_TAB_MOVE # 标签可移动变换位置（不允许启用，首个标签不允许删除）
                | wx.aui.AUI_NB_SCROLL_BUTTONS # 左右溢出部分隐藏
                # | wx.aui.AUI_NB_WINDOWLIST_BUTTON # 允许上下左右拖拽
                | wx.aui.AUI_NB_CLOSE_BUTTON # 在最右边显示关掉窗口按钮
                # | wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB # 仅在激活标签上显示关掉窗口按钮
                # | wx.aui.AUI_NB_CLOSE_ON_ALL_TABS # 在所有标签上显示关掉窗口按钮
                # | wx.aui.AUI_NB_MIDDLE_CLICK_CLOSE
                # | wx.aui.AUI_NB_TOP # 限定标签只能显示在最上方，不能随意拖拽
                # | wx.aui.AUI_NB_BOTTOM # 限定标签只能显示在最下方，不能随意拖拽
        )
        
        self.labelBook = LB.LabelBook(
            self.auiNotebook, -1, 
            agwStyle = LB.INB_FIT_BUTTON
                | LB.INB_SHOW_ONLY_TEXT # 仅显示文本
                | LB.INB_LEFT # 显示在右边
                | LB.INB_BORDER # 画出边界
                | LB.INB_DRAW_SHADOW # 描绘按钮阴影
                # | LB.INB_GRADIENT_BACKGROUND # 绘制渐变色
                | LB.INB_WEB_HILITE # hover超链接显示
                | LB.INB_FIT_LABELTEXT
                | LB.INB_BOLD_TAB_SELECTION
        ) # 79 80 73 DFE0D9
        self.labelBook.SetColour(LB.INB_TAB_AREA_BACKGROUND_COLOUR, '#2c3e50')
        # self.labelBook.SetColour(LB.INB_ACTIVE_TAB_COLOUR, colour)
        # self.labelBook.SetColour(LB.INB_TABS_BORDER_COLOUR, colour)
        self.labelBook.SetColour(LB.INB_TEXT_COLOUR, '#ffffff')
        # self.labelBook.SetColour(LB.INB_ACTIVE_TEXT_COLOUR, colour)
        # self.labelBook.SetColour(LB.INB_HILITE_TAB_COLOUR, colour)
        
        self.panelSizer.Add(self.auiNotebook, 1, wx.EXPAND | wx.ALL, 5)

        self.labelBook.AddPage(self.midPanel, '基本功能')
        self.labelBook.AddPage(UrlsListPanel(self.panel), '路由')
        self.labelBook.AddPage(wx.Panel(self.panel), '模型')
        self.labelBook.AddPage(PipListCtrlPanel(self.panel), '三方库')
        self.labelBook.AddPage(BatchExcelPanel(self.panel), '表格批处理')
        self.labelBook.AddPage(wx.Panel(self.panel), '数据可视化')
        self.labelBook.AddPage(wx.Panel(self.panel), '基爬虫API')
        self.labelBook.AddPage(wx.Panel(self.panel), '人工智能API')
        self.labelBook.AddPage(wx.Panel(self.panel), 'VUE快捷操作')
        self.labelBook.AddPage(wx.Panel(self.panel), '命令')
        self.labelBook.AddPage(WxPythonCtrlsPanel(self.panel), 'wxPython控件')

        self.auiNotebook.AddPage(self.labelBook, '核心功能')
        wx.CallAfter(self.auiNotebook.SendSizeEvent)

        # self.labelBook.Refresh()

    def _init_choicebook(self):
        """初始化选择窗口"""
        choicebook = wx.Choicebook(self.midPanel)
        self.midPanelSizer.Add(choicebook, 1, wx.EXPAND | wx.ALL, 1)

        '''
            自定义消息命令行
        '''
        panel1 = wx.Panel(choicebook)
        panel1Sizer = wx.BoxSizer(wx.VERTICAL)
        panel1.SetSizer(panel1Sizer)

        self.infos = wx.TextCtrl(panel1, -1, style=wx.TE_MULTILINE)
        panel1Sizer.Add(self.infos, 1, wx.EXPAND | wx.ALL)

        choicebook.AddPage(panel1, '自定义消息命令行')

        '''
            原生 Python Shell 命令行
        '''
        panel2 = wx.Panel(choicebook)
        panel2Sizer = wx.BoxSizer(wx.VERTICAL)
        panel2.SetSizer(panel2Sizer)

        self.pyShell = wx.py.shell.Shell(panel2, introText='【此环境取自您的本机Python环境，即运行此程序的Python环境】')
        panel2Sizer.Add(self.pyShell, 1, wx.EXPAND | wx.ALL, 0)

        choicebook.AddPage(panel2, f'Python Shell（{sys.version}）')

        '''
            增强版 原生指令行
        '''
        panel3 = wx.Panel(choicebook)
        panel3Sizer = wx.BoxSizer(wx.VERTICAL)
        panel3.SetSizer(panel3Sizer)

        self.pyShellMore = wx.py.crust.Crust(panel3)
        panel3Sizer.Add(self.pyShellMore, 1, wx.EXPAND | wx.ALL, 0)

        choicebook.AddPage(panel3, f'Python Shell增强版（{sys.version}）')

    def _init_menu(self):
        """设置工具栏"""
        self.topBar = wx.MenuBar()  # 创建顶部菜单条
        
        self._init_menu_file() # 文件 菜单项
        self._init_menu_percheck() # 单项检测 菜单项
        self._init_menu_perfix() # 单项修复 菜单项
        self._init_menu_admin() # 后台管理中心 菜单项
        self._init_menu_run() # 运行 菜单项
        self._init_menu_helps() # 帮助 菜单项
        self._init_menu_quit() # 退出 菜单项
        
        self.SetMenuBar(self.topBar)

    def _init_systoolBar(self):
        """初始化系统工具栏"""
        self.sys_toolbar = self.CreateToolBar(wx.TB_HORIZONTAL|wx.NO_BORDER|wx.TB_FLAT) # 工具栏
        # self.sys_toolbar.SetBackgroundColour('#465789')

        # self._append_separator_to_tools()
        # self.shotcut_file = self.sys_toolbar.AddTool(wx.ID_ANY, "选择Django项目", wx.Bitmap(BITMAP_FILE_PATH), shortHelp='选择Django项目')

        self.shotcut_run = self.sys_toolbar.AddTool(wx.ID_ANY, "运行", wx.Bitmap(BITMAP_RUN_PATH), shortHelp='运行')
        self.shotcut_stop = self.sys_toolbar.AddTool(wx.ID_ANY, "停止", wx.Bitmap(BITMAP_STOP_PATH), shortHelp='停止')

        # self._append_separator_to_tools()
        # self.shotcut_database = self.sys_toolbar.AddTool(wx.ID_ANY, "数据库", wx.Bitmap(BITMAP_DATABASE_PATH), shortHelp='数据库')
        # self.shotcut_setting = self.sys_toolbar.AddTool(wx.ID_ANY, "选项/修改", wx.Bitmap(BITMAP_SETTINGS_PATH), shortHelp='选项/修改')

        self._append_separator_to_tools()
        self.shotcut_code = self.sys_toolbar.AddTool(wx.ID_ANY, "VSCode打开", wx.Bitmap(BITMAP_CODE_PATH), shortHelp='VSCode打开')
        self.shotcut_command = self.sys_toolbar.AddTool(wx.ID_ANY, "shell", wx.Bitmap(BITMAP_COMMAND_PATH), shortHelp='shell')

        self._append_separator_to_tools()
        self.shotcut_makemigration = self.sys_toolbar.AddTool(wx.ID_ANY, "makemigration", wx.Bitmap(BITMAP_MAKEMIGRATION_PATH), shortHelp='makemigration')
        self.shotcut_migrate = self.sys_toolbar.AddTool(wx.ID_ANY, "migrate", wx.Bitmap(BITMAP_MIGRATE_PATH), shortHelp='migrate')

        self._append_separator_to_tools()
        self.shotcut_pipinstall = self.sys_toolbar.AddTool(wx.ID_ANY, "pip install", wx.Bitmap(BITMAP_PIPINSTALL_PATH), shortHelp='pip install')

        self._append_separator_to_tools()
        self.shotcut_info = self.sys_toolbar.AddTool(wx.ID_ANY, "帮助", wx.Bitmap(BITMAP_INFO_PATH), shortHelp='帮助')

        self.sys_toolbar.Realize() # Windows 适应

    def _init_menu_file(self):
        """文件"""

        menus = wx.Menu()
        self.topBar.Append(menus, "&文件")
        
        self.menuOpen = menus.Append(wx.ID_OPEN, "&查看文件", "查看文件")

        self._append_separator(menus)
        menusOpenDjango = wx.Menu()
        menus.Append(wx.ID_ANY, "&打开", menusOpenDjango)
        self.menuVSCode = menusOpenDjango.Append(wx.ID_ANY, "&使用VSCode打开项目", "使用VSCode打开项目")

        self._append_separator(menus)
        menusCreate = wx.Menu()
        menus.Append(wx.ID_ANY, "&新建", menusCreate)

        menusCreateVersionProject =  wx.Menu()
        self.create_project = menusCreateVersionProject.Append(wx.ID_ANY, "&Django", "Django")
        menusCreate.Append(wx.ID_ANY, "&项目", menusCreateVersionProject)
        
        self._append_separator(menusCreate)
        self.menuGenerate = menusCreate.Append(wx.ID_ANY, "&应用程序", "应用程序")
        
        self._append_separator(menusCreate)
        modelsSubMenu = wx.Menu()
        self.modelsGenerate = modelsSubMenu.Append(wx.ID_ANY, "&完整模型", "完整模型")
        self.modelsProxyGenerate = modelsSubMenu.Append(wx.ID_ANY, "&代理模型", "代理模型")
        menusCreate.Append(wx.ID_ANY, "&模型", modelsSubMenu)

        self._append_separator(menusCreate)
        self.viewsGenerateFunc = menusCreate.Append(wx.ID_ANY, "&视图", "视图")
        self.create_project.Enable(True)

        self._append_separator(menusCreate)
        self.viewsRestFramework = menusCreate.Append(wx.ID_ANY, "&rest-framework", "rest-framework")

        self._append_separator(menus)
        menusProject = wx.Menu()
        menus.Append(wx.ID_ANY, "&Django项目", menusProject)

        self.menusSettings = menusProject.Append(wx.ID_ANY, "&Settings", "Settings")
        
        self._append_separator(menus)
        settings = wx.Menu()
        menus.Append(wx.ID_ANY, "&工具", settings)

        fonts = wx.Menu()
        settings.Append(wx.ID_ANY, "&字体", fonts)

        self.fonts_minus = fonts.Append(wx.ID_ANY, "&-1", "-1")
        self.fonts_add = fonts.Append(wx.ID_ANY, "&+1", "+1")
        
        self._append_separator(settings)
        self.language = settings.Append(wx.ID_ANY, "&语言", "语言")

        self._append_separator(settings)
        self.sqliteManageTool = settings.Append(wx.ID_ANY, "&SQLite3", "SQLite3")

    def _init_menu_helps(self):
        """帮助"""

        helps = wx.Menu()
        self.topBar.Append(helps, "&帮助")
        
        self.helpsORM = helps.Append(wx.ID_ANY, "&AUTO-ORM", "AUTO-ORM")

        self._append_separator(helps)
        self.helpsDocumentation = helps.Append(wx.ID_ANY, "&参考文档", "参考文档")

        self._append_separator(helps)
        self.helpsSeeOrKill = helps.Append(wx.ID_ANY, "&进程", "进程")

        self._append_separator(helps)
        self.menuAbout = helps.Append(wx.ID_ANY, "&关于", "关于")

    def _init_menu_run(self):
        """运行"""

        portProgress = wx.Menu()
        self.topBar.Append(portProgress, "&运行")

        speeder = wx.Menu()
        portProgress.Append(wx.ID_ANY, "&镜像源", speeder)

        self.portProgressFaster = speeder.Append(wx.ID_ANY, "&一键配置", "一键配置")

        self._append_separator(portProgress)
        virtualenv = wx.Menu()
        portProgress.Append(wx.ID_ANY, "&虚拟环境", virtualenv)

        self.portProgressVirtual = virtualenv.Append(wx.ID_ANY, "&创建", "创建")

        self._append_separator(virtualenv)
        self.portProgressVirtualChoice = virtualenv.Append(wx.ID_ANY, "&绑定", "绑定")

        self._append_separator(virtualenv)
        self.portProgressVirtualView = virtualenv.Append(wx.ID_ANY, "&查看", "查看")

        self._append_separator(portProgress)
        self.portProgressRun = portProgress.Append(wx.ID_ANY, "&运行", "运行")
        self.portProgressStop = portProgress.Append(wx.ID_ANY, "&停止", "停止")
        
        self._append_separator(portProgress)
        djangoOrder = wx.Menu()
        portProgress.Append(wx.ID_ANY, "&原生指令", djangoOrder)

        self.portProgressPipInstall = djangoOrder.Append(wx.ID_ANY, "&pip install", "pip install")
        self.portProgressPipFreeze = djangoOrder.Append(wx.ID_ANY, "&pip freeze", "pip freeze")

        self._append_separator(djangoOrder)
        self.portProgressShell = djangoOrder.Append(wx.ID_ANY, "&shell（Django交互式界面）", "shell（Django交互式界面）")

        self._append_separator(djangoOrder)
        self.portProgressMakemigrations = djangoOrder.Append(wx.ID_ANY, "&makemigrations（数据迁移）", "makemigrations（数据迁移）")
        self.portProgressMigrate = djangoOrder.Append(wx.ID_ANY, "&migrate（数据写入）", "migrate（数据写入）")
        self.portProgressFlush = djangoOrder.Append(wx.ID_ANY, "&flush（数据清空）", "flush（数据清空）")
        self.portProgressCollectstatic = djangoOrder.Append(wx.ID_ANY, "&collectstatic（静态文件收集）", "collectstatic（静态文件收集）")
        self.portProgressCreatesuperuser = djangoOrder.Append(wx.ID_ANY, "&createsupersuer（创建管理员）", "createsupersuer（创建管理员）")
        
        self._append_separator(portProgress)
        progresser = wx.Menu()
        portProgress.Append(wx.ID_ANY, "&进程", progresser)

        self.portProgressKillProgress = progresser.Append(wx.ID_ANY, "&终止进程", "终止进程")

    def _init_menu_quit(self):
        """退出"""

        directExit = wx.Menu()
        self.topBar.Append(directExit, "&退出")

        self.btnDirectExit = directExit.Append(wx.ID_ANY, "&退出", "退出")

    def _init_menu_percheck(self):
        """单项检测"""

        perCheck = wx.Menu()
        self.topBar.Append(perCheck, "&单项检测")

        self.apps_check = perCheck.Append(wx.ID_ANY, "&应用程序", "应用程序")
        self.urls_check = perCheck.Append(wx.ID_ANY, "&路由", "路由")
        self.views_check = perCheck.Append(wx.ID_ANY, "&视图", "视图")
        self.templates_check = perCheck.Append(wx.ID_ANY, "&模板", "模板")
        self.forms_check = perCheck.Append(wx.ID_ANY, "&表单", "表单")
        self.models_check = perCheck.Append(wx.ID_ANY, "&模型", "模型")
        self.database_check = perCheck.Append(wx.ID_ANY, "&数据库", "数据库")

    def _init_menu_perfix(self):
        """单项修复"""

        perFix = wx.Menu()
        self.topBar.Append(perFix, "&单项修复")
        
        self.apps_fix = perFix.Append(wx.ID_ANY, "&应用程序", "应用程序")
        self.urls_fix = perFix.Append(wx.ID_ANY, "&路由", "路由")
        self.views_fix = perFix.Append(wx.ID_ANY, "&视图", "视图")
        self.templates_fix = perFix.Append(wx.ID_ANY, "&模板", "模板")
        self.forms_fix = perFix.Append(wx.ID_ANY, "&表单", "表单")
        self.models_fix = perFix.Append(wx.ID_ANY, "&模型", "模型")
        self.database_fix = perFix.Append(wx.ID_ANY, "&数据库", "数据库")

    def _init_menu_admin(self):
        """管理中心"""
        
        admin = wx.Menu()
        self.topBar.Append(admin, "&后台管理中心")
        
        self.adminGenerateBase = admin.Append(wx.ID_ANY, "&后台绑定模型", "后台绑定模型")

        self._append_separator(admin)
        self.adminRename = admin.Append(wx.ID_ANY, "&修改后台名称", "修改后台名称")

    def _init_statusbar(self):
        """设置状态栏"""
        '''
            状态栏分为三份，比例为 1 : 2 : 1，0代表第一栏，以此类推。
        '''
        sb = self.CreateStatusBar(4)
        self.SetStatusWidths([-1, -2, -5, -1]) # 后期扩展
        self.SetStatusText("Ready", 0)

    def _init_self_tools(self):
        """自定义工具条"""
        '''
            自定义工具条 - 整体
        '''
        toolPanel = wx.Panel(self.midPanel)
        toolPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        toolPanel.SetSizer(toolPanelSizer)
        self.midPanelSizer.Add(toolPanel, 0, wx.EXPAND | wx.ALL, 0)

        '''
            自定义工具条 - 左侧
        '''
        toolLeftPanel = wx.Panel(toolPanel)
        toolLeftPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        toolLeftPanel.SetSizer(toolLeftPanelSizer)
        toolPanelSizer.Add(toolLeftPanel, 0, wx.EXPAND | wx.ALL, 0)

        self.btn_select_project = buttons.GenButton(toolLeftPanel, -1, label='选择Django项目')
        toolLeftPanelSizer.Add(self.btn_select_project, 0, wx.EXPAND | wx.ALL, 0)

        self.btn_check_project = buttons.GenButton(toolLeftPanel, -1, label='[一键]校验')
        toolLeftPanelSizer.Add(self.btn_check_project, 0, wx.EXPAND | wx.ALL, 0)

        self.btn_fixed_project = buttons.GenButton(toolLeftPanel, -1, label='[一键]修复')
        toolLeftPanelSizer.Add(self.btn_fixed_project, 0, wx.EXPAND | wx.ALL, 0)

        self.btn_config_project = buttons.GenButton(toolLeftPanel, -1, label='选项/修改')
        toolLeftPanelSizer.Add(self.btn_config_project, 0, wx.EXPAND | wx.ALL, 0)

        self.btn_clear_text = buttons.GenButton(toolLeftPanel, -1, label='清空')
        toolLeftPanelSizer.Add(self.btn_clear_text, 0, wx.EXPAND | wx.ALL, 0)
        
        self.btn_test = buttons.GenButton(toolLeftPanel, -1, label='测试按钮（后期删除）')
        toolLeftPanelSizer.Add(self.btn_test, 0, wx.EXPAND | wx.ALL, 0)
        self.btn_test.Show(False)

        '''
            自定义工具条 - 右侧
        '''
        toolRightPanel = wx.Panel(toolPanel)
        toolRightPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        toolRightPanel.SetSizer(toolRightPanelSizer)
        toolPanelSizer.Add(toolRightPanel, 1, wx.EXPAND | wx.ALL, 0)

        self.cmdInput = wx.TextCtrl(toolRightPanel, -1, size=(200, -1))
        toolRightPanelSizer.Add(self.cmdInput, 1, wx.EXPAND | wx.ALL, 0)
        
        self.btn_exec = buttons.GenButton(toolRightPanel, -1, '执行/Enter')
        toolRightPanelSizer.Add(self.btn_exec, 0, wx.EXPAND | wx.ALL, 0)

    def _init_ctrls(self):
        """初始化控制器"""
        '''
            全局控件控制
        '''
        self.needFonts.extend([self.infos, self.cmdInput,])
        self.allInitBtns['global'][CON_CONTROL_CHECK].append(self.btn_check_project)
        self.allInitBtns['global'][CON_CONTROL_FIX].append(self.btn_fixed_project)
        self.allInitBtns['global'][CON_CONTROL_OTHER].extend([
            self.btn_config_project, self.menusSettings,
        ])

        '''
            应用程序
        '''
        self.allInitBtns['apps'][CON_CONTROL_CREATE].append(self.menuGenerate)
        self.allInitBtns['apps'][CON_CONTROL_CHECK].append(self.apps_check)
        self.allInitBtns['apps'][CON_CONTROL_FIX].append(self.apps_fix)

        '''
            视图
        '''
        self.allInitBtns['views'][CON_CONTROL_CREATE].extend([
            self.viewsGenerateFunc, 
            # 临时存放 开始
            self.menuVSCode,
            self.helpsORM,
            # """可用性失效，后期需修复"""
            self.shotcut_code,
            self.shotcut_command,
            self.shotcut_makemigration,
            self.shotcut_migrate,
            # 临时存放 结束
        ])
        self.allInitBtns['views'][CON_CONTROL_CHECK].append(self.views_check)
        self.allInitBtns['views'][CON_CONTROL_FIX].append(self.views_fix)

        '''
            路由
        '''
        self.allInitBtns['urls'][CON_CONTROL_CHECK].append(self.urls_check)
        self.allInitBtns['urls'][CON_CONTROL_FIX].append(self.urls_fix)

        '''
            模板
        '''
        self.allInitBtns['templates'][CON_CONTROL_CHECK].append(self.templates_check)
        self.allInitBtns['templates'][CON_CONTROL_FIX].append(self.templates_fix)

        '''
            表单
        '''
        self.allInitBtns['forms'][CON_CONTROL_CHECK].append(self.forms_check)
        self.allInitBtns['forms'][CON_CONTROL_FIX].append(self.forms_fix)

        '''
            模型
        '''
        self.allInitBtns['models'][CON_CONTROL_CREATE].extend([self.modelsGenerate,self.modelsProxyGenerate,])
        self.allInitBtns['models'][CON_CONTROL_CHECK].append(self.models_check)
        self.allInitBtns['models'][CON_CONTROL_FIX].append(self.models_fix)

        '''
            数据库
        '''
        self.allInitBtns['database'][CON_CONTROL_CHECK].append(self.database_check)
        self.allInitBtns['database'][CON_CONTROL_FIX].append(self.database_fix)

        '''
            管理中心
        '''
        self.allInitBtns['admin'][CON_CONTROL_CREATE].extend([
            self.adminGenerateBase,
            self.adminRename,
        ])

    def _append_separator(self, obj):
        """添加分割线"""
        obj.AppendSeparator()

    def _append_separator_to_tools(self):
        """向系统工具栏添加不可点击分割按钮"""
        self.sys_toolbar.AddSeparator()
        # self.sys_toolbar.AddTool(wx.ID_ANY, "", wx.Bitmap(BITMAP_SPLIT_PATH), shortHelp='我是分割符').Enable(False)
