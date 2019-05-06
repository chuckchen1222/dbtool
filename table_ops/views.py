from django.shortcuts import render,redirect

# Create your views here.
"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190322
"""
from login.functions.islogin import isLogin
from .models import Tables, Columns
from db_ops.models import Database,Host

@isLogin
def tableColList(request, servername, dbname, tablename):
    dbid = Database.objects.filter(v_hostname = servername).filter(dbname = dbname).values_list("id")
    tableid = Tables.objects.filter(db_id = dbid[0][0]).filter(table_name = tablename).values_list("id")
    collist = Columns.objects.filter(table_id_id = tableid[0][0]).order_by('id')
    context = { 'servername': servername, 'dbname': dbname, 'tablename': tablename, 'collist': collist }
    return render(request, 'table_ops/tablecollist.html', context)

@isLogin
def tableSearch(request):
    error = []
    if request.method == "POST":
        tablename = request.POST.get('tablename')
        if not tablename:
            error.append('Please enter a search term.')
            return render(request,'table_ops/tablesearch.html',{'error': error})
        elif len(tablename) > 80:
            error.append('This input tablename is too lang.')
            return render(request,'table_ops/tablesearch.html',{'error': error})
        elif len(tablename) <= 2:
            error.append('This input tablename is too short.')
            return render(request,'table_ops/tablesearch.html',{'error': error})
        else:
            tablenames = Tables.objects.filter(table_name__icontains=tablename)
            context = { 'tablenames': tablenames }
            return render(request,'table_ops/tablesearch.html', context)
    return render(request,'table_ops/tablesearch.html')

@isLogin
def tableList(request):
    tablenames = Tables.objects.all().order_by('db_id')
    context = { 'tablenames': tablenames }
    return render(request,'table_ops/tablelist.html', context)
