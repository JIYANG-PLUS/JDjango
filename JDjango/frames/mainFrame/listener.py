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
        self.Bind(wx.EVT_MENU, self.onAbout, self.menuAbout)  # 关于菜单项点击事件
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
        self.Bind(wx.EVT_TOOL, self.onPortProgressRun, self.shotcut_run)
        self.Bind(wx.EVT_TOOL, self.onPortProgressStop, self.shotcut_stop)
        self.Bind(wx.EVT_TOOL, self.onBtnOpenDocs, self.shotcut_info)

        '''
            其它
        '''
        self.Bind(wx.EVT_MENU, self.onExit, self.btnDirectExit) # 退出


    """基方法注册（一览无余）"""
    def OnTest(self, e): ... # 测试函数，开发用
    def onDrfGenerators(self, e): ... # pip install drf-generators
    def onRegisterkfenvRest(self, e): ... # 注册rest_framework
    def onRegisterkfenvDrf(self, e): ... # 注册drf_generators
    def onRegisterkfenvAll(self, e): ... # 一键全部注册rest_framework、drf_generators
    def onFastSimpleui(self, e): ... # 一键配置 simpleui
    def onInstallSimpleui(self, e): ... # 安装 simpleui
    def onRegisterSimpleui(self, e): ... # 注册 simpleui
    def onDjango_filter(self, e): ... # pip install django-filter
    def onMarkdown(self, e): ... # pip install markdown
    def onDjangorestframework(self, e): ... # pip install djangorestframework
    def onHelpsORM(self, e): ... # ORM帮助（一键生成）
    def onMenuVSCode(self, e): ... # 外部发起VSCode编辑
    def onPortProgressVirtual(self, e): ... # 创建虚拟环境
    def onPortProgressVirtualView(self, e): ... # 查看虚拟环境路径
    def onPortProgressCollectstatic(self, e): ... # python manage.py collectstatic
    def onPortProgressPipFreeze(self, e): ... # 导出包pip freeze
    def onPortProgressPipInstall(self, e): ... # 虚拟环境安装包pip install
    def onPortProgressShell(self, e): ... # python manage.py shell
    def onPortProgressMakemigrations(self, e): ... # python manage.py makemigrations
    def onPortProgressMigrate(self, e): ... # python manage.py migtrate
    def onPortProgressFlush(self, e): ... # python manage.py flush
    def onPortProgressCreatesuperuser(self, e): ... # python manage.py createsuperuser
    def onCreateProject1100(self, e): ... # 创建Django1.10.0项目
    def onPortProgressKillProgress(self, e): ... # 终止进程
    def onPortProgressFaster(self, e): ... # 一键配置镜像环境
    def onModelsProxyGenerate(self, e): ... # 创建代理模型
    def onPortProgressStop(self, e): ... # 关闭
    def onPortProgressVirtualChoice(self, e): ... # 选择虚拟环境
    def onHelpSeeOrKill(self, e): ... # 查看或终止进程
    def onPortProgressRun(self, e): ... # 运行
    def onModelsGenerate(self, e): ... # 创建模型
    def onSqliteManageTool(self, e): ... # 跨平台的Sqlite工具
    def onMenusSettings(self, e): ... # Settings
    def onHelpsDocumentation(self, e): ... # 帮助文档
    def onCreateProject(self, e): ... # 新建项目
    def onUrlsFix(self, e): ... # 修复路由
    def onUrlsCheck(self, e): ... # 检查路由
    def onAdminRename(self, e): ... # 重命名后台名称
    def onViewsGenerateFunc(self, e): ... # 多样式新增视图
    def onFontsMinus(self, e): ... # 显示框字体减小
    def onFontsAdd(self, e): ... # 显示框字体增大
    def OnKeyDown(self, event): ... # 键盘监听
    def onAbout(self, e): ... # 关于
    def onExit(self, e): ... # 退出
    def onOpen(self, e): ... # 查看文件
    def onClear(self, e): ... # 清空提示台
    def onGenerate(self, e): ... # 生成应用程序
    def onButtonClick(self, e): ... # 界面按钮点击事件
    def onBtnOpenDocs(self, e): ... # 查看帮助文档
    def onExecCommand(self): ... # 仿Linux命令
    def onSelectProjectRoot(self): ... # 选择项目根路径【项目入口】
    def onAppsCheck(self, e): ... # 应用程序 检测
    def onCheckGlobalProject(self, e): ... # 检测项目【全局】
    def onAppsFix(self, e): ... # 修复未注册应用
    def onFixGlobalProject(self, e): ... # 修复项目 【全局】
    def onAdminGenerateBase(self, e): ... # 管理中心 简单配置
