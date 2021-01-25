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
CON_COLOR_MAIN = '#93c2f5' # 程序主色调
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

# dialogOption.py
CON_MODELSCREATEDIALOG_COLS = (
    '列名',
    '主键',
    '允许为空',
    'null值',
    '默认值',
    '字段值唯一',
    '创建索引',
    '可选列表',
    '日期组合唯一',
    '月份日期组合唯一',
    '年份日期组合唯一',
    '表单错误输入提醒',
    '表单可编辑',
    '表单帮助文本信息',
    'max_length',
    'max_digits',
    'decimal_places',
    'auto_now',
    'auto_now_add',
    'upload_to',
)
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
]