from .common import *
import wx.stc as stc
import keyword

if wx.Platform == '__WXMSW__':
    faces = {
        'times': 'Times New Roman',
        'mono' : 'Courier New',
        'helv' : 'Arial',
        'other': 'Comic Sans MS',
        'size' : 10,
        'size2': 8,
    }
elif wx.Platform == '__WXMAC__':
    faces = {
        'times': 'Times New Roman',
        'mono' : 'Monaco',
        'helv' : 'Arial',
        'other': 'Comic Sans MS',
        'size' : 12,
        'size2': 10,
    }
else:
    faces = {
        'times': 'Times',
        'mono' : 'Courier',
        'helv' : 'Helvetica',
        'other': 'new century schoolbook',
        'size' : 12,
        'size2': 10,
    }

class PythonEditor(stc.StyledTextCtrl):
    def __init__(self, parent, ID=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        stc.StyledTextCtrl.__init__(self, parent, ID, pos, size, style)

        self.CmdKeyAssign(ord('B'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('N'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)
        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))
        self.SetProperty("fold", "1")
        self.SetProperty("tab.timmy.whinge.level", "1")
        self.SetMargins(0, 0)

        self.SetViewWhiteSpace(False)
        # self.SetBufferedDraw(False)
        # self.SetViewEOL(True)
        # self.SetEOLMode(stc.STC_EOL_CRLF)
        # self.SetUseAntiAliasing(True)

        self.SetEdgeMode(stc.STC_EDGE_BACKGROUND)
        self.SetEdgeColumn(78) # 78是较合理的列数，超出的列数会用文字阴影标记

        self._init_symbols_style(3)
        self._init_language_style()
        self._init_register()

    def _init_symbols_style(self, fold_symbols = 2):
        """初始化代码展开风格"""
        #self.SetFoldFlags(16) # 设置边距以容纳折叠标记
        # self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        # self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        # self.SetMarginSensitive(2, True)
        # self.SetMarginWidth(2, 12)
        self.SetMarginType(2, stc.STC_MARGIN_NUMBER) # 对每行进行数字标记
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 25)
        if fold_symbols == 0: # 向右箭头表示收缩的文件夹，向下箭头表示展开的文件夹
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_ARROWDOWN, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_ARROW, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_EMPTY, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_EMPTY, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")
        elif fold_symbols == 1: # 压缩文件夹加，扩展文件夹减
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_MINUS, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_PLUS,  "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")
        elif fold_symbols == 2: # 类似于使用圆形标头和曲线连接的展平树控件
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_CIRCLEMINUS, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_CIRCLEPLUS, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNERCURVE, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_CIRCLEPLUSCONNECTED, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_CIRCLEMINUSCONNECTED, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNERCURVE, "white", "#404040")
        elif fold_symbols == 3: # 就像一个使用方形标题的扁平树控件
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_BOXMINUS, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_BOXPLUS, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNER, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_BOXPLUSCONNECTED, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER, "white", "#808080")

    def _init_language_style(self):
        """初始化语言风格"""
        # 所有语言的全局默认样式
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % faces)
        self.StyleClearAll() # 全部重置为默认值
        # 所有语言的全局默认样式
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER, "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD, "fore:#000000,back:#FF0000,bold")
        # Python 界面语法风格
        self.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#000000,face:%(helv)s,size:%(size)d" % faces) # 默认值
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#007F00,face:%(other)s,size:%(size)d" % faces) # 注释
        self.StyleSetSpec(stc.STC_P_NUMBER, "fore:#007F7F,size:%(size)d" % faces) # 数值
        self.StyleSetSpec(stc.STC_P_STRING, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces) # 字符串
        self.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces) # 单引号字符串
        self.StyleSetSpec(stc.STC_P_WORD, "fore:#00007F,bold,size:%(size)d" % faces) # 关键词
        self.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % faces) # 三引号
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % faces) # 三双引号
        self.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % faces) # 类名定义
        self.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % faces) # 函数或方法名定义
        self.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces) # 运算符
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(helv)s,size:%(size)d" % faces) # 标识符
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % faces) # 注释块
        self.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces) # 字符串未闭合的行尾
        self.SetCaretForeground("BLUE")

    def _init_register(self):
        """初始化监听"""
        self.Bind(stc.EVT_STC_UPDATEUI, self.onUpdateUI)
        self.Bind(stc.EVT_STC_MARGINCLICK, self.onMarginClick)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyPressed)

    def onUpdateUI(self, evt):
        """界面更新时触发"""
        # 检查是否有匹配的大括号
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()
        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)

        # 检查之前
        if charBefore and chr(charBefore) in "[]{}()" and styleBefore == stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1

        # 检查之后
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)
            if charAfter and chr(charAfter) in "[]{}()" and styleAfter == stc.STC_P_OPERATOR:
                braceAtCaret = caretPos
        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)
        if braceAtCaret != -1  and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)
            # pt = self.PointFromPosition(braceOpposite)
            # self.Refresh(True, wxRect(pt.x, pt.y, 5,5))
            # print(pt)
            # self.Refresh(False)

    def onMarginClick(self, evt):
        """折叠或展开响应事件"""
        # 根据需要折叠和展开
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())

                if self.GetFoldLevel(lineClicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.Expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.Expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.Expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)

    def onKeyPressed(self, event):
        """按键按下时响应"""
        if self.CallTipActive(): self.CallTipCancel()
        key = event.GetKeyCode()
        
        if event.ControlDown(): # 按下Ctrl进行代码补全
            pos = self.GetCurrentPos()

            # 提示
            if event.ShiftDown():
                self.CallTipSetBackground("yellow") # 提示信息的背景图
                self.CallTipShow(pos, '函数的相关介绍')
            # 代码补全
            else:
                kw = keyword.kwlist[:] # Python 内置关键词列表
                kw.append("showMessage") # 将显示在提示信息列表中

                kw.sort() # Python排序区分大小写
                self.AutoCompSetIgnoreCase(False) # 不忽视大小写

                for i in range(len(kw)): # 附加"?type"表示图片类型
                    if kw[i] in keyword.kwlist:
                        kw[i] = kw[i] + "?1"

                self.AutoCompShow(0, " ".join(kw))
        else:
            event.Skip()

    def FoldAll(self):
        lineCount = self.GetLineCount()
        expanding = True

        for lineNum in range(lineCount): # 看看是在折叠还是展开
            if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break

        lineNum = 0
        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & stc.STC_FOLDLEVELHEADERFLAG and (level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:
                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)

                    if lastChild > lineNum:
                        self.HideLines(lineNum+1, lastChild)
            lineNum = lineNum + 1

    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        lastChild = self.GetLastChild(line, level)
        line = line + 1
        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)
            if level == -1:
                level = self.GetFoldLevel(line)
            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)
                    line = self.Expand(line, doExpand, force, visLevels-1)
                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.Expand(line, True, force, visLevels-1)
                    else:
                        line = self.Expand(line, False, force, visLevels-1)
            else:
                line = line + 1
        return line
