from .common import *

class EncryptionFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = CON_ENCRYPTION_TITLE, pos = wx.DefaultPosition, size = wx.Size( 1000,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
          
        self._init_UI()
        self._init_menus()
        self._init_statusbar()

    def _init_UI(self):
        """初始化页面控件"""
        self.mainSizer = wx.BoxSizer( wx.VERTICAL )
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.mainPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.mainPanelSizer = wx.BoxSizer( wx.VERTICAL )
        self.mainPanel.SetSizer( self.mainPanelSizer )
        self.mainPanel.Layout()
        self.mainPanelSizer.Fit( self.mainPanel )
        self.mainSizer.Add( self.mainPanel, 1, wx.EXPAND |wx.ALL, 5 )
        self.SetSizer( self.mainSizer )

    def _init_statusbar(self):
        """初始化底部状态条"""
        self.statusBar = self.CreateStatusBar( 2, wx.STB_SIZEGRIP, wx.ID_ANY )
        self.SetStatusWidths([-1, -2])  # 比例为1：2
        # self.SetStatusText(msg, 1)

    def _init_menus(self):
        """初始化菜单项"""
        self.menubar = wx.MenuBar( 0 )
        # self.linkBar = wx.Menu()
        # self.newSQLite3 = wx.MenuItem( self.linkBar, wx.ID_ANY, u"SQLite3", wx.EmptyString, wx.ITEM_NORMAL )
        # self.linkBar.Append( self.newSQLite3 )
        # self.menubar.Append( self.linkBar, u"连接" )

        self.directExit = wx.Menu()
        self.btnDirectExit = self.directExit.Append(wx.ID_ANY, "&退出", "退出")
        self.menubar.Append( self.directExit, u"退出" )

        self.SetMenuBar( self.menubar )

        # 事件
        self.Bind(wx.EVT_MENU, self.onExit, self.btnDirectExit)

    def onExit(self, e):
        """退出"""
        self.Close(True)

    def __del__( self ):
        """释放资源"""

