import xml.etree.ElementTree as ET

tree = ET.parse('test.xml') # 从文件读取
root = tree.getroot()
# 从字符串读取
# root = ET.fromstring(country_data_as_string)


print(root.tag) # 查看标签
print(root.attrib) # 查看属性
print(root.text) # 查看文本内容（不读取子标签）
# print(root[0][1].text) # 索引取值


# 迭代子节点
for child in root:
    print(child.tag, child.attrib)


# 遍历所有子集
for neighbor in root.iter('name'):
    print('HHH: ', neighbor.attrib)


# 查找当前元素的直接子元素中带有特定标签的元素
# Element.findall("property")


# Element.find("property") 找带有特定标签的第一个子级
# Element.text 访问文本内容
# Element.get 访问元素的属性
