import wx.dataview as wxdv

class ShowAllPipsModel(wxdv.DataViewIndexListModel):
    def __init__(self, data):
        wxdv.DataViewIndexListModel.__init__(self, len(data))
        self.data = data

    def GetColumnType(self, col):
        """默认全部是字符串类型"""
        return "string"

    def GetValueByRow(self, row, col):
        """行列索引单个值"""
        return self.data[row][col]

    def SetValueByRow(self, value, row, col):
        """当用户编辑数据项的时候触发本函数"""
        self.data[row][col] = value
        return True

    def GetColumnCount(self):
        """列表页总的列数"""
        return len(self.data[0])

    def GetCount(self):
        """列表页总的行数"""
        return len(self.data)

    def GetAttrByRow(self, row, col, attr):
        """调用以检查是否应在（行、列）处的单元格中使用非标准属性"""
        if col == 3:
            attr.SetColour('blue')
            attr.SetBold(True)
            return True
        return False


    # This is called to assist with sorting the data in the view.  The
    # first two args are instances of the DataViewItem class, so we
    # need to convert them to row numbers with the GetRow method.
    # Then it's just a matter of fetching the right values from our
    # data set and comparing them.  The return value is -1, 0, or 1,
    # just like Python's cmp() function.
    def Compare(self, item1, item2, col, ascending):
        """比较排序"""
        if not ascending: # swap sort order?
            item2, item1 = item1, item2
        row1 = self.GetRow(item1)
        row2 = self.GetRow(item2)
        a = self.data[row1][col]
        b = self.data[row2][col]
        if col == 0:
            a = int(a)
            b = int(b)
        if a < b: return -1
        if a > b: return 1
        return 0

    def DeleteRows(self, rows):
        """删除行"""
        rows = sorted(rows, reverse=True)

        for row in rows:
            del self.data[row]
            self.RowDeleted(row) # 通知列表已删除


    def AddRow(self, value):
        """新增行"""
        self.data.append(value)
        self.RowAppended() # 通知视图
