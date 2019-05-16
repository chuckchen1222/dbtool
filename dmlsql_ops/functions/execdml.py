# encoding: utf-8
"""
Author: chzhang@tripadvisor.com
Date: 2019-04-29
Version: 20190429
"""

import sys
sys.path.append("libs/")
import dbutils
from .sqlparse import SQLParse
import paramiko

# 解析每条SQL，解析出需要备份的SQL，并去执行
def getAllBackupSQLs(sql):
    backup_sql = []
    if isinstance(sql,list):
        sql = " ".join(sql)
    sqls = sql.split(";")
    for i in sqls:
        if i:
            i_sql = SQLParse(i)
            op = i_sql.getSQLOpType()
            if op == 'u':
                if not i_sql.isIncludeWhere():
                    backup_sql.clear()
                    backup_sql.append('error')
                    return backup_sql
                bak_sql = i_sql.backupUpdateOldValueSQL()
                backup_sql.append(bak_sql)
            elif op == 'd':
                if not i_sql.isIncludeWhere():
                    backup_sql.clear()
                    backup_sql.append('error')
                    return backup_sql
                bak_sql = i_sql.backupDeleteOldValueSQL()
                backup_sql.append(bak_sql)
            elif op == 0:
                backup_sql.clear()
                backup_sql.append('error')
    return backup_sql


####################
# 在sync01s 执行命令
####################
def ExecRemoteHost(func):
    def wrapper(*args, **kwargs):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('sync01s.daodao.com', 22, timeout=20)
            commands = func(*args, **kwargs)
            for command in commands:
                if command == "error":
                    result = ''
                    error = [('error'),]
                else:
                    stdin, stdout, stderr = ssh.exec_command(command)
                    result = stdout.readlines()
                    error = stderr.readlines()
                yield result , error
        except Exception as e:
            return e
        finally:
            ssh.close()
    return wrapper

# 根据 dbname 找 Host(primary)
def getLiveDBHost(dbname):
    sql = '''select v_hostname from db_ops_database  
where 
  (env = 'live' and pgsync_mode <> 'ro' 
  and topology = 'dbw' and is_pgsync = 't' 
  and dbname not in ('tripmaster_schema','site_config','site_instrumentation') 
  and dbname = \'%s\')  
or 
  (env = 'sc' and pgsync_mode <> 'ro'
  and dbname not in ('tripmaster_schema','site_config','site_instrumentation')
  and v_hostname not in ('dbw01s','dbw02s','dbw03s','syncdb01c','sync03s','tm01c','tm04c','tm01s','rivendell') 
  and dbname = \'%s\')
    ''' % (dbname,dbname)
    db = dbutils.DataBase(host='dbtool01s.daodao.com',database='tripmaster_dbtool')
    v_hostname = db.query(sql)
    return v_hostname

@ExecRemoteHost
def execSchemaChangeRomteCommand(host, dbname, sql):
    command = '''psql -U %s -d %s -h %s -At -c "%s" ''' % (dbname, dbname, host, sql)
    yield command
