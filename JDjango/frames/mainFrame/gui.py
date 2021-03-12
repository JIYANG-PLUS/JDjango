from .basedata import *

"""
    作用：布局
"""

class MainFrameGUI(wx.Frame, BaseData):

    def __init__(self, parent = None):
        BaseData.__init__(self)
        wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = CON_JDJANGO_TITLE, pos = wx.DefaultPosition, size = wx.Size(960, 540), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
        
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
        panel = wx.Panel(self)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(panelSizer)
        panel.SetBackgroundColour(CON_COLOR_GREY)

        '''
            实际存储容器（控件全部在这里）
        '''
        self.midPanel = wx.Panel(panel)
        self.midPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.midPanel.SetSizer(self.midPanelSizer)
        panelSizer.Add(self.midPanel, 1, wx.EXPAND | wx.ALL, 3)
        self.midPanel.SetBackgroundColour(CON_COLOR_WHITE)

        '''
            自定义工具条
        '''
        self._init_self_tools()

        '''
            项目路径提示框（显示项目路径）
        '''
        self.path = wx.TextCtrl(self.midPanel, -1)
        self.midPanelSizer.Add(self.path, 0, wx.EXPAND | wx.ALL, 5)

        '''
            输出提示面板（实时显示操作反馈信息）
        '''
        self.infos = wx.TextCtrl(self.midPanel, -1, style=wx.TE_MULTILINE)
        self.midPanelSizer.Add(self.infos, 1, wx.EXPAND | wx.ALL, 5)

    def _init_menu(self):
        """设置工具栏"""
        self.topBar = wx.MenuBar()  # 创建顶部菜单条
        
        self._init_menu_file() # 文件 菜单项
        self._init_menu_percheck() # 单项检测 菜单项
        self._init_menu_perfix() # 单项修复 菜单项
        self._init_menu_admin() # 后台管理中心 菜单项
        self._init_menu_run() # 运行 菜单项
        self._init_menu_integrate() # 集成 菜单项
        self._init_menu_helps() # 帮助 菜单项
        self._init_menu_quit() # 退出 菜单项
        
        self.SetMenuBar(self.topBar)

    def _init_systoolBar(self):
        """初始化系统工具栏"""
        self.sys_toolbar = self.CreateToolBar(wx.TBK_HORZ_LAYOUT) # 工具栏
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
        self.create_project_1_10_0 = menusCreateVersionProject.Append(wx.ID_ANY, "&Django1.10.0", "Django1.10.0")
        self.create_project = menusCreateVersionProject.Append(wx.ID_ANY, "&Django3.0.8", "Django3.0.8")
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
        
    def _init_menu_integrate(self):
        """集成 菜单项"""
        integrateMenu = wx.Menu()
        self.topBar.Append(integrateMenu, "&集成")

        kfenv = wx.Menu()
        integrateMenu.Append(wx.ID_ANY, "&路由", kfenv)

        restFramework = wx.Menu()
        kfenv.Append(wx.ID_ANY, "&安装", restFramework)

        self.djangorestframework = restFramework.Append(wx.ID_ANY, "&djangorestframework", "djangorestframework")
        self.markdown = restFramework.Append(wx.ID_ANY, "&markdown", "markdown")
        self.django_filter = restFramework.Append(wx.ID_ANY, "&django-filter", "django-filter")
        self.drf_generators = restFramework.Append(wx.ID_ANY, "&drf-generators", "drf-generators")

        self.registerkfenvRest = kfenv.Append(wx.ID_ANY, "&注册rest_framework", "注册rest_framework")
        self.registerkfenvDrf = kfenv.Append(wx.ID_ANY, "&注册drf_generators", "注册drf_generators")
        self.registerkfenvAll = kfenv.Append(wx.ID_ANY, "&一键注册", "一键注册")

        self._append_separator(integrateMenu)
        adminPFProject = wx.Menu()
        integrateMenu.Append(wx.ID_ANY, "&皮肤", adminPFProject)

        self.fastSimpleui = adminPFProject.Append(wx.ID_ANY, "&simpleui", "simpleui")

        # adminPFProjectSimpleui = wx.Menu()
        # adminPFProject.Append(wx.ID_ANY, "&simpleui", adminPFProjectSimpleui)

        # self.installSimpleui = adminPFProjectSimpleui.Append(wx.ID_ANY, "&安装simpleui", "安装simpleui")
        # self.registerSimpleui = adminPFProjectSimpleui.Append(wx.ID_ANY, "&注册simpleui", "注册simpleui")

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
        sb = self.CreateStatusBar(3)
        self.SetStatusWidths([-1, -2, -1])
        self.SetStatusText("Ready", 0)

    def _init_self_tools(self):
        """自定义工具条"""
        '''
            自定义工具条 - 整体
        '''
        toolPanel = wx.Panel(self.midPanel)
        toolPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        toolPanel.SetSizer(toolPanelSizer)
        self.midPanelSizer.Add(toolPanel, 0, wx.EXPAND | wx.ALL, 5)

        '''
            自定义工具条 - 左侧
        '''
        toolLeftPanel = wx.Panel(toolPanel)
        toolLeftPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        toolLeftPanel.SetSizer(toolLeftPanelSizer)
        toolPanelSizer.Add(toolLeftPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.btn_select_project = buttons.GenButton(toolLeftPanel, -1, label='选择Django项目')
        toolLeftPanelSizer.Add(self.btn_select_project, 0, wx.EXPAND | wx.ALL, 2)

        self.btn_check_project = buttons.GenButton(toolLeftPanel, -1, label='[一键]校验')
        toolLeftPanelSizer.Add(self.btn_check_project, 0, wx.EXPAND | wx.ALL, 2)

        self.btn_fixed_project = buttons.GenButton(toolLeftPanel, -1, label='[一键]修复')
        toolLeftPanelSizer.Add(self.btn_fixed_project, 0, wx.EXPAND | wx.ALL, 2)

        self.btn_config_project = buttons.GenButton(toolLeftPanel, -1, label='选项/修改')
        toolLeftPanelSizer.Add(self.btn_config_project, 0, wx.EXPAND | wx.ALL, 2)

        self.btn_clear_text = buttons.GenButton(toolLeftPanel, -1, label='清空')
        toolLeftPanelSizer.Add(self.btn_clear_text, 0, wx.EXPAND | wx.ALL, 2)

        '''
            自定义工具条 - 右侧
        '''
        toolRightPanel = wx.Panel(toolPanel)
        toolRightPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        toolRightPanel.SetSizer(toolRightPanelSizer)
        toolPanelSizer.Add(toolRightPanel, 1, wx.EXPAND | wx.ALL, 2)

        # self.cmdTip = wx.StaticText(toolRightPanel, -1, "命令：")
        # toolRightPanelSizer.Add(self.cmdTip, 0, wx.EXPAND | wx.ALL, 2)

        self.cmdInput = wx.TextCtrl(toolRightPanel, -1, size=(200, -1))
        toolRightPanelSizer.Add(self.cmdInput, 1, wx.EXPAND | wx.ALL, 2)
        
        self.btn_exec = buttons.GenButton(toolRightPanel, -1, '执行/Enter')
        toolRightPanelSizer.Add(self.btn_exec, 0, wx.EXPAND | wx.ALL, 2)

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
            self.registerkfenvRest,
            self.registerkfenvDrf,
            self.registerkfenvAll,
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
