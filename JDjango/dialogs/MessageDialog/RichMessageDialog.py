from .common import *

class RichMsgDialog:

    def __init__(self) -> None:
        pass

    @classmethod
    def showScrolledMsgDialog(cls, parent, msg: str, title: str):
        """纯文本滚动面板提示消息"""
        dlg = wx.lib.dialogs.ScrolledMessageDialog(parent, msg, title)
        dlg.ShowModal()

    @classmethod
    def showAboutMsgDialog(cls, parent, name: str, description: str, version='1.0.0', copyright='(c) 2020-2021', licenseText='', developers=['JDjango']):
        """【关于】信息展示"""
        info = wx.adv.AboutDialogInfo()
        info.Name = name
        info.Version = version
        info.Copyright = copyright
        info.Description = wordwrap(description, 350, wx.ClientDC(parent))
        # info.WebSite = ("http://en.wikipedia.org/wiki/Hello_world", "Hello World home page")
        info.Developers = developers
        info.License = wordwrap(licenseText, 500, wx.ClientDC(parent))
        wx.adv.AboutBox(info)

    @classmethod
    def showOkMsgDialog(cls, parent, msg: str, title: str):
        """仅有OK的提示对话框"""
        dlg = wx.MessageDialog(parent, msg, title, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    @classmethod
    def showYesNoCancelMsgDialog(cls, parent, msg: str, title: str):
        """有YES、NO、Cancel的对话框（返回YES或NO）"""
        dlg = wx.MessageDialog(parent, msg, title, wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION)
        action = False
        if wx.ID_YES == dlg.ShowModal():
            action = True
        dlg.Destroy()
        return action

    @classmethod
    def showYesNoMsgDialog(cls, parent, msg: str, title: str):
        """有YES、NO的对话框（返回YES或NO）"""
        dlg = wx.MessageDialog(parent, msg, title, wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
        action = False
        if wx.ID_YES == dlg.ShowModal():
            action = True
        dlg.Destroy()
        return action

    @classmethod
    def showMultiChoiceDialog(cls, parent, msg: str, title: str, list_data: list=[])->list:
        """展示列表多选对话框并返回选择列表结果"""
        dlg = wx.MultiChoiceDialog(parent, msg, title, list_data)
        choices = []
        if wx.ID_OK == dlg.ShowModal():
            selections = dlg.GetSelections()
            choices = [list_data[x] for x in selections]
        dlg.Destroy()
        return choices

    @classmethod
    def showSingleChoiceDialog(cls, parent, msg: str, title: str, list_data: list=[])->str:
        """展示列表单选对话框并返回选择结果，无结果返回None"""
        dlg = wx.SingleChoiceDialog(parent, msg, title, list_data, wx.CHOICEDLG_STYLE)
        choice = None
        if wx.ID_OK == dlg.ShowModal():
            choice = dlg.GetStringSelection()
        dlg.Destroy()
        return choice

    @classmethod
    def showAskQuestionDialog(cls, parent, msg: str, title: str, default: str='')->str:
        """输入表单交互界面（无任何输入返回空字符串）"""
        dlg = wx.TextEntryDialog(parent, msg, title, default)
        enter = ''
        if dlg.ShowModal() == wx.ID_OK:
            enter = dlg.GetValue()
        dlg.Destroy()
        return enter

    @classmethod
    def showSafeMessage(cls, text: str, title: str):
        """安全弹出窗口"""
        wx.SafeShowMessage(title, text)

    @classmethod
    def showProgressDialog(cls, parent, msg, title, max: int=100):
        """显示进度信息"""
        dlg = wx.ProgressDialog(title,
            msg,
            maximum = max,
            parent=parent,
            style = 0
            | wx.PD_APP_MODAL
            | wx.PD_CAN_ABORT
            | wx.PD_ESTIMATED_TIME
            | wx.PD_REMAINING_TIME
            #| wx.PD_AUTO_HIDE | wx.PD_CAN_SKIP | wx.PD_ELAPSED_TIME
        )
        keepGoing, count = True, 0
        while keepGoing and count < max:
            count += 1
            wx.MilliSleep(250)
            wx.Yield()
            if count >= max / 2:
                (keepGoing, skip) = dlg.Update(count, "时间还剩一半!")
            else:
                (keepGoing, skip) = dlg.Update(count)
        dlg.Destroy()
