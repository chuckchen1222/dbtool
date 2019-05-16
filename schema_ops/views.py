from django.shortcuts import render

# Create your views here.

"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190327
"""

import json
from libs import dbutils

from login.functions.islogin import isLogin
from logexec.models import ExecLogging
from .forms import DbwSchemaChange, DbrSchemaChange, RosDDSchemaChange, TableSyncTrigger
from .functions import schemachange

@isLogin
def dbwSchemaChange(request):
    error = []
    success_env = []
    failed_env = []
    if request.method == "POST":
        forms = DbwSchemaChange(request.POST)
        user = request.session['user_name']
        if user not in ('sli', 'bcui', 'fkang', 'chzhang'):
            error.append('Permission Deny!')
            context = { 'error': error, 'forms': forms}
            return render(request, 'schema_ops/dbwschemachange.html', context)
        if forms.is_valid():
            env = forms.cleaned_data['env']
            dbname = forms.cleaned_data['dbname']
            sql = forms.cleaned_data['sql']
            if env == '1':
                exec_env = ['dev','sc','live']
            elif env == '2':
                exec_env = ['live']
            elif env == '3':
                exec_env = ['sc','dev']
            for env_t in exec_env:
                try:
                    for flag, e in schemachange.execSchemaChange(env_t, dbname, sql):
                        if flag:
                            success_env.append(env_t)
                        else:
                            failed_env.append([env_t,e])
                        ExecLogging.objects.create(user=request.session['user_name'], 
                            exec_command=json.dumps({ 'env':env_t, 'dbname': dbname, 'sql': sql ,'is_success': flag}))
                except Exception as e:
                    error.append(e)
            if env == '1' or env == '2':
                if dbname not in ['tripmaster_pii','tripmaster_booking','tripmaster_secure','tripmaster_auth']:
                    try:
                        for flag, e in schemachange.execSchemaChange('sc','tripmonster', sql):
                            if flag:
                                success_env.append('tripmonster')
                            else:
                                failed_env.append(['tripmonster',e])
                            ExecLogging.objects.create(user=request.session['user_name'], 
                                exec_command=json.dumps({ 'env':'tripmonster', 'dbname': dbname, 'sql': sql , 'is_success': flag}))
                    except Exception as e:
                        error.append(e)
                else:
                    pass
            context = {'forms': forms, 'success_env': success_env, 'failed_env':failed_env,'error':error }
            return render(request, 'schema_ops/dbwschemachange.html', context)
    else:
        forms = DbwSchemaChange()
        return render(request, 'schema_ops/dbwschemachange.html', {'forms': forms})

@isLogin
def createTableSyncTrigger(request):
    error = []
    if request.method == "POST":
        forms = TableSyncTrigger(request.POST)
        user = request.session['user_name']
        if user not in ('sli', 'bcui', 'fkang', 'chzhang'):
            error.append('Permission Deny!')
            context = { 'error': error, 'forms': forms}
            return render(request, 'schema_ops/createtablesynctrigger.html', context)
        if forms.is_valid():
            dbname = forms.cleaned_data['dbname']
            tablename = forms.cleaned_data['table']
            exec_hosts = schemachange.createSyncTrigger(dbname, tablename)
            context = { 'dbname': dbname, 'exec_hosts':exec_hosts ,'forms': forms }
            return render(request, 'schema_ops/createtablesynctrigger.html', context)
    else:
        forms = TableSyncTrigger()
        return render(request, 'schema_ops/createtablesynctrigger.html', {'forms': forms})

@isLogin
def dbrSchemaChange(request):
    error = []
    success_env = []
    failed_env = []
    if request.method == "POST":
        forms = DbrSchemaChange(request.POST)
        user = request.session['user_name']
        if user not in ('sli', 'bcui', 'fkang', 'chzhang'):
            error.append('Permission Deny!')
            context = { 'error': error, 'forms': forms}
            return render(request, 'schema_ops/dbrschemachange.html', context)
        if forms.is_valid():
            env = forms.cleaned_data['env']
            dbname = forms.cleaned_data['dbname']
            sql = forms.cleaned_data['sql']
            exec_env = ['dev','sc','live']
            for env_t in exec_env:
                try:
                    for flag, e in schemachange.execSchemaChange(env_t, dbname, sql):
                        if flag:
                            success_env.append(env_t)
                        else:
                            failed_env.append([env_t,e])
                        ExecLogging.objects.create(user=request.session['user_name'], 
                            exec_command=json.dumps({ 'env':env_t, 'dbname': dbname, 'sql': sql ,'is_success': flag}))
                except Exception as e:
                    error.append(e)
            try:
                for flag, e in schemachange.execSchemaChange('sc','tripmonster', sql):
                    if flag:
                        success_env.append('tripmonster')
                    else:
                        failed_env.append(['tripmonster',e])
                    ExecLogging.objects.create(user=request.session['user_name'], 
                        exec_command=json.dumps({ 'env':'tripmonster', 'dbname': dbname, 'sql': sql , 'is_success': flag}))
            except Exception as e:
                error.append(e)
            context = {'forms': forms, 'success_env': success_env, 'failed_env':failed_env,'error':error }
            return render(request, 'schema_ops/dbrschemachange.html', context)
    else:
        forms = DbrSchemaChange()
        return render(request, 'schema_ops/dbrschemachange.html', {'forms': forms})

@isLogin
def rosDDSchemaChange(request):
    error = []
    success_env = []
    failed_env = []
    if request.method == "POST":
        forms = RosDDSchemaChange(request.POST)
        user = request.session['user_name']
        if user not in ('sli', 'bcui', 'fkang', 'chzhang'):
            error.append('Permission Deny!')
            context = { 'error': error, 'forms': forms}
            return render(request, 'schema_ops/rosddschemachange.html', context)
        if forms.is_valid():
            env = forms.cleaned_data['env']
            dbname = forms.cleaned_data['dbname']
            sql = forms.cleaned_data['sql']
            if env == '1':
                exec_env = ['dev','sc']
            elif env == '2':
                exec_env = ['sc']  # 取sc的机器， 只执行在dbros01s中
            elif env == '3': 
                exec_env = ['sc','dev'] # 取sc的机器，但不包括 dbros01s
            for env_t in exec_env:
                try:
                    for flag, e in schemachange.execSchemaChange(env_t, dbname, sql):
                        if flag:
                            success_env.append(env_t)
                        else:
                            failed_env.append([env_t,e])
                        ExecLogging.objects.create(user=request.session['user_name'], 
                            exec_command=json.dumps({ 'env':env_t, 'dbname': dbname, 'sql': sql ,'is_success': flag}))
                except Exception as e:
                    error.append(e)
            context = {'forms': forms, 'success_env': success_env, 'failed_env':failed_env,'error':error }
            return render(request, 'schema_ops/rosddschemachange.html', context)
    else:
        forms = RosDDSchemaChange()
        return render(request, 'schema_ops/rosddschemachange.html', {'forms': forms})
