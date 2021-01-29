#! /usr/bin/env python  
#coding=utf-8  
  
import wx  
  
class MyFrame(wx.Frame):  
    def __init__(self, parent=None, title=u'折叠与展开'):  
        wx.Frame.__init__(self, parent, -1, title=title)  
        self.panel = wx.Panel(self, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN | wx.FULL_REPAINT_ON_RESIZE)  
          
        #增加一些控件:用户名密码部分，并使用GridBagSizer来管理这些控件  
        self.label1=wx.StaticText(self.panel,-1,label=u'用户名：')  
        self.label2=wx.StaticText(self.panel,-1,label=u'密     码：')  
        self.userText=wx.TextCtrl(self.panel,-1,size=(200,25))  
        self.passText=wx.TextCtrl(self.panel,-1,size=(200,25))  
        self.rempassCheck=wx.CheckBox(self.panel,-1,label=u'记住密码')  
        self.autologCheck=wx.CheckBox(self.panel,-1,label=u'自动登录')  
          
        self.gbsizer1=wx.GridBagSizer(hgap=10, vgap=10)  
        self.gbsizer1.Add(self.label1,pos=(0,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)  
        self.gbsizer1.Add(self.userText,pos=(0,1),span=(1,1),flag=wx.EXPAND)  
        self.gbsizer1.Add(self.label2,pos=(1,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)  
        self.gbsizer1.Add(self.passText,pos=(1,1),span=(1,1),flag=wx.EXPAND)  
        self.gbsizer1.Add(self.rempassCheck,pos=(2,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)  
        self.gbsizer1.Add(self.autologCheck,pos=(2,1),span=(1,1),flag=wx.ALIGN_CENTER|wx.ALIGN_CENTRE_VERTICAL)  
          
        #增加一些控件:服务器设置部分，并使用GridBagSizer来管理这些控件，  
        #然后再使用StaticBoxSizer管理GridBagSizer  
        self.label3=wx.StaticText(self.panel,-1,label=u'地址：')  
        self.label4=wx.StaticText(self.panel,-1,label=u'端口：')  
        self.ipadText=wx.TextCtrl(self.panel,-1,size=(170,25))  
        self.portText=wx.TextCtrl(self.panel,-1,size=(170,25))  
        self.proxyBtn=wx.Button(self.panel,-1,label=u'代理\n设置')  
          
        self.gbsizer2=wx.GridBagSizer(hgap=10,vgap=10)  
        self.gbsizer2.Add(self.label3,pos=(0,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)  
        self.gbsizer2.Add(self.ipadText,pos=(0,1),span=(1,1),flag=wx.EXPAND)  
        self.gbsizer2.Add(self.proxyBtn,pos=(0,2),span=(2,1),flag=wx.EXPAND)  
        self.gbsizer2.Add(self.label4,pos=(1,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)  
        self.gbsizer2.Add(self.portText,pos=(1,1),span=(1,1),flag=wx.EXPAND)  
          
        sbox=wx.StaticBox(self.panel,-1,label=u'服务器')  
        self.sbsizer=wx.StaticBoxSizer(sbox,wx.VERTICAL)  
        self.sbsizer.Add(self.gbsizer2,proportion=0,flag=wx.EXPAND,border=10)  
          
        #增加一些控件:最下方的按钮，并使用水平方向的BoxSizer来管理这些控件  
        self.setserverBtn=wx.Button(self.panel,-1,label=u'服务器设置↓')  
        self.loginBtn=wx.Button(self.panel,-1,label=u'登录')  
        self.cancelBtn=wx.Button(self.panel,-1,label=u'取消')  
          
        self.bsizer=wx.BoxSizer(wx.HORIZONTAL)  
        self.bsizer.Add(self.setserverBtn,1,flag=wx.EXPAND)  
        self.bsizer.Add(self.loginBtn)  
        self.bsizer.Add(self.cancelBtn)          
          
        #给"服务器设置"按钮绑定事件处理器  
        self.Bind(wx.EVT_BUTTON, self.OnTouch, self.setserverBtn)  
          
        #增加BoxSizer,管理用户名密码部分的gbsizer1，  
        #服务器设置部分的sbsizer，以及最下方的bsizer  
        self.sizer = wx.BoxSizer(wx.VERTICAL)  
        self.sizer.Add(self.gbsizer1, 0, wx.EXPAND, 20)  
        self.sizer.Add(self.sbsizer, 0, wx.EXPAND, 20)  
        self.sizer.Add(self.bsizer, 0, wx.EXPAND, 20)  
        self.isShown = False    #用这个变量指示当前是否已将控件隐藏  
        self.sizer.Hide(self.sbsizer)    #将控件隐藏  
        self.SetClientSize((330,118))    #更改面板尺寸  
          
        self.panel.SetSizerAndFit(self.sizer)  
        self.sizer.SetSizeHints(self.panel)  
          
    def OnTouch(self, event):  
        if self.isShown:    #如果当前控件已显示  
            self.setserverBtn.SetLabel(u'服务器设置↓')    #更新按钮标签  
            self.sizer.Hide(self.sbsizer)    #隐藏服务器设置部分  
            self.isShown = False    #服务器设置部分当前已隐藏  
            self.SetClientSize((330,118))    #更新面板尺寸  
        else:  
            self.sizer.Show(self.sbsizer)    #如果当前控件已隐藏  
            self.setserverBtn.SetLabel(u'服务器设置↑')    #更新按钮标签  
            self.isShown = True    #服务器设置部分当前已显示  
            self.SetClientSize((330,200))    #更新面板尺寸  
        self.sizer.Layout()    #关键所在，强制sizer重新计算并布局sizer中的控件  
          
          
if __name__ == "__main__":  
    app = wx.PySimpleApp()  
    frame = MyFrame(None)  
    frame.Show(True)  
    app.MainLoop()  