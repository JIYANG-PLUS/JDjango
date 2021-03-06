from .listener import *
from ..sqliteFrame import *

"""
作用：实现事件功能
"""

class MainFrameFuncs(MainFrameListener):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.order_container = (self.cmdCodes, self.info_cmdCodes,)

    def onHelpsORM(self, e):
        """ORM帮助（一键生成）"""
        dlg = ORMDialog(self)
        dlg.ShowModal()
        dlg.Close(True)

    def onMenuVSCode(self, e):
        """外部发起VSCode编辑"""
        # 检测是否配置code命令环境
        if wx.Shell("code -v"):
            dirname = get_configs(CONFIG_PATH)['dirname']
            self.cmdVscode = subprocess.Popen(f'code {dirname}', shell=True)
            self.cmdCodes.append(self.cmdVscode)
            self.info_cmdCodes[self.cmdVscode] = '开启VSCode编辑器'
        else:
            self.infoBar.ShowMessage(f'未检测到code命令', wx.ICON_ERROR)

    def onPortProgressVirtualView(self, e):
        """查看虚拟环境路径"""
        RichMsgDialog.showOkMsgDialog(self, env.getPython3Env(), '虚拟环境路径')

    @RegisterOriginOrderDecorator(msg = 'collectstatic')
    @VirtualEnvMustExistDecorator()
    def onPortProgressCollectstatic(self, e):
        """python manage.py collectstatic"""
        return (
            subprocess.Popen(f'{env.getDjangoOrderArgs()} collectstatic', shell=True)
            , *self.order_container
        )

    @RegisterOriginOrderDecorator(msg = 'freeze')
    @VirtualEnvMustExistDecorator()
    def onPortProgressPipFreeze(self, e):
        """导出包pip freeze"""
        return (
            subprocess.Popen(f'{env.getPipOrderArgs(mode="freeze")}', shell=True)
            , *self.order_container
        )

    @VirtualEnvMustExistDecorator()
    def onPortProgressPipInstall(self, e):
        """虚拟环境安装包pip install"""
        dlg = wx.TextEntryDialog(self, u"包名：", u"虚拟环境安装三方库", u"")
        if dlg.ShowModal() == wx.ID_OK:
            module_name = dlg.GetValue()
            self.cmdPipInstall = subprocess.Popen(f'{env.getPipOrderArgs()} {module_name}', shell=True)
            self.cmdCodes.append(self.cmdPipInstall)
            self.info_cmdCodes[self.cmdPipInstall] = 'install'
        dlg.Close(True)

    @RegisterOriginOrderDecorator(msg = 'shell')
    @VirtualEnvMustExistDecorator()
    def onPortProgressShell(self, e):
        """python manage.py shell"""
        return (
            subprocess.Popen(f'{env.getDjangoOrderArgs()} shell', shell=True)
            , *self.order_container
        )
        
    @RegisterOriginOrderDecorator(msg = 'makemigrations')
    @VirtualEnvMustExistDecorator()
    def onPortProgressMakemigrations(self, e):
        """python manage.py makemigrations"""
        return (
            subprocess.Popen(f'{env.getDjangoOrderArgs()} makemigrations', shell=True)
            , *self.order_container
        )

    @RegisterOriginOrderDecorator(msg = 'migrate')
    @VirtualEnvMustExistDecorator()
    def onPortProgressMigrate(self, e):
        """python manage.py migtrate"""
        return (
            subprocess.Popen(f'{env.getDjangoOrderArgs()} migrate', shell=True)
            , *self.order_container
        )

    @RegisterOriginOrderDecorator(msg = 'flush')
    @VirtualEnvMustExistDecorator()
    def onPortProgressFlush(self, e):
        """python manage.py flush"""
        return (
            subprocess.Popen(f'{env.getDjangoOrderArgs()} flush', shell=True)
            , *self.order_container
        )

    @RegisterOriginOrderDecorator(msg = 'createsuperuser')
    @VirtualEnvMustExistDecorator()
    def onPortProgressCreatesuperuser(self, e):
        """python manage.py createsuperuser"""
        return (
            subprocess.Popen(f'{env.getDjangoOrderArgs()} createsuperuser', shell=True)
            , *self.order_container
        )

    def onPortProgressVirtual(self, e):
        """创建虚拟环境"""
        # venv.create(env_dir, system_site_packages=False, clear=False, symlinks=False, with_pip=False, prompt=None)
        dlg = wx.DirDialog(self, u"选择即将写入的虚拟环境文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            env_dir = dlg.GetPath()
            t = len(os.listdir(env_dir))
            if t > 0:
                self.infoBar.ShowMessage(f'检测到选择的文件夹下存在其它文件，禁止操作。', wx.ICON_ERROR)
            else:
                venv.create(env_dir, system_site_packages=False, clear=True, symlinks=False, with_pip=True, prompt=None)
                # 分操作系统自动绑定python解释器
                this_platform = env.getPlatform().lower()
                if 'windows' == this_platform:
                    temp_path = os.path.join(env_dir, 'Scripts', 'python.exe')
                    env.setPython3Env(temp_path)
                    self.infoBar.ShowMessage(f'创建并绑定成功，命令路径：{temp_path}', wx.ICON_INFORMATION)
                elif 'darwin' == this_platform:
                    temp_path = os.path.join(env_dir, 'bin', 'python')
                    env.setPython3Env(temp_path)
                    self.infoBar.ShowMessage(f'创建并绑定成功，命令路径：{temp_path}', wx.ICON_INFORMATION)
                else:
                    self.infoBar.ShowMessage(f'创建成功，虚拟目录：{env_dir}', wx.ICON_INFORMATION)
        dlg.Destroy()

    def onPortProgressKillProgress(self, e):
        """终止进程"""
        dlg = wx.TextEntryDialog(self, u"占用端口号：", u"终止进程", u"")
        if dlg.ShowModal() == wx.ID_OK:
            port = dlg.GetValue()
            env.killProgress(port = port)
            self.infoBar.ShowMessage(f'已终止。', wx.ICON_INFORMATION)
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
                    self.infoBar.ShowMessage(f'当前环境已配置镜像。', wx.ICON_WARNING)
                else:
                    # TEMPLATE_DIR
                    write_file(os.path.join(pip_path, 'pip.ini'), read_file(os.path.join(TEMPLATE_DIR, 'pip', 'pip.ini')))
                    self.infoBar.ShowMessage(f'配置镜像环境成功。', wx.ICON_INFORMATION)
            else:
                pip_path = os.path.join(rpath, 'pip')
                os.mkdir(pip_path)
                write_file(os.path.join(pip_path, 'pip.ini'), read_file(os.path.join(TEMPLATE_DIR, 'pip', 'pip.ini')))
                self.infoBar.ShowMessage(f'配置镜像环境成功。', wx.ICON_INFORMATION)
        elif 'linux' == platform: # 理论上，Mac和Linux配置镜像环境步骤一致
            if '.pip' in os.listdir(rpath):
                pip_path = os.path.join(rpath, '.pip')
                if 'pip.conf' in os.listdir(pip_path):
                    self.infoBar.ShowMessage(f'当前环境已配置镜像。', wx.ICON_WARNING)
                else:
                    write_file(os.path.join(pip_path, 'pip.conf'), read_file(os.path.join(TEMPLATE_DIR, 'pip', 'pip.ini')))
                    self.infoBar.ShowMessage(f'配置镜像环境成功。', wx.ICON_INFORMATION)
            else:
                pip_path = os.path.join(rpath, '.pip')
                os.mkdir(pip_path)
                write_file(os.path.join(pip_path, 'pip.conf'), read_file(os.path.join(TEMPLATE_DIR, 'pip', 'pip.ini')))
                self.infoBar.ShowMessage(f'配置镜像环境成功。', wx.ICON_INFORMATION)
        elif 'darwin' == platform:
            if '.pip' in os.listdir(rpath):
                pip_path = os.path.join(rpath, '.pip')
                if 'pip.conf' in os.listdir(pip_path):
                    self.infoBar.ShowMessage(f'当前环境已配置镜像。', wx.ICON_WARNING)
                else:
                    write_file(os.path.join(pip_path, 'pip.conf'), read_file(os.path.join(TEMPLATE_DIR, 'pip', 'pip.ini')))
                    self.infoBar.ShowMessage(f'配置镜像环境成功。', wx.ICON_INFORMATION)
            else:
                pip_path = os.path.join(rpath, '.pip')
                os.mkdir(pip_path)
                write_file(os.path.join(pip_path, 'pip.conf'), read_file(os.path.join(TEMPLATE_DIR, 'pip', 'pip.ini')))
                self.infoBar.ShowMessage(f'配置镜像环境成功。', wx.ICON_INFORMATION)
        else:
            self.infoBar.ShowMessage(f'未知系统', wx.ICON_WARNING)

    def onModelsProxyGenerate(self, e):
        """创建代理模型"""

    def onPortProgressStop(self, e):
        """关闭网站运行状态"""
        try:
            self.server.terminate()
            env.killProgress()
        except:
            self.infoBar.ShowMessage(f'网站未正常启动或启动异常，导致关闭失败。', wx.ICON_ERROR)
        else:
            self.infos.AppendText(out_infos(f"网站已关闭。", level=1))
            self.portProgressRun.Enable(True)
            self.portProgressStop.Enable(False)

            self.sys_toolbar.EnableTool(self.shotcut_run.GetId(), True)
            self.sys_toolbar.EnableTool(self.shotcut_stop.GetId(), False)
            self.infoBar.ShowMessage(f'网站已关闭。', wx.ICON_INFORMATION)

    def onPortProgressVirtualChoice(self, e):
        """选择虚拟环境"""
        dlg = wx.FileDialog(self, "选择虚拟环境下的python.exe文件", "", "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            env.setPython3Env(os.path.join(dlg.GetDirectory(), dlg.GetFilename()))
            self.infoBar.ShowMessage(f'虚拟环境绑定成功！', wx.ICON_INFORMATION)
        dlg.Close(True)
    
    def onHelpSeeOrKill(self, e):
        """查看或终止进程"""
        RichMsgDialog.showOkMsgDialog(self, CON_MSG_PROGRESS_USE, CON_TIPS_COMMON)

    @VirtualEnvMustExistDecorator()
    def onPortProgressRun(self, e):
        """子进程运行Django"""
        port = env.getDjangoRunPort()
        host = env.getDjangoRunHost()
        try:
            self.server = subprocess.Popen(f'{env.getDjangoOrderArgs()} runserver {port}', shell=True) # , stderr=subprocess.PIPE, stdout=subprocess.PIPE
        except:
            self.infos.AppendText(out_infos(f"虚拟环境错误，或项目路径错误，或端口被占用。", level=3))
        else:
            import webbrowser
            webbrowser.open(f"{host}:{port}/admin/")
            self.infos.AppendText(out_infos(f"网站正在运行，根路由：{host}:{port}。可复制到浏览器打开", level=1))
            self.portProgressRun.Enable(False)
            self.portProgressStop.Enable(True)

            self.sys_toolbar.EnableTool(self.shotcut_run.GetId(), False)
            self.sys_toolbar.EnableTool(self.shotcut_stop.GetId(), True)

    def onModelsGenerate(self, e):
        """创建模型"""
        # dlg = ModelsCreateDialog(self)
        # dlg.ShowModal()
        # dlg.Close(True)
        self.auiNotebook.AddPage(AutoGenModelsPanel(self.auiNotebook), '新增模型', select=True)
        self.auiNotebook.SetSelection(self.auiNotebook.GetPageCount())

    def onSqliteManageTool(self, e):
        """跨平台的Sqlite工具"""
        subFrame = SQLiteManageFrame(None)
        subFrame.Show()
        # manager = os.path.join(os.path.dirname(BASE_DIR), 'sqlite3Manager.pyw')
        # subprocess.Popen(f'{env.getRealPythonOrder()} {manager}', shell=True)

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
            djangotools.fix_urls(_) # 逐个修复
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
        self.unurls = set(djangotools.judge_in_main_urls()) # 全局监测
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
        # dlg = ViewGenerateDialog(self)
        # dlg.ShowModal()
        # dlg.Close(True)
        self.auiNotebook.AddPage(AutoGenViewsPanel(self.auiNotebook), '新增视图', select=True)
        self.auiNotebook.SetSelection(self.auiNotebook.GetPageCount()) # 页签焦点切换

    def onFontsMinus(self, e):
        """显示框字体减小"""
        env.setFontSize(step = 1, method = 'minus')
        self._set_fonts(e)

    def onFontsAdd(self, e):
        """显示框字体增大"""
        env.setFontSize(step = 1, method = 'add')
        self._set_fonts(e)

    def OnKeyDown(self, event):
        """键盘监听"""
        code = event.GetKeyCode()
        if wx.WXK_NUMPAD_ENTER == code or 13 == code:
            self.onExecCommand()
        
    def onAbout(self, e):
        """关于"""
        aboutInfo = wx.adv.AboutDialogInfo()
        aboutInfo.SetName("JDjango")
        aboutInfo.SetVersion(MY_APP_VERSION_STRING)
        aboutInfo.SetDescription(T_("一种快速编写Django的辅助工具！QQ交流群：781517315"))
        aboutInfo.SetCopyright("(C) 2020-2021")
        aboutInfo.SetWebSite("https://github.com/JIYANG-PLUS/JDjango")
        aboutInfo.AddDeveloper("笔小芯 -- jiyangj@foxmail.com\n感谢：@coshare")

        wx.adv.AboutBox(aboutInfo)

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
            returnStatus = djangotools.startapp(message)
            if 0 == returnStatus:
                self.unapps.add(message)
                url_alias = [os.path.basename(_).split('.')[0] for _ in env.getUrlsAlias()][0]
                self.unurls.add(f'{message}.{url_alias}')
                self.infos.AppendText(out_infos(f"{message}应用程序创建成功！", level=1))
                self.onAppsFix(e) # 自动完成注册
                self.onUrlsFix(e) # 自动完成路由注册
                self._init_config() # 重新初始化 配置文件【此操作为敏感操作】
                self.infoBar.ShowMessage(f"{message}应用程序创建成功！", wx.ICON_INFORMATION)
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
            self.infoBar.ShowMessage("检测成功，具体内容详见输出窗口。", wx.ICON_INFORMATION)
        elif bId == self.btn_fixed_project.GetId(): # 修复项目
            self.onFixGlobalProject(e)
            self.infoBar.ShowMessage(f"修复成功！", wx.ICON_INFORMATION)
        elif bId == self.btn_config_project.GetId(): # 项目配置和修改
            dlg = SettingsDialog(self)
            dlg.ShowModal()
            dlg.Close(True)
        elif bId == self.btn_exec.GetId(): # 执行命令
            self.onExecCommand()
        elif bId == self.btn_clear_text.GetId():
            self.onClear(e)

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
                elif '>' == order_split[0].lower():
                    s = cmd.print(' '.join(args))
                else:
                    s = cmd.exec(' '.join(order_split))
                self.infos.AppendText(out_command_infos(command))
                if s:
                    self.infos.AppendText(f"{s}\n")
                self.cmdInput.Clear()
        except Exception as e:
            self.infos.AppendText(out_infos(f'{e}'))

    def onSelectProjectRoot(self):
        """选择项目根路径【项目入口】"""
        dlg = wx.FileDialog(self, "选择Django项目的manage.py文件", r'', "", "*.py", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self._disable_all_btn() # 初始化按钮状态
            filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            if 'manage.py' == filename:
                # self.path.SetValue(f'当前项目路径：{self.dirname}') 【为了美观而放弃】
                self.SetStatusText(f'{self.dirname}', 2)
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
                    self.infoBar.ShowMessage(f'项目{os.path.basename(self.dirname)}导入成功！', wx.ICON_INFORMATION)
            else:
                self.infos.AppendText(out_infos('项目导入失败，请选择Django项目根路径下的manage.py文件。', level=3))
        dlg.Close(True)

    def onAppsCheck(self, e):
        """应用程序 检测"""
        apps = get_configs(CONFIG_PATH)['app_names'] # 实际的 所有 应用程序
        flag = 0
        with open(self.path_settings, 'r', encoding='utf-8') as f:
            settings_apps = eval(djangotools.get_list_patt_content_contain_code(retools.PATT_INSTALLED_APPS, f.read()))
        for app in apps:
            if app not in settings_apps:
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
            temp = retools.PATT_INSTALLED_APPS.search(content).group(0)
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

    def onCloseWindow(self, e):
        """窗口关闭前操作"""
        if self.timer is not None:
            self.timer.Stop()
            self.timer = None
        self.Destroy()

    def DoSearch(self, text):
        return True

    def onAuiNotebookClose(self, e):
        """切换标签关闭前"""
        # print(self.auiNotebook.GetPageText(self.auiNotebook.GetCurrentPage()))
        if (0 == e.GetSelection()):
            # e.Skip()
            # e.StopPropagation()
            e.Veto() # 否决掉事件的发生
            self.infoBar.ShowMessage(f"核心标签不允许关闭！", wx.ICON_WARNING)

    def onLanguage(self, e):
        """语言"""
        self.auiNotebook.AddPage(wx.Panel(self.auiNotebook), '测试', select=True)
        self.auiNotebook.SetSelection(self.auiNotebook.GetPageCount())

    def OnTest(self, e):
        """开发用，测试函数"""
        r = RichMsgDialog.showAskQuestionDialog(self, '测试', '标题')
        print(r)
