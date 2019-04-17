# encoding: utf-8
"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190318
"""

import sys
sys.path.append("libs/")
import dbutils

def getDestHost(dbname, env_type):
    query_exclude_db = "('tripmaster_secure','tripmaster_pii')"
    dbops = dbutils.DataBase(host='dbtool01s', database='tripmaster_dbtool', user='dbadmin', password='', port=5432)
    if env_type == 'dev':
        env = ('dev') 
        sql_dbinfo = 'select v_hostname from db_ops_database where dbname = \'%s\' and v_hostname not in (\'syncdb01c\',\'sync03s\') and env in (\'%s\') ' % (dbname, env)
    elif env_type == 'sc':
        env = ('sc')
        sql_dbinfo = 'select v_hostname from db_ops_database where dbname = \'%s\' and v_hostname not in (\'syncdb01c\',\'sync03s\') and env in (\'%s\') ' % (dbname, env)
    elif env_type == 'livesite':
        env = ('live')
        sql_dbinfo = 'select v_hostname from db_ops_database where dbname = \'%s\' and env = \'live\' and dbname not in %s and v_hostname in (select distinct v_hostname from db_ops_host where dc_id_id in (select id from db_ops_datacenter where is_live = \'false\')) ' % (dbname, query_exclude_db)
    host = dbops.query(sql_dbinfo)
    if host:
        return host[0][0]
    else:
        return None

def pgExecSQL(host='localhost', port=5432, dbname='postgresql', user='dbadmin', password='', sql='select 1;'):
    db = dbutils.DataBase(host=host, database=dbname, user=dbname, password=password, port=port)
    f_sql = sql.strip()
    if f_sql[-1] == ';':
        f_sql = f_sql[:-1]
    f_sql = f_sql.strip()
    if "limit" not in f_sql[-15:]:
        f_sql = f_sql + ' limit 10000'
    query_result,e = db.queryWithColName(f_sql)
    return query_result,e

def pgSQLexplain(host='localhost', port=5432, dbname='postgresql', user='dbadmin', password='', sql='select 1;'):
    db = dbutils.DataBase(host=host, database=dbname, user=user, password=password, port=port)
    f_sql = sql.strip()
    if f_sql[-1] == ';':
        f_sql = f_sql[:-1]
    f_sql = f_sql.strip()
    if "limit" not in f_sql[-15:]:
        f_sql = f_sql + ' limit 10000'
    explain,e = db.explain(sql)
    return explain,e

def MySQLExecSQL(host='localhost', port=3306, dbname='mysql', user='root', password='', sql='select 1;'):
    db = dbutils.MySQLDataBase(host=host, database=dbname, user=user, password=password, port=port)
    f_sql = sql.strip()
    if f_sql[-1] == ';':
        f_sql = f_sql[:-1]
    f_sql = f_sql.strip()
    if "limit" not in f_sql[-15:]:
        f_sql = f_sql + ' limit 10000'
    f_sql = f_sql + (';')
    query_result, e = db.queryWithColName(f_sql)
    return query_result, e


def MSSQLExecSQL(server='localhost', dbname='master', user='sa', password='', sql='select 1;'):
    db = dbutils.MSSQLDataBase(server=server, database=dbname, user=user, password=password)
    f_sql = sql.strip()
    if f_sql[-1] == ';':
        f_sql = f_sql[:-1]
    f_sql = f_sql.strip()
    if "select top" not in f_sql[15:]:
        f_sql = f_sql.replace('select ','select top 10000 ', 1)
    f_sql = f_sql + (';')
    query_result, e = db.queryWithColName(f_sql)
    return query_result, e