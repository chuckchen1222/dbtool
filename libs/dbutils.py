# -*- coding: UTF-8 -*-
"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190318
"""
import psycopg2
import pymysql
import pymssql

class DataBase():
    """
    DB utils.
    Usage:
    1. connect DB to execute
    db = DataBase(host='XX', database='XXX', user='XXX', password='', port=5432)
    conn = dbops.get_conn()
    cur = dbops.get_cursor(conn)
    result = cur.execute(sql)
    test = cur.fetchone()
    results = dbops.explain(sql)
    # print results
    for i in results:
        print (i[0])
    2. execute query or execute DML/DDL
    db.query(sql)
    db.update(sql)
    """
    def __init__(self, host='dbtool01s.daodao.com', database='tripmaster_dbtool', user='dbadmin', password = '', port=5432):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self._conn = self.get_conn()
        if (self.get_conn):
            self._cursor = self.get_cursor(self._conn)

    # get connect
    def get_conn(self):
        conn = psycopg2.connect(host = self.host, database = self.database, user = self.user, password = self.password, port = self.port)
        return conn

    # get cursor
    def get_cursor(self,conn):
        return conn.cursor()

    # close connect
    def conn_close(conn):
        if conn != None:
            conn.close()

    # close cursor
    def cursor_close(self,cursor):
        if cursor != None:
            cursor.close()

    # close all
    def close(self, cursor, conn):
        cursor_close(cursor)
        conn_close(conn)

    # query SQL without columns, only data. limit 3000.
    def query(self, sql):
        res = ''
        if (self._conn):
            try:
                self._cursor.execute(sql)
                res = self._cursor.fetchmany(5000)
            except Exception as e:
                res = False
                print (e)
        return res

    # query SQL with columns. limit 3000
    def queryWithColName(self, sql):
        result = []
        res = ''
        error = []
        if (self._conn):
            try:
                self._cursor.execute(sql)
                cols = [tuple([desc[0] for desc in self._cursor.description])]
                res = self._cursor.fetchmany(5000)
                result = cols + res
            except Exception as e:
                result = False
                error.append(e)
        return result, error

    # 
    def update(self, sql):
        flag = False
        exception = ''
        if (self._conn):
            try:
                self._cursor.execute(sql)
                self._conn.commit()
                flag = True
            except Exception as e:
                flag = False
                exception = e
        return flag, exception

    def explain(self, sql):
        res = ''
        error = []
        if (self._conn):
            try:
                self._cursor.execute('explain ' + sql)
                res = self._cursor.fetchall()
            except Exception as e:
                res = False
                error.append(e)
        return res,error


class MySQLDataBase():
    def __init__(self, host, database, user, password, port=3306):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self._conn = self.get_conn()
        if (self.get_conn):
            self._cursor = self.get_cursor(self._conn)

    # get connect
    def get_conn(self):
        conn = pymysql.connect(host = self.host, database = self.database, user = self.user, password = self.password, port = self.port)
        return conn

    # get cursor
    def get_cursor(self,conn):
        return conn.cursor()

    # close connect
    def conn_close(conn):
        if conn != None:
            conn.close()

    # close cursor
    def cursor_close(self,cursor):
        if cursor != None:
            cursor.close()

    # close all
    def close(self, cursor, conn):
        cursor_close(cursor)
        conn_close(conn)

    # query SQL without columns, only data. limit 3000.
    def query(self, sql):
        res = ''
        if (self._conn):
            try:
                self._cursor.execute(sql)
                res = self._cursor.fetchmany(5000)
            except Exception as e:
                res = False
                print (e)
        return res

    # query SQL with columns. limit 3000
    def queryWithColName(self, sql):
        result = []
        res = ''
        error = []
        if (self._conn):
            try:
                self._cursor.execute(sql)
                cols = [tuple([desc[0] for desc in self._cursor.description])]
                res = list(self._cursor.fetchmany(5000))
                result = cols + res
            except Exception as e:
                result = False
                error.append(e)
        return result, error

    # 
    def update(self, sql):
        flag = False
        if (self._conn):
            try:
                self._cursor.execute(sql)
                self._conn.commit()
                flag = True
            except Exception as e:
                flag = False
                print (e)
        return flag

    def explain(self, sql):
        res = ''
        error = []
        if (self._conn):
            try:
                self._cursor.execute('explain ' + sql)
                res = self._cursor.fetchall()
            except Exception as e:
                res = False
                error.append(e)
        return res,error

class MSSQLDataBase():
    def __init__(self, server, user, password, database):
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self._conn = self.get_conn()
        if (self.get_conn):
            self._cursor = self.get_cursor(self._conn)
    
    # get connect
    def get_conn(self):
        conn = pymssql.connect(server = self.server, database = self.database, user = self.user, password = self.password)
        return conn

    # get cursor
    def get_cursor(self,conn):
        return conn.cursor()

    # close connect
    def conn_close(conn):
        if conn != None:
            conn.close()

    # close cursor
    def cursor_close(self,cursor):
        if cursor != None:
            cursor.close()

    # close all
    def close(self, cursor, conn):
        cursor_close(cursor)
        conn_close(conn)

    # query SQL without columns, only data. limit 5000.
    def query(self, sql):
        res = ''
        if (self._conn):
            try:
                self._cursor.execute(sql)
                res = self._cursor.fetchmany(5000)
            except Exception as e:
                res = False
                print (e)
        return res

    # query SQL with columns. limit 5000
    def queryWithColName(self, sql):
        result = []
        res = ''
        error = []
        if (self._conn):
            try:
                self._cursor.execute(sql)
                cols = [tuple([desc[0] for desc in self._cursor.description])]
                res = list(self._cursor.fetchmany(5000))
                result = cols + res
            except Exception as e:
                result = False
                error.append(e)
        return result, error   

    def update(self, sql):
        flag = False
        if (self._conn):
            try:
                self._cursor.execute(sql)
                self._conn.commit()
                flag = True
            except Exception as e:
                flag = False
                print (e)
        return flag


