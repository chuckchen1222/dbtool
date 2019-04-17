#!/usr/bin/python
# coding: utf-8

"""
Author: chzhang@tripadvisor.com
Date: 2019-04-04
Version: 20190416
"""
########################################
# 
# 收集所有数据库的信息。将信息插入到tools DB。
# 根据Host，收集DB。根据DB收集Table。根据Table收集column。
# ™
# 
########################################
from dbutils import DataBase
import logging

####################
# 日志初始化
####################
logfile = '/home/site/dbops/collector.log'
logger = logging.getLogger('[Collect-DB]')
logger.setLevel(logging.INFO)  
handler = logging.FileHandler(logfile, mode='a')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

####################
# 对主机操作
# 1. 对tool DB进行查询
# 2. 对 tool DB进行DML
# 3. 查询所有主机名
# 4. 查询v_hostname
# *5. 更改主机是否为primary
# 6. truncate 表，重置sequence，为了插入新的信息.
####################
# 对tool DB进行查询
def queryInfoFromOps(sql):
    db = DataBase(host='dbtool01s.daodao.com',database='tripmaster_dbtool', user='dbadmin', password='',port=5432)
    result = db.query(sql)
    return result 

# 对 tool DB 进行DML
def updateInfoToOps(sql):
    db = DataBase(host='dbtool01s.daodao.com',database='tripmaster_dbtool', user='dbadmin', password='',port=5432)
    db.update(sql)

# 查 full_hostname 列表
def getAllDBHostName():
    sql = '''SELECT full_hostname FROM db_ops_host 
    WHERE short_hostname NOT IN (\'dbw01mc\',\'dbr01mc\') 
    '''
    f_hosts = queryInfoFromOps(sql)
    return f_hosts

# 查 v_hostname 列表(主备只取其一)
def getVDBHostName():
    sql = '''SELECT DISTINCT v_hostname FROM db_ops_host 
    WHERE short_hostname NOT IN (\'dbw01mc\',\'dbr01mc\',\'sync03s\') 
    '''
    v_hosts = queryInfoFromOps(sql)
    return v_hosts

# 更改主机是否为primary
def updateServerIsPrimary():
    for f_host in getAllDBHostName():
        try:
            hostname = f_host[0]
            sql = 'SELECT pg_is_in_recovery();'
            # primary
            u_sql_p = 'UPDATE db_ops_host SET is_master = true WHERE full_hostname = \'%s\'' % hostname
            # slave
            u_sql_s = 'UPDATE db_ops_host SET is_master = false WHERE full_hostname = \'%s\'' % hostname
            db = DataBase(host=hostname,database='postgres', user='dbadmin', password='',port=5432)
            result = db.query(sql)
            if result[0][0] == False:
                updateInfoToOps(u_sql_p)
            else:
                updateInfoToOps(u_sql_s)
        except Exception as e:
            logger.error('updateServerIsPrimary error: hostname: ' + hostname + ' , exception: ' + str(e))
    updateInfoToOps('CLUSTER db_ops_host USING db_ops_host_pkey;')

# truncate table
def truncOpsTable(tablename):
    sql = 'TRUNCATE TABLE %s CASCADE; ' % tablename
    updateInfoToOps(sql)

# reset sequence
def resetOpsSequence(sequencename):
    sql = 'ALTER SEQUENCE %s RESTART 1;' % sequencename
    updateInfoToOps(sql)

####################
# 对数据库进行操作
# 1. 查询数据库名称,
# 2. 查询数据库信息（size, topology, env, is_sync, pgsync mode）
# *3. 将查询到的数据库信息插入到tool DB
####################

# 查询一个host中所有的DB名
def getAllDBNameFromServer(host):
    sql = 'SELECT datname FROM pg_database WHERE datname NOT IN (\'template0\',\'template1\',\'postgres\')'
    db = DataBase(host=host,database='postgres', user='dbadmin', password='',port=5432)
    dbs = db.query(sql)
    return dbs

# 查询数据库的大小
def getDBSizeFromServer(host,dbname):
    sql = 'SELECT pg_size_pretty(pg_database_size(\'%s\'))' % dbname
    db = DataBase(host=host,database=dbname, user='dbadmin', password='',port=5432)
    dbsize = db.query(sql)
    return dbsize[0][0]

