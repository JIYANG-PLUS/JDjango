import wx, sqlite3
import wx.lib.buttons as buttons
from wx.lib import scrolledpanel

class SqliteManageDialog(wx.Frame):
    
    def __init__(self, parent=None, id=-1, pos=wx.DefaultPosition, title='SQLite3管理中心-V0.0.1'):
        size = (800, 600)
        wx.Frame.__init__(self, parent, id, title, pos, size)

        panel = wx.Panel(self)

        self.db_path = ''

    def _init_database(self):
        """初始化数据库"""
        # self.conn = sqlite3.connect(self.db_path)
        # self.cursor = self.conn.cursor()

        # c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
        # conn.commit() # 提交更改
        # conn.close() # 关闭连接

        