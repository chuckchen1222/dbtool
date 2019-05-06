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
    import_sql = SQLParse(sql)
    sql_commands = import_sql.getSQLCommand()
    for sql_command in sql_commands:
        if sql_command not in ['e1']:
            command = '''psql -U %s -d %s -h %s -At -c "%s" ''' % (dbname, dbname, host, sql_command)
            yield command
        else:
            yield "error"




