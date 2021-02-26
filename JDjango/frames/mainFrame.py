import wx, time, os, venv
import wx.lib.buttons as buttons
from ..dialogs.dialogOption import *
from ..dialogs.dialogDocument import *
from ..dialogs.dialogTips import *
from ..dialogs.dialogModels import *
from ..dialogs.dialogViews import *
from ..dialogs.dialogORM import *
from ..miniCmd.djangoCmd import startapp, judge_in_main_urls, fix_urls
from ..miniCmd.miniCmd import CmdTools
from ..tools._tools import *
from ..tools._re import *
from ..tools import environment as env
from ..settings import BASE_DIR, CONFIG_PATH, TEMPLATE_DIR, PRINT_PATH
from ..constant import *

"""
### 新增一个菜单按钮步骤
#1 在菜单合适的位置添加按钮控件；
#2 控制它的可用性，在项目引入之前开放还是之后；
#3 为了简便控制，可以直接加载任意一个功能的create模块下，已达到可用性控制。（不可取但可行）

### 新增命令的步骤
#1 使用 subprocess 添加命令进程；
#2 将进程添加进 cmdCodes 中;
#3 在 info_cmdCodes 添加对照提示信息即可。

"""

cmd = CmdTools() # 命令行对象
# 所有的功能按钮
classifies = ['global', 'apps', 'views', 'urls', 'templates', 'forms', 'models', 'database', 'admin']

