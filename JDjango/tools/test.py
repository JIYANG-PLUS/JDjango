import wx
import wx.grid
class TestTable(wx.grid.PyGridTableBase):
    def __init__(self):
        wx.grid.PyGridTableBase.__init__(self)
        #下面代替取出的数据bai
        self.data = [ [1, 1],
            [2, 2] ,
            [3, 3] ,
            [4, 4] ,
        ]
        # these five are the required methods
    def GetNumberRows(self): return len(self.data)
    def GetNumberCols(self): return len(self.data[0])
    def IsEmptyCell(self, row, col): return True
    def GetValue(self, row, col): return self.data[row][col]
    def SetValue(self, row, col, value): pass

class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title = "Grid Table",
        size = (640, 480))
        grid = wx.grid.Grid(self)
        table = TestTable()
        grid.SetTable(table, True)
app = wx.PySimpleApp()
frame = TestFrame()
frame.Show()
app.MainLoop()