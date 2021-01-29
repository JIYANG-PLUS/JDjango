# mainFrame.py
CON_CONTROL_CHECK = 'check'
CON_CONTROL_FIX = 'fix'
CON_CONTROL_CREATE = 'create'
CON_CONTROL_OTHER = 'other'

CON_JDJANGO_TITLE = 'JDjango-V1.1.1'
CON_TIPS_COMMON = '提示信息'

CON_COLOR_GREY = '#4f5049' # 灰色
CON_COLOR_WHITE = '#ededed' # 白色
CON_COLOR_BLACK = '#000000' # 纯黑
CON_COLOR_BLUE = '#0000ff' # 蓝色
CON_COLOR_MAIN = '#fbe4d5' # 程序主色调
CON_COLOR_RADIO = '#d2dce7'

CON_MSG_PROGRESS_USE = """
    MacOS：
    查看PID：sudo lsof -i:8080
    终止进程：sudo kill PID


    Windows：
    查看所有端口占用情况：netstat -ano
    查看指定端口：netstat -ano |findstr "端口号"
    查看占用端口的进程：tasklist |findstr "进程id号"
    杀进程：taskkill /f /t /im "进程id或者进程名称"
"""

# sqliteFrame.py
CON_SQLITE3_TITLE = 'SQLite3管理工具-V1.0.0'
CON_RECOGNITION_TITLE = '数字图片识别工具-V1.0.0'
CON_ENCRYPTION_TITLE = '加解密工具-V0.0.1'

# dialogOption.py
# 下面两个常量主要用于表格的临时展示
CON_MODELSCREATEDIALOG_COLS = (
    '字段属性名',
    '数据库列名',
    '字段备注',
    '字段类型',
    '为空时赋NULL',
    '允许为空',
    '默认值',
    '字段值唯一',
    '长度上限',
    '实数总位数',
    '小数位数',
    '创建索引',
    '主键',
    '表空间',
    '可选列表',
    '日期组合唯一',
    '月份日期组合唯一',
    '年份日期组合唯一',
    '表单错误输入提醒',
    '表单可编辑',
    '表单帮助文本信息',
    '字段校验器',
    '每次保存时更新时间',
    '仅新增时赋值时间',
    '文件上传路径',
)
CON_ARGS_NAME_DICT = {
    '字段属性名' : 'field_name',
    '数据库列名' : 'db_column',
    '字段备注' : 'remarker',
    '字段类型' : 'field_type',
    '允许为空' : 'blank',
    '为空时赋NULL' : 'null',
    '默认值' : 'default',
    '主键' : 'primary_key',
    '字段值唯一' : 'unique',
    '日期组合唯一' : 'unique_for_date',
    '月份日期组合唯一' : 'unique_for_month',
    '年份日期组合唯一' : 'unique_for_year',
    '创建索引' : 'db_index',
    '表空间' : 'db_tablespace',
    '表单错误输入提醒' : 'error_messages',
    '表单可编辑' : 'editable',
    '表单帮助文本信息' : 'help_text',
    '字段校验器' : 'validators',
    '可选列表' : 'choices',
    '长度上限' : 'max_length',
    '实数总位数' : 'max_digits',
    '小数位数' : 'decimal_places',
    '文件上传路径' : 'upload_to',
    '每次保存时更新时间' : 'auto_now',
    '仅新增时赋值时间' : 'auto_now_add',
}

CON_VIEW_CHOICES = [
    '简单函数视图'
    , '简单类视图'
    , '简单列表视图'
    , '快速模板视图'
    , '简单详细视图'
]

