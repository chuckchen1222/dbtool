# encoding: utf-8
"""
Author: chzhang@tripadvisor.com
Date: 2019-04-17
Version: 20190422
"""
from libs import dbutils
import paramiko

def getHostFromDbName(dbname,env):
    sql = '''select v_hostname from db_ops_database 
    where dbname = \'%s\'
      and env = \'%s\'
      and v_hostname not in (\'tm01c\',\'tm04c\',\'syncdb01c\',\'tm01s\')
    ''' % (dbname, env)
    db = dbutils.DataBase(host='dbtool01s.daodao.com')
    v_hostname = db.query(sql)
    return v_hostname

def getHostFromDbnameExcludeHost(dbname, env, exclude_host):
    sql = '''select v_hostname from db_ops_database 
    where dbname = \'%s\'
      and env = \'%s\'
      and v_hostname not in (\'tm01c\',\'tm04c\',\'syncdb01c\',\'tm01s\')
      and v_hostname <> \'%s\'
    ''' % (dbname, env, exclude_host )
    db = dbutils.DataBase(host='dbtool01s.daodao.com')
    v_hostname = db.query(sql)
    return v_hostname

def getTMHostFromTool():
    sql = '''select v_hostname from db_ops_database 
    where dbname = \'tripmonster\'
      and env = \'sc\'
    '''
    db = dbutils.DataBase(host='dbtool01s.daodao.com')
    v_hostname = db.query(sql)
    return v_hostname

####################
# 在sync01s 执行命令
####################
def ExecRemoteHost(func):
    def wrapper(*args, **kwargs):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('sync01s.daodao.com', 22, timeout=20)
            command = func(*args, **kwargs)
            stdin, stdout, stderr = ssh.exec_command(command)
            result = stdout.readlines()
            error = stderr.readlines()
            return result , error
        except Exception as e:
            return e
        finally:
            ssh.close()
    return wrapper

# SQL
@ExecRemoteHost
def execSchemaChangeRomteCommand(host, dbname, sql):
    command = '''psql -U %s -d %s -h %s -c "%s" ''' % (dbname, dbname, host, sql)
    return command

####################
# 执行schema change
# 1. 判断env
# 2. 根据dbname找到host
# 3. 执行
####################

def execSchemaChange(env, dbname, sql):
    if dbname == 'tripmonster':
        hosts = getTMHostFromTool()
    else:
        hosts = getHostFromDbName(dbname,env)
    if not hosts:
        flag = False
        e = 'DB %s is not exist! ' % dbname
        yield flag, e
    else:
        if env == 'live':
            for host in hosts:
                # 如果是 live 就在 sync01s 执行
                result , error = execSchemaChangeRomteCommand(host[0], dbname, sql)
                yield result, error
        else:
            for host in hosts:
                db = dbutils.DataBase(host=host[0], database=dbname, user=dbname)
                flag, e = db.update(sql)
                yield flag, e


####################
# 执行Create
# 1. 确定表是否存在
# 2. 根据dbname,table 找到需要执行的主机执行
####################
@ExecRemoteHost
def checkTableIsExistCommand(host, dbname, table):
    command = '''psql -U %s -d %s -h %s -Aqtc "select count(*) from pg_tables where tablename = \'%s\';" 
    ''' % (dbname, dbname, host, table)
    return command

@ExecRemoteHost
def createPgSyncTriggerOnTableCommand(host, dbname, table):
    command = '''psql -U %s -d %s -h %s -Aqtc "select dbmirror_create_repl_trigger(\'%s\');"
    ''' % (dbname, dbname, host, table)
    return command

def createSyncTrigger(dbname, table):
    exec_hosts = []
    hosts_live = getHostFromDbName(dbname,'live')
    hosts_s = getHostFromDbName(dbname,'sc')
    sql = ''' select dbmirror_create_repl_trigger(\'%s\') ''' % table
    for host in hosts_live:
        if checkTableIsExistCommand(host, dbname, table):
            createPgSyncTriggerOnTableCommand(host[0], dbname, table)
            exec_hosts.append(host[0])
        else:
            continue
    if checkTableIsExistCommand(hosts_s, dbname, table):
        createPgSyncTriggerOnTableCommand(hosts_s[0][0], dbname, table)
        exec_hosts.append(hosts_s[0][0])
    return exec_hosts
