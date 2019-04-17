from django.shortcuts import render,redirect

# Create your views here.
"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190320
"""
from table_ops.models import Tables
from .models import Database,Host
from login.functions.islogin import isLogin

@isLogin
def dbList(request):
    dblist = Database.objects.all().order_by('v_hostname').order_by('dbname')
    context = { 'dblist': dblist }
    return render(request, 'db_ops/dblist.html', context)

def dbCreate(request):
    pass
    return render(request, 'db_ops/dbcreate.html')

def dbSchemaInit(request):
    pass
    return render(request, 'db_ops/dbschemainit.html')

def dbDrop(request):
    pass
    return render(request, 'db_ops/dbdrop.html')

@isLogin
def DBTableList(request, servername, dbname):
    dbid = Database.objects.filter(v_hostname = servername).filter(dbname = dbname).values_list("id")
    tablelist = Tables.objects.filter(db_id = dbid[0][0]).order_by('table_name')
    context = { 'servername': servername, 'dbname': dbname, 'tablelist': tablelist }
    return render(request, 'db_ops/dbtablelist.html', context)


