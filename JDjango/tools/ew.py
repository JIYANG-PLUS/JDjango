# python 获取sqlite3数据库mydb.db中的表名和表字段名
 
import os
print(os.getcwd())
import sqlite3
print(os.getcwd())
conn=sqlite3.connect('./db.sqlite3')
cu=conn.cursor()
 
#获取表名，保存在tab_name列表
cu.execute("select name from sqlite_master where type='table'")
tab_name=cu.fetchall()
tab_name=[line[0] for line in tab_name]
 
#获取表的列名（字段名），保存在col_names列表,每个表的字段名集为一个元组
col_names=[]
for line in tab_name:
    cu.execute('pragma table_info({})'.format(line))
    col_name=cu.fetchall()
    col_name=[x[1] for x in col_name]
    col_names.append(col_name)
    col_name=tuple(col_name)
 
#之所以保存为元组，一是可避免误操作修改字段名，二是元组巧用转化字符串，可
#直接用于SQL的insert语句中。例如下面代码可得到第一个表的带括号字段名集合：
'''
    sql_col_name=str(col_names[0]).replace('\'','')
'''
 
print(tab_name)
print(col_names)

cu.execute("PRAGMA database_list;")
curr_table = cu.fetchall()
print(curr_table)



# https://www.sqlite.org/pragma.html#pragma_table_info
# SQLite3官方文档
            