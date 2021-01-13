import wx

class SQLiteManageFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"SQLite3管理工具", pos = wx.DefaultPosition, size = wx.Size( 851,598 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		mainSizer = wx.BoxSizer( wx.VERTICAL )
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self._init_menus()
		self._init_toolbar()
		self._init_statusbar()

		self.mainPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		mainPanelSizer = wx.BoxSizer( wx.VERTICAL )

		self.mainPanel.SetSizer( mainPanelSizer )
		self.mainPanel.Layout()
		mainPanelSizer.Fit( self.mainPanel )

		mainSizer.Add( self.mainPanel, 1, wx.EXPAND |wx.ALL, 5 )
		self.SetSizer( mainSizer ) # frame窗口布局

		self.Layout()
		self.Centre( wx.BOTH )

	def _init_statusbar(self):
		"""初始化底部状态条"""
		self.statusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		
	def _init_toolbar(self):
		"""初始化工具条"""
		self.toolBar = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY )
		self.toolBar.Realize()

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

		self.SetMenuBar( self.menubar )


	def __del__( self ):
		"""释放资源"""
		pass

