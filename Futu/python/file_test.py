# -*- coding: utf-8 -*-

import os

# os.mkdir('./newdir')
file = open('./test.txt', 'w')
content = '''我是文件内容
内容是
如何做好量化投资
'''
file.write(content)
file.close()

file = open('./test.txt', 'r')
while True:
    line = file.readline()
    if len(line) == 0:
        break
    print(line)

file.seek(0)
for u in file:
    print(u)

file.close()
