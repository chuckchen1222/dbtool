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
from .forms import liveExecuteDML

# Create your views here.

@isLogin
def liveExecDML(request):
    error = []
    res = []
    exec_sql = []
    if request.method == "POST":
        forms = liveExecuteDML(request.POST)
        user = request.session['user_name']
        if user not in ('sli', 'bcui', 'fkang', 'chzhang'):
            error.append('Permission Deny!')
            context = { 'error': error, 'forms': forms}
            return render(request, 'ros_ops/roslist.html', context)
        if forms.is_valid():
            dbname = forms.cleaned_data['dbname']
            sql = forms.cleaned_data['sql']
        hostname = execdml.getLiveDBHost(dbname)
        if hostname:
            hostname = hostname[0][0]
        else:
            error.append('You can\'t execute DML in this DB.')
            return render(request, 'dmlsql_ops/liveexecdml.html',{'forms': forms, 'error':error})
        sql = sql.split(';')
        for s_sql in sql:
            if not s_sql:
                continue
            results = execdml.execSchemaChangeRomteCommand(hostname, dbname, s_sql)
            for command in results:
                if command[1]:
                    error.append(command[1][0])
                    error.append('''Please Check you SQL.
1. The "where" clause must exist in the SQL.
2. Check the table name is correct.
3. Check the column name is correct.
4. Check SQL is correct.
5. Don't TRUNCATE !!!''')
                else:
                    exec_sql.append(s_sql)
                    res.append(command[0])
                ExecLogging.objects.create(user=request.session['user_name'], 
                        exec_command=json.dumps({'dbname': dbname, 'sql': s_sql , 'result': command }))
        context = {'forms': forms, 'result': res, 'hostname':hostname, 'error': error}
        return render(request, 'dmlsql_ops/liveexecdml.html',context)
            
    else:
       forms =  liveExecuteDML()
       return render(request, 'dmlsql_ops/liveexecdml.html',{'forms': forms})