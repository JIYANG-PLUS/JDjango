"""
    后期将添加的内容
"""

### 剪切板功能
#1 向剪切板写入数据
# if wx.TheClipboard.Open():
#       wx.TheClipboard.SetData(wx.TextDataObject("我是测试数据，喝牛奶女女"))
#       wx.TheClipboard.Close()

#2 判断内容是否可获取
# not_empty = wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_TEXT))

#3 从剪切板读取数据
# text_data = wx.TextDataObject()
# if wx.TheClipboard.Open():
#     success = wx.TheClipboard.GetData(text_data)
#     wx.TheClipboard.Close()
# if success:
#     return text_data.GetText()