class Main(wx.Frame):

    def __init__(self, parent = None):

        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = CON_JDJANGO_TITLE, pos = wx.DefaultPosition, size = wx.Size(960, 540), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.cmdCodes = [] # 所有的控制台指令（用于监听是否结束）
        self.info_cmdCodes = {} # 用于对照输出指令提示信息
        
        # 以下初始化流程必须按顺序进行（自上而下）
        self._init_platform() # 初始化平台类型（加限制）
        self._init_control_btn() # 初始化运行时控制按钮
        self._init_UI()  # 初始化界面布局
        self._init_menu()  # 初始化工具栏
        self._init_statusbar()  # 初始化底部状态栏

        self._disable_all_btn() # 统一设置按钮不可用状态
        self._set_fonts(None) # 统一设置字体大小

        # 独立于初始化之外的其它变量（检测和修复功能专用）
        self.unapps = set()  # 未注册的应用程序
        self.unurls = set() # 未注册的路由
        self.needfix = set() # 需要修复的模块

        # 历史数据
        self._auto_loading_history() # 自动加载历史数据

    def _auto_loading_history(self):
        """自动加载最新的一个历史项目数据"""
        if os.path.exists(CONFIG_PATH):
            # 自动加载
            self._disable_all_btn() # 初始化按钮状态
            try:
                self.dirname = get_configs(CONFIG_PATH)['dirname']
            except:
                self.infos.AppendText(out_infos('历史项目失效！', level=3))
                return
            else:
                if not os.path.exists(self.dirname):
                    self.infos.AppendText(out_infos('历史项目失效！', level=3))
                    return
                if 'manage.py' in os.listdir(self.dirname):
                    self.path.SetValue(f'当前项目路径：{self.dirname}')
                    try:
                        self._init_config() # 初始化配置文件
                    except Exception as e:
                        self.infos.AppendText(out_infos('配置文件config.json初始化失败！', level=3))
                    else:
                        # 开放所有的检测按钮
                        self._open_all_check_btn()
                        # 开放部分必要按钮
                        self._open_part_necessary_btns()
                        self.infos.Clear()
                        # self.path.Clear()
                        self.infos.AppendText(out_infos(f'项目{os.path.basename(self.dirname)}导入成功！', level=1))
                else:
                    self.infos.AppendText(out_infos('历史项目失效！', level=3))

    def _init_control_btn(self):
        """初始化功能按钮控制器"""
        self.allInitBtns = {}
        for _ in classifies:
            self.allInitBtns[_] = {
                CON_CONTROL_CHECK : []
                , CON_CONTROL_FIX : []
                , CON_CONTROL_CREATE : []
                , CON_CONTROL_OTHER : []
            }
        
    def _init_platform(self):
        """初始化并检查"""
        import platform
        self.platform_name = platform.system()
        if self.platform_name.lower() not in env.getAllSupportPlatform():
            wx.MessageBox(f'暂不支持当前平台，已支持：Windows、MacOS。', CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
            self.onExit()
        env.setPlatfrom(self.platform_name)

    def _init_UI(self):
        """面板布局"""
        self.needFonts = [] # 待设置字体的控件
        # 主容器
        panel = wx.Panel(self)  # 最外层容器
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(panelSizer)
        panel.SetBackgroundColour(CON_COLOR_GREY)

        # 子容器
        midPanel = wx.Panel(panel)
        midPanelSizer = wx.BoxSizer(wx.VERTICAL)
        midPanel.SetSizer(midPanelSizer)
        panelSizer.Add(midPanel, 1, wx.EXPAND | wx.ALL, 3)
        midPanel.SetBackgroundColour(CON_COLOR_WHITE)

        # 自定义工具条
        toolPanel = wx.Panel(midPanel)
        toolPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        toolPanel.SetSizer(toolPanelSizer)
        midPanelSizer.Add(toolPanel, 0, wx.EXPAND | wx.ALL, 5)

        # 自定义工具条 - 左侧
        toolLeftPanel = wx.Panel(toolPanel)
        toolLeftPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        toolLeftPanel.SetSizer(toolLeftPanelSizer)
        toolPanelSizer.Add(toolLeftPanel, 1, wx.EXPAND | wx.ALL, 2)

        self.btn_select_project = buttons.GenButton(toolLeftPanel, -1, label='选择Django项目')
        self.btn_clear_text = buttons.GenButton(toolLeftPanel, -1, label='清空')
        self.btn_check_project = buttons.GenButton(toolLeftPanel, -1, label='[一键]校验')
        self.btn_fixed_project = buttons.GenButton(toolLeftPanel, -1, label='[一键]修复')
        self.btn_config_project = buttons.GenButton(toolLeftPanel, -1, label='选项/修改')
        self.btn_docs = buttons.GenButton(toolLeftPanel, -1, label='文档')
        toolLeftPanelSizer.Add(self.btn_select_project, 0, wx.EXPAND | wx.ALL, 2)
        toolLeftPanelSizer.Add(self.btn_check_project, 0, wx.EXPAND | wx.ALL, 2)
        toolLeftPanelSizer.Add(self.btn_fixed_project, 0, wx.EXPAND | wx.ALL, 2)
        toolLeftPanelSizer.Add(self.btn_config_project, 0, wx.EXPAND | wx.ALL, 2)
        toolLeftPanelSizer.Add(self.btn_clear_text, 0, wx.EXPAND | wx.ALL, 2)
        toolLeftPanelSizer.Add(self.btn_docs, 0, wx.EXPAND | wx.ALL, 2)

        # 自定义工具条 - 右侧
        toolRightPanel = wx.Panel(toolPanel)
        toolRightPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        toolRightPanel.SetSizer(toolRightPanelSizer)
        toolPanelSizer.Add(toolRightPanel, 0, wx.EXPAND | wx.ALL, 2)

        cmdTip = wx.StaticText(toolRightPanel, -1, "命令：")
        self.cmdInput = wx.TextCtrl(toolRightPanel, -1, size=(200, -1))  # 输入命令
        self.btn_exec = buttons.GenButton(toolRightPanel, -1, '执行/Enter')
        cmdTip.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        toolRightPanelSizer.Add(cmdTip, 0, wx.EXPAND | wx.ALL, 2)
        toolRightPanelSizer.Add(self.cmdInput, 0, wx.EXPAND | wx.ALL, 2)
        toolRightPanelSizer.Add(self.btn_exec, 0, wx.EXPAND | wx.ALL, 2)

        # 其它控件（非线性控件）
        self.infos = wx.TextCtrl(midPanel, -1, style=wx.TE_MULTILINE)  # 消息框
        self.path = wx.TextCtrl(midPanel, -1)  # 项目选择成功提示框
        self.infos.SetEditable(False)
        self.path.SetEditable(False)
        midPanelSizer.Add(self.path, 0, wx.EXPAND | wx.ALL, 5)
        midPanelSizer.Add(self.infos, 1, wx.EXPAND | wx.ALL, 5)

        # 控制器初始化
        self.needFonts.extend([self.infos, self.cmdInput,])
        self.allInitBtns['global'][CON_CONTROL_CHECK].append(self.btn_check_project)
        self.allInitBtns['global'][CON_CONTROL_FIX].append(self.btn_fixed_project)
        self.allInitBtns['global'][CON_CONTROL_OTHER].append(self.btn_config_project)

        # 事件绑定
        self.Bind(wx.EVT_BUTTON, self.onButtonClick, self.btn_select_project)
        self.Bind(wx.EVT_BUTTON, self.onButtonClick, self.btn_check_project)
        self.Bind(wx.EVT_BUTTON, self.onButtonClick, self.btn_fixed_project)
        self.Bind(wx.EVT_BUTTON, self.onButtonClick, self.btn_config_project)
        self.Bind(wx.EVT_BUTTON, self.onButtonClick, self.btn_exec)
        self.Bind(wx.EVT_BUTTON, self.onButtonClick, self.btn_clear_text)
        self.Bind(wx.EVT_BUTTON, self.onButtonClick, self.btn_docs)
        self.cmdInput.Bind(wx.EVT_KEY_UP, self.OnKeyDown)

    def _init_menu(self):
        """设置工具栏"""
        # 创建文件菜单项
        menus = wx.Menu()
        menuOpen = menus.Append(wx.ID_OPEN, "&查看文件", "查看文件")
        menus.AppendSeparator() # --
        self.menuVSCode = menus.Append(wx.ID_ANY, "&使用VSCode打开项目", "使用VSCode打开项目")
        menus.AppendSeparator() # --
        menusCreate = wx.Menu()
        menusCreateVersionProject =  wx.Menu()
        self.create_project_1_10_0 = menusCreateVersionProject.Append(wx.ID_ANY, "&Django1.10.0", "Django1.10.0")
        self.create_project = menusCreateVersionProject.Append(wx.ID_ANY, "&Django3.0.8", "Django3.0.8")
        menusCreate.Append(wx.ID_ANY, "&项目", menusCreateVersionProject)
        menusCreate.AppendSeparator()
        self.menuGenerate = menusCreate.Append(wx.ID_ANY, "&应用程序", "应用程序")
        menusCreate.AppendSeparator()
        modelsSubMenu = wx.Menu()
        self.modelsGenerate = modelsSubMenu.Append(wx.ID_ANY, "&完整模型", "完整模型")
        self.modelsProxyGenerate = modelsSubMenu.Append(wx.ID_ANY, "&代理模型", "代理模型")
        menusCreate.Append(wx.ID_ANY, "&模型", modelsSubMenu)
        menusCreate.AppendSeparator()
        self.viewsGenerateFunc = menusCreate.Append(wx.ID_ANY, "&视图", "视图")
        self.create_project.Enable(True)
        menus.Append(wx.ID_ANY, "&新建", menusCreate)
        menus.AppendSeparator()
        menusProject = wx.Menu()
        self.menusSettings = menusProject.Append(wx.ID_ANY, "&Settings", "Settings")
        self.allInitBtns['global'][CON_CONTROL_OTHER].append(self.menusSettings)
        self.menusSettings.Enable(False)
        menus.Append(wx.ID_ANY, "&Django项目", menusProject)
        menus.AppendSeparator() # --
        settings = wx.Menu()
        fonts = wx.Menu()
        self.fonts_minus = fonts.Append(wx.ID_ANY, "&-1", "-1")
        self.fonts_add = fonts.Append(wx.ID_ANY, "&+1", "+1")
        settings.Append(wx.ID_ANY, "&字体", fonts)
        settings.AppendSeparator() # --
        self.language = settings.Append(wx.ID_ANY, "&语言", "语言")
        settings.AppendSeparator() # --
        self.sqliteManageTool = settings.Append(wx.ID_ANY, "&SQLite3", "SQLite3")
        menus.Append(wx.ID_ANY, "&工具", settings)
        
        # 帮助 菜单项
        helps = wx.Menu()
        self.helpsORM = helps.Append(wx.ID_ANY, "&ORM一键生成", "ORM一键生成")
        helps.AppendSeparator()
        helpsDocumentation = helps.Append(wx.ID_ANY, "&参考文档", "参考文档")
        helps.AppendSeparator()
        self.helpsSeeOrKill = helps.Append(wx.ID_ANY, "&查看/终止进程", "查看/终止进程")
        helps.AppendSeparator()
        menuAbout = helps.Append(wx.ID_ANY, "&关于", "关于")

        # 运行端口与进程
        portProgress = wx.Menu()
        virtualenv = wx.Menu()
        self.portProgressVirtual = virtualenv.Append(wx.ID_ANY, "&创建", "创建")
        virtualenv.AppendSeparator()
        self.portProgressVirtualChoice = virtualenv.Append(wx.ID_ANY, "&绑定", "绑定")
        virtualenv.AppendSeparator()
        self.portProgressVirtualView = virtualenv.Append(wx.ID_ANY, "&查看", "查看")
        portProgress.Append(wx.ID_ANY, "&虚拟环境", virtualenv)
        portProgress.AppendSeparator()
        self.portProgressRun = portProgress.Append(wx.ID_ANY, "&运行", "运行")
        self.portProgressStop = portProgress.Append(wx.ID_ANY, "&停止", "停止")
        portProgress.AppendSeparator()
        speeder = wx.Menu()
        self.portProgressFaster = speeder.Append(wx.ID_ANY, "&一键配置", "一键配置")
        portProgress.Append(wx.ID_ANY, "&Python镜像", speeder)
        portProgress.AppendSeparator()
        djangoOrder = wx.Menu()
        self.portProgressPipInstall = djangoOrder.Append(wx.ID_ANY, "&pip install", "pip install")
        self.portProgressPipFreeze = djangoOrder.Append(wx.ID_ANY, "&pip freeze", "pip freeze")
        djangoOrder.AppendSeparator()
        self.portProgressShell = djangoOrder.Append(wx.ID_ANY, "&shell（Django交互式界面）", "shell（Django交互式界面）")
        djangoOrder.AppendSeparator()
        self.portProgressMakemigrations = djangoOrder.Append(wx.ID_ANY, "&makemigrations（数据迁移）", "makemigrations（数据迁移）")
        self.portProgressMigrate = djangoOrder.Append(wx.ID_ANY, "&migrate（数据写入）", "migrate（数据写入）")
        self.portProgressFlush = djangoOrder.Append(wx.ID_ANY, "&flush（数据清空）", "flush（数据清空）")
        self.portProgressCollectstatic = djangoOrder.Append(wx.ID_ANY, "&collectstatic（静态文件收集）", "collectstatic（静态文件收集）")
        self.portProgressCreatesuperuser = djangoOrder.Append(wx.ID_ANY, "&createsupersuer（创建管理员）", "createsupersuer（创建管理员）")
        portProgress.Append(wx.ID_ANY, "&原生指令", djangoOrder)
        portProgress.AppendSeparator()
        progresser = wx.Menu()
        self.portProgressKillProgress = progresser.Append(wx.ID_ANY, "&终止进程", "终止进程")
        portProgress.Append(wx.ID_ANY, "&进程", progresser)
        self.portProgressRun.Enable(False)
        self.portProgressStop.Enable(False)
        # self.portProgressVirtual.Enable(False)
        
        # 单项检测
        perCheck = wx.Menu()
        self.apps_check = perCheck.Append(wx.ID_ANY, "&应用程序", "应用程序")
        self.urls_check = perCheck.Append(wx.ID_ANY, "&路由", "路由")
        self.views_check = perCheck.Append(wx.ID_ANY, "&视图", "视图")
        self.templates_check = perCheck.Append(wx.ID_ANY, "&模板", "模板")
        self.forms_check = perCheck.Append(wx.ID_ANY, "&表单", "表单")
        self.models_check = perCheck.Append(wx.ID_ANY, "&模型", "模型")
        self.database_check = perCheck.Append(wx.ID_ANY, "&数据库", "数据库")
        
        # 单项修复
        perFix = wx.Menu()
        self.apps_fix = perFix.Append(wx.ID_ANY, "&应用程序", "应用程序")
        self.urls_fix = perFix.Append(wx.ID_ANY, "&路由", "路由")
        self.views_fix = perFix.Append(wx.ID_ANY, "&视图", "视图")
        self.templates_fix = perFix.Append(wx.ID_ANY, "&模板", "模板")
        self.forms_fix = perFix.Append(wx.ID_ANY, "&表单", "表单")
        self.models_fix = perFix.Append(wx.ID_ANY, "&模型", "模型")
        self.database_fix = perFix.Append(wx.ID_ANY, "&数据库", "数据库")

        # 三方应用集成
        # threeApp = wx.Menu()
        # self.django_sampleui = threeApp.Append(wx.ID_ANY, "&django-simpleui", "django-simpleui")

        # 应用程序
        self.allInitBtns['apps'][CON_CONTROL_CREATE].append(self.menuGenerate)
        self.allInitBtns['apps'][CON_CONTROL_CHECK].append(self.apps_check)
        self.allInitBtns['apps'][CON_CONTROL_FIX].append(self.apps_fix)

        # 视图
        self.allInitBtns['views'][CON_CONTROL_CREATE].extend([
            self.viewsGenerateFunc, 
            self.menuVSCode, # 暂时将VSCode打开的按钮放这里控制流程
            self.helpsORM, # 暂时将orm放在这里参与流程控制
        ])
        self.allInitBtns['views'][CON_CONTROL_CHECK].append(self.views_check)
        self.allInitBtns['views'][CON_CONTROL_FIX].append(self.views_fix)

        # 路由
        # self.urlsGenerate = urls.Append(wx.ID_ANY, "&创建", "创建")
        # self.allInitBtns['urls'][CON_CONTROL_CREATE].append(self.urlsGenerate)
        self.allInitBtns['urls'][CON_CONTROL_CHECK].append(self.urls_check)
        self.allInitBtns['urls'][CON_CONTROL_FIX].append(self.urls_fix)

        # 模板
        # self.templatesGenerate = templates.Append(wx.ID_ANY, "&创建", "创建")
        # self.allInitBtns['templates'][CON_CONTROL_CREATE].append(self.templatesGenerate)
        self.allInitBtns['templates'][CON_CONTROL_CHECK].append(self.templates_check)
        self.allInitBtns['templates'][CON_CONTROL_FIX].append(self.templates_fix)

        # 表单
        # self.formsGenerate = forms.Append(wx.ID_ANY, "&创建", "创建")
        # self.allInitBtns['forms'][CON_CONTROL_CREATE].append(self.formsGenerate)
        self.allInitBtns['forms'][CON_CONTROL_CHECK].append(self.forms_check)
        self.allInitBtns['forms'][CON_CONTROL_FIX].append(self.forms_fix)

        # 模型
        self.allInitBtns['models'][CON_CONTROL_CREATE].extend([self.modelsGenerate,self.modelsProxyGenerate,])
        self.allInitBtns['models'][CON_CONTROL_CHECK].append(self.models_check)
        self.allInitBtns['models'][CON_CONTROL_FIX].append(self.models_fix)

        # 数据库
        # self.databaseGenerate = database.Append(wx.ID_ANY, "&创建", "创建")
        # self.allInitBtns['database'][CON_CONTROL_CREATE].append(self.databaseGenerate)
        self.allInitBtns['database'][CON_CONTROL_CHECK].append(self.database_check)
        self.allInitBtns['database'][CON_CONTROL_FIX].append(self.database_fix)

        # 管理中心 菜单项
        admin = wx.Menu()
        self.adminGenerateBase = admin.Append(wx.ID_ANY, "&后台绑定模型", "后台绑定模型")
        # self.adminGenerateComplex = admin.Append(wx.ID_ANY, "&创建复杂管理中心", "创建复杂管理中心")
        # admin.AppendSeparator()
        # self.admin_check = admin.Append(wx.ID_ANY, "&校验", "校验")
        # self.admin_fix = admin.Append(wx.ID_ANY, "&修复", "修复")
        admin.AppendSeparator()
        self.adminRename = admin.Append(wx.ID_ANY, "&修改后台名称", "修改后台名称")
        # admin.AppendSeparator()
        # self.quickAdminGenerateBase = admin.Append(wx.ID_ANY, "&一键创建简单管理中心", "一键创建简单管理中心")
        # self.quickAdminGenerateComplex = admin.Append(wx.ID_ANY, "&一键创建复杂管理中心", "一键创建复杂管理中心")

        self.allInitBtns['admin'][CON_CONTROL_CREATE].extend([
            self.adminGenerateBase
            # , self.adminGenerateComplex
            , self.adminRename
            # , self.quickAdminGenerateBase
            # , self.quickAdminGenerateComplex
        ])
        # self.allInitBtns['admin'][CON_CONTROL_CHECK].append(self.admin_check)
        # self.allInitBtns['admin'][CON_CONTROL_FIX].append(self.admin_fix)

        # 退出 菜单项
        directExit = wx.Menu()
        self.btnDirectExit = directExit.Append(wx.ID_ANY, "&退出", "退出")

        menuBar = wx.MenuBar()  # 创建顶部菜单条
        menuBar.Append(menus, "&文件")  # 将菜单添加进菜单条中（无法两次加入同一个菜单对象）
        menuBar.Append(perCheck, "&单项检测")
        menuBar.Append(perFix, "&单项修复")
        menuBar.Append(admin, "&后台管理中心")
        menuBar.Append(portProgress, "&运行")
        # menuBar.Append(threeApp, "&三方应用集成")
        menuBar.Append(helps, "&帮助")
        menuBar.Append(directExit, "&退出")
        self.SetMenuBar(menuBar)

        # 子菜单绑定事件
        self.Bind(wx.EVT_MENU, self.onAbout, menuAbout)  # 关于菜单项点击事件
        self.Bind(wx.EVT_MENU, self.onHelpsDocumentation, helpsDocumentation)  # 帮助文档
        self.Bind(wx.EVT_MENU, self.onOpen, menuOpen)  # 文件打开点击事件
        self.Bind(wx.EVT_MENU, self.onGenerate, self.menuGenerate)  # 代码生成点击事件
        self.Bind(wx.EVT_MENU, self.onMenusSettings, self.menusSettings)  # Settings
        self.Bind(wx.EVT_MENU, self.onMenuVSCode, self.menuVSCode)  # VSCode

        # 三方应用集成
        # self.Bind(wx.EVT_MENU, self.onDjangoSampleui, self.django_sampleui)  # django_sampleui

        # 应用程序  事件绑定
        self.Bind(wx.EVT_MENU, self.onAppsCheck, self.apps_check) # 检测
        self.Bind(wx.EVT_MENU, self.onAppsFix, self.apps_fix) # 修复

        # 管理中心 事件绑定
        self.Bind(wx.EVT_MENU, self.onAdminGenerateBase, self.adminGenerateBase) # 创建简单管理中心
        self.Bind(wx.EVT_MENU, self.onAdminRename, self.adminRename) # 修改后台网站名

        # 工具 事件绑定
        self.Bind(wx.EVT_MENU, self.onFontsMinus, self.fonts_minus) # 字体减小
        self.Bind(wx.EVT_MENU, self.onFontsAdd, self.fonts_add) # 字体减小
        self.Bind(wx.EVT_MENU, self.onSqliteManageTool, self.sqliteManageTool) # SqLite

        # 视图 事件绑定
        self.Bind(wx.EVT_MENU, self.onViewsGenerateFunc, self.viewsGenerateFunc) # 新增视图（多样新增）

        # 模型
        self.Bind(wx.EVT_MENU, self.onModelsGenerate, self.modelsGenerate)
        self.Bind(wx.EVT_MENU, self.onModelsProxyGenerate, self.modelsProxyGenerate)

        # 路由 事件绑定
        self.Bind(wx.EVT_MENU, self.onUrlsCheck, self.urls_check) # 检查路由
        self.Bind(wx.EVT_MENU, self.onUrlsFix, self.urls_fix) # 修复路由

        # 新项目 事件绑定
        self.Bind(wx.EVT_MENU, self.onCreateProject, self.create_project) # 新建项目
        self.Bind(wx.EVT_MENU, self.onCreateProject1100, self.create_project_1_10_0) # 新建项目

        # 运行 事件绑定
        self.Bind(wx.EVT_MENU, self.onPortProgressRun, self.portProgressRun) # 运行
        self.Bind(wx.EVT_MENU, self.onPortProgressStop, self.portProgressStop)
        self.Bind(wx.EVT_MENU, self.onPortProgressVirtualChoice, self.portProgressVirtualChoice) 
        self.Bind(wx.EVT_MENU, self.onHelpSeeOrKill, self.helpsSeeOrKill) 
        self.Bind(wx.EVT_MENU, self.onHelpsORM, self.helpsORM) 
        self.Bind(wx.EVT_MENU, self.onPortProgressFaster, self.portProgressFaster) 
        self.Bind(wx.EVT_MENU, self.onPortProgressKillProgress, self.portProgressKillProgress) 
        self.Bind(wx.EVT_MENU, self.onPortProgressVirtual, self.portProgressVirtual) 
        self.Bind(wx.EVT_MENU, self.onPortProgressMakemigrations, self.portProgressMakemigrations)
        self.Bind(wx.EVT_MENU, self.onPortProgressShell, self.portProgressShell)
        self.Bind(wx.EVT_MENU, self.onPortProgressMigrate, self.portProgressMigrate) 
        self.Bind(wx.EVT_MENU, self.onPortProgressFlush, self.portProgressFlush) 
        self.Bind(wx.EVT_MENU, self.onPortProgressCreatesuperuser, self.portProgressCreatesuperuser) 
        self.Bind(wx.EVT_MENU, self.onPortProgressPipInstall, self.portProgressPipInstall) 
        self.Bind(wx.EVT_MENU, self.onPortProgressPipFreeze, self.portProgressPipFreeze) 
        self.Bind(wx.EVT_MENU, self.onPortProgressCollectstatic, self.portProgressCollectstatic) 
        self.Bind(wx.EVT_MENU, self.onPortProgressVirtualView, self.portProgressVirtualView) 

        # 退出 事件绑定
        self.Bind(wx.EVT_MENU, self.onExit, self.btnDirectExit)

    def onHelpsORM(self, e):
        """ORM帮助（一键生成）"""
        dlg = ORMDialog(self)
        dlg.ShowModal()
        dlg.Close(True)

    # def onDjangoSampleui(self, e):
    #     """sampleui管理后台集成"""
    #     TipsMessageOKBox(self, "功能正在准备中", '待定')

    def onMenuVSCode(self, e):
        """外部发起VSCode编辑"""
        dlg_tip = wx.MessageDialog(self, f"打开之前请确认您已经安装了Visual Studio Code，并且已经配置了code环境。", CON_TIPS_COMMON, wx.CANCEL | wx.OK)
        if dlg_tip.ShowModal() == wx.ID_OK:
            import subprocess
            dirname = get_configs(CONFIG_PATH)['dirname']

            self.cmdVscode = subprocess.Popen(f'code {dirname}', shell=True)
            self.cmdCodes.append(self.cmdVscode)
            self.info_cmdCodes[self.cmdVscode] = '开启VSCode编辑器'
        dlg_tip.Close(True)

    def onPortProgressVirtualView(self, e):
        """查看虚拟环境路径"""
        TipsMessageOKBox(self, env.getPython3Env(), '虚拟环境路径')

    @property
    def _check_env_exist(self)->bool:
        """检测虚拟环境是否存在"""
        env_path = env.getPython3Env()
        if '' == env_path.strip() or not os.path.exists(env_path):
            return False
        return True

    def onPortProgressCollectstatic(self, e):
        """python manage.py collectstatic"""
        if not self._check_env_exist:
            wx.MessageBox(f'虚拟环境未绑定，或绑定失败！', CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
            return
            
        import subprocess
        path = os.path.join(get_configs(CONFIG_PATH)['dirname'], 'manage.py')
        env_python3 = os.path.splitext(env.getPython3Env())[0]

        self.amdSubProcess = subprocess.Popen(f'{env_python3} {path} collectstatic', shell=True)
        self.cmdCodes.append(self.amdSubProcess)
        self.info_cmdCodes[self.amdSubProcess] = 'collectstatic'

    def onPortProgressPipFreeze(self, e):
        """导出包pip freeze"""
        if not self._check_env_exist:
            wx.MessageBox(f'虚拟环境未绑定，或绑定失败！', CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
            return
        
        import subprocess
        env_python3_pip = os.path.join(os.path.dirname(env.getPython3Env()), 'pip')
        self.cmdEnvPipFreeze = subprocess.Popen(f'{env_python3_pip} freeze', shell=True)
        self.cmdCodes.append(self.cmdEnvPipFreeze)
        self.info_cmdCodes[self.cmdEnvPipFreeze] = 'freeze'

    def onPortProgressPipInstall(self, e):
        """虚拟环境安装包pip install"""
        if not self._check_env_exist:
            wx.MessageBox(f'虚拟环境未绑定，或绑定失败！', CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
            return
        
        dlg = wx.TextEntryDialog(self, u"包名：", u"虚拟环境安装三方库", u"")
        if dlg.ShowModal() == wx.ID_OK:
            module_name = dlg.GetValue()

            import subprocess
            
            env_python3_pip = os.path.join(os.path.dirname(env.getPython3Env()), 'pip')

            self.cmdPipInstall = subprocess.Popen(f'{env_python3_pip} install {module_name}', shell=True)
            self.cmdCodes.append(self.cmdPipInstall)
            self.info_cmdCodes[self.cmdPipInstall] = 'install'
        dlg.Close(True)

    def onPortProgressShell(self, e):
        """python manage.py shell"""
        if not self._check_env_exist:
            wx.MessageBox(f'虚拟环境未绑定，或绑定失败！', CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
            return

        import subprocess
        path = os.path.join(get_configs(CONFIG_PATH)['dirname'], 'manage.py')
        env_python3 = os.path.splitext(env.getPython3Env())[0]

        self.cmdDjangoShell = subprocess.Popen(f'{env_python3} {path} shell', shell=True)
        self.cmdCodes.append(self.cmdDjangoShell)
        self.info_cmdCodes[self.cmdDjangoShell] = 'shell'
        

    def onPortProgressMakemigrations(self, e):
        """python manage.py makemigrations"""
        if not self._check_env_exist:
            wx.MessageBox(f'虚拟环境未绑定，或绑定失败！', CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
            return
            
        import subprocess
        path = os.path.join(get_configs(CONFIG_PATH)['dirname'], 'manage.py')
        env_python3 = os.path.splitext(env.getPython3Env())[0]

        self.cmdMakemigrations = subprocess.Popen(f'{env_python3} {path} makemigrations', shell=True)
        self.cmdCodes.append(self.cmdMakemigrations)
        self.info_cmdCodes[self.cmdMakemigrations] = 'makemigrations'

    def onPortProgressMigrate(self, e):
        """python manage.py migtrate"""
        if not self._check_env_exist:
            wx.MessageBox(f'虚拟环境未绑定，或绑定失败！', CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
            return
            
        import subprocess
        path = os.path.join(get_configs(CONFIG_PATH)['dirname'], 'manage.py')
        env_python3 = os.path.splitext(env.getPython3Env())[0]

        self.cmdMigrate = subprocess.Popen(f'{env_python3} {path} migrate', shell=True)
        self.cmdCodes.append(self.cmdMigrate)
        self.info_cmdCodes[self.cmdMigrate] = 'migrate'

    def onPortProgressFlush(self, e):
        """python manage.py flush"""
        if not self._check_env_exist:
            wx.MessageBox(f'虚拟环境未绑定，或绑定失败！', CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
            return
             
        import subprocess
        path = os.path.join(get_configs(CONFIG_PATH)['dirname'], 'manage.py')
        env_python3 = os.path.splitext(env.getPython3Env())[0]

        self.cmdFlush = subprocess.Popen(f'{env_python3} {path} flush', shell=True)
        self.cmdCodes.append(self.cmdFlush)
        self.info_cmdCodes[self.cmdFlush] = 'flush'

    def onPortProgressCreatesuperuser(self, e):
        """python manage.py createsuperuser"""
        if not self._check_env_exist:
            wx.MessageBox(f'虚拟环境未绑定，或绑定失败！', CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
            return
            
        import subprocess
        path = os.path.join(get_configs(CONFIG_PATH)['dirname'], 'manage.py')
        env_python3 = os.path.splitext(env.getPython3Env())[0]

        self.cmdCreateSuperuser = subprocess.Popen(f'{env_python3} {path} createsuperuser', shell=True)
        self.cmdCodes.append(self.cmdCreateSuperuser)
        self.info_cmdCodes[self.cmdCreateSuperuser] = 'createsuperuser'

    def onCreateProject1100(self, e):
        """创建Django1.10.0项目"""
        TipsMessageOKBox(self, '待考虑的功能。', '提示')

    def onPortProgressVirtual(self, e):
        """创建虚拟环境"""
        # venv.create(env_dir, system_site_packages=False, clear=False, symlinks=False, with_pip=False, prompt=None)
        dlg = wx.DirDialog(self, u"选择即将写入的虚拟环境文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            env_dir = dlg.GetPath()
            t = len(os.listdir(env_dir))
            if t > 0:
                TipsMessageOKBox(self, f'检测到选择的文件夹下存在其它文件，禁止操作。', '提示')
            else:
                venv.create(env_dir, system_site_packages=False, clear=True, symlinks=False, with_pip=True, prompt=None)
                TipsMessageOKBox(self, f'创建成功，虚拟目录：{env_dir}', '提示')
        dlg.Destroy()

    def onPortProgressKillProgress(self, e):
        """终止进程"""
        dlg = wx.TextEntryDialog(self, u"占用端口号：", u"终止进程", u"")
        if dlg.ShowModal() == wx.ID_OK:
            port = dlg.GetValue()
            env.killProgress(port = port)
            TipsMessageOKBox(self, '已终止', '提示信息')
        dlg.Close(True)

    def onPortProgressFaster(self, e):
        """一键配置镜像环境"""
        rpath = os.path.expanduser('~')
        # 根据系统依次安装镜像环境
        platform = env.getPlatform().lower()
        if 'windows' == platform:
            if 'pip' in os.listdir(rpath):
                pip_path = os.path.join(rpath, 'pip')
                if 'pip.ini' in os.listdir(pip_path):
                    TipsMessageOKBox(self, '当前环境已配置镜像。', '重复提醒')
                else:
                    # TEMPLATE_DIR
                    write_file(os.path.join(pip_path, 'pip.ini'), read_file(os.path.join(TEMPLATE_DIR, 'pip', 'pip.ini')))
                    TipsMessageOKBox(self, '配置成功！', '提示')
            else:
                pip_path = os.path.join(rpath, 'pip')
                os.mkdir(pip_path)
                write_file(os.path.join(pip_path, 'pip.ini'), read_file(os.path.join(TEMPLATE_DIR, 'pip', 'pip.ini')))
                TipsMessageOKBox(self, '配置成功！', '提示')
        elif 'linux' == platform: # 理论上，Mac和Linux配置镜像环境步骤一致
            if '.pip' in os.listdir(rpath):
                pip_path = os.path.join(rpath, '.pip')
                if 'pip.conf' in os.listdir(pip_path):
                    TipsMessageOKBox(self, '当前环境已配置镜像。', '重复提醒')
                else:
                    write_file(os.path.join(pip_path, 'pip.conf'), read_file(os.path.join(TEMPLATE_DIR, 'pip', 'pip.ini')))
                    TipsMessageOKBox(self, '配置成功！', '提示')
            else:
                pip_path = os.path.join(rpath, '.pip')
                os.mkdir(pip_path)
                write_file(os.path.join(pip_path, 'pip.conf'), read_file(os.path.join(TEMPLATE_DIR, 'pip', 'pip.ini')))
                TipsMessageOKBox(self, '配置成功！', '提示')
        elif 'darwin' == platform:
            if '.pip' in os.listdir(rpath):
                pip_path = os.path.join(rpath, '.pip')
                if 'pip.conf' in os.listdir(pip_path):
                    TipsMessageOKBox(self, '当前环境已配置镜像。', '重复提醒')
                else:
                    write_file(os.path.join(pip_path, 'pip.conf'), read_file(os.path.join(TEMPLATE_DIR, 'pip', 'pip.ini')))
                    TipsMessageOKBox(self, '配置成功！', '提示')
            else:
                pip_path = os.path.join(rpath, '.pip')
                os.mkdir(pip_path)
                write_file(os.path.join(pip_path, 'pip.conf'), read_file(os.path.join(TEMPLATE_DIR, 'pip', 'pip.ini')))
                TipsMessageOKBox(self, '配置成功！', '提示')
        else:
            TipsMessageOKBox(self, '未知系统', '提示')

    def onModelsProxyGenerate(self, e):
        """创建代理模型"""

    def onPortProgressStop(self, e):
        """关闭网站运行状态"""
        self.portProgressRun.Enable(True)
        self.portProgressStop.Enable(False)
        try:
            self.server.terminate()
            env.killProgress()
        except:
            self.infos.AppendText(out_infos(f"网站未正常启动或启动异常，导致关闭失败。", level=3))
        else:
            self.infos.AppendText(out_infos(f"网站已关闭。", level=1))

    def onPortProgressVirtualChoice(self, e):
        """选择虚拟环境"""
        dlg = wx.FileDialog(self, "选择虚拟环境下的python.exe文件", "", "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            env.setPython3Env(os.path.join(dlg.GetDirectory(), dlg.GetFilename()))
            wx.MessageBox(f'虚拟环境绑定成功！', CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
        dlg.Close(True)
    
    def onHelpSeeOrKill(self, e):
        """查看或终止进程"""
        TipsMessageOKBox(self, CON_MSG_PROGRESS_USE, CON_TIPS_COMMON)

    def onPortProgressRun(self, e):
        """子进程运行Django"""
        # 运行前必要检查
        # 检查一：虚拟环境是否正确配置
        if not self._check_env_exist:
            wx.MessageBox(f'虚拟环境未绑定，或绑定失败！', CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
            return

        # 检查二：项目路径是否正确（此处可省略，此步骤前已经多处检查）

        import subprocess
        path = os.path.join(get_configs(CONFIG_PATH)['dirname'], 'manage.py')
        port = env.getDjangoRunPort()
        env_python3 = os.path.splitext(env.getPython3Env())[0]
        try:
            self.server = subprocess.Popen(f'{env_python3} {path} runserver {port}', shell=True) # , stderr=subprocess.PIPE, stdout=subprocess.PIPE
        except:
            self.infos.AppendText(out_infos(f"虚拟环境错误，或项目路径错误，或端口被占用。", level=3))
        else:
            import webbrowser
            webbrowser.open(f"http://127.0.0.1:{port}/admin/")
            self.infos.AppendText(out_infos(f"网站正在运行，根路由：http://127.0.0.1:{port}。可复制到浏览器打开", level=1))
            self.portProgressRun.Enable(False)
            self.portProgressStop.Enable(True)

    def onModelsGenerate(self, e):
        """创建模型"""
        dlg = ModelsCreateDialog(self)
        dlg.ShowModal()
        dlg.Close(True)

    def onSqliteManageTool(self, e):
        """跨平台的Sqlite工具"""
        # dlg = wx.MessageDialog(self, "请双击同级目录下的sqlite3Manager.pyw启动文件。", CON_TIPS_COMMON, wx.OK)
        # dlg.ShowModal()
        # dlg.Close(True)
        import subprocess
        manager = os.path.join(os.path.dirname(BASE_DIR), 'sqlite3Manager.pyw')
        subprocess.Popen(f'{env.getRealPythonOrder()} {manager}', shell=True)

    def onMenusSettings(self, e):
        """Settings"""
        dlg = SettingsDialog(self)
        dlg.ShowModal()
        dlg.Close(True)

    def onHelpsDocumentation(self, e):
        """帮助文档"""
        dlg = DocumentationDialog(self)
        dlg.ShowModal()
        dlg.Close(True)

    def onCreateProject(self, e):
        """新建项目"""
        dlg = ProjectCreateDialog(self)
        dlg.ShowModal()
        dlg.Close(True)

    def onUrlsFix(self, e):
        """修复路由"""
        for _ in self.unurls:
            fix_urls(_) # 逐个修复
            self.infos.AppendText(out_infos(f"{_}注册完成！", level=1))
        else:
            self.unurls.clear()
            self.infos.AppendText(out_infos(f"路由修复完成！", level=1))
            if 'urls' in self.needfix:
                self.needfix.remove('urls')
            self._open_checked_fix_btn('urls', f_type='close')

    def onUrlsCheck(self, e):
        """检查路由"""
        # 检查情形有：
        # 只针对以本工具生成的app，而不是Django原生命令python manage.py startapp ...
        # 路由必须在主路径urls.py中用include()函数注册
        # 默认未每个应用程序注册ulrs，取environment.py中的urls别名
        self.unurls = set(judge_in_main_urls()) # 全局监测
        if len(self.unurls) <= 0:
            self._open_checked_fix_btn('urls', f_type='close')
            self.infos.AppendText(out_infos(f"路由检测完成，无已知错误。", level=1))
        else:
            msg = '，'.join(self.unurls)
            self.infos.AppendText(out_infos(f"{msg}未注册。", level=3))
            self._open_checked_fix_btn('urls')
        
    def onAdminRename(self, e):
        """重命名后台名称"""
        dlg = AdminRenameDialog(self)
        dlg.ShowModal()
        dlg.Close(True)

    def onViewsGenerateFunc(self, e):
        """多样式新增视图"""
        dlg = ViewGenerateDialog(self)
        dlg.ShowModal()
        dlg.Close(True)

    def onFontsMinus(self, e):
        """显示框字体减小"""
        env.setFontSize(step = 1, method = 'minus')
        self._set_fonts(e)

    def onFontsAdd(self, e):
        """显示框字体增大"""
        env.setFontSize(step = 1, method = 'add')
        self._set_fonts(e)

    def _set_fonts(self, e):
        """统一设置字体"""
        font = wx.Font(env.getFontSize(), wx.SWISS, wx.NORMAL, wx.BOLD, False)
        for _ in self.needFonts:
            _.SetFont(font)

    def OnKeyDown(self, event):
        """键盘监听"""
        code = event.GetKeyCode()
        if wx.WXK_NUMPAD_ENTER == code or 13 == code:
            self.onExecCommand()

    def _init_statusbar(self):
        """设置状态栏"""
        # 状态栏
        sb = self.CreateStatusBar(3)  # 状态栏分成三份
        self.SetStatusWidths([-1, -2, -1])  # 比例为1:2:1
        self.SetStatusText("Ready", 0)  # 0代表第一个栏，Ready为内容
        
        # 循环定时器
        self.timer = wx.PyTimer(self.notify)
        self.timer.Start(1000, wx.TIMER_CONTINUOUS)
        self.notify()

    def notify(self):
        """底部信息二、三栏提示"""
        now_time = time.localtime(time.time())
        format_time = time.strftime('%Y-%m-%d %H:%M:%S', now_time)
        self.SetStatusText(f'系统时间：{format_time}', 1)  # 这里的1代表将时间放入状态栏的第二部分上
        try:
            if (None == self.server.poll()):
                self.SetStatusText("网站正在运行中", 2)
            else:
                self.SetStatusText("网站已关闭", 2)
        except:
            self.SetStatusText("网站已关闭", 2)

        # 监听指令
        for i, _ in enumerate(self.cmdCodes[::-1]):
            try:
                if (None != _.poll()):
                    t_info = self.info_cmdCodes[_]
                    info = f"【{t_info}】指令执行完成！"
                    self.infos.AppendText(out_infos(info, level=1))
                    # 往进程添加提示信息
                    import subprocess
                    python_order = env.getRealPythonOrder()
                    mode = 'print'
                    self.cmdPipInstall = subprocess.Popen(f'{python_order} {PRINT_PATH} {mode} {info}', shell=True)

                    # 已经完成的命令进行移除
                    self.cmdCodes.pop(i)
            except:
                self.infos.AppendText(out_infos(f"程序级错误，请联系作者修复。", level=3))

    def onAbout(self, e):
        """关于"""
        TipsMessageOKBox(self, "关于软件：目前为个人使用版。【部分功能正在实现】", CON_TIPS_COMMON)

    def onExit(self, e):
        """退出"""
        self.Close(True)

    def onOpen(self, e):
        """查看文件"""
        self.dirname = r''
        dlg = wx.FileDialog(self, "选择一个文件", self.dirname, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            with open(os.path.join(self.dirname, self.filename), 'r', encoding="utf-8") as f:
                self.infos.SetValue(f.read())
        dlg.Close(True)

    def onClear(self, e):
        """清空提示台"""
        self.infos.Clear()

    def onGenerate(self, e):
        """生成应用程序"""
        dlg = wx.TextEntryDialog(None, u"请输入应用程序名：", u"创建应用程序", u"")
        if dlg.ShowModal() == wx.ID_OK:
            message = dlg.GetValue()  # 获取文本框中输入的值
            returnStatus = startapp(message)
            if 0 == returnStatus:
                self.unapps.add(message)
                url_alias = [os.path.basename(_).split('.')[0] for _ in env.getUrlsAlias()][0]
                self.unurls.add(f'{message}.{url_alias}')
                self.infos.AppendText(out_infos(f"{message}应用程序创建成功！", level=1))
                dlg_tip = wx.MessageDialog(None, f"{message}创建成功！", CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
                if dlg_tip.ShowModal() == wx.ID_OK: pass
                dlg_tip.Close(True)
                self.onAppsFix(e) # 自动完成注册
                self.onUrlsFix(e) # 自动完成路由注册
                self._init_config() # 重新初始化 配置文件【此操作为敏感操作】
            else:
                dlg_tip = wx.MessageDialog(None, f"{message}应用程序名已存在，或不符合纯字母+数字命名的约定！", CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
                if dlg_tip.ShowModal() == wx.ID_OK: pass
                dlg_tip.Close(True)
        dlg.Close(True)

    def onButtonClick(self, e):
        """界面按钮点击事件"""
        bId = e.GetId()
        if bId == self.btn_select_project.GetId(): # 选择项目根路径
            self.onSelectProjectRoot()
        elif bId == self.btn_check_project.GetId(): # 检测/校验项目
            self.onCheckGlobalProject(e)
        elif bId == self.btn_fixed_project.GetId(): # 修复项目
            self.onFixGlobalProject(e)
        elif bId == self.btn_config_project.GetId(): # 项目配置和修改
            dlg = SettingsDialog(self)
            dlg.ShowModal()
            dlg.Close(True)
        elif bId == self.btn_exec.GetId(): # 执行命令
            self.onExecCommand()
        elif bId == self.btn_clear_text.GetId():
            self.onClear(e)
        elif bId == self.btn_docs.GetId():
            self.onBtnOpenDocs(e)

    def onBtnOpenDocs(self, e):
        """查看帮助文档"""
        dlg = DocumentationDialog(self)
        dlg.ShowModal()
        dlg.Close(True)

    def onExecCommand(self):
        """仿Linux命令"""
        command = self.cmdInput.GetValue().strip()
        try:
            order_split = [_ for _ in command.split() if _]
            if order_split:
                args = order_split[1:]
                if 'ls' == order_split[0].lower():
                    s = cmd.ls(*args)
                elif 'pwd' == command.lower():
                    s = cmd.pwd()
                elif 'cd' == order_split[0].lower():
                    s = cmd.cd(*args)
                elif 'zip' == order_split[0].lower():
                    s = cmd.zip(*args)
                elif 'unzip' == order_split[0].lower():
                    s = cmd.unzip(*args)
                elif 'rm' == order_split[0].lower():
                    s = cmd.rm(*args)
                elif 'mkdir' == order_split[0].lower():
                    s = cmd.mkdir(*args)
                elif 'mkfile' == order_split[0].lower():
                    s = cmd.mkfile(*args)
                elif 'ping' == order_split[0].lower():
                    s = cmd.ping(*args)
                elif 'date' == command.lower():
                    s = cmd.date()
                elif 'print' == order_split[0].lower():
                    s = cmd.print(' '.join(args))
                else:
                    s = cmd.exec(' '.join(order_split))
                self.infos.AppendText(out_command_infos(command))
                if s:
                    self.infos.AppendText(f"{s}\n")
                self.cmdInput.Clear()
        except Exception as e:
            self.infos.AppendText(out_infos(f'{e}'))

    def _init_config(self):
        """初始化配置文件"""
        configs = {} # 全局配置文件待写入
        # 必要前缀赋值
        configs['dirname'] = self.dirname # 项目路径
        configs['project_name'] = os.path.basename(self.dirname) # 项目名称
        apps = os.listdir(self.dirname) # 所有的应用程序（包含主程序）
        try:
            apps.remove(configs['project_name']) # 移除主程序
        except:
            self.infos.AppendText(out_infos('项目残缺，无法校验。请检查本项目是否为Django项目。', level=3))
            return

        configs['app_names'] = [_ for _ in apps if os.path.exists(os.path.join(self.dirname, _, 'migrations'))] # 以迁移目录为依据进行筛选
        
        self.path_settings = os.path.join(self.dirname, configs['project_name'], 'settings.py')
        try:
            assert os.path.exists(self.path_settings)
        except Exception as e:
            self.infos.AppendText(out_infos('项目残缺，无法校验。请检查本项目是否为Django项目。', level=3))
            return

        settings = {}
        with open(self.path_settings, 'r', encoding='utf-8') as f:
            text = PATT_BASE_DIR.sub('', f.read())
            exec(f"BASE_DIR = r'{self.dirname}'", {}, settings)
            exec(text, {}, settings)

        configs['DATABASES'] = settings.get('DATABASES') # 数据库
        configs['DEBUG'] = settings.get("DEBUG") # 调试状态
        configs['LANGUAGE_CODE'] = settings.get("LANGUAGE_CODE") # 语言环境
        configs['TIME_ZONE'] = settings.get("TIME_ZONE") # 时区
        configs['USE_I18N'] = settings.get("USE_I18N") # 全局语言设置
        configs['USE_L10N'] = settings.get("USE_L10N")
        configs['USE_TZ'] = settings.get("USE_TZ") # 是否使用标准时区
        configs['STATIC_URL'] = settings.get("STATIC_URL") # 静态文件路径
        configs['ALLOWED_HOSTS'] = settings.get("ALLOWED_HOSTS") # 允许连接ip
        configs['X_FRAME_OPTIONS'] = settings.get("X_FRAME_OPTIONS") # 是否开启iframe
        configs['SECRET_KEY'] = settings.get("SECRET_KEY") # SECRET_KEY
        configs['CORS_ORIGIN_ALLOW_ALL'] = settings.get("CORS_ORIGIN_ALLOW_ALL") # 跨域
        temp_templates_app = settings.get("TEMPLATES")
        if temp_templates_app and len(temp_templates_app) > 0:
            try:
                configs['TEMPLATES_APP_DIRS'] = temp_templates_app[0]['APP_DIRS'] # 是否开启应用程序模板文件路径
                configs['TEMPLATES_DIRS'] = temp_templates_app[0]['DIRS'] # 默认模板路径
            except:
                configs['TEMPLATES_APP_DIRS'] = None
                configs['TEMPLATES_DIRS'] = None # 默认模板路径
        else:
            configs['TEMPLATES_APP_DIRS'] = None
            configs['TEMPLATES_DIRS'] = None # 默认模板路径

        
        dump_json(CONFIG_PATH, configs)  # 写入配置文件

    def onSelectProjectRoot(self):
        """选择项目根路径【项目入口】"""
        dlg = wx.FileDialog(self, "选择Django项目的manage.py文件", r'', "", "*.py", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self._disable_all_btn() # 初始化按钮状态
            filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            if 'manage.py' == filename:
                self.path.SetValue(f'当前项目路径：{self.dirname}')
                try:
                    self._init_config() # 初始化配置文件
                except Exception as e:
                    self.infos.AppendText(out_infos('配置文件config.json初始化失败！', level=3))
                else:
                    # 开放所有的检测按钮
                    self._open_all_check_btn()
                    # 开放部分必要按钮
                    self._open_part_necessary_btns()
                    self.infos.Clear()
                    # self.path.Clear()
                    self.infos.AppendText(out_infos(f'项目{os.path.basename(self.dirname)}导入成功！', level=1))
            else:
                self.infos.AppendText(out_infos('项目导入失败，请选择Django项目根路径下的manage.py文件。', level=3))
        else:
            # self.infos.AppendText(out_infos('您已取消选择。', level=2))
            pass
        dlg.Close(True)

    def onAppsCheck(self, e):
        """应用程序 检测"""
        apps = get_configs(CONFIG_PATH)['app_names']
        settings = {}
        flag = 0
        with open(self.path_settings, 'r', encoding='utf-8') as f:
            text = f.read().replace('__file__', '"."')
            exec(text, {}, settings)
        for app in apps:
            if app not in settings['INSTALLED_APPS']:
                self.unapps.add(app)
                self.infos.AppendText(out_infos(f'{app}应用程序未注册！', 2))
                flag = 1
        if 1 == flag:
            self._open_checked_fix_btn('apps')
        else:
            self._open_checked_fix_btn('apps', f_type='close')
            self.infos.AppendText(out_infos('应用程序检测完成，无已知错误。', level=1))

    def onCheckGlobalProject(self, e):
        """检测项目【全局】"""
        self.onAppsCheck(e)  # 校验 APP
        self.onUrlsCheck(e) # 校验 路由

    def onAppsFix(self, e):
        """修复未注册应用"""
        try:
            content = read_file(self.path_settings)
            temp = PATT_INSTALLED_APPS.search(content).group(0)
            INSTALLED_APPS = temp.split('\n')
            for _ in self.unapps:
                INSTALLED_APPS.insert(-1, f"    '{_}',")
                self.infos.AppendText(out_infos(f'{_}注册完成。', level=1))
            self.unapps.clear()  # 清空未注册应用程序
        except:
            self.infos.AppendText(
                out_infos('项目残缺，无法修复。请检查本项目是否为Django项目。', level=3))
        else:
            new_content = content.replace(temp, '\n'.join(INSTALLED_APPS))
            write_file(self.path_settings, new_content)
            self.infos.AppendText(out_infos('应用程序修复完成。', level=1))
            if 'apps' in self.needfix:
                self.needfix.remove('apps')
            self._open_checked_fix_btn('apps', f_type='close') # 必须最后执行（控件的不可用性）

    def onFixGlobalProject(self, e):
        """修复项目 【全局】"""
        self.onAppsFix(e) # 修复 应用程序
        self.onUrlsFix(e) # 修复 路由

    def onAdminGenerateBase(self, e):
        """管理中心 简单配置"""
        dlg = AdminCreateSimpleDialog(self)
        dlg.ShowModal()
        dlg.Close(True)

    def _disable_all_btn(self):
        """关闭所有按钮权限"""
        for a in self.allInitBtns:
            for b in self.allInitBtns[a]:
                for _ in self.allInitBtns[a][b]:
                    _.Enable(False)

    def _open_all_check_btn(self):
        """ 开启所有检测按钮权限 """
        for a in self.allInitBtns:
            for _ in self.allInitBtns[a]["check"]:
                _.Enable(True)

    def _open_checked_fix_btn(self, model, f_type = 'open'):
        """开启通过检测的修复按钮"""
        if 'open' == f_type:
            self.needfix.add(model)
        switch = True if 'open' == f_type else False
        for _ in self.allInitBtns[model][CON_CONTROL_FIX]:
            _.Enable(switch)
        # 开启/关闭全局的修复按钮【一键修复】
        if len(self.needfix) > 0:
            for _ in self.allInitBtns['global'][CON_CONTROL_FIX]:
                _.Enable(True) # 需要修复时开启，否则关闭
        else:
            for _ in self.allInitBtns['global'][CON_CONTROL_FIX]:
                _.Enable(False)

    def _open_part_necessary_btns(self):
        """开启部分必要的、控制流程之外的按钮"""
        for a in self.allInitBtns:
            for _ in self.allInitBtns[a][CON_CONTROL_CREATE]:
                _.Enable(True) # 开启所有的创建按钮
                
        self.modelsProxyGenerate.Enable(False) # 代理模型 功能暂未实现，待实现后去掉此行代码
        self.btn_config_project.Enable(True) # 选项
        self.menusSettings.Enable(True) # Settings

        if self.platform_name.lower() in env.getSupportEnvPlatform(): # 平台限制
            self.portProgressRun.Enable(True) # 运行

    def __del__(self):
        """释放资源"""
        try:
            env.killProgress()
        except: ...