# 字段下拉选择
CON_BINARYFIELD = '字节--BinaryField--【字节型字段】'
CON_SMALLINTEGERFIELD = '整型--SmallIntegerField--【16位整型字段】'
CON_POSITIVESMALLINTEGERFIELD = '整型--PositiveSmallIntegerField--【16位正整型字段】'
CON_INTEGERFIELD = '整型--IntegerField--【32位整型字段】'
CON_POSITIVEINTEGERFIELD = '整型--PositiveIntegerField--【32位正整型字段】'
CON_BIGINTEGERFIELD = '整型--BigIntegerField--【64位整型字段】'
CON_AUTOFIELD = '整型--AutoField--【32位自增型字段】'
CON_BIGAUTOFIELD = '整型--BigAutoField--【64位自增型字段】'
CON_FLOATFIELD = '浮点型--FloatField--【浮点型字段】'
CON_DECIMALFIELD = '浮点型--DecimalField--【高精度浮点型字段】'
CON_BOOLEANFIELD = '布尔型--BooleanField--【布尔类型字段】'
CON_CHARFIELD = '字符型--CharField--【字符型字段】'
CON_TEXTFIELD = '字符型--TextField--【大文本字段】'
CON_EMAILFIELD = '字符型--EmailField--【邮箱字段】'
CON_IPADRESSFIELD = '字符型--GenericIPAddressField--【IPv4IPv6字段】'
CON_SLUGFIELD = '字符型--SlugField--【只包含字母、数字、下划线或连字符】'
CON_URLFIELD = '字符型--URLField--【路由字段】'
CON_UUIDFIELD = '字符型--UUIDField--【uuid字段】'
CON_DATEFIELD = '日期型--DateField--【日期型字段】'
CON_DATETIMEFIELD = '日期型--DateTimeField--【长日期字段】'
CON_DURATIONFIELD = '日期型--DurationField--【时间戳字段】'
CON_TIMEFIELD = '日期型--TimeField--【时间字段】'
CON_FILEFIELD = '文件型--FileField--【文件上传字段】'
CON_IMAGEFIELD = '文件型--ImageField--【图片上传字段】'
CON_FILEPATHFIELD = '文件型--FilePathField--【文件路径上传字段】'
CON_FOREIGNFIELD = '关联型--ForeignKey--【多对一字段】'
CON_MANYTOMANYFIELD = '关联型--ManyToManyField--【多对多字段】'
CON_ONETOONEFIELD = '关联型--OneToOneField--【一对一字段】'
CON_SPLIT_STR = '------------------------------------------------------------------'
CON_FIELD_TYPES = [
    CON_SMALLINTEGERFIELD,
    CON_POSITIVESMALLINTEGERFIELD,
    CON_INTEGERFIELD,
    CON_POSITIVEINTEGERFIELD,
    CON_BIGINTEGERFIELD,
    CON_AUTOFIELD,
    CON_BIGAUTOFIELD,
    CON_SPLIT_STR,
    CON_FLOATFIELD,
    CON_DECIMALFIELD,
    CON_SPLIT_STR,
    CON_CHARFIELD,
    CON_TEXTFIELD,
    CON_EMAILFIELD,
    CON_IPADRESSFIELD,
    CON_SLUGFIELD,
    CON_URLFIELD,
    CON_UUIDFIELD,
    CON_SPLIT_STR,
    CON_DATEFIELD,
    CON_DATETIMEFIELD,
    CON_DURATIONFIELD,
    CON_TIMEFIELD,
    CON_SPLIT_STR,
    CON_FILEFIELD,
    CON_IMAGEFIELD,
    CON_FILEPATHFIELD,
    CON_SPLIT_STR,
    CON_BINARYFIELD,
    CON_SPLIT_STR,
    CON_BOOLEANFIELD,
    CON_SPLIT_STR,
    CON_FOREIGNFIELD,
    CON_MANYTOMANYFIELD,
    CON_ONETOONEFIELD,
]

def con_getFieldTypeName(name: str):
    """获取字段类型名称"""
    return [_ for _ in name.split('--') if _][1]

# 所有的文本类字段类型
CON_CHAR_FIELDS = (
    'CharField',
    'TextField',
    'EmailField',
    'GenericIPAddressField',
    'SlugField',
    'URLField',
    'UUIDField',
)

# 所有拥有max_length属性的字段类型
CON_OWN_MAX_LENGTH_FILEDS = (
    'BinaryField',
    'CharField',
    'EmailField',
    'SlugField',
    'URLField',
    'FileField',
)

# 日期相关的字段类型
CON_DATE_FIELDS = (
    'DateField',
    'DateTimeField',
    'DurationField',
    'TimeField',
)

CON_YES = '是'
CON_NO = '否'
