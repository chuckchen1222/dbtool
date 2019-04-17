from django.shortcuts import render,redirect

# Create your views here.

"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190327
"""
import json
from login.functions.islogin import isLogin
from .functions import queryutils
from .forms import QueryForms, OtherQueryForms
from logexec.models import ExecLogging

@isLogin
def query(request):
    error = []    
    sql_explain = []
    username = 'dbadmin'
    if request.method == "POST":
        query_form = QueryForms(request.POST)
        if query_form.is_valid():
            dbname = query_form.cleaned_data['dbname']
            env = query_form.cleaned_data['env']
            sql = query_form.cleaned_data['sql']
            is_explain = query_form.cleaned_data['is_explain']
            if dbname == 'ddmonster':
                host = 'tm01c'
                username = 'ddmonster'
            elif env == '3' and 'ros' in dbname:
                host = 'dbros01s'
            elif env == '3':
                dbname = 'tripmonster'
                host = 'tm01c'
            else:
                if env == '1':
                    env = 'dev'
                elif env == '2':
                    env = 'sc'
                host = queryutils.getDestHost(dbname, env)
                if not host:
                    error.append('database "%s" does not exist' % dbname)
                    return  render(request,'sql_ops/exec_query.html',{'error': error, 'QueryForms':query_form})
            try:
                query_results,e = queryutils.pgExecSQL(host=host, port=5432, dbname=dbname, user=username, password='', sql=sql)
                if e:
                    error.append(e[0])
                    return  render(request,'sql_ops/exec_query.html',{'error': error, 'QueryForms':query_form})
            except Exception as e:
                error.append(e)
                return  render(request,'sql_ops/exec_query.html',{'error': error, 'QueryForms':query_form})
            is_explain = request.POST['is_explain']
            if is_explain:
                try:
                    sql_explain,e = queryutils.pgSQLexplain(host=host, port=5432, dbname=dbname, user=username, password='', sql=sql)
                    if e:
                        error.append(e[0])
                        return  render(request,'sql_ops/exec_query.html',{'error': error})
                except Exception as e:
                    error.append(e)
                    return  render(request,'sql_ops/exec_query.html',{'error': error})
            ExecLogging.objects.create(user=request.session['user_name'], exec_command=json.dumps({ 'env': env , 'dbname': dbname, 'query': sql }))
            context = { "QueryForms": query_form, "host": host ,"dbname": dbname , "query": sql , "query_results":query_results, "sql_explain": sql_explain}
            return render(request, 'sql_ops/exec_query.html', context)
    query_form = QueryForms()
    return render(request, 'sql_ops/exec_query.html', {'QueryForms':query_form})

@isLogin
def otherDBQuery(request):
    error = []
    if request.method == "POST":
        forms = OtherQueryForms(request.POST)
        if forms.is_valid():
            dbtype = forms.cleaned_data['dbtype']
            hostname = forms.cleaned_data['hostname']
            port = forms.cleaned_data['port']
            dbname = forms.cleaned_data['dbname']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            sql = forms.cleaned_data['sql']
            if dbtype == '1':
                try:
                    query_results,e = queryutils.pgExecSQL(host=hostname, port=port, dbname=dbname, user=username, password=password, sql=sql)
                    if e:
                        error.append(e[0])
                        return render(request,'sql_ops/anydbquery.html',{'error': error, 'forms': forms})
                except Exception as e:
                    error.append(e)
                    return render(request,'sql_ops/anydbquery.html',{'error': error, 'forms': forms})
            elif dbtype == '2':
                try:
                    query_results,e = queryutils.MySQLExecSQL(host=hostname, port=int(port), dbname=dbname, user=username, password=password, sql=sql)
                    if e:
                        error.append(e[0])
                        return  render(request,'sql_ops/anydbquery.html',{'error': error, 'forms': forms})
                except Exception as e:
                    error.append(e)
                    return render(request,'sql_ops/anydbquery.html',{'error': error, 'forms': forms})
            elif dbtype == '3':
                try:
                    query_results,e = queryutils.MSSQLExecSQL(server=hostname, dbname=dbname, user=username, password=password, sql=sql)
                    if e:
                        error.append(e[0])
                        return  render(request,'sql_ops/anydbquery.html',{'error': error, 'forms': forms})
                except Exception as e:
                    error.append(e)
                    return render(request,'sql_ops/anydbquery.html',{'error': error, 'forms': forms})
            ExecLogging.objects.create(user=request.session['user_name'], exec_command=json.dumps({ 'dbtype': dbtype , "hostname": hostname, "port": port, 'dbname': dbname, 'query': sql }))
            context = {"forms": forms ,"dbtype": dbtype, "hostname": hostname, "port": port, "dbname": dbname, "query":sql, "query_results": query_results, "error": error }
            return render(request,'sql_ops/anydbquery.html',context)
    forms = OtherQueryForms()
    return render(request, 'sql_ops/anydbquery.html', {'forms': forms})
