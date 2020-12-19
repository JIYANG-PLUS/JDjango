import wx
import time
import os
import json
import datetime
import wx.lib.buttons as buttons
from ..dialogs.dialogOption import ConfigDialog
from ..miniCmd.djangoCmd import startapp
from ..miniCmd.miniCmd import CmdTools
from ..tools._tools import *
from ..settings import BASE_DIR

cmd = CmdTools()

ID_EXIT = 200
ID_ABOUT = 201
ID_FILE = 202
ID_FLODER = 202


class Main(wx.Frame):

    def __init__(self, parent=None, id=-1, pos=wx.DefaultPosition, title='《Django辅助工具》-V1.0.0'):
        size = (960, 540)

        wx.Frame.__init__(self, parent, id, title, pos, size)

        self.font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False)

        self.InitUI()  # 初始化布局
        self.InitMenu()  # 工具栏
        self.setupStatusBar()  # 底部状态栏

        self.unapps = []  # 未注册的应用程序

    def InitUI(self):
        """面板"""
        panel = wx.Panel(self)  # 最外层容器
        midPan = wx.Panel(panel)  # 向panel容器添加子容器midpan
        toolPanel = wx.Panel(midPan)
        toolLeftPanel = wx.Panel(toolPanel)
        toolRightPanel = wx.Panel(toolPanel)
        panel.SetBackgroundColour('#4f5049')  # 最外层容器颜色
        midPan.SetBackgroundColour('#ededed')  # 设置子容器颜色

        """按钮控件"""
        self.btn_select_project = buttons.GenButton(
            toolLeftPanel, -1, label='选择Django项目')
        self.btn_check_project = buttons.GenButton(
            toolLeftPanel, -1, label='校验/检测')
        self.btn_fixed_project = buttons.GenButton(
            toolLeftPanel, -1, label='自动修复')
        self.btn_config_project = buttons.GenButton(
            toolLeftPanel, -1, label='选项/修改')
        self.btn_check_project.Enable(False)
        self.btn_fixed_project.Enable(False)
        self.btn_config_project.Enable(False)

        """文本框控件"""
        self.infos = wx.TextCtrl(midPan, -1, style=wx.TE_MULTILINE)  # 消息框
        self.path = wx.TextCtrl(midPan, -1)  # 项目选择成功提示框
        self.infos.SetFont(self.font)
        self.infos.SetEditable(False)
        self.path.SetEditable(False)

        """命令控件"""
        cmdTip = wx.StaticText(toolRightPanel, -1, "命令：")
        cmdTip.SetFont(self.font)
        self.cmdInput = wx.TextCtrl(toolRightPanel, -1, size=(200, -1))  # 输入命令
        self.cmdInput.SetFont(self.font)
        self.btn_exec = buttons.GenButton(toolRightPanel, -1, '执行/Enter')

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

    # 设置工具栏
    def InitMenu(self):

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
        self.menuGenerate.Enable(False)

        # 视图 菜单项
        views = wx.Menu()

        # 路由 菜单项
        urls = wx.Menu()

        # 模板 菜单项
        templates = wx.Menu()

        # 表单 菜单项
        forms = wx.Menu()

        # 模型 菜单项
        models = wx.Menu()

        # 测试 菜单项
        test = wx.Menu()

        # 管理中心 菜单项
        admin = wx.Menu()

        menuBar = wx.MenuBar()  # 创建顶部菜单条
        menuBar.Append(menus, "&文件")  # 将菜单添加进菜单条中（无法两次加入同一个菜单对象）
        # menuBar.Append(edits, "&编辑")
        menuBar.Append(apps, "&应用程序")
        menuBar.Append(views, "&视图")
        menuBar.Append(urls, "&路由")
        menuBar.Append(templates, "&模板")
        menuBar.Append(forms, "&表单")
        menuBar.Append(models, "&模型")
        menuBar.Append(test, "&测试")
        menuBar.Append(admin, "&管理中心")
        menuBar.Append(helps, "&帮助")
        self.SetMenuBar(menuBar)

        # 子菜单绑定事件
        self.Bind(wx.EVT_MENU, self.onAbout, menuAbout)  # 关于菜单项点击事件
        self.Bind(wx.EVT_MENU, self.onExit, menuExit)  # 退出菜单项点击事件
        self.Bind(wx.EVT_MENU, self.onOpen, menuOpen)  # 文件打开点击事件
        self.Bind(wx.EVT_MENU, self.onGenerate, self.menuGenerate)  # 代码生成点击事件
        self.Bind(wx.EVT_MENU, self.onClear, menuClear)  # 清空

    # 键盘监听
    def OnKeyDown(self, event):
        code = event.GetKeyCode()
        if wx.WXK_NUMPAD_ENTER == code or 13 == code:
            self.exec_command()

    # 设置状态栏
    def setupStatusBar(self):
        # 状态栏
        sb = self.CreateStatusBar(2)  # 2代表将状态栏分为两个
        self.SetStatusWidths([-1, -2])  # 比例为1：2
        self.SetStatusText("Ready", 0)  # 0代表第一个栏，Ready为内容

        # 循环定时器
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(1000, wx.TIMER_CONTINUOUS)
        self.Notify()

    def Notify(self):
        t = time.localtime(time.time())
        st = time.strftime('%Y-%m-%d %H:%M:%S', t)
        self.SetStatusText(f'系统时间：{st}', 1)  # 这里的1代表将时间放入状态栏的第二部分上

    def onAbout(self, e):
        dlg = wx.MessageDialog(self, "关于软件：目前为个人使用版。【部分功能正在实现】", "提示信息", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        # 截止事件的发生
        # event.Skip()

    def onExit(self, e):
        self.Close(True)

    def onOpen(self, e):
        self.dirname = r''
        dlg = wx.FileDialog(self, "选择一个文件", self.dirname,
                            "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            with open(os.path.join(self.dirname, self.filename), 'r', encoding="utf-8") as f:
                self.infos.SetValue(f.read())
        dlg.Destroy()

    def onClear(self, e):
        self.infos.Clear()

    def onGenerate(self, e):
        dlg = wx.TextEntryDialog(None, u"请输入应用程序名：", u"创建应用程序", u"")
        if dlg.ShowModal() == wx.ID_OK:
            message = dlg.GetValue()  # 获取文本框中输入的值
            returnStatus = startapp(message)
            if 0 == returnStatus:
                self.infos.AppendText(
                    out_infos(f"{message}应用程序创建成功！请重新【校验】后点击【自动修复】按钮，完成应用程序注册。", level=1))
                dlg_tip = wx.MessageDialog(
                    None, f"{message}创建成功！", u"成功", wx.OK | wx.ICON_INFORMATION)
                if dlg_tip.ShowModal() == wx.ID_OK:
                    pass
                dlg_tip.Destroy()
            else:
                self.infos.AppendText(
                    out_infos(f"{message}应用程序名已存在，或不符合纯字母+数字命名的约定！", level=3))
                dlg_tip = wx.MessageDialog(
                    None, f"{message}应用程序名已存在，或不符合纯字母+数字命名的约定！", u"失败", wx.OK | wx.ICON_INFORMATION)
                if dlg_tip.ShowModal() == wx.ID_OK:
                    pass
                dlg_tip.Destroy()
        dlg.Destroy()

    def ButtonClick(self, e):
        bId = e.GetId()
        # 选择项目根路径
        if bId == self.btn_select_project.GetId():
            self.select_root()
        # 检测/校验项目
        elif bId == self.btn_check_project.GetId():
            self.generate_check_project()
        # 修复项目
        elif bId == self.btn_fixed_project.GetId():
            self.fix_project()
        # 项目配置和修改
        elif bId == self.btn_config_project.GetId():
            dlg = ConfigDialog(self, -1)
            dlg.ShowModal()
            dlg.Destroy()
        # 执行命令
        elif bId == self.btn_exec.GetId():
            self.exec_command()

    def exec_command(self):
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

    # 选择项目根路径
    def select_root(self):
        dlg = wx.FileDialog(self, "选择Django项目的manage.py文件",
                            r'', "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            if 'manage.py' == filename:
                self.path.SetValue(f'当前项目路径：{self.dirname}')
                # self.path.AppendText(f'你的项目路径：{self.dirname}')
                self.btn_check_project.Enable(True)
                self.btn_fixed_project.Enable(False)
                self.btn_config_project.Enable(False)
                self.infos.AppendText(out_infos('项目导入成功！', level=1))
                # self.infos.AppendText(out_infos('检测校验功能已开放。'))
            else:
                self.infos.AppendText(
                    out_infos('项目导入失败，请选择Django项目根路径下的manage.py文件。', level=3))
        else:
            self.infos.AppendText(out_infos('您已取消选择。', level=2))
        dlg.Destroy()

    # 修复项目
    def fix_project(self):
        # 获取settings.py所在的路径
        path_settings = os.path.join(
            self.dirname, os.path.basename(self.dirname), 'settings.py')
        try:
            import re
            content = read_file(path_settings)
            temp = re.search(
                r"(?ms:INSTALLED_APPS\s.*?=\s.*?\[.*?\])", content).group(0)
            INSTALLED_APPS = temp.split('\n')
            for _ in self.unapps:
                INSTALLED_APPS.insert(-1, f"    '{_}',")
                self.infos.AppendText(out_infos(f'{_}注册完成。', level=1))
            self.unapps.clear()  # 清空未注册应用程序
        except:
            self.infos.AppendText(
                out_infos('项目残缺，无法校验。请检查本项目是否为Django项目。', level=3))
        else:
            new_content = content.replace(temp, '\n'.join(INSTALLED_APPS))
            write_file(path_settings, new_content)
            self.infos.AppendText(out_infos('修复完成。', level=1))

    # 检测项目
    def generate_check_project(self):
        self.infos.AppendText(out_infos('正在整合和校验项目......'))
        configs = {}
        configs['dirname'] = self.dirname
        configs['project_name'] = os.path.basename(self.dirname)
        apps = os.listdir(self.dirname)
        try:
            apps.remove(configs['project_name'])
        except:
            self.menuGenerate.Enable(False)
            self.infos.AppendText(
                out_infos('项目残缺，无法校验。请检查本项目是否为Django项目。', level=3))
            return
        configs['app_names'] = [_ for _ in apps if os.path.exists(
            os.path.join(self.dirname, _, 'migrations'))]
        path_settings = os.path.join(
            self.dirname, configs['project_name'], 'settings.py')
        try:
            assert os.path.exists(path_settings)
        except Exception as e:
            self.menuGenerate.Enable(False)
            self.infos.AppendText(
                out_infos('项目残缺，无法校验。请检查本项目是否为Django项目。', level=3))
            return

        configs['DATABASES'] = []
        configs['DEBUG'] = True
        configs['LANGUAGE_CODE'] = ''
        configs['TIME_ZONE'] = ''
        configs['USE_I18N'] = True
        configs['USE_L10N'] = True
        configs['USE_TZ'] = False
        configs['STATIC_URL'] = ''
        
        dump_json(os.path.join(BASE_DIR, 'config.json'), configs)  # 写入配置文件
        self.menuGenerate.Enable(True)

        # self.infos.AppendText(out_infos('项目整合完成，正在进行项目检查和校验......'))
        check_result = self.check(configs['app_names'], path_settings)  # 检测校验
        if check_result:
            self.infos.AppendText(out_infos('项目校验完成，未发现已知问题。', level=1))
            self.btn_fixed_project.Enable(False)
            self.btn_config_project.Enable(True)
        else:
            self.btn_fixed_project.Enable(True)
            self.btn_config_project.Enable(False)

    def check(self, apps, path_settings):
        # 检测应用程序是否均已注册
        settings = {}
        flag = 0
        with open(path_settings, 'r', encoding='utf-8') as f:
            text = f.read().replace('__file__', '"."')
            exec(text, {}, settings)
        for app in apps:
            if app not in settings['INSTALLED_APPS']:
                self.unapps.append(app)
                self.infos.AppendText(
                    out_infos(f'{app}应用程序未注册！（将可能导致项目无法运行）', 2))
                flag = 1

        if 1 == flag:
            return False
        else:
            return True
