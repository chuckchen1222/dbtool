# encoding: utf-8
"""
Author: chzhang@tripadvisor.com
Date: 2019-04-28
Version: 20190428
"""

import re

class SQLParse():
    def __init__(self, sql):
        self.sql = sql
    
    # 格式化SQL
    def formatSQL(self):
        f_sql = self.sql.strip().replace('\n',' ')
        return f_sql
    
    # 判断DML类型。
    def getSQLOpType(self):
        f_sql = self.formatSQL()
        sql_prefix = f_sql[:10].lower()
        if 'insert' in sql_prefix:
            return 'i'
        elif 'delete' in sql_prefix:
            return 'd'
        elif 'update' in sql_prefix:
            return 'u'
        elif 'truncate' in sql_prefix:
            return '0'
    
    # SQL末端加上returning
    def addReturningToSQL(self):
        if self.sql.strip()[-1] == ';':
            sql = self.sql.strip()[:-1]
        else:
            sql = self.sql
        returning_sql = sql + ' returning *;'
        return returning_sql
    
    # 判断SQL中是否包含where clause
    def isIncludeWhere(self):
        f_sql = self.formatSQL()
        if ' where ' in f_sql:
            return 1
        else:
            return 0    # error: Please check SQL.
    
    # 解析update语句，取出tablename,更新内容, 更新条件
    def updateSQLParse(self):
        sql = self.formatSQL()
        c = r'update (\w*) set (.*) where (.*)'
        s = re.match(c, sql, re.I|re.M)
        return s.groups()
    
    def backupUpdateOldValue(self):
        sql = self.updateSQLParse()
        tablename = sql[0]
        condition = sql[2]
        backSQL = ''' select * from %s where %s ''' % (tablename, condition)
        return backSQL

    def getSQLCommand(self):
        op = self.getSQLOpType()
        if op == 'i':
            sqlcommand = self.addReturningToSQL()
            yield sqlcommand
        elif op == 'd':
            isContainWhere = self.isIncludeWhere()
            if isContainWhere:
                sqlcommand = self.addReturningToSQL()
                yield sqlcommand
            else:
                # need to define some error for this
                # e1 meas 'no where in SQL'
                yield 'e1'
        elif op == 'u':
            isContainWhere = self.isIncludeWhere()
            if isContainWhere:
                backupsql = self.backupUpdateOldValue()
                yield backupsql
                yield self.sql
            else:
                yield 'e1'
        elif not op:
            yield 'e1'
            
####################
# 步骤：
# 1. 判断SQL类型(insert, delete, update)
# 2. insert
# 2.1 加上 " returning *"
# 2.2 执行，保存执行结果
# 3. delete
# 3.1 判断有无where条件。
# 3.2 加上 " returning *"
# 3.3 执行，保存执行结果
# 4. update
# 4.1 判断有无where条件。
# 4.2 拆解语句
# 4.3 拼凑backup语句，并执行，保存结果
# 4.4 执行，并保存结果
####################            

