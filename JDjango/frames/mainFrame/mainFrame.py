from .events import *

"""
作用：界面以及功能的展示和补充
"""

class MainFrameFinalGUI(MainFrameFuncs):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._init_platform() # 初始化平台类型（ + 使用限制）
        self._auto_loading_history() # 自动加载历史数据

    def _init_platform(self):
        """初始化并检查"""
        import platform
        self.platform_name = platform.system()
        if self.platform_name.lower() not in env.getAllSupportPlatform():
            wx.MessageBox(f'暂不支持当前平台，已支持：Windows、MacOS。', CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
            self.onExit()
        env.setPlatfrom(self.platform_name)

    def _auto_loading_history(self):
        """自动加载最新的一个历史项目数据"""
        if os.path.exists(CONFIG_PATH):
            self._disable_all_btn() # 初始化按钮状态
            try:
                self.dirname = get_configs(CONFIG_PATH)['dirname']
            except:
                self.infos.AppendText(out_infos('历史项目失效，已被移除，请重新选择！', level=3))
                return
            else:
                if not os.path.exists(self.dirname):
                    self.infos.AppendText(out_infos('历史项目失效，已被移除，请重新选择！', level=3))
                    return
                if 'manage.py' in os.listdir(self.dirname):
                    self.path.SetValue(f'当前项目路径：{self.dirname}')
                    try:
                        self._init_config() # 初始化配置文件
                    except Exception as e:
                        self.infos.AppendText(out_infos('配置文件config.json初始化失败！', level=3))
                    else:
                        self._open_all_check_btn() # 开放所有的检测按钮
                        self._open_part_necessary_btns() # 开放部分必要按钮
                        self.infos.Clear()
                        self.infos.AppendText(out_infos(f'项目{os.path.basename(self.dirname)}导入成功！', level=1))
                else:
                    self.infos.AppendText(out_infos('历史项目失效，已被移除，请重新选择！', level=3))

    def _init_statusbar(self):
        """底部状态栏"""
        super()._init_statusbar()

        self.timer = wx.PyTimer(self.notify) # 循环定时器
        self.timer.Start(1000, wx.TIMER_CONTINUOUS) # 间隔 1 秒
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

        # 按钮监听 不可用
        # simpleui是否启用
        try:
            if djcmd.judge_installed_library(name='simpleui'):
                self.fastSimpleui.Enable(False)
        except: ...


    def __del__(self):
        """释放资源"""
        try:
            env.killProgress()
        except: ...
