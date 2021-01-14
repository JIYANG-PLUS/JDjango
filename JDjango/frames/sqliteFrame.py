import wx, os
from ..dialogs.dialogSQLite3 import SelectSQLite3Dialog
from ..tools._tools import *
from ..settings import CONFIG_PATH
import wx.lib.buttons as buttons
# import sqlite3

class SQLiteManageFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"SQLite3管理工具", pos = wx.DefaultPosition, size = wx.Size( 1000,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		mainSizer = wx.BoxSizer( wx.VERTICAL )
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.mainPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.mainPanelSizer = wx.BoxSizer( wx.VERTICAL ) # 垂直
		self.mainPanel.SetSizer( self.mainPanelSizer )
		self.mainPanel.Layout()
		self.mainPanelSizer.Fit( self.mainPanel )
		mainSizer.Add( self.mainPanel, 1, wx.EXPAND |wx.ALL, 5 )
		self.SetSizer( mainSizer ) # frame窗口布局

		self._init_UI()
		self._init_menus()
		self._init_toolbar()
		self._init_statusbar()

		self.Layout()
		self.Centre( wx.BOTH )

		self._init_data()

	def _init_data(self):
		"""初始化截面数据"""
		# 读config.json配置文件
		CONFIGS = get_configs(CONFIG_PATH)
		# if ('DATABASES' in CONFIGS) and ('default' in CONFIGS['DATABASES']) and ('NAME' in CONFIGS['DATABASES']['default']):
		# 	sqlite_path = CONFIGS['DATABASES']['default']['NAME']
		# 	if os.path.isfile(sqlite_path):
		# 		try:
		# 			# self.connectSQLiteObj = sqlite3.connect(sqlite_path)
		# 			...
		# 		except:
		# 			pass
		# 		else:
		# 			# 先提示，后显示
		# 			self.path.SetValue(f"SQLite数据库路径：{sqlite_path}")
		# 			dlg = wx.MessageDialog(self, f"已自动连接SQLite数据库，读取数据库路径{sqlite_path}", "提示信息", wx.OK)
		# 			dlg.ShowModal()
		# 			dlg.Destroy()

	def _init_UI(self):
		"""初始化页面控件"""
		self.path = wx.TextCtrl(self.mainPanel, -1)  # sqlite路径
		self.path.SetEditable(False)
		self.path.Enable(False)

		self.toolPanel = wx.Panel(self.mainPanel) # 工具按钮集
		toolSizer = wx.BoxSizer( wx.HORIZONTAL ) # 水平
		# self.btnSelect = buttons.GenButton(self.toolPanel, -1, 'SELECT') # SELECT查询
		self.btnSelect = wx.Button( self.toolPanel, wx.ID_ANY, u"SELECT", wx.DefaultPosition, wx.DefaultSize, 0 )
		# self.btnDefault = buttons.GenButton(self.toolPanel, -1, '恢复默认布局')
		self.btnDefault = wx.Button( self.toolPanel, wx.ID_ANY, u"恢复默认布局", wx.DefaultPosition, wx.DefaultSize, 0 )
		toolSizer.Add(self.btnSelect, 0, wx.EXPAND | wx.ALL, 2)
		toolSizer.Add(self.btnDefault, 0, wx.EXPAND | wx.ALL, 2)
		self.toolPanel.SetSizer(toolSizer)

		# 分割面板（上下分割）
		self.splitWindow = wx.SplitterWindow(self.mainPanel, -1)
		self.leftPanel = wx.Panel(self.splitWindow, style=wx.SUNKEN_BORDER) # 左子面板
		self.rightPanel = wx.Panel(self.splitWindow, style=wx.SUNKEN_BORDER) # 右子面板
		self.splitWindow.Initialize(self.leftPanel)
		self.splitWindow.Initialize(self.rightPanel)
		# self.leftPanel.SetBackgroundColour("yellow")
		# self.rightPanel.SetBackgroundColour("blue")
		self.splitWindow.SplitVertically(self.leftPanel, self.rightPanel, 621)


		# 左子面板继续分割
		leftPanelSizer = wx.BoxSizer(wx.HORIZONTAL) # 水平
		self.leftSplitWindow = wx.SplitterWindow(self.leftPanel, -1)
		self.leftLeftPanel = wx.Panel(self.leftSplitWindow, style=wx.SUNKEN_BORDER) # 左-左子面板
		self.leftRightPanel = wx.Panel(self.leftSplitWindow, style=wx.SUNKEN_BORDER) # 左-右子面板
		self.leftSplitWindow.Initialize(self.leftLeftPanel)
		self.leftSplitWindow.Initialize(self.leftRightPanel)
		self.leftSplitWindow.SplitVertically(self.leftLeftPanel, self.leftRightPanel, 112)
		leftPanelSizer.Add(self.leftSplitWindow, 1, wx.EXPAND | wx.ALL, 2)
		self.leftPanel.SetSizer(leftPanelSizer)	


		# 左面板-左面板  树形控件
		leftLeftPanelSizer = wx.BoxSizer(wx.VERTICAL)
		self.leftLeftPanel.SetSizer(leftLeftPanelSizer)
		self.tree = wx.TreeCtrl(self.leftLeftPanel)
		self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnClickTree, self.tree)
		self._init_tree()
		leftLeftPanelSizer.Add(self.tree, 1, wx.EXPAND | wx.ALL, 2)

		self.mainPanelSizer.Add(self.path, 0, wx.EXPAND | wx.ALL, 2)
		self.mainPanelSizer.Add(self.toolPanel, 0, wx.EXPAND | wx.ALL, 2)
		self.mainPanelSizer.Add(self.splitWindow, 1, wx.EXPAND | wx.ALL, 2)

	def _init_tree(self):
		"""构建左-左目录树"""
		self.rootdata = self.tree.AddRoot("parent")
		t = self.tree.AppendItem(self.rootdata, "child1")
		self.tree.AppendItem(self.rootdata, "child2")
		self.tree.AppendItem(self.rootdata, "child3")
		self.tree.AppendItem(t, "哈哈")

	def OnClickTree(self, e):
		filename = self.tree.GetItemText(e.GetItem())
		print(filename)

	def _init_statusbar(self):
		"""初始化底部状态条"""
		self.statusBar = self.CreateStatusBar( 2, wx.STB_SIZEGRIP, wx.ID_ANY )
		self.SetStatusWidths([-1, -2])  # 比例为1：2
		self.SetStatusText("连接成功", 1)  # 0代表第一个栏，Ready为内容
		
	def _init_toolbar(self):
		"""初始化工具条"""
		# self.toolBar = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY )
		# self.toolBar.Realize()

	def _init_menus(self):
		"""初始化菜单项"""
		self.menubar = wx.MenuBar( 0 )
		self.linkBar = wx.Menu()
		self.newSQLite3 = wx.MenuItem( self.linkBar, wx.ID_ANY, u"SQLite3", wx.EmptyString, wx.ITEM_NORMAL )
		self.linkBar.Append( self.newSQLite3 )

		self.menubar.Append( self.linkBar, u"连接" )

		self.operateBar = wx.Menu()
		self.DDL = wx.Menu()
		self.DDLCreateDatabase = wx.MenuItem( self.DDL, wx.ID_ANY, u"CREATE DATABASE", wx.EmptyString, wx.ITEM_NORMAL )
		self.DDL.Append( self.DDLCreateDatabase )

		self.DDLCreateTable = wx.MenuItem( self.DDL, wx.ID_ANY, u"CREATE TABLE", wx.EmptyString, wx.ITEM_NORMAL )
		self.DDL.Append( self.DDLCreateTable )

		self.DDLAlterTable = wx.MenuItem( self.DDL, wx.ID_ANY, u"ALTER TABLE", wx.EmptyString, wx.ITEM_NORMAL )
		self.DDL.Append( self.DDLAlterTable )

		self.DDLDropTable = wx.MenuItem( self.DDL, wx.ID_ANY, u"DROP TABLE", wx.EmptyString, wx.ITEM_NORMAL )
		self.DDL.Append( self.DDLDropTable )

		self.DDLCreateView = wx.MenuItem( self.DDL, wx.ID_ANY, u"CREATE VIEW", wx.EmptyString, wx.ITEM_NORMAL )
		self.DDL.Append( self.DDLCreateView )

		self.DDLAlterView = wx.MenuItem( self.DDL, wx.ID_ANY, u"ALTER VIEW", wx.EmptyString, wx.ITEM_NORMAL )
		self.DDL.Append( self.DDLAlterView )

		self.DDLDropView = wx.MenuItem( self.DDL, wx.ID_ANY, u"DROP VIEW", wx.EmptyString, wx.ITEM_NORMAL )
		self.DDL.Append( self.DDLDropView )

		self.DDLTruncateTable = wx.MenuItem( self.DDL, wx.ID_ANY, u"TRUNCATE TABLE", wx.EmptyString, wx.ITEM_NORMAL )
		self.DDL.Append( self.DDLTruncateTable )

		self.operateBar.AppendSubMenu( self.DDL, u"DDL" )

		self.DML = wx.Menu()
		self.DMLInsert = wx.MenuItem( self.DML, wx.ID_ANY, u"INSERT", wx.EmptyString, wx.ITEM_NORMAL )
		self.DML.Append( self.DMLInsert )

		self.DMLUpdate = wx.MenuItem( self.DML, wx.ID_ANY, u"UPDATE", wx.EmptyString, wx.ITEM_NORMAL )
		self.DML.Append( self.DMLUpdate )

		self.DMLDelete = wx.MenuItem( self.DML, wx.ID_ANY, u"DELETE", wx.EmptyString, wx.ITEM_NORMAL )
		self.DML.Append( self.DMLDelete )

		self.operateBar.AppendSubMenu( self.DML, u"DML" )

		self.menubar.Append( self.operateBar, u"数据库操作" )

		self.lltimeMenu = wx.Menu()
		self.lltimeInsert = wx.MenuItem( self.lltimeMenu, wx.ID_ANY, u"SQL导入", wx.EmptyString, wx.ITEM_NORMAL )
		self.lltimeMenu.Append( self.lltimeInsert )

		self.lltimeOutput = wx.MenuItem( self.lltimeMenu, wx.ID_ANY, u"SQL导出", wx.EmptyString, wx.ITEM_NORMAL )
		self.lltimeMenu.Append( self.lltimeOutput )

		self.menubar.Append( self.lltimeMenu, u"持久化" )

		self.directExit = wx.Menu()
		self.btnDirectExit = self.directExit.Append(wx.ID_ANY, "&退出", "退出")

		self.menubar.Append( self.directExit, u"退出" )

		self.SetMenuBar( self.menubar )

		# 事件监听
		self.Bind( wx.EVT_MENU, self.onNewSQLite3, id = self.newSQLite3.GetId() )
		self.Bind(wx.EVT_MENU, self.onExit, self.btnDirectExit)

	def onNewSQLite3(self, e):
		"""创建新的SQLite3连接"""
		dlg = wx.FileDialog(self, "选择SQLite文件", "", "", "*.*", wx.FD_OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
		dlg.Destroy()

	def onExit(self, e):
		"""退出"""
		self.Close(True)

	def __del__( self ):
		"""释放资源"""
		self.connectSQLiteObj.close()
