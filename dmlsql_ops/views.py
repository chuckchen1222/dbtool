from django.shortcuts import render
# encoding: utf-8
"""
Author: chzhang@tripadvisor.com
Date: 2019-04-29
Version: 20190429
"""

import json
from libs import dbutils

from login.functions.islogin import isLogin
from logexec.models import ExecLogging
from .functions import execdml, sqlparse
from .forms import liveExecuteDML,liveExecUploadSQLFileForm
from .models import BackupData,SqlFile,SqlExecHistory
import time

# upload file function
from .functions.uploadfile import handle_uploaded_file,readFile

# Create your views here.

SQLERROR = '''Please Check you SQL.
1. The "where" clause must exist in the SQL.
2. Check the table name is correct.
3. Check the column name is correct.
4. Check SQL is correct.
5. Don't TRUNCATE !!!'''


@isLogin
def liveExecDML(request):
    error = []
    exec_result = []
    exec_sql = []
    backupsql_id = []
    backupdata_id = ''
    if request.method == "POST":
        forms = liveExecuteDML(request.POST)
        user = request.session['user_name']
        if user not in ('sli', 'bcui', 'fkang', 'chzhang'):
            error.append('Permission Deny!')
            context = { 'error': error, 'forms': forms}
            return render(request, 'ros_ops/liveexecdml.html', context)
        if forms.is_valid():
            dbname = forms.cleaned_data['dbname']
            sql = forms.cleaned_data['sql']
        hostname = execdml.getLiveDBHost(dbname)
        if hostname:
            hostname = hostname[0][0]
        else:
            error.append('You can\'t execute DML in this DB.')
            return render(request, 'dmlsql_ops/liveexecdml.html',{'forms': forms, 'error':error})
        # Begin
        # exec backup if 
        try:
            backup_sqls = execdml.getAllBackupSQLs(sql)
            if backup_sqls:
                if backup_sqls[0] == 'error':
                    error.append(SQLERROR)
                    return render(request, 'dmlsql_ops/liveexecdml.html',{'forms': forms, 'error':error})
                else:
                    for bak_sql in backup_sqls:
                        results = execdml.execSchemaChangeRomteCommand(hostname, dbname, bak_sql)
                    # 记录backup data -> BackupData
                        for res in results:
                            if res[1]:
                                error.append('Backup Data Failed.')
                                for e in res[1]:
                                    error.append(e)
                                return render(request, 'dmlsql_ops/liveexecdml.html',{'forms': forms, 'error':error})
                            else:
                                exec_result.append('Backup Data Susscess.')
                                bd = BackupData.objects.create(dbname=dbname, exec_sql=bak_sql, back_data=res[0])
                                bd.save()
                                backupdata_id = bd.id
                                backupsql_id.append(backupdata_id)
        except Exception as e:
            error.append(SQLERROR)
            return render(request, 'dmlsql_ops/liveexecdml.html',{'forms': forms, 'error':error})
        results = execdml.execSchemaChangeRomteCommand(hostname, dbname, sql)
        for res in results:
            if res[1]:
                for err in res[1]:
                    error.append(err)
                SqlExecHistory.objects.create(dbname=dbname, execed_sql=sql,is_executed=False, exec_result=res[1])
                return render(request, 'dmlsql_ops/liveexecdml.html',{'forms': forms, 'error':error})
            else:
                # 记录执行SQL -> SqlExecHistory
                SqlExecHistory.objects.create(dbname=dbname, execed_sql=sql,is_executed=True, backupdata_ids=backupsql_id)
                if backupdata_id:
                    BackupData.objects.filter(id=backupdata_id).update(is_executed=True)
                exec_result.append('Execute DML Susscess.')
                ExecLogging.objects.create(user=request.session['user_name'], 
                        exec_command=json.dumps({'dbname': dbname, 'sql': sql , 'exec_dml': 'success' }))
        context = {'forms': forms, 'result': exec_result, 'hostname':hostname, 'error': error}
        return render(request, 'dmlsql_ops/liveexecdml.html',context)
            
    else:
       forms =  liveExecuteDML()
       return render(request, 'dmlsql_ops/liveexecdml.html',{'forms': forms})

