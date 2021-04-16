from ..common import *
from ..basetools import *
from ..exceptions import *
from .sets import *

__all__ = [
    'refresh_config', # 更新配置文件config.json
    'update_settings_DTATBASES', # 数据库引擎更换
]

def refresh_config()->None:
    """初始化配置文件"""
    PROJECT_CONFIG = get_configs(CONFIG_PATH)
    PROJECT_BASE_DIR = PROJECT_CONFIG['dirname']
    DIRSETTINGS = os.path.join(PROJECT_BASE_DIR, PROJECT_CONFIG['project_name'], 'settings.py')
    temp_configs = {} # 全局配置文件待写入
    temp_configs['dirname'] = PROJECT_BASE_DIR # 项目路径
    temp_configs['project_name'] = os.path.basename(PROJECT_BASE_DIR) # 项目名称
    apps = os.listdir(PROJECT_BASE_DIR) # 所有的应用程序（包含主程序）
    temp_configs['app_names'] = [_ for _ in apps if os.path.exists(os.path.join(PROJECT_BASE_DIR, _, 'migrations'))] # 以迁移目录为依据进行筛选
    set_configs(DIRSETTINGS, temp_configs)
    dump_json(CONFIG_PATH, temp_configs)  # 写入配置文件

def update_settings_DTATBASES(db_type: str, *args, **kwargs)->None:
    """更新数据库引擎"""
    if db_type not in ('sqlite', 'mysql',):
        raise UnsupportDatabaseException('暂不支持的数据库引擎')

    if 'mysql' == db_type:
        DB_TYPE_NAME = 'mysql.django'
    elif 'sqlite' == db_type:
        DB_TYPE_NAME = 'sqlite.django'
    else:
        DB_TYPE_NAME = 'sqlite.django' # 默认 SQLite3 引擎

    config = get_configs(CONFIG_PATH)
    root_path = config['dirname']
    project_name = config['project_name']
    root_settingspy = os.path.join(root_path, project_name, 'settings.py')

    DAtABASES_content = get_list_patt_content(PATT_DATABASES, root_settingspy, leftCode='{', rightCode='}')

    template_str = get_content(DB_TYPE_NAME, concat=['settings',], replace=True, 
        engine = kwargs['engine'], 
        database_name = kwargs['database_name'], 
        username = kwargs['username'], 
        password = kwargs['password'], 
        ip = kwargs['ip'], 
        port = kwargs['port'], 
        test = kwargs['test']
    )
    whole_text = read_file(root_settingspy)
    replace_text = whole_text.replace(DAtABASES_content, ''.join(template_str))
    write_file(root_settingspy, content=replace_text)

    refresh_config()
