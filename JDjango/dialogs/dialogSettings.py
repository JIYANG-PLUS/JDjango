import wx, json, glob, os
import wx.lib.buttons as buttons
from wx.lib import scrolledpanel
from ..tools._tools import *
from ..tools._re import *
from ..settings import BASE_DIR, CONFIG_PATH, SETTINGSS, COR_MIDDLEWARE
from ..tools import environment as env
from ..tools import models as model_env
from ..miniCmd.djangoCmd import *
from ..constant import *
from .dialogTips import *

LABEL_LEN = 99 # 数据库页签 标签 长度（用于美化布局）

class SettingsDialog(wx.Dialog):
    
    def __init__(self, parent):

        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = '项目配置', size=(550, 600))

        self.configs = get_configs(CONFIG_PATH)
       
        self.DIRNAME = self.configs["dirname"] # 正常来说，项目地址和settings.py的路径是不会改变，所以此处拿出。
        self.DIRSETTINGS = os.path.join(self.DIRNAME, self.configs['project_name'], 'settings.py')

        self.specialControls = [] # 特殊的参数

        self._init_UI()

        self.DATA_SETTINGS = {} # settings.py 数据包

        self._init_data()

        self._init_label_font()
        self._init_status()
        self._unshow_special_control()

    def _init_UI(self):
        """初始化界面布局"""
       
        self.labelStaticTexts = [] # 一些控制容器
        
        self.wholePanel = wx.Panel(self)
        self.wholePanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.wholePanel.SetSizer(self.wholePanelSizer)

        self.labels = wx.Notebook(self.wholePanel)
        self.wholePanelSizer.Add(self.labels, 1, wx.EXPAND | wx.ALL, 2)
        
        self._init_settings()        
        self._init_databases()
        self._init_rename()        

        # 底部工具
        wholeToolsPanel = wx.Panel(self.wholePanel)
        wholeToolsBox = wx.BoxSizer(wx.HORIZONTAL)
        wholeToolsPanel.SetSizer(wholeToolsBox)
        self.saveConfig = buttons.GenButton(wholeToolsPanel, -1, '保存')
        wholeToolsBox.Add(self.saveConfig, 0, wx.EXPAND | wx.ALL, 2)
        self.wholePanelSizer.Add(wholeToolsPanel, 0, wx.EXPAND | wx.ALL, 2)

        # 事件监听
        self.Bind(wx.EVT_BUTTON, self.onBtnSaveConfig, self.saveConfig)
    
    def _init_settings(self):
        """setings页面布局"""
        self.otherPanel = scrolledpanel.ScrolledPanel(self.labels, -1) # 其它（可滚动面板）
        self.otherPanel.SetupScrolling()
        otherPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.otherPanel.SetSizer(otherPanelSizer)
        self.labels.AddPage(self.otherPanel, 'Settings')

        # SECRET_KEY
        otherRefreshKeyPanel = wx.Panel(self.otherPanel)
        otherRefreshKeyBOX = wx.BoxSizer(wx.HORIZONTAL)
        otherRefreshKeyPanel.SetSizer(otherRefreshKeyBOX)
        otherPanelSizer.Add(otherRefreshKeyPanel, 0, wx.EXPAND | wx.ALL, 2)
        
        self.btnRefreshSecretKey = buttons.GenButton(otherRefreshKeyPanel, -1, '重置SECRET_KEY') # 刷新 SECRET_KEY
        self.inputRefreshSecretKey = wx.TextCtrl(otherRefreshKeyPanel, -1, style=wx.ALIGN_LEFT) # 显示 SECRET_KEY
        self.inputRefreshSecretKey.Enable(False)
        otherRefreshKeyBOX.Add(self.inputRefreshSecretKey, 1, wx.EXPAND | wx.ALL, 2)
        otherRefreshKeyBOX.Add(self.btnRefreshSecretKey, 0, wx.EXPAND | wx.ALL, 2)
        
        # ALLOWED_HOSTS
        nm = wx.StaticBox(self.otherPanel, -1, 'ALLOWED_HOSTS')
        otherAllowedHostsPanel = wx.StaticBoxSizer(nm, wx.HORIZONTAL)
        otherPanelSizer.Add(otherAllowedHostsPanel, 0, wx.EXPAND | wx.ALL, 2)
        
        self.inputAllowedHosts = wx.TextCtrl(self.otherPanel, -1, style = wx.ALIGN_LEFT) # ip设置
        otherAllowedHostsPanel.Add(self.inputAllowedHosts, 1, wx.EXPAND | wx.ALL, 2)

        # DEBUG
        otherDebugPanel = wx.Panel(self.otherPanel)
        otherDebugBOX = wx.BoxSizer(wx.HORIZONTAL)
        otherDebugPanel.SetSizer(otherDebugBOX)
        otherPanelSizer.Add(otherDebugPanel, 0, wx.EXPAND | wx.ALL, 2)
        
        self.radiosPanel = wx.RadioBox(otherDebugPanel, -1, "调式模式【DEBUG】", choices=['开启', '关闭'])
        otherDebugBOX.Add(self.radiosPanel, 1, wx.EXPAND | wx.ALL, 2)
        
        # LANGUAGE_CODE
        otherLanguageCodePanel = wx.Panel(self.otherPanel)
        otherLanguageCodeBOX = wx.BoxSizer(wx.HORIZONTAL)
        otherLanguageCodePanel.SetSizer(otherLanguageCodeBOX)
        otherPanelSizer.Add(otherLanguageCodePanel, 0, wx.EXPAND | wx.ALL, 2)
        
        self.radiosLanguageCodePanel = wx.RadioBox(otherLanguageCodePanel, -1, "语言环境【LANGUAGE_CODE】", choices=['中文', '英文'])
        otherLanguageCodeBOX.Add(self.radiosLanguageCodePanel, 1, wx.EXPAND | wx.ALL, 2)
        
        # TIME_ZONE
        otherTimeZonePanel = wx.Panel(self.otherPanel)
        otherTimeZoneBOX = wx.BoxSizer(wx.HORIZONTAL)
        otherTimeZonePanel.SetSizer(otherTimeZoneBOX)
        otherPanelSizer.Add(otherTimeZonePanel, 0, wx.EXPAND | wx.ALL, 2)
        
        self.radiosTimeZonePanel = wx.RadioBox(otherTimeZonePanel, -1, "时区【TIME_ZONE】", choices=['伦敦时区', '上海时区', '美国芝加哥'])
        otherTimeZoneBOX.Add(self.radiosTimeZonePanel, 1, wx.EXPAND | wx.ALL, 2)
        
        # USE_I18N
        otherUseI18NPanel = wx.Panel(self.otherPanel)
        otherUseI18NBOX = wx.BoxSizer(wx.HORIZONTAL)
        otherUseI18NPanel.SetSizer(otherUseI18NBOX)
        otherPanelSizer.Add(otherUseI18NPanel, 0, wx.EXPAND | wx.ALL, 2)
        
        self.radiosUseI18NPanel = wx.RadioBox(otherUseI18NPanel, -1, "国际化【USE_I18N】", choices=['开启', '关闭'])
        otherUseI18NBOX.Add(self.radiosUseI18NPanel, 1, wx.EXPAND | wx.ALL, 2)
        
        # USE_L10N
        otherUseL10NPanel = wx.Panel(self.otherPanel)
        otherUseL10NBOX = wx.BoxSizer(wx.HORIZONTAL)
        otherUseL10NPanel.SetSizer(otherUseL10NBOX)
        otherPanelSizer.Add(otherUseL10NPanel, 0, wx.EXPAND | wx.ALL, 2)
        
        self.radiosUseL10NPanel = wx.RadioBox(otherUseL10NPanel, -1, "区域设置优先【USE_L10N】", choices=['开启', '关闭'])
        otherUseL10NBOX.Add(self.radiosUseL10NPanel, 1, wx.EXPAND | wx.ALL, 2)
        
        # USE_TZ
        otherUseTzPanel = wx.Panel(self.otherPanel)
        otherUseTzBOX = wx.BoxSizer(wx.HORIZONTAL)
        otherUseTzPanel.SetSizer(otherUseTzBOX)
        otherPanelSizer.Add(otherUseTzPanel, 0, wx.EXPAND | wx.ALL, 2)
        
        self.radiosUseTzPanel = wx.RadioBox(otherUseTzPanel, -1, "系统时区【USE_TZ】", choices=['开启', '关闭'])
        otherUseTzBOX.Add(self.radiosUseTzPanel, 1, wx.EXPAND | wx.ALL, 2)

        # 主要是后台接口，暂时对静态文件、模板不予处理。
        # STATIC_URL
        # self.radiosUseTzPanel = wx.RadioBox(otherUseTzPanel, -1, "系统时区【USE_TZ】", choices=['开启', '关闭'])

        # STATICFILES_DIRS

        # STATIC_ROOT

        # MEDIA_URL

        # MEDIA_ROOT

        # 跨域 CORS_ORIGIN_ALLOW_ALL  第三方库 django-cors-headers
        otherCorsOriginAllowAllPanel = wx.Panel(self.otherPanel)
        otherCorsOriginAllowAllBOX = wx.BoxSizer(wx.HORIZONTAL)
        otherCorsOriginAllowAllPanel.SetSizer(otherCorsOriginAllowAllBOX)
        otherPanelSizer.Add(otherCorsOriginAllowAllPanel, 0, wx.EXPAND | wx.ALL, 2)
        
        self.radiosCorsOriginAllowAllPanel = wx.RadioBox(otherCorsOriginAllowAllPanel, -1, "跨域请求", choices=['开启', '关闭'])
        otherCorsOriginAllowAllBOX.Add(self.radiosCorsOriginAllowAllPanel, 1, wx.EXPAND | wx.ALL, 2)
        
        # iframe
        otherIframePanel = wx.Panel(self.otherPanel)
        otherIframeBOX = wx.BoxSizer(wx.HORIZONTAL)
        otherIframePanel.SetSizer(otherIframeBOX)
        otherPanelSizer.Add(otherIframePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.radiosIframePanel = wx.RadioBox(otherIframePanel, -1, "iframe模式", choices=['开启', '关闭'])
        otherIframeBOX.Add(self.radiosIframePanel, 1, wx.EXPAND | wx.ALL, 2)
        
        # 事件
        self.Bind(wx.EVT_BUTTON, self.onBtnRefreshSecretKey, self.btnRefreshSecretKey)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, self.radiosPanel)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, self.radiosIframePanel)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, self.radiosLanguageCodePanel)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, self.radiosTimeZonePanel)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, self.radiosUseI18NPanel)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, self.radiosUseL10NPanel)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, self.radiosUseTzPanel)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, self.radiosCorsOriginAllowAllPanel)

    def _init_databases(self):
        """databases页面布局"""
        self.databasesPanel = wx.Panel(self.labels)
        databasesPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.databasesPanel.SetSizer(databasesPanelSizer)
        self.labels.AddPage(self.databasesPanel, '数据库')

        # 当前使用的引擎
        self.labelRecentDatabase = wx.StaticText(self.databasesPanel, -1, "当前数据库引擎：", style=wx.ALIGN_CENTRE_HORIZONTAL)
        databasesPanelSizer.Add(self.labelRecentDatabase, 0, wx.EXPAND | wx.ALL, 2)

        # 选择数据库引擎
        self.choiceDatabaseStaticBox = wx.StaticBox(self.databasesPanel, -1, '')
        self.choiceDatabasePanel = wx.StaticBoxSizer(self.choiceDatabaseStaticBox, wx.HORIZONTAL)
        databasesPanelSizer.Add(self.choiceDatabasePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelChoiceDatabase = wx.StaticText(self.databasesPanel, -1, "切换引擎：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_LEN, -1))
        self.choiceDatabase = wx.Choice(self.databasesPanel, -1, choices=[' ',]+env.getDjangoSupportDatabase())
        self.choiceDatabasePanel.Add(self.labelChoiceDatabase, 0, wx.EXPAND | wx.ALL, 2)
        self.choiceDatabasePanel.Add(self.choiceDatabase, 1, wx.EXPAND | wx.ALL, 2)

        # ENGINE
        self.inputEngineStaticBox = wx.StaticBox(self.databasesPanel, -1, '')
        self.inputEnginePanel = wx.StaticBoxSizer(self.inputEngineStaticBox, wx.HORIZONTAL)
        databasesPanelSizer.Add(self.inputEnginePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputEngine = wx.StaticText(self.databasesPanel, -1, "引擎名称：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_LEN, -1))
        self.inputEngine = wx.TextCtrl(self.databasesPanel, -1)
        self.inputEnginePanel.Add(self.labelInputEngine, 0, wx.EXPAND | wx.ALL, 2)
        self.inputEnginePanel.Add(self.inputEngine, 1, wx.EXPAND | wx.ALL, 2)

        # NAME
        self.inputNameStaticBox = wx.StaticBox(self.databasesPanel, -1, '')
        self.inputNamePanel = wx.StaticBoxSizer(self.inputNameStaticBox, wx.HORIZONTAL)
        databasesPanelSizer.Add(self.inputNamePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputName = wx.StaticText(self.databasesPanel, -1, "数据库名：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_LEN, -1))
        self.inputName = wx.TextCtrl(self.databasesPanel, -1)
        self.inputNamePanel.Add(self.labelInputName, 0, wx.EXPAND | wx.ALL, 2)
        self.inputNamePanel.Add(self.inputName, 1, wx.EXPAND | wx.ALL, 2)

        # 下面的参数在选择引擎的时候，按需开启
        # USER
        self.inputUserStaticBox = wx.StaticBox(self.databasesPanel, -1, '')
        self.inputUserPanel = wx.StaticBoxSizer(self.inputUserStaticBox, wx.HORIZONTAL)
        databasesPanelSizer.Add(self.inputUserPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputUser = wx.StaticText(self.databasesPanel, -1, "用户名：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_LEN, -1))
        self.inputUser = wx.TextCtrl(self.databasesPanel, -1)
        self.inputUserPanel.Add(self.labelInputUser, 0, wx.EXPAND | wx.ALL, 2)
        self.inputUserPanel.Add(self.inputUser, 1, wx.EXPAND | wx.ALL, 2)

        # PASSWORD
        self.inputPasswordStaticBox = wx.StaticBox(self.databasesPanel, -1, '')
        self.inputPasswordPanel = wx.StaticBoxSizer(self.inputPasswordStaticBox, wx.HORIZONTAL)
        databasesPanelSizer.Add(self.inputPasswordPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputPassword = wx.StaticText(self.databasesPanel, -1, "密码：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_LEN, -1))
        self.inputPassword = wx.TextCtrl(self.databasesPanel, -1, style = wx.TE_PASSWORD)
        self.inputPasswordPanel.Add(self.labelInputPassword, 0, wx.EXPAND | wx.ALL, 2)
        self.inputPasswordPanel.Add(self.inputPassword, 1, wx.EXPAND | wx.ALL, 2)

        # HOST
        self.inputHostStaticBox = wx.StaticBox(self.databasesPanel, -1, '')
        self.inputHostPanel = wx.StaticBoxSizer(self.inputHostStaticBox, wx.HORIZONTAL)
        databasesPanelSizer.Add(self.inputHostPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputHost = wx.StaticText(self.databasesPanel, -1, "IP地址：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_LEN, -1))
        self.inputHost = wx.TextCtrl(self.databasesPanel, -1)
        self.inputHostPanel.Add(self.labelInputHost, 0, wx.EXPAND | wx.ALL, 2)
        self.inputHostPanel.Add(self.inputHost, 1, wx.EXPAND | wx.ALL, 2)

        # PORT
        self.inputPortStaticBox = wx.StaticBox(self.databasesPanel, -1, '')
        self.inputPortPanel = wx.StaticBoxSizer(self.inputPortStaticBox, wx.HORIZONTAL)
        databasesPanelSizer.Add(self.inputPortPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputPort = wx.StaticText(self.databasesPanel, -1, "端口：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_LEN, -1))
        self.inputPort = wx.TextCtrl(self.databasesPanel, -1)
        self.inputPortPanel.Add(self.labelInputPort, 0, wx.EXPAND | wx.ALL, 2)
        self.inputPortPanel.Add(self.inputPort, 1, wx.EXPAND | wx.ALL, 2)

        # TEST
        self.inputTestStaticBox = wx.StaticBox(self.databasesPanel, -1, '')
        self.inputTestPanel = wx.StaticBoxSizer(self.inputTestStaticBox, wx.HORIZONTAL)
        databasesPanelSizer.Add(self.inputTestPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputTest = wx.StaticText(self.databasesPanel, -1, "编码环境：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_LEN, -1))
        self.inputTest = wx.TextCtrl(self.databasesPanel, -1)
        self.inputTestPanel.Add(self.labelInputTest, 0, wx.EXPAND | wx.ALL, 2)
        self.inputTestPanel.Add(self.inputTest, 1, wx.EXPAND | wx.ALL, 2)

        # 按钮
        self.btnOperationStaticBox = wx.StaticBox(self.databasesPanel, -1, '')
        self.btnOperationPanel = wx.StaticBoxSizer(self.btnOperationStaticBox, wx.HORIZONTAL)
        databasesPanelSizer.Add(self.btnOperationPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.btnOperationBlank = buttons.GenButton(self.databasesPanel, -1, ' ')
        self.btnOperationTestLink = buttons.GenButton(self.databasesPanel, -1, '测试连接')
        self.btnOperationChangeDataSource = buttons.GenButton(self.databasesPanel, -1, '切换数据源')
        self.btnOperationPanel.Add(self.btnOperationBlank, 1, wx.EXPAND | wx.ALL, 2)
        self.btnOperationPanel.Add(self.btnOperationTestLink, 0, wx.EXPAND | wx.ALL, 2)
        self.btnOperationPanel.Add(self.btnOperationChangeDataSource, 0, wx.EXPAND | wx.ALL, 2)

        # 专属控件
        self.specialControls.extend([
            self.inputNameStaticBox, self.labelInputName, self.inputName,
            self.inputUserStaticBox, self.labelInputUser, self.inputUser,
            self.inputPasswordStaticBox, self.labelInputPassword, self.inputPassword,
            self.inputHostStaticBox, self.labelInputHost, self.inputHost,
            self.inputPortStaticBox, self.labelInputPort, self.inputPort,
            self.inputTestStaticBox, self.labelInputTest, self.inputTest,
            self.btnOperationStaticBox, self.btnOperationBlank, self.btnOperationTestLink, self.btnOperationChangeDataSource,
        ])

        # 标签美化
        self.labelStaticTexts.extend([
            self.labelRecentDatabase, self.labelChoiceDatabase,
            self.labelInputEngine, self.labelInputName,

            self.labelInputUser, self.labelInputPassword,
            self.labelInputHost, self.labelInputPort,
            self.labelInputTest, 
        ])

        # 事件
        self.Bind(wx.EVT_CHOICE, self.onChoiceDatabase, self.choiceDatabase)

        self.Bind(wx.EVT_BUTTON, self.onBtnOperationTestLink, self.btnOperationTestLink)
        self.Bind(wx.EVT_BUTTON, self.onBtnOperationChangeDataSource, self.btnOperationChangeDataSource)

    def onBtnOperationTestLink(self, e):
        """测试连接"""
        # 能看到按钮，必定选择了支持的数据源，否则绝对看不到

        # 取出所有的值
        name = self.inputName.GetValue().strip()
        user = self.inputUser.GetValue().strip()
        password = self.inputPassword.GetValue().strip()
        host = self.inputHost.GetValue().strip()
        port = int(self.inputPort.GetValue().strip())

        if all([name, user, password, host, port]):
            # 检测有没有安装 pymysql
            try:
                import pymysql
            except:
                TipsMessageOKBox(self, '此功能需要您在非虚拟环境安装pymysql模块。（pip install pymysql）', '错误') # ，请在【运行】->【原生指令】->【pip install】弹出窗口输入【pymysql】进行安装
            else:
                try:
                    conn = pymysql.connect(host=host, user=user, password=password, db=name, port=port)
                    # conn.ping() # 查看实时连接
                except Exception as e:
                    TipsMessageOKBox(self, f'连接失败。{e}', '错误')
                else:
                    TipsMessageOKBox(self, '连接成功', '成功')
            finally:
                try:
                    conn.close()
                except:
                    pass
        else:
            TipsMessageOKBox(self, '请填全数据库信息。', '错误')

    def onBtnOperationChangeDataSource(self, e):
        """切换数据源"""
        source = self.choiceDatabase.GetString(self.choiceDatabase.GetSelection()).strip()
        django_engine = self.inputEngine.GetValue().strip()
        test = self.inputTest.GetValue().strip()

        if 'sqlite' == source:
            name = f"os.path.join(BASE_DIR, '{self.inputName.GetValue().strip()}')"
        else:
            name = self.inputName.GetValue().strip()
        user = self.inputUser.GetValue().strip()
        password = self.inputPassword.GetValue().strip()
        host = self.inputHost.GetValue().strip()
        port = self.inputPort.GetValue().strip()

        if all([name, user, password, host, port]) or ('sqlite' == source and all([name,])):
            # update_settings_DTATBASES
            dlg_tip = wx.MessageDialog(self, f"一旦切换数据源，之前的数据源配置将丢失，请做好备份。建议测试连接成功后进行切换！（sqlite无需测试）", CON_TIPS_COMMON, wx.CANCEL | wx.OK)
            if dlg_tip.ShowModal() == wx.ID_OK:
                try:
                    update_settings_DTATBASES(source,
                        engine=django_engine,
                        database_name = name,
                        username = user,
                        password = password,
                        ip = host,
                        port = port,
                        test = test
                    )
                except Exception as e:
                    TipsMessageOKBox(self, f'暂不支持{source}数据库引擎。', '错误')
                else:
                    last_engine = self.labelRecentDatabase.GetLabel().replace('当前数据库引擎：', '')
                    TipsMessageOKBox(self, f'成功，数据库引擎已从{last_engine}替换成{source}！', '成功')
            dlg_tip.Close(True)
        else:
            TipsMessageOKBox(self, '请填全数据库信息。', '错误')

    def _init_status(self):
        """初始化控件状态"""
        # database
        self.inputEngine.Enable(False)
        self.btnOperationBlank.Enable(False)

    def _unshow_special_control(self):
        """隐藏特殊控件"""
        for _ in self.specialControls:
            _.Show(False)

    def _show_special_control(self):
        """显示所有特殊控件"""
        for _ in self.specialControls:
            _.Show(True)

    def onChoiceDatabase(self, e):
        """选择数据库类型"""
        database_type = e.GetString().strip()

        self._unshow_special_control() # 先隐藏，后按需打开

        if not database_type:
            return

        if 'sqlite' == database_type:
            self.inputEngine.SetValue('django.db.backends.sqlite3')
            self.inputName.SetValue("db.sqlite3") # os.path.join(BASE_DIR, 'db.sqlite3')
            self.inputTest.SetValue("")
            self.inputPort.SetValue('')

            self.inputNameStaticBox.Show(True)
            self.labelInputName.Show(True)
            self.inputName.Show(True)

            self.btnOperationStaticBox.Show(True)
            self.btnOperationBlank.Show(True)
            self.btnOperationChangeDataSource.Show(True)
            
        elif 'mysql' == database_type:
            self.inputEngine.SetValue('django.db.backends.mysql')
            self.inputName.SetValue("")
            self.inputTest.SetValue("{'CHARSET' : 'utf8', 'COLLATION':'utf8_general_ci', }")
            self.inputPort.SetValue('3306')

            self._show_special_control()

        elif 'postgresql' == database_type:
            self.inputEngine.SetValue('django.db.backends.postgresql')
            self.inputName.SetValue("")
            self.inputTest.SetValue("")
            self.inputPort.SetValue('5432')

        elif 'oracle' == database_type:
            self.inputEngine.SetValue('django.db.backends.oracle')
            self.inputName.SetValue("")
            self.inputTest.SetValue("")
            self.inputPort.SetValue('1521')

        # 共用
        self.inputHost.SetValue('127.0.0.1')
        self.inputUser.SetValue('')
        self.inputPassword.SetValue('')

        self.databasesPanel.Layout()

    def _init_label_font(self):
        """标签提示信息字体初始化"""
        for _ in self.labelStaticTexts:
            _.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            _.SetForegroundColour(CON_COLOR_BLUE)

    def _init_rename(self):
        """rename页面布局"""
        self.projectRenamePanel = wx.Panel(self.labels)
        projectRenameBox = wx.BoxSizer(wx.VERTICAL)
        self.projectRenamePanel.SetSizer(projectRenameBox)
        self.labels.AddPage(self.projectRenamePanel, '项目重命名')

        # 内部实际布局
        self.renamePanel = wx.Panel(self.projectRenamePanel)
        renameBox = wx.BoxSizer(wx.VERTICAL)
        self.renamePanel.SetSizer(renameBox)
        projectRenameBox.Add(self.renamePanel, 1, wx.ALL | wx.CENTER, 5)

        # 名称输入框
        inputNameStaticBox = wx.StaticBox(self.renamePanel, -1, 'Django项目：')
        inputNamePanel = wx.StaticBoxSizer(inputNameStaticBox, wx.VERTICAL)
        inputNameBoxHor = wx.BoxSizer(wx.HORIZONTAL)
        inputNamePanel.Add(inputNameBoxHor, 0, wx.ALL | wx.CENTER, 10)
        renameBox.Add(inputNamePanel, 0, wx.ALL | wx.CENTER, 5)

        labelProjectName = wx.StaticText(self.renamePanel, -1, "您的项目名称：") # 项目名称
        self.inputProjectName = wx.TextCtrl(self.renamePanel, -1, style=wx.ALIGN_LEFT) # 输入框
        inputNameBoxHor.Add(labelProjectName, 0, wx.ALL | wx.CENTER, 5)
        inputNameBoxHor.Add(self.inputProjectName, 0, wx.ALL | wx.CENTER, 5)

        # 其它
        self.labelFirst = wx.StaticText(self.renamePanel, -1, "请先关闭所有占用此Django项目的程序。（否则会遇到修改权限问题）")
        self.btnModify = buttons.GenButton(self.renamePanel, -1, label='修改（修改前请提前做好备份）')
        self.labelTip = wx.StaticText(self.renamePanel, -1, "请确保您的项目名称在您整个项目中是独一无二的，否则本功能会严重破坏您的项目")
        renameBox.Add(self.labelFirst, 0, wx.ALL | wx.CENTER, 5)
        renameBox.Add(self.labelTip, 0, wx.ALL | wx.CENTER, 5)
        renameBox.Add(self.btnModify, 0, wx.ALL | wx.CENTER, 5)

        # 事件绑定
        self.Bind(wx.EVT_BUTTON, self.onBtnModify, self.btnModify)

    def _init_data(self):
        CONFIGS = get_configs(CONFIG_PATH)
        # settings 0 开启，1关闭
        self.radiosPanel.SetSelection(0 if CONFIGS['DEBUG'] else 1)
        self.radiosIframePanel.SetSelection(0 if CONFIGS['X_FRAME_OPTIONS'] else 1)
        self.radiosLanguageCodePanel.SetSelection(0 if CONFIGS['LANGUAGE_CODE'].lower() in [_.lower() for _ in SETTINGSS['LANGUAGE_CODE'][0]] else 1)
        for k, v in SETTINGSS['TIME_ZONE'].items():
            if CONFIGS['TIME_ZONE'].lower() in [_.lower() for _ in v]:
                self.radiosTimeZonePanel.SetSelection(k)
                break
        else:
            self.radiosTimeZonePanel.SetSelection(0)
        self.radiosUseI18NPanel.SetSelection(0 if CONFIGS['USE_I18N'] else 1)
        self.radiosUseL10NPanel.SetSelection(0 if CONFIGS['USE_L10N'] else 1)
        self.radiosUseTzPanel.SetSelection(0 if CONFIGS['USE_TZ'] else 1)
        self.inputRefreshSecretKey.SetValue(CONFIGS['SECRET_KEY'])
        self.inputAllowedHosts.SetValue(','.join(CONFIGS['ALLOWED_HOSTS']))
        self.radiosCorsOriginAllowAllPanel.SetSelection(0 if CONFIGS['CORS_ORIGIN_ALLOW_ALL'] else 1)

        # 重命名
        self.inputProjectName.SetValue(CONFIGS['project_name'])

        # database
        try:
            t = get_configs(CONFIG_PATH)['DATABASES']['default']['ENGINE'].lower()
            if 'sqlite3' in t:
                n_engine = 'sqlite3'
            elif 'mysql' in t:
                n_engine = 'mysql'
            elif 'oracle' in t:
                n_engine = 'oracle'
            elif 'postgresql' in t:
                n_engine = 'postgresql'
            else: # Django 原生不支持 SQLServer
                n_engine = '未知'
        except:
            self.labelRecentDatabase.SetLabel(self.labelRecentDatabase.GetLabel()+'配置文件错误，读取失败！')
        else:
            self.labelRecentDatabase.SetLabel(self.labelRecentDatabase.GetLabel()+n_engine)
        self.choiceDatabase.SetSelection(0)

    @property
    def _check_env_exist(self)->bool:
        """检测虚拟环境是否存在"""
        env_path = env.getPython3Env()
        if '' == env_path.strip() or not os.path.exists(env_path):
            return False
        return True

    def onBtnSaveConfig(self, e):
        """保存修改"""
        try:
            CONFIGS = get_configs(CONFIG_PATH)
            content_settings = read_file(self.DIRSETTINGS)
            temp = content_settings
            if None != self.DATA_SETTINGS.get('DEBUG'):
                temp = patt_sub_only_capture_obj(PATT_DEBUG, self.DATA_SETTINGS['DEBUG'], temp)
            if None != self.DATA_SETTINGS.get('USE_I18N'):
                temp = patt_sub_only_capture_obj(PATT_USE_I18N, self.DATA_SETTINGS['USE_I18N'], temp)
            if None != self.DATA_SETTINGS.get('USE_L10N'):
                temp = patt_sub_only_capture_obj(PATT_USE_L10N, self.DATA_SETTINGS['USE_L10N'], temp)
            if None != self.DATA_SETTINGS.get('USE_TZ'):
                temp = patt_sub_only_capture_obj(PATT_USE_TZ, self.DATA_SETTINGS['USE_TZ'], temp)
            if None != self.DATA_SETTINGS.get('CORS_ORIGIN_ALLOW_ALL'):
                temp = patt_sub_only_capture_obj(PATT_CORS_ORIGIN_ALLOW_ALL, self.DATA_SETTINGS['CORS_ORIGIN_ALLOW_ALL'], temp)
            if None != self.DATA_SETTINGS.get('X_FRAME_OPTIONS'):
                if self.DATA_SETTINGS['X_FRAME_OPTIONS']: # 开启
                    if not CONFIGS['X_FRAME_OPTIONS']: # 且原文件不存在
                        TEMPLATE_DIR = os.path.join(BASE_DIR, 'djangoTemplates', 'settings', 'iframe.django')
                        # 在文件末尾添加iframe开启代码
                        write_file(self.DIRSETTINGS, temp) # 刷新
                        append_file(self.DIRSETTINGS, read_file_list(TEMPLATE_DIR))
                        temp = read_file(self.DIRSETTINGS) # 刷新
                else: # 关闭（删除）
                    temp = PATT_X_FRAME_OPTIONS.sub('', temp)
            if None != self.DATA_SETTINGS.get('LANGUAGE_CODE'):
                re_str = SETTINGSS['LANGUAGE_CODE'][self.DATA_SETTINGS['LANGUAGE_CODE']][0]
                temp = patt_sub_only_capture_obj(PATT_LANGUAGE_CODE, re_str, temp)
            if None != self.DATA_SETTINGS.get('TIME_ZONE'):
                re_str = SETTINGSS['TIME_ZONE'][self.DATA_SETTINGS['TIME_ZONE']][0]
                temp = patt_sub_only_capture_obj(PATT_TIME_ZONE, re_str, temp)
            # 写入SECRET_KEY和HOST
            temp = patt_sub_only_capture_obj(PATT_SECRET_KEY, self.inputRefreshSecretKey.GetValue(), temp)
            host_contents = [f"'{_}'" for _ in self.inputAllowedHosts.GetValue().strip().split(',') if _]
            temp = patt_sub_only_capture_obj_obtain_double(PATT_ALLOWED_HOSTS, ','.join(host_contents), temp)

            write_file(self.DIRSETTINGS, temp) # 更新settings.py文件

            # 跨域中间件介入
            if 'True' == self.DATA_SETTINGS.get('CORS_ORIGIN_ALLOW_ALL'): # 开启时写入中间件
                # 检测是否正确配置虚拟环境
                if not self._check_env_exist:
                    wx.MessageBox(f'虚拟环境未绑定，或绑定失败！（仅跨域请求更新失败）', CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
                    return

                add_oneline_to_listattr(self.DIRSETTINGS, PATT_MIDDLEWARE, COR_MIDDLEWARE)
                # 开进程，安装必须库
                module_name = 'django-cors-headers'
                import subprocess
                env_python3_pip = os.path.join(os.path.dirname(env.getPython3Env()), 'pip')
                subprocess.Popen(f'{env_python3_pip} install {module_name}', shell=True)
            else:
                pop_oneline_to_listattr(self.DIRSETTINGS, PATT_MIDDLEWARE, COR_MIDDLEWARE)

            refresh_config() # 更新配置文件【重要且必须！！！】

            self.DATA_SETTINGS = {} # 防止重复确定，重要！！！
        except:
            wx.MessageBox(f'错误，配置文件已损坏。', '错误', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox(f'修改成功！', '成功', wx.OK | wx.ICON_INFORMATION)
        
    def onBtnModify(self, e):
        """重命名项目名称"""
        # 再次提醒
        dlgA = wx.MessageDialog(self, u"请再次确认", u"确认信息", wx.YES_NO | wx.ICON_QUESTION)
        if dlgA.ShowModal() == wx.ID_YES:
            self.configs = get_configs(os.path.join(BASE_DIR, 'config.json'))
            # 获取新的名称
            old_name = self.configs['project_name']
            new_name = self.inputProjectName.GetValue().strip()

            if old_name == new_name:
                dlg = wx.MessageDialog( self, "未做任何修改", "警告", wx.OK)
                dlg.ShowModal()
                dlg.Close(True)
                return

            if not PATT_CHARS.match(new_name):
                dlg = wx.MessageDialog( self, "请使用字母+下划线的方式命名", "错误", wx.OK)
                dlg.ShowModal()
                dlg.Close(True)
                return
            try:
                # 重命名项目（先文件，后目录）
                search_path = os.path.join(self.DIRNAME, '**', '*')
                alls = glob.glob(search_path, recursive=True)

                # 分类文件和文件夹
                files, floders = [], []
                for _ in alls:
                    if os.path.isfile(_): files.append(_)
                    else: floders.append(_)

                for p in files:
                    # 先读后写
                    if '.py' == os.path.splitext(p)[1]:
                        content = read_file(p)
                        content = content.replace(old_name.strip(), new_name)
                        write_file(p, content)

                for P in floders:
                    if old_name.strip().lower() == os.path.basename(P).strip().lower():
                        temp = os.path.join(os.path.dirname(P), new_name)
                        os.rename(P, temp)

                # 修改根目录名称
                os.rename(self.DIRNAME, os.path.join(os.path.dirname(self.DIRNAME), new_name))
                
                dlg = wx.MessageDialog( self, "修改成功，请退出所有窗口后重新打开，进行后续操作。", "成功", wx.OK)
                if dlg.ShowModal() == wx.ID_OK:
                    self.Close(True)
                dlg.ShowModal()
                dlg.Close(True)
            except:
                """操作回退，将之前所有的改动还原"""
                pass # 待完成
        dlgA.Close(True)

    def onRadioBox(self, e):
        """单选框组事件"""
        # 原则上只对需要改变的内容进行修改
        key = e.GetId()
        if key == self.radiosPanel.GetId(): # DEBUG
            self.DATA_SETTINGS['DEBUG'] = 'True' if 0 == self.radiosPanel.GetSelection() else 'False'
        elif key == self.radiosIframePanel.GetId(): # X_FRAME_OPTIONS
            self.DATA_SETTINGS['X_FRAME_OPTIONS'] = True if 0 == self.radiosIframePanel.GetSelection() else False
        elif key == self.radiosLanguageCodePanel.GetId(): # LANGUAGE_CODE
            self.DATA_SETTINGS['LANGUAGE_CODE'] = self.radiosLanguageCodePanel.GetSelection()
        elif key == self.radiosTimeZonePanel.GetId(): # TIME_ZONE
            self.DATA_SETTINGS['TIME_ZONE'] = self.radiosTimeZonePanel.GetSelection()
        elif key == self.radiosUseI18NPanel.GetId(): # USE_I18N
            self.DATA_SETTINGS['USE_I18N'] = 'True' if 0 == self.radiosUseI18NPanel.GetSelection() else 'False'
        elif key == self.radiosUseL10NPanel.GetId(): # USE_L10N
            self.DATA_SETTINGS['USE_L10N'] = 'True' if 0 == self.radiosUseL10NPanel.GetSelection() else 'False'
        elif key == self.radiosUseTzPanel.GetId(): # USE_TZ
            self.DATA_SETTINGS['USE_TZ'] = 'True' if 0 == self.radiosUseTzPanel.GetSelection() else 'False'
        elif key == self.radiosCorsOriginAllowAllPanel.GetId(): # CORS_ORIGIN_ALLOW_ALL
            self.DATA_SETTINGS['CORS_ORIGIN_ALLOW_ALL'] = 'True' if 0 == self.radiosCorsOriginAllowAllPanel.GetSelection() else 'False'
        
    def onBtnRefreshSecretKey(self, e):
        """刷新SECRET_KEY"""
        new_key = generate_secret_key()
        self.DATA_SETTINGS['SECRET_KEY'] = new_key
        self.inputRefreshSecretKey.SetValue(new_key)
