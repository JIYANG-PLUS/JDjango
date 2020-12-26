import datetime, json

LEVEL = {
    1: '【success】',
    2: '【warning】',
    3: '【error】',
}


def out_infos(info, level=None):
    d = datetime.datetime.now()
    if level:
        l_info = LEVEL[level]
    else:
        l_info = ''
    return f'{d:%Y/%m/%d %H:%M:%S}{l_info}：{info}\n'


def out_command_infos(info):
    return f'>>> {info}\n'


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content


def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def dump_json(file_name, configs):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(configs, f, indent=4)

def get_configs(path):
    with open(path, 'r', encoding='utf-8') as f:
        configs = json.load(f)
    return configs

def new_file(name, content=None):
    with open(name, 'w', encoding='utf-8') as f:
        if content: f.writelines(content)