# 获取数据库topology
def getDBTopology(dbname):
    dbr = ('tripmaster','commerce','tripmaster_foreign_member','menus_rws','foreign_member_profile','tripmaster_daodao')
    if 'ros' in dbname:
        topology = 'ros'
    elif dbname in dbr:
        topology = 'dbr'
    else:
        topology = 'dbw'
    return topology

# 获取数据库ENV
def getEnvFromHostname(v_host):
    sql = 'SELECT dc_id_id FROM db_ops_host WHERE v_hostname = \'%s\'' % v_host
    dcid = queryInfoFromOps(sql)
    if dcid[0][0] == 1 or dcid[0][0] == 2:
        return 'live'
    elif dcid[0][0] == 3:
        return 'sc'
    elif dcid[0][0] == 4:
        return 'dev'

def getDBIsPgSync(host,dbname):
    sql_pgsync_tables = 'SELECT count(*) FROM pg_tables WHERE tablename LIKE \'dbmirror%\'; '
    sql_slave_count = 'SELECT count(*) FROM dbmirror_mirrorhost; '
    db = DataBase(host=host,database=dbname, user='dbadmin', password='',port=5432)
    pgsync_tables = db.query(sql_pgsync_tables)
    if pgsync_tables[0][0]:
        slave_count = db.query(sql_slave_count)
        if slave_count[0][0]:
            return True
        else:
            return False
    else:
        return False

# 获取pgsync mode
def getPgSyncMode(host,dbname):
    sql = 'SELECT replication_mode FROM dbmirror_mode;'
    db = DataBase(host=host,database=dbname, user='dbadmin', password='',port=5432)
    pgsyncmode = db.query(sql)
    return pgsyncmode[0][0]

# 插入DB 信息到 tool DB
def InsertDBInfoToOps():
    # truncate table, reset sequence
    truncOpsTable('db_ops_database')
    resetOpsSequence('db_ops_database_id_seq')
    # resetOpsSequence('table_ops_tables_id_seq')
    # resetOpsSequence('table_ops_columns_id_seq')
    for v_host in getVDBHostName():
        host = v_host[0]
        dbnames = getAllDBNameFromServer(host)
        for dbname in dbnames:
            try:
                dbname = dbname[0]
                dbsize = getDBSizeFromServer(host,dbname)
                env = getEnvFromHostname(host)
                topology = getDBTopology(dbname)
                is_pgsync = getDBIsPgSync(host,dbname)
                if is_pgsync:
                    syncmode = getPgSyncMode(host,dbname)
                else:
                    syncmode = ''
                sql = '''INSERT INTO db_ops_database(dbname, port, dbsize, env, topology, v_hostname, is_pgsync, pgsync_mode)
                VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')
                ''' % (dbname, 5432, dbsize, env, topology, host, is_pgsync, syncmode)
                updateInfoToOps(sql)
            except Exception as e:
                logger.error('InsertDBInfoToOps error: hostname: ' + hostname + ' , dbname' + dbname + '  , exception: ' + str(e))


####################
# 对表进行操作
# 1. 查询表名称,schema
# 2. 查询表信息（size, topology, env, is_sync, pgsync mode）
# *3. 将查询到的表信息插入到tool DB
####################
# 获取db_ops_database 表中数据库的 id, v_hostname, dbname
def getDBInfoFromToolDB():
    toolsdb = DataBase(host = 'dbtool01s',database = 'tripmaster_dbtool')
    sql_dbinfo = '''SELECT v_hostname, dbname, id FROM db_ops_database 
    WHERE dbname NOT IN (\'daodao_hedwig_hive_metastore\', \'daodao_swedwig_hive_metastore\',\'tripmaster_test\',\'kv1\',\'kv2\',\'kv3\',\'kv4\',\'kv5\',\'kv6\',\'kv7\',\'kv8\',\'kv9\',\'kv10\',\'kv11\',\'kv12\')
    ORDER BY id; '''
    dbsinfo = toolsdb.query(sql_dbinfo)
    return dbsinfo

