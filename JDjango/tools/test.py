#! /usr/bin/env python  
#coding=utf-8  
  
import wx  
  
class MyFrame(wx.Frame):  

    def __init__(self, parent=None, title=u'折叠与展开'):  
        wx.Frame.__init__(self, parent, -1, title=title)  
        self.panel = wx.Panel(self, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN | wx.FULL_REPAINT_ON_RESIZE)  
        self.panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.panelSizer)
          
        self.radiosFiledBlankY = wx.RadioButton(self.panel, -1, '允许', style=wx.RB_GROUP)
        self.radiosFiledBlankN = wx.RadioButton(self.panel, -1, '不允许')

        self.panelSizer.Add(self.radiosFiledBlankY, 0, wx.EXPAND | wx.ALL, 2)
        self.panelSizer.Add(self.radiosFiledBlankN, 0, wx.EXPAND | wx.ALL, 2)

        self.Bind(wx.EVT_RADIOBUTTON, self.Funcs, self.radiosFiledBlankY)
        self.Bind(wx.EVT_RADIOBUTTON, self.Funcs, self.radiosFiledBlankN)

    def Funcs(self, e):
        if e.GetId() == self.radiosFiledBlankY.GetId():
            print(self.radiosFiledBlankY.GetValue(), self.radiosFiledBlankN.GetValue())

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyFrame(None)
    frame.Show(True)
    app.MainLoop()
