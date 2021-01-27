import wx, json, glob, os
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

class ModelsCreateDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = '新增模型', size=(888, 888))

        # 必要的控制容器
        self.allArgs = [] # 所有的参数选项
        self.commonArgs = [] # 共有的参数选项
        self.specialArgs = [] # 特有的参数选项
        self.afterBtns = [] # 所有的后触发按钮
        self.allRows = [] # 所有的待新增按钮

        self._init_UI()
        self._disable_all_args()
        self._init_all_args_value()
        self._init_input_args()

        self._disable_all_afterBtns()

        self._init_table() # 表格布局默认加最后

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

        # 可滚动
        self.scollPanel = scrolledpanel.ScrolledPanel(self.panel, -1)
        # self.scollPanel.SetScrollRate( 1, 1 )
        # self.scollPanel.SetVirtualSize( ( 888, 345 ) )
        self.scollPanel.SetupScrolling()
        scollPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.scollPanel.SetSizer(scollPanelSizer)
        self.panelSizer.Add(self.scollPanel, 3, wx.EXPAND | wx.ALL, 2)

        # 选择字段类型
        selectFieldTypeStaticBox = wx.StaticBox(self.scollPanel, -1, '【选择】字段类型：')
        # selectFieldTypeStaticBox.SetBackgroundColour(CON_COLOR_BLACK)
        self.selectFieldTypePanel = wx.StaticBoxSizer(selectFieldTypeStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.selectFieldTypePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.choiceFieldType = wx.Choice(self.scollPanel, -1, choices = [' ']+CON_FIELD_TYPES, style = wx.CB_SORT)
        self.selectFieldTypePanel.Add(self.choiceFieldType, 1, wx.EXPAND | wx.ALL, 2)

        # 字段命名
        modelsNameStaticBox = wx.StaticBox(self.scollPanel, -1, '字段名【db_column】')
        self.modelsNamePanel = wx.StaticBoxSizer(modelsNameStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.modelsNamePanel, 0, wx.EXPAND | wx.ALL, 2)

        # 字段命名 - 左
        self.modelsNameLeftPanel = wx.Panel(self.scollPanel)
        modelsNameLeftPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.modelsNameLeftPanel.SetSizer(modelsNameLeftPanelSizer)
        self.modelsNamePanel.Add(self.modelsNameLeftPanel, 1, wx.EXPAND | wx.ALL, 2)

        self.labelFieldModelName = wx.StaticText(self.modelsNameLeftPanel, -1, "字段属性名：")
        self.inputFieldModelName = wx.TextCtrl(self.modelsNameLeftPanel, -1)
        modelsNameLeftPanelSizer.Add(self.labelFieldModelName, 0, wx.EXPAND | wx.ALL, 2)
        modelsNameLeftPanelSizer.Add(self.inputFieldModelName, 1, wx.EXPAND | wx.ALL, 2)

        # 字段命名 - 中
        self.modelsNameMiddlePanel = wx.Panel(self.scollPanel)
        modelsNameMiddlePanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.modelsNameMiddlePanel.SetSizer(modelsNameMiddlePanelSizer)
        self.modelsNamePanel.Add(self.modelsNameMiddlePanel, 1, wx.EXPAND | wx.ALL, 2)

        self.labelFieldDatabaseName = wx.StaticText(self.modelsNameMiddlePanel, -1, "数据库列名：（选填）")
        self.inputFieldDatabaseName = wx.TextCtrl(self.modelsNameMiddlePanel, -1)
        modelsNameMiddlePanelSizer.Add(self.labelFieldDatabaseName, 0, wx.EXPAND | wx.ALL, 2)
        modelsNameMiddlePanelSizer.Add(self.inputFieldDatabaseName, 1, wx.EXPAND | wx.ALL, 2)

        # 字段命名 - 右
        self.modelsNameRightPanel = wx.Panel(self.scollPanel)
        modelsNameRightPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.modelsNameRightPanel.SetSizer(modelsNameRightPanelSizer)
        self.modelsNamePanel.Add(self.modelsNameRightPanel, 1, wx.EXPAND | wx.ALL, 2)

        self.labelFieldRemarkName = wx.StaticText(self.modelsNameRightPanel, -1, "字段备注：（选填）")
        self.inputFieldRemarkName = wx.TextCtrl(self.modelsNameRightPanel, -1)
        modelsNameRightPanelSizer.Add(self.labelFieldRemarkName, 0, wx.EXPAND | wx.ALL, 2)
        modelsNameRightPanelSizer.Add(self.inputFieldRemarkName, 1, wx.EXPAND | wx.ALL, 2)

        """三个一行，布局"""
        # 混乱布局第1行
        self.complex1Panel = wx.Panel(self.scollPanel)
        complex1PanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.complex1Panel.SetSizer(complex1PanelSizer)
        scollPanelSizer.Add(self.complex1Panel, 0, wx.EXPAND | wx.ALL, 2)

        self.radiosFiledBlank = wx.RadioBox(self.complex1Panel, -1, "允许为空【blank】", choices=['允许', '不允许'])
        self.radiosFiledNull = wx.RadioBox(self.complex1Panel, -1, "为空时赋NULL【null】", choices=['赋', '不赋'])
        self.radiosFiledPrimary = wx.RadioBox(self.complex1Panel, -1, "主键【primary_key】", choices=['是', '否'])
        complex1PanelSizer.Add(self.radiosFiledBlank, 1, wx.EXPAND | wx.ALL, 2)
        complex1PanelSizer.Add(self.radiosFiledNull, 1, wx.EXPAND | wx.ALL, 2)
        complex1PanelSizer.Add(self.radiosFiledPrimary, 1, wx.EXPAND | wx.ALL, 2)
        # self.radiosFiledBlank.SetBackgroundColour(CON_COLOR_RADIO)

        # 混乱布局第2行
        self.complex2Panel = wx.Panel(self.scollPanel)
        complex2PanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.complex2Panel.SetSizer(complex2PanelSizer)
        scollPanelSizer.Add(self.complex2Panel, 0, wx.EXPAND | wx.ALL, 2)

        self.radiosFiledUnique = wx.RadioBox(self.complex2Panel, -1, "值唯一【unique】", choices=['唯一', '不唯一'])
        self.radiosFiledDbIndex = wx.RadioBox(self.complex2Panel, -1, "创建索引【db_index】", choices=['创建', '不创建'])
        self.radiosFiledEditable = wx.RadioBox(self.complex2Panel, -1, "表单显示【editable】", choices=['显示', '不显示'])
        complex2PanelSizer.Add(self.radiosFiledUnique, 1, wx.EXPAND | wx.ALL, 2)
        complex2PanelSizer.Add(self.radiosFiledDbIndex, 1, wx.EXPAND | wx.ALL, 2)
        complex2PanelSizer.Add(self.radiosFiledEditable, 1, wx.EXPAND | wx.ALL, 2)

        # 其它特有字段布局第2行【位置调整至此处，提高使用感】
        self.specialArgs2Panel = wx.Panel(self.scollPanel)
        specialArgs2PanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.specialArgs2Panel.SetSizer(specialArgs2PanelSizer)
        scollPanelSizer.Add(self.specialArgs2Panel, 0, wx.EXPAND | wx.ALL, 2)

        # 其它特有字段布局第2行 - 长度上限【max_length】
        self.maxLengthStaticBox = wx.StaticBox(self.specialArgs2Panel, -1, '长度上限【max_length】')
        self.maxLengthPanel = wx.StaticBoxSizer(self.maxLengthStaticBox, wx.HORIZONTAL)
        specialArgs2PanelSizer.Add(self.maxLengthPanel, 1, wx.EXPAND | wx.ALL, 2)

        self.inputMaxLength = wx.TextCtrl(self.specialArgs2Panel, -1)
        self.maxLengthPanel.Add(self.inputMaxLength, 1, wx.EXPAND | wx.ALL, 2)

        # 其它特有字段布局第2行 - save调用更新日期【auto_now】
        self.radiosAutoNow = wx.RadioBox(self.specialArgs2Panel, -1, "save调用更新日期【auto_now】", choices=['启用', '不启用'])
        specialArgs2PanelSizer.Add(self.radiosAutoNow, 1, wx.EXPAND | wx.ALL, 2)

        # 其它特有字段布局第2行 - 仅创建时一次赋值日期【auto_now_add】
        self.radiosAutoNowAdd = wx.RadioBox(self.specialArgs2Panel, -1, "仅创建时一次赋值日期【auto_now_add】", choices=['启用', '不启用'])
        specialArgs2PanelSizer.Add(self.radiosAutoNowAdd, 1, wx.EXPAND | wx.ALL, 2)

        # 混乱布局第4行
        self.complex4Panel = wx.Panel(self.scollPanel)
        complex4PanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.complex4Panel.SetSizer(complex4PanelSizer)
        scollPanelSizer.Add(self.complex4Panel, 0, wx.EXPAND | wx.ALL, 2)

        # 混乱布局第4行 - 默认值【default】
        defaultValueStaticBox = wx.StaticBox(self.complex4Panel, -1, '默认值【default】（选填）')
        self.defaultValuePanel = wx.StaticBoxSizer(defaultValueStaticBox, wx.HORIZONTAL)
        complex4PanelSizer.Add(self.defaultValuePanel, 1, wx.EXPAND | wx.ALL, 2)

        self.inputDefaultValue = wx.TextCtrl(self.complex4Panel, -1)
        self.defaultValuePanel.Add(self.inputDefaultValue, 1, wx.EXPAND | wx.ALL, 2)

        # 混乱布局第4行 - 表单帮助文本信息【help_text】
        formHelpTextStaticBox = wx.StaticBox(self.complex4Panel, -1, '表单帮助信息【help_text】（选填）')
        self.formHelpTextPanel = wx.StaticBoxSizer(formHelpTextStaticBox, wx.HORIZONTAL)
        complex4PanelSizer.Add(self.formHelpTextPanel, 1, wx.EXPAND | wx.ALL, 2)

        self.inputFormHelpText = wx.TextCtrl(self.complex4Panel, -1)
        self.formHelpTextPanel.Add(self.inputFormHelpText, 1, wx.EXPAND | wx.ALL, 2)

        # 混乱布局第4行 - 表单错误输入提醒【error_messages】
        formErrorMessageStaticBox = wx.StaticBox(self.complex4Panel, -1, '表单错误提醒【error_messages】（选填）')
        self.formErrorMessagePanel = wx.StaticBoxSizer(formErrorMessageStaticBox, wx.HORIZONTAL)
        complex4PanelSizer.Add(self.formErrorMessagePanel, 1, wx.EXPAND | wx.ALL, 2)

        self.inputFormErrorMessage = wx.TextCtrl(self.complex4Panel, -1)
        self.formErrorMessagePanel.Add(self.inputFormErrorMessage, 1, wx.EXPAND | wx.ALL, 2)

        # 其它特有字段布局第1行
        self.specialArgs1Panel = wx.Panel(self.scollPanel)
        specialArgs1PanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.specialArgs1Panel.SetSizer(specialArgs1PanelSizer)
        scollPanelSizer.Add(self.specialArgs1Panel, 0, wx.EXPAND | wx.ALL, 2)

        # 其它特有字段布局第1行 - 文件上传路径【upload_to】
        self.uploadToStaticBox = wx.StaticBox(self.specialArgs1Panel, -1, '文件上传路径【upload_to】')
        self.uploadToPanel = wx.StaticBoxSizer(self.uploadToStaticBox, wx.HORIZONTAL)
        specialArgs1PanelSizer.Add(self.uploadToPanel, 1, wx.EXPAND | wx.ALL, 2)

        self.inputUploadTo = wx.TextCtrl(self.specialArgs1Panel, -1)
        self.uploadToPanel.Add(self.inputUploadTo, 1, wx.EXPAND | wx.ALL, 2)

        # 其它特有字段布局第1行 - 实数总位数【max_digits】
        self.maxDigitsStaticBox = wx.StaticBox(self.specialArgs1Panel, -1, '实数总位数【max_digits】')
        self.maxDigitsPanel = wx.StaticBoxSizer(self.maxDigitsStaticBox, wx.HORIZONTAL)
        specialArgs1PanelSizer.Add(self.maxDigitsPanel, 1, wx.EXPAND | wx.ALL, 2)

        self.inputMaxDigits = wx.TextCtrl(self.specialArgs1Panel, -1)
        self.maxDigitsPanel.Add(self.inputMaxDigits, 1, wx.EXPAND | wx.ALL, 2)

        # 其它特有字段布局第1行 - 小数总位数【decimal_places】
        self.decimalPlacesStaticBox = wx.StaticBox(self.specialArgs1Panel, -1, '小数总位数【decimal_places】（默认为0）')
        self.decimalPlacesPanel = wx.StaticBoxSizer(self.decimalPlacesStaticBox, wx.HORIZONTAL)
        specialArgs1PanelSizer.Add(self.decimalPlacesPanel, 1, wx.EXPAND | wx.ALL, 2)

        self.inputDecimalPlaces = wx.TextCtrl(self.specialArgs1Panel, -1)
        self.decimalPlacesPanel.Add(self.inputDecimalPlaces, 1, wx.EXPAND | wx.ALL, 2)


        # 混乱布局第3行【放在末尾，提升使用感】
        self.complex3Panel = wx.Panel(self.scollPanel)
        complex3PanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.complex3Panel.SetSizer(complex3PanelSizer)
        scollPanelSizer.Add(self.complex3Panel, 0, wx.EXPAND | wx.ALL, 2)

        # 混乱布局第3行 - 与日期组合唯一【unique_for_date】
        choicesFiledUniqueForDateStaticBox = wx.StaticBox(self.complex3Panel, -1, '与日期组合唯一【unique_for_date】（可选）')
        self.choicesFiledUniqueForDatePanel = wx.StaticBoxSizer(choicesFiledUniqueForDateStaticBox, wx.HORIZONTAL)
        complex3PanelSizer.Add(self.choicesFiledUniqueForDatePanel, 1, wx.EXPAND | wx.ALL, 2)

        self.choicesFiledUniqueForDate = wx.Choice(self.complex3Panel, -1, choices=[' ']+['列举当前字段1', ], style = wx.CB_SORT)
        self.choicesFiledUniqueForDatePanel.Add(self.choicesFiledUniqueForDate, 1, wx.EXPAND | wx.ALL, 2)

        # 混乱布局第3行 - 与月份组合唯一【unique_for_month】
        choicesFiledUniqueForMonthStaticBox = wx.StaticBox(self.complex3Panel, -1, '与月份组合唯一【unique_for_month】（可选）')
        self.choicesFiledUniqueForMonthPanel = wx.StaticBoxSizer(choicesFiledUniqueForMonthStaticBox, wx.HORIZONTAL)
        complex3PanelSizer.Add(self.choicesFiledUniqueForMonthPanel, 1, wx.EXPAND | wx.ALL, 2)

        self.choicesFiledUniqueForMonth = wx.Choice(self.complex3Panel, -1, choices=[' ']+['列举当前字段2', ], style = wx.CB_SORT)
        self.choicesFiledUniqueForMonthPanel.Add(self.choicesFiledUniqueForMonth, 1, wx.EXPAND | wx.ALL, 2)

        # 混乱布局第3行 - 与年份组合唯一【unique_for_year】
        choicesFiledUniqueForYearStaticBox = wx.StaticBox(self.complex3Panel, -1, '与年份组合唯一【unique_for_year】（可选）')
        self.choicesFiledUniqueForYearPanel = wx.StaticBoxSizer(choicesFiledUniqueForYearStaticBox, wx.HORIZONTAL)
        complex3PanelSizer.Add(self.choicesFiledUniqueForYearPanel, 1, wx.EXPAND | wx.ALL, 2)

        self.choicesFiledUniqueForYear = wx.Choice(self.complex3Panel, -1, choices=[' ']+['列举当前字段3', ], style = wx.CB_SORT)
        self.choicesFiledUniqueForYearPanel.Add(self.choicesFiledUniqueForYear, 1, wx.EXPAND | wx.ALL, 2)
        
        # 关联关系字段布局1
        self.relationFiledStaticBox = wx.StaticBox(self.scollPanel, -1, '关联关系字段专属参数')
        self.relationFiledPanel = wx.StaticBoxSizer(self.relationFiledStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.relationFiledPanel, 1, wx.EXPAND | wx.ALL, 2)

        # 关联关系字段布局1 - 模型下拉列表选择
        self.relationFiledChoiceModelStaticBox = wx.StaticBox(self.scollPanel, -1, '关联模型')
        self.relationFiledChoiceModelPanel = wx.StaticBoxSizer(self.relationFiledChoiceModelStaticBox, wx.HORIZONTAL)
        self.relationFiledPanel.Add(self.relationFiledChoiceModelPanel, 1, wx.EXPAND | wx.ALL, 2)

        self.choiceSelectModel = wx.Choice(self.scollPanel, -1, choices = [' ']+['self'], style = wx.CB_SORT)
        self.relationFiledChoiceModelPanel.Add(self.choiceSelectModel, 1, wx.EXPAND | wx.ALL, 2)

        # 关联关系字段布局1 - 记录删除规则【on_delete】
        self.relationFiledDelRuleStaticBox = wx.StaticBox(self.scollPanel, -1, '记录删除规则【on_delete】')
        self.relationFiledDelRulePanel = wx.StaticBoxSizer(self.relationFiledDelRuleStaticBox, wx.HORIZONTAL)
        self.relationFiledPanel.Add(self.relationFiledDelRulePanel, 1, wx.EXPAND | wx.ALL, 2)

        self.choiceSelectDelRule = wx.Choice(self.scollPanel, -1, choices = [' ']+['models.CASCADE'], style = wx.CB_SORT)
        self.relationFiledDelRulePanel.Add(self.choiceSelectDelRule, 1, wx.EXPAND | wx.ALL, 2)

        # 关联关系字段布局1 - 备注名【verbose_name】
        self.relationFiledRemarkStaticBox = wx.StaticBox(self.scollPanel, -1, '关联字段备注名【verbose_name】')
        self.relationFiledRemarkPanel = wx.StaticBoxSizer(self.relationFiledRemarkStaticBox, wx.HORIZONTAL)
        self.relationFiledPanel.Add(self.relationFiledRemarkPanel, 1, wx.EXPAND | wx.ALL, 2)

        self.inputRelationRemark = wx.TextCtrl(self.scollPanel, -1)
        self.relationFiledRemarkPanel.Add(self.inputRelationRemark, 1, wx.EXPAND | wx.ALL, 2)

        # Meta选项
        modelMetaStaticBox = wx.StaticBox(self.scollPanel, -1, 'Meta选项（数据表选项）')
        self.modelMetaPanel = wx.StaticBoxSizer(modelMetaStaticBox, wx.HORIZONTAL)
        scollPanelSizer.Add(self.modelMetaPanel, 1, wx.EXPAND | wx.ALL, 2)

        self.modelMetaPanel.Add(wx.StaticText(self.scollPanel, -1, "此处暂时搁置，后期完善。"), 1, wx.EXPAND | wx.ALL, 2)

        self.afterBtns.extend([
            self.btnResetInput, self.btnAddFieldToArea,
            # self.btnExecSave,
        ])

        # 所有的参数
        self.allArgs.extend([
            self.choiceFieldType, # 字段类型选择放这里不合理【暂时不调整】
            self.inputFieldModelName, self.inputFieldDatabaseName, self.inputFieldRemarkName,
            self.radiosFiledBlank, self.radiosFiledNull, self.radiosFiledPrimary, # 英文拼错了，不改了
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
            self.radiosFiledBlank, self.radiosFiledNull, self.radiosFiledPrimary,
            self.radiosFiledUnique, self.radiosFiledDbIndex, self.radiosFiledEditable,
            self.choicesFiledUniqueForDate, self.choicesFiledUniqueForMonth, self.choicesFiledUniqueForYear,
            self.inputDefaultValue, self.inputFormHelpText, self.inputFormErrorMessage,
        ])

        # 私有参数
        self.specialArgs.extend([
            self.maxLengthStaticBox, self.inputMaxLength,
            self.maxDigitsStaticBox, self.inputMaxDigits,
            self.decimalPlacesStaticBox, self.inputDecimalPlaces,
            self.radiosAutoNow, self.radiosAutoNowAdd, 
            self.uploadToStaticBox, self.inputUploadTo,

            # 关联字段专属
            self.relationFiledStaticBox,
            self.relationFiledChoiceModelStaticBox, self.choiceSelectModel,
            self.relationFiledDelRuleStaticBox, self.choiceSelectDelRule,
            self.relationFiledRemarkStaticBox, self.inputRelationRemark,

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

    def onBtnPreview(self, e):
        """预览待插入代码"""

        pre_fields = []

        for _ in self.allRows:

            # 若和默认值一致，则不显式显示参数
            field = ''
            args = []
            field += _['field_name']
            field_type = _['field_type']
            # 位置参数
            if _['remarker'] != _['field_name'].replace('_', ' '): # 默认下划线默认换成空格）
                t = _['remarker']
                args.append(f"'{t}'")

            # 关键字参数
            if _['field_name'] != _['db_column']: # 默认一致，不一致则新增
                t = _['db_column']
                args.append(", db_column='{t}'")
            
            if CON_YES == _['primary_key']:
                args.append(f", primary_key=True")

            pre_fields.append(f"{field} = models.{field_type}({args})")

        TipsMessageOKBox(self, f'{pre_fields}', '预览')

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
            else:
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
        self.tableObjPanel = wx.Panel(self.panel)
        tableObjPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.tableObjPanel.SetSizer(tableObjPanelSizer)
        self.panelSizer.Add(self.tableObjPanel, 1, wx.EXPAND | wx.ALL, 2)
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

    def onGridBtnDelete(self, e):
        """删除行"""
        row_indexs = self.infoGrid.GetSelectedRows()
        t = '、'.join([str(_+1) for _ in row_indexs])
        if len(row_indexs) > 0:
            dlg_tip = wx.MessageDialog(self, f"确认删除第{t}行？一旦删除不可恢复。", CON_TIPS_COMMON, wx.CANCEL | wx.OK)
            if dlg_tip.ShowModal() == wx.ID_OK:
                result = self.removeRows(row_indexs)
                if result:
                    TipsMessageOKBox(self, '删除成功！', '提示')
                else:
                    TipsMessageOKBox(self, f"{'、'.join(result)}删除失败！", '提示')
            dlg_tip.Close(True)
        else:
            TipsMessageOKBox(self, '无选择行可删除。', '警告')

    def _init_header(self):
        """初始化列名"""
        for i,v in enumerate(CON_MODELSCREATEDIALOG_COLS):
            self.infoGrid.SetColLabelValue(i, v)

    def onChoiceFieldType(self, e):
        """选择要新建的字段类型"""
        field_type = e.GetString().strip()

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
        self._unshow_special_args() # 先隐藏所有的特殊参数

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

            # 界面数据全部初始化
            self._disable_all_args()
            self._init_all_args_value()
            self._init_input_args()
            self.choiceFieldType.SetSelection(0) # 单独拎出来初始化【不影响大体功能】

            # 重新开放新增按钮 锁定后触发按钮
            self.btnAddNew.Enable(True)
            self._disable_all_afterBtns()

        dlg_tip.Close(True)


    def _replace01_to_bool(self, v):
        if 0 == v: return CON_YES
        else: return CON_NO

    def removeRows(self, row_indexs):
        """同步删除界面和数据包里的数据"""
        # all([self.infoGrid.DeleteRows(_) for _ in reversed(row_indexs)])
        for i in row_indexs:
            print(self.infoGrid[i])

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
        # for _ in set(self.allArgs)-set(self.commonArgs)-set([self.choiceFieldType,]):
        #     _.Show(False)

        # 其余特殊参数按需开启

    def selectBinaryField(self):
        """字节型字段"""
        self.radiosFiledEditable.SetSelection(1)
        self.maxLengthStaticBox.Show(True)
        self.inputMaxLength.Show(True)
        self.inputMaxLength.Enable(True)

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
        self.maxDigitsStaticBox.Show(True)
        self.inputMaxDigits.Show(True)
        self.decimalPlacesStaticBox.Show(True)
        self.inputDecimalPlaces.Show(True)
        self.maxDigitsStaticBox.Enable(True)
        self.inputMaxDigits.Enable(True)
        self.decimalPlacesStaticBox.Enable(True)
        self.inputDecimalPlaces.Enable(True)

    def selectBooleanField(self):
        """布尔类型字段"""
        self.inputDefaultValue.SetValue('None')

    def selectCharField(self):
        """字符型字段"""
        self.maxLengthStaticBox.Show(True)
        self.inputMaxLength.Show(True)
        self.inputMaxLength.Enable(True)

    def selectTextField(self):
        ...
    def selectEmailField(self):
        """电子邮件字段"""
        self.maxLengthStaticBox.Show(True)
        self.inputMaxLength.Show(True)
        self.inputMaxLength.Enable(True)
        self.inputMaxLength.SetValue('254')

    def selectGenericIPAddressField(self):
        ...
    def selectSlugField(self):
        """字母、数字、连字符字段"""
        self.maxLengthStaticBox.Show(True)
        self.inputMaxLength.Show(True)
        self.inputMaxLength.Enable(True)
        self.inputMaxLength.SetValue('50')

    def selectURLField(self):
        """url字段"""
        self.maxLengthStaticBox.Show(True)
        self.inputMaxLength.Show(True)
        self.inputMaxLength.Enable(True)
        self.inputMaxLength.SetValue('200')

        
    def selectUUIDField(self):
        ...
    def selectDateField(self):
        """日期型字段"""
        self.radiosAutoNow.Show(True)
        self.radiosAutoNowAdd.Show(True)
        self.radiosAutoNow.Enable(True)
        self.radiosAutoNowAdd.Enable(True)
        self.inputDefaultValue.SetValue('date.today')

    def selectDateTimeField(self):
        """长日期字段"""
        self.radiosAutoNow.Show(True)
        self.radiosAutoNowAdd.Show(True)
        self.radiosAutoNow.Enable(True)
        self.radiosAutoNowAdd.Enable(True)
        self.inputDefaultValue.SetValue('timezone.now')

    def selectDurationField(self):
        """时间戳字段"""

    def selectTimeField(self):
        """时间字段"""
        self.radiosAutoNow.Show(True)
        self.radiosAutoNowAdd.Show(True)
        self.radiosAutoNow.Enable(True)
        self.radiosAutoNowAdd.Enable(True)

    def selectFileField(self):
        """文件字段"""
        self.maxLengthStaticBox.Show(True)
        self.inputMaxLength.Show(True)
        self.inputMaxLength.Enable(True)
        self.inputMaxLength.SetValue('100')

        self.uploadToStaticBox.Show(True)
        self.inputUploadTo.Show(True)
        self.inputUploadTo.Enable(True)
        self.inputUploadTo.SetValue(r'uploads/%Y/%m/%d/')

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