# 从各数据库中获取表名称
def getTableNameFromDB(db):
    sql_tablenames = '''SELECT schemaname, tablename FROM pg_tables 
    WHERE schemaname NOT IN (\'pg_catalog\' , \'information_schema\', \'dbmirror\', \'debug\',\'MySchema\') and schemaname not like \'pg_temp%\' and tablename not like \'dbmirror%\' 
      AND tablename NOT IN (\'AA-926 CtripTA_DomesticHotelInfo\',\'daodao_ibdm_2016-06-21\',\'shipan_exported_winners_tc_Hotels2015_China\',\'AA989 Alitrip Listing Match\',\'temp_Jinling_hotel_taid\',
      \'AppStoreCampaigns_xiaofei\',\'DD-7521-TC 2015 All Category\',\'DD-7521TCH 2016 Winner list final 011216\',\'clickable type\',\'Jingyi_country_location\',\'IX_mcid_group_mcid\',\'target_2017_copy_H2\',
      \'target_2017_copy_H2V3\',\'target_2017_copy_H2V5\',\'target_2017_copy_20170721_H1\',\'target_2017_copy_H2V2\',\'target_2017_copy_H2V4\',\'temp_Ctrip_hotel_AA1677\',\'bd  landingpage\',\'temp_TC_2019_clubmed\',
      \'temp_TC_2019_China\', \'TopShopsPergeo\')
      AND tablename NOT LIKE \'tmp_%%%\' 
      AND tablename NOT LIKE \'temp_%%%\'
      '''
    tables = db.query(sql_tablenames)
    return tables

def getTableSizeFromDB(db, schemaname, tablename):
    sql_tablesize = 'SELECT pg_size_pretty(pg_relation_size(\'%s.%s\'));' % (schemaname, tablename)
    tablesize = db.query(sql_tablesize)
    return tablesize[0][0]

def getTableRowsFromDB(db, schemaname, tablename):
    sql_tablerows = 'SELECT n_live_tup FROM pg_stat_user_tables WHERE schemaname = \'%s\' AND relname = \'%s\' ' % (schemaname,tablename)
    try:
        tablerows = db.query(sql_tablerows)
        return tablerows[0][0]
    except Exception as e:
        logger.error('tablename: ' + tablename + ' , exception: ' + str(e))
        return 0

def getTableTriggerNumFromDB(db, schemaname, tablename):
    sql_triggernum = 'SELECT count(*) FROM information_schema.triggers WHERE event_object_table = \'%s\' AND action_statement = \'EXECUTE PROCEDURE recordchange()\' ' % tablename
    triggernum = db.query(sql_triggernum)
    if triggernum >= 3:
        is_sync = 't'
    else:
        is_sync = 'f'
    return is_sync

def getTableAnylyzeVacuum(db, schemaname, tablename):
    sql_anylyze_vacuum = 'SELECT last_autoanalyze,last_vacuum FROM pg_stat_all_tables WHERE relname = \'%s\' ' % tablename
    try:
        table_analyze_vacuum = db.query(sql_anylyze_vacuum)[0]
        if table_analyze_vacuum[0] is None and table_analyze_vacuum[1] is not None:
            return ('null','\'' + str(table_analyze_vacuum[1]) + '\'') 
        elif table_analyze_vacuum[0] is not None and table_analyze_vacuum[1] is None:
            return ('\'' + str(table_analyze_vacuum[0]) + '\'' , 'null')
        elif table_analyze_vacuum[0] is not None and table_analyze_vacuum[1] is not None:
            return ('\'' + str(table_analyze_vacuum[0]) + '\'' , '\'' + str(table_analyze_vacuum[1]) + '\'')
        else:
            return ('null','null')
    except Exception as e:
        logger.error('tablename: ' + tablename + ' , exception: ' + str(e))
        return ('null','null')

