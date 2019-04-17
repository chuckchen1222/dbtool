
"""
Author: chzhang@tripadvisor.com
Date: 2019-04-02
Version: 20190411
"""
from libs import dbutils
import time
# got Ros DB List
def getAllRosList():
    sql = ''' select dbname, enabled from t_ros_db order by enabled desc
    '''
    db = dbutils.DataBase(host='dbwvm01as.daodao.com', database='ros_admin', user='ros_admin', password = '', port=5432)
    roslist = db.query(sql)
    return roslist


def getRosStatus(dbname):
    sql = ''' select state from t_ros_admin_status
    where rosname = \'%s\'
      and eventtime = (select max(eventtime) from t_ros_admin_status where rosname = \'%s\');
    ''' % (dbname, dbname)
    db = dbutils.DataBase(host='dbwvm01as.daodao.com', database='ros_admin', user='ros_admin', password = '', port=5432)
    rosstatus = db.query(sql)
    status = rosstatus[0][0]
    return status


# dump completed: ALL_COMPLETED
# restore completed: DB_RENAMING_COMPLETED
def getRosStatusDone(dbname):
    status = getRosStatus(dbname)
    while not (status in ('ALL_COMPLETED' , 'DB_RENAMING_COMPLETED') or 'FAILED' in status):
        time.sleep(10)
        status = getRosStatus(dbname)
        yield '0'
    return '1'

 
def allROSInfo():
    allros = []
    roslist = getAllRosList()
    for dbname in roslist:
        if dbname[1]:
            ros = []
            ros.append(dbname[0])
            ros.append(dbname[1])
            ros.append(getRosStatus(dbname[0]))
            allros.append(ros)
    return allros

