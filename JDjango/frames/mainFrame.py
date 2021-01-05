import wx, time, os, json, datetime
import wx.lib.buttons as buttons
from ..dialogs.dialogOption import *
from ..miniCmd.djangoCmd import startapp
from ..miniCmd.miniCmd import CmdTools
from ..tools._tools import *
from ..tools import environment as env
from ..settings import BASE_DIR, CONFIG_PATH

cmd = CmdTools()

ID_EXIT = 200
ID_ABOUT = 201
ID_FILE = 202
ID_FLODER = 202

class Main(wx.Frame):

    def __init__(self, parent=None, id=-1, pos=wx.DefaultPosition, title='《Django辅助工具》-V1.1.0'):
        size = (960, 540)

        wx.Frame.__init__(self, parent, id, title, pos, size)

        # 所有的运行时按钮
        classifies = ['global', 'apps', 'views', 'urls', 'templates', 'forms', 'models', 'database', 'admin']
        self.allInitBtns = {}
        for _ in classifies:
            self.allInitBtns[_] = {
                'check' : []
                , 'fix' : []
                , 'create' : []
                , 'other' : []
            }
        self.needFonts = [] # 待设置字体的控件

        self.InitUI()  # 初始化布局
        self.InitMenu()  # 工具栏
        self.setupStatusBar()  # 底部状态栏

        self._close_all() # 统一设置按钮不可用状态
        self._set_fonts(None)# 统一设置字体大小

        # 独立于初始化之外的其它变量
        self.unapps = []  # 未注册的应用程序

    def InitUI(self):
        """面板布局"""
        panel = wx.Panel(self)  # 最外层容器
        midPan = wx.Panel(panel)  # 向panel容器添加子容器midpan
        toolPanel = wx.Panel(midPan)
        toolLeftPanel = wx.Panel(toolPanel)
        toolRightPanel = wx.Panel(toolPanel)
        panel.SetBackgroundColour('#4f5049')  # 最外层容器颜色
        midPan.SetBackgroundColour('#ededed')  # 设置子容器颜色

        """按钮控件"""
        self.btn_select_project = buttons.GenButton(toolLeftPanel, -1, label='选择Django项目')
        self.btn_clear_text = buttons.GenButton(toolLeftPanel, -1, label='清空')
        self.btn_check_project = buttons.GenButton(toolLeftPanel, -1, label='[一键]校验')
        self.btn_fixed_project = buttons.GenButton(toolLeftPanel, -1, label='[一键]修复')
        self.btn_config_project = buttons.GenButton(toolLeftPanel, -1, label='选项/修改')
        
        self.allInitBtns['global']['check'].append(self.btn_check_project)
        self.allInitBtns['global']['fix'].append(self.btn_fixed_project)
        self.allInitBtns['global']['other'].append(self.btn_config_project)

        """文本框控件"""
        self.infos = wx.TextCtrl(midPan, -1, style=wx.TE_MULTILINE)  # 消息框
        self.path = wx.TextCtrl(midPan, -1)  # 项目选择成功提示框
        self.infos.SetEditable(False)
        self.path.SetEditable(False)
        self.needFonts.extend([
            self.infos
        ])

        """命令控件"""
        cmdTip = wx.StaticText(toolRightPanel, -1, "命令：")
        self.cmdInput = wx.TextCtrl(toolRightPanel, -1, size=(200, -1))  # 输入命令
        self.btn_exec = buttons.GenButton(toolRightPanel, -1, '执行/Enter')
        self.needFonts.extend([
            self.cmdInput
        ])
        cmdTip.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False))

        """水平、垂直布局"""
        vbox = wx.BoxSizer(wx.VERTICAL)
        midbox = wx.BoxSizer(wx.VERTICAL)  # midpan的垂直布局
        toolsBox = wx.BoxSizer(wx.HORIZONTAL)
        toolLeftBox = wx.BoxSizer(wx.HORIZONTAL)
        toolRightBox = wx.BoxSizer(wx.HORIZONTAL)

        # 监听键盘按下事件
        self.cmdInput.Bind(wx.EVT_KEY_UP, self.OnKeyDown)

        # 左侧工具填充
        toolLeftBox.Add(self.btn_select_project, 0, wx.EXPAND | wx.ALL, 2)
        toolLeftBox.Add(self.btn_check_project, 0, wx.EXPAND | wx.ALL, 2)
        toolLeftBox.Add(self.btn_fixed_project, 0, wx.EXPAND | wx.ALL, 2)
        toolLeftBox.Add(self.btn_config_project, 0, wx.EXPAND | wx.ALL, 2)
        toolLeftBox.Add(self.btn_clear_text, 0, wx.EXPAND | wx.ALL, 2)

        # 右侧工具栏填充
        toolRightBox.Add(cmdTip, 0, wx.EXPAND | wx.ALL, 2)
        toolRightBox.Add(self.cmdInput, 0, wx.EXPAND | wx.ALL, 2)
        toolRightBox.Add(self.btn_exec, 0, wx.EXPAND | wx.ALL, 2)

        # 工具栏填充
        toolsBox.Add(toolLeftPanel, 1, wx.EXPAND | wx.ALL, 2)
        toolsBox.Add(toolRightPanel, 0, wx.EXPAND | wx.ALL, 2)

        # 次容器填充
        midbox.Add(toolPanel, 0, wx.EXPAND | wx.ALL, 5)
        midbox.Add(self.path, 0, wx.EXPAND | wx.ALL, 5)
        midbox.Add(self.infos, 1, wx.EXPAND | wx.ALL, 5)  # 1 控制比例

        # 大容器填充
        vbox.Add(midPan, 1, wx.EXPAND | wx.ALL, 3)

        # 面板绑定布局
        toolLeftPanel.SetSizer(toolLeftBox)
        toolRightPanel.SetSizer(toolRightBox)
        toolPanel.SetSizer(toolsBox)
        midPan.SetSizer(midbox)
        panel.SetSizer(vbox)

        # 事件绑定
        self.Bind(wx.EVT_BUTTON, self.ButtonClick, self.btn_select_project)
        self.Bind(wx.EVT_BUTTON, self.ButtonClick, self.btn_check_project)
        self.Bind(wx.EVT_BUTTON, self.ButtonClick, self.btn_fixed_project)
        self.Bind(wx.EVT_BUTTON, self.ButtonClick, self.btn_config_project)
        self.Bind(wx.EVT_BUTTON, self.ButtonClick, self.btn_exec)
        self.Bind(wx.EVT_BUTTON, self.ButtonClick, self.btn_clear_text)

    def InitMenu(self):
        """设置工具栏"""
        # 创建文件菜单项
        menus = wx.Menu()
        menuOpen = menus.Append(wx.ID_OPEN, "&选择文件", "选择文件")
        # menuFloder = menus.Append(wx.ID_ANY, "&选择Django项目根目录", "选择Django项目根目录")
        # menus.AppendSeparator()
        # menuAccent = menus.Append(wx.ID_ANY, "&最近打开", "最近打开")
        # menus.AppendSeparator()
        # menuSave = menus.Append(wx.ID_ANY, "&另存为", "另存为")
        menus.AppendSeparator()
        menuClear = menus.Append(wx.ID_ANY, "&清空", "清空")
        menus.AppendSeparator()
        menuExit = menus.Append(wx.ID_ANY, "&退出", "退出")

        # # 创建编辑菜单项
        # edits = wx.Menu()
        # menuCopy = edits.Append(wx.ID_ANY, "&复制", "复制")
        # menuCut = edits.Append(wx.ID_ANY, "&剪切", "剪切")
        # menuPaste = edits.Append(wx.ID_ANY, "&粘贴", "粘贴")
        # edits.AppendSeparator()
        # menuback = edits.Append(wx.ID_ANY, "&撤回", "撤回")
        # menuAfter = edits.Append(wx.ID_ANY, "&逆向撤回", "逆向撤回")

        # 帮助 菜单项
        helps = wx.Menu()
        menuAbout = helps.Append(wx.ID_ANY, "&关于", "关于")

        # 应用程序 菜单项
        apps = wx.Menu()
        self.menuGenerate = apps.Append(wx.ID_ANY, "&生成", "生成")
        apps.AppendSeparator()
        self.apps_check = apps.Append(wx.ID_ANY, "&校验", "校验")
        self.apps_fix = apps.Append(wx.ID_ANY, "&修复", "修复")

        self.allInitBtns['apps']['create'].append(self.menuGenerate)
        self.allInitBtns['apps']['check'].append(self.apps_check)
        self.allInitBtns['apps']['fix'].append(self.apps_fix)

        # 视图 菜单项
        views = wx.Menu()
        self.viewsGenerate = wx.Menu()
        self.viewsGenerateFunc = self.viewsGenerate.Append(wx.ID_ANY, "&视图", "视图")
        views.Append(wx.ID_ANY, "&创建", self.viewsGenerate) # 创建二级菜单项
        views.AppendSeparator()
        self.views_check = views.Append(wx.ID_ANY, "&校验", "校验")
        self.views_fix = views.Append(wx.ID_ANY, "&修复", "修复")

        self.allInitBtns['views']['create'].extend([
            self.viewsGenerateFunc
        ])
        self.allInitBtns['views']['check'].append(self.views_check)
        self.allInitBtns['views']['fix'].append(self.views_fix)

        # 路由 菜单项
        urls = wx.Menu()
        # self.urlsGenerate = urls.Append(wx.ID_ANY, "&创建", "创建")
        # urls.AppendSeparator()
        self.urls_check = urls.Append(wx.ID_ANY, "&校验", "校验")
        self.urls_fix = urls.Append(wx.ID_ANY, "&修复", "修复")

        # self.allInitBtns['urls']['create'].append(self.urlsGenerate)
        self.allInitBtns['urls']['check'].append(self.urls_check)
        self.allInitBtns['urls']['fix'].append(self.urls_fix)

        # 模板 菜单项
        templates = wx.Menu()
        self.templatesGenerate = templates.Append(wx.ID_ANY, "&创建", "创建")
        templates.AppendSeparator()
        self.templates_check = templates.Append(wx.ID_ANY, "&校验", "校验")
        self.templates_fix = templates.Append(wx.ID_ANY, "&修复", "修复")

        self.allInitBtns['templates']['create'].append(self.templatesGenerate)
        self.allInitBtns['templates']['check'].append(self.templates_check)
        self.allInitBtns['templates']['fix'].append(self.templates_fix)

        # 表单 菜单项
        forms = wx.Menu()
        self.formsGenerate = forms.Append(wx.ID_ANY, "&创建", "创建")
        forms.AppendSeparator()
        self.forms_check = forms.Append(wx.ID_ANY, "&校验", "校验")
        self.forms_fix = forms.Append(wx.ID_ANY, "&修复", "修复")

        self.allInitBtns['forms']['create'].append(self.formsGenerate)
        self.allInitBtns['forms']['check'].append(self.forms_check)
        self.allInitBtns['forms']['fix'].append(self.forms_fix)

        # 模型 菜单项
        models = wx.Menu()
        self.modelsGenerate = models.Append(wx.ID_ANY, "&创建", "创建")
        models.AppendSeparator()
        self.models_check = models.Append(wx.ID_ANY, "&校验", "校验")
        self.models_fix = models.Append(wx.ID_ANY, "&修复", "修复")

        self.allInitBtns['models']['create'].append(self.modelsGenerate)
        self.allInitBtns['models']['check'].append(self.models_check)
        self.allInitBtns['models']['fix'].append(self.models_fix)

        # 数据库
        database = wx.Menu()
        self.databaseGenerate = database.Append(wx.ID_ANY, "&创建", "创建")
        database.AppendSeparator()
        self.database_check = database.Append(wx.ID_ANY, "&校验", "校验")
        self.database_fix = database.Append(wx.ID_ANY, "&修复", "修复")

        self.allInitBtns['database']['create'].append(self.databaseGenerate)
        self.allInitBtns['database']['check'].append(self.database_check)
        self.allInitBtns['database']['fix'].append(self.database_fix)

        # 管理中心 菜单项
        admin = wx.Menu()
        self.adminGenerateBase = admin.Append(wx.ID_ANY, "&创建简单管理中心", "创建简单管理中心")
        # self.adminGenerateComplex = admin.Append(wx.ID_ANY, "&创建复杂管理中心", "创建复杂管理中心")
        # admin.AppendSeparator()
        # self.admin_check = admin.Append(wx.ID_ANY, "&校验", "校验")
        # self.admin_fix = admin.Append(wx.ID_ANY, "&修复", "修复")
        admin.AppendSeparator()
        self.adminRename = admin.Append(wx.ID_ANY, "&修改后台网站名", "修改后台网站名")
        # admin.AppendSeparator()
        # self.quickAdminGenerateBase = admin.Append(wx.ID_ANY, "&一键创建简单管理中心", "一键创建简单管理中心")
        # self.quickAdminGenerateComplex = admin.Append(wx.ID_ANY, "&一键创建复杂管理中心", "一键创建复杂管理中心")

        self.allInitBtns['admin']['create'].extend([
            self.adminGenerateBase
            # , self.adminGenerateComplex
            , self.adminRename
            # , self.quickAdminGenerateBase
            # , self.quickAdminGenerateComplex
        ])
        # self.allInitBtns['admin']['check'].append(self.admin_check)
        # self.allInitBtns['admin']['fix'].append(self.admin_fix)

        # 测试 菜单项
        test = wx.Menu()

        # 新项目
        new_project = wx.Menu()
        self.create_project = new_project.Append(wx.ID_ANY, "&新建项目", "新建项目")
        self.create_project.Enable(True)

        # 设置
        settings = wx.Menu()
        fonts = wx.Menu()
        self.fonts_minus = fonts.Append(wx.ID_ANY, "&字体减小-1", "字体减小-1")
        self.fonts_add = fonts.Append(wx.ID_ANY, "&字体增大+1", "字体增大+1")
        settings.Append(wx.ID_ANY, "&字体", fonts)
        settings.AppendSeparator()
        self.language = settings.Append(wx.ID_ANY, "&语言和时区", "语言和时区")

        menuBar = wx.MenuBar()  # 创建顶部菜单条
        menuBar.Append(menus, "&文件")  # 将菜单添加进菜单条中（无法两次加入同一个菜单对象）
        menuBar.Append(new_project, "&新项目")
        menuBar.Append(admin, "&后台管理中心")
        # menuBar.Append(edits, "&编辑")
        menuBar.Append(apps, "&应用程序")
        menuBar.Append(views, "&视图")
        menuBar.Append(urls, "&路由")
        menuBar.Append(templates, "&模板")
        menuBar.Append(forms, "&表单")
        menuBar.Append(models, "&模型")
        menuBar.Append(database, "&数据库")
        menuBar.Append(test, "&测试")
        menuBar.Append(settings, "&设置")
        menuBar.Append(helps, "&帮助")
        self.SetMenuBar(menuBar)

        # 子菜单绑定事件
        self.Bind(wx.EVT_MENU, self.onAbout, menuAbout)  # 关于菜单项点击事件
        self.Bind(wx.EVT_MENU, self.onExit, menuExit)  # 退出菜单项点击事件
        self.Bind(wx.EVT_MENU, self.onOpen, menuOpen)  # 文件打开点击事件
        self.Bind(wx.EVT_MENU, self.onGenerate, self.menuGenerate)  # 代码生成点击事件
        self.Bind(wx.EVT_MENU, self.onClear, menuClear)  # 清空

        # 应用程序  事件绑定
        self.Bind(wx.EVT_MENU, self.onAppsCheck, self.apps_check) # 检测
        self.Bind(wx.EVT_MENU, self.onAppsFix, self.apps_fix) # 修复

        # 管理中心 事件绑定
        self.Bind(wx.EVT_MENU, self.onAdminGenerateBase, self.adminGenerateBase) # 创建简单管理中心
        self.Bind(wx.EVT_MENU, self.onAdminRename, self.adminRename) # 修改后台网站名

        # 设置 事件绑定
        self.Bind(wx.EVT_MENU, self.onFontsMinus, self.fonts_minus) # 字体减小
        self.Bind(wx.EVT_MENU, self.onFontsAdd, self.fonts_add) # 字体减小

        # 视图 事件绑定
        self.Bind(wx.EVT_MENU, self.onViewsGenerateFunc, self.viewsGenerateFunc) # 新增视图（多样新增）

        # 路由 事件绑定
        self.Bind(wx.EVT_MENU, self.onUrlsCheck, self.urls_check) # 检查路由
        self.Bind(wx.EVT_MENU, self.onUrlsFix, self.urls_fix) # 修复路由

        # 新项目 事件绑定
        self.Bind(wx.EVT_MENU, self.onCreateProject, self.create_project) # 新建项目

    def onCreateProject(self):
        """新建项目"""
        # 通过模板建

    def onUrlsFix(self):
        pass

    def onUrlsCheck(self, e):
        """检查路由"""
        # 检查情形有：
        # 只针对以本工具生成的app，而不是Django原生命令python manage.py startapp ...
        # 路由必须在主路径urls.py中用include()函数注册
        # 默认未每个应用程序注册ulrs，取environment.py中的urls别名

        config = get_configs(CONFIG_PATH)
        apps = config['app_names'] # 取所有的app名称
        root_path = config['dirname'] # Django项目根路径
        project_name = config['project_name'] # 项目名称
        # 取所有的urls别名，（带后缀名）
        alias = [os.path.basename(_) for _ in env.getUrlsAlias()] # 仅取文件名
        root_urlspy = os.path.join(root_path, project_name, 'urls.py') # 定位项目的主urls.py文件
        urlpatterns_content = get_urlpatterns_content(root_urlspy)
        
        for app in apps:
            pass
        

    def onAdminRename(self, e):
        """重命名后台名称"""
        dlg = AdminRenameDialog(self, -1)
        dlg.ShowModal()
        dlg.Destroy()

    def onViewsGenerateFunc(self, e):
        """多样式新增视图"""
        dlg = ViewGenerateDialog(self, -1)
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
            self.exec_command()

    def setupStatusBar(self):
        """设置状态栏"""
        # 状态栏
        sb = self.CreateStatusBar(2)  # 2代表将状态栏分为两个
        self.SetStatusWidths([-1, -2])  # 比例为1：2
        self.SetStatusText("Ready", 0)  # 0代表第一个栏，Ready为内容

        # 循环定时器
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(1000, wx.TIMER_CONTINUOUS)
        self.Notify()

    def Notify(self):
        """底部信息栏"""
        t = time.localtime(time.time())
        st = time.strftime('%Y-%m-%d %H:%M:%S', t)
        self.SetStatusText(f'系统时间：{st}', 1)  # 这里的1代表将时间放入状态栏的第二部分上

    def onAbout(self, e):
        """关于"""
        dlg = wx.MessageDialog(self, "关于软件：目前为个人使用版。【部分功能正在实现】", "提示信息", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        # 截止事件的发生
        # event.Skip()

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
                self.unapps.append(message)
                self.infos.AppendText(out_infos(f"{message}应用程序创建成功！", level=1))
                dlg_tip = wx.MessageDialog(None, f"{message}创建成功！", u"成功", wx.OK | wx.ICON_INFORMATION)
                if dlg_tip.ShowModal() == wx.ID_OK: pass
                dlg_tip.Destroy()
                self.onAppsFix(e) # 自动完成注册
                self._init_config() # 重新初始化 配置文件【此操作为敏感操作】
            else:
                dlg_tip = wx.MessageDialog(None, f"{message}应用程序名已存在，或不符合纯字母+数字命名的约定！", u"失败", wx.OK | wx.ICON_INFORMATION)
                if dlg_tip.ShowModal() == wx.ID_OK: pass
                dlg_tip.Destroy()
        dlg.Destroy()

    def ButtonClick(self, e):
        """界面按钮点击事件"""
        bId = e.GetId()
        if bId == self.btn_select_project.GetId(): # 选择项目根路径
            self.select_root()
        elif bId == self.btn_check_project.GetId(): # 检测/校验项目
            self.check_project_global(e)
        elif bId == self.btn_fixed_project.GetId(): # 修复项目
            self.fix_project_global(e)
        elif bId == self.btn_config_project.GetId(): # 项目配置和修改
            dlg = ConfigDialog(self, -1)
            dlg.ShowModal()
            dlg.Destroy()
        elif bId == self.btn_exec.GetId(): # 执行命令
            self.exec_command()
        elif bId == self.btn_clear_text.GetId():
            self.onClear(e)

    def exec_command(self):
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
            text = f.read().replace('__file__', '"."')
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

    def select_root(self):
        """选择项目根路径【项目入口】"""
        self._close_all() # 初始化按钮状态
        dlg = wx.FileDialog(self, "选择Django项目的manage.py文件", r'', "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            if 'manage.py' == filename:
                self.path.SetValue(f'当前项目路径：{self.dirname}')
                self.infos.AppendText(out_infos('项目导入成功！', level=1))
                # 开放所有的检测按钮
                self._open_all_check()
                # 开放部分必要按钮
                self._open_part_btns()
            else:
                self.infos.AppendText(out_infos('项目导入失败，请选择Django项目根路径下的manage.py文件。', level=3))
        else:
            # self.infos.AppendText(out_infos('您已取消选择。', level=2))
            pass
        dlg.Destroy()
        self._init_config() # 初始化配置文件

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
                self.unapps.append(app)
                self.infos.AppendText(
                    out_infos(f'{app}应用程序未注册！', 2))
                flag = 1
        if 1 == flag:
            self._open_point_fix('apps')
        else:
            self._open_point_fix('apps', f_type='close')
            self.infos.AppendText(out_infos('应用程序检测完成，无已知错误。', level=1))

    def check_project_global(self, e):
        """检测项目【全局】"""
        check_result = self.onAppsCheck(e)  # 校验 APP

    def onAppsFix(self, e):
        """修复未注册应用"""
        try:
            import re
            content = read_file(self.path_settings)
            temp = re.search(r"(?ms:INSTALLED_APPS\s.*?=\s.*?\[.*?\])", content).group(0)
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
            self._open_point_fix('apps', f_type='close')

    def fix_project_global(self, e):
        """修复项目 【全局】"""
        self.onAppsFix(e) # 修复 应用程序

    """"""

    def onAdminGenerateBase(self, e):
        """管理中心 简单配置"""
        dlg = AdminCreateSimpleDialog(self, -1)
        dlg.ShowModal()
        dlg.Destroy()

    """"""

    def _close_all(self):
        """关闭所有按钮权限"""
        for a in self.allInitBtns:
            for b in self.allInitBtns[a]:
                for _ in self.allInitBtns[a][b]:
                    _.Enable(False)

    def _open_all_check(self):
        """ 开启所有检测按钮权限 """
        for a in self.allInitBtns:
            for _ in self.allInitBtns[a]["check"]:
                _.Enable(True)

    def _open_point_fix(self, model, f_type = 'open'):
        """开启通过检测的修复按钮"""
        switch = True if 'open' == f_type else False
        for _ in self.allInitBtns[model]['fix']:
            _.Enable(switch)
        # 开启/关闭全局的修复按钮
        for _ in self.allInitBtns['global']['fix']:
            _.Enable(switch)

    def _open_part_btns(self):
        """开启部分必要的、控制流程之外的按钮"""
        for a in self.allInitBtns:
            for _ in self.allInitBtns[a]["create"]:
                _.Enable(True) # 开启所有的创建按钮
        self.btn_config_project.Enable(True)
