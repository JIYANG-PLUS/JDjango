import sys

filename, mode, content, *_ = sys.argv

if 'print' == mode:
    print(content)