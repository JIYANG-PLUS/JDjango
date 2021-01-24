import wx, time, os
import wx.lib.buttons as buttons
from ..dialogs.dialogOption import *
from ..dialogs.dialogDocument import *
from ..dialogs.dialogTips import *
from ..miniCmd.djangoCmd import startapp, judge_in_main_urls, fix_urls
from ..miniCmd.miniCmd import CmdTools
from ..tools._tools import *
from ..tools._re import *
from ..tools import environment as env
from ..settings import BASE_DIR, CONFIG_PATH
from ..constant import *

cmd = CmdTools() # 命令行对象
# 所有的功能按钮
classifies = ['global', 'apps', 'views', 'urls', 'templates', 'forms', 'models', 'database', 'admin']

class Main(wx.Frame):

    def __init__(self, parent = None):

        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = CON_JDJANGO_TITLE, pos = wx.DefaultPosition, size = wx.Size(960, 540), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
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
        menusCreate = wx.Menu()
        self.create_project = menusCreate.Append(wx.ID_ANY, "&项目", "项目")
        menusCreate.AppendSeparator()
        self.menuGenerate = menusCreate.Append(wx.ID_ANY, "&应用程序", "应用程序")
        menusCreate.AppendSeparator()
        self.modelsGenerate = menusCreate.Append(wx.ID_ANY, "&模型", "模型")
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
        helpsDocumentation = helps.Append(wx.ID_ANY, "&参考文档", "参考文档")
        helps.AppendSeparator()
        self.helpsSeeOrKill = helps.Append(wx.ID_ANY, "&查看/终止进程", "查看/终止进程")
        helps.AppendSeparator()
        menuAbout = helps.Append(wx.ID_ANY, "&关于", "关于")

        # 运行端口与进程
        portProgress = wx.Menu()
        virtualenv = wx.Menu()
        self.portProgressVirtualInstall = virtualenv.Append(wx.ID_ANY, "&安装", "安装")
        virtualenv.AppendSeparator()
        self.portProgressVirtualChoice = virtualenv.Append(wx.ID_ANY, "&绑定", "绑定")
        virtualenv.AppendSeparator()
        self.portProgressVirtual = virtualenv.Append(wx.ID_ANY, "&创建", "创建")
        portProgress.Append(wx.ID_ANY, "&虚拟环境", virtualenv)
        portProgress.AppendSeparator()
        self.portProgressRun = portProgress.Append(wx.ID_ANY, "&运行", "运行")
        portProgress.AppendSeparator()
        self.portProgressStop = portProgress.Append(wx.ID_ANY, "&停止", "停止")
        self.portProgressRun.Enable(False)
        self.portProgressStop.Enable(False)
        self.portProgressVirtualInstall.Enable(False)
        self.portProgressVirtual.Enable(False)
        
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
        self.models_fix = perFix.Append(wx.ID_ANY, "&修复", "修复")
        self.database_fix = perFix.Append(wx.ID_ANY, "&数据库", "数据库")


        # 应用程序
        self.allInitBtns['apps'][CON_CONTROL_CREATE].append(self.menuGenerate)
        self.allInitBtns['apps'][CON_CONTROL_CHECK].append(self.apps_check)
        self.allInitBtns['apps'][CON_CONTROL_FIX].append(self.apps_fix)

        # 视图
        self.allInitBtns['views'][CON_CONTROL_CREATE].extend([
            self.viewsGenerateFunc
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
        self.allInitBtns['models'][CON_CONTROL_CREATE].append(self.modelsGenerate)
        self.allInitBtns['models'][CON_CONTROL_CHECK].append(self.models_check)
        self.allInitBtns['models'][CON_CONTROL_FIX].append(self.models_fix)

        # 数据库
        # self.databaseGenerate = database.Append(wx.ID_ANY, "&创建", "创建")
        # self.allInitBtns['database'][CON_CONTROL_CREATE].append(self.databaseGenerate)
        self.allInitBtns['database'][CON_CONTROL_CHECK].append(self.database_check)
        self.allInitBtns['database'][CON_CONTROL_FIX].append(self.database_fix)

        # 管理中心 菜单项
        admin = wx.Menu()
        self.adminGenerateBase = admin.Append(wx.ID_ANY, "&创建", "创建")
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
        menuBar.Append(portProgress, "运行")
        menuBar.Append(helps, "&帮助")
        menuBar.Append(directExit, "&退出")
        self.SetMenuBar(menuBar)

        # 子菜单绑定事件
        self.Bind(wx.EVT_MENU, self.onAbout, menuAbout)  # 关于菜单项点击事件
        self.Bind(wx.EVT_MENU, self.onHelpsDocumentation, helpsDocumentation)  # 帮助文档
        self.Bind(wx.EVT_MENU, self.onOpen, menuOpen)  # 文件打开点击事件
        self.Bind(wx.EVT_MENU, self.onGenerate, self.menuGenerate)  # 代码生成点击事件
        self.Bind(wx.EVT_MENU, self.onMenusSettings, self.menusSettings)  # Settings

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

        # 路由 事件绑定
        self.Bind(wx.EVT_MENU, self.onUrlsCheck, self.urls_check) # 检查路由
        self.Bind(wx.EVT_MENU, self.onUrlsFix, self.urls_fix) # 修复路由

        # 新项目 事件绑定
        self.Bind(wx.EVT_MENU, self.onCreateProject, self.create_project) # 新建项目

        # 运行 事件绑定
        self.Bind(wx.EVT_MENU, self.onPortProgressRun, self.portProgressRun) # 运行
        self.Bind(wx.EVT_MENU, self.onPortProgressStop, self.portProgressStop)
        self.Bind(wx.EVT_MENU, self.onPortProgressVirtualChoice, self.portProgressVirtualChoice) 
        self.Bind(wx.EVT_MENU, self.onHelpSeeOrKill, self.helpsSeeOrKill) 

        # 退出 事件绑定
        self.Bind(wx.EVT_MENU, self.onExit, self.btnDirectExit)

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
        dlg.Destroy()
    
    def onHelpSeeOrKill(self, e):
        """查看或终止进程"""
        TipsMessageOKBox(self, CON_MSG_PROGRESS_USE, CON_TIPS_COMMON)

    def onPortProgressRun(self, e):
        """子进程运行Django"""
        # 运行前必要检查
        # 检查一：虚拟环境是否正确配置
        env_path = env.getPython3Env()
        if '' == env_path.strip() or not os.path.exists(env_path):
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
            self.infos.AppendText(out_infos(f"网站正在运行，根路由：http://127.0.0.1:{port}。（以实际为准）", level=1))
            self.portProgressRun.Enable(False)
            self.portProgressStop.Enable(True)

    def onModelsGenerate(self, e):
        """创建模型"""
        dlg = ModelsCreateDialog(self)
        dlg.ShowModal()
        dlg.Destroy()

    def onSqliteManageTool(self, e):
        """跨平台的Sqlite工具"""
        dlg = wx.MessageDialog(self, "请双击同级目录下的sqlite3Manager.pyw启动文件。", CON_TIPS_COMMON, wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def onMenusSettings(self, e):
        """Settings"""
        dlg = SettingsDialog(self)
        dlg.ShowModal()
        dlg.Destroy()

    def onHelpsDocumentation(self, e):
        """帮助文档"""
        dlg = DocumentationDialog(self)
        dlg.ShowModal()
        dlg.Destroy()

    def onCreateProject(self, e):
        """新建项目"""
        dlg = ProjectCreateDialog(self)
        dlg.ShowModal()
        dlg.Destroy()

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
        dlg.Destroy()

    def onViewsGenerateFunc(self, e):
        """多样式新增视图"""
        dlg = ViewGenerateDialog(self)
        dlg.ShowModal()
        dlg.Destroy()

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
        dlg.Destroy()

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
                dlg_tip.Destroy()
                self.onAppsFix(e) # 自动完成注册
                self.onUrlsFix(e) # 自动完成路由注册
                self._init_config() # 重新初始化 配置文件【此操作为敏感操作】
            else:
                dlg_tip = wx.MessageDialog(None, f"{message}应用程序名已存在，或不符合纯字母+数字命名的约定！", CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
                if dlg_tip.ShowModal() == wx.ID_OK: pass
                dlg_tip.Destroy()
        dlg.Destroy()

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
            dlg.Destroy()
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
        dlg.Destroy()

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
        dlg.Destroy()

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
        dlg.Destroy()

    def _disable_all_btn(self):
        """关闭所有按钮权限"""
        for a in self.allInitBtns:
            for b in self.allInitBtns[a]:
                for _ in self.allInitBtns[a][b]:
                    _.Enable(False)
        # 如果当前环境安装了virtualenv包，则关闭虚拟环境的安装按钮
        # 待考虑功能

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
        # # 开启/关闭全局的修复按钮
        if len(self.needfix) > 0:
            for _ in self.allInitBtns['global'][CON_CONTROL_FIX]:
                _.Enable(True)
        else:
            for _ in self.allInitBtns['global'][CON_CONTROL_FIX]:
                _.Enable(False)

    def _open_part_necessary_btns(self):
        """开启部分必要的、控制流程之外的按钮"""
        for a in self.allInitBtns:
            for _ in self.allInitBtns[a][CON_CONTROL_CREATE]:
                _.Enable(True) # 开启所有的创建按钮
        self.btn_config_project.Enable(True) # 选项
        self.menusSettings.Enable(True) # Settings

        if self.platform_name.lower() in env.getSupportEnvPlatform(): # 平台限制
            self.portProgressRun.Enable(True) # 运行

    def __del__(self):
        """释放资源"""
        try:
            env.killProgress()
        except: ...