from .listener import *

"""
作用：实现事件功能
"""

class MainFrameFuncs(MainFrameListener):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def onRegisterkfenvRest(self, e):
        """注册rest_framework"""
        TipsMessageOKBox(self, "功能正在实现中", '提示')

    def onRegisterkfenvDrf(self, e):
        """注册drf_generators"""
        TipsMessageOKBox(self, "功能正在实现中", '提示')

    def onRegisterkfenvAll(self, e):
        """一键全部注册rest_framework、drf_generators"""
        TipsMessageOKBox(self, "功能正在实现中", '提示')

    def onSimpleui(self, e):
        """admin皮肤切换"""
        TipsMessageOKBox(self, "功能正在实现中", '提示')

    @VirtualEnvMustExist()
    def onDjango_filter(self, e):
        """pip install django-filter"""
        TipsMessageOKBox(self, "功能正在实现中", '提示')

    @VirtualEnvMustExist()
    def onMarkdown(self, e):
        """pip install markdown"""
        TipsMessageOKBox(self, "功能正在实现中", '提示')

    @VirtualEnvMustExist()
    def onDjangorestframework(self, e):
        """pip install djangorestframework"""
        TipsMessageOKBox(self, "功能正在实现中", '提示')

    def onHelpsORM(self, e):
        """ORM帮助（一键生成）"""
        dlg = ORMDialog(self)
        dlg.ShowModal()
        dlg.Close(True)

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

    @VirtualEnvMustExist()
    def onPortProgressCollectstatic(self, e):
        """python manage.py collectstatic"""
        import subprocess
        path = os.path.join(get_configs(CONFIG_PATH)['dirname'], 'manage.py')
        env_python3 = os.path.splitext(env.getPython3Env())[0]

        self.amdSubProcess = subprocess.Popen(f'{env_python3} {path} collectstatic', shell=True)
        self.cmdCodes.append(self.amdSubProcess)
        self.info_cmdCodes[self.amdSubProcess] = 'collectstatic'

    @VirtualEnvMustExist()
    def onPortProgressPipFreeze(self, e):
        """导出包pip freeze"""
        import subprocess
        env_python3_pip = os.path.join(os.path.dirname(env.getPython3Env()), 'pip')
        self.cmdEnvPipFreeze = subprocess.Popen(f'{env_python3_pip} freeze', shell=True)
        self.cmdCodes.append(self.cmdEnvPipFreeze)
        self.info_cmdCodes[self.cmdEnvPipFreeze] = 'freeze'

    @VirtualEnvMustExist()
    def onPortProgressPipInstall(self, e):
        """虚拟环境安装包pip install"""
        dlg = wx.TextEntryDialog(self, u"包名：", u"虚拟环境安装三方库", u"")
        if dlg.ShowModal() == wx.ID_OK:
            module_name = dlg.GetValue()

            import subprocess
            
            env_python3_pip = os.path.join(os.path.dirname(env.getPython3Env()), 'pip')

            self.cmdPipInstall = subprocess.Popen(f'{env_python3_pip} install {module_name}', shell=True)
            self.cmdCodes.append(self.cmdPipInstall)
            self.info_cmdCodes[self.cmdPipInstall] = 'install'
        dlg.Close(True)

    @VirtualEnvMustExist()
    def onPortProgressShell(self, e):
        """python manage.py shell"""
        import subprocess
        self.cmdDjangoShell = subprocess.Popen(f'{env.getDjangoOrderArgs()} shell', shell=True)
        self.cmdCodes.append(self.cmdDjangoShell)
        self.info_cmdCodes[self.cmdDjangoShell] = 'shell'
        
    @VirtualEnvMustExist()
    def onPortProgressMakemigrations(self, e):
        """python manage.py makemigrations"""
        import subprocess
        self.cmdMakemigrations = subprocess.Popen(f'{env.getDjangoOrderArgs()} makemigrations', shell=True)
        self.cmdCodes.append(self.cmdMakemigrations)
        self.info_cmdCodes[self.cmdMakemigrations] = 'makemigrations'

    @VirtualEnvMustExist()
    def onPortProgressMigrate(self, e):
        """python manage.py migtrate"""
        import subprocess
        self.cmdMigrate = subprocess.Popen(f'{env.getDjangoOrderArgs()} migrate', shell=True)
        self.cmdCodes.append(self.cmdMigrate)
        self.info_cmdCodes[self.cmdMigrate] = 'migrate'

    @VirtualEnvMustExist()
    def onPortProgressFlush(self, e):
        """python manage.py flush"""
        import subprocess
        self.cmdFlush = subprocess.Popen(f'{env.getDjangoOrderArgs()} flush', shell=True)
        self.cmdCodes.append(self.cmdFlush)
        self.info_cmdCodes[self.cmdFlush] = 'flush'

    @VirtualEnvMustExist()
    def onPortProgressCreatesuperuser(self, e):
        """python manage.py createsuperuser"""
        import subprocess
        self.cmdCreateSuperuser = subprocess.Popen(f'{env.getDjangoOrderArgs()} createsuperuser', shell=True)
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

    @VirtualEnvMustExist()
    def onPortProgressRun(self, e):
        """子进程运行Django"""
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

    def OnKeyDown(self, event):
        """键盘监听"""
        code = event.GetKeyCode()
        if wx.WXK_NUMPAD_ENTER == code or 13 == code:
            self.onExecCommand()
        
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
