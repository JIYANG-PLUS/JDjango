import wx, json, glob, os, string
import wx.lib.buttons as buttons
from wx.lib import scrolledpanel
from .dialogTips import *
from ..tools._tools import *
from ..tools._re import *
from ..settings import BASE_DIR, CONFIG_PATH, SETTINGSS
from ..tools import environment as env
from ..tools import models as toolModel
from ..miniCmd.djangoCmd import *
from ..constant import *

"""
Mac上布局有BUG，推测是RadioBox和scrolledpanel组合使用的问题，Mac上勉强还能用，暂时不改。
"""

STATIC_TEXT_WIDTH = -1 # StaticText宽度

class ModelsCreateDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = '新增模型', size=(730, 888))

        # 必要的控制容器
        self.allArgs = [] # 所有的参数选项
        self.commonArgs = [] # 共有的参数选项
        self.specialArgs = [] # 特有的参数选项
        self.afterBtns = [] # 所有的后触发按钮
        self.allRows = [] # 所有的待新增按钮
        self.readmeStaticTexts = [] # 所有的脚注提示信息控件
        self.labelStaticTexts = [] # 所有的标签控件

        self._init_UI()
        self._disable_all_args()
        self._init_all_args_value()
        self._init_input_args()

        self._disable_all_afterBtns()

        # 按顺序布局面板
        self._init_table() # 表格布局默认加最后
        self._init_Meta_panel() # 初始化Meta选项面板

        # 字体默认设置
        self._init_readme_font()
        self._init_label_font()

    def _init_readme_font(self):
        """脚注提示信息字体初始化"""
        for _ in self.readmeStaticTexts:
            _.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            _.SetForegroundColour(CON_COLOR_BLUE)

    def _init_label_font(self):
        """标签提示信息字体初始化"""
        for _ in self.labelStaticTexts:
            _.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

    def _init_UI(self):
        """初始化界面布局"""
        # 主界面
        self.panel = wx.Panel(self)
        self.panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.panelSizer)
        # self.panel.SetBackgroundColour(CON_COLOR_MAIN)

        # 选择文件写入路径
        self.selectFilePanel = wx.Panel(self.panel)
        selectFilePanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.selectFilePanel.SetSizer(selectFilePanelSizer)
        self.panelSizer.Add(self.selectFilePanel, 0, wx.EXPAND | wx.ALL, 2)
        self.selectFilePanel.SetBackgroundColour(CON_COLOR_BLACK)

        self.btnSelectFile = buttons.GenButton(self.selectFilePanel, -1, '选择模型写入路径')
        self.inputSelectFile = wx.TextCtrl(self.selectFilePanel, -1, style=wx.ALIGN_LEFT)
        selectFilePanelSizer.Add(self.btnSelectFile, 0, wx.EXPAND | wx.ALL, 2)
        selectFilePanelSizer.Add(self.inputSelectFile, 1, wx.EXPAND | wx.ALL, 2)

        # 自定义工具栏
        self.toolPanel = wx.Panel(self.panel)
        toolPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.toolPanel.SetSizer(toolPanelSizer)
        self.panelSizer.Add(self.toolPanel, 0, wx.EXPAND | wx.ALL, 2)
        self.toolPanel.SetBackgroundColour(CON_COLOR_BLACK)

        self.btnAddNew = buttons.GenButton(self.toolPanel, -1, '新增字段')
        self.btnResetInput = buttons.GenButton(self.toolPanel, -1, '重置字段')
        self.btnAddFieldToArea = buttons.GenButton(self.toolPanel, -1, '添加至待新增区')
        # self.btnModifyFieldArgs = buttons.GenButton(self.toolPanel, -1, '修改')
        self.btnPreview = buttons.GenButton(self.toolPanel, -1, '代码预览')
        self.btnExecSave = buttons.GenButton(self.toolPanel, -1, '保存')
        self.btnExit = buttons.GenButton(self.toolPanel, -1, '退出')
        self.btnWhite = buttons.GenButton(self.toolPanel, -1, ' ') # 空白区域补全按钮
        toolPanelSizer.Add(self.btnAddNew, 0, wx.EXPAND | wx.ALL, 2)
        toolPanelSizer.Add(self.btnResetInput, 0, wx.EXPAND | wx.ALL, 2)
        toolPanelSizer.Add(self.btnAddFieldToArea, 0, wx.EXPAND | wx.ALL, 2)
        # toolPanelSizer.Add(self.btnModifyFieldArgs, 0, wx.EXPAND | wx.ALL, 2)
        toolPanelSizer.Add(self.btnPreview, 0, wx.EXPAND | wx.ALL, 2)
        toolPanelSizer.Add(self.btnExecSave, 0, wx.EXPAND | wx.ALL, 2)
        toolPanelSizer.Add(self.btnExit, 0, wx.EXPAND | wx.ALL, 2)
        toolPanelSizer.Add(self.btnWhite, 1, wx.EXPAND | wx.ALL, 2)
        self.btnWhite.Enable(False)

        # 选择字段类型【行冻结】
        self.selectFieldTypeStaticBox = wx.StaticBox(self.panel, -1, '')
        self.selectFieldTypePanel = wx.StaticBoxSizer(self.selectFieldTypeStaticBox, wx.HORIZONTAL)
        self.panelSizer.Add(self.selectFieldTypePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.choiceFieldTypeLabel = wx.StaticText(self.panel, -1, "1、字段类型：")
        self.choiceFieldType = wx.Choice(self.panel, -1, choices = [' ']+CON_FIELD_TYPES) # , style = wx.CB_SORT
        self.readmeChoiceFieldType = wx.StaticText(self.panel, -1, "【字段类型】** 新增字段前，必须先选择字段类型，选择后即可填写详细的参数数据。") # 选项说明
        self.selectFieldTypePanel.Add(self.choiceFieldTypeLabel, 0, wx.EXPAND | wx.ALL, 2)
        self.selectFieldTypePanel.Add(self.choiceFieldType, 1, wx.EXPAND | wx.ALL, 2)
        self.panelSizer.Add(self.readmeChoiceFieldType, 0, wx.EXPAND | wx.ALL, 2)

        # 可滚动面板（包裹所有的参数）
        self.scollPanel = scrolledpanel.ScrolledPanel(self.panel, -1)
        self.scollPanel.SetupScrolling()
        scollPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.scollPanel.SetSizer(scollPanelSizer)
        self.panelSizer.Add(self.scollPanel, 3, wx.EXPAND | wx.ALL, 2)

        # 字段属性命名
        self.modelsNameStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.modelsNamePanel = wx.StaticBoxSizer(self.modelsNameStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.modelsNamePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelFieldModelName = wx.StaticText(self.scollPanel, -1, "2、字段属性名：")
        self.inputFieldModelName = wx.TextCtrl(self.scollPanel, -1)
        self.readmeInputFieldModelName = wx.StaticText(self.scollPanel, -1, "【字段属性名】** 字段属性名，是代码中的字段名称，并非数据库中实际存储的列名。")
        self.modelsNamePanel.Add(self.labelFieldModelName, 0, wx.EXPAND | wx.ALL, 2)
        self.modelsNamePanel.Add(self.inputFieldModelName, 1, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeInputFieldModelName, 0, wx.EXPAND | wx.ALL, 2)

        # 数据库列名（db_column）
        self.dbColumnNameStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.dbColumnNamePanel = wx.StaticBoxSizer(self.dbColumnNameStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.dbColumnNamePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelFieldDatabaseName = wx.StaticText(self.scollPanel, -1, "3、数据库列名（db_column）：")
        self.inputFieldDatabaseName = wx.TextCtrl(self.scollPanel, -1)
        self.readmeInputFieldDatabaseName = wx.StaticText(self.scollPanel, -1, "【数据库列名（db_column）】** 实际存储在数据库中的列名，若不指定默认取【字段属性名】。")
        self.dbColumnNamePanel.Add(self.labelFieldDatabaseName, 0, wx.EXPAND | wx.ALL, 2)
        self.dbColumnNamePanel.Add(self.inputFieldDatabaseName, 1, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeInputFieldDatabaseName, 0, wx.EXPAND | wx.ALL, 2)


        # 字段备注
        self.fieldRemarkStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.fieldRemarkPanel = wx.StaticBoxSizer(self.fieldRemarkStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.fieldRemarkPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelFieldRemarkName = wx.StaticText(self.scollPanel, -1, "4、字段备注：", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.inputFieldRemarkName = wx.TextCtrl(self.scollPanel, -1)
        self.readmeInputFieldRemarkName = wx.StaticText(self.scollPanel, -1, "【字段备注】** 字段备注默认取【字段属性名】，下划线将自动转换成空格。")
        self.fieldRemarkPanel.Add(self.labelFieldRemarkName, 0, wx.EXPAND | wx.ALL, 2)
        self.fieldRemarkPanel.Add(self.inputFieldRemarkName, 1, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeInputFieldRemarkName, 0, wx.EXPAND | wx.ALL, 2)

        # 主键（primary_key）
        self.radiosFiledPrimaryStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.radiosFiledPrimaryPanel = wx.StaticBoxSizer(self.radiosFiledPrimaryStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.radiosFiledPrimaryPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelRadiosFiledPrimary = wx.StaticText(self.scollPanel, -1, "5、主键（primary_key）：", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.radiosFiledPrimary = wx.RadioBox(self.scollPanel, -1, "", choices=['是', '否'])
        self.readmeRadiosFiledPrimary = wx.StaticText(self.scollPanel, -1, "【主键（primary_key）】** 数据库主键唯一字段。")
        self.radiosFiledPrimaryPanel.Add(self.labelRadiosFiledPrimary, 0, wx.EXPAND | wx.ALL, 2)
        self.radiosFiledPrimaryPanel.Add(self.radiosFiledPrimary, 0, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeRadiosFiledPrimary, 0, wx.EXPAND | wx.ALL, 2)

        # 值唯一（unique）
        self.radiosFiledUniqueStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.radiosFiledUniquePanel = wx.StaticBoxSizer(self.radiosFiledUniqueStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.radiosFiledUniquePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelRadiosFiledUnique = wx.StaticText(self.scollPanel, -1, "6、值唯一（unique）：", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.radiosFiledUnique = wx.RadioBox(self.scollPanel, -1, "", choices=['唯一', '不唯一'])
        self.readmeRadiosFiledUnique = wx.StaticText(self.scollPanel, -1, "【值唯一（unique）】** 数据库字段值唯一。")
        self.radiosFiledUniquePanel.Add(self.labelRadiosFiledUnique, 0, wx.EXPAND | wx.ALL, 2)
        self.radiosFiledUniquePanel.Add(self.radiosFiledUnique, 0, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeRadiosFiledUnique, 0, wx.EXPAND | wx.ALL, 2)

        # 允许为空、blank
        self.radiosFiledBlankStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.radiosFiledBlankPanel = wx.StaticBoxSizer(self.radiosFiledBlankStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.radiosFiledBlankPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelRadiosFiledBlank = wx.StaticText(self.scollPanel, -1, "7、允许为空（blank）：", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        # self.radiosFiledBlank = wx.RadioBox(self.scollPanel, -1, "", choices=['允许', '不允许'])
        self.radiosFiledBlankY = wx.RadioButton(panel, -1, '允许', style=wx.RB_GROUP)
        self.radiosFiledBlankN = wx.RadioButton(panel, -1, '不允许', style=wx.RB_GROUP)
        # rb2 = event.GetEventObject()
        # print('二选择{0}'.format(rb2.GetLabel()))
        self.readmeRadiosFiledBlank = wx.StaticText(self.scollPanel, -1, "【允许为空（blank）】** 数据库表字段允许为空，表单验证允许为空。")
        self.radiosFiledBlankPanel.Add(self.labelRadiosFiledBlank, 0, wx.EXPAND | wx.ALL, 2)
        self.radiosFiledBlankPanel.Add(self.radiosFiledBlankY, 0, wx.EXPAND | wx.ALL, 2)
        self.radiosFiledBlankPanel.Add(self.radiosFiledBlankN, 0, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeRadiosFiledBlank, 0, wx.EXPAND | wx.ALL, 2)

        # 默认值（default）
        self.inputDefaultValueStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.inputDefaultValuePanel = wx.StaticBoxSizer(self.inputDefaultValueStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.inputDefaultValuePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputDefaultValue = wx.StaticText(self.scollPanel, -1, "8、默认值（default）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.inputDefaultValue = wx.TextCtrl(self.scollPanel, -1)
        self.readmeInputDefaultValue = wx.StaticText(self.scollPanel, -1, "【默认值（default）】** 字段默认值，可以是常量，也可以是一个函数。")
        self.inputDefaultValuePanel.Add(self.labelInputDefaultValue, 0, wx.EXPAND | wx.ALL, 2)
        self.inputDefaultValuePanel.Add(self.inputDefaultValue, 1, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeInputDefaultValue, 0, wx.EXPAND | wx.ALL, 2)

        # 为空时赋NULL（null）
        self.radiosFiledNullStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.radiosFiledNullPanel = wx.StaticBoxSizer(self.radiosFiledNullStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.radiosFiledNullPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelRadiosFiledNull = wx.StaticText(self.scollPanel, -1, "9、为空时赋NULL（null）：", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.radiosFiledNull = wx.RadioBox(self.scollPanel, -1, "", choices=['赋', '不赋'])
        self.readmeRadiosFiledNull = wx.StaticText(self.scollPanel, -1, "【为空时赋NULL（null）】** 数据库表字段为空时，用NULL作默认值。")
        self.radiosFiledNullPanel.Add(self.labelRadiosFiledNull, 0, wx.EXPAND | wx.ALL, 2)
        self.radiosFiledNullPanel.Add(self.radiosFiledNull, 0, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeRadiosFiledNull, 0, wx.EXPAND | wx.ALL, 2)

        # 创建索引（db_index）
        self.radiosFiledDbIndexStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.radiosFiledDbIndexPanel = wx.StaticBoxSizer(self.radiosFiledDbIndexStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.radiosFiledDbIndexPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelRadiosFiledDbIndex = wx.StaticText(self.scollPanel, -1, "10、创建索引（db_index）：", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.radiosFiledDbIndex = wx.RadioBox(self.scollPanel, -1, "", choices=['创建', '不创建'])
        self.readmeRadiosFiledDbIndex = wx.StaticText(self.scollPanel, -1, "【创建索引（db_index）】** 创建数据库的字段索引。")
        self.radiosFiledDbIndexPanel.Add(self.labelRadiosFiledDbIndex, 0, wx.EXPAND | wx.ALL, 2)
        self.radiosFiledDbIndexPanel.Add(self.radiosFiledDbIndex, 0, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeRadiosFiledDbIndex, 0, wx.EXPAND | wx.ALL, 2)

        # 与日期组合唯一（unique_for_date）
        self.choicesFiledUniqueForDateStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.choicesFiledUniqueForDatePanel = wx.StaticBoxSizer(self.choicesFiledUniqueForDateStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.choicesFiledUniqueForDatePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelChoicesFiledUniqueForDate = wx.StaticText(self.scollPanel, -1, "11、与日期组合唯一（unique_for_date）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.choicesFiledUniqueForDate = wx.Choice(self.scollPanel, -1, choices=[' ',])
        self.readmeChoicesFiledUniqueForDate = wx.StaticText(self.scollPanel, -1, "【与日期组合唯一（unique_for_date）】** 当前字段与当前选择日期字段的值组合唯一。")
        self.choicesFiledUniqueForDatePanel.Add(self.labelChoicesFiledUniqueForDate, 0, wx.EXPAND | wx.ALL, 2)
        self.choicesFiledUniqueForDatePanel.Add(self.choicesFiledUniqueForDate, 1, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeChoicesFiledUniqueForDate, 0, wx.EXPAND | wx.ALL, 2)

        # 与月份组合唯一（unique_for_month）
        self.choicesFiledUniqueForMonthStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.choicesFiledUniqueForMonthPanel = wx.StaticBoxSizer(self.choicesFiledUniqueForMonthStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.choicesFiledUniqueForMonthPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelChoicesFiledUniqueForMonth = wx.StaticText(self.scollPanel, -1, "12、与月份组合唯一（unique_for_month）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.choicesFiledUniqueForMonth = wx.Choice(self.scollPanel, -1, choices=[' ',])
        self.readmeChoicesFiledUniqueForMonth = wx.StaticText(self.scollPanel, -1, "【与月份组合唯一（unique_for_month）】** 当前字段与当前选择月份字段的值组合唯一。")
        self.choicesFiledUniqueForMonthPanel.Add(self.labelChoicesFiledUniqueForMonth, 0, wx.EXPAND | wx.ALL, 2)
        self.choicesFiledUniqueForMonthPanel.Add(self.choicesFiledUniqueForMonth, 1, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeChoicesFiledUniqueForMonth, 0, wx.EXPAND | wx.ALL, 2)

        # 与年份组合唯一（unique_for_year）
        self.choicesFiledUniqueForYearStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.choicesFiledUniqueForYearPanel = wx.StaticBoxSizer(self.choicesFiledUniqueForYearStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.choicesFiledUniqueForYearPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelChoicesFiledUniqueForYear = wx.StaticText(self.scollPanel, -1, "13、与年份组合唯一（unique_for_year）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.choicesFiledUniqueForYear = wx.Choice(self.scollPanel, -1, choices=[' ',])
        self.readmeChoicesFiledUniqueForYear = wx.StaticText(self.scollPanel, -1, "【与年份组合唯一（unique_for_year）】** 当前字段与当前选择年份字段的值组合唯一。")
        self.choicesFiledUniqueForYearPanel.Add(self.labelChoicesFiledUniqueForYear, 0, wx.EXPAND | wx.ALL, 2)
        self.choicesFiledUniqueForYearPanel.Add(self.choicesFiledUniqueForYear, 1, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeChoicesFiledUniqueForYear, 0, wx.EXPAND | wx.ALL, 2)

        # 表单显示（editable）
        self.radiosFiledEditableStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.radiosFiledEditablePanel = wx.StaticBoxSizer(self.radiosFiledEditableStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.radiosFiledEditablePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelRadiosFiledEditable = wx.StaticText(self.scollPanel, -1, "14、表单显示（editable）：", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.radiosFiledEditable = wx.RadioBox(self.scollPanel, -1, "", choices=['显示', '不显示'])
        self.readmeRadiosFiledEditable = wx.StaticText(self.scollPanel, -1, "【表单显示（editable）】** 表单页面提供交互式控件。")
        self.radiosFiledEditablePanel.Add(self.labelRadiosFiledEditable, 0, wx.EXPAND | wx.ALL, 2)
        self.radiosFiledEditablePanel.Add(self.radiosFiledEditable, 0, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeRadiosFiledEditable, 0, wx.EXPAND | wx.ALL, 2)

        # 表单帮助文本信息（help_text）
        self.inputFormHelpTextStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.inputFormHelpTextPanel = wx.StaticBoxSizer(self.inputFormHelpTextStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.inputFormHelpTextPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputFormHelpText = wx.StaticText(self.scollPanel, -1, "15、表单帮助信息（help_text）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.inputFormHelpText = wx.TextCtrl(self.scollPanel, -1)
        self.readmeInputFormHelpText = wx.StaticText(self.scollPanel, -1, "【表单帮助信息（help_text）】** 表单填写时的提示信息。")
        self.inputFormHelpTextPanel.Add(self.labelInputFormHelpText, 0, wx.EXPAND | wx.ALL, 2)
        self.inputFormHelpTextPanel.Add(self.inputFormHelpText, 1, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeInputFormHelpText, 0, wx.EXPAND | wx.ALL, 2)

        # 表单错误提醒（error_messages）
        self.inputFormErrorMessageStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.inputFormErrorMessagePanel = wx.StaticBoxSizer(self.inputFormErrorMessageStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.inputFormErrorMessagePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputFormErrorMessage = wx.StaticText(self.scollPanel, -1, "16、表单错误提醒（error_messages）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.inputFormErrorMessage = wx.TextCtrl(self.scollPanel, -1)
        self.readmeInputFormErrorMessage = wx.StaticText(self.scollPanel, -1, "【表单错误提醒（error_messages）】** 表单填写错误时的提示信息。")
        self.inputFormErrorMessagePanel.Add(self.labelInputFormErrorMessage, 0, wx.EXPAND | wx.ALL, 2)
        self.inputFormErrorMessagePanel.Add(self.inputFormErrorMessage, 1, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeInputFormErrorMessage, 0, wx.EXPAND | wx.ALL, 2)

        # 长度上限（max_length）
        self.inputMaxLengthStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.inputMaxLengthPanel = wx.StaticBoxSizer(self.inputMaxLengthStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.inputMaxLengthPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputMaxLength = wx.StaticText(self.scollPanel, -1, "17、长度上限（max_length）：", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.inputMaxLength = wx.TextCtrl(self.scollPanel, -1)
        self.readmeInputMaxLength = wx.StaticText(self.scollPanel, -1, "【长度上限（max_length）】** 数据库允许存储的最大长度。")
        self.inputMaxLengthPanel.Add(self.labelInputMaxLength, 0, wx.EXPAND | wx.ALL, 2)
        self.inputMaxLengthPanel.Add(self.inputMaxLength, 1, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeInputMaxLength, 0, wx.EXPAND | wx.ALL, 2)

        # 实数总位数（max_digits）
        self.inputMaxDigitsStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.inputMaxDigitsPanel = wx.StaticBoxSizer(self.inputMaxDigitsStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.inputMaxDigitsPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputMaxDigits = wx.StaticText(self.scollPanel, -1, "18、实数总位数（max_digits）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.inputMaxDigits = wx.TextCtrl(self.scollPanel, -1)
        self.readmeInputMaxDigits = wx.StaticText(self.scollPanel, -1, "【实数总位数（max_digits）】** 整数位数和小数位数的总和，不包括小数点。")
        self.inputMaxDigitsPanel.Add(self.labelInputMaxDigits, 0, wx.EXPAND | wx.ALL, 2)
        self.inputMaxDigitsPanel.Add(self.inputMaxDigits, 1, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeInputMaxDigits, 0, wx.EXPAND | wx.ALL, 2)

        # 小数总位数（decimal_places）（默认为0）
        self.inputDecimalPlacesStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.inputDecimalPlacesPanel = wx.StaticBoxSizer(self.inputDecimalPlacesStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.inputDecimalPlacesPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputDecimalPlaces = wx.StaticText(self.scollPanel, -1, "19、小数总位数（decimal_places）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.inputDecimalPlaces = wx.TextCtrl(self.scollPanel, -1)
        self.readmeInputDecimalPlaces = wx.StaticText(self.scollPanel, -1, "【小数总位数（decimal_places）】** 小数位数的总和，不包括小数点。")
        self.inputDecimalPlacesPanel.Add(self.labelInputDecimalPlaces, 0, wx.EXPAND | wx.ALL, 2)
        self.inputDecimalPlacesPanel.Add(self.inputDecimalPlaces, 1, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeInputDecimalPlaces, 0, wx.EXPAND | wx.ALL, 2)

        # save调用更新日期（auto_now）
        self.radiosAutoNowStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.radiosAutoNowPanel = wx.StaticBoxSizer(self.radiosAutoNowStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.radiosAutoNowPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelRadiosAutoNow = wx.StaticText(self.scollPanel, -1, "20、保存更新日期（auto_now）：", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.radiosAutoNow = wx.RadioBox(self.scollPanel, -1, "", choices=['启用', '不启用'])
        self.readmeRadiosAutoNow = wx.StaticText(self.scollPanel, -1, "【保存更新日期（auto_now）】** 仅在调用模型控制器的save()方法时自动更新该日期字段。")
        self.radiosAutoNowPanel.Add(self.labelRadiosAutoNow, 0, wx.EXPAND | wx.ALL, 2)
        self.radiosAutoNowPanel.Add(self.radiosAutoNow, 0, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeRadiosAutoNow, 0, wx.EXPAND | wx.ALL, 2)

        # 仅创建时一次赋值日期（auto_now_add）
        self.radiosAutoNowAddStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.radiosAutoNowAddPanel = wx.StaticBoxSizer(self.radiosAutoNowAddStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.radiosAutoNowAddPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelRadiosAutoNowAdd = wx.StaticText(self.scollPanel, -1, "21、创建赋值日期（auto_now_add）：", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.radiosAutoNowAdd = wx.RadioBox(self.scollPanel, -1, "", choices=['启用', '不启用'])
        self.readmeRadiosAutoNowAdd = wx.StaticText(self.scollPanel, -1, "【创建赋值日期（auto_now_add）】** 仅在创建记录时一次赋值该日期，赋值后不允许修改。")
        self.radiosAutoNowAddPanel.Add(self.labelRadiosAutoNowAdd, 0, wx.EXPAND | wx.ALL, 2)
        self.radiosAutoNowAddPanel.Add(self.radiosAutoNowAdd, 0, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeRadiosAutoNowAdd, 0, wx.EXPAND | wx.ALL, 2)

        # 文件上传路径（upload_to）
        self.inputUploadToStaticBox = wx.StaticBox(self.scollPanel, -1, '')
        self.inputUploadToPanel = wx.StaticBoxSizer(self.inputUploadToStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.inputUploadToPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputUploadTo = wx.StaticText(self.scollPanel, -1, "22、文件上传路径（upload_to）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.inputUploadTo = wx.TextCtrl(self.scollPanel, -1)
        self.readmeInputUploadTo = wx.StaticText(self.scollPanel, -1, "【文件上传路径（upload_to）】** 指定文件上传路径。")
        self.inputUploadToPanel.Add(self.labelInputUploadTo, 0, wx.EXPAND | wx.ALL, 2)
        self.inputUploadToPanel.Add(self.inputUploadTo, 1, wx.EXPAND | wx.ALL, 2)
        scollPanelSizer.Add(self.readmeInputUploadTo, 0, wx.EXPAND | wx.ALL, 2)
        
        # 关联关系字段布局1
        self.relationFiledStaticBox = wx.StaticBox(self.scollPanel, -1, '关联关系字段专属参数')
        self.relationFiledPanel = wx.StaticBoxSizer(self.relationFiledStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.relationFiledPanel, 1, wx.EXPAND | wx.ALL, 2)

        # 关联关系字段布局1 - 模型下拉列表选择
        self.relationFiledChoiceModelStaticBox = wx.StaticBox(self.scollPanel, -1, '关联模型')
        self.relationFiledChoiceModelPanel = wx.StaticBoxSizer(self.relationFiledChoiceModelStaticBox, wx.HORIZONTAL)
        self.relationFiledPanel.Add(self.relationFiledChoiceModelPanel, 1, wx.EXPAND | wx.ALL, 2)

        self.choiceSelectModel = wx.Choice(self.scollPanel, -1, choices = [' ']+['self'])
        self.relationFiledChoiceModelPanel.Add(self.choiceSelectModel, 1, wx.EXPAND | wx.ALL, 2)

        # 关联关系字段布局1 - 记录删除规则【on_delete】
        self.relationFiledDelRuleStaticBox = wx.StaticBox(self.scollPanel, -1, '记录删除规则【on_delete】')
        self.relationFiledDelRulePanel = wx.StaticBoxSizer(self.relationFiledDelRuleStaticBox, wx.HORIZONTAL)
        self.relationFiledPanel.Add(self.relationFiledDelRulePanel, 1, wx.EXPAND | wx.ALL, 2)

        self.choiceSelectDelRule = wx.Choice(self.scollPanel, -1, choices = [' ']+['models.CASCADE'])
        self.relationFiledDelRulePanel.Add(self.choiceSelectDelRule, 1, wx.EXPAND | wx.ALL, 2)

        # 关联关系字段布局1 - 备注名【verbose_name】
        self.relationFiledRemarkStaticBox = wx.StaticBox(self.scollPanel, -1, '关联字段备注名【verbose_name】')
        self.relationFiledRemarkPanel = wx.StaticBoxSizer(self.relationFiledRemarkStaticBox, wx.HORIZONTAL)
        self.relationFiledPanel.Add(self.relationFiledRemarkPanel, 1, wx.EXPAND | wx.ALL, 2)

        self.inputRelationRemark = wx.TextCtrl(self.scollPanel, -1)
        self.relationFiledRemarkPanel.Add(self.inputRelationRemark, 1, wx.EXPAND | wx.ALL, 2)

        self.afterBtns.extend([
            self.btnResetInput, self.btnAddFieldToArea,
            # self.btnExecSave,
        ])

        # 所有的参数
        self.allArgs.extend([
            self.choiceFieldType, # 字段类型选择放这里不合理【暂时不调整】
            self.inputFieldModelName, self.inputFieldDatabaseName, self.inputFieldRemarkName,
            self.radiosFiledBlankY,self.radiosFiledBlankN,
            self.radiosFiledNull, self.radiosFiledPrimary, # 英文拼错了，不改了
            self.radiosFiledUnique, self.radiosFiledDbIndex, self.radiosFiledEditable,
            self.choicesFiledUniqueForDate, self.choicesFiledUniqueForMonth, self.choicesFiledUniqueForYear,
            self.inputDefaultValue, self.inputFormHelpText, self.inputFormErrorMessage,
            self.inputMaxLength, self.inputMaxDigits, self.inputDecimalPlaces,
            self.radiosAutoNow, self.radiosAutoNowAdd, self.inputUploadTo,
            self.choiceSelectModel, self.choiceSelectDelRule, self.inputRelationRemark,
        ])

        # 共用参数
        self.commonArgs.extend([
            self.inputFieldModelName, self.inputFieldDatabaseName, self.inputFieldRemarkName,
            self.radiosFiledBlankY,self.radiosFiledBlankN,
            self.radiosFiledNull, self.radiosFiledPrimary,
            self.radiosFiledUnique, self.radiosFiledDbIndex, self.radiosFiledEditable,
            self.choicesFiledUniqueForDate, self.choicesFiledUniqueForMonth, self.choicesFiledUniqueForYear,
            self.inputDefaultValue, self.inputFormHelpText, self.inputFormErrorMessage,
        ])

        # 私有参数
        self.specialArgs.extend([
            self.inputMaxLengthStaticBox, self.inputMaxLength, self.labelInputMaxLength, self.readmeInputMaxLength,
            self.inputMaxDigitsStaticBox, self.inputMaxDigits, self.labelInputMaxDigits, self.readmeInputMaxDigits,
            self.inputDecimalPlacesStaticBox, self.inputDecimalPlaces, self.labelInputDecimalPlaces, self.readmeInputDecimalPlaces,
            self.radiosAutoNowStaticBox, self.radiosAutoNow, self.labelRadiosAutoNow, self.readmeRadiosAutoNow,
            self.radiosAutoNowAddStaticBox, self.radiosAutoNowAdd, self.labelRadiosAutoNowAdd, self.readmeRadiosAutoNowAdd,
            self.inputUploadToStaticBox, self.inputUploadTo, self.labelInputUploadTo, self.readmeInputUploadTo,

            # 关联字段专属
            self.relationFiledStaticBox,
            self.relationFiledChoiceModelStaticBox, self.choiceSelectModel,
            self.relationFiledDelRuleStaticBox, self.choiceSelectDelRule,
            self.relationFiledRemarkStaticBox, self.inputRelationRemark,

        ])

        # 字体初始化控件录入
        self.readmeStaticTexts.extend([
            self.readmeChoiceFieldType,self.readmeInputFieldModelName,
            self.readmeInputFieldDatabaseName,self.readmeInputFieldRemarkName,
            self.readmeRadiosFiledBlank,self.readmeRadiosFiledNull,
            self.readmeRadiosFiledPrimary,self.readmeRadiosFiledUnique,
            self.readmeRadiosFiledDbIndex,self.readmeRadiosFiledEditable,
            self.readmeInputMaxLength,self.readmeRadiosAutoNow,
            self.readmeRadiosAutoNowAdd,self.readmeInputDefaultValue,
            self.readmeInputFormHelpText,self.readmeInputFormErrorMessage,
            self.readmeInputUploadTo,self.readmeInputMaxDigits,
            self.readmeInputDecimalPlaces,self.readmeChoicesFiledUniqueForDate,
            self.readmeChoicesFiledUniqueForMonth,self.readmeChoicesFiledUniqueForYear,
        ])
        self.labelStaticTexts.extend([
            self.choiceFieldTypeLabel,self.labelFieldModelName,
            self.labelFieldDatabaseName,self.labelFieldRemarkName,
            self.labelRadiosFiledBlank,self.labelRadiosFiledNull,
            self.labelRadiosFiledPrimary,self.labelRadiosFiledUnique,
            self.labelRadiosFiledDbIndex,self.labelRadiosFiledEditable,
            self.labelInputMaxLength,self.labelRadiosAutoNow,
            self.labelRadiosAutoNowAdd,self.labelInputDefaultValue,
            self.labelInputFormHelpText,self.labelInputFormErrorMessage,
            self.labelInputUploadTo,self.labelInputMaxDigits,
            self.labelInputDecimalPlaces,self.labelChoicesFiledUniqueForDate,
            self.labelChoicesFiledUniqueForMonth,self.labelChoicesFiledUniqueForYear,
        ])

        # 按钮点击事件
        self.Bind(wx.EVT_BUTTON, self.onBtnSelectPath, self.btnSelectFile)
        self.Bind(wx.EVT_BUTTON, self.onExit, self.btnExit)
        self.Bind(wx.EVT_BUTTON, self.onBtnAddNew, self.btnAddNew)
        self.Bind(wx.EVT_BUTTON, self.onBtnResetInput, self.btnResetInput)
        self.Bind(wx.EVT_BUTTON, self.onBtnAddFieldToArea, self.btnAddFieldToArea)
        self.Bind(wx.EVT_BUTTON, self.onBtnExecSave, self.btnExecSave)
        self.Bind(wx.EVT_BUTTON, self.onBtnPreview, self.btnPreview)
        # 下拉框选择事件
        self.Bind(wx.EVT_CHOICE, self.onChoiceFieldType, self.choiceFieldType)
        # 文本实时监听事件
        self.Bind(wx.EVT_TEXT, self.onInputFieldModelName, self.inputFieldModelName)
        self.Bind(wx.EVT_TEXT, self.onInputMaxLength, self.inputMaxLength)
        self.Bind(wx.EVT_TEXT, self.onInputMaxDigits, self.inputMaxDigits)
        self.Bind(wx.EVT_TEXT, self.onInputDecimalPlaces, self.inputDecimalPlaces)
        # 单选框事件
        self.Bind(wx.EVT_RADIOBOX, self.onRadioChanged, self.radiosFiledBlank)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioChanged, self.radiosFiledNull)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioChanged, self.radiosFiledPrimary)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioChanged, self.radiosFiledUnique)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioChanged, self.radiosFiledDbIndex)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioChanged, self.radiosFiledEditable)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioChanged, self.radiosAutoNow)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioChanged, self.radiosAutoNowAdd)

    def _init_Meta_panel(self):
        """初始化Meta选项面板"""
        # 显示和隐藏Meta按钮，用于空间的合理布局
        self.btnShowUnshowMeta = buttons.GenButton(self.panel, -1, '【显示】Meta元数据')
        self.panelSizer.Add(self.btnShowUnshowMeta, 0, wx.EXPAND | wx.ALL, 2)
        self.btnShowUnshowMeta.SetBackgroundColour(CON_COLOR_BLUE)
        self.btnShowUnshowMeta.SetForegroundColour(CON_COLOR_WHITE)

        self.metaScollPanel = scrolledpanel.ScrolledPanel(self.panel, -1, size=(730,444))
        self.metaScollPanel.SetupScrolling()
        metaScollPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.metaScollPanel.SetSizer(metaScollPanelSizer)
        self.panelSizer.Add(self.metaScollPanel, 0, wx.EXPAND | wx.ALL, 2)

        # Meta的各种选项
        # 抽象类（abstract）
        self.metaAbstractOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaAbstractOptionPanel = wx.StaticBoxSizer(self.metaAbstractOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaAbstractOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaAbstractOption = wx.StaticText(self.metaScollPanel, -1, "1、抽象类（abstract）：", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaAbstractOption = wx.RadioBox(self.metaScollPanel, -1, "", choices=['是', '否'])
        self.readmeMetaAbstractOption = wx.StaticText(self.metaScollPanel, -1, " ** 该模型声明为抽象模型后，不会在数据库中建表。")
        self.metaAbstractOptionPanel.Add(self.labelMetaAbstractOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaAbstractOptionPanel.Add(self.metaAbstractOption, 0, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaAbstractOption, 0, wx.EXPAND | wx.ALL, 2)

        # 模型归属应用程序（app_label）
        # 可以用model._meta.label或model._meta.label_lower获取模型名称
        self.metaAppLabelOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaAppLabelOptionPanel = wx.StaticBoxSizer(self.metaAppLabelOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaAppLabelOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaAppLabelOption = wx.StaticText(self.metaScollPanel, -1, "2、模型归属应用程序（app_label）：", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaAppLabelOption = wx.Choice(self.metaScollPanel, -1, choices=[' ',]+get_configs(CONFIG_PATH)['app_names'])
        self.readmeMetaAppLabelOption = wx.StaticText(self.metaScollPanel, -1, " ** 不指定，则默认归属于当前模型文件所在的应用程序。")
        self.metaAppLabelOptionPanel.Add(self.labelMetaAppLabelOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaAppLabelOptionPanel.Add(self.metaAppLabelOption, 1, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaAppLabelOption, 0, wx.EXPAND | wx.ALL, 2)

        # 模型管理器名称（base_manager_name）
        self.metaObjectsOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaObjectsOptionPanel = wx.StaticBoxSizer(self.metaObjectsOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaObjectsOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaObjectsOption = wx.StaticText(self.metaScollPanel, -1, "3、模型管理器名称（base_manager_name）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaObjectsOption = wx.TextCtrl(self.metaScollPanel, -1)
        self.readmeMetaObjectsOption = wx.StaticText(self.metaScollPanel, -1, " ** 默认为objects。可用model.objects调出管理器。")
        self.metaObjectsOptionPanel.Add(self.labelMetaObjectsOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaObjectsOptionPanel.Add(self.metaObjectsOption, 1, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaObjectsOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaObjectsOption.SetValue('objects')

        # 数据表名（db_table）
        # 在mysql中均小写，Oracle中数据库表名要用双引号括起来
        self.metaDBTableOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaDBTableOptionPanel = wx.StaticBoxSizer(self.metaDBTableOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaDBTableOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaDBTableOption = wx.StaticText(self.metaScollPanel, -1, "4、数据表名（db_table）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaDBTableOption = wx.TextCtrl(self.metaScollPanel, -1)
        self.readmeMetaDBTableOption = wx.StaticText(self.metaScollPanel, -1, " ** 默认为应用程序名+模型名，全小写。如：app_model。")
        self.metaDBTableOptionPanel.Add(self.labelMetaDBTableOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaDBTableOptionPanel.Add(self.metaDBTableOption, 1, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaDBTableOption, 0, wx.EXPAND | wx.ALL, 2)

        # 表空间名（db_tablespace）
        self.metaDBTableSpaceOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaDBTableSpaceOptionPanel = wx.StaticBoxSizer(self.metaDBTableSpaceOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaDBTableSpaceOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaDBTableSpaceOption = wx.StaticText(self.metaScollPanel, -1, "5、表空间名（db_tablespace）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaDBTableSpaceOption = wx.TextCtrl(self.metaScollPanel, -1)
        self.readmeMetaDBTableSpaceOption = wx.StaticText(self.metaScollPanel, -1, " ** 默认使用settings.py中的DEFAULT_TABLESPACE值。")
        self.metaDBTableSpaceOptionPanel.Add(self.labelMetaDBTableSpaceOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaDBTableSpaceOptionPanel.Add(self.metaDBTableSpaceOption, 1, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaDBTableSpaceOption, 0, wx.EXPAND | wx.ALL, 2)

        # 指定默认解析管理器（default_manager_name）
        self.metaDefaultManagerNameOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaDefaultManagerNameOptionPanel = wx.StaticBoxSizer(self.metaDefaultManagerNameOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaDefaultManagerNameOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaDefaultManagerNameOption = wx.StaticText(self.metaScollPanel, -1, "6、指定默认解析管理器（default_manager_name）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaDefaultManagerNameOption = wx.TextCtrl(self.metaScollPanel, -1)
        self.readmeMetaDefaultManagerNameOption = wx.StaticText(self.metaScollPanel, -1, " ** 用于Django的默认行为，防止数据集缺失导致的错误。")
        self.metaDefaultManagerNameOptionPanel.Add(self.labelMetaDefaultManagerNameOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaDefaultManagerNameOptionPanel.Add(self.metaDefaultManagerNameOption, 1, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaDefaultManagerNameOption, 0, wx.EXPAND | wx.ALL, 2)

        # 默认关联名称（default_related_name）
        self.metaDefaultRelatedNameOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaDefaultRelatedNameOptionPanel = wx.StaticBoxSizer(self.metaDefaultRelatedNameOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaDefaultRelatedNameOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaDefaultRelatedNameOption = wx.StaticText(self.metaScollPanel, -1, "7、反向名称（default_related_name）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaDefaultRelatedNameOption = wx.TextCtrl(self.metaScollPanel, -1)
        self.readmeMetaDefaultRelatedNameOption = wx.StaticText(self.metaScollPanel, -1, " ** 外键关联反向名称，默认<model_name>_set。")
        self.metaDefaultRelatedNameOptionPanel.Add(self.labelMetaDefaultRelatedNameOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaDefaultRelatedNameOptionPanel.Add(self.metaDefaultRelatedNameOption, 1, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaDefaultRelatedNameOption, 0, wx.EXPAND | wx.ALL, 2)

        # 取最新的一条记录（get_latest_by）
        # 配合latest()函数使用
        self.metaGetLatestByOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaGetLatestByOptionPanel = wx.StaticBoxSizer(self.metaGetLatestByOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaGetLatestByOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaGetLatestByOption = wx.StaticText(self.metaScollPanel, -1, "8、取最新的一条记录（get_latest_by）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaGetLatestByOption = wx.TextCtrl(self.metaScollPanel, -1)
        self.readmeMetaGetLatestByOption = wx.StaticText(self.metaScollPanel, -1, " ** 默认指定日期字段，加前缀'-'表示倒序，可组合。配合latest()函数使用。")
        self.metaGetLatestByOptionPanel.Add(self.labelMetaGetLatestByOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaGetLatestByOptionPanel.Add(self.metaGetLatestByOption, 1, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaGetLatestByOption, 0, wx.EXPAND | wx.ALL, 2)

        # 托管模型（managed）
        self.metaManagedOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaManagedOptionPanel = wx.StaticBoxSizer(self.metaManagedOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaManagedOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaManagedOption = wx.StaticText(self.metaScollPanel, -1, "9、托管模型（managed）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaManagedOption = wx.RadioBox(self.metaScollPanel, -1, "", choices=['是', '否'])
        self.readmeMetaManagedOption = wx.StaticText(self.metaScollPanel, -1, " ** 托管意味着由Django掌控模型的所有生命周期，这也是Django的默认行为。")
        self.metaManagedOptionPanel.Add(self.labelMetaManagedOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaManagedOptionPanel.Add(self.metaManagedOption, 0, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaManagedOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaManagedOption.SetSelection(0)

        # 指定排序字段（ordering）
        # ordering = [F('author').asc(nulls_last=True)]
        self.metaOrderingOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaOrderingOptionPanel = wx.StaticBoxSizer(self.metaOrderingOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaOrderingOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaOrderingOption = wx.StaticText(self.metaScollPanel, -1, "10、指定排序字段（ordering）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaOrderingOption = wx.TextCtrl(self.metaScollPanel, -1)
        self.readmeMetaOrderingOption = wx.StaticText(self.metaScollPanel, -1, " ** 前缀'-'表示倒叙，可多字段组合，中间用英文逗号隔开。")
        self.metaOrderingOptionPanel.Add(self.labelMetaOrderingOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaOrderingOptionPanel.Add(self.metaOrderingOption, 1, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaOrderingOption, 0, wx.EXPAND | wx.ALL, 2)

        # 默认权限（default_permissions）
        self.metaDefaultPermissionsOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaDefaultPermissionsOptionPanel = wx.StaticBoxSizer(self.metaDefaultPermissionsOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaDefaultPermissionsOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaDefaultPermissionsOption = wx.StaticText(self.metaScollPanel, -1, "11、默认权限（default_permissions）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaDefaultPermissionsOption = wx.TextCtrl(self.metaScollPanel, -1)
        self.readmeMetaDefaultPermissionsOption = wx.StaticText(self.metaScollPanel, -1, " ** 默认值('add', 'change', 'delete', 'view')，view为Django2.1版本后添加。")
        self.metaDefaultPermissionsOptionPanel.Add(self.labelMetaDefaultPermissionsOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaDefaultPermissionsOptionPanel.Add(self.metaDefaultPermissionsOption, 1, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaDefaultPermissionsOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaDefaultPermissionsOption.SetValue("('add', 'change', 'delete', 'view')")

        # 额外权限（permissions）
        # (permission_code, human_readable_permission_name)
        self.metaPermissionsOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaPermissionsOptionPanel = wx.StaticBoxSizer(self.metaPermissionsOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaPermissionsOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaPermissionsOption = wx.StaticText(self.metaScollPanel, -1, "12、额外权限（permissions）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaPermissionsOption = wx.TextCtrl(self.metaScollPanel, -1)
        self.readmeMetaPermissionsOption = wx.StaticText(self.metaScollPanel, -1, " ** 默认添加增删改查权限，可新增权限，用二元组列表表示。如[('code', 'name'),]")
        self.metaPermissionsOptionPanel.Add(self.labelMetaPermissionsOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaPermissionsOptionPanel.Add(self.metaPermissionsOption, 1, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaPermissionsOption, 0, wx.EXPAND | wx.ALL, 2)

        # 代理模型（proxy）
        self.metaProxyOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaProxyOptionPanel = wx.StaticBoxSizer(self.metaProxyOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaProxyOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaProxyOption = wx.StaticText(self.metaScollPanel, -1, "13、代理模型（proxy）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaProxyOption = wx.RadioBox(self.metaScollPanel, -1, "", choices=['是', '否'])
        self.readmeMetaProxyOption = wx.StaticText(self.metaScollPanel, -1, " ** 为原模型创建一个代理，用于扩展排序或管理器，与原模型共用一个表。")
        self.metaProxyOptionPanel.Add(self.labelMetaProxyOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaProxyOptionPanel.Add(self.metaProxyOption, 0, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaProxyOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaProxyOption.SetSelection(1)

        # 保存旧算法（select_on_save）
        self.metaSelectOnSaveOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaSelectOnSaveOptionPanel = wx.StaticBoxSizer(self.metaSelectOnSaveOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaSelectOnSaveOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaSelectOnSaveOption = wx.StaticText(self.metaScollPanel, -1, "14、保存旧算法（select_on_save）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaSelectOnSaveOption = wx.RadioBox(self.metaScollPanel, -1, "", choices=['是', '否'])
        self.readmeMetaSelectOnSaveOption = wx.StaticText(self.metaScollPanel, -1, " ** 旧算法只对存在的数据更新，新算法直接尝试更新。")
        self.metaSelectOnSaveOptionPanel.Add(self.labelMetaSelectOnSaveOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaSelectOnSaveOptionPanel.Add(self.metaSelectOnSaveOption, 0, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaSelectOnSaveOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaSelectOnSaveOption.SetSelection(1)

        # 指定后端数据库类型（required_db_vendor）
        self.metaRequiredDBVendorOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaRequiredDBVendorOptionPanel = wx.StaticBoxSizer(self.metaRequiredDBVendorOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaRequiredDBVendorOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaRequiredDBVendorOption = wx.StaticText(self.metaScollPanel, -1, "15、指定后端数据库类型（required_db_vendor）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaRequiredDBVendorOption = wx.Choice(self.metaScollPanel, -1, choices=[' ',]+env.getDjangoSupportDatabase())
        self.readmeMetaRequiredDBVendorOption = wx.StaticText(self.metaScollPanel, -1, " ** 不指定则默认支持所有。")
        self.metaRequiredDBVendorOptionPanel.Add(self.labelMetaRequiredDBVendorOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaRequiredDBVendorOptionPanel.Add(self.metaRequiredDBVendorOption, 0, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaRequiredDBVendorOption, 0, wx.EXPAND | wx.ALL, 2)

        # 索引集合（indexes）
        self.metaIndexesOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaIndexesOptionPanel = wx.StaticBoxSizer(self.metaIndexesOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaIndexesOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaIndexesOption = wx.StaticText(self.metaScollPanel, -1, "16、索引集合（indexes）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaIndexesOption = wx.TextCtrl(self.metaScollPanel, -1)
        self.readmeMetaIndexesOption = wx.StaticText(self.metaScollPanel, -1, " ** 示例：[models.Index(fields=['first_name',], name='first_name_idx'),]")
        self.metaIndexesOptionPanel.Add(self.labelMetaIndexesOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaIndexesOptionPanel.Add(self.metaIndexesOption, 1, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaIndexesOption, 0, wx.EXPAND | wx.ALL, 2)

        # 值唯一组合（unique_together）
        self.metaUniqueTogetherOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaUniqueTogetherOptionPanel = wx.StaticBoxSizer(self.metaUniqueTogetherOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaUniqueTogetherOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaUniqueTogetherOption = wx.StaticText(self.metaScollPanel, -1, "17、值唯一组合（unique_together）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaUniqueTogetherOption = wx.TextCtrl(self.metaScollPanel, -1)
        self.readmeMetaUniqueTogetherOption = wx.StaticText(self.metaScollPanel, -1, " ** 示例：[['driver', 'restaurant',],]。将来可能被弃用。")
        self.metaUniqueTogetherOptionPanel.Add(self.labelMetaUniqueTogetherOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaUniqueTogetherOptionPanel.Add(self.metaUniqueTogetherOption, 1, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaUniqueTogetherOption, 0, wx.EXPAND | wx.ALL, 2)

        # 索引组合（index_together）
        self.metaIndexTogetherOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaIndexTogetherOptionPanel = wx.StaticBoxSizer(self.metaIndexTogetherOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaIndexTogetherOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaIndexTogetherOption = wx.StaticText(self.metaScollPanel, -1, "18、索引组合（index_together）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaIndexTogetherOption = wx.TextCtrl(self.metaScollPanel, -1)
        self.readmeMetaIndexTogetherOption = wx.StaticText(self.metaScollPanel, -1, " ** 示例：[['pub_date', 'deadline'],]。将来可能被弃用。")
        self.metaIndexTogetherOptionPanel.Add(self.labelMetaIndexTogetherOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaIndexTogetherOptionPanel.Add(self.metaIndexTogetherOption, 1, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaIndexTogetherOption, 0, wx.EXPAND | wx.ALL, 2)

        # 约束条件（constraints）
        self.metaConstraintsOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaConstraintsOptionPanel = wx.StaticBoxSizer(self.metaConstraintsOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaConstraintsOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaConstraintsOption = wx.StaticText(self.metaScollPanel, -1, "19、约束条件（constraints）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaConstraintsOption = wx.TextCtrl(self.metaScollPanel, -1)
        self.readmeMetaConstraintsOption = wx.StaticText(self.metaScollPanel, -1, " ** 示例：[models.CheckConstraint(check=models.Q(age__gte=18), name='age_gte_18'),]。")
        self.metaConstraintsOptionPanel.Add(self.labelMetaConstraintsOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaConstraintsOptionPanel.Add(self.metaConstraintsOption, 1, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaConstraintsOption, 0, wx.EXPAND | wx.ALL, 2)

        # 模型可读单数名称（verbose_name）
        self.metaVerboseNameOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaVerboseNameOptionPanel = wx.StaticBoxSizer(self.metaVerboseNameOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaVerboseNameOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaVerboseNameOption = wx.StaticText(self.metaScollPanel, -1, "20、模型可读单数名称（verbose_name）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaVerboseNameOption = wx.TextCtrl(self.metaScollPanel, -1)
        self.readmeMetaVerboseNameOption = wx.StaticText(self.metaScollPanel, -1, " ** 用于后台展示模型名称。")
        self.metaVerboseNameOptionPanel.Add(self.labelMetaVerboseNameOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaVerboseNameOptionPanel.Add(self.metaVerboseNameOption, 1, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaVerboseNameOption, 0, wx.EXPAND | wx.ALL, 2)

        # 模型可读复数名称（verbose_name_plural）
        self.metaVerboseNamePluralOptionStaticBox = wx.StaticBox(self.metaScollPanel, -1, '')
        self.metaVerboseNamePluralOptionPanel = wx.StaticBoxSizer(self.metaVerboseNamePluralOptionStaticBox, wx.HORIZONTAL)
        metaScollPanelSizer.Add(self.metaVerboseNamePluralOptionPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelMetaVerboseNamePluralOption = wx.StaticText(self.metaScollPanel, -1, "21、模型可读复数名称（verbose_name_plural）", size=(STATIC_TEXT_WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.metaVerboseNamePluralOption = wx.TextCtrl(self.metaScollPanel, -1)
        self.readmeMetaVerboseNamePluralOption = wx.StaticText(self.metaScollPanel, -1, " ** 默认是verbose_name+s。")
        self.metaVerboseNamePluralOptionPanel.Add(self.labelMetaVerboseNamePluralOption, 0, wx.EXPAND | wx.ALL, 2)
        self.metaVerboseNamePluralOptionPanel.Add(self.metaVerboseNamePluralOption, 1, wx.EXPAND | wx.ALL, 2)
        metaScollPanelSizer.Add(self.readmeMetaVerboseNamePluralOption, 0, wx.EXPAND | wx.ALL, 2)

        # order_with_respect_to暂不放出

        # 标签显示优化
        self.readmeStaticTexts.extend([
            self.readmeMetaAbstractOption,
            self.readmeMetaAppLabelOption,
            self.readmeMetaObjectsOption,
            self.readmeMetaDBTableOption,
            self.readmeMetaDBTableSpaceOption,
            self.readmeMetaDefaultManagerNameOption,
            self.readmeMetaDefaultRelatedNameOption,
            self.readmeMetaGetLatestByOption,
            self.readmeMetaManagedOption,
            self.readmeMetaOrderingOption,
            self.readmeMetaPermissionsOption,
            self.readmeMetaDefaultPermissionsOption,
            self.readmeMetaProxyOption,
            self.readmeMetaSelectOnSaveOption,
            self.readmeMetaRequiredDBVendorOption,
            self.readmeMetaIndexesOption,
            self.readmeMetaUniqueTogetherOption,
            self.readmeMetaIndexTogetherOption,
            self.readmeMetaConstraintsOption,
            self.readmeMetaVerboseNameOption,
            self.readmeMetaVerboseNamePluralOption,
        ])
        self.labelStaticTexts.extend([
            self.labelMetaAbstractOption,
            self.labelMetaAppLabelOption,
            self.labelMetaObjectsOption,
            self.labelMetaDBTableOption,
            self.labelMetaDBTableSpaceOption,
            self.labelMetaDefaultManagerNameOption,
            self.labelMetaDefaultRelatedNameOption,
            self.labelMetaGetLatestByOption,
            self.labelMetaManagedOption,
            self.labelMetaOrderingOption,
            self.labelMetaPermissionsOption,
            self.labelMetaDefaultPermissionsOption,
            self.labelMetaProxyOption,
            self.labelMetaSelectOnSaveOption,
            self.labelMetaRequiredDBVendorOption,
            self.labelMetaIndexesOption,
            self.labelMetaUniqueTogetherOption,
            self.labelMetaIndexTogetherOption,
            self.labelMetaConstraintsOption,
            self.labelMetaVerboseNameOption,
            self.labelMetaVerboseNamePluralOption,
        ])

        # 按钮事件
        self.Bind(wx.EVT_BUTTON, self.onBtnShowUnshowMeta, self.btnShowUnshowMeta)
        # 单选框事件
        self.Bind(wx.EVT_RADIOBOX, self.onMetaRadioChanged, self.metaAbstractOption)

        self.metaScollPanel.Show(False) # 默认不显示
        self._init_meta_data()
    
    def _init_meta_data(self):
        """初始化Meta选项数据"""
        self.metaAbstractOption.SetSelection(1)

    def onMetaRadioChanged(self, e):
        """单选框值更新事件"""
        fid = e.GetId() # 控件id

        status_abstract = self.metaAbstractOption.GetSelection()

        if fid == self.metaAbstractOption.GetId():
            if 0 == status_abstract:
                TipsMessageOKBox(self, '抽象模型不会在数据库中建表。', '警告')

    def onBtnShowUnshowMeta(self, e):
        """显示和隐藏Meta按钮，用于空间的合理布局"""
        if '【显示】Meta元数据' == self.btnShowUnshowMeta.Label:
            self.metaScollPanel.Show(True)
            self.btnShowUnshowMeta.SetLabel('【隐藏】Meta元数据')
            self.panel.Layout() # 重新计算布局
        else:
            self.metaScollPanel.Show(False)
            self.btnShowUnshowMeta.SetLabel('【显示】Meta元数据')
            self.panel.Layout()

    def onBtnPreview(self, e):
        """预览待插入代码"""

        pre_fields = []

        for _ in self.allRows:

            # 若和默认值一致，则不显式显示参数
            args = []
            field_name = _['field_name']
            field_type = _['field_type']
            # 位置参数
            if _['remarker'] != _['field_name'].replace('_', ' '): # 默认下划线默认换成空格）
                t = _['remarker']
                args.append(f"'{t}'")

            # 关键字参数
            if _['field_name'] != _['db_column']: # 默认一致，不一致则新增
                t = _['db_column']
                args.append(f"db_column='{t}'")
                
            if CON_YES == _['primary_key']:
                args.append(f"primary_key=True")
            
            if CON_YES == _['blank']:
                args.append(f"blank=True")
                
            if CON_YES == _['null']:
                args.append(f"null=True")

            if CON_YES == _['unique']:
                args.append(f"unique=True")

            if CON_YES == _['db_index']:
                args.append(f"db_index=True")

            if CON_YES == _['auto_now']:
                args.append(f"auto_now=True")

            if CON_YES == _['auto_now_add']:
                args.append(f"auto_now_add=True")

            if CON_NO == _['editable']:
                args.append(f"editable=False")

            if '' != _['default']:
                t = _['default']
                args.append(f"default={t}")

            if '' != _['unique_for_date']:
                t = _['unique_for_date']
                args.append(f"unique_for_date='{t}'")

            if '' != _['unique_for_month']:
                t = _['unique_for_month']
                args.append(f"unique_for_month='{t}'")
            
            if '' != _['unique_for_year']:
                t = _['unique_for_year']
                args.append(f"unique_for_year='{t}'")
            
            if '' != _['error_messages']:
                t = _['error_messages']
                args.append(f"error_messages='{t}'") 

            if '' != _['help_text']:
                t = _['help_text']
                args.append(f"help_text='{t}'") 

            if '' != _['max_length']:
                t = _['max_length']
                args.append(f"max_length={t}")

            if 'DecimalField' == field_type:
                if '' != _['max_digits']:
                    t = _['max_digits']
                    args.append(f"max_digits={t}")

                if '' != _['decimal_places']:
                    t = _['decimal_places']
                    args.append(f"decimal_places={t}")

            if '' != _['upload_to']:
                t = _['upload_to']
                args.append(f"upload_to={t}")

            pre_fields.append(f"{field_name} = models.{field_type}({', '.join(args)})")

        # 字段详细定义
        if len(pre_fields) > 0:
            fields_code = '\n'.join([f'    {_}' for _ in pre_fields])
        else:
            fields_code = '    pass'

        # Meta元数据定义
        meta_code = '    pass'

        # __str__()返回值
        str_msg = "    return ''"

        # 如果没有设置主键，则自动增加主键【预览界面有效，实际代码无此行】
        if len([_ for _ in self.allRows if CON_YES==_['primary_key']]) <= 0: # 用户无主动设置主键
            auto_primary = 'id = models.AutoField(primary_key=True)'
        else:
            auto_primary = ''
        
        model_code = f"""
class DemoModel(models.Model):
    {auto_primary}
{fields_code}

    class meta:
    {meta_code}

    def __str__(self):
    {str_msg}
"""
        CodePreviewBox(self, model_code)

    def _show_special_args(self):
        """显示特殊参数"""
        for _ in self.specialArgs:
            _.Show(True)

    def _unshow_special_args(self):
        """隐藏特殊参数"""
        for _ in self.specialArgs:
            _.Show(False)

    def onRadioChanged(self, e):
        """单选框值更新事件"""
        fid = e.GetId() # 控件id

        field_type = con_getFieldTypeName(self.choiceFieldType.GetString(self.choiceFieldType.GetSelection()).strip()) # 当前字段类型

        status_null = self.radiosFiledNull.GetSelection()
        status_blank = self.radiosFiledBlank.GetSelection()
        status_unique = self.radiosFiledUnique.GetSelection()
        status_primary_key = self.radiosFiledPrimary.GetSelection()
        status_editable = self.radiosFiledEditable.GetSelection()
        status_autonow = self.radiosAutoNow.GetSelection()
        status_autonowadd = self.radiosAutoNowAdd.GetSelection()

        if fid == self.radiosFiledPrimary.GetId():
            # 同时只能有一个显式主键存在
            if len([_ for _ in self.allRows if CON_YES==_['primary_key']]) > 0:
                self.radiosFiledPrimary.SetSelection(1)
                TipsMessageOKBox(self, '一个模型只能拥有一个显式主键，若想对此字段设置主键，请使用隐式方式：null=False且unique=True。', '警告')
                return

            # 自动赋值默认值None
            if 0 == status_primary_key: # 主键
                self.inputDefaultValue.SetValue('None')
                self.inputDefaultValue.Enable(False)
                # 自动锁定null blank unique db_index
                self.radiosFiledNull.Enable(False)
                self.radiosFiledBlank.Enable(False)
                self.radiosFiledUnique.Enable(False)
                self.radiosFiledDbIndex.Enable(False)
                # 初始状态
                self.radiosFiledBlank.SetSelection(1) # 不允许为空
                self.radiosFiledNull.SetSelection(1) # 字段为空不赋值NULL
                self.radiosFiledUnique.SetSelection(1) # 值不唯一
                self.radiosFiledDbIndex.SetSelection(1) # 不创建索引
            else: # 反向操作，状态复原
                self.inputDefaultValue.SetValue('')
                self.inputDefaultValue.Enable(True)
                self.radiosFiledNull.Enable(True)
                self.radiosFiledBlank.Enable(True)
                self.radiosFiledUnique.Enable(True)
                self.radiosFiledDbIndex.Enable(True)

        elif fid == self.radiosFiledNull.GetId():
            # 避免在CharField之类的字段中使用 null=True 【用户选中时给予提示】
            # 当 CharField 同时具有 unique=True 和 blank=True 时。 在这种情况下，需要设置 null=True
            if field_type in CON_CHAR_FIELDS and 0 == status_null:
                TipsMessageOKBox(self, '字符类型的字段设置null=True会出现两种可能的值，如非必要，请勿选择。', '警告')
            
            if 'BooleanField' == field_type and 0 == status_null:
                TipsMessageOKBox(self, 'BooleanField字段在2.1版本之前不支持设置null=True，新版本可以。不建议使用NullBooleanField。', '警告')

        elif fid == self.radiosFiledBlank.GetId():
            if field_type in CON_CHAR_FIELDS and 0 == status_unique and 0 == status_blank:
                self.radiosFiledNull.SetSelection(0)
                self.radiosFiledNull.Enable(False) # 同时锁定无法修改
                TipsMessageOKBox(self, '字符类型的字段同时设置unique=True和blank=True时，必须设置null=True。', '警告')
            if 0 != status_blank:
                self.radiosFiledNull.Enable(True) # 不是同时选中的状态，解锁null字段

        elif fid == self.radiosFiledUnique.GetId():
            if field_type in CON_CHAR_FIELDS and 0 == status_unique and 0 == status_blank:
                self.radiosFiledNull.SetSelection(0)
                self.radiosFiledNull.Enable(False) # 同时锁定无法修改
                TipsMessageOKBox(self, '字符类型的字段同时设置unique=True和blank=True时，必须设置null=True。', '警告')
            if 0 != status_unique:
                self.radiosFiledNull.Enable(True) # 不是同时选中的状态，解锁null字段

        elif fid == self.radiosFiledEditable.GetId():
            # BinaryField字段在2.1版本之前不支持editable=True
            if 'BinaryField' == field_type and 0 == status_editable:
                TipsMessageOKBox(self, 'Django2.1版本之前（不包括2.1），不支持设置editable=True。', '警告')
        
        elif fid == self.radiosAutoNow.GetId():
            if 0 == status_autonow:
                self.radiosAutoNowAdd.SetSelection(1)
                self.inputDefaultValue.SetValue('')
                self.inputDefaultValue.Enable(False)
                # 当设置auto_now_add=True或auto_now=True时，默认同时设置editable=False和blank=True
                self.radiosFiledEditable.SetSelection(1)
                self.radiosFiledBlank.SetSelection(0)
                self.radiosFiledEditable.Enable(False)
                self.radiosFiledBlank.Enable(False)

            else:
                if 1 == status_autonowadd:
                    self.inputDefaultValue.SetValue('date.today')
                    # 反向操作
                    self.inputDefaultValue.Enable(True)
                    self.radiosFiledEditable.SetSelection(0)
                    self.radiosFiledBlank.SetSelection(1)
                    self.radiosFiledEditable.Enable(True)
                    self.radiosFiledBlank.Enable(True)

        elif fid == self.radiosAutoNowAdd.GetId():
            if 0 == status_autonowadd:
                self.radiosAutoNow.SetSelection(1)
                self.inputDefaultValue.SetValue('')
                self.inputDefaultValue.Enable(False)
                # 当设置auto_now_add=True或auto_now=True时，默认同时设置editable=False和blank=True
                self.radiosFiledEditable.SetSelection(1)
                self.radiosFiledBlank.SetSelection(0)
                self.radiosFiledEditable.Enable(False)
                self.radiosFiledBlank.Enable(False)
            else:
                if 1 == status_autonow:
                    self.inputDefaultValue.SetValue('date.today')
                    self.inputDefaultValue.Enable(True)
                    self.radiosFiledEditable.SetSelection(0)
                    self.radiosFiledBlank.SetSelection(1)
                    self.radiosFiledEditable.Enable(True)
                    self.radiosFiledBlank.Enable(True)

    def onInputFieldModelName(self, e):
        """模型字段名设置时自动触发值更新"""
        field_name = self.inputFieldModelName.GetValue().strip()
        # 每次取最新的一次输入字符
        if PATT_CHARS.match(field_name):
            self.inputFieldDatabaseName.SetValue(field_name)
            self.inputFieldRemarkName.SetValue(field_name.replace('_', ' '))
        else:
            self.inputFieldModelName.SetValue(PATT_CHARS_REVERSED.sub('', field_name))
            self.inputFieldModelName.SetInsertionPointEnd() # 光标定位到最后

    def onInputMaxLength(self, e):
        """长度上限属性填写时自动触发值更新"""
        v = str(self.inputMaxLength.GetValue().strip())
        if '0' == v:
            self.inputMaxLength.SetValue('')
            return
        if v and isinstance(v, str): # 此处条件分支解决递归错误问题
            if not PATT_DIGITS_WHOLE.match(v):
                self.inputMaxLength.SetValue(PATT_DIGITS_REVERSED.sub('', v))
                self.inputMaxLength.SetInsertionPointEnd()

    def onInputMaxDigits(self, e):
        """实数总位数自动触发值更新"""
        v = str(self.inputMaxDigits.GetValue().strip())
        if '0' == v:
            self.inputMaxDigits.SetValue('')
            return
        if v and isinstance(v, str):
            if not PATT_DIGITS_WHOLE.match(v):
                self.inputMaxDigits.SetValue(PATT_DIGITS_REVERSED.sub('', v))
                self.inputMaxDigits.SetInsertionPointEnd()

    def onInputDecimalPlaces(self, e):
        """小数总位数自动触发值更新"""
        v = str(self.inputDecimalPlaces.GetValue().strip())
        if '0' == v:
            self.inputDecimalPlaces.SetValue('')
            return
        if v and isinstance(v, str):
            if not PATT_DIGITS_WHOLE.match(v):
                self.inputDecimalPlaces.SetValue(PATT_DIGITS_REVERSED.sub('', v))
                self.inputDecimalPlaces.SetInsertionPointEnd()

    def _disable_all_args(self):
        """关闭所有的参数填写入口"""
        for _ in self.allArgs:
            _.Enable(False)

    def _init_all_args_value(self):
        """初始化参数默认值"""
        self.radiosFiledBlank.SetSelection(1) # 不允许为空
        self.radiosFiledNull.SetSelection(1) # 字段为空不赋值NULL
        self.radiosFiledPrimary.SetSelection(1) # 不是主键
        self.radiosFiledUnique.SetSelection(1) # 值不唯一
        self.radiosFiledDbIndex.SetSelection(1) # 不创建索引
        self.radiosFiledEditable.SetSelection(0) # 菜单默认可编辑
        self.choicesFiledUniqueForDate.SetSelection(0) # 无组合唯一
        self.choicesFiledUniqueForMonth.SetSelection(0) # 无组合唯一
        self.choicesFiledUniqueForYear.SetSelection(0) # 无组合唯一
        self.radiosAutoNow.SetSelection(1)
        self.radiosAutoNowAdd.SetSelection(1)
        self.choiceSelectModel.SetSelection(0)
        self.choiceSelectDelRule.SetSelection(1)

    def _init_input_args(self):
        """初始化输入框"""
        self.choiceFieldType.SetSelection(0)
        self.inputFieldModelName.SetValue('')
        self.inputFieldRemarkName.SetValue('')
        self.inputFieldDatabaseName.SetValue('')
        self.inputDefaultValue.SetValue('')
        self.inputFormHelpText.SetValue('')
        self.inputFormErrorMessage.SetValue('')
        self.inputMaxLength.SetValue('')
        self.inputMaxDigits.SetValue('')
        self.inputDecimalPlaces.SetValue('')
        self.inputUploadTo.SetValue('')
        self.inputRelationRemark.SetValue('')

    def _disable_all_afterBtns(self):
        """关闭所有的后触发按钮"""
        for _ in self.afterBtns:
            _.Enable(False)

    def _init_table(self):
        """初始化表格控件"""

        # 显示和隐藏按钮，用于空间的合理布局
        self.btnShowUnshowTable = buttons.GenButton(self.panel, -1, '【显示】待新增字段表格数据')
        self.panelSizer.Add(self.btnShowUnshowTable, 0, wx.EXPAND | wx.ALL, 2)
        self.btnShowUnshowTable.SetBackgroundColour(CON_COLOR_BLUE)
        self.btnShowUnshowTable.SetForegroundColour(CON_COLOR_WHITE)

        # 表格
        self.tableObjPanel = wx.Panel(self.panel, size=(730, 222))
        tableObjPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.tableObjPanel.SetSizer(tableObjPanelSizer)
        self.panelSizer.Add(self.tableObjPanel, 0, wx.EXPAND | wx.ALL, 2)
        self.tableObjPanel.SetBackgroundColour('#000000')

        # 表头
        self.gridToolsPanel = wx.Panel(self.tableObjPanel)
        gridToolsPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.gridToolsPanel.SetSizer(gridToolsPanelSizer)
        tableObjPanelSizer.Add(self.gridToolsPanel, 0, wx.EXPAND | wx.ALL, 2)
        
        self.gridBtnDelete = buttons.GenButton(self.gridToolsPanel, -1, '删除选中行')
        self.gridBtnOther = buttons.GenButton(self.gridToolsPanel, -1, ' ')
        self.gridBtnOther.Enable(False)
        gridToolsPanelSizer.Add(self.gridBtnDelete, 0, wx.EXPAND | wx.ALL, 2)
        gridToolsPanelSizer.Add(self.gridBtnOther, 1, wx.EXPAND | wx.ALL, 2)

        # 表体
        self.infoGrid = wx.grid.Grid( self.tableObjPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

        self.infoGrid.CreateGrid( 0, len(CON_MODELSCREATEDIALOG_COLS) ) # row  col
        self.infoGrid.EnableEditing( False )
        self.infoGrid.EnableGridLines( True )
        self.infoGrid.EnableDragGridSize( True )
        self.infoGrid.SetMargins( 0, 0 )

        self.infoGrid.EnableDragColMove( False )
        self.infoGrid.EnableDragColSize( True )
        self.infoGrid.SetColLabelSize( 30 )
        self.infoGrid.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        self.infoGrid.EnableDragRowSize( True )
        self.infoGrid.SetRowLabelSize( 70 )
        self.infoGrid.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        self.infoGrid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        tableObjPanelSizer.Add( self.infoGrid, 1, wx.EXPAND | wx.ALL, 2 ) # 表格默认加最后

        self._init_header()

        # 事件
        self.Bind(wx.EVT_BUTTON, self.onGridBtnDelete, self.gridBtnDelete)
        self.Bind(wx.EVT_BUTTON, self.onBtnShowUnshowTable, self.btnShowUnshowTable)

        self.tableObjPanel.Show(False) # 默认隐藏

    def onBtnShowUnshowTable(self, e):
        """显示和隐藏按钮，用于空间的合理布局"""
        if '【显示】待新增字段表格数据' == self.btnShowUnshowTable.Label:
            self.tableObjPanel.Show(True)
            self.btnShowUnshowTable.SetLabel('【隐藏】待新增字段表格数据')
            self.panel.Layout() # 重新计算布局
        else:
            self.tableObjPanel.Show(False)
            self.btnShowUnshowTable.SetLabel('【显示】待新增字段表格数据')
            self.panel.Layout()

    def onGridBtnDelete(self, e):
        """删除行"""
        row_indexs = self.infoGrid.GetSelectedRows()
        t = '、'.join([str(_+1) for _ in row_indexs])
        if len(row_indexs) > 0:
            dlg_tip = wx.MessageDialog(self, f"确认删除第{t}行？一旦删除不可恢复。", CON_TIPS_COMMON, wx.CANCEL | wx.OK)
            if dlg_tip.ShowModal() == wx.ID_OK:
                result = self.removeRows(row_indexs)
                if not result:
                    TipsMessageOKBox(self, '删除成功！', '提示')
                else:
                    if isinstance(result, list):
                        TipsMessageOKBox(self, f"{'、'.join(result)}删除失败！", '提示')
                    else:
                        TipsMessageOKBox(self, '未知错误，删除失败。', '提示')
            dlg_tip.Close(True)
        else:
            TipsMessageOKBox(self, '无选择行可删除。', '警告')

    def _init_header(self):
        """初始化列名"""
        for i,v in enumerate(CON_MODELSCREATEDIALOG_COLS):
            self.infoGrid.SetColLabelValue(i, v)

    def onChoiceFieldType(self, e):
        """选择要新建的字段类型"""
        field_type = e.GetString().strip(string.whitespace+'-')

        if not field_type:
            return

        # try:
        #     if self.record != field_type: # 值未更新
        #         # 每次更新时均初始化状态
        #         self._init_all_args_value()
        #         self._init_input_args()
        # except: ...
        # self.record = field_type # 记录上一次的状态

        self._open_required_args() # 共用参数开启
        self._unshow_special_args() # 先隐藏所有的特殊参数，后按需开启

        if CON_BINARYFIELD == field_type:
            self.selectBinaryField()
        elif CON_SMALLINTEGERFIELD == field_type:
            self.selectSmallIntegerField()
        elif CON_POSITIVESMALLINTEGERFIELD == field_type:
            self.selectPositiveSmallIntegerField()
        elif CON_INTEGERFIELD == field_type:
            self.selectIntegerField()
        elif CON_POSITIVEINTEGERFIELD == field_type:
            self.selectPositiveIntegerField()
        elif CON_BIGINTEGERFIELD == field_type:
            self.selectBigIntegerField()
        elif CON_AUTOFIELD == field_type:
            self.selectAutoField()
        elif CON_BIGAUTOFIELD == field_type:
            self.selectBigAutoField()
        elif CON_FLOATFIELD == field_type:
            self.selectFloatField()
        elif CON_DECIMALFIELD == field_type:
            self.selectDecimalField()
        elif CON_BOOLEANFIELD == field_type:
            self.selectBooleanField()
        elif CON_CHARFIELD == field_type:
            self.selectCharField()
        elif CON_TEXTFIELD == field_type:
            self.selectTextField()
        elif CON_EMAILFIELD == field_type:
            self.selectEmailField()
        elif CON_IPADRESSFIELD == field_type:
            self.selectGenericIPAddressField()
        elif CON_SLUGFIELD == field_type:
            self.selectSlugField()
        elif CON_URLFIELD == field_type:
            self.selectURLField()
        elif CON_UUIDFIELD == field_type:
            self.selectUUIDField()
        elif CON_DATEFIELD == field_type:
            self.selectDateField()
        elif CON_DATETIMEFIELD == field_type:
            self.selectDateTimeField()
        elif CON_DURATIONFIELD == field_type:
            self.selectDurationField()
        elif CON_TIMEFIELD == field_type:
            self.selectTimeField()
        elif CON_FILEFIELD == field_type:
            self.selectFileField()
        elif CON_IMAGEFIELD == field_type:
            self.selectImageField()
        elif CON_FILEPATHFIELD == field_type:
            self.selectFilePathField()
        elif CON_FOREIGNFIELD == field_type:
            self.selectForeignKey()
        elif CON_MANYTOMANYFIELD == field_type:
            self.selectManyToManyField()
        elif CON_ONETOONEFIELD == field_type:
            self.selectOneToOneField()

        self.choiceFieldType.Enable(False) # 一旦选择将锁定字段的重新选择，可点击【重置字段】解锁

        self.panelSizer.Layout() # 重要！！！ 重新计算布局

    def onBtnSelectPath(self, e):
        """选择文件写入路径"""
        dlg = wx.FileDialog(self, "选择写入文件", get_configs(CONFIG_PATH)['dirname'], "", "*.py", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            self.inputSelectFile.SetValue(os.path.join(dirname, filename))
        dlg.Close(True)

    def onBtnAddNew(self, e):
        """新增字段"""
        self.choiceFieldType.Enable(True) # 开放字段下拉选择框
        self._show_special_args() # 显示所有的可选参数
        # 开放 后触发 按钮
        for _ in self.afterBtns:
            _.Enable(True)
        # 锁定新增按钮
        self.btnAddNew.Enable(False)

    def onBtnResetInput(self, e):
        """恢复字段默认值"""
        dlg_tip = wx.MessageDialog(self, f"确认重置字段？重置后将丢失界面所有已填数据。（待新增区不受影响）", CON_TIPS_COMMON, wx.CANCEL | wx.OK)
        if dlg_tip.ShowModal() == wx.ID_OK:
            self._init_all_args_value()
            self._init_input_args()
            # 参数重新选定，开放类型选择按钮
            self._disable_all_args()
            self._show_special_args() # 显示所有的可选参数
            self.choiceFieldType.Enable(True)
        dlg_tip.Close(True)

    def onBtnAddFieldToArea(self, e):
        """添加至待生成区"""
        dlg_tip = wx.MessageDialog(self, f"确认添加？", CON_TIPS_COMMON, wx.CANCEL | wx.OK)
        if dlg_tip.ShowModal() == wx.ID_OK:
            # 添加操作
            # 获取界面的所有值
            vchoiceFieldType = self.choiceFieldType.GetString(self.choiceFieldType.GetSelection()).strip()
            vinputFieldModelName = self.inputFieldModelName.GetValue().strip()
            vinputFieldDatabaseName = self.inputFieldDatabaseName.GetValue().strip()
            vinputDefaultValue = self.inputDefaultValue.GetValue().strip()
            vinputFormHelpText = self.inputFormHelpText.GetValue().strip()
            vinputFormErrorMessage = self.inputFormErrorMessage.GetValue().strip()
            vinputFieldRemarkName = self.inputFieldRemarkName.GetValue().strip()
            vinputMaxLength = self.inputMaxLength.GetValue().strip()
            vinputMaxDigits = self.inputMaxDigits.GetValue().strip()
            vinputDecimalPlaces = self.inputDecimalPlaces.GetValue().strip()
            vinputUploadTo = self.inputUploadTo.GetValue().strip()
            vradiosFiledBlank = self.radiosFiledBlank.GetSelection()
            vradiosFiledNull = self.radiosFiledNull.GetSelection()
            vradiosFiledPrimary = self.radiosFiledPrimary.GetSelection()
            vradiosFiledUnique = self.radiosFiledUnique.GetSelection()
            vradiosFiledDbIndex = self.radiosFiledDbIndex.GetSelection()
            vradiosFiledEditable = self.radiosFiledEditable.GetSelection()
            vradiosAutoNow = self.radiosAutoNow.GetSelection()
            vradiosAutoNowAdd = self.radiosAutoNowAdd.GetSelection()
            vchoicesFiledUniqueForDate = self.choicesFiledUniqueForDate.GetString(self.choicesFiledUniqueForDate.GetSelection()).strip()
            vchoicesFiledUniqueForMonth = self.choicesFiledUniqueForMonth.GetString(self.choicesFiledUniqueForMonth.GetSelection()).strip()
            vchoicesFiledUniqueForYear = self.choicesFiledUniqueForYear.GetString(self.choicesFiledUniqueForYear.GetSelection()).strip()

            # 先校验，后操作
            # 字段属性名+数据库列名+字段备注，三者只要有一个重复，便不允许新增该字段
            tfield_name, tfield_dbname, tfieldremark = [], [], []
            for _ in self.allRows:
                tfield_name.append(_['field_name'])
                tfield_dbname.append(_['field_name'])
                tfieldremark.append(_['remarker'])

            if vinputFieldModelName in tfield_name or vinputFieldDatabaseName in tfield_dbname or ('' != vinputFieldRemarkName and vinputFieldRemarkName in tfieldremark):
                TipsMessageOKBox(self, '字段属性名、数据库列名、字段备注均不能重复。', '警告')
                return

            # 必填项检测
            if not vchoiceFieldType: # 字段类型必选
                TipsMessageOKBox(self, '请选择字段类型！', '错误')
                return

            if not vinputFieldModelName: # 字段属性名必填
                TipsMessageOKBox(self, '请填写【字段属性名】！', '错误')
                return

            if (con_getFieldTypeName(vchoiceFieldType) in CON_OWN_MAX_LENGTH_FILEDS) and (not vinputMaxLength): # 所有有max_length属性的字段，必填max_length
                TipsMessageOKBox(self, '【长度上限】max_length必填！', '错误')
                return

            if 'DecimalField' == con_getFieldTypeName(vchoiceFieldType):
                if not vinputMaxDigits:
                    TipsMessageOKBox(self, '【实数总位数】必填！', '错误')
                    return
                else:
                    maxdigits = int(vinputMaxDigits)
                    dicimalplaces = int(vinputDecimalPlaces if vinputDecimalPlaces else '0')
                    if maxdigits < dicimalplaces:
                        TipsMessageOKBox(self, '【实数总位数】必需大于等于【小数总位数】！', '错误')
                        return

            # 待插入的行
            insertRow = {}
            insertRow['field_name'] = vinputFieldModelName
            insertRow['db_column'] = vinputFieldDatabaseName
            insertRow['remarker'] = vinputFieldRemarkName
            insertRow['field_type'] = con_getFieldTypeName(vchoiceFieldType)
            insertRow['primary_key'] = self._replace01_to_bool(vradiosFiledPrimary)
            insertRow['blank'] = self._replace01_to_bool(vradiosFiledBlank)
            insertRow['null'] = self._replace01_to_bool(vradiosFiledNull)
            insertRow['default'] = vinputDefaultValue
            insertRow['unique'] = self._replace01_to_bool(vradiosFiledUnique)
            insertRow['db_index'] = self._replace01_to_bool(vradiosFiledDbIndex)
            insertRow['choices'] = '' # 前端暂未放出
            insertRow['unique_for_date'] = vchoicesFiledUniqueForDate
            insertRow['unique_for_month'] = vchoicesFiledUniqueForMonth
            insertRow['unique_for_year'] = vchoicesFiledUniqueForYear
            insertRow['error_messages'] = vinputFormErrorMessage
            insertRow['editable'] = self._replace01_to_bool(vradiosFiledEditable)
            insertRow['help_text'] = vinputFormHelpText
            insertRow['max_length'] = vinputMaxLength
            insertRow['max_digits'] = vinputMaxDigits
            insertRow['decimal_places'] = vinputDecimalPlaces if vinputDecimalPlaces else '0'
            insertRow['auto_now'] = self._replace01_to_bool(vradiosAutoNow)
            insertRow['auto_now_add'] = self._replace01_to_bool(vradiosAutoNowAdd)
            insertRow['upload_to'] = vinputUploadTo

            self.allRows.append(insertRow) # 删除时根据字段名删除

            # 插入待新增数据区域
            self.infoGrid.AppendRows(1)
            row = self.infoGrid.GetNumberRows() - 1
            for col, _ in enumerate(CON_MODELSCREATEDIALOG_COLS):
                self.infoGrid.SetCellValue(row, col, str(insertRow.get(CON_ARGS_NAME_DICT[_])))

            # 界面数据全部初始化【全部参数暂时不放，只显示上一个字段相关的参数锁定界面】
            self._disable_all_args()
            self._init_all_args_value()
            self._init_input_args()
            self.choiceFieldType.SetSelection(0) # 单独拎出来初始化【不影响大体功能】

            # 重新开放新增按钮 锁定后触发按钮
            self.btnAddNew.Enable(True)
            self._disable_all_afterBtns()

            # 更新日期组合唯一的三个相关下拉框【只给日期字段相关的字段属性名】
            self.choicesFiledUniqueForDate.Clear()
            # self.choicesFiledUniqueForMonth.Clear()
            # self.choicesFiledUniqueForYear.Clear()

            # 目前只实现Date的日期唯一关联，其余两个暂不实现
            self.choicesFiledUniqueForDate.Append(' ')
            for _ in self.allRows:
                if _['field_type'] in CON_DATE_FIELDS:
                    self.choicesFiledUniqueForDate.Append(_['field_name'])

        dlg_tip.Close(True)

    def _replace01_to_bool(self, v):
        if 0 == v: return CON_YES
        else: return CON_NO

    def removeRows(self, row_indexs):
        """同步删除界面和数据包里的数据"""
        errors = []
        for i in sorted(row_indexs, reverse=True): # 倒序
            try:
                temp = self.infoGrid.GetCellValue(i, 0) # 字段属性名
                self.infoGrid.DeleteRows(i)
            except:
                errors.append(str(i+1))
            else:
                self._removeRowsByFieldName(temp)
        return errors

    def _removeRowsByFieldName(self, field_name):
        """"根据字段属性名删除"""
        for i,_ in enumerate(self.allRows):
            if field_name == _['field_name']:
                self.allRows.pop(i)
                break

    def onBtnExecSave(self, e):
        """保存"""
        if len(self.allRows) <= 0:
            dlg_tip = wx.MessageDialog(self, f"未添加任何字段，是否创建空模型？", CON_TIPS_COMMON, wx.CANCEL | wx.OK)
            if dlg_tip.ShowModal() == wx.ID_OK:
                dlg = wx.TextEntryDialog(self, u"模型命名：", u"保存模型", u"")
                if dlg.ShowModal() == wx.ID_OK:
                    message = dlg.GetValue()  # 获取文本框中输入的值
                dlg.Close(True)
            dlg_tip.Close(True)
        else:
            dlg = wx.TextEntryDialog(self, u"模型命名：", u"保存模型", u"")
            if dlg.ShowModal() == wx.ID_OK:
                message = dlg.GetValue()  # 获取文本框中输入的值
            dlg.Close(True)

    def _open_required_args(self):
        """所有字段必须同步开启的参数"""
        for _ in self.commonArgs:
            _.Enable(True)

    def _open_max_length_field(self):
        """开启max_length字段"""
        self.inputMaxLengthStaticBox.Show(True)
        self.inputMaxLength.Show(True)
        self.labelInputMaxLength.Show(True)
        self.readmeInputMaxLength.Show(True)
        self.inputMaxLength.Enable(True)

    def selectBinaryField(self):
        """字节型字段"""
        self.radiosFiledEditable.SetSelection(1)
        self._open_max_length_field()

    def selectSmallIntegerField(self):
        ...
    def selectPositiveSmallIntegerField(self):
        ...
    def selectIntegerField(self):
        ...
    def selectPositiveIntegerField(self):
        ...
    def selectBigIntegerField(self):
        ...
    def selectAutoField(self):
        """32位自增型字段"""
    def selectBigAutoField(self):
        ...
    def selectFloatField(self):
        ...
    def selectDecimalField(self):
        """高精度浮点型字段"""
        self.inputMaxDigitsStaticBox.Show(True)
        self.inputMaxDigits.Show(True)
        self.labelInputMaxDigits.Show(True)
        self.readmeInputMaxDigits.Show(True)
        self.inputDecimalPlacesStaticBox.Show(True)
        self.inputDecimalPlaces.Show(True)
        self.labelInputDecimalPlaces.Show(True)
        self.readmeInputDecimalPlaces.Show(True)
        self.inputMaxDigits.Enable(True)
        self.inputDecimalPlaces.Enable(True)

    def selectBooleanField(self):
        """布尔类型字段"""
        self.inputDefaultValue.SetValue('None')

    def selectCharField(self):
        """字符型字段"""
        self._open_max_length_field()
        self.inputMaxLength.SetValue('255') # 默认长度255

    def selectTextField(self):
        ...
    def selectEmailField(self):
        """电子邮件字段"""
        self._open_max_length_field()
        self.inputMaxLength.SetValue('254')

    def selectGenericIPAddressField(self):
        ...
    def selectSlugField(self):
        """字母、数字、连字符字段"""
        self._open_max_length_field()
        self.inputMaxLength.SetValue('50')

    def selectURLField(self):
        """url字段"""
        self._open_max_length_field()
        self.inputMaxLength.SetValue('200')

    def selectUUIDField(self):
        ...

    def _open_autonow_add(self):
        """开启日期相关的特殊参数"""
        self.radiosAutoNowStaticBox.Show(True)
        self.radiosAutoNow.Show(True)
        self.labelRadiosAutoNow.Show(True)
        self.readmeRadiosAutoNow.Show(True)
        self.radiosAutoNowAddStaticBox.Show(True)
        self.radiosAutoNowAdd.Show(True)
        self.labelRadiosAutoNowAdd.Show(True)
        self.readmeRadiosAutoNowAdd.Show(True)
        self.radiosAutoNow.Enable(True)
        self.radiosAutoNowAdd.Enable(True)

    def selectDateField(self):
        """日期型字段"""
        self._open_autonow_add()
        self.inputDefaultValue.SetValue('date.today')

    def selectDateTimeField(self):
        """长日期字段"""
        self._open_autonow_add()
        self.inputDefaultValue.SetValue('timezone.now')

    def selectDurationField(self):
        """时间戳字段"""

    def selectTimeField(self):
        """时间字段"""
        self._open_autonow_add()

    def selectFileField(self):
        """文件字段"""
        self._open_max_length_field()
        self.inputMaxLength.SetValue('100')

        self.inputUploadToStaticBox.Show(True)
        self.inputUploadTo.Show(True)
        self.labelInputUploadTo.Show(True)
        self.readmeInputUploadTo.Show(True)
        self.inputUploadTo.Enable(True)
        self.inputUploadTo.SetValue(r"'uploads/%Y/%m/%d/'")

    def selectImageField(self):
        ...
    def selectFilePathField(self):
        ...
    def selectForeignKey(self):
        """多对一字段"""
    def selectManyToManyField(self):
        """多对多字段"""
    def selectOneToOneField(self):
        """一对一字段"""
        
    def onExit(self, e):
        """退出窗口"""
        dlg_tip = wx.MessageDialog(self, f"确认退出？退出后界面数据将丢失。", CON_TIPS_COMMON, wx.CANCEL | wx.OK)
        if dlg_tip.ShowModal() == wx.ID_OK:
            self.Close(True)
        dlg_tip.Close(True)