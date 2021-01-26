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
CON_COLOR_MAIN = '#f0efe0' # 程序主色调
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

# dialogOption.py
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
CON_FIELD_TYPES = [
    'BinaryField--【字节型字段】',
    'SmallIntegerField--【16位整型字段】',
    'PositiveSmallIntegerField--【16位正整型字段】',
    'IntegerField--【32位整型字段】',
    'PositiveIntegerField--【32位正整型字段】',
    'BigIntegerField--【64位整型字段】',
    'AutoField--【32位自增型字段】',
    'BigAutoField--【64位自增型字段】',
    'FloatField--【浮点型字段】',
    'DecimalField--【高精度浮点型字段】',
    'BooleanField--【布尔类型字段】',
    'CharField--【字符型字段】',
    'TextField--【大文本字段】',
    'EmailField--【邮箱字段】',
    'GenericIPAddressField--【IPv4IPv6字段】',
    'SlugField--【只包含字母、数字、下划线或连字符】',
    'URLField--【路由字段】',
    'UUIDField--【uuid字段】',
    'DateField--【日期型字段】',
    'DateTimeField--【长日期字段】',
    'DurationField--【时间戳字段】',
    'TimeField--【时间字段】',
    'FileField--【文件上传字段】',
    'ImageField--【图片上传字段】',
    'FilePathField--【文件路径上传字段】',
    'ForeignKey--【多对一字段】',
    'ManyToManyField--【多对多字段】',
    'OneToOneField--【一对一字段】',
]

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