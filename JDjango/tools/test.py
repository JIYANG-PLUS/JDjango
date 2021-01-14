import wx
 
class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'MyFrame', pos = (-1,-1), size = (700,700), style = wx.DEFAULT_FRAME_STYLE)
        self.tree = wx.TreeCtrl(self)
        self.tree.SetWindowStyle(wx.TR_HAS_VARIABLE_ROW_HEIGHT)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnClickLeftKey, self.tree)
        self.rootdata = self.tree.AddRoot("parent")
        self.tree.AppendItem(self.rootdata, "child1")
        self.tree.AppendItem(self.rootdata, "child2")
        self.tree.AppendItem(self.rootdata, "child3")
 
    def OnClickLeftKey(self, event):
        filename = self.tree.GetItemText(event.GetItem())
        print(filename)

app=wx.PySimpleApp()

frame=MyFrame()

frame.Show(True)

app.MainLoop()
