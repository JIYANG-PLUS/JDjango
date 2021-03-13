from .control import *

"""
作用：实现事件监听
"""

class MainFrameListener(MainFrameGUIControl):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._register_listener()

    def _register_listener(self):
        """注册监听事件"""

        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)

        '''
            界面按钮监听
        '''
        self.Bind(wx.EVT_BUTTON, self.onButtonClick, self.btn_select_project) # 选择项目
        self.Bind(wx.EVT_BUTTON, self.onButtonClick, self.btn_check_project) # 一键检测项目
        self.Bind(wx.EVT_BUTTON, self.onButtonClick, self.btn_fixed_project) # 一键修复项目
        self.Bind(wx.EVT_BUTTON, self.onButtonClick, self.btn_config_project) # 选项/修改
        self.Bind(wx.EVT_BUTTON, self.onButtonClick, self.btn_exec) # 运行【命令】
        self.Bind(wx.EVT_BUTTON, self.onButtonClick, self.btn_clear_text) # 清空输入窗口

        '''
            鼠标键盘监听
        '''
        self.cmdInput.Bind(wx.EVT_KEY_UP, self.OnKeyDown) # 键盘按键监听

        '''
            菜单事件绑定
        '''
        self.Bind(wx.EVT_MENU, self.onAbout, self.menuAbout)  # 关于
        self.Bind(wx.EVT_MENU, self.onHelpsDocumentation, self.helpsDocumentation)  # 帮助文档
        self.Bind(wx.EVT_MENU, self.onOpen, self.menuOpen)  # 文件打开点击事件
        self.Bind(wx.EVT_MENU, self.onGenerate, self.menuGenerate)  # 代码生成点击事件
        self.Bind(wx.EVT_MENU, self.onMenusSettings, self.menusSettings)  # Settings
        self.Bind(wx.EVT_MENU, self.onMenuVSCode, self.menuVSCode)  # VSCode

        self.Bind(wx.EVT_MENU, self.onAppsCheck, self.apps_check) # 检测
        self.Bind(wx.EVT_MENU, self.onAppsFix, self.apps_fix) # 修复

        self.Bind(wx.EVT_MENU, self.onAdminGenerateBase, self.adminGenerateBase) # 创建简单管理中心
        self.Bind(wx.EVT_MENU, self.onAdminRename, self.adminRename) # 修改后台网站名

        self.Bind(wx.EVT_MENU, self.onFontsMinus, self.fonts_minus) # 字体减小
        self.Bind(wx.EVT_MENU, self.onFontsAdd, self.fonts_add) # 字体减小
        self.Bind(wx.EVT_MENU, self.onSqliteManageTool, self.sqliteManageTool) # SqLite

        self.Bind(wx.EVT_MENU, self.onViewsGenerateFunc, self.viewsGenerateFunc) # 新增视图（多样新增）

        self.Bind(wx.EVT_MENU, self.onModelsGenerate, self.modelsGenerate)
        self.Bind(wx.EVT_MENU, self.onModelsProxyGenerate, self.modelsProxyGenerate)

        self.Bind(wx.EVT_MENU, self.onUrlsCheck, self.urls_check) # 检查路由
        self.Bind(wx.EVT_MENU, self.onUrlsFix, self.urls_fix) # 修复路由

        self.Bind(wx.EVT_MENU, self.onCreateProject, self.create_project) # 新建项目
        self.Bind(wx.EVT_MENU, self.onCreateProject1100, self.create_project_1_10_0) # 新建项目

        self.Bind(wx.EVT_MENU, self.onPortProgressRun, self.portProgressRun) # 运行
        self.Bind(wx.EVT_MENU, self.onPortProgressStop, self.portProgressStop) # 停止
        self.Bind(wx.EVT_MENU, self.onPortProgressVirtual, self.portProgressVirtual) # 创建虚拟环境
        self.Bind(wx.EVT_MENU, self.onPortProgressVirtualChoice, self.portProgressVirtualChoice) # 选择虚拟环境
        self.Bind(wx.EVT_MENU, self.onPortProgressVirtualView, self.portProgressVirtualView) # 查看虚拟环境
        self.Bind(wx.EVT_MENU, self.onHelpSeeOrKill, self.helpsSeeOrKill) # 进程命令查看
        self.Bind(wx.EVT_MENU, self.onHelpsORM, self.helpsORM) # ORM查看器
        self.Bind(wx.EVT_MENU, self.onPortProgressFaster, self.portProgressFaster) # 镜像环境配置
        self.Bind(wx.EVT_MENU, self.onPortProgressKillProgress, self.portProgressKillProgress) # 根据端口终止进程
        self.Bind(wx.EVT_MENU, self.onPortProgressMakemigrations, self.portProgressMakemigrations) # migration
        self.Bind(wx.EVT_MENU, self.onPortProgressShell, self.portProgressShell) # shell
        self.Bind(wx.EVT_MENU, self.onPortProgressMigrate, self.portProgressMigrate) # migrate
        self.Bind(wx.EVT_MENU, self.onPortProgressFlush, self.portProgressFlush) # flush
        self.Bind(wx.EVT_MENU, self.onPortProgressCreatesuperuser, self.portProgressCreatesuperuser) # createsuperuser
        self.Bind(wx.EVT_MENU, self.onPortProgressPipInstall, self.portProgressPipInstall) # install
        self.Bind(wx.EVT_MENU, self.onPortProgressPipFreeze, self.portProgressPipFreeze) # freeze
        self.Bind(wx.EVT_MENU, self.onPortProgressCollectstatic, self.portProgressCollectstatic) # collectstatic
        self.Bind(wx.EVT_MENU, self.onDjangorestframework, self.djangorestframework) # restframework
        self.Bind(wx.EVT_MENU, self.onDrfGenerators, self.drf_generators) # drf_generators
        self.Bind(wx.EVT_MENU, self.onMarkdown, self.markdown) # markdown
        self.Bind(wx.EVT_MENU, self.onDjango_filter, self.django_filter) # django_filter
        # self.Bind(wx.EVT_MENU, self.onInstallSimpleui, self.installSimpleui) # pip install simpleui
        # self.Bind(wx.EVT_MENU, self.onRegisterSimpleui, self.registerSimpleui) # 注册 simpleui
        self.Bind(wx.EVT_MENU, self.onFastSimpleui, self.fastSimpleui) # 一键配置 simpleui
        self.Bind(wx.EVT_MENU, self.onRegisterkfenvRest, self.registerkfenvRest) # 注册rest_framework
        self.Bind(wx.EVT_MENU, self.onRegisterkfenvDrf, self.registerkfenvDrf) # 注册drf_generators
        self.Bind(wx.EVT_MENU, self.onRegisterkfenvAll, self.registerkfenvAll) # 一键全部注册rest_framework、drf_generators

        '''
            系统工具栏
        '''
        # self.Bind(wx.EVT_TOOL, self., self.shotcut_file)
        self.Bind(wx.EVT_TOOL, self.onPortProgressRun, self.shotcut_run)
        self.Bind(wx.EVT_TOOL, self.onPortProgressStop, self.shotcut_stop)
        self.Bind(wx.EVT_TOOL, self.onMenuVSCode, self.shotcut_code)
        self.Bind(wx.EVT_TOOL, self.onAbout, self.shotcut_info)
        self.Bind(wx.EVT_TOOL, self.onPortProgressShell, self.shotcut_command)
        self.Bind(wx.EVT_TOOL, self.onPortProgressMakemigrations, self.shotcut_makemigration)
        self.Bind(wx.EVT_TOOL, self.onPortProgressMigrate, self.shotcut_migrate)
        self.Bind(wx.EVT_TOOL, self.onPortProgressPipInstall, self.shotcut_pipinstall)

        '''
            其它
        '''
        self.Bind(wx.EVT_MENU, self.onExit, self.btnDirectExit) # 退出