# env = [live, dev, sc]
def insertTableInfo():
    truncOpsTable('table_ops_tables')
    resetOpsSequence('table_ops_tables_id_seq')
    tooldb = DataBase(host = 'dbtool01s',database = 'tripmaster_dbtool')
    dbsinfo = getDBInfoFromToolDB()
    for dbinfo in dbsinfo:
        v_hostname = dbinfo[0]
        dbname = dbinfo[1]
        dbid = dbinfo[2]
        db = DataBase(host = v_hostname , database = dbname )
        tables = getTableNameFromDB(db)
        logger.info('Collect Table info in '+ v_hostname + ':' + dbname)
        for table in tables:
            try:
                tablename = table[1]
                schemaname = table[0]
                tablesize = getTableSizeFromDB(db, schemaname, tablename)
                tablerows = getTableRowsFromDB(db, schemaname, tablename)
                is_sync = getTableTriggerNumFromDB(db, schemaname, tablename)
                table_anylyze_vacuum =  getTableAnylyzeVacuum(db, schemaname, tablename)
                table_auto_anylyze = table_anylyze_vacuum[0]
                table_auto_vacuum = table_anylyze_vacuum[1]
                sql_insertinfo = '''INSERT INTO table_ops_tables(table_name , schema_name, table_size , rows_count, sync_trigger, last_analyze, last_vacuum, db_id_id) 
                VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', %s, %s, %s)
                ''' % (tablename, schemaname, tablesize, tablerows, is_sync, table_auto_anylyze, table_auto_vacuum, dbid)
                tooldb.update(sql_insertinfo)
            except Exception as e:
                logger.error('insertTableInfo error: hostname: ' + hostname + 'dbname: ' + dbname +  'tablename: ' + tablename +  ' , exception: ' + str(e))


############################################
# 对列进行操作
# 1. 查询列信息 (列名，type, comment, 是否为空,table_id)
# 2. 将查询到的列信息插入到tool DB
############################################

def getTablesInfoFromToolDB(db, dbid):
    sql_tableinfo = '''SELECT id, schema_name, table_name FROM table_ops_tables 
    WHERE db_id_id = \'%s\'
    ''' % (dbid)
    tablesinfo = db.query(sql_tableinfo)
    return tablesinfo

def getColumnsInfoFromDB(db, schemaname, tablename):
    sql_columns = ''' SELECT 
    attname AS colname,
    atttypid ::regtype AS col_type, 
    attnotnull AS is_notnull 
    FROM pg_catalog.pg_attribute 
    WHERE attrelid = \'%s.%s\'::regclass AND attnum>0 AND attisdropped = \'f\'; 
    ''' % (schemaname, tablename)
    try:
        columns = db.query(sql_columns)
        return columns
    except Exception as e:
        logger.error('tablename: ' + tablename + ' , exception: ' + str(e))
        return 0

def insertColumnInfo():
    truncOpsTable('table_ops_columns')
    resetOpsSequence('table_ops_columns_id_seq')
    tooldb = DataBase(host = 'dbtool01s',database = 'tripmaster_dbtool')
    dbsinfo = getDBInfoFromToolDB()
    for dbinfo in dbsinfo:
        v_hostname = dbinfo[0]
        dbname = dbinfo[1]
        dbid = dbinfo[2]
        tablesinfo = getTablesInfoFromToolDB(tooldb, dbid)
        logger.info('Collect Column info in ' + v_hostname + ':' + dbname)
        for table in tablesinfo:
            tableid = table[0]
            schemaname = table[1]
            tablename = table[2]
            db = DataBase(host = v_hostname , database = dbname)
            cols = getColumnsInfoFromDB(db, schemaname, tablename)
            if cols:
                for col in cols:
                    colname = col[0]
                    coltype = col[1]
                    is_notnull = col[2]
                    sql_insertinfo = ''' INSERT INTO table_ops_columns(column_name, column_type, is_notnull, table_id_id)
                    VALUES (\'%s\', \'%s\', \'%s\', \'%s\')
                    ''' % (colname, coltype, is_notnull, tableid)
                    tooldb.update(sql_insertinfo)
            else:
                logger.warning(str('Host: ' + v_hostname + ', DB: ' + dbname + ', Table: ' + tablename))


############################################
# main
############################################
def main():
    try:
        logger.info('='*68)
        logger.info('Start to Collect All DB Info...')

        logger.info('Server Pirmary...')
        updateServerIsPrimary()

        logger.info('DB Info...')
        InsertDBInfoToOps()

        logger.info('Table Info...')
        insertTableInfo()

        logger.info('Column Info...')
        insertColumnInfo()

    except Exception as e:
        logger.error(e)
    finally:
        logger.info('End.')
        logger.info('='*68)


if __name__ == "__main__":
    main()