def liveExecDMLFile(request):
    error = []    
    exec_result = []
    exec_sql = []
    backupsql_id = []
    filename = ''
    if request.method == 'POST':
        forms = liveExecUploadSQLFileForm(request.POST, request.FILES)
        user = request.session['user_name']
        if user not in ('sli', 'bcui', 'fkang', 'chzhang'):
            error.append('Permission Deny!')
            context = { 'error': error,  'forms': forms }
            return render(request, 'ros_ops/liveexecdmlsqlfile.html', context)
        if forms.is_valid():
            dbname = forms.cleaned_data['dbname']
            sqlfile = request.FILES['sqlfile']
            filename = sqlfile.name
            time_name = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
            new_filename = filename + '_' + time_name
            handle_uploaded_file(new_filename, sqlfile)
            sf = SqlFile.objects.create(dbname=dbname,filename=new_filename,file_path='/root/dbtool/dmlsql/sqlfiles/')
            sf.save()
            sqlfile_id = sf.id
            sql = readFile(new_filename)
            hostname = execdml.getLiveDBHost(dbname)
            if isinstance(sql,list):
                sql = " ".join(sql)
            if hostname:
                hostname = hostname[0][0]
            else:
                error.append('You can\'t execute DML in this DB.')
                return render(request, 'dmlsql_ops/liveexecdmlsqlfile.html',{ 'forms': forms , 'error':error})
            try:
                backup_sqls = execdml.getAllBackupSQLs(sql)
                if backup_sqls:
                    if backup_sqls[0] == 'error':
                        error.append(SQLERROR)
                        return render(request, 'dmlsql_ops/liveexecdmlsqlfile.html',{ 'forms': forms , 'error':error})
                    else:
                        for bak_sql in backup_sqls:
                            results = execdml.execSchemaChangeRomteCommand(hostname, dbname, bak_sql)
                        # 记录backup data -> BackupData
                            for res in results:
                                if res[1]:
                                    error.append('Backup Data Failed.')
                                    for e in res[1]:
                                        error.append(e)
                                    return render(request, 'dmlsql_ops/liveexecdmlsqlfile.html',{ 'forms': forms , 'error':error})
                                else:
                                    exec_result.append('Backup Data Susscess.')
                                    bd = BackupData.objects.create(dbname=dbname, exec_sql=bak_sql, back_data=res[0])
                                    bd.save()
                                    backupdata_id = bd.id
                                    backupsql_id.append(backupdata_id)
            except Exception as e:
                error.append(SQLERROR)
                return render(request, 'dmlsql_ops/liveexecdmlsqlfile.html',{ 'forms': forms , 'error':error})
            results = execdml.execSchemaChangeRomteCommand(hostname, dbname, sql)
            for res in results:
                if res[1]:
                    for err in res[1]:
                        error.append(err)
                    SqlExecHistory.objects.create(dbname=dbname, is_executed=False, sqlfile_id = sf, exec_result=res[1])
                    return render(request, 'dmlsql_ops/liveexecdmlsqlfile.html',{ 'forms': forms , 'error':error})
                else:
                    # 记录执行SQL -> SqlExecHistory
                    SqlExecHistory.objects.create(dbname=dbname, is_executed=True, sqlfile_id = sf , backupdata_ids=backupsql_id)
                    if backupdata_id:
                        BackupData.objects.filter(id=backupdata_id).update(is_executed=True)
                    if sqlfile_id:
                        SqlFile.objects.filter(id=sqlfile_id).update(is_executed=True)
                    exec_result.append('Execute DML Susscess.')
                    ExecLogging.objects.create(user=request.session['user_name'], 
                            exec_command=json.dumps({'dbname': dbname, 'sqlfile_id': sqlfile_id , 'exec_dml': 'success' }))
            context = { 'forms': forms , 'result': exec_result, 'hostname':hostname, 'error': error, 'sqlfile': sql}
            return render(request, 'dmlsql_ops/liveexecdmlsqlfile.html',context)
    else:
        forms =  liveExecUploadSQLFileForm()
    return render(request, 'dmlsql_ops/liveexecdmlsqlfile.html',{ 'forms': forms })
