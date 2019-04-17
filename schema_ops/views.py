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
from .models import dbwSchemaChange, dbrSchemaChange, rosSchemaChange, TableSyncTrigger

@isLogin
def dbwSchemaChange(request):
    if request.method == "POST":
        if user not in ('sli', 'bcui', 'fkang', 'chzhang'):
            error.append('Permission Deny!')
            context = { 'allros': allros, 'roslist': roslist, 'error': error}
            return render(request, 'ros_ops/roslist.html', context)
        context = {}
        return render(request, 'schema_ops/dbrschemachange.html', context)
    forms = dbwSchemaChange()
    return render(request, 'schema_ops/dbwschemachange.html', {'forms': forms})

@isLogin
def dbrSchemaChange(request):
    if request.method == "POST":
        if user not in ('sli', 'bcui', 'fkang', 'chzhang'):
            error.append('Permission Deny!')
            context = { 'allros': allros, 'roslist': roslist, 'error': error}
            return render(request, 'ros_ops/roslist.html', context)
        context = {}
        return render(request, 'schema_ops/dbrschemachange.html', context)
    return render(request, 'schema_ops/dbrschemachange.html', {'forms': forms})

@isLogin
def rosSchemaChange(request):
    if request.method == "POST":
        if user not in ('sli', 'bcui', 'fkang', 'chzhang'):
            error.append('Permission Deny!')
            context = { 'allros': allros, 'roslist': roslist, 'error': error}
            return render(request, 'ros_ops/roslist.html', context)
        context = {}
        return render(request, 'schema_ops/dbrschemachange.html', context)

    return render(request, 'schema_ops/dbrschemachange.html', {'forms': forms})
