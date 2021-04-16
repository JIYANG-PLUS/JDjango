import json
from .. settings import KV_PATH

with open(KV_PATH, encoding='utf-8') as f:
    PROPERTY_CONFIGS = json.load(f)

class Propertys:

    PROPERTY_CONFIGS = PROPERTY_CONFIGS

    def __init__(self) -> None: pass

    @classmethod
    def combine_objs(cls):
        """整合所有的属性对象"""
        combine_objs = []
        for page in cls.PROPERTY_CONFIGS:
            for category in page["categorys"]:
                combine_objs.extend(category["objs"])
        return combine_objs

    @classmethod
    def combine_matchings(cls):
        """整合所有的 matching 对象"""
        conbine_matchings = {}
        for page in cls.PROPERTY_CONFIGS:
            conbine_matchings.update(page["matching"])
        return conbine_matchings

    @classmethod
    def find_property_by_key(cls, key: str):
        """通过属性 key 获取 属性节点"""
        for obj in cls.combine_objs():
            if key.lower() == obj["key"].lower():
                return obj
        return {}

    @classmethod
    def transfer_value(cls, k: str, v):
        """键值转换，适配配置（可读化名称转变为程序可认知的名称）"""
        obj = cls.find_property_by_key(k)
        if 'X_FRAME_OPTIONS' == k:
            if None == v: return False
            if isinstance(v, str): return True
            return v
        if 'EnumProperty'.lower() == obj["type"].lower():
            for ch_name, v_list in cls.combine_matchings().items():
                if v in v_list:
                    return obj["labels"].index(ch_name)
            return None
        return v

    @classmethod
    def get_default_value_by_key(cls, key: str):
        """通过属性的 key 获取 value"""
        for obj in cls.combine_objs():
            if key == obj["key"]:
                return obj["default"]
        return None

    @classmethod
    def judge_need_insert(cls, k, v):
        """判断配置文件是否需要写入（暂时不跟进）"""
        default_v = cls.get_default_value_by_key(k)
        if default_v == v:
            return False
        return True

    @classmethod
    def get_realname_by_readname(cls, key, index):
        """通过可读名称获取实际可用名称"""
        obj = cls.find_property_by_key(key)
        label = obj["labels"][index]
        return cls.combine_matchings()[label][0]
