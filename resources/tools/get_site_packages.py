import sysconfig

# from pprint import pprint
# pprint(sysconfig.get_paths())

print(sysconfig.get_paths()["purelib"]) # 虚拟环境 site-packages 的路径
