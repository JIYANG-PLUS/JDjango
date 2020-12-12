import os
import xml.etree.ElementTree as ET

TREE = ET.parse('./environment.xml')
ROOT = TREE.getroot()


print(ROOT[1][0].